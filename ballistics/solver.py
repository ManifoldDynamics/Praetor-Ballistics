import numpy as np
from scipy.integrate import solve_ivp
from ballistics.eom import get_eom

class Solver6DoF:
    def __init__(self, projectile, aero, environment_atm, environment_earth, environment_wind=None, latitude_rad=0.0, propulsion=None):
        self.projectile = projectile
        self.aero = aero
        self.env_atm = environment_atm
        self.env_earth = environment_earth
        self.env_wind = environment_wind
        self.latitude_rad = latitude_rad
        self.propulsion = propulsion

    def solve(self, t_span, initial_position, initial_velocity, initial_pitch, initial_yaw, spin_rate, max_step=0.01, custom_events=None):
        if np.isscalar(initial_velocity):
            vx = initial_velocity * np.cos(initial_pitch) * np.cos(initial_yaw)
            vy = initial_velocity * np.cos(initial_pitch) * np.sin(initial_yaw)
            vz = initial_velocity * np.sin(initial_pitch)
            v0 = np.array([vx, vy, vz])
        else:
            v0 = np.array(initial_velocity)

        cy = np.cos(initial_yaw * 0.5)
        sy = np.sin(initial_yaw * 0.5)
        cp = np.cos(initial_pitch * 0.5)
        sp = np.sin(initial_pitch * 0.5)
        cr = np.cos(0.0)
        sr = np.sin(0.0)

        q0 = cr * cp * cy + sr * sp * sy
        q1 = sr * cp * cy - cr * sp * sy
        q2 = cr * sp * cy + sr * cp * sy
        q3 = cr * cp * sy - sr * sp * cy
        q_init = np.array([q0, q1, q2, q3])
        q_init = q_init / np.linalg.norm(q_init)

        omega0 = np.array([spin_rate, 0.0, 0.0])

        # Include 14th state for temperature if material is provided
        use_thermo = hasattr(self.projectile, 'material') and self.projectile.material is not None
        num_states = 14 if use_thermo else 13

        y0 = np.zeros(num_states)
        y0[0:3] = initial_position
        y0[3:6] = v0
        y0[6:10] = q_init
        y0[10:13] = omega0

        if use_thermo:
            y0[13] = 300.0 # Start at ~27C (300K)

        def hit_ground(t, y, *args):
            return y[2] # Z position
        hit_ground.terminal = True
        hit_ground.direction = -1

        events = [hit_ground]
        if custom_events is not None:
            if isinstance(custom_events, list):
                events.extend(custom_events)
            else:
                events.append(custom_events)

        def eom_wrapper(t, y):
            return get_eom(t, y, self.projectile, self.aero, self.env_atm, self.env_earth, self.env_wind, self.latitude_rad, self.propulsion)

        sol = solve_ivp(
            eom_wrapper,
            t_span,
            y0,
            method='RK45',
            events=events,
            max_step=max_step,
            dense_output=True
        )

        return sol