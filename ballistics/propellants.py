"""
Thermodynamic properties of standard solid propellants used in interior ballistics.
Values are approximate generic representations of common single, double, and triple-base powders.

Keys:
- impetus (J/kg): The specific force constant (F) of the propellant gases.
- covolume (m^3/kg): The volume occupied by the gas molecules themselves (alpha).
- gamma (dimensionless): Ratio of specific heats (Cp/Cv).
- density (kg/m^3): Solid density of the unburned propellant grains (rho_p).
- burn_coeff (m/(s*Pa^n)): Burn rate coefficient (a).
- burn_exponent (dimensionless): Burn rate pressure exponent (n).
- flame_temp (K): Isochoric flame temperature (T_v).
"""

PROPELLANT_DATABASE = {
    "Generic Single-Base (NC)": {
        "impetus": 980000.0,
        "covolume": 0.001,
        "gamma": 1.25,
        "density": 1600.0,
        "burn_coeff": 1.2e-8,
        "burn_exponent": 0.9,
        "flame_temp": 2800.0
    },
    "Generic Double-Base (NC/NG)": {
        "impetus": 1050000.0,
        "covolume": 0.00105,
        "gamma": 1.22,
        "density": 1650.0,
        "burn_coeff": 1.5e-8,
        "burn_exponent": 0.85,
        "flame_temp": 3200.0
    },
    "Generic Triple-Base (Artillery)": {
        "impetus": 1100000.0,
        "covolume": 0.0011,
        "gamma": 1.23,
        "density": 1630.0,
        "burn_coeff": 1.8e-8,
        "burn_exponent": 0.8,
        "flame_temp": 3000.0
    },
    "Fast Rifle Powder (Extruded)": {
        "impetus": 1020000.0,
        "covolume": 0.00095,
        "gamma": 1.24,
        "density": 1580.0,
        "burn_coeff": 3.0e-8,
        "burn_exponent": 0.95,
        "flame_temp": 2900.0
    },
    "Slow Cannon Powder (M30)": {
        "impetus": 1080000.0,
        "covolume": 0.00108,
        "gamma": 1.23,
        "density": 1610.0,
        "burn_coeff": 0.8e-8,
        "burn_exponent": 0.82,
        "flame_temp": 2950.0
    }
}

class Propellant:
    def __init__(self, name):
        if name not in PROPELLANT_DATABASE:
            raise ValueError(f"Propellant '{name}' not found in database.")
        data = PROPELLANT_DATABASE[name]
        self.name = name
        self.impetus = data["impetus"]
        self.covolume = data["covolume"]
        self.gamma = data["gamma"]
        self.density = data["density"]
        self.burn_coeff = data["burn_coeff"]
        self.burn_exponent = data["burn_exponent"]
        self.flame_temp = data["flame_temp"]
