import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel, WindProfile
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF

def run_wind_demo():
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()

    # 155mm standard projectile, G7 aerodynamics
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
    aero = Aerodynamics.g7()

    t_span = (0, 300)
    pos0 = [0, 0, 0]
    v0 = 800.0 # m/s
    pitch0 = np.deg2rad(15.0) # Lower angle for faster flight time in demo
    yaw0 = 0.0
    spin = 300.0 * 2 * np.pi

    print("--- 1. Baseline: Zero Wind ---")
    solver_no_wind = Solver6DoF(proj, aero, env_atm, env_earth)
    sol_no_wind = solver_no_wind.solve(t_span, pos0, v0, pitch0, yaw0, spin, max_step=1.0)
    print(f"Impact Range: {sol_no_wind.y[0, -1]:.2f} m")
    print(f"Impact Deflection: {sol_no_wind.y[1, -1]:.2f} m (Pure spin drift / coriolis)")

    print("\n--- 2. Wind Profile: Severe Crosswind ---")
    wind = WindProfile()
    # Define a wind blowing from the left (towards negative Y) that gets stronger at higher altitudes
    # altitudes in meters, speed in m/s, direction 270 (blowing towards negative Y axis)
    wind.set_wind_layers_polar(
        altitudes=[0, 1000, 5000, 15000],
        speeds=[2.0, 5.0, 15.0, 30.0],
        azimuths_deg=[270, 270, 270, 270]
    )

    solver_wind = Solver6DoF(proj, aero, env_atm, env_earth, environment_wind=wind)
    sol_wind = solver_wind.solve(t_span, pos0, v0, pitch0, yaw0, spin, max_step=1.0)
    print(f"Impact Range: {sol_wind.y[0, -1]:.2f} m")
    print(f"Impact Deflection: {sol_wind.y[1, -1]:.2f} m")

    diff_y = sol_wind.y[1, -1] - sol_no_wind.y[1, -1]
    print(f"\n-> Net Wind Deflection: {diff_y:.2f} m")

if __name__ == "__main__":
    run_wind_demo()
