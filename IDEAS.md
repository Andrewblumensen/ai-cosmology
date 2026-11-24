# Idea ledger

Every hypothesis, including failures. Never delete an entry: the counts are used to
correct significances for the look-elsewhere effect.

**Hypotheses tested on data or published numbers: 15** (ID-004, 005, 012, 016, 017, 018, 020, 022, 024, 025, 029, 030, 032)
**Ideas screened against the literature only: 15** (table at the bottom)
**Open ideas waiting for a test: 11** (ID-001, 002, 003, 010, 011, 021, 026, 027, 031, 032, 034)

Status values: `proposed` · `parked` · `testing` · `dead` · `known` (prior art covers it) · `interesting` · `promising`

Held-out data: **DES-SN5YR / DES-Dovekie supernovae are reserved.** Never search on them;
use only to confirm a finalist. (Decided 2026-11-24.)

## Template

```
### ID-000 — <short name>
- Status:
- Origin: human / LLM (model, run id)
- Idea:
- If true, it would mean: (impact gate)
- Pre-registered test and success criterion:
- Data:
- Result:
- Code / notebook:
- Date:
```

## Open ideas (highest priority first)

### ID-035 — Idea factory, batch 1: score many expansion histories, mock-calibrated
- Status: testing (pre-registered 2026-11-24, session 12, before the full batch was scored)
- Origin: user + Claude. Catalogue = models harvested from 2025–26 DESI-era papers
  ("paper-new"), older alternatives to Λ ("paper-old"), and new ones from Claude ("llm-new");
  all in src/aicosmo/catalogue.py with sources.
- If true, it would mean: an expansion history with a physical story that the data prefer over
  w0wa, with a significance that survives the look-elsewhere effect over the whole catalogue.
- Honesty note: the 5 llm-new models were scored once (pipeline smoke test) *before* this entry
  was written. Smoke-test best: "tanh step in w", ΔAIC −2.07 vs w0wa. They stay in the
  catalogue and count as tests; the criterion below applies to them unchanged.
- **Pre-registered test.** Data: DESI DR2 BAO + CMB (θ*, ω_b, ω_bc) + Pantheon+. Per model:
  best fit (4 starts), ΔAIC vs w0wa. Catalogue statistic: T = −min over models of ΔAIC(model − w0wa).
  - *interesting*: a model with ΔAIC ≤ −2 vs w0wa.
  - *promising* needs all of: (1) look-elsewhere: T on the real data is exceeded in < 1% of
    ≥ 100 mocks generated from the best-fit w0wa (same catalogue, same fitting); (2) the
    model has a physical interpretation, not just a shape; (3) it keeps ΔAIC ≤ −2 when the held-out
    DES-SN5YR replaces Pantheon+ (only for a finalist, once).
  - Secondary (feeds ID-034): the best model with no crossing (w ≥ −1 for z ≤ 3) vs w0wa.
- Hypothesis count: every catalogue model counts as one test once scored.
- Code: scripts/run_catalogue.py → docs/catalogue-leaderboard.md
- Date: 2026-11-24

### ID-033 — Re-score the catalogue of published models on DESI DR2 (+ Pantheon+)
- Status: **known** for the catalogue part (session 11). Literature check
  (docs/literature-dr2-rescoring.md): DESI 2503.14743, Chaudhary 2508.10514 (8 forms, same
  compressed CMB), Malekjani 2511.18657, Mangang 2609.02910 already re-score many
  parametrisations on DR2; all find w0wa sufficient and crossing near z ≈ 0.5. Not run, so
  not counted as a test. The engine built for it is kept: scorer (session 10), generic model
  API `src/aicosmo/score.py` and mocks `src/aicosmo/mocks.py` (session 11), all validated.
  Remaining gap, moved to ID-034: mock-calibrated significance.
- Origin: Claude, from the Erdős-problems lesson (2026-11-24)
- Idea: many published dark-energy / H0-tension models were fitted only to pre-DESI
  data. Build a catalogue of models that have closed-form H(z) or w(z) (start from H0
  and DE review compilations), implement each, and score all of them on DESI DR2 BAO +
  Pantheon+ (later + compressed CMB) with an Occam penalty (AIC/BIC; evidence for finalists).
- If true, it would mean: forgotten models that beat w0wa with a physical theory behind
  them, i.e. leads that come with an interpretation. If none do, that is a strong
  statement about the model space.
- Pre-registered test and success criterion: to be written before scoring (which
  catalogue, penalty, threshold vs w0wa; look-elsewhere correction over the catalogue size).
- Data: DESI DR2 BAO, Pantheon+, compressed CMB (θ*, ω_b, ω_bc) (DES-SN5YR held out for finalists).
- Scorer caveat for the pre-registration: the compressed CMB lacks lensing, so Δχ²(w0wa − ΛCDM)
  for DESI+CMB+Pantheon+ is −7.6 with our scorer vs −10.7 with DESI's full CMB. The scorer is
  conservative by about 3 in χ²; thresholds must be set relative to our own w0wa value.
- Code: src/aicosmo/cosmology.py, cmb.py, fit.py; scripts/reproduce_desi_dr2.py;
  tests/test_cosmology_vs_camb.py, tests/test_desi_dr2_reproduction.py
- Date: 2026-11-24

### ID-034 — Evolutionary symbolic search over expansion histories, calibrated on mocks
- Status: proposed (after ID-033; reuses its scorer). Sharpened target (user + Claude,
  2026-11-24): can a physical model with no phantom crossing (w ≥ −1 at all z) fit as well as
  w0wa? Free-form search alone would mostly rediscover w0wa, since the data fix only 2–3 numbers of w(z).
  Literature (session 11): DESI says non-crossing models are "disfavored, but cannot yet be
  ruled out"; de Souza 2504.16337 says thawing is comparable to CPL. Nobody (in abstracts)
  calibrates this with mocks. Plan: fit the best non-crossing model, make mocks with it as the
  truth, and ask how often CPL then shows a crossing preference as large as in the real data.
  That gives a frequentist answer to "is the crossing real or a parametrisation artefact?".
- Origin: Claude, from the AlphaEvolve pattern; = the feasibility study's original plan
- Idea: evolve compact symbolic H(z)/w(z) forms with an LLM mutation step. Score with
  the likelihoods plus physicality constraints and a complexity penalty. Run the
  identical search on ΛCDM mocks to get the false-alarm distribution.
- If true, it would mean: a data-preferred expansion history no human wrote down, with a
  calibrated significance.
- Date: 2026-11-24

### ID-021 — Public prediction registry for DESI DR3 and Euclid
- Status: first entry committed: `docs/predictions/desi-final-bao.md` (no-CMB version;
  most discriminating bin: Lyman-α D_H at z = 2.33, 0.96σ). Next: a CMB-inclusive version.
- Origin: Claude (2026-11-24)
- Idea: before the next data releases, commit to this repo the predictions each live
  hypothesis makes (e.g. DR3 BAO values and errors if DR2's CPL fit is true, vs ΛCDM).
  The git timestamp proves they came first.
- If true, it would mean: confirmed predictions carry far more weight than fits to
  existing data, especially from outside the field.
- Date: 2026-11-24

### ID-010 — Anomaly dependency graph
- Status: proposed
- Origin: Claude (2026-11-24)
- Idea: build a graph whose nodes are anomalies and datasets, and whose edges are
  shared data, shared calibration, or shared parameter directions. Estimate the
  effective number of *independent* anomalies.
- If true, it would mean: a principled ranking of which anomalies are real
  independent evidence, and which mechanism has to explain how many.
- Pre-registered test: TBD. Start from docs/anomaly-map.md "How the anomalies are connected".
- Date: 2026-11-24

### ID-011 — Sign-fingerprint matrix
- Status: testing (first version: docs/sign-fingerprint.md). Already exposes two
  conflicts: evolving DE vs Hubble tension, and boosted-early / suppressed-late growth.
- Origin: Claude (2026-11-24)
- Idea: for each anomaly, write the sign of the change it needs in a few primitive
  quantities: H(z) in redshift bins, growth amplitude in bins, r_d, CMB lensing
  amplitude. Then find which sign patterns are mutually consistent. Example: the CMB
  lensing excess (more clustering at z ≈ 1–3) together with DES's low S8 (less
  clustering at z < 1) would require growth that is enhanced early and suppressed late.
- If true, it would mean: a target "shape" that any single new-physics mechanism must
  have. This is the input the automated theory search (ID-001) needs.
- Date: 2026-11-24

### ID-001 — Evolving dark energy search (baseline)
- Status: proposed (deferred; the user wants ideas first)
- Origin: human (feasibility study)
- Idea: LLM-driven evolutionary search over w(z) and scalar-field Lagrangians.
- If true, it would mean: a physical alternative to Λ that explains DESI.
- Date: 2026-11-24

### ID-002 — Cross-probe residual mining
- Status: proposed
- Origin: human (2026-11-24)
- Idea: search for structure shared between the residuals of different probes. ID-005
  is the first small instance of this.
- Date: 2026-11-24

### ID-003 — Automated ΛCDM consistency tests
- Status: proposed
- Origin: human (2026-11-24)
- Idea: generate many relations between observables that must hold in ΛCDM and test them all.
- Date: 2026-11-24

### ID-026 — Does the JWST bright-galaxy excess scale like a clustering-amplitude excess?
- Status: proposed (follows from ID-024)
- Origin: Claude (2026-11-24)
- Idea: an amplitude excess boosts halo abundance by a factor that grows with peak
  height ν in a specific way (d ln n / d ln σ ≈ aν² − 1 for Sheth–Tormen). Rising
  star-formation efficiency does not have to follow that pattern. Fit the JWST UV
  luminosity function excess versus mass and redshift to see which pattern it follows.
- If true, it would mean: JWST becomes the most sensitive probe of a few-percent
  amplitude anomaly, linking it to the CMB lensing excess (two epochs, one cause).
- Date: 2026-11-24

### ID-032 — Independent check of the timescape claim (ln B > 5 on Pantheon+)
- Status: **tested: does not reproduce on SNe; disfavoured when DESI BAO are added**
  (both pre-registered; see results below).
- Result (standard Pantheon+ likelihood, zHD): Δχ²(ΛCDM − timescape) = −5.13, −5.05,
  −2.06 for z_min = 0.01, 0.033, 0.075, i.e. ΛCDM fits better at every cut. Best-fit
  f_v0 = 0.86, 0.83, 0.79 (inside Wiltshire's published 0.76 +0.12/−0.09). ΛCDM Ωm = 0.332
  matches Pantheon+'s published value, validating the pipeline. Implementation check:
  low-z slope reproduces the dressed H0 of eq. B9 to 0.04%.
- Exploratory, NOT pre-registered and not counted: with zCMB (no peculiar-velocity
  corrections) or zHEL, timescape wins only at z_min = 0.01 (Δχ² +0.8 and +3.6);
  above z = 0.033 ΛCDM wins in every frame (−1.2 to −3.6). So any timescape preference
  lives in the lowest-redshift SNe, where velocity modelling dominates, which is the
  same place the published ln B shrinks (ln B > 5 overall → > 1 above z = 0.075).
- Caveats: Seifert+ use a light-curve-level Bayesian likelihood, not ours; Pantheon+
  bias corrections were simulated in ΛCDM, which could disadvantage alternatives.
  Next: add DESI BAO with timescape's own geometry (needs its sound-horizon treatment).
- **ID-032b pre-registration (2026-11-24, before fitting):** DESI DR2 BAO under
  timescape. Assumptions stated in advance: D_M = dressed comoving distance D(z);
  D_H = dD/dz; D_V = (z D_M² D_H)^(1/3); the sound horizon is free (absorbed in one
  scale parameter, as h·r_d is for ΛCDM), so each model has 2 free parameters on BAO
  alone and the same count jointly with Pantheon+ (M marginalised).
  (A) BAO alone, (B) BAO + Pantheon+ (zHD, z > 0.01). Δχ² = χ²(ΛCDM) − χ²(timescape).
  "Timescape favoured" if Δχ² ≥ 4 in both A and B; "timescape disfavoured" if
  Δχ² ≤ −4 in B; otherwise "inconclusive". (C) Robustness, reported but not used for
  the verdict: add a 1% systematic in quadrature to each BAO error (AP-scaling
  accuracy for non-fiducial models, Heinesen+ 2020).
- **ID-032b result: timescape disfavoured** (pre-registered rule). Δχ²(ΛCDM − TS):
  (A) BAO alone −4.6; (B) BAO + Pantheon+ **−29.0**. Robustness with +1% BAO systematic:
  −1.6 and −25.0. Cause: one void fraction cannot fit both probes. Supernovae want
  f_v0 ≈ 0.79–0.86, BAO want ≈ 0.69; the compromise fails both. Largest timescape pulls:
  Lyman-α D_H at z = 2.33 (−2.3σ) and D_H at z = 0.93 (+2.3σ). Caveats: the D_H = dD/dz
  mapping and DESI's ΛCDM-fiducial AP compression are assumptions; a full timescape
  BAO re-analysis of the galaxy correlation function could change the BAO-alone number,
  but a 25–29 Δχ² gap in the joint fit is large.
  Code: `scripts/test_timescape_bao.py`
- Code: `src/aicosmo/timescape.py`, `scripts/test_timescape.py` (`--explore` for frames)
- Origin: Claude (2026-11-24); idea lineage Einstein–Straus 1945 → Ellis 1984 → Buchert → Wiltshire
- Idea: timescape replaces dark energy with backreaction of inhomogeneities and claims
  very strong evidence over ΛCDM on Pantheon+, falling to ln B > 1 above z = 0.075
  ([Seifert+ 2025](https://arxiv.org/abs/2412.15143); [talk 2026](https://indico.global/event/16070/contributions/144489/)).
  Most of the preference therefore comes from low z, where peculiar-velocity
  modelling dominates. Implement timescape distances from the original papers, refit
  Pantheon+ with the standard likelihood and with z-cuts, then add DESI BAO.
- If true, it would mean: dark energy is (partly) an averaging artefact. Very high impact.
- **Pre-registered (2026-11-24, before any fit):** fit flat ΛCDM (free Ωm) and timescape
  (free void fraction f_v0) to Pantheon+ with the standard STAT+SYS covariance and M
  marginalised, in the CMB frame as published (zHD), for z_min = 0.01, 0.033, 0.075.
  Report Δχ² = χ²(ΛCDM) − χ²(timescape); both models have one free shape parameter, so
  Δχ² is a likelihood ratio. "Supports the claim" if Δχ² ≥ 4 at z_min = 0.075;
  "partially reproduces" if Δχ² ≥ 4 only at low z_min; "does not reproduce" otherwise.
  Also report the best-fit f_v0 against Wiltshire's published range.
  Caveat stated in advance: Seifert+ use a different (Bayesian, light-curve-level)
  likelihood, so disagreement does not by itself refute them.
- Date: 2026-11-24

### ID-031 — Baade-type population-mixing audit of today's standard candles
- Status: proposed
- Idea: list every place a "standard" population could be two populations mixed
  differently in calibrators vs targets (SN Ia progenitor channels vs z; Cepheid host
  types; quasar sub-populations in dipole catalogues), and check which are tested.
- If true, it would mean: a known historical error class (factor ~2 in 1952) applied
  systematically. Highest relevance: the disputed SN progenitor-age bias.
- Date: 2026-11-24
- **ID-031a pre-registration (2026-11-24, before computing):** Pantheon+ (z > 0.01,
  non-calibrators, HOST_LOGMASS valid), residuals from the joint DESI DR2 BAO + Pantheon+
  flat-ΛCDM fit, full STAT+SYS covariance. In redshift bins [0.01, 0.1), [0.1, 0.3),
  [0.3, 0.6), [0.6, 2.3) fit residual = a_bin + s_bin·[logM > 10] by generalised least
  squares. Then fit s(z) = s0 + s1·z across bins. "Evidence of an evolving
  population effect" if |s1| > 2σ; "none" otherwise. Also report how the high-mass
  fraction changes with z and the implied magnitude drift
  Δm(z) = s1·z·(high-mass fraction), compared with the ~0.04 mag needed to matter for DE.
- **ID-031a result: none.** Residual step s(z) = 0.007 + 0.030(±0.037)·z, slope 0.8σ;
  implied drift 0.006 ± 0.007 mag vs ~0.04 needed. Consistent with DES. Limitation: mass
  is only a proxy for age. Details: docs/baade-audit.md; code
  `scripts/test_mass_step_evolution.py`.

### ID-027 — Full SN × BAO residual correlation matrix
- Status: proposed (generalises ID-005; the engine for ID-002)
- Idea: for every redshift shell, compare SN and BAO residuals from a common fit,
  separately for transverse (D_M) and radial (D_H) BAO. A real geometric feature must
  appear in both; a tracer-specific systematic appears in one.
- Date: 2026-11-24

## Tested

### ID-029 — Dirac/Teller varying G behind both a SN brightness drift and the faint young Sun
- Status: **dead** (unless G varied in the past and froze recently)
- Result: SN drift of 0.04 mag over 5 Gyr needs |Ġ/G| ≈ 4.9×10⁻¹² /yr (6.7σ from
  LLR); the faint young Sun needs ≈ 2.5×10⁻¹² /yr (3.3σ). The only escape (G frozen today)
  runs against DESI's suggestion that the DE field is moving today.
- Code: `scripts/estimate_old_ideas.py`
- Date: 2026-11-24

### ID-030 — Today's tensions under empirically calibrated heavy-tailed errors
- Status: **tested** (cross-field: metrology / meta-science)
- Result: with errors ×1.5 or Student-t (ν = 3–10), every core anomaly falls to
  ~2–3.5σ; H0 stays strongest (2.4–3.5σ). None is decisive alone. See
  docs/history-lessons.md.
- Code: `scripts/estimate_old_ideas.py`
- Date: 2026-11-24

### ID-020 — Fading-or-real monitor
- Status: **tested** (criterion pre-registered and committed before collecting numbers)
- Result (pull per successive nested release; survey errors only):
  - H0 (SH0ES − Planck): R19 → R22 pull -1.02 (borderline fading), R22 → 2025 +0.22
    (stable). The effect has held near 5.6–5.8 km/s/Mpc while errors shrank.
  - Birefringence: PR3 → PR4 -0.58, PR4 → WMAP+PR4 +0.63. **Stable**; 0.34° held while
    the significance rose to ~3.8σ.
  - S8 (KiDS): KiDS-1000 → Legacy pull **-4.37, fading** (3.2σ → 0.9σ; includes
    methodology changes, which is the point).
  - DESI evolving DE: signal-like but low power (ID-016).
  - Cosmic dipole: not computable; the significance changes (4.9σ → 3.3–3.6σ) come
    from different methods on the same data, not from new data.
- Ranking for effort: H0 and birefringence behave most like real signals; evolving DE
  is consistent with real but untested at high power; S8 is fading.
- Code: `scripts/test_regression_monitor.py`
- Date: 2026-11-24

### ID-022 — Do the reported anomaly axes cluster on the sky?
- Status: **dead** (pre-registered)
- Result: all 10 axes: mean |cos| = 0.498 (isotropic expectation 0.500), p = 0.46.
  Without CMB-dipole-derived axes: p = 0.84. Leave-one-out p range 0.18–0.76. The
  2010 analysis that found ~0.8% chance alignment does not survive the updated axis
  list. A sub-group (CMB dipole, quadrupole, octopole, quasar polarisation, CatWISE)
  sits within ~30° of each other, the known "axis of evil" family, but that is a
  post-hoc observation and is not counted as evidence.
- Code: `scripts/test_anomaly_axes.py`
- Date: 2026-11-24

### ID-024 — How much would the CMB lensing excess boost JWST's early halos?
- Status: **tested (sizing)**; leads to ID-026
- Assumption: the lensing excess (A_lens = 1.083 ± 0.032) is a real ~4% amplitude
  excess, and it persists to z ≈ 10. The second part is a strong, model-dependent assumption.
- Result: halos hosting bright galaxies (10^10.5–10^11.5 M☉) become ×1.6–2.3 more
  common at z = 10 and ×1.9–3.2 at z = 12 (×1.3–2.1 for A_lens − 1σ). Same direction
  as the JWST excess, but not the whole of it, and a real high-z boost has to coexist
  with S8 not being high at z < 1 (the "boosted early, suppressed late" fingerprint).
- Code: `scripts/test_lensing_excess_jwst.py` (Eisenstein–Hu + Sheth–Tormen)
- Date: 2026-11-24

### ID-025 — Neutron-lifetime discrepancy explains the low primordial helium?
- Status: **dead**
- Result: δY_p/Y_p = 0.72 δτ_n/τ_n. The beam–bottle gap (~10 s of ~880 s) shifts Y_p by
  ~0.002, and the beam value moves it the wrong way. The EMPRESS deficit is ~0.008
  (approximate). Prior work already notes EMPRESS would need a much shorter lifetime
  ([2210.12031](https://arxiv.org/pdf/2210.12031)).
- Date: 2026-11-24

### ID-012 — DES as a common node behind two anomalies
- Status: **dead**
- Origin: Claude, cross-anomaly bookkeeping (2026-11-24)
- Idea: a DES-specific ingredient links the DES Y6 S8 tension and the strong DES
  supernova dark-energy signal.
- Pre-registration: not done. I read DES's own consistency statement before writing a
  criterion. Logged honestly; this counts as a tested hypothesis.
- Result: DES Y6, KiDS-Legacy and HSC Y3 are consistent with each other and with the
  CMB; DES Y6 differs from the CMB by 1.8σ in full parameter space (2.6σ along S8). On
  the SN side, the shared ingredient across compilations is the low-z sample, not DES;
  after recalibrations Pantheon+, DES-Dovekie and Union3.1 converge at 3.2–3.4σ.
  Sources: [DES Y6](https://arxiv.org/abs/2601.14559),
  [Union3.1](https://arxiv.org/abs/2601.19424),
  [Vincenzi+ comparison](https://arxiv.org/pdf/2501.06664).
- Date: 2026-11-24

### ID-016 — Did DESI's dark-energy signal grow from DR1 to DR2 like a real signal?
- Status: **tested: signal-like, but low power**
- Origin: Claude (2026-11-24)
- Pre-registered criterion: within 1σ of the Asimov expectation = signal-like.
- Data: DESI DR1 and DR2 BAO + Pantheon+ (no CMB).
- Result: Δχ²(ΛCDM − CPL) = 3.50 (DR1) → 4.86 (DR2). Expected for DR2 if DR1's best
  fit were true: 4.51 ± 4.25. Observed − expected = +0.08σ: signal-like. But the test
  barely discriminates (the expected spread is as large as the signal), and the best
  fit moved toward ΛCDM in wa (-0.48 → -0.22). Needs CMB to gain power.
- Code: `scripts/test_signal_growth_dr1_dr2.py`
- Date: 2026-11-24

### ID-017 — One axion for dark energy + birefringence + supernova dimming
- Status: **dead** (order-of-magnitude)
- Origin: Claude (2026-11-24)
- Idea: a single axion-like field is the evolving dark energy, rotates CMB polarisation
  (β = 0.34°), and dims supernovae by converting photons to axions in intergalactic
  magnetic fields. That would break the distance-duality relation and could explain
  the BAO–SN mismatch.
- Result: a dark-energy-sized field excursion (0.1–1 M_pl) needs g ≈ 5×10⁻²¹–5×10⁻²⁰ GeV⁻¹
  for the birefringence; that gives no measurable dimming. Dimming of ~0.04 mag needs
  g ≈ 3×10⁻¹² GeV⁻¹ with nG fields, above the Chandra bound of 6–8×10⁻¹³
  ([Reynolds+ 2020](https://arxiv.org/abs/1907.05475)). At the bound the dimming is
  only ~0.001 mag. Dead on both arms.
- Code: `scripts/estimate_quick_kills.py`
- Date: 2026-11-24

### ID-018 — Black-hole mass (LRDs, overmassive BHs) causes the CMB lensing excess
- Status: **dead** (order-of-magnitude)
- Result: Ω_BH ≈ 4×10⁻⁶, about 10⁻⁵ of all matter, and black holes sit inside
  existing halos. The lensing excess is a few-percent effect. Short by 3–4 orders of
  magnitude.
- Code: `scripts/estimate_quick_kills.py`
- Date: 2026-11-24

### ID-004 — Does the cosmic dipole anomaly leak into the dark-energy signal?
- Status: **dead**
- Origin: Claude (2026-11-24)
- Idea: if our velocity relative to distant matter is ~2× the CMB value (the quasar
  dipole anomaly), supernova redshifts are boosted into the wrong frame. Low-z SNe are
  unevenly spread on the sky, so the error might not cancel and could fake w0 > -1.
- If true, it would mean: two anomalies (dipole, evolving DE) explained by one frame error.
- Pre-registered criterion: "interesting" if any plausible frame shifts w0 or wa by
  > 0.5σ in a DESI DR2 BAO + Pantheon+ fit.
- Data: DESI DR2 BAO, Pantheon+ (1590 SNe, z > 0.01, STAT+SYS covariance).
- Result: baseline w0 = -0.891 ± 0.062, wa = -0.215 ± 0.425. Re-boosting to 800 km/s
  (CMB direction) shifts w0 by -0.42σ and wa by +0.26σ; 800 km/s toward the quasar
  dipole: < 0.1σ; 1000 km/s: -0.46σ / +0.25σ. All below threshold. Side result: the
  re-boosted fits are much worse (Δχ² = +173 to +454), so with Pantheon+'s
  peculiar-velocity model, low-z SNe strongly prefer the standard CMB frame. Caveat:
  those velocity corrections were built in the CMB frame, so this is a consistency check, not an independent test.
- Code: `scripts/test_dipole_frame_bias.py`
- Date: 2026-11-24

### ID-005 — Is DESI's LRG distance anomaly also in supernovae?
- Status: **known** (reproduces prior work)
- Origin: Claude (2026-11-24)
- Idea: if DESI's LRG deviation is real geometry, SNe at the same redshift should show it.
- Pre-registered criterion: "same feature" if the SN fractional-distance residual has
  the LRG DM residual's sign and lies within 1σ of it.
- Data: DESI DR2 BAO + Pantheon+, joint ΛCDM fit (Ωm = 0.3042).
- Result: z = 0.51: DESI D_M is +2.2% (+1.7σ) but SNe at 0.4–0.6 are -0.9% (-1.3σ):
  opposite sign, fails. z = 0.706: DESI D_M -0.6%, SNe -2.0%: same sign, within ~1σ.
  DESI's radial D_H is low at both LRG redshifts (-2.7%, -2.6%), and the SN shortfall is
  more consistent with that than with LRG1's D_M. Prior art already noted the LRG1-SN
  conflict ([Ó Colgáin+ 2024](https://arxiv.org/abs/2404.08633)).
- Code: `scripts/test_lrg_shell_crosscheck.py`
- Date: 2026-11-24

## Screened against the literature (not tested on data)

| ID | Idea | Verdict | Why |
| --- | --- | --- | --- |
| ID-006 | Primordial black holes from one small-scale power bump explain JWST galaxies, LRD black-hole seeds and the PTA signal | dead (Gaussian) / known (non-Gaussian) | CMB μ-distortion bounds rule out Gaussian seeds; non-Gaussian escapes are active work ([Balaji+ 2026](https://arxiv.org/pdf/2611.12861), [Dave+ 2026](https://arxiv.org/abs/2607.03138)) |
| ID-007 | Black holes as the source of dark energy (cosmological coupling) | known, contested | [Croker+ 2024](https://arxiv.org/abs/2405.12282) fits DESI; tensions with JWST AGN and LVK |
| ID-008 | One scalar field drives both evolving DE and CMB birefringence | known | e.g. [Barman & Girmohanta 2026](https://journals.aps.org/prd/pdf/10.1103/169s-4g17) |
| ID-009 | SN progenitor-age bias fakes evolving DE | known, disputed | [Son+ 2025](https://arxiv.org/pdf/2510.13121) vs [Wiseman+ 2026](https://arxiv.org/abs/2601.13785) |
| ID-014 | DE density "peaks" at z ≈ 0.4, near matter–DE equality: a physical feedback? | parked | Crossing sits at the CPL pivot redshift, likely a parameterisation effect ([2607.01226](https://arxiv.org/pdf/2607.01226)) |
| ID-013 | Varying electron mass + the dark-energy field together fix H0 and DESI | known | [Smith+ 2025](https://arxiv.org/abs/2510.21931): DE preference survives (≳2σ) with varying m_e; dilaton version in [2512.13544](https://arxiv.org/pdf/2512.13544v2) |
| ID-019 | The DM↔DE interaction that mimics DESI also fixes S8 | known, and problematic | It lowers S8 but suppresses fσ8 at z ≲ 0.8 against growth data ([Petri+ 2025](https://arxiv.org/abs/2508.17955)); S8 is fading anyway |
| ID-023 | Dark energy differs by hemisphere | known | Anisotropic DE improves Pantheon+ fits but violates the CMB quadrupole ([Battye & Moss 2026](https://arxiv.org/abs/2601.22351)) |
| ID-028 | Birefringence comes from the (DESI) dark-energy field: test with low-z sources | known; decisive tests are future | DE-type fields give a "universal" rotation profile mostly at z ≲ 10, while DM-type fields give ~0 at low z ([Naokawa 2025](https://arxiv.org/pdf/2504.06709)). Radio galaxies (~3000 now) need ~10⁵ sources to reach ~0.1° ([Battye+ 2026](https://arxiv.org/pdf/2607.02664)); LiteBIRD reionization tomography can rule out DE origin ([Nakatsuka+ 2022](https://arxiv.org/abs/2203.08560)) |
| ID-015 | Dark matter–dark energy energy exchange makes phantom crossing only apparent | known | [Guedezounme+ 2026](https://arxiv.org/abs/2507.18274), many others |
| — | JWST bright galaxies need new cosmology | parked | ΛCDM fits with rising star-formation efficiency ([Prada+ 2026](https://arxiv.org/html/2604.18683v1)) |
| — | PTA amplitude needs new physics | parked | Largely resolved astrophysically ([Mingarelli+ 2026](https://arxiv.org/abs/2603.13643)) |
| — | Negative neutrino mass is excess lensing | known | [Craig+ 2024](https://arxiv.org/abs/2407.07878), [Green & Meyers 2025](https://arxiv.org/abs/2508.20999) |
| — | Local bulk flow / dipole explains acceleration | known, contested | [Rameez 2024](https://arxiv.org/abs/2411.14758) vs [Rubin & Heitlauf 2020](https://par.nsf.gov/servlets/purl/10273965) |
| ID-033 | Re-score a catalogue of DE parametrisations on DESI DR2 | known | [Lodha+ 2025](https://arxiv.org/abs/2503.14743), [Chaudhary+ 2025](https://arxiv.org/abs/2508.10514), [Malekjani+ 2025](https://arxiv.org/abs/2511.18657); see docs/literature-dr2-rescoring.md |

## Archived open-idea entries (moved after testing; pre-registrations kept verbatim)

Pre-registration commits: ID-020 in 5e744c9, ID-022 in 26b2940.

### ID-020 — Regression-to-the-mean monitor for every anomaly
- Status: proposed (high value, cheap)
- Origin: Claude (2026-11-24), generalising ID-016
- Idea: for each anomaly with several data releases (DESI DR1→DR2, CatWISE dipole
  versions, SH0ES releases, birefringence WMAP→Planck→ACT), compare how the signal
  changed with the change expected if the earlier best fit were true. Real effects
  keep pace with precision; flukes and release-specific systematics fade.
- If true, it would mean: an objective ranking of which anomalies behave like real
  signals. That decides where all later effort goes.
- **Pre-registered criterion (written 2026-11-24, before collecting numbers):** for each
  pair of successive releases where the newer data include the older, let Δ be the
  anomaly's effect size (deviation from the standard expectation) with error e.
  pull = (Δ_new − Δ_old) / sqrt(e_old² − e_new²). "Fading" if pull < −1, "stable" if
  |pull| ≤ 1, "growing" if pull > 1. Where releases are independent rather than nested,
  use sqrt(e_old² + e_new²). Where only significances are published, use Δ/e = σ and
  report the result as indicative only.
- Date: 2026-11-24

### ID-022 — Do the reported anomaly axes cluster on the sky? (2026 update)
- Status: testing
- Origin: Claude (2026-11-24); updates [Antoniou & Perivolaropoulos 2010](https://arxiv.org/abs/1007.4347)
- Idea: many anomalies report a preferred direction. If they share one axis, a single
  cause (a super-horizon gradient, a tilted frame) is implied.
- If true, it would mean: evidence against statistical isotropy, the deepest
  assumption of ΛCDM.
- **Pre-registered (before computing):** fixed list of 10 axes, Galactic (l, b):
  CMB dipole (264.0, 48.3); CatWISE quasar dipole (238.2, 28.8); CMB hemispherical
  asymmetry (230, -16); CMB quadrupole (240, 63); CMB octopole (308, 63); quasar
  polarisation alignment (267, 69); fine-structure-constant dipole (330, -15);
  cluster H0 anisotropy (280, -15); Pantheon+ z<0.1 dipole (334.5, 16.0);
  Kashlinsky bulk flow (283, 11). Treated as sign-less axes. Statistic: mean pairwise
  |cos θ|; p-value from 10⁶ isotropic random sets. "Interesting" if p < 0.003 with all
  10 AND p < 0.003 with the CMB-dipole-derived items (CMB dipole, CatWISE) removed.
  Leave-one-out spread reported.
- Date: 2026-11-24

### ID-019 — Does the dark-sector interaction that fakes phantom crossing also fix or worsen S8?
- Status: proposed
- Origin: Claude, from the sign fingerprint (2026-11-24)
- Idea: fits that explain DESI with a dark matter–dark energy interaction find energy
  flowing DM→DE early and reversing later ([Guedezounme+ 2026](https://arxiv.org/abs/2507.18274)).
  That pattern implies a definite change in late-time growth. Check its sign against
  the clustering entries in docs/sign-fingerprint.md.
- If true, it would mean: a fast consistency check that could kill or support a whole
  model class.
- Date: 2026-11-24
