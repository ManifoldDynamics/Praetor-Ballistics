import numpy as np

def visualize_trajectory_3d(sol, projectile_stl_path=None):
    """
    Uses PyVista to render a fully interactive 3D scene of the trajectory.
    """
    try:
        import pyvista as pv
    except ImportError:
        print("PyVista is not installed. Cannot render 3D scene.")
        return

    # Extract coordinates
    x = sol.y[0, :]
    y = sol.y[1, :]
    z = sol.y[2, :]

    # Create an array of shape (N, 3) for the spline
    points = np.column_stack((x, y, z))

    # Create the PyVista plotter
    plotter = pv.Plotter(title="Wilson Ballistic Suite - 3D Trajectory Viewer")

    # Create a spline representing the flight path
    spline = pv.Spline(points, len(points))

    # Add the trajectory to the scene
    plotter.add_mesh(spline, color="red", line_width=4, label="Trajectory")

    # Add a ground plane
    max_range = np.max(x)
    max_deflection = np.max(np.abs(y))
    # Create a simple plane slightly below Z=0 so it doesn't clip the line perfectly
    plane = pv.Plane(
        center=(max_range/2, 0, -0.1),
        direction=(0, 0, 1),
        i_size=max_range * 1.2,
        j_size=max(max_deflection * 4.0, max_range * 0.2) # Ensure it has some width
    )
    plotter.add_mesh(plane, color="forestgreen", opacity=0.8, show_edges=False)

    # Add start and end markers
    start_sphere = pv.Sphere(radius=max_range * 0.01, center=points[0])
    plotter.add_mesh(start_sphere, color="yellow", label="Launch Point")

    end_sphere = pv.Sphere(radius=max_range * 0.01, center=points[-1])
    plotter.add_mesh(end_sphere, color="black", label="Impact")

    # Add axes indicator
    plotter.add_axes()

    # Show the grid
    plotter.show_bounds(grid='front', location='outer', all_edges=True)

    # Make it interactive
    plotter.show()
