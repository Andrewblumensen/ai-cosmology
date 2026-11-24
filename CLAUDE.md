# CLAUDE.md — project instructions

This repo is a long-running, hobby-pace research project: using AI to search for
new ideas in cosmology, starting from public data. Sessions are short and context
is lost between them. **The repo is the memory.** If it is not written here, it
did not happen.

## Start of every session

1. Read `RESEARCH_LOG.md` (latest entries first) and `IDEAS.md`.
2. Check the "Next up" section at the top of `RESEARCH_LOG.md`.
3. Continue from there unless the user says otherwise.

## End of every session (non-negotiable)

1. Append a dated entry to `RESEARCH_LOG.md`: what was done, what was learned, what failed.
2. Update every idea touched in `IDEAS.md` (status, result, link to code or notebook).
3. Rewrite "Next up" in `RESEARCH_LOG.md` so a fresh session can start cold.
4. Commit.

## The user

- AI engineer with a master's in space engineering. Strong on ML and engineering.
  Not working in cosmology day to day: explain field-specific context briefly.
- Wants breadth: many unconventional, machine-generated ideas, not one niche result.
- Wants to be told plainly when something looks promising, and when it does not.

## Research rules

1. **Impact gate.** Before testing an idea, write in `IDEAS.md` what it would mean
   for cosmology if true. If the answer is "a small correction to a nuisance
   parameter", drop it or park it.
2. **Log every test, including failures.** The count of hypotheses tried is what
   lets us correct for the look-elsewhere effect. Never delete a failed idea.
3. **Pre-register.** Write the success criterion before running the test.
4. **Null tests.** Before a search result is called interesting, run the same
   search on mock ΛCDM data. How often it "finds" something on mocks is the false-alarm rate.
5. **Deterministic numbers.** LLMs propose; code computes. No number in a result comes from an LLM.
6. **Held-out data.** Where possible, search on one dataset and confirm on another
   (for example, search on Pantheon+ and confirm on DES-SN5YR).
7. **Data is not committed.** `data/` is gitignored; `scripts/download_data.py` fetches it.
8. **Every run longer than a few minutes must checkpoint.** Save each finished unit of work as it
   completes (`src/aicosmo/checkpoint.py`) and skip finished units on restart, so a shutdown loses
   at most the fits in flight. Never write results only at the end. (Session 13 lost a ~2 h
   mock run to a planned shutdown because of this.)

## Promise reports

When a result passes the null tests, write `docs/reports/YYYY-MM-DD-<slug>.md` and
tell the user. Use this format:

- **Rating:** noise / interesting / promising
- **What we found** (two sentences, plain language)
- **How unlikely by chance**, after correcting for everything tried (cite IDEAS.md counts)
- **What would kill it** (the test that could disprove it)
- **What it would mean if real**
- **Next step**

## Layout

- `src/aicosmo/` — library code (cosmology, likelihoods, search loop)
- `scripts/` — runnable entry points (data download, fits, searches)
- `tests/` — tests; `pytest` must pass before commit
- `docs/` — feasibility study notes, reports
- `data/` — downloaded data (gitignored)

## Feasibility study

The original study is a Claude doc:
https://claude.ai/artifact/STrQkf3Bsko7gsj7Svah4K
Summary: start with expansion-history model search (DESI DR2 BAO + SNe + compressed
CMB), cheap likelihoods in the search loop, full MCMC only for finalists.
