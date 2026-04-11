import numpy as np
from scipy.optimize import root

class TargetingResult:
    def __init__(self, success, pitch, yaw, time_of_flight, terminal_velocity, terminal_energy, trajectory, message):
        self.success = success
        self.pitch = pitch
        self.yaw = yaw
        self.time_of_flight = time_of_flight
        self.terminal_velocity = terminal_velocity
        self.terminal_energy = terminal_energy
        self.trajectory = trajectory
        self.message = message

class TargetingSystem:
    def __init__(self, solver):
        """
        Initializes the targeting system with a configured Solver6DoF.
        """
        self.solver = solver

    def find_firing_solution(self, target_pos, v0, spin_rate, initial_guess_pitch=None, initial_guess_yaw=0.0):
        """
        Finds the required pitch and yaw angles to hit a 3D target coordinate.

        target_pos: [X, Y, Z] of the target
        v0: Muzzle velocity
        spin_rate: Projectile spin rate
        """
        x_t, y_t, z_t = target_pos

        # Determine initial guess for pitch using a simple vacuum parabola approximation
        if initial_guess_pitch is None:
            # Vacuum equation: R = v^2 * sin(2*theta) / g -> sin(2*theta) = R*g / v^2
            g = 9.81
            range_xy = np.sqrt(x_t**2 + y_t**2)
            val = (range_xy * g) / (v0**2)
            if val > 1.0:
                return TargetingResult(False, 0, 0, 0, 0, 0, None, "Target is out of absolute physical range (vacuum bounds).")
            initial_guess_pitch = 0.5 * np.arcsin(val)

            # Account for Z elevation roughly
            if z_t != 0:
                initial_guess_pitch += np.arctan2(z_t, range_xy)

        # Event to terminate when passing the target's X coordinate
        def reach_target_x(t, state):
            return state[0] - x_t
        reach_target_x.terminal = True
        reach_target_x.direction = 1 # Passing from negative to positive relative to target

        def objective(angles):
            pitch, yaw = angles

            # Run fast low-res simulation for the optimizer
            sol = self.solver.solve(
                t_span=(0, 300),
                initial_position=[0, 0, 0],
                initial_velocity=v0,
                initial_pitch=pitch,
                initial_yaw=yaw,
                spin_rate=spin_rate,
                max_step=2.0, # Massive step for very fast approximation during iteration
                custom_events=reach_target_x
            )

            final_x = sol.y[0, -1]
            if final_x < x_t - 1.0:
                # Penalize heavily if it hits ground before target
                return [1000.0 * (x_t - final_x), 1000.0 * (x_t - final_x)]

            miss_y = sol.y[1, -1] - y_t
            miss_z = sol.y[2, -1] - z_t
            return [miss_y, miss_z]

        # Optimize using Nelder-Mead instead of hybr. It is much more robust
        # and requires fewer gradient calculations, which is critical for expensive 6DoF
        from scipy.optimize import minimize

        def scalar_objective(angles):
            miss = objective(angles)
            return miss[0]**2 + miss[1]**2

        initial_guess = [initial_guess_pitch, initial_guess_yaw]
        res = minimize(scalar_objective, initial_guess, method='Nelder-Mead', options={'xatol': 1e-3, 'fatol': 1.0})

        if res.success or res.fun < 5.0: # Accept if error is small even if it maxed iterations
            opt_pitch, opt_yaw = res.x

            # Run one final medium-resolution simulation to confirm and generate trajectory
            sol = self.solver.solve(
                t_span=(0, 300),
                initial_position=[0, 0, 0],
                initial_velocity=v0,
                initial_pitch=opt_pitch,
                initial_yaw=opt_yaw,
                spin_rate=spin_rate,
                max_step=0.1,
                custom_events=reach_target_x
            )

            final_v_vec = sol.y[3:6, -1]
            term_vel = np.linalg.norm(final_v_vec)
            term_energy = 0.5 * self.solver.projectile.mass * term_vel**2

            # Verify final hit within a tolerance (e.g., 0.5 meters)
            final_y = sol.y[1, -1]
            final_z = sol.y[2, -1]
            final_x = sol.y[0, -1]
            dist_error = np.sqrt((final_x - x_t)**2 + (final_y - y_t)**2 + (final_z - z_t)**2)

            if dist_error > 2.0:
                return TargetingResult(False, opt_pitch, opt_yaw, sol.t[-1], term_vel, term_energy, sol,
                                       f"Optimizer converged but final error is too high ({dist_error:.2f}m). Target may be unreachable.")

            return TargetingResult(True, opt_pitch, opt_yaw, sol.t[-1], term_vel, term_energy, sol, "Target hit successfully.")

        else:
            return TargetingResult(False, 0, 0, 0, 0, 0, None, f"Optimization failed: {res.message}")
