import numpy as np

class ProportionalNavigation:
    """
    Calculates the commanded lateral acceleration required to intercept a target
    using Proportional Navigation (ProNav).
    """
    def __init__(self, nav_constant=4.0, max_g=30.0, activation_time_s=0.5):
        """
        nav_constant: N. Usually between 3 and 5.
        max_g: Maximum lateral acceleration the missile structure or fins can pull.
        activation_time_s: Time delay after launch before the seeker turns on and guidance begins.
        """
        self.nav_constant = nav_constant
        self.max_accel_ms2 = max_g * 9.80665
        self.activation_time = activation_time_s

    def get_commanded_acceleration(self, t, missile_pos, missile_vel, target_pos, target_vel):
        """
        Calculates the commanded acceleration vector in Earth frame.

        missile_pos: [X, Y, Z]
        missile_vel: [Vx, Vy, Vz]
        target_pos: [X, Y, Z]
        target_vel: [Vx, Vy, Vz]

        Returns: [Ax, Ay, Az] commanded lateral acceleration in m/s^2
        """
        if t < self.activation_time:
            return np.zeros(3)

        m_p = np.array(missile_pos)
        m_v = np.array(missile_vel)
        t_p = np.array(target_pos)
        t_v = np.array(target_vel)

        # Line of Sight (LOS) Vector (Missile to Target)
        r = t_p - m_p
        r_mag = np.linalg.norm(r)

        if r_mag < 1.0:
            return np.zeros(3) # Essentially intercepted

        r_hat = r / r_mag

        # Relative Velocity Vector
        v_rel = t_v - m_v

        # Closing Velocity (Scalar speed along the LOS)
        v_c = -np.dot(v_rel, r_hat)

        if v_c < 0.0:
            # Target is moving away faster than missile is approaching
            # ProNav breaks down here. Command 0.
            return np.zeros(3)

        # LOS Rotation Vector (Omega)
        # Omega = (r x v_rel) / r_mag^2
        omega = np.cross(r, v_rel) / (r_mag**2)

        # Pure Proportional Navigation Command
        # a_cmd = N * V_c * (Omega x u_LOS)
        a_cmd = self.nav_constant * v_c * np.cross(omega, r_hat)

        # Limit acceleration (Max G)
        a_mag = np.linalg.norm(a_cmd)
        if a_mag > self.max_accel_ms2:
            a_cmd = a_cmd * (self.max_accel_ms2 / a_mag)

        return a_cmd
