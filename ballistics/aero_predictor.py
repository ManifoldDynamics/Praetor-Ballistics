import numpy as np
from ballistics.projectile import Aerodynamics

class AeroPredictor:
    """
    A semi-empirical aerodynamic prediction engine for axisymmetric projectiles.
    Calculates Cd(M) and Cl(M) curves over subsonic, transonic, and supersonic regimes.
    """
    def __init__(self, geometry, density_sl=1.225, sound_speed_sl=340.3):
        """
        geometry: ProjectileGeometry instance.
        density_sl: Sea-level air density (kg/m^3) used for Re calculation.
        sound_speed_sl: Sea-level speed of sound (m/s).
        """
        self.geo = geometry
        self.rho = density_sl
        self.a = sound_speed_sl
        self.mu = 1.81e-5 # Dynamic viscosity of air at sea level (kg/(m*s))

    def predict_aerodynamics(self, num_points=100, max_mach=5.0):
        """
        Generates the Cd vs Mach and Cl vs Mach arrays and returns an Aerodynamics instance.
        """
        mach_array = np.linspace(0.1, max_mach, num_points)
        cd_array = np.zeros_like(mach_array)
        cl_array = np.zeros_like(mach_array)

        # Calculate components for each Mach number
        for i, M in enumerate(mach_array):
            v = M * self.a
            Re = (self.rho * v * self.geo.total_length) / self.mu

            # 1. Skin Friction Drag (Cd_f)
            # using Prandtl-Schlichting formula for a flat plate turbulent boundary layer
            C_f = 0.455 / (np.log10(Re)**2.58) if Re > 0 else 0.0

            # Form factor for an axisymmetric body
            form_factor = 1.0 + 1.5 * (self.geo.caliber / self.geo.total_length)**1.5 + 7.0 * (self.geo.caliber / self.geo.total_length)**3

            # Scale skin friction from wetted area to reference area
            A_wet = self.geo.wetted_area()
            A_ref = self.geo.ref_area
            Cd_f = C_f * form_factor * (A_wet / A_ref)

            # 2. Base Drag (Cd_b)
            # Empirical Korst/McCoy Base Pressure Model
            # Subsonic base drag is high. Supersonic base pressure drops to a vacuum limit.
            base_ratio = (self.geo.boattail_base_diameter / self.geo.caliber)

            if M < 0.9:
                Cd_b_base = 0.12 + 0.08 * (M/0.9)**2
            elif M >= 0.9 and M < 1.1:
                # Transonic spike
                Cd_b_base = 0.20 + 0.05 * (M - 0.9)/0.2
            else:
                # Supersonic decay (Base pressure falls, but Cd = (P_inf - P_b) / q drops because q grows rapidly)
                Cd_b_base = 0.25 / M

            # Boattail relieves base drag by reducing the base area and preventing flow separation
            # The effectiveness of the boattail depends on its angle. An angle > ~9 deg will separate.
            boattail_angle_deg = np.rad2deg(self.geo.boattail_angle)
            if self.geo.boattail_length > 0:
                # Flow separation limit check
                if boattail_angle_deg > 10.0:
                    bt_eff = 0.5 # Fully separated flow, boattail is only half effective
                else:
                    bt_eff = 1.0 # Attached flow, boattail is fully effective

                # The drag is proportional to the base area ratio squared
                Cd_b = Cd_b_base * (base_ratio**3) * bt_eff
            else:
                Cd_b = Cd_b_base

            # 3. Wave Drag (Cd_w)
            # Exists only in transonic and supersonic flow
            if M < 0.9:
                Cd_w = 0.0
            elif M >= 0.9 and M < 1.1:
                # Transonic drag rise (very complex, empirical bridging)
                # Sharp noses have lower spikes.
                L_n = self.geo.nose_length
                D = self.geo.caliber
                # Slenderness of the nose limits the spike
                nose_ratio = L_n / D
                # The wave drag spike around Mach 1 is approximately inversely proportional to nose slenderness squared
                Cd_w_max = 0.2 / (nose_ratio**1.5)

                # Linear interpolation across transonic gap
                Cd_w = Cd_w_max * ((M - 0.9)/0.2)
            else:
                # Modified Newtonian Theory for Supersonic Wave Drag
                # Integrates pressure over the nose surface.
                # For an ogive, Cd_w ~ 2 * sin^2(theta_avg) where theta is the slope.
                L_n = self.geo.nose_length
                D = self.geo.caliber
                theta_v = np.arctan((D / 2.0) / L_n) # Average half-angle of the nose

                # Newtonian impact: Cd = Cp_max * sin^2(theta)
                # Where Cp_max is the stagnation pressure coefficient behind a normal shock
                # For M -> infinity, Cp_max -> 2.0. We use a Mach-dependent Rayleigh Pitot tube formula approx:
                gamma = 1.4
                cp_max = (2.0 / (gamma * M**2)) * ( ((gamma+1)**2 * M**2 / (4*gamma*M**2 - 2*(gamma-1)))**(gamma/(gamma-1)) * ((1 - gamma + 2*gamma*M**2) / (gamma+1)) - 1.0 )

                # Approximate integral over ogive surface
                Cd_w = cp_max * np.sin(theta_v)**2

                # A blunt meplat adds massive wave drag proportional to its area
                meplat_ratio = self.geo.meplat_diameter / D
                if meplat_ratio > 0:
                    Cd_w += cp_max * (meplat_ratio**2)

            # Total Drag
            cd_array[i] = Cd_f + Cd_b + Cd_w

            # Lift Coefficient (Cl)
            # Lift primarily comes from the nose in supersonic flow.
            # Newtonian theory: Cn_alpha ~ 2 * (Base Area / Ref Area). Since Base=Ref for nose cylinder, Cn_alpha ~ 2 per rad.
            # Convert to a standard Cl gradient
            if M < 1.0:
                cl_array[i] = 1.5 + 0.5 * M # Gradual rise
            else:
                cl_array[i] = 2.0 + 1.5 / M # Decay with Mach

        return Aerodynamics(cd=(mach_array, cd_array), cl=(mach_array, cl_array))
