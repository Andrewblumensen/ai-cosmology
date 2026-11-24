import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aicosmo.sn import DATA_DIR, TABLE, radec_to_galactic  # noqa: E402


def test_galactic_conversion_cmb_dipole():
    # Planck CMB dipole: RA 167.942, Dec -6.944  ->  l 264.02, b 48.25
    l, b = radec_to_galactic(np.array([167.942]), np.array([-6.944]))
    assert l[0] == pytest.approx(264.02, abs=0.05)
    assert b[0] == pytest.approx(48.25, abs=0.05)


@pytest.mark.skipif(not (DATA_DIR / TABLE).exists(), reason="run scripts/download_data.py first")
def test_reboost_is_identity_for_cmb_frame():
    from aicosmo.sn import CMB_DIPOLE, PantheonPlus
    sn = PantheonPlus()
    z = sn.reboost(CMB_DIPOLE["v"], CMB_DIPOLE["l"], CMB_DIPOLE["b"])
    assert np.allclose(z, sn.z_hd)
