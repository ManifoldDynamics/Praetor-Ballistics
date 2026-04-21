import numpy as np
import trimesh
from ballistics.terminal import TerminalBallistics
from ballistics.terminal_v2 import TerminalBallisticsV2
from ballistics.eom import quaternion_to_rotation_matrix

class LethalityResult:
    def __init__(self, target_stl_path, total_fragments, hit_count, penetration_count, penetration_mm, hit_points, penetrated_points):
        self.target_stl_path = target_stl_path
        self.total_fragments = total_fragments
        self.hit_count = hit_count
        self.penetration_count = penetration_count
        self.penetration_mm = penetration_mm
        self.hit_points = hit_points # Nx3 numpy array
        self.penetrated_points = penetrated_points # Mx3 numpy array

class LethalityRayTracer:
    """
    Uses trimesh ray tracing to calculate fragment impacts against a 3D STL target.
    """
    def __init__(self, target_stl_path, target_position_m, target_armor_mm=10.0):
        """
        target_stl_path: Path to the target 3D mesh file.
        target_position_m: [X, Y, Z] world coordinates where the target is located.
        target_armor_mm: Thickness of the armor on the target mesh.
        """
        self.target_stl_path = target_stl_path
        self.target_position = np.array(target_position_m)
        self.target_armor_mm = target_armor_mm

        # Load mesh and translate it to the target position
        self.mesh = trimesh.load(target_stl_path)

        # Determine center of the loaded mesh's bounding box and move it to target_position
        center = self.mesh.bounding_box.centroid
        translation = self.target_position - center
        self.mesh.apply_translation(translation)

    def analyze_lethality(self, explosion_pos_m, projectile_vel_m_s, projectile_quat,
                          fragment_mass_kg, fragment_diam_m, fragment_spray_vectors_body, version=1, fragment_masses_v2=None, terrain=None):
        """
        Ray traces fragments from the explosion position against the target mesh.
        Returns a LethalityResult.
        """
        from ballistics.lethality_v2 import FragmentationModelV2
        from ballistics.terrain_v2 import TerrainModelV2
        # Ensure numpy arrays
        explosion_pos = np.array(explosion_pos_m)
        proj_vel = np.array(projectile_vel_m_s)

        num_fragments = len(fragment_spray_vectors_body)

        # Convert spray vectors from body frame to Earth frame
        # The quaternion defines Body -> Earth rotation
        R_b2e = quaternion_to_rotation_matrix(projectile_quat)
        spray_vectors_earth = np.dot(R_b2e, fragment_spray_vectors_body.T).T

        # Add the projectile's forward velocity to every fragment vector
        # This accurately models forward momentum during detonation
        total_frag_velocities = spray_vectors_earth + proj_vel

        # Ray tracing requires origins (Nx3) and direction vectors (Nx3)
        origins = np.tile(explosion_pos, (num_fragments, 1))

        # Directions are simply the normalized velocity vectors
        directions = np.copy(total_frag_velocities)
        speeds = np.linalg.norm(directions, axis=1)

        # Avoid div by zero for any static fragments
        nonzero = speeds > 0.0
        directions[nonzero] = directions[nonzero] / speeds[nonzero, np.newaxis]

        # V2: Rigorous Obstruction Check (Distance-Sorted Occlusion)
        # Fragments are only blocked if the terrain intersection is closer than the target intersection
        blocked_rays = set()
        if version == 2 and terrain is not None and terrain.mesh is not None:
            # 1. Get all intersections with the target mesh
            locs_target, idx_target, _ = self.mesh.ray.intersects_location(origins, directions)
            dist_target = {idx: np.linalg.norm(loc - origins[idx]) for loc, idx in zip(locs_target, idx_target)}

            # 2. Get intersections with terrain
            t_locs, t_idx_ray, _ = terrain.mesh.ray.intersects_location(origins, directions)

            for i, ray_idx in enumerate(t_idx_ray):
                d_terrain = np.linalg.norm(t_locs[i] - origins[ray_idx])
                d_target = dist_target.get(ray_idx, float('inf'))

                if d_terrain < d_target:
                    blocked_rays.add(ray_idx) # Terrain is in front of the target

        # Perform ray intersection using trimesh
        # 'intersects_location' returns:
        # locations: The (M, 3) point of intersection.
        # index_ray: The (M,) index of the ray that hit.
        # index_tri: The (M,) index of the triangle that was hit.
        locations, index_ray, index_tri = self.mesh.ray.intersects_location(
            ray_origins=origins,
            ray_directions=directions,
            multiple_hits=False # Only care about the first impact surface
        )

        hit_count = len(index_ray)
        penetration_count = 0
        penetrated_points = []
        hit_points = []

        # V2: Secondary Fragmentation (Ground Splash)
        if version == 2 and terrain is not None:
            # Check if any fragments hit the terrain
            t_locs, t_idx_ray, _ = terrain.mesh.ray.intersects_location(origins, directions) if terrain.mesh else ([], [], [])

            # If we don't have a terrain mesh, check for Z=0 intersection
            if terrain.mesh is None:
                # Find rays going down
                down = directions[:, 2] < 0
                if np.any(down):
                    # t = -z0 / vz
                    t_ground = -origins[down, 2] / directions[down, 2]
                    t_ground_locs = origins[down] + directions[down] * t_ground[:, np.newaxis]
                    t_idx_ray = np.where(down)[0]
                    t_locs = t_ground_locs

            secondary_origins = []
            secondary_directions = []
            secondary_masses = []

            for i, ray_idx in enumerate(t_idx_ray):
                # Only splash if it hits ground far from target? No, any ground hit can splash.
                impact_vel = directions[ray_idx] * speeds[ray_idx]
                splash = terrain.calculate_secondary_splash(t_locs[i], impact_vel, fragment_mass_kg)
                for v_s, m_s in splash:
                    secondary_origins.append(t_locs[i])
                    secondary_directions.append(v_s / np.linalg.norm(v_s))
                    secondary_directions[-1] = secondary_directions[-1] # Normalized
                    secondary_masses.append(m_s)

            if secondary_origins:
                # Trace secondary fragments
                s_locs, s_idx_ray, _ = self.mesh.ray.intersects_location(
                    ray_origins=np.array(secondary_origins),
                    ray_directions=np.array(secondary_directions),
                    multiple_hits=False
                )

                # Process secondary hits
                for i, s_ray_idx in enumerate(s_idx_ray):
                    hit_points.append(s_locs[i])
                    # Secondary fragments are usually less lethal
                    # but we count them as hits
                    # penetration_count += 0 # Typically don't penetrate heavy armor
                    # hit_count += 1

        if hit_count > 0:
            for i, ray_idx in enumerate(index_ray):
                if ray_idx in blocked_rays:
                    continue # Fragment was shadowed by terrain

                loc = locations[i]
                hit_points.append(loc)

                # Calculate Terminal Velocity of this fragment
                frag_speed = speeds[ray_idx]

                # Determine fragment properties for this ray
                curr_mass = fragment_mass_kg
                curr_diam = fragment_diam_m
                if version == 2 and fragment_masses_v2 is not None:
                    curr_mass = fragment_masses_v2[ray_idx]
                    _, curr_diam = FragmentationModelV2.get_fragment_properties(curr_mass)

                # Apply Penetration Logic
                if version == 2:
                    # V2 logic: Thor and multi-layer simulation
                    layers = [{'thickness_mm': self.target_armor_mm, 'material': 'RHA', 'type': 'rha'}]
                    res_v2 = TerminalBallisticsV2.multi_layer_penetration(frag_speed, curr_mass, curr_diam, layers)
                    is_penetrated = res_v2['success']
                    pen_mm = self.target_armor_mm if is_penetrated else 0.0 # simplified for result
                else:
                    # V1 logic: De Marre
                    pen_mm = TerminalBallistics.demarre(frag_speed, curr_mass, curr_diam, armor_constant=1.0)
                    is_penetrated = pen_mm >= self.target_armor_mm

                if is_penetrated:
                    penetration_count += 1
                    penetrated_points.append(loc)

        return LethalityResult(
            target_stl_path=self.target_stl_path,
            total_fragments=num_fragments,
            hit_count=hit_count,
            penetration_count=penetration_count,
            penetration_mm=0.0 if hit_count == 0 else pen_mm, # just returning the last calculated as a sample
            hit_points=np.array(hit_points),
            penetrated_points=np.array(penetrated_points)
        )
