"""Look-elsewhere calibration for batch 2 (ID-036 criterion 1), combined with batch 1.

Same mocks as scripts/catalogue_lee.py (truth = best-fit w0wa, seeds 0..n-1), so the
batch-1 statistic per mock can be reused: T_all[s] = max(T_batch1[s], T_batch2[s]),
T = -min over models of Delta AIC(model - w0wa). Saves every AIC per mock and model.

Usage: python scripts/catalogue2_lee.py [n_mocks]
Needs runs/catalogue_lee_32models_<n>mocks.txt from the batch-1 run.
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
from aicosmo.catalogue2 import CATALOGUE2  # noqa: E402
from aicosmo.mocks import fiducial_vectors, make_mock  # noqa: E402
from aicosmo.score import W0WA, Data, score  # noqa: E402

DATA = Data(cmb=True, sn=True)
FID = score(W0WA, DATA, errors=False)  # identical to catalogue_lee.py: same mocks per seed
VECTORS = fiducial_vectors(DATA, W0WA, FID.x)
MODELS = [W0WA] + CATALOGUE2


def _aic(m, d) -> float:
    try:
        return score(m, d, errors=False, starts=4).aic
    except Exception:
        return np.inf  # unfittable on this mock: cannot beat w0wa


def one(job: tuple[int, int]):
    seed, i = job
    mock = make_mock(DATA, VECTORS, np.random.default_rng(seed))
    return seed, i, _aic(MODELS[i], mock)


def t_stat(aic: np.ndarray) -> float:
    return -np.min(aic[1:] - aic[0])


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    b1 = ROOT / "runs" / f"catalogue_lee_{len(CATALOGUE)}models_{n}mocks.txt"
    t1_mocks = np.loadtxt(b1)
    t1_real = float(open(b1).readline().split("=")[1])
    real = np.array([_aic(m, DATA) for m in MODELS])
    t2_real = t_stat(real)
    t_real = max(t1_real, t2_real)
    print(f"{len(CATALOGUE2)} batch-2 models; real T: batch 1 {t1_real:.2f}, batch 2 {t2_real:.2f}, "
          f"all {t_real:.2f}", flush=True)

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
    aic = np.array([[per_mock[s][i] for i in range(len(MODELS))] for s in range(n)])
    t2_mocks = np.array([t_stat(a) for a in aic])
    t_all = np.maximum(t1_mocks, t2_mocks)
    out = ROOT / "runs" / f"catalogue2_lee_{len(CATALOGUE2)}models_{n}mocks.npz"
    out.parent.mkdir(exist_ok=True)
    np.savez(out, aic=aic, names=[m.name for m in MODELS], real_aic=real,
             t1_mocks=t1_mocks, t2_mocks=t2_mocks, t_all=t_all, t_real=t_real)
    for label, t, tr in (("batch 2", t2_mocks, t2_real), ("batch 1 + 2", t_all, t_real)):
        p = (t >= tr).mean()
        print(f"{label}: mocks median {np.median(t):.2f}, 95% {np.quantile(t, 0.95):.2f}, "
              f"99% {np.quantile(t, 0.99):.2f}; real {tr:.2f}; p = {p:.3f} ({(t >= tr).sum()}/{n})")
    print(f"saved {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
