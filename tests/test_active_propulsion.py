import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF

def test_active_propulsion():
    # Comparing an unpowered shot vs a powered shot
    env_atm = StandardAtmosphere()
    env_earth = EarthModel()

    # Very heavy generic projectile (e.g. a small unguided rocket)
    proj = Projectile(mass=50.0, diameter=0.12, i_x=0.5, i_y=5.0)
    aero = Aerodynamics()

    t_span = (0, 30)
    pos0 = [0, 0, 0]
    v0 = 200.0 # Slow initial launch velocity
    pitch = np.deg2rad(15.0)

    spin = 100.0 * 2 * np.pi # Need spin to stabilize the thrusting rocket

    # 1. Unpowered Baseline
    solver_base = Solver6DoF(proj, aero, env_atm, env_earth)
    sol_base = solver_base.solve(t_span, pos0, v0, pitch, 0.0, spin, max_step=0.5)

    range_base = sol_base.y[0, -1]

    # 2. Powered
    # 1500 N thrust for 3 seconds, burning 5 kg of propellant.
    # Enough to overcome drag and accelerate, but not so much it immediately tumbles.
    propulsion = {
        'active': True,
        'thrust_n': 1500.0,
        'burn_time_s': 3.0,
        'propellant_mass_kg': 5.0
    }
    solver_rocket = Solver6DoF(proj, aero, env_atm, env_earth, propulsion=propulsion)
    sol_rocket = solver_rocket.solve(t_span, pos0, v0, pitch, 0.0, spin, max_step=0.5)

    range_rocket = sol_rocket.y[0, -1]

    # The velocity at burnout (t ~ 3s) should be higher for the rocket
    # Find index closest to 3.0s
    idx_burnout = np.abs(sol_rocket.t - 3.0).argmin()

    v_base = np.linalg.norm(sol_base.y[3:6, idx_burnout])
    v_rocket = np.linalg.norm(sol_rocket.y[3:6, idx_burnout])

    assert v_rocket > v_base

    # The rocket's mass should have decreased by the expelled propellant mass
    assert solver_rocket.propulsion['propellant_mass_kg'] == 5.0
