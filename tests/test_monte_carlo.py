import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.monte_carlo import MonteCarloSimulator

def test_monte_carlo_zero_variance():
    # If standard deviations are 0, all shots should land in exactly the same spot
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
    aero = Aerodynamics()
    solver = Solver6DoF(proj, aero, env_atm, env_earth)

    mc = MonteCarloSimulator(solver)

    # Run 5 shots with 0 variance
    res = mc.run(
        num_shots=5,
        target_plane='vertical',
        target_distance=1000.0,
        base_v0=800.0,
        base_pitch_rad=np.deg2rad(5.0),
        base_yaw_rad=0.0,
        base_spin_rads=100.0,
        max_workers=2
    )

    assert res.cep_50 == 0.0 # CEP should be perfectly 0
    assert len(res.impacts) == 5

    # All impacts should equal the MPI
    for imp in res.impacts:
        assert np.isclose(imp[0], res.mpi[0])
        assert np.isclose(imp[1], res.mpi[1])

def test_monte_carlo_variance():
    # If standard deviations > 0, shots should diverge
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
    aero = Aerodynamics()
    solver = Solver6DoF(proj, aero, env_atm, env_earth)

    mc = MonteCarloSimulator(solver)

    res = mc.run(
        num_shots=10,
        target_plane='horizontal',
        target_distance=0.0,
        base_v0=800.0,
        base_pitch_rad=np.deg2rad(5.0),
        base_yaw_rad=0.0,
        base_spin_rads=100.0,
        sd_v0_ms=10.0,
        max_workers=2
    )

    assert res.cep_50 > 0.0 # CEP should be non-zero due to variance
    assert len(res.impacts) == 10
