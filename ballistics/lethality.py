import numpy as np

class FragmentationModel:
    """
    Empirical models for calculating warhead fragmentation effects.
    """

    @staticmethod
    def gurney_velocity(explosive_mass_kg, metal_mass_kg, gurney_constant_ms, geometry="cylinder"):
        """
        Calculates the initial velocity of fragments using the Gurney equations.

        explosive_mass_kg (C): Mass of the explosive charge.
        metal_mass_kg (M): Mass of the metal casing (projectile mass - explosive mass).
        gurney_constant_ms (sqrt(2E)): Gurney energy constant of the explosive.
        geometry: 'cylinder', 'sphere', or 'flat_plate'.

        Returns: Initial fragment velocity in m/s relative to the warhead center of mass.
        """
        if explosive_mass_kg <= 0 or metal_mass_kg <= 0:
            return 0.0

        ratio = explosive_mass_kg / metal_mass_kg

        if geometry == "cylinder":
            # Standard for artillery shells
            # V0 = sqrt(2E) * sqrt( (C/M) / (1 + 0.5 * C/M) )
            multiplier = np.sqrt(ratio / (1.0 + 0.5 * ratio))
        elif geometry == "sphere":
            # Standard for grenades
            # V0 = sqrt(2E) * sqrt( (C/M) / (1 + 0.6 * C/M) )
            multiplier = np.sqrt(ratio / (1.0 + 0.6 * ratio))
        elif geometry == "flat_plate":
            # Standard for mines/claymores/EFPs
            # V0 = sqrt(2E) * sqrt( (C/M) / (1 + 0.33 * C/M) )
            multiplier = np.sqrt(ratio / (1.0 + (1.0/3.0) * ratio))
        else:
            raise ValueError(f"Unknown Gurney geometry: {geometry}")

        return gurney_constant_ms * multiplier

    @staticmethod
    def generate_fragments(total_metal_mass_kg, num_fragments):
        """
        Generates a simplified uniform distribution of N fragments.
        For an MVP, we assume all fragments are equal mass spheres of steel.

        Returns a dictionary with average fragment properties.
        """
        if num_fragments <= 0:
            raise ValueError("Must generate at least 1 fragment.")

        frag_mass_kg = total_metal_mass_kg / float(num_fragments)

        # Assume spherical steel fragments (density ~ 7850 kg/m^3) to calculate aerodynamic diameter
        # V = 4/3 * pi * r^3 -> r = cbrt( 3V / 4pi )
        # m = rho * V -> V = m / rho
        density_steel = 7850.0
        frag_volume_m3 = frag_mass_kg / density_steel
        frag_radius_m = np.cbrt((3.0 * frag_volume_m3) / (4.0 * np.pi))
        frag_diam_m = frag_radius_m * 2.0

        # Cross-sectional area for drag/penetration
        frag_area_m2 = np.pi * frag_radius_m**2

        return {
            "mass_kg": frag_mass_kg,
            "diameter_m": frag_diam_m,
            "area_m2": frag_area_m2,
            "count": num_fragments
        }

    @staticmethod
    def spray_vectors(num_fragments, blast_velocity_ms, geometry="cylinder", pitch_bias=0.0):
        """
        Generates 3D velocity vectors for fragments originating from an explosion.

        Returns an Nx3 array of velocity vectors [Vx, Vy, Vz] in the projectile's body frame.
        """
        vectors = np.zeros((num_fragments, 3))

        if geometry == "sphere":
            # Uniform spherical distribution using Fibonacci lattice
            phi = np.pi * (3. - np.sqrt(5.))  # golden angle in radians
            for i in range(num_fragments):
                y = 1 - (i / float(num_fragments - 1)) * 2  # y goes from 1 to -1
                radius = np.sqrt(1 - y * y)  # radius at y
                theta = phi * i  # golden angle increment
                x = np.cos(theta) * radius
                z = np.sin(theta) * radius
                vectors[i] = [x, y, z]

        elif geometry == "cylinder":
            # Artillery shells spray mostly laterally (perpendicular to X-axis).
            # We generate a band of fragments around the X-axis.
            # Elevation (angle off X-axis) is biased strongly towards 90 degrees.
            # Azimuth is uniform 0 to 360 around the X-axis.
            for i in range(num_fragments):
                # Normal distribution centered at 90 deg (pi/2) with 15 deg standard deviation
                theta = np.random.normal(np.pi/2, np.deg2rad(15.0))
                # Add optional pitch bias (e.g. for shaped charges or nose cones)
                theta += pitch_bias

                # Uniform azimuth
                phi = np.random.uniform(0, 2*np.pi)

                # Spherical to Cartesian (X is longitudinal axis)
                x = np.cos(theta)
                y = np.sin(theta) * np.cos(phi)
                z = np.sin(theta) * np.sin(phi)

                vectors[i] = [x, y, z]
        else:
            raise ValueError(f"Unsupported spray geometry: {geometry}")

        # Scale unit vectors by blast velocity
        vectors *= blast_velocity_ms
        return vectors
