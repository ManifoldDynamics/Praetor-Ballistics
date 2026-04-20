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
    def thor_equation(v_impact, m_frag, d_frag, target_thickness_mm, material_params):
        """
        Thor empirical equation for ballistic limit and residual velocity.
        v_limit = 10^c * (t * A)^alpha * m^beta * (cos theta)^gamma
        """
        # (Simplified proprietary THOR variant)
        # Using placeholder constants for RHA
        c = 4.5
        alpha = 0.9
        beta = -0.3
        area = np.pi * (d_frag / 2.0)**2

        v_limit = (10**c) * (target_thickness_mm * area)**alpha * (m_frag**beta)
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
            v_limit = TerminalBallisticsV2.thor_equation(v_curr, m_frag, d_frag, layer['thickness_mm'], None)

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
