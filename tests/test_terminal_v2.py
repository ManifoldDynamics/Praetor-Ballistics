import numpy as np
from ballistics.terminal_v2 import TerminalBallisticsV2
from ballistics.lethality_v2 import FragmentationModelV2

def test_terminal_v2_lambert():
    v_impact = 1000.0
    v_limit = 500.0
    v_res = TerminalBallisticsV2.lambert_residual_velocity(v_impact, v_limit)
    assert v_res > 0
    assert v_res < v_impact
    assert np.isclose(v_res, np.sqrt(1000**2 - 500**2))

def test_terminal_v2_multi_layer():
    layers = [
        {'thickness_mm': 5.0, 'material': 'RHA', 'type': 'rha'},
        {'thickness_mm': 10.0, 'material': 'ERA', 'type': 'era'}
    ]
    res = TerminalBallisticsV2.multi_layer_penetration(2000.0, 0.1, 0.01, layers)
    assert 'pierced_count' in res
    assert 'success' in res

def test_lethality_v2_mott():
    masses = FragmentationModelV2.mott_distribution(10.0, 100, 0.5)
    assert len(masses) == 100
    assert np.isclose(np.sum(masses), 10.0)

def test_lethality_v2_gurney():
    v1 = FragmentationModelV2.gurney_v2(1.0, 5.0, 2500.0, confinement_factor=1.0)
    v2 = FragmentationModelV2.gurney_v2(1.0, 5.0, 2500.0, confinement_factor=2.0)
    assert v2 > v1
