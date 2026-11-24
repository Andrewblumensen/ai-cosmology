# Research log

Newest entries first. Every session ends by updating "Next up".

## Next up

The user's direction (2026-11-24): research and unconventional cross-connections first;
heavy evaluator work later; validate mainly against published research; only small,
fast computations.

1. **Birefringence is now the most "real-behaving" anomaly with the fewest
   cross-connections.** Next batch: what else must a parity-violating photon coupling
   do (anisotropic birefringence, frequency independence, effect on CMB B-modes,
   galaxy polarisation)? Find a test no one has run. Pre-register first.
2. **ID-026.** Check whether the JWST UV-luminosity-function excess grows with peak
   height like an amplitude excess (needs published UVLF tables).
3. **ID-027.** Full SN × BAO residual matrix (transverse vs radial).
4. **ID-021.** CMB-inclusive DR3 predictions (needs a compressed CMB prior and
   radiation in background.py).
5. **ID-011.** Quantitative fingerprint (ΔH/H, Δσ8 per bin).

## 2026-11-24 (session 4) — Batch 3: fading-or-real, sky axes, cross-epoch, predictions

**Done (pre-registrations committed before data for ID-020 and ID-022)**
- ID-020 monitor: H0 and birefringence behave like real signals; S8 fading (pull -4.4);
  dipole significance changes are method-driven.
- ID-022: 10 reported anomaly axes are consistent with random (p = 0.46).
- ID-021: first prediction registry entry, `docs/predictions/desi-final-bao.md`.
- ID-024: lensing excess, if real and persistent to z ≈ 10, boosts JWST bright-galaxy
  halos ×1.6–2.3 (z = 10). Leads to ID-026.
- ID-025: neutron lifetime cannot explain low helium (dead).
- ID-019, ID-023: already published (interaction model breaks fσ8; anisotropic DE breaks
  the CMB quadrupole).
- Anomaly map: added lensing excess, radio background excess, helium, parity-odd LSS,
  and a fading-or-real table.

**Learned**
- The anomaly list is shrinking to a core: H0, birefringence, evolving DE (~3.2–3.4σ),
  CMB lensing excess, cosmic dipole. S8, helium, parity-odd LSS, JWST, PTA are fading.
- Birefringence is stable and under-connected: the best target for creative work next.
- The "more structure early, not late" pattern keeps reappearing (lensing excess,
  JWST direction, low S8 at z < 1), but each piece is individually weak.

## 2026-11-24 (session 3) — Idea batch 2: DES node, signal growth, quick kills

**Done**
- ID-012 (DES common node): dead. DES, KiDS, HSC agree; SN compilations converge at
  3.2–3.4σ for evolving DE after recalibration. Updated anomaly map accordingly.
- ID-016 (DR1→DR2 signal growth, Asimov test): signal-like but low power.
- ID-017 (one axion for DE + birefringence + SN dimming): dead by many orders.
- ID-018 (black holes cause CMB lensing excess): dead by 3–4 orders.
- ID-013 (varying m_e + DE): already published.
- First sign fingerprint: `docs/sign-fingerprint.md`.
- New open ideas: ID-019 (interaction growth sign), ID-020 (regression monitor),
  ID-021 (prediction registry).

**Learned**
- Evolving DE got *more* robust today in one sense: the SN samples now agree (3.2–3.4σ)
  instead of spanning 2.8–4.2σ. S8 is fading. The cosmic dipole and birefringence
  are the anomalies least explored by cross-connections, because no FLRW background
  change can touch them.
- Quick order-of-magnitude kills are cheap and effective; keep using them first.
- Process slip: ID-012 was not pre-registered before seeing the deciding number.

## 2026-11-24 (session 2) — Anomaly map, idea triage, two quick tests

**Done**
- Mapped 9 anomalies with current strength, trend and sources: `docs/anomaly-map.md`.
- Triaged 10 cross-connection ideas against the literature. Most obvious pairings are
  already published (black holes as DE, DE + birefringence, PBH seeds, interacting dark sector).
- Added a Pantheon+ likelihood (`src/aicosmo/sn.py`), with a Galactic-coordinate
  conversion and rest-frame re-boosting.
- Reserved DES-SN5YR / DES-Dovekie as held-out data (not downloaded).

**Results**
- ID-004 dead: re-boosting SN redshifts to an 800–1000 km/s "matter frame" moves w0, wa
  by < 0.5σ. Low-z SNe also strongly prefer the standard CMB frame (Δχ² +173 to +454).
- ID-005 known: DESI's LRG1 transverse distance (z = 0.51) disagrees in sign with
  Pantheon+ SNe at the same redshift. Already noted in the literature.
- Baseline DESI DR2 BAO + Pantheon+ (CPL): w0 = -0.891 ± 0.062, wa = -0.215 ± 0.425,
  i.e. a weak preference without CMB, consistent with DESI's reported range.

**Learned**
- The anomaly count overstates the number of independent anomalies. Evolving DE and
  negative neutrino mass share the DESI–CMB geometry mismatch; the DE signal is
  amplified by SN calibration; DES is a common node for two anomalies.
- Fading as cosmology anomalies: JWST bright galaxies, PTA amplitude. Strengthening
  or persistent: cosmic dipole, birefringence (systematics-limited), Hubble tension.
- The workspace can download GitHub-hosted data (Pantheon+ worked).

## 2026-11-24 — Project set up; DESI DR2 BAO reproduced

**Done**
- Wrote a feasibility study (Claude doc, linked in CLAUDE.md). Verdict: feasible as a
  hobby if the search loop uses cheap likelihoods; first target is expansion-history
  model search.
- Set up the repo: CLAUDE.md working rules, idea ledger, this log, data download script.
- Wrote a background cosmology module (flat, matter + arbitrary w(z), no radiation)
  and a DESI DR2 BAO likelihood (13 points, full covariance).

**Result**
- Flat LCDM fit to DESI DR2 BAO alone: Omega_m = 0.2975 +/- 0.0086,
  h*r_d = 101.54 +/- 0.74 Mpc, chi2 = 10.27 for 13 points.
  DESI's published values: 0.2975 +/- 0.0086 and 101.54 +/- 0.73 Mpc. Exact match.
  Locked in as `tests/test_desi_bao.py`.
- CPL (w0, wa) on BAO alone improves chi2 by 4.65 but is poorly constrained
  (best fit w0 = -0.18, wa = -2.72). Expected: BAO alone does not pin down dark energy;
  it needs CMB and SN. Not counted as a hypothesis test.

**Learned**
- The session workspace can fetch from GitHub but not most data archives. Large
  downloads (SN compilations, Planck) may need to run on the user's machine.
