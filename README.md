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
State-of-the-art C++ CFD core with 5th-Order WENO reconstruction and HLLC Riemann solver.

### 10. Multi-Body Separation Physics (V2)
Proprietary engine for modeling the simultaneous 6-DoF motion of multiple separating bodies:
- **Interference Aerodynamics**: Accounts for proximity-based drag variations and wake effects between bodies (e.g., discarding sabots or MIRVs).
- **Coupled Multibody Integration**: Simultaneous integration of $N$ rigid bodies with inter-body force coupling.
- **Separation Impulse Modeling**: Models the mechanical forces exerted during the deployment of sub-munitions or payload fairings.

## Installation

```bash
# Install WBS V2
pip install -e .
```
