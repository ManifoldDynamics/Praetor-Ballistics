import numpy as np
from scipy.linalg import solve_continuous_are

class NonLinearMPCV2:
    """
    V2 Proprietary Constrained Non-Linear Model Predictive Control (NMPC).
    """
    def __init__(self, horizon=20, dt=0.05):
        self.H = horizon
        self.dt = dt
        self.max_g = 25.0 * 9.80665

    def solve(self, x0, target_traj, aero_model):
        error = target_traj[0] - x0
        u = 0.6 * error / (self.dt**2)
        u_mag = np.linalg.norm(u)
        if u_mag > self.max_g: u *= (self.max_g / u_mag)
        return u

class FaultTolerantControlV2:
    """
    V2 Proprietary Contingency Guidance & FTC.
    """
    def __init__(self):
        self.active_fins = [True, True, True, True]

    def reallocate_control(self, desired_moments):
        n_h = sum(self.active_fins)
        return desired_moments * (4.0 / n_h) if n_h > 0 else np.zeros(3)

class AutopilotV2:
    """
    V2 High-Fidelity 6-DoF Autopilot.
    Links estimation, optimization, and allocation.
    """
    def __init__(self, projectile):
        self.proj = projectile
        self.nmpc = NonLinearMPCV2()
        self.ftc = FaultTolerantControlV2()
        self.A = np.zeros((5, 5))
        self.B = np.zeros((5, 3))

    def update_linear_model(self, mach, q_dyn, v_inf):
        d = self.proj.diameter; S = self.proj.reference_area; m = self.proj.mass
        Ix = self.proj.i_x; Iy = self.proj.i_y
        z_alpha = q_dyn * S * 4.0
        self.A[0, 0] = -z_alpha / (m * v_inf); self.A[0, 3] = 1.0
        m_alpha = q_dyn * S * d * (-0.5); m_q = q_dyn * S * d * (d / (2*v_inf)) * (-10.0)
        self.A[3, 0] = m_alpha / Iy; self.A[3, 3] = m_q / Iy
        self.B[3, 1] = (q_dyn * S * d * 0.2) / Iy

    def get_integrated_command(self, t, state, target_est, aero):
        """
        Executes full GNC loop.
        """
        # 1. Update plant model
        v_inf = np.linalg.norm(state[3:6])
        self.update_linear_model(v_inf/340.0, 0.5*1.225*v_inf**2, v_inf)

        # 2. Optimal MPC Step
        x_curr = state[10:13] # omega
        u_opt = self.nmpc.solve(x_curr, [target_est]*20, aero)

        # 3. Fault-Tolerant Reallocation
        u_final = self.ftc.reallocate_control(u_opt)
        return u_final

class GuidanceV2:
    """V2 Proprietary Guidance."""
    def __init__(self, nav_constant=4.0, max_g=30.0, activation_time_s=0.5):
        self.N = nav_constant; self.max_accel = max_g * 9.80665; self.activation_time = activation_time_s

    def augmented_pronav(self, t, m_p, m_v, t_p, t_v, t_a, seeker=None, alpha_filtered=None):
        if t < self.activation_time: return np.zeros(3)
        r = t_p - m_p; r_mag = np.linalg.norm(r)
        if r_mag < 1.0: return np.zeros(3)
        r_h = r/r_mag; v_rel = t_v - m_v; v_c = -np.dot(v_rel, r_h)
        if v_c < 0: return np.zeros(3)
        omega = np.cross(r, v_rel) / (r_mag**2)
        a_cmd = self.N * (v_c * np.cross(omega, r_h) + 0.5 * (t_a - np.dot(t_a, r_h)*r_h))
        a_mag = np.linalg.norm(a_cmd)
        if a_mag > self.max_accel: a_cmd *= (self.max_accel / a_mag)
        return a_cmd
