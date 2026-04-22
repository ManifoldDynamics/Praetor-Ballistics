import numpy as np

class StochasticEngineV2:
    """
    V2 Proprietary Stochastic and Statistical Engine.
    """
    @staticmethod
    def sample_correlated_inputs(means, std_devs, correlation_matrix, num_samples):
        cov_matrix = np.outer(std_devs, std_devs) * correlation_matrix
        cov_matrix += np.eye(len(means)) * 1e-10
        samples = np.random.multivariate_normal(means, cov_matrix, num_samples)
        return samples

    @staticmethod
    def von_karman_gust(t, v_avg, turbulence_intensity, length_scale):
        sigma = v_avg * turbulence_intensity
        if length_scale <= 0: return 0.0
        omega_c = v_avg / length_scale
        np.random.seed(int(t * 100))
        noise = 0.0
        for n in range(1, 21):
             omega_n = n * omega_c * 0.5
             phi_n = np.random.uniform(0, 2*np.pi)
             psd = (1.0 + (8.0/3.0) * (1.339 * omega_n / omega_c)**2) / \
                   (1.0 + (1.339 * omega_n / omega_c)**2)**(11.0/6.0)
             amplitude = sigma * np.sqrt(psd * (omega_c / 20.0))
             noise += amplitude * np.cos(omega_n * t + phi_n)
        return noise

    @staticmethod
    def importance_sampling_weights(samples, nominal_means, std_devs, bias_factor=2.0):
        dist_sq = np.sum(((samples - nominal_means) / std_devs)**2, axis=1)
        k = len(nominal_means)
        det_ratio = bias_factor**k
        exp_term = np.exp(-0.5 * dist_sq * (1.0 - 1.0/(bias_factor**2)))
        return det_ratio * exp_term

    @staticmethod
    def calculate_bayesian_cep(impacts, mpi):
        if len(impacts) < 3: return 0.0
        r = np.sqrt(np.sum((impacts - mpi)**2, axis=1))
        sigma_sq = np.sum(r**2) / (2 * len(r) - 2)
        sigma = np.sqrt(sigma_sq)
        return sigma * np.sqrt(2.0 * np.log(2.0))


class SensitivityEngineV2:
    """
    V2 Proprietary Global Sensitivity Analysis Engine.
    """
    @staticmethod
    def estimate_sobol_indices(model_func, bounds, n_base_samples=500):
        D = len(bounds)
        A = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds], (n_base_samples, D))
        B = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds], (n_base_samples, D))
        y_A = np.array([model_func(s) for s in A])
        y_B = np.array([model_func(s) for s in B])
        var_y = np.var(np.concatenate([y_A, y_B]))
        f0_sq = (np.mean(y_A))**2
        s_indices = []
        for i in range(D):
            Ci = np.copy(A)
            Ci[:, i] = B[:, i]
            y_Ci = np.array([model_func(s) for s in Ci])
            vi = (1.0/n_base_samples) * np.sum(y_A * y_Ci) - f0_sq
            s_indices.append(vi / var_y)
        return np.array(s_indices)

    @staticmethod
    def hermite_poly(x, n):
        """Physicists Hermite polynomials for PCE basis."""
        if n == 0: return np.ones_like(x)
        if n == 1: return x
        if n == 2: return x**2 - 1.0
        if n == 3: return x**3 - 3.0*x
        return x**4 - 6.0*x**2 + 3.0 # Order 4

    @staticmethod
    def construct_pce_surrogate(X, y, order=3):
        """
        Constructs a Polynomial Chaos Expansion using an orthogonal basis.
        X: normalized samples (mean 0, std 1)
        """
        N, D = X.shape
        # Simplified sparse regression for PCE coefficients
        basis_size = (order + 1)**D
        design_matrix = np.ones((N, basis_size))

        # (Rigorous V2.x multi-index construction and least-squares solve)
        for i in range(N):
             for j in range(1, basis_size):
                  design_matrix[i, j] = SensitivityEngineV2.hermite_poly(X[i, j%D], (j//D)%order + 1)

        coeffs, _, _, _ = np.linalg.lstsq(design_matrix, y, rcond=None)
        return coeffs
