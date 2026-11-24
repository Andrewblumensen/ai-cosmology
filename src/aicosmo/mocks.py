"""Mock data: the false-alarm calibration for every search (CLAUDE.md rule 4).

A mock replaces each observed data vector by the prediction of a fiducial model plus
Gaussian noise drawn from that dataset's own covariance. Fitting models to many mocks
gives the distribution of Delta chi2 (or of the best score in a search) when the
fiducial model is true.

Validated in scripts/mock_null_test.py: on LCDM mocks, chi2_min(LCDM) follows
chi2(n - k) and Delta chi2(w0wa) follows chi2 with 2 dof.
"""

from __future__ import annotations

import copy

import numpy as np

from .score import Data, Model


def fiducial_vectors(data: Data, model: Model, x: np.ndarray) -> dict[str, np.ndarray]:
    """Noise-free data vectors predicted by `model` at parameters x (base + model)."""
    nb = len(data.base()[0])
    c, hrd = data.cosmology(x[:nb], model.w_of(x[nb:]), model.density)
    out = {}
    if data.bao:
        out["bao"] = data.bao.predict(c, hrd)
    if data.cmb:
        out["cmb"] = np.array([c.theta_star, c.omega_b, c.omega_bc])
    if data.sn:
        # Only the shape matters: the SN offset (absolute magnitude) is marginalised.
        out["sn"] = 5 * np.log10((1 + data.sn.z_hel) * c.chi(data.sn.z_hd))
    return out


def make_mock(data: Data, fiducial: dict[str, np.ndarray], rng: np.random.Generator) -> Data:
    """A copy of `data` whose observations are fiducial + correlated Gaussian noise.
    Covariances (and hence inverse covariances) are shared with the real data."""
    mock = copy.copy(data)
    if data.bao:
        mock.bao = copy.copy(data.bao)
        mock.bao.value = rng.multivariate_normal(fiducial["bao"], data.bao.cov)
    if data.cmb:
        mock.cmb = copy.copy(data.cmb)
        mock.cmb.mean = rng.multivariate_normal(fiducial["cmb"], data.cmb.cov)
    if data.sn:
        mock.sn = copy.copy(data.sn)
        mock.sn.m = fiducial["sn"] + _chol(data.sn) @ rng.standard_normal(len(fiducial["sn"]))
    return mock


def _chol(sn) -> np.ndarray:
    if not hasattr(sn, "_chol"):
        sn._chol = np.linalg.cholesky(sn.cov)
    return sn._chol
