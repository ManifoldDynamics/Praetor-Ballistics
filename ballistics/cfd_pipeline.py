import numpy as np
import trimesh

class CFDPipeline:
    """
    Manages the 3D Voxel CFD pipeline.
    Loads an STL, voxelizes it, and sends the boolean grid to the C++ Euler solver.
    """
    def __init__(self, stl_filepath, pitch_deg=0.0):
        self.stl_filepath = stl_filepath
        self.pitch_deg = pitch_deg
        self.mesh = trimesh.load(stl_filepath)

        # Ensure mesh is aligned. For our solver, X is the longitudinal flow direction.
        # If the mesh is not aligned to X, we assume the user provides a well-aligned mesh for now.

    def run_simulation(self, mach, altitude_m, env_atm, grid_resolution=50):
        """
        Voxelizes the mesh and executes the C++ CFD core.
        grid_resolution: Number of voxels along the longest axis.
        """
        # Get atmospheric properties
        props = env_atm.get_properties(altitude_m)
        p_inf = props['pressure']
        rho_inf = props['density']

        print(f"CFD: Voxelizing mesh to resolution {grid_resolution}...")
        # Voxelize the mesh. This creates a 3D boolean grid where True is solid.
        # To leave room for the fluid to flow around the projectile, we need to embed
        # this voxel grid into a larger "wind tunnel" bounding box.

        # First, voxelize the raw mesh
        pitch_rad = np.deg2rad(self.pitch_deg)

        # Apply pitch to the mesh before voxelizing if we want an AoA simulation
        if pitch_rad != 0.0:
            rot_mat = trimesh.transformations.rotation_matrix(pitch_rad, [0, 1, 0])
            self.mesh.apply_transform(rot_mat)

        voxel_obj = self.mesh.voxelized(pitch=self.mesh.extents.max() / grid_resolution)
        raw_matrix = voxel_obj.matrix # Boolean array

        # Create a larger fluid domain (e.g., 2x the size of the bounding box)
        pad_x = raw_matrix.shape[0] // 2
        pad_y = raw_matrix.shape[1] * 2
        pad_z = raw_matrix.shape[2] * 2

        # Avoid zero padding issues
        pad_x = max(pad_x, 5)
        pad_y = max(pad_y, 5)
        pad_z = max(pad_z, 5)

        tunnel_matrix = np.zeros(
            (raw_matrix.shape[0] + pad_x*2,
             raw_matrix.shape[1] + pad_y*2,
             raw_matrix.shape[2] + pad_z*2),
            dtype=bool
        )

        # Insert the solid into the center of the tunnel
        tunnel_matrix[
            pad_x : pad_x + raw_matrix.shape[0],
            pad_y : pad_y + raw_matrix.shape[1],
            pad_z : pad_z + raw_matrix.shape[2]
        ] = raw_matrix

        # Ensure dx, dy, dz are standard python floats, not numpy arrays
        dx = float(np.mean(voxel_obj.pitch))
        dy = float(np.mean(voxel_obj.pitch))
        dz = float(np.mean(voxel_obj.pitch))

        try:
            import wbs_cfd_3d
        except ImportError:
            raise ImportError("wbs_cfd_3d C++ extension not found. Did you compile it?")

        print(f"CFD: Handing off {tunnel_matrix.shape} grid to C++ Engine...")

        # Calculate iterations based on grid size to ensure wave propagation
        iterations = int(max(tunnel_matrix.shape) * 3)

        # The CFD solver assumes flow is coming from -X.
        # If we already rotated the mesh, we set alpha=0 for the solver freestream.
        res = wbs_cfd_3d.solve_cfd_3d(
            tunnel_matrix,
            dx, dy, dz,
            float(mach), float(p_inf), float(rho_inf),
            iterations, 0.0
        )

        # Add metadata for visualization
        res['dx'] = dx
        res['dy'] = dy
        res['dz'] = dz
        res['pad_x'] = pad_x
        res['pad_y'] = pad_y
        res['pad_z'] = pad_z
        res['mesh'] = self.mesh

        print("CFD: Simulation Complete.")
        return res
