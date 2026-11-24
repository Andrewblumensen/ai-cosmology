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


# ------------------------------------------------------------- paper-new ----
# Harvested 2026-11-24 (session 12) from DESI-era papers. Where a model has a w(z), we give
# w(z) and let Cosmology integrate it (avoids hand-derived densities). Formulas were checked
# against the cited equation unless the source says otherwise.
def _a(z):
    return 1.0 / (1.0 + np.asarray(z, dtype=float))


W = dict(w0=Param(-0.9, 0.1, -3.0, 1.0))  # common w0 range (DESI prior)

add("Barboza-Alcaniz",
    {**W, "w1": Param(-0.3, 0.2, -3.0, 3.0)},
    lambda w0, w1: (lambda z: w0 + w1 * z * (1 + z) / (1 + z ** 2)),
    "paper-new", "Barboza & Alcaniz 2008; DESI-era use: Wolf+ 2025 arXiv:2502.04929 eq. 10",
    "If preferred: w evolves but stays bounded at all z (unlike CPL's linear-in-a form).")

add("JBP",
    {**W, "wa": Param(-0.5, 0.3, -4.0, 4.0)},
    lambda w0, wa: (lambda z: w0 + wa * z / (1 + z) ** 2),
    "paper-new", "Jassal, Bagla & Padmanabhan 2005; Wolf+ 2025 arXiv:2502.04929 eqs. 8-9",
    "If preferred: dark energy is dynamical only around z ~ 1 and returns to w0 early on.")

add("Logarithmic (Efstathiou)",
    {**W, "wa": Param(-0.3, 0.2, -2.0, 2.0)},
    lambda w0, wa: (lambda z: w0 - wa * np.log1p(z)),
    "paper-new", "Efstathiou 1999 astro-ph/9904356; Malekjani+ 2024 arXiv:2407.09767",
    "If preferred: w drifts logarithmically; diverges at high z, so CMB strongly limits wa.")

add("Linear-in-z w",
    {**W, "wb": Param(-0.05, 0.05, -1.0, 1.0)},
    lambda w0, wb: (lambda z: w0 + wb * z),
    "paper-new", "Cheng+ 2026 arXiv:2610.23954",
    "Taylor-in-z baseline; diverges at high z, so it is effectively pinned by the CMB.")


def _gen_beta(w0, wa, b):
    def w(z):
        lna = np.log(_a(z))
        frac = -lna if abs(b) < 1e-6 else -np.expm1(b * lna) / b
        return w0 + wa * frac
    return w


add("Generalised-beta CPL",
    {**W, "wa": Param(-0.5, 0.3, -3.0, 2.0), "b": Param(1.0, 0.5, -2.0, 2.0)},
    _gen_beta,
    "paper-new", "Malekjani+ 2024 arXiv:2407.09767",
    "Family containing CPL (b = 1) and log (b -> 0); asks which shape of evolution the data want.")

add("Second-order CPL",
    {**W, "wa": Param(-0.5, 0.3, -4.0, 4.0)},
    lambda w0, wa: (lambda z: w0 + wa * ((z / (1 + z)) + 0.5 * (z / (1 + z)) ** 2)),
    "paper-new", "Barua+ 2025 arXiv:2506.12709",
    "Next order in the (1 - a) expansion; tests whether CPL's linear form is limiting.")

add("Wang tanh transition",
    {"w0": Param(-0.9, 0.1, -2.0, 0.0), "wa": Param(-1.2, 0.2, -2.0, 0.0),
     "zT": Param(0.6, 0.3, 0.1, 2.0), "dz": Param(0.3, 0.2, 0.05, 2.0)},
    lambda w0, wa, zT, dz: (lambda z: 0.5 * ((w0 + wa) + (wa - w0) * np.tanh((z - zT) / dz))),
    "paper-new", "Barua+ 2025 arXiv:2506.12709",
    "If preferred: a transition in w between two plateaus at redshift zT with width dz.")

add("Pade thawing",
    {"w0": Param(-0.85, 0.1, -1.0, 0.3), "eta0": Param(1.0, 1.0, -1.0, 10.0)},
    lambda w0, eta0: (lambda z: -1 + (1 + w0) / (1 + (eta0 / 3) * ((1 + z) ** 3 - 1))),
    "paper-new", "Shlivko+ 2025 arXiv:2512.20832 eq. 1",
    "If preferred: a thawing scalar field (w >= -1, no crossing) explains DESI.")


def _ds_thawing(w0):
    b, p = 0.5, 1.0
    return lambda z: -1 + (1 + w0) * _a(z) ** p * ((1 + b) / (1 + b * _a(z) ** -3)) ** (1 - p / 3)


add("Dutta-Scherrer/Linder thawing",
    {"w0": Param(-0.85, 0.1, -1.0, 0.0)}, _ds_thawing,
    "paper-new", "Barua+ 2026 arXiv:2611.01505 eq. 5 (b = 0.5, p = 1)",
    "If preferred: hilltop-like thawing quintessence with one parameter, no crossing.")

add("GEDE",
    {"D": Param(0.3, 0.3, -3.0, 3.0), "zt": Param(1.0, 0.5, 0.1, 5.0)},
    lambda D, zt: (lambda z: (1 - np.tanh(D * np.log10((1 + z) / (1 + zt))))
                   / (1 + np.tanh(D * np.log10(1 + zt)))),
    "paper-new", "Li & Shafieloo 2020; Sharma+ 2025 arXiv:2507.00835 eq. 7",
    "If preferred: dark energy emerged at late times around zt.", density=True)

add("PEDE",
    {}, lambda: (lambda z: 1 - np.tanh(np.log10(1 + np.asarray(z, dtype=float)))),
    "paper-new", "Li & Shafieloo 2019; Hernandez-Almada+ 2024 arXiv:2407.09430 eq. 2",
    "If preferred: emergent, phantom-like dark energy with no extra parameter.", density=True)

add("MEDE",
    {"D": Param(0.3, 0.2, 0.0, 3.0), "zt": Param(0.5, 0.3, 0.1, 2.0)},
    lambda D, zt: (lambda z: -1 - D * np.tanh(np.log10((1 + z) / (1 + zt)))),
    "paper-new", "Li+ 2026 arXiv:2606.05723 eq. 3",
    "If preferred: emergent DE that crosses w = -1 exactly at zt.")

add("LambdaS CDM (abrupt)",
    {"zd": Param(2.0, 0.3, 1.0, 3.0)},
    lambda zd: (lambda z: np.sign(zd - np.asarray(z, dtype=float))),
    "paper-new", "Akarsu+; Yadav+ 2025 arXiv:2509.26049",
    "If preferred: the cosmological constant switched sign (AdS -> dS) at zd.", density=True)

add("LambdaS CDM (smooth)",
    {"zd": Param(2.0, 0.3, 0.5, 3.0), "D": Param(5.0, 3.0, 0.5, 50.0)},
    lambda zd, D: (lambda z: np.tanh(D * (zd - np.asarray(z, dtype=float))) / np.tanh(D * zd)),
    "paper-new", "Mitra+ 2026 arXiv:2607.06735",
    "If preferred: a smooth sign switch of the vacuum energy around zd.", density=True)


def _neg_lambda_cpl(OL, w0, wa, Om):
    def f(z):
        z = np.asarray(z, dtype=float)
        x = (1 - Om - OL) * (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
        return (OL + x) / (1 - Om)
    return f


add("Negative Lambda + CPL",
    {"OL": Param(-0.2, 0.2, -1.0, 0.0), "w0": Param(-0.9, 0.1, -3.0, 1.0),
     "wa": Param(-0.5, 0.3, -3.0, 2.0)}, _neg_lambda_cpl,
    "paper-new", "Wang+ 2024 arXiv:2406.03395; Mukherjee+ 2025 arXiv:2501.18335",
    "If preferred: an anti-de Sitter vacuum hides under dynamical dark energy.",
    density=True)
CATALOGUE[-1].uses_om = True

add("Step-density quintessence",
    {"zi": Param(1.0, 0.5, 0.0, 5.0), "al": Param(1.0, 0.5, -5.0, 5.0)},
    lambda zi, al: (lambda z: (1 + (1 + zi) ** al) / (1 + ((1 + zi) / (1 + np.asarray(z, dtype=float))) ** al)),
    "paper-new", "Akthar+ 2024 arXiv:2411.15892",
    "If preferred: dark-energy density changed by a smooth step around zi.", density=True)


def _dgp(Om):
    orc = (1 - Om) ** 2 / 4
    return lambda z: ((np.sqrt(Om * (1 + np.asarray(z)) ** 3 + orc) + np.sqrt(orc)) ** 2
                      - Om * (1 + np.asarray(z)) ** 3) / (1 - Om)


add("DGP (flat, self-accelerating)", {}, _dgp,
    "paper-new", "Dvali, Gabadadze & Porrati 2000 hep-th/0005016; Deffayet 2001 astro-ph/0105068",
    "If preferred: gravity leaks into a fifth dimension; no dark energy at all.", density=True)
CATALOGUE[-1].uses_om = True


def _rvm(nu, Om):
    return lambda z: (1 + Om / (1 - nu) * ((1 + np.asarray(z)) ** (3 * (1 - nu)) - 1)
                      - Om * (1 + np.asarray(z)) ** 3) / (1 - Om)


add("Running vacuum (nu)", {"nu": Param(0.0, 0.003, -0.1, 0.1)}, _rvm,
    "paper-new", "Shapiro & Sola; Sola, Gomez-Valent & de Cruz Perez 2015 arXiv:1501.03832",
    "If preferred: the vacuum energy runs with H^2 as QFT in curved space suggests.",
    density=True)
CATALOGUE[-1].uses_om = True

# ------------------------------------------------------------- paper-old ----
add("wCDM / Cardassian power law", {"w": Param(-0.95, 0.05, -3.0, 1.0)},
    lambda w: (lambda z: w * np.ones_like(np.asarray(z, dtype=float))),
    "paper-old", "Freese & Lewis 2002 astro-ph/0201229 (Cardassian n = 1 + w); Ozer & Taha 1986",
    "If preferred: constant w != -1; the simplest non-Lambda dark energy.")


def _mp_cardassian(n, q, Om):
    def f(z):
        x = 1 + np.asarray(z, dtype=float)
        e2 = Om * x ** 3 * (1 + (Om ** -q - 1) * x ** (3 * q * (n - 1))) ** (1 / q)
        return (e2 - Om * x ** 3) / (1 - Om)
    return f


add("Modified polytropic Cardassian",
    {"n": Param(0.0, 0.1, -1.0, 0.66), "q": Param(1.0, 0.3, 0.1, 5.0)}, _mp_cardassian,
    "paper-old", "Freese & Lewis 2002 astro-ph/0201229 (formula from memory, not checked)",
    "If preferred: acceleration from a modified Friedmann equation, not a new fluid.",
    density=True)
CATALOGUE[-1].uses_om = True


def _ricci(c, Om):
    def f(z):
        x = 1 + np.asarray(z, dtype=float)
        e2 = 2 * Om / (2 - c) * x ** 3 + (1 - 2 * Om / (2 - c)) * x ** (4 - 2 / c)
        return (e2 - Om * x ** 3) / (1 - Om)
    return f


add("Ricci holographic DE", {"c": Param(0.45, 0.05, 0.2, 0.9)}, _ricci,
    "paper-old", "Gao+ 2009 arXiv:0712.1394 (formula derived by harvester, not checked)",
    "If preferred: dark energy set by the Ricci curvature scale (holographic principle).",
    density=True)
CATALOGUE[-1].uses_om = True


def _lambda_h(Om):
    ol = 1 - np.sqrt(Om)
    return lambda z: ((ol + (1 - ol) * (1 + np.asarray(z)) ** 1.5) ** 2 - Om * (1 + np.asarray(z)) ** 3) / (1 - Om)


add("Vacuum decay Lambda ~ H", {}, _lambda_h,
    "paper-old", "Borges & Carneiro 2005; Carneiro & Lima 2005 (derived by harvester)",
    "If preferred: vacuum energy decays into matter at a rate set by H.", density=True)
CATALOGUE[-1].uses_om = True


def _viscous(z0, Om):
    ol = (1 - Om) * (1 - z0)
    return lambda z: (Om * (1 + np.asarray(z)) ** (3 * (1 - z0)) + ol / (1 - z0)
                      - Om * (1 + np.asarray(z)) ** 3) / (1 - Om)


add("Bulk-viscous matter + Lambda", {"z0": Param(0.001, 0.002, 0.0, 0.1)}, _viscous,
    "paper-old", "Barrow 1986; Padmanabhan & Chitre 1987; Ren & Meng 2006 (derived by harvester)",
    "If preferred: dark matter has bulk viscosity zeta ~ H, changing its dilution.",
    density=True)
CATALOGUE[-1].uses_om = True


def _alam(A1, A2, Om):
    a0 = 1 - Om - A1 - A2
    return lambda z: (a0 + A1 * (1 + np.asarray(z)) + A2 * (1 + np.asarray(z)) ** 2) / (1 - Om)


add("Alam-Sahni-Starobinsky Taylor",
    {"A1": Param(0.0, 0.2, -5.0, 5.0), "A2": Param(0.0, 0.1, -5.0, 5.0)}, _alam,
    "paper-old", "Alam, Sahni, Saini & Starobinsky 2004 astro-ph/0311364",
    "If preferred: the dark-energy density has curvature-like and string-like terms.",
    density=True)
CATALOGUE[-1].uses_om = True

add("Linder-Huterer transition",
    {"wi": Param(-1.2, 0.2, -2.0, 0.5), "wf": Param(-0.9, 0.1, -2.0, 0.5),
     "at": Param(0.6, 0.1, 0.1, 1.0), "tau": Param(0.2, 0.1, 0.05, 1.0)},
    lambda wi, wf, at, tau: (lambda z: wf + (wi - wf) / (1 + (_a(z) / at) ** (1 / tau))),
    "paper-old", "Linder & Huterer 2005 astro-ph/0505330",
    "If preferred: w moved from wi to wf around scale factor at; generic transition.")

add("Corasaniti-Copeland kink",
    {"w0": Param(-0.9, 0.1, -1.5, -0.5), "wm": Param(-1.2, 0.2, -2.0, 0.5),
     "ac": Param(0.6, 0.1, 0.1, 0.9), "Gam": Param(10.0, 5.0, 1.0, 30.0)},
    lambda w0, wm, ac, Gam: (lambda z: w0 + (wm - w0) / (1 + np.exp(Gam * (_a(z) - ac)))),
    "paper-old", "Corasaniti & Copeland 2003 astro-ph/0205544",
    "If preferred: a kink in w, as in tracker quintessence models.")


def _sahni_shtanov(Ol, Om):
    OL = 1 + 2 * np.sqrt(Ol) - Om
    def f(z):
        m = Om * (1 + np.asarray(z, dtype=float)) ** 3
        e2 = m + OL + 2 * Ol - 2 * np.sqrt(Ol) * np.sqrt(m + OL + Ol)
        return (e2 - m) / (1 - Om)
    return f


add("Sahni-Shtanov braneworld (phantom branch)", {"Ol": Param(0.01, 0.01, 0.0, 0.5)},
    _sahni_shtanov,
    "paper-old", "Sahni & Shtanov 2003 astro-ph/0202346 (closed form derived by harvester)",
    "If preferred: phantom-like acceleration from a brane, without a phantom field.",
    density=True)
CATALOGUE[-1].uses_om = True
