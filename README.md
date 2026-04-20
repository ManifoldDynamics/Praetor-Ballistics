# Wilson Ballistic Suite (WBS) - V2 Proprietary Release

Wilson Ballistic Suite (WBS) is an industry-leading 6-Degree-of-Freedom (6-DoF) ballistics, lethality, and aerothermodynamics engine. Built on a hybrid architecture, it utilizes a modular Python frontend powered by a natively compiled, high-performance C++ backend.

V2 marks the transition to a **completely proprietary architecture**, replacing standard empirical models with advanced, custom-derived physical algorithms for unparalleled accuracy in extreme flight regimes.

## V2 Proprietary Enhancements

### 1. Advanced Interior Ballistics (V2)
The V2 Interior Solver moves beyond simple energy conservation, implementing:
- **Convective Heat Loss**: Models energy dissipation to barrel walls using a pressure-dependent convective coefficient.
- **Advanced Grain Geometry**: Support for multi-perforated propellant grains with progressive-to-degressive burn transitions (Mott/STANAG compliant).
- **Lagrange Gradient Effects**: Accounts for gas velocity gradients within the chamber for higher-fidelity pressure curves.

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
- **Ray-Traced Lethality**: Integrates with `trimesh` to perform high-fidelity fragment-target interaction simulations in 3D.

## Key Features

- **Hybrid C++/Python Architecture:** Heavy differential equation derivatives and 3D CFD finite-volume grids are evaluated in native C++.
- **6-DoF Physics Solver:** Accurate rigid-body modeling with quaternions and euler-angle stability guards.
- **Hypersonic Aerothermodynamics:** Stagnation point heating (Fay-Riddell) and radiative cooling modeling.
- **Monte Carlo Dispersion:** Parallelized simulation of variance in environmental and muzzle conditions.
- **Live Weather Integration:** Real-time atmospheric correction via Open-Meteo API.

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd ballistics

# Install WBS V2 (compiles the C++ core extensions automatically)
pip install -e .
```

## Python API Examples

### V2 Interior Ballistics

```python
from ballistics.interior_solver import InteriorSolver
# ... setup gun and charge ...
solver = InteriorSolver(gun, charge, version=2)
res = solver.solve()
print(f"Proprietary MV: {res.muzzle_velocity:.1f} m/s")
```

### V2 Aerodynamics

```python
from ballistics.projectile import Aerodynamics
# ... define geometry ...
aero = Aerodynamics.from_predictor_v2(geometry)
```

### V2 Terminal Ballistics

```python
from ballistics.terminal_v2 import TerminalBallisticsV2
layers = [{'thickness_mm': 10, 'type': 'era'}, {'thickness_mm': 20, 'type': 'rha'}]
res = TerminalBallisticsV2.multi_layer_penetration(v_impact=1200, m_frag=0.05, d_frag=0.01, layers=layers)
```
