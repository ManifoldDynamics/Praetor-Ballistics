import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF

env_atm = StandardAtmosphere()
env_earth = EarthModel()
proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)
aero = Aerodynamics()
solver = Solver6DoF(proj, aero, env_atm, env_earth)

t_span = (0, 100)
pos0 = [0, 0, 0]
v0 = 800.0 # m/s
pitch0 = np.deg2rad(45.0)
yaw0 = 0.0
spin = 300.0 * 2 * np.pi

sol = solver.solve(t_span, pos0, v0, pitch0, yaw0, spin, max_step=0.1)

print(f"Status: {sol.status}")
print(f"Message: {sol.message}")
print(f"Final time: {sol.t[-1]}")
print(f"Final Z: {sol.y[2, -1]}")
print(f"Max Z: {np.max(sol.y[2, :])}")
