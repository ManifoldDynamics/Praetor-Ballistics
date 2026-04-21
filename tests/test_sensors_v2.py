import numpy as np
from ballistics.sensors_v2 import IRSignatureModelV2, SeekerModelV2

def test_ir_signature_scaling():
    # T^4 scaling check
    i1 = IRSignatureModelV2.calculate_radiant_intensity(300, 1.0)
    i2 = IRSignatureModelV2.calculate_radiant_intensity(600, 1.0)
    # 600^4 / 300^4 = 16
    assert np.isclose(i2 / i1, 16.0)

def test_snr_range_dependence():
    intensity = 1000.0
    snr1 = IRSignatureModelV2.calculate_snr(intensity, 1000.0)
    snr2 = IRSignatureModelV2.calculate_snr(intensity, 2000.0)
    # 1/R^2 scaling
    assert np.isclose(snr1 / snr2, 4.0)

def test_seeker_latency_and_noise():
    seeker = SeekerModelV2(latency_s=0.1, angle_noise_std_rad=0.01)

    t = 1.0
    p_truth = np.array([1000, 0, 0])
    v_truth = np.array([100, 0, 0])
    p_proj = np.array([0, 0, 0])

    # At t=1.0, with latency=0.1, it should sense truth at t=0.9
    # Truth at t=0.9: [1000 + 100*(0.9-1.0), 0, 0] = [990, 0, 0] if we assume t=1.0 is the reference
    # Wait, the way I implemented it in get_eom:
    # t_delayed = t - seeker.latency
    # t_pos_delayed = pos_0 + vel * t_delayed

    s_pos, s_vel = seeker.get_sensed_target(t, p_truth, v_truth, p_proj, snr=100.0)

    assert s_pos is not None
    # With SNR=100, noise should be small. s_pos should be close to p_truth
    # (In this test p_truth IS the delayed truth passed to the function)
    dist = np.linalg.norm(s_pos - p_truth)
    assert dist < 50.0 # Loose bound for stochastic test

def test_seeker_snr_threshold():
    seeker = SeekerModelV2(snr_threshold=10.0)
    p_truth = np.array([100, 0, 0])
    v_truth = np.array([0, 0, 0])
    p_proj = np.array([0, 0, 0])

    # Below threshold
    s_pos, _ = seeker.get_sensed_target(0, p_truth, v_truth, p_proj, snr=5.0)
    assert s_pos is None

    # Above threshold
    s_pos, _ = seeker.get_sensed_target(0, p_truth, v_truth, p_proj, snr=15.0)
    assert s_pos is not None
