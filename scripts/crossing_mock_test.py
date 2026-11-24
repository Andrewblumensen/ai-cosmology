"""ID-034 part A: is the phantom crossing real? (pre-registered in IDEAS.md, session 13)

For each non-crossing truth (T1 = Dutta-Scherrer/Linder thawing, T2 = running vacuum):
fit it to the real data, make N mocks from that best fit, and on every mock fit the truth,
LCDM and w0wa. Primary statistic S = chi2_min(truth) - chi2_min(w0wa); p = fraction of
mocks with S >= the real S.

Validation gate (checked first, printed before any p-value): chi2_min(truth) on its own
mocks must follow chi2(n - k): mean within 3 sigma of n - k and KS p > 0.01.

Usage: python scripts/crossing_mock_test.py [n_mocks] [T1|T2]   (default 500, both)
Writes runs/crossing_<truth>_<n>mocks.npz with every chi2 per mock and model.
Crash-safe: every finished mock goes to runs/crossing_<truth>_<n>mocks.ckpt.jsonl; re-running
the same command skips what is done.
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import sys  # noqa: E402
from multiprocessing import Pool  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aicosmo.catalogue import CATALOGUE  # noqa: E402
from aicosmo.checkpoint import Checkpoint  # noqa: E402
from aicosmo.mocks import fiducial_vectors, make_mock  # noqa: E402
from aicosmo.score import LCDM, W0WA, Data, score  # noqa: E402

TRUTHS = {"T1": "Dutta-Scherrer/Linder thawing", "T2": "Running vacuum (nu)"}
DATA = Data(cmb=True, sn=True)
STARTS = 4

# Filled per truth in main(); module-level so Pool workers (spawned on Windows) see them
# through the initializer.
_STATE: dict = {}


def _init(truth_key: str) -> None:
    truth = next(m for m in CATALOGUE if m.name == TRUTHS[truth_key])
    fid = score(truth, DATA, errors=False, starts=STARTS)
    _STATE.update(truth=truth, vectors=fiducial_vectors(DATA, truth, fid.x))


def one(seed: int):
    mock = make_mock(DATA, _STATE["vectors"], np.random.default_rng(seed))
    t = score(_STATE["truth"], mock, errors=False, starts=STARTS)
    lc = score(LCDM, mock, errors=False)
    cp = score(W0WA, mock, errors=False, starts=STARTS)
    return seed, t.chi2, t.k, lc.chi2, cp.chi2, cp.phantom_crossing, \
        cp.best["w0"], cp.best["wa"]


def run(truth_key: str, n: int) -> None:
    truth = next(m for m in CATALOGUE if m.name == TRUTHS[truth_key])
    real_t = score(truth, DATA, errors=False, starts=STARTS)
    real_lc = score(LCDM, DATA, errors=False)
    real_cp = score(W0WA, DATA, errors=False, starts=STARTS)
    s_real = real_t.chi2 - real_cp.chi2
    dchi2_real = real_lc.chi2 - real_cp.chi2
    print(f"[{truth_key}] {truth.name}: real S = {s_real:.2f}, "
          f"real dchi2(LCDM - w0wa) = {dchi2_real:.2f}", flush=True)

    ck = Checkpoint(ROOT / "runs" / f"crossing_{truth_key}_{n}mocks.ckpt.jsonl")
    rows = [tuple(ck[str(s)]) for s in range(n) if str(s) in ck]
    todo = [s for s in range(n) if str(s) not in ck]
    print(f"  resuming: {len(rows)}/{n} mocks done", flush=True)
    with Pool(min(16, os.cpu_count()), initializer=_init, initargs=(truth_key,)) as pool:
        for r in pool.imap_unordered(one, todo, chunksize=1):
            r = (int(r[0]), float(r[1]), int(r[2]), float(r[3]), float(r[4]), bool(r[5]),
                 float(r[6]), float(r[7]))
            ck.add(str(r[0]), list(r))
            rows.append(r)
            if len(rows) % max(1, n // 20) == 0:
                print(f"  {len(rows)}/{n} mocks done", flush=True)
    ck.close()
    rows.sort()
    seed, chi_t, k_t, chi_lc, chi_cp, cross, w0, wa = map(np.array, zip(*rows))

    out = ROOT / "runs" / f"crossing_{truth_key}_{n}mocks.npz"
    out.parent.mkdir(exist_ok=True)
    np.savez(out, seed=seed, chi2_truth=chi_t, chi2_lcdm=chi_lc, chi2_w0wa=chi_cp,
             w0wa_crosses=cross, w0=w0, wa=wa, s_real=s_real, dchi2_real=dchi2_real)

    # Validation gate first
    # The SN chi2 profiles out the absolute magnitude analytically: one more dof absorbed.
    dof = DATA.n_points - int(k_t[0]) - (1 if DATA.sn else 0)
    z_mean = (chi_t.mean() - dof) / (np.sqrt(2 * dof) / np.sqrt(n))
    ks = stats.kstest(chi_t, stats.chi2(dof).cdf).pvalue
    ok = abs(z_mean) < 3 and ks > 0.01
    print(f"  validation: mean chi2(truth) {chi_t.mean():.2f} vs dof {dof} "
          f"({z_mean:+.2f} sigma), KS p = {ks:.3f} -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("  Validation failed: no statistic is reported (pre-registered gate).")
        return

    s = chi_t - chi_cp
    p = (s >= s_real).mean()
    verdict = ("truth rejected (crossing not an artefact of it)" if p < 0.01 else
               "truth explains the w0wa preference" if p >= 0.05 else "inconclusive")
    sec = (cross & (chi_lc - chi_cp >= dchi2_real)).mean()
    print(f"  primary: p = {p:.3f} ({(s >= s_real).sum()}/{n}) -> {verdict}")
    print(f"  secondary: P(w0wa crosses and dchi2 >= {dchi2_real:.2f}) = {sec:.3f}; "
          f"mock w0 {np.median(w0):.3f} [real {real_cp.best['w0']:.3f}], "
          f"wa {np.median(wa):.3f} [real {real_cp.best['wa']:.3f}]")
    print(f"  saved {out.relative_to(ROOT)}")


def main() -> None:
    n = int(next((a for a in sys.argv[1:] if a.isdigit()), 500))
    keys = [a for a in sys.argv[1:] if a in TRUTHS] or list(TRUTHS)
    for k in keys:
        run(k, n)


if __name__ == "__main__":
    main()
