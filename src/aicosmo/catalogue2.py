"""Idea factory, batch 2 (ID-036): mechanisms imported from other fields.

Harvested by eight field agents into docs/batch2-harvest/*.md (one file per field cluster),
curated by the pre-registered rules in IDEAS.md (ID-036). Kept apart from batch 1
(catalogue.py) so batch-1 results stay reproducible.

Origins:
- "field-new":   analogy imported from another field; no prior cosmology paper found
- "field-known": the harvester found prior art in cosmology (still counts as a test)

Each entry records its ΛCDM limit (parameter values) in LCDM_LIMITS, or None if it has none;
tests/test_catalogue2.py checks every limit and the sanity gate (finite, positive DE density
for 0 <= z <= 1100 at the start values).
"""

from __future__ import annotations

import numpy as np

from .score import Model, Param

CATALOGUE2: list[Model] = []
LCDM_LIMITS: dict[str, dict[str, float] | None] = {}
FIELD: dict[str, str] = {}


def add(name, params, fn, origin, field, source, impact, limit, density=False,
        uses_om=False, constraint=None):
    if name in LCDM_LIMITS:
        raise ValueError(f"duplicate model name {name!r}")
    m = Model(name, params, fn, constraint=constraint, density=density,
              source=f"[{origin}] {source}", notes=impact, uses_om=uses_om)
    CATALOGUE2.append(m)
    LCDM_LIMITS[name] = limit
    FIELD[name] = field


def _z(z):
    return np.asarray(z, dtype=float)


def _norm(g):
    """Turn g(z) into f(z) = g(z) / g(0)."""
    return lambda z: g(_z(z)) / g(np.zeros(1))[0]


def _t_cosmic(z, Om):
    """Cosmic time in units of 1/H0 in a reference flat matter + Lambda model with the same Om.
    Used only as a clock (recasting: ignores the model's own DE deviation)."""
    a = 1.0 / (1.0 + _z(z))
    OL = 1.0 - Om
    return 2.0 / (3.0 * np.sqrt(OL)) * np.arcsinh(np.sqrt(OL / Om) * a ** 1.5)


def _E_ref(z, Om):
    """Reference flat LCDM H/H0 (late-time; radiation ignored), used as a drive or clock."""
    return np.sqrt(Om * (1.0 + _z(z)) ** 3 + 1.0 - Om)


P = Param
PI = np.pi
H_CM = "docs/batch2-harvest/condensed-matter-stat-phys.md"


# ------------------------------------------------- condensed matter / stat phys ----
def _lppl(A, alpha, omega, phi):
    return _norm(lambda z: 1.0 + A * (1.0 + z) ** (-alpha) * np.cos(omega * np.log1p(z) + phi))


add("Log-periodic critical DE",
    {"A": P(0.1, 0.1, -0.9, 0.9), "alpha": P(0.5, 0.3, 0.0, 4.0),
     "omega": P(4.0, 2.0, 0.3, 12.0), "phi": P(0.0, 1.0, -PI, PI)}, _lppl,
    "field-known", "condensed matter",
    f"{H_CM}; Sornette discrete scale invariance; close prior art: Barenboim+ astro-ph/0510178. "
    "Merged with 'Efimov log-periodic DE' (chemistry harvest, identical form; omega lo 0.5 -> 0.3) "
    "and 'Log-periodic discrete-scale-invariance ring' (information harvest, same family with "
    "A' = A/(1 + A cos phi)): proposed independently by three harvesters",
    "If true: a fractal-in-time dark sector with a preferred scale ratio exp(2 pi/omega).",
    dict(A=0, alpha=0.5, omega=4, phi=0), density=True)


def _arcsine(A, tw, p, Om):
    def g(z):
        u = (_t_cosmic(z, Om) / tw) ** p
        return 1.0 + A * (2.0 / PI) * np.arcsin(1.0 / np.sqrt(1.0 + u))
    return _norm(g)


add("Arcsine-law trap aging",
    {"A": P(0.1, 0.2, -0.9, 3.0), "tw": P(0.5, 0.3, 0.02, 5.0), "p": P(1.0, 0.3, 0.3, 3.0)},
    _arcsine, "field-new", "condensed matter", f"{H_CM}; Bouchaud trap model",
    "If true: dark energy is a glassy, ageing component with a memory of a quench time.",
    dict(A=0, tw=0.5, p=1), density=True, uses_om=True)


def _bkt(A, zk, b):
    def f(z):
        t = np.maximum((1.0 + _z(z)) / (1.0 + zk) - 1.0, 1e-12)
        return 1.0 + A * np.exp(-b / np.sqrt(t))
    return f


add("BKT essential-singularity onset",
    {"A": P(0.1, 0.2, -0.9, 3.0), "zk": P(0.5, 0.3, 0.05, 3.0), "b": P(1.0, 0.5, 0.05, 10.0)},
    _bkt, "field-new", "condensed matter", f"{H_CM}; Berezinskii-Kosterlitz-Thouless",
    "If true: exactly LCDM below z_k, an infinitely smooth (infinite-order) transition above.",
    dict(A=0, zk=0.5, b=1), density=True)


def _kz(A, zc, eh, beta):
    def g(z):
        eps = np.clip(1.0 - (1.0 + z) / (1.0 + zc), 0.0, eh)
        return 1.0 + A * eps ** beta
    return _norm(g)


add("Kibble-Zurek frozen order parameter",
    {"A": P(0.2, 0.2, -0.9, 3.0), "zc": P(1.0, 0.3, 0.1, 3.0), "eh": P(0.2, 0.1, 0.02, 1.0),
     "beta": P(0.5, 0.2, 0.5, 3.0)}, _kz,
    "field-new", "condensed matter", f"{H_CM}; Kibble-Zurek freeze-out",
    "If true: Lambda is a frozen relic of a critical transition, with a recent ramp whose "
    "exponent is a universality class.",
    dict(A=0, zc=1, eh=0.2, beta=0.5), density=True)


def _hn(A, tau, alpha, beta, Om):
    return _norm(lambda z: 1.0 + A * np.real((1.0 + (1j * _E_ref(z, Om) * tau) ** alpha) ** (-beta)))


add("Havriliak-Negami dispersive vacuum",
    {"A": P(0.2, 0.2, -0.9, 3.0), "tau": P(1.0, 0.5, 0.05, 20.0), "alpha": P(0.7, 0.2, 0.1, 1.0),
     "beta": P(0.7, 0.2, 0.1, 1.0)}, _hn,
    "field-new", "condensed matter", f"{H_CM}; dielectric relaxation",
    "If true: dark energy is a frequency-dependent response of the vacuum to the expansion rate.",
    dict(A=0, tau=1, alpha=0.7, beta=0.7), density=True, uses_om=True)


def _time_crystal(A, T, phi, Om):
    return _norm(lambda z: 1.0 + A * np.cos(2.0 * PI * _t_cosmic(z, Om) / T + phi))


add("Time-crystal modulation",
    {"A": P(0.1, 0.1, -0.5, 0.5), "T": P(1.5, 0.5, 0.5, 6.0), "phi": P(0.0, 1.0, -PI, PI)},
    _time_crystal, "field-new", "condensed matter",
    f"{H_CM}; Floquet time crystals; related: Mersini-Houghton arXiv:2502.08887",
    "If true: broken time-translation symmetry in the dark sector; a repeat should be seen.",
    dict(A=0, T=1.5, phi=0), density=True, uses_om=True)


def _reaction_order(A, tau, m, Om):
    q = m - 1.0

    def g(z):
        t = _t_cosmic(z, Om)
        if abs(q) < 1e-6:
            core = np.exp(-t / tau)
        else:
            core = np.maximum(1.0 + q * t / tau, 0.0) ** (-1.0 / q)
        return 1.0 + A * core
    return _norm(g)


add("Reaction-order defect relaxation",
    {"A": P(0.1, 0.2, -0.9, 3.0), "tau": P(0.5, 0.3, 0.02, 5.0), "m": P(2.0, 0.5, 0.3, 4.0)},
    _reaction_order, "field-new", "condensed matter", f"{H_CM}; Vinen vortex decay, Smoluchowski",
    "If true: DE is a defect density decaying by m-body annihilation; m is a universality class.",
    dict(A=0, tau=0.5, m=2), density=True, uses_om=True)


def _void_perc(A, p0, s, beta):
    def g(z):
        p = p0 * (1.0 + z) ** (-s)
        return 1.0 + A * np.maximum(p - 0.3116, 0.0) ** beta
    return _norm(g)


add("Void-percolation order parameter",
    {"A": P(0.5, 0.3, -0.9, 5.0), "p0": P(0.6, 0.1, 0.35, 0.95), "s": P(1.0, 0.4, 0.1, 3.0),
     "beta": P(0.42, 0.1, 0.3, 1.0)}, _void_perc,
    "field-new", "condensed matter", f"{H_CM}; 3D site percolation (p_c = 0.3116)",
    "If true: DE onset is a percolation transition of the void network (cosmic-web topology).",
    dict(A=0, p0=0.6, s=1, beta=0.42), density=True)


def _bcs(A, zc, s):
    def g(z):
        x = np.maximum(((1.0 + zc) / (1.0 + z)) ** s - 1.0, 0.0)
        return 1.0 + A * np.tanh(1.82 * (1.018 * x) ** 0.51) ** 2
    return _norm(g)


add("BCS-gap condensation onset",
    {"A": P(-0.2, 0.2, -0.9, 3.0), "zc": P(1.0, 0.5, 0.05, 5.0), "s": P(1.0, 0.3, 0.5, 2.0)},
    _bcs, "field-known", "condensed matter",
    f"{H_CM}; concept: Alexander, Biswas & Calcagni arXiv:0906.5161",
    "If true: DE carries the condensation energy of a dark pairing transition.",
    dict(A=0, zc=1, s=1), density=True)


def _avrami(L, an, n):
    return _norm(lambda z: 1.0 + L * -np.expm1(-((1.0 / (1.0 + z)) / an) ** n))


add("Avrami-KWW vacuum conversion",
    {"L": P(-0.2, 0.2, -0.9, 3.0), "an": P(0.6, 0.2, 0.2, 1.5), "n": P(4.0, 1.0, 0.45, 6.0)},
    _avrami, "field-known", "condensed matter",
    f"{H_CM}; JMAK kinetics; concept: Pen & Zhang arXiv:1202.0107. Merged with the chemistry "
    "harvest's 'Avrami-KWW vacuum conversion' (same family: n_CM = 1.5 n; n lo 1 -> 0.45 adds "
    "its glassy stretched-exponential range)",
    "If true: a late false-vacuum conversion; n > 1 bubble nucleation (GW background), "
    "n < 1 glassy relaxation.",
    dict(L=0, an=0.6, n=4), density=True)


def _granular(A, tau, B, Om):
    return _norm(lambda z: 1.0 + A / (1.0 + B * np.log1p(_t_cosmic(z, Om) / tau)))


add("Inverse-log granular compaction",
    {"A": P(0.1, 0.2, -0.95, 3.0), "tau": P(0.1, 0.1, 0.005, 2.0), "B": P(2.0, 1.0, 0.1, 20.0)},
    _granular, "field-new", "condensed matter",
    f"{H_CM}; Knight+ 1995 granular compaction. Merged with the geoscience harvest's "
    "'Granular-compaction DE' (identical with A = -D; A lo -0.9 -> -0.95)",
    "If true: glassy, logarithmically slow vacuum relaxation; w = -1 only approximately.",
    dict(A=0, tau=0.1, B=2), density=True, uses_om=True)


# ------------------------------------------------- biology / ecology / epidemiology ----
H_BIO = "docs/batch2-harvest/biology-ecology-epidemiology.md"


def _wbe(r0, k):
    return lambda z: (np.maximum(1.0 - (1.0 - r0) * (1.0 + _z(z)) ** k, 0.0) / r0) ** 4


add("Ontogenetic growth DE",
    # start k = 0.2 (harvest: 0.3) so the birth redshift lies beyond z = 1100 at the start
    # values (pre-registered sanity gate); range unchanged.
    {"r0": P(0.8, 0.1, 0.1, 3.0), "k": P(0.2, 0.2, -3.0, 3.0)}, _wbe,
    "field-new", "biology", f"{H_BIO}; West, Brown & Enquist 2001 growth law",
    "If true: DE is a 'born' component with a universal sigmoid history and a birth redshift.",
    dict(r0=0.8, k=0), density=True, constraint=lambda r0, k: not (r0 > 1 and k > 0))


def _gompertz(lam, alpha, beta):
    def f(z):
        a = 1.0 / (1.0 + _z(z))
        g = a - 1.0 if abs(beta) < 1e-8 else (np.exp(beta * a) - np.exp(beta)) / beta
        return np.exp(-lam * (a - 1.0) - alpha * g)
    return f


def _gompertz_ok(lam, alpha, beta):
    return abs(lam + alpha * (np.expm1(beta) / beta if abs(beta) > 1e-8 else 1.0)) <= 12.0


add("Gompertz-Makeham vacuum senescence",
    {"lam": P(0.3, 0.3, -3.0, 6.0), "alpha": P(0.3, 0.3, -3.0, 6.0), "beta": P(2.0, 1.0, -6.0, 6.0)},
    _gompertz, "field-new", "biology", f"{H_BIO}; Gompertz-Makeham mortality law",
    "If true: Lambda early, then exponential-in-a 'ageing' of the vacuum (1 + w ~ a e^(beta a)).",
    dict(lam=0, alpha=0, beta=2), density=True, constraint=_gompertz_ok)


def _stair(kappa, Lam, eps, x0):
    def S(x):
        th = 2 * PI * (x - x0) / Lam
        return (x - x0) - (Lam / PI) * np.angle(1.0 - eps * np.exp(1j * th))
    return lambda z: np.exp(kappa * (S(np.log1p(_z(z))) - S(np.zeros(1))[0]))


add("Punctuated-equilibrium staircase",
    {"kappa": P(-0.3, 0.3, -1.5, 1.0), "Lam": P(0.8, 0.2, 0.2, 3.0), "eps": P(0.8, 0.1, 0.0, 0.95),
     "x0": P(0.0, 0.3, -3.0, 3.0)}, _stair,
    "field-new", "biology", f"{H_BIO}; Eldredge & Gould punctuated equilibrium",
    "If true: the vacuum energy 'ratchets' in discrete log-periodic jumps (w = -1 on plateaus).",
    dict(kappa=0, Lam=0.8, eps=0.8, x0=0), density=True)


def _pk(B, tau, ke, phi):
    ka = 5.0 * ke

    def c(t):
        return np.exp(-ke * t) / (1 - np.exp(-ke * tau)) - np.exp(-ka * t) / (1 - np.exp(-ka * tau))
    cmax = c(np.linspace(0.0, tau, 400)).max()

    def g(z):
        u = np.log1p(_z(z)) / tau + phi
        return 1.0 + B * c((1.0 - np.mod(u, 1.0)) * tau) / cmax
    return _norm(g)


add("Pharmacokinetic repeated-dose DE",
    {"B": P(0.2, 0.2, -0.9, 20.0), "tau": P(1.0, 0.3, 0.3, 3.0), "ke": P(2.0, 1.0, 0.2, 10.0),
     "phi": P(0.3, 0.2, 0.0, 1.0)}, _pk,
    "field-new", "biology", f"{H_BIO}; Bateman function, periodic dosing",
    "If true: DE is a periodically re-dosed, asymmetrically relaxing component (sawtooth in ln a).",
    dict(B=0, tau=1, ke=2, phi=0.3), density=True)


def _hopf_onset(A, omega, zh, phi):
    def g(z):
        return 1.0 + A / np.sqrt(1.0 + ((1.0 + z) / (1.0 + zh)) ** 4) * np.cos(omega * np.log1p(z) + phi)
    return _norm(g)


add("Hopf-onset oscillator",
    {"A": P(0.1, 0.1, -0.9, 0.9), "omega": P(6.0, 2.0, 0.5, 20.0), "zh": P(1.0, 0.5, 0.0, 5.0),
     "phi": P(0.5, 1.0, -PI, PI)}, _hopf_onset,
    "field-new", "biology", f"{H_BIO}; Stuart-Landau normal form; K->0 limit ~ Linder astro-ph/0511415",
    "If true: DE is a dormant clock that wakes up late (oscillation only at low z).",
    dict(A=0, omega=6, zh=1, phi=0.5), density=True)


def _ricker(B, r, dx, x1):
    nmax = int(np.ceil(np.log(1101.0) / dx)) + 2
    xs = [x1]
    for _ in range(nmax):
        xs.append(r * xs[-1] * (1.0 - xs[-1]))
    xs = np.array(xs)
    return _norm(lambda z: 1.0 + B * np.interp((np.log(1101.0) - np.log1p(z)) / dx,
                                               np.arange(len(xs)), xs))


add("Logistic-map generational DE",
    {"B": P(0.2, 0.2, -0.9, 5.0), "r": P(3.2, 0.2, 2.5, 4.0), "dx": P(0.4, 0.1, 0.1, 1.0),
     "x1": P(0.3, 0.1, 0.01, 0.99)}, _ricker,
    "field-new", "biology", f"{H_BIO}; May 1976 logistic map",
    "If true: deterministic chaos in the DE history (a stress test for any wiggle structure).",
    dict(B=0, r=3.2, dx=0.4, x1=0.3), density=True)


def _rinf(R0):
    from scipy.special import lambertw
    R0 = np.asarray(R0, dtype=float)
    x = np.maximum(R0, 1.0 + 1e-12)
    # Principal branch W_0. (The harvest used W_-1, which returns the trivial root R_inf = 0;
    # caught by tests/test_catalogue2.py before any fit.)
    return np.where(R0 > 1.0, 1.0 + np.real(lambertw(-x * np.exp(-x), 0)) / x, 0.0)


def _sir(R0, p, delta):
    r_now = _rinf(R0)
    return lambda z: (_rinf(R0 * (1.0 + _z(z)) ** (-p)) / r_now) ** delta


add("Epidemic-threshold DE",
    # start p = 0.1 (harvest: 0.5) so the threshold redshift lies beyond z = 1100 at the start
    # values (pre-registered sanity gate); range unchanged.
    {"R0": P(2.5, 0.5, 1.2, 8.0), "p": P(0.1, 0.3, 0.0, 3.0), "delta": P(1.0, 0.3, 0.3, 3.0)},
    _sir, "field-new", "biology", f"{H_BIO}; SIR final-size relation (Lambert W)",
    "If true: DE is a threshold phenomenon with a sharp birth redshift (R0 crosses 1).",
    dict(R0=2.5, p=0, delta=1), density=True)


def _hormesis(d, f_, e, b):
    return lambda z: -1.0 + (d + f_ * (1.0 + _z(z))) / (1.0 + ((1.0 + _z(z)) / e) ** b)


add("Hormetic equation of state",
    {"d": P(0.2, 0.2, -2.0, 2.0), "f_": P(-0.1, 0.1, -2.0, 2.0), "e": P(2.0, 0.5, 1.0, 10.0),
     "b": P(2.5, 0.5, 1.2, 8.0)}, _hormesis,
    "field-new", "biology", f"{H_BIO}; Brain-Cousens hormesis dose-response",
    "If true: a single phantom crossing with a Hill-type return to Lambda early (low novelty).",
    dict(d=0, f_=0, e=2, b=2.5))


def _adler(A, Om_slip, K, x0):
    Dl = np.sqrt(Om_slip ** 2 + K ** 2)

    def cphi(z):
        u = 0.5 * Om_slip * (np.log1p(_z(z)) - x0)
        s = K * np.cos(u) + Om_slip * np.sin(u)
        c = Dl * np.cos(u)
        return (c ** 2 - s ** 2) / (c ** 2 + s ** 2)
    return lambda z: (1.0 + A * cphi(z)) / (1.0 + A * cphi(np.zeros(1))[0])


add("Adler phase-slip heartbeat DE",
    {"A": P(0.1, 0.1, -0.9, 0.9), "Om_slip": P(5.0, 2.0, 0.5, 15.0), "K": P(3.0, 2.0, 0.0, 15.0),
     "x0": P(0.0, 0.5, -3.0, 3.0)}, _adler,
    "field-new", "biology", f"{H_BIO}; Adler injection locking; K=0 limit ~ Linder astro-ph/0511415",
    "If true: DE is a phase-locked oscillator; one coupling sets sinusoid vs spike-train shape.",
    dict(A=0, Om_slip=5, K=3, x0=0), density=True)


# ------------------------------------------------- chemistry / nuclear / particle ----
H_CH = "docs/batch2-harvest/chemistry-nuclear-particle.md"


def _msw(eps, s, zr):
    c = np.sqrt(1 - s ** 2)

    def p(z):
        d = c * ((1 + _z(z)) / (1 + zr)) ** 3
        return 0.5 * (1 - (c - d) / np.sqrt((c - d) ** 2 + s ** 2))
    return lambda z: (1 - eps * p(z)) / (1 - eps * p(0.0))


add("MSW level-crossing dark fluid",
    {"eps": P(0.3, 0.2, -2.0, 0.95), "s": P(0.4, 0.2, 0.05, 1.0), "zr": P(1.0, 0.5, 0.1, 20.0)},
    _msw, "field-known", "chemistry/particle",
    f"{H_CH}; MSW resonance; concept: Muursepp arXiv:2405.20478, Hung & Pas astro-ph/0311131",
    "If true: Lambda is only partly 'on'; its size is set by a level crossing tied to rho_m.",
    dict(eps=0, s=0.4, zr=1), density=True)


def _saha(eps, logA, b):
    def x(a):
        S = 10 ** logA * a ** 1.5 * np.exp(-b * a)
        return 2 * S / (S + np.sqrt(S * S + 4 * S))
    return lambda z: 1 - eps + eps * x(1 / (1 + _z(z))) / x(1.0)


add("Saha ionisation DE",
    {"eps": P(0.3, 0.2, 0.0, 1.0), "logA": P(1.0, 1.0, -2.0, 4.0), "b": P(2.0, 1.0, 0.1, 6.0)},
    _saha, "field-new", "chemistry/particle", f"{H_CH}; Saha equilibrium of a dark plasma",
    "If true: DE is an equilibrium property of a dark plasma (non-monotonic w with fixed shape).",
    dict(eps=0, logA=1, b=2), density=True)


def _eyring(kappa, E):
    from scipy.special import erf
    g = lambda a: np.sqrt(PI / E) * erf(np.sqrt(E * a))  # noqa: E731
    return lambda z: np.exp(kappa * (g(1.0) - g(1 / (1 + _z(z)))))


add("Eyring-Polanyi decaying vacuum",
    {"kappa": P(0.1, 0.1, -0.5, 3.0), "E": P(2.0, 1.0, 0.05, 30.0)}, _eyring,
    "field-new", "chemistry/particle", f"{H_CH}; transition-state theory, thermally activated decay",
    "If true: the vacuum decays by thermal activation that froze out (w -> -1 from above).",
    dict(kappa=0, E=2), density=True)


def _somm(eps, ev0, ep):
    c6 = PI ** 2 * ep / 6

    def S(z):
        ev = np.minimum(ev0 * (1 + _z(z)), 40 * c6)
        X = 2 * PI * ev / c6
        Y = 2 * PI * np.sqrt(np.asarray(1 / c6 - (ev / c6) ** 2, dtype=complex))
        e = np.exp(-X)
        return PI / ev * (1 - e * e) / (1 + e * e - 2 * e * np.real(np.cos(Y)))
    return lambda z: (1 + eps * S(z)) / (1 + eps * S(0.0))


add("Hulthen-Sommerfeld resonance ladder",
    {"eps": P(0.1, 0.1, 0.0, 3.0), "ev0": P(0.02, 0.02, 0.001, 0.5), "ep": P(0.05, 0.03, 0.005, 0.5)},
    _somm, "field-new", "chemistry/particle", f"{H_CH}; Sommerfeld enhancement (Hulthen potential)",
    "If true: DE tied to a dark Yukawa force; spikes in H(z) at resonance redshifts.",
    dict(eps=0, ev0=0.02, ep=0.05), density=True)


def _landau(eps, zc, beta):
    return lambda z: ((1 + eps * np.clip(1 - (1 + _z(z)) / (1 + zc), 0, None) ** (2 * beta))
                      / (1 + eps * (zc / (1 + zc)) ** (2 * beta)))


add("Landau critical-exponent condensate",
    {"eps": P(0.3, 0.3, -0.9, 5.0), "zc": P(1.0, 0.5, 0.05, 3.0), "beta": P(0.5, 0.15, 0.5, 2.0)},
    _landau, "field-new", "chemistry/particle",
    f"{H_CH}; second-order transition order parameter (nested in Kibble-Zurek with no freeze-out)",
    "If true: DE is a condensate; the data measure its critical temperature and exponent.",
    dict(eps=0, zc=1, beta=0.5), density=True)


add("Michaelis-Menten matter-to-vacuum conversion",
    {"eps": P(0.2, 0.2, -1.0, 1.0), "kappa": P(3.0, 2.0, 0.05, 50.0)},
    lambda eps, kappa: (lambda z: 1 - eps + eps * np.arctan(kappa * (1 / (1 + _z(z))) ** 1.5)
                        / np.arctan(kappa)),
    "field-known", "chemistry/particle",
    f"{H_CH}; enzyme kinetics; concept: Paliathanasis & Duffy arXiv:2604.21671",
    "If true: DM -> DE conversion with a half-saturation scale (substrate-limited growth).",
    dict(eps=0, kappa=3), density=True)


def _seesaw(zs, p, n):
    g = lambda x: 2 / (x + np.sqrt(x * x + 4))  # noqa: E731
    return lambda z: (g(((1 + _z(z)) / (1 + zs)) ** p) / g((1 / (1 + zs)) ** p)) ** n


add("Time-dependent seesaw eigenvalue",
    {"zs": P(1.0, 0.5, 0.05, 10.0), "p": P(1.5, 0.5, 0.2, 2.5), "n": P(0.3, 0.3, -0.2, 3.0)},
    _seesaw, "field-new", "chemistry/particle",
    f"{H_CH}; type-I seesaw; adjacent: Enqvist, Hannestad & Sloth hep-ph/0702236",
    "If true: DE emerges late as a heavy partner decouples; rho_DE set by a ratio of two scales.",
    dict(zs=1, p=1.5, n=0), density=True)


def _rydberg(eps, zinf, sig):
    ns = np.arange(2, 13)
    zn = (1 + zinf) * (1 - 1 / ns ** 2) - 1
    wn = ns ** -3.0

    def G(z):
        z = _z(z)
        return 1 + eps * np.sum(wn * 0.5 * (1 - np.tanh((z[..., None] - zn) / sig)), axis=-1)
    return lambda z: G(z) / G(0.0)


add("Rydberg staircase",
    {"eps": P(0.5, 0.5, -4.0, 20.0), "zinf": P(2.0, 0.5, 0.3, 6.0), "sig": P(0.1, 0.05, 0.02, 0.5)},
    _rydberg, "field-new", "chemistry/particle", f"{H_CH}; hydrogen-like 1/n^2 series",
    "If true: DE has discrete spectral structure (a 'dark atom' with a Rydberg constant).",
    dict(eps=0, zinf=2, sig=0.1), density=True)


def _bateman(A, lam1, r):
    lam2 = r * lam1
    P2 = lambda t: lam1 / (lam2 - lam1) * (np.exp(-lam1 * t) - np.exp(-lam2 * t))  # noqa: E731
    return lambda z: (1 + A * P2((1 / (1 + _z(z))) ** 1.5)) / (1 + A * P2(1.0))


add("Bateman intermediate-daughter DE",
    {"A": P(0.2, 0.2, -0.95, 3.0), "lam1": P(2.0, 1.0, 0.2, 20.0), "r": P(4.0, 2.0, 1.1, 50.0)},
    _bateman, "field-new", "chemistry/particle", f"{H_CH}; Bateman decay chain A -> B -> C",
    "If true: a dark decay chain; an asymmetric transient with two measurable lifetimes.",
    dict(A=0, lam1=2, r=4), density=True)


# ------------------------------------------------- economics / control / networks ----
H_EC = "docs/batch2-harvest/econ-control-networks.md"


def _lppl_tc(A, ac, m, omega):
    def f(z):
        a = 1.0 / (1.0 + _z(z))
        s = (ac - a) / (ac - 1.0)
        return np.exp(A * (s ** m * (1.0 + 0.5 * np.cos(omega * np.log(s))) - 1.5))
    return f


add("LPPL critical-time DE",
    {"A": P(0.02, 0.05, -0.3, 0.3), "ac": P(1.3, 0.1, 1.1, 3.0), "m": P(0.5, 0.15, 0.1, 1.0),
     "omega": P(8.0, 2.0, 2.0, 20.0)}, _lppl_tc,
    "field-new", "economics/control", f"{H_EC}; Sornette log-periodic power law (bubbles)",
    "If true: DE is a precursor of a future finite-time singularity at a_c (log-periodic residuals).",
    dict(A=0, ac=1.3, m=0.5, omega=8), density=True)


def _pid(r, zs, omega, zeta):
    wd = omega * np.sqrt(1.0 - zeta ** 2)
    k = zeta / np.sqrt(1.0 - zeta ** 2)

    def g(z):
        tau = np.maximum(np.log1p(zs) - np.log1p(_z(z)), 0.0)
        y = 1.0 - np.exp(-zeta * omega * tau) * (np.cos(wd * tau) + k * np.sin(wd * tau))
        return r + (1.0 - r) * y
    return lambda z: g(z) / g(0.0)


add("PID step-response DE",
    {"r": P(0.8, 0.1, 0.3, 2.0), "zs": P(1.5, 0.5, 0.3, 5.0), "omega": P(5.0, 1.0, 1.0, 12.0),
     "zeta": P(0.4, 0.1, 0.2, 0.95)}, _pid,
    "field-known", "economics/control",
    f"{H_EC}; second-order step response; close: damped oscillating DE arXiv:2606.17550",
    "If true: DE is a regulated quantity settling to a setpoint with overshoot and ringing.",
    dict(r=1, zs=1.5, omega=5, zeta=0.4), density=True)


def _avalanche(A, q, L, s0):
    k = np.arange(8)[:, None]
    uk, qk, wd = s0 + k * L, q ** k, 0.25 * L

    def g(z):
        u = np.atleast_1d(np.log1p(_z(z)))[None, :]
        return (qk * 0.5 * (1.0 + np.tanh((uk - u) / (2.0 * wd)))).sum(axis=0)

    def f(z):
        zz = _z(z)
        return ((1.0 + A * g(zz)) / (1.0 + A * g(0.0)[0])).reshape(zz.shape)
    return f


add("Avalanche staircase",
    {"A": P(0.05, 0.05, -0.05, 0.5), "q": P(0.8, 0.1, 0.3, 1.2), "L": P(0.4, 0.1, 0.15, 1.0),
     "s0": P(0.2, 0.1, 0.0, 0.8)}, _avalanche,
    "field-new", "economics/control", f"{H_EC}; self-organised criticality, log-spaced avalanches",
    "If true: the vacuum evolves through a cascade of discrete events with a fixed scale ratio.",
    dict(A=0, q=0.8, L=0.4, s0=0.2), density=True)


def _bs_put(phi, K, v):
    from scipy.special import ndtr

    def Pput(S):
        d1 = (np.log(S / K) + 0.5 * v * v) / v
        return K * ndtr(-(d1 - v)) - S * ndtr(-d1)
    P0 = Pput(1.0)
    return lambda z: 1.0 - phi + phi * np.maximum(Pput((1.0 + _z(z)) ** 3), 0.0) / P0


add("Black-Scholes put-option DE",
    {"phi": P(0.2, 0.1, -0.5, 0.95), "K": P(3.0, 1.0, 1.0, 30.0), "v": P(1.0, 0.3, 0.1, 3.0)},
    _bs_put, "field-new", "economics/control", f"{H_EC}; European put on rho_m (zero rate)",
    "If true: part of DE is a functional of the matter density, turning off when rho_m > strike.",
    dict(phi=0, K=3, v=1), density=True)


def _riccati(eps, Nc, phi):
    kap = phi * PI / (Nc + 7.0)
    return lambda z: (np.sin(kap * (Nc + np.log1p(_z(z)))) / np.sin(kap * Nc)) ** (3.0 * eps)


add("Riccati fold sine-power DE",
    {"eps": P(0.03, 0.02, -0.15, 0.15), "Nc": P(0.5, 0.2, 0.1, 3.0), "phi": P(0.3, 0.1, 0.01, 0.9)},
    _riccati, "field-new", "economics/control", f"{H_EC}; saddle-node (fold) normal form",
    "If true: DE approaches a finite-time singularity N_c e-folds in the future (tipping point).",
    dict(eps=0, Nc=0.5, phi=0.3), density=True)


def _cusp(A, zf, s):
    HF = 2.0 / (3.0 * np.sqrt(3.0))

    def x(z):
        z = _z(z)
        c = 1.5 * np.sqrt(3.0) * HF * (1.0 - s * np.log((1.0 + z) / (1.0 + zf)))
        low_tr = (2 / np.sqrt(3)) * np.cos(np.arccos(np.clip(c, -1, 1)) / 3.0 - 4 * PI / 3)
        low_ch = -(2 / np.sqrt(3)) * np.cosh(np.arccosh(np.maximum(-c, 1.0)) / 3.0)
        lower = np.where(c >= -1.0, low_tr, low_ch)
        upper = (2 / np.sqrt(3)) * np.cosh(np.arccosh(np.maximum(c, 1.0)) / 3.0)
        return np.where(z > zf, lower, upper)
    return lambda z: (1.0 + A * x(z)) / (1.0 + A * x(0.0))


add("Cusp-catastrophe hysteresis jump",
    {"A": P(0.05, 0.05, -0.4, 0.4), "zf": P(0.6, 0.3, 0.1, 2.5), "s": P(0.5, 0.2, 0.05, 2.0)},
    _cusp, "field-new", "economics/control", f"{H_EC}; cusp catastrophe, fold jump",
    "If true: a hysteretic first-order jump in DE at a fold, with a fixed jump-to-drift ratio.",
    dict(A=0, zf=0.6, s=0.5), density=True)


def _perc_kuramoto(phi, zc, beta):
    ac = 1.0 / (1.0 + zc)
    return lambda z: 1.0 - phi + phi * (np.maximum(1.0 / (1.0 + _z(z)) - ac, 0.0) / (1.0 - ac)) ** beta


add("Percolation-Kuramoto order parameter",
    {"phi": P(0.2, 0.1, -1.0, 0.95), "zc": P(1.0, 0.3, 0.1, 3.0), "beta": P(0.5, 0.15, 0.1, 2.5)},
    _perc_kuramoto, "field-new", "economics/control",
    f"{H_EC}; network giant component / Kuramoto synchronisation onset in a. Merged with the "
    "geoscience harvest's 'Percolation-onset DE' (same family after normalising f(0) = 1; "
    "beta hi 1.5 -> 2.5 covers its exponent range)",
    "If true: DE is an emergent collective phase; the fitted exponent names a universality class.",
    dict(phi=0, zc=1, beta=0.5), density=True)


def _inv_gauss(phi, m, lam):
    from scipy.special import ndtr

    def F(t):
        return (ndtr(np.sqrt(lam / t) * (t / m - 1.0))
                + np.exp(2.0 * lam / m) * ndtr(-np.sqrt(lam / t) * (t / m + 1.0)))
    return lambda z: 1.0 - phi + phi * F((1.0 + _z(z)) ** -1.5) / F(1.0)


add("First-passage emergence",
    {"phi": P(0.2, 0.1, -0.5, 0.95), "m": P(1.0, 0.3, 0.1, 5.0), "lam": P(0.5, 0.2, 0.01, 5.0)},
    _inv_gauss, "field-new", "economics/control", f"{H_EC}; inverse-Gaussian first-passage CDF",
    "If true: DE emergence is a stochastic barrier-crossing event with skewed arrival times.",
    dict(phi=0, m=1, lam=0.5), density=True)


def _gompertz_u(b, gam, rho):
    return lambda z: np.exp(-b * (np.expm1(gam * np.log1p(_z(z))) / gam + rho * np.log1p(_z(z))))


add("Gompertz hazard in lookback e-folds",
    # start gam = 0.5 (harvest: 1.5): at 1.5 the density underflows to 0 at z ~ 1100, failing
    # the pre-registered positivity gate; range unchanged.
    {"b": P(0.05, 0.05, 0.0, 3.0), "gam": P(0.5, 0.5, 0.3, 3.0), "rho": P(0.0, 0.3, -1.0, 1.0)},
    _gompertz_u, "field-new", "economics/control", f"{H_EC}; Gompertz-Makeham actuarial law",
    "If true: DE is a 'survivor' with a hazard rising into the past: sharply emergent, no early DE.",
    dict(b=0, gam=0.5, rho=0), density=True)


def _omori_cusp(A, am, c, p):
    def g(a):
        return (c / (np.abs(a - am) + c)) ** p
    g1 = g(1.0)
    return lambda z: np.exp(A * (g(1.0 / (1.0 + _z(z))) - g1))


add("Omori-Utsu fore/aftershock cusp",
    {"A": P(0.1, 0.1, -1.0, 1.0), "am": P(0.7, 0.1, 0.3, 0.95), "c": P(0.1, 0.05, 0.02, 0.5),
     "p": P(1.0, 0.3, 0.3, 1.5)}, _omori_cusp,
    "field-new", "economics/control", f"{H_EC}; Omori-Utsu / Hawkes self-exciting processes",
    "If true: a single 'cosmic quake' at z_m with scale-free power-law wings.",
    dict(A=0, am=0.7, c=0.1, p=1), density=True)


# ------------------------------------------------- geoscience / fluids / materials ----
H_GEO = "docs/batch2-harvest/geoscience-fluids-materials.md"


def _omori_cum(A, te, c, q, Om):
    def N(t):
        L = np.log1p(np.maximum(t - te, 0.0) / c)
        return L if abs(q) < 1e-9 else np.expm1(q * L) / q
    t0 = _t_cosmic(0.0, Om)
    return lambda z: (1 + A * N(_t_cosmic(z, Om))) / (1 + A * N(t0))


add("Omori aftershock DE",
    {"A": P(0.3, 0.3, -0.05, 5.0), "te": P(0.5, 0.15, 0.05, 0.9), "c": P(0.2, 0.1, 0.02, 2.0),
     "q": P(0.0, 0.3, -1.5, 0.9)}, _omori_cum,
    "field-new", "geoscience/fluids", f"{H_GEO}; Omori-Utsu cumulative aftershock count",
    "If true: DE is the tail of one dated 'mainshock' plus a universal power-law relaxation.",
    dict(A=0, te=0.5, c=0.2, q=0), density=True, uses_om=True)


def _colecole(A, xs, al, Om):
    ca = np.cos(al * PI / 2)

    def D(e):
        s = (e / xs) ** al
        return (1 + s * ca) / (1 + 2 * s * ca + s * s)
    return lambda z: (1 + A * D(_E_ref(z, Om))) / (1 + A * D(1.0))


add("Cole-Cole Hubble-rate dispersion",
    {"A": P(0.3, 0.3, -0.9, 5.0), "xs": P(2.0, 1.0, 0.5, 8.0), "al": P(0.7, 0.2, 0.1, 1.0)},
    _colecole, "field-new", "geoscience/fluids",
    f"{H_GEO}; Cole-Cole dielectric relaxation (nested in Havriliak-Negami with beta = 1)",
    "If true: DE is the static response of a dissipative medium driven by H (relaxation at ~H0).",
    dict(A=0, xs=2, al=0.7), density=True, uses_om=True)


def _lorentz(A, xr, Q, Om):
    chi = lambda e: (1 - (e / xr) ** 2) / ((1 - (e / xr) ** 2) ** 2 + (e / (xr * Q)) ** 2)  # noqa: E731
    return lambda z: (1 + A * chi(_E_ref(z, Om))) / (1 + A * chi(1.0))


add("Lorentz-resonance DE",
    {"A": P(0.1, 0.1, -0.3, 0.3), "xr": P(1.5, 0.3, 1.0, 3.0), "Q": P(2.0, 1.0, 0.3, 4.0)},
    _lorentz, "field-new", "geoscience/fluids", f"{H_GEO}; driven damped oscillator, tidal resonance",
    "If true: a dark mode with natural rate ~H0 (mass ~1e-33 eV); phantom crossing = resonance dip.",
    dict(A=0, xr=1.5, Q=2), density=True, uses_om=True)


def _andrade(A, n, gam, Om):
    g = lambda t: t ** n + gam * t  # noqa: E731
    t0 = _t_cosmic(0.0, Om)
    return lambda z: (1 + A * g(_t_cosmic(z, Om))) / (1 + A * g(t0))


add("Andrade creep of space",
    {"A": P(0.3, 0.3, -0.3, 3.0), "n": P(0.333, 0.15, 0.05, 1.5), "gam": P(0.2, 0.2, 0.0, 1.0)},
    _andrade, "field-new", "geoscience/fluids", f"{H_GEO}; Andrade transient creep (n ~ 1/3)",
    "If true: the vacuum has a rheology with a transient creep exponent (n = 1/3 would be striking).",
    dict(A=0, n=0.333, gam=0.2), density=True, uses_om=True)


def _stickslip(A, om, ph, s):
    S = lambda psi: np.arctan2(s * np.sin(psi), 1 - s * np.cos(psi))  # noqa: E731
    psi = lambda z: om * np.log1p(_z(z)) + ph  # noqa: E731
    return lambda z: (1 + A * S(psi(z))) / (1 + A * S(psi(0.0)))


add("Stick-slip sawtooth DE",
    {"A": P(0.2, 0.2, -0.4, 0.4), "om": P(4.0, 1.5, 0.5, 12.0), "ph": P(0.0, 1.0, -PI, PI),
     "s": P(0.5, 0.3, -0.85, 0.85)}, _stickslip,
    "field-new", "geoscience/fluids",
    f"{H_GEO}; stick-slip / glacial sawtooth; s = 0 limit ~ Linder astro-ph/0511415",
    "If true: DE is a relaxation oscillator (slow load, fast slip), periodic in ln(1+z).",
    dict(A=0, om=4, ph=0, s=0.5), density=True)


def _nwave(A, zc, sig, B):
    def w(z):
        xi = _z(z) - zc
        g = np.exp(-(xi / sig) ** 2)
        return -1 + A * xi * g / (g + B)
    return w


add("Burgers N-wave in w",
    {"A": P(-0.3, 0.3, -1.5, 1.5), "zc": P(0.5, 0.2, 0.05, 2.0), "sig": P(0.5, 0.2, 0.1, 2.0),
     "B": P(1.0, 0.5, 0.05, 20.0)}, _nwave,
    "field-new", "geoscience/fluids", f"{H_GEO}; viscous Burgers N-wave (Cole-Hopf)",
    "If true: one exact phantom crossing as a localised odd 'shock' in w, zero net effect early.",
    dict(A=0, zc=0.5, sig=0.5, B=1))


def _cascade(B, q, Om):
    kH = lambda z: _E_ref(z, Om) / (1 + _z(z))  # noqa: E731
    return lambda z: (B + kH(z) ** (-q)) / (B + 1.0)


add("Comoving-horizon Kolmogorov cascade",
    {"B": P(1.0, 1.0, 0.0, 20.0), "q": P(0.667, 0.3, -1.0, 4.0)}, _cascade,
    "field-new", "geoscience/fluids", f"{H_GEO}; turbulent inertial-range energy above k = aH",
    "If true: DE follows the comoving Hubble scale and peaks at the acceleration onset (z ~ 0.6).",
    dict(B=1, q=0), density=True, uses_om=True)


def _adler_ghost(A, wr, r, tc, Om):
    s = np.sqrt(1 - r * r)

    def cth(t):
        u = r + s * np.tan(0.5 * wr * s * (t - tc))
        return (1 - u * u) / (1 + u * u)
    t0 = _t_cosmic(0.0, Om)
    return lambda z: (1 + A * cth(_t_cosmic(z, Om))) / (1 + A * cth(t0))


add("Adler ghost-bottleneck DE",
    {"A": P(0.2, 0.2, -0.5, 0.5), "wr": P(3.0, 1.5, 0.5, 12.0), "r": P(0.8, 0.2, 0.0, 0.98),
     "tc": P(0.5, 0.4, -1.0, 2.0)}, _adler_ghost,
    "field-new", "geoscience/fluids",
    f"{H_GEO}; saddle-node ghost / phase slip in cosmic time (biology's Adler model uses ln(1+z))",
    "If true: near-Lambda for most of history, then one late phase slip; the next slip is predicted.",
    dict(A=0, wr=3, r=0.8, tc=0.5), density=True, uses_om=True)


def _jmak_t(B, tau, n, Om):
    X = lambda t: -np.expm1(-(t / tau) ** n)  # noqa: E731
    t0 = _t_cosmic(0.0, Om)
    return lambda z: (1 + B * X(_t_cosmic(z, Om))) / (1 + B * X(t0))


add("JMAK vacuum conversion in cosmic time",
    {"B": P(0.3, 0.3, -0.9, 9.0), "tau": P(0.8, 0.3, 0.05, 5.0), "n": P(1.5, 0.5, 0.2, 4.0)},
    _jmak_t, "field-known", "geoscience/fluids",
    f"{H_GEO}; JMAK/Stefan growth; partly known: arXiv:2605.30259 late vacuum decay. Merged "
    "with the signals harvest's 'Glassy KWW relaxation clock' (same family: A = -B/(1+B), tau "
    "rescaled by t0; n lo 0.5 -> 0.2 and B hi 5 -> 9 cover its range)",
    "If true: a late first-order vacuum transition percolating now; n names the growth mechanism.",
    dict(B=0, tau=0.8, n=1.5), density=True, uses_om=True)


# ------------------------------------------------- information / thermo / computation / ML ----
H_INF = "docs/batch2-harvest/information-thermo-computation-ml.md"


add("Hajek log-cooling DE",
    {"A": P(0.1, 0.1, -0.05, 5.0), "ts": P(0.5, 0.3, 0.01, 10.0)},
    lambda A, ts: (lambda z: 1 + A * (np.log1p(1 / ts) / np.log1p((1 + _z(z)) ** -1.5 / ts) - 1)),
    "field-new", "information/ML", f"{H_INF}; Hajek logarithmic annealing schedule",
    "If true: DE is the leftover 'temperature' of a slow optimisation; it never freezes out.",
    dict(A=0, ts=0.5), density=True)


def _double_descent(A, zc, eps):
    R = lambda r: np.minimum(r, 1.0) / np.sqrt((1 - r) ** 2 + eps ** 2)  # noqa: E731
    return lambda z: 1 + A * (R((1 + _z(z)) / (1 + zc)) / R(1 / (1 + zc)) - 1)


add("Double-descent interpolation peak",
    {"A": P(0.2, 0.2, -0.3, 0.95), "zc": P(1.0, 0.4, 0.1, 3.0), "eps": P(0.3, 0.1, 0.1, 1.0)},
    _double_descent, "field-new", "information/ML", f"{H_INF}; double-descent risk curve",
    "If true: a threshold-like cusp episode in DE at z_c with asymmetric power-law wings.",
    dict(A=0, zc=1, eps=0.3), density=True)


add("Shannon-Hartley wideband saturation",
    {"A": P(0.1, 0.1, -0.1, 3.0), "b": P(3.0, 2.0, 0.01, 30.0), "p": P(1.5, 0.5, 0.3, 3.0)},
    lambda A, b, p: (lambda z: 1 + A * ((1 + _z(z)) ** p * np.log1p(b * (1 + _z(z)) ** -p)
                                        / np.log1p(b) - 1)),
    "field-new", "information/ML", f"{H_INF}; channel capacity with bandwidth ~ H",
    "If true: the vacuum energy is capped by a signal-to-noise ceiling, not a potential.",
    dict(A=0, b=3, p=1.5), density=True)


add("Jarzynski rare-event emergent DE",
    {"A": P(0.2, 0.2, -3.0, 0.99), "b": P(3.0, 2.0, 0.01, 100.0)},
    lambda A, b: (lambda z: 1 + A * (np.log1p(b * (1 + _z(z))) / (1 + _z(z)) / np.log1p(b) - 1)),
    "field-new", "information/ML", f"{H_INF}; Jarzynski equality, exponential work distribution",
    "If true: DE is a non-equilibrium free-energy gap set by fluctuation statistics.",
    dict(A=0, b=3), density=True)


def _saddle_stair(A, z1, Dl, dl):
    wk = np.array([1, 2, 4, 8]) / 15
    Lk = np.log1p(z1) + Dl * np.arange(4)
    S = lambda L: (wk * 0.5 * (1 - np.tanh((_z(L)[..., None] - Lk) / dl))).sum(-1)  # noqa: E731
    return lambda z: 1 + A * (S(np.log1p(_z(z))) - S(0.0))


add("Saddle-to-saddle staircase",
    {"A": P(0.2, 0.2, -3.0, 0.99), "z1": P(0.3, 0.2, 0.02, 3.0), "Dl": P(0.6, 0.3, 0.1, 2.0),
     "dl": P(0.15, 0.1, 0.03, 0.6)}, _saddle_stair,
    "field-new", "information/ML",
    f"{H_INF}; Saxe+ deep-linear-net learning (arXiv:1312.6120); partial: arXiv:2208.05583",
    "If true: DE is a multi-stage relaxation with geometrically spaced, hierarchy-weighted steps.",
    dict(A=0, z1=0.3, Dl=0.6, dl=0.15), density=True)


def _cyc(A, T0, m):
    def f(z):
        s = np.log1p(_z(z)) / T0
        k = np.floor(np.log1p(s * (m - 1)) / np.log(m))
        u = (s - (m ** k - 1) / (m - 1)) / m ** k
        return 1 + A * 0.5 * (1 - np.cos(2 * PI * u))
    return f


add("Doubling-period cyclical schedule",
    {"A": P(0.3, 0.2, -0.9, 3.0), "T0": P(0.5, 0.3, 0.3, 3.0), "m": P(2.0, 0.5, 1.2, 4.0)},
    _cyc, "field-new", "information/ML", f"{H_INF}; SGDR warm-restart learning-rate schedules",
    "If true: DE cycles with self-similar, ever longer periods; acceleration recurs.",
    dict(A=0, T0=0.5, m=2), density=True)


add("Dyadic-map chirp",
    {"A": P(0.2, 0.2, -0.9, 0.9), "th": P(0.5, 0.3, 0.05, 3.2), "k": P(1.0, 0.4, 0.2, 2.0)},
    lambda A, th, k: (lambda z: 1 + A * (np.sin(th * (1 + _z(z)) ** k) ** 2 - np.sin(th) ** 2)),
    "field-new", "information/ML", f"{H_INF}; solvable logistic map at r = 4",
    "If true: a chaotic, bounded vacuum history (a sanity test of how sparsely data sample z).",
    dict(A=0, th=0.5, k=1), density=True)


add("Fold-bifurcation tipping DE",
    {"A": P(0.5, 0.3, -0.5, 10.0), "d": P(0.5, 0.3, 0.02, 3.0)},
    lambda A, d: (lambda z: (1 + A * np.sqrt(1 + d - 1 / (1 + _z(z)))) / (1 + A * np.sqrt(d))),
    "field-new", "information/ML", f"{H_INF}; saddle-node square-root law; cousin arXiv:2502.20430",
    "If true: the vacuum approaches a tipping point at a_c = 1 + d (end of acceleration or rip).",
    dict(A=0, d=0.5), density=True)


def _levin(A, s, eps, Om):
    q = np.sqrt((1 - Om) / Om)
    clock = lambda z: np.arcsinh(q * (1 + _z(z)) ** -1.5)  # noqa: E731
    x = lambda z: clock(z) / clock(0.0)  # noqa: E731
    g = lambda z: 1 / ((x(z) + s) * np.log(np.e + x(z) / s) ** (1 + eps))  # noqa: E731
    return lambda z: 1 + A * (g(z) / g(0.0) - 1)


add("Levin-Chaitin universal-prior clock",
    {"A": P(0.1, 0.1, 0.0, 3.0), "s": P(0.1, 0.1, 0.01, 3.0), "eps": P(0.5, 0.3, 0.0, 2.0)},
    _levin, "field-new", "information/ML", f"{H_INF}; Levin/Chaitin algorithmic prior",
    "If true: the energy budget tracks the algorithmic prior weight of the current epoch.",
    dict(A=0, s=0.1, eps=0.5), density=True, uses_om=True)


def _kl_gain(A, lk, q):
    K = lambda x: np.log1p(x) - x / (1 + x)  # noqa: E731
    return lambda z: 1 + A * (K(10 ** lk * (1 + _z(z)) ** (-q)) / K(10 ** lk) - 1)


add("Self-evidencing KL information gain",
    {"A": P(0.2, 0.2, -3.0, 0.99), "lk": P(1.0, 1.0, -1.0, 4.0), "q": P(1.0, 0.5, 0.1, 3.0)},
    _kl_gain, "field-new", "information/ML", f"{H_INF}; Gaussian Bayesian KL information gain",
    "If true: DE tracks accumulated information gain (emergent, phantom-like, never saturates).",
    dict(A=0, lk=1, q=1), density=True)


# ------------------------------------------------- pure math / math phys / quantum ----
H_MA = "docs/batch2-harvest/math-physics-quantum.md"


def _mittag(A, s, al, zi):
    import math
    g = math.gamma(1 + al)
    M = lambda u: 1.0 / (1.0 + u ** al / g)  # noqa: E731

    def f(z):
        u = s * np.log((1 + zi) / (1 + np.minimum(_z(z), zi)))
        return (1 + A * M(u)) / (1 + A * M(s * np.log(1 + zi)))
    return f


add("Mittag-Leffler memory relaxation",
    {"A": P(0.3, 0.2, -0.9, 5.0), "s": P(1.0, 0.3, 0.05, 20.0), "al": P(0.7, 0.1, 0.15, 1.0),
     "zi": P(5.0, 1.0, 3.0, 1100.0)}, _mittag,
    "field-new", "math/quantum",
    f"{H_MA}; fractional relaxation (Mainardi approximation); fractional cosmology family "
    "arXiv:2207.00878 modifies the equations instead",
    "If true: DE relaxes with a power-law memory of an early kick; w set by a fractional order.",
    dict(A=0, s=1, al=0.7, zi=5), density=True)

_GAM = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062])


def _riemann(A, m, phi, s):
    W = _GAM[0] / _GAM

    def S(z):
        x = np.log1p(_z(z))
        return np.exp(-m * x) * (W * np.cos(s * _GAM * x[..., None] + phi)).sum(-1)
    return lambda z: 1 + A * (S(z) - S(0.0))


add("Riemann-zero log-periodic Lambda",
    {"A": P(0.02, 0.02, -0.12, 0.12), "m": P(0.5, 0.3, 0.0, 3.0), "phi": P(0.0, 1.0, -PI, PI),
     "s": P(0.3, 0.05, 0.05, 2.0)}, _riemann,
    "field-new", "math/quantum", f"{H_MA}; Berry-Keating xp, first five Riemann zeros",
    "If true: the vacuum carries fixed log-periodic frequency ratios 1:1.49:1.77:2.15:2.33.",
    dict(A=0, m=0.5, phi=0, s=0.3), density=True)


def _weierstrass(A, D, b):
    n = np.arange(-6, 7)

    def W(z):
        x = np.log1p(_z(z))[..., None]
        return ((1 - np.cos(b ** n * x)) / b ** ((2 - D) * n)).sum(-1)
    return lambda z: 1 + A * W(z)


add("Weierstrass-Mandelbrot fractal Lambda",
    {"A": P(0.02, 0.03, -0.15, 0.15), "D": P(1.5, 0.1, 1.05, 1.9), "b": P(2.0, 0.3, 1.5, 6.0)},
    _weierstrass, "field-new", "math/quantum", f"{H_MA}; Berry & Lewis 1980",
    "If true: DE is self-similar in e-fold time with a measurable fractal dimension D.",
    dict(A=0, D=1.5, b=2), density=True)


def _binomial(A, p, L):
    def f(z):
        r = np.clip(np.log1p(_z(z)) / L, 0.0, 1 - 1e-12)
        F = np.zeros_like(r)
        m = np.ones_like(r)
        for _ in range(12):
            r = 2 * r
            bit = np.floor(r)
            r = r - bit
            F = F + np.where(bit == 1, m * p, 0.0)
            m = m * np.where(bit == 1, 1 - p, p)
        return 1 + A * (F + m * r)
    return f


add("Binomial-cascade singular DE",
    {"A": P(0.2, 0.1, -0.9, 2.0), "p": P(0.35, 0.08, 0.02, 0.98), "L": P(2.0, 0.4, 0.3, 7.0)},
    _binomial, "field-new", "math/quantum",
    f"{H_MA}; binomial p-model multifractal staircase. Merged with the signals harvest's "
    "'Binomial-cascade staircase' (same algorithm at depth 6; this one uses depth 12)",
    "If true: DE evolves on a fractal set of epochs (w = -1 almost everywhere).",
    dict(A=0, p=0.35, L=2), density=True)


def _zeno(B, G, sz):
    Pz = lambda s: np.exp(-G * (s - sz * np.log1p(s / sz)))  # noqa: E731
    return lambda z: (1 + B * Pz((1 + _z(z)) ** -1.5)) / (1 + B * Pz(1.0))


add("Zeno-frozen metastable decay",
    {"B": P(0.3, 0.2, -0.9, 5.0), "G": P(2.0, 0.5, 0.0, 20.0), "sz": P(0.3, 0.1, 0.02, 5.0)},
    _zeno, "field-known", "math/quantum",
    f"{H_MA}; quantum Zeno regime; close: Szydlowski+ arXiv:1704.05364",
    "If true: a metastable vacuum whose decay switched on after a Zeno time.",
    dict(B=0, G=2, sz=0.3), density=True)


def _eisenstein(c, y0, kap):
    n = np.arange(1, 9)
    s3 = np.array([sum(d ** 3 for d in range(1, k + 1) if k % d == 0) for k in n], dtype=float)

    def H(y):
        Y = np.maximum(y, 1.0 / y)
        q = np.exp(-2 * PI * Y)
        return Y ** 2 * (1 + 240 * (s3 * q[..., None] ** n).sum(-1))
    return lambda z: (c + H(y0 * (1 + _z(z)) ** (-kap))) / (c + H(np.asarray(y0, dtype=float)))


add("Modular Eisenstein vacuum energy",
    {"c": P(2.0, 1.0, 0.0, 50.0), "y0": P(1.2, 0.2, 0.3, 5.0), "kap": P(0.05, 0.03, -0.3, 0.3)},
    _eisenstein, "field-known", "math/quantum",
    f"{H_MA}; weight-4 Eisenstein series; concept: modular quintessence arXiv:2506.02731",
    "If true: DE is a duality-invariant function of a modulus with a self-dual epoch.",
    dict(c=2, y0=1.2, kap=0), density=True)


def _bkt_late(A, xc, b):
    def s(x):
        d = np.maximum(xc - _z(x), 0.0)
        return np.where(d > 0, np.exp(-b / np.sqrt(np.where(d > 0, d, 1.0))), 0.0)
    return lambda z: (1 + A * s(np.log1p(_z(z)))) / (1 + A * s(0.0))


add("BKT late switch-on in e-folds",
    {"A": P(0.3, 0.2, -0.9, 5.0), "xc": P(0.7, 0.2, 0.1, 3.0), "b": P(0.5, 0.2, 0.01, 5.0)},
    _bkt_late, "field-new", "math/quantum",
    f"{H_MA}; BKT essential singularity (switches on at LOW z; the condensed-matter BKT model "
    "switches on at high z)",
    "If true: the late DE rise is a topological ordering transition with essential scaling.",
    dict(A=0, xc=0.7, b=0.5), density=True)


def _kerr(A, nbar, chi):
    C = lambda x: np.exp(nbar * (np.cos(chi * x) - 1)) * np.cos(nbar * np.sin(chi * x))  # noqa: E731
    return lambda z: 1 + A * (C(np.log1p(_z(z))) - 1)


add("Kerr collapse-revival vacuum",
    {"A": P(0.1, 0.1, -0.45, 0.45), "nbar": P(3.0, 1.0, 0.1, 30.0), "chi": P(1.0, 0.3, 0.05, 8.0)},
    _kerr, "field-new", "math/quantum", f"{H_MA}; Kerr-medium coherent-state autocorrelation",
    "If true: DE is a quantum object with collapse and exact revivals in e-fold time.",
    dict(A=0, nbar=3, chi=1), density=True)


def _fibonacci(A, ell, kap):
    gold = (1 + 5 ** 0.5) / 2
    n = np.arange(1, 161)
    xn = ell * (n + kap * np.floor(n / gold + 0.5))

    def S(z):
        x = np.log1p(_z(z))[..., None]
        return (0.5 * (1 + np.tanh((x - xn) / 0.03))).sum(-1)
    return lambda z: 1 + A * ell * (S(z) - S(0.0))


add("Fibonacci-chain epoch staircase",
    {"A": P(0.02, 0.03, -0.12, 0.12), "ell": P(0.3, 0.05, 0.05, 2.0), "kap": P(0.5, 0.2, 0.0, 3.0)},
    _fibonacci, "field-new", "math/quantum", f"{H_MA}; quasicrystal cut-and-project chain",
    "If true: DE changes in quasi-ordered steps with golden-ratio epoch spacing.",
    dict(A=0, ell=0.3, kap=0.5), density=True)


add("Page-curve cusp Lambda",
    {"A": P(0.05, 0.05, -0.15, 0.15), "xp": P(0.5, 0.2, 0.05, 3.0), "dl": P(0.1, 0.05, 0.01, 1.0)},
    lambda A, xp, dl: (lambda z: 1 + A * ((xp - np.sqrt((np.log1p(_z(z)) - xp) ** 2 + dl ** 2))
                                          - (xp - np.sqrt(xp ** 2 + dl ** 2)))),
    "field-new", "math/quantum", f"{H_MA}; Page curve of horizon entanglement entropy",
    "If true: DE turns over at a horizon 'Page time' (weak: a kinked bump).",
    dict(A=0, xp=0.5, dl=0.1), density=True)


# ------------------------------------------------- signals / nonlinear dynamics ----
H_SIG = "docs/batch2-harvest/signal-nonlinear-dynamics.md"


add("Box-Cox chirp in w",
    {"A": P(0.10, 0.05, 0.0, 1.0), "th": P(2.0, 0.5, 0.2, 4.0), "p": P(0.30, 0.10, 0.05, 0.60),
     "phi0": P(0.0, 1.0, -PI, PI)},
    lambda A, th, p, phi0: (lambda z: -1 + A * np.cos(phi0 + th * np.expm1(p * np.log1p(_z(z))) / p)),
    "field-new", "signals/dynamics",
    f"{H_SIG}; radar/GW chirp; fixed-frequency oscillating w known (arXiv:2404.00181)",
    "If true: an oscillating DE whose frequency drifts: a 'ringing' field with time-varying mass.",
    dict(A=0, th=2, p=0.3, phi0=0))


def _sl_hopf(mu, s, om, b):
    def w(z):
        tau = -np.log1p(_z(z))
        e = np.exp(2 * mu * tau)
        den = s * e + 1 - s
        u = mu * s * e / den
        return -1 + np.sqrt(u) * np.cos(om * tau + 0.5 * b * np.log(den))
    return w


add("Stuart-Landau Hopf cycle in w",
    {"mu": P(0.25, 0.10, 0.01, 1.0), "s": P(0.30, 0.20, 0.0, 1.0), "om": P(3.0, 1.0, 0.2, 12.0),
     "b": P(0.0, 1.0, -6.0, 6.0)}, _sl_hopf,
    "field-new", "signals/dynamics", f"{H_SIG}; supercritical Hopf normal form (exact solution)",
    "If true: DE is a limit cycle born at a Hopf bifurcation, with an onset redshift.",
    dict(mu=0.25, s=0, om=3, b=0))


def _cnoidal(A, om, m, phi):
    from scipy.special import ellipj
    return lambda z: -1 + A * ellipj(om * np.log1p(_z(z)) + phi, m)[1]


add("Cnoidal wave in w",
    {"A": P(0.10, 0.05, 0.0, 1.0), "om": P(3.0, 1.0, 0.3, 12.0), "m": P(0.5, 0.2, 0.0, 0.999),
     "phi": P(0.0, 1.0, -PI, PI)}, _cnoidal,
    "field-new", "signals/dynamics", f"{H_SIG}; KdV cnoidal wave / Jacobi cn",
    "If true: a strongly anharmonic DE oscillator (harmonics measure its self-interaction).",
    dict(A=0, om=3, m=0.5, phi=0))


add("Gabor atom in w",
    {"A": P(0.10, 0.05, -1.0, 1.0), "xc": P(0.40, 0.15, 0.05, 2.0), "sg": P(0.40, 0.15, 0.10, 1.5),
     "k": P(6.0, 2.0, 1.0, 20.0)},
    lambda A, xc, sg, k: (lambda z: -1 + A * np.exp(-0.5 * ((np.log1p(_z(z)) - xc) / sg) ** 2)
                          * np.cos(k * (np.log1p(_z(z)) - xc))),
    "field-known", "signals/dynamics",
    f"{H_SIG}; Gabor/Morlet atom; partly known: wavelet w(z) arXiv:0912.4843",
    "If true: one localised wave packet in w: a transient dynamical episode in DE.",
    dict(A=0, xc=0.4, sg=0.4, k=6))


def _cheby(A, eps, n, xc):
    def w(z):
        x = np.log1p(_z(z)) / xc
        Tn = np.where(x <= 1.0, np.cos(n * np.arccos(np.minimum(x, 1.0))),
                      np.cosh(n * np.arccosh(np.maximum(x, 1.0))))
        return -1 + A / np.sqrt(1.0 + (eps * Tn) ** 2)
    return w


add("Chebyshev equiripple DE",
    {"A": P(0.10, 0.05, -1.0, 1.0), "eps": P(0.5, 0.2, 0.05, 1.5), "n": P(2.5, 0.7, 1.2, 8.0),
     "xc": P(1.0, 0.4, 0.2, 3.0)}, _cheby,
    "field-new", "signals/dynamics", f"{H_SIG}; Chebyshev type-I low-pass filter response",
    "If true: DE is an n-mode composite: equal ripples below a cutoff, off above it.",
    dict(A=0, eps=0.5, n=2.5, xc=1))


def _airy_w(A, s, xt):
    from scipy.special import airy
    return lambda z: -1 + A * airy(s * (np.log1p(_z(z)) - xt))[0]


add("Airy turning-point wave",
    {"A": P(0.30, 0.20, -3.0, 3.0), "s": P(3.0, 1.0, 0.5, 10.0), "xt": P(0.5, 0.3, 0.0, 3.0)},
    _airy_w, "field-new", "signals/dynamics", f"{H_SIG}; WKB turning point (Airy Ai)",
    "If true: DE has a turning point: evanescent (w = -1) early, oscillating after x_t.",
    dict(A=0, s=3, xt=0.5))


def _delay_hopf(A, gam, d, phi):
    from scipy.special import lambertw
    s = complex(lambertw(-gam, 0)) / d
    return lambda z: -1 + A * np.real(np.exp(-s * np.log1p(_z(z)) + 1j * phi))


add("Delayed-feedback Hopf in w",
    {"A": P(0.10, 0.05, -1.0, 1.0), "gam": P(2.0, 0.5, 1.6, 8.0), "d": P(0.40, 0.15, 0.15, 2.0),
     "phi": P(0.0, 1.0, -PI, PI)}, _delay_hopf,
    "field-new", "signals/dynamics", f"{H_SIG}; delay-differential Hopf (Lambert W roots)",
    "If true: DE responds with a causal lag; growth and frequency tied by one number.",
    dict(A=0, gam=2, d=0.4, phi=0))


def _adler_w(A, mu, om, ph0):
    q = np.sqrt(1 - mu ** 2)

    def w(z):
        ph = ph0 - 0.5 * om * q * np.log1p(_z(z))
        N = mu * np.cos(ph) + q * np.sin(ph)
        D = np.cos(ph)
        return -1 + A * (D ** 2 - N ** 2) / (D ** 2 + N ** 2)
    return w


add("Adler phase-slip in w",
    {"A": P(0.10, 0.05, 0.0, 1.0), "mu": P(0.5, 0.2, 0.0, 0.98), "om": P(3.0, 1.0, 0.3, 15.0),
     "ph0": P(0.0, 0.5, -PI / 2, PI / 2)}, _adler_w,
    "field-new", "signals/dynamics",
    f"{H_SIG}; Adler / Josephson phase slips applied to w (biology and geoscience Adler models "
    "act on the density, in ln(1+z) and cosmic time)",
    "If true: a phase-locked DE oscillator with dwell-and-slip waveform in w.",
    dict(A=0, mu=0.5, om=3, ph0=0))
