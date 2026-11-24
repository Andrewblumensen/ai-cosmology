"""ID-016: did DESI's evolving-dark-energy signal grow from DR1 to DR2 like a real signal?

A real effect should strengthen roughly as precision improves. A statistical fluke or
a data-release-specific systematic tends to regress toward zero. Test: take the DR1 +
Pantheon+ best-fit CPL model as "truth", predict (noise-free, "Asimov") how big the
CPL-vs-LCDM preference should be with DR2 precision, and compare with what DR2 shows.

Pre-registered criterion: "signal-like" if the observed DR2 delta-chi2 is within
1 sigma of the Asimov expectation (sigma ~ sqrt(4 * expected delta-chi2), the standard
spread of a non-central chi2 statistic with large non-centrality); "fading" if it is
below by more than 1 sigma; "growing faster" if above by more than 1 sigma.

Caveats: DR2 contains the DR1 data (not independent); Pantheon+ is shared; no CMB.
"""

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aicosmo.background import Background, w_cpl  # noqa: E402
from aicosmo.bao import DesiDR2BAO  # noqa: E402
from aicosmo.sn import PantheonPlus  # noqa: E402

DR1_DIR = ROOT / "data" / "desi_dr1_bao"


class DesiDR1BAO(DesiDR2BAO):
    def __init__(self):
        import aicosmo.bao as b
        old = (b.MEAN_FILE, b.COV_FILE)
        b.MEAN_FILE, b.COV_FILE = ("desi_2024_gaussian_bao_ALL_GCcomb_mean.txt",
                                   "desi_2024_gaussian_bao_ALL_GCcomb_cov.txt")
        try:
            super().__init__(DR1_DIR)
        finally:
            b.MEAN_FILE, b.COV_FILE = old


sn = PantheonPlus()


def chi2(bao, p, sn_m=None):
    om, hrd = p[0], p[1]
    w = w_cpl(p[2], p[3]) if len(p) == 4 else None
    if len(p) == 4 and not (0.05 < om < 0.7 and p[2] + p[3] < 0):
        return 1e10
    try:
        bg = Background(om, w) if w else Background(om)
    except ValueError:
        return 1e10
    c = bao.chi2(bg, hrd)
    if sn_m is None:
        return c + sn.chi2(bg)
    saved = sn.m
    sn.m = sn_m
    try:
        return c + sn.chi2(bg)
    finally:
        sn.m = saved


def best(bao, x0, sn_m=None):
    r = minimize(lambda p: chi2(bao, p, sn_m), x0, method="Nelder-Mead",
                 options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 60000, "adaptive": True})
    return minimize(lambda p: chi2(bao, p, sn_m), r.x, method="Nelder-Mead",
                    options={"xatol": 1e-9, "fatol": 1e-11, "maxiter": 60000, "adaptive": True})


def dchi2(bao, sn_m=None):
    l = best(bao, [0.31, 100.0], sn_m)
    c = best(bao, [0.31, 100.0, -0.85, -0.5], sn_m)
    return l.fun - c.fun, c


def main():
    dr1, dr2 = DesiDR1BAO(), DesiDR2BAO()
    d1, cpl1 = dchi2(dr1)
    d2, cpl2 = dchi2(dr2)
    print(f"DR1 + Pantheon+: delta-chi2(LCDM - CPL) = {d1:.2f}  best CPL w0={cpl1.x[2]:.3f} wa={cpl1.x[3]:.3f}")
    print(f"DR2 + Pantheon+: delta-chi2(LCDM - CPL) = {d2:.2f}  best CPL w0={cpl2.x[2]:.3f} wa={cpl2.x[3]:.3f}")

    # Asimov: DR2 data vector and SN magnitudes replaced by DR1-best-fit CPL predictions
    om, hrd, w0, wa = cpl1.x
    bg = Background(om, w_cpl(w0, wa))
    saved = dr2.value.copy()
    dr2.value = dr2.predict(bg, hrd)
    sn_m = 5 * np.log10((1 + sn.z_hel) * bg.chi(sn.z_hd))
    d_exp, _ = dchi2(dr2, sn_m)
    dr2.value = saved
    spread = np.sqrt(4 * max(d_exp, 1e-9))
    z = (d2 - d_exp) / spread
    print(f"Asimov expectation for DR2 if DR1's CPL were true: delta-chi2 = {d_exp:.2f} +/- {spread:.2f}")
    print(f"Observed minus expected: {d2 - d_exp:+.2f}  ({z:+.2f} sigma)")
    verdict = "signal-like" if abs(z) <= 1 else ("fading" if z < 0 else "growing faster")
    print(f"Verdict (pre-registered): {verdict}")


if __name__ == "__main__":
    main()
