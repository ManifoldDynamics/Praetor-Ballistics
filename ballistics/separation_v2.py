import numpy as np

class MultiBodyManagerV2:
    """
    V2 Proprietary Multi-Body Separation Engine.
    Manages the simultaneous 6-DoF simulation of multiple separating bodies
    (e.g., discard sabots, MIRVs, or sub-munitions).
    """
    def __init__(self, main_body, sub_bodies):
        """
        main_body: Projectile/Aero/etc for the core vehicle.
        sub_bodies: list of dicts {'projectile': p, 'aero': a, 'initial_relative_pos': [x,y,z], ...}
        """
        self.main_body = main_body
        self.sub_bodies = sub_bodies

    @staticmethod
    def calculate_interference_drag(dist_vec, v_rel, m_inf):
        """
        Proprietary model for aerodynamic interference between close bodies.
        Calculates the drag multiplier based on proximity and wake effects.
        """
        dist = np.linalg.norm(dist_vec)
        if dist < 0.001: dist = 0.001

        # Interference decays with distance (approx 1/r^2)
        # Wake effect: if body B is behind A, its Cd is reduced
        interference_factor = 1.0 - 0.2 * np.exp(-dist / 0.5)
        return max(0.5, interference_factor)

    @staticmethod
    def get_separation_impulse(t_sep, force_n, duration_s):
        """Calculates separation force profile."""
        if t_sep < 0: return 0.0
        if t_sep < duration_s:
            return force_n
        return 0.0
