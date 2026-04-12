import numpy as np
import pytest

from ballistics.environment import StandardAtmosphere, EarthModel, WindProfile
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.materials import Material
from ballistics.eom import get_eom

try:
    import wbs_core
    HAS_CPP_CORE = True
except ImportError:
    HAS_CPP_CORE = False

@pytest.mark.skipif(not HAS_CPP_CORE, reason="C++ core not compiled")
def test_cpp_vs_python_parity():
    # 1. Setup Environment
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()
    wind = WindProfile()
    wind.set_constant_wind(5.0, 10.0, 0.0)

    # 2. Setup Projectile (with active prop and hypersonics to test everything)
    mat = Material("Tungsten (WHA)")
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6, material=mat, nose_radius_m=0.01)

    # We must use a fully tabular aerodynamics model to test the C++ interpolation
    # The default G7 only defines CD as a table, others are constants.
    # To test C++, we build dummy tables for all 6 coefficients.
    machs = np.linspace(0, 5, 10)
    cd_arr = np.linspace(0.2, 0.4, 10)
    cl_arr = np.linspace(0.1, 0.1, 10)
    cma_arr = np.linspace(2.5, 2.5, 10)
    cmaq_arr = np.linspace(-10.0, -10.0, 10)
    cnlp_arr = np.linspace(0.5, 0.5, 10)
    cmag_arr = np.linspace(-0.5, -0.5, 10)

    aero = Aerodynamics(
        cd=(machs, cd_arr),
        cl=(machs, cl_arr),
        cma=(machs, cma_arr),
        cmaq=(machs, cmaq_arr),
        cnlp=(machs, cnlp_arr),
        cmag=(machs, cmag_arr)
    )

    propulsion = {
        'active': True,
        'thrust_n': 5000.0,
        'burn_time_s': 2.0,
        'propellant_mass_kg': 2.0
    }

    # 3. Create a mock State Vector
    t = 1.0 # 1 second into flight (motor still burning)
    state = np.zeros(14)
    state[0:3] = [800.0, 5.0, 20.0] # Pos
    state[3:6] = [850.0, 10.0, -5.0] # Vel
    state[6:10] = [1.0, 0.0, 0.0, 0.0] # Quat (Identity)
    state[10:13] = [300.0, 0.1, 0.0] # Omega
    state[13] = 400.0 # Temp K

    # 4. Run Pure Python EOM
    res_py = get_eom(t, state, proj, aero, env_atm, env_earth, wind, 0.0, propulsion)

    # 5. Run C++ EOM
    res_cpp = wbs_core.get_eom(
        t, state,
        proj.mass, proj.diameter, proj.reference_area,
        proj.i_x, proj.i_y,
        env_atm.T0, env_atm.P0, env_atm.L, env_atm.R, env_atm.G, env_atm.RH,
        env_earth.G0, env_earth.R_EARTH, env_earth.OMEGA, 0.0,
        aero._cd_func.x, aero._cd_func.y, aero._cl_func.y,
        aero._cma_func.y, aero._cmaq_func.y, aero._cnlp_func.y, aero._cmag_func.y,
        5.0, 10.0, 0.0, # Wind
        True, 5000.0, 2.0, 2.0, # Propulsion
        True, mat.density, mat.specific_heat, mat.emissivity, proj.nose_radius_m, # Hypersonics
        False, 4.0, 30.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 # Guidance args (inactive)
    )

    # 6. Compare
    assert np.allclose(res_py, res_cpp, rtol=1e-3, atol=1e-5)
