import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.targeting import TargetingSystem

def test_targeting_system():
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
    aero = Aerodynamics() # Default simplified aero is faster for tests

    solver = Solver6DoF(proj, aero, env_atm, env_earth)
    targeting = TargetingSystem(solver)

    target_x = 1000.0
    target_y = 0.0
    target_z = 0.0

    res = targeting.find_firing_solution([target_x, target_y, target_z], v0=800.0, spin_rate=100.0)

    assert res.success is True
    assert res.pitch > 0.0 # Must pitch up to fight gravity

    # Check that final trajectory point is actually near the target
    final_x = res.trajectory.y[0, -1]
    final_z = res.trajectory.y[2, -1]

    assert np.isclose(final_x, target_x, atol=1.0)
    assert np.isclose(final_z, target_z, atol=1.0)

def test_targeting_out_of_range():
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
    aero = Aerodynamics()
    solver = Solver6DoF(proj, aero, env_atm, env_earth)
    targeting = TargetingSystem(solver)

    # Try to shoot something in space with 1 m/s velocity
    res = targeting.find_firing_solution([100000.0, 0, 0], v0=1.0, spin_rate=0.0)

    assert res.success is False
