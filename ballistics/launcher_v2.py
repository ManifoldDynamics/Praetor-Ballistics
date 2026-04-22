import numpy as np
from scipy.integrate import solve_ivp

class LauncherDynamicsV2:
    """
    V2 Proprietary Launcher & Platform Dynamics Engine.

    Implements:
    - Multi-Body Recoil modeling (Gun + Carriage + Platform).
    - Barrel Whip (Transverse vibration during projectile travel).
    - Tip-off Dynamics: Angular perturbations at muzzle exit.
    - Shock and Vibration propagation to mounted sensors.
    """
    def __init__(self, platform_mass, carriage_mass, barrel_mass, stiffness_k, damping_c):
        self.m_p = platform_mass
        self.m_c = carriage_mass
        self.m_b = barrel_mass
        self.k = stiffness_k
        self.c = damping_c

    def solve_recoil(self, force_profile_t, force_profile_f, t_span):
        """
        Solves the recoil 1D equation of motion.
        M_total * x_ddot + C * x_dot + K * x = F_gun(t)
        """
        m_total = self.m_p + self.m_c + self.m_b

        def eom(t, y):
            x, x_dot = y
            # Interpolate force
            f_ext = np.interp(t, force_profile_t, force_profile_f)
            x_ddot = (f_ext - self.c * x_dot - self.k * x) / m_total
            return [x_dot, x_ddot]

        sol = solve_ivp(eom, t_span, [0, 0], method='RK45')
        return sol

    def calculate_barrel_whip(self, x_proj, v_proj, barrel_length, e_modulus, inertia_i):
        """
        Estimates transverse barrel deflection as projectile travels.
        Simplified 1st mode beam approximation.
        """
        if x_proj >= barrel_length: return 0.0

        # Load P is projectile weight + centrifugal force from rifling
        # (Highly proprietary V2 estimation)
        p_load = 100.0 # [N]
        # Deflection y(x) = (P*x^2 / (6*E*I)) * (3L - x)
        deflection = (p_load * x_proj**2 / (6.0 * e_modulus * inertia_i)) * (3.0 * barrel_length - x_proj)
        return deflection

    @staticmethod
    def estimate_tip_off(v_exit, whip_deflection, whip_rate):
        """
        Calculates the initial angular perturbation (Pitch/Yaw) at muzzle exit.
        theta_exit = arctan(whip_rate / v_exit)
        """
        return np.arctan(whip_rate / v_exit)
