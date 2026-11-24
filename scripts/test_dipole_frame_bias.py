"""ID-004: does the cosmic dipole anomaly leak into the dark-energy signal?

If the quasar/radio dipole excess means our velocity relative to distant matter is
~2x the CMB-inferred 370 km/s, then supernova redshifts are boosted into the wrong
rest frame. Low-z supernovae are not spread evenly on the sky, so a frame error does
not average out: it can shift low-z vs high-z distances and hence w0, wa.

Pre-registered criterion (written before running): the connection is "interesting"
if re-boosting to a plausible matter frame shifts w0 or wa by more than 0.5 sigma of
the DESI DR2 BAO + Pantheon+ fit. Otherwise the connection is dead.
"""

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aicosmo.background import Background, w_cpl  # noqa: E402
from aicosmo.bao import DesiDR2BAO  # noqa: E402
from aicosmo.sn import CMB_DIPOLE, PantheonPlus, unit  # noqa: E402

bao, sn = DesiDR2BAO(), PantheonPlus()


def total_chi2(p, z_sn):
    om, hrd, w0, wa = p
    if not (0.05 < om < 0.7 and w0 + wa < 0.0):
        return 1e10
    try:
        bg = Background(om, w_cpl(w0, wa))
    except ValueError:
        return 1e10
    return bao.chi2(bg, hrd) + sn.chi2(bg, z_sn)


def fit(z_sn, x0=(0.31, 100.0, -0.85, -0.6)):
    res = minimize(total_chi2, x0, args=(z_sn,), method="Nelder-Mead",
                   options={"xatol": 1e-7, "fatol": 1e-9, "maxiter": 40000, "adaptive": True})
    return minimize(total_chi2, res.x, args=(z_sn,), method="Nelder-Mead",
                    options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 40000, "adaptive": True})


def errors(p, z_sn):
    f = lambda x: total_chi2(x, z_sn)
    h = np.array([2e-3, 0.1, 1e-2, 4e-2])
    H = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            ei, ej = np.eye(4)[i] * h[i], np.eye(4)[j] * h[j]
            H[i, j] = (f(p + ei + ej) - f(p + ei - ej) - f(p - ei + ej) + f(p - ei - ej)) / (4 * h[i] * h[j])
    return np.sqrt(np.diag(np.linalg.inv(H / 2)))


def main():
    print(f"Pantheon+ SNe used (z > 0.01): {len(sn.z_hd)}")
    # How unevenly are low-z SNe spread relative to the dipole axes?
    low = sn.z_hd < 0.1
    for name, (l, b) in {"CMB dipole": (CMB_DIPOLE["l"], CMB_DIPOLE["b"]),
                         "CatWISE quasar dipole": (238.2, 28.8)}.items():
        cos = unit(sn.l, sn.b) @ unit(l, b)
        print(f"  mean cos(angle to {name}) for z<0.1 SNe: {cos[low].mean():+.3f}  "
              f"(1/z-weighted: {np.average(cos[low], weights=1/sn.z_hd[low]):+.3f})")

    base = fit(sn.z_hd)
    err = errors(base.x, sn.z_hd)
    print("\nBaseline DESI DR2 BAO + Pantheon+ (CPL):")
    print(f"  Om={base.x[0]:.4f}+/-{err[0]:.4f}  w0={base.x[2]:.3f}+/-{err[2]:.3f}  "
          f"wa={base.x[3]:.3f}+/-{err[3]:.3f}  chi2={base.fun:.2f}")

    scenarios = {
        "v=800 km/s, CMB direction": (800.0, CMB_DIPOLE["l"], CMB_DIPOLE["b"]),
        "v=800 km/s, quasar-dipole direction": (800.0, 238.2, 28.8),
        "v=1000 km/s, CMB direction (~2.7x, Dam+23)": (1000.0, CMB_DIPOLE["l"], CMB_DIPOLE["b"]),
        "v=0 (heliocentric-like, control)": (0.0, CMB_DIPOLE["l"], CMB_DIPOLE["b"]),
    }
    print("\nShifts when SN redshifts are re-boosted to another rest frame:")
    for name, (v, l, b) in scenarios.items():
        z_new = sn.reboost(v, l, b)
        r = fit(z_new, x0=base.x)
        d = r.x - base.x
        print(f"  {name:42s} dw0={d[2]:+.3f} ({d[2]/err[2]:+.2f} sig)  "
              f"dwa={d[3]:+.3f} ({d[3]/err[3]:+.2f} sig)  dOm={d[0]:+.4f}  dchi2={r.fun-base.fun:+.2f}")


if __name__ == "__main__":
    main()
