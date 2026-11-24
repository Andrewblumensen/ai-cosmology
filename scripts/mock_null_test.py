"""Null test of the scorer on LCDM mocks: validates the mock machinery and gives the
false-alarm distribution of Delta chi2(w0wa - LCDM).

Expected if the machinery is right (Wilks' theorem):
- chi2_min(LCDM) on mocks follows chi2 with n - k dof (mean n - k);
- Delta chi2 = chi2_min(LCDM) - chi2_min(w0wa) follows chi2 with 2 dof (mean 2),
  slightly less where DESI's w0 + wa < 0 prior bites.

Usage: python scripts/mock_null_test.py [n_mocks] [--sn]
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import sys  # noqa: E402
from multiprocessing import Pool  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aicosmo.mocks import fiducial_vectors, make_mock  # noqa: E402
from aicosmo.score import LCDM, W0WA, Data, score  # noqa: E402

DATA = Data(cmb=True, sn="--sn" in sys.argv)
FID = score(LCDM, DATA, errors=False)
VECTORS = fiducial_vectors(DATA, LCDM, FID.x)


def one(seed: int) -> tuple[float, float]:
    mock = make_mock(DATA, VECTORS, np.random.default_rng(seed))
    lcdm = score(LCDM, mock, errors=False)
    w0wa = score(W0WA, mock, errors=False)
    return lcdm.chi2, lcdm.chi2 - w0wa.chi2


def main() -> None:
    n = int(next((a for a in sys.argv[1:] if a.isdigit()), 200))
    res = []
    with Pool(min(16, os.cpu_count())) as pool:
        for r in pool.imap_unordered(one, range(n)):
            res.append(r)
            if len(res) % max(1, n // 10) == 0:
                print(f"  {len(res)}/{n} mocks done", flush=True)
    res = np.array(res)
    chi2, dchi2 = res[:, 0], np.clip(res[:, 1], 0, None)
    dof = FID.n - FID.k
    real = FID.chi2 - score(W0WA, DATA, errors=False).chi2
    print(f"data: DESI DR2 BAO + CMBc{' + Pantheon+' if DATA.sn else ''}; {n} LCDM mocks")
    print(f"chi2_min(LCDM): mean {chi2.mean():.2f} +/- {chi2.std() / np.sqrt(n):.2f}  "
          f"(expect {dof}),  KS p vs chi2({dof}) = {stats.kstest(chi2, 'chi2', args=(dof,)).pvalue:.2f}")
    print(f"Delta chi2(w0wa): mean {dchi2.mean():.2f} +/- {dchi2.std() / np.sqrt(n):.2f}  (expect <= 2),  "
          f"KS p vs chi2(2) = {stats.kstest(dchi2, 'chi2', args=(2,)).pvalue:.2f}")
    print(f"real data Delta chi2 = {real:.2f}; fraction of mocks >= real: {(dchi2 >= real).mean():.4f} "
          f"(chi2(2) tail: {stats.chi2.sf(real, 2):.4f})")


if __name__ == "__main__":
    main()
