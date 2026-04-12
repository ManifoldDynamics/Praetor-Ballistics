import numpy as np
import trimesh
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.targeting import TargetingSystem
from ballistics.explosives import Explosive
from ballistics.lethality import FragmentationModel
from ballistics.raytracer import LethalityRayTracer

def run_lethality_demo():
    print("--- 1. Generating Target Mesh (Virtual Tank) ---")
    # Generate a simple 3D box representing a vehicle 20m wide, 10m deep, 5m high
    mesh = trimesh.creation.box(extents=[10, 20, 5])
    stl_path = "virtual_tank.stl"
    mesh.export(stl_path)

    # 2. Setup standard firing parameters
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()
    # 155mm shell with 5kg of Comp B explosive
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
    aero = Aerodynamics.g7()

    solver = Solver6DoF(proj, aero, env_atm, env_earth)
    targeting = TargetingSystem(solver)

    target_pos = [1000.0, 0.0, 0.0]
    print(f"\n--- 2. Finding Intercept Solution for Target at {target_pos} ---")
    res = targeting.find_firing_solution(target_pos, v0=800.0, spin_rate=100.0)

    if not res.success:
        print("Failed to intercept.")
        return

    print(f"Intercept successful. TOF: {res.time_of_flight:.2f}s. Terminal Vel: {res.terminal_velocity:.1f} m/s")

    print("\n--- 3. Running Fragmentation & Ray-Tracing Lethality ---")
    # Comp B Explosive
    exp = Explosive("Composition B")
    exp_mass = 5.0
    metal_mass = proj.mass - exp_mass

    g_vel = FragmentationModel.gurney_velocity(exp_mass, metal_mass, exp.gurney_constant)
    print(f"Gurney Fragment Velocity: {g_vel:.1f} m/s")

    # Generate 1000 fragments
    frag_props = FragmentationModel.generate_fragments(metal_mass, num_fragments=1000)
    spray = FragmentationModel.spray_vectors(1000, g_vel)

    # Target Armor: 20mm RHA
    tracer = LethalityRayTracer(stl_path, target_pos, target_armor_mm=20.0)

    term_pos = res.trajectory.y[0:3, -1]
    term_vel = res.trajectory.y[3:6, -1]
    term_quat = res.trajectory.y[6:10, -1]

    leth = tracer.analyze_lethality(term_pos, term_vel, term_quat, frag_props['mass_kg'], frag_props['diameter_m'], spray)

    print(f"\nTotal Fragments: {leth.total_fragments}")
    print(f"Fragments Impacting Target: {leth.hit_count}")
    print(f"Fragments Penetrating >20mm RHA: {leth.penetration_count}")

if __name__ == "__main__":
    run_lethality_demo()
