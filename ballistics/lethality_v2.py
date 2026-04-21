import numpy as np
from ballistics.fracture_v2 import FractureEngineV2

class FragmentationModelV2:
    """
    V2 Proprietary Fragmentation and Lethality Engine.
    Implements:
    - Mott Distribution for fragment mass frequency.
    - Advanced Gurney corrections for end-leakage and casing confinement.
    - Stochastic fragment shape factors.
    """
    @staticmethod
    def mott_distribution(total_mass, num_fragments, mott_constant):
        """
        Mott's equation for fragment distribution:
        N(m) = N0 * exp(-m^0.5 / mu)
        """
        # (Simplified proprietary stochastic sampler)
        mu = mott_constant
        masses = np.random.exponential(mu, num_fragments)**2
        # Normalize to total mass
        return masses * (total_mass / np.sum(masses))

    @staticmethod
    def gurney_v2(explosive_mass, casing_mass, gurney_constant, confinement_factor=1.0):
        """
        Enhanced Gurney model with confinement corrections.
        """
        ratio = explosive_mass / casing_mass
        # Standard Gurney (cylinder)
        v_base = gurney_constant * np.sqrt(ratio / (1.0 + 0.5 * ratio))
        # V2 Correction: Confinement increases effective explosive coupling
        v_eff = v_base * (1.0 + 0.05 * confinement_factor)
        return v_eff

    @staticmethod
    def generate_fragments_v2(total_mass, explosive_v_det, casing_radius, material_params, num_fragments):
        """
        Generates fragments using the V2 Fracture Engine (Grady-Kipp physics).
        """
        strain_rate = FractureEngineV2.estimate_strain_rate(explosive_v_det, casing_radius, 0.005)
        masses = FractureEngineV2.sample_grady_kipp_distribution(total_mass, strain_rate, material_params, num_fragments)
        return masses

    @staticmethod
    def get_fragment_properties(mass, shape_factor=None):
        """
        Calculates geometric properties for a non-spherical fragment.
        V2.x stochastic shape factor modeling.
        """
        density_steel = 7850.0
        volume = mass / density_steel
        # Characteristic dimension (equivalent cube)
        s = volume**(1.0/3.0)

        # Stochastic shape factor (S): ratio of average projected area to s^2
        # For sphere, S=0.785. For cube, S=1.5. For shards, S > 2.0.
        if shape_factor is None:
            # Proprietary stochastic distribution for jagged fragments
            shape_factor = np.random.normal(1.8, 0.3)
            shape_factor = np.clip(shape_factor, 1.2, 3.0)

        area = shape_factor * s**2
        diameter = 2 * np.sqrt(area / np.pi)
        return area, diameter
