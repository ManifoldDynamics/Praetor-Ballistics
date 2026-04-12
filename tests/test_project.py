import json
from ballistics.project import BallisticsProject

def test_project_save_load(tmp_path):
    proj = BallisticsProject()

    # Modify default state
    proj.state["projectile"]["mass_kg"] = 12.0
    proj.state["target"]["x_m"] = 5000.0

    # Save it
    filepath = tmp_path / "test_proj.blst"
    proj.save(filepath)

    assert filepath.exists()

    # Load it into a new instance
    proj_loaded = BallisticsProject()
    proj_loaded.load(filepath)

    assert proj_loaded.state["projectile"]["mass_kg"] == 12.0
    assert proj_loaded.state["target"]["x_m"] == 5000.0
    assert proj_loaded.filepath == filepath
