# Ballistics Engine

A deep, 6-Degree-of-Freedom (6-DoF) true physics-based ballistics engine written in Python. This package aims to simulate realistic projectile trajectories, matching the fidelity of industry-standard tools like PRODAS.

## Features

- **6-DoF Physics Solver**: Solves the complete equations of motion over time using Runge-Kutta integration, accurately modeling a rigid body's translation and rotation.
- **Interior Ballistics Thermodynamics**: Solves lumped-parameter thermodynamic differential equations (like STANAG 4367) to calculate the pressure curve, burn fraction, and muzzle velocity of a projectile based on chamber volume, barrel length, charge mass, and propellant type. Includes a database of standard energetic materials.
- **Active Propulsion**: Supports modeling rocket-assisted projectiles (RAP) or missiles via configurable thrust vectors and time-varying mass loss curves.
- **PyVista 3D Visualization**: Renders stunning, interactive 3D flight paths of the simulated trajectory directly from the GUI.
- **Monte Carlo Dispersion**: Simulates $N$ parallel shots utilizing Python `multiprocessing` to introduce variance into projectile mass, muzzle velocity, wind speed, and firing angles, calculating the resulting Circular Error Probable (CEP) and Mean Point of Impact (MPI).
- **Targeting & Zeroing System**: Iteratively solves for the exact Elevation (Pitch) and Azimuth (Yaw) required to intercept a specific 3D coordinate, taking into account spin drift, Coriolis effect, and aerodynamic drop.
- **Terminal Ballistics**: Includes standard empirical armor penetration formulas (`De Marre`, `Krupp`, `Lanz-Odermatt` for APFSDS) to estimate lethality against armor upon target impact.
- **Environmental Modeling**: Uses standard models for Earth's gravity (with altitude decay), Coriolis effect, and atmospheric properties. Supports custom weather baselines (accounting for humidity via Virtual Temperature) and **Live Weather Fetching** using coordinates.
- **Advanced Wind Profiles**: Support for 3D vector wind fields, allowing definition of custom layered crosswinds (by speed/azimuth or Cartesian vectors) that smoothly interpolate across altitude bands.
- **Aerodynamics Model**: Supports calculating aerodynamic forces and moments based on:
  - Default simple analytical approximations
  - Standard Reference Models (G1 and G7 functions included out-of-the-box)
  - Custom user-defined tabular data via CSV parsing.
- **CAD Integration**: Ingest STL files directly to automatically calculate the projectile's Mass, Reference Area (Caliber), and Principal Moments of Inertia ($I_x$, $I_y$) based on material density.

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd ballistics

# Install requirements
pip install -r requirements.txt
```

## Desktop GUI

The easiest way to interact with the engine is via the built-in PyQt6 graphical user interface. This provides a split-pane layout to configure interior thermodynamics (propellant type, barrel length), download live weather via GPS coordinates, set target parameters, and calculate the exact firing solution while instantly plotting the 3D trajectory profiles. It also features a dedicated **Monte Carlo Dispersion tab** to visualize your weapon system's CEP hit-probability envelope natively.

```bash
python gui.py
```

The GUI includes a fully-featured **Main Menu** and **Project System**. You can use `File -> Save` to save your projectile parameters, target coordinates, and environment setup as a `.blst` JSON file, allowing you to reload and resume your ballistic studies later using `File -> Open Project...`.

## Python API Quick Start

You can simulate a standard 155mm projectile using the built-in G7 standard aerodynamics model:

```python
import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF

# 1. Initialize Environmental Models (Live Weather Example)
from ballistics.weather import LiveWeather
# Fetch live weather for a high-altitude location (e.g. Leadville, CO)
env_atm = LiveWeather.fetch_atmosphere(latitude=39.2508, longitude=-106.2925)
env_earth = EarthModel()

from ballistics.environment import WindProfile
wind = WindProfile()
# Define a 5 m/s wind blowing from the left (270 degrees azimuth) at all altitudes
wind.set_constant_wind(vx=0.0, vy=-5.0, vz=0.0)

# 2. Define the Projectile (Mass, Diameter, Inertia)
proj = Projectile(mass=43.0, diameter=0.155, i_x=0.15, i_y=1.6)

# 3. Load Aerodynamics (Using built-in G7 standard)
aero = Aerodynamics.g7()

# 4. Setup Solver
solver = Solver6DoF(proj, aero, env_atm, env_earth, environment_wind=wind)

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

## Target Intercept (Zeroing)

Instead of guessing launch angles, you can use the `TargetingSystem` to find the exact firing solution needed to hit a specific 3D coordinate.

```python
from ballistics.targeting import TargetingSystem

targeting = TargetingSystem(solver)

target_x, target_y, target_z = 2500.0, 0.0, 50.0 # Hit a target 2.5km away and 50m high
v0 = 800.0
spin = 300.0 * 2 * 3.14159

# Optionally calculate Terminal Ballistics penetration depth (Lanz-Odermatt for APFSDS)
res = targeting.find_firing_solution(
    [target_x, target_y, target_z],
    v0,
    spin,
    penetration_model='lanz_odermatt',
    penetration_kwargs={'penetrator_density_kg_m3': 17600.0, 'penetrator_length_m': 0.6}
)

if res.success:
    print(f"Required Pitch: {np.rad2deg(res.pitch):.2f} degrees")
    print(f"Required Yaw: {np.rad2deg(res.yaw):.2f} degrees")
    print(f"Armor Penetration: {res.penetration_mm:.1f} mm of RHA steel")
```

## Using Custom CAD Models (STL)

If you have a 3D model of your projectile, you can bypass manually defining the physical properties. The engine will automatically parse the mesh, calculate its volume, and derive the Mass, Caliber, and Inertia Tensors based on your specified material density.

```python
from ballistics.projectile import Projectile

# Load an STL of a lead bullet (Density of Lead ≈ 11340 kg/m^3)
# Assumes the STL was exported with units in meters.
proj = Projectile.from_stl("my_bullet.stl", density_kg_m3=11340.0)

print(f"Auto-calculated Mass: {proj.mass} kg")
print(f"Auto-calculated Caliber: {proj.diameter} m")
print(f"Auto-calculated I_x: {proj.i_x}")
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
