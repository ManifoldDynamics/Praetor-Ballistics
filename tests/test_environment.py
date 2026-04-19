import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel

def test_atmosphere_sea_level():
    atm = StandardAtmosphere() # Use instance in V2
    props = atm.get_properties(0)
    assert np.isclose(props['temperature'], 288.15)
    assert np.isclose(props['pressure'], 101325.0)
    assert np.isclose(props['density'], 1.225, atol=0.001)
    # Speed of sound at sea level ~ 340.29
    assert np.isclose(props['speed_of_sound'], 340.294, atol=0.01)

def test_atmosphere_tropopause():
    atm = StandardAtmosphere()
    props = atm.get_properties(11000)
    # ~216.65 K, 22632 Pa, 0.3639 kg/m^3
    assert np.isclose(props['temperature'], 216.65)
    assert np.isclose(props['pressure'], 22632, atol=1.0)

def test_gravity():
    g_0 = EarthModel.gravity(0)
    assert np.isclose(g_0, 9.80665)

    g_10k = EarthModel.gravity(10000)
    assert g_10k < g_0

def test_coriolis():
    # Eastbound velocity at equator
    v = np.array([1000.0, 0.0, 0.0]) # East, North, Up
    lat = 0.0 # Equator
    a = EarthModel.coriolis_acceleration(v, lat)
    # Expect an upward force (Eötvös effect)
    assert np.isclose(a[0], 0.0)
    assert np.isclose(a[1], 0.0)
    assert np.isclose(a[2], 2.0 * EarthModel.OMEGA * 1000.0)
