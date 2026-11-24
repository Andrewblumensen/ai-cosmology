# Batch 2 harvest: signal processing, nonlinear dynamics, chaos, special functions

Conventions used below. `x = np.log1p(z)` = ln(1+z) = -ln a. `tau = -x` is e-folds of time (forward = increasing). All w(z) forms are zero-mean or localised oscillations unless stated, so the integrated dark-energy density stays finite at z = 1100. Forms marked `scipy` need `scipy.special` (ellipj, airy, lambertw); lambertw is only called on scalar parameters. No fits were run; nothing here is a result.

Recasting note: every idea is a direct w(z) or f(z); no recasting of G, matter scaling or interactions is needed. Where I say "DE density finite at high z" I mean f(z) = exp(3 * integral of (1+w) dx) stays O(1), so the CMB sees an LCDM-like early universe.

---

### Box-Cox chirp
- Field and analogy: Radar/gravitational-wave chirps (frequency drifting with time) and the exact solution of the fully chaotic logistic map x_n = sin^2(2^n theta), whose phase grows exponentially (Bernoulli shift). Here the phase of w is a Box-Cox power transform of (1+z).
- Cosmology story: A field whose oscillation frequency is set by a Lyapunov-like stretching rate would ring slowly today and ever faster in the past. Averaged over fast oscillations the early universe looks like w = -1 (rapid oscillation averages out), which is how the CMB survives. Pure analogy: no Lagrangian is offered.
- Form: w(z).
  ```python
  # phase = phi0 + th*((1+z)**p - 1)/p ; p->0 gives log-periodic, p=1 gives linear-in-(1+z) chirp
  def chirp(A, th, p, phi0):
      return lambda z: -1 + A*np.cos(phi0 + th*np.expm1(p*np.log1p(np.asarray(z, float)))/p)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.10 | 0.05 | 0.0 | 1.0 |
  | th | 2.0 | 0.5 | 0.2 | 4.0 |
  | p | 0.30 | 0.10 | 0.05 | 0.60 |
  | phi0 | 0.0 | 1.0 | -3.14159 | 3.14159 |

  LCDM limit: A = 0. Present-day w0 = -1 + A cos(phi0), so w0 > -1 with w < -1 earlier is reachable (DESI-like sign pattern).
- High-z behaviour (z up to 1100): |w+1| <= A <= 1. With p = 0.6 and th = 4 the phase reaches about 430 rad (roughly 70 cycles) by z = 1100, so the integrator grid must resolve it; if not, cap p at 0.4. Mean of cos is zero, so f stays near O(1): no blow-up.
- Impact if true: A secular drift of the oscillation frequency would point to a field that is not a fixed-mass oscillator (time-varying mass or stretching phase space), a discriminating test between "rolling field" and "ringing field" dark energy. Fixed-frequency oscillating DE is already fitted in the literature; a drift term would say which kind.
- Beyond-background fingerprint: Growth and ISW would show alternating enhancement and suppression with a drifting period; the fast early oscillations predict a nearly scale-free sound-speed-averaged perturbation (effective w = -1 early).
- Prior art: Query "arXiv chirped oscillating dark energy equation of state w(z) log-periodic oscillation frequency drift". Fixed-frequency oscillating w is KNOWN: Escamilla et al., arXiv:2404.00181 "Testing an oscillatory behavior of dark energy"; Tamayo and Vazquez, arXiv:1901.08679 "Fourier-series expansion of the dark-energy equation of state"; arXiv:1003.6084 "Oscillations in the dark energy EoS: new MCMC lessons" (all abstracts opened). A frequency-drifting (chirp) phase: none found. So the family is KNOWN, the chirp is not.
- Weirdness (1-5) / Plausibility (1-5): 4 / 2

---

### Stuart-Landau Hopf cycle
- Field and analogy: Nonlinear dynamics. The normal form of a supercritical Hopf bifurcation, dZ/dtau = (mu + i omega) Z - (1 + i b)|Z|^2 Z, has an exact closed-form amplitude (logistic in |Z|^2) and an exact phase (log term).
- Cosmology story: Dark energy sits at w = -1 (fixed point) in the past; as the universe expands the fixed point loses stability (matter dilution acts as the bifurcation parameter) and the field settles onto a limit cycle of fixed amplitude sqrt(mu). The oscillation then switches on smoothly instead of being imposed by hand.
- Form: w(z). Exact solution with tau = -ln(1+z), u = |Z|^2, u(0) = mu*s (s in [0,1] guarantees no finite-z pole), phase theta(0) = 0.
  ```python
  def hopf(mu, s, om, b):
      def w(z):
          tau = -np.log1p(np.asarray(z, float))
          e = np.exp(2*mu*tau)
          den = s*e + 1 - s
          u = mu*s*e/den
          th = om*tau + 0.5*b*np.log(den)       # integral of (om + b*u) dtau, exact
          return -1 + np.sqrt(u)*np.cos(th)
      return w
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | mu | 0.25 | 0.10 | 0.01 | 1.0 |
  | s | 0.30 | 0.20 | 0.0 | 1.0 |
  | om | 3.0 | 1.0 | 0.2 | 12.0 |
  | b | 0.0 | 1.0 | -6.0 | 6.0 |

  LCDM limit: s = 0. Fixing theta(0) = 0 means w0 = -1 + sqrt(mu*s) (>= -1) and w dips below -1 further back.
- High-z behaviour (z up to 1100): u ~ mu*s*(1+z)^(-2mu)/(1-s) -> 0, so w -> -1 and f -> const. At s = 1 the amplitude is constant sqrt(mu) <= 1 at all z (still zero-mean, so finite). |w+1| <= 1.
- Impact if true: Dark energy would be a self-sustained oscillator (limit cycle) born at a Hopf bifurcation, giving a definite amplitude-frequency relation and an "onset redshift". It would turn "why now" into "when the bifurcation parameter crossed zero".
- Beyond-background fingerprint: The amplitude-dependent frequency (b term) gives a specific correlation between w oscillation period and amplitude; growth rate modulated at the cycle frequency.
- Prior art: Query "arXiv Hopf bifurcation limit cycle dark energy equation of state Stuart-Landau amplitude equation late-time expansion". Results were all non-cosmology Stuart-Landau papers. none found.
- Weirdness (1-5) / Plausibility (1-5): 5 / 2

---

### Cnoidal wave w
- Field and analogy: Water waves and KdV theory. A nonlinear oscillator (Duffing/pendulum, KdV cnoidal wave) has an exact Jacobi elliptic solution cn(u, m). Modulus m = 0 gives a cosine, m -> 1 gives well-separated solitons (sech pulses of alternating sign).
- Cosmology story: If the dark-energy field is a strongly anharmonic oscillator, its w(t) is not a sine but a cnoidal wave, with sharp pulses separated by long plateaus at w = -1 + 0. One extra parameter (m) interpolates from "ringing" to "intermittent solitary events".
- Form: w(z). Needs `scipy.special.ellipj`.
  ```python
  from scipy.special import ellipj
  def cnoidal(A, om, m, phi):
      return lambda z: -1 + A*ellipj(om*np.log1p(np.asarray(z, float)) + phi, m)[1]
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.10 | 0.05 | 0.0 | 1.0 |
  | om | 3.0 | 1.0 | 0.3 | 12.0 |
  | m | 0.5 | 0.2 | 0.0 | 0.999 |
  | phi | 0.0 | 1.0 | -3.14159 | 3.14159 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): |w+1| <= A <= 1, cn has zero mean over its period, so f stays O(1). About om*7/(2*pi) cycles (for m near 1 the period is longer, 4K(m)/om), at most about 13 cycles: well resolved.
- Impact if true: A flat-topped or spiky, non-sinusoidal w(z) is a direct measure of field self-interaction strength; it would show up as harmonics in a Fourier decomposition of the reconstructed w (the sinusoid-only fits would see excess power at 3x, 5x the base frequency).
- Beyond-background fingerprint: Harmonic content in w implies the perturbation sound speed also has harmonics; short "events" would give brief bursts in the ISW/growth history.
- Prior art: Query "arXiv Jacobi elliptic function cnoidal wave dark energy equation of state oscillation". Adjacent only: Debnath arXiv:2112.00296 "Roles of Modified Chaplygin-Jacobi and Chaplygin-Abel Gases in FRW Universe" (abstract opened) uses Jacobi functions to generate a Chaplygin-type equation of state, not a cn oscillation of w; Bamba and Yesmakhanova arXiv:1203.3401 uses Weierstrass zeta (not opened). For cn(w) itself: none found.
- Weirdness (1-5) / Plausibility (1-5): 4 / 2

---

### Gabor atom in w
- Field and analogy: Time-frequency analysis. A Gabor/Morlet atom (Gaussian envelope times cosine) is the minimum-uncertainty localised oscillation; it is the basic building block of wavelet transforms.
- Cosmology story: One finite wave packet of w, launched at some redshift and gone afterwards: a transient oscillation rather than a global one. This is the "wavelet-localised" version of oscillating dark energy, with centre, width and carrier frequency as independent parameters.
- Form: w(z).
  ```python
  def gabor(A, xc, sg, k):
      def w(z):
          x = np.log1p(np.asarray(z, float)) - xc
          return -1 + A*np.exp(-0.5*(x/sg)**2)*np.cos(k*x)
      return w
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.10 | 0.05 | -1.0 | 1.0 |
  | xc | 0.40 | 0.15 | 0.05 | 2.0 |
  | sg | 0.40 | 0.15 | 0.10 | 1.5 |
  | k | 6.0 | 2.0 | 1.0 | 20.0 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): Gaussian tail; at z = 1100 (x = 7) the envelope is below 4e-3 even for xc = 2, sg = 1.5, so w = -1 and f is constant. No blow-up.
- Impact if true: A localised packet says dark energy had one "event" in a limited epoch (a transient dynamical episode), not a global slow drift. If the best packet sits at z of 0.3 to 1 it would link to the DESI hint of a mid-redshift feature.
- Beyond-background fingerprint: Growth anomaly confined to the packet epoch; a signature in fsigma8 localised in redshift.
- Prior art: KNOWN (partly). Query "arXiv Morlet wavelet Gabor localized oscillation dark energy equation of state parametrization". Hojjati, Pogosian, Zhao, arXiv:0912.4843 "Detecting Features in the Dark Energy Equation of State: A Wavelet Approach" (abstract opened) reconstructs bumps in w with wavelets; oscillating w is KNOWN (arXiv:2404.00181). A single Gabor atom as a parametric model: none found.
- Weirdness (1-5) / Plausibility (1-5): 3 / 2

---

### Chebyshev equiripple dark energy
- Field and analogy: Analog filter design. A Chebyshev type-I low-pass has |H|^2 = 1/(1 + eps^2 T_n(x)^2): equal ripple inside the passband (x <= 1), monotonic roll-off ~ x^(-n) outside. Order n sets how many ripples; for non-integer n the analytic continuation of T_n is used.
- Cosmology story: Dark energy as the output of a chain of n weakly coupled resonant modes (a coupled-resonator filter): it responds with ripples while the driving "frequency" ln(1+z) is below a cutoff and shuts off above it. This builds in the CMB-safe "off at early times" behaviour with a physically named shape rather than a tanh.
- Form: w(z). Signed amplitude A allows phantom side too.
  ```python
  def cheby(A, eps, n, xc):
      def w(z):
          x = np.log1p(np.asarray(z, float))/xc
          xi = np.minimum(x, 1.0); xo = np.maximum(x, 1.0)
          Tn = np.where(x <= 1.0, np.cos(n*np.arccos(xi)), np.cosh(n*np.arccosh(xo)))
          return -1 + A/np.sqrt(1.0 + (eps*Tn)**2)
      return w
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.10 | 0.05 | -1.0 | 1.0 |
  | eps | 0.5 | 0.2 | 0.05 | 1.5 |
  | n | 2.5 | 0.7 | 1.2 | 8.0 |
  | xc | 1.0 | 0.4 | 0.2 | 3.0 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): w + 1 ~ A/(eps*T_n) falls as x^(-n), n > 1, so the integral converges; f tends to a finite constant (about exp(3*A*xc*O(1))), not zero: early dark energy is a constant of order a few times rho_DE0 at most for A <= 0.3, negligible against matter at z = 1100. Not zero-mean: for A > 0 the density grows toward the past, then saturates.
- Impact if true: Ripples with equal amplitude and a sharp cutoff would identify dark energy as an n-mode composite, and n would count the active modes. Even a null is informative: ripple count and cutoff are physical, interpretable fit outputs.
- Beyond-background fingerprint: Equal-height w ripples imply a regular comb of growth bumps in the low-z fsigma8; the stopband implies no early dark energy signal in CMB lensing.
- Prior art: Query "arXiv Chebyshev filter equiripple dark energy equation of state passband". Only Chebyshev polynomial expansions of w (arXiv:1712.07978, arXiv:1304.5532 "The Dark Energy Cosmic Clock", abstract opened) exist; those are polynomial bases, not a filter magnitude response. none found for the filter form.
- Weirdness (1-5) / Plausibility (1-5): 5 / 1

---

### Airy turning-point wave
- Field and analogy: Quantum mechanics/WKB. The Airy function Ai(x) is the exact solution near a classical turning point: oscillatory with increasing frequency in the allowed region, exponentially (super-exponentially) dying in the forbidden region.
- Cosmology story: A dark-energy mode crossing a turning point of its effective potential as the universe expands: before the turning point (high z) the mode is evanescent and w = -1; after it (low z) it oscillates, with frequency rising towards today and amplitude falling like |arg|^(-1/4). Only 3 parameters.
- Form: w(z). Needs `scipy.special.airy`.
  ```python
  from scipy.special import airy
  def airy_w(A, s, xt):
      return lambda z: -1 + A*airy(s*(np.log1p(np.asarray(z, float)) - xt))[0]
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.30 | 0.20 | -3.0 | 3.0 |
  | s | 3.0 | 1.0 | 0.5 | 10.0 |
  | xt | 0.5 | 0.3 | 0.0 | 3.0 |

  LCDM limit: A = 0. Ai peaks at 0.536, so |w+1| <= 1.6 at A = 3.
- High-z behaviour (z up to 1100): For x >> xt, Ai ~ exp(-(2/3)(s(x-xt))^1.5): w = -1 exactly for z above e^(xt + few/s) - 1, f constant. Finite, sane.
- Impact if true: Dark energy would have a turning point: a definite redshift where its effective restoring force changes sign. That is a sharper statement than "w crosses -1" and ties the onset of dynamics to one scale xt.
- Beyond-background fingerprint: Chirp-up of the w oscillation toward today with falling amplitude; perturbations would show a sound-horizon-like resonance condition at xt.
- Prior art: Query "arXiv Airy function turning point dark energy equation of state parametrization". Only the unrelated quadratic "turning point" parametrisation arXiv:1401.5615 (Hu et al.) and an Airy use for tachyonic dark-matter production arXiv:2601.07670 (not opened, different subject). none found for Airy w(z).
- Weirdness (1-5) / Plausibility (1-5): 5 / 2

---

### Delayed-feedback Hopf (Lambert W)
- Field and analogy: Delay differential equations (laser feedback, population cycles, control with latency). The linear equation y'(tau) = -a*y(tau - d) has characteristic roots s = W0(-gamma)/d (Lambert W, gamma = a*d), and it becomes unstable (oscillation grows) exactly when gamma > pi/2: a delayed-feedback Hopf bifurcation. Damping and frequency are tied by one number, not two free parameters.
- Cosmology story: Dark energy responds to the state of the universe with a causal lag of d e-folds. For gamma just above pi/2 the dominant mode is a growing oscillation, so w is -1 early and oscillates with rising amplitude toward today; the frequency/growth ratio is fixed by gamma alone.
- Form: w(z). Needs `scipy.special.lambertw` (scalar call only).
  ```python
  from scipy.special import lambertw
  def delay_hopf(A, gam, d, phi):
      s = complex(lambertw(-gam, 0))/d          # growth rate (Re>0 for gam>pi/2) + frequency (Im)
      return lambda z: -1 + A*np.real(np.exp(-s*np.log1p(np.asarray(z, float)) + 1j*phi))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.10 | 0.05 | -1.0 | 1.0 |
  | gam | 2.0 | 0.5 | 1.6 | 8.0 |
  | d | 0.40 | 0.15 | 0.15 | 2.0 |
  | phi | 0.0 | 1.0 | -3.14159 | 3.14159 |

  LCDM limit: A = 0. Lower bound gam = 1.6 is just above pi/2 so that Re(s) > 0 (damped-forward roots would blow up in the past).
- High-z behaviour (z up to 1100): amplitude A*exp(-Re(s)*x) decays into the past, w -> -1, f -> constant. Only the dominant root is kept (other branches decay faster forward; check the single-mode truncation is not what drives a fit). |w+1| <= A.
- Impact if true: A measurable "latency" in the dark sector (delay in e-folds) and a fixed ratio between growth and frequency of the oscillation: a falsifiable relation with no free damping. It would suggest memory/causal-lag physics in dark energy.
- Beyond-background fingerprint: Ratio of oscillation period to amplitude e-folding time is a pure function of gamma; growth and ISW show the same linked period.
- Prior art: Query "arXiv delay differential equation time-delayed dark energy Lambert W oscillation cosmology". Adjacent: arXiv:2111.10742 "Testing time-delayed cosmology" (abstract opened) puts a delay in the Friedmann equation, not a delayed-feedback oscillation of w; arXiv:2504.05705 fractional time-delayed cosmology (not opened). For a delay-Hopf w(z): none found.
- Weirdness (1-5) / Plausibility (1-5): 5 / 2

---

### Adler phase-slip dark energy
- Field and analogy: Overdamped Josephson junction / phase-locked loop / driven pendulum: dtheta/dtau = omega - K sin(theta) (Adler equation). For omega > K it is solved exactly by tan(theta/2) = mu + sqrt(1-mu^2) tan(...), with mu = K/omega. It is intermittent: long dwell near the bottleneck, quick 2*pi phase slips (a saddle-node ghost, as in type-I intermittency).
- Cosmology story: The cosine of the phase is w + 1. The universe spends long stretches near a "stuck" value then slips rapidly; the shape is strongly non-sinusoidal when mu approaches 1 and sinusoidal at mu = 0. The mean of cos(theta) over a full cycle is exactly zero for this flow, so no net density drift.
- Form: w(z). Closed form, no poles.
  ```python
  def adler(A, mu, om, ph0):
      q = np.sqrt(1 - mu**2)
      def w(z):
          tau = -np.log1p(np.asarray(z, float))
          ph = ph0 + 0.5*om*q*tau
          N = mu*np.cos(ph) + q*np.sin(ph); D = np.cos(ph)       # tan(theta/2) = N/D
          return -1 + A*(D**2 - N**2)/(D**2 + N**2)               # cos(theta)
      return w
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.10 | 0.05 | 0.0 | 1.0 |
  | mu | 0.5 | 0.2 | 0.0 | 0.98 |
  | om | 3.0 | 1.0 | 0.3 | 15.0 |
  | ph0 | 0.0 | 0.5 | -1.5708 | 1.5708 |

  LCDM limit: A = 0.
- High-z behaviour (z up to 1100): Periodic, bounded |w+1| <= A <= 1, zero mean per cycle, so f stays O(1) (it oscillates around 1). Number of cycles up to om*q*7/(2*pi) <= about 17: resolved. No decay, so the CMB-era DE density is of order rho_DE0, which is tiny against matter at z = 1100.
- Impact if true: Dark energy as a phase-locked oscillator with "phase slips": the data could pick the dwell-and-slip waveform over a sine; the dwell plateau would also look like a constant-w phase at an unusual w.
- Beyond-background fingerprint: Non-sinusoidal w implies spiky epochs in the growth rate and ISW; the exact dwell-time/period ratio is fixed by mu.
- Prior art: Query "arXiv Adler equation phase slip Josephson junction analogy dark energy cosmology". Adjacent only: Beck, arXiv:1110.5871 "Testing axion physics in a Josephson junction environment" (axion misalignment angle obeys a Josephson-junction equation; lab test, not an expansion-history model; not opened). none found for an Adler-type w(z).
- Weirdness (1-5) / Plausibility (1-5): 5 / 1

---

### Binomial-cascade staircase
- Field and analogy: Turbulence and multifractals. The cumulative distribution of a binomial multiplicative cascade (weights p and 1-p repeatedly splitting an interval) is a devil's-staircase-like singular monotone function. At p = 0.5 it is the straight line.
- Cosmology story: Dark-energy density builds up in the cascade fashion: energy handed down log-scale by log-scale, with asymmetry p deciding how unevenly it lands in early versus late e-folds. p = 0.5 is smooth log-growth; p far from 0.5 gives plateaus separated by sharp steps in ln(1+z). Pure analogy.
- Form: density f(z), f(0) = 1. Finite recursion (depth 6), fully vectorised.
  ```python
  def _casc(u, p, depth=6):
      u = np.clip(u, 0.0, 1.0); F = np.zeros_like(u); wt = np.ones_like(u)
      for _ in range(depth):
          left = u < 0.5
          F = F + np.where(left, 0.0, wt*p)
          wt = wt*np.where(left, p, 1.0 - p)
          u = np.where(left, 2*u, 2*u - 1)
      return F + wt*u                              # F(0)=0, F(1)=1, continuous
  def cascade(A, p, xs):
      return lambda z: 1 + A*_casc(np.log1p(np.asarray(z, float))/xs, p)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.10 | 0.10 | -0.9 | 5.0 |
  | p | 0.5 | 0.1 | 0.2 | 0.8 |
  | xs | 2.0 | 0.7 | 0.3 | 7.0 |

  LCDM limit: A = 0. (p = 0.5 with A != 0 gives f = 1 + A x/xs, a logarithmic density law, which is not LCDM.)
- High-z behaviour (z up to 1100): u clipped at 1 for ln(1+z) > xs, so f -> 1 + A (constant, positive since A > -0.9). Monotone in z. Caveat: the effective w = -1 + (1+z) f'/(3f) inherits the staircase slopes up to (2*max(p,1-p))^depth (about 17 at p = 0.8, depth 6), so the |w+1| < 4 pathology check can trip for large A/xs; the scorer will tell.
- Impact if true: Scale-by-scale, intermittent build-up of dark energy would link it to cascade physics (structure formation or turbulent energy transfer) and imply w jumps between plateaus; A positive result would be remarkable, and the fit (the p value) directly measures the asymmetry.
- Beyond-background fingerprint: Step-like features in H(z)/growth at the cascade breakpoints; the pattern is self-similar in ln(1+z), so breakpoints sit at fixed ratios.
- Prior art: Query "arXiv devil's staircase multiplicative cascade singular function dark energy density history". Cascades exist in cosmology only as models for density-field statistics (arXiv:2004.10155 "Scale Symmetry in the Universe", snippet only, not opened); none found for dark-energy density history.
- Weirdness (1-5) / Plausibility (1-5): 5 / 1

---

### Glassy KWW relaxation clock
- Field and analogy: Glasses and disordered media. Relaxation follows a Kohlrausch-Williams-Watts stretched exponential exp(-(t/tau)^beta), the superposition of many exponentials with a distribution of rates (beta < 1 means a broad distribution).
- Cosmology story: The vacuum energy is a relaxing glassy system; each independent sector relaxes at its own rate, giving a stretched exponential in proper time rather than a single exponential. Proper time comes from the LCDM clock with the fitted Om, a stated approximation.
- Form: uses Om. Proper-time fraction T(z) = t(z)/t0 for flat LCDM; f(0) = 1.
  ```python
  def kww(A, tau, beta, Om):
      k = np.sqrt((1 - Om)/Om)
      T = lambda z: np.arcsinh(k*(1 + np.asarray(z, float))**-1.5)/np.arcsinh(k)
      den = 1 + A*np.exp(-(1.0/tau)**beta)
      return lambda z: (1 + A*np.exp(-(T(z)/tau)**beta))/den
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.10 | 0.10 | -0.9 | 10.0 |
  | tau | 0.5 | 0.2 | 0.05 | 3.0 |
  | beta | 0.7 | 0.2 | 0.2 | 3.0 |

  LCDM limit: A = 0. Set `uses_om = True`.
- High-z behaviour (z up to 1100): T -> 0 so exp -> 1 and f -> (1+A)/den, a finite constant; positive since A > -0.9. Monotone in z for A > 0.
- Impact if true: A stretched (beta < 1) rather than plain exponential decay of vacuum energy would signal many relaxation channels, i.e. an underlying disordered or multi-component vacuum; beta = 1 collapses to the standard decaying-Lambda story.
- Beyond-background fingerprint: Time-varying vacuum energy needs energy exchange with matter (modified growth, a changed matter dilution); clock-based DE also shifts the age of the universe by a computable amount.
- Prior art: Query "arXiv stretched exponential Kohlrausch relaxation dark energy decaying vacuum Lambda(t)". Exponential decaying vacuum is KNOWN: arXiv:1804.03113 "From quantum unstable systems to the decaying dark energy: Cosmological implications" (abstract opened). Stretched-exponential version: none found.
- Weirdness (1-5) / Plausibility (1-5): 3 / 2

---

## Summary table

| # | Name | Type | Weirdness | KNOWN? |
|---|---|---|---|---|
| 1 | Box-Cox chirp | w | 4 | family KNOWN, chirp not found |
| 2 | Stuart-Landau Hopf cycle | w | 5 | no |
| 3 | Cnoidal wave w | w | 4 | adjacent only |
| 4 | Gabor atom in w | w | 3 | KNOWN (partly) |
| 5 | Chebyshev equiripple | w | 5 | no |
| 6 | Airy turning-point wave | w | 5 | no |
| 7 | Delayed-feedback Hopf | w | 5 | adjacent only |
| 8 | Adler phase-slip | w | 5 | no |
| 9 | Binomial-cascade staircase | f | 5 | no |
| 10 | Glassy KWW relaxation clock | f (Om) | 3 | adjacent only |

## Needs ODE

1. **Kuramoto / Ott-Antonsen with Hubble-diluted frequency spread.** Order parameter u = r^2 obeys du/dtau = (K - 2*Delta0*exp(-p*tau)) u - K u^2 (tau = ln a); closed form needs an incomplete gamma, so it is a one-line ODE. Dark-energy density follows f = (1 + eps*u)/(1 + eps*u0). Without the time-dependent Delta it is just a logistic in ln(1+z), which is probably covered by existing saturating models, so I did not list it.
2. **Painleve II Hastings-McLeod.** u'' = 2u^3 + x*u (alpha = 0), with u ~ Ai(x) as x -> +infinity and u ~ sqrt(-x/2) as x -> -infinity; set w + 1 = A*u(s*(ln(1+z) - xt)). A boundary-value solution, so no closed form; an interpolated tabulation would make it usable. Behaviour is an Airy-like decay that turns into a sqrt rise, the opposite of the Airy idea above.
3. **van der Pol relaxation oscillator.** x'' - eps*(1 - x^2) x' + x = 0 with tau = ln a: relaxation oscillations for large eps (slow drift, sudden jumps); the weakly nonlinear limit is the Stuart-Landau idea above.
4. **FitzHugh-Nagumo excitable spike.** dv/dtau = v - v^3/3 - r + I(a); dr/dtau = eps*(v + a - b*r). Dark energy is quiescent until a trigger (matter density crossing a threshold) fires one spike and then a refractory recovery. Needs the ODE (or a tabulated spike template).
5. **Lorenz-forced w.** w + 1 = A*x_L(s*ln(1+z)) for the Lorenz-63 attractor: chaotic but bounded; reproducibility needs a fixed initial condition and is probably over-parameterised.
