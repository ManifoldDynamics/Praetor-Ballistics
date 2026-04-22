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
        V2.x Proprietary Material-Dependent Reflection/Absorption.
        """
        v_mag = np.linalg.norm(impact_vel)
        energy = 0.5 * impact_mass * v_mag**2

        # Ground Material Properties: [Absorption, Elasticity, Fragmentation_Threshold]
        # High absorption = soft ground (soil). High elasticity = hard ground (concrete).
        ground_params = {
            'soil':     [0.85, 0.1, 200.0],
            'rock':     [0.2, 0.6, 500.0],
            'concrete': [0.15, 0.7, 800.0],
            'water':    [0.95, 0.05, 50.0],
            'steel':    [0.05, 0.85, 2000.0]
        }

        abs_k, el_k, frag_thresh = ground_params.get(self.ground_type, [0.5, 0.3, 300.0])

        # Effective Splash Energy: E_eff = E * (1 - Absorption)
        # However, for soft ground, more energy goes into cratering than splashing.
        e_splash = energy * (1.0 - abs_k)

        # Number of secondary fragments scales with energy exceeding threshold
        if e_splash < frag_thresh:
            return []

        num_frags = int((e_splash - frag_thresh) / (frag_thresh * 0.1))
        num_frags = np.clip(num_frags, 1, 64)

        secondary_frags = []
        normal = np.array([0.0, 0.0, 1.0]) # Simplified for V2

        # Reflection Vector (perfect elastic bounce)
        v_refl = impact_vel - 2.0 * np.dot(impact_vel, normal) * normal

        for _ in range(num_frags):
            # Stochastic scattering biased by elasticity
            # Harder ground (high el_k) follows reflection vector more closely.
            rand_vec = np.random.normal(0, 1, 3)
            rand_vec[2] = abs(rand_vec[2]) # Keep above ground
            rand_vec /= np.linalg.norm(rand_vec)

            # Weighted average: Elasticity * Reflection + (1-Elasticity) * Scattering
            v_frag = el_k * (v_refl / v_mag) + (1.0 - el_k) * rand_vec
            v_frag /= np.linalg.norm(v_frag)

            # Residual velocity: proportional to elasticity and energy share
            v_resid = np.sqrt(2.0 * (e_splash / num_frags) / 0.01) * (0.5 + 0.5 * el_k)
            secondary_frags.append((v_frag * v_resid, 0.01))

        return secondary_frags
