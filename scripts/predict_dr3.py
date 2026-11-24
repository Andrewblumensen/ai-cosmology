"""ID-021: timestamped predictions for DESI's final (DR3 / Y5) BAO release.

Two hypotheses, both fitted to DESI DR2 BAO + Pantheon+ (no CMB):
  H_L: flat LCDM            H_D: flat CPL (evolving dark energy)
For each DESI bin we predict D/r_d under both and the expected final-survey error.

Error assumption (stated, approximate): DR2 is ~70% of the dark-time survey, so for
statistics-limited bins the final error is ~ DR2 error x sqrt(0.7) = 0.84x.

A second, model-free prediction for nested releases: if a DR2 residual is a
statistical fluctuation, the final release keeps only ~ (e_final/e_DR2)^2 = 0.7 of it;
if it is real it keeps all of it.

Writes docs/predictions/desi-final-bao.md. The git commit timestamp is the proof of priority.
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

SHRINK = np.sqrt(0.7)
bao, sn = DesiDR2BAO(), PantheonPlus()


def tot(p):
    try:
        bg = Background(p[0], w_cpl(p[2], p[3])) if len(p) == 4 else Background(p[0])
    except ValueError:
        return 1e10
    if len(p) == 4 and p[2] + p[3] >= 0:
        return 1e10
    return bao.chi2(bg, p[1]) + sn.chi2(bg)


def fit(x0):
    r = minimize(tot, x0, method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 60000, "adaptive": True})
    return minimize(tot, r.x, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-11, "maxiter": 60000, "adaptive": True})


def main():
    L = fit([0.31, 100.0])
    D = fit([0.31, 100.0, -0.89, -0.2])
    pL = bao.predict(Background(L.x[0]), L.x[1])
    pD = bao.predict(Background(D.x[0], w_cpl(D.x[2], D.x[3])), D.x[1])
    err = np.sqrt(np.diag(np.linalg.inv(bao.inv_cov)))
    ef = err * SHRINK
    rows = []
    for i, (z, k) in enumerate(zip(bao.z, bao.kind)):
        sep = abs(pD[i] - pL[i]) / ef[i]
        res = bao.value[i] - pL[i]
        rows.append((z, k.replace("_over_rs", "/r_d"), bao.value[i], err[i], pL[i], pD[i], ef[i], sep,
                     pL[i] + 0.7 * res, bao.value[i]))
    out = ROOT / "docs" / "predictions"
    out.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Predictions for DESI's final BAO release (ID-021)",
        "",
        "Committed before the release. Both models fitted to DESI DR2 BAO + Pantheon+ (no CMB).",
        f"- Flat ΛCDM: Ωm = {L.x[0]:.4f}, h·r_d = {L.x[1]:.2f} Mpc",
        f"- Flat CPL: Ωm = {D.x[0]:.4f}, h·r_d = {D.x[1]:.2f} Mpc, w0 = {D.x[2]:.3f}, wa = {D.x[3]:.3f}",
        "- Final-survey errors assumed = DR2 errors × 0.84 (DR2 ≈ 70% of the dark-time survey; approximate).",
        "",
        "**Model-separation columns:** how far apart the two models' predictions are, in units of the",
        "expected final error. **Fluctuation test:** for each bin, the value expected if the DR2",
        "residual from ΛCDM is a statistical fluctuation (it shrinks to ~70%), vs real (it stays).",
        "",
        "| z | Quantity | DR2 value ± err | ΛCDM pred. | CPL pred. | Final err (est.) | Separation (σ) | If fluctuation | If real |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for z, k, v, e, a, b, f, s, fl, rl in rows:
        lines.append(f"| {z:.3f} | {k} | {v:.3f} ± {e:.3f} | {a:.3f} | {b:.3f} | {f:.3f} | {s:.2f} | {fl:.3f} | {rl:.3f} |")
    best = sorted(rows, key=lambda r: -r[7])[:3]
    lines += ["", "Most discriminating bins: " + "; ".join(f"z={r[0]:.3f} {r[1]} ({r[7]:.2f}σ)" for r in best) + ".",
              "",
              "Honest limitation: without CMB, single bins separate the models by well under 1σ each;",
              "the discrimination comes from the combined pattern. A CMB-inclusive version should follow."]
    (out / "desi-final-bao.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
