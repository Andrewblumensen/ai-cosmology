# Batch 2 harvest: biology, ecology, epidemiology, evolution, physiology

Harvester: field cluster "biology-ecology-epidemiology". Nine ideas, all closed-form (scipy only for idea 7).
Conventions: `x = ln(1+z)`, `a = 1/(1+z)`. Density models give f(z) = rho_DE(z)/rho_DE(0). Relation used: w = -1 + (1+z) f'/(3 f),
so f decreasing with z means 1+w > 0 (non-phantom side) only when f' > 0; f growing toward the past means 1+w > 0, f shrinking toward the past means phantom (1+w < 0).
Nothing here was fitted; no numbers are results.
Honest summary of prior art: no exact match found for any idea; two ideas (5, 9) contain the known "oscillating dark energy" (Linder, astro-ph/0511415, sinusoidal w) as a limit, and idea 8 overlaps with generic rational/Pade parametrisations of w.

---

### Ontogenetic growth curve DE (West-Brown-Enquist 3/4 law)
- Field and analogy: Metabolic theory of growth. An organism's mass m grows as dm/dt = a m^(3/4) [1 - (m/M)^(1/4)] (West, Brown & Enquist 2001, Nature 413:628), solved by r = (m/M)^(1/4) = 1 - (1 - r0) e^(-k t): all species collapse onto one universal sigmoid, and "mass" is the fourth power of a linear variable.
- Cosmology story: Treat the DE density as the "biomass" of the vacuum: rho_DE is proportional to r^4 where r relaxes to its adult value exponentially in e-folds of expansion (time = ln a). A juvenile universe (r0 < 1, k > 0) has DE that was zero before a finite "birth redshift" z_b and then grew; an overgrown one (r0 > 1, k < 0) shrinks to adult size. Pure analogy; the 4th power is the distinctive part.
- Form: density f(z).
  ```python
  f = lambda r0, k: (lambda z: (np.maximum(1.0 - (1.0 - r0) * (1.0 + np.asarray(z, float))**k, 0.0) / r0)**4)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | r0 | 0.8 | 0.1 | 0.1 | 3.0 |
  | k | 0.3 | 0.2 | -3.0 | 3.0 |

  Constraint to pass to the scorer: `lambda r0, k: not (r0 > 1 and k > 0)` (otherwise f grows like (1+z)^(4k) at high z). LCDM limit: k = 0 (also r0 = 1).
- High-z behaviour (z up to 1100): k > 0, r0 < 1: f = 0 exactly beyond z_b = (1/(1-r0))^(1/k) - 1, so the early universe is pure matter plus radiation, no negative or divergent density (flag "DE density <= 0" only fires if z_b < 3). k < 0, r0 < 1: f tends to the constant r0^-4 (for r0 = 0.1 that is 1e4 x rho_DE0, still about 1e-5 of the matter density at z = 1100). Finite everywhere.
- Impact if true: dark energy would be a "born" component with a universal sigmoid history and a predicted onset redshift, with w < -1 on the growing branch and no ghost field needed (effective, like PEDE-type phantom-looking emergence but with a hard birth and the 4th-power shape). Would point at the DE density being a power of a simpler, linearly relaxing quantity.
- Beyond-background fingerprint: no DE at z > z_b means ISW and late-time growth suppression switch on at a sharp redshift; the CMB lensing / galaxy ISW cross-correlation should show a cut-off. Also H0-sound-horizon inference changes because early expansion is pure matter-radiation.
- Prior art: query "ontogenetic growth model West Brown Enquist dark energy cosmology" (web search): none found (only the biology papers and critiques of the WBE law; no cosmology link).
- Weirdness 5 / Plausibility 1

---

### Gompertz-Makeham vacuum senescence
- Field and analogy: Actuarial/biological ageing. Mortality hazard h(t) = lambda + alpha e^(beta t) (Makeham constant risk plus Gompertz exponential senescence); the surviving fraction is exp(-integral of h).
- Cosmology story: The vacuum energy is a "survivor function" S(a) in the scale factor, decaying under a constant-risk term (lambda) plus an exponentially rising ageing term (alpha e^(beta a)). Hazard goes to zero at a -> 0 so DE is exactly Lambda-like early and ages late. Analogy only.
- Form: density f(z), with a = 1/(1+z).
  ```python
  def _gm(lam, alpha, beta):
      def f(z):
          a = 1.0 / (1.0 + np.asarray(z, float))
          g = np.where(np.abs(beta) < 1e-8, a - 1.0, (np.exp(beta * a) - np.exp(beta)) / np.where(np.abs(beta) < 1e-8, 1.0, beta))
          return np.exp(-lam * (a - 1.0) - alpha * g)
      return f
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | lam | 0.3 | 0.3 | -3.0 | 6.0 |
  | alpha | 0.3 | 0.3 | -3.0 | 6.0 |
  | beta | 2.0 | 1.0 | -6.0 | 6.0 |

  Constraint: `lambda lam, alpha, beta: abs(lam + alpha * np.expm1(beta) / (beta if abs(beta) > 1e-8 else 1.0)) <= 12.0` (limits ln f at a -> 0). LCDM limit: lam = 0 and alpha = 0 (any beta).
  Equation of state: 1 + w = a (lam + alpha e^(beta a)) / 3, so w -> -1 as z -> infinity automatically.
- High-z behaviour (z up to 1100): f tends to the constant exp(lam + alpha (e^beta - 1)/beta) (bounded by the constraint at e^12); w -> -1 early. Positive everywhere by construction (exponential).
- Impact if true: DE has a thawing history with a built-in "Lambda at early times" limit, and the late rise is exponential in a, not a power: a new functional family (w+1 proportional to a e^(beta a)) and with lam, alpha < 0 it gives phantom side without crossing. The lam-only piece equals the one-parameter CPL slice wa = -(1+w0) (known); the Gompertz term is the new part.
- Beyond-background fingerprint: thawing w >= -1 (for lam, alpha >= 0) reduces late growth suppression relative to phantom fits: fsigma8 and galaxy-ISW cross-correlation sign/amplitude differ from CPL w0 > -1, wa < 0 at z < 0.5.
- Prior art: query "Gompertz-Makeham mortality law dark energy equation of state" (web search): none found.
- Weirdness 4 / Plausibility 3

---

### Punctuated-equilibrium staircase (log-periodic steps)
- Field and analogy: Evolution by punctuated equilibrium (Eldredge & Gould): long stasis broken by bursts of change at (here) regularly spaced scale ratios. Mathematically a smooth devil's-staircase built from the argument of 1 - eps e^(i theta): eps = 0 is a smooth ramp, eps -> 1 gives flat plateaus with jumps.
- Cosmology story: ln rho_DE advances in discrete jumps, one per factor e^Lam in (1+z) (discrete scale invariance), with the vacuum energy exactly constant (w = -1) on the plateaus and rapid transitions between them. Analogy: stasis and punctuation; no field theory behind it.
- Form: density f(z).
  ```python
  def _stair(kappa, Lam, eps, x0):
      def S(x):
          th = 2 * np.pi * (x - x0) / Lam
          return (x - x0) - (Lam / np.pi) * np.angle(1.0 - eps * np.exp(1j * th))
      return lambda z: np.exp(kappa * (S(np.log1p(np.asarray(z, float))) - S(np.zeros(1))[0]))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | kappa | -0.3 | 0.3 | -1.5 | 1.0 |
  | Lam | 0.8 | 0.2 | 0.2 | 3.0 |
  | eps | 0.8 | 0.1 | 0.0 | 0.95 |
  | x0 | 0.0 | 0.3 | -3.0 | 3.0 |

  LCDM limit: kappa = 0. (eps = 0 gives constant w = -1 + kappa/3, the wCDM slice.)
- High-z behaviour (z up to 1100): average slope f ~ (1+z)^kappa, so at most e^7 ~ 1e3 times rho_DE0 at z = 1100 for kappa = 1 (negligible against matter); kappa < 0 decays. Positive and finite everywhere; np.angle on a number with positive real part never jumps.
- Impact if true: a discretely scale-invariant history of the vacuum energy, the same family of ideas as log-periodic precursors in critical phenomena; it would mean DE is not slowly rolling but "ratcheting". A localised DESI-like w(z) wiggle and Hubble tension "steps" would both be natural outputs.
- Beyond-background fingerprint: each step changes H(z) abruptly, so BAO/SN residuals should oscillate log-periodically in 1+z with ratio e^Lam, and the growth rate fsigma8(z) gets kinks at the steps (sharp ISW pulses).
- Prior art: query "arXiv log-periodic discrete scale invariance dark energy staircase expansion history" (web search). Related but not the same: Calcagni & De Felice, arXiv:2004.02896 "Multifractional theories: late-time acceleration" (abstract read: geometry-driven acceleration, no log-periodic DE density in abstract). None found for a log-periodic staircase DE density.
- Weirdness 5 / Plausibility 1

---

### Pharmacokinetic repeated-dose DE (Bateman sawtooth)
- Field and analogy: Pharmacokinetics. A drug dose is absorbed (rate ka) and eliminated (rate ke); the plasma concentration is the Bateman function e^(-ke t) - e^(-ka t), and periodic dosing builds the steady-state curve e^(-ke t)/(1 - e^(-ke tau)) - e^(-ka t)/(1 - e^(-ka tau)).
- Cosmology story: A recurring "dose" of vacuum energy is injected every tau e-folds of expansion (successive phase transitions or reheating-like events), rises fast, decays slowly, and the DE density is the concentration on top of a Lambda baseline. Time-since-dose is measured in forward cosmic time (decreasing ln(1+z)). Pure analogy.
- Form: density f(z), ka = 5 ke fixed.
  ```python
  def _pk(B, tau, ke, phi):
      ka = 5.0 * ke
      def c(t):
          return np.exp(-ke * t) / (1 - np.exp(-ke * tau)) - np.exp(-ka * t) / (1 - np.exp(-ka * tau))
      cmax = c(np.linspace(0.0, tau, 400)).max()
      def g(z):
          u = np.log1p(np.asarray(z, float)) / tau + phi
          t = (1.0 - np.mod(u, 1.0)) * tau          # time since last dose (dose at the higher-z node)
          return 1.0 + B * c(t) / cmax
      return lambda z: g(z) / g(np.zeros(1))[0]
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | B | 0.2 | 0.2 | -0.9 | 20.0 |
  | tau | 1.0 | 0.3 | 0.3 | 3.0 |
  | ke | 2.0 | 1.0 | 0.2 | 10.0 |
  | phi | 0.3 | 0.2 | 0.0 | 1.0 |

  LCDM limit: B = 0.
- High-z behaviour (z up to 1100): perfectly periodic in ln(1+z), bounded between (1 + B c_min/c_max) and (1 + B) relative; no growth, so DE never exceeds (1+B) x its Lambda baseline at CMB. Positive for B > -0.9. f has kinks (w jumps) at each dose; large B can trip the scorer's |1+w| > 4 flag.
- Impact if true: DE would be a periodic-in-ln(a) forced-relaxation process with asymmetric pulses (fast rise, slow fall), giving a natural origin for non-Gaussian, asymmetric localised bumps in binned w(z) reconstructions; the existing symmetric "Transient bump" model cannot produce an asymmetric causal profile.
- Beyond-background fingerprint: asymmetric steps in H(z) and sawtooth growth-rate residuals; a repeating ISW pulse train at fixed ratios of 1+z.
- Prior art: query "arXiv pharmacokinetic Bateman function dark energy cosmology" (web search): none found (results were the math "Bateman functions" and unrelated beta-function quintessence).
- Weirdness 5 / Plausibility 1

---

### Hopf-onset oscillator (Stuart-Landau amplitude switch-on)
- Field and analogy: Circadian/limit-cycle oscillators. The Stuart-Landau normal form dr/dN = mu r - r^3 has the exact solution r^2 = r_inf^2 / (1 + C e^(-2 mu N)), with N = ln a: a supercritical Hopf bifurcation, where the oscillation amplitude grows from zero to a saturated limit cycle.
- Cosmology story: A DE component is a clock that is dormant (amplitude zero, pure Lambda) in the early universe and "wakes up" at redshift zh as the expansion crosses a Hopf threshold, settling into a fixed-amplitude, log-periodic oscillation. Analogy; the oscillation frequency is in ln(1+z).
- Form: density f(z), with growth rate mu = 2 fixed (amplitude ~ (1+z)^-2 above zh).
  ```python
  f = lambda A, omega, zh, phi: (lambda z: (
      1.0 + A / np.sqrt(1.0 + ((1.0 + np.asarray(z, float)) / (1.0 + zh))**4) * np.cos(omega * np.log1p(np.asarray(z, float)) + phi))
      / (1.0 + A / np.sqrt(1.0 + (1.0 / (1.0 + zh))**4) * np.cos(phi)))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.1 | 0.1 | -0.9 | 0.9 |
  | omega | 6.0 | 2.0 | 0.5 | 20.0 |
  | zh | 1.0 | 0.5 | 0.0 | 5.0 |
  | phi | 0.5 | 1.0 | -3.1416 | 3.1416 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): amplitude decays as (1+z)^-2, so f tends to 1/(1 + A r0 cos phi): a constant, exactly Lambda-like early universe. Positive for |A| < 1.
- Impact if true: oscillating DE exists in the literature, but a dormant-then-waking oscillation explains why oscillations show up only at late times and not in the CMB. It would mean DE is a self-sustained oscillator (a "clock"), not a slowly rolling field; a binned-w(z) with a ringing pattern at z < 1 would be the signature.
- Beyond-background fingerprint: oscillating growth rate and a series of alternating ISW sign flips; matter-power-spectrum ringing in the late-time growth index.
- Prior art: query "Stuart-Landau Hopf bifurcation limit cycle amplitude oscillating dark energy scalar field expansion history" (web search): none found for the amplitude switch-on; related: Linder, arXiv:astro-ph/0511415 "On Oscillating Dark Energy" (abstract read: constraints on oscillatory w; the K -> amplitude-constant limit of this model resembles it) and arXiv:2512.04607 "Mode interactions in scalar field cosmology" (Hopf bifurcation in a reduced cosmological dynamical system; not read in full). Not marked KNOWN because the closed-form amplitude switch-on is not in either.
- Weirdness 4 / Plausibility 2

---

### Ricker-map generational DE (logistic-map chaos in ln a)
- Field and analogy: Population ecology with discrete, non-overlapping generations (insects): x_{n+1} = r x_n (1 - x_n) (logistic/Ricker map) shows a fixed point, period doubling and chaos as r grows (May 1976).
- Cosmology story: Each "generation" is a fixed step dx in ln(1+z), and the DE density modulation follows one iterate of the logistic map; linearly interpolated between iterates. Regime r < 3: relaxation to a constant; 3 < r < 3.57: 2, 4, 8-cycles; r > 3.57: chaos. A deliberately non-human model; no physical mechanism offered.
- Form: density f(z). Finite recursion (at most ~75 iterations), no ODE.
  ```python
  def _ricker(B, r, dx, x1):
      nmax = int(np.ceil(np.log(1101.0) / dx)) + 2
      xs = [x1]
      for _ in range(nmax):
          xs.append(r * xs[-1] * (1.0 - xs[-1]))
      xs = np.array(xs)
      def g(z):
          n = (np.log(1101.0) - np.log1p(np.asarray(z, float))) / dx   # generations elapsed since z = 1100
          return 1.0 + B * np.interp(n, np.arange(len(xs)), xs)
      return lambda z: g(z) / g(np.zeros(1))[0]
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | B | 0.2 | 0.2 | -0.9 | 5.0 |
  | r | 3.2 | 0.2 | 2.5 | 4.0 |
  | dx | 0.4 | 0.1 | 0.1 | 1.0 |
  | x1 | 0.3 | 0.1 | 0.01 | 0.99 |

  LCDM limit: B = 0. The fit landscape is multimodal (chaotic for r > 3.57): the scorer should use many starts.
- High-z behaviour (z up to 1100): iterates stay in (0, 1) for r <= 4, so 1 + B x is bounded between 1 + B and 1 (finite, positive for B > -0.9). At the CMB it equals 1 + B x1 relative to its start: no blow-up.
- Impact if true: DE with deterministic chaos in ln a would make dark-energy history unpredictable beyond a few "generations" but locally simple, consistent with the Hubble tension appearing as a local-vs-global mismatch. Realistically a stress test of whether the data prefer any wiggle structure at all.
- Beyond-background fingerprint: period doubling gives a hierarchy of features at ratios of 1+z; alternating growth-rate residuals at generation spacing.
- Prior art: query "logistic map period doubling chaos dark energy density cosmology arXiv" (web search): none found.
- Weirdness 5 / Plausibility 1

---

### Epidemic-threshold DE (SIR final size via Lambert W)
- Field and analogy: Epidemiology. For an SIR outbreak with basic reproduction number R0, the final attacked fraction R_inf solves R_inf = 1 - exp(-R0 R_inf), so R_inf = 0 for R0 <= 1 and R_inf = 1 + W_-1(-R0 e^-R0)/R0 for R0 > 1 (lower branch of Lambert W). Order-parameter-like onset at the threshold R0 = 1.
- Cosmology story: The dark-energy "infected" fraction of the vacuum is R_inf evaluated at an R0 that rises as the universe expands, R0(z) = R0_0 (1+z)^-p. DE is exactly zero until R0 crosses 1 at zc, then switches on with a mean-field threshold and saturates. Analogy; the exponent delta is left free (non-mean-field).
- Form: density f(z). Needs `from scipy.special import lambertw` (scipy is in requirements.txt).
  ```python
  from scipy.special import lambertw
  def _rinf(R0):
      R0 = np.asarray(R0, float)
      x = np.maximum(R0, 1.0 + 1e-12)
      return np.where(R0 > 1.0, 1.0 + np.real(lambertw(-x * np.exp(-x), -1)) / x, 0.0)
  f = lambda R0, p, delta: (lambda z: (_rinf(R0 * (1.0 + np.asarray(z, float))**(-p)) / _rinf(R0))**delta)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | R0 | 2.5 | 0.5 | 1.2 | 8.0 |
  | p | 0.5 | 0.3 | 0.0 | 3.0 |
  | delta | 1.0 | 0.3 | 0.3 | 3.0 |

  LCDM limit: p = 0 (R0 constant, f = 1).
- High-z behaviour (z up to 1100): R0(z) < 1 beyond zc = R0^(1/p) - 1, so f = 0 exactly (pure matter plus radiation, no blow-up); in between f is finite and positive. At zc the w(z) from f has a pole (w -> -infinity as f -> 0); the scorer flags this only if zc < 3, which pushes the fit to zc > 3 or kills it.
- Impact if true: DE would be a threshold phenomenon with a sharp birth redshift and phantom-like emergent behaviour, with the exponent delta telling whether the transition is mean-field (delta = 1, linear onset). A fit favouring the model would point to a percolation-like origin of the late acceleration.
- Beyond-background fingerprint: the birth redshift zc implies a sudden onset of ISW and growth suppression; also changes the inferred early-universe H(z) at z > zc relative to LCDM.
- Prior art: query "SIR epidemic model analogy dark energy emergence threshold cosmology arXiv" (web search): none found for the final-size/threshold idea. Related only: arXiv:2409.05348 "Compartmentalization and Coexistence in the Dark Sector of the Universe" (Paliathanasis et al.; abstract read: dark matter / dark energy interaction with asymptotic solutions; no closed-form DE density, not a threshold model).
- Weirdness 4 / Plausibility 2

---

### Hormetic (Brain-Cousens) equation of state
- Field and analogy: Toxicology/pharmacology. Hormesis: a biphasic dose-response, with stimulation at low dose and inhibition at high dose; the Brain-Cousens form is y = c + (d - c + f x)/(1 + (x/e)^b).
- Cosmology story: The "dose" is the matter density proxy x = 1+z; the response is 1 + w. At low dose (late times) the response is stimulatory, at high dose it is damped by a Hill roll-off with cooperativity b, and the stimulation term f x makes the response change sign once, giving a phantom crossing without a phantom field. Analogy only; w is given directly.
- Form: w(z).
  ```python
  w = lambda d, f_, e, b: (lambda z: -1.0 + (d + f_ * (1.0 + np.asarray(z, float))) / (1.0 + ((1.0 + np.asarray(z, float)) / e)**b))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | d | 0.2 | 0.2 | -2.0 | 2.0 |
  | f_ | -0.1 | 0.1 | -2.0 | 2.0 |
  | e | 2.0 | 0.5 | 1.0 | 10.0 |
  | b | 2.5 | 0.5 | 1.2 | 8.0 |

  LCDM limit: d = 0 and f_ = 0.
- High-z behaviour (z up to 1100): 1 + w ~ f_ e^b (1+z)^(1-b) -> 0 for b > 1.2, so w -> -1 and f(z) tends to a finite constant (integral of 1 + w over ln(1+z) converges). No divergence.
- Impact if true: a single-crossing w(z) with a built-in return to Lambda at early times; it overlaps with rational/Pade parametrisations of w, so the added value is mostly the shape and its Hill-type cooperativity, not a new mechanism. Low novelty; kept for completeness.
- Beyond-background fingerprint: crossing of the phantom divide changes sign of the ISW-galaxy cross-correlation shift at the crossing redshift; modified-gravity-like growth signature if the crossing is real.
- Prior art: query "hormesis biphasic dose-response Brain-Cousens model dark energy equation of state phantom crossing" (web search): none found. Overlaps with generic w(z) rational parametrisations already tested in the repo (thawing Pade).
- Weirdness 3 / Plausibility 3

---

### Adler phase-slip "heartbeat" DE (injection-locked oscillator)
- Field and analogy: Physiology and coupled oscillators (cardiac pacemakers, circadian entrainment). The Adler equation dphi/dx = Delta - K sin(phi) describes an oscillator pulled by a periodic drive; exact solution tan(phi/2) = [K + Omega tan(Omega (x - x0)/2)]/Delta with Omega = sqrt(Delta^2 - K^2). Weak coupling K gives a sinusoid, strong coupling K -> Delta gives long dwells with rapid 2 pi phase slips (a spike train).
- Cosmology story: A DE phase phi is entrained by the expansion itself (x = ln(1+z) acts as the "time"), so the density modulation is 1 + A cos phi: a smooth cosine for K = 0 and a heartbeat-like pulse train for large K at fixed period 2 pi/Omega in ln(1+z). Analogy; the K -> 0 limit is the known sinusoidal oscillating DE.
- Form: density f(z).
  ```python
  def _adler(A, Om_slip, K, x0):
      Dl = np.sqrt(Om_slip**2 + K**2)
      def cphi(z):
          u = 0.5 * Om_slip * (np.log1p(np.asarray(z, float)) - x0)
          s = K * np.cos(u) + Om_slip * np.sin(u)
          c = Dl * np.cos(u)
          return (c**2 - s**2) / (c**2 + s**2)       # cos(phi) with no tan poles
      return lambda z: (1.0 + A * cphi(z)) / (1.0 + A * cphi(np.zeros(1))[0])
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.1 | 0.1 | -0.9 | 0.9 |
  | Om_slip | 5.0 | 2.0 | 0.5 | 15.0 |
  | K | 3.0 | 2.0 | 0.0 | 15.0 |
  | x0 | 0.0 | 0.5 | -3.0 | 3.0 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): bounded and periodic in ln(1+z), so f is between (1 - A)/(1 + A cos phi_0) and (1 + A)/(1 + A cos phi_0): at most a factor ~ (1+A)/(1-A) times Lambda, negligible at the CMB. Positive for |A| < 1. The denominator c^2 + s^2 never vanishes.
- Impact if true: the DE component would be a driven, phase-locking oscillator whose waveform shape (sinusoid or spikes) is set by one coupling constant K; a preference for K > 0 would say the late-time modulation is pulsed, not sinusoidal, a very different microphysics (injection locking) from axion-like oscillating DE.
- Beyond-background fingerprint: pulse trains in H(z) give sharp growth-rate kicks and a sequence of ISW bursts with period ratio e^(2 pi/Omega) in 1+z.
- Prior art: query "Adler equation phase locking synchronization oscillating dark energy Hubble expansion arXiv" (web search): none found for phase-locked/Adler DE; the sinusoidal K = 0 limit is the known Linder arXiv:astro-ph/0511415 "On Oscillating Dark Energy" (abstract read, oscillatory w with a phase term).
- Weirdness 5 / Plausibility 1

---

## Needs ODE

The best versions of these ideas have no closed form; listed with equations in e-folds N = ln a, DE and DM energy densities in units of today's critical density.

1. **Lotka-Volterra predator-prey DM/DE with Holling type II response (Michaelis-Menten saturation).** Dark matter is prey q = rho_dm a^3, dark energy density u acts as predator:
   dq/dN = -c u q / (K + q) + (small source), du/dN = e c u q / (K + q) - m u, with the standard coupling rho_total' + 3 H (rho_dm) = 0 closing the system; Friedmann equation H^2 = rho_b + rho_dm + u + rho_r. LCDM limit c -> 0, m -> 3 effective. Prior art: interacting dark sector models are known; the saturating (Holling II) functional response is not; search not exhaustive.
2. **Allee-threshold bistable DE.** dy/dN = r y (y/A - 1)(1 - y/K) for the DE amplitude y(N): below the Allee threshold A the DE dies out (collapse), above it grows to carrying capacity K. Tipping point and hysteresis: a first-order-transition-like history. Integrable in implicit form (partial fractions) but not invertible in closed form.
3. **FitzHugh-Nagumo excitable DE (spike plus refractory period).** dv/dN = v - v^3/3 - w + I(N), dw/dN = eps (v + a - b w), rho_DE = rho_0 (1 + A v): a threshold-triggered pulse and recovery, like a neuron. One limit-cycle pulse per excitation; DE reacts to a drive such as matter density I = Om (1+z)^3.
4. **Goodwin/repressilator gene-circuit oscillator.** Three-species delayed negative feedback x' = a / (1 + z^n) - x, y' = x - y, z' = y - z; DE density = 1 + A x. Sustained oscillation for Hill coefficient n > 8; Hopf threshold depends on n.
5. **Turing patterns.** Two-field reaction-diffusion; the fastest-growing wavelength selected by the dispersion relation. Needs perturbation theory in a clustering background, not a background-only model.
