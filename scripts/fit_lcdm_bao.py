"""Fit flat LCDM and CPL (w0, wa) to DESI DR2 BAO alone.

Validation target (DESI DR2, arXiv:2503.14738, BAO-only flat LCDM):
Omega_m and h*r_d should match the paper's values within a small fraction of 1 sigma.
"""

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aicosmo.background import Background, w_cpl  # noqa: E402
from aicosmo.bao import DesiDR2BAO  # noqa: E402


def fit_lcdm(bao: DesiDR2BAO):
    f = lambda p: bao.chi2(Background(p[0]), p[1])
    res = minimize(f, x0=[0.3, 100.0], method="Nelder-Mead",
                   options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 5000})
    # 1-sigma errors from a numerical Hessian of chi2/2
    h = np.array([1e-4, 1e-2])
    p = res.x
    H = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            ei, ej = np.eye(2)[i] * h[i], np.eye(2)[j] * h[j]
            H[i, j] = (f(p + ei + ej) - f(p + ei - ej) - f(p - ei + ej) + f(p - ei - ej)) / (4 * h[i] * h[j])
    err = np.sqrt(np.diag(np.linalg.inv(H / 2)))
    return res, err


def fit_cpl(bao: DesiDR2BAO):
    def f(p):
        try:
            return bao.chi2(Background(p[0], w_cpl(p[2], p[3])), p[1])
        except ValueError:
            return 1e10
    return minimize(f, x0=[0.3, 100.0, -0.9, -0.3], method="Nelder-Mead",
                    options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 20000})


def main() -> None:
    bao = DesiDR2BAO()
    res, err = fit_lcdm(bao)
    print(f"Flat LCDM   Omega_m = {res.x[0]:.4f} +/- {err[0]:.4f}   "
          f"h*r_d = {res.x[1]:.2f} +/- {err[1]:.2f} Mpc   chi2 = {res.fun:.2f} (13 points, 2 params)")
    cpl = fit_cpl(bao)
    print(f"CPL (BAO only, poorly constrained)  w0 = {cpl.x[2]:.2f}  wa = {cpl.x[3]:.2f}  "
          f"chi2 = {cpl.fun:.2f}  delta chi2 vs LCDM = {res.fun - cpl.fun:.2f}")


if __name__ == "__main__":
    main()
