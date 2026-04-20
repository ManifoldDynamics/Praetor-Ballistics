# Wilson Ballistic Suite (WBS) - V2 Proprietary Release

Wilson Ballistic Suite (WBS) is an industry-leading 6-Degree-of-Freedom (6-DoF) ballistics, lethality, and aerothermodynamics engine. Built on a hybrid architecture, it utilizes a modular Python frontend powered by a natively compiled, high-performance C++ backend.

V2 marks the transition to a **completely proprietary architecture**, replacing standard empirical models with advanced, custom-derived physical algorithms for unparalleled accuracy in extreme flight regimes.

## V2 Proprietary Enhancements

### 1. Advanced Interior Ballistics (V2)
The V2 Interior Solver implements convective heat loss and support for multi-perforated propellant grains with progressive-to-degressive burn transitions.

### 2. High-Fidelity Aerodynamics Engine (V2)
Our new proprietary aero-predictor replaces Mach-based lookups with geometric physics including Van Driest II Transformation and Korst-McCoy base pressure modeling.

### 3. Terminal Ballistics & Lethality (V2)
State-of-the-art lethality modeling including multi-layer armor penetration and dynamic fracture mechanics (Mott-Grady theory).

### 4. Active Propulsion & Guidance (V2)
Advanced flight control for smart munitions with multi-stage rocket motors and Augmented Proportional Navigation (APN).

### 5. Advanced Aerothermodynamics (V2)
High-fidelity 1D Radial Nodal Conduction solver for tracking temperature gradients through projectile skins during hypersonic flight.

### 6. Strategic Targeting & Engagement (V2)
Multi-objective intercept optimization for precision, impact geometry, and terminal kinetic energy.

### 7. High-Fidelity Environmental Physics (V2)
J2 Gravity Perturbation and an expanded 100km atmospheric model.

### 8. Advanced Stochastic Dispersion (V2)
Gaussian Copula sampling and von Karman turbulence modeling for high-fidelity Monte Carlo simulations.

### 9. Proprietary High-Order CFD (V2)
A state-of-the-art C++ Computational Fluid Dynamics core:
- **5th-Order WENO Reconstruction**: Captures complex supersonic shockwave interactions and contact discontinuities with extreme precision and minimal numerical dissipation.
- **HLLC Riemann Solver**: Improved resolution of shock fronts and contact surfaces compared to standard Rusanov/Lax-Friedrichs schemes.
- **3rd-Order TVD Runge-Kutta**: High-order temporal integration for stable, accurate time-accurate flow simulations.

## Installation

```bash
# Install WBS V2 (compiles C++ cores automatically)
pip install -e .
```

## Python API Examples

### V2 High-Order CFD

```python
from ballistics.cfd_v2 import CFDPipelineV2
pipeline = CFDPipelineV2("projectile_cad.stl")
# Execute high-order WENO solver
results = pipeline.run_simulation_v2(mach=3.5, altitude_m=15000, env_atm=atm)
print(f"High-Order Cd: {results['cd']:.4f}")
```
