import numpy as np
from scipy.linalg import inv

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
        Uses Stefan-Boltzmann law integrated over a hemisphere.
        """
        total_power = emissivity * IRSignatureModelV2.SIGMA * projected_area_m2 * (temperature_k**4)
        return total_power / np.pi

    @staticmethod
    def calculate_snr(intensity, range_m, detector_nep=1e-12, optics_aperture_m2=0.01):
        """
        Calculates Signal-to-Noise Ratio at the seeker detector.
        Accounts for 1/R^2 power drop and detector Noise Equivalent Power (NEP).
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
        Incorporates angular jitter and range estimation errors.
        """
        if snr < self.snr_threshold:
            return None, None

        # Deterministic seed based on time to ensure integrator stability
        seed_t = int(t * self.fs)
        rng = np.random.RandomState(seed_t)

        # Noise scales inversely with SNR
        noise_scale = 1.0 + (5.0 / max(0.1, snr))

        r_vec = truth_pos - projectile_pos
        range_mag = np.linalg.norm(r_vec)

        if range_mag < 0.1:
            return truth_pos, truth_vel

        # 1. Angular Noise (Jitter)
        jitter_std = self.angle_noise * noise_scale * range_mag
        noise_vec = rng.normal(0, jitter_std, 3)
        r_hat = r_vec / range_mag
        noise_perp = noise_vec - np.dot(noise_vec, r_hat) * r_hat

        # 2. Range Noise
        range_err = rng.normal(0, self.range_noise * noise_scale)

        sensed_pos = truth_pos + noise_perp + r_hat * range_err

        # 3. Velocity estimation noise
        sensed_vel = truth_vel + rng.normal(0, 0.2 * noise_scale, 3)

        return sensed_pos, sensed_vel

    @staticmethod
    def apply_epicyclic_filter(command_vec, alpha_history, cutoff_freq=5.0):
        """
        V2.x Proprietary Epicyclic Low-Pass Filter.
        Ignores high-frequency stabilizing nutation/precession wobbles in the guidance loop.
        """
        if alpha_history is None or len(alpha_history) < 2:
            return command_vec

        swerve_mag = np.linalg.norm(np.diff(alpha_history, axis=0)) if hasattr(alpha_history, 'ndim') and alpha_history.ndim > 1 else 0.0
        filter_gain = 1.0 / (1.0 + 10.0 * swerve_mag)
        return command_vec * max(0.2, filter_gain)


class ExtendedKalmanFilterV2:
    """
    V2 Proprietary Extended Kalman Filter (EKF) for seeker state estimation.
    Tracks target position, velocity, and acceleration using non-linear measurements.
    """
    def __init__(self, dt=0.02):
        self.dt = dt
        # State: [px, py, pz, vx, vy, vz, ax, ay, az]
        self.x = np.zeros(9)
        self.P = np.eye(9) * 100.0

        # Process Noise Covariance Q
        self.Q = np.eye(9) * 0.05
        # Measurement Noise Covariance R (Az, El, Range)
        self.R = np.diag([0.002**2, 0.002**2, 2.0**2])

    def predict(self):
        """State transition: x_k = F * x_{k-1} + Q"""
        F = np.eye(9)
        dt = self.dt
        F[0:3, 3:6] = np.eye(3) * dt
        F[0:3, 6:9] = np.eye(3) * (0.5 * dt**2)
        F[3:6, 6:9] = np.eye(3) * dt

        self.x = F @ self.x
        self.P = F @ self.P @ F.T + self.Q

    def update(self, measurement, seeker_pos):
        """
        Non-linear update using [Azimuth, Elevation, Range].
        """
        relative_pos = self.x[0:3] - seeker_pos
        px, py, pz = relative_pos
        r = np.linalg.norm(relative_pos)
        if r < 0.1: return

        h_x = np.array([
            np.arctan2(py, px),
            np.arcsin(pz / r),
            r
        ])

        H = np.zeros((3, 9))
        r2_xy = px**2 + py**2

        H[0, 0] = -py / r2_xy
        H[0, 1] = px / r2_xy
        H[1, 0] = -(px * pz) / (r**2 * np.sqrt(r2_xy))
        H[1, 1] = -(py * pz) / (r**2 * np.sqrt(r2_xy))
        H[1, 2] = np.sqrt(r2_xy) / r**2
        H[2, 0:3] = [px/r, py/r, pz/r]

        y = measurement - h_x
        y[0] = (y[0] + np.pi) % (2 * np.pi) - np.pi

        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ inv(S)

        self.x = self.x + K @ y
        self.P = (np.eye(9) - K @ H) @ self.P


class RadarSignalProcessorV2:
    """
    V2 Proprietary Radar & Signal Processing Engine.
    """
    @staticmethod
    def calculate_rcs_po(geometry, freq_hz, aspect_angle_rad):
        """
        Physical Optics (PO) approximation for RCS.
        """
        k = 2.0 * np.pi * freq_hz / 3e8
        L = geometry.total_length
        R = geometry.caliber / 2.0

        theta = aspect_angle_rad
        if abs(theta) < 1e-6:
            return 2.0 * np.pi * R * L**2 * k

        val = k * L * np.sin(theta)
        sinc_term = (np.sin(val) / val)**2
        sigma = (k * R * L**2) * sinc_term * (np.cos(theta)**2)

        return max(1e-4, sigma)

    @staticmethod
    def generate_clutter_k_distribution(num_samples, shape_v=1.5, scale_b=1.0):
        """
        Generates non-Rayleigh radar clutter using the K-distribution.
        """
        gamma_samples = np.random.gamma(shape_v, scale_b, num_samples)
        rayleigh_samples = np.random.rayleigh(1.0, num_samples)
        return gamma_samples * rayleigh_samples

    @staticmethod
    def pulse_compression_lfm(signal, sweep_bw, pulse_width):
        """
        Applies LFM (Linear Frequency Modulation) pulse compression.
        """
        n = len(signal)
        t = np.linspace(-pulse_width/2, pulse_width/2, n)
        ref_chirp = np.exp(1j * np.pi * (sweep_bw / pulse_width) * t**2)
        compressed = np.fft.ifft(np.fft.fft(signal) * np.conj(np.fft.fft(ref_chirp)))
        return np.abs(compressed)

    @staticmethod
    def cell_averaging_cfar(power_map, guard_cells=2, ref_cells=6, p_fa=1e-6):
        """
        CA-CFAR implementation.
        """
        num_cells = len(power_map)
        detections = np.zeros(num_cells, dtype=bool)
        N = 2 * ref_cells
        alpha = N * (p_fa**(-1.0/N) - 1.0)

        for i in range(ref_cells + guard_cells, num_cells - (ref_cells + guard_cells)):
            noise_sum = (np.sum(power_map[i-ref_cells-guard_cells : i-guard_cells]) +
                         np.sum(power_map[i+guard_cells+1 : i+guard_cells+ref_cells+1]))
            noise_avg = noise_sum / N
            if power_map[i] > alpha * noise_avg:
                detections[i] = True
        return detections
