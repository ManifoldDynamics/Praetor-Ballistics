import numpy as np
from ballistics.propulsion_v2 import RocketMotorV2

def test_multi_stage_thrust():
    stages = [
        {'thrust_sl_n': 1000.0, 'burn_time_s': 2.0, 'propellant_mass_kg': 5.0, 'exit_area_m2': 0.01},
        {'thrust_sl_n': 500.0, 'burn_time_s': 3.0, 'propellant_mass_kg': 2.0, 'exit_area_m2': 0.005}
    ]
    motor = RocketMotorV2(stages)

    # Stage 1
    f1, mdot1 = motor.get_thrust_and_mdot(1.0, 101325.0)
    assert f1 == 1000.0
    assert mdot1 == 2.5

    # Stage 2
    f2, mdot2 = motor.get_thrust_and_mdot(3.0, 101325.0)
    assert f2 == 500.0
    assert np.isclose(mdot2, 2.0/3.0)

    # Post burnout
    f3, mdot3 = motor.get_thrust_and_mdot(6.0, 101325.0)
    assert f3 == 0.0
    assert mdot3 == 0.0

def test_pressure_correction():
    stages = [{'thrust_sl_n': 1000.0, 'burn_time_s': 1.0, 'propellant_mass_kg': 1.0, 'exit_area_m2': 0.1}]
    motor = RocketMotorV2(stages)

    # Vacuum
    f_vac, _ = motor.get_thrust_and_mdot(0.5, 0.0)
    # F = 1000 + (101325 - 0) * 0.1 = 1000 + 10132.5 = 11132.5
    assert np.isclose(f_vac, 11132.5)

    # High pressure
    f_high, _ = motor.get_thrust_and_mdot(0.5, 200000.0)
    assert f_high < 1000.0

def test_mass_decay():
    stages = [{'thrust_sl_n': 1000.0, 'burn_time_s': 10.0, 'propellant_mass_kg': 10.0, 'exit_area_m2': 0.01}]
    motor = RocketMotorV2(stages)

    m0 = 50.0
    m_mid = motor.get_current_mass(5.0, m0)
    assert m_mid == 45.0

    m_end = motor.get_current_mass(15.0, m0)
    assert m_end == 40.0
