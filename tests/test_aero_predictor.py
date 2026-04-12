import numpy as np
from ballistics.geometry import ProjectileGeometry
from ballistics.aero_predictor import AeroPredictor

def test_geometry_wetted_area():
    # Simple cylinder: D=0.1, L=1.0
    # Wetted area = pi * D * L
    geo = ProjectileGeometry(caliber_m=0.1, nose_length_m=0.0, body_length_m=1.0)
    assert np.isclose(geo.wetted_area(), np.pi * 0.1 * 1.0)

def test_aero_prediction_physics():
    # Test a realistic 155mm artillery shell geometry
    geo = ProjectileGeometry(
        caliber_m=0.155,
        nose_length_m=0.4,
        nose_type="tangent_ogive",
        body_length_m=0.3,
        boattail_length_m=0.1,
        boattail_base_diameter_m=0.13
    )

    predictor = AeroPredictor(geo)
    aero = predictor.predict_aerodynamics()

    # 1. Drag should be positive everywhere
    assert aero.cd(0.5) > 0.0

    # 2. Transonic drag spike: Drag at Mach 1.1 should be higher than Mach 0.5
    assert aero.cd(1.1) > aero.cd(0.5)

    # 3. Supersonic decay: Drag at Mach 3.0 should be lower than the transonic peak (Mach 1.1)
    assert aero.cd(3.0) < aero.cd(1.1)

def test_boattail_effectiveness():
    geo_flat = ProjectileGeometry(
        caliber_m=0.155, nose_length_m=0.4, body_length_m=0.4,
        boattail_length_m=0.0 # Flat base
    )

    geo_bt = ProjectileGeometry(
        caliber_m=0.155, nose_length_m=0.4, body_length_m=0.3,
        boattail_length_m=0.1, boattail_base_diameter_m=0.13 # Boattail base
    )

    aero_flat = AeroPredictor(geo_flat).predict_aerodynamics()
    aero_bt = AeroPredictor(geo_bt).predict_aerodynamics()

    # The boattail should reduce base drag significantly at subsonic speeds
    assert aero_bt.cd(0.8) < aero_flat.cd(0.8)
