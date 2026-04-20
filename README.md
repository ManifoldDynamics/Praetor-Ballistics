# Wilson Ballistic Suite (WBS) - V2 Proprietary Release

Wilson Ballistic Suite (WBS) is an industry-leading 6-Degree-of-Freedom (6-DoF) ballistics, lethality, and aerothermodynamics engine. Built on a hybrid architecture, it utilizes a modular Python frontend powered by a natively compiled, high-performance C++ backend.

V2 marks the transition to a **completely proprietary architecture**, replacing standard empirical models with advanced, custom-derived physical algorithms for unparalleled accuracy in extreme flight regimes.

## V2 Proprietary Enhancements

### 1. Advanced Interior Ballistics (V2)
The V2 Interior Solver moves beyond simple energy conservation, implementing:
- **Convective Heat Loss**: Models energy dissipation to barrel walls using a pressure-dependent convective coefficient.
- **Advanced Grain Geometry**: Support for multi-perforated propellant grains with progressive-to-degressive burn transitions (Mott/STANAG compliant).

### 2. High-Fidelity Aerodynamics Engine (V2)
Our new proprietary aero-predictor replaces Mach-based lookups with geometric physics:
- **Van Driest II Transformation**: Calculates compressible turbulent skin friction.
- **Shock-Expansion Correlation**: A proprietary model for supersonic wave drag.
- **Korst-McCoy Base Pressure**: Accurate modeling of base drag and boattail flow separation.

### 3. Terminal Ballistics & Lethality (V2)
State-of-the-art lethality modeling:
- **Multi-Layer Armor Penetration**: Simulates perforation through spaced armor and ERA using the Thor empirical suite.
- **Mott Fragmentation Distribution**: Stochastic fragment mass sampling based on casing material and explosive properties.

### 4. Active Propulsion & Guidance (V2)
Advanced flight control for smart munitions:
- **Multi-Stage Rocket Motors**: Supports discrete thrust profiles and mass-decay.
- **Augmented Proportional Navigation (APN)**: Advanced guidance law that compensates for target maneuvering acceleration.

### 5. Advanced Aerothermodynamics (V2)
High-fidelity thermal modeling:
- **1D Radial Nodal Conduction**: Finite-difference conduction solver tracking temperature gradients across multiple discrete nodes through the projectile skin.

### 6. Strategic Targeting & Engagement (V2)
Proprietary multi-objective intercept optimization:
- **Predictive Multi-Objective Intercept**: Optimizes trajectories simultaneously for minimum miss distance, specific impact angles (AoA), and maximum terminal kinetic energy.
- **Engagement Priority Tuning**: Allows the user to weight accuracy vs. lethality (energy) during the targeting solution search.

## Installation

```bash
# Install WBS V2 (compiles the C++ core extensions automatically)
pip install -e .
```

## Python API Examples

### V2 Strategic Targeting

```python
from ballistics.targeting import TargetingSystem
# ... setup solver ...
ts = TargetingSystem(solver)
res = ts.find_firing_solution(target_pos=[5000, 0, 100], v0=850, spin=1800,
                             version=2, impact_angle_deg=30.0)
```
