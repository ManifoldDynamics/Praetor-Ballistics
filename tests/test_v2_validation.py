import numpy as np
from ballistics.aero_v2 import AeroPredictorV2
from ballistics.terminal_v2 import TerminalBallisticsV2

def test_m193_drag_delta():
    # Validating against known M193 Doppler data (Cd ~ 0.25 at M2.5)
    class M193Geo:
        caliber = 0.00556
        ref_area = 2.42e-5
        total_length = 0.023
        nose_length = 0.012
        boattail_base_diameter = 0.004
        meplat_diameter = 0.0005
        def wetted_area(self): return 0.0004

    predictor = AeroPredictorV2(M193Geo())
    aero = predictor.predict_aerodynamics(num_points=10)
    cd_at_m25 = aero.cd(2.5)

    # Target Delta < 2%
    target_cd = 0.25
    delta = abs(cd_at_m25 - target_cd) / target_cd
    assert delta < 0.02

def test_m829_penetration_delta():
    l_rod = 0.5
    v_impact = 1500.0
    rho_p = 17600.0
    rho_t = 7850.0
    y_p = 2.0e9
    r_t = 5.0e9

    depth = TerminalBallisticsV2.alekseevskii_tate_penetration(v_impact, l_rod, 0.02, rho_p, rho_t, y_p, r_t)

    expected = 0.65
    delta = abs(depth - expected) / expected
    assert delta < 0.05
