import numpy as np

class StandardAtmosphere:
    """
    Computes standard atmospheric properties based on the 1976 US Standard Atmosphere.
    Currently simplified to the troposphere layer (0 to 11,000 meters).
    """
    # Sea level standard constants
    T0 = 288.15      # Sea level standard temperature [K]
    P0 = 101325.0    # Sea level standard pressure [Pa]
    RHO0 = 1.225     # Sea level standard density [kg/m^3]
    G = 9.80665      # Standard acceleration of gravity [m/s^2]
    R = 287.05       # Specific gas constant for dry air [J/(kg*K)]
    L = -0.0065      # Temperature lapse rate in the troposphere [K/m]

    @classmethod
    def get_properties(cls, altitude):
        """
        Returns temperature, pressure, density, and speed of sound at a given altitude.
        Altitude in meters.
        """
        if altitude < 0:
            altitude = 0.0 # Clamp to sea level

        if altitude < 11000.0:
            # Troposphere
            T = cls.T0 + cls.L * altitude
            P = cls.P0 * (T / cls.T0) ** (-cls.G / (cls.L * cls.R))
        else:
            # Tropopause / Lower Stratosphere (11km to 20km)
            T_11k = cls.T0 + cls.L * 11000.0
            P_11k = cls.P0 * (T_11k / cls.T0) ** (-cls.G / (cls.L * cls.R))

            T = T_11k # Isothermal layer
            P = P_11k * np.exp(-cls.G * (altitude - 11000.0) / (cls.R * T))

        rho = P / (cls.R * T)

        # Speed of sound: a = sqrt(gamma * R * T), gamma = 1.4 for dry air
        gamma = 1.4
        speed_of_sound = np.sqrt(gamma * cls.R * T)

        return {
            'temperature': T,         # [K]
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
