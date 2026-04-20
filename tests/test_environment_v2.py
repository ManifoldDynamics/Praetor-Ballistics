import numpy as np
from ballistics.environment_v2 import AtmosphereV2, EarthModelV2

def test_atmosphere_v2_layers():
    # Troposphere
    p_sl = AtmosphereV2.get_properties(0)
    assert np.isclose(p_sl['pressure'], 101325.0)

    # Stratosphere (30km)
    p_30k = AtmosphereV2.get_properties(30000)
    assert p_30k['temperature'] > 200.0

    # Mesosphere (70km)
    p_70k = AtmosphereV2.get_properties(70000)
    assert p_70k['pressure'] < 10.0 # Very low

def test_gravity_j2():
    # Equator [R_EQ, 0, 0]
    pos_eq = np.array([6378137.0, 0.0, 0.0])
    g_eq = EarthModelV2.gravity_j2(pos_eq)

    # Pole [0, 0, R_EQ] (approximate)
    pos_pole = np.array([0.0, 0.0, 6378137.0])
    g_pole = EarthModelV2.gravity_j2(pos_pole)

    # Gravity at pole should be stronger due to J2 and proximity to center
    assert np.linalg.norm(g_pole) > np.linalg.norm(g_eq)
