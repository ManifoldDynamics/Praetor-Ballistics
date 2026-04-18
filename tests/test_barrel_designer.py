import numpy as np
from ballistics.interior_ballistics import GunSystem, Charge
from ballistics.propellants import Propellant
from ballistics.interior_solver import InteriorSolver

def test_barrel_twist_and_spin():
    # 5.56 NATO Style setup
    bore = 0.00556
    mass = 0.004 # 4 grams (62 gr)
    ix = 0.5 * mass * (bore / 2)**2

    # 1:7 twist rate
    gun = GunSystem(
        chamber_volume_m3=0.000002, # 2.0 cc
        barrel_length_m=0.5,
        bore_diameter_m=bore,
        bullet_mass_kg=mass,
        bullet_ix_kgm2=ix,
        twist_rate_in_per_turn=7.0,
        engraving_force_n=1000.0,
        bore_friction_n=100.0
    )

    prop = Propellant("Fast Rifle Powder (Extruded)")
    charge = Charge(propellant=prop, mass_kg=0.0016, web_thickness_m=0.0005)

    solver = InteriorSolver(gun, charge, start_pressure_pa=10e6)
    res = solver.solve()

    assert res.success is True

    # Check Spin Rate
    # Twist rate is 1 turn per 7 inches.
    # Spin rate (rad/s) = (velocity_ms / twist_m) * 2*pi
    twist_m = 7.0 * 0.0254
    expected_spin_revs_per_s = res.muzzle_velocity / twist_m
    expected_spin_rads = expected_spin_revs_per_s * 2.0 * np.pi

    # Spin should closely match the ideal kinematic relation
    # since we assumed the bullet perfectly engages rifling
    assert np.isclose(res.spin_rate_rads, expected_spin_rads, rtol=1e-3)

    # It should be spinning VERY fast (> 100k rad/s for typical rifle)
    assert res.spin_rate_rads > 10000.0

def test_barrel_length_impact():
    # A longer barrel should yield higher muzzle velocity for a slow burning powder,
    # up to a point.

    bore = 0.00556
    mass = 0.004
    ix = 0.5 * mass * (bore / 2)**2

    prop = Propellant("Fast Rifle Powder (Extruded)")
    charge = Charge(propellant=prop, mass_kg=0.0016, web_thickness_m=0.0005)

    gun_short = GunSystem(
        chamber_volume_m3=0.000002, barrel_length_m=0.25, bore_diameter_m=bore,
        bullet_mass_kg=mass, bullet_ix_kgm2=ix, twist_rate_in_per_turn=7.0
    )
    res_short = InteriorSolver(gun_short, charge).solve()

    gun_long = GunSystem(
        chamber_volume_m3=0.000002, barrel_length_m=0.5, bore_diameter_m=bore,
        bullet_mass_kg=mass, bullet_ix_kgm2=ix, twist_rate_in_per_turn=7.0
    )
    res_long = InteriorSolver(gun_long, charge).solve()

    # The longer barrel gives more time for gases to push the bullet
    assert res_long.muzzle_velocity > res_short.muzzle_velocity
