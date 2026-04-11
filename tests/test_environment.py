import numpy as np
from ballistics.environment import StandardAtmosphere, EarthModel

def test_atmosphere_sea_level():
    props = StandardAtmosphere.get_properties(0)
    assert np.isclose(props['temperature'], 288.15)
    assert np.isclose(props['pressure'], 101325.0)
    assert np.isclose(props['density'], 1.225, atol=0.001)
    # Speed of sound at sea level ~ 340.29
    assert np.isclose(props['speed_of_sound'], 340.294, atol=0.01)

def test_atmosphere_tropopause():
    props = StandardAtmosphere.get_properties(11000)
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

from ballistics.environment import WindProfile

def test_wind_profile():
    wind = WindProfile()

    # Default is zero
    assert np.all(wind.get_wind(100) == [0, 0, 0])

    # Constant wind
    wind.set_constant_wind(5.0, -2.0)
    assert np.all(wind.get_wind(500) == [5.0, -2.0, 0.0])

    # Layered Wind
    alts = [0, 100, 200]
    vecs = [[0, 0, 0], [10, 0, 0], [10, 10, 0]]
    wind.set_wind_layers(alts, vecs)

    # Interpolation
    assert np.all(wind.get_wind(50) == [5.0, 0.0, 0.0])
    assert np.all(wind.get_wind(150) == [10.0, 5.0, 0.0])

    # Out of bounds clamping
    assert np.all(wind.get_wind(300) == [10.0, 10.0, 0.0])
    assert np.all(wind.get_wind(-10) == [0.0, 0.0, 0.0])

    # Polar setup (Blowing 90 deg / Y-axis)
    wind.set_wind_layers_polar([0], [10.0], [90.0])
    v = wind.get_wind(0)
    assert np.isclose(v[0], 0.0, atol=1e-10)
    assert np.isclose(v[1], 10.0)
