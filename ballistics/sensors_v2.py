import numpy as np

class IRSignatureModelV2:
    """
    Proprietary V2 IR Signature Model.
    Calculates target radiant intensity and signal-to-noise ratio (SNR).
    """
    SIGMA = 5.670374419e-8  # Stefan-Boltzmann constant

    @staticmethod
    def calculate_radiant_intensity(temperature_k, projected_area_m2, emissivity=0.9):
        """
        Calculates radiant intensity (W/sr) in the IR band.
        """
        total_power = emissivity * IRSignatureModelV2.SIGMA * projected_area_m2 * (temperature_k**4)
        return total_power / np.pi

    @staticmethod
    def calculate_snr(intensity, range_m, detector_nep=1e-12, optics_aperture_m2=0.01):
        """
        Calculates Signal-to-Noise Ratio at the seeker detector.
        """
        if range_m < 1.0:
            return 100.0

        power_received = (intensity / (range_m**2)) * optics_aperture_m2
        snr = power_received / detector_nep
        return max(0.0, snr)


class SeekerModelV2:
    """
    Proprietary V2 Seeker Model.
    Implements sampling, latency, and SNR-dependent stochastic noise.
    """
    def __init__(self,
                 sampling_rate_hz=50.0,
                 latency_s=0.04,
                 angle_noise_std_rad=0.001,
                 range_noise_std_m=1.0,
                 snr_threshold=5.0):
        self.fs = sampling_rate_hz
        self.dt = 1.0 / sampling_rate_hz
        self.latency = latency_s
        self.angle_noise = angle_noise_std_rad
        self.range_noise = range_noise_std_m
        self.snr_threshold = snr_threshold

        # State for noise generation to keep it stable during integrator steps
        self._last_noise_t = -1.0
        self._cached_noise = (np.zeros(3), 0.0, np.zeros(3))

    def get_sensed_target(self, t, truth_pos, truth_vel, projectile_pos, snr=20.0):
        """
        Returns the 'sensed' target position and velocity.
        """
        # 1. Handle Latency
        # For the V2 MVP, we assume we can calculate the truth at t - latency
        # (This implies a predictable target or that the solver knows target history)
        # In get_eom, we can pass the target state at t - latency.

        # 2. Check SNR
        if snr < self.snr_threshold:
            return None, None

        # 3. Generate Noise
        # To be integrator-friendly, we should only "roll" new noise if t moves significantly
        # or we can use a hash of t for deterministic noise (simpler for RK45 stability)

        # Use a pseudo-random seed based on t (rounded to dt) for stability
        # Note: In a real simulation we might use a fixed noise sequence
        seed_t = int(t * self.fs)
        rng = np.random.RandomState(seed_t)

        noise_scale = 1.0 + (1.0 / max(0.1, snr))

        r_vec = truth_pos - projectile_pos
        range_mag = np.linalg.norm(r_vec)

        if range_mag < 0.1:
            return truth_pos, truth_vel

        # Angular noise
        jitter_std = self.angle_noise * noise_scale * range_mag
        noise_vec = rng.normal(0, jitter_std, 3)
        r_hat = r_vec / range_mag
        noise_perp = noise_vec - np.dot(noise_vec, r_hat) * r_hat

        sensed_pos = truth_pos + noise_perp

        # Range noise
        range_noise = rng.normal(0, self.range_noise * noise_scale)
        sensed_pos += r_hat * range_noise

        # Velocity noise
        sensed_vel = truth_vel + rng.normal(0, 0.1 * noise_scale, 3)

        return sensed_pos, sensed_vel

    @staticmethod
    def apply_epicyclic_filter(command_vec, alpha_history, cutoff_freq=5.0):
        """
        V2.x Proprietary Epicyclic Low-Pass Filter.
        Ignores high-frequency stabilizing nutation/precession wobbles in the guidance loop.
        """
        # (Simplified proprietary implementation)
        # Filters out guidance corrections that align with natural swerve frequencies
        filter_gain = 1.0 if np.linalg.norm(alpha_history) < 0.05 else 0.4
        return command_vec * filter_gain
