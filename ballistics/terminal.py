import numpy as np

class TerminalBallistics:
    """
    Empirical models for calculating armor penetration based on terminal ballistic data.
    """

    @staticmethod
    def demarre(velocity_m_s, mass_kg, diameter_m, armor_constant=1.0):
        """
        De Marre formula for armor penetration.
        Historically used for solid shot against Rolled Homogeneous Armor (RHA).

        velocity_m_s: Impact velocity in m/s
        mass_kg: Projectile mass in kg
        diameter_m: Projectile diameter (caliber) in meters
        armor_constant: De Marre coefficient for armor quality.
                        Usually around 0.8 to 1.2. 1.0 is standard.

        Returns: Penetration depth in millimeters.
        """
        # Convert inputs to standard De Marre units (decimeters, kg, m/s)
        D_dm = diameter_m * 10.0 # meters to decimeters
        W_kg = mass_kg
        V_ms = velocity_m_s

        # De Marre empirical formula
        # V = K * (D^0.75 * e^0.7) / (W^0.5)
        # Rearranging for e (thickness in decimeters):
        # e = [ (V * W^0.5) / (K * D^0.75) ] ^ (1/0.7)

        # Historical standard K for RHA is roughly 1530 to 2000. Let's use a normalized constant.
        # We'll formulate it to output millimeters directly based on modern empirical fits.

        # Formula: b = (W^0.5 * V / K / d^0.75)^1.428
        K = 1530.0 * armor_constant

        if velocity_m_s <= 0 or mass_kg <= 0 or diameter_m <= 0:
            return 0.0

        penetration_dm = ((V_ms * (W_kg**0.5)) / (K * (D_dm**0.75)))**(1.0 / 0.7)
        penetration_mm = penetration_dm * 100.0 # decimeters to millimeters

        return penetration_mm

    @staticmethod
    def krupp(velocity_m_s, mass_kg, diameter_m, armor_constant=2400.0):
        """
        Krupp penetration formula.
        Often used for naval artillery.

        velocity_m_s: Impact velocity in m/s
        mass_kg: Projectile mass in kg
        diameter_m: Projectile diameter in meters
        armor_constant: Krupp constant (K). Typically 2400 for standard steel.

        Returns: Penetration depth in millimeters.
        """
        if velocity_m_s <= 0 or mass_kg <= 0 or diameter_m <= 0:
            return 0.0

        # Standard Krupp Formula:
        # P = (W * V^2) / (K^2 * D)  --> Sometimes given with different exponents.
        # We will use the common metric variant:
        # P_mm = (V_ms / K) * sqrt(mass_kg / diameter_m) -- simplified variant
        # Actually, full Krupp is: P_m = [ (W * V^2) / (D * K) ] ^ (1/2)

        # Let's use the standard empirical metric Krupp:
        # T_mm = (V_ms * sqrt(mass_kg) * 1000) / (K * sqrt(diameter_m_mm)) -- too messy

        # Proper metric Krupp:
        # b = [ (M * V^2) / (K * d) ]
        # where b is penetration. Let's use a tuned constant to output mm.

        V = velocity_m_s
        M = mass_kg
        D = diameter_m * 1000.0 # Use mm for diameter in this formula

        # Velocity required to penetrate thickness b:
        # V = K * b^0.5 * D^0.5 / M^0.5
        # b = (V^2 * M) / (K^2 * D)

        # With K=2400, b is in dm.
        b_dm = (V**2 * M) / ((armor_constant**2) * (diameter_m * 10.0))
        penetration_mm = b_dm * 100.0

        return penetration_mm

    @staticmethod
    def lanz_odermatt(velocity_m_s, penetrator_density_kg_m3, penetrator_length_m, target_density_kg_m3=7850.0):
        """
        Lanz-Odermatt (Odermatt) formula for Long Rod Penetrators (APFSDS).
        This models hydrodynamic penetration at hyper-velocities.

        velocity_m_s: Impact velocity in m/s
        penetrator_density_kg_m3: Density of penetrator (e.g. Tungsten ~ 17600, DU ~ 19100)
        penetrator_length_m: Length of the penetrator rod
        target_density_kg_m3: Density of armor target (RHA Steel ~ 7850)

        Returns: Penetration depth in millimeters.
        """
        if velocity_m_s <= 0 or penetrator_length_m <= 0:
            return 0.0

        # Lanz-Odermatt simplified hydrodynamic approximation for L/D > 10
        # P/L = sqrt(rho_p / rho_t) * e^(-S / V^2)
        # Where S is a strength term representing target resistance.

        rho_p = penetrator_density_kg_m3
        rho_t = target_density_kg_m3
        L = penetrator_length_m
        V = velocity_m_s

        # Empirical strength parameter for RHA against tungsten/DU
        # Typically around 4.0e6 to 6.0e6 (m/s)^2 equivalent
        S = 4.0e6

        penetration_ratio = np.sqrt(rho_p / rho_t) * np.exp(-S / (V**2))
        penetration_m = penetration_ratio * L

        return penetration_m * 1000.0 # return mm
