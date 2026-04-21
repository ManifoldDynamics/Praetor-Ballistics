import numpy as np
from ballistics.terrain_v2 import TerrainModelV2

def test_flat_terrain_elevation():
    terrain = TerrainModelV2()
    assert terrain.get_elevation(100.0, 200.0) == 0.0

def test_secondary_splash_generation():
    terrain = TerrainModelV2(ground_type='rock')
    impact_pos = np.array([0, 0, 0])
    impact_vel = np.array([0, 0, -500.0]) # Straight down
    impact_mass = 0.5

    splash = terrain.calculate_secondary_splash(impact_pos, impact_vel, impact_mass)

    assert len(splash) > 0
    for v_s, m_s in splash:
        assert v_s[2] > 0 # Secondary fragments must go UP
        assert m_s == 0.01

def test_splash_ground_type_absorption():
    t_soil = TerrainModelV2(ground_type='soil')
    t_rock = TerrainModelV2(ground_type='rock')

    pos = np.array([0,0,0])
    vel = np.array([0,0,-1000])
    m = 1.0

    s_soil = t_soil.calculate_secondary_splash(pos, vel, m)
    s_rock = t_rock.calculate_secondary_splash(pos, vel, m)

    # Rock should generate more/faster fragments than soil (less absorption)
    assert len(s_rock) >= len(s_soil)
