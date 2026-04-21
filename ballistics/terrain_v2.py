import numpy as np
import trimesh

class TerrainModelV2:
    """
    Proprietary V2 Terrain-Aware Engine.
    Handles terrain intersection and secondary fragmentation (ground splash).
    """
    def __init__(self, terrain_stl_path=None, ground_type='soil'):
        self.ground_type = ground_type
        if terrain_stl_path:
            self.mesh = trimesh.load(terrain_stl_path)
            self.ray_intersector = trimesh.ray.ray_pyembree.RayMeshIntersector(self.mesh)
        else:
            self.mesh = None
            self.ray_intersector = None

    def get_elevation(self, x, y):
        """Returns terrain elevation at (x, y). Defaults to 0 for flat ground."""
        if not self.ray_intersector:
            return 0.0

        # Ray cast from high up downwards
        origin = [[x, y, 10000.0]]
        direction = [[0.0, 0.0, -1.0]]
        locations, _, _ = self.ray_intersector.intersects_location(origin, direction)

        if len(locations) > 0:
            return locations[0][2]
        return 0.0

    def calculate_secondary_splash(self, impact_pos, impact_vel, impact_mass):
        """
        Calculates secondary fragments (splash) from ground impact.
        Returns a list of (velocity_vector, mass).
        """
        # Proprietary V2 Splash Logic
        # Impact energy E = 0.5 * m * v^2
        v_mag = np.linalg.norm(impact_vel)
        energy = 0.5 * impact_mass * v_mag**2

        # Ground absorption factor
        absorption = {'soil': 0.8, 'rock': 0.3, 'concrete': 0.4}.get(self.ground_type, 0.5)
        splash_energy = energy * (1.0 - absorption)

        # Number of secondary fragments depends on energy and ground type
        num_frags = int(splash_energy / 50.0) # 50J per secondary frag
        num_frags = np.clip(num_frags, 0, 50) # Limit for MVP

        secondary_frags = []
        if num_frags == 0: return []

        # Splash vectors are biased upwards and outwards from the impact normal
        # For flat ground, normal is [0, 0, 1]
        normal = np.array([0.0, 0.0, 1.0])

        for _ in range(num_frags):
            # Stochastic distribution in the upper hemisphere
            rand_vec = np.random.normal(0, 1, 3)
            rand_vec[2] = abs(rand_vec[2]) # Ensure it goes up
            rand_vec /= np.linalg.norm(rand_vec)

            # Mix with reflection vector for momentum conservation
            v_refl = impact_vel - 2 * np.dot(impact_vel, normal) * normal
            v_frag = 0.7 * rand_vec + 0.3 * (v_refl / v_mag)
            v_frag /= np.linalg.norm(v_frag)

            # Velocity magnitude based on remaining energy
            frag_v = np.sqrt(2 * (splash_energy / num_frags) / 0.01) # Assuming 10g frags
            secondary_frags.append((v_frag * frag_v, 0.01))

        return secondary_frags
