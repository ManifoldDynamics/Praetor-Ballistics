import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.targeting import TargetingSystem

def run_targeting():
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()

    # We will use the 155mm standard projectile since it has more inertia and converges easily
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
    aero = Aerodynamics.g7()

    solver = Solver6DoF(proj, aero, env_atm, env_earth)
    targeting = TargetingSystem(solver)

    # Hit a target 2.5 km away, at +50m elevation
    target_x = 2500.0
    target_y = 0.0
    target_z = 50.0

    v0 = 800.0 # m/s
    spin = 300.0 * 2 * np.pi

    print(f"Targeting System Engaged.")
    print(f"Target Coordinate: X={target_x}m, Y={target_y}m, Z={target_z}m")
    print(f"Calculating firing solution...")

    # We do not provide an initial pitch hint to show the vacuum approximation works
    res = targeting.find_firing_solution([target_x, target_y, target_z], v0, spin)

    if res.success:
        print("\n--- Firing Solution Found ---")
        print(f"Required Elevation (Pitch): {np.rad2deg(res.pitch):.2f} degrees")
        print(f"Required Azimuth (Yaw): {np.rad2deg(res.yaw):.2f} degrees (To counter drift)")
        print(f"Time of Flight: {res.time_of_flight:.2f} seconds")
        print(f"Terminal Velocity: {res.terminal_velocity:.2f} m/s")
        print(f"Terminal Energy: {res.terminal_energy:.2f} Joules")

        final_x = res.trajectory.y[0, -1]
        final_y = res.trajectory.y[1, -1]
        final_z = res.trajectory.y[2, -1]
        print(f"\nIntercept Coordinates: X={final_x:.2f}m, Y={final_y:.2f}m, Z={final_z:.2f}m")
    else:
        print(f"Failed to find solution: {res.message}")

if __name__ == "__main__":
    run_targeting()
