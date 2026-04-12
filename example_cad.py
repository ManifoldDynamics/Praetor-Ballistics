import numpy as np
import trimesh
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.solver import Solver6DoF

def run_cad_demo():
    print("--- 1. Generating a Virtual STL (Solid Lead Cylinder) ---")
    # We create a simple cylinder mesh programmatically to simulate an STL file
    # Diameter = 0.00762m (7.62mm / .308 caliber)
    # Length = 0.03m (30mm)
    radius = 0.00762 / 2.0
    height = 0.03

    # trimesh creates cylinders along the Z axis by default. We want the length along the X axis.
    mesh = trimesh.creation.cylinder(radius=radius, height=height)
    transform = trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0])
    mesh.apply_transform(transform)

    # Save to a temporary STL
    stl_path = "test_bullet.stl"
    mesh.export(stl_path)
    print(f"Saved generated mesh to {stl_path}")

    print("\n--- 2. Loading Projectile from STL ---")
    # Lead density is approx 11340 kg/m^3
    lead_density = 11340.0
    proj = Projectile.from_stl(stl_path, density_kg_m3=lead_density)

    print(f"Auto-Calculated Properties:")
    print(f"  Mass:     {proj.mass * 1000.0:.2f} grams (approx {proj.mass * 15432.3584:.0f} grains)")
    print(f"  Caliber:  {proj.diameter * 1000.0:.2f} mm")
    print(f"  I_x:      {proj.i_x:.8f} kg*m^2")
    print(f"  I_y:      {proj.i_y:.8f} kg*m^2")

    print("\n--- 3. Running 6-DoF Simulation with CAD Projectile ---")
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()
    aero = Aerodynamics.g7() # Using standard aero for the demonstration

    solver = Solver6DoF(proj, aero, env_atm, env_earth)

    # Firing parameters for a rifle
    t_span = (0, 10)
    pos0 = [0, 0, 0]
    v0 = 850.0 # m/s
    pitch0 = np.deg2rad(5.0)
    yaw0 = 0.0
    spin = 3000.0 * 2 * np.pi

    sol = solver.solve(t_span, pos0, v0, pitch0, yaw0, spin, max_step=0.1)

    print(f"Impact Range: {sol.y[0, -1]:.2f} m")

if __name__ == "__main__":
    run_cad_demo()
