import numpy as np
from ballistics.interior_ballistics import GunSystem, Charge, InteriorResult
from ballistics.propellants import Propellant
from ballistics.interior_solver import InteriorSolver

def test_interior_ballistics_thermo():
    # Model a generic 155mm Howitzer
    # 43kg shell, 155mm bore, 5m barrel length, 18 liter chamber (0.018 m^3)
    gun = GunSystem(chamber_volume_m3=0.018, barrel_length_m=5.0, bore_diameter_m=0.155, bullet_mass_kg=43.0)

    # Generic Triple-Base powder, 12 kg charge, 3mm web thickness, neutral burn
    prop = Propellant("Generic Triple-Base (Artillery)")
    charge = Charge(propellant=prop, mass_kg=12.0, web_thickness_m=0.003, form_factor_theta=0.0)

    solver = InteriorSolver(gun, charge, start_pressure_pa=30e6)

    res = solver.solve(max_time_s=0.05)

    assert res.success is True
    # The projectile should have accelerated out of the barrel (accounting for float precision)
    assert np.isclose(res.travel_m[-1], 5.0, atol=1e-3)

    # Velocity should be realistic for artillery (e.g. 500-1000 m/s)
    assert res.muzzle_velocity > 300.0 and res.muzzle_velocity < 1500.0

    # Peak pressure should be very high (e.g. 200 - 450 MPa)
    assert res.peak_pressure > 40e6 # Now slightly lower due to adding engraving force modeling delaying acceleration
    assert res.peak_pressure < 800e6

def test_charge_scaling():
    # If we double the charge mass, the peak pressure and velocity should increase
    gun = GunSystem(chamber_volume_m3=0.018, barrel_length_m=5.0, bore_diameter_m=0.155, bullet_mass_kg=43.0)
    prop = Propellant("Generic Triple-Base (Artillery)")

    charge1 = Charge(prop, mass_kg=6.0, web_thickness_m=0.003)
    solver1 = InteriorSolver(gun, charge1)
    res1 = solver1.solve()

    charge2 = Charge(prop, mass_kg=12.0, web_thickness_m=0.003)
    solver2 = InteriorSolver(gun, charge2)
    res2 = solver2.solve()

    assert res2.muzzle_velocity > res1.muzzle_velocity
    assert res2.peak_pressure > res1.peak_pressure
