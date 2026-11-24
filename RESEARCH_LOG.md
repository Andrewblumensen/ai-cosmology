# Research log

Newest entries first. Every session ends by updating "Next up".

## Next up

1. Add a supernova likelihood (Pantheon+ first; DES-SN5YR and Union3 later as held-out
   data). Check public download URLs work from the user's machine.
2. Add compressed CMB priors (shift parameter R, acoustic scale l_A, omega_b). This
   needs radiation in `background.py`.
3. Reproduce DESI's BAO + CMB preference for w0wa over LCDM (3.1 sigma), then
   BAO + CMB + SN (2.8-4.2 sigma depending on the SN sample).
4. Then: pre-register ID-001 in IDEAS.md and wire the evaluator into OpenEvolve.

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
