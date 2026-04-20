import numpy as np
from scipy.optimize import minimize

class PredictiveInterceptSolverV2:
    """
    V2 Proprietary Strategic Targeting Solver.
    Optimizes trajectories for:
    - Minimum terminal miss distance.
    - Desired impact angle (Angle of Attack).
    - Maximum terminal kinetic energy.
    """
    def __init__(self, solver):
        self.solver = solver

    def solve_multi_objective(self, target_pos, v0, spin,
                             desired_impact_angle_deg=None,
                             priority='accuracy'):
        """
        Runs a Nelder-Mead optimization to find initial pitch/yaw that satisfies
        multiple engagement objectives.
        """
        x_t, y_t, z_t = target_pos

        def reach_target_x(t, state):
            return state[0] - x_t
        reach_target_x.terminal = True
        reach_target_x.direction = 1

        def objective(angles):
            pitch, yaw = angles
            sol = self.solver.solve(
                t_span=(0, 500),
                initial_position=[0,0,0],
                initial_velocity=v0,
                initial_pitch=pitch,
                initial_yaw=yaw,
                spin_rate=spin,
                max_step=2.0,
                custom_events=reach_target_x
            )

            # 1. Miss Distance Penalty
            final_pos = sol.y[0:3, -1]
            miss_dist = np.linalg.norm(final_pos - target_pos)

            # 2. Impact Angle Penalty
            angle_penalty = 0.0
            if desired_impact_angle_deg is not None:
                final_vel = sol.y[3:6, -1]
                # Angle relative to horizontal (XZ plane)
                actual_angle = np.rad2deg(np.arcsin(-final_vel[2] / np.linalg.norm(final_vel)))
                angle_penalty = (actual_angle - desired_impact_angle_deg)**2

            # 3. Kinetic Energy Objective
            # Minimize negative energy to maximize actual energy
            ke_obj = -0.5 * self.solver.projectile.mass * np.linalg.norm(sol.y[3:6, -1])**2

            if priority == 'accuracy':
                return miss_dist**2 * 1000 + angle_penalty
            elif priority == 'lethality':
                return miss_dist**2 * 100 + ke_obj / 1e6
            else:
                return miss_dist**2

        # Initial Guess (45 deg pitch, 0 yaw)
        res = minimize(objective, [np.deg2rad(45), 0.0], method='Nelder-Mead', tol=1e-2)
        return res
