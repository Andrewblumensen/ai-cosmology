# Idea ledger

Every hypothesis, including failures. Never delete an entry: the counts are used to
correct significances for the look-elsewhere effect.

**Hypotheses tested on data: 2** (ID-004, ID-005)
**Ideas screened against the literature only: 10** (table at the bottom)
**Open ideas waiting for a test: 7**

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

### ID-012 — DES as a common node behind two anomalies
- Status: proposed (top priority)
- Origin: Claude, cross-anomaly bookkeeping (2026-11-24)
- Idea: DES Y6 shows the S8 tension (2.4–2.7σ) while KiDS-Legacy does not (< 1σ). DES
  supernovae gave the strongest dark-energy signal until a photometric recalibration
  cut it from 4.2σ to 3.2σ. Test whether a shared DES-specific ingredient (photometric
  calibration, photo-z calibration, a shared external low-z sample) links them.
- If true, it would mean: two of the headline anomalies weaken together, and the
  remaining signal is cleaner. That re-ranks what theorists should explain.
- Pre-registered test: list every probe as DES / non-DES. Compare tension sizes per
  group using published numbers. Criterion: TBD before running.
- Data: published constraints (no heavy computation).
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
- Status: proposed
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

### ID-013 — Varying electron mass driven by the dark-energy field
- Status: proposed (prior-art check not yet done)
- Origin: Claude (2026-11-24)
- Idea: a varying electron mass at recombination is one of the better-ranked H0
  fixes. If the same scalar field is the evolving dark energy, its late-time motion
  must also vary m_e today, which atomic clocks and quasar spectra constrain. Check
  whether a single field can do both without breaking clock bounds.
- If true, it would mean: one field linking the H0 tension and evolving dark energy,
  with a lab-testable prediction.
- Date: 2026-11-24

## Tested

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
| ID-015 | Dark matter–dark energy energy exchange makes phantom crossing only apparent | known | [Guedezounme+ 2026](https://arxiv.org/abs/2507.18274), many others |
| — | JWST bright galaxies need new cosmology | parked | ΛCDM fits with rising star-formation efficiency ([Prada+ 2026](https://arxiv.org/html/2604.18683v1)) |
| — | PTA amplitude needs new physics | parked | Largely resolved astrophysically ([Mingarelli+ 2026](https://arxiv.org/abs/2603.13643)) |
| — | Negative neutrino mass is excess lensing | known | [Craig+ 2024](https://arxiv.org/abs/2407.07878), [Green & Meyers 2025](https://arxiv.org/abs/2508.20999) |
| — | Local bulk flow / dipole explains acceleration | known, contested | [Rameez 2024](https://arxiv.org/abs/2411.14758) vs [Rubin & Heitlauf 2020](https://par.nsf.gov/servlets/purl/10273965) |
