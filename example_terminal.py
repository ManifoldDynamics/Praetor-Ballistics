import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.targeting import TargetingSystem

def run_terminal_demo():
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()

    # Simulate a 120mm APFSDS-like penetrator
    # High mass (8 kg tungsten rod), very small aerodynamic diameter (sabot discarded, e.g. 25mm rod)
    proj = Projectile(mass=8.0, diameter=0.025, i_x=0.05, i_y=0.5)

    # Highly aerodynamic (low drag)
    aero = Aerodynamics(cd=0.15)

    solver = Solver6DoF(proj, aero, env_atm, env_earth)
    targeting = TargetingSystem(solver)

    # Tank target 2 km away
    target_x = 2000.0
    target_y = 0.0
    target_z = 0.0

    # Extremely high muzzle velocity (1600 m/s ~ Mach 4.7)
    v0 = 1600.0
    spin = 0.0 # Fin stabilized, not spin stabilized

    print(f"--- Firing APFSDS Penetrator at Target 2000m Away ---")

    # Use Lanz-Odermatt specifically for long-rod penetrators
    # Need to pass density and length of rod
    penetration_kwargs = {
        'penetrator_density_kg_m3': 17600.0, # Tungsten
        'penetrator_length_m': 0.6 # 60cm long rod
    }

    res = targeting.find_firing_solution(
        [target_x, target_y, target_z],
        v0, spin,
        penetration_model='lanz_odermatt',
        penetration_kwargs=penetration_kwargs
    )

    if res.success:
        print(f"Time of Flight: {res.time_of_flight:.2f} seconds")
        print(f"Impact Velocity: {res.terminal_velocity:.2f} m/s")
        print(f"Impact Energy: {res.terminal_energy / 1e6:.2f} Megajoules")
        print(f"Armor Penetration (Lanz-Odermatt): {res.penetration_mm:.1f} mm of RHA")

        # We can also compare against the historical Krupp formula just for fun
        from ballistics.terminal import TerminalBallistics
        p_krupp = TerminalBallistics.krupp(res.terminal_velocity, proj.mass, proj.diameter)
        print(f"Armor Penetration (Krupp equivalent): {p_krupp:.1f} mm")
    else:
        print("Failed to find solution.")

if __name__ == "__main__":
    run_terminal_demo()
