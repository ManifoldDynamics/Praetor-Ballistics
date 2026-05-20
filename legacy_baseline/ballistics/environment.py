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
