import numpy as np
from ballistics.stochastic_v2 import StochasticEngineV2

def test_correlated_sampling():
    means = [100.0, 10.0]
    sds = [5.0, 1.0]
    corr = np.array([[1.0, -0.8], [-0.8, 1.0]])
    num = 1000

    samples = StochasticEngineV2.sample_correlated_inputs(means, sds, corr, num)

    assert samples.shape == (num, 2)
    # Check correlation of results
    res_corr = np.corrcoef(samples[:, 0], samples[:, 1])[0, 1]
    assert res_corr < -0.5

def test_von_karman_gust():
    v_avg = 10.0
    intensity = 0.1
    length_scale = 100.0

    g1 = StochasticEngineV2.von_karman_gust(1.0, v_avg, intensity, length_scale)
    g2 = StochasticEngineV2.von_karman_gust(1.01, v_avg, intensity, length_scale)

    assert g1 != g2
    assert abs(g1) < 5.0 # Reasonable range

def test_bayesian_cep():
    impacts = np.array([
        [1.0, 1.0],
        [-1.0, -1.0],
        [0.5, -0.5],
        [-0.5, 0.5]
    ])
    mpi = [0.0, 0.0]

    cep = StochasticEngineV2.calculate_bayesian_cep(impacts, mpi)
    assert cep > 0
    assert cep < 2.0
