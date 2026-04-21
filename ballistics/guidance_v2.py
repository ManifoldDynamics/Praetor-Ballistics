import numpy as np

class GuidanceV2:
    """
    V2 Proprietary Guidance Laws.
    Implements:
    - Augmented Proportional Navigation (APN): Accounts for target acceleration.
    - Optimal Guidance Law (OGL): Minimizes control effort and terminal miss.
    """
    def __init__(self, nav_constant=4.0, max_g=30.0, activation_time_s=0.5):
        self.N = nav_constant
        self.max_accel = max_g * 9.80665
        self.activation_time = activation_time_s

    def augmented_pronav(self, t, m_p, m_v, t_p, t_v, t_a, seeker=None):
        """
        APN guidance law.
        a_cmd = N * (V_c * omega + 0.5 * t_a_perp)
        """
        if t < self.activation_time:
            return np.zeros(3)

        # If seeker is provided, use "sensed" target instead of truth
        if seeker is not None:
            # For simplicity in this wrapper, we assume seeker handles internal history
            # But the caller should pass the sensed states
            pass

        r = t_p - m_p
        r_mag = np.linalg.norm(r)
        if r_mag < 1.0: return np.zeros(3)

        r_hat = r / r_mag
        v_rel = t_v - m_v
        v_c = -np.dot(v_rel, r_hat)

        if v_c < 0: return np.zeros(3)

        omega = np.cross(r, v_rel) / (r_mag**2)

        # Target acceleration perpendicular to LOS
        t_a_perp = t_a - np.dot(t_a, r_hat) * r_hat

        a_cmd = self.N * (v_c * np.cross(omega, r_hat) + 0.5 * t_a_perp)

        # Limit G
        a_mag = np.linalg.norm(a_cmd)
        if a_mag > self.max_accel:
            a_cmd *= (self.max_accel / a_mag)

        return a_cmd

    def optimal_guidance(self, t, m_p, m_v, t_p, t_v, t_go, seeker=None):
        """
        Simple Optimal Guidance Law for intercept.
        a_cmd = N/t_go^2 * [ (t_p - m_p) + t_go*(t_v - m_v) ]
        """
        if t < self.activation_time or t_go <= 0.01:
            return np.zeros(3)

        z_miss = (t_p - m_p) + t_go * (t_v - m_v)
        a_cmd = (self.N / (t_go**2)) * z_miss

        a_mag = np.linalg.norm(a_cmd)
        if a_mag > self.max_accel:
            a_cmd *= (self.max_accel / a_mag)

        return a_cmd
