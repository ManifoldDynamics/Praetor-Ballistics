import numpy as np

def quaternion_to_rotation_matrix(q):
    """
    Convert a quaternion (q0, q1, q2, q3) where q0 is the scalar part,
    to a 3x3 rotation matrix. Transforms from body frame to Earth frame.
    """
    q0, q1, q2, q3 = q
    # Normalize to avoid numerical drift
    norm = np.linalg.norm(q)
    q0, q1, q2, q3 = q0/norm, q1/norm, q2/norm, q3/norm

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
    return q / np.linalg.norm(q)


def quaternion_to_euler(q):
    """
    Convert a quaternion (q0, q1, q2, q3) to Euler angles (yaw, pitch, roll) in radians.
    Assumes Z-Y-X rotation sequence.
    """
    q0, q1, q2, q3 = q
    # Normalize
    norm = np.linalg.norm(q)
    q0, q1, q2, q3 = q0/norm, q1/norm, q2/norm, q3/norm

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

def get_eom(t, state, projectile, aero, env_atmosphere, env_earth, latitude_rad=0.0):
    pos = state[0:3]
    vel = state[3:6]
    q = state[6:10]
    omega = state[10:13] # [p, q, r]

    v_mag = np.linalg.norm(vel)

    # Normalizing quaternion to prevent drift
    q_norm = q / np.linalg.norm(q)

    # Calculate environment
    altitude = pos[2]
    atm = env_atmosphere.get_properties(altitude)
    g = env_earth.gravity(altitude)

    mach = v_mag / atm['speed_of_sound']
    q_dyn = 0.5 * atm['density'] * v_mag**2 # Dynamic pressure

    # Stop simulation if we hit the ground
    if altitude < 0 and vel[2] < 0:
        return np.zeros(13)

    # Rotation matrix Body -> Earth
    R_b2e = quaternion_to_rotation_matrix(q_norm)
    # Earth -> Body
    R_e2b = R_b2e.T

    # Velocity in body frame
    v_body = R_e2b @ vel

    # Wind logic could go here. For now, v_air = vel.
    v_air = vel
    v_air_body = R_e2b @ v_air

    if v_mag > 0:
        v_air_hat = v_air_body / v_mag
    else:
        v_air_hat = np.array([1.0, 0.0, 0.0])

    S = projectile.reference_area
    d = projectile.diameter
    m = projectile.mass

    # Drag is primarily axial
    C_X = -aero.cd(mach)

    # Normal force coefficients (Linear approx: C_N = C_N_alpha * alpha)
    # Lift acts perpendicular to the body axis.
    # sin(alpha) approx = v_air_body[2] / v_mag
    alpha_approx = np.arcsin(np.clip(v_air_body[2] / v_mag, -1, 1)) if v_mag > 0 else 0
    beta_approx = np.arcsin(np.clip(v_air_body[1] / v_mag, -1, 1)) if v_mag > 0 else 0

    C_Y = -aero.cl(mach) * beta_approx
    C_Z = aero.cl(mach) * alpha_approx

    # Moments in body frame
    pitch_damping = aero.cmaq(mach) * (omega[1] * d / (2 * v_mag)) if v_mag > 0 else 0
    yaw_damping = aero.cmaq(mach) * (omega[2] * d / (2 * v_mag)) if v_mag > 0 else 0

    C_m = aero.cma(mach) * alpha_approx + pitch_damping
    C_n = -aero.cma(mach) * beta_approx + yaw_damping # Assuming symmetry

    C_l = -0.01 * (omega[0] * d / (2 * v_mag)) if v_mag > 0 else 0

    p_hat = (omega[0] * d / (2 * v_mag)) if v_mag > 0 else 0
    C_m_mag = aero.cmag(mach) * p_hat * beta_approx
    C_n_mag = -aero.cmag(mach) * p_hat * alpha_approx

    M_aero_body = np.array([C_l, C_m + C_m_mag, C_n + C_n_mag]) * q_dyn * S * d

    # Magnus Force (Spin drift)
    # acts mutually perpendicular to velocity vector and spin axis.
    # C_Y_mag = cnlp * (pd/2V) * alpha
    # C_Z_mag = -cnlp * (pd/2V) * beta
    C_Y_mag = aero.cnlp(mach) * p_hat * alpha_approx
    C_Z_mag = -aero.cnlp(mach) * p_hat * beta_approx

    # Add magnus force to the aerodynamic force
    F_aero_body = np.array([C_X, C_Y + C_Y_mag, C_Z + C_Z_mag]) * q_dyn * S
    F_aero_earth = R_b2e @ F_aero_body

    F_gravity_earth = np.array([0, 0, -g * m])
    F_coriolis_earth = m * env_earth.coriolis_acceleration(vel, latitude_rad)

    F_total_earth = F_aero_earth + F_gravity_earth + F_coriolis_earth

    accel = F_total_earth / m

    Ix = projectile.i_x
    Iy = projectile.i_y

    p, q_ang, r = omega

    p_dot = M_aero_body[0] / Ix
    q_dot = (M_aero_body[1] - (Ix - Iy) * r * p) / Iy
    r_dot = (M_aero_body[2] - (Iy - Ix) * p * q_ang) / Iy
    omega_dot = np.array([p_dot, q_dot, r_dot])

    q0, q1, q2, q3 = q_norm
    q_dot_mat = 0.5 * np.array([
        [-q1, -q2, -q3],
        [ q0, -q3,  q2],
        [ q3,  q0, -q1],
        [-q2,  q1,  q0]
    ])
    q_dot_vec = q_dot_mat @ omega

    state_dot = np.zeros(13)
    state_dot[0:3] = vel
    state_dot[3:6] = accel
    state_dot[6:10] = q_dot_vec
    state_dot[10:13] = omega_dot

    return state_dot