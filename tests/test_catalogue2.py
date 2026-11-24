"""Batch 2 (ID-036) sanity gate, pre-registered: every model reproduces LCDM at its stated
limit, and at its start values has a finite, positive dark-energy density and a finite
expansion rate for 0 <= z <= 1100. No model is fitted to data here."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aicosmo.catalogue import CATALOGUE  # noqa: E402
from aicosmo.catalogue2 import CATALOGUE2, FIELD, LCDM_LIMITS  # noqa: E402
from aicosmo.cosmology import Cosmology  # noqa: E402
from aicosmo.score import Data  # noqa: E402

BASE = [0.68, 0.0222, 0.142]
Z = np.concatenate([np.linspace(0, 3, 61), np.geomspace(3.1, 1100, 60)])
NAMES = sorted(m.name for m in CATALOGUE2)


def _build(m, theta):
    data = Data.__new__(Data)
    data.calibrated = True
    return Data.build(data, m, np.array(BASE + list(theta)))[0]


def test_names_unique_and_new():
    assert len(NAMES) == len(set(NAMES))
    assert not set(NAMES) & {m.name for m in CATALOGUE}
    assert set(FIELD) == set(NAMES)


@pytest.mark.parametrize("name", [n for n in NAMES if LCDM_LIMITS[n] is not None])
def test_lcdm_limit(name):
    m = next(m for m in CATALOGUE2 if m.name == name)
    c = _build(m, [LCDM_LIMITS[name][k] for k in m.params])
    ref = Cosmology(*BASE)
    z = np.array([0.1, 0.5, 1.0, 2.0, 10.0, 1000.0])
    assert np.allclose(c.E(z), ref.E(z), rtol=1e-6)
    assert c.theta_star == pytest.approx(ref.theta_star, rel=1e-6)


@pytest.mark.parametrize("name", NAMES)
def test_sane_at_start(name):
    m = next(m for m in CATALOGUE2 if m.name == name)
    theta = [p.x0 for p in m.params.values()]
    for (pn, p), v in zip(m.params.items(), theta):
        assert p.lo <= v <= p.hi, f"start value of {pn} outside its range"
    c = _build(m, theta)  # raises if H^2 <= 0 or non-finite anywhere up to Z_MAX
    assert np.all(np.isfinite(c.E(Z))) and np.all(c.E(Z) > 0)
    fn = m.w_of(np.array(theta), Om=c.omega_m)
    if m.density:
        rho = np.asarray(fn(Z), dtype=float) * np.ones_like(Z)
    else:
        x = np.log1p(Z)
        w = np.asarray(fn(Z), dtype=float) * np.ones_like(Z)
        assert np.all(np.isfinite(w)), "w(z) not finite"
        rho = np.exp(3 * np.concatenate([[0], np.cumsum(np.diff(x) * 0.5 * (2 + w[1:] + w[:-1]))]))
    assert np.all(np.isfinite(rho)) and np.all(rho > 0), "DE density not finite/positive"


@pytest.mark.parametrize("name", NAMES)
def test_only_value_errors_inside_ranges(name):
    """The fitter treats ValueError as a rejected point; any other exception would crash a fit.
    Build each model at 40 random points inside its ranges (no data, no chi2)."""
    m = next(m for m in CATALOGUE2 if m.name == name)
    rng = np.random.default_rng(0)
    for _ in range(40):
        theta = [rng.uniform(p.lo, p.hi) for p in m.params.values()]
        try:
            _build(m, theta)
        except ValueError:
            pass
