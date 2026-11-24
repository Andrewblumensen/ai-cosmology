"""Generic model scorer: the engine for ID-033 (catalogue re-scoring) and ID-034 (search).

A `Model` is a dark-energy equation of state w(z; theta) with named parameters and
hard bounds. `score(model, data)` returns the best-fit chi2 over the model parameters
plus the base cosmology, information criteria, and physicality flags.

Validated by scripts/reproduce_desi_dr2.py / tests/test_desi_dr2_reproduction.py:
LCDM and w0wa through this API reproduce DESI DR2's published fits.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from .background import WFunc, w_cpl, w_lcdm
from .bao import DesiDR2BAO
from .cmb import BBNPrior, CMBCompressed, ThetaStarPrior
from .cosmology import OMEGA_NU, Cosmology
from .fit import best_fit, gaussian_errors
from .sn import PantheonPlus

# Redshifts at which physicality is checked (data reach z ~ 2.3; CMB needs up to 1100)
Z_CHECK = np.concatenate([np.linspace(0, 3, 301), np.geomspace(3.01, 1100, 100)])


@dataclass
class Param:
    x0: float     # starting point
    scale: float  # initial simplex step (also sets the Hessian step / 10)
    lo: float = -np.inf
    hi: float = np.inf


@dataclass
class Model:
    name: str
    params: dict[str, Param]
    w: Callable[..., WFunc]  # w(**params) -> callable w(z)
    constraint: Callable[..., bool] | None = None  # extra prior, e.g. DESI's w0 + wa < 0
    notes: str = ""

    def w_of(self, theta: np.ndarray) -> WFunc:
        kw = dict(zip(self.params, theta))
        for (n, p), v in zip(self.params.items(), theta):
            if not p.lo <= v <= p.hi:
                raise ValueError(f"{n} outside its range")
        if self.constraint and not self.constraint(**kw):
            raise ValueError("constraint violated")
        return self.w(**kw)


LCDM = Model("LCDM", {}, lambda: w_lcdm)
W0WA = Model("w0wa (CPL)",
             {"w0": Param(-0.8, 0.1, -3, 1), "wa": Param(-0.5, 0.3, -3, 2)},
             w_cpl, constraint=lambda w0, wa: w0 + wa < 0,
             notes="DESI DR2 priors: w0 in [-3,1], wa in [-3,2], w0 + wa < 0")


class Data:
    """A data combination. If neither CMB nor BBN calibrates the BAO ruler, h*r_d is a
    free parameter and omega_b is fixed (BAO and SN then only see Omega_m, h*r_d and w)."""

    def __init__(self, bao=True, cmb=False, sn=False, bbn=False, theta=False):
        self.bao = DesiDR2BAO() if bao else None
        self.cmb = CMBCompressed() if cmb else None
        self.sn = PantheonPlus() if sn else None
        self.priors = [p for p, on in ((BBNPrior(), bbn), (ThetaStarPrior(), theta)) if on]
        self.calibrated = cmb or bbn
        self.n_points = (len(self.bao.value) if bao else 0) + (3 if cmb else 0) \
            + (len(self.sn.m) if sn else 0) + len(self.priors)

    # base parameters: calibrated -> (h, omega_b, omega_bc); free ruler -> (Omega_m, h*r_d)
    def base(self):
        if self.calibrated:
            return [0.68, 0.0222, 0.142], [0.01, 0.0003, 0.002], [1e-3, 2e-5, 2e-4]
        return [0.30, 101.5], [0.01, 1.0], [5e-4, 0.05]

    def cosmology(self, base, w: WFunc) -> tuple[Cosmology, float]:
        if self.calibrated:
            c = Cosmology(base[0], base[1], base[2], w)
            return c, c.hrd
        h = 0.68  # only sets the tiny radiation term
        return Cosmology(h, 0.0222, base[0] * h * h - OMEGA_NU, w), base[1]

    def chi2(self, c: Cosmology, hrd: float) -> float:
        out = sum(p.chi2(c) for p in self.priors)
        if self.bao:
            out += self.bao.chi2(c, hrd)
        if self.cmb:
            out += self.cmb.chi2(c)
        if self.sn:
            out += self.sn.chi2(c)
        return out


@dataclass
class Score:
    model: str
    chi2: float
    k: int                   # total free parameters (base + model)
    n: int                   # data points
    best: dict[str, float]
    errors: dict[str, float]
    w_min: float             # min w(z) over 0 <= z <= 3
    phantom_crossing: bool   # w - (-1) changes sign for 0 <= z <= 3
    x: np.ndarray = field(default=None, repr=False)  # raw best-fit vector (base + model)
    extra: dict = field(default_factory=dict)

    @property
    def aic(self) -> float:
        return self.chi2 + 2 * self.k

    @property
    def bic(self) -> float:
        return self.chi2 + self.k * np.log(self.n)


def score(model: Model, data: Data, errors: bool = True) -> Score:
    b0, bscale, bsteps = data.base()
    nb = len(b0)
    x0 = b0 + [p.x0 for p in model.params.values()]
    scale = bscale + [p.scale for p in model.params.values()]
    steps = bsteps + [p.scale / 10 for p in model.params.values()]

    def f(x):
        c, hrd = data.cosmology(x[:nb], model.w_of(x[nb:]))
        return data.chi2(c, hrd)

    x, chi2 = best_fit(f, x0, scale)
    err = gaussian_errors(f, x, steps) if errors else np.full(len(x), np.nan)
    c, _ = data.cosmology(x[:nb], model.w_of(x[nb:]))
    names = (["h", "omega_b", "omega_bc"] if data.calibrated else ["Omega_m", "hrd"]) + list(model.params)
    best = dict(zip(names, map(float, x)))
    best["Omega_m"] = c.omega_m
    if data.calibrated:
        best["H0"] = 100 * x[0]
    wz = model.w_of(x[nb:])(Z_CHECK[Z_CHECK <= 3]) + 1.0
    return Score(model.name, chi2, len(x), data.n_points, best,
                 dict(zip(names, map(float, err))), float(wz.min() - 1),
                 bool(wz.min() < -1e-9 and wz.max() > 1e-9), x=np.asarray(x))
