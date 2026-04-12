import numpy as np

class GunSystem:
    def __init__(self, chamber_volume_m3, barrel_length_m, bore_diameter_m, bullet_mass_kg):
        self.chamber_volume = chamber_volume_m3
        self.barrel_length = barrel_length_m
        self.bore_diameter = bore_diameter_m
        self.bore_area = np.pi * (bore_diameter_m / 2.0)**2
        self.bullet_mass = bullet_mass_kg

class Charge:
    def __init__(self, propellant, mass_kg, web_thickness_m, form_factor_theta=0.5):
        """
        web_thickness_m: The minimum burning dimension (e_0) of a single powder grain.
        form_factor_theta: A shape factor describing how the burning surface area changes.
                           0.0 = Neutral burning (e.g. multi-perforated cylinder)
                           >0.0 = Degressive burning (e.g. solid sphere/cube)
                           <0.0 = Progressive burning (e.g. single perforated cylinder)
        """
        self.propellant = propellant
        self.mass = mass_kg
        self.web_thickness = web_thickness_m
        self.form_factor_theta = form_factor_theta

class InteriorResult:
    def __init__(self, success, t, p_pa, v_ms, x_m, z_frac, message):
        self.success = success
        self.time = t
        self.pressure_pa = p_pa
        self.velocity_ms = v_ms
        self.travel_m = x_m
        self.fraction_burned = z_frac
        self.message = message

        self.muzzle_velocity = v_ms[-1] if len(v_ms) > 0 else 0.0
        self.peak_pressure = np.max(p_pa) if len(p_pa) > 0 else 0.0
