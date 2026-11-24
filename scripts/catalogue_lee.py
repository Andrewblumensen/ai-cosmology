"""Look-elsewhere calibration for the idea-factory catalogue (ID-035 criterion 1).

Generate mocks from the best-fit w0wa model (truth = w0wa), score the whole catalogue on
each mock exactly as on the real data, and record T = -min over models of
Delta AIC(model - w0wa). The p-value of the real T is the fraction of mocks with T >= T_real.

Usage: python scripts/catalogue_lee.py [n_mocks]     (~2 min per mock on 16 cores)

Crash-safe: every finished fit is saved to runs/catalogue_lee_<models>models_<n>mocks.ckpt.jsonl.
Re-running the same command after a shutdown skips everything already done.
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import sys  # noqa: E402
from collections import defaultdict  # noqa: E402
from multiprocessing import Pool  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aicosmo.catalogue import CATALOGUE  # noqa: E402
from aicosmo.checkpoint import Checkpoint  # noqa: E402
from aicosmo.mocks import fiducial_vectors, make_mock  # noqa: E402
from aicosmo.score import W0WA, Data, score  # noqa: E402

DATA = Data(cmb=True, sn=True)
FID = score(W0WA, DATA, errors=False)
VECTORS = fiducial_vectors(DATA, W0WA, FID.x)
MODELS = [W0WA] + CATALOGUE


def one(job: tuple[int, int]):
    seed, i = job
    mock = make_mock(DATA, VECTORS, np.random.default_rng(seed))
    m = MODELS[i]
    return seed, i, score(m, mock, errors=False, starts=4).aic


def t_stat(aic: dict[int, float]) -> float:
    return -min(aic[i] - aic[0] for i in range(1, len(MODELS)))


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    stem = f"catalogue_lee_{len(CATALOGUE)}models_{n}mocks"
    ck = Checkpoint(ROOT / "runs" / f"{stem}.ckpt.jsonl")

    if "real" not in ck:
        ck.add("real", [score(m, DATA, errors=False, starts=4).aic for m in MODELS])
    t_real = t_stat(dict(enumerate(ck["real"])))
    print(f"{len(CATALOGUE)} catalogue models; real T = {t_real:.2f}", flush=True)

    jobs = [(s, i) for s in range(n) for i in range(len(MODELS))]
    per_mock: dict[int, dict[int, float]] = defaultdict(dict)
    for s, i in jobs:
        if f"{s},{i}" in ck:
            per_mock[s][i] = ck[f"{s},{i}"]
    todo = [(s, i) for s, i in jobs if f"{s},{i}" not in ck]
    done = sum(len(per_mock[s]) == len(MODELS) for s in range(n))
    print(f"  resuming: {done}/{n} mocks complete, {len(todo)} fits to go", flush=True)

    with Pool(min(16, os.cpu_count())) as pool:
        for seed, i, aic in pool.imap_unordered(one, todo, chunksize=1):
            ck.add(f"{seed},{i}", aic)
            per_mock[seed][i] = aic
            if len(per_mock[seed]) == len(MODELS):
                done += 1
                if done % max(1, n // 20) == 0:
                    print(f"  {done}/{n} mocks done", flush=True)
    ck.close()
    t_mocks = np.array([t_stat(per_mock[s]) for s in range(n)])
    out = ROOT / "runs" / f"{stem}.txt"
    np.savetxt(out, t_mocks, header=f"T on w0wa mocks; real T = {t_real:.4f}")
    p = (t_mocks >= t_real).mean()
    print(f"T on mocks: median {np.median(t_mocks):.2f}, 95% {np.quantile(t_mocks, 0.95):.2f}, "
          f"99% {np.quantile(t_mocks, 0.99):.2f}")
    print(f"real T = {t_real:.2f}; p = {p:.3f} ({(t_mocks >= t_real).sum()}/{n})  -> saved {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
