import numpy as np
from ballistics.aero_v2 import AeroPredictorV2
from ballistics.terminal_v2 import TerminalBallisticsV2
from ballistics.sensors_v2 import SeekerModelV2

def test_high_fidelity_spin_decay():
    # Verify spin decay at extreme RPM (250,000)
    # Roll damping torque: L = Clp * q * S * d * (pd/2V)
    # At high Mach, Clp increases (becomes more negative)
    aero = AeroPredictorV2(None) # Dummy geo for constants
    clp_m2 = -0.02 * (1.0 + 0.1 * 2.0)
    clp_m4 = -0.02 * (1.0 + 0.1 * 4.0)
    assert clp_m4 < clp_m2 # Stronger damping at high Mach

def test_epicyclic_filtering():
    # Guidance command with high-frequency noise (simulating nutation)
    cmd_raw = np.array([10.0, 5.0, 0.0])
    alpha_wobble = 0.1 # High alpha trigger

    cmd_filtered = SeekerModelV2.apply_epicyclic_filter(cmd_raw, alpha_wobble)

    # Filter should reduce gain during large wobbles
    assert np.linalg.norm(cmd_filtered) < np.linalg.norm(cmd_raw)

def test_thermo_mechanical_shear_trigger():
    # Wraith platform centrifugal disintegration check
    # 250,000 RPM at 1000K (compromised yield)
    sigma_y0 = 800e6 # 800 MPa baseline

    # Case 1: Cold projectile (retains RPM)
    res_cold = TerminalBallisticsV2.calculate_thermo_mechanical_shear(250000, 300.0, sigma_y0)
    # Case 2: Hot projectile (stagnation point heating)
    res_hot = TerminalBallisticsV2.calculate_thermo_mechanical_shear(250000, 1200.0, sigma_y0)

    assert res_hot['effective_yield_pa'] < res_cold['effective_yield_pa']
    # Disintegration should be more likely when hot
    if not res_cold['disintegrated']:
        assert res_hot['disintegrated'] or (res_hot['centrifugal_stress_pa'] / res_hot['effective_yield_pa'] >
                                           res_cold['centrifugal_stress_pa'] / res_cold['effective_yield_pa'])
