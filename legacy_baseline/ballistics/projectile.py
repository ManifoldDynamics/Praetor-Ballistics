import numpy as np

class Projectile:
    """
    Physical properties of the projectile.
    """
    def __init__(self, mass, diameter, i_x, i_y):
        self.mass = mass
        self.diameter = diameter
        self.reference_area = np.pi * (diameter / 2.0)**2
        self.i_x = i_x
        self.i_y = i_y


class Aerodynamics:
    def __init__(self, cd_func=None, cl_func=None, cma_func=None, cmaq_func=None, cnlp_func=None, cmag_func=None):
        self._cd_func = cd_func if cd_func else lambda mach: 0.2 + 0.1 * np.exp(-0.5 * ((mach - 1.0)/0.2)**2)
        self._cl_func = cl_func if cl_func else lambda mach: 0.1
        self._cma_func = cma_func if cma_func else lambda mach: 2.5
        self._cmaq_func = cmaq_func if cmaq_func else lambda mach: -10.0
        self._cnlp_func = cnlp_func if cnlp_func else lambda mach: 0.5
        self._cmag_func = cmag_func if cmag_func else lambda mach: -0.5

    def cd(self, mach): return self._cd_func(mach)
    def cl(self, mach): return self._cl_func(mach)
    def cma(self, mach): return self._cma_func(mach)
    def cmaq(self, mach): return self._cmaq_func(mach)
    def cnlp(self, mach): return self._cnlp_func(mach)
    def cmag(self, mach): return self._cmag_func(mach)
