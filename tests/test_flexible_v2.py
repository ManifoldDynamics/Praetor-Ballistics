import numpy as np
from ballistics.projectile import Projectile
from ballistics.flexible_v2 import FlexibleBeamModelV2

def test_modal_frequencies():
    proj = Projectile(mass=0.045, diameter=0.009, i_x=1e-6, i_y=1e-5, youngs_modulus=200e9)
    flex = FlexibleBeamModelV2(proj)

    # First mode should be in the hundreds/thousands of Hz range for a small projectile
    assert flex.omega_n[0] > 100.0
    assert flex.omega_n[1] > flex.omega_n[0]

def test_aeroelastic_corrections():
    proj = Projectile(mass=0.045, diameter=0.009, i_x=1e-6, i_y=1e-5)
    flex = FlexibleBeamModelV2(proj)

    # No deformation -> No correction
    eta_zero = np.zeros(2)
    corr_zero = flex.get_aeroelastic_corrections(eta_zero, 1.5)
    assert corr_zero['cd'] == 0.0
    assert corr_zero['cma'] == 0.0

    # Positive deformation -> Increased Cd, Decreased Cma
    eta_pos = np.array([0.01, 0.0])
    corr_pos = flex.get_aeroelastic_corrections(eta_pos, 1.5)
    assert corr_pos['cd'] > 0.0
    assert corr_pos['cma'] < 0.0

def test_modal_derivatives():
    proj = Projectile(mass=0.045, diameter=0.009, i_x=1e-6, i_y=1e-5)
    flex = FlexibleBeamModelV2(proj)

    eta = np.zeros(2)
    eta_dot = np.zeros(2)
    # High q_dyn and alpha should drive deformation
    eta_ddot = flex.calculate_modal_derivatives(0.0, eta, eta_dot, q_dyn=100000, mach=2.0, alpha=0.1)

    assert eta_ddot[0] > 0
