import numpy as np
from ballistics.guidance import ProportionalNavigation

def test_pronav_head_on():
    pn = ProportionalNavigation(nav_constant=4.0, max_g=30.0, activation_time_s=0.0)

    # Missile flying directly along X at 1000 m/s
    m_pos = [0.0, 0.0, 0.0]
    m_vel = [1000.0, 0.0, 0.0]

    # Target sitting 1000m away on X, perfectly stationary
    t_pos = [1000.0, 0.0, 0.0]
    t_vel = [0.0, 0.0, 0.0]

    # Since they are on a perfect collision course (LOS rate = 0), commanded accel should be 0
    a_cmd = pn.get_commanded_acceleration(1.0, m_pos, m_vel, t_pos, t_vel)
    assert np.allclose(a_cmd, [0.0, 0.0, 0.0])

def test_pronav_crossing_target():
    pn = ProportionalNavigation(nav_constant=4.0, max_g=30.0, activation_time_s=0.0)

    # Missile flying directly along X at 1000 m/s
    m_pos = [0.0, 0.0, 0.0]
    m_vel = [1000.0, 0.0, 0.0]

    # Target is 1000m away on X, but moving 100 m/s to the right (+Y)
    t_pos = [1000.0, 0.0, 0.0]
    t_vel = [0.0, 100.0, 0.0]

    a_cmd = pn.get_commanded_acceleration(1.0, m_pos, m_vel, t_pos, t_vel)

    # Missile should command a positive Y acceleration to turn and intercept
    assert a_cmd[1] > 0.0

    # Should not command X or Z
    assert np.isclose(a_cmd[0], 0.0)
    assert np.isclose(a_cmd[2], 0.0)

def test_pronav_max_g():
    pn = ProportionalNavigation(nav_constant=4.0, max_g=10.0, activation_time_s=0.0)
    max_a_ms2 = 10.0 * 9.80665

    # Target crossing extremely fast (should require more than 10Gs)
    m_pos = [0.0, 0.0, 0.0]
    m_vel = [1000.0, 0.0, 0.0]
    t_pos = [1000.0, 0.0, 0.0]
    t_vel = [0.0, 5000.0, 0.0]

    a_cmd = pn.get_commanded_acceleration(1.0, m_pos, m_vel, t_pos, t_vel)

    # Acceleration should be clipped to exactly max_a_ms2
    a_mag = np.linalg.norm(a_cmd)
    assert np.isclose(a_mag, max_a_ms2)
