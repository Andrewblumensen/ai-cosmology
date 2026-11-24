"""Pantheon+ Type Ia supernova likelihood (no SH0ES calibration).

Data: PantheonPlusSH0ES/DataRelease, Pantheon+_Data/4_DISTANCES_AND_COVAR
Paper: Brout et al. 2022, arXiv:2202.04077

The absolute magnitude M is marginalised analytically, so H0 drops out and only
the shape of the distance-redshift relation is used.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .background import Background

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "pantheon_plus"
TABLE = "Pantheon+SH0ES.dat"
COV = "Pantheon+SH0ES_STAT+SYS.cov"

C_KM_S = 299_792.458

# Planck 2018 CMB dipole (Galactic): Peterson et al. 2022, eq. 7
CMB_DIPOLE = dict(v=369.82, l=264.021, b=48.253)


def radec_to_galactic(ra_deg, dec_deg):
    """J2000 equatorial -> Galactic (l, b) in degrees."""
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    xyz = np.stack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)])
    R = np.array([[-0.0548755604, -0.8734370902, -0.4838350155],
                  [+0.4941094279, -0.4448296300, +0.7469822445],
                  [-0.8676661490, -0.1980763734, +0.4559837762]])
    g = R @ xyz
    l = np.degrees(np.arctan2(g[1], g[0])) % 360
    b = np.degrees(np.arcsin(np.clip(g[2], -1, 1)))
    return l, b


def unit(l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    return np.stack([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)], axis=-1)


class PantheonPlus:
    def __init__(self, data_dir: Path = DATA_DIR, z_min: float = 0.01):
        names = (data_dir / TABLE).read_text().splitlines()[0].split()
        tab = np.genfromtxt(data_dir / TABLE, names=names, dtype=None, encoding=None, skip_header=1)
        n = len(tab)
        cov = np.loadtxt(data_dir / COV, skiprows=1).reshape(n, n)
        keep = tab["zHD"] > z_min
        self.tab = tab[keep]
        self.z_hd = self.tab["zHD"].astype(float)
        self.z_hel = self.tab["zHEL"].astype(float)
        self.m = self.tab["m_b_corr"].astype(float)
        self.l, self.b = radec_to_galactic(self.tab["RA"].astype(float), self.tab["DEC"].astype(float))
        c = cov[np.ix_(keep, keep)]
        self.cov = c
        self.inv_cov = np.linalg.inv(c)
        self._ones_inv = self.inv_cov.sum(axis=1)
        self._norm = self._ones_inv.sum()

    def reboost(self, v: float, l: float, b: float) -> np.ndarray:
        """Redshifts re-boosted from the CMB-dipole frame to a frame moving with
        velocity v [km/s] toward Galactic (l, b) as seen from the Sun.
        Keeps Pantheon+'s peculiar-velocity corrections unchanged."""
        n = unit(self.l, self.b)
        cos_old = n @ unit(CMB_DIPOLE["l"], CMB_DIPOLE["b"])
        cos_new = n @ unit(l, b)
        return (1 + self.z_hd) * (1 - CMB_DIPOLE["v"] / C_KM_S * cos_old) / (1 - v / C_KM_S * cos_new) - 1

    def chi2(self, bg: Background, z_cosmo: np.ndarray | None = None) -> float:
        z = self.z_hd if z_cosmo is None else z_cosmo
        # distance modulus up to an additive constant (absorbed into M)
        mu = 5 * np.log10((1 + self.z_hel) * bg.chi(z))
        r = self.m - mu
        a = r @ self.inv_cov @ r
        bterm = r @ self._ones_inv
        return float(a - bterm ** 2 / self._norm)
