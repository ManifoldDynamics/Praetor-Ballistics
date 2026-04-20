import numpy as np
from ballistics.targeting import TargetingSystem

def test_v2_multi_objective_targeting():
    from unittest.mock import MagicMock
    solver = MagicMock()
    # Mock a trajectory that "hits" at a certain angle
    sol_mock = MagicMock()
    sol_mock.y = np.zeros((13, 10))
    # Final state
    sol_mock.y[0, -1] = 1000.0 # x
    sol_mock.y[1, -1] = 0.0    # y
    sol_mock.y[2, -1] = 0.0    # z
    sol_mock.y[3, -1] = 400.0  # vx
    sol_mock.y[5, -1] = -100.0 # vz (falling)
    sol_mock.t = np.linspace(0, 5, 10)

    solver.solve.return_value = sol_mock
    solver.projectile.mass = 43.0
    solver.projectile.diameter = 0.155

    ts = TargetingSystem(solver)

    # This will trigger v2_solver
    res = ts.find_firing_solution([1000, 0, 0], 800, 1800, version=2, impact_angle_deg=45.0)

    assert res is not None
    # Since we mocked the solver to return a "hit", res should be success
    # (Actually it runs Nelder-Mead which calls solver many times,
    # so we'd need a more complex mock to actually test the convergence,
    # but this verifies the plumbing).
    assert hasattr(ts, 'v2_solver')
