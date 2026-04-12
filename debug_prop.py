import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF

env_atm = StandardAtmosphere()
env_earth = EarthModel()
proj = Projectile(mass=50.0, diameter=0.12, i_x=0.5, i_y=5.0)
aero = Aerodynamics()
t_span = (0, 300) # Increased max time
pos0 = [0, 0, 0]
v0 = 200.0
pitch = np.deg2rad(15.0)

solver_base = Solver6DoF(proj, aero, env_atm, env_earth)
sol_base = solver_base.solve(t_span, pos0, v0, pitch, 0.0, 0.0, max_step=0.5)
print(f"Base: Time {sol_base.t[-1]}, Range {sol_base.y[0, -1]}")

propulsion = {'active': True, 'thrust_n': 10000.0, 'burn_time_s': 3.0, 'propellant_mass_kg': 5.0}
solver_rocket = Solver6DoF(proj, aero, env_atm, env_earth, propulsion=propulsion)
sol_rocket = solver_rocket.solve(t_span, pos0, v0, pitch, 0.0, 0.0, max_step=0.5)
print(f"Rocket: Time {sol_rocket.t[-1]}, Range {sol_rocket.y[0, -1]}")
