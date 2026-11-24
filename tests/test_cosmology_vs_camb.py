"""Our fast Cosmology must match CAMB (the code behind DESI DR2 and the CMB compression).

Tolerance: theta_* to 1e-5 relative (~0.1 sigma of the DESI CMB prior); E, distances and
r_d to 1e-5. Observed agreement is ~1e-7.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

camb = pytest.importorskip("camb")
from camb.dark_energy import DarkEnergyPPF  # noqa: E402

from aicosmo.background import w_cpl  # noqa: E402
from aicosmo.cosmology import C_KM_S, Cosmology  # noqa: E402

MODELS = [  # h, omega_b, omega_bc, w0, wa
    (0.675, 0.0222, 0.142, -1.0, 0.0),
    (0.637, 0.0223, 0.1425, -0.43, -1.72),  # DESI+CMB w0wa best fit region
    (0.70, 0.0215, 0.150, -1.15, 0.3),      # phantom today
    (0.62, 0.0232, 0.133, -0.6, -1.9),
]
ZS = np.array([0.1, 0.51, 1.0, 2.33, 10.0, 300.0, 1000.0])


@pytest.mark.parametrize("h, wb, wbc, w0, wa", MODELS)
def test_matches_camb(h, wb, wbc, w0, wa):
    p = camb.set_params(H0=100 * h, ombh2=wb, omch2=wbc - wb, mnu=0.06, nnu=3.044,
                        num_massive_neutrinos=1)
    p.DarkEnergy = DarkEnergyPPF(w=w0, wa=wa)
    ref = camb.get_background(p)
    derived = ref.get_derived_params()
    c = Cosmology(h, wb, wbc, w_cpl(w0, wa))

    assert np.allclose(c.E(ZS), ref.hubble_parameter(ZS) / (100 * h), rtol=1e-5, atol=0)
    assert np.allclose(c.chi(ZS) * C_KM_S / (100 * h), ref.comoving_radial_distance(ZS), rtol=1e-5)
    assert 100 * c.theta_star == pytest.approx(derived["thetastar"], rel=1e-5)
    assert c.r_drag == pytest.approx(derived["rdrag"], rel=1e-5)
