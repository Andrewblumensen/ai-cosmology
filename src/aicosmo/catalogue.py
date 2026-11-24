"""Idea factory catalogue: every expansion-history model scored by scripts/run_catalogue.py.

Each entry is a `Model` with a source and an impact note (CLAUDE.md rule 1).
Origins:
- "paper-new": proposed or revived after DESI (2025-26), harvested from arXiv
- "paper-old": older alternatives to Lambda (1980-2020), harvested from arXiv
- "llm-new":  proposed by Claude/Copilot in this project; no known prior paper

Density models give f(z) = rho_DE(z) / rho_DE(0) (effective: everything beyond matter
and radiation). All functions must be vectorised over z.
"""

from __future__ import annotations

import numpy as np

from .score import Model, Param

CATALOGUE: list[Model] = []


def add(name, params, fn, origin, source, impact, density=False, constraint=None):
    CATALOGUE.append(Model(name, params, fn, constraint=constraint, density=density,
                           source=f"[{origin}] {source}", notes=impact))


def _norm(g):
    """Turn g(z) into f(z) = g(z) / g(0)."""
    return lambda z: g(np.asarray(z, dtype=float)) / g(np.zeros(1))[0]


# ---------------------------------------------------------------- llm-new ----
# Madau & Dickinson 2014 (arXiv:1403.0007) cosmic star-formation rate density shape
def _sfrd(z):
    return (1 + z) ** 2.7 / (1 + ((1 + z) / 2.9) ** 5.6)


add("SFR-sourced DE",
    {"beta": Param(0.1, 0.1, -0.9, 5.0)},
    lambda beta: _norm(lambda z: 1 + beta * _sfrd(z) / _sfrd(0.0)),
    "llm-new", "Claude 2026-11-24; SFRD shape from Madau & Dickinson 2014",
    "If true: dark energy has an astrophysical source term tracking star formation, "
    "a link between galaxy physics and the expansion rate (one shape-free parameter).",
    density=True)

add("Collapse-sourced DE",
    {"beta": Param(0.1, 0.1, -0.9, 5.0), "zs": Param(0.5, 0.2, 0.05, 3.0)},
    lambda beta, zs: _norm(lambda z: 1 + beta * (1 + z) ** 3 * np.exp(-z / zs)),
    "llm-new", "Claude 2026-11-24 (backreaction-inspired, phenomenological)",
    "If true: an effective dark-energy term proportional to matter in collapsed structures; "
    "it peaks at z = 3 zs - 1 and mimics a phantom crossing without a phantom field.",
    density=True)

add("Transient DE bump",
    {"A": Param(0.1, 0.1, -0.9, 3.0), "zc": Param(0.5, 0.2, 0.0, 2.5)},
    lambda A, zc: _norm(lambda z: 1 + A * np.exp(-0.5 * ((z - zc) / 0.3) ** 2)),
    "llm-new", "Claude 2026-11-24 (motivated by DESI binned w(z) reconstructions)",
    "If true: dark energy had a temporary excess (or deficit) around z_c; a localised event, "
    "not a slow roll. Width fixed at 0.3 to keep 2 parameters.",
    density=True)

add("Saturating DE",
    {"B": Param(0.1, 0.1, -0.9, 5.0), "zt": Param(0.5, 0.2, 0.02, 5.0)},
    lambda B, zt: _norm(lambda z: 1 + B * (1 - np.exp(-z / zt))),
    "llm-new", "Claude 2026-11-24",
    "If true: dark-energy density changed by a finite step at late times and then froze; "
    "B > 0 is a non-phantom (w >= -1) thawing-like history.",
    density=True)

add("tanh step in w",
    {"w_lo": Param(-0.9, 0.1, -2.0, 0.0), "w_hi": Param(-1.1, 0.1, -3.0, 0.0),
     "zt": Param(0.5, 0.2, 0.02, 3.0)},
    lambda w_lo, w_hi, zt: (lambda z: w_hi + (w_lo - w_hi) * 0.5 * (1 - np.tanh((z - zt) / 0.1))),
    "llm-new", "Claude 2026-11-24 (generic sharp transition)",
    "If true: a fast transition in the dark-energy equation of state at z_t, pointing to a "
    "phase transition rather than slow evolution.")
