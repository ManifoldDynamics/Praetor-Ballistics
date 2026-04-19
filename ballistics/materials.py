"""
Thermodynamic and physical properties of standard engineering and aerospace materials.
Values are approximate generic representations for hypersonic aerothermodynamic calculations.

Keys:
- density (kg/m^3): Solid density of the material.
- specific_heat (J/(kg*K)): Specific heat capacity (Cp) at constant pressure.
- thermal_conductivity (W/(m*K)): Thermal conductivity (k).
- emissivity (dimensionless): Emissivity factor (epsilon) for radiative cooling (0.0 to 1.0).
- melting_point (K): Absolute melting temperature in Kelvin.
"""

MATERIALS_DATABASE = {
    "Steel (RHA)": {
        "density": 7850.0,
        "specific_heat": 460.0,
        "thermal_conductivity": 45.0,
        "emissivity": 0.8,
        "melting_point": 1780.0
    },
    "Aluminum (7075-T6)": {
        "density": 2810.0,
        "specific_heat": 960.0,
        "thermal_conductivity": 130.0,
        "emissivity": 0.1, # Polished
        "melting_point": 900.0
    },
    "Titanium (Ti-6Al-4V)": {
        "density": 4430.0,
        "specific_heat": 526.0,
        "thermal_conductivity": 6.7,
        "emissivity": 0.6,
        "melting_point": 1940.0
    },
    "Tungsten (WHA)": {
        "density": 17600.0,
        "specific_heat": 134.0,
        "thermal_conductivity": 173.0,
        "emissivity": 0.4,
        "melting_point": 3695.0 # Extremely high
    },
    "Depleted Uranium (DU)": {
        "density": 19100.0,
        "specific_heat": 116.0,
        "thermal_conductivity": 27.5,
        "emissivity": 0.5,
        "melting_point": 1405.0 # Surprisingly low compared to Tungsten
    },
    "Copper": {
        "density": 8960.0,
        "specific_heat": 385.0,
        "thermal_conductivity": 401.0,
        "emissivity": 0.05,
        "melting_point": 1358.0
    },
    "Lead": {
        "density": 11340.0,
        "specific_heat": 128.0,
        "thermal_conductivity": 35.0,
        "emissivity": 0.6,
        "melting_point": 600.0 # Melts very easily
    },
    "Inconel 718": {
        "density": 8190.0,
        "specific_heat": 435.0,
        "thermal_conductivity": 11.4,
        "emissivity": 0.85,
        "melting_point": 1600.0
    },
    "Carbon-Carbon Composite": {
        "density": 1850.0,
        "specific_heat": 710.0,
        "thermal_conductivity": 40.0,
        "emissivity": 0.9, # Excellent radiator
        "melting_point": 3800.0 # Sublimes
    }
}

class Material:
    def __init__(self, name):
        if name not in MATERIALS_DATABASE:
            raise ValueError(f"Material '{name}' not found in database.")
        data = MATERIALS_DATABASE[name]
        self.name = name
        self.density = data["density"]
        self.specific_heat = data["specific_heat"]
        self.thermal_conductivity = data["thermal_conductivity"]
        self.emissivity = data["emissivity"]
        self.melting_point = data["melting_point"]
