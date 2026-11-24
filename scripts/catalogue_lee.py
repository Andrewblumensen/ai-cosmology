"""Look-elsewhere calibration for the idea-factory catalogue (ID-035 criterion 1).

Generate mocks from the best-fit w0wa model (truth = w0wa), score the whole catalogue on
each mock exactly as on the real data, and record T = -min over models of
Delta AIC(model - w0wa). The p-value of the real T is the fraction of mocks with T >= T_real.

Usage: python scripts/catalogue_lee.py [n_mocks]     (~1 h per 100 mocks on 16 cores)
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
    real = {i: score(m, DATA, errors=False, starts=4).aic for i, m in enumerate(MODELS)}
    t_real = t_stat(real)
    print(f"{len(CATALOGUE)} catalogue models; real T = {t_real:.2f}", flush=True)

    jobs = [(s, i) for s in range(n) for i in range(len(MODELS))]
    per_mock: dict[int, dict[int, float]] = defaultdict(dict)
    done = 0
    with Pool(min(16, os.cpu_count())) as pool:
        for seed, i, aic in pool.imap_unordered(one, jobs, chunksize=1):
            per_mock[seed][i] = aic
            if len(per_mock[seed]) == len(MODELS):
                done += 1
                if done % max(1, n // 20) == 0:
                    print(f"  {done}/{n} mocks done", flush=True)
    t_mocks = np.array([t_stat(per_mock[s]) for s in range(n)])
    out = ROOT / "runs" / f"catalogue_lee_{len(CATALOGUE)}models_{n}mocks.txt"
    out.parent.mkdir(exist_ok=True)
    np.savetxt(out, t_mocks, header=f"T on w0wa mocks; real T = {t_real:.4f}")
    p = (t_mocks >= t_real).mean()
    print(f"T on mocks: median {np.median(t_mocks):.2f}, 95% {np.quantile(t_mocks, 0.95):.2f}, "
          f"99% {np.quantile(t_mocks, 0.99):.2f}")
    print(f"real T = {t_real:.2f}; p = {p:.3f} ({(t_mocks >= t_real).sum()}/{n})  -> saved {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
