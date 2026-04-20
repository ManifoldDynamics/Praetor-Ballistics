# Wilson Ballistic Suite (WBS) - V2 Proprietary Release

Wilson Ballistic Suite (WBS) is an industry-leading 6-Degree-of-Freedom (6-DoF) ballistics, lethality, and aerothermodynamics engine. Built on a hybrid architecture, it utilizes a modular Python frontend powered by a natively compiled, high-performance C++ backend.

V2 marks the transition to a **completely proprietary architecture**, replacing standard empirical models with advanced, custom-derived physical algorithms for unparalleled accuracy in extreme flight regimes.

## V2 Proprietary Enhancements

### 1. Advanced Interior Ballistics (V2)
The V2 Interior Solver moves beyond simple energy conservation, implementing convective heat loss and support for multi-perforated propellant grains with progressive-to-degressive burn transitions.

### 2. High-Fidelity Aerodynamics Engine (V2)
Our new proprietary aero-predictor replaces Mach-based lookups with geometric physics including Van Driest II Transformation and Korst-McCoy base pressure modeling.

### 3. Terminal Ballistics & Lethality (V2)
State-of-the-art lethality modeling:
- **Multi-Layer Armor Penetration**: Simulates perforation through spaced armor and ERA using the Thor empirical suite.
- **Dynamic Fracture Mechanics**: Replaces empirical mass distributions with a proprietary physics-based fracture engine.
- **Mott-Grady High Strain-Rate Breaking**: Predicts casing breakup and fragment size based on explosive energy balance and material toughness.
- **Stochastic Fragment Properties**: Generates variable fragment shapes and masses using Grady-Kipp statistics.

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
Next-generation Monte Carlo simulation:
- **Gaussian Copula Sampling**: Models correlated input variance.
- **von Karman Gust Modeling**: Stochastic non-white turbulence profiles for wind.

## Installation

```bash
# Install WBS V2
pip install -e .
```

## Python API Examples

### V2 Dynamic Fragmentation

```python
from ballistics.lethality_v2 import FragmentationModelV2
# Generate fragments using high-strain-rate physics
material_params = {'toughness': 50000, 'density': 7850, 'sound_speed': 5000}
masses = FragmentationModelV2.generate_fragments_v2(total_mass=10.0, explosive_v_det=8000,
                                                   casing_radius=0.05, material_params=material_params,
                                                   num_fragments=500)
```
