import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.utils import export_trajectory_csv, plot_trajectory

def run_example():
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)

    # Use the G7 aerodynamics model
    aero = Aerodynamics.g7()

    solver = Solver6DoF(proj, aero, env_atm, env_earth)

    t_span = (0, 300)
    pos0 = [0, 0, 0]
    v0 = 800.0 # m/s
    pitch0 = np.deg2rad(45.0)
    yaw0 = 0.0
    spin = 300.0 * 2 * np.pi

    print("Running 6-DoF simulation with G7 aerodynamics...")
    sol = solver.solve(t_span, pos0, v0, pitch0, yaw0, spin, max_step=0.1)

    print(f"Simulation Finished. Status: {sol.status}")
    print(f"Time of Flight: {sol.t[-1]:.2f} s")
    print(f"Max Altitude: {np.max(sol.y[2, :]):.2f} m")
    print(f"Impact Range (X): {sol.y[0, -1]:.2f} m")
    print(f"Impact Deflection (Y): {sol.y[1, -1]:.2f} m")

    csv_filename = "trajectory_output.csv"
    print(f"Exporting data to {csv_filename}...")
    export_trajectory_csv(sol, csv_filename)

    print("Generating plots...")
    plot_trajectory(sol)

if __name__ == "__main__":
    run_example()
