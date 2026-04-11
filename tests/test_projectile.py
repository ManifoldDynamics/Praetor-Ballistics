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
