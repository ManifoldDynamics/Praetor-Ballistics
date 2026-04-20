import numpy as np

class FractureEngineV2:
    """
    V2 Proprietary Dynamic Fracture and Fragmentation Engine.
    Models high-strain-rate casing breakup using energy-based Mott-Grady theory.
    """
    @staticmethod
    def calculate_fragment_size_grady(strain_rate, material_toughness, density, sound_speed):
        """
        Grady's formula for nominal fragment size based on energy balance.
        s = [ sqrt(24) * G_c / (rho * strain_rate^2) ]^(1/3)
        """
        if strain_rate <= 0: return 0.1 # Large default

        # G_c: fracture toughness energy (J/m^2)
        s = (np.sqrt(24) * material_toughness / (density * strain_rate**2))**(1.0/3.0)
        return s

    @staticmethod
    def sample_grady_kipp_distribution(total_mass, strain_rate, material_params, num_fragments):
        """
        Stochastic sampler using Grady-Kipp statistics.
        Unlike Mott (empirical), this is derived from the strain-rate energy balance.
        """
        # Nominal size
        s_nom = FractureEngineV2.calculate_fragment_size_grady(
            strain_rate,
            material_params['toughness'],
            material_params['density'],
            material_params['sound_speed']
        )

        # Nominal mass
        m_nom = material_params['density'] * s_nom**3

        # Grady-Kipp distribution for fragment mass:
        # F(m) = 1 - exp(-(m/m_nom)^(1/3))
        # Sampler: m = m_nom * (-ln(1 - rand))^3
        rands = np.random.uniform(0.01, 0.99, num_fragments)
        masses = m_nom * (-np.log(1.0 - rands))**3

        # Scaling to conserve total mass
        return masses * (total_mass / np.sum(masses))

    @staticmethod
    def estimate_strain_rate(explosive_v_det, casing_radius, casing_thickness):
        """
        Estimates the initial expansion strain rate (dot{epsilon}) at the casing wall.
        """
        # Simple expansion model: dot{epsilon} ~ v_expansion / r
        # v_expansion is approx 1/4 of detonation velocity for typical explosives
        v_exp = 0.25 * explosive_v_det
        return v_exp / casing_radius
