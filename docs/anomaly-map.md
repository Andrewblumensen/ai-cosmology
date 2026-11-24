# Anomaly map (status as of 2026-11-24)

What each anomaly is, how strong it is now, which way it is moving, and what it
shares with the others. Built from the literature on 2026-11-24; every row links
its source. Update rows in place as new results appear; keep the date column honest.

## The anomalies

| Anomaly | Current strength | Trend | Key source |
| --- | --- | --- | --- |
| **Evolving dark energy** (w0 > -1, wa < 0) | DESI DR2 + CMB 3.1σ; + SNe originally 2.8–4.2σ depending on SN sample. After SN recalibrations the samples **converge at 3.2–3.4σ** (Pantheon+ corrected 3.2σ, DES-Dovekie 3.4σ, Union3.1 3.4σ) | Converging: less sample-dependent, not gone | [DESI DR2](https://arxiv.org/abs/2503.14738), [DES-Dovekie](https://arxiv.org/abs/2511.07517), [Union3.1](https://arxiv.org/abs/2601.19424) |
| **Hubble tension** (local H0 ≈ 73 vs CMB ≈ 67–68) | SH0ES 73.17 ± 0.86; CCHP lower; JWST confirms HST Cepheid distances | Persistent; debate is now SH0ES vs CCHP methods | [SH0ES JWST](https://ui.adsabs.harvard.edu/abs/2025AAS...24631002B/abstract), [Local Distance Network 2026](https://www.aanda.org/articles/aa/full_html/2026/04/aa57993-25/aa57993-25.html) |
| **S8 tension** (less late-time clustering) | DES Y6 2.6σ along S8 but 1.8σ in full parameter space; KiDS-Legacy < 1σ; DES, KiDS and HSC are consistent with each other | Fading | [DES Y6](https://arxiv.org/abs/2601.14559), [S8 review 2026](https://arxiv.org/abs/2602.12238), [KiDS-Legacy](https://www.aanda.org/articles/aa/pdf/2025/11/aa54908-25.pdf) |
| **Negative neutrino mass** | Posterior peaks below zero when allowed; driven by excess CMB lensing plus the DESI/CMB H0·r_d mismatch | Robust across likelihoods | [Craig+ 2024](https://arxiv.org/abs/2407.07878), [Green & Meyers 2025](https://arxiv.org/abs/2508.20999) |
| **Cosmic dipole anomaly** (quasar/radio dipole ≈ 2× kinematic) | CatWISE 4.9σ originally; reassessments 3.3–3.6σ; clustering does not explain it | Reduced but persistent | [von Hausegger+ 2026](https://arxiv.org/abs/2510.23769), [Bashir+ 2025](https://arxiv.org/abs/2511.00822) |
| **Cosmic birefringence** (CMB polarisation rotated) | WMAP+Planck β = 0.34° ± 0.09°; ACT DR6 consistent, but ACT has unexplained systematics | Persistent, systematics-limited | [MPA 2026](https://www.mpa-garching.mpg.de/1137699/hl202602), [ACT DR6](https://journals.aps.org/prd/abstract/10.1103/pbc3-t52s) |
| **JWST bright galaxies at z > 10** | Abundance is real | Fading as a cosmology anomaly: ΛCDM fits with rising star-formation efficiency | [Prada+ 2026](https://arxiv.org/html/2604.18683v1) |
| **Little red dots / overmassive early black holes** | Black holes overmassive vs hosts at z > 4; LRDs vanish below z ≈ 3 | Active; mostly astrophysics | [LRD evolution 2026](https://arxiv.org/html/2606.02773) |
| **CMB lensing excess** (driver of "negative neutrino mass") | A_lens = 1.083 ± 0.032, 2.7σ | Persistent across likelihoods | [What's the matter with Σmν (2025)](https://arxiv.org/pdf/2503.14470) |
| **Radio background excess** (ARCADE 2) | > 5σ excess at 3–10 GHz; origin unknown | Persistent, unconnected to other anomalies so far | [Dev+ 2026](https://eprints.soton.ac.uk/506710/2/2509.03441v2.pdf) |
| **Primordial helium deficit** (EMPRESS) | ~3σ low (2022) → "mild 1–2σ" (2025) | Fading | [EMPRESS XV](https://arxiv.org/abs/2506.24050) |
| **Parity-odd galaxy 4-point function** | BOSS 2.9σ hint (2022) → DESI DR1 consistent with zero | Faded | [Philcox 2022](https://arxiv.org/abs/2206.04227), [DESI DR1 parity-odd](https://journals.aps.org/prd/abstract/10.1103/2dmd-hyt1) |
| **PTA nanohertz background amplitude** | A ≈ 2×10⁻¹⁵, at the high end of predictions | Largely resolved by new SMBH binary population models | [Mingarelli+ 2026](https://arxiv.org/abs/2603.13643) |

## Fading or real? (ID-020, ID-022)

| Anomaly | Verdict | Evidence |
| --- | --- | --- |
| Hubble tension | behaves like a real signal | Effect held at 5.6–5.8 km/s/Mpc as errors shrank (pulls -1.02, +0.22) |
| Birefringence | behaves like a real signal | 0.35 → 0.30 → 0.34°, pulls within ±0.7, significance up to ~3.8σ |
| Evolving dark energy | consistent with real, low-power test | DR1 → DR2 matched the Asimov expectation (ID-016) |
| S8 | fading | KiDS pull -4.4; DES/KiDS/HSC now mutually consistent |
| Cosmic dipole | method-dependent | 4.9σ → 3.3–3.6σ from re-analyses of the same data |
| Shared anomaly axis | not supported | 10 reported axes are consistent with random (p = 0.46) |
| Helium deficit, parity-odd LSS, JWST galaxies, PTA amplitude | fading or faded | see table above |

## How the anomalies are connected

Machine bookkeeping finding: the headline count overstates the number of
independent anomalies. Several share inputs or parameter directions.

- **Evolving dark energy and negative neutrino mass share a root.** Both draw on the
  2.3σ mismatch between DESI BAO geometry and the CMB in ΛCDM. Neutrino mass adds a
  second, separate ingredient (excess CMB lensing).
- **Evolving dark energy is amplified by supernovae, and the amplification is fragile.**
  DESI BAO supplies the geometric tension; SN calibration decides how big it looks
  ([review](https://arxiv.org/pdf/2606.21826)). Recalibration cut DES from 4.2σ to 3.2σ.
- **Inside DESI, the signal is localised.** LRG1 (z = 0.51) drove w0 > -1 in DR1. In
  DR2, LRG1 and ELG1 are the biggest outliers, and LRG2 (z = 0.706) has the greatest
  bearing on w0 > -1 ([Ó Colgáin+ 2026](https://arxiv.org/abs/2504.04417)). LRG1 disagrees with supernovae
  at the same redshift (reproduced here, ID-005).
- **DES is not a common node (ID-012, dead).** DES Y6, KiDS-Legacy and HSC are mutually
  consistent; the S8 gap is mild. The real shared ingredient of the SN compilations is
  the low-z sample (> 90% of DES-SN5YR low-z SNe are in Pantheon+), and after
  recalibration all compilations converge at 3.2–3.4σ for evolving DE.
- **Cosmic dipole and supernova cosmology are linked by the choice of rest frame.**
  Tested today (ID-004): the frame choice does not move w0, wa by more than 0.5σ.

## Characteristic redshifts

| Anomaly | Redshift range |
| --- | --- |
| Local H0 | z < 0.15 |
| DESI DE signal (LRG1-2, ELG1) | z ≈ 0.5–1.1 |
| w = -1 crossing in CPL fits | z ≈ 0.4 (tracks the pivot redshift, likely a parameterisation effect) |
| S8 weak lensing | z ≈ 0.3–1 |
| CMB lensing excess | z ≈ 1–3 (lensing kernel) |
| Little red dots disappear | z ≈ 3 |
| JWST bright-galaxy excess | z > 10 |
