import numpy as np

class AerothermodynamicsV2:
    """
    V2 Proprietary Aerothermodynamics Solver.
    Implements a 1D Radial Nodal Conduction model for projectile nose heating.
    """
    @staticmethod
    def calculate_derivatives(t, temperatures, q_conv, q_rad, r_nose, skin_thickness, material, num_nodes=5):
        """
        Calculates dT/dt for each node in a 1D radial finite difference grid.
        temperatures: list or array of current nodal temperatures [T_surface, ..., T_core]
        q_conv, q_rad: External heat fluxes (W/m^2)
        r_nose: External nose radius (m)
        skin_thickness: Total depth being modeled (m)
        material: Material object with density, specific_heat, thermal_conductivity
        num_nodes: Number of discrete nodes through the thickness.
        """
        dr = skin_thickness / (num_nodes - 1)
        rho = material.density
        cp = material.specific_heat
        k = material.thermal_conductivity

        # dT/dt = (1 / (rho*cp)) * [ k * d2T/dr2 + (2k/r) * dT/dr ] (Spherical coordinates)

        dT_dt = np.zeros(num_nodes)

        for i in range(num_nodes):
            # radius of current node
            r_i = r_nose - i * dr

            if i == 0:
                # Surface Node (Boundary Condition)
                # q_net = q_conv - q_rad - k * dT/dr_at_surface
                # Heat balance: (rho*cp*dV) * dT/dt = q_net * dA
                # For a thin spherical shell cap:
                dT_dt[i] = (q_conv - q_rad - k * (temperatures[0] - temperatures[1])/dr) * (3 / (rho * cp * dr))
            elif i == num_nodes - 1:
                # Core Node (Insulated or Heat Sink)
                # Assuming adiabatic core for now: k * dT/dr = 0
                dT_dt[i] = k * (temperatures[i-1] - temperatures[i]) / (rho * cp * dr**2)
            else:
                # Interior Nodes (Central Difference)
                d2T_dr2 = (temperatures[i-1] - 2*temperatures[i] + temperatures[i+1]) / dr**2
                dT_dr = (temperatures[i-1] - temperatures[i+1]) / (2*dr)

                dT_dt[i] = (k / (rho * cp)) * (d2T_dr2 + (2 / r_i) * dT_dr)

        return dT_dt
