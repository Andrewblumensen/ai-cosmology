"""Compressed early-universe priors, exactly as used in DESI DR2 (arXiv:2503.14738).

- `CMBCompressed`: correlated Gaussian on (theta_*, omega_b, omega_bc), DESI DR2
  Appendix A eqs. 35-36, from the CamSpec compression of Lemos & Lewis (2023).
  DESI calls this the "(theta_*, omega_b, omega_bc) CMB" prior.
- `ThetaStarPrior`: 100 theta_* = 1.04110 +/- 0.00053 (DESI DR2 sec. IV, error
  inflated to cover late-time model dependence).
- `BBNPrior`: omega_b = 0.02218 +/- 0.00055 (DESI DR2 eq. 14).
"""

from __future__ import annotations

import numpy as np

from .cosmology import Cosmology


class CMBCompressed:
    mean = np.array([0.01041, 0.02223, 0.14208])
    cov = 1e-9 * np.array([[0.006621, 0.12444, -1.1929],
                           [0.12444, 21.344, -94.001],
                           [-1.1929, -94.001, 1488.4]])

    def __init__(self):
        self.inv_cov = np.linalg.inv(self.cov)

    def chi2(self, cosmo: Cosmology) -> float:
        r = np.array([cosmo.theta_star, cosmo.omega_b, cosmo.omega_bc]) - self.mean
        return float(r @ self.inv_cov @ r)


class ThetaStarPrior:
    def chi2(self, cosmo: Cosmology) -> float:
        return float(((100 * cosmo.theta_star - 1.04110) / 0.00053) ** 2)


class BBNPrior:
    def chi2(self, cosmo: Cosmology) -> float:
        return float(((cosmo.omega_b - 0.02218) / 0.00055) ** 2)
