"""Every catalogue model with a LCDM limit must reproduce LCDM there (catches sign and
formula errors in harvested models)."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aicosmo.catalogue import CATALOGUE  # noqa: E402
from aicosmo.cosmology import Cosmology  # noqa: E402
from aicosmo.score import LCDM, Data  # noqa: E402

LIMITS = {
    "SFR-sourced DE": dict(beta=0), "Collapse-sourced DE": dict(beta=0, zs=0.5),
    "Transient DE bump": dict(A=0, zc=0.5), "Saturating DE": dict(B=0, zt=0.5),
    "tanh step in w": dict(w_lo=-1, w_hi=-1, zt=0.5),
    "Barboza-Alcaniz": dict(w0=-1, w1=0), "JBP": dict(w0=-1, wa=0),
    "Logarithmic (Efstathiou)": dict(w0=-1, wa=0), "Linear-in-z w": dict(w0=-1, wb=0),
    "Generalised-beta CPL": dict(w0=-1, wa=0, b=1), "Second-order CPL": dict(w0=-1, wa=0),
    "Wang tanh transition": dict(w0=-1, wa=-1, zT=0.5, dz=0.3),
    "Pade thawing": dict(w0=-1, eta0=1), "Dutta-Scherrer/Linder thawing": dict(w0=-1),
    "GEDE": dict(D=0, zt=1), "MEDE": dict(D=0, zt=0.5),
    "Negative Lambda + CPL": dict(OL=0, w0=-1, wa=0), "Step-density quintessence": dict(zi=1, al=0),
    "Running vacuum (nu)": dict(nu=0), "wCDM / Cardassian power law": dict(w=-1),
    "Modified polytropic Cardassian": dict(n=0, q=1), "Bulk-viscous matter + Lambda": dict(z0=0),
    "Alam-Sahni-Starobinsky Taylor": dict(A1=0, A2=0),
    "Linder-Huterer transition": dict(wi=-1, wf=-1, at=0.5, tau=0.2),
    "Corasaniti-Copeland kink": dict(w0=-1, wm=-1, ac=0.5, Gam=10),
    "Sahni-Shtanov braneworld (phantom branch)": dict(Ol=0),
}
NO_LIMIT = {"PEDE", "DGP (flat, self-accelerating)", "Ricci holographic DE",
            "Vacuum decay Lambda ~ H", "LambdaS CDM (abrupt)", "LambdaS CDM (smooth)"}


def test_every_model_is_classified():
    assert {m.name for m in CATALOGUE} == set(LIMITS) | NO_LIMIT


@pytest.mark.parametrize("name", sorted(LIMITS))
def test_lcdm_limit(name):
    m = next(m for m in CATALOGUE if m.name == name)
    base = [0.68, 0.0222, 0.142]
    x = np.array(base + [LIMITS[name][k] for k in m.params])
    data = Data.__new__(Data)
    data.calibrated = True
    c, _ = Data.build(data, m, x)
    ref = Cosmology(*base)
    z = np.array([0.1, 0.5, 1.0, 2.0, 10.0, 1000.0])
    assert np.allclose(c.E(z), ref.E(z), rtol=1e-6)
    assert c.theta_star == pytest.approx(ref.theta_star, rel=1e-6)
