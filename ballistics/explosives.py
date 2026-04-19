"""
Thermodynamic properties of standard high explosives used in warheads.
Values are approximate generic representations for lethality calculations.

Keys:
- gurney_constant (m/s): The Gurney energy constant (sqrt(2E)), which dictates the velocity a specific explosive imparts to a metal casing.
- density (kg/m^3): Solid density of the explosive filler.
- tnt_equivalent (dimensionless): Relative effectiveness factor (RE factor) compared to TNT.
"""

EXPLOSIVES_DATABASE = {
    "TNT": {
        "gurney_constant": 2440.0,
        "density": 1654.0,
        "tnt_equivalent": 1.0
    },
    "Composition B": {
        "gurney_constant": 2700.0,
        "density": 1720.0,
        "tnt_equivalent": 1.33
    },
    "RDX": {
        "gurney_constant": 2930.0,
        "density": 1820.0,
        "tnt_equivalent": 1.60
    },
    "HMX": {
        "gurney_constant": 2970.0,
        "density": 1910.0,
        "tnt_equivalent": 1.70
    },
    "Octol": {
        "gurney_constant": 2890.0,
        "density": 1800.0,
        "tnt_equivalent": 1.54
    },
    "Torpex": {
        "gurney_constant": 2600.0, # High blast, lower brisance/gurney than pure RDX
        "density": 1810.0,
        "tnt_equivalent": 1.60
    }
}

class Explosive:
    def __init__(self, name):
        if name not in EXPLOSIVES_DATABASE:
            raise ValueError(f"Explosive '{name}' not found in database.")
        data = EXPLOSIVES_DATABASE[name]
        self.name = name
        self.gurney_constant = data["gurney_constant"]
        self.density = data["density"]
        self.tnt_equivalent = data["tnt_equivalent"]
