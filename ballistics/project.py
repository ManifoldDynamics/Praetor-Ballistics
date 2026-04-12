import json
import os

class BallisticsProject:
    """
    Manages serialization and deserialization of a ballistics project state.
    """
    def __init__(self):
        # Default state
        self.state = {
            "projectile": {
                "mass_kg": 43.0,
                "diameter_m": 0.155,
                "muzzle_velocity_ms": 800.0,
                "spin_rate_rads": 1884.95,
                "aero_model": "G7 Standard",
                "custom_stl_path": "",
                "custom_csv_path": ""
            },
            "environment": {
                "wind_speed_ms": 0.0,
                "wind_direction_deg": 90.0,
                "latitude": 39.7392,
                "longitude": -104.9903,
                "use_live_weather": False
            },
            "target": {
                "x_m": 2500.0,
                "y_m": 0.0,
                "z_m": 0.0
            },
            "dispersion": {
                "shots": 50,
                "plane": "vertical", # 'vertical' or 'horizontal'
                "v0_sd_ms": 2.0,
                "mass_sd_kg": 0.01,
                "wind_speed_sd_ms": 1.0,
                "pitch_sd_deg": 0.05,
                "yaw_sd_deg": 0.05
            },
            "propulsion": {
                "active": False,
                "thrust_n": 1000.0,
                "burn_time_s": 2.0,
                "propellant_mass_kg": 2.0
            },
            "lethality": {
                "active": False,
                "explosive": "Composition B",
                "explosive_mass_kg": 5.0,
                "target_stl": "",
                "target_armor_mm": 10.0,
                "fragments": 500
            }
        }
        self.filepath = None

    def load(self, filepath):
        """Loads project state from a JSON (.blst) file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Project file not found: {filepath}")

        with open(filepath, 'r') as f:
            data = json.load(f)

        # Basic validation
        if "projectile" in data and "environment" in data and "target" in data:
            self.state = data
            self.filepath = filepath
        else:
            raise ValueError("Invalid project file format.")

    def save(self, filepath=None):
        """Saves project state to a JSON (.blst) file."""
        if filepath:
            self.filepath = filepath

        if not self.filepath:
            raise ValueError("No filepath specified for saving.")

        with open(self.filepath, 'w') as f:
            json.dump(self.state, f, indent=4)
