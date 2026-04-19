import numpy as np

# Standard G1 Drag Model data
# Data points approximated from standard G1 reference tables (Mach vs Drag Coefficient)
G1_MACH = np.array([
    0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 4.0, 5.0
])
G1_CD = np.array([
    0.160, 0.160, 0.161, 0.165, 0.180, 0.220, 0.280, 0.380, 0.450, 0.490, 0.520, 0.510, 0.480, 0.450, 0.420, 0.360, 0.310, 0.250, 0.210
])

# Standard G7 Drag Model data (boat-tail standard projectile, lower drag than G1 at supersonic)
G7_MACH = np.array([
    0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 4.0, 5.0
])
G7_CD = np.array([
    0.120, 0.120, 0.121, 0.122, 0.125, 0.135, 0.160, 0.240, 0.300, 0.340, 0.360, 0.350, 0.330, 0.310, 0.290, 0.240, 0.200, 0.150, 0.120
])
