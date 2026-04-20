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
- **Van Driest II Transformation**: Calculates compressible turbulent skin friction, essential for high-transonic and supersonic stability.
- **Sutherland’s Law Integration**: Dynamic viscosity is computed based on local air temperature, improving Reynolds number fidelity.
- **Shock-Expansion Correlation**: A proprietary model for supersonic wave drag that outranks traditional Modified Newtonian Impact Theory.
- **Korst-McCoy Base Pressure**: Accurate modeling of base drag and boattail flow separation.

### 3. Terminal Ballistics & Lethality (V2)
State-of-the-art lethality modeling for fragmentation warheads:
- **Multi-Layer Armor Penetration**: Simulates perforation through spaced armor and Explosive Reactive Armor (ERA) using the Thor empirical suite.
- **Lambert Correlation**: Predicts fragment residual velocity and mass loss during target perforation.
- **Mott Fragmentation Distribution**: Stochastic fragment mass sampling based on casing material and explosive properties.

### 4. Active Propulsion & Guidance (V2)
Advanced flight control for smart munitions and missiles:
- **Multi-Stage Rocket Motors**: Supports discrete thrust profiles and mass-decay for booster/sustainer configurations.
- **Atmospheric Pressure Correction**: Proprietary thrust calculation ($F = F_{sl} + (P_{sl} - P_a) A_e$) for varying altitudes.
- **Augmented Proportional Navigation (APN)**: Advanced guidance law that compensates for target maneuvering acceleration.

### 5. Advanced Aerothermodynamics (V2)
High-fidelity thermal modeling for hypersonic flight:
- **1D Radial Nodal Conduction**: Replaces simple lumped-mass models with a finite-difference radial heat conduction solver.
- **Internal Thermal Gradients**: Tracks temperature soaking from the outer skin to the internal core across multiple discrete nodes.
- **Structural Integrity Monitoring**: Allows for precise calculation of thermal stress and structural failure points based on material-specific thermal conductivity.

## Key Features

- **Hybrid C++/Python Architecture:** Heavy differential equation derivatives and 3D CFD finite-volume grids are evaluated in native C++.
- **6-DoF Physics Solver:** Accurate rigid-body modeling with quaternions and euler-angle stability guards.
- **Live Weather Integration:** Real-time atmospheric correction via Open-Meteo API.

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd ballistics

# Install WBS V2 (compiles the C++ core extensions automatically)
pip install -e .
```
