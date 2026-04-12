import numpy as np
from scipy.integrate import solve_ivp
from ballistics.eom import get_eom

class Solver6DoF:
    def __init__(self, projectile, aero, environment_atm, environment_earth, environment_wind=None, latitude_rad=0.0, propulsion=None, guidance=None, target_state=None):
        self.projectile = projectile
        self.aero = aero
        self.env_atm = environment_atm
        self.env_earth = environment_earth
        self.env_wind = environment_wind
        self.latitude_rad = latitude_rad
        self.propulsion = propulsion
        self.guidance = guidance
        self.target_state = target_state

    def solve(self, t_span, initial_position, initial_velocity, initial_pitch, initial_yaw, spin_rate, max_step=0.01, custom_events=None):
        import numpy as np

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

        # Attempt to use C++ Core if available for maximum performance
        try:
            import wbs_core
            use_cpp = True
        except ImportError:
            use_cpp = False

        # Temporarily disable C++ core for testing Guidance since the C++ module needs to be recompiled
        # with the latest guidance logic changes to match Python precisely, but we are running in an environment
        # where we might not want to re-run `pip install -e .` on every minor tweak.
        use_cpp = False

        import numpy as np

        # Pre-extract Aerodynamics tables for C++
        if use_cpp:
            # C++ expects mach_array and corresponding coeff_arrays
            # If the user passed a constant/function, we evaluate it over a generic Mach range to create a lookup table for C++
            if hasattr(self.aero._cd_func, 'x') and hasattr(self.aero._cd_func, 'y'):
                aero_machs = self.aero._cd_func.x
            else:
                aero_machs = np.linspace(0.0, 10.0, 50)

            def _get_array(func):
                if hasattr(func, 'y') and hasattr(func, 'x') and np.array_equal(func.x, aero_machs):
                    return func.y
                else:
                    return np.array([func(m) for m in aero_machs])

            self._cpp_machs = aero_machs
            self._cpp_cds = _get_array(self.aero._cd_func)
            self._cpp_cls = _get_array(self.aero._cl_func)
            self._cpp_cmas = _get_array(self.aero._cma_func)
            self._cpp_cmaqs = _get_array(self.aero._cmaq_func)
            self._cpp_cnlps = _get_array(self.aero._cnlp_func)
            self._cpp_cmags = _get_array(self.aero._cmag_func)

        def eom_wrapper(t, y):
            if use_cpp:
                # Prepare arguments for C++
                pos = y[0:3]
                altitude = pos[2]

                # Atmosphere baseline
                T0 = self.env_atm.T0
                P0 = self.env_atm.P0
                L = self.env_atm.L
                R = self.env_atm.R
                G_atm = self.env_atm.G
                RH = self.env_atm.RH

                # Earth baseline
                G0 = self.env_earth.G0
                R_EARTH = self.env_earth.R_EARTH
                OMEGA = self.env_earth.OMEGA

                # Wind
                wind_vx, wind_vy, wind_vz = 0.0, 0.0, 0.0
                if self.env_wind is not None:
                    # To keep C++ fast, we just grab the wind at the current altitude
                    w = self.env_wind.get_wind(altitude)
                    wind_vx, wind_vy, wind_vz = w[0], w[1], w[2]

                # Propulsion
                p_act = False
                p_t = 0.0
                p_b = 0.0
                p_m = 0.0
                if self.propulsion is not None and self.propulsion.get('active', False):
                    p_act = True
                    p_t = self.propulsion.get('thrust_n', 0.0)
                    p_b = self.propulsion.get('burn_time_s', 0.0)
                    p_m = self.propulsion.get('propellant_mass_kg', 0.0)

                # Hypersonics
                h_act = False
                mat_density = 0.0
                mat_cp = 0.0
                mat_eps = 0.0
                if hasattr(self.projectile, 'material') and self.projectile.material is not None:
                    h_act = True
                    mat_density = self.projectile.material.density
                    mat_cp = self.projectile.material.specific_heat
                    mat_eps = self.projectile.material.emissivity

                nose_rad = getattr(self.projectile, 'nose_radius_m', 0.001)

                # Guidance
                g_act = False
                n_const = 0.0
                max_g = 0.0
                g_act_t = 0.0
                tgt_px = tgt_py = tgt_pz = 0.0
                tgt_vx = tgt_vy = tgt_vz = 0.0

                if self.guidance is not None and self.target_state is not None:
                    g_act = True
                    n_const = self.guidance.nav_constant
                    max_g = self.guidance.max_accel_ms2 / 9.80665 # C++ expects max_g in Gs
                    g_act_t = self.guidance.activation_time
                    tgt_px, tgt_py, tgt_pz = self.target_state['pos']
                    tgt_vx, tgt_vy, tgt_vz = self.target_state['vel']

                return wbs_core.get_eom(
                    t, y,
                    self.projectile.mass, self.projectile.diameter, self.projectile.reference_area,
                    self.projectile.i_x, self.projectile.i_y,
                    T0, P0, L, R, G_atm, RH,
                    G0, R_EARTH, OMEGA, self.latitude_rad,
                    self._cpp_machs, self._cpp_cds, self._cpp_cls,
                    self._cpp_cmas, self._cpp_cmaqs, self._cpp_cnlps, self._cpp_cmags,
                    wind_vx, wind_vy, wind_vz,
                    p_act, p_t, p_b, p_m,
                    h_act, mat_density, mat_cp, mat_eps, nose_rad,
                    g_act, n_const, max_g, g_act_t,
                    tgt_px, tgt_py, tgt_pz,
                    tgt_vx, tgt_vy, tgt_vz
                )
            else:
                return get_eom(t, y, self.projectile, self.aero, self.env_atm, self.env_earth, self.env_wind, self.latitude_rad, self.propulsion, self.guidance, self.target_state)

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