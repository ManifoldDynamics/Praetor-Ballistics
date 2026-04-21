import numpy as np
from ballistics.separation_v2 import MultiBodyManagerV2
from ballistics.eom import get_multibody_eom
from unittest.mock import MagicMock

def test_interference_drag():
    v_rel = np.array([0, 0, 0])
    dist_close = np.array([0.1, 0, 0])
    dist_far = np.array([10.0, 0, 0])

    f_close = MultiBodyManagerV2.calculate_interference_drag(dist_close, v_rel, 0)
    f_far = MultiBodyManagerV2.calculate_interference_drag(dist_far, v_rel, 0)

    # Close proximity should have more interference (reduced drag in this simple model)
    assert f_close < f_far
    assert f_far <= 1.0

def test_multibody_eom_plumbing():
    # Mock 2 bodies
    b1 = MagicMock(); b2 = MagicMock()
    b1.mass = 1.0; b2.mass = 0.5
    b1.reference_area = 0.01; b2.reference_area = 0.005
    b1.diameter = 0.05; b2.diameter = 0.03

    a1 = MagicMock(); a2 = MagicMock()

    # Combined state (2 * 13 = 26)
    full_state = np.zeros(26)
    full_state[0:3] = [0, 0, 100] # body 1 pos
    full_state[13:16] = [0, 1, 100] # body 2 pos (1m separation)

    # Mock environment
    env_atm = MagicMock()
    env_atm.get_properties.return_value = {'pressure': 101325, 'density': 1.225, 'speed_of_sound': 340}
    env_earth = MagicMock()
    env_earth.gravity.return_value = 9.81
    env_earth.coriolis_acceleration.return_value = np.zeros(3)

    # The get_multibody_eom will call get_eom internally
    # which we can't easily mock since it is in the same module.
    # But we can check that it returns the correct size.
    dot = get_multibody_eom(0.1, full_state, [b1, b2], [a1, a2], env_atm, env_earth)

    assert len(dot) == 26
