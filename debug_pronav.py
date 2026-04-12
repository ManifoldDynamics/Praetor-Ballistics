import numpy as np
from ballistics.guidance import ProportionalNavigation

# Missile 1km away from a target moving to the right
m_pos = [0, 0, 0]
m_vel = [800, 0, 0]
t_pos = [1000, 0, 0]
t_vel = [0, 50, 0] # moving right at 50 m/s

pn = ProportionalNavigation()
a_cmd = pn.get_commanded_acceleration(1.0, m_pos, m_vel, t_pos, t_vel)
print(f"Commanded Accel: {a_cmd} m/s^2")
