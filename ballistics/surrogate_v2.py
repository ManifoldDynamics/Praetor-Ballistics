import numpy as np
from scipy.spatial.distance import cdist
from scipy.linalg import cholesky, cho_solve

class GaussianProcessSurrogateV2:
    """
    V2 Proprietary Machine Learning Surrogate Model.
    """
    def __init__(self, kernel_type='matern', length_scale=1.0, noise=1e-6):
        self.kernel_type = kernel_type; self.ls = length_scale; self.noise = noise
        self.X_train = None; self.y_train = None; self.L = None; self.alpha = None

    def kernel(self, x1, x2):
        d2 = cdist(x1, x2, 'sqeuclidean')
        if self.kernel_type == 'matern':
            r = np.sqrt(d2 + 1e-12)
            return (1.0 + np.sqrt(5.0)*r/self.ls + 5.0*d2/(3.0*self.ls**2)) * np.exp(-np.sqrt(5.0)*r/self.ls)
        return np.exp(-0.5 * d2 / (self.ls**2))

    def train(self, X, y):
        self.X_train = X; self.y_train = y
        N = X.shape[0]
        K = self.kernel(X, X) + self.noise * np.eye(N)
        self.L = cholesky(K, lower=True)
        self.alpha = cho_solve((self.L, True), y)

    def predict(self, X_test):
        if self.L is None: raise ValueError("Not trained.")
        Ks = self.kernel(self.X_train, X_test)
        mu = Ks.T @ self.alpha
        v = np.linalg.solve(self.L, Ks)
        var = np.diag(self.kernel(X_test, X_test) - v.T @ v)
        return mu, var

class TrajectorySurrogateManagerV2:
    """
    V2 Strategic Surrogate Management.
    """
    def __init__(self, solver_6dof):
        self.solver = solver_6dof
        self.surrogates = {}

    def build_global_surrogate(self, input_bounds, n_samples=250):
        D = len(input_bounds)
        X = np.random.uniform([b[0] for b in input_bounds], [b[1] for b in input_bounds], (n_samples, D))

        y_range = []; y_drift = []; y_tof = []; y_energy = []

        for i in range(n_samples):
            v0, pitch, yaw = X[i]
            sol = self.solver.solve((0, 400), [0, 0, 0], v0, pitch, yaw, 2500.0)
            y_range.append(sol.y[0, -1])
            y_drift.append(sol.y[1, -1])
            y_tof.append(sol.t[-1])
            v_final = np.linalg.norm(sol.y[3:6, -1])
            y_energy.append(0.5 * self.solver.projectile.mass * v_final**2)

        for name, data in [('range', y_range), ('drift', y_drift), ('tof', y_tof), ('energy', y_energy)]:
            self.surrogates[name] = GaussianProcessSurrogateV2()
            self.surrogates[name].train(X, np.array(data))

        return X, np.array(y_range)

    def fast_predict(self, X_test):
        results = {}
        for name, gp in self.surrogates.items():
            results[name], results[f'{name}_var'] = gp.predict(X_test)
        return results
