import numpy as np
import pytest
from ballistics.cfd_pipeline import CFDPipeline
from ballistics.environment import StandardAtmosphere
import trimesh

def test_cfd_pipeline(tmp_path):
    # Create a small virtual cylinder to test the CFD solver
    # We use a very low resolution to ensure the test runs quickly
    mesh = trimesh.creation.cylinder(radius=0.05, height=0.3)
    transform = trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0])
    mesh.apply_transform(transform)

    stl_path = tmp_path / "test_cfd_bullet.stl"
    mesh.export(stl_path)

    # Run the pipeline
    pipeline = CFDPipeline(stl_path)
    atm = StandardAtmosphere()

    # Run at Mach 2.0 with a coarse grid of 10 voxels along the longest axis
    # The actual CFD grid will be padded to ~20x30x30
    res = pipeline.run_simulation(mach=2.0, altitude_m=0.0, env_atm=atm, grid_resolution=10)

    # Check outputs
    assert 'drag_force' in res
    assert 'lift_force' in res
    assert 'pressure_slice_z' in res

    # Because it's moving at Mach 2.0, it should generate positive pressure drag
    assert res['drag_force'] > 0.0

    # The pressure slice should have the correct 2D shape corresponding to the padded grid
    shape = res['pressure_slice_z'].shape
    assert shape[0] > 10 # Padded X
    assert shape[1] > 10 # Padded Y
