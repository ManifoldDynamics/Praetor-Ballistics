import numpy as np

class ProjectileGeometry:
    """
    Parametric definition of an axisymmetric projectile shape for aerodynamic prediction.
    All dimensions are in meters unless specified.
    """
    def __init__(self, caliber_m,
                 nose_length_m, nose_type="tangent_ogive", meplat_diameter_m=0.0,
                 body_length_m=0.0,
                 boattail_length_m=0.0, boattail_base_diameter_m=None):

        self.caliber = caliber_m
        self.radius = caliber_m / 2.0
        self.ref_area = np.pi * self.radius**2

        # Nose
        self.nose_length = nose_length_m
        self.nose_type = nose_type.lower()
        self.meplat_diameter = meplat_diameter_m

        # Body (cylindrical bearing surface)
        self.body_length = body_length_m

        # Boattail (tapered base)
        self.boattail_length = boattail_length_m
        if boattail_base_diameter_m is None:
            self.boattail_base_diameter = caliber_m
        else:
            self.boattail_base_diameter = boattail_base_diameter_m

        self.base_area = np.pi * (self.boattail_base_diameter / 2.0)**2

        # Calculate Boattail Angle (radians)
        if self.boattail_length > 0.0:
            self.boattail_angle = np.arctan((self.caliber - self.boattail_base_diameter) / (2.0 * self.boattail_length))
        else:
            self.boattail_angle = 0.0

        self.total_length = self.nose_length + self.body_length + self.boattail_length
        self.fineness_ratio = self.total_length / self.caliber

    def wetted_area(self):
        """
        Calculates the approximate total wetted surface area of the projectile.
        Used for skin friction calculations.
        """
        # 1. Body cylinder area
        a_body = np.pi * self.caliber * self.body_length

        # 2. Nose area
        a_nose = 0.0
        if self.nose_length > 0.0:
            if self.nose_type == "cone":
                # Frustum of a cone (if meplat > 0)
                r1 = self.radius
                r2 = self.meplat_diameter / 2.0
                slant = np.sqrt(self.nose_length**2 + (r1 - r2)**2)
                a_nose = np.pi * (r1 + r2) * slant
            else:
                # Approximate Ogive surface area.
                # An exact integral for tangent ogive exists, but a parabolic approx is very close:
                # A_ogive ~ 2 * pi * r * L_nose * (1 - 0.33 * (r/L_nose)^2)
                # For simplicity, we use the cone approximation multiplied by a shape factor ~1.1 for ogives
                r1 = self.radius
                r2 = self.meplat_diameter / 2.0
                slant = np.sqrt(self.nose_length**2 + (r1 - r2)**2)
                a_nose = np.pi * (r1 + r2) * slant * 1.08 # Empirical bulge factor for ogives

        # 3. Boattail area (Frustum of a cone)
        if self.boattail_length > 0.0:
            r1 = self.radius
            r2 = self.boattail_base_diameter / 2.0
            slant = np.sqrt(self.boattail_length**2 + (r1 - r2)**2)
            a_boattail = np.pi * (r1 + r2) * slant
        else:
            a_boattail = 0.0

        return a_body + a_nose + a_boattail

    def nose_volume(self):
        """Calculates volume of the nose section."""
        r_base = self.radius
        r_tip = self.meplat_diameter / 2.0
        h = self.nose_length

        if self.nose_type == "cone":
            return (np.pi * h / 3.0) * (r_base**2 + r_base*r_tip + r_tip**2)
        else:
            # Approximate tangent ogive volume
            # V_ogive ~ pi * r^2 * h * (1 - 2/3 * (r/h)^2) for a sharp tip.
            # We'll use a standard empirical volume coefficient for ogives: ~0.54 * bounding cylinder
            return 0.54 * np.pi * r_base**2 * h

    def total_volume(self):
        """Calculates the total internal volume."""
        v_body = np.pi * self.radius**2 * self.body_length
        v_nose = self.nose_volume()

        if self.boattail_length > 0.0:
            r1 = self.radius
            r2 = self.boattail_base_diameter / 2.0
            v_boat = (np.pi * self.boattail_length / 3.0) * (r1**2 + r1*r2 + r2**2)
        else:
            v_boat = 0.0

        return v_body + v_nose + v_boat
