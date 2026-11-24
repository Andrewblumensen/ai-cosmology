"""Full flat background from z = 0 to recombination, on the same footing as DESI DR2.

Unlike `Background` (matter + DE only, z < 3), this includes photons and neutrinos
(Neff = 3.044, one massive eigenstate of 0.06 eV, as in DESI DR2 and CAMB), so it can
compute the CMB acoustic scale theta_* and the BAO ruler r_d.

Parameters are physical: h, omega_b = Omega_b h^2, omega_bc = (Omega_b + Omega_c) h^2.
Dark energy fills the rest of a flat universe; its equation of state is any w(z).

The object exposes the same E / chi / *_over_rd methods as `Background`, so the
BAO and SN likelihoods accept it unchanged. Validated against CAMB in
tests/test_cosmology_vs_camb.py.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_trapezoid, quad
from scipy.interpolate import CubicSpline, RectBivariateSpline
from scipy.optimize import brentq

from .background import WFunc, w_lcdm

C_KM_S = 299_792.458
TCMB = 2.7255
NEFF = 3.044
MNU = 0.06  # eV, one massive eigenstate
# Omega_gamma h^2 for TCMB = 2.7255 K (CAMB constants)
OMEGA_GAMMA = 2.4729753278460546e-5
# One fully relativistic neutrino species relative to photons
NU_PER_SPECIES = 7.0 / 8.0 * (4.0 / 11.0) ** (4.0 / 3.0)
# CAMB convention: the massive eigenstate carries Neff/3 of the degeneracy
NU_MASSIVE_DEG = NEFF / 3.0
NU_MASSLESS = NEFF - NU_MASSIVE_DEG
# CAMB: omnuh2 = mnu / 94.0641 eV * deg^(3/4)
OMEGA_NU = MNU / 94.06410581217612 * NU_MASSIVE_DEG ** 0.75

Z_MAX = 1300.0
N_GRID = 20001

_TABLE = Path(__file__).with_name("early_table.txt")


# --- massive neutrinos -------------------------------------------------------

def _fd_energy(y: float) -> float:
    """Integral x^2 sqrt(x^2 + y^2) / (e^x + 1): energy density of one FD species."""
    return quad(lambda x: x * x * np.sqrt(x * x + y * y) / (np.exp(x) + 1), 0, 60, limit=200)[0]


@lru_cache(maxsize=1)
def _nu_tables():
    """Spline of F(y)/F(0) in log y, and y0 = m / T_nu today matching OMEGA_NU."""
    f0 = 7 * np.pi ** 4 / 120
    log_y = np.linspace(np.log(1e-5), np.log(1e4), 600)
    ratio = np.array([_fd_energy(np.exp(v)) / f0 for v in log_y])
    spline = CubicSpline(log_y, np.log(ratio))
    rho_rel_today = NU_MASSIVE_DEG * NU_PER_SPECIES * OMEGA_GAMMA
    y0 = brentq(lambda ly: np.exp(spline(ly)) * rho_rel_today - OMEGA_NU, log_y[0], log_y[-1])
    return spline, np.exp(y0)


def omega_nu_massive(z: np.ndarray) -> np.ndarray:
    """omega (physical density / critical per h^2) of the massive species at z."""
    spline, y0 = _nu_tables()
    a = 1.0 / (1.0 + np.asarray(z, dtype=float))
    y = np.clip(y0 * a, 1e-5, 1e4)
    return NU_MASSIVE_DEG * NU_PER_SPECIES * OMEGA_GAMMA * np.exp(spline(np.log(y))) / a ** 4


# --- early-universe quantities from CAMB -------------------------------------

@lru_cache(maxsize=1)
def _early_splines():
    t = np.loadtxt(_TABLE)
    wb, wbc = np.unique(t[:, 0]), np.unique(t[:, 1])
    grid = lambda col: t[:, col].reshape(len(wb), len(wbc))  # noqa: E731
    return {name: RectBivariateSpline(wb, wbc, grid(col), kx=3, ky=3)
            for name, col in (("z_star", 2), ("r_star", 3), ("r_drag", 4))}


def early(name: str, omega_b: float, omega_bc: float) -> float:
    return float(_early_splines()[name](omega_b, omega_bc)[0, 0])


# --- the model ---------------------------------------------------------------

class Cosmology:
    def __init__(self, h: float, omega_b: float, omega_bc: float, w: WFunc = w_lcdm,
                 rho_de: WFunc | None = None):
        """Dark energy is given either by w(z) or directly by rho_de(z) = rho_DE(z)/rho_DE(0)
        (effective density: everything beyond matter and radiation, may go negative)."""
        self.h, self.omega_b, self.omega_bc = h, omega_b, omega_bc
        x = np.linspace(0.0, np.log1p(Z_MAX), N_GRID)  # x = ln(1 + z)
        z = np.expm1(x)
        omega_rad = (OMEGA_GAMMA + NU_MASSLESS * NU_PER_SPECIES * OMEGA_GAMMA) * (1 + z) ** 4
        omega_nu = omega_nu_massive(z)
        omega_de0 = h * h - omega_bc - omega_rad[0] - omega_nu[0]
        # rho_de(z)/rho_de(0) = exp(3 int (1 + w) dln(1+z))
        if rho_de is None:
            de = np.exp(3.0 * cumulative_trapezoid(1.0 + w(z), x, initial=0.0))
        else:
            de = np.asarray(rho_de(z), dtype=float)
        e2 = (omega_bc * (1 + z) ** 3 + omega_rad + omega_nu + omega_de0 * de) / (h * h)
        if np.any(e2 <= 0) or not np.all(np.isfinite(e2)):
            raise ValueError("Unphysical expansion history (H^2 <= 0 or non-finite).")
        self._x = x
        self._e = np.sqrt(e2)
        self._chi = cumulative_trapezoid((1 + z) / self._e, x, initial=0.0)
        self.omega_m = (omega_bc + omega_nu[0]) / (h * h)  # Omega_m today, incl. neutrinos (DESI)
        self.omega_de = omega_de0 / (h * h)

    def E(self, z) -> np.ndarray:
        return np.interp(np.log1p(z), self._x, self._e)

    def chi(self, z) -> np.ndarray:
        """Comoving distance in units of c/H0."""
        return np.interp(np.log1p(z), self._x, self._chi)

    @property
    def r_drag(self) -> float:
        return early("r_drag", self.omega_b, self.omega_bc)

    @property
    def hrd(self) -> float:
        return self.h * self.r_drag

    @property
    def theta_star(self) -> float:
        """Angular acoustic scale r_* / D_M(z_*) in radians."""
        z_star = early("z_star", self.omega_b, self.omega_bc)
        dm = C_KM_S / (100.0 * self.h) * self.chi(z_star)
        return early("r_star", self.omega_b, self.omega_bc) / float(dm)

    # Same BAO interface as Background (hrd is h * r_d in Mpc)
    def dm_over_rd(self, z, hrd: float) -> np.ndarray:
        return C_KM_S / (100.0 * hrd) * self.chi(z)

    def dh_over_rd(self, z, hrd: float) -> np.ndarray:
        return C_KM_S / (100.0 * hrd) / self.E(z)

    def dv_over_rd(self, z, hrd: float) -> np.ndarray:
        z = np.asarray(z, dtype=float)
        return np.cbrt(z * self.dm_over_rd(z, hrd) ** 2 * self.dh_over_rd(z, hrd))
