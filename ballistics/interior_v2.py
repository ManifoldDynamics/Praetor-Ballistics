import numpy as np
from scipy.integrate import solve_ivp
from ballistics.interior_ballistics import InteriorResult

class GrainGeometryV2:
    """
    Advanced form functions for propellant grains in V2.
    z = fraction of mass burned.
    phi(z) = S(z)/S0 where S is the instantaneous surface area.
    """
    @staticmethod
    def get_form_function(theta, z):
        """
        Generic form function: phi(z) = (1-z)^theta
        theta = 0: Neutral (single perf or multi-perf)
        theta = 2/3: Sphere/Cube (highly degressive)
        theta = 0.5: Long cylinder (degressive)
        """
        return max(0.0, 1.0 - z)**theta

    @staticmethod
    def multi_perforated_7_perf(z):
        """
        Approximate form function for 7-perforated grains.
        Initially progressive, then degressive after slivering.
        """
        if z < 0.85:
            # Progressive phase
            return 1.0 + 0.6 * z
        else:
            # Slivering phase
            return 1.51 * (1.0 - z)**0.5

class InteriorSolverV2:
    """
    V2 Proprietary Interior Ballistics Solver.
    Features:
    - Convective heat loss to barrel walls.
    - Bore resistance profile (engraving + sliding).
    - Advanced grain geometry form functions.
    - Variable gamma effects (optional, currently constant).
    """
    def __init__(self, gun, charge, start_pressure_pa=30e6):
        self.gun = gun
        self.charge = charge
        self.P0 = start_pressure_pa
        self.T_barrel = 293.15 # K (20 C)
        self.h_conv_coeff = 0.05 # Empirical heat transfer coefficient scalar

    def solve(self, max_time_s=0.1, max_step=1e-5):
        # Charge/Propellant properties
        C = self.charge.mass
        prop = self.charge.propellant
        F = prop.impetus
        eta = prop.covolume
        gamma = prop.gamma
        rho_p = prop.density
        T_flame = prop.flame_temp
        a_burn = prop.burn_coeff
        n_burn = prop.burn_exponent
        e0 = self.charge.web_thickness
        theta = self.charge.form_factor_theta

        # Gun properties
        M = self.gun.bullet_mass
        A = self.gun.bore_area
        V0 = self.gun.chamber_volume
        L_barrel = self.gun.barrel_length
        d_bore = self.gun.bore_diameter

        rot_mass = self.gun.bullet_ix_kgm2 * (self.gun.rads_per_meter**2)
        M_eff = M + (C / 3.0) + rot_mass

        def get_surface_area(x):
            # Surface area of the chamber + barrel for heat loss
            # Chamber is approx V0/A length
            L_chamber = V0 / A
            return np.pi * d_bore * (L_chamber + x) + 2 * A

        def eom(t, y):
            x, v, z, Q_lost = y # Travel, Velocity, Fraction burned, Total Heat Lost

            z = np.clip(z, 0.0, 1.0)
            x = max(0.0, x)

            # 1. Volume and Geometry
            V_gas = V0 + A * x - (C * (1.0 - z) / rho_p)

            # 2. Pressure calculation via Energy Balance (V2.x NAC Equation of State)
            # Noble-Abel-Coward accounts for gas co-volume (eta) at extreme pressures
            # U = (C * z * F) / (gamma - 1) - 0.5 * M_eff * v^2 - Q_lost
            # P = (gamma - 1) * U / (V_gas - C * z * eta)

            energy_chem = (C * z * F) / (gamma - 1.0)
            energy_kin = 0.5 * M_eff * (v**2)

            U = energy_chem - energy_kin - Q_lost

            # co-volume correction (Noble-Abel-Coward)
            covolume_correction = C * z * eta
            effective_volume = V_gas - covolume_correction

            if effective_volume <= 1e-9:
                P = 101325.0
            else:
                # P * (V - b) = nRT -> Energy-based form
                P = U * (gamma - 1.0) / effective_volume

            # Lagrange Gradient Correction (Pressure at breech vs projectile)
            # P_avg = P * (1 + C / (3 * M))
            # P_proj = P_avg / (1 + C / (2 * M))
            lagrange_factor = (1.0 + C / (3.0 * M)) / (1.0 + C / (2.0 * M))
            P = P * lagrange_factor

            P = max(101325.0, P)

            # 3. Gas Temperature (needed for heat loss)
            # T_gas = P * (V_gas - C * z * eta) / (C * z * (F / T_flame))
            if z > 1e-4:
                T_gas = P * effective_volume / (C * z * (F / T_flame))
            else:
                T_gas = T_flame

            # 4. Heat Loss Rate (dQ/dt) - V2.x Bartz Equation Correlation
            # h = [0.026 / D^0.2] * [mu^0.2 * Cp / Pr^0.6] * (P/a)^0.8
            # (Simplified Bartz-style proprietary implementation)
            h_bartz = self.h_conv_coeff * (P**0.8) * (1.0 + 0.1 * (v / 1000.0))
            S_bore = get_surface_area(x)
            dQ_dt = h_bartz * S_bore * (T_gas - self.T_barrel)
            if dQ_dt < 0: dQ_dt = 0

            # 5. Resistance and Acceleration
            friction = self.gun.engraving_force_n if x < 0.005 else self.gun.bore_friction_n
            net_force = (P * A) - friction

            if x <= 0.0 and net_force <= 0.0:
                dv_dt = 0.0
                dx_dt = 0.0
            else:
                dv_dt = net_force / M_eff
                dx_dt = v

            # 6. Burn Rate - Vieille's Law with Temperature Sensitivity
            # r = a * P^n * (1 + beta * (T_initial - T_ref))
            # (Simplified V2.x proprietary sensitivity model)
            T_ref = 294.15 # 21C reference
            T_init = 294.15 # assuming nominal for now
            temp_sensitivity = 0.002 # 0.2% per degree K
            beta_v = 1.0 + temp_sensitivity * (T_init - T_ref)

            # Using multi-perf logic if theta is exactly 0 as a flag, otherwise generic
            if theta == 0:
                phi = GrainGeometryV2.multi_perforated_7_perf(z)
            else:
                phi = GrainGeometryV2.get_form_function(theta, z)

            dz_dt = (a_burn * beta_v * (P**n_burn) / e0) * phi if z < 1.0 else 0.0

            return [dx_dt, dv_dt, dz_dt, dQ_dt]

        def exit_muzzle(t, y):
            return y[0] - L_barrel
        exit_muzzle.terminal = True
        exit_muzzle.direction = 1

        y0 = [0.0, 0.0, 0.005, 0.0] # x, v, z, Q_lost

        sol = solve_ivp(
            eom,
            (0, max_time_s),
            y0,
            method='RK45',
            events=exit_muzzle,
            max_step=max_step,
            dense_output=True
        )

        # Post-process results
        times = sol.t
        states = sol.y
        pressures = []
        temperatures = []

        for i in range(len(times)):
            x, v, z, Q_l = states[:, i]
            V_gas = V0 + A * x - (C * (1.0 - z) / rho_p)
            U = (C * z * F) / (gamma - 1.0) - 0.5 * M_eff * (v**2) - Q_l
            P = U * (gamma - 1.0) / (V_gas - C * z * eta) if (V_gas - C * z * eta) > 0 else 101325.0
            pressures.append(P)

        final_velocity = states[1, -1]
        final_spin = final_velocity * self.gun.rads_per_meter

        return InteriorResult(
            success=sol.success,
            t=times,
            p_pa=np.array(pressures),
            v_ms=states[1, :],
            x_m=states[0, :],
            z_frac=states[2, :],
            message=sol.message,
            spin_rads=final_spin
        )
