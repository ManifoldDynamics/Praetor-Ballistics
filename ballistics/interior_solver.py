import numpy as np
from scipy.integrate import solve_ivp
from ballistics.interior_ballistics import InteriorResult
from ballistics.interior_v2 import InteriorSolverV2

class InteriorSolver:
    """
    Thermodynamic Lumped-Parameter Interior Ballistics Solver.
    Uses simplified energy conservation to model the pressure curve and muzzle velocity.
    """
    def __init__(self, gun_system, charge, start_pressure_pa=30e6, version=1):
        """
        gun_system: The GunSystem object (barrel length, chamber vol, etc.)
        charge: The Charge object (propellant, mass, web thickness)
        start_pressure_pa: Shot-start pressure (the pressure required to engrave the
                           projectile into the rifling and start it moving). Default 30 MPa.
        version: 1 for V1 solver, 2 for V2 proprietary solver.
        """
        self.gun = gun_system
        self.charge = charge
        self.P0 = start_pressure_pa
        self.version = version

    def solve(self, max_time_s=0.05, max_step=1e-5):
        if self.version == 2:
            v2_solver = InteriorSolverV2(self.gun, self.charge, self.P0)
            return v2_solver.solve(max_time_s, max_step)

        """
        Integrates the interior ballistics equations.
        State vector: y = [x, v, z]
        x: Projectile travel (m)
        v: Projectile velocity (m/s)
        z: Fraction of propellant burned (0.0 to 1.0)
        """

        # Precompute constants
        C = self.charge.mass
        M = self.gun.bullet_mass
        A = self.gun.bore_area
        V0 = self.gun.chamber_volume

        prop = self.charge.propellant
        F = prop.impetus
        eta = prop.covolume
        gamma = prop.gamma
        rho_p = prop.density

        a_burn = prop.burn_coeff
        n_burn = prop.burn_exponent

        e_0 = self.charge.web_thickness
        theta = self.charge.form_factor_theta

        # Effective mass (accounts for the kinetic energy of the accelerating gas and unburned powder)
        # Typically M_eff = M + C/3
        # Also need to account for rotational inertia converting linear energy to rotational energy

        # v_rot = omega * r.
        # Rotational Energy E_r = 0.5 * Ix * omega^2
        # Since omega = v * rads_per_meter, E_r = 0.5 * Ix * (v * rads_per_m)^2
        # We can fold this directly into the effective mass!
        # E_k_total = 0.5 * m * v^2 + 0.5 * Ix * (rads_per_m)^2 * v^2 = 0.5 * v^2 * (m + Ix * rads_per_m^2)
        rot_inertia_equivalent_mass = self.gun.bullet_ix_kgm2 * (self.gun.rads_per_meter**2)

        M_eff = M + (C / 3.0) + rot_inertia_equivalent_mass

        # Form function for burning: dz/dt = f(z) * burn_rate
        # For a simple geometry (like a cylinder or sphere), form function relates fraction burned z to web remaining
        # z = (1 - f) * (1 + theta * f), where f is fraction of web remaining.
        # This can get highly complex. For a lumped solver, we'll use a standard empirical derivative:
        def dz_dt_func(P, z):
            if z >= 1.0:
                return 0.0

            # Linear burn rate law: r = a * P^n
            r = a_burn * (P ** n_burn)

            # The rate of change of mass fraction dz/dt is proportional to r and the current surface area.
            # Simplified shape function for a generic grain:
            # S_ratio = sqrt(1 - z) for a sphere/cube, or 1.0 for neutral burning tube.
            # We'll use a generic interpolation: S_ratio = (1 - z)^theta
            # For theta=0 (neutral), S_ratio = 1.
            S_ratio = max(0.0, 1.0 - z)**theta

            # dz/dt = (Surface_Area_0 / Volume_0) * r * S_ratio
            # For a characteristic dimension e_0 (web), Volume_0 / Surface_Area_0 ~ e_0
            return (r / e_0) * S_ratio

        def eom(t, y):
            x, v, z = y

            # Clamp z
            z = min(1.0, max(0.0, z))

            # 1. Volume currently available for gas
            # V(t) = Chamber_Volume + (Travel * Area) - Volume_of_solid_propellant
            # Solid propellant volume = C * (1 - z) / rho_p
            V_t = V0 + A * x - (C * (1.0 - z) / rho_p)

            # 2. Energy Conservation to find Pressure
            # Energy of burned gas = C * z * F / (gamma - 1)
            # Kinetic energy of projectile and gas = 0.5 * M_eff * v^2
            # E_available = E_gas - E_kinetic (Ignoring heat loss to barrel for MVP)

            # The gas equation of state: P * (V_t - C*z*eta) = E_available * (gamma - 1)
            # Therefore: P = [ C*z*F - 0.5*(gamma-1)*M_eff*v^2 ] / [ V_t - C*z*eta ]

            numerator = C * z * F - 0.5 * (gamma - 1.0) * M_eff * (v**2)
            denominator = V_t - C * z * eta

            if denominator <= 0:
                P = 0.0 # Prevent singularity
            else:
                P = numerator / denominator

            # Floor pressure at 1 atm
            P = max(101325.0, P)

            # 3. Derivatives

            # Evaluate friction depending on travel
            friction_n = 0.0
            if x <= 0.001:
                # Bullet is engaging the rifling (high engraving force)
                friction_n = self.gun.engraving_force_n
            else:
                # Bullet is traveling down the bore
                friction_n = self.gun.bore_friction_n

            # The force pushing the bullet is Base Pressure minus Friction
            net_force = (P * A) - friction_n

            # Projectile doesn't move until Shot Start Pressure is reached (force > friction)
            if x <= 0.0 and net_force <= 0.0:
                dx_dt = 0.0
                dv_dt = 0.0
            else:
                dx_dt = v
                # Ensure we don't accidentally decelerate back into the chamber
                if v <= 0.0 and net_force < 0.0:
                    dv_dt = 0.0
                else:
                    dv_dt = net_force / M_eff

            dz_dt = dz_dt_func(P, z)

            return [dx_dt, dv_dt, dz_dt]

        # Event: Projectile reaches muzzle
        def exit_muzzle(t, y):
            return y[0] - self.gun.barrel_length
        exit_muzzle.terminal = True
        exit_muzzle.direction = 1

        # Initial state: x=0, v=0, z=small_ignition_fraction
        # We start with a tiny fraction of powder burned to provide initial pressure
        z0 = 0.01
        y0 = [0.0, 0.0, z0]

        # Integrate
        sol = solve_ivp(
            eom,
            (0, max_time_s),
            y0,
            method='RK45',
            events=exit_muzzle,
            max_step=max_step,
            dense_output=True
        )

        # We must recompute pressure over the history to return the P-T curve
        # since solve_ivp only returns the state vector.
        times = sol.t
        pressures = []
        for i in range(len(times)):
            x, v, z = sol.y[:, i]
            V_t = V0 + A * x - (C * (1.0 - z) / rho_p)
            numerator = C * z * F - 0.5 * (gamma - 1.0) * M_eff * (v**2)
            denominator = V_t - C * z * eta
            P = numerator / denominator if denominator > 0 else 101325.0
            pressures.append(P)

        pressures = np.array(pressures)

        # Calculate final spin rate
        final_velocity = sol.y[1, -1] if len(sol.y[1]) > 0 else 0.0
        final_spin = final_velocity * self.gun.rads_per_meter

        return InteriorResult(
            success=sol.success,
            t=times,
            p_pa=pressures,
            v_ms=sol.y[1, :],
            x_m=sol.y[0, :],
            z_frac=sol.y[2, :],
            message=sol.message,
            spin_rads=final_spin
        )
