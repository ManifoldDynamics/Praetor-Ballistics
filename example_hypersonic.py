import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.materials import Material

def run_hypersonic_demo():
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()

    # Simulating a massive railgun slug (Mach 7.5 launch velocity)
    v0 = 2500.0 # 2500 m/s
    t_span = (0, 2) # Only 2 seconds of flight to see the immediate thermal shock
    pos0 = [0, 0, 0]
    pitch0 = np.deg2rad(15.0)

    # Tungsten Slug
    mat_w = Material("Tungsten (WHA)")
    proj_w = Projectile(mass=10.0, diameter=0.05, i_x=0.01, i_y=0.1, material=mat_w, nose_radius_m=0.005)

    # Aluminum Slug
    mat_al = Material("Aluminum (7075-T6)")
    proj_al = Projectile(mass=10.0, diameter=0.05, i_x=0.01, i_y=0.1, material=mat_al, nose_radius_m=0.005)

    aero = Aerodynamics(cd=0.1) # Hypersonic sleek cone

    print("--- Hypersonic Aerothermodynamics Test ---")
    print(f"Launch Velocity: {v0} m/s")

    print("\n1. Firing Tungsten Railgun Slug...")
    solver_w = Solver6DoF(proj_w, aero, env_atm, env_earth)
    sol_w = solver_w.solve(t_span, pos0, v0, pitch0, 0.0, 0.0, max_step=0.2)
    max_t_w = np.max(sol_w.y[13, :])
    print(f"  Max Nose Temperature: {max_t_w:.1f} K")
    print(f"  Tungsten Melting Point: {mat_w.melting_point} K")
    if max_t_w > mat_w.melting_point:
        print("  -> TUNGSTEN MELTED!")
    else:
        print("  -> SURVIVED. Tungsten handles the heat.")

    print("\n2. Firing Aluminum Railgun Slug...")
    solver_al = Solver6DoF(proj_al, aero, env_atm, env_earth)
    sol_al = solver_al.solve(t_span, pos0, v0, pitch0, 0.0, 0.0, max_step=0.2)
    max_t_al = np.max(sol_al.y[13, :])
    print(f"  Max Nose Temperature: {max_t_al:.1f} K")
    print(f"  Aluminum Melting Point: {mat_al.melting_point} K")
    if max_t_al > mat_al.melting_point:
        print("  -> ALUMINUM MELTED!")
    else:
        print("  -> SURVIVED.")

if __name__ == "__main__":
    run_hypersonic_demo()
