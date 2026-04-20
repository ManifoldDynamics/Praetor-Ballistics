# Wilson Ballistic Suite (WBS) - V2 Proprietary Release

Wilson Ballistic Suite (WBS) is an industry-leading 6-Degree-of-Freedom (6-DoF) ballistics, lethality, and aerothermodynamics engine. Built on a hybrid architecture, it utilizes a modular Python frontend powered by a natively compiled, high-performance C++ backend.

V2 marks the transition to a **completely proprietary architecture**, replacing standard empirical models with advanced, custom-derived physical algorithms for unparalleled accuracy in extreme flight regimes.

## V2 Proprietary Enhancements

### 1. Advanced Interior Ballistics (V2)
The V2 Interior Solver moves beyond simple energy conservation, implementing convective heat loss and support for multi-perforated propellant grains with progressive-to-degressive burn transitions.

### 2. High-Fidelity Aerodynamics Engine (V2)
Our new proprietary aero-predictor replaces Mach-based lookups with geometric physics:
- **Van Driest II Transformation**: Calculates compressible turbulent skin friction.
- **Sutherland’s Law Integration**: Dynamic viscosity is computed based on local air temperature.
- **Shock-Expansion Correlation**: A proprietary model for supersonic wave drag.
- **Korst-McCoy Base Pressure**: Accurate modeling of base drag.

### 3. Terminal Ballistics & Lethality (V2)
State-of-the-art lethality modeling:
- **Multi-Layer Armor Penetration**: Simulates perforation through spaced armor and ERA.
- **Mott Fragmentation Distribution**: Stochastic fragment mass sampling.

### 4. Active Propulsion & Guidance (V2)
Advanced flight control for smart munitions:
- **Multi-Stage Rocket Motors**: Supports discrete thrust profiles and mass-decay.
- **Augmented Proportional Navigation (APN)**: Advanced guidance law that compensates for target maneuvering acceleration.

### 5. Advanced Aerothermodynamics (V2)
High-fidelity thermal modeling:
- **1D Radial Nodal Conduction**: Finite-difference conduction solver tracking temperature gradients through the skin.

### 6. Strategic Targeting & Engagement (V2)
Proprietary multi-objective intercept optimization:
- **Predictive Multi-Objective Intercept**: Optimizes trajectories for minimum miss distance, specific impact angles, and maximum kinetic energy.

### 7. High-Fidelity Environmental Physics (V2)
Next-generation planetary and atmospheric modeling:
- **J2 Gravity Perturbation**: Accounts for Earth's oblateness (nodal regression and perigee shift), critical for long-range and sub-orbital flight.
- **Expanded Atmospheric Model**: Proprietary implementation of the full 1976 US Standard Atmosphere up to 100km, including the Stratosphere and Mesosphere layers.
- **Geopotential Correction**: Dynamically adjusts altitude calculations to account for varying gravitational strength with height.

## Installation

```bash
# Install WBS V2
pip install -e .
```

## Python API Examples

### V2 High-Fidelity Environment

```python
from ballistics.environment import EarthModel, StandardAtmosphere
# J2 gravity requires position vector relative to Earth center
g_vec = EarthModel.gravity(altitude=0, version=2, pos_vec=[6378137, 0, 0])

# Access stratosphere properties
atm = StandardAtmosphere()
props = atm.get_properties(altitude=30000, version=2)
print(f"Stratosphere Density: {props['density']:.4f} kg/m^3")
```
