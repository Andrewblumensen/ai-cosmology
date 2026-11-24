"""Background (homogeneous) cosmology: expansion rate and distances.

Flat universe with matter + dark energy. Radiation is neglected: at z < 2.5 it
changes distances by roughly 0.1%, below current BAO errors. Add it before using
these functions at high redshift or with CMB data.

Dark energy is given as an equation of state w(z), any vectorised callable.
That is the interface the LLM-proposed models will plug into.
"""

from __future__ import annotations

from typing import Callable

import numpy as np
from scipy.integrate import cumulative_trapezoid

C_KM_S = 299_792.458  # speed of light [km/s]

WFunc = Callable[[np.ndarray], np.ndarray]


def w_lcdm(z: np.ndarray) -> np.ndarray:
    return np.full_like(np.asarray(z, dtype=float), -1.0)


def w_cpl(w0: float, wa: float) -> WFunc:
    """Chevallier-Polarski-Linder: w(a) = w0 + wa (1 - a)."""
    return lambda z: w0 + wa * np.asarray(z) / (1.0 + np.asarray(z))


class Background:
    """Precomputes E(z) and comoving distance on a redshift grid."""

    def __init__(self, omega_m: float, w: WFunc = w_lcdm, z_max: float = 3.0, n: int = 3001):
        self.omega_m = omega_m
        z = np.linspace(0.0, z_max, n)
        # rho_de(z)/rho_de(0) = exp(3 * int_0^z (1 + w) / (1 + z') dz')
        integrand = (1.0 + w(z)) / (1.0 + z)
        log_rho = 3.0 * cumulative_trapezoid(integrand, z, initial=0.0)
        e2 = omega_m * (1.0 + z) ** 3 + (1.0 - omega_m) * np.exp(log_rho)
        if np.any(e2 <= 0) or not np.all(np.isfinite(e2)):
            raise ValueError("Unphysical expansion history (H^2 <= 0 or non-finite).")
        self._z = z
        self._e = np.sqrt(e2)
        # dimensionless comoving distance: int_0^z dz / E
        self._chi = cumulative_trapezoid(1.0 / self._e, z, initial=0.0)

    def E(self, z) -> np.ndarray:
        return np.interp(z, self._z, self._e)

    def chi(self, z) -> np.ndarray:
        """Comoving distance in units of c/H0."""
        return np.interp(z, self._z, self._chi)

    # --- BAO observables, in units of the sound horizon r_d ---
    # All scale as c / (H0 r_d) = C_KM_S / (100 * h * r_d), so BAO alone
    # constrains the combination h*r_d [Mpc], not h and r_d separately.

    def dm_over_rd(self, z, hrd: float) -> np.ndarray:
        return C_KM_S / (100.0 * hrd) * self.chi(z)

    def dh_over_rd(self, z, hrd: float) -> np.ndarray:
        return C_KM_S / (100.0 * hrd) / self.E(z)

    def dv_over_rd(self, z, hrd: float) -> np.ndarray:
        z = np.asarray(z, dtype=float)
        return np.cbrt(z * self.dm_over_rd(z, hrd) ** 2 * self.dh_over_rd(z, hrd))
