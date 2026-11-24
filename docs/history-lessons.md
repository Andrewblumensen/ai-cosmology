# What history says about today's anomalies (2026-11-24)

Treating the history of physics and astronomy as data: how past tensions looked while
they were open, and how they ended. Classification of outcomes is mine; facts are
standard history unless linked.

## Past tensions and their resolutions

| Era | Anomaly | Resolution | Type |
| --- | --- | --- | --- |
| 1840s | Uranus orbit residuals | Unseen planet (Neptune) | new matter |
| 1859–1915 | Mercury perihelion excess (~43″/century) | General relativity ([summary](https://mathscholar.org/?p=832)) | new physics |
| 1860s–1910s | "Vulcan" (same anomaly, wrong fix) | Planet never existed | wrong mechanism |
| 1929–1952 | Universe younger than Earth (H0 ≈ 500) | Two Cepheid populations conflated ([AIP](https://history.aip.org/exhibits/cosmology/ideas/hubble-distance-double.htm)); further fix by Sandage 1958 | systematic (distance ladder) |
| 1933–1980 | Missing mass in clusters, flat rotation curves | Dark matter (~40 years to accept) | new physics |
| 1968–2001 | Solar neutrino deficit | Neutrino oscillations; experiment and solar model were both right | new physics |
| 1970s–1990s | H0 = 50 vs 100 (Sandage vs de Vaucouleurs) | Both camps had systematics; HST Key Project landed in between (~72) | systematics on both sides |
| 1990s | Globular clusters older than the universe | Hipparcos recalibration cut ~3 Gyr ([Chaboyer+ 1997](https://arxiv.org/pdf/astro-ph/9706128)) **and** Λ turned out to be real | **mixed** |
| 1985–1993 | 17 keV neutrino | Instrumental | systematic |
| 1998–2012 | Pioneer anomaly | Thermal recoil | systematic |
| 2010–2019 | Proton radius puzzle | Older e-p measurements were off | systematic |
| 2011 | OPERA faster-than-light neutrinos | Loose fibre connector | systematic |
| 2014 | BICEP2 primordial B-modes | Galactic dust | systematic (foreground) |
| 2015–2016 | 750 GeV diphoton bump | Went away with more data | fluctuation |
| 1998–present | DAMA annual modulation (8.9σ) | Not confirmed by same-target experiments ([What makes a discovery](https://arxiv.org/pdf/2312.00672)) | systematic (presumed) |
| 2001–2025 | Muon g−2 | Theory (lattice) prediction moved | theory error |
| 2018– | EDGES 21-cm depth | Disputed by later experiments | systematic (likely) |
| 2022–2025 | Parity-odd galaxy 4-point function | DESI DR1 consistent with zero | fluctuation / systematic |

**Rough base rate** (resolved cases above, my classification): new physics or new
matter 5, systematics or theory error 10, fluctuations 2, mixed 1. So roughly **one in
four to one in three** persistent anomalies turned out to be new physics. That is far
higher than "anomalies are always errors", and far lower than "this one is surely new physics".

## What separated the real ones

1. **Same effect size for decades while errors shrank** (Mercury 43″; solar ν deficit
   stable). Systematics usually shrank or moved.
2. **Several independent methods or teams saw it** (dark matter: dynamics, lensing, CMB).
   Systematics were usually tied to one instrument, method or calibration rung
   (OPERA, Pioneer, BICEP2 at one frequency, Hubble's Cepheids).
3. **A simple explanation predicted something new that was then seen** (GR → light
   bending; oscillations → SNO neutral-current rate).
4. **"Mixed" is real.** The 1990s age crisis was partly a calibration error and partly
   new physics. Recalibration removed the anomaly a year before supernovae revealed Λ
   anyway. An anomaly being explained away is not proof the underlying physics is standard.

## Two cross-field corrections to today's significances

- **Heavy tails.** Across 41,000 measurements, disagreements follow heavy-tailed
  (Student-t, often near-Cauchy) distributions, with 5σ disagreements up to 10⁵ times
  more frequent than Gaussian ([Bailey 2017](https://arxiv.org/abs/1612.00778)).
  Re-evaluated this way (ID-030), today's anomalies are worth roughly:

  | Anomaly | Quoted | errors ×1.5 | Student-t ν=5 | Student-t ν=3 |
  | --- | --- | --- | --- | --- |
  | H0 | 5.0σ | 3.3σ | 2.9σ | 2.4σ |
  | Birefringence | 3.8σ | 2.5σ | 2.5σ | 2.1σ |
  | Cosmic dipole | 3.5σ | 2.3σ | 2.4σ | 2.1σ |
  | Evolving DE | 3.3σ | 2.2σ | 2.3σ | 2.0σ |
  | CMB lensing excess | 2.7σ | 1.8σ | 2.0σ | 1.8σ |

- **Cosmology's own track record.** Before 2000, cosmological error bars were too small
  by ~2×; after 2000 they were roughly right
  ([Croft & Dailey 2011](https://arxiv.org/abs/1112.3108)). So the ×1.5 column is a fair
  middle estimate for 2020s results with new systematics.

## Scoring today's core anomalies on the historical features

| Anomaly | Stable while errors shrank? | Independent methods? | Single calibration rung? | Historical analogue |
| --- | --- | --- | --- | --- |
| Hubble tension | yes (ID-020) | partly: sound-horizon-free methods give ~69, between the camps | Cepheid/SN ladder is the strongest leg | H0 50 vs 100 (both camps partly wrong) and Baade 1952 (same rung) |
| Birefringence | yes (ID-020) | WMAP, Planck, ACT agree in sign | depends on Galactic dust modelling for calibration | BICEP2 (dust-dependent) — caution |
| Evolving DE | likely (ID-016, low power) | BAO+CMB alone 3.1σ; SNe amplify | SN low-z sample shared by all compilations | 1990s age crisis (mixed) |
| Cosmic dipole | method-dependent | radio + infrared agree on excess | number counts only; selection effects | Ellis–Baldwin debates; unresolved |
| CMB lensing excess | yes, across likelihoods | Planck, ACT lensing | CMB only | solar ν? (too early to say) |

**Reading:** no anomaly scores as clearly as Mercury or the solar neutrinos did. Evolving
DE matches the "mixed" age-crisis pattern best: calibration fixes shrink it, but the
independent BAO+CMB leg remains. H0 matches the "both camps partly wrong" pattern of
the 1970s–90s, which predicts a resolution between the camps (~69–70).

## The Baade lesson as a search rule (ID-031)

Baade's error was a **population-mixing** error: one class of standard candle was
secretly two classes, mixed differently in the calibrators than in the targets.
Where could that happen today?

- **SN Ia progenitor channels** (prompt vs delayed) whose mix changes with redshift.
  This is exactly the disputed "progenitor age bias" (Son+ 2025 vs Wiseman+ 2026, see
  IDEAS ID-009). History says this error class can be large; it should not be dismissed lightly.
- **Cepheid hosts vs Hubble-flow SN hosts** (metallicity, star-formation mix).
- **Quasar populations in dipole catalogues** (evolving spectral slopes and magnification bias).
