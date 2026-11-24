# ai-cosmology

Using AI to generate and test unconventional ideas in cosmology, with public data.

The approach is an evolutionary search loop. An LLM proposes candidate models as
code; deterministic physics checks and fast likelihoods score them; only the
survivors get full MCMC analysis and null tests on mock data.

## Status

Phase 0: building and validating the evaluator (DESI DR2 BAO done; supernovae and
compressed CMB next). See `RESEARCH_LOG.md`.

## Quick start

```bash
pip install -r requirements.txt
python scripts/download_data.py      # fetches public likelihood data into data/
python scripts/fit_lcdm_bao.py       # flat ΛCDM fit to DESI DR2 BAO
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
