import numpy as np

class StandardAtmosphere:
    """
    Computes standard atmospheric properties based on the 1976 US Standard Atmosphere.
    Can be initialized with custom baseline weather conditions to calculate non-standard air density,
    utilizing Virtual Temperature to account for relative humidity.
    """
    G = 9.80665      # Standard acceleration of gravity [m/s^2]
    R = 287.05       # Specific gas constant for dry air [J/(kg*K)]
    L = -0.0065      # Temperature lapse rate in the troposphere [K/m]

    def __init__(self, temperature_c=15.0, pressure_pa=101325.0, humidity_percent=0.0):
        """
        Initializes the atmospheric model. Defaults to Standard Sea Level conditions.
        temperature_c: Temperature in Celsius
        pressure_pa: Station pressure in Pascals (Absolute, not sea-level corrected)
        humidity_percent: Relative humidity (0.0 to 100.0)
        """
        self.T0 = temperature_c + 273.15 # Convert to Kelvin
        self.P0 = pressure_pa
        self.RH = humidity_percent / 100.0

    def _calculate_virtual_temperature(self, T_k, P_pa):
        """
        Calculates virtual temperature to account for humidity reducing air density.
        """
        if self.RH <= 0.0:
            return T_k

        # Tetens equation for saturation vapor pressure of water
        T_c = T_k - 273.15
        P_sat = 610.78 * np.exp((17.27 * T_c) / (T_c + 237.3))

        # Actual vapor pressure
        P_vapor = self.RH * P_sat

        # Virtual temperature
        T_v = T_k / (1.0 - (P_vapor / P_pa) * (1.0 - 0.622))
        return T_v

    def get_properties(self, altitude):
        """
        Returns temperature, pressure, density, and speed of sound at a given altitude.
        Altitude in meters relative to the baseline station.
        """
        if altitude < 0:
            altitude = 0.0 # Clamp to station level

        if altitude < 11000.0:
            # Troposphere
            T = self.T0 + self.L * altitude
            P = self.P0 * (T / self.T0) ** (-self.G / (self.L * self.R))
        else:
            # Tropopause / Lower Stratosphere (11km to 20km)
            T_11k = self.T0 + self.L * 11000.0
            P_11k = self.P0 * (T_11k / self.T0) ** (-self.G / (self.L * self.R))

            T = T_11k # Isothermal layer
            P = P_11k * np.exp(-self.G * (altitude - 11000.0) / (self.R * T))

        # Adjust Temperature to Virtual Temperature to account for humidity in density calculation
        T_v = self._calculate_virtual_temperature(T, P)

        rho = P / (self.R * T_v)

        # Speed of sound: a = sqrt(gamma * R * T_v), gamma = 1.4 for dry air
        gamma = 1.4
        speed_of_sound = np.sqrt(gamma * self.R * T_v)

        return {
            'temperature': T,         # Actual Temperature [K]
            'virtual_temperature': T_v, # Virtual Temperature [K]
            'pressure': P,            # [Pa]
            'density': rho,           # [kg/m^3]
            'speed_of_sound': speed_of_sound # [m/s]
        }

class EarthModel:
    """
    A model of the Earth's gravity and rotation effects (Coriolis).
    Using WGS84 standard constants approximately.
    """
    OMEGA = 7.292115e-5 # Earth rotation rate [rad/s]
    R_EARTH = 6371000.0 # Approximate mean Earth radius [m]
    G0 = 9.80665        # Standard gravity at sea level [m/s^2]

    @classmethod
    def gravity(cls, altitude):
        """
        Calculates acceleration due to gravity varying with altitude.
        g = g0 * (R / (R + h))^2
        """
        return cls.G0 * (cls.R_EARTH / (cls.R_EARTH + altitude))**2

    @classmethod
    def coriolis_acceleration(cls, velocity, latitude_rad):
        """
        Calculates the Coriolis acceleration vector given current velocity and latitude.
        Assuming velocity is in a local ENU (East, North, Up) frame.
        """
        omega_vec = np.array([
            0.0,
            cls.OMEGA * np.cos(latitude_rad),
            cls.OMEGA * np.sin(latitude_rad)
        ])

        a_coriolis = -2.0 * np.cross(omega_vec, velocity)

        return a_coriolis

class WindProfile:
    """
    Models a 3D wind vector field that can vary with altitude.
    Interpolates smoothly between defined altitude layers.
    """
    def __init__(self):
        # We start with a default zero-wind profile
        self.altitudes = np.array([0.0, 100000.0]) # Surface to near-space
        self.wind_vectors = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        self._build_interpolator()

    def _build_interpolator(self):
        from scipy.interpolate import interp1d

        # If there's only one layer, interp1d will fail with linear, so we double it
        if len(self.altitudes) == 1:
            self.altitudes = np.array([self.altitudes[0], self.altitudes[0] + 100000.0])
            self.wind_vectors = np.array([self.wind_vectors[0], self.wind_vectors[0]])

        # Interpolate along the altitude axis (axis 0 of the vectors)
        # We clamp to the nearest boundary if outside the defined altitudes
        self._interpolator = interp1d(
            self.altitudes,
            self.wind_vectors,
            axis=0,
            kind='linear',
            bounds_error=False,
            fill_value=(self.wind_vectors[0], self.wind_vectors[-1])
        )

    def set_constant_wind(self, vx, vy, vz=0.0):
        """Sets a uniform wind field for all altitudes."""
        self.altitudes = np.array([0.0, 100000.0])
        self.wind_vectors = np.array([[vx, vy, vz], [vx, vy, vz]])
        self._build_interpolator()

    def set_wind_layers(self, altitudes, vectors):
        """
        Defines wind at specific altitude layers.
        altitudes: List or array of altitudes in meters (must be sorted ascending)
        vectors: List of [Vx, Vy, Vz] arrays for each altitude
        """
        self.altitudes = np.array(altitudes)
        self.wind_vectors = np.array(vectors)
        # Ensure it is sorted by altitude
        sort_idx = np.argsort(self.altitudes)
        self.altitudes = self.altitudes[sort_idx]
        self.wind_vectors = self.wind_vectors[sort_idx]
        self._build_interpolator()

    def set_wind_layers_polar(self, altitudes, speeds, azimuths_deg, updrafts=0.0):
        """
        Defines wind layers using polar coordinates (Speed and Direction).
        azimuth_deg: The direction the wind is BLOWING TOWARDS (0 deg = North/X-axis)
        """
        vectors = []
        # If updrafts is a scalar, make it a list
        if np.isscalar(updrafts):
            updrafts = [updrafts] * len(altitudes)

        for speed, az, vz in zip(speeds, azimuths_deg, updrafts):
            az_rad = np.deg2rad(az)
            vx = speed * np.cos(az_rad)
            vy = speed * np.sin(az_rad)
            vectors.append([vx, vy, vz])

        self.set_wind_layers(altitudes, vectors)

    def get_wind(self, altitude):
        """Returns the [Vx, Vy, Vz] wind vector at the given altitude."""
        return self._interpolator(altitude)
