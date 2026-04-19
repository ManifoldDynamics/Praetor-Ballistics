import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ballistics.eom import quaternion_to_euler

def export_trajectory_csv(sol, filepath):
    """
    Exports the integration results to a CSV file.
    Translates quaternion states to Euler angles for readability.
    """
    with open(filepath, mode='w', newline='') as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow([
            "Time (s)",
            "X (m)", "Y (m)", "Z (m)",
            "Vx (m/s)", "Vy (m/s)", "Vz (m/s)",
            "Yaw (deg)", "Pitch (deg)", "Roll (deg)",
            "p (rad/s)", "q (rad/s)", "r (rad/s)"
        ])

        # Write data rows
        # sol.t is 1D array of times
        # sol.y is 2D array: rows are states, columns are time steps
        num_steps = len(sol.t)
        for i in range(num_steps):
            t = sol.t[i]
            x, y, z = sol.y[0:3, i]
            vx, vy, vz = sol.y[3:6, i]
            q = sol.y[6:10, i]
            p, q_ang, r = sol.y[10:13, i]

            # Convert quaternion to euler angles (degrees)
            yaw_rad, pitch_rad, roll_rad = quaternion_to_euler(q)
            yaw_deg = np.rad2deg(yaw_rad)
            pitch_deg = np.rad2deg(pitch_rad)
            roll_deg = np.rad2deg(roll_rad)

            writer.writerow([
                t,
                x, y, z,
                vx, vy, vz,
                yaw_deg, pitch_deg, roll_deg,
                p, q_ang, r
            ])


def plot_trajectory(sol):
    """
    Generates a 3D and 2D plot of the projectile's trajectory.
    """
    t = sol.t
    x = sol.y[0, :]
    y = sol.y[1, :]
    z = sol.y[2, :]

    # Create a figure with a 3D plot and two 2D projections
    fig = plt.figure(figsize=(15, 5))

    # 1. 3D Trajectory Plot
    ax1 = fig.add_subplot(1, 3, 1, projection='3d')
    ax1.plot(x, y, z, label='Trajectory', color='b')
    ax1.set_xlabel('Range X (m)')
    ax1.set_ylabel('Deflection Y (m)')
    ax1.set_zlabel('Altitude Z (m)')
    ax1.set_title('3D Trajectory')
    ax1.legend()

    # 2. Side Profile (Altitude vs Range)
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.plot(x, z, label='Trajectory', color='r')
    ax2.set_xlabel('Range X (m)')
    ax2.set_ylabel('Altitude Z (m)')
    ax2.set_title('Side Profile (Altitude vs Range)')
    ax2.grid(True)

    # 3. Top-Down View (Deflection vs Range)
    # Often deflection is very small compared to range, so scaling helps.
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.plot(x, y, label='Deflection (Spin Drift / Coriolis)', color='g')
    ax3.set_xlabel('Range X (m)')
    ax3.set_ylabel('Deflection Y (m)')
    ax3.set_title('Top-Down Profile (Deflection)')
    ax3.grid(True)

    plt.tight_layout()
    plt.show()
