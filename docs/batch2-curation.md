# Batch 2 (ID-036): curation record

Written 2026-11-24 (session 13), **before any batch-2 model was fitted to real data**. The rules
applied here were pre-registered in IDEAS.md (ID-036) before the harvest was read.

## Harvest

Eight agents, one per field cluster, wrote 83 ideas to `docs/batch2-harvest/*.md`. Each idea has
a cosmology story, a closed-form w(z) or ρ_DE(z), an impact note and a web-checked prior-art
search. 33 further "needs ODE" ideas are listed at the end of those files (not in this batch).

| Field cluster | Harvested | In catalogue | Marked known |
|---|---|---|---|
| Condensed matter / stat. phys. | 11 | 11 | 3 |
| Biology / ecology / epidemiology | 9 | 9 | 0 |
| Economics / control / networks | 10 | 10 | 1 |
| Information / thermodynamics / ML | 11 | 10 | 0 |
| Chemistry / nuclear / particle | 11 | 9 | 2 |
| Geoscience / fluids / materials | 11 | 9 | 1 |
| Pure math / quantum foundations | 10 | 10 | 2 |
| Signals / nonlinear dynamics | 10 | 8 | 1 |
| **Total** | **83** | **76** | **10** |

Parameter counts: 7 models with 2, 41 with 3, 28 with 4 parameters (plus 3 base parameters).

## Merges (exact duplicates, same family up to reparametrisation)

Kept entry ← merged entry; the kept entry's range was widened to cover both.

1. Log-periodic critical DE ← Efimov log-periodic DE (identical form; ω lo 0.5 → 0.3)
2. Log-periodic critical DE ← Log-periodic discrete-scale-invariance ring (A' = A/(1 + A cos φ)).
   The same log-periodic form was proposed independently by three harvesters.
3. Avrami-KWW vacuum conversion ← chemistry "Avrami-KWW vacuum conversion" (n_CM = 1.5 n; n lo 1 → 0.45)
4. Inverse-log granular compaction ← geoscience "Granular-compaction DE" (A = −D; A lo −0.9 → −0.95)
5. Percolation-Kuramoto order parameter ← geoscience "Percolation-onset DE" (same after
   normalising f(0) = 1; β hi 1.5 → 2.5)
6. Binomial-cascade singular DE ← signals "Binomial-cascade staircase" (same algorithm, depth 6 vs 12)
7. JMAK vacuum conversion in cosmic time ← signals "Glassy KWW relaxation clock"
   (A = −B/(1+B), τ rescaled by t0; n lo 0.5 → 0.2, B hi 5 → 9)

Near-relatives kept as separate tests (different variable, clock or observable): Landau exponent
(nested in Kibble-Zurek), Cole-Cole (nested in Havriliak-Negami), three Adler-equation models
(density in ln(1+z); density in cosmic time; w directly), two BKT models (switch-on at high z vs
low z), two Gompertz models (hazard in a vs in ln(1+z)), two Omori models, three staircases.

## Changes to harvested formulas (all before any fit)

- **Epidemic-threshold DE: bug fixed.** The harvest used the Lambert W branch −1, which returns
  the trivial root R∞ = 0 (division by zero). The principal branch gives the textbook SIR final
  size (R0 = 2.5 → 0.893). Caught by `tests/test_catalogue2.py`.
- **Start values moved to pass the sanity gate** (ranges unchanged):
  Ontogenetic growth k 0.3 → 0.2 and Epidemic threshold p 0.5 → 0.1 (birth redshift beyond
  z = 1100 at the start); Gompertz hazard in lookback e-folds γ 1.5 → 0.5 (density underflowed
  to 0 at high z).
- Name changes only where two fields used the same name for different models.

## Checks run (no data, no χ²)

- `tests/test_catalogue2.py`: names unique and new versus batch 1; ΛCDM limit reproduced for every
  model that claims one (E(z) and θ* to 1e-6); finite, positive DE density for 0 ≤ z ≤ 1300 at
  the start values; only `ValueError` (a rejected point) at 40 random points inside the ranges
  (also with numpy warnings turned into errors).
- Scorer's `effective_w` and pathology flag at the start values: no flags.
- Pipeline smoke test on **one ΛCDM mock** (never real data) for two models (Burgers N-wave,
  Lorentz resonance): fits run, ≈ 25 s each on one core.

## Cost of the next steps

- Leaderboard on real data (`scripts/run_catalogue2.py`): 78 fits, ≈ 5 min on 16 cores.
- Look-elsewhere (`scripts/catalogue2_lee.py 100`): 77 models × 100 mocks, ≈ 7–8 h on 16 cores.
  Needs the batch-1 file `runs/catalogue_lee_32models_100mocks.txt` (same seeds).
