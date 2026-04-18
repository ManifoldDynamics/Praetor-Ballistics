#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>
#include <vector>
#include <iostream>

namespace py = pybind11;

struct State3D {
    double rho;    // Density
    double rhou;   // X-momentum
    double rhov;   // Y-momentum
    double rhow;   // Z-momentum
    double E;      // Total Energy
};

inline double get_pressure(const State3D& U, double gamma) {
    double kinetic = 0.5 * (U.rhou * U.rhou + U.rhov * U.rhov + U.rhow * U.rhow) / U.rho;
    return (gamma - 1.0) * (U.E - kinetic);
}

// Highly simplified Rusanov / Lax-Friedrichs flux for 3D stability
inline void compute_flux_3d(const State3D& UL, const State3D& UR, double nx, double ny, double nz, double gamma, State3D& Flux) {
    double pL = get_pressure(UL, gamma);
    double pR = get_pressure(UR, gamma);

    double uL = UL.rhou / UL.rho;
    double vL = UL.rhov / UL.rho;
    double wL = UL.rhow / UL.rho;
    double cL = std::sqrt(gamma * pL / UL.rho);
    double vnL = uL * nx + vL * ny + wL * nz;

    double uR = UR.rhou / UR.rho;
    double vR = UR.rhov / UR.rho;
    double wR = UR.rhow / UR.rho;
    double cR = std::sqrt(gamma * pR / UR.rho);
    double vnR = uR * nx + vR * ny + wR * nz;

    double s_max = std::max(std::abs(vnL) + cL, std::abs(vnR) + cR);

    State3D FL, FR;
    FL.rho = UL.rho * vnL;
    FL.rhou = UL.rhou * vnL + pL * nx;
    FL.rhov = UL.rhov * vnL + pL * ny;
    FL.rhow = UL.rhow * vnL + pL * nz;
    FL.E = (UL.E + pL) * vnL;

    FR.rho = UR.rho * vnR;
    FR.rhou = UR.rhou * vnR + pR * nx;
    FR.rhov = UR.rhov * vnR + pR * ny;
    FR.rhow = UR.rhow * vnR + pR * nz;
    FR.E = (UR.E + pR) * vnR;

    Flux.rho  = 0.5 * (FL.rho + FR.rho) - 0.5 * s_max * (UR.rho - UL.rho);
    Flux.rhou = 0.5 * (FL.rhou + FR.rhou) - 0.5 * s_max * (UR.rhou - UL.rhou);
    Flux.rhov = 0.5 * (FL.rhov + FR.rhov) - 0.5 * s_max * (UR.rhov - UL.rhov);
    Flux.rhow = 0.5 * (FL.rhow + FR.rhow) - 0.5 * s_max * (UR.rhow - UL.rhow);
    Flux.E    = 0.5 * (FL.E + FR.E) - 0.5 * s_max * (UR.E - UL.E);
}

// 3D CFD Solver
py::dict solve_cfd_3d(
    py::array_t<bool> is_solid_arr,
    double dx, double dy, double dz,
    double mach_inf,
    double p_inf,
    double rho_inf,
    int iterations,
    double alpha_rad // Angle of attack
) {
    auto is_solid = is_solid_arr.unchecked<3>();

    int nx = is_solid.shape(0);
    int ny = is_solid.shape(1);
    int nz = is_solid.shape(2);

    double gamma = 1.4;
    double c_inf = std::sqrt(gamma * p_inf / rho_inf);

    // Freestream velocity components based on angle of attack (alpha is pitch, so Z direction)
    double v_mag = mach_inf * c_inf;
    double u_inf = v_mag * std::cos(alpha_rad);
    double v_inf = 0.0;
    double w_inf = v_mag * std::sin(alpha_rad);
    double E_inf = p_inf / (gamma - 1.0) + 0.5 * rho_inf * (u_inf * u_inf + v_inf * v_inf + w_inf * w_inf);

    // Initialize state matrices (flattened for performance)
    std::vector<State3D> U(nx * ny * nz);
    for (int i = 0; i < nx; ++i) {
        for (int j = 0; j < ny; ++j) {
            for (int k = 0; k < nz; ++k) {
                int idx = i*ny*nz + j*nz + k;
                U[idx].rho = rho_inf;
                U[idx].rhou = rho_inf * u_inf;
                U[idx].rhov = rho_inf * v_inf;
                U[idx].rhow = rho_inf * w_inf;
                U[idx].E = E_inf;
            }
        }
    }

    std::vector<State3D> U_new = U;

    // CFL condition
    double dt = 0.5 * std::min({dx, dy, dz}) / (v_mag + c_inf);
    double inv_vol = 1.0 / (dx * dy * dz);

    double total_drag = 0.0;
    double total_lift = 0.0;

    // Print progress context
    int report_step = iterations / 10;
    if (report_step == 0) report_step = 1;

    for (int iter = 0; iter < iterations; ++iter) {
        total_drag = 0.0;
        total_lift = 0.0;

        for (int i = 1; i < nx - 1; ++i) {
            for (int j = 1; j < ny - 1; ++j) {
                for (int k = 1; k < nz - 1; ++k) {
                    if (is_solid(i, j, k)) continue;

                    int idx = i*ny*nz + j*nz + k;
                    State3D F_R, F_L, F_T, F_B, F_F, F_K;

                    // X fluxes (Faces i+1/2, i-1/2)
                    if (is_solid(i+1, j, k)) {
                        State3D wall = U[idx]; wall.rhou = -wall.rhou;
                        compute_flux_3d(U[idx], wall, 1.0, 0.0, 0.0, gamma, F_R);
                        total_drag += get_pressure(U[idx], gamma) * dy * dz; // Drag force element
                    } else {
                        compute_flux_3d(U[idx], U[(i+1)*ny*nz + j*nz + k], 1.0, 0.0, 0.0, gamma, F_R);
                    }

                    if (is_solid(i-1, j, k)) {
                        State3D wall = U[idx]; wall.rhou = -wall.rhou;
                        compute_flux_3d(wall, U[idx], 1.0, 0.0, 0.0, gamma, F_L);
                        total_drag -= get_pressure(U[idx], gamma) * dy * dz;
                    } else {
                        compute_flux_3d(U[(i-1)*ny*nz + j*nz + k], U[idx], 1.0, 0.0, 0.0, gamma, F_L);
                    }

                    // Y fluxes (Faces j+1/2, j-1/2)
                    if (is_solid(i, j+1, k)) {
                        State3D wall = U[idx]; wall.rhov = -wall.rhov;
                        compute_flux_3d(U[idx], wall, 0.0, 1.0, 0.0, gamma, F_T);
                    } else {
                        compute_flux_3d(U[idx], U[i*ny*nz + (j+1)*nz + k], 0.0, 1.0, 0.0, gamma, F_T);
                    }

                    if (is_solid(i, j-1, k)) {
                        State3D wall = U[idx]; wall.rhov = -wall.rhov;
                        compute_flux_3d(wall, U[idx], 0.0, 1.0, 0.0, gamma, F_B);
                    } else {
                        compute_flux_3d(U[i*ny*nz + (j-1)*nz + k], U[idx], 0.0, 1.0, 0.0, gamma, F_B);
                    }

                    // Z fluxes (Faces k+1/2, k-1/2) - Z is our vertical axis for lift
                    if (is_solid(i, j, k+1)) {
                        State3D wall = U[idx]; wall.rhow = -wall.rhow;
                        compute_flux_3d(U[idx], wall, 0.0, 0.0, 1.0, gamma, F_F);
                        total_lift += get_pressure(U[idx], gamma) * dx * dy;
                    } else {
                        compute_flux_3d(U[idx], U[i*ny*nz + j*nz + (k+1)], 0.0, 0.0, 1.0, gamma, F_F);
                    }

                    if (is_solid(i, j, k-1)) {
                        State3D wall = U[idx]; wall.rhow = -wall.rhow;
                        compute_flux_3d(wall, U[idx], 0.0, 0.0, 1.0, gamma, F_K);
                        total_lift -= get_pressure(U[idx], gamma) * dx * dy;
                    } else {
                        compute_flux_3d(U[i*ny*nz + j*nz + (k-1)], U[idx], 0.0, 0.0, 1.0, gamma, F_K);
                    }

                    // Update state
                    U_new[idx].rho = U[idx].rho - dt * inv_vol * ((F_R.rho - F_L.rho)*dy*dz + (F_T.rho - F_B.rho)*dx*dz + (F_F.rho - F_K.rho)*dx*dy);
                    U_new[idx].rhou = U[idx].rhou - dt * inv_vol * ((F_R.rhou - F_L.rhou)*dy*dz + (F_T.rhou - F_B.rhou)*dx*dz + (F_F.rhou - F_K.rhou)*dx*dy);
                    U_new[idx].rhov = U[idx].rhov - dt * inv_vol * ((F_R.rhov - F_L.rhov)*dy*dz + (F_T.rhov - F_B.rhov)*dx*dz + (F_F.rhov - F_K.rhov)*dx*dy);
                    U_new[idx].rhow = U[idx].rhow - dt * inv_vol * ((F_R.rhow - F_L.rhow)*dy*dz + (F_T.rhow - F_B.rhow)*dx*dz + (F_F.rhow - F_K.rhow)*dx*dy);
                    U_new[idx].E = U[idx].E - dt * inv_vol * ((F_R.E - F_L.E)*dy*dz + (F_T.E - F_B.E)*dx*dz + (F_F.E - F_K.E)*dx*dy);
                }
            }
        }

        // Simple Boundary Conditions (Freestream boundaries)
        for (int j = 0; j < ny; ++j) {
            for (int k = 0; k < nz; ++k) {
                U_new[0*ny*nz + j*nz + k] = U_new[1*ny*nz + j*nz + k]; // Inlet
                U_new[(nx-1)*ny*nz + j*nz + k] = U_new[(nx-2)*ny*nz + j*nz + k]; // Outlet
            }
        }
        for (int i = 0; i < nx; ++i) {
            for (int k = 0; k < nz; ++k) {
                U_new[i*ny*nz + 0*nz + k] = U_new[i*ny*nz + 1*nz + k]; // Y-walls
                U_new[i*ny*nz + (ny-1)*nz + k] = U_new[i*ny*nz + (ny-2)*nz + k];
            }
            for (int j = 0; j < ny; ++j) {
                U_new[i*ny*nz + j*nz + 0] = U_new[i*ny*nz + j*nz + 1]; // Z-walls
                U_new[i*ny*nz + j*nz + (nz-1)] = U_new[i*ny*nz + j*nz + (nz-2)];
            }
        }

        U = U_new;

        if (iter % report_step == 0) {
            std::cout << "CFD Iteration " << iter << "/" << iterations << " | Drag: " << total_drag << " N | Lift: " << total_lift << " N\n";
        }
    }

    // Export pressure field (Central Z slice for visualization)
    int slice_z = nz / 2;
    auto pressure_slice = py::array_t<double>({nx, ny});
    auto p_buf = pressure_slice.mutable_unchecked<2>();

    for (int i = 0; i < nx; ++i) {
        for (int j = 0; j < ny; ++j) {
            if (is_solid(i, j, slice_z)) {
                p_buf(i, j) = 0.0;
            } else {
                p_buf(i, j) = get_pressure(U[i*ny*nz + j*nz + slice_z], gamma);
            }
        }
    }

    py::dict results;
    results["pressure_slice_z"] = pressure_slice;
    results["drag_force"] = total_drag;
    results["lift_force"] = total_lift;

    // Calculate empirical reference area (cross-section of the bounding box)
    // To find the true reference area of the voxelized mesh, we count solid pixels in the YZ plane.
    double ref_area = 0.0;
    for (int j = 0; j < ny; ++j) {
        for (int k = 0; k < nz; ++k) {
            // If any voxel in this column is solid, it contributes to the frontal area
            bool is_frontal = false;
            for (int i = 0; i < nx; ++i) {
                if (is_solid(i, j, k)) {
                    is_frontal = true;
                    break;
                }
            }
            if (is_frontal) {
                ref_area += (dy * dz);
            }
        }
    }

    double q_inf = 0.5 * rho_inf * v_mag * v_mag;
    double cd = (q_inf > 0 && ref_area > 0) ? total_drag / (q_inf * ref_area) : 0.0;
    double cl = (q_inf > 0 && ref_area > 0) ? total_lift / (q_inf * ref_area) : 0.0;

    results["cd"] = cd;
    results["cl"] = cl;
    results["ref_area"] = ref_area;

    return results;
}

PYBIND11_MODULE(wbs_cfd_3d, m) {
    m.doc() = "Wilson Ballistic Suite C++ 3D CFD Core";
    m.def("solve_cfd_3d", &solve_cfd_3d, "Run 3D Euler CFD solver on a boolean voxel grid");
}
