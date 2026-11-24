"""ID-031a: does the host-mass brightness step in Pantheon+ evolve with redshift?
(pre-registered in IDEAS.md; a Baade-type population-mixing test)

m_b_corr already includes Pantheon+'s standard mass-step correction, so a residual
step that changes with z would indicate a population effect the standard correction misses.
"""

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aicosmo.background import Background  # noqa: E402
from aicosmo.bao import DesiDR2BAO  # noqa: E402
from aicosmo.sn import PantheonPlus  # noqa: E402

EDGES = [0.01, 0.1, 0.3, 0.6, 2.3]


def gls(X, y, Cinv):
    A = X.T @ Cinv @ X
    cov = np.linalg.inv(A)
    beta = cov @ (X.T @ Cinv @ y)
    return beta, cov


def main():
    sn, bao = PantheonPlus(), DesiDR2BAO()
    r = minimize(lambda p: bao.chi2(Background(p[0]), p[1]) + sn.chi2(Background(p[0])),
                 [0.31, 100.0], method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-9})
    bg = Background(r.x[0])
    resid = sn.m - 5 * np.log10((1 + sn.z_hel) * bg.chi(sn.z_hd))

    mass = sn.tab["HOST_LOGMASS"].astype(float)
    calib = sn.tab["IS_CALIBRATOR"].astype(int)
    ok = (mass > 5) & (calib == 0)
    idx = np.where(ok)[0]
    C = np.linalg.inv(sn.inv_cov)[np.ix_(idx, idx)]
    Cinv = np.linalg.inv(C)
    z, y, H = sn.z_hd[idx], resid[idx], (mass[idx] > 10).astype(float)
    print(f"Joint LCDM fit Om = {r.x[0]:.4f}; SNe with valid host mass (non-calibrators): {len(idx)}")

    nb = len(EDGES) - 1
    b = np.digitize(z, EDGES) - 1
    # (1) per-bin offsets and per-bin steps
    X = np.zeros((len(idx), 2 * nb))
    for k in range(nb):
        X[:, k] = (b == k)
        X[:, nb + k] = (b == k) * H
    beta, cov = gls(X, y, Cinv)
    print("\nPer-bin residual mass step s (high-mass minus low-mass, mag) and high-mass fraction:")
    for k in range(nb):
        sel = b == k
        print(f"  {EDGES[k]:.2f}-{EDGES[k+1]:.2f}  N={sel.sum():4d}  s = {beta[nb+k]:+.4f} +/- {np.sqrt(cov[nb+k, nb+k]):.4f}"
              f"   high-mass fraction = {H[sel].mean():.2f}")

    # (2) direct linear evolution of the step with z (per-bin offsets kept free)
    X2 = np.zeros((len(idx), nb + 2))
    for k in range(nb):
        X2[:, k] = (b == k)
    X2[:, nb] = H
    X2[:, nb + 1] = H * z
    beta2, cov2 = gls(X2, y, Cinv)
    s0, s1 = beta2[nb], beta2[nb + 1]
    e0, e1 = np.sqrt(cov2[nb, nb]), np.sqrt(cov2[nb + 1, nb + 1])
    print(f"\nStep evolution: s(z) = {s0:+.4f}(+/-{e0:.4f}) + {s1:+.4f}(+/-{e1:.4f}) * z   -> s1 at {s1/e1:+.2f} sigma")
    f_hi = H[z > 0.4].mean()
    print(f"Implied mean magnitude drift between z=0 and z=0.5: s1*0.5*f_high ~ {s1*0.5*f_hi:+.4f} mag "
          f"(+/- {e1*0.5*f_hi:.4f}); compare ~0.04 mag needed to matter for evolving DE")
    verdict = "evidence of an evolving population effect" if abs(s1 / e1) > 2 else "none"
    print(f"Verdict (pre-registered): {verdict}")


if __name__ == "__main__":
    main()
