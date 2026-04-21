import numpy as np

class AtmosphereV2:
    """
    V2 Proprietary Atmospheric Engine.
    Expanded 1976 US Standard Atmosphere (up to 100km).
    Includes multiple thermal layers and geopotential correction.
    """
    # Standard Constants
    G = 9.80665
    R = 287.05
    RE = 6371000.0 # Earth Radius

    # Layer defined by [h_base (km), T_base (K), lapse_rate (K/km)]
    LAYERS = [
        [0.0, 288.15, -6.5],   # Troposphere
        [11.0, 216.65, 0.0],   # Tropopause
        [20.0, 216.65, 1.0],   # Stratosphere 1
        [32.0, 228.65, 2.8],   # Stratosphere 2
        [47.0, 270.65, 0.0],   # Stratopause
        [51.0, 270.65, -2.8],  # Mesosphere 1
        [71.0, 214.65, -2.0],  # Mesosphere 2
        [84.85, 186.87, 0.0]   # Mesopause
    ]

    @classmethod
    def get_properties(cls, alt_m):
        if alt_m < 0: alt_m = 0.0

        # Geopotential Altitude (km)
        h = (cls.RE/1000.0 * (alt_m/1000.0)) / (cls.RE/1000.0 + (alt_m/1000.0))

        # Initial SSL values
        P0 = 101325.0
        T0 = 288.15

        T_curr = T0
        P_curr = P0

        for i in range(len(cls.LAYERS)):
            h_base, t_base, lapse = cls.LAYERS[i]
            h_next = cls.LAYERS[i+1][0] if i+1 < len(cls.LAYERS) else 1000.0

            # Distance within this layer
            dz = min(h, h_next) - h_base
            if dz < 0: break

            if lapse != 0:
                T_next = t_base + lapse * dz
                P_next = P_curr * (T_next / t_base)**(-cls.G / (lapse/1000.0 * cls.R))
            else:
                T_next = t_base
                P_next = P_curr * np.exp(-cls.G * dz * 1000.0 / (cls.R * t_base))

            if h <= h_next:
                T_curr = T_next
                P_curr = P_next
                break
            else:
                T_curr = T_next
                P_curr = P_next

        rho = P_curr / (cls.R * T_curr)
        gamma = 1.4
        a = np.sqrt(gamma * cls.R * T_curr)

        return {
            'temperature': T_curr,
            'pressure': P_curr,
            'density': rho,
            'speed_of_sound': a
        }

class EarthModelV2:
    """
    V2 Proprietary Earth Physics Engine.
    Implements J2 Gravitational Perturbation (Oblateness).
    """
    MU = 3.986004418e14 # m^3/s^2
    R_EQ = 6378137.0    # m
    J2 = 1.08262668e-3
    OMEGA = 7.292115e-5

    @classmethod
    def gravity_j2(cls, pos_vec):
        """
        Calculates gravity acceleration vector including J2 perturbation.
        pos_vec: [X, Y, Z] in ECI frame.
        """
        r = np.linalg.norm(pos_vec)
        if r < cls.R_EQ: r = cls.R_EQ

        z = pos_vec[2]
        z2_r2 = (z/r)**2

        # Spherical term
        a_sph = -(cls.MU / r**3) * pos_vec

        # J2 term
        j2_factor = 1.5 * cls.J2 * (cls.MU / r**2) * (cls.R_EQ / r)**2

        a_j2 = np.array([
            j2_factor * (pos_vec[0]/r) * (5*z2_r2 - 1),
            j2_factor * (pos_vec[1]/r) * (5*z2_r2 - 1),
            j2_factor * (pos_vec[2]/r) * (5*z2_r2 - 3)
        ])

        return a_sph + a_j2

    @classmethod
    def calculate_magnetic_field_wmm(cls, lat_deg, lon_deg, alt_m):
        """
        V2.x Proprietary World Magnetic Model (WMM) logic.
        Calculates magnetic field vector for IMU sensor simulation.
        (Simplified spherical harmonic implementation)
        """
        # Baseline magnetic field at equator ~ 3e-5 Tesla
        # B = B0 * (R_EQ / r)^3
        r = cls.R_EQ + alt_m
        b0 = 3.12e-5
        strength = b0 * (cls.R_EQ / r)**3

        # Magnetic inclination (dip angle) approx: tan(I) = 2 * tan(lat)
        lat_rad = np.deg2rad(lat_deg)
        inc_rad = np.arctan(2 * np.tan(lat_rad))

        # Field vector in local NED (North, East, Down)
        b_n = strength * np.cos(inc_rad)
        b_e = 0.0 # simplified declination
        b_d = strength * np.sin(inc_rad)

        return np.array([b_n, b_e, b_d])
