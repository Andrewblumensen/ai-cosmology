# Baade-type population-mixing audit (ID-031, 2026-11-24)

Walter Baade's 1952 correction doubled the distance scale because one "standard"
candle was secretly two populations, mixed differently in the calibrators than in the
targets. This audit lists where the same error class could hide today.

| Rung | Two populations? | Mixed differently where? | Status |
| --- | --- | --- | --- |
| SN Ia, cosmology (low-z vs high-z) | Prompt (young) vs delayed (old) progenitors; stretch distribution evolves with z ([Nicolas+ 2021](https://arxiv.org/abs/2005.09441)) | Young fraction rises with redshift | **Tested here (ID-031a): no standardised-brightness drift via the host-mass proxy.** Age-based version disputed (Son+ 2025 vs Wiseman+ 2026) |
| SN Ia, H0 (Cepheid hosts vs Hubble flow) | Same two populations | Cepheid calibrator hosts are star-forming by construction (young); Hubble-flow hosts are mixed ([Rigault+ 2015, via Nicolas+ 2021](https://arxiv.org/abs/2005.09441)) | Known and debated; SH0ES applies host corrections. Not tested here |
| Cepheids | Metallicity / host-type differences | Anchors (MW, LMC, NGC 4258) vs SN hosts | JWST ruled out crowding; metallicity term is fitted. Not tested here |
| Quasars in dipole catalogues | Sub-populations with different spectral slopes and magnification bias | Selection depends on flux and colour, which a moving observer changes | Partly modelled in dipole papers. Not tested here |

## ID-031a result (pre-registered)

Pantheon+ standardised magnitudes (which already include the standard mass-step
correction), residuals from the joint DESI DR2 BAO + Pantheon+ ΛCDM fit, full
covariance, 1578 SNe with host masses:

| Redshift | N | Residual mass step (mag) | High-mass fraction |
| --- | --- | --- | --- |
| 0.01–0.10 | 620 | +0.004 ± 0.014 | 0.56 |
| 0.10–0.30 | 466 | +0.013 ± 0.014 | 0.58 |
| 0.30–0.60 | 363 | +0.026 ± 0.016 | 0.52 |
| 0.60–2.30 | 129 | +0.022 ± 0.034 | 0.31 |

Step evolution s(z) = 0.007 + 0.030 z (slope ± 0.037, **0.8σ**). Implied mean drift from
z = 0 to 0.5: +0.006 ± 0.007 mag, against the ~0.04 mag needed to matter for evolving DE.
**Verdict: none.** This agrees with DES (−0.028 ± 0.034 mag per unit z, Wiseman+ 2026).

**Limitation:** host stellar mass is only a proxy for progenitor age. The age-bias claim
is precisely that the mass step misses the effect, so this does not settle the
Son-vs-Wiseman dispute; it does rule out a large drift that tracks host mass.
