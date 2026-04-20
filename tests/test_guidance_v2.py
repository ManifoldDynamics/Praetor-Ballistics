import numpy as np
from ballistics.guidance_v2 import GuidanceV2

def test_apn_guidance():
    guidance = GuidanceV2(nav_constant=4.0, max_g=30.0, activation_time_s=0.0)

    m_p = np.array([0.0, 0.0, 0.0])
    m_v = np.array([500.0, 0.0, 0.0])
    t_p = np.array([1000.0, 100.0, 0.0])
    t_v = np.array([0.0, 0.0, 0.0])
    t_a = np.array([0.0, 10.0, 0.0]) # Target accelerating up

    a_cmd = guidance.augmented_pronav(1.0, m_p, m_v, t_p, t_v, t_a)

    assert a_cmd[1] > 0 # Should command acceleration towards target and its motion
    assert np.linalg.norm(a_cmd) <= guidance.max_accel

def test_ogl_guidance():
    guidance = GuidanceV2(nav_constant=3.0, max_g=30.0, activation_time_s=0.0)

    m_p = np.array([0.0, 0.0, 0.0])
    m_v = np.array([800.0, 0.0, 0.0])
    t_p = np.array([2400.0, 0.0, 0.0])
    t_v = np.array([0.0, 0.0, 0.0])

    # t_go = 3.0s
    a_cmd = guidance.optimal_guidance(0.0, m_p, m_v, t_p, t_v, 3.0)
    # With zero miss, a_cmd should be zero
    assert np.linalg.norm(a_cmd) < 1e-6

    # Offset target
    t_p_off = np.array([2400.0, 100.0, 0.0])
    a_cmd_off = guidance.optimal_guidance(0.0, m_p, m_v, t_p_off, t_v, 3.0)
    assert a_cmd_off[1] > 0
