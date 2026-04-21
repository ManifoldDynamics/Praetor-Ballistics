import numpy as np
import concurrent.futures
from copy import deepcopy

from ballistics.environment import WindProfile
from ballistics.projectile import Projectile
from ballistics.solver import Solver6DoF
from ballistics.stochastic_v2 import StochasticEngineV2

class MonteCarloResult:
    def __init__(self, target_plane, impacts, mpi, cep_50, message):
        """
        target_plane: 'vertical' or 'horizontal'
        impacts: Nx2 numpy array of [U, V] coordinates on the target plane
                 Vertical plane: [Y, Z] (Deflection, Elevation)
                 Horizontal plane: [X, Y] (Range, Deflection)
        mpi: [mean_U, mean_V] Mean Point of Impact
        cep_50: Radius enclosing 50% of the shots from the MPI
        message: String message regarding the simulation success
        """
        self.target_plane = target_plane
        self.impacts = impacts
        self.mpi = mpi
        self.cep_50 = cep_50
        self.message = message

def _run_single_shot(base_solver, p_state, target_plane, target_distance):
    """
    Worker function to run a single trajectory with randomized parameters.
    Must be a module-level function to work cleanly with multiprocessing.
    """
    # 1. Rebuild the solver with the new randomized parameters
    proj = Projectile(
        mass=p_state['mass'],
        diameter=base_solver.projectile.diameter,
        i_x=base_solver.projectile.i_x,
        i_y=base_solver.projectile.i_y
    )

    wind = WindProfile()
    if p_state['wind_speed'] > 0:
        # Assuming constant wind for dispersion for simplicity, keeping original direction
        original_wind = base_solver.env_wind
        wind_dir = 90.0 # Default
        if original_wind is not None:
            # Basic fallback if they had a polar wind defined
            pass # A full robust solution would randomize all layers, but we simplify here
        wind.set_wind_layers_polar([0], [p_state['wind_speed']], [wind_dir])
    else:
        wind = base_solver.env_wind

    solver = Solver6DoF(
        projectile=proj,
        aero=base_solver.aero,
        environment_atm=base_solver.env_atm,
        environment_earth=base_solver.env_earth,
        environment_wind=wind,
        latitude_rad=base_solver.latitude_rad,
        propulsion=base_solver.propulsion
    )

    # 2. Define custom termination event
    if target_plane == 'vertical':
        # Stop at target X distance
        def reach_target_x(t, state):
            return state[0] - target_distance
        reach_target_x.terminal = True
        reach_target_x.direction = 1
        events = reach_target_x
    else:
        # Horizontal plane: stop when hitting the ground (Z=0)
        events = None # Default is already hit ground

    # 3. Run solver
    sol = solver.solve(
        t_span=(0, 100),
        initial_position=[0, 0, 0],
        initial_velocity=p_state['v0'],
        initial_pitch=p_state['pitch'],
        initial_yaw=p_state['yaw'],
        spin_rate=p_state['spin'],
        max_step=0.2, # Use large step for faster Monte Carlo
        custom_events=events
    )

    if not sol.success:
        return None

    # 4. Extract impact coordinates
    if target_plane == 'vertical':
        # Return Y and Z at target distance X
        if sol.y[0, -1] < target_distance - 1.0:
            return None # Hit the ground before reaching target distance
        return [sol.y[1, -1], sol.y[2, -1]]
    else:
        # Return X and Y at ground impact Z=0
        return [sol.y[0, -1], sol.y[1, -1]]


class MonteCarloSimulator:
    def __init__(self, base_solver):
        self.base_solver = base_solver

    def run(self, num_shots, target_plane, target_distance,
            base_v0, base_pitch_rad, base_yaw_rad, base_spin_rads,
            sd_v0_ms=0.0, sd_mass_kg=0.0, sd_wind_speed_ms=0.0,
            sd_pitch_rad=0.0, sd_yaw_rad=0.0, max_workers=None, version=1):
        """
        Runs the Monte Carlo simulation.
        target_plane: 'vertical' or 'horizontal'
        target_distance: Distance X in meters (only used if vertical plane)
        """

        # 1. Generate random states
        np.random.seed(42)
        random_states = []

        if version == 2:
            # Use V2 Correlated Sampling
            means = [base_v0, self.base_solver.projectile.mass, base_pitch_rad, base_yaw_rad]
            sds = [sd_v0_ms, sd_mass_kg, sd_pitch_rad, sd_yaw_rad]
            # Assuming a standard correlation matrix (e.g. higher mass -> lower v0)
            corr = np.eye(4)
            corr[0, 1] = corr[1, 0] = -0.3 # 30% negative correlation

            samples = StochasticEngineV2.sample_correlated_inputs(means, sds, corr, num_shots)
            for s in samples:
                random_states.append({
                    'v0': s[0], 'mass': max(0.001, s[1]), 'pitch': s[2], 'yaw': s[3],
                    'wind_speed': max(0.0, np.random.normal(0.0, sd_wind_speed_ms)),
                    'spin': base_spin_rads
                })
        else:
            for _ in range(num_shots):
                state = {
                    'v0': np.random.normal(base_v0, sd_v0_ms),
                    'mass': max(0.001, np.random.normal(self.base_solver.projectile.mass, sd_mass_kg)),
                    'wind_speed': max(0.0, np.random.normal(0.0, sd_wind_speed_ms)),
                    'pitch': np.random.normal(base_pitch_rad, sd_pitch_rad),
                    'yaw': np.random.normal(base_yaw_rad, sd_yaw_rad),
                    'spin': base_spin_rads
                }
                random_states.append(state)

        # 2. Run Simulations in Parallel
        impacts = []

        # Use ThreadPoolExecutor or ProcessPoolExecutor. Process is better for CPU bound
        # but ThreadPool is easier for pickling complex objects.
        # solve_ivp releases the GIL in the compiled scipy routines partially, but Process is safer.
        # To use ProcessPoolExecutor, all arguments must be picklable.
        # To simplify, we will use ProcessPoolExecutor and pass simple dicts.

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all jobs
            futures = [
                executor.submit(_run_single_shot, self.base_solver, state, target_plane, target_distance)
                for state in random_states
            ]

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result is not None:
                        impacts.append(result)
                except Exception as e:
                    print(f"Shot failed: {e}")

        if len(impacts) == 0:
            return MonteCarloResult(target_plane, np.array([]), [0, 0], 0.0, "All shots failed to reach the target plane.")

        impacts = np.array(impacts)

        # 3. Calculate Statistics (MPI and CEP)
        # Mean Point of Impact
        mpi_u = np.mean(impacts[:, 0])
        mpi_v = np.mean(impacts[:, 1])
        mpi = [mpi_u, mpi_v]

        # Circular Error Probable (CEP)
        if version == 2:
            # Use V2 Bayesian Engine
            cep_50 = StochasticEngineV2.calculate_bayesian_cep(impacts, mpi)
        else:
            distances = np.sqrt((impacts[:, 0] - mpi_u)**2 + (impacts[:, 1] - mpi_v)**2)
            cep_50 = np.median(distances)

        msg = f"Successfully simulated {len(impacts)}/{num_shots} shots."

        return MonteCarloResult(target_plane, impacts, mpi, cep_50, msg)
