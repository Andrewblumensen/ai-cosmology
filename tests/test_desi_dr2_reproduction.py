"""Validation gate for the scoring engine: reproduce published DESI DR2 fits
(arXiv:2503.14738, Tables V-VI) with our Cosmology + compressed CMB prior.

Observed agreement (2026-11-24): parameters within 0.11 sigma, Delta chi2_MAP within 0.1.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from aicosmo.bao import DATA_DIR, MEAN_FILE  # noqa: E402
from aicosmo.sn import DATA_DIR as SN_DIR  # noqa: E402

pytestmark = pytest.mark.skipif(not (DATA_DIR / MEAN_FILE).exists() or not SN_DIR.exists(),
                                reason="run scripts/download_data.py first")


@pytest.mark.parametrize("name", ["LCDM DESI+BBN+theta*", "w0wa DESI",
                                  "w0wa DESI+Pantheon+", "w0wa DESI+CMBc"])
def test_reproduces_desi_dr2(name):
    from reproduce_desi_dr2 import PUBLISHED, run

    ours = run(name)
    for key, ref in PUBLISHED[name].items():
        mine = ours[key][0] if isinstance(ours[key], tuple) else ours[key]
        if isinstance(ref, tuple):
            assert abs(mine - ref[0]) < 0.25 * ref[1], key
        else:
            assert mine == pytest.approx(ref, abs=0.25), key
