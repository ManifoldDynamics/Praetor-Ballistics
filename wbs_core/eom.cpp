#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>
#include <array>
#include <algorithm>
#include <stdexcept>
#include <iostream>

namespace py = pybind11;

// Helper: 3D vector magnitude
inline double norm3(const double* v) {
    return std::sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]);
}

// Helper: 4D vector (quaternion) magnitude
inline double norm4(const double* q) {
    return std::sqrt(q[0]*q[0] + q[1]*q[1] + q[2]*q[2] + q[3]*q[3]);
}

// Helper: 3x3 Matrix-Vector multiplication
inline void mat_vec_mult(const double M[3][3], const double* v, double* out) {
    out[0] = M[0][0]*v[0] + M[0][1]*v[1] + M[0][2]*v[2];
    out[1] = M[1][0]*v[0] + M[1][1]*v[1] + M[1][2]*v[2];
    out[2] = M[2][0]*v[0] + M[2][1]*v[1] + M[2][2]*v[2];
}

// Helper: Cross product
inline void cross_product(const double* a, const double* b, double* out) {
    out[0] = a[1]*b[2] - a[2]*b[1];
    out[1] = a[2]*b[0] - a[0]*b[2];
    out[2] = a[0]*b[1] - a[1]*b[0];
}

// Equivalent of quaternion_to_rotation_matrix
inline void quat_to_rot_mat(const double* q_in, double R[3][3]) {
    double q[4] = {q_in[0], q_in[1], q_in[2], q_in[3]};
    double n = norm4(q);
    if (n > 1e-12) {
        q[0] /= n; q[1] /= n; q[2] /= n; q[3] /= n;
    }

    double q0 = q[0], q1 = q[1], q2 = q[2], q3 = q[3];

    R[0][0] = q0*q0 + q1*q1 - q2*q2 - q3*q3;
    R[0][1] = 2.0*(q1*q2 - q0*q3);
    R[0][2] = 2.0*(q1*q3 + q0*q2);

    R[1][0] = 2.0*(q1*q2 + q0*q3);
    R[1][1] = q0*q0 - q1*q1 + q2*q2 - q3*q3;
    R[1][2] = 2.0*(q2*q3 - q0*q1);

    R[2][0] = 2.0*(q1*q3 - q0*q2);
    R[2][1] = 2.0*(q2*q3 + q0*q1);
    R[2][2] = q0*q0 - q1*q1 - q2*q2 + q3*q3;
}

// Helper: Matrix transpose
inline void transpose(const double M[3][3], double Mt[3][3]) {
    for (int i=0; i<3; ++i) {
        for (int j=0; j<3; ++j) {
            Mt[i][j] = M[j][i];
        }
    }
}

// C++ Implementation of get_eom
py::array_t<double> get_eom_cpp(
    double t,
    py::array_t<double> state_arr,

    // Projectile physical properties
    double proj_mass,
    double proj_diam,
    double proj_ref_area,
    double proj_ix,
    double proj_iy,

    // Aerodynamics (We pass the coefficients pre-evaluated at the current Mach, or as arrays.
    // Wait, predicting aero inside C++ requires calling Python interpolation, which is slow.
    // Instead, we can pass arrays to C++ and do linear interpolation in C++!)
    // For simplicity, we will assume Python evaluates the atmosphere and Mach BEFORE calling C++,
    // OR we implement the atmosphere/aero table lookups in C++.

    // Actually, calling python callbacks for `cd(mach)` from C++ defeats the speedup.
    // Let's pass the pre-computed coefficients and environment variables evaluated in Python
    // for this specific state.
    // WAIT: The integrator (solve_ivp) calls get_eom thousands of times with different states.
    // If we only evaluate the environment/aero in Python beforehand, it won't be accurate for the RK45 intermediate steps.
    // We MUST do the interpolation in C++.

    // Environment standard constants
    double atm_T0, double atm_P0, double atm_L, double atm_R, double atm_G, double atm_RH,
    double earth_G0, double earth_R_EARTH, double earth_OMEGA, double latitude_rad,

    // Aero arrays (mach, cd, cl, cma, cmaq, cnlp, cmag)
    py::array_t<double> aero_mach_arr,
    py::array_t<double> aero_cd_arr,
    py::array_t<double> aero_cl_arr,
    py::array_t<double> aero_cma_arr,
    py::array_t<double> aero_cmaq_arr,
    py::array_t<double> aero_cnlp_arr,
    py::array_t<double> aero_cmag_arr,

    // Wind vector (assuming constant for C++ speedup, or evaluating it. We'll pass a constant wind vector for now)
    double wind_vx, double wind_vy, double wind_vz,

    // Propulsion
    bool prop_active, double prop_thrust_n, double prop_burn_time_s, double prop_mass_kg,

    // Hypersonics
    bool hyper_active, double mat_density, double mat_cp, double mat_eps, double nose_rad
) {

    auto state = state_arr.unchecked<1>();
    int state_len = state.shape(0);

    // 1. Unpack State
    double pos[3] = {state(0), state(1), state(2)};
    double vel[3] = {state(3), state(4), state(5)};
    double q[4] = {state(6), state(7), state(8), state(9)};
    double omega[3] = {state(10), state(11), state(12)};
    double T_nose = (state_len > 13) ? state(13) : 300.0;

    double altitude = pos[2];

    // Stop condition (Ground hit)
    if (altitude < 0.0 && vel[2] < 0.0) {
        auto result = py::array_t<double>(state_len);
        auto res_buf = result.mutable_unchecked<1>();
        for (int i=0; i<state_len; ++i) res_buf(i) = 0.0;
        return result;
    }

    // 2. Environment (Atmosphere)
    double T_atm, P_atm;
    double alt_c = std::max(0.0, altitude);
    if (alt_c < 11000.0) {
        T_atm = atm_T0 + atm_L * alt_c;
        P_atm = atm_P0 * std::pow(T_atm / atm_T0, -atm_G / (atm_L * atm_R));
    } else {
        double T_11k = atm_T0 + atm_L * 11000.0;
        double P_11k = atm_P0 * std::pow(T_11k / atm_T0, -atm_G / (atm_L * atm_R));
        T_atm = T_11k;
        P_atm = P_11k * std::exp(-atm_G * (alt_c - 11000.0) / (atm_R * T_atm));
    }

    // Virtual Temp (simplified, assuming RH=0 for pure C++ speed unless passed explicitly)
    double T_v = T_atm; // We will assume dry air in C++ for maximum speed, or user pre-calculates T0/P0 with virtual temp equivalent
    double rho_atm = P_atm / (atm_R * T_v);
    double speed_of_sound = std::sqrt(1.4 * atm_R * T_v);

    // Gravity
    double g_local = earth_G0 * std::pow(earth_R_EARTH / (earth_R_EARTH + alt_c), 2);

    // 3. Relative Air Velocity
    double v_air[3] = {vel[0] - wind_vx, vel[1] - wind_vy, vel[2] - wind_vz};
    double v_air_mag = norm3(v_air);

    double mach = v_air_mag / speed_of_sound;
    double q_dyn = 0.5 * rho_atm * v_air_mag * v_air_mag;

    // Normalize Quaternion
    double q_norm[4] = {q[0], q[1], q[2], q[3]};
    double nq = norm4(q_norm);
    if (nq > 1e-12) {
        q_norm[0] /= nq; q_norm[1] /= nq; q_norm[2] /= nq; q_norm[3] /= nq;
    }

    // Rotations
    double R_b2e[3][3];
    quat_to_rot_mat(q_norm, R_b2e);
    double R_e2b[3][3];
    transpose(R_b2e, R_e2b);

    double v_air_body[3];
    mat_vec_mult(R_e2b, v_air, v_air_body);

    double v_air_hat_earth[3] = {1,0,0};
    if (v_air_mag > 1e-6) {
        v_air_hat_earth[0] = v_air[0] / v_air_mag;
        v_air_hat_earth[1] = v_air[1] / v_air_mag;
        v_air_hat_earth[2] = v_air[2] / v_air_mag;
    }

    // 4. Linear Interpolation for Aerodynamics in C++
    auto machs = aero_mach_arr.unchecked<1>();
    auto cds = aero_cd_arr.unchecked<1>();
    auto cls = aero_cl_arr.unchecked<1>();
    auto cmas = aero_cma_arr.unchecked<1>();
    auto cmaqs = aero_cmaq_arr.unchecked<1>();
    auto cnlps = aero_cnlp_arr.unchecked<1>();
    auto cmags = aero_cmag_arr.unchecked<1>();

    int n_pts = machs.shape(0);
    double cd=cds(0), cl=cls(0), cma=cmas(0), cmaq=cmaqs(0), cnlp=cnlps(0), cmag=cmags(0);

    if (n_pts > 1) {
        // Find interval
        int idx = 0;
        if (mach <= machs(0)) {
            idx = 0;
        } else if (mach >= machs(n_pts-1)) {
            idx = n_pts - 2;
        } else {
            auto it = std::lower_bound(machs.data(0), machs.data(0) + n_pts, mach);
            idx = std::distance(machs.data(0), it) - 1;
            if (idx < 0) idx = 0;
        }

        double m0 = machs(idx);
        double m1 = machs(idx+1);
        double f = (m1 > m0) ? (mach - m0) / (m1 - m0) : 0.0;

        cd = cds(idx) + f * (cds(idx+1) - cds(idx));
        cl = cls(idx) + f * (cls(idx+1) - cls(idx));
        cma = cmas(idx) + f * (cmas(idx+1) - cmas(idx));
        cmaq = cmaqs(idx) + f * (cmaqs(idx+1) - cmaqs(idx));
        cnlp = cnlps(idx) + f * (cnlps(idx+1) - cnlps(idx));
        cmag = cmags(idx) + f * (cmags(idx+1) - cmags(idx));
    }

    // 5. Active Propulsion
    double m = proj_mass;
    double thrust = 0.0;
    if (prop_active && prop_burn_time_s > 0) {
        if (t <= prop_burn_time_s) {
            thrust = prop_thrust_n;
            m = proj_mass - prop_mass_kg * (t / prop_burn_time_s);
        } else {
            thrust = 0.0;
            m = proj_mass - prop_mass_kg;
        }
    }

    // 6. Aerodynamic Forces & Moments
    double S = proj_ref_area;
    double d = proj_diam;

    double alpha_approx = (v_air_mag > 1e-6) ? std::asin(std::max(-1.0, std::min(1.0, v_air_body[2] / v_air_mag))) : 0.0;
    double beta_approx = (v_air_mag > 1e-6) ? std::asin(std::max(-1.0, std::min(1.0, v_air_body[1] / v_air_mag))) : 0.0;

    double C_X = -cd;
    double C_Y = -cl * beta_approx;
    double C_Z = cl * alpha_approx;

    double pitch_damping = (v_air_mag > 1e-6) ? cmaq * (omega[1] * d / (2.0 * v_air_mag)) : 0.0;
    double yaw_damping = (v_air_mag > 1e-6) ? cmaq * (omega[2] * d / (2.0 * v_air_mag)) : 0.0;

    double C_m = cma * alpha_approx + pitch_damping;
    double C_n = -cma * beta_approx + yaw_damping;

    double p_hat = (v_air_mag > 1e-6) ? (omega[0] * d / (2.0 * v_air_mag)) : 0.0;
    double C_l = -0.01 * p_hat; // simple roll damping

    double C_m_mag = cmag * p_hat * beta_approx;
    double C_n_mag = -cmag * p_hat * alpha_approx;

    double M_aero_body[3] = {
        C_l * q_dyn * S * d,
        (C_m + C_m_mag) * q_dyn * S * d,
        (C_n + C_n_mag) * q_dyn * S * d
    };

    double C_Y_mag = cnlp * p_hat * alpha_approx;
    double C_Z_mag = -cnlp * p_hat * beta_approx;

    // Drag acts opposite to air velocity
    double F_drag_earth[3] = {
        C_X * q_dyn * S * v_air_hat_earth[0],
        C_X * q_dyn * S * v_air_hat_earth[1],
        C_X * q_dyn * S * v_air_hat_earth[2]
    };

    double F_aero_body_no_drag[3] = {0.0, (C_Y + C_Y_mag) * q_dyn * S, (C_Z + C_Z_mag) * q_dyn * S};
    double F_lift_earth[3];
    mat_vec_mult(R_b2e, F_aero_body_no_drag, F_lift_earth);

    double F_thrust_body[3] = {thrust, 0.0, 0.0};
    double F_thrust_earth[3];
    mat_vec_mult(R_b2e, F_thrust_body, F_thrust_earth);

    double F_gravity_earth[3] = {0.0, 0.0, -g_local * m};

    // Coriolis: a = -2 * (Omega x V)
    double omega_vec[3] = {0.0, earth_OMEGA * std::cos(latitude_rad), earth_OMEGA * std::sin(latitude_rad)};
    double a_coriolis[3];
    cross_product(omega_vec, vel, a_coriolis);
    double F_coriolis_earth[3] = {-2.0 * m * a_coriolis[0], -2.0 * m * a_coriolis[1], -2.0 * m * a_coriolis[2]};

    double accel[3] = {
        (F_drag_earth[0] + F_lift_earth[0] + F_thrust_earth[0] + F_gravity_earth[0] + F_coriolis_earth[0]) / m,
        (F_drag_earth[1] + F_lift_earth[1] + F_thrust_earth[1] + F_gravity_earth[1] + F_coriolis_earth[1]) / m,
        (F_drag_earth[2] + F_lift_earth[2] + F_thrust_earth[2] + F_gravity_earth[2] + F_coriolis_earth[2]) / m
    };

    // 7. Rigid Body Dynamics (Euler Equations)
    double Ix = proj_ix;
    double Iy = proj_iy;
    double p = omega[0], q_ang = omega[1], r = omega[2];

    double p_dot = M_aero_body[0] / Ix;
    double q_dot = (M_aero_body[1] - (Ix - Iy) * r * p) / Iy;
    double r_dot = (M_aero_body[2] - (Iy - Ix) * p * q_ang) / Iy;

    // Quaternion derivative
    double q_dot_vec[4] = {
        0.5 * (-q_norm[1]*p - q_norm[2]*q_ang - q_norm[3]*r),
        0.5 * ( q_norm[0]*p - q_norm[3]*q_ang + q_norm[2]*r),
        0.5 * ( q_norm[3]*p + q_norm[0]*q_ang - q_norm[1]*r),
        0.5 * (-q_norm[2]*p + q_norm[1]*q_ang + q_norm[0]*r)
    };

    // 8. Hypersonic Aerothermodynamics
    double dT_dt = 0.0;
    if (state_len > 13 && hyper_active) {
        double nr = std::max(nose_rad, 0.001);
        double q_conv = 1.83e-4 * std::sqrt(rho_atm / nr) * std::pow(v_air_mag, 3.0);
        double q_rad = mat_eps * 5.670374419e-8 * std::pow(T_nose, 4.0);

        double area = 2.0 * M_PI * nr * nr;
        double volume = (2.0 / 3.0) * M_PI * nr * nr * nr;
        double thermal_mass = volume * mat_density * mat_cp;

        dT_dt = ((q_conv - q_rad) * area) / thermal_mass;
    }

    // Build Output
    auto result = py::array_t<double>(state_len);
    auto res_buf = result.mutable_unchecked<1>();

    res_buf(0) = vel[0]; res_buf(1) = vel[1]; res_buf(2) = vel[2];
    res_buf(3) = accel[0]; res_buf(4) = accel[1]; res_buf(5) = accel[2];
    res_buf(6) = q_dot_vec[0]; res_buf(7) = q_dot_vec[1]; res_buf(8) = q_dot_vec[2]; res_buf(9) = q_dot_vec[3];
    res_buf(10) = p_dot; res_buf(11) = q_dot; res_buf(12) = r_dot;

    if (state_len > 13) {
        res_buf(13) = dT_dt;
    }

    return result;
}

PYBIND11_MODULE(wbs_core, m) {
    m.doc() = "Wilson Ballistic Suite C++ Physics Core";
    m.def("get_eom", &get_eom_cpp, "High-performance 6-DoF derivative calculator");
}
