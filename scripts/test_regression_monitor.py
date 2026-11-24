"""ID-020: regression-to-the-mean monitor (criterion pre-registered in IDEAS.md).

pull = (D_new - D_old) / sqrt(e_old^2 - e_new^2) for nested releases.
D is the anomaly's effect size relative to the standard expectation.
"""

import numpy as np

PLANCK_H0 = 67.4          # Planck 2018 LCDM (as used by CCHP status report)
PLANCK_S8 = 0.832         # Planck 2018

# (label, effect, error); successive entries are nested releases
SERIES = {
    "H0 (SH0ES - Planck), km/s/Mpc": [
        ("Riess+ 2019 (R19)", 74.03 - PLANCK_H0, 1.42),
        ("Riess+ 2022 (R22)", 73.04 - PLANCK_H0, 1.04),
        ("SH0ES 2025 (HST+JWST)", 73.17 - PLANCK_H0, 0.86),
    ],
    "Birefringence beta, deg": [
        ("Minami & Komatsu 2020 (Planck PR3)", 0.35, 0.14),
        ("Diego-Palazuelos+ 2022 (Planck PR4)", 0.30, 0.11),
        ("Eskilt & Komatsu 2022 (WMAP+PR4)", 0.34, 0.09),
    ],
    "S8 deficit (Planck - KiDS)": [
        ("KiDS-1000 (2020)", PLANCK_S8 - 0.759, 0.0225),
        ("KiDS-Legacy (2025)", PLANCK_S8 - 0.815, 0.0185),
    ],
}


def verdict(p):
    return "fading" if p < -1 else ("growing" if p > 1 else "stable")


def main():
    for name, rel in SERIES.items():
        print(name)
        for (l0, d0, e0), (l1, d1, e1) in zip(rel, rel[1:]):
            denom = np.sqrt(max(e0 ** 2 - e1 ** 2, 1e-12))
            p = (d1 - d0) / denom
            print(f"  {l0} -> {l1}: effect {d0:.3f}+/-{e0:.3f} -> {d1:.3f}+/-{e1:.3f}  "
                  f"significance {d0/e0:.1f} -> {d1/e1:.1f} sigma  pull {p:+.2f}  [{verdict(p)}]")
        print()


if __name__ == "__main__":
    main()
