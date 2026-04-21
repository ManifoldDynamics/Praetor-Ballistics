import numpy as np

class FlexibleBeamModelV2:
    """
    Proprietary V2 Flexible-Body & Aeroelasticity Engine.
    Models the projectile as a non-rigid body using a Modal Representation.

    The state vector is expanded to include modal coordinates (eta) and modal velocities (eta_dot).
    """
    def __init__(self, projectile):
        self.projectile = projectile
        self.num_modes = 2 # First two bending modes

        # Calculate fundamental bending frequency (approximate for a cylinder)
        # f = (3.52 / (2*pi*L^2)) * sqrt(EI/rhoA)
        # We simplify this for the MVP
        E = getattr(projectile, 'youngs_modulus', 200e9) # Steel default
        I_area = (np.pi / 64) * (projectile.diameter**4)
        L = 5.0 * projectile.diameter # Aspect ratio assumption
        A = np.pi * (projectile.diameter/2)**2
        rho = 7850.0 # Steel

        # Fundamental angular frequency
        omega_n1 = (3.52 / L**2) * np.sqrt((E * I_area) / (rho * A))
        omega_n2 = omega_n1 * 6.27 # Second mode factor

        self.omega_n = np.array([omega_n1, omega_n2])
        self.zeta = getattr(projectile, 'structural_damping', 0.02) * np.ones(self.num_modes)

    def calculate_modal_derivatives(self, t, eta, eta_dot, q_dyn, mach, alpha):
        """
        Calculates derivatives for modal coordinates:
        eta_ddot + 2*zeta*omega_n*eta_dot + omega_n^2*eta = Q_aero / M_modal
        """
        # Modal Mass (normalized to 1.0 for simplicity)
        m_modal = 1.0

        # Aeroelastic Forcing (Proprietary V2 Logic)
        # Bending increases the effective angle of attack along the body
        # Q_aero = q_dyn * S * d * C_m_theta * deformation
        q_aero = np.zeros(self.num_modes)
        for i in range(self.num_modes):
            # Coupling factor: deformation increases with alpha and dynamic pressure
            coupling = 0.01 * q_dyn * alpha * (i + 1)
            q_aero[i] = coupling - 0.001 * q_dyn * eta[i] # Aero-damping effect

        # Equation of motion: eta_ddot = (Q - C*eta_dot - K*eta) / M
        eta_ddot = (q_aero - 2 * self.zeta * self.omega_n * eta_dot - (self.omega_n**2) * eta) / m_modal

        return eta_ddot

    def get_aeroelastic_corrections(self, eta, mach):
        """
        Calculates corrections to aerodynamic coefficients based on body deformation.
        Flexing usually increases Cd and reduces stability (Cma).
        """
        def_sum = np.sum(np.abs(eta))
        # Proprietary V2 Empirical Corrections
        cd_corr = 0.05 * def_sum * (1.0 + 0.2 * mach)
        cma_corr = -0.1 * def_sum # Reduction in static stability

        return {
            'cd': cd_corr,
            'cma': cma_corr
        }
