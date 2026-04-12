import numpy as np
from ballistics.aerothermodynamics import HypersonicHeating
from ballistics.materials import Material

def test_heat_flux_scaling():
    # Fay-Riddell: q is proportional to V^3
    rho = 1.225
    r_n = 0.01

    q_v1 = HypersonicHeating.fay_riddell_heat_flux(rho, 1000.0, r_n)
    q_v2 = HypersonicHeating.fay_riddell_heat_flux(rho, 2000.0, r_n)

    # 2^3 = 8
    assert np.isclose(q_v2, q_v1 * 8.0, rtol=0.01)

def test_radiative_cooling():
    # Stefan-Boltzmann: q_rad is proportional to T^4
    q_rad1 = HypersonicHeating.radiative_cooling_flux(1000.0, emissivity=1.0)
    q_rad2 = HypersonicHeating.radiative_cooling_flux(2000.0, emissivity=1.0)

    # 2^4 = 16
    assert np.isclose(q_rad2, q_rad1 * 16.0, rtol=0.01)

def test_thermal_mass():
    mat_steel = Material("Steel (RHA)")

    # If q_conv = q_rad, dT/dt should be 0 (equilibrium)
    q_conv = 10000.0
    q_rad = 10000.0

    dt = HypersonicHeating.calculate_nose_temperature_derivative(q_conv, q_rad, 0.01, mat_steel)
    assert np.isclose(dt, 0.0)

    # If heating > cooling, dT/dt is positive
    dt2 = HypersonicHeating.calculate_nose_temperature_derivative(20000.0, 10000.0, 0.01, mat_steel)
    assert dt2 > 0.0
