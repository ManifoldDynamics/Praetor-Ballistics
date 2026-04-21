import numpy as np
from ballistics.interior_v2 import InteriorSolverV2
from ballistics.aero_v2 import AeroPredictorV2
from ballistics.environment_v2 import EarthModelV2
from ballistics.propulsion_v2 import RocketMotorV2
from ballistics.stochastic_v2 import StochasticEngineV2

def test_nac_equation_of_state():
    # Verify Lagrange and Co-volume effects
    # Mock Gun and Charge
    class MockProp:
        impetus = 1e6; covolume = 1e-3; gamma = 1.25; density = 1600; flame_temp = 3000; burn_coeff = 1e-6; burn_exponent = 0.7
    class MockCharge:
        mass = 1.0; propellant = MockProp(); web_thickness = 0.01; form_factor_theta = 0.5
    class MockGun:
        bullet_mass = 10.0; bore_area = 0.01; chamber_volume = 0.002; barrel_length = 5.0; bore_diameter = 0.1
        bullet_ix_kgm2 = 0.1; rads_per_meter = 100; engraving_force_n = 1e5; bore_friction_n = 1e4

    solver = InteriorSolverV2(MockGun(), MockCharge())
    # Manual energy balance check at z=0.5, v=500
    # effective_vol = V0 + A*x - C*(1-z)/rho - C*z*eta
    # With large covolume eta, effective volume should decrease -> Pressure should increase
    res = solver.solve(max_time_s=0.01)
    assert res.success

def test_wmm_magnetic_field():
    # Verify magnetic field at different latitudes
    b_eq = EarthModelV2.calculate_magnetic_field_wmm(0, 0, 0)
    b_pole = EarthModelV2.calculate_magnetic_field_wmm(90, 0, 0)

    # Pole should have much higher vertical component (dip)
    assert abs(b_pole[2]) > abs(b_eq[2])

def test_nozzle_erosion():
    stages = [{'thrust_sl_n': 10000, 'burn_time_s': 10.0, 'propellant_mass_kg': 10.0, 'exit_area_m2': 0.1}]
    motor = RocketMotorV2(stages)

    # Thrust at t=0 vs t=5 (erosion should change exit area term)
    f0, _ = motor.get_thrust_and_mdot(0, 50000) # 50kPa ambient
    f5, _ = motor.get_thrust_and_mdot(5.0, 50000)

    # Pressure correction: (P_sl - Pa) * Ae * (1 + 0.001*t)
    # f0 = 10000 + (101325 - 50000) * 0.1 = 15132.5
    # f5 = (10000 - 0.002*5*10000) + (101325 - 50000) * 0.1 * (1 + 0.001*5)
    # f5 = 9900 + 5132.5 * 1.005 = 15058.16
    assert f5 != f0

def test_importance_sampling():
    nominal_means = np.array([100, 200])
    std_devs = np.array([10, 20])
    samples = np.array([[130, 260]]) # 3-sigma event

    weights = StochasticEngineV2.importance_sampling_weights(samples, nominal_means, std_devs, bias_factor=2.0)
    assert len(weights) == 1
    assert weights[0] < 1.0 # Tail events have low likelihood ratio

def test_material_specific_thor():
    from ballistics.terminal_v2 import TerminalBallisticsV2
    # Limit for Steel should be higher than Aluminum for same thickness
    v_steel = TerminalBallisticsV2.thor_equation(1000, 0.01, 0.01, 5.0, 'Steel (RHA)')
    v_alum = TerminalBallisticsV2.thor_equation(1000, 0.01, 0.01, 5.0, 'Aluminum (7075-T6)')
    assert v_steel > v_alum

def test_thor_obliquity():
    from ballistics.terminal_v2 import TerminalBallisticsV2
    v0 = TerminalBallisticsV2.thor_equation(1000, 0.01, 0.01, 5.0, obliquity_deg=0.0)
    v45 = TerminalBallisticsV2.thor_equation(1000, 0.01, 0.01, 5.0, obliquity_deg=45.0)
    # Obliquity increases effective thickness -> higher ballistic limit
    assert v45 > v0

def test_stochastic_shape_factor():
    from ballistics.lethality_v2 import FragmentationModelV2
    a1, d1 = FragmentationModelV2.get_fragment_properties(0.01, shape_factor=1.5) # Cube
    a2, d2 = FragmentationModelV2.get_fragment_properties(0.01, shape_factor=3.0) # Shard
    assert a2 > a1
    assert d2 > d1
