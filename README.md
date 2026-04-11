# Ballistics Engine

A deep, 6-Degree-of-Freedom (6-DoF) true physics-based ballistics engine written in Python. This package aims to simulate realistic projectile trajectories, matching the fidelity of industry-standard tools like PRODAS.

## Features

- **6-DoF Physics Solver**: Solves the complete equations of motion over time using Runge-Kutta integration, accurately modeling a rigid body's translation and rotation.
- **Environmental Modeling**: Uses standard models for Earth's gravity (with altitude decay), Coriolis effect, and the 1976 US Standard Atmosphere (calculating air density and speed of sound dynamically).
- **Aerodynamics Model**: Supports calculating aerodynamic forces and moments based on:
  - Default simple analytical approximations
  - Standard Reference Models (G1 and G7 functions included out-of-the-box)
  - Custom user-defined tabular data via CSV parsing.

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd ballistics

# Install requirements
pip install -r requirements.txt
```

## Quick Start

You can simulate a standard 155mm projectile using the built-in G7 standard aerodynamics model:

```python
import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF

# 1. Initialize Environmental Models
env_atm = StandardAtmosphere()
env_earth = EarthModel()

# 2. Define the Projectile (Mass, Diameter, Inertia)
proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)

# 3. Load Aerodynamics (Using built-in G7 standard)
aero = Aerodynamics.g7()

# 4. Setup Solver
solver = Solver6DoF(proj, aero, env_atm, env_earth)

# 5. Define Launch Parameters
t_span = (0, 300)        # Max simulation time (s)
pos0 = [0, 0, 0]         # Initial X, Y, Z (m)
v0 = 800.0               # Muzzle velocity (m/s)
pitch0 = np.deg2rad(45.0)# Launch elevation (radians)
yaw0 = 0.0               # Launch azimuth (radians)
spin = 300.0 * 2 * np.pi # Spin rate (rad/s)

# 6. Run Simulation
sol = solver.solve(t_span, pos0, v0, pitch0, yaw0, spin, max_step=0.1)

print(f"Time of Flight: {sol.t[-1]:.2f} s")
print(f"Impact Range: {sol.y[0, -1]:.2f} m")
```

## Using Custom Aerodynamics Data (CSV)

You can load your own tabular aerodynamic coefficient data (e.g., from wind tunnel testing or CFD) via a CSV file. The file must have a header row and a column named `Mach`. You can optionally map any of the 6 aerodynamic coefficients (`Cd`, `Cl`, `Cma`, `Cmaq`, `Cnlp`, `Cmag`).

**Example `custom_aero.csv`:**
```csv
Mach, Cd, Cl, Cma
0.5, 0.20, 0.10, 2.5
1.0, 0.38, 0.15, 3.0
2.0, 0.29, 0.10, 2.0
```

**Loading the custom data:**
```python
from ballistics.projectile import Aerodynamics

# This automatically creates interpolation functions (extrapolating out of bounds by default)
aero = Aerodynamics.from_csv("custom_aero.csv")

print(aero.cd(1.5)) # Outputs interpolated value: ~0.335
```

## Running Tests

To run the unit tests, use pytest from the root directory:
```bash
PYTHONPATH=. pytest tests/
```
