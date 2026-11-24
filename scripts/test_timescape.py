"""ID-032: independent check of the timescape-vs-LCDM supernova claim (pre-registered).

Standard Pantheon+ likelihood (STAT+SYS, M marginalised, zHD), one free shape parameter
per model: Omega_m (flat LCDM) vs void fraction f_v0 (timescape tracker solution).
"""

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aicosmo.background import Background  # noqa: E402
from aicosmo.sn import PantheonPlus  # noqa: E402
from aicosmo.timescape import Timescape  # noqa: E402


def best(fun, lo, hi):
    grid = np.linspace(lo, hi, 41)
    vals = [fun(x) for x in grid]
    i = int(np.argmin(vals))
    a, b = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    r = minimize_scalar(fun, bounds=(a, b), method="bounded", options={"xatol": 1e-5})
    return r.x, r.fun


def main():
    print(f"{'z_min':>6s} {'N':>5s} {'Om (LCDM)':>10s} {'chi2 LCDM':>10s} {'f_v0 (TS)':>10s} {'chi2 TS':>10s} {'dchi2 (L-TS)':>13s}")
    results = {}
    for zmin in (0.01, 0.033, 0.075):
        sn = PantheonPlus(z_min=zmin)
        om, cl = best(lambda o: sn.chi2(Background(o)), 0.05, 0.7)
        fv, ct = best(lambda f: sn.chi2(Timescape(f, n=1500)), 0.05, 0.95)
        results[zmin] = cl - ct
        print(f"{zmin:6.3f} {len(sn.z_hd):5d} {om:10.4f} {cl:10.2f} {fv:10.3f} {ct:10.2f} {cl - ct:13.2f}")
    d = results[0.075]
    if d >= 4:
        verdict = "supports the claim"
    elif any(v >= 4 for v in results.values()):
        verdict = "partially reproduces (low z only)"
    else:
        verdict = "does not reproduce"
    print(f"\nVerdict (pre-registered): {verdict}")
    print("Published timescape range (Wiltshire 2009, older SN data): f_v0 = 0.76 +0.12/-0.09")


if __name__ == "__main__":
    main()


def exploratory_frames():
    """NOT pre-registered: sensitivity to the redshift frame. Timescape proponents
    argue against FLRW-based peculiar-velocity corrections, so try zCMB (boost only,
    no PV corrections) and zHEL (no corrections at all)."""
    print("\nExploratory (not pre-registered): redshift-frame sensitivity")
    for col in ("zCMB", "zHEL"):
        for zmin in (0.01, 0.033, 0.075):
            sn = PantheonPlus(z_min=zmin)
            z = sn.tab[col].astype(float)
            from aicosmo.background import Background as B
            om, cl = best(lambda o: sn.chi2(B(o), z), 0.05, 0.7)
            fv, ct = best(lambda f: sn.chi2(Timescape(f, n=1500), z), 0.05, 0.95)
            print(f"  {col:5s} z_min={zmin:5.3f}  LCDM chi2={cl:8.2f} (Om={om:.3f})  TS chi2={ct:8.2f} (f_v0={fv:.3f})  dchi2(L-TS)={cl-ct:+6.2f}")


if __name__ == "__main__" and "--explore" in sys.argv:
    exploratory_frames()
