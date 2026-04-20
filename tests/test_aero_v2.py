import numpy as np
from ballistics.geometry import ProjectileGeometry
from ballistics.projectile import Aerodynamics

def test_aero_v2_prediction():
    # Define a typical 155mm projectile geometry
    geo = ProjectileGeometry(
        caliber_m=0.155,
        nose_length_m=0.3,
        body_length_m=0.6,
        boattail_length_m=0.05,
        boattail_base_diameter_m=0.14
    )

    aero = Aerodynamics.from_predictor_v2(geo)

    # Check drag at subsonic and supersonic
    cd_sub = aero.cd(0.5)
    cd_super = aero.cd(2.5)

    assert cd_sub > 0
    assert cd_super > cd_sub # Wave drag should make it higher
    assert aero.cl(1.5) > 0
    assert aero.cma(1.5) != 0
    assert aero.cmaq(1.5) < 0 # Damping should be negative

def test_van_driest_effect():
    from ballistics.aero_v2 import AeroPredictorV2
    geo = ProjectileGeometry(caliber_m=0.155, nose_length_m=0.3)
    predictor = AeroPredictorV2(geo)

    # Re = 1e7
    cf_sub = predictor._get_van_driest_cf(0.1, 1e7, 288.15)
    cf_super = predictor._get_van_driest_cf(3.0, 1e7, 288.15)

    # Compressibility should reduce Cf
    assert cf_super < cf_sub

def test_sutherland_viscosity():
    from ballistics.aero_v2 import AeroPredictorV2
    geo = ProjectileGeometry(caliber_m=0.155, nose_length_m=0.3)
    predictor = AeroPredictorV2(geo)

    mu_cold = predictor._get_viscosity(200.0)
    mu_hot = predictor._get_viscosity(1000.0)

    assert mu_hot > mu_cold
