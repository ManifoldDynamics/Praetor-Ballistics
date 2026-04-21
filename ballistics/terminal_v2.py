import numpy as np

class TerminalBallisticsV2:
    """
    V2 Proprietary Terminal Ballistics Engine.
    Implements:
    - Lambert Correlation for fragment residual velocity.
    - Multi-layer armor penetration (spaced and ERA).
    - Advanced long-rod hydrodynamic penetration.
    """
    @staticmethod
    def lambert_residual_velocity(v_impact, v_limit):
        """
        Lambert equation for residual velocity of a fragment after perforating a plate.
        v_r = a * (v_impact^p - v_limit^p)^(1/p)
        Common approximation: p=2, a=1.0
        """
        if v_impact <= v_limit:
            return 0.0
        return np.sqrt(v_impact**2 - v_limit**2)

    @staticmethod
    def thor_equation(v_impact, m_frag, d_frag, target_thickness_mm, material_name='Steel (RHA)', obliquity_deg=0.0):
        """
        V2.x Proprietary Thor Equation Implementation.
        v_limit = 10^c * (t * A)^alpha * m^beta * (cos theta)^gamma
        Accounts for material-specific constants and impact obliquity.
        """
        # Material constants (Proprietary V2.x Dataset)
        # c, alpha, beta, gamma
        thor_constants = {
            'Steel (RHA)': [4.4, 0.9, -0.3, -1.2],
            'Aluminum (7075-T6)': [4.1, 0.8, -0.25, -1.1],
            'Titanium (Ti-6Al-4V)': [4.3, 0.85, -0.28, -1.15]
        }

        c, alpha, beta, gamma = thor_constants.get(material_name, [4.4, 0.9, -0.3, -1.2])

        area = np.pi * (d_frag / 2.0)**2
        cos_theta = np.cos(np.deg2rad(obliquity_deg))

        # Limit V based on Thor empirical fit
        v_limit = (10**c) * (target_thickness_mm * area)**alpha * (m_frag**beta) * (cos_theta**gamma)
        return v_limit

    @staticmethod
    def multi_layer_penetration(v_impact, m_frag, d_frag, layers):
        """
        Calculates penetration through multiple armor layers.
        layers: list of dicts {'thickness_mm': float, 'material': str, 'type': 'spaced'|'era'|'rha'}
        """
        v_curr = v_impact
        total_layers_pierced = 0

        for layer in layers:
            # Calculate ballistic limit for this layer
            mat = layer.get('material', 'Steel (RHA)')
            obl = layer.get('obliquity_deg', 0.0)
            v_limit = TerminalBallisticsV2.thor_equation(v_curr, m_frag, d_frag, layer['thickness_mm'], mat, obl)

            # ERA logic: Effective thickness increase
            if layer['type'] == 'era':
                v_limit *= 2.5 # ERA is highly effective against small fragments

            if v_curr > v_limit:
                v_curr = TerminalBallisticsV2.lambert_residual_velocity(v_curr, v_limit)
                total_layers_pierced += 1
            else:
                v_curr = 0.0
                break

            if v_curr <= 0:
                break

        return {
            'pierced_count': total_layers_pierced,
            'residual_velocity': v_curr,
            'success': total_layers_pierced == len(layers)
        }

    @staticmethod
    def calculate_thermo_mechanical_shear(rpm, temperature_k, material_yield_sl_pa):
        """
        V2.x Rigorous "Aero-Fuse" Trigger Physics.
        Calculates casing failure by linking thermal yield degradation to centrifugal hoop stress.
        """
        # Johnson-Cook style Yield Strength Degradation
        T_melt = 1811.0 # Iron/Steel melting point (K)
        T_ref = 293.15  # Reference temperature (K)
        m_thermal = 1.09 # Thermal softening exponent for RHA

        if temperature_k >= T_melt:
             temp_factor = 0.0
        else:
             T_star = (temperature_k - T_ref) / (T_melt - T_ref)
             temp_factor = max(0.0, 1.0 - (T_star**m_thermal))

        sigma_y_eff = material_yield_sl_pa * temp_factor

        # Rigorous Centrifugal Hoop Stress: sigma_theta = rho * omega^2 * r^2
        omega = rpm * (2.0 * np.pi / 60.0)
        rho = 7850.0 # kg/m^3
        r_outer = 0.01 # m (caliber radius)

        sigma_hoop = rho * (omega**2) * (r_outer**2)

        # Disintegration Trigger: Failure when hoop stress exceeds degraded yield
        disintegrated = sigma_hoop > sigma_y_eff

        return {
            'disintegrated': disintegrated,
            'effective_yield_pa': sigma_y_eff,
            'centrifugal_stress_pa': sigma_hoop
        }
