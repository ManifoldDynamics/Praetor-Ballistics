import requests
from ballistics.environment import StandardAtmosphere

class LiveWeather:
    """
    Fetches real-time weather data from the open-meteo API (no API key required)
    and constructs a StandardAtmosphere object.
    """
    API_URL = "https://api.open-meteo.com/v1/forecast"

    @classmethod
    def fetch_atmosphere(cls, latitude, longitude, altitude=None):
        """
        Fetches current weather for the given coordinates and returns an initialized Atmosphere.

        latitude: Float, e.g., 39.7392 (Denver)
        longitude: Float, e.g., -104.9903 (Denver)
        altitude: Optional float (meters). If None, the API will use the geographic elevation of the lat/lon.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,surface_pressure",
        }

        if altitude is not None:
            params["elevation"] = altitude

        response = requests.get(cls.API_URL, params=params, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch weather data: {response.text}")

        data = response.json()
        current = data.get("current", {})

        temp_c = current.get("temperature_2m", 15.0)
        humidity = current.get("relative_humidity_2m", 0.0)
        # Open-Meteo returns pressure in hPa (millibars). Need Pascals.
        pressure_hpa = current.get("surface_pressure", 1013.25)
        pressure_pa = pressure_hpa * 100.0

        return StandardAtmosphere(
            temperature_c=temp_c,
            pressure_pa=pressure_pa,
            humidity_percent=humidity
        )
