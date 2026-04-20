import numpy as np
from unittest.mock import MagicMock
import sys

def test_cfd_v2_wrapper():
    # Mock trimesh and atmosphere
    mock_mesh = MagicMock()
    mock_mesh.extents.max.return_value = 0.5
    mock_voxel = MagicMock()
    mock_voxel.matrix = np.zeros((10, 10, 10), dtype=bool)
    mock_voxel.pitch = [0.01]
    mock_mesh.voxelized.return_value = mock_voxel

    with MagicMock() as mock_trimesh:
        mock_trimesh.load.return_value = mock_mesh
        sys.modules['trimesh'] = mock_trimesh

        from ballistics.cfd_v2 import CFDPipelineV2
        from ballistics.environment import StandardAtmosphere

        atm = StandardAtmosphere()
        pipeline = CFDPipelineV2("dummy.stl")

        # Test simulation run (with mocked wbs_cfd_v2 via the wrapper's fallback)
        res = pipeline.run_simulation_v2(mach=2.0, altitude_m=0, env_atm=atm)

        assert 'cd' in res
        assert res['cd'] > 0
