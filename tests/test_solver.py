import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF

def test_simple_trajectory():
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()

    # 155mm projectile
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
    aero = Aerodynamics()

    solver = Solver6DoF(proj, aero, env_atm, env_earth)

    t_span = (0, 300)
    pos0 = [0, 0, 0]
    v0 = 800.0 # m/s (approx Mach 2.3)
    pitch0 = np.deg2rad(45.0)
    yaw0 = 0.0
    spin = 300.0 * 2 * np.pi # rad/s

    # Run solver with a relatively large max_step for fast testing
    sol = solver.solve(t_span, pos0, v0, pitch0, yaw0, spin, max_step=0.5)

    assert sol.success
    # Ensure it hit the ground
    assert sol.y[2, -1] <= 0.1

    # Ensure it travelled forward
    assert sol.y[0, -1] > 1000.0

def test_wind_deflection():
    from ballistics.environment import WindProfile

    env_atm = StandardAtmosphere()
    env_earth = EarthModel()
    proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
    aero = Aerodynamics()

    # 1. No wind
    solver_no_wind = Solver6DoF(proj, aero, env_atm, env_earth)
    sol_no = solver_no_wind.solve((0, 30), [0, 0, 0], 800.0, np.deg2rad(5.0), 0.0, 100.0, max_step=1.0)

    # 2. Strong crosswind
    wind = WindProfile()
    wind.set_constant_wind(0, 10.0, 0) # 10 m/s wind in positive Y direction
    solver_wind = Solver6DoF(proj, aero, env_atm, env_earth, environment_wind=wind)
    sol_wind = solver_wind.solve((0, 30), [0, 0, 0], 800.0, np.deg2rad(5.0), 0.0, 100.0, max_step=1.0)

    y_no_wind = sol_no.y[1, -1]
    y_wind = sol_wind.y[1, -1]

    # The wind blowing in positive Y should push the projectile further in positive Y
    assert y_wind > y_no_wind + 5.0 # Should be deflected by at least a few meters
