import numpy as np
from ballistics.terminal import TerminalBallistics

def test_demarre_penetration():
    # Solid steel shot, 10kg, 100mm caliber, 500m/s
    p1 = TerminalBallistics.demarre(500.0, 10.0, 0.1)

    # Doubling velocity should vastly increase penetration
    p2 = TerminalBallistics.demarre(1000.0, 10.0, 0.1)
    assert p2 > p1 * 1.5

    # Halving mass should decrease penetration
    p3 = TerminalBallistics.demarre(500.0, 5.0, 0.1)
    assert p3 < p1

    # Zero velocity means zero penetration
    assert TerminalBallistics.demarre(0.0, 10.0, 0.1) == 0.0

def test_krupp_penetration():
    # Naval gun example: 1000kg shell, 400mm caliber, 500m/s
    p1 = TerminalBallistics.krupp(500.0, 1000.0, 0.4)

    # Velocity squared relationship in Krupp formula
    p2 = TerminalBallistics.krupp(1000.0, 1000.0, 0.4)
    assert np.isclose(p2, p1 * 4.0, rtol=0.01) # Doubling V quadruples penetration (V^2)

def test_lanz_odermatt_penetration():
    # APFSDS: 1500m/s, Tungsten (17600), 0.6m length
    p1 = TerminalBallistics.lanz_odermatt(1500.0, 17600.0, 0.6)

    # At hyper-velocities (V -> infinity), penetration approaches the hydrodynamic limit: L * sqrt(rho_p / rho_t)
    limit = 0.6 * np.sqrt(17600.0 / 7850.0) * 1000.0 # in mm

    p_hyper = TerminalBallistics.lanz_odermatt(5000.0, 17600.0, 0.6)
    assert p_hyper > p1
    assert p_hyper < limit
    assert np.isclose(p_hyper, limit, rtol=0.2) # Gets close to limit
