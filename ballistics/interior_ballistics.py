import numpy as np

class GunSystem:
    def __init__(self, chamber_volume_m3, barrel_length_m, bore_diameter_m, bullet_mass_kg, bullet_ix_kgm2=0.0, twist_rate_in_per_turn=10.0, engraving_force_n=500.0, bore_friction_n=100.0):
        self.chamber_volume = chamber_volume_m3
        self.barrel_length = barrel_length_m
        self.bore_diameter = bore_diameter_m
        self.bore_area = np.pi * (bore_diameter_m / 2.0)**2
        self.bullet_mass = bullet_mass_kg
        self.bullet_ix_kgm2 = bullet_ix_kgm2

        # Twist Rate: Inches of forward travel required to complete 1 full 360 degree rotation
        # 0.0 means smoothbore
        self.twist_rate_in_per_turn = twist_rate_in_per_turn

        # Engraving Force: Peak friction required to push the bullet through the initial rifling lands
        self.engraving_force_n = engraving_force_n

        # Bore Friction: Sustained sliding friction as the bullet travels the barrel
        self.bore_friction_n = bore_friction_n

        # Convert twist rate to a multiplier: radians per meter of forward travel
        if self.twist_rate_in_per_turn > 0.0:
            meters_per_turn = self.twist_rate_in_per_turn * 0.0254
            self.rads_per_meter = (2.0 * np.pi) / meters_per_turn
        else:
            self.rads_per_meter = 0.0

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
    def __init__(self, success, t, p_pa, v_ms, x_m, z_frac, message, spin_rads=0.0):
        self.success = success
        self.time = t
        self.pressure_pa = p_pa
        self.velocity_ms = v_ms
        self.travel_m = x_m
        self.fraction_burned = z_frac
        self.message = message

        self.muzzle_velocity = v_ms[-1] if len(v_ms) > 0 else 0.0
        self.spin_rate_rads = spin_rads
        self.peak_pressure = np.max(p_pa) if len(p_pa) > 0 else 0.0
