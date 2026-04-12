import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF

env_atm = StandardAtmosphere()
env_earth = EarthModel()
proj = Projectile(mass=50.0, diameter=0.12, i_x=0.5, i_y=5.0)
aero = Aerodynamics()
t_span = (0, 300)
pos0 = [0, 0, 0]
v0 = 200.0
pitch = np.deg2rad(15.0)

propulsion = {'active': True, 'thrust_n': 10000.0, 'burn_time_s': 3.0, 'propellant_mass_kg': 5.0}
solver_rocket = Solver6DoF(proj, aero, env_atm, env_earth, propulsion=propulsion)
sol_rocket = solver_rocket.solve(t_span, pos0, v0, pitch, 0.0, 0.0, max_step=0.1)
print(sol_rocket.y[2, :]) # Print Z heights
