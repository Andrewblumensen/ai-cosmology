# Batch 2 harvest: condensed matter and statistical physics

Harvester: field cluster "condensed matter / statistical physics". 11 ideas. No fit was run; no number below is a result. All `f(z)` are density ratios rho_DE(z)/rho_DE(0) (f(0) = 1 by construction, normalised inside the code). Shapes are meant to be scored by `src/aicosmo/score.py` with `density=True`.

Shared helper (copy once, used by the models marked "uses Om"):

```python
import numpy as np

def _t_cosmic(z, Om):
    """Cosmic time in units of 1/H0 in a reference flat LCDM (matter + Lambda) with the same Om.
    Used only as a clock. Recasting statement: the clock ignores the model's own DE deviation
    (percent-level error on t(z), absorbed by the clock parameters)."""
    a = 1.0 / (1.0 + np.asarray(z, dtype=float))
    OL = 1.0 - Om
    return 2.0 / (3.0 * np.sqrt(OL)) * np.arcsinh(np.sqrt(OL / Om) * a ** 1.5)

def _norm(g):
    return lambda z: g(np.asarray(z, dtype=float)) / g(np.zeros(1))[0]
```

Summary table

| # | Name | Source field | Weirdness | Plausibility | Prior art |
|---|---|---|---|---|---|
| 1 | Log-periodic critical DE | critical phenomena, discrete scale invariance | 5 | 2 | KNOWN (close) |
| 2 | Arcsine-law trap aging | spin-glass aging (Bouchaud trap model) | 4 | 2 | none found |
| 3 | BKT essential-singularity onset | 2D superfluid / XY vortex unbinding | 5 | 2 | none found |
| 4 | Kibble-Zurek frozen order parameter | quench dynamics | 5 | 3 | none found |
| 5 | Havriliak-Negami dispersive vacuum | dielectric relaxation | 5 | 2 | none found |
| 6 | Prethermal time-crystal modulation | Floquet time crystals | 5 | 2 | partial (related, not same) |
| 7 | Reaction-order (Smoluchowski/Vinen) relaxation | vortex-tangle decay, chemical kinetics | 4 | 3 | none found |
| 8 | Void-percolation order parameter | percolation | 4 | 3 | none found |
| 9 | BCS-gap condensation-energy onset | superconductivity | 4 | 2 | KNOWN (concept) |
| 10 | Avrami (JMAK) latent-heat release | first-order transition kinetics | 3 | 3 | KNOWN (concept) |
| 11 | Inverse-log granular compaction | granular glass relaxation | 5 | 2 | none found |

---

### Log-periodic critical DE
- Field and analogy: Systems near a critical point with discrete (not continuous) scale invariance show log-periodic power-law corrections, `1 + A x^{-alpha} cos(omega ln x + phi)` (Sornette; fracture, earthquakes, hierarchical lattices). Here x = 1+z.
- Cosmology story: Suppose the dark-energy density carries a complex critical exponent, so that it breathes with period ln(lambda) in e-folds, with a power-law envelope. Honest analogy: nothing in known physics gives cosmic discrete scale invariance, but the signal is cheap to test and would be striking.
- Form: density f(z).
  ```python
  def lppl(A, alpha, omega, phi):
      def g(z):
          z = np.asarray(z, dtype=float)
          return 1.0 + A * (1.0 + z) ** (-alpha) * np.cos(omega * np.log1p(z) + phi)
      return _norm(g)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.1 | 0.1 | -0.9 | 0.9 |
  | alpha | 0.5 | 0.3 | 0.0 | 4.0 |
  | omega | 4.0 | 2.0 | 0.5 | 12.0 |
  | phi | 0.0 | 1.0 | -3.1416 | 3.1416 |

  LCDM limit: A=0.
- High-z behaviour: bounded. g stays in [1-A, 1+A] (>= 0.1), the oscillation decays as (1+z)^-alpha, so f tends to 1/g(0) for alpha > 0. For alpha = 0 it oscillates forever with ln(1101) = 7 rad of phase times omega (up to 84 rad, about 13 cycles), still bounded; w swings are about A*omega/3 (the cap omega <= 12, A <= 0.9 can hit the |w+1| > 4 flag, a feature of the bounds not a bug).
- Impact if true: a fractal-in-time dark sector, with a preferred scale ratio lambda = exp(2 pi / omega) between successive "events". Would point to hierarchical/discretely self-similar structure in the vacuum, not a smooth field.
- Beyond-background fingerprint: oscillations in the growth rate fsigma8(z) and ISW at the same ln(1+z) period; a matching comb of features in the binned w(z) reconstructions.
- Prior art: query "log-periodic oscillations discrete scale invariance dark energy equation of state arXiv" and "log-periodic dark energy discrete scale invariance cosmological constant oscillation ln a". Found **KNOWN (close)**: Barenboim, Mena Requejo, Quigg, arXiv:astro-ph/0510178 "Observational Constraints on Undulant Cosmologies" (abstract read: dark-energy equation of state oscillating periodically in e-folds of the scale factor). Differences: they oscillate w(a) = -cos(b ln a) with no decay envelope; ours oscillates the density with a power-law envelope and free phase (LPPL form). Also a non-arXiv preprint "Cyclic Tests v2" (academia.edu, not verified, not read in full) proposes rho_de ~ a^lambda cos(Omega ln a + phi); treat as unreviewed. Discrete-scale-invariance background: Sornette cond-mat/9707012 (not cosmology).
- Weirdness 5 / Plausibility 2

### Arcsine-law trap aging
- Field and analogy: In the Bouchaud trap model of spin-glass aging, the probability that a system has not left its trap between waiting time t_w and t_w + t follows the arcsine law (2/pi) arcsin(sqrt(t_w/(t_w+t))) (mean-field exponent mu = 1/2). Dynamics depends on the ratio t/t_w, not on t alone ("full aging").
- Cosmology story: Let the dark-energy density be a fraction of vacuum "domains" still sitting in the traps they fell into at time t_w; the fraction decays with cosmic age by the arcsine law, with a slow t^(-1/2) tail. This is an analogy only; it replaces the exponential relaxation everyone writes with a heavy-tailed one derived from a disordered energy landscape.
- Form: density f(z), uses Om.
  ```python
  def arcsine_aging(A, tw, p, Om):
      def g(z):
          u = (_t_cosmic(z, Om) / tw) ** p
          return 1.0 + A * (2.0 / np.pi) * np.arcsin(1.0 / np.sqrt(1.0 + u))
      return _norm(g)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.1 | 0.2 | -0.9 | 3.0 |
  | tw | 0.5 | 0.3 | 0.02 | 5.0 |
  | p | 1.0 | 0.3 | 0.3 | 3.0 |

  LCDM limit: A=0. Recasting: p generalises t/t_w to (t/t_w)^p (p = 1 is the trap-model law).
- High-z behaviour: t -> 0 so u -> 0 and the arcsine factor -> 1; f tends to (1+A)/g(0). Finite, positive for A > -1.
- Impact if true: dark energy would be a glassy relaxing component with a memory of a "quench" time t_w; the late-time slope is set by a universality class (power-law tail), not a field mass.
- Beyond-background fingerprint: history dependence; the effective w(z) approaches -1 only as a power law, so the apparent w0 depends on survey depth. In the lab: two-time correlation functions would be needed, not available; for cosmology, a growth-rate tail that decays as a power law.
- Prior art: query "Bouchaud trap model aging arcsine law cosmology dark energy". none found (results were all trap-model mathematics: Ben Arous and Cerny arXiv:math/0603340, Bouchaud-model papers arXiv:1008.3855; none cosmological).
- Weirdness 4 / Plausibility 2

### BKT essential-singularity onset
- Field and analogy: At the Berezinskii-Kosterlitz-Thouless transition of a 2D superfluid/XY system, free vortex density above T_KT is `exp(-2b/sqrt(t))` with reduced temperature t = T/T_KT - 1, and exactly zero below. It is a smooth (C-infinity) infinite-order transition with no power-law cusp.
- Cosmology story: A dark sector at temperature T proportional to (1+z) has a vortex-gas contribution to the vacuum energy that switches on in the past of z_k and vanishes identically at later times. So the late universe is exactly LCDM and all deviation lives above z_k, through a gentle essential singularity. Pure analogy; the exponent 1/2 comes from the RG flow of the Coulomb gas.
- Form: density f(z).
  ```python
  def bkt(A, zk, b):
      def f(z):
          z = np.asarray(z, dtype=float)
          t = np.maximum((1.0 + z) / (1.0 + zk) - 1.0, 1e-12)   # reduced temperature, clipped at 0
          return 1.0 + A * np.exp(-b / np.sqrt(t))               # f(0) = 1 exactly for z < zk
      return f
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.1 | 0.2 | -0.9 | 3.0 |
  | zk | 0.5 | 0.3 | 0.05 | 3.0 |
  | b | 1.0 | 0.5 | 0.05 | 10.0 |

  LCDM limit: A=0 (also b large with z_k large).
- High-z behaviour: exp(-b/sqrt(t)) -> 1, so f -> 1 + A, finite and positive (A > -1). No blow-up.
- Impact if true: dark energy is topologically protected until a critical epoch, then switches on with an infinitely smooth onset: the signature of an infinite-order transition, the first of its kind in the dark-energy literature. Requires a 2D-like (layered or brane) dark sector.
- Beyond-background fingerprint: w(z) has zero derivative of every order at z_k (no kink), unlike a first or second-order transition; a universal relation between the width and the onset z_k (single parameter b).
- Prior art: query "Berezinskii-Kosterlitz-Thouless transition vortex unbinding dark energy cosmological constant arXiv". none found (closest: arXiv:2603.13544, BKT in superfluids near black-hole horizons; no dark-energy model).
- Weirdness 5 / Plausibility 2

### Kibble-Zurek frozen order parameter
- Field and analogy: When a system is cooled through a second-order transition at finite rate, the order parameter follows its equilibrium cusp, epsilon^beta, until critical slowing down makes the relaxation time exceed the time left (Kibble-Zurek adiabatic-impulse picture); it then freezes at the value reached at the freeze-out reduced temperature epsilon_hat.
- Cosmology story: Dark energy as the energy of an order parameter that condensed as the dark sector cooled with the CMB (T proportional to 1+z), grew as epsilon^beta, then froze out: late-time dark energy is a constant (Lambda) set by the frozen value, with a recent history of growth. Analogy: Kibble-Zurek is used for defect formation in cosmology, but not for the dark-energy density itself.
- Form: density f(z).
  ```python
  def kz_frozen(A, zc, eh, beta):
      def g(z):
          z = np.asarray(z, dtype=float)
          eps = np.clip(1.0 - (1.0 + z) / (1.0 + zc), 0.0, eh)  # reduced undercooling, frozen at eh
          return 1.0 + A * eps ** beta
      return _norm(g)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.2 | 0.2 | -0.9 | 3.0 |
  | zc | 1.0 | 0.3 | 0.1 | 3.0 |
  | eh | 0.2 | 0.1 | 0.02 | 1.0 |
  | beta | 0.5 | 0.2 | 0.5 | 3.0 |

  LCDM limit: A=0.
- High-z behaviour: for z > z_c epsilon = 0, so f is the constant 1/(1 + A eh^beta) up to z = 1100. Finite, positive for A > -1.
- Impact if true: the late-time acceleration is a frozen relic of a critical transition: Lambda-like today, but with a built-in recent ramp, and the ramp exponent beta would be a universality class (0.5 mean field, 0.33 Ising).
- Beyond-background fingerprint: the frozen epoch (z < z_f = (1+z_c)(1-eh)-1) is exactly LCDM, so growth and lensing are standard today; deviations only at z_f < z < z_c, where a w jump (with beta < 1 a w spike) occurs. For beta < 1, w has an integrable singularity at z_c; the scorer's z <= 3 pathology grid may flag |w+1| > 4 for large A.
- Prior art: query "Kibble-Zurek freeze-out order parameter dark energy late-time acceleration arXiv". none found (KZ papers found: Suzuki and Zurek arXiv:2412.15568, order-parameter dynamics; Zurek-Kibble defect formation gr-qc/9808059; none apply to the dark-energy density).
- Weirdness 5 / Plausibility 3

### Havriliak-Negami dispersive vacuum
- Field and analogy: A dielectric responds to a drive at angular frequency omega with susceptibility `1/(1 + (i omega tau)^alpha)^beta` (Havriliak-Negami; alpha = beta = 1 is Debye, beta = 1 Cole-Cole, alpha = 1 Davidson-Cole). The real part is a smooth dispersion step; the same function has a loss peak in the imaginary part (Kramers-Kronig pair).
- Cosmology story: Treat the expansion rate H as the drive frequency of the vacuum: dark-energy density is a dispersive response rho_DE = rho_inf + Delta Re chi(H tau). The step happens when H tau ~ 1. Analogy only; the "frequency" is a rate, and H is evaluated in a reference LCDM (recasting), not self-consistently.
- Form: density f(z), uses Om.
  ```python
  def hn_vacuum(A, tau, alpha, beta, Om):
      def g(z):
          z = np.asarray(z, dtype=float)
          E = np.sqrt(Om * (1.0 + z) ** 3 + 1.0 - Om)        # reference-LCDM H/H0 as the drive
          return 1.0 + A * np.real((1.0 + (1j * E * tau) ** alpha) ** (-beta))
      return _norm(g)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.2 | 0.2 | -0.9 | 3.0 |
  | tau | 1.0 | 0.5 | 0.05 | 20.0 |
  | alpha | 0.7 | 0.2 | 0.1 | 1.0 |
  | beta | 0.7 | 0.2 | 0.1 | 1.0 |

  LCDM limit: A=0.
- High-z behaviour: with alpha, beta in (0,1] the real part lies in [0,1], so g in [1, 1+A] for A >= 0 (positive for A > -1). At z = 1100, H tau ~ 1e4 tau, the response tends to 0 (power law (H tau)^(-alpha beta)); f -> 1/g(0). Finite.
- Impact if true: dark energy is not a dynamical field but a frequency-dependent material response of the vacuum to the expansion rate; it would imply a dissipative (imaginary) partner by causality.
- Beyond-background fingerprint: Kramers-Kronig demands an absorptive part, i.e. energy exchange between the dark component and matter at the epoch H tau ~ 1: a small dark-sector-matter coupling, visible as a growth-rate (fsigma8) anomaly and a modified matter power spectrum slope at z ~ 0.5-1.
- Prior art: query "Havriliak-Negami Cole-Cole dielectric relaxation dark energy Hubble rate susceptibility cosmology". none found (only dielectric-physics hits, e.g. arXiv:1611.06433, nothing in cosmology).
- Weirdness 5 / Plausibility 2

### Prethermal time-crystal modulation
- Field and analogy: A discrete (Floquet) time crystal responds with a rigid subharmonic oscillation that persists without decay, set by the period of the drive, not by any decay rate.
- Cosmology story: The dark-energy density is Lambda modulated by a rigid sinusoid in cosmic time with period T of order the Hubble time, and the "rigidity" means it does not damp. Different from oscillating scalar fields (which decay as a^-3 and rely on Hubble friction): here the oscillation is imposed in t, so its redshift pattern is chirped.
- Form: density f(z), uses Om.
  ```python
  def time_crystal(A, T, phi, Om):
      def g(z):
          return 1.0 + A * np.cos(2.0 * np.pi * _t_cosmic(z, Om) / T + phi)
      return _norm(g)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.1 | 0.1 | -0.5 | 0.5 |
  | T | 1.5 | 0.5 | 0.5 | 6.0 |
  | phi | 0.0 | 1.0 | -3.1416 | 3.1416 |

  LCDM limit: A=0.
- High-z behaviour: t -> 0 as a^(3/2), so the phase freezes at phi: f tends to the constant (1 + A cos phi)/g(0). Bounded, positive (A <= 0.5). The w excursion near today is about A*2 pi/(3T) (below 4 inside the bounds).
- Impact if true: broken time-translation symmetry in the dark sector, with a clock; the Hubble tension and the DESI preference for evolving w would be rhythmic features, and future surveys should see a repeat.
- Beyond-background fingerprint: periodic modulation of the growth rate and of ISW with period T in cosmic time (not in ln a); a repeating w(z) pattern in a future z > 1.5 reconstruction.
- Prior art: query "time crystal dark energy oscillating cosmological constant cosmic time period arXiv". Related but not the same, so not marked KNOWN: Mersini-Houghton arXiv:2502.08887 "Dark Energy from Time Crystals" (abstract read: a fluid of scalar-field time-crystal bound states acts as phantom dark energy, w <= -1); comment by Cline arXiv:2502.19448; Easson and Vikman arXiv:1607.00996 (scalar field with periodic motion). None proposes a rigid cosmic-time-periodic modulation of Lambda scored against background data. Oscillating-w ("undulant") models are periodic in ln a, not in t.
- Weirdness 5 / Plausibility 2

### Reaction-order (Smoluchowski/Vinen) relaxation
- Field and analogy: Defects that annihilate by m-body reactions obey `dn/dt = -k n^m`: m = 2 is the Vinen decay of a superfluid vortex tangle (n ~ 1/t) and Smoluchowski coagulation; m -> 1 is exponential decay. The solution is `n0 (1 + (m-1) t/tau)^(-1/(m-1))`, the Tsallis q-exponential.
- Cosmology story: Dark energy is a defect-like density (vortex lines, wall junctions) that decays by m-body annihilation in cosmic time, with m a universality-class parameter rather than an assumed exponential. Analogy only; for m < 1 the density hits exactly zero at finite time t = tau/(1-m), after which only Lambda remains.
- Form: density f(z), uses Om.
  ```python
  def reaction_order(A, tau, m, Om):
      q = m - 1.0
      def g(z):
          t = _t_cosmic(z, Om)
          if abs(q) < 1e-6:
              core = np.exp(-t / tau)
          else:
              core = np.maximum(1.0 + q * t / tau, 0.0) ** (-1.0 / q)   # for q < 0 this reaches 0, finite-time extinction
          return 1.0 + A * core
      return _norm(g)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.1 | 0.2 | -0.9 | 3.0 |
  | tau | 0.5 | 0.3 | 0.02 | 5.0 |
  | m | 2.0 | 0.5 | 0.3 | 4.0 |

  LCDM limit: A=0.
- High-z behaviour: t -> 0 gives core -> 1, so f -> (1+A)/g(0). Finite, positive for A > -1.
- Impact if true: the form of the relaxation (power law versus exponential versus finite-time extinction) distinguishes the defect type; a tail slower than exponential means the DE decay never completes and mimics a w slightly above -1 at all late times.
- Beyond-background fingerprint: for m near 2 the late-time excess density falls as 1/t, a specific slow w(a) drift above -1 (power law, not exponential); defect networks also leave a stochastic gravitational-wave background tied to the annihilation rate.
- Prior art: query "Vinen vortex tangle decay dark energy OR reaction order decaying vacuum energy power-law relaxation Tsallis q-exponential dark energy". none found (hits were vortex-tangle physics, arXiv:1607.03719, and a superfluid-universe paper arXiv:1309.5707 that does not use this law).
- Weirdness 4 / Plausibility 3

### Void-percolation order parameter
- Field and analogy: Near a percolation threshold p_c the strength of the infinite cluster is `P_inf ~ (p - p_c)^beta` for p > p_c, with universal beta (about 0.41 in 3D site percolation, p_c = 0.3116 on the simple cubic lattice, 5/36 in 2D).
- Cosmology story: Voids expand and merge; once the volume fraction p(z) of underdense regions passes p_c a single connected void network spans the universe and its "strength" switches on with a universal exponent. Dark energy (really a backreaction-like effective term) is proportional to that strength. Honest analogy: the dark-energy amplitude is put in by hand; only the onset exponent is imported.
- Form: density f(z).
  ```python
  PC = 0.3116   # 3D simple-cubic site percolation threshold

  def void_percolation(A, p0, s, beta):
      def g(z):
          z = np.asarray(z, dtype=float)
          p = p0 * (1.0 + z) ** (-s)                  # void volume fraction, grows with time
          return 1.0 + A * np.maximum(p - PC, 0.0) ** beta
      return _norm(g)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.5 | 0.3 | -0.9 | 5.0 |
  | p0 | 0.6 | 0.1 | 0.35 | 0.95 |
  | s | 1.0 | 0.4 | 0.1 | 3.0 |
  | beta | 0.42 | 0.1 | 0.3 | 1.0 |

  LCDM limit: A=0.
- High-z behaviour: p < p_c at (1+z) > (p0/p_c)^(1/s), so P = 0 and f is the constant 1/g(0). Finite, positive for A > -1. For beta < 1, w has an integrable spike at the onset redshift (possible |w+1| > 4 flag at large A).
- Impact if true: the apparent dark-energy onset is a critical phenomenon in structure formation: one connected void network, with a universal exponent that is the same in unrelated systems. Would link DE timing (z ~ 0.5-1) to the cosmic-web topology, tying into the "why now" coincidence.
- Beyond-background fingerprint: genus/Euler-characteristic and void-connectivity statistics of the cosmic web showing a percolation transition at the same redshift; topology-dependent signal in void lensing.
- Prior art: query "percolation of voids dark energy backreaction critical exponent infinite cluster cosmology". none found for void percolation as a dark-energy onset (hits: void percolation in simulations, Aanda 2018 table of percolation thresholds; backreaction reviews, e.g. arXiv:1112.5335; Khoury and Wong use percolation for the eternal-inflation landscape, not void networks).
- Weirdness 4 / Plausibility 3

### BCS-gap condensation-energy onset
- Field and analogy: In a BCS superconductor the gap Delta(T) vanishes as sqrt(1 - T/T_c) at T_c and saturates at low T; a standard interpolation is `Delta/Delta0 = tanh(1.82 [1.018 (T_c/T - 1)]^0.51)` (recalled from the literature on s-wave gap fits; verify before use). The condensation energy is proportional to Delta^2.
- Cosmology story: A dark fermion condensate forms below T_c with T proportional to (1+z)^s, contributing a gap-squared term to the vacuum energy that is flat at low T and cusps at z_c. The BCS temperature profile (saturating, not a power law) is the new ingredient.
- Form: density f(z).
  ```python
  def bcs_onset(A, zc, s):
      def g(z):
          z = np.asarray(z, dtype=float)
          x = np.maximum(((1.0 + zc) / (1.0 + z)) ** s - 1.0, 0.0)   # Tc/T - 1, zero above Tc
          gap = np.tanh(1.82 * (1.018 * x) ** 0.51)
          return 1.0 + A * gap ** 2
      return _norm(g)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | -0.2 | 0.2 | -0.9 | 3.0 |
  | zc | 1.0 | 0.5 | 0.05 | 5.0 |
  | s | 1.0 | 0.3 | 0.5 | 2.0 |

  LCDM limit: A=0.
- High-z behaviour: above z_c, x = 0 and g = 1, so f = 1/g(0), constant. Gap squared goes as x^1.02, so f has no singular w at z_c (finite jump in slope only). Positive for A > -1.
- Impact if true: DE is the condensation energy of a dark-sector pairing transition; a negative A (condensation lowers the energy) gives a recent drop in density, i.e. w > -1 today.
- Beyond-background fingerprint: a dark-sector latent specific-heat jump (a step in the effective number of relativistic species at z_c, a tiny BBN/CMB hint); modified growth through the gap-dependent dark-matter mass if the same condensate carries mass.
- Prior art: query "BCS gap condensate dark energy fermion pairing cosmological constant temperature dependence arXiv". **KNOWN (concept)**: Alexander, Biswas, Calcagni, arXiv:0906.5161 "Cosmological Bardeen-Cooper-Schrieffer condensate as dark energy" (abstract read: dark energy as a fermion BCS-like condensate formed in the early universe, with gap and chemical potential evolving to give negative pressure). Their model is a full field-theory calculation; the closed-form tanh gap profile in T proportional to (1+z)^s used here is not their form (not verified in the paper body).
- Weirdness 4 / Plausibility 2

### Avrami (JMAK) latent-heat release
- Field and analogy: A first-order transition by nucleation and growth completes as `X = 1 - exp(-(t/t0)^n)` (Johnson-Mehl-Avrami-Kolmogorov), with Avrami exponent n = 3 or 4 for 3D growth, and releases latent heat in proportion to X.
- Cosmology story: A hidden-sector false vacuum converts to true vacuum by bubble nucleation late in cosmic history; the vacuum energy is lowered by a latent heat L in proportion to the converted volume fraction, which follows JMAK in the scale factor. Included as a low-weirdness anchor.
- Form: density f(z).
  ```python
  def avrami(L, an, n):
      def g(z):
          a = 1.0 / (1.0 + np.asarray(z, dtype=float))
          X = -np.expm1(-(a / an) ** n)               # converted fraction 1 - exp(-(a/an)^n)
          return 1.0 + L * X
      return _norm(g)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | L | -0.2 | 0.2 | -0.9 | 3.0 |
  | an | 0.6 | 0.2 | 0.2 | 1.5 |
  | n | 4.0 | 1.0 | 1.0 | 6.0 |

  LCDM limit: L=0.
- High-z behaviour: a -> 0 gives X -> 0, so f -> 1/g(0). Finite and positive for L > -1.
- Impact if true: the dark energy is a metastable false vacuum decaying late; implies bubble collisions and a gravitational-wave background. Sharper than a tanh step because n controls the transition width in a way fixed by growth dimensionality.
- Beyond-background fingerprint: GW background from bubble collisions at the nucleation epoch; ISW from the density drop.
- Prior art: query "Avrami JMAK nucleation kinetics first-order phase transition dark energy vacuum latent heat late universe". **KNOWN (concept)**: Pen and Zhang, arXiv:1202.0107 "Observational Consequences of Dark Energy Decay" (abstract read: dark energy as energy released by a first-order hidden-sector transition, bubble nucleation, kSZ and ISW signals). JMAK itself is used for early-universe transitions (arXiv:2608.30115, not opened, listed from search). The specific closed-form JMAK-in-scale-factor profile with Avrami exponent has not been found against late-time data.
- Weirdness 3 / Plausibility 3

### Inverse-log granular compaction
- Field and analogy: A tapped granular pile densifies not exponentially but as the inverse-logarithmic law `rho(t) = rho_inf - Delta rho / (1 + B ln(1 + t/tau))` (Knight et al. 1995; Ben-Naim, Knight, Nowak, arXiv:cond-mat/9603150), the glass-like slow relaxation of a system that must rearrange free volume to move.
- Cosmology story: The dark-energy density relaxes like a compacting glass: a rapid early drop that then slows to a logarithm, so the vacuum energy never settles. Cosmic time replaces tap number. Analogy only; no microscopic model.
- Form: density f(z), uses Om.
  ```python
  def granular_compaction(A, tau, B, Om):
      def g(z):
          t = _t_cosmic(z, Om)
          return 1.0 + A / (1.0 + B * np.log1p(t / tau))
      return _norm(g)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.1 | 0.2 | -0.9 | 3.0 |
  | tau | 0.1 | 0.1 | 0.005 | 2.0 |
  | B | 2.0 | 1.0 | 0.1 | 20.0 |

  LCDM limit: A=0.
- High-z behaviour: t -> 0 gives g -> 1 + A. Finite and positive for A > -1. The decay is slower than any power law, so the late-time w sits very close to -1 but is not exactly -1.
- Impact if true: a dark component with logarithmically slow relaxation would mean "w = -1" is only an approximation valid over a finite window, and w0 would drift slowly towards -1; a signal for glassy vacuum dynamics.
- Beyond-background fingerprint: an extremely slowly decaying DE density gives a predictable, nearly scale-free evolution of the growth rate at z < 1; no sharp scale for ISW.
- Prior art: query "inverse logarithmic relaxation granular compaction law dark energy density cosmology". none found (all hits are granular-matter physics: cond-mat/9603150, cond-mat/0211688, cond-mat/9907144).
- Weirdness 5 / Plausibility 2

---

## Needs ODE

These are the better versions of ideas above, but need integration of an equation of motion.

1. **Time-dependent Ginzburg-Landau (Landau-Khalatnikov) order parameter** (best version of the Kibble-Zurek and BCS ideas). Scalar psi (order parameter), with N = ln a and a temperature T = T0/a:
   `psi'' + (3 + dlnH/dN) psi' + (1/H^2) dV/dpsi = 0` (underdamped), or overdamped `Gamma H psi' = -dV/dpsi`, with `V = (a(T - Tc)/2) psi^2 + (b/4) psi^4`, a(T-Tc) crossing zero at z_c. DE density `rho = V(psi) + (H^2 psi'^2)/2`. The real Kibble-Zurek freeze-out comes from letting the relaxation time `tau ~ |T - Tc|^(-z nu)` exceed 1/H.
2. **Bouchaud trap model with master equation**: `dP_i/dN = -r_i(N) P_i + sum_j w_ji P_j`, trap depths drawn from an exponential distribution, `r_i = (1/tau0) exp(-E_i/T)`, with T as the dark-sector temperature; DE = sum_i P_i E_i. Gives exact aging with mu = T/Tg varying in time.
3. **Self-consistent dispersive vacuum**: H = f(H) rather than the reference-LCDM drive: `E^2 = Om (1+z)^3 + (1-Om) g(E)/g(1)` solved at each z (fixed-point iteration; a 1D root find per redshift).
4. **Kovacs-memory hump** (not in the list above): rho_DE after a two-step thermal history has a non-monotonic relaxation, modelled by the Tool-Narayanaswamy-Moynihan equation `d(Tf)/dt = (T - Tf)/tau(T, Tf)`, `tau = tau0 exp[x Dh/(R T) + (1-x) Dh/(R Tf)]`, needs ODE in fictive temperature Tf.
