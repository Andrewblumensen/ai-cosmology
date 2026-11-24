# Idea ledger

Every hypothesis, including failures. Never delete an entry: the counts are used to
correct significances for the look-elsewhere effect.

**Hypotheses tested on data or published numbers: 6** (ID-004, 005, 012, 016, 017, 018)
**Ideas screened against the literature only: 11** (table at the bottom)
**Open ideas waiting for a test: 8**

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

### ID-020 — Regression-to-the-mean monitor for every anomaly
- Status: proposed (high value, cheap)
- Origin: Claude (2026-11-24), generalising ID-016
- Idea: for each anomaly with several data releases (DESI DR1→DR2, CatWISE dipole
  versions, SH0ES releases, birefringence WMAP→Planck→ACT), compare how the signal
  changed with the change expected if the earlier best fit were true. Real effects
  keep pace with precision; flukes and release-specific systematics fade.
- If true, it would mean: an objective ranking of which anomalies behave like real
  signals. That decides where all later effort goes.
- Date: 2026-11-24

### ID-021 — Public prediction registry for DESI DR3 and Euclid
- Status: proposed
- Origin: Claude (2026-11-24)
- Idea: before the next data releases, commit to this repo the predictions each live
  hypothesis makes (e.g. DR3 BAO values and errors if DR2's CPL fit is true, vs ΛCDM).
  The git timestamp proves they came first.
- If true, it would mean: confirmed predictions carry far more weight than fits to
  existing data, especially from outside the field.
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

## Tested

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
| ID-015 | Dark matter–dark energy energy exchange makes phantom crossing only apparent | known | [Guedezounme+ 2026](https://arxiv.org/abs/2507.18274), many others |
| — | JWST bright galaxies need new cosmology | parked | ΛCDM fits with rising star-formation efficiency ([Prada+ 2026](https://arxiv.org/html/2604.18683v1)) |
| — | PTA amplitude needs new physics | parked | Largely resolved astrophysically ([Mingarelli+ 2026](https://arxiv.org/abs/2603.13643)) |
| — | Negative neutrino mass is excess lensing | known | [Craig+ 2024](https://arxiv.org/abs/2407.07878), [Green & Meyers 2025](https://arxiv.org/abs/2508.20999) |
| — | Local bulk flow / dipole explains acceleration | known, contested | [Rameez 2024](https://arxiv.org/abs/2411.14758) vs [Rubin & Heitlauf 2020](https://par.nsf.gov/servlets/purl/10273965) |
