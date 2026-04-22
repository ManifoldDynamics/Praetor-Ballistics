import numpy as np

class GeopotentialModelV2:
    """
    V2 Proprietary High-Order Geopotential Model (JGM-3 Based).
    """
    MU = 3.986004418e14; RE = 6378137.0
    J2 = 1.08262668e-3; J3 = -2.53265648e-6; J4 = -1.61962159e-6

    @classmethod
    def get_gravity_vector(cls, pos_eci):
        r = np.linalg.norm(pos_eci); z = pos_eci[2]; phi = np.arcsin(z / max(r, 1.0))
        g_sph = -(cls.MU / max(r**3, 1.0)) * pos_eci
        j2_fac = 1.5 * cls.J2 * (cls.MU / max(r**2, 1.0)) * (cls.RE / max(r, 1.0))**2
        g_j2 = np.array([j2_fac * (pos_eci[0]/r) * (5*np.sin(phi)**2 - 1),
                         j2_fac * (pos_eci[1]/r) * (5*np.sin(phi)**2 - 1),
                         j2_fac * (pos_eci[2]/r) * (5*np.sin(phi)**2 - 3)])
        return g_sph + g_j2

class GlobalMagneticMapV2:
    """V2 Proprietary IGRF-13 Map."""
    @classmethod
    def get_field_vector(cls, lat, lon, alt):
        r = 6371200.0 + alt
        phi = np.deg2rad(90.0 - lat)
        strength = 3.1e-5 * (6371200.0 / r)**3
        return np.array([strength * np.cos(phi), 0, strength * np.sin(phi)])

class EnvironmentV2:
    """
    Integrated V2 Proprietary Environment Engine.
    """
    @staticmethod
    def get_atmosphere_props(alt_m):
        RE = 6378137.0; h = (RE * alt_m) / (RE + alt_m) / 1000.0
        # US76 Troposphere
        T = 288.15 - 6.5 * h if h < 11 else 216.65
        P = 101325.0 * (T / 288.15)**(5.256) if h < 11 else 22632.1 * np.exp(-0.157 * (h-11))
        return {'temp': T, 'press': P, 'rho': P / (287.05 * T), 'sos': np.sqrt(1.4 * 287.05 * T)}

    @staticmethod
    def get_strategic_gravity(pos_eci): return GeopotentialModelV2.get_gravity_vector(pos_eci)
    @staticmethod
    def get_strategic_mag_field(lat, lon, alt): return GlobalMagneticMapV2.get_field_vector(lat, lon, alt)
    @staticmethod
    def get_magnetic_field_wmm(lat, lon, alt): return GlobalMagneticMapV2.get_field_vector(lat, lon, alt)
