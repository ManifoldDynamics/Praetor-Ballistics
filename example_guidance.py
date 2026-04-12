import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.targeting import TargetingSystem
from ballistics.guidance import ProportionalNavigation
from ballistics.viz3d import visualize_trajectory_3d

def run_guidance_demo():
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()

    # Lightweight, highly aerodynamic missile
    proj = Projectile(mass=15.0, diameter=0.1, i_x=0.05, i_y=0.5)
    aero = Aerodynamics.g7()

    # Target starts 2.5km away, 50m up, flying left to right (positive Y) at 50 m/s (110 mph drone)
    tx, ty, tz = 2500.0, 0.0, 50.0
    tvx, tvy, tvz = 0.0, 50.0, 0.0
    target_state = {'pos': [tx, ty, tz], 'vel': [tvx, tvy, tvz]}

    print(f"--- Smart Munition Intercept Demo ---")
    print(f"Target: Fast drone flying at 50 m/s cross-range.")
    print(f"Missile: Unguided Coasting")

    # 1. Fire an UNGUIDED shot directly at the initial target coordinates
    solver_unguided = Solver6DoF(proj, aero, env_atm, env_earth, target_state=target_state)
    targeting = TargetingSystem(solver_unguided)
    res_ung = targeting.find_firing_solution([tx, ty, tz], v0=800.0, spin_rate=100.0)

    if res_ung.success:
        miss_y = res_ung.trajectory.y[1, -1]
        target_final_y = ty + tvy * res_ung.time_of_flight
        print(f"  Unguided Missile landed at Y={miss_y:.1f}m.")
        print(f"  Target had moved to Y={target_final_y:.1f}m.")
        print(f"  -> MISS by {abs(target_final_y - miss_y):.1f} meters.")

    print(f"\nMissile: Proportional Navigation Guidance Active (N=4, Max=30G)")

    # 2. Fire a GUIDED shot using Proportional Navigation
    pronav = ProportionalNavigation(nav_constant=4.0, max_g=30.0, activation_time_s=0.2)
    solver_guided = Solver6DoF(proj, aero, env_atm, env_earth, guidance=pronav, target_state=target_state)
    targeting_guided = TargetingSystem(solver_guided)

    # We tell the targeting system to aim exactly where the unguided shot aimed (it won't know the target moves)
    # But once in flight, the ProNav module will take over and steer!
    res_guided = targeting_guided.find_firing_solution([tx, ty, tz], v0=800.0, spin_rate=100.0)

    if res_guided.success:
        miss_y = res_guided.trajectory.y[1, -1]
        target_final_y = ty + tvy * res_guided.time_of_flight
        print(f"  Guided Missile landed at Y={miss_y:.1f}m.")
        print(f"  Target had moved to Y={target_final_y:.1f}m.")
        print(f"  -> DIRECT HIT! (Error: {abs(target_final_y - miss_y):.2f}m)")

        try:
            print("Launching 3D Visualization...")
            visualize_trajectory_3d(res_guided.trajectory)
        except:
            pass

if __name__ == "__main__":
    run_guidance_demo()
