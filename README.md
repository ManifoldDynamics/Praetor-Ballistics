# Wilson Ballistic Suite (WBS) - V1 Release

Wilson Ballistic Suite (WBS) is a next-generation 6-Degree-of-Freedom (6-DoF) ballistics and lethality engine. Built on a hybrid architecture, it utilizes a modular Python frontend powered by a natively compiled, high-performance C++ backend. This suite simulates incredibly realistic projectile trajectories, lethality, interior thermodynamics, and aerothermodynamics, designed as a modern alternative to industry-standard tools.

## Key Features

- **Hybrid C++/Python Architecture:** The heavy differential equation derivatives (14-state ODE solver) and the 3D CFD finite-volume grid are evaluated using a natively compiled C++ extension (`wbs_core` and `wbs_cfd_3d`) connected via `pybind11`. This allows computationally intensive tasks (like Monte Carlo dispersion and CFD) to run orders of magnitude faster than pure Python.
- **Wizard-Style GUI:** A streamlined PyQt6 desktop application featuring a step-by-step wizard flow: Main Menu -> Projectile Selection (Small Arms, Artillery, Missiles) -> Firearm/Barrel Designer -> Projectile CAD & Material -> Simulation Dashboard.
- **6-DoF Physics Solver:** Solves the complete equations of motion over time using Runge-Kutta (RK45) integration, accurately modeling a rigid body's translation and 3D rotation (via quaternions).
- **Interior Ballistics Thermodynamics:** Solves lumped-parameter thermodynamic differential equations (like STANAG 4367) to calculate the pressure curve, burn fraction, muzzle velocity, and resulting spin rate based on chamber volume, twist rate, engraving force, bore friction, charge mass, and propellant type. Includes a database of standard energetic materials.
- **True 3D CFD (Navier-Stokes/Euler) Solver:** Execute a native C++ 3D Cartesian Finite Volume Method (FVM) Euler solver directly from the GUI. It voxelizes custom STL meshes to calculate exact pressure drag and lift coefficients over a body at any Mach number, complete with supersonic shockwave capturing.
- **Empirical Aero Predictor (Datcom):** Automatically generates Mach-dependent Drag ($C_D$) and Lift ($C_L$) curves using Modified Newtonian Impact Theory and Korst base pressure equations, based solely on the projectile's nose, body, and boattail dimensions.
- **Monte Carlo Dispersion:** Simulates $N$ parallel shots utilizing Python `multiprocessing` to introduce variance into projectile mass, muzzle velocity, wind speed, and firing angles, calculating the resulting Circular Error Probable (CEP) and Mean Point of Impact (MPI).
- **Lethality & Ray-Tracing:** Computes warhead fragmentation using the Gurney equations and casts hundreds of individual fragments against a 3D Target STL using `trimesh` ray-tracing to calculate hit probability and armor penetration for each fragment.
- **Active Propulsion & Smart Munitions:** Supports modeling rocket-assisted projectiles (RAP) or missiles via configurable thrust vectors. Includes a Guidance, Navigation, and Control (GNC) module utilizing Proportional Navigation to actively steer towards dynamic, moving targets.
- **Hypersonic Aerothermodynamics:** Simulates convective stagnation point heating (Fay-Riddell) and Stefan-Boltzmann radiative cooling over a database of aerospace materials (Tungsten, Titanium, Inconel) to calculate instantaneous nose temperature, alerting the user if structural melting points are exceeded.
- **Targeting & Zeroing System:** Iteratively solves for the exact Elevation (Pitch) and Azimuth (Yaw) required to intercept a specific 3D coordinate, accounting for spin drift, Coriolis effect, and aerodynamic drop.
- **Terminal Ballistics:** Includes standard empirical armor penetration formulas (`De Marre`, `Krupp`, `Lanz-Odermatt` for APFSDS) to estimate lethality against armor upon target impact.
- **Environmental & Live Weather Modeling:** Uses standard models for Earth's gravity (with altitude decay), Coriolis effect, and advanced 3D layered wind profiles. Supports **Live Weather Fetching** using Open-Meteo GPS coordinates, adjusting air density based on humidity via virtual temperature.
- **CAD Integration & PyVista Visualization:** Ingest STL files directly to automatically calculate the projectile's Mass, Caliber, and Principal Moments of Inertia ($I_x$, $I_y$). Renders stunning, interactive 3D flight paths and lethality impacts directly from the GUI.

## Installation

WBS utilizes a hybrid C++/Python architecture. `setuptools` and `pybind11` will automatically compile the core C++ extensions when you install the package. Ensure you have a standard C++11 compiler installed on your system (like GCC or MSVC).

```bash
# Clone the repository
git clone <repo-url>
cd ballistics

# Install WBS locally (compiles the C++ core automatically)
pip install -e .
```

## Desktop GUI Quick Start

The easiest way to interact with the engine is via the built-in PyQt6 graphical user interface.

```bash
python gui.py
```

The app will guide you through a step-by-step wizard:
1. **Projectile Category:** Choose between Small Arms, Artillery, or Missile to pre-populate appropriate starting values.
2. **Firearm & Barrel Designer:** Configure chamber volume, rifling twist rate, sliding friction, engraving force, and propellant thermochemistry to simulate the pressure curve and muzzle velocity.
3. **Projectile Designer:** Configure exterior characteristics. Upload an STL CAD file to auto-generate physical properties, or run an Empirical Datcom / 3D CFD analysis to generate aerodynamic curves. Enable Hypersonics or Active Rocket Propulsion here.
4. **Simulation Dashboard:** Configure live weather, 3D target coordinates, and dispersion settings. Click "Calculate Firing Solution" or "Run Monte Carlo" to run the C++ numerical backend and view 2D/3D visualizations.

You can use `File -> Save` at any time to save your entire workspace as a `.blst` JSON project file.

## Python API Examples

WBS is fully accessible as a standard Python library for scripting or headless execution.

### Interior Ballistics Thermodynamics

```python
from ballistics.interior_ballistics import GunSystem, Charge
from ballistics.propellants import Propellant
from ballistics.interior_solver import InteriorSolver

# Model a generic 5.56 NATO Rifle (1:7 Twist Rate)
gun = GunSystem(
    chamber_volume_m3=0.000002,
    barrel_length_m=0.5,
    bore_diameter_m=0.00556,
    bullet_mass_kg=0.004,
    bullet_ix_kgm2=1.5e-8,
    twist_rate_in_per_turn=7.0
)

# Load a Fast Rifle Propellant from the thermodynamic database
prop = Propellant("Fast Rifle Powder (Extruded)")
charge = Charge(propellant=prop, mass_kg=0.0016, web_thickness_m=0.0005)

solver = InteriorSolver(gun, charge)
res = solver.solve()

print(f"Muzzle Velocity: {res.muzzle_velocity:.1f} m/s")
print(f"Spin Rate: {res.spin_rate_rads:.1f} rad/s")
print(f"Peak Pressure: {res.peak_pressure / 1e6:.1f} MPa")
```

### Exterior Ballistics & Targeting

```python
import numpy as np
from ballistics.environment import EarthModel
from ballistics.weather import LiveWeather
from ballistics.projectile import Projectile, Aerodynamics
from ballistics.solver import Solver6DoF
from ballistics.targeting import TargetingSystem

# 1. Fetch Live Weather for a location
env_atm = LiveWeather.fetch_atmosphere(latitude=39.2508, longitude=-106.2925)
env_earth = EarthModel()

# 2. Define Projectile from an STL CAD model
proj = Projectile.from_stl("test_bullet.stl", density_kg_m3=11340.0)
aero = Aerodynamics.g7() # Or Aerodynamics.from_csv()

# 3. Setup Solver
solver = Solver6DoF(proj, aero, env_atm, env_earth)

# 4. Zero the weapon onto a Target Intercept
targeting = TargetingSystem(solver)
target_coords = [2500.0, 0.0, 50.0] # 2.5km away, 50m high

res = targeting.find_firing_solution(target_coords, v0=800.0, spin=1800.0)

if res.success:
    print(f"Required Pitch: {np.rad2deg(res.pitch):.2f} degrees")
    print(f"Required Yaw: {np.rad2deg(res.yaw):.2f} degrees")
```
