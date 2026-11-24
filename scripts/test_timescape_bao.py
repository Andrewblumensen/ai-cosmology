"""ID-032b: timescape vs LCDM on DESI DR2 BAO, alone and with Pantheon+ (pre-registered)."""

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aicosmo.background import Background  # noqa: E402
from aicosmo.bao import DesiDR2BAO  # noqa: E402
from aicosmo.sn import PantheonPlus  # noqa: E402
from aicosmo.timescape import Timescape  # noqa: E402

sn = PantheonPlus()
_cache = {}


def ts(f):
    key = round(float(f), 6)
    if key not in _cache:
        _cache[key] = Timescape(key, z_max=2.5, n=2500)
    return _cache[key]


def fit(fun, x0, bounds):
    best = None
    for start in x0:
        r = minimize(fun, start, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 4000})
        if best is None or r.fun < best.fun:
            best = r
    return best


def run(bao, label, with_sn):
    def chi_l(p):
        if not 0.05 < p[0] < 0.7:
            return 1e10
        bg = Background(p[0])
        return bao.chi2(bg, p[1]) + (sn.chi2(bg) if with_sn else 0.0)

    def chi_t(p):
        if not 0.05 < p[0] < 0.97:
            return 1e10
        m = ts(p[0])
        return bao.chi2(m, p[1]) + (sn.chi2(m) if with_sn else 0.0)

    L = fit(chi_l, [[0.3, 100.0], [0.35, 95.0]], None)
    T = fit(chi_t, [[0.76, 100.0], [0.6, 95.0], [0.85, 105.0]], None)
    print(f"  {label:34s} LCDM chi2={L.fun:8.2f} (Om={L.x[0]:.3f})   TS chi2={T.fun:8.2f} (f_v0={T.x[0]:.3f})   dchi2(L-TS)={L.fun - T.fun:+7.2f}")
    return L.fun - T.fun, T


def main():
    bao = DesiDR2BAO()
    print("Baseline errors:")
    dA, TA = run(bao, "(A) DESI DR2 BAO alone", False)
    dB, TB = run(bao, "(B) DESI DR2 BAO + Pantheon+", True)
    # (C) robustness: +1% systematic in quadrature on each BAO point
    cov = np.linalg.inv(bao.inv_cov) + np.diag((0.01 * bao.value) ** 2)
    bao_c = DesiDR2BAO()
    bao_c.inv_cov = np.linalg.inv(cov)
    print("Robustness (C), +1% BAO systematic:")
    run(bao_c, "(C-A) BAO alone", False)
    run(bao_c, "(C-B) BAO + Pantheon+", True)

    if dA >= 4 and dB >= 4:
        v = "timescape favoured"
    elif dB <= -4:
        v = "timescape disfavoured"
    else:
        v = "inconclusive"
    print(f"\nVerdict (pre-registered, baseline): {v}")

    # Where does it come from? Per-point residuals for the BAO+SN best fits.
    print("\nPer-point pulls at the (B) best fits [(data - model)/sigma]:")
    err = np.sqrt(np.diag(np.linalg.inv(bao.inv_cov)))
    L = fit(lambda p: bao.chi2(Background(p[0]), p[1]) + sn.chi2(Background(p[0])), [[0.3, 100.0]], None)
    pl = bao.predict(Background(L.x[0]), L.x[1])
    pt = bao.predict(ts(TB.x[0]), TB.x[1])
    for z, k, v_, a, b, e in zip(bao.z, bao.kind, bao.value, pl, pt, err):
        print(f"  z={z:5.3f} {k:11s}  LCDM {(v_-a)/e:+5.2f}   TS {(v_-b)/e:+5.2f}")


if __name__ == "__main__":
    main()
