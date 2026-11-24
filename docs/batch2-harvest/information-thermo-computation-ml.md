# Batch 2 harvest: information theory, thermodynamics, computation, machine learning

Harvester: field cluster "information theory / thermodynamics / computation / ML". 2026-11-24.
All forms below were only syntax-checked (finite on z = 0..1100, f(0) = 1, f > 0 at the example parameters). No fit, no chi-squared.
Conventions: `Param(x0, scale, lo, hi)` as in `src/aicosmo/score.py`. Every model is a density ratio f(z) = rho_DE(z)/rho_DE(0), unless it says "uses Om".
Common pattern: f = 1 + A * (shape(z)/shape(0) - 1), so A = 0 is exactly LCDM and f(0) = 1 by construction.
Prior-art searches were run 2026-11-24 with WebSearch; abstracts were opened with WebFetch where a paper is cited.

Summary table

| # | Name | Weirdness | Plausibility | KNOWN? |
|---|------|-----------|--------------|--------|
| 1 | Hajek log-cooling DE | 4 | 2 | no |
| 2 | Double-descent interpolation peak | 3 | 2 | no |
| 3 | Shannon-Hartley wideband saturation | 3 | 2 | no (overlaps catalogued "Saturating DE" shape) |
| 4 | Jarzynski rare-event emergent DE | 4 | 2 | no (near PEDE family at data level) |
| 5 | Saddle-to-saddle staircase | 4 | 2 | partial (multi-step vacuum energy exists, 2208.05583) |
| 6 | Doubling-period cyclical schedule | 5 | 1 | no |
| 7 | Log-periodic discrete-scale-invariance ring | 4 | 2 | partial (informal draft only) |
| 8 | Dyadic-map chirp | 5 | 1 | no |
| 9 | Fold-bifurcation tipping DE | 4 | 3 | no (cousin: 2502.20430) |
| 10 | Levin-Chaitin universal-prior clock | 5 | 1 | no |
| 11 | Self-evidencing KL information gain | 4 | 2 | no |

Weirdness >= 4: ideas 1, 4, 5, 6, 7, 8, 9, 10, 11 (9 of 11).

---

### Hajek log-cooling DE
- Field and analogy: Simulated annealing converges to the global optimum only if the temperature falls no faster than T(t) = Gamma / ln(t) (Hajek / Geman-Geman logarithmic schedule). The same 1/ln law is the compression ratio of Lempel-Ziv coding of a random sequence.
- Cosmology story: Suppose the dark sector is a system annealing toward its ground state and rho_DE tracks the "temperature" of that search, with cosmic time as the step count. In the matter era time goes as a^1.5, so rho_DE is a power law at early times (in z) and relaxes only logarithmically at late times, an unusually slow, non-exponential tail. Pure analogy.
- Form: density f(z).
  `lambda A, ts: (lambda z: 1 + A*(np.log1p(1/ts)/np.log1p((1+np.asarray(z,float))**-1.5/ts) - 1))`
  
  | name | x0 | scale | lo | hi |
  |------|----|-------|----|----|
  | A | 0.1 | 0.1 | -0.05 | 5.0 |
  | ts | 0.5 | 0.3 | 0.01 | 10.0 |

  LCDM limit: A = 0. (Time proxy tau = a^1.5, the matter-era clock, so no Om needed; ts is the "freeze-in" time in units of today's tau = 1.) A < 0 only viable for tiny |A| because f must stay positive at z = 1100.
- High-z behaviour (z up to 1100): f grows like (1+z)^1.5 once tau < ts (g ~ ts/tau), so for large A and ts the density at z = 1100 can reach about 1e5 times today's value. That is still about 1e-4 of the matter density at recombination, so finite and sane. No pole (ln(1 + x) > 0 always).
- Impact if true: dark energy would be the leftover "temperature" of a slow optimisation in the vacuum; its decay rate is logarithmic forever (no exponential freeze-out), which changes the far-future fate (never a pure de Sitter).
- Beyond-background fingerprint: growth suppression from a w(z) that approaches -1 only logarithmically in the future; a slowly varying w today without a thawing-field potential.
- Prior art: query "dark energy simulated annealing logarithmic cooling schedule cosmology arXiv". None found: results were annealing used as a fitting tool in cosmology (astro-ph/9911330, 2505.02223) and the math paper arXiv:1901.10269 (annealing under fast cooling, opened via search results only, not about cosmology). No dark-energy model with a cooling schedule.
- Weirdness 4 / Plausibility 2

### Double-descent interpolation peak
- Field and analogy: In over-parameterised learning, test error vs model size first falls, then spikes at the interpolation threshold (parameters = data points), then falls again. For ridgeless regression the spike has power-law wings: risk ~ r/(1-r) below the threshold and 1/(r-1) above it, softened by regularisation eps.
- Cosmology story: Treat r = (1+z)/(1+zc) as the ratio "modes the vacuum must fit / constraints available" and let rho_DE follow the risk curve. This gives a localised excess at zc with asymmetric power-law tails, unlike the symmetric Gaussian of the catalogued transient bump.
- Form: density f(z).
  `R = lambda r, e: np.minimum(r, 1.0)/np.sqrt((1-r)**2 + e**2)`
  `lambda A, zc, eps: (lambda z: 1 + A*(R((1+np.asarray(z,float))/(1+zc), eps)/R(1/(1+zc), eps) - 1))`

  | name | x0 | scale | lo | hi |
  |------|----|-------|----|----|
  | A | 0.2 | 0.2 | -0.3 | 0.95 |
  | zc | 1.0 | 0.4 | 0.1 | 3.0 |
  | eps | 0.3 | 0.1 | 0.1 | 1.0 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): R falls as 1/r, so f tends to 1 - A (finite, positive for A < 1). A < 0 range limited by the peak height so f stays positive.
- Impact if true: dark energy has a resonant episode at a critical epoch (a capacity-matching threshold), with a sharp-ish cusp. If the data prefer a cusp over a Gaussian bump it hints at a threshold phenomenon, not a slow field.
- Beyond-background fingerprint: a feature in the ISW signal and the growth rate at z about zc; extremely non-smooth w(z) near the cusp (testable with future SN binning).
- Prior art: query "double descent interpolation threshold dark energy cosmological expansion arXiv". None found: only ML and particle-physics double-descent papers (e.g. arXiv:2611.09138 review). Note: mathematically a transient bump with asymmetric power-law wings, so overlap at the data level with the catalogued bump is likely.
- Weirdness 3 / Plausibility 2

### Shannon-Hartley wideband saturation
- Field and analogy: Capacity of a band-limited channel, C = B ln(1 + S/(N0 B)), rises with bandwidth B but saturates at S/N0 (the power-limited, infinite-bandwidth limit).
- Cosmology story: Let rho_DE be proportional to the channel capacity of the horizon, with bandwidth B proportional to the Hubble rate, B ~ (1+z)^p (p about 1.5 in the matter era). Dark energy then plateaus in the past (power-limited) and declines only when the bandwidth falls.
- Form: density f(z).
  `lambda A, b, p: (lambda z: 1 + A*((1+np.asarray(z,float))**p*np.log1p(b*(1+np.asarray(z,float))**-p)/np.log1p(b) - 1))`

  | name | x0 | scale | lo | hi |
  |------|----|-------|----|----|
  | A | 0.1 | 0.1 | -0.1 | 3.0 |
  | b | 3.0 | 2.0 | 0.01 | 30.0 |
  | p | 1.5 | 0.5 | 0.3 | 3.0 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): u(z) tends to b/ln(1+b), so f tends to 1 + A(b/ln(1+b) - 1), a finite plateau (at most a factor of about 10 for the extreme corner). Never negative for A >= 0.
- Impact if true: the vacuum energy would be limited by a signal-to-noise ceiling instead of by a potential; a thawing-like w > -1 history with an algebraic (not exponential) approach to the early plateau.
- Beyond-background fingerprint: an early plateau of dark energy at 1e-3 to 1e-2 of the total at recombination for the large-A corner (EDE-like constraint on the CMB acoustic scale).
- Prior art: query "Shannon-Hartley channel capacity cosmological horizon dark energy density arXiv". None found for a dark-energy density. Nearest: arXiv:1608.05728 "Information carrying capacity of a cosmological constant" (Simidzija and Martin-Martinez; opened: about recoverable information in fields, no DE density model). Warning: shape overlaps the catalogued "Saturating DE" (monotone, saturating at high z); differences are the algebraic approach and the 1/ln regime.
- Weirdness 3 / Plausibility 2

### Jarzynski rare-event emergent DE
- Field and analogy: Jarzynski's equality gives the free-energy difference as -T ln<exp(-W/T)>. With an exponentially distributed work W the average is closed-form: Delta F = T ln(1 + b/T), dominated by rare low-work events.
- Cosmology story: Let rho_DE be the free-energy gap Delta F of a system driven out of equilibrium by expansion, with T proportional to the scale factor a and work scale b. Then rho_DE(a) = a ln(1 + b/a): it vanishes at early times (about ln(1+z)/(1+z)) and grows toward today, an emergent dark energy with a logarithmic tail. Analogy only.
- Form: density f(z).
  `lambda A, b: (lambda z: 1 + A*(np.log1p(b*(1+np.asarray(z,float)))/(1+np.asarray(z,float))/np.log1p(b) - 1))`

  | name | x0 | scale | lo | hi |
  |------|----|-------|----|----|
  | A | 0.2 | 0.2 | -3.0 | 0.99 |
  | b | 3.0 | 2.0 | 0.01 | 100.0 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): g tends to 0, so f tends to 1 - A: positive for A < 1; with A close to 1 the dark energy is essentially absent at recombination (PEDE-like). Finite everywhere.
- Impact if true: dark energy as a non-equilibrium free-energy gap, so its value is set by fluctuation statistics and the arrow of time rather than by a fixed vacuum constant; phantom-like (w < -1) for A > 0 without a phantom field.
- Beyond-background fingerprint: a w(z) whose phantom depth depends on the work-distribution scale b; tail law ln(1+z)/(1+z) differs from PEDE's (1+z)^-0.87 and is distinguishable by high-z BAO and CMB distance.
- Prior art: query "Jarzynski equality free energy dark energy cosmology arXiv". None found: results are all in statistical mechanics, lattice QFT (arXiv:1710.04435-like) and social systems. Warning: kinematically close to the catalogued PEDE/GEDE at z < 2.
- Weirdness 4 / Plausibility 2

### Saddle-to-saddle staircase
- Field and analogy: In deep linear networks, gradient descent learns the input-output modes one at a time: long plateaus followed by rapid transitions, with larger singular values learned first (Saxe, McClelland and Ganguli, arXiv:1312.6120, opened). The transition times are roughly geometrically spaced.
- Cosmology story: The dark sector "learns" a hierarchy of modes, each switching on as a logistic step in ln(1+z); the earliest-learned mode carries the largest weight (weights 8:4:2:1). The result is a staircase in rho_DE with geometric spacing in ln(1+z) rather than one smooth transition.
- Form: density f(z).
  ```
  def stair(A, z1, Dl, dl):
      w = np.array([1, 2, 4, 8])/15
      Lk = np.log1p(z1) + Dl*np.arange(4)
      S = lambda L: (w*0.5*(1 - np.tanh((np.asarray(L, float)[..., None] - Lk)/dl))).sum(-1)
      return lambda z: 1 + A*(S(np.log1p(np.asarray(z, float))) - S(0.0))
  ```

  | name | x0 | scale | lo | hi |
  |------|----|-------|----|----|
  | A | 0.2 | 0.2 | -3.0 | 0.99 |
  | z1 | 0.3 | 0.2 | 0.02 | 3.0 |
  | Dl | 0.6 | 0.3 | 0.1 | 2.0 |
  | dl | 0.15 | 0.1 | 0.03 | 0.6 |

  LCDM limit: A = 0. Four modes fixed.
- High-z behaviour (z up to 1100): all steps off, f tends to 1 - A (finite, positive for A < 1). Last step at ln(1+z1) + 3 Dl, at most about 7.
- Impact if true: dark energy is a multi-stage relaxation (stepwise phase transitions at geometrically spaced epochs), giving binned-w reconstructions a "wiggly" signature without any oscillating field; might explain why different SN/BAO bins disagree on w.
- Beyond-background fingerprint: a pattern of sound-horizon-scale features at several z, and ISW power in steps; low-z step produces a jump in H(z) derivative.
- Prior art: query "staircase multiple successive steps dark energy equation of state sequence of transitions arXiv". PARTIAL: arXiv:2208.05583 "Multiple transitions in vacuum dark energy and H0 tension" (Moshafi, Firouzjahi, Talebian; opened, form of transitions not stated in the abstract) has several vacuum-energy transitions with free amplitudes. No paper with geometrically spaced, hierarchy-weighted steps or the deep-linear-net motivation was found.
- Weirdness 4 / Plausibility 2

### Doubling-period cyclical schedule
- Field and analogy: Cosine-annealing learning-rate schedules with warm restarts (SGDR) and cyclical learning rates, where each cycle is twice as long as the previous one. Cosine-shaped cycles are C^1 (smooth at restarts).
- Cosmology story: The dark sector is "re-annealed" in cycles whose length doubles in the variable ln(1+z). rho_DE goes up and back to its baseline repeatedly, with ever longer cycles; late-time data see only the first one or two cycles.
- Form: density f(z).
  ```
  def cyc(A, T0, m):
      def f(z):
          s = np.log1p(np.asarray(z, float))/T0
          k = np.floor(np.log1p(s*(m-1))/np.log(m))
          u = (s - (m**k - 1)/(m - 1))/m**k
          return 1 + A*0.5*(1 - np.cos(2*np.pi*u))
      return f
  ```

  | name | x0 | scale | lo | hi |
  |------|----|-------|----|----|
  | A | 0.3 | 0.2 | -0.9 | 3.0 |
  | T0 | 0.5 | 0.3 | 0.3 | 3.0 |
  | m | 2.0 | 0.5 | 1.2 | 4.0 |

  LCDM limit: A = 0. (m = 2 is the SGDR doubling; the cos bump is C^1 so no pole in w.)
- High-z behaviour (z up to 1100): f stays in [1, 1 + A] (bounded, positive for A > -1) with ever slower cycles; the lower bound T0 >= 0.3 keeps |w + 1| below about 3.5 A in the data range.
- Impact if true: dark energy cycles with a self-similar (period-doubling) rhythm in e-folds: the present "dark energy epoch" would be the first cycle of an infinite sequence, so future recurrence of acceleration would be predicted. If real it implies a cyclic rather than monotonic vacuum.
- Beyond-background fingerprint: a modulation of the ISW-lensing cross-correlation at z about e^(T0 * (2^k - 1/2)) - 1, and a mismatch between low-z and high-z w in CPL fits.
- Prior art: query "period-doubling oscillating dark energy periods growing geometrically cyclical cosmology arXiv". None found for this form. Related but different: arXiv:2010.03314 (Tian, "scalar field with oscillating equation of state II"; opened: oscillating scaling to chaotic accelerating solution via period-doubling bifurcation, no explicit doubling-period density), and Linder astro-ph/0511415 "On Oscillating Dark Energy" (opened; explicit oscillation form not read).
- Weirdness 5 / Plausibility 1

### Log-periodic discrete-scale-invariance ring
- Field and analogy: Discrete scale invariance in hierarchical or critical systems gives complex critical exponents, hence corrections of the form x^-beta cos(omega ln x + phi) (Sornette, cond-mat/9707012; "log-periodic power law" in rupture, earthquakes, finance). Also the ring-down of an under-damped momentum optimiser, written in e-folds.
- Cosmology story: The dark sector has a preferred scale ratio (discrete self-similarity), so rho_DE wiggles periodically in ln(1+z) with a power-law envelope. Quasi-periodic wiggles in SN and BAO residuals would be the symptom.
- Form: density f(z).
  `lambda A, om, ph, beta: (lambda z: 1 + A*((1+np.asarray(z,float))**(-beta)*np.cos(om*np.log1p(np.asarray(z,float)) + ph) - np.cos(ph)))`

  | name | x0 | scale | lo | hi |
  |------|----|-------|----|----|
  | A | 0.1 | 0.1 | -0.45 | 0.45 |
  | om | 4.0 | 1.5 | 0.5 | 15.0 |
  | ph | 0.0 | 1.0 | -3.2 | 3.2 |
  | beta | 0.3 | 0.3 | 0.0 | 3.0 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): envelope decays as (1+z)^-beta, so f tends to 1 - A cos(ph) (beta > 0), finite and positive since |A| <= 0.45. For beta = 0 the wiggles persist to z = 1100 (still bounded). In the data range |w + 1| is about A * om / 3 at most.
- Impact if true: a fixed scale ratio e^(2 pi/om) in the vacuum energy would be a fossil of discrete self-similarity (hierarchical structure, "complex dimension") in the dark sector, a very different physical origin from slow-roll.
- Beyond-background fingerprint: log-periodic features in the matter power spectrum and in the redshift distribution of lensing kernels; the same om should reappear in the growth rate.
- Prior art: query "log-periodic oscillations dark energy equation of state discrete scale invariance arXiv". PARTIAL / informal: only an unreviewed Academia.edu draft "Cyclic Tests v2" surfaced (could not be opened, HTTP 403; its content is known only from a search snippet claiming a log-periodic cosine for the dark-energy density, so UNVERIFIED). No arXiv paper found. Oscillating-DE literature exists in a different form (Linder astro-ph/0511415, abstract opened; oscillation variable not confirmed). Treat as KNOWN-in-spirit for plain oscillating DE.
- Weirdness 4 / Plausibility 2

### Dyadic-map chirp
- Field and analogy: The logistic map at r = 4 is solvable: x_n = sin^2(2^n theta), a chaotic orbit with bounded values and exponentially growing frequency in n. Writing n as e-folds gives a chirp.
- Cosmology story: Let rho_DE follow the dyadic orbit, with the iteration index proportional to ln(1+z), so the phase grows as theta (1+z)^k. At low z the density varies slowly; at high z it oscillates so fast that only its average (a constant) matters, giving an effective cosmological constant in the past. Pure curiosity-driven analogy.
- Form: density f(z).
  `lambda A, th, k: (lambda z: 1 + A*(np.sin(th*(1+np.asarray(z,float))**k)**2 - np.sin(th)**2))`

  | name | x0 | scale | lo | hi |
  |------|----|-------|----|----|
  | A | 0.2 | 0.2 | -0.9 | 0.9 |
  | th | 0.5 | 0.3 | 0.05 | 3.2 |
  | k | 1.0 | 0.4 | 0.2 | 2.0 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): f is bounded in [1 - |A|, 1 + |A|] (positive for |A| < 1) with infinitely fast oscillation; the density-only background is smooth in an averaged sense, but w(z) swings wildly (large |w + 1| for z > 1). Floating-point sin of arguments up to about 1e6 is fine for k <= 2.
- Impact if true: the vacuum energy would carry a chaotic, bounded history; the expansion at z < 1 is smooth but H(z) at z > 1 carries unresolved ripples. A strong sanity test for how sparsely the data sample z.
- Beyond-background fingerprint: stochastic-looking residuals in the SN Hubble diagram at z > 1; scatter in BAO distance as a function of z that no smooth model reproduces; extreme sound-speed oscillation at the perturbation level (a strong disfavouring test).
- Prior art: query "logistic map chaotic dark energy density bounded iteration cosmology arXiv". None found for a dyadic-map chirp. Related but different: Beck, arXiv:astro-ph/0310479 "Chaotic scalar fields as models for dark energy" (opened: vacuum energy from the invariant measure of a chaotic field, no explicit time-dependent formula).
- Weirdness 5 / Plausibility 1

### Fold-bifurcation tipping DE
- Field and analogy: Near a saddle-node (fold) bifurcation the order parameter has a square-root dependence on the distance to the tipping point, x - xc ~ sqrt(mu_c - mu), with critical slowing down (diverging variance and relaxation time) as the tipping point nears. Used for early-warning signals in climate and ecosystems.
- Cosmology story: The vacuum state that supplies rho_DE disappears in a fold at a future scale factor a_c = 1 + d. Before that, rho_DE = c + B sqrt(a_c - a): finite, but with infinite slope at a_c. For B < 0 it grows toward a finite-time singularity (rip-like); for B > 0 it collapses (vacuum decay).
- Form: density f(z).
  `lambda A, d: (lambda z: (1 + A*np.sqrt(1 + d - 1/(1+np.asarray(z,float))))/(1 + A*np.sqrt(d)))`

  | name | x0 | scale | lo | hi |
  |------|----|-------|----|----|
  | A | 0.5 | 0.3 | -0.5 | 10.0 |
  | d | 0.5 | 0.3 | 0.02 | 3.0 |

  LCDM limit: A = 0. (a_c = 1 + d is the future scale factor of the tipping point.)
- High-z behaviour (z up to 1100): a tends to 0, f tends to (1 + A sqrt(1+d))/(1 + A sqrt(d)), a finite constant; positive for A > -0.5 given d <= 3. No blow-up.
- Impact if true: the universe is not in a stable de Sitter vacuum but approaching a tipping point at a_c; this gives a falsifiable future (end of acceleration or rip at a_c) and a prediction that dark-energy perturbations show critical slowing down (sound speed to zero) near a_c.
- Beyond-background fingerprint: DE perturbations with growing variance/autocorrelation (critical slowing down) visible as scale-dependent clustering of the DE component at late times; w(z) with a diverging derivative as a_c is approached.
- Prior art: query "saddle-node bifurcation fold tipping point square-root singularity dark energy future cosmology critical slowing down arXiv". None found for this density form. Related: Cotsakis, arXiv:2502.20430 "Cosmic acceleration as a saddle-node bifurcation" (opened: the Friedmann flow in (H, Omega) has a saddle-node, no dark-energy density formula given, and it explicitly avoids a separate dark-energy component).
- Weirdness 4 / Plausibility 3

### Levin-Chaitin universal-prior clock
- Field and analogy: Algorithmic probability: the Levin / Chaitin universal prior assigns weight about 1/(n (ln n)^(1+eps)) to the n-th epoch (the series converges only with eps > 0), tied to Kolmogorov complexity via Levin's coding theorem. The regularised form below is bounded as n tends to 0.
- Cosmology story: rho_DE is proportional to the algorithmic prior weight of the present cosmic time step, g(t) = 1/((x + s) ln(e + x/s)^(1+eps)), with x = t(z)/t0 and s a "minimum description length" cutoff. The universe's energy budget tracks how compressible its current epoch label is. Very speculative.
- Form: uses Om.
  ```
  def levin(A, s, eps, Om):
      q = np.sqrt((1-Om)/Om)
      clock = lambda z: np.arcsinh(q*(1+np.asarray(z, float))**-1.5)
      x = lambda z: clock(z)/clock(0.0)
      g = lambda z: 1/((x(z) + s)*np.log(np.e + x(z)/s)**(1 + eps))
      return lambda z: 1 + A*(g(z)/g(0.0) - 1)
  ```
  (x is the flat LCDM age ratio t(z)/t0, t proportional to arcsinh(sqrt(OL/Om) a^1.5); radiation neglected.)

  | name | x0 | scale | lo | hi |
  |------|----|-------|----|----|
  | A | 0.1 | 0.1 | 0.0 | 3.0 |
  | s | 0.1 | 0.1 | 0.01 | 3.0 |
  | eps | 0.5 | 0.3 | 0.0 | 2.0 |

  LCDM limit: A = 0. A is restricted to A >= 0 because g(z)/g(0) can reach 1e2 to 1e4 at high z, so A < 0 would drive f negative.
- High-z behaviour (z up to 1100): g tends to 1/s (finite, because s regularises x -> 0), so f tends to 1 + A((1+s) ln(e + 1/s)^(1+eps)/s - 1), at most about 1e4 times 3 for the extreme corner. That is of order 1e-5 to 1e-4 of the matter density at recombination: finite and sane.
- Impact if true: dark energy would be a signature of computability constraints on the universe (a "prior over epochs"). Even a mild preference would be a startling link between algorithmic information and the vacuum.
- Beyond-background fingerprint: a time-dependent rather than a-dependent w(z) (the density depends on age), so it differs from the same function of a once Om shifts; also an early-time plateau at 1e-5 level that could show up in precision CMB.
- Prior art: query "algorithmic probability Kolmogorov complexity universal prior dark energy density cosmic time arXiv". None found: only general algorithmic-probability papers (Schmidhuber quant-ph/0011122 on priors over computable universes, no dark energy density).
- Weirdness 5 / Plausibility 1

### Self-evidencing KL information gain
- Field and analogy: Free-energy principle / active inference: an agent that minimises surprise accumulates Bayesian information, measured by KL(posterior || prior). For a Gaussian conjugate update with N observations, KL = (1/2)[ln(1 + kappa N) - kappa N/(1 + kappa N)] (closed form): it starts as N^2 and grows only logarithmically.
- Cosmology story: Let rho_DE be proportional to the information the universe has gained about itself, with N proportional to a^q (more observations later). Then rho_DE is tiny at early times, rises, and keeps growing logarithmically with the scale factor forever. Analogy only.
- Form: density f(z).
  `lambda A, lk, q: (lambda z: 1 + A*((lambda x: np.log1p(x) - x/(1+x))(10**lk*(1+np.asarray(z,float))**(-q))/(lambda x: np.log1p(x) - x/(1+x))(10**lk) - 1))`

  | name | x0 | scale | lo | hi |
  |------|----|-------|----|----|
  | A | 0.2 | 0.2 | -3.0 | 0.99 |
  | lk | 1.0 | 1.0 | -1.0 | 4.0 |
  | q | 1.0 | 0.5 | 0.1 | 3.0 |

  LCDM limit: A = 0. (lk = log10 kappa.)
- High-z behaviour (z up to 1100): K tends to 0 like (1+z)^(-2q), so f tends to 1 - A: finite, positive for A < 1. For tiny x the difference ln(1+x) - x/(1+x) loses precision, but the absolute error (about 1e-16) is negligible against K(0).
- Impact if true: dark energy tracks accumulated information gain, an emergent, phantom-like history (w < -1) that never saturates (log growth), tying the vacuum to the amount of "learning" done by the universe.
- Beyond-background fingerprint: a late-time rise of w toward phantom values in the future and a matching decrease of dark energy in the past; no extra early dark energy for lk small (power-law tail).
- Prior art: query "Bayesian information gain KL divergence free energy principle dark energy cosmological constant arXiv". None found: the KL divergence appears in cosmology only as a forecasting / constraint metric (e.g. arXiv:1606.06273 "Information Gain in Cosmology", arXiv:1607.00270). Warning: at the data level it is a PEDE-like emergent family.
- Weirdness 4 / Plausibility 2

---

## Needs ODE (or an implicit equation)

### Landauer horizon-erasure ledger (KNOWN in recast)
- Equations (derived by the harvester in natural units, not checked): horizon entropy S = pi/(G H^2), T_H = H/2 pi, erasure power per Hubble volume Q = 3 ln2 * eta * H (rho_tot + p_tot), where eta <= 1 is an efficiency. Then drho_DE/dt + 3H(1+w)rho_DE = Q, and matter loses the same energy: drho_m/dt + 3H rho_m = -Q. For w = -1 this is the standard interacting vacuum Q proportional to H rho_m, which is closed-form (rho_m proportional to a^(-3(1 - xi))) and is therefore a "paper-old" family, not new.
- Prior art: query "Landauer principle bit erasure cosmological horizon dark energy interaction arXiv". KNOWN: arXiv:0709.0047 Lee, Lee and Kim, "Quantum Informational Dark Energy: Dark energy from forgetting" (opened: holographic dark energy from Landauer erasure at the event horizon, parameter d about 1); also arXiv:2407.15231 Trivedi, "Landauer's principle and information at the cosmological horizon" (abstract from search results only; versions disagree on whether the horizon erases efficiently).

### Barrow-entropy holographic dark energy (KNOWN)
- Implicit equation: rho_DE = C H^(2-Delta); with E = H/H0: E^2 = Om (1+z)^3 + (1 - Om) E^(2-Delta). Needs a root-finder for E at each z (no closed form for general Delta). LCDM limit: Delta = 2 (rho_DE constant). Physical range 0 <= Delta <= 1.
- Prior art: query "Barrow holographic dark energy H^(2-Delta) observational constraints arXiv". KNOWN: arXiv:2005.10302 Anagnostopoulos, Basilakos and Saridakis, "Observational constraints on Barrow holographic dark energy" (opened; the abstract does not state the explicit rho_DE or the cutoff, so the Hubble-cutoff form above is the harvester's reading); also DESI DR2 BAO study arXiv:2506.03019 (title seen in search only).

### Self-consistent annealing clock (extension of ideas 1 and 10)
- Ideas 1 and 10 use the matter-era / LCDM age as the clock. The self-consistent version makes the clock the actual age: t(z) = integral from z to infinity of dz' / ((1+z') E(z')), with E^2 = Om (1+z)^3 + (1 - Om) f(z) and f depending on t. Equation: df/dt = F(f, t), E from the Friedmann equation. Solve as an ODE in ln a.
