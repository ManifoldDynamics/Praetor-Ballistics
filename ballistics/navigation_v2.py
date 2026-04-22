import numpy as np
from scipy.linalg import inv

class InertialMeasurementUnitV2:
    """
    V2 Proprietary Inertial Measurement Unit (IMU).
    """
    def __init__(self, frequency_hz=100.0):
        self.fs = frequency_hz
        self.dt = 1.0 / frequency_hz
        self.accel_bias = np.array([0.01, -0.005, 0.008])
        self.accel_noise_std = 0.002
        self.accel_scale_err = np.diag([1.001, 0.999, 1.0])
        self.gyro_bias = np.array([0.0001, 0.0002, -0.0001])
        self.gyro_noise_std = 0.00005

    def sense(self, true_accel_body, true_omega_body, temperature_k=300.0):
        meas_accel = self.accel_scale_err @ true_accel_body
        thermal_drift = (temperature_k - 300.0) * 1e-4
        meas_accel += self.accel_bias + thermal_drift
        meas_omega = true_omega_body + self.gyro_bias + thermal_drift * 0.1
        meas_accel += np.random.normal(0, self.accel_noise_std / np.sqrt(self.dt), 3)
        meas_omega += np.random.normal(0, self.gyro_noise_std / np.sqrt(self.dt), 3)
        return meas_accel, meas_omega

class GPSModelV2:
    """
    V2 Proprietary GNSS / GPS Model.
    """
    def __init__(self, update_rate_hz=5.0):
        self.fs = update_rate_hz
        self.dt = 1.0 / update_rate_hz
        self.pos_error_std = 2.5
        self.vel_error_std = 0.1
        self.is_locked = True

    def get_update(self, t, true_pos_ecef, true_vel_ecef):
        if not self.is_locked: return None, None
        return true_pos_ecef + np.random.normal(0, self.pos_error_std, 3), true_vel_ecef + np.random.normal(0, self.vel_error_std, 3)

class NavigationFilterV2:
    """
    V2 Proprietary Navigation EKF.
    """
    def __init__(self, dt=0.01):
        self.dt = dt
        self.x = np.zeros(15)
        self.P = np.eye(15) * 1.0
        self.Q = np.eye(15) * 1e-4
        self.R_gps = np.diag([2.0, 2.0, 2.0, 0.1, 0.1, 0.1])**2

    def predict(self, imu_accel, imu_omega):
        F = np.eye(15)
        F[0:3, 3:6] = np.eye(3) * self.dt
        self.P = F @ self.P @ F.T + self.Q

    def update_gps(self, gps_pos, gps_vel):
        H = np.zeros((6, 15))
        H[0:3, 0:3] = np.eye(3); H[3:6, 3:6] = np.eye(3)
        z = np.concatenate([gps_pos, gps_vel])
        y = z - H @ self.x
        S = H @ self.P @ H.T + self.R_gps
        K = self.P @ H.T @ inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(15) - K @ H) @ self.P

    def get_estimated_state(self):
        return {'pos': self.x[0:3], 'vel': self.x[3:6]}

class PhasedArrayRadarV2:
    """V2 Phased Array."""
    def __init__(self, num_elements=64, freq_hz=9.5e9):
        self.n = num_elements; self.wavelength = 3e8 / freq_hz; self.d = self.wavelength / 2.0
    def calculate_beam_pattern(self, theta_steer, scan_angles):
        k = 2 * np.pi / self.wavelength
        steering_vector = np.exp(1j * k * self.d * np.arange(self.n) * np.sin(theta_steer))
        gains = []
        for theta in scan_angles:
            received = np.exp(1j * k * self.d * np.arange(self.n) * np.sin(theta))
            gains.append((np.abs(np.dot(np.conj(steering_vector), received)) / self.n)**2)
        return np.array(gains)

class NavigationSuiteV2:
    """V2 Suite."""
    def compute_pseudorange(self, sat_pos, true_pos, clock_bias):
        return np.linalg.norm(sat_pos - true_pos) + 3e8 * clock_bias + 5.0
    def terrain_match_update(self, sensed_alt, pos_est, terrain_model):
        return sensed_alt - terrain_model.get_elevation(pos_est[0], pos_est[1])
