# Research log

Newest entries first. Every session ends by updating "Next up".

## Next up

The user's direction (2026-11-24): research and unconventional cross-connections first;
heavy evaluator work later; validate mainly against published research; only small,
fast computations.

1. **ID-012 (DES as a common node).** Tabulate every DES vs non-DES probe result for
   S8 and dark energy from published papers. Pre-register a criterion first.
2. **ID-011 (sign-fingerprint matrix).** For each anomaly in docs/anomaly-map.md, write
   the required sign of change in H(z) bins, growth bins, r_d, lensing amplitude.
   Look for a consistent pattern.
3. **ID-013.** Prior-art check on varying electron mass + dark-energy field + atomic clocks.
4. **ID-010.** Turn "How the anomalies are connected" into an explicit graph.
5. Generate a fresh batch of 10+ unconventional ideas and triage them the same way.

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
