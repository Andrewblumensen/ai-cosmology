# ai-cosmology

Using AI to generate and test unconventional ideas in cosmology, with public data.

The approach is an evolutionary search loop. An LLM proposes candidate models as
code; deterministic physics checks and fast likelihoods score them; only the
survivors get full MCMC analysis and null tests on mock data.

## Status

Phase 0: building and validating the evaluator. DESI DR2 BAO, Pantheon+ and the
compressed CMB prior (θ*, ω_b, ω_bc) are done and reproduce DESI DR2's published fits
(`scripts/reproduce_desi_dr2.py`). See `RESEARCH_LOG.md`.

## Quick start

```bash
pip install -r requirements.txt
python scripts/download_data.py      # fetches public likelihood data into data/
python scripts/fit_lcdm_bao.py       # flat ΛCDM fit to DESI DR2 BAO
python scripts/reproduce_desi_dr2.py # ΛCDM / w0wa fits vs DESI DR2 published values
pytest
```

## How this project works

- `IDEAS.md` — every hypothesis ever tested, with its result. Failures stay.
- `RESEARCH_LOG.md` — dated log, newest first, with a "Next up" section.
- `CLAUDE.md` — working rules for AI sessions (impact gate, null tests, logging).

## Data sources

| Data | Source |
| --- | --- |
| DESI DR2 BAO | [CobayaSampler/bao_data](https://github.com/CobayaSampler/bao_data), paper [arXiv:2503.14738](https://arxiv.org/abs/2503.14738) |
| Pantheon+ SNe | [PantheonPlusSH0ES/DataRelease](https://github.com/PantheonPlusSH0ES/DataRelease), paper [arXiv:2202.04077](https://arxiv.org/abs/2202.04077) |
| CMB (θ*, ω_b, ω_bc) prior | DESI DR2 Appendix A (from Lemos & Lewis CamSpec compression); hard-coded in `src/aicosmo/cmb.py` |
| z*, r*, r_d | [CAMB](https://camb.info) table, `scripts/build_early_table.py` → `src/aicosmo/early_table.txt` |
