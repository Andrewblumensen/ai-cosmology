"""Reproduce published DESI DR2 fits (arXiv:2503.14738) with our own scorer.

This is the validation gate for the model-scoring engine (ID-033 / ID-034): if these
numbers do not match DESI, nothing scored by the engine can be trusted.

We compute best fits (MAP) and Delta chi2_MAP = chi2(w0wa) - chi2(LCDM), and compare
with DESI's Table V / VI. DESI quotes posterior means; for the strongly non-Gaussian
w0wa posteriors the MAP can sit a fraction of a sigma away from the mean.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aicosmo.background import w_cpl, w_lcdm  # noqa: E402
from aicosmo.bao import DesiDR2BAO  # noqa: E402
from aicosmo.cmb import BBNPrior, CMBCompressed, ThetaStarPrior  # noqa: E402
from aicosmo.cosmology import OMEGA_NU, Cosmology  # noqa: E402
from aicosmo.fit import best_fit, gaussian_errors  # noqa: E402
from aicosmo.sn import PantheonPlus  # noqa: E402

# DESI DR2 published values: (mean, sigma) per parameter, and Delta chi2_MAP vs LCDM.
PUBLISHED = {
    "LCDM DESI+BBN+theta*": {"Omega_m": (0.2967, 0.0045), "H0": (68.45, 0.47)},
    "w0wa DESI": {"dchi2": -4.7},
    "w0wa DESI+Pantheon+": {"w0": (-0.888, 0.060), "wa": (-0.17, 0.46), "dchi2": -4.9},
    "w0wa DESI+CMBc": {"Omega_m": (0.353, 0.022), "H0": (63.7, 2.0),
                       "w0": (-0.43, 0.22), "wa": (-1.72, 0.64), "dchi2": -8.0},
}
# Full-CMB result (CamSpec + lensing); we only have the compression, so this is indicative.
INDICATIVE = {
    "w0wa DESI+CMBc+Pantheon+": {"Omega_m": (0.3114, 0.0057), "H0": (67.51, 0.59),
                                 "w0": (-0.838, 0.055), "wa": (-0.62, 0.20), "dchi2": -10.7},
}


def desi_w_prior(w0: float, wa: float) -> None:
    """DESI DR2 sampling priors: w0 in [-3, 1], wa in [-3, 2], w0 + wa < 0."""
    if not (-3 <= w0 <= 1 and -3 <= wa <= 2 and w0 + wa < 0):
        raise ValueError("outside DESI prior")


class Combo:
    """A data combination. Parameters: h, omega_b, omega_bc[, w0, wa].
    Without CMB or BBN the BAO ruler is free: then omega_b is fixed and h*r_d is a parameter
    replacing omega_b (BAO and SN only see Omega_m, h*r_d and w)."""

    def __init__(self, bao=True, cmb=False, sn=False, bbn=False, theta=False):
        self.bao = DesiDR2BAO() if bao else None
        self.cmb = CMBCompressed() if cmb else None
        self.sn = PantheonPlus() if sn else None
        self.priors = [p for p, on in ((BBNPrior(), bbn), (ThetaStarPrior(), theta)) if on]
        self.calibrated = cmb or bbn

    def model(self, p, w0wa: bool) -> tuple[Cosmology, float]:
        w = w_cpl(p[3], p[4]) if w0wa else w_lcdm
        if w0wa:
            desi_w_prior(p[3], p[4])
        if self.calibrated:
            c = Cosmology(p[0], p[1], p[2], w)
            return c, c.hrd
        # free ruler: p = [Omega_m, h*r_d, (unused), w0, wa]; h only sets the tiny radiation term
        h = 0.68
        c = Cosmology(h, 0.0222, p[0] * h * h - OMEGA_NU, w)
        return c, p[1]

    def chi2(self, p, w0wa: bool) -> float:
        c, hrd = self.model(p, w0wa)
        out = sum(pr.chi2(c) for pr in self.priors)
        if self.bao:
            out += self.bao.chi2(c, hrd)
        if self.cmb:
            out += self.cmb.chi2(c)
        if self.sn:
            out += self.sn.chi2(c)
        return out

    def fit(self, w0wa: bool):
        if self.calibrated:
            x0, scale = [0.68, 0.0222, 0.142], [0.01, 0.0003, 0.002]
            steps = [1e-3, 2e-5, 2e-4]
        else:
            x0, scale, steps = [0.30, 101.5, 0.0], [0.01, 1.0, 0.0], [5e-4, 0.05, 1.0]
        if w0wa:
            x0, scale, steps = x0 + [-0.8, -0.5], scale + [0.1, 0.3], steps + [0.01, 0.03]
        free = np.array(scale) > 0
        fixed = np.array(x0, dtype=float)

        def f(q):
            p = fixed.copy()
            p[free] = q
            return self.chi2(p, w0wa)

        q, chi2 = best_fit(f, fixed[free], np.array(scale)[free])
        err = gaussian_errors(f, q, np.array(steps)[free])
        p, e = fixed.copy(), np.zeros_like(fixed)
        p[free], e[free] = q, err
        return p, e, chi2

    def summary(self, p, e, w0wa: bool) -> dict:
        c, _ = self.model(p, w0wa)
        out = {"Omega_m": c.omega_m}
        if self.calibrated:
            out["H0"] = 100 * p[0]
        if w0wa:
            out.update(w0=(p[3], e[3]), wa=(p[4], e[4]))
        return out


COMBOS = {
    "LCDM DESI+BBN+theta*": (dict(bbn=True, theta=True), False),
    "w0wa DESI": (dict(), True),
    "w0wa DESI+Pantheon+": (dict(sn=True), True),
    "w0wa DESI+CMBc": (dict(cmb=True), True),
    "w0wa DESI+CMBc+Pantheon+": (dict(cmb=True, sn=True), True),
}


def run(name: str) -> dict:
    kwargs, w0wa = COMBOS[name]
    combo = Combo(**kwargs)
    p, e, chi2 = combo.fit(w0wa)
    out = combo.summary(p, e, w0wa)
    out["chi2"] = chi2
    if w0wa:
        out["dchi2"] = chi2 - combo.fit(False)[2]
    return out


def main() -> None:
    for name in COMBOS:
        ours = run(name)
        ref = PUBLISHED.get(name) or INDICATIVE[name]
        tag = "" if name in PUBLISHED else "  (indicative: DESI used the full CMB likelihood)"
        print(f"\n{name}{tag}   chi2_min = {ours['chi2']:.2f}")
        for k, v in ref.items():
            mine = ours[k][0] if isinstance(ours[k], tuple) else ours[k]
            if isinstance(v, tuple):
                print(f"  {k:8s} ours {mine:9.4f}   DESI {v[0]:9.4f} +/- {v[1]:.4f}   "
                      f"diff {(mine - v[0]) / v[1]:+.2f} sigma")
            else:
                print(f"  {k:8s} ours {mine:9.2f}   DESI {v:9.2f}")


if __name__ == "__main__":
    main()
