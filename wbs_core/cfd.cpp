#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>
#include <vector>
#include <iostream>

namespace py = pybind11;

// A highly simplified 2D Axisymmetric Compressible Euler Solver
// using a basic explicit time-marching finite volume scheme.
// For the WBS MVP, we implement a first-order Lax-Friedrichs or highly simplified flux scheme
// to capture basic supersonic shock structures and pressure drag.

struct State {
    double rho;    // Density
    double rhou;   // X-momentum
    double rhov;   // Radial-momentum
    double E;      // Total Energy
};

inline double get_pressure(const State& U, double gamma) {
    // P = (gamma - 1) * (E - 0.5 * rho * (u^2 + v^2))
    double kinetic = 0.5 * (U.rhou * U.rhou + U.rhov * U.rhov) / U.rho;
    return (gamma - 1.0) * (U.E - kinetic);
}

// Calculate fluxes across a face
inline void compute_flux(const State& UL, const State& UR, double nx, double ny, double gamma, State& Flux) {
    // Extremely simplified Rusanov / Lax-Friedrichs flux for stability
    double pL = get_pressure(UL, gamma);
    double pR = get_pressure(UR, gamma);

    double uL = UL.rhou / UL.rho;
    double vL = UL.rhov / UL.rho;
    double cL = std::sqrt(gamma * pL / UL.rho);
    double vnL = uL * nx + vL * ny;

    double uR = UR.rhou / UR.rho;
    double vR = UR.rhov / UR.rho;
    double cR = std::sqrt(gamma * pR / UR.rho);
    double vnR = uR * nx + vR * ny;

    double s_max = std::max(std::abs(vnL) + cL, std::abs(vnR) + cR);

    State FL, FR;
    FL.rho = UL.rho * vnL;
    FL.rhou = UL.rhou * vnL + pL * nx;
    FL.rhov = UL.rhov * vnL + pL * ny;
    FL.E = (UL.E + pL) * vnL;

    FR.rho = UR.rho * vnR;
    FR.rhou = UR.rhou * vnR + pR * nx;
    FR.rhov = UR.rhov * vnR + pR * ny;
    FR.E = (UR.E + pR) * vnR;

    Flux.rho  = 0.5 * (FL.rho + FR.rho) - 0.5 * s_max * (UR.rho - UL.rho);
    Flux.rhou = 0.5 * (FL.rhou + FR.rhou) - 0.5 * s_max * (UR.rhou - UL.rhou);
    Flux.rhov = 0.5 * (FL.rhov + FR.rhov) - 0.5 * s_max * (UR.rhov - UL.rhov);
    Flux.E    = 0.5 * (FL.E + FR.E) - 0.5 * s_max * (UR.E - UL.E);
}

// Run the CFD solver loop
py::dict solve_cfd_2d(
    py::array_t<double> x_grid_arr,
    py::array_t<double> y_grid_arr,
    py::array_t<int> is_solid_arr,
    double mach_inf,
    double p_inf,
    double rho_inf,
    int iterations
) {
    auto x_grid = x_grid_arr.unchecked<2>();
    auto y_grid = y_grid_arr.unchecked<2>();
    auto is_solid = is_solid_arr.unchecked<2>();

    int nx = x_grid.shape(0);
    int ny = x_grid.shape(1);

    double gamma = 1.4;
    double c_inf = std::sqrt(gamma * p_inf / rho_inf);
    double u_inf = mach_inf * c_inf;
    double v_inf = 0.0;
    double E_inf = p_inf / (gamma - 1.0) + 0.5 * rho_inf * (u_inf * u_inf);

    // Initialize state
    std::vector<std::vector<State>> U(nx, std::vector<State>(ny));
    for (int i = 0; i < nx; ++i) {
        for (int j = 0; j < ny; ++j) {
            U[i][j].rho = rho_inf;
            U[i][j].rhou = rho_inf * u_inf;
            U[i][j].rhov = rho_inf * v_inf;
            U[i][j].E = E_inf;
        }
    }

    std::vector<std::vector<State>> U_new = U;

    // Calculate cell sizes (simplified Cartesian approximation for the MVP)
    double dx = x_grid(1,0) - x_grid(0,0);
    double dy = y_grid(0,1) - y_grid(0,0);

    // CFL condition
    double dt = 0.5 * std::min(dx, dy) / (u_inf + c_inf);

    double total_drag = 0.0;

    // Time marching loop
    for (int iter = 0; iter < iterations; ++iter) {
        total_drag = 0.0; // Reset drag accumulator

        for (int i = 1; i < nx - 1; ++i) {
            for (int j = 1; j < ny - 1; ++j) {
                if (is_solid(i, j)) continue;

                State F_right, F_left, F_top, F_bottom;

                // X fluxes
                if (is_solid(i+1, j)) {
                    // Wall boundary: reflect momentum
                    State wall_state = U[i][j];
                    wall_state.rhou = -wall_state.rhou;
                    compute_flux(U[i][j], wall_state, 1.0, 0.0, gamma, F_right);
                    total_drag += get_pressure(U[i][j], gamma) * dy;
                } else {
                    compute_flux(U[i][j], U[i+1][j], 1.0, 0.0, gamma, F_right);
                }

                if (is_solid(i-1, j)) {
                    State wall_state = U[i][j];
                    wall_state.rhou = -wall_state.rhou;
                    compute_flux(wall_state, U[i][j], 1.0, 0.0, gamma, F_left);
                    total_drag -= get_pressure(U[i][j], gamma) * dy;
                } else {
                    compute_flux(U[i-1][j], U[i][j], 1.0, 0.0, gamma, F_left);
                }

                // Y fluxes
                if (is_solid(i, j+1)) {
                    State wall_state = U[i][j];
                    wall_state.rhov = -wall_state.rhov;
                    compute_flux(U[i][j], wall_state, 0.0, 1.0, gamma, F_top);
                } else {
                    compute_flux(U[i][j], U[i][j+1], 0.0, 1.0, gamma, F_top);
                }

                if (is_solid(i, j-1)) {
                    State wall_state = U[i][j];
                    wall_state.rhov = -wall_state.rhov;
                    compute_flux(wall_state, U[i][j], 0.0, 1.0, gamma, F_bottom);
                } else {
                    compute_flux(U[i][j-1], U[i][j], 0.0, 1.0, gamma, F_bottom);
                }

                // Update state
                double inv_vol = 1.0 / (dx * dy);
                U_new[i][j].rho = U[i][j].rho - dt * inv_vol * ((F_right.rho - F_left.rho)*dy + (F_top.rho - F_bottom.rho)*dx);
                U_new[i][j].rhou = U[i][j].rhou - dt * inv_vol * ((F_right.rhou - F_left.rhou)*dy + (F_top.rhou - F_bottom.rhou)*dx);
                U_new[i][j].rhov = U[i][j].rhov - dt * inv_vol * ((F_right.rhov - F_left.rhov)*dy + (F_top.rhov - F_bottom.rhov)*dx);
                U_new[i][j].E = U[i][j].E - dt * inv_vol * ((F_right.E - F_left.E)*dy + (F_top.E - F_bottom.E)*dx);
            }
        }

        // Apply boundary conditions (Inlet/Outlet)
        for (int j = 0; j < ny; ++j) {
            U_new[0][j] = U_new[1][j]; // Inlet (simplified)
            U_new[nx-1][j] = U_new[nx-2][j]; // Outlet zero-gradient
        }
        for (int i = 0; i < nx; ++i) {
            U_new[i][ny-1] = U_new[i][ny-2]; // Far field
        }

        U = U_new;
    }

    // Extract results to numpy arrays
    auto density_out = py::array_t<double>({nx, ny});
    auto pressure_out = py::array_t<double>({nx, ny});
    auto d_buf = density_out.mutable_unchecked<2>();
    auto p_buf = pressure_out.mutable_unchecked<2>();

    for (int i = 0; i < nx; ++i) {
        for (int j = 0; j < ny; ++j) {
            if (is_solid(i, j)) {
                d_buf(i, j) = 0.0;
                p_buf(i, j) = 0.0;
            } else {
                d_buf(i, j) = U[i][j].rho;
                p_buf(i, j) = get_pressure(U[i][j], gamma);
            }
        }
    }

    py::dict results;
    results["density"] = density_out;
    results["pressure"] = pressure_out;
    results["drag_force"] = total_drag;

    // 2D reference area for an axisymmetric slice is essentially the radius
    double ref_area = std::abs(y_grid(0,0));
    double q_inf = 0.5 * rho_inf * u_inf * u_inf;
    double cd = (q_inf > 0 && ref_area > 0) ? total_drag / (q_inf * ref_area) : 0.0;

    results["cd"] = cd;

    return results;
}

PYBIND11_MODULE(wbs_cfd, m) {
    m.doc() = "Wilson Ballistic Suite C++ CFD Core";
    m.def("solve_cfd_2d", &solve_cfd_2d, "Run 2D Euler CFD solver");
}
