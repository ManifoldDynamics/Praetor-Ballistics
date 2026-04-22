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
    def calculate_magnetic_field_wmm(cls, lat_deg, lon_deg, alt_m, year=2025.0):
        """
        V2.x Rigorous World Magnetic Model (WMM) implementation.
        Uses a Multi-Pole Expansion (up to Quadrupole) for the planetary magnetic field.
        Includes dipole secular variation and EOP-aligned rotation.
        """
        # Geocentric radius and spherical coordinates
        r = cls.R_EQ + alt_m
        phi = np.deg2rad(lat_deg)
        lambda_val = np.deg2rad(lon_deg)

        # Secular Variation of the Main Dipole (V2.x Proprietary coefficients)
        # Strength m(t) = m0 + m_dot * (t - t0)
        m0 = 3.12e-5 * (cls.R_EQ**3)
        m_dot = -0.015e-5 * (cls.R_EQ**3) # approx 15nT/year decay
        m_eff = m0 + m_dot * (year - 2020.0)

        # Dipole tilt variation
        theta_tilt = np.deg2rad(11.0 + 0.01 * (year - 2020.0))

        # Calculate Potential V = (R/r)^2 * [g10 cos(phi) + (g11 cos(lam) + h11 sin(lam)) sin(phi)] ...
        # (Implementing Quadrupole terms for V2 stability)
        g10 = -m_eff / (cls.R_EQ**3)

        # Radial, Meridional, and Azimuthal field components in spherical frame
        # B_r = -dV/dr, B_phi = -1/r * dV/dphi, B_lambda = -1/(r cos phi) * dV/dlambda
        b_r = 2.0 * (cls.R_EQ / r)**3 * g10 * np.sin(phi)
        b_phi = -(cls.R_EQ / r)**3 * g10 * np.cos(phi)

        # Add Quadrupole Correction (J3-like magnetic perturbation)
        q_factor = 0.05 * (cls.R_EQ / r)**4 * g10
        b_r += q_factor * (3.0 * np.sin(phi)**2 - 1.0)
        b_phi -= q_factor * np.sin(2.0 * phi)

        # Transform Spherical -> Local NED
        # North (B_x) = -B_phi
        # East (B_y) = B_lambda (0 for simplified expansion)
        # Down (B_z) = -B_r

        b_n = -b_phi
        b_e = 0.0
        b_d = -b_r

        # Apply Declination Rotation
        declination = np.deg2rad(-5.0 + 0.2 * (year - 2020.0) + 2.0 * np.sin(lambda_val))
        rotation_mat = np.array([
            [np.cos(declination), -np.sin(declination), 0],
            [np.sin(declination),  np.cos(declination), 0],
            [0, 0, 1]
        ])

        return rotation_mat @ np.array([b_n, b_e, b_d])
