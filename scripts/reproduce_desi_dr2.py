"""Reproduce published DESI DR2 fits (arXiv:2503.14738) through the scoring engine.

This is the validation gate for src/aicosmo/score.py (ID-033 / ID-034): if these
numbers do not match DESI, nothing scored by the engine can be trusted.

We compute best fits (MAP) and Delta chi2_MAP = chi2(w0wa) - chi2(LCDM), and compare
with DESI's Tables V / VI. DESI quotes posterior means; for the strongly non-Gaussian
w0wa posteriors the MAP can sit a fraction of a sigma away from the mean.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aicosmo.score import LCDM, W0WA, Data, score  # noqa: E402

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

COMBOS = {
    "LCDM DESI+BBN+theta*": (dict(bbn=True, theta=True), LCDM),
    "w0wa DESI": (dict(), W0WA),
    "w0wa DESI+Pantheon+": (dict(sn=True), W0WA),
    "w0wa DESI+CMBc": (dict(cmb=True), W0WA),
    "w0wa DESI+CMBc+Pantheon+": (dict(cmb=True, sn=True), W0WA),
}


def run(name: str) -> dict:
    kwargs, model = COMBOS[name]
    data = Data(**kwargs)
    s = score(model, data)
    out = dict(s.best, chi2=s.chi2)
    if model is not LCDM:
        out["dchi2"] = s.chi2 - score(LCDM, data, errors=False).chi2
    return out


def main() -> None:
    for name in COMBOS:
        ours = run(name)
        ref = PUBLISHED.get(name) or INDICATIVE[name]
        tag = "" if name in PUBLISHED else "  (indicative: DESI used the full CMB likelihood)"
        print(f"\n{name}{tag}   chi2_min = {ours['chi2']:.2f}")
        for k, v in ref.items():
            if isinstance(v, tuple):
                print(f"  {k:8s} ours {ours[k]:9.4f}   DESI {v[0]:9.4f} +/- {v[1]:.4f}   "
                      f"diff {(ours[k] - v[0]) / v[1]:+.2f} sigma")
            else:
                print(f"  {k:8s} ours {ours[k]:9.2f}   DESI {v:9.2f}")


if __name__ == "__main__":
    main()
