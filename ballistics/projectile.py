import numpy as np
from scipy.interpolate import interp1d

class Projectile:
    """
    Physical properties of the projectile.
    """
    def __init__(self, mass, diameter, i_x, i_y, material=None, nose_radius_m=0.0):
        self.mass = mass
        self.diameter = diameter
        self.reference_area = np.pi * (diameter / 2.0)**2
        self.i_x = i_x
        self.i_y = i_y
        self.material = material
        self.nose_radius_m = nose_radius_m

    @classmethod
    def from_stl(cls, filepath, density_kg_m3, scale_to_meters=1.0):
        """
        Loads an STL file using trimesh to automatically compute the physical properties.
        Assumes the mesh is watertight and aligned with the principal axes.

        filepath: Path to the STL file.
        density_kg_m3: Material density in kg/m^3 (e.g., Lead=11340, Steel=7850)
        scale_to_meters: Factor to convert mesh units to meters (e.g., if mesh is in mm, use 0.001)
        """
        import trimesh

        # Load mesh
        mesh = trimesh.load(filepath)

        # Apply scaling if the STL isn't natively in meters
        if scale_to_meters != 1.0:
            mesh.apply_scale(scale_to_meters)

        # Ensure watertight for accurate volume calculation
        if not mesh.is_watertight:
            # We will still try to compute, but it might be slightly inaccurate
            import warnings
            warnings.warn(f"Mesh {filepath} is not watertight. Volume/Inertia calculations may be imprecise.")

        # Calculate Mass
        volume = mesh.volume
        mass = volume * density_kg_m3

        # Calculate Inertia Tensor
        # trimesh returns inertia assuming density=1, so we multiply by our material density
        inertia_tensor = mesh.moment_inertia * density_kg_m3

        # Principal moments are the diagonal of the inertia tensor
        # Assuming the mesh is aligned such that X is the longitudinal (roll) axis,
        # and Y/Z are the transverse axes.
        i_x = inertia_tensor[0, 0]

        # For an axisymmetric projectile, Iy should equal Iz.
        # We take the average to smooth out minor meshing artifacts.
        i_y = (inertia_tensor[1, 1] + inertia_tensor[2, 2]) / 2.0

        # Determine Reference Diameter
        # We look at the bounding box extents in the Y and Z axes (transverse)
        extents = mesh.extents
        diameter = max(extents[1], extents[2])

        return cls(mass=mass, diameter=diameter, i_x=i_x, i_y=i_y)


class Aerodynamics:
    """
    Aerodynamic coefficients, handled either as analytical functions or via tabular data lookup.
    """
    @staticmethod
    def _default_cd(mach): return float(0.2 + 0.1 * np.exp(-0.5 * ((mach - 1.0)/0.2)**2))
    @staticmethod
    def _default_cl(mach): return 0.1
    @staticmethod
    def _default_cma(mach): return 2.5
    @staticmethod
    def _default_cmaq(mach): return -10.0
    @staticmethod
    def _default_cnlp(mach): return 0.5
    @staticmethod
    def _default_cmag(mach): return -0.5

    def __init__(self, cd=None, cl=None, cma=None, cmaq=None, cnlp=None, cmag=None):
        """
        Initialize coefficients. They can be passed as:
        - A callable function that takes Mach number as input.
        - A tuple (mach_array, coeff_array) for tabular interpolation.
        - A scalar value for a constant coefficient.
        - None, which will fall back to a default simplified model.
        """
        self._cd_func = self._build_callable(cd, self._default_cd)
        self._cl_func = self._build_callable(cl, self._default_cl)
        self._cma_func = self._build_callable(cma, self._default_cma)
        self._cmaq_func = self._build_callable(cmaq, self._default_cmaq)
        self._cnlp_func = self._build_callable(cnlp, self._default_cnlp)
        self._cmag_func = self._build_callable(cmag, self._default_cmag)

    def _build_callable(self, input_val, default_func, kind='linear', bounds_error=False, fill_value='extrapolate'):
        if input_val is None:
            return default_func
        if callable(input_val):
            return input_val
        if isinstance(input_val, (int, float)):
            # Create a true class to hold constant values so they are picklable
            class ConstantReturn:
                def __init__(self, val): self.val = float(val)
                def __call__(self, mach): return self.val
            return ConstantReturn(input_val)
        if isinstance(input_val, tuple) and len(input_val) == 2:
            mach_arr, coeff_arr = input_val
            return interp1d(mach_arr, coeff_arr, kind=kind, bounds_error=bounds_error, fill_value=fill_value)
        raise ValueError("Invalid format for aerodynamic coefficient.")

    def cd(self, mach): return self._cd_func(mach)
    def cl(self, mach): return self._cl_func(mach)
    def cma(self, mach): return self._cma_func(mach)
    def cmaq(self, mach): return self._cmaq_func(mach)
    def cnlp(self, mach): return self._cnlp_func(mach)
    def cmag(self, mach): return self._cmag_func(mach)

    @classmethod
    def g1(cls):
        """Returns an Aerodynamics instance using the standard G1 drag profile."""
        from ballistics.standard_models import G1_MACH, G1_CD
        return cls(cd=(G1_MACH, G1_CD))

    @classmethod
    def g7(cls):
        """Returns an Aerodynamics instance using the standard G7 drag profile."""
        from ballistics.standard_models import G7_MACH, G7_CD
        return cls(cd=(G7_MACH, G7_CD))

    @classmethod
    def from_csv(cls, filepath, kind='linear', bounds_error=False, fill_value='extrapolate'):
        """
        Loads aerodynamic tabular data from a CSV file.
        The CSV must have a header. Expected column names (case-insensitive):
        'Mach', 'Cd', 'Cl', 'Cma', 'Cmaq', 'Cnlp', 'Cmag'
        Only 'Mach' and at least one other coefficient column are required.
        """
        import csv

        mach_data = []
        coeff_data = {
            'cd': [], 'cl': [], 'cma': [], 'cmaq': [], 'cnlp': [], 'cmag': []
        }

        with open(filepath, mode='r') as f:
            reader = csv.DictReader(f)
            # Lowercase headers for robustness
            headers = [h.lower().strip() for h in reader.fieldnames]
            reader.fieldnames = headers

            if 'mach' not in headers:
                raise ValueError("CSV must contain a 'Mach' column.")

            for row in reader:
                mach_data.append(float(row['mach']))
                for key in coeff_data.keys():
                    if key in headers and row[key].strip() != '':
                        coeff_data[key].append(float(row[key]))
                    else:
                        coeff_data[key].append(None)

        mach_arr = np.array(mach_data)

        init_kwargs = {}
        for key, vals in coeff_data.items():
            # If we have any non-None values for this coefficient
            if any(v is not None for v in vals):
                # Filter out None values for this specific series
                valid_indices = [i for i, v in enumerate(vals) if v is not None]
                if len(valid_indices) > 0:
                    filtered_mach = mach_arr[valid_indices]
                    filtered_vals = np.array(vals)[valid_indices]
                    init_kwargs[key] = (filtered_mach, filtered_vals)

        instance = cls(**init_kwargs)

        # Override the build method behavior specifically for loaded tables to respect config
        for key in init_kwargs.keys():
            func_name = f"_{key}_func"
            m, c = init_kwargs[key]
            setattr(instance, func_name, interp1d(m, c, kind=kind, bounds_error=bounds_error, fill_value=fill_value))

        return instance
