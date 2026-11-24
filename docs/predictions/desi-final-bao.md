# Predictions for DESI's final BAO release (ID-021)

Committed before the release. Both models fitted to DESI DR2 BAO + Pantheon+ (no CMB).
- Flat ΛCDM: Ωm = 0.3042, h·r_d = 101.01 Mpc
- Flat CPL: Ωm = 0.3052, h·r_d = 99.71 Mpc, w0 = -0.891, wa = -0.215
- Final-survey errors assumed = DR2 errors × 0.84 (DR2 ≈ 70% of the dark-time survey; approximate).

**Model-separation columns:** how far apart the two models' predictions are, in units of the
expected final error. **Fluctuation test:** for each bin, the value expected if the DR2
residual from ΛCDM is a statistical fluctuation (it shrinks to ~70%), vs real (it stays).

| z | Quantity | DR2 value ± err | ΛCDM pred. | CPL pred. | Final err (est.) | Separation (σ) | If fluctuation | If real |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.295 | DV/r_d | 7.942 ± 0.076 | 7.928 | 7.929 | 0.064 | 0.00 | 7.938 | 7.942 |
| 0.510 | DM/r_d | 13.588 ± 0.168 | 13.294 | 13.285 | 0.141 | 0.07 | 13.500 | 13.588 |
| 0.510 | DH/r_d | 21.863 ± 0.429 | 22.479 | 22.354 | 0.359 | 0.35 | 22.048 | 21.863 |
| 0.706 | DM/r_d | 17.351 ± 0.180 | 17.451 | 17.421 | 0.151 | 0.20 | 17.381 | 17.351 |
| 0.706 | DH/r_d | 19.455 ± 0.334 | 19.981 | 19.905 | 0.279 | 0.27 | 19.613 | 19.455 |
| 0.934 | DM/r_d | 21.576 ± 0.162 | 21.709 | 21.670 | 0.135 | 0.29 | 21.616 | 21.576 |
| 0.934 | DH/r_d | 17.641 ± 0.201 | 17.439 | 17.424 | 0.168 | 0.09 | 17.581 | 17.641 |
| 1.321 | DM/r_d | 27.601 ± 0.325 | 27.758 | 27.727 | 0.272 | 0.11 | 27.648 | 27.601 |
| 1.321 | DH/r_d | 14.176 ± 0.225 | 13.991 | 14.043 | 0.188 | 0.27 | 14.121 | 14.176 |
| 1.484 | DM/r_d | 30.512 ± 0.764 | 29.941 | 29.920 | 0.639 | 0.03 | 30.341 | 30.512 |
| 1.484 | DH/r_d | 12.817 ± 0.518 | 12.821 | 12.887 | 0.433 | 0.15 | 12.818 | 12.817 |
| 2.330 | DH/r_d | 8.632 ± 0.101 | 8.593 | 8.674 | 0.085 | 0.96 | 8.620 | 8.632 |
| 2.330 | DM/r_d | 38.989 ± 0.532 | 38.816 | 38.862 | 0.445 | 0.10 | 38.937 | 38.989 |

Most discriminating bins: z=2.330 DH/r_d (0.96σ); z=0.510 DH/r_d (0.35σ); z=0.934 DM/r_d (0.29σ).

Honest limitation: without CMB, single bins separate the models by well under 1σ each;
the discrimination comes from the combined pattern. A CMB-inclusive version should follow.
