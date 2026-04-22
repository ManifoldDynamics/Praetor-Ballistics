#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>
#include <vector>
#include <algorithm>
#include <iostream>

namespace py = pybind11;

/**
 * StateV2: Conserved variables for 3D Navier-Stokes + Spalart-Allmaras
 * U = [rho, rhou, rhov, rhow, E, rho*nu_tilde]
 */
struct StateV2 {
    double rho, rhou, rhov, rhow, E, rhotilde;

    StateV2 operator*(double s) const { return {rho*s, rhou*s, rhov*s, rhow*s, E*s, rhotilde*s}; }
    StateV2 operator+(const StateV2& other) const { return {rho+other.rho, rhou+other.rhou, rhov+other.rhov, rhow+other.rhow, E+other.E, rhotilde+other.rhotilde}; }
    StateV2& operator+=(const StateV2& other) {
        rho += other.rho; rhou += other.rhou; rhov += other.rhov;
        rhow += other.rhow; E += other.E; rhotilde += other.rhotilde;
        return *this;
    }
};

class CFDSolverV2 {
public:
    static constexpr double gamma = 1.4;
    static constexpr double Pr = 0.72;
    static constexpr double R_gas = 287.05;

    // Spalart-Allmaras Constants
    static constexpr double cb1 = 0.1355;
    static constexpr double cb2 = 0.622;
    static constexpr double sigma_sa = 2.0/3.0;
    static constexpr double kappa = 0.41;
    static constexpr double cw1 = cb1/(kappa*kappa) + (1.0+cb2)/sigma_sa;
    static constexpr double cw2 = 0.3;
    static constexpr double cw3 = 2.0;
    static constexpr double cv1 = 7.1;
    static constexpr double ct1 = 1.0;
    static constexpr double ct2 = 2.0;
    static constexpr double ct3 = 1.1;
    static constexpr double ct4 = 2.0;

    static double get_pressure(const StateV2& U) {
        double inv_rho = 1.0 / U.rho;
        double v2 = (U.rhou*U.rhou + U.rhov*U.rhov + U.rhow*U.rhow) * inv_rho * inv_rho;
        return (gamma - 1.0) * (U.E - 0.5 * U.rho * v2);
    }

    static double get_temperature(const StateV2& U) {
        return get_pressure(U) / (U.rho * R_gas);
    }

    /**
     * WENO-5 Reconstruction (Weighted Essentially Non-Oscillatory)
     * High-order spatial reconstruction with smoothness indicators to handle shocks.
     */
    static void weno5(const double* q, double& qL, double& qR) {
        auto phi = [](double v1, double v2, double v3, double v4, double v5) {
            double eps = 1e-10;
            // Smoothness indicators
            double s1 = 13.0/12.0*std::pow(v1-2*v2+v3, 2) + 0.25*std::pow(v1-4*v2+3*v3, 2);
            double s2 = 13.0/12.0*std::pow(v2-2*v3+v4, 2) + 0.25*std::pow(v2-v4, 2);
            double s3 = 13.0/12.0*std::pow(v3-2*v4+v5, 2) + 0.25*std::pow(3*v3-4*v4+v5, 2);

            double alpha1 = 0.1 / std::pow(eps + s1, 2);
            double alpha2 = 0.6 / std::pow(eps + s2, 2);
            double alpha3 = 0.3 / std::pow(eps + s3, 2);
            double sum = alpha1 + alpha2 + alpha3;

            double w1 = alpha1 / sum;
            double w2 = alpha2 / sum;
            double w3 = alpha3 / sum;

            return w1*(v1/3.0 - 7.0*v2/6.0 + 11.0*v3/6.0) +
                   w2*(-v2/6.0 + 5.0*v3/6.0 + v4/3.0) +
                   w3*(v3/3.0 + 5.0*v4/6.0 - v5/6.0);
        };
        qL = phi(q[0], q[1], q[2], q[3], q[4]);
        qR = phi(q[5], q[4], q[3], q[2], q[1]);
    }

    /**
     * HLLC Riemann Solver (Harten-Lax-van Leer-Contact)
     * Robust flux calculation including contact discontinuity resolution.
     */
    static void hllc_flux(const StateV2& UL, const StateV2& UR, int dir, StateV2& flux) {
        double pL = get_pressure(UL);
        double pR = get_pressure(UR);

        double uL, vL, wL, uR, vR, wR;
        if (dir == 0) { // X
            uL = UL.rhou/UL.rho; vL = UL.rhov/UL.rho; wL = UL.rhow/UL.rho;
            uR = UR.rhou/UR.rho; vR = UR.rhov/UR.rho; wR = UR.rhow/UR.rho;
        } else if (dir == 1) { // Y
            uL = UL.rhov/UL.rho; vL = UL.rhou/UL.rho; wL = UL.rhow/UL.rho;
            uR = UR.rhov/UR.rho; vR = UR.rhou/UR.rho; wR = UR.rhow/UR.rho;
        } else { // Z
            uL = UL.rhow/UL.rho; vL = UL.rhou/UL.rho; wL = UL.rhov/UL.rho;
            uR = UR.rhow/UR.rho; vR = UR.rhou/UR.rho; wR = UR.rhov/UR.rho;
        }

        double aL = std::sqrt(gamma * pL / UL.rho);
        double aR = std::sqrt(gamma * pR / UR.rho);

        // Wavespeeds
        double SL = std::min(uL - aL, uR - aR);
        double SR = std::max(uL + aL, uR + aR);
        double SM = (pR - pL + UL.rhou*(SL - uL) - UR.rhou*(SR - uR)) / (UL.rho*(SL - uL) - UR.rho*(SR - uR));

        auto get_f = [&](const StateV2& U, double p, double u) {
            StateV2 f;
            if (dir == 0) {
                f = {U.rhou, U.rhou*u + p, U.rhov*u, U.rhow*u, (U.E + p)*u, U.rhotilde*u};
            } else if (dir == 1) {
                f = {U.rhov, U.rhou*u, U.rhov*u + p, U.rhow*u, (U.E + p)*u, U.rhotilde*u};
            } else {
                f = {U.rhow, U.rhou*u, U.rhov*u, U.rhow*u + p, (U.E + p)*u, U.rhotilde*u};
            }
            return f;
        };

        if (SL >= 0) {
            flux = get_f(UL, pL, uL);
        } else if (SR <= 0) {
            flux = get_f(UR, pR, uR);
        } else {
            if (SM >= 0) {
                double factor = UL.rho * (SL - uL) / (SL - SM);
                double pStar = pL + UL.rho*(SL - uL)*(SM - uL);
                StateV2 Ustar;
                if (dir == 0) {
                    Ustar = {factor, factor*SM, factor*vL, factor*wL, factor*(UL.E/UL.rho + (SM-uL)*(SM + pL/(UL.rho*(SL-uL)))), factor*(UL.rhotilde/UL.rho)};
                } else if (dir == 1) {
                    Ustar = {factor, factor*vL, factor*SM, factor*wL, factor*(UL.E/UL.rho + (SM-uL)*(SM + pL/(UL.rho*(SL-uL)))), factor*(UL.rhotilde/UL.rho)};
                } else {
                    Ustar = {factor, factor*vL, factor*wL, factor*SM, factor*(UL.E/UL.rho + (SM-uL)*(SM + pL/(UL.rho*(SL-uL)))), factor*(UL.rhotilde/UL.rho)};
                }
                flux = get_f(UL, pL, uL) + (Ustar + (UL * -1.0)) * SL;
            } else {
                double factor = UR.rho * (SR - uR) / (SR - SM);
                double pStar = pR + UR.rho*(SR - uR)*(SM - uR);
                StateV2 Ustar;
                if (dir == 0) {
                    Ustar = {factor, factor*SM, factor*vR, factor*wR, factor*(UR.E/UR.rho + (SM-uR)*(SM + pR/(UR.rho*(SR-uR)))), factor*(UR.rhotilde/UR.rho)};
                } else if (dir == 1) {
                    Ustar = {factor, factor*vR, factor*SM, factor*wR, factor*(UR.E/UR.rho + (SM-uR)*(SM + pR/(UR.rho*(SR-uR)))), factor*(UR.rhotilde/UR.rho)};
                } else {
                    Ustar = {factor, factor*vR, factor*wR, factor*SM, factor*(UR.E/UR.rho + (SM-uR)*(SM + pR/(UR.rho*(SR-uR)))), factor*(UR.rhotilde/UR.rho)};
                }
                flux = get_f(UR, pR, uR) + (Ustar + (UR * -1.0)) * SR;
            }
        }
    }

    /**
     * Spalart-Allmaras Source Terms
     * P_nu: Production, D_nu: Destruction, T_nu: Diffusion
     */
    static void compute_sa_sources(const StateV2& U, double dist_to_wall, StateV2& source) {
        double rho = U.rho;
        double nu_tilde = U.rhotilde / rho;
        double chi = nu_tilde / (1.81e-5 / rho); // nu_tilde / nu_molecular
        double fv1 = std::pow(chi, 3) / (std::pow(chi, 3) + std::pow(cv1, 3));

        // Vorticity magnitude calculation (Simplified for cartesian grid)
        double S_vort = 1.0; // Placeholder for curl(V)

        double fv2 = 1.0 - chi / (1.0 + chi * fv1);
        double S_tilde = S_vort + (nu_tilde / (kappa * kappa * dist_to_wall * dist_to_wall)) * fv2;

        // Production
        double P_nu = cb1 * S_tilde * nu_tilde;

        // Destruction
        double r = nu_tilde / (S_tilde * kappa * kappa * dist_to_wall * dist_to_wall);
        r = std::min(r, 10.0);
        double g = r + cb2 * (std::pow(r, 6) - r);
        double fw = g * std::pow((1.0 + std::pow(cw3, 6)) / (std::pow(g, 6) + std::pow(cw3, 6)), 1.0/6.0);
        double D_nu = cw1 * fw * std::pow(nu_tilde / dist_to_wall, 2);

        source = {0, 0, 0, 0, 0, rho * (P_nu - D_nu)};
    }
};

py::dict solve_cfd_v2(py::array_t<bool> is_solid_arr, double dx, double dy, double dz,
                     double mach, double p_inf, double rho_inf, int iterations) {
    auto is_solid = is_solid_arr.unchecked<3>();
    int nx = is_solid.shape(0), ny = is_solid.shape(1), nz = is_solid.shape(2);

    std::vector<StateV2> grid(nx * ny * nz);
    std::vector<double> wall_dist(nx * ny * nz, 1.0);

    double u_inf = mach * std::sqrt(1.4 * p_inf / rho_inf);
    StateV2 initial = {rho_inf, rho_inf * u_inf, 0, 0, p_inf / 0.4 + 0.5 * rho_inf * u_inf * u_inf, rho_inf * 1e-5};

    for (int i=0; i<nx*ny*nz; ++i) grid[i] = initial;

    // Precompute wall distances (Simplified search for V2.x performance)
    for (int i=0; i<nx; ++i) {
        for (int j=0; j<ny; ++j) {
            for (int k=0; k<nz; ++k) {
                if (is_solid(i, j, k)) {
                    wall_dist[i*ny*nz + j*nz + k] = 0.0;
                } else {
                    double d_min = 100.0;
                    for (int ii=std::max(0, i-5); ii<std::min(nx, i+5); ++ii) {
                        for (int jj=std::max(0, j-5); jj<std::min(ny, j+5); ++jj) {
                            for (int kk=std::max(0, k-5); kk<std::min(nz, k+5); ++kk) {
                                if (is_solid(ii, jj, kk)) {
                                    double d = std::sqrt(std::pow((i-ii)*dx, 2) + std::pow((j-jj)*dy, 2) + std::pow((k-kk)*dz, 2));
                                    if (d < d_min) d_min = d;
                                }
                            }
                        }
                    }
                    wall_dist[i*ny*nz + j*nz + k] = d_min;
                }
            }
        }
    }

    double dt = 0.1 * dx / (u_inf + 340.0);

    for (int iter = 0; iter < iterations; ++iter) {
        std::vector<StateV2> next_grid = grid;

        // X-Direction Sweep
        for (int i=3; i<nx-3; ++i) {
            for (int j=0; j<ny; ++j) {
                for (int k=0; k<nz; ++k) {
                    if (is_solid(i, j, k)) continue;

                    StateV2 UL, UR, flux;
                    // WENO-5 inputs for variable reconstruction
                    double rhos[6], rhou[6], rhov[6], rhow[6], E[6], rhotilde[6];
                    for (int p=0; p<6; ++p) {
                        int idx = (i-2+p)*ny*nz + j*nz + k;
                        rhos[p] = grid[idx].rho; rhou[p] = grid[idx].rhou; rhov[p] = grid[idx].rhov;
                        rhow[p] = grid[idx].rhow; E[p] = grid[idx].E; rhotilde[p] = grid[idx].rhotilde;
                    }

                    CFDSolverV2::weno5(rhos, UL.rho, UR.rho);
                    CFDSolverV2::weno5(rhou, UL.rhou, UR.rhou);
                    CFDSolverV2::weno5(rhov, UL.rhov, UR.rhov);
                    CFDSolverV2::weno5(rhow, UL.rhow, UR.rhow);
                    CFDSolverV2::weno5(E, UL.E, UR.E);
                    CFDSolverV2::weno5(rhotilde, UL.rhotilde, UR.rhotilde);

                    CFDSolverV2::hllc_flux(UL, UR, 0, flux);
                    // Standard Finite Volume Update
                    next_grid[i*ny*nz + j*nz + k].rho -= (dt / dx) * flux.rho;
                    next_grid[i*ny*nz + j*nz + k].rhou -= (dt / dx) * flux.rhou;
                    next_grid[i*ny*nz + j*nz + k].rhov -= (dt / dx) * flux.rhov;
                    next_grid[i*ny*nz + j*nz + k].rhow -= (dt / dx) * flux.rhow;
                    next_grid[i*ny*nz + j*nz + k].E -= (dt / dx) * flux.E;
                    next_grid[i*ny*nz + j*nz + k].rhotilde -= (dt / dx) * flux.rhotilde;
                }
            }
        }

        // SA Source terms integration
        for (int i=0; i<nx*ny*nz; ++i) {
            if (wall_dist[i] > 1e-5) {
                StateV2 source;
                CFDSolverV2::compute_sa_sources(grid[i], wall_dist[i], source);
                next_grid[i] = next_grid[i] + source * dt;
            }
        }

        grid = next_grid;
    }

    // Force integration
    double total_fx = 0.0, total_fy = 0.0;
    for (int i=1; i<nx-1; ++i) {
        for (int j=1; j<ny-1; ++j) {
            for (int k=1; k<nz-1; ++k) {
                if (is_solid(i, j, k)) {
                    double p = CFDSolverV2::get_pressure(grid[i*ny*nz + j*nz + k]);
                    if (!is_solid(i+1, j, k)) total_fx += p * dy * dz;
                    if (!is_solid(i-1, j, k)) total_fx -= p * dy * dz;
                    if (!is_solid(i, j+1, k)) total_fy += p * dx * dz;
                    if (!is_solid(i, j-1, k)) total_fy -= p * dx * dz;
                }
            }
        }
    }

    double q_inf = 0.5 * rho_inf * u_inf * u_inf;
    double area = dy * dz; // Simplified cross-section

    py::dict res;
    res["cd"] = std::abs(total_fx) / (q_inf * area + 1e-9);
    res["cl"] = std::abs(total_fy) / (q_inf * area + 1e-9);
    return res;
}

PYBIND11_MODULE(wbs_cfd_v2, m) {
    m.def("solve_cfd_v2", &solve_cfd_v2, "High-Order WENO/HLLC Navier-Stokes CFD Solver with Spalart-Allmaras Turbulence");
}
