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
                          fragment_mass_kg, fragment_diam_m, fragment_spray_vectors_body, version=1):
        """
        Ray traces fragments from the explosion position against the target mesh.
        Returns a LethalityResult.
        """
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

        if hit_count > 0:
            for i, ray_idx in enumerate(index_ray):
                loc = locations[i]
                hit_points.append(loc)

                # Calculate Terminal Velocity of this fragment
                # We assume no air drag over the short distance between explosion and target for MVP
                # Distance traveled = norm(loc - origin)
                # In a real model, we would decay the speed based on drag.
                frag_speed = speeds[ray_idx]

                # Apply Penetration Logic
                if version == 2:
                    # V2 logic: Thor and multi-layer simulation
                    layers = [{'thickness_mm': self.target_armor_mm, 'material': 'RHA', 'type': 'rha'}]
                    res_v2 = TerminalBallisticsV2.multi_layer_penetration(frag_speed, fragment_mass_kg, fragment_diam_m, layers)
                    is_penetrated = res_v2['success']
                    pen_mm = self.target_armor_mm if is_penetrated else 0.0 # simplified for result
                else:
                    # V1 logic: De Marre
                    pen_mm = TerminalBallistics.demarre(frag_speed, fragment_mass_kg, fragment_diam_m, armor_constant=1.0)
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
