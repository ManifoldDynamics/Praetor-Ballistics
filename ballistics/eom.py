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

def get_eom(t, state, projectile, aero, env_atmosphere, env_earth, env_wind=None, latitude_rad=0.0, propulsion=None, guidance=None, target_state=None, seeker=None):
    """
    propulsion: None, or a dict containing:
      - 'thrust_n': Thrust in Newtons
      - 'burn_time_s': Duration of motor burn
      - 'propellant_mass_kg': Mass expelled during burn
    guidance: An instance of ProportionalNavigation, or None
    target_state: dict {'pos': [x,y,z], 'vel': [vx,vy,vz]} representing the target at t=0
    """
    pos = state[0:3]
    vel = state[3:6] # Inertial velocity
    q = state[6:10]
    omega = state[10:13] # [p, q, r]

    # V2: Track multiple temperatures if state vector is large enough
    num_thermal_nodes = 5
    if len(state) >= 13 + num_thermal_nodes:
        t_nodes = state[13:13+num_thermal_nodes]
        T_surface = t_nodes[0]
    elif len(state) > 13:
        T_surface = state[13]
        t_nodes = None
    else:
        T_surface = 300.0
        t_nodes = None

    # Calculate environment variables
    altitude = pos[2]
    atm = env_atmosphere.get_properties(altitude)
    g = env_earth.gravity(altitude)

    # Air relative velocity vector
    if env_wind is not None:
        v_wind = env_wind.get_wind(altitude)
        v_air = vel - v_wind
    else:
        v_air = vel

    v_air_mag = np.linalg.norm(v_air)

    mach = v_air_mag / atm['speed_of_sound']
    q_dyn = 0.5 * atm['density'] * v_air_mag**2 # Dynamic pressure using air-relative velocity

    # Normalizing quaternion to prevent drift
    q_norm_val = np.linalg.norm(q)
    if q_norm_val > 1e-12:
        q_norm = q / q_norm_val
    else:
        q_norm = np.array([1.0, 0.0, 0.0, 0.0])

    # Stop simulation if we hit the ground
    if altitude < 0 and vel[2] < 0:
        return np.zeros(13)

    # Rotation matrix Body -> Earth
    R_b2e = quaternion_to_rotation_matrix(q_norm)
    # Earth -> Body
    R_e2b = R_b2e.T

    # Air velocity in body frame
    # A wind blowing in +Y direction makes v_air have a negative Y component (since v_air = v - v_wind)
    # This means v_air_body[1] is negative.
    v_air_body = R_e2b @ v_air

    if v_air_mag > 0:
        v_air_hat_earth = v_air / v_air_mag
        v_air_hat_body = v_air_body / v_air_mag
    else:
        v_air_hat_earth = np.array([1.0, 0.0, 0.0])
        v_air_hat_body = np.array([1.0, 0.0, 0.0])

    S = projectile.reference_area
    d = projectile.diameter

    # Active Propulsion / Time-Varying Mass
    m = projectile.mass
    thrust_n = 0.0

    # Support V2 Proprietary Rocket Motor
    if hasattr(propulsion, 'get_thrust_and_mdot'):
        thrust_n, _ = propulsion.get_thrust_and_mdot(t, atm['pressure'])
        m = propulsion.get_current_mass(t, projectile.mass)
    elif propulsion is not None and propulsion.get('active', False):
        # Fallback to V1
        burn_t = propulsion.get('burn_time_s', 0.0)
        p_mass = propulsion.get('propellant_mass_kg', 0.0)
        max_t = propulsion.get('thrust_n', 0.0)

        if t <= burn_t and burn_t > 0:
            thrust_n = max_t
            m = projectile.mass - p_mass * (t / burn_t)
        else:
            thrust_n = 0.0
            m = projectile.mass - p_mass

    # Base drag reduction / rocket flame effect logic could be added here
    # (e.g., Cd reduces while motor is burning due to base bleed effect)

    # Drag is primarily axial
    C_X = -aero.cd(mach)

    # Normal force coefficients (Linear approx: C_N = C_N_alpha * alpha)
    # Lift acts perpendicular to the body axis relative to the air velocity vector
    # A positive v_air_body[2] means the wind hits the bottom of the projectile, meaning positive alpha
    # A positive v_air_body[1] means wind hits the right side, meaning negative beta in standard conventions
    alpha_approx = np.arcsin(np.clip(v_air_body[2] / v_air_mag, -1, 1)) if v_air_mag > 0 else 0
    beta_approx = np.arcsin(np.clip(v_air_body[1] / v_air_mag, -1, 1)) if v_air_mag > 0 else 0

    # Lift creates a force in the direction of the angle of attack/sideslip
    # If v_air_body[1] is negative (wind blowing from left to right, +Y direction),
    # the side force should push the projectile to the right (+Y).
    # Thus C_Y should be positive.
    C_Y = -aero.cl(mach) * beta_approx
    C_Z = aero.cl(mach) * alpha_approx

    # Moments in body frame (using air magnitude for normalization)
    pitch_damping = aero.cmaq(mach) * (omega[1] * d / (2 * v_air_mag)) if v_air_mag > 0 else 0
    yaw_damping = aero.cmaq(mach) * (omega[2] * d / (2 * v_air_mag)) if v_air_mag > 0 else 0

    C_m = aero.cma(mach) * alpha_approx + pitch_damping
    C_n = -aero.cma(mach) * beta_approx + yaw_damping # Assuming symmetry

    C_l = -0.01 * (omega[0] * d / (2 * v_air_mag)) if v_air_mag > 0 else 0

    p_hat = (omega[0] * d / (2 * v_air_mag)) if v_air_mag > 0 else 0
    C_m_mag = aero.cmag(mach) * p_hat * beta_approx
    C_n_mag = -aero.cmag(mach) * p_hat * alpha_approx

    M_aero_body = np.array([C_l, C_m + C_m_mag, C_n + C_n_mag]) * q_dyn * S * d

    # Active Guidance Control
    F_guide_earth = np.zeros(3)

    if guidance is not None and target_state is not None:
        t_pos_truth = np.array(target_state['pos']) + np.array(target_state['vel']) * t
        t_vel_truth = np.array(target_state['vel'])

        if seeker is not None:
            # Sensed state includes latency and noise
            # We calculate truth at t - latency for the sensed signal
            t_delayed = max(0.0, t - seeker.latency)
            t_pos_delayed = np.array(target_state['pos']) + np.array(target_state['vel']) * t_delayed
            t_vel_delayed = np.array(target_state['vel'])

            # Simple IR SNR logic
            t_temp = target_state.get('temperature_k', 300.0)
            t_area = target_state.get('area_m2', 1.0)
            from ballistics.sensors_v2 import IRSignatureModelV2
            intensity = IRSignatureModelV2.calculate_radiant_intensity(t_temp, t_area)
            snr = IRSignatureModelV2.calculate_snr(intensity, np.linalg.norm(t_pos_truth - pos))

            t_pos, t_vel = seeker.get_sensed_target(t, t_pos_delayed, t_vel_delayed, pos, snr)
        else:
            t_pos, t_vel = t_pos_truth, t_vel_truth

        # Support V2 Guidance Laws
        if t_pos is not None and hasattr(guidance, 'augmented_pronav'):
            t_accel = target_state.get('accel', np.zeros(3))
            a_cmd_earth = guidance.augmented_pronav(t, pos, vel, t_pos, t_vel, t_accel, seeker=seeker)
        elif t_pos is not None:
            # Fallback to V1
            a_cmd_earth = guidance.get_commanded_acceleration(t, pos, vel, t_pos, t_vel)

        F_guide_earth = m * a_cmd_earth

    # Magnus Force (Spin drift)
    # acts mutually perpendicular to velocity vector and spin axis.
    # C_Y_mag = cnlp * (pd/2V) * alpha
    # C_Z_mag = -cnlp * (pd/2V) * beta
    C_Y_mag = aero.cnlp(mach) * p_hat * alpha_approx
    C_Z_mag = -aero.cnlp(mach) * p_hat * beta_approx

    # Add magnus force to the aerodynamic force
    F_aero_body = np.array([C_X, C_Y + C_Y_mag, C_Z + C_Z_mag]) * q_dyn * S
    F_aero_earth = R_b2e @ F_aero_body

    # Wind Drag correction: The drag acts along the negative air-relative velocity vector
    # Our C_X primarily acts along the body axis. But there is also a drag component
    # directly opposing v_air that pushes the projectile laterally in a crosswind.
    # To model this properly in 6-DoF, the total aerodynamic force should be oriented
    # with the air relative velocity vector for the pure drag component.
    # For a rigid body, the axial force C_X already opposes forward motion, but it's along the body axis.
    # The crosswind drag is effectively standard drag opposing the lateral air velocity.
    # We will compute the force vector directly opposing v_air for the drag, and use C_Y/C_Z for lift.

    # Let's override the simple body-axial drag with the true air-relative drag vector
    # The aerodynamic force from Lift, Magnus, etc acts mostly relative to body, but
    # principal Drag acts opposite to air velocity vector.
    F_drag_earth = -aero.cd(mach) * q_dyn * S * v_air_hat_earth

    # We remove C_X from F_aero_body to avoid double counting drag
    F_aero_body_no_drag = np.array([0.0, C_Y + C_Y_mag, C_Z + C_Z_mag]) * q_dyn * S
    F_lift_earth = R_b2e @ F_aero_body_no_drag

    # Active Thrust vector (assumes thrust acts strictly along the body's forward X-axis)
    F_thrust_body = np.array([thrust_n, 0.0, 0.0])
    F_thrust_earth = R_b2e @ F_thrust_body

    F_gravity_earth = np.array([0, 0, -g * m])
    F_coriolis_earth = m * env_earth.coriolis_acceleration(vel, latitude_rad)

    F_total_earth = F_drag_earth + F_lift_earth + F_thrust_earth + F_guide_earth + F_gravity_earth + F_coriolis_earth

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

    # Aerothermodynamics
    thermal_derivatives = []
    if len(state) > 13 and hasattr(projectile, 'material') and hasattr(projectile, 'nose_radius_m'):
        q_conv = HypersonicHeating.fay_riddell_heat_flux(atm['density'], v_air_mag, projectile.nose_radius_m)
        q_rad = HypersonicHeating.radiative_cooling_flux(T_surface, projectile.material.emissivity)

        if t_nodes is not None:
            # Use V2 Finite Difference model
            thermal_derivatives = AerothermodynamicsV2.calculate_derivatives(
                t, t_nodes, q_conv, q_rad, projectile.nose_radius_m,
                projectile.skin_thickness_m, projectile.material, num_nodes=num_thermal_nodes
            )
        else:
            # Fallback to V1 Lumped Mass model
            dT_dt = HypersonicHeating.calculate_nose_temperature_derivative(q_conv, q_rad, projectile.nose_radius_m, projectile.material)
            thermal_derivatives = [dT_dt]
    else:
        if len(state) > 13:
            thermal_derivatives = [0.0] * (len(state) - 13)

    state_dot = np.zeros(len(state))
    state_dot[0:3] = vel
    state_dot[3:6] = accel
    state_dot[6:10] = q_dot_vec
    state_dot[10:13] = omega_dot

    if len(thermal_derivatives) > 0:
        state_dot[13:13+len(thermal_derivatives)] = thermal_derivatives

    return state_dot

def get_multibody_eom(t, full_state, bodies, aero, env_atmosphere, env_earth, env_wind=None, latitude_rad=0.0):
    """
    Computes derivatives for N dynamic bodies simultaneously, accounting for interference.
    full_state: [body1_state, body2_state, ...] each 13+ elements.
    bodies: list of Projectile objects.
    """
    n_bodies = len(bodies)
    # Assume 13 states per body for simplicity in multibody
    state_size = 13
    state_dot = np.zeros(len(full_state))

    from ballistics.separation_v2 import MultiBodyManagerV2

    for i in range(n_bodies):
        idx = i * state_size
        y_i = full_state[idx : idx + state_size]

        # Calculate base derivatives
        dot_i = get_eom(t, y_i, bodies[i], aero[i], env_atmosphere, env_earth, env_wind, latitude_rad)

        # Add interference from other bodies
        for j in range(n_bodies):
            if i == j: continue
            idx_j = j * state_size
            y_j = full_state[idx_j : idx_j + state_size]

            dist_vec = y_j[0:3] - y_i[0:3]
            v_rel = y_j[3:6] - y_i[3:6]

            # Simple Interference Force integration
            int_factor = MultiBodyManagerV2.calculate_interference_drag(dist_vec, v_rel, 0)
            # Apply interference to acceleration (state indices 3:6)
            # This is a highly simplified coupling for the V2 MVP
            dot_i[3:6] *= int_factor

        state_dot[idx : idx + state_size] = dot_i

    return state_dot