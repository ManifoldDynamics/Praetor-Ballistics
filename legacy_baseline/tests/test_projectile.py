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
