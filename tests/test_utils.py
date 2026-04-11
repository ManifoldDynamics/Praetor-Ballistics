import numpy as np
from ballistics.eom import quaternion_to_euler, rotation_matrix_to_quaternion

def test_quaternion_to_euler():
    # Test 1: Identity (No rotation)
    q = np.array([1, 0, 0, 0])
    y, p, r = quaternion_to_euler(q)
    assert np.isclose(y, 0)
    assert np.isclose(p, 0)
    assert np.isclose(r, 0)

    # Test 2: Pitch 90 degrees
    # q = cos(45) + sin(45)j
    q2 = np.array([np.cos(np.pi/4), 0, np.sin(np.pi/4), 0])
    y, p, r = quaternion_to_euler(q2)
    assert np.isclose(y, 0)
    assert np.isclose(p, np.pi/2)
    assert np.isclose(r, 0)

def test_export_trajectory_csv(tmp_path):
    from ballistics.utils import export_trajectory_csv
    from ballistics.environment import StandardAtmosphere, EarthModel
    from ballistics.projectile import Projectile, Aerodynamics
    from ballistics.solver import Solver6DoF

    # Run a very short simulation just to get a valid solution object
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
    aero = Aerodynamics()
    solver = Solver6DoF(proj, aero, env_atm, env_earth)

    sol = solver.solve((0, 1), [0, 0, 0], 800.0, np.deg2rad(45.0), 0.0, 100.0, max_step=0.5)

    csv_file = tmp_path / "test_out.csv"
    export_trajectory_csv(sol, csv_file)

    # Verify file was created and has correct headers
    import csv
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)

        assert "Time (s)" in headers[0]
        assert "Roll (deg)" in headers[9]

        # Verify it has data rows corresponding to time steps
        rows = list(reader)
        assert len(rows) == len(sol.t)
