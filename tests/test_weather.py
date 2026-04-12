import pytest
from unittest.mock import patch
from ballistics.weather import LiveWeather

def test_live_weather_fetcher():
    mock_response_data = {
        "current": {
            "temperature_2m": 35.0, # Hot
            "relative_humidity_2m": 80.0, # Humid
            "surface_pressure": 900.0 # Low pressure (high altitude)
        }
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        atm = LiveWeather.fetch_atmosphere(latitude=0.0, longitude=0.0)

        # Verify it converted hPa to Pa correctly
        assert atm.P0 == 90000.0
        # Verify it passed through temperature and humidity
        assert atm.T0 == 35.0 + 273.15
        assert atm.RH == 0.8

        props = atm.get_properties(0)
        # Should be much less dense than standard sea level (~1.225)
        assert props['density'] < 1.1
