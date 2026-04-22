import numpy as np

def quaternion_to_rotation_matrix(q):
    """
    Convert a quaternion (q0, q1, q2, q3) where q0 is the scalar part,
    to a 3x3 rotation matrix. Transforms from body frame to Earth frame.
    """
    q0, q1, q2, q3 = q
    # Normalize to avoid numerical drift
    norm = np.linalg.norm(q)
    if norm > 1e-12:
        q0, q1, q2, q3 = q0/norm, q1/norm, q2/norm, q3/norm
    else:
        q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0

    R = np.array([
        [q0**2 + q1**2 - q2**2 - q3**2, 2*(q1*q2 - q0*q3),           2*(q1*q3 + q0*q2)],
        [2*(q1*q2 + q0*q3),           q0**2 - q1**2 + q2**2 - q3**2, 2*(q2*q3 - q0*q1)],
        [2*(q1*q3 - q0*q2),           2*(q2*q3 + q0*q1),           q0**2 - q1**2 - q2**2 + q3**2]
    ])
    return R

def rotation_matrix_to_quaternion(R):
    """Convert a rotation matrix to a quaternion (scalar first)"""
    tr = np.trace(R)
    if tr > 0:
        S = np.sqrt(tr + 1.0) * 2
        q0 = 0.25 * S
        q1 = (R[2,1] - R[1,2]) / S
        q2 = (R[0,2] - R[2,0]) / S
        q3 = (R[1,0] - R[0,1]) / S
    elif (R[0,0] > R[1,1]) and (R[0,0] > R[2,2]):
        S = np.sqrt(1.0 + R[0,0] - R[1,1] - R[2,2]) * 2
        q0 = (R[2,1] - R[1,2]) / S
        q1 = 0.25 * S
        q2 = (R[0,1] + R[1,0]) / S
        q3 = (R[0,2] + R[2,0]) / S
    elif R[1,1] > R[2,2]:
        S = np.sqrt(1.0 + R[1,1] - R[0,0] - R[2,2]) * 2
        q0 = (R[0,2] - R[2,0]) / S
        q1 = (R[0,1] + R[1,0]) / S
        q2 = 0.25 * S
        q3 = (R[1,2] + R[2,1]) / S
    else:
        S = np.sqrt(1.0 + R[2,2] - R[0,0] - R[1,1]) * 2
        q0 = (R[1,0] - R[0,1]) / S
        q1 = (R[0,2] + R[2,0]) / S
        q2 = (R[1,2] + R[2,1]) / S
        q3 = 0.25 * S

    q = np.array([q0, q1, q2, q3])
    norm = np.linalg.norm(q)
    if norm > 1e-12:
        return q / norm
    else:
        return np.array([1.0, 0.0, 0.0, 0.0])


def quaternion_to_euler(q):
    """
    Convert a quaternion (q0, q1, q2, q3) to Euler angles (yaw, pitch, roll) in radians.
    Assumes Z-Y-X rotation sequence.
    """
    q0, q1, q2, q3 = q
    # Normalize
    norm = np.linalg.norm(q)
    if norm > 1e-12:
        q0, q1, q2, q3 = q0/norm, q1/norm, q2/norm, q3/norm
    else:
        q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0

    # Roll (x-axis rotation)
    sinr_cosp = 2 * (q0 * q1 + q2 * q3)
    cosr_cosp = 1 - 2 * (q1 * q1 + q2 * q2)
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    # Pitch (y-axis rotation)
    sinp = np.clip(2 * (q0 * q2 - q3 * q1), -1.0, 1.0)
    pitch = np.arcsin(sinp)

    # Yaw (z-axis rotation)
    siny_cosp = 2 * (q0 * q3 + q1 * q2)
    cosy_cosp = 1 - 2 * (q2 * q2 + q3 * q3)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return yaw, pitch, roll

from ballistics.aerothermodynamics import HypersonicHeating
from ballistics.aerothermodynamics_v2 import AerothermodynamicsV2

def get_eom(t, state, projectile, aero, env_atmosphere, env_earth, env_wind=None, latitude_rad=0.0, propulsion=None, guidance=None, target_state=None, seeker=None, flexible_model=None):
    """
    Proprietary V2 6-DoF Equations of Motion.
    """
    pos = state[0:3]
    vel = state[3:6]
    q = state[6:10]
    omega = state[10:13]

    num_thermal_nodes = 5
    num_flexible_modes = 2

    if len(state) >= 13 + num_thermal_nodes:
        t_nodes = state[13:13+num_thermal_nodes]
        T_surface = t_nodes[0]
    elif len(state) > 13:
        T_surface = state[13]
        t_nodes = None
    else:
        T_surface = 300.0
        t_nodes = None

    altitude = pos[2]
    atm = env_atmosphere.get_properties(altitude)
    g = env_earth.gravity(altitude)

    if env_wind is not None:
        v_wind = env_wind.get_wind(altitude)
        v_air = vel - v_wind
    else:
        v_air = vel

    v_air_mag = np.linalg.norm(v_air)
    mach = v_air_mag / atm['speed_of_sound']
    q_dyn = 0.5 * atm['density'] * v_air_mag**2

    q_norm_val = np.linalg.norm(q)
    q_norm = q / q_norm_val if q_norm_val > 1e-12 else np.array([1, 0, 0, 0])

    if altitude < 0 and vel[2] < 0:
        return np.zeros(len(state))

    R_b2e = quaternion_to_rotation_matrix(q_norm)
    R_e2b = R_b2e.T
    v_air_body = R_e2b @ v_air

    S = projectile.reference_area
    d = projectile.diameter
    m = projectile.mass

    # V2.x Dynamic Mass and CoG
    if hasattr(propulsion, 'get_thrust_and_mdot'):
        thrust_n, _ = propulsion.get_thrust_and_mdot(t, atm['pressure'])
        m, _ = propulsion.get_current_mass_and_cog(t, projectile.mass, 0.0)
    else:
        thrust_n = 0.0

    alpha_approx = np.arcsin(np.clip(v_air_body[2] / v_air_mag, -1, 1)) if v_air_mag > 0 else 0
    beta_approx = np.arcsin(np.clip(v_air_body[1] / v_air_mag, -1, 1)) if v_air_mag > 0 else 0

    # Indicial Lag Coordination
    if len(state) > 18:
        lambda_alpha = state[18]
        tau_unsteady = (3.0 * d / v_air_mag) if v_air_mag > 10.0 else 0.01
        d_lambda = (alpha_approx - lambda_alpha) / tau_unsteady
    else:
        lambda_alpha = alpha_approx
        d_lambda = 0.0

    # Forces
    F_drag_earth = -aero.cd(mach) * q_dyn * S * (v_air / v_air_mag if v_air_mag > 0 else np.array([1, 0, 0]))

    # Non-linear Lift (V2 Proprietary)
    from ballistics.aero_v2 import AeroPredictorV2
    cn = AeroPredictorV2.calculate_high_alpha_lift(lambda_alpha, aero.cl(mach), mach, projectile)
    F_lift_body = np.array([0, 0, cn * q_dyn * S])
    F_lift_earth = R_b2e @ F_lift_body

    F_thrust_earth = R_b2e @ np.array([thrust_n, 0, 0])
    F_gravity_earth = np.array([0, 0, -g * m])

    F_total = F_drag_earth + F_lift_earth + F_thrust_earth + F_gravity_earth
    accel = F_total / m

    # Moments
    pitch_damping = aero.cmaq(mach) * (omega[1] * d / (2 * v_air_mag)) if v_air_mag > 0 else 0
    C_m = aero.cma(mach) * lambda_alpha + pitch_damping

    M_body = np.array([0, C_m, 0]) * q_dyn * S * d
    omega_dot = M_body / projectile.i_y # Simplified

    q_dot_mat = 0.5 * np.array([
        [-q_norm[1], -q_norm[2], -q_norm[3]],
        [ q_norm[0], -q_norm[3],  q_norm[2]],
        [ q_norm[3],  q_norm[0], -q_norm[1]],
        [-q_norm[2],  q_norm[1],  q_norm[0]]
    ])
    q_dot = q_dot_mat @ omega

    # Thermal & Flexible
    state_dot = np.zeros(len(state))
    state_dot[0:3] = vel
    state_dot[3:6] = accel
    state_dot[6:10] = q_dot
    state_dot[10:13] = omega_dot
    if len(state) > 18: state_dot[18] = d_lambda

    return state_dot

def get_multibody_eom(t, full_state, bodies, aero, env_atmosphere, env_earth, env_wind=None, latitude_rad=0.0):
    """
    Computes derivatives for N dynamic bodies simultaneously.
    """
    n_bodies = len(bodies)
    state_size = 13
    state_dot = np.zeros(len(full_state))
    for i in range(n_bodies):
        idx = i * state_size
        state_dot[idx : idx + state_size] = get_eom(t, full_state[idx : idx + state_size], bodies[i], aero[i], env_atmosphere, env_earth, env_wind, latitude_rad)
    return state_dot
