import numpy as np

class HypersonicHeating:
    """
    Computes stagnation point heat flux and temperature variation
    due to aerothermodynamic heating during high-speed flight.
    """
    STEFAN_BOLTZMANN = 5.670374419e-8 # W / (m^2 * K^4)

    @staticmethod
    def fay_riddell_heat_flux(rho_air, v_infinity, nose_radius_m):
        """
        Calculates the convective stagnation point heat flux using the Detra-Kemp-Riddell (DKR)
        empirical engineering approximation of the Fay-Riddell equations.

        rho_air: Free-stream air density (kg/m^3)
        v_infinity: Free-stream relative air velocity (m/s)
        nose_radius_m: Radius of curvature at the stagnation point (meters). Must be > 0.

        Returns: Convective heat flux (q_conv) in Watts per square meter (W/m^2).
        """
        if v_infinity <= 0.0:
            return 0.0

        if nose_radius_m <= 0.0:
            # Prevent singularity. A perfectly sharp point mathematically burns instantly.
            # In reality, sharp tips melt into small radii immediately. We clamp it.
            nose_radius_m = 0.001 # 1mm minimum radius

        # The DKR simplified correlation for stagnation point heat flux (cold wall assumption):
        # q_s = 1.83e-4 * (rho / R_n)^0.5 * V^3  (Outputs in W/m^2 for SI units)
        # Note: The coefficient 1.83e-4 is an empirical fit for standard Earth atmosphere.

        q_conv = 1.83e-4 * np.sqrt(rho_air / nose_radius_m) * (v_infinity**3)

        return q_conv

    @staticmethod
    def radiative_cooling_flux(temperature_k, emissivity):
        """
        Calculates the heat flux radiated away from the hot surface.
        Stefan-Boltzmann Law: q_rad = epsilon * sigma * T^4

        Returns: Radiative heat flux out in W/m^2.
        """
        return emissivity * HypersonicHeating.STEFAN_BOLTZMANN * (temperature_k**4)

    @staticmethod
    def calculate_nose_temperature_derivative(q_conv, q_rad, nose_radius_m, material):
        """
        Calculates the rate of temperature change (dT/dt) for the nose region.

        We treat the nose tip as a lumped thermal mass for simplicity in the 6-DoF solver.
        The volume of the hemispherical nose tip cap = (2/3) * pi * R^3
        The surface area exposed to heating = 2 * pi * R^2
        Mass of tip = Volume * Density
        Thermal Mass (Joules/Kelvin) = Mass * Specific Heat

        dT/dt = (Net Heat Flux In * Area) / Thermal Mass
        """
        r = max(nose_radius_m, 0.001)

        # Surface area of a hemisphere
        area = 2.0 * np.pi * (r**2)

        # Volume of a hemisphere
        volume = (2.0 / 3.0) * np.pi * (r**3)

        mass = volume * material.density
        thermal_mass_j_k = mass * material.specific_heat

        # Net Heat Flux (W/m^2)
        q_net = q_conv - q_rad

        # Total Power (Watts or Joules/sec)
        power_net_w = q_net * area

        # Temperature derivative (K/s)
        dT_dt = power_net_w / thermal_mass_j_k

        return dT_dt
