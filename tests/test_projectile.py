import numpy as np
from ballistics.projectile import Projectile, Aerodynamics

def test_projectile():
    mass = 43.0 # 155mm standard shell mass
    dia = 0.155
    ix = 0.15
    iy = 1.6
    proj = Projectile(mass, dia, ix, iy)

    assert proj.mass == 43.0
    assert proj.diameter == 0.155
    assert np.isclose(proj.reference_area, np.pi * (0.155 / 2.0)**2)

def test_aerodynamics_defaults():
    aero = Aerodynamics()
    cd_mach0 = aero.cd(0.5)
    cd_mach1 = aero.cd(1.0)

    assert cd_mach1 > cd_mach0
    assert aero.cl(1.0) == 0.1

def test_aerodynamics_tabular():
    mach_arr = [0.0, 1.0, 2.0]
    cd_arr = [0.2, 0.4, 0.3]

    aero = Aerodynamics(cd=(mach_arr, cd_arr))

    # Test interpolation
    assert np.isclose(aero.cd(0.5), 0.3)

    # Test extrapolation
    assert np.isclose(aero.cd(3.0), 0.2)

def test_aerodynamics_constant():
    aero = Aerodynamics(cl=0.15)
    assert np.isclose(aero.cl(0.5), 0.15)
    assert np.isclose(aero.cl(3.0), 0.15)

def test_aerodynamics_csv(tmp_path):
    import csv
    filepath = tmp_path / "custom_aero.csv"
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Mach', 'Cd', 'Cl'])
        writer.writerow(['0.5', '0.2', '0.1'])
        writer.writerow(['1.0', '0.4', '0.15'])
        writer.writerow(['2.0', '0.3', '']) # Missing Cl value
        writer.writerow(['3.0', '0.25', '0.05'])

    aero = Aerodynamics.from_csv(filepath)

    # Test Cd interpolation
    assert np.isclose(aero.cd(0.5), 0.2)
    assert np.isclose(aero.cd(1.5), 0.35)

    # Test Cl interpolation with missing value handled correctly
    assert np.isclose(aero.cl(0.5), 0.1)
    # The point at mach 2.0 is missing for cl, so interpolation between 1.0 and 3.0 gives 0.1
    assert np.isclose(aero.cl(2.0), 0.1)

    # Defaults should remain for unprovided columns
    assert aero.cmaq(1.0) == -10.0

def test_g1_g7_models():
    aero_g1 = Aerodynamics.g1()
    aero_g7 = Aerodynamics.g7()

    # Drag peak around Mach 1.2
    assert aero_g1.cd(1.2) > aero_g1.cd(0.5)
    assert aero_g7.cd(1.2) > aero_g7.cd(0.5)

    # G7 should be more aerodynamic (lower Cd) than G1 at supersonic speeds
    assert aero_g7.cd(2.0) < aero_g1.cd(2.0)

def test_projectile_from_stl(tmp_path):
    import trimesh
    # Create a known unit cylinder: radius = 0.5, height = 1.0
    # Mass = density * volume = density * pi * r^2 * h
    radius = 0.5
    height = 1.0
    density = 1000.0 # kg/m^3

    mesh = trimesh.creation.cylinder(radius=radius, height=height)

    # trimesh cylinder is aligned with Z. We rotate it to align with X (our roll axis)
    transform = trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0])
    mesh.apply_transform(transform)

    stl_path = tmp_path / "test_cylinder.stl"
    mesh.export(stl_path)

    proj = Projectile.from_stl(stl_path, density_kg_m3=density)

    # 1. Check Mass
    expected_vol = np.pi * radius**2 * height
    expected_mass = expected_vol * density
    assert np.isclose(proj.mass, expected_mass, rtol=0.01) # Small tolerance for mesh discretization

    # 2. Check Caliber (Diameter)
    assert np.isclose(proj.diameter, radius * 2.0, rtol=0.01)

    # 3. Check Inertia
    # For a solid cylinder along X axis:
    # Ix = 0.5 * m * r^2
    # Iy = Iz = (1/12) * m * (3*r^2 + h^2)
    expected_ix = 0.5 * expected_mass * radius**2
    expected_iy = (1.0/12.0) * expected_mass * (3*radius**2 + height**2)

    # STL meshes are faceted, so a cylinder is actually a prism.
    # This introduces a small error in volume and inertia compared to a perfect theoretical cylinder.
    assert np.isclose(proj.i_x, expected_ix, rtol=0.05)
    assert np.isclose(proj.i_y, expected_iy, rtol=0.05)
