import numpy as np
from ballistics.fracture_v2 import FractureEngineV2

def test_grady_size_scaling():
    material_toughness = 50000.0 # J/m2
    density = 7850.0
    sound_speed = 5000.0

    s_slow = FractureEngineV2.calculate_fragment_size_grady(1000.0, material_toughness, density, sound_speed)
    s_fast = FractureEngineV2.calculate_fragment_size_grady(10000.0, material_toughness, density, sound_speed)

    # Faster strain rate should result in smaller fragments
    assert s_fast < s_slow

def test_grady_kipp_distribution():
    total_mass = 10.0
    strain_rate = 5000.0
    material_params = {
        'toughness': 50000.0,
        'density': 7850.0,
        'sound_speed': 5000.0
    }
    num = 100

    masses = FractureEngineV2.sample_grady_kipp_distribution(total_mass, strain_rate, material_params, num)

    assert len(masses) == num
    assert np.isclose(np.sum(masses), total_mass)
    assert np.all(masses > 0)

def test_strain_rate_estimation():
    v_det = 8000.0 # m/s (Comp B)
    r = 0.05 # 50mm

    edot = FractureEngineV2.estimate_strain_rate(v_det, r, 0.005)
    # edot ~ (0.25 * 8000) / 0.05 = 2000 / 0.05 = 40000 s^-1
    assert np.isclose(edot, 40000.0)
