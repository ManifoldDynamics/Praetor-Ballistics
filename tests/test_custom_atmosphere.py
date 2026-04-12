import numpy as np
from ballistics.environment import StandardAtmosphere

def test_custom_atmosphere():
    # Standard Sea level
    atm_std = StandardAtmosphere()
    props_std = atm_std.get_properties(0)

    # Custom hot day (30 C, same pressure, no humidity)
    atm_hot = StandardAtmosphere(temperature_c=30.0, pressure_pa=101325.0, humidity_percent=0.0)
    props_hot = atm_hot.get_properties(0)

    # Hot air is less dense
    assert props_hot['density'] < props_std['density']
    # Hot air has higher speed of sound
    assert props_hot['speed_of_sound'] > props_std['speed_of_sound']

def test_humidity_virtual_temperature():
    # Hot dry day
    atm_dry = StandardAtmosphere(temperature_c=30.0, pressure_pa=101325.0, humidity_percent=0.0)
    props_dry = atm_dry.get_properties(0)

    # Hot humid day
    atm_humid = StandardAtmosphere(temperature_c=30.0, pressure_pa=101325.0, humidity_percent=100.0)
    props_humid = atm_humid.get_properties(0)

    # Humid air is less dense than dry air (water vapor is lighter than N2/O2)
    assert props_humid['density'] < props_dry['density']

    # Virtual temperature should be higher than actual temperature to lower density
    assert props_humid['virtual_temperature'] > props_humid['temperature']
