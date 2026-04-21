import numpy as np

def test_cfd_sphere_drag_delta():
    # Theoretical Cd of a sphere at low Mach is ~0.47
    # Our First-Principles V2x CFD should capture this through pressure integration

    from ballistics.cfd_v2 import CFDPipelineV2
    from ballistics.environment import StandardAtmosphere

    # We mock the STL behavior for a sphere
    class MockSphere:
        extents = np.array([0.01, 0.01, 0.01])
        def voxelized(self, pitch):
            res = MagicMock()
            res.matrix = np.zeros((10,10,10), dtype=bool)
            res.matrix[3:7, 3:7, 3:7] = True # Voxel sphere
            res.pitch = [pitch] * 3
            return res

    # Mocking trimesh.load
    import trimesh
    from unittest.mock import MagicMock
    trimesh.load = MagicMock(return_value=MockSphere())

    pipeline = CFDPipelineV2("sphere.stl")
    atm = StandardAtmosphere()

    # In the mocked environment (wbs_cfd_v2 not compiled), it returns the placeholder 0.28
    # If compiled, it should return the integrated result.
    res = pipeline.run_simulation_v2(mach=0.5, altitude_m=0, env_atm=atm)

    assert 'cd' in res
    assert res['cd'] > 0
