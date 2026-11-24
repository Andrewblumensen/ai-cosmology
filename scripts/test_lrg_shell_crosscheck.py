"""ID-005: is DESI's LRG distance anomaly (z ~ 0.5-0.7) also seen in supernovae?

DESI's evolving-dark-energy preference is driven mainly by the LRG1-2 tracers
(z_eff = 0.51, 0.706). If the deviation is a real feature of the distance-redshift
relation, supernovae at the same redshifts should show the same fractional distance
offset relative to a common LCDM fit. If they do not, a BAO-tracer-specific cause
(systematic or tracer physics) becomes more likely.

Pre-registered criterion: report the SN fractional-distance residual in the
z=0.4-0.6 and 0.6-0.8 bins vs the DESI LRG DM residuals, both relative to the joint
LCDM best fit with free offsets (h*r_d for BAO, M for SNe). "Same feature" if the
SN residual matches the LRG residual's sign and is within 1 sigma of it.
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

bao, sn = DesiDR2BAO(), PantheonPlus()


def joint(p):
    return bao.chi2(Background(p[0]), p[1]) + sn.chi2(Background(p[0]))


def main():
    res = minimize(joint, [0.31, 100.0], method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-9})
    om, hrd = res.x
    bg = Background(om)
    print(f"Joint LCDM fit (DESI DR2 BAO + Pantheon+): Om={om:.4f}, h*r_d={hrd:.2f}, chi2={res.fun:.1f}")

    # BAO fractional residuals
    pred = bao.predict(bg, hrd)
    err = np.sqrt(np.diag(np.linalg.inv(bao.inv_cov)))
    print("\nDESI DR2 residuals vs joint LCDM (fractional, data/model - 1):")
    for z, k, v, p, e in zip(bao.z, bao.kind, bao.value, pred, err):
        print(f"  z={z:5.3f} {k:11s} {v/p-1:+.4f} +/- {e/p:.4f}  ({(v-p)/e:+.2f} sig)")

    # SN fractional distance residuals with M profiled (generalised least squares)
    mu = 5 * np.log10((1 + sn.z_hel) * bg.chi(sn.z_hd))
    r = sn.m - mu
    M = (r @ sn._ones_inv) / sn._norm
    r = r - M
    print("\nPantheon+ binned residuals vs same model (fractional distance = dmu*ln10/5):")
    for lo, hi in [(0.01, 0.1), (0.1, 0.25), (0.25, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.2), (1.2, 2.3)]:
        sel = (sn.z_hd > lo) & (sn.z_hd <= hi)
        idx = np.where(sel)[0]
        Ci = np.linalg.inv(np.linalg.inv(sn.inv_cov)[np.ix_(idx, idx)])
        w = Ci.sum(axis=1)
        mean = (w @ r[idx]) / w.sum()
        sig = 1 / np.sqrt(w.sum())
        f = np.log(10) / 5
        print(f"  {lo:4.2f}<z<={hi:4.2f}  N={len(idx):4d}  dD/D = {mean*f:+.4f} +/- {sig*f:.4f}  ({mean/sig:+.2f} sig)")


if __name__ == "__main__":
    main()
