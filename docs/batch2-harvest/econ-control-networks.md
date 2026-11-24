# Batch 2 harvest: economics, finance, control theory, networks, game theory, complex systems

Harvester field cluster: econ / finance / control / networks / complex systems.
All models are density ratios f(z) = rho_DE(z)/rho_DE(0) (scorer option b), so f(0) = 1 and each is
copy-paste ready. Notation: `a = 1/(1+z)`, `u = np.log1p(z)` (e-folds back in time), `N = -u`.
`ndtr` = `scipy.special.ndtr` (normal CDF). No fit or chi-squared was run; all remarks on behaviour
are analytic. Every parameter table row is: name, x0, scale, lo, hi.

Summary table (10 ideas, 1 marked KNOWN, 7 with weirdness >= 4):

| # | Name | Weirdness | Plausibility | Prior art |
|---|---|---|---|---|
| 1 | LPPL critical-time DE | 4 | 2 | adjacent only |
| 2 | PID step-response DE | 3 | 2 | KNOWN (close) |
| 3 | Avalanche staircase | 5 | 2 | adjacent only |
| 4 | Black-Scholes put-option DE | 5 | 1 | none found |
| 5 | Riccati fold, sine-power DE | 4 | 2 | adjacent only |
| 6 | Cusp-catastrophe hysteresis jump | 4 | 2 | adjacent only |
| 7 | Percolation / Kuramoto order parameter | 4 | 2 | none found |
| 8 | First-passage (inverse Gaussian) emergence | 3 | 2 | none found |
| 9 | Gompertz-Makeham mortality DE | 5 | 1 | none found (logistic DE exists) |
| 10 | Omori-Utsu fore/aftershock cusp | 3 | 2 | none found |

---

### LPPL critical-time DE
- Field and analogy: Log-periodic power law (LPPL, Sornette): bubble price ln p(t) = A + B (tc - t)^m [1 + C cos(w ln(tc - t) - phi)], i.e. a power-law approach to a critical time tc decorated with oscillations that are periodic in ln(tc - t) (discrete scale invariance).
- Cosmology story: Treat the scale factor as the clock and put the "critical time" in the future at a_c > 1, so the DE density carries a power-law approach to a_c with log-periodic wiggles in (a_c - a). An analogy only; the point is that the wiggle frequency is non-uniform in z (dense near today as a_c -> 1), unlike the sin(B ln a) oscillating-DE models.
- Form: density f(z). Parameters fixed: C = 0.5, phi = 0 (phase fixed by f(0) = 1).
  ```python
  def lppl(A, ac, m, omega):
      def f(z):
          a = 1.0 / (1.0 + np.asarray(z, dtype=float))
          s = (ac - a) / (ac - 1.0)              # s = 1 today, s -> ac/(ac-1) at z -> inf
          h = s**m * (1.0 + 0.5 * np.cos(omega * np.log(s)))
          return np.exp(A * (h - 1.5))           # h(today) = 1.5
      return f
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.02 | 0.05 | -0.3 | 0.3 |
  | ac | 1.3 | 0.1 | 1.1 | 3.0 |
  | m | 0.5 | 0.15 | 0.1 | 1.0 |
  | omega | 8.0 | 2.0 | 2.0 | 20.0 |

  LCDM limit: A = 0 (other three then irrelevant; multimodal, use `starts > 1`).
- High-z behaviour (z up to 1100): s is bounded by ac/(ac-1) <= 11, so h <= ~16.5 and f = exp(A (h - 1.5)) stays finite and positive (at most exp(0.3*15) ~ 90 times today's DE, still ~1e-8 of matter at z = 1100). No blow-up because the singularity sits at a_c > 1, not in the past.
- Impact if true: DE would be a critical-phenomenon precursor, with a finite-time singularity (Big-Rip-like or phase-transition-like) at a_c in our future and log-periodic residuals in H(z). That would be a prediction of a future event, not only a fit.
- Beyond-background fingerprint: log-periodic modulation of the growth rate f*sigma8(z) and ISW at the same ln(a_c - a) frequency; a_c fixes the time to the singularity.
- Prior art: Query "log-periodic power law dark energy cosmology arXiv". No LPPL dark energy model found. Adjacent: sinusoidal-in-ln a oscillating DE (Linder, astro-ph/0511415, "On Oscillating Dark Energy", abstract opened); Calcagni and De Felice, arXiv:2004.02896 "Dark energy in multi-fractional spacetimes" (abstract opened; it does NOT mention log-periodicity). A non-arXiv Academia.edu note "Cyclic Tests v2" surfaced in the search with rho_de ~ a^lambda cos(Omega ln a + phi); seen only in a search snippet, unverified. Not marked KNOWN because the (a_c - a)^m envelope and tc singularity are new.
- Weirdness (1-5) / Plausibility (1-5): 4 / 2

### PID step-response DE
- Field and analogy: Control theory. A PI(D) loop pushing a process variable to a setpoint produces the classical underdamped second-order step response: overshoot, ringing, settling.
- Cosmology story: A hidden regulator switches on at z_s and drives rho_DE from an initial level r toward its setpoint, with controller gain and damping setting overshoot (windup) and ringing in ln a. Analogy only; no actual feedback law for the vacuum is proposed.
- Form: density f(z); clock is e-folds since switch-on.
  ```python
  def pid(r, zs, omega, zeta):
      wd = omega * np.sqrt(1.0 - zeta**2)
      k = zeta / np.sqrt(1.0 - zeta**2)
      def g(z):
          tau = np.maximum(np.log1p(zs) - np.log1p(np.asarray(z, dtype=float)), 0.0)
          y = 1.0 - np.exp(-zeta * omega * tau) * (np.cos(wd * tau) + k * np.sin(wd * tau))
          return r + (1.0 - r) * y                # y = 0 for z > zs (C1 onset)
      return lambda z: g(z) / g(0.0)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | r | 0.8 | 0.1 | 0.3 | 2.0 |
  | zs | 1.5 | 0.5 | 0.3 | 5.0 |
  | omega | 5.0 | 1.0 | 1.0 | 12.0 |
  | zeta | 0.4 | 0.1 | 0.2 | 0.95 |

  LCDM limit: r = 1 (then g = 1).
- High-z behaviour (z up to 1100): for z > zs, y = 0 so f is the constant 1/g(0), i.e. exact LCDM-like constant DE at high z. Positive because zeta >= 0.2 limits overshoot to ~1.53 and r <= 2.
- Impact if true: DE is a regulated, self-correcting quantity with a characteristic ringing frequency and settling time; would mean the late universe is approaching a fixed setpoint (a de Sitter attractor) with transient oscillations.
- Beyond-background fingerprint: ringing means w(z) oscillates around -1, so growth-rate suppression alternates with epoch; ISW sign flips on the ringing scale.
- Prior art: KNOWN (close). Queries: "PID controller feedback integral windup dark energy cosmological constant arXiv" (nothing on PID), then "oscillating dark energy log-periodic ... DESI". arXiv:2606.17550 "Does DESI prefer Damped Oscillating Dark Energy over Cosmological constant?" (abstract opened) models w as a damped harmonic oscillator with under/critically/over-damped solutions, which is the same underdamped-response mathematics. Differences here: applied to rho_DE with an onset redshift and a start level r, and the control-theory framing. Also adjacent: Mbonye, arXiv:2211.11708 "Is cosmic dynamics self-regulating?" (from search snippet only).
- Weirdness (1-5) / Plausibility (1-5): 3 / 2

### Avalanche staircase (discrete-scale-invariant punctuated DE)
- Field and analogy: Self-organised criticality and punctuated equilibrium: a system relaxes through a hierarchy of discrete avalanches (devil's-staircase-like) whose positions are log-spaced (discrete scale invariance) and whose sizes follow a geometric/power law.
- Cosmology story: The vacuum energy changes in a sequence of up to 8 smooth steps, equally spaced in ln(1+z) with geometrically scaled sizes q^k, like avalanche sizes in a critical sandpile. An analogy; the new ingredient is a whole ladder with a built-in scale ratio instead of one transition.
- Form: density f(z); step width fixed at 0.25 L.
  ```python
  def stair(A, q, L, s0):
      k = np.arange(8)[:, None]
      uk = s0 + k * L                    # step positions in ln(1+z)
      qk = q ** k
      w = 0.25 * L
      def g(z):
          u = np.atleast_1d(np.log1p(np.asarray(z, dtype=float)))[None, :]
          return (qk * 0.5 * (1.0 + np.tanh((uk - u) / (2.0 * w)))).sum(axis=0)
      def f(z):
          zz = np.asarray(z, dtype=float)
          return ((1.0 + A * g(zz)) / (1.0 + A * g(0.0)[0])).reshape(zz.shape)
      return f
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.05 | 0.05 | -0.05 | 0.5 |
  | q | 0.8 | 0.1 | 0.3 | 1.2 |
  | L | 0.4 | 0.1 | 0.15 | 1.0 |
  | s0 | 0.2 | 0.1 | 0.0 | 0.8 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): all steps have completed on the low-z side, g -> 0 at high z, so f -> 1/(1 + A g(0)), a positive constant. With q <= 1.2 the sum of amplitudes is <= 12.4, and A >= -0.05 keeps 1 + A g > 0.
- Impact if true: the dark sector evolves through a cascade of discrete events with a fixed scale ratio e^L in (1+z), the signature of a hierarchical or scale-invariant vacuum process; would predict further steps at higher z only if the staircase continues, testable with high-z BAO.
- Beyond-background fingerprint: each step leaves a feature in f*sigma8 and a jump in the growth friction; log-spaced bumps in the ISW cross-correlation.
- Prior art: Query "dark energy staircase step-like multiple transitions equation of state sequence of steps geometric amplitudes arXiv" and "self-organized criticality avalanche staircase dark energy discrete scale invariance arXiv". Adjacent only: Bouhmadi-Lopez and Ibarra-Uriondo, arXiv:2602.16795 "The Sign-Switching of the Cosmological Constant" and arXiv:2506.12139 "Cosmographic analysis of sign-switching dark energy" (abstracts opened; "generalised ladder-step" Lambda, no log-spaced or geometric structure stated); Wang, arXiv:0908.2477 "Cosmic Steps in Modeling Dark Energy" (single step, from search listing); arXiv:2003.12594 "The Self-Organized Critical Multiverse" (abstract opened; SOC for vacuum selection, not an expansion model). No geometric/log-spaced multi-step model found.
- Weirdness (1-5) / Plausibility (1-5): 5 / 2

### Black-Scholes put-option DE
- Field and analogy: Finance. A European put on an underlying S with strike K and total volatility v has value P = K Phi(-d2) - S Phi(-d1), d1 = (ln(S/K) + v^2/2)/v, d2 = d1 - v (zero interest rate).
- Cosmology story: A fraction phi of the dark energy is priced like an option on the matter density S = rho_m/rho_m0 = (1+z)^3: it is worth intrinsic value K - S while matter is below the strike and decays to zero once S exceeds K, smoothed by "volatility" v. Pure analogy (a vacuum "insurance" whose payoff is matter dilution), but it gives a smooth turn-off redshift z_K = K^(1/3) - 1 plus an asymmetric, finance-shaped transition.
- Form: density f(z).
  ```python
  from scipy.special import ndtr
  def bs_put(phi, K, v):
      def P(S):
          d1 = (np.log(S / K) + 0.5 * v * v) / v
          return K * ndtr(-(d1 - v)) - S * ndtr(-d1)
      P0 = P(1.0)
      return lambda z: 1.0 - phi + phi * np.maximum(P((1.0 + np.asarray(z, dtype=float)) ** 3), 0.0) / P0
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | phi | 0.2 | 0.1 | -0.5 | 0.95 |
  | K | 3.0 | 1.0 | 1.0 | 30.0 |
  | v | 1.0 | 0.3 | 0.1 | 3.0 |

  LCDM limit: phi = 0.
- High-z behaviour (z up to 1100): P decreases with S, so p = P/P0 in (0, 1] and tends to 0 (exponentially in ln S); f -> 1 - phi, positive for phi < 1. For phi < 0, f = 1 + |phi| (1 - p) >= 1 and bounded by 1 + |phi|. The `np.maximum(.,0)` guards round-off cancellation at large S.
- Impact if true: part of the dark energy would be a derived quantity whose redshift dependence is fixed by the matter density history (a built-in coupling to rho_m), giving a natural coincidence mechanism (DE turns on when matter drops below a threshold). A new class: functional DE = F(rho_m).
- Beyond-background fingerprint: because DE depends on local matter density in the analogy, a local (environment-dependent) response in voids vs clusters; in the strict background version, a distinctive growth suppression after z_K.
- Prior art: Query "Black-Scholes option pricing analogy dark energy density cosmology arXiv". None found: results were option pricing papers (physics/0001040, quant-ph/0510121, cond-mat/0203304) with no cosmology.
- Weirdness (1-5) / Plausibility (1-5): 5 / 1

### Riccati fold, sine-power DE (finite-time singularity of a tipping point)
- Field and analogy: Tipping points. Near a saddle-node (fold) bifurcation the normal form dx/dN = kappa^2 + x^2 (Riccati) blows up in finite time; critical slowing down means the response accelerates as the singularity nears.
- Cosmology story: Let 1 + w = eps * x(N) with x obeying the fold normal form and the blow-up in the future at N_c > 0. This integrates in closed form to rho_DE ~ [sin(kappa (N_c - N))]^(3 eps), a power of a sine of ln a. An analogy; the equation for x is postulated, not derived.
- Form: density f(z). Here w(z) = -1 + eps*kappa*cot(kappa*(Nc + u)); the density below is its exact integral.
  ```python
  def riccati(eps, Nc, phi):
      kap = phi * np.pi / (Nc + 7.0)         # keeps kappa*(Nc+u) < pi up to z = 1100
      return lambda z: (np.sin(kap * (Nc + np.log1p(np.asarray(z, dtype=float))))
                        / np.sin(kap * Nc)) ** (3.0 * eps)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | eps | 0.03 | 0.02 | -0.15 | 0.15 |
  | Nc | 0.5 | 0.2 | 0.1 | 3.0 |
  | phi | 0.3 | 0.1 | 0.01 | 0.9 |

  LCDM limit: eps = 0.
- High-z behaviour (z up to 1100): argument of sin stays in (0, 0.9*pi*(Nc+7.004)/(Nc+7)) < pi, so sin > 0 and f finite; for small phi it tends to ((Nc+u)/Nc)^(3 eps), slow power of ln(1+z). Worst case eps = 0.15, Nc = 0.1: f(1100) ~ 7. w+1 = eps*kappa*cot(.) decays slowly into the past (thawing-like).
- Impact if true: dark energy is a controlled approach to a finite-time singularity at e-fold N_c in the future (a soft Big-Rip-like event); the time to the singularity would be measurable from the fit. This also gives the thawing shape 1 + w ~ eps/(N_c + ln(1+z)), a one-parameter-lighter alternative to CPL.
- Beyond-background fingerprint: growth and lensing follow a w(z) that steepens as z -> 0; a late-time divergence of w (precursor of the singularity) that future surveys could bound.
- Prior art: Queries "saddle-node bifurcation finite-time singularity Riccati equation of state dark energy w(N) arXiv". Adjacent: Cotsakis, arXiv:2502.20430 "Cosmic acceleration as a saddle-node bifurcation: background identities and structure" (abstract opened; normal form of the Friedmann system, no closed-form w(N) or Riccati DE density); Nojiri-Odintsov-Tsujikawa hep-th/0501025 (finite-time singularities by assumed EoS, from search listing). The sine-power form is not found.
- Weirdness (1-5) / Plausibility (1-5): 4 / 2

### Cusp-catastrophe hysteresis jump
- Field and analogy: Catastrophe theory / hysteresis in economics and ecology: a state variable x sits on the lower branch of x^3 - x = h while the control h is swept; at the fold h = 2/(3 sqrt 3) the branch disappears and the system jumps to the other branch (delayed, supercooled transition).
- Cosmology story: A DE order parameter x(z) obeys the cusp equilibrium with control h(z) linear in ln(1+z). The universe stays on the metastable branch until the fold at z_f and then jumps, so the jump size (1.73 in x) is fixed by theory and not a free parameter. Analogy; no potential is derived.
- Form: density f(z), Cardano closed form for the roots, lower branch for z > zf, upper branch for z < zf.
  ```python
  def cusp(A, zf, s):
      HF = 2.0 / (3.0 * np.sqrt(3.0))
      def x(z):
          z = np.asarray(z, dtype=float)
          h = HF * (1.0 - s * np.log((1.0 + z) / (1.0 + zf)))
          c = 1.5 * np.sqrt(3.0) * h                         # = (3 sqrt3 / 2) h
          low_tr = (2/np.sqrt(3)) * np.cos(np.arccos(np.clip(c, -1, 1)) / 3.0 - 4*np.pi/3)
          low_ch = -(2/np.sqrt(3)) * np.cosh(np.arccosh(np.maximum(-c, 1.0)) / 3.0)
          lower = np.where(c >= -1.0, low_tr, low_ch)
          upper = (2/np.sqrt(3)) * np.cosh(np.arccosh(np.maximum(c, 1.0)) / 3.0)
          return np.where(z > zf, lower, upper)
      return lambda z: (1.0 + A * x(z)) / (1.0 + A * x(0.0))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.05 | 0.05 | -0.4 | 0.4 |
  | zf | 0.6 | 0.3 | 0.1 | 2.5 |
  | s | 0.5 | 0.2 | 0.05 | 2.0 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): lower branch x ~ -|h|^(1/3), growing only like (s ln(1+z))^(1/3); for example s = 1, zf = 0.5 gives x(1100) ~ -1.6, so 1 + A x > 0 for |A| <= 0.4. Finite and positive; f is discontinuous at z_f (a step, harmless for integration; flagged as "jump in w" by the pathology check).
- Impact if true: a first-order (hysteretic) late-time transition: DE jumps once, at a redshift set by when the control parameter crosses the fold, with slow critical drift before and after. Distinguishes from the tanh-step by a fixed jump-to-drift ratio.
- Beyond-background fingerprint: a sudden jump in H would produce a localised kink in the growth rate and a possible stochastic GW or isocurvature signal from bubble nucleation; supercooled-transition remnants.
- Prior art: Query "cusp catastrophe hysteresis first-order transition dark energy density jump supercooling late-time arXiv". Adjacent: Koren, Tsai and Wang, arXiv:2509.07076 "Boiling After the Dust Settles: Constraining First-Order Phase Transitions During Dark Energy Domination" (abstract opened; late first-order transition releasing a fraction of DE to radiation, not a cusp-hysteresis background model). Cusp-branch following for the DE density not found.
- Weirdness (1-5) / Plausibility (1-5): 4 / 2

### Percolation / Kuramoto order-parameter DE
- Field and analogy: Network science. Above the percolation threshold the giant-component fraction grows as (p - p_c)^beta with universal exponent (3D percolation beta ~ 0.418, mean-field and Kuramoto synchronisation beta = 1/2).
- Cosmology story: The coherent (connected) part of the vacuum energy is the order parameter of a connectivity transition driven by the scale factor, switching on at z_c with a universal critical exponent. The fitted beta is then a sharp test of "which universality class". Analogy only.
- Form: density f(z). Connectivity p taken to be the scale factor.
  ```python
  def perc(phi, zc, beta):
      ac = 1.0 / (1.0 + zc)
      return lambda z: 1.0 - phi + phi * (np.maximum(1.0 / (1.0 + np.asarray(z, dtype=float)) - ac, 0.0) / (1.0 - ac)) ** beta
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | phi | 0.2 | 0.1 | -1.0 | 0.95 |
  | zc | 1.0 | 0.3 | 0.1 | 3.0 |
  | beta | 0.5 | 0.15 | 0.1 | 1.5 |

  LCDM limit: phi = 0.
- High-z behaviour (z up to 1100): for z > zc the order parameter is 0, f = 1 - phi (constant, positive for phi < 1). For phi < 0, f = 1 + |phi| (1 - m) in [1, 1 + |phi|]. Caveat: for beta < 1 the slope of f is infinite at z_c, so w(z) has an integrable spike there and the scorer's pathology check may flag "pole/jump in w".
- Impact if true: DE as an emergent collective phase with universal exponents; the "why now" is that the cosmic network just crossed a threshold. A fitted beta near 0.42 or 0.5 would be a striking hint of a critical-phenomena origin.
- Beyond-background fingerprint: critical opalescence analogue: enhanced DE perturbations (large susceptibility) near z_c, giving a localised bump in the matter power spectrum growth.
- Prior art: Queries "percolation giant cluster order parameter critical exponent dark energy cosmic web arXiv" and "Kuramoto synchronization transition dark energy cosmology arXiv". None found for the DE role. Adjacent only: percolation as a cosmic-web statistic (e.g. arXiv:1903.07626 "Constraining Cosmology with Big Data Statistics of Cosmological Graphs", abstract opened; graph measures of simulated matter, not a DE model); Kuramoto-like synchronisation for axion dark matter (arXiv:2601.07836, from search listing only).
- Weirdness (1-5) / Plausibility (1-5): 4 / 2

### First-passage (inverse Gaussian) emergence
- Field and analogy: Finance and stochastic processes. The first time a drifted Brownian motion hits a barrier has the inverse Gaussian distribution; its CDF is a skewed, heavy-right-tail sigmoid (gambler's ruin, default-time models).
- Cosmology story: A fraction phi of vacuum "patches" flips to its DE state when a random internal variable first hits a barrier; with cosmic time proxy t = a^(3/2) the flipped fraction is the inverse-Gaussian CDF, giving an asymmetric emergence curve. Analogy; asymmetric transitions are the new part relative to tanh.
- Form: density f(z).
  ```python
  from scipy.special import ndtr
  def ig(phi, m, lam):
      def F(t):
          return (ndtr(np.sqrt(lam / t) * (t / m - 1.0))
                  + np.exp(2.0 * lam / m) * ndtr(-np.sqrt(lam / t) * (t / m + 1.0)))
      return lambda z: 1.0 - phi + phi * F((1.0 + np.asarray(z, dtype=float)) ** -1.5) / F(1.0)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | phi | 0.2 | 0.1 | -0.5 | 0.95 |
  | m | 1.0 | 0.3 | 0.1 | 5.0 |
  | lam | 0.5 | 0.2 | 0.01 | 5.0 |

  LCDM limit: phi = 0.
- High-z behaviour (z up to 1100): t = a^1.5 > 3e-5, F -> 0 smoothly, f -> 1 - phi. exp(2 lam/m) <= e^100, no overflow. For phi < 0, f in [1, 1 + |phi|].
- Impact if true: DE emergence is a stochastic first-passage event with a skewed distribution of "arrival times"; the skewness is a testable shape feature beyond a symmetric tanh.
- Beyond-background fingerprint: patch-to-patch variance: if different regions flip at different times, an inhomogeneous DE, i.e. a small anisotropy/dipole in H0 and lensing.
- Prior art: Query "first-passage time inverse Gaussian dark energy emergence cosmology arXiv". None found (results were molecular-communication and probability papers, e.g. arXiv:2602.15335, arXiv:1105.1468, not cosmology).
- Weirdness (1-5) / Plausibility (1-5): 3 / 2

### Gompertz-Makeham mortality DE
- Field and analogy: Actuarial science. The Gompertz-Makeham law has hazard h(t) = A + B e^(g t); survival is S = exp(-A t - (B/g)(e^(g t) - 1)), a double-exponential decay.
- Cosmology story: Read lookback e-folds u as "age" and let the DE density be the survival function: dark energy is the "survivor" of a vacuum population whose hazard rises exponentially into the past, so DE is super-exponentially absent at early times, with a constant-hazard (wCDM-like) part tied to it. Analogy; b scales the whole hazard.
- Form: density f(z).
  ```python
  def gompertz(b, gam, rho):
      return lambda z: np.exp(-b * (np.expm1(gam * np.log1p(np.asarray(z, dtype=float))) / gam
                                    + rho * np.log1p(np.asarray(z, dtype=float))))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | b | 0.05 | 0.05 | 0.0 | 3.0 |
  | gam | 1.5 | 0.5 | 0.3 | 3.0 |
  | rho | 0.0 | 0.3 | -1.0 | 1.0 |

  LCDM limit: b = 0.
- High-z behaviour (z up to 1100): hazard >= b(e^(gam u) + rho) > 0 for rho > -1, so f is decreasing in z and underflows to exactly 0 at high z (e.g. gam = 3: (1+z)^3 b). f = 0 is allowed (never negative); the scorer will see "no DE before z of a few", like an emergent-DE model. Because f underflows, w(z) is NaN there (scorer sets NaN where f < 1e-6), which is cosmetic.
- Impact if true: DE is an emergent, late-time quantity with an extremely sharp early cutoff; would explain "why now" as ageing, and rule out any early DE.
- Beyond-background fingerprint: zero DE at z > ~2 means no DE contribution to the CMB lensing and a sharp onset of the growth suppression; no early-DE Hubble-tension relief.
- Prior art: Query "Gompertz law dark energy density model cosmology arXiv". None found for Gompertz-Makeham DE. Nearest: Nelleri et al., arXiv:2406.18095 "Observational Evidence to Logistic Dark Energy Driving the Accelerating Universe" (abstract opened; logistic function of the scale factor), and a Gompertzian reionization model arXiv:2604.13423 (from search listing, not DE).
- Weirdness (1-5) / Plausibility (1-5): 5 / 1

### Omori-Utsu fore/aftershock cusp
- Field and analogy: Seismology / self-exciting (Hawkes) point processes. Aftershock rate decays as (t + c)^(-p) (Omori-Utsu) and foreshock rate grows as an inverse Omori law toward a main shock.
- Cosmology story: A single "main event" at scale factor a_m in the vacuum: dark energy density rises as an inverse power law toward it and relaxes afterwards with the same heavy tail, with a regularising core c. It is the "transient bump" with a cusp and power-law wings instead of a Gaussian-like bump. An analogy.
- Form: density f(z).
  ```python
  def omori(A, am, c, p):
      def g(a):
          return (c / (np.abs(a - am) + c)) ** p      # peak 1 at a = am
      g1 = g(1.0)
      return lambda z: np.exp(A * (g(1.0 / (1.0 + np.asarray(z, dtype=float))) - g1))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.1 | 0.1 | -1.0 | 1.0 |
  | am | 0.7 | 0.1 | 0.3 | 0.95 |
  | c | 0.1 | 0.05 | 0.02 | 0.5 |
  | p | 1.0 | 0.3 | 0.3 | 1.5 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): g -> (c/(am + c))^p, finite, so f -> exp(A (g_inf - g(1))), finite and positive (within exp(+-1)); fully LCDM-like constant at all high z.
- Impact if true: a single discrete event in the vacuum history with scale-free (Omori) wings: a one-off cosmic "quake" at z_m = 1/am - 1, with identifiable foreshock/aftershock exponent p. Low weirdness since it overlaps the tested transient bump; kept for the heavy-tail shape.
- Beyond-background fingerprint: heavy-tailed w(z) wings mean small but long-lasting w deviations; GW from the event if it is a transition.
- Prior art: Queries "Omori law aftershock decay dark energy density cosmology power-law relaxation after main shock" and "Hawkes self-exciting process dark energy cosmology arXiv". None found in cosmology (results all seismology: physics/0609179, cond-mat/0407208; Hawkes: arXiv:2405.10527, review, no cosmology).
- Weirdness (1-5) / Plausibility (1-5): 3 / 2

---

## needs ODE

These are the best versions of ideas from this field that do not close in elementary form.

1. Goodwin / Lotka-Volterra "predator-prey" dark sector (Kondratiev long waves). Variables: x = rho_DE / rho_c (predator), y = rho_m / rho_c (prey) in e-folds N:
   dx/dN = x (-alpha + beta y), dy/dN = y (gamma - delta x) with limit cycles; the scorer needs rho_DE(N) from numerical integration. LCDM: beta = 0 or amplitude zero. Prediction: cyclic dark sector with a period set by sqrt(alpha gamma).
2. Hawkes self-exciting DE sourced by structure collapse. Intensity lambda(N) obeys d lambda/dN = -beta (1 - n) lambda + beta mu + s(N), with s(N) a (non-closed-form) collapse rate and branching ratio n < 1; near n -> 1 critical slowing down. Closed form only for power-law s(N) (it reduces to a sum of power laws, already covered by the Alam-Sahni-Starobinsky-type fit).
3. PID loop with real actuator saturation and integral windup. State: e = rho_DE - rho_set, I = integral of e, dN: d rho_DE/dN = -(Kp e + Ki I + Kd de/dN) clipped to [-umax, umax]. The clipping (anti-windup) is a non-smooth ODE; no closed form.
4. Delay-differential (cobweb) vacuum: rho_DE(N) = gamma * rho_tot(N - Delta) + rho_Lambda. For power-law matter it collapses to a rescaled LCDM (shown by geometric-series summation) unless a history cutoff is added, which gives a discontinuous staircase; the smooth version requires a delay-differential solver.
5. Fractional (Mittag-Leffler) memory relaxation: D^alpha_N rho_DE = -lambda (rho_DE - rho_inf), a Caputo fractional ODE whose solution E_alpha(-lambda N^alpha) interpolates stretched-exponential and power-law relaxation. Series evaluation is unstable at large argument; needs a dedicated implementation.
6. Rock-paper-scissors replicator dynamics (game theory) between three vacuum phases: dx_i/dN = x_i ((A x)_i - x^T A x), with rho_DE = sum x_i rho_i; heteroclinic cycles produce intermittent, log-periodic plateaus. ODE with no elementary solution.
