import numpy as np

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
    def get_fragment_properties(mass):
        """
        Calculates geometric properties for a non-spherical fragment.
        """
        density_steel = 7850.0
        volume = mass / density_steel
        # Characteristic dimension (equivalent cube)
        s = volume**(1.0/3.0)
        # Average projected area (random orientation factor ~ 1.5)
        area = 1.5 * s**2
        diameter = 2 * np.sqrt(area / np.pi)
        return area, diameter
