"""Timescape cosmology distances (tracker solution), from Wiltshire 2009,
"Average observational quantities in the timescape cosmology", arXiv:0909.0749:

  1+z  = 2^{4/3} t^{1/3} (t+b) / [ f_v0^{1/3} Hb t (2t+3b)^{4/3} ]      (eq. 38)
  d_A  = t^{2/3} [ F(t0) - F(t) ]                                      (eq. 40, c = 1)
  F(t) = 2 t^{1/3} + (b^{1/3}/6) ln[(t^{1/3}+b^{1/3})^2 / (t^{2/3} - b^{1/3} t^{1/3} + b^{2/3})]
         + (b^{1/3}/sqrt3) atan[(2 t^{1/3} - b^{1/3}) / (sqrt3 b^{1/3})]   (eq. 41)
  b    = 2 (1-f_v0)(2+f_v0) / (9 f_v0 Hb)                               (eq. 39)
  t0   = (2+f_v0) / (3 Hb)                                              (App. B)
  H0 (dressed) = (4 f_v0^2 + f_v0 + 4) Hb / (2 (2+f_v0))                (eq. B9)

t is volume-average time; Hb is the bare Hubble parameter. Distances here are in units
of c/H0_dressed so they plug into the same likelihoods as the FLRW Background (only
the shape matters for supernovae, since M is marginalised).
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

SQ3 = np.sqrt(3.0)


class Timescape:
    def __init__(self, fv0: float, z_max: float = 2.5, n: int = 4000):
        if not 0.0 < fv0 < 1.0:
            raise ValueError("void fraction must be in (0, 1)")
        self.fv0 = fv0
        Hb = 1.0
        self.b = 2 * (1 - fv0) * (2 + fv0) / (9 * fv0 * Hb)
        self.t0 = (2 + fv0) / (3 * Hb)
        self.H0_dressed = (4 * fv0**2 + fv0 + 4) * Hb / (2 * (2 + fv0))
        zg = np.linspace(0.0, z_max, n)
        tg = np.array([self._t_of_z(z) for z in zg])
        D = (1 + zg) * tg ** (2 / 3) * (self._F(self.t0) - self._F(tg))  # comoving-like, c/Hb units
        self._z, self._D = zg, D * self.H0_dressed                          # -> units of c/H0_dressed

    def _onepz(self, t):
        b, f = self.b, self.fv0
        return 2 ** (4 / 3) * t ** (1 / 3) * (t + b) / (f ** (1 / 3) * t * (2 * t + 3 * b) ** (4 / 3))

    def _t_of_z(self, z):
        if z == 0:
            return self.t0
        return brentq(lambda t: self._onepz(t) - (1 + z), 1e-12 * self.t0, self.t0, xtol=1e-14, rtol=1e-13, maxiter=500)

    def _F(self, t):
        b3 = self.b ** (1 / 3)
        t3 = np.asarray(t) ** (1 / 3)
        return (2 * t3 + (b3 / 6) * np.log((t3 + b3) ** 2 / (t3**2 - b3 * t3 + b3**2))
                + (b3 / SQ3) * np.arctan((2 * t3 - b3) / (SQ3 * b3)))

    def chi(self, z):
        """Comoving-type distance D(z) = (1+z) d_A in units of c/H0_dressed,
        the same role as Background.chi for the supernova likelihood."""
        return np.interp(z, self._z, self._D)

    # --- BAO observables (ID-032b assumptions: D_M = D, D_H = dD/dz) ---
    # hrd plays the same role as for FLRW: a free scale c/(H0 r_d) absorbs H0 and r_d.

    def _dDdz(self, z):
        return np.interp(z, self._z, np.gradient(self._D, self._z))

    def dm_over_rd(self, z, hrd):
        return 299_792.458 / (100.0 * hrd) * self.chi(z)

    def dh_over_rd(self, z, hrd):
        return 299_792.458 / (100.0 * hrd) * self._dDdz(z)

    def dv_over_rd(self, z, hrd):
        z = np.asarray(z, dtype=float)
        return np.cbrt(z * self.dm_over_rd(z, hrd) ** 2 * self.dh_over_rd(z, hrd))
