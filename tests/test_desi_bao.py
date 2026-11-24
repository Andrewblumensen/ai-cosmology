"""Regression test: reproduce DESI DR2 BAO-only flat LCDM (arXiv:2503.14738, eq. 17).

Published: Omega_m = 0.2975 +/- 0.0086, h*r_d = 101.54 +/- 0.73 Mpc.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from aicosmo.bao import DATA_DIR, MEAN_FILE  # noqa: E402

pytestmark = pytest.mark.skipif(not (DATA_DIR / MEAN_FILE).exists(),
                                reason="run scripts/download_data.py first")


def test_reproduces_desi_dr2_lcdm():
    from aicosmo.bao import DesiDR2BAO
    from fit_lcdm_bao import fit_lcdm

    res, err = fit_lcdm(DesiDR2BAO())
    om, hrd = res.x
    # within 0.1 sigma of the published values
    assert abs(om - 0.2975) < 0.1 * 0.0086
    assert abs(hrd - 101.54) < 0.1 * 0.73
    assert err[0] == pytest.approx(0.0086, rel=0.1)
    assert err[1] == pytest.approx(0.73, rel=0.1)
