import sys
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import quad

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aicosmo.background import Background, w_cpl  # noqa: E402


def test_lcdm_comoving_distance_matches_quad():
    om = 0.3
    bg = Background(om)
    exact = quad(lambda z: 1 / np.sqrt(om * (1 + z) ** 3 + 1 - om), 0, 2.0)[0]
    assert bg.chi(2.0) == pytest.approx(exact, rel=1e-6)


def test_cpl_reduces_to_lcdm():
    a, b = Background(0.3), Background(0.3, w_cpl(-1.0, 0.0))
    assert np.allclose(a.E(np.linspace(0, 2.5, 50)), b.E(np.linspace(0, 2.5, 50)))


def test_cpl_density_matches_closed_form():
    w0, wa, om = -0.8, -0.5, 0.3
    bg = Background(om, w_cpl(w0, wa))
    z = 1.5
    a = 1 / (1 + z)
    rho = a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
    assert bg.E(z) ** 2 == pytest.approx(om * (1 + z) ** 3 + (1 - om) * rho, rel=1e-6)


def test_unphysical_history_rejected():
    with pytest.raises(ValueError):
        Background(-0.5)  # negative matter density makes H^2 < 0 above z ~ 0.44
