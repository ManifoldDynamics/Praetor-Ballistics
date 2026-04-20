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
- **Predictive Multi-Objective Intercept**: Optimizes trajectories for minimum miss distance, specific impact angles, and maximum kinetic energy.

### 7. High-Fidelity Environmental Physics (V2)
Next-generation planetary and atmospheric modeling:
- **J2 Gravity Perturbation**: Accounts for Earth's oblateness.
- **Expanded Atmospheric Model**: Proprietary implementation of the full 1976 US Standard Atmosphere up to 100km.

### 8. Advanced Stochastic Dispersion (V2)
Next-generation Monte Carlo simulation for precision Munitions:
- **Gaussian Copula Sampling**: Proprietary implementation for correlated input variance (e.g., modeling the realistic coupling between muzzle velocity and propellant mass).
- **von Karman Gust Modeling**: Replaces constant wind noise with stochastic non-white turbulence profiles for realistic flight instability.
- **Bayesian Impact Probability (BIP)**: A high-precision engine for estimating Circular Error Probable (CEP) and Mean Point of Impact (MPI) with Bayesian uncertainty quantification.

## Installation

```bash
# Install WBS V2
pip install -e .
```

## Python API Examples

### V2 Monte Carlo Simulation

```python
from ballistics.monte_carlo import MonteCarloSimulator
# ... setup simulator ...
sim = MonteCarloSimulator(base_solver)
res = sim.run(num_shots=1000, target_plane='vertical', target_distance=2000,
             base_v0=850, base_pitch_rad=0.5, base_yaw_rad=0, base_spin_rads=1800,
             sd_v0_ms=2.0, sd_mass_kg=0.01, version=2)
print(f"Bayesian CEP 50: {res.cep_50:.2f} meters")
```
