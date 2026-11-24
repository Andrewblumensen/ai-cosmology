"""Old-literature track: two quick quantitative checks.

ID-029  Dirac/Teller varying G as one cause of two modern puzzles:
        (a) a supernova brightness drift that would inflate the evolving-DE signal,
        (b) the faint young Sun paradox (Sahni & Shtanov 2014: a ~1% higher G
            ~4 Gyr ago keeps early Earth warm, since L_sun ~ G^7).
        Compare the required |dG/dt|/G with lunar laser ranging (0.2 +/- 0.7)e-12 /yr.

ID-030  Heavy-tailed measurement errors (Bailey 2017; Croft & Dailey 2011):
        what are today's tensions worth if errors follow the empirically observed
        heavy-tailed distributions rather than a Gaussian?
"""

import numpy as np
from scipy import stats

LLR, LLR_ERR = 0.2e-12, 0.7e-12  # per year


def id029():
    print("ID-029: Dirac/Teller varying G")
    # (a) SN Ia: L ~ M_Ch ~ G^-1.5 (one common assumption)  -> dm = 1.63 dlnG
    dm, lookback = 0.04, 5e9          # ~0.04 mag offset needed between z~0 and z~0.5
    dlnG = dm / (2.5 * 1.5 / np.log(10))
    rate_sn = dlnG / lookback
    # (b) faint young Sun: ~1% higher G 4 Gyr ago (Sahni & Shtanov 2014)
    rate_fys = 0.01 / 4e9
    for name, r in [("SN brightness drift (0.04 mag over 5 Gyr)", rate_sn),
                    ("Faint young Sun (+1% G, 4 Gyr ago)", rate_fys)]:
        z = (r - abs(LLR)) / LLR_ERR
        print(f"  {name:44s} needs |dG/dt|/G ~ {r:.1e} /yr  -> {z:.1f} sigma from LLR (if the rate were constant)")
    print("  Both need a few x 1e-12 /yr; LLR allows < ~1.6e-12 (2 sigma) today. A common")
    print("  varying-G cause survives only if G varied in the past and froze recently, i.e.")
    print("  the opposite of a thawing field that DESI's w0 > -1 suggests is moving today.\n")


def id030():
    print("ID-030: tension significances under heavy-tailed error models")
    tensions = {
        "H0 (SH0ES vs Planck)": 5.0,
        "Birefringence (WMAP+Planck)": 3.8,
        "Evolving DE (DESI+CMB+SN)": 3.3,
        "Cosmic dipole (CatWISE, reassessed)": 3.5,
        "CMB lensing excess (A_lens)": 2.7,
    }
    models = [("Gaussian", None), ("errors x1.5", "scale"), ("Student-t nu=10", 10),
              ("Student-t nu=5", 5), ("Student-t nu=3", 3)]
    hdr = "  " + f"{'tension':38s}" + "".join(f"{m:>18s}" for m, _ in models)
    print(hdr)
    for name, z in tensions.items():
        row = []
        for _, m in models:
            if m is None:
                p = 2 * stats.norm.sf(z)
            elif m == "scale":
                p = 2 * stats.norm.sf(z / 1.5)
            else:
                p = 2 * stats.t.sf(z, m)
            row.append(f"{stats.norm.isf(p / 2):>17.1f}σ")
        print(f"  {name:38s}" + "".join(row))
    print("  (Gaussian-equivalent significance after re-evaluating the same z under each model.)")


if __name__ == "__main__":
    id029()
    id030()
