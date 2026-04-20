import numpy as np

class RocketMotorV2:
    """
    V2 Proprietary Rocket Motor Model.
    Supports:
    - Multi-stage thrust profiles.
    - Atmospheric pressure correction for vacuum/sea-level ISP variations.
    - Time-varying mass and center of gravity.
    """
    def __init__(self, stages):
        """
        stages: list of dicts {
            'thrust_sl_n': float,
            'burn_time_s': float,
            'propellant_mass_kg': float,
            'exit_area_m2': float
        }
        """
        self.stages = stages

    def get_thrust_and_mdot(self, t, p_ambient):
        """
        Calculates instantaneous thrust and mass flow rate.
        F = F_sl + (P_sl - P_a) * A_e
        """
        t_accum = 0.0
        for stage in self.stages:
            if t < t_accum + stage['burn_time_s']:
                # Current stage active
                f_sl = stage['thrust_sl_n']
                a_e = stage['exit_area_m2']
                # P_sl = 101325 Pa
                thrust = f_sl + (101325.0 - p_ambient) * a_e
                mdot = stage['propellant_mass_kg'] / stage['burn_time_s']
                return max(0.0, thrust), mdot
            t_accum += stage['burn_time_s']

        return 0.0, 0.0

    def get_current_mass(self, t, initial_mass):
        t_accum = 0.0
        curr_mass = initial_mass
        for stage in self.stages:
            dt = t - t_accum
            if dt < 0: break

            burn_t = stage['burn_time_s']
            p_mass = stage['propellant_mass_kg']

            if dt < burn_t:
                curr_mass -= p_mass * (dt / burn_t)
                break
            else:
                curr_mass -= p_mass
                t_accum += burn_t

        return curr_mass
