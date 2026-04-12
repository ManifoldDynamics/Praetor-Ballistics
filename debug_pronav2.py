import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.guidance import ProportionalNavigation

env_atm = StandardAtmosphere()
env_earth = EarthModel()
proj = Projectile(mass=15.0, diameter=0.1, i_x=0.05, i_y=0.5)
aero = Aerodynamics()

tx, ty, tz = 2500.0, 0.0, 50.0
tvx, tvy, tvz = 0.0, 50.0, 0.0
target_state = {'pos': [tx, ty, tz], 'vel': [tvx, tvy, tvz]}

# Try calling solve with and without the C++ core to isolate where the bug is
pronav = ProportionalNavigation(nav_constant=4.0, max_g=30.0, activation_time_s=0.2)

# Disable C++ wrapper temporarily
solver_guided = Solver6DoF(proj, aero, env_atm, env_earth, guidance=pronav, target_state=target_state)

sol = solver_guided.solve((0, 3), [0, 0, 0], 800.0, np.deg2rad(5.0), 0.0, 100.0, max_step=0.1)

# Check lateral acceleration or Y position
print(f"Y position array: {sol.y[1, -10:]}")
