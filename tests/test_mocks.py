import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aicosmo.bao import DATA_DIR, MEAN_FILE  # noqa: E402

pytestmark = pytest.mark.skipif(not (DATA_DIR / MEAN_FILE).exists(),
                                reason="run scripts/download_data.py first")


def test_noise_free_mock_is_fitted_exactly_and_noise_has_right_scale():
    from aicosmo.mocks import fiducial_vectors, make_mock
    from aicosmo.score import LCDM, Data

    data = Data(cmb=True, sn=True)
    x = np.array([0.68, 0.0222, 0.142])
    vec = fiducial_vectors(data, LCDM, x)
    c, hrd = data.cosmology(x, LCDM.w_of([]))

    exact = make_mock(data, vec, np.random.default_rng(0))
    exact.bao.value, exact.cmb.mean, exact.sn.m = vec["bao"], vec["cmb"], vec["sn"] + 19.3
    assert exact.chi2(c, hrd) == pytest.approx(0, abs=1e-6)

    # Noise chi2 at the true parameters follows chi2(n): check the mean over draws
    draws = [make_mock(data, vec, np.random.default_rng(s)).chi2(c, hrd) for s in range(40)]
    n = data.n_points - 1  # SN offset is marginalised
    assert np.mean(draws) == pytest.approx(n, abs=4 * np.sqrt(2 * n / 40))
