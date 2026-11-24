# Literature check: has DESI DR2 already been re-scored across many models? (2026-11-24)

Purpose: decide whether ID-033 (re-score a catalogue of published models on DR2) is still
worth doing, and how to aim ID-034. Titles, dates and abstract claims below were checked
against the arXiv API. Body-level numbers (Δχ² per model) were **not** read and are marked
as such.

## Verdict

- **ID-033 as planned is already done by others.** Multi-parametrisation re-scorings on DR2
  exist, including one with the same compressed CMB likelihood we use. They agree: a
  two-parameter w(z) is enough, and most forms cross w = −1 near z ≈ 0.5.
- **Phantom crossing is the open question.** DESI: models without crossing are "disfavored,
  [but] cannot yet be ruled out". A thawing (w ≥ −1) form is reported as comparable to CPL.
- **Gap we can fill:** mock-calibrated significance. The papers below quote Gaussian σ,
  Δχ², AIC/BIC or Bayes factors. None of the abstracts mention calibrating against mocks in
  which the truth is ΛCDM *or a non-crossing model*. Absence from abstracts is not proof
  of absence; check full texts before claiming novelty.

## Re-scorings of many models on DESI DR2

| arXiv | First author, date | Models | Data | Abstract claim |
|---|---|---|---|---|
| 2503.14743 | Lodha (DESI), 2025-03 | Parametric + binned + GP + 3 physical classes incl. quintessence w ≥ −1 | DESI DR2 + Planck + 3 SN sets | Two-parameter w(z) suffices; "clear preference for models that feature a phantom crossing; alternatives lacking this feature are disfavored, [but] cannot yet be ruled out" |
| 2508.10514 | Chaudhary, 2025-08 | Logarithmic, Exponential, CPL, BA, JBP, Thawing, Mirage, GEDE | DESI DR2 + Pantheon+ / DES-Dovekie / Union3 + **CMB compressed likelihood** | All models land in w0 > −1, wa < 0; crossing near z ≈ 0.5 in most; Mirage "inconclusive-to-moderate"; Nσ ≈ 1.1–2.3 for late-time data alone |
| 2511.18657 | Malekjani, 2025-11 | wCDM, CPL, CPL⁺, CPL⁺⁺ (+ higher-order) | CMB + DESI + Pantheon+ / Union3 | Bayesian: CPL preferred over wCDM; higher-order extensions not supported |
| 2609.02910 | Mangang, 2026-07 | CPL, Wang, parabolic | Planck + ACT DR6, DESI DR2, Pantheon+, DES-SN5YR | Up to ~4σ frequentist preference; AIC/BIC comparison (Δχ² values not read) |
| 2512.07281 | Zhang, 2025-12 | ΛCDM, wCDM, w0wa, φCDM, interacting (ξ-index) | DESI DR2, Pantheon+, Planck + ACT with lensing | Bayesian comparison; persistent H0 tension; evidence for dynamical DE (details not read) |

## Phantom crossing

| arXiv | First author, date | Abstract claim |
|---|---|---|
| 2504.16337 | de Souza, 2025-04 | Background degeneracy between EoS parametrisations and quintessence makes the crossing ambiguous; non-phantom thawing EoS "performs comparably to CPL" (Δχ² not read) |
| 2510.14941 | Sánchez López, 2025-10 | Non-minimally coupled (Palatini) exponential quintessence; CMB+DESI+DESY5: log B = 5.52 vs ΛCDM; crossing in the effective w at 2–3σ |

## Symbolic regression

| arXiv | First author, date | Abstract claim |
|---|---|---|
| 2502.10506 | Sousa-Neto, 2025-02 (updated for DR2) | PySR reconstruction of w(z); DESI DR2 alone agrees with w = −1; SN combinations discussed (conclusion not read in full) |

## Leads not verified (from a search-snippet pass only)

2511.04610 (scalar-tensor reconstruction enabling crossing), 2604.08449 (fermion-coupled
quintessence giving an apparent crossing), 2509.15453 (CosmoGen evolutionary symbolic
regression), 2602.12870 (genetic-algorithm H(z) reconstruction, no DESI).
