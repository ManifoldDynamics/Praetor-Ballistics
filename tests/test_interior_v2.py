import numpy as np
from ballistics.interior_ballistics import GunSystem, Charge
from ballistics.propellants import Propellant
from ballistics.interior_solver import InteriorSolver

def test_interior_v2_basic():
    # Model a generic 5.56 NATO Rifle
    gun = GunSystem(
        chamber_volume_m3=2.0e-6,
        barrel_length_m=0.5,
        bore_diameter_m=0.00556,
        bullet_mass_kg=0.004,
        bullet_ix_kgm2=1.5e-8,
        twist_rate_in_per_turn=7.0
    )

    prop = Propellant("Fast Rifle Powder (Extruded)")
    charge = Charge(propellant=prop, mass_kg=0.0016, web_thickness_m=0.0005)

    # Use V2 solver
    solver = InteriorSolver(gun, charge, version=2)
    res = solver.solve()

    assert res.success
    assert res.muzzle_velocity > 500.0 # m/s
    assert res.peak_pressure > 100e6 # Pa

def test_interior_v2_vs_v1():
    gun = GunSystem(
        chamber_volume_m3=2.0e-6,
        barrel_length_m=0.5,
        bore_diameter_m=0.00556,
        bullet_mass_kg=0.004,
        bullet_ix_kgm2=1.5e-8,
        twist_rate_in_per_turn=7.0
    )
    prop = Propellant("Fast Rifle Powder (Extruded)")
    charge = Charge(propellant=prop, mass_kg=0.0016, web_thickness_m=0.0005)

    solver_v1 = InteriorSolver(gun, charge, version=1)
    res_v1 = solver_v1.solve()

    solver_v2 = InteriorSolver(gun, charge, version=2)
    res_v2 = solver_v2.solve()

    assert res_v1.success
    assert res_v2.success

    # V2 should generally have lower muzzle velocity due to heat loss
    # (assuming everything else is equal and V1 has no heat loss)
    print(f"V1 MV: {res_v1.muzzle_velocity:.2f}, V2 MV: {res_v2.muzzle_velocity:.2f}")
    assert res_v2.muzzle_velocity < res_v1.muzzle_velocity
