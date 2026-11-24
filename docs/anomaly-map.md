# Anomaly map (status as of 2026-11-24)

What each anomaly is, how strong it is now, which way it is moving, and what it
shares with the others. Built from the literature on 2026-11-24; every row links
its source. Update rows in place as new results appear; keep the date column honest.

## The anomalies

| Anomaly | Current strength | Trend | Key source |
| --- | --- | --- | --- |
| **Evolving dark energy** (w0 > -1, wa < 0) | DESI DR2 + CMB 3.1σ; + SNe 2.8–4.2σ depending on SN sample. With the recalibrated DES-Dovekie SNe: 3.2σ (was 4.2σ), "weak Bayesian preference" | Weakening as SN calibration improves | [DESI DR2](https://arxiv.org/abs/2503.14738), [DES-Dovekie](https://arxiv.org/abs/2511.07517) |
| **Hubble tension** (local H0 ≈ 73 vs CMB ≈ 67–68) | SH0ES 73.17 ± 0.86; CCHP lower; JWST confirms HST Cepheid distances | Persistent; debate is now SH0ES vs CCHP methods | [SH0ES JWST](https://ui.adsabs.harvard.edu/abs/2025AAS...24631002B/abstract), [Local Distance Network 2026](https://www.aanda.org/articles/aa/full_html/2026/04/aa57993-25/aa57993-25.html) |
| **S8 tension** (less late-time clustering) | Split: DES Y6 2.4–2.7σ; KiDS-Legacy < 1σ | Becoming survey-specific | [S8 review 2026](https://arxiv.org/abs/2602.12238), [KiDS-Legacy](https://www.aanda.org/articles/aa/pdf/2025/11/aa54908-25.pdf) |
| **Negative neutrino mass** | Posterior peaks below zero when allowed; driven by excess CMB lensing plus the DESI/CMB H0·r_d mismatch | Robust across likelihoods | [Craig+ 2024](https://arxiv.org/abs/2407.07878), [Green & Meyers 2025](https://arxiv.org/abs/2508.20999) |
| **Cosmic dipole anomaly** (quasar/radio dipole ≈ 2× kinematic) | CatWISE 4.9σ originally; reassessments 3.3–3.6σ; clustering does not explain it | Reduced but persistent | [von Hausegger+ 2026](https://arxiv.org/abs/2510.23769), [Bashir+ 2025](https://arxiv.org/abs/2511.00822) |
| **Cosmic birefringence** (CMB polarisation rotated) | WMAP+Planck β = 0.34° ± 0.09°; ACT DR6 consistent, but ACT has unexplained systematics | Persistent, systematics-limited | [MPA 2026](https://www.mpa-garching.mpg.de/1137699/hl202602), [ACT DR6](https://journals.aps.org/prd/abstract/10.1103/pbc3-t52s) |
| **JWST bright galaxies at z > 10** | Abundance is real | Fading as a cosmology anomaly: ΛCDM fits with rising star-formation efficiency | [Prada+ 2026](https://arxiv.org/html/2604.18683v1) |
| **Little red dots / overmassive early black holes** | Black holes overmassive vs hosts at z > 4; LRDs vanish below z ≈ 3 | Active; mostly astrophysics | [LRD evolution 2026](https://arxiv.org/html/2606.02773) |
| **PTA nanohertz background amplitude** | A ≈ 2×10⁻¹⁵, at the high end of predictions | Largely resolved by new SMBH binary population models | [Mingarelli+ 2026](https://arxiv.org/abs/2603.13643) |

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
- **DES is a common node.** DES Y6 shows the S8 tension while KiDS does not, and DES
  supernovae gave the strongest dark-energy signal before recalibration. A shared
  cause (photometric calibration, photo-z) is untested (ID-012).
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
