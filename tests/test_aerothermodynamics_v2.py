import numpy as np
from ballistics.aerothermodynamics_v2 import AerothermodynamicsV2
from ballistics.materials import Material

def test_fdm_conduction_derivatives():
    material = Material("Titanium (Ti-6Al-4V)")
    num_nodes = 5
    temperatures = np.array([500.0, 450.0, 400.0, 350.0, 300.0])

    q_conv = 1.0e6 # 1 MW/m2
    q_rad = 0.5e6
    r_nose = 0.01
    skin_thickness = 0.005

    dT_dt = AerothermodynamicsV2.calculate_derivatives(0, temperatures, q_conv, q_rad, r_nose, skin_thickness, material, num_nodes)

    assert len(dT_dt) == num_nodes
    # Surface should be heating up
    assert dT_dt[0] > 0
    # Heat should be flowing inwards
    assert dT_dt[1] > 0

def test_steady_state_gradient():
    material = Material("Steel (RHA)")
    num_nodes = 3
    # No external flux, uniform temperature
    temperatures = np.array([300.0, 300.0, 300.0])

    dT_dt = AerothermodynamicsV2.calculate_derivatives(0, temperatures, 0, 0, 0.01, 0.005, material, num_nodes)

    # All derivatives should be zero (or near zero due to Stefan-Boltzmann at 300K being non-zero)
    # Actually, q_rad at 300K is ~epsilon * sigma * 300^4 ~ 0.8 * 5.67e-8 * 8.1e9 ~ 367 W/m2.
    # So it will cool down slightly.
    assert dT_dt[0] < 0
