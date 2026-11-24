# Batch 2 harvest: pure mathematics, mathematical physics, quantum foundations / information

Harvester field cluster: math, math-phys, quantum foundations and information.
10 ideas. Notation: `x = ln(1+z)` (e-folds back in time). All code is closed form, numpy only
(`import numpy as np`), vectorised over z (array or scalar). No fits were run, no numbers computed.
Every density model has f(0)=1 by construction and is positive for the stated bounds.

Prior-art searches were run on 2026-11-24 (web search, then abstracts opened for every paper cited).
"none found" means the web search for the exact idea in a cosmology context returned nothing; it
is not proof of absence.

---

### Mittag-Leffler memory relaxation
- Field and analogy: Fractional calculus / anomalous relaxation in glassy and viscoelastic media. A system with a power-law memory kernel relaxes as the Mittag-Leffler function E_a(-t^a), which has a fast initial drop and a heavy power-law tail instead of an exponential. Here the Mainardi rational approximation 1/(1+u^a/Gamma(1+a)) is used so no special function is needed.
- Cosmology story: Dark energy was "kicked" at some early redshift z_i and has been relaxing since with a memory kernel, so rho_DE keeps drifting as a power law in e-fold time instead of settling to a constant. It is an analogy: the kernel is imposed, not derived from an action.
- Form: density f(z).
  ```python
  def make(A, s, al, zi):
      g = __import__('math').gamma(1 + al)
      def f(z):
          z = np.asarray(z, dtype=float)
          M = lambda u: 1.0 / (1.0 + u**al / g)
          u = s * np.log((1 + zi) / (1 + np.minimum(z, zi)))   # relaxation clock, 0 at z>=zi
          u0 = s * np.log(1 + zi)
          return (1 + A * M(u)) / (1 + A * M(u0))
      return f
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A  | 0.3 | 0.2 | -0.9 | 5 |
  | s  | 1.0 | 0.3 | 0.05 | 20 |
  | al | 0.7 | 0.1 | 0.15 | 1.0 |
  | zi | 5.0 | 1.0 | 3.0 | 1100 |

  LCDM limit: A=0.
- High-z behaviour (z up to 1100): f is exactly constant for z >= z_i, equal to (1+A)/(1+A*M(u0)); finite, positive (A > -0.9), no blow-up. For al<1 the slope at z_i is infinite (a cusp), which is why z_i is bounded below by 3 (outside the scored data range).
- Impact if true: Dark energy would carry a memory of an early-universe event; w(z) would be a power-law relaxation with a tunable fractional order, which would link the DESI "evolving w" hint to a single non-integer exponent.
- Beyond-background fingerprint: Slow power-law drift of the dark-energy perturbation sound speed / growth suppression; a fractional-order system also predicts non-exponential (power-law) late-time approach to de Sitter, which no integer-order scalar field does.
- Prior art: query "arXiv Mittag-Leffler relaxation dark energy density fractional memory kernel cosmology" and "fractional Friedmann equation Caputo derivative dark energy Mittag-Leffler scale factor". Specific form (ML relaxation of rho_DE from an early kick): none found. Related fractional cosmology is KNOWN as a family: arXiv:2207.00878 (Leon et al., "Cosmology under the fractional calculus approach"; Caputo-modified Friedmann equations, acceleration without dark energy), arXiv:1011.3304 (fractional Friedmann equations with Mittag-Leffler form). Those modify the equations; this idea instead imposes the memory on the DE density, so it is a different object. Status: related-KNOWN, exact form none found.
- Weirdness / Plausibility: 4 / 2

### Riemann-zero log-periodic Lambda
- Field and analogy: Number theory and quantum chaos. The Berry-Keating Hamiltonian H = xp generates dilations and its (conjectured) spectrum is the imaginary parts of the Riemann zeros; the explicit formula writes the prime-counting fluctuation as a sum of (x^{1/2}) cos(gamma_k ln x). Cosmic expansion is a dilation, so ln a is the natural "x".
- Cosmology story: The vacuum energy is a smooth Weyl-law term plus oscillating quantum-chaos corrections whose frequencies in ln(1+z) are the first Riemann zeros (14.13, 21.02, 25.01, 30.42, 32.94), with an amplitude decaying as (1+z)^(-m) like the explicit formula. Honest: a numerological analogy; the free scale s allows the unit of "log time" to be wrong.
- Form: density f(z).
  ```python
  GAM = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062])
  def make(A, m, phi, s):
      W = GAM[0] / GAM                       # weights 1, 0.67, 0.56, 0.46, 0.43
      def S(z):
          x = np.log1p(np.asarray(z, dtype=float))
          return np.exp(-m * x) * (W * np.cos(s * GAM * x[..., None] + phi)).sum(-1)
      return lambda z: 1 + A * (S(z) - S(0.0))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A   | 0.02 | 0.02 | -0.12 | 0.12 |
  | m   | 0.5  | 0.3  | 0.0   | 3.0 |
  | phi | 0.0  | 1.0  | -3.1416 | 3.1416 |
  | s   | 0.3  | 0.05 | 0.05  | 2.0 |

  (`S(0.0)` works as written because `x[..., None]` on a 0-d array gives shape (1,).)
  LCDM limit: A=0.
- High-z behaviour (z up to 1100): for m>0 the oscillation decays; f -> 1 - A*S(0) where |S(0)| <= 3.13, so f >= 0.62 for A <= 0.12. Bounded, positive, no blow-up. Frequencies are fast at s=1 (about 10 radians over z 0 to 1), so the SN data will pin s to small values; that is itself the test.
- Impact if true: Vacuum energy encodes arithmetic of the primes; the expansion history would show a discrete, universal set of log-periodic frequencies with fixed ratios (1 : 1.49 : 1.77 : 2.15 : 2.33), a parameter-free prediction once s is fixed.
- Beyond-background fingerprint: Same fixed frequency ratios should appear as oscillations in the BAO distance residuals at all redshifts and as tiny log-periodic wiggles in the growth rate; a null result at ratios 1.49, 1.77 kills it cleanly.
- Prior art: query "arXiv Riemann zeta zeros log-periodic oscillation dark energy cosmological constant Berry-Keating" and "arXiv log-periodic oscillations dark energy equation of state discrete scale invariance supernovae BAO". None found for zeta-zero frequencies in dark energy (results were Berry-Keating quantum-chaos papers, e.g. arXiv:0712.0705, with no cosmology). Generic oscillating dark energy is KNOWN (arXiv:0709.4234, "Cosmological bounds on oscillating dark energy models", opened and read) but uses free frequencies, not a fixed spectrum.
- Weirdness / Plausibility: 5 / 1

### Weierstrass-Mandelbrot fractal Lambda
- Field and analogy: Fractal geometry. The Weierstrass-Mandelbrot function (Berry and Lewis 1980) is continuous, nowhere differentiable with graph dimension D, and has no intrinsic scale beyond the ratio b (discrete scale invariance with complex fractal dimensions).
- Cosmology story: The dark-energy density, as a function of e-fold time, is a fractal curve of dimension D: it wiggles at every scale with power-law-decaying amplitude, like a vacuum energy that is the sum of a tower of modes spaced by a fixed factor b. Honest: a phenomenological texture, no dynamical origin.
- Form: density f(z).
  ```python
  def make(A, D, b):
      n = np.arange(-6, 7)                    # truncation: scales b^-6 .. b^6
      def W(z):
          x = np.log1p(np.asarray(z, dtype=float))[..., None]
          return ((1 - np.cos(b**n * x)) / b**((2 - D) * n)).sum(-1)
      return lambda z: 1 + A * W(z)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.02 | 0.03 | -0.15 | 0.15 |
  | D | 1.5  | 0.1  | 1.05  | 1.9 |
  | b | 2.0  | 0.3  | 1.5   | 6.0 |

  LCDM limit: A=0.
- High-z behaviour (z up to 1100): W is bounded (every term is in [0, 2 b^(-(2-D)n)] and the sum is truncated), W(0)=0 so f(0)=1. |W| is at most about 6 at x=7 for the bounds above, so f stays positive for |A|<=0.15. No blow-up. Derivative-based w picks up terms of size A*b^(n(D-1)), kept below the |w|>4 pathology flag by the truncation at n=6.
- Impact if true: Dark energy would be a self-similar object in e-fold time, with a measurable fractal dimension; a clean null on D would rule out scale-free "texture" in the expansion history at the percent level.
- Beyond-background fingerprint: High-frequency structure in the BAO/SN residuals with a fixed ratio b between successive scales (discrete scale invariance); also a stochastic-like tail in the ISW signal.
- Prior art: query "arXiv Weierstrass-Mandelbrot fractal function dark energy expansion history". None found (the nearest was arXiv:1203.4226, "Periodic Cosmological Evolutions of Equation of State for Dark Energy", opened and read: it uses Weierstrass elliptic functions, an unrelated object; Calcagni's multifractional dark energy uses fractal measures, not this function).
- Weirdness / Plausibility: 5 / 1

### Binomial-cascade singular dark energy
- Field and analogy: Multifractal measures from turbulence and number theory (the binomial p-model, de Rham curve, Cantor/devil's-staircase family). The cumulative distribution of a binomial cascade is continuous and strictly increasing but has zero derivative almost everywhere (for p != 1/2).
- Cosmology story: Dark energy is released through a cascade of splitting events in e-fold time: each epoch interval sends a fraction p of its remaining budget to its first half. The accumulated density is a singular multifractal staircase, so w = -1 almost everywhere and the "evolution" happens on a fractal set of epochs.
- Form: density f(z).
  ```python
  def make(A, p, L):
      def f(z):
          r = np.clip(np.log1p(np.asarray(z, dtype=float)) / L, 0.0, 1 - 1e-12)
          F = np.zeros_like(r)
          m = np.ones_like(r)
          for _ in range(12):                 # 12 binary digits, linear remainder below
              r = 2 * r
              b = np.floor(r)
              r = r - b
              F = F + np.where(b == 1, m * p, 0.0)
              m = m * np.where(b == 1, 1 - p, p)
          return 1 + A * (F + m * r)
      return f
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.2 | 0.1 | -0.9 | 2.0 |
  | p | 0.35 | 0.08 | 0.02 | 0.98 |
  | L | 2.0 | 0.4 | 0.3 | 7.0 |

  LCDM limit: A=0. (p=0.5 gives f linear in ln(1+z), not LCDM.)
- High-z behaviour (z up to 1100): x is clipped at L, so F saturates at 1 and f = 1+A for z >= e^L - 1. Finite, positive for A > -0.9. The 12-digit truncation with linear remainder gives a continuous piecewise-smooth curve with resolution 2^-12 of the span, so the formally singular w is a rough but finite function (jumps of the numeric gradient may trip the pole flag for p far from 0.5; that is informative).
- Impact if true: Dark energy "turns on" in a scale-free cascade rather than a smooth transition; a fit that prefers p far from 0.5 would show the evolution is concentrated on a set of measure zero, a completely new category.
- Beyond-background fingerprint: Epoch-selective energy injection events imply sharp, localised features in H(z) (bursts), visible as correlated residual steps in BAO at specific z bins and in cosmic-chronometer data; no scalar-field model predicts that.
- Prior art: query "arXiv multifractal binomial cascade devil's staircase dark energy density cosmology". None found for dark energy (hits: Gaite, arXiv:2004.10155 "Scale Symmetry in the Universe", multifractal mass distribution from cascades, not DE; Saint-Mont arXiv:2103.14390, math of the p-model).
- Weirdness / Plausibility: 5 / 1

### Zeno-frozen metastable decay
- Field and analogy: Quantum measurement theory. Short-time survival probability of an unstable state is quadratic in t (Zeno regime), so the effective decay rate starts at zero and grows ~linearly before settling to the exponential rate: Gamma(t) = Gamma0 * t/(t + t_Z).
- Cosmology story: Dark energy is a metastable vacuum whose decay rate is suppressed at early times (Zeno-frozen) and switches on only after t ~ t_Z, so rho_DE is nearly constant early and then decays. Time is proxied by t/t0 = (1+z)^(-3/2), the matter-era relation (a recasting, because t(z) would need an integral).
- Form: density f(z).
  ```python
  def make(B, G, sz):
      def P(s):
          return np.exp(-G * (s - sz * np.log1p(s / sz)))   # survival probability
      def f(z):
          s = (1 + np.asarray(z, dtype=float)) ** -1.5
          return (1 + B * P(s)) / (1 + B * P(1.0))
      return f
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | B  | 0.3 | 0.2 | -0.9 | 5.0 |
  | G  | 2.0 | 0.5 | 0.0 | 20.0 |
  | sz | 0.3 | 0.1 | 0.02 | 5.0 |

  LCDM limit: B=0 (or G=0).
- High-z behaviour (z up to 1100): s -> 0, P -> 1, f -> (1+B)/(1+B*P(1)). Finite, positive. No blow-up.
- Impact if true: DE is a decaying vacuum with a measurable Zeno time t_Z; its energy drains into matter/radiation, shifting the matter budget over cosmic time.
- Beyond-background fingerprint: Energy transfer from vacuum to dark matter, producing a late-time growth-rate offset and an altered ISW signal; also a finite lifetime for the vacuum (a prediction for the far future).
- Prior art: KNOWN (close). Query "arXiv quantum Zeno effect suppressed vacuum decay dark energy time-dependent decay rate". Szydlowski, Stachowski and Urbanowski, arXiv:1704.05364, "Quantum mechanical look at the radioactive-like decay of metastable dark energy" (opened and read: derives the time-dependent decay rate from Fock-Krylov theory of unstable states, with three phases of decay). The (1+z)^(-3/2) time proxy and the t/(t+t_Z) rate form are mine, but the idea is in the literature.
- Weirdness / Plausibility: 4 / 3

### Modular Eisenstein vacuum energy
- Field and analogy: Number theory / string theory. The weight-4 Eisenstein series E_4(tau) = 1 + 240 sum sigma_3(n) q^n (q = e^{2 pi i tau}) satisfies E_4(-1/tau) = tau^4 E_4(tau). So Y^2 E_4(iY) is invariant under Y -> 1/Y (T-duality-like), with a self-dual minimum at Y=1.
- Cosmology story: A torus modulus y slides with expansion as y = y0 (1+z)^(-kappa) and the dark-energy density is the duality-invariant function H(y) = Y^2 E_4(iY), Y = max(y, 1/y), plus a constant c. If the modulus passes through the self-dual point, rho_DE has a smooth minimum at that epoch. Honest: kinematic ansatz; a real model would solve the modulus equation.
- Form: density f(z).
  ```python
  def make(c, y0, kap):
      n = np.arange(1, 9)
      s3 = np.array([sum(d**3 for d in range(1, k + 1) if k % d == 0) for k in n], dtype=float)
      def H(y):
          Y = np.maximum(y, 1.0 / y)
          q = np.exp(-2 * np.pi * Y)
          return Y**2 * (1 + 240 * (s3 * q[..., None] ** n).sum(-1))
      def f(z):
          y = y0 * (1 + np.asarray(z, dtype=float)) ** (-kap)
          return (c + H(y)) / (c + H(np.asarray(y0, dtype=float)))
      return f
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | c   | 2.0  | 1.0  | 0.0  | 50 |
  | y0  | 1.2  | 0.2  | 0.3  | 5.0 |
  | kap | 0.05 | 0.03 | -0.3 | 0.3 |

  LCDM limit: kap=0.
- High-z behaviour (z up to 1100): y runs over y0*[1100^-kap, 1]; for |kap|<=0.3, Y <= ~ 8/y0, so H ~ Y^2 <= 200 at y0=0.5: f at most tens, positive (H>0 and c>=0). The DE density grows polynomially like (1+z)^(2 kap) at high z, which is harmless against matter (1+z)^3.
- Impact if true: Dark energy would be a duality-invariant function of a modulus, with a self-dual epoch where w crosses -1 smoothly with a symmetric "bounce"; this is the string-theory picture of a thawing/freezing minimum.
- Beyond-background fingerprint: Time-varying couplings tied to the modulus (alpha, proton-electron mass ratio) with the same y(z) path: a quasar/atomic-clock link between dark energy and varying constants.
- Prior art: NEAR-KNOWN. Query "arXiv modular invariant Eisenstein series Casimir energy modulus rolling dark energy self-dual radius". Anchordoqui et al. line "S-dual quintessence" and arXiv:2506.02731 "Bulk/boundary Modular Quintessence and DESI" (opened and read: modular-invariant quintessence potential, field rolling from a self-dual point, agrees with DESI). The specific E_4 Casimir form with a power-law modulus path is not there, but the modular-invariant-quintessence concept is KNOWN.
- Weirdness / Plausibility: 5 / 2

### BKT essential-singularity switch-on
- Field and analogy: Topological phase transitions (Berezinskii-Kosterlitz-Thouless). The BKT transition is of infinite order: the order parameter and all its derivatives vanish at T_c, and the correlation length diverges as exp(b/sqrt(T-T_c)), not as a power law.
- Cosmology story: A topological-defect sector (vortex unbinding) contributes extra vacuum energy only below a critical redshift z_c, switching on with all derivatives zero at z_c, as exp(-b/sqrt(x_c - x)). The transition is infinitely smooth yet sudden. Honest: a form borrowed from BKT scaling; the variable is e-fold time.
- Form: density f(z).
  ```python
  def make(A, xc, b):
      def s(x):
          d = np.maximum(xc - np.asarray(x, dtype=float), 0.0)
          return np.where(d > 0, np.exp(-b / np.sqrt(np.where(d > 0, d, 1.0))), 0.0)
      return lambda z: (1 + A * s(np.log1p(np.asarray(z, dtype=float)))) / (1 + A * s(0.0))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A  | 0.3 | 0.2 | -0.9 | 5.0 |
  | xc | 0.7 | 0.2 | 0.1  | 3.0 |
  | b  | 0.5 | 0.2 | 0.01 | 5.0 |

  LCDM limit: A=0.
- High-z behaviour (z up to 1100): for x >= x_c, s=0 and f = 1/(1+A*s(0)), a constant. Finite, positive. No blow-up.
- Impact if true: The late-time dark-energy rise is a topological ordering transition with a universal (essential) scaling law, not a smooth rolling field; sharp predictions for the shape of the onset.
- Beyond-background fingerprint: Topological-defect networks leave stochastic gravitational-wave or string-like lensing signatures; the onset has zero derivatives, so no abrupt feature in growth, only a delayed rise.
- Prior art: query "arXiv Berezinskii-Kosterlitz-Thouless essential singularity dark energy transition cosmology". None found (search returned only condensed-matter BKT papers, e.g. arXiv:cond-mat/0412512, none with cosmology).
- Weirdness / Plausibility: 4 / 2

### Kerr collapse-revival vacuum
- Field and analogy: Quantum optics / quantum foundations. A coherent state evolving under an anharmonic (Kerr) Hamiltonian has an autocorrelation that collapses to zero and then revives at t_rev = 2 pi / chi. Exact form for mean photon number n: C(t) = exp(n (cos(chi t) - 1)) cos(n sin(chi t)).
- Cosmology story: The dark-energy field sits in a macroscopic coherent state with a slightly anharmonic spectrum, so its expectation-value energy shows quantum collapse and then revival, with the e-fold time x = ln(1+z) as clock. Honest: a pure analogy; whether a Kerr-like nonlinearity exists in the dark sector is unknown.
- Form: density f(z).
  ```python
  def make(A, nbar, chi):
      def C(x):
          return np.exp(nbar * (np.cos(chi * x) - 1)) * np.cos(nbar * np.sin(chi * x))
      return lambda z: 1 + A * (C(np.log1p(np.asarray(z, dtype=float))) - 1)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A    | 0.1 | 0.1 | -0.45 | 0.45 |
  | nbar | 3.0 | 1.0 | 0.1 | 30 |
  | chi  | 1.0 | 0.3 | 0.05 | 8.0 |

  LCDM limit: A=0.
- High-z behaviour (z up to 1100): |C|<=1 always, so f in [1-2A, 1+2A], positive for A<0.5. The collapse-revival pattern repeats with period 2 pi/chi in ln(1+z) (for chi=1 the first full revival is near z of about 530, near recombination), so a high-z revival is built in.
- Impact if true: Dark energy would be a quantum object whose energy is non-monotonic in time with exact revivals; a smoking-gun log-periodic pattern with fractional revivals at t_rev/k.
- Beyond-background fingerprint: Fractional revivals imply a Schrodinger-cat superposition of vacuum states: a predicted decoherence signature in CMB-epoch H(z) at multiples of the revival e-fold.
- Prior art: query "arXiv quantum collapse and revival coherent state Kerr dark energy oscillating cosmological constant". None found for dark energy (collapse-revival papers are all quantum optics, e.g. arXiv:1211.2228; the nearest cosmology hit, arXiv:1611.03347 Baulieu "Early Universes with Effective Discrete Time", opened and read: about inflation and discrete time, not dark energy).
- Weirdness / Plausibility: 5 / 1

### Fibonacci-chain epoch staircase
- Field and analogy: Aperiodic order / quasicrystals. A Fibonacci chain places tile boundaries at x_n = ell (n + kappa floor(n/phi + theta)), i.e. two tile lengths ell and ell(1+kappa) ordered by the golden ratio (cut-and-project). Its Fourier spectrum is pure-point with dense incommensurate peaks (no periodic repeat).
- Cosmology story: Dark energy accumulates in small quasi-ordered steps at e-fold epochs forming a quasicrystal (like a sequence of bubble nucleations on a Fibonacci chain), giving a slow net drift with a never-repeating stair texture. Honest: a texture ansatz for the transient steps, not a mechanism.
- Form: density f(z).
  ```python
  def make(A, ell, kap):
      phi = (1 + 5 ** 0.5) / 2
      n = np.arange(1, 161)
      xn = ell * (n + kap * np.floor(n / phi + 0.5))
      def S(z):
          x = np.log1p(np.asarray(z, dtype=float))[..., None]
          return (0.5 * (1 + np.tanh((x - xn) / 0.03))).sum(-1)
      return lambda z: 1 + A * ell * (S(z) - S(0.0))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A   | 0.02 | 0.03 | -0.12 | 0.12 |
  | ell | 0.3  | 0.05 | 0.05  | 2.0 |
  | kap | 0.5  | 0.2  | 0.0   | 3.0 |

  LCDM limit: A=0.
- High-z behaviour (z up to 1100): total rise is about A*x/(1+0.62*kap) (<= 7*0.12 at x=7), so f >= ~0.16 for the largest allowed A, positive; with 160 steps all ell>=0.05 up to x=7 are covered. No blow-up. Each step is a tanh of width 0.03 in x, so w is finite.
- Impact if true: Dark energy changes in discrete, quasi-ordered steps; the data would see a staircase with a golden-ratio texture in epochs, which no continuous field model produces.
- Beyond-background fingerprint: Steps imply quasi-periodic features in the growth rate and in the BAO distance residuals with golden-ratio incommensurate spacing; also non-repeating pulses in a stochastic GW background.
- Prior art: query "arXiv quasicrystal Fibonacci quasiperiodic aperiodic order dark energy equation of state golden ratio". None found for a Fibonacci-chain step model in the dark-energy density. Nearest: Aschheim et al., arXiv:1611.04858, "Starobinsky Inflation and Dark Energy and Dark Matter Effects from Quasicrystal Like Spacetime Structures" (opened and read: modified-gravity exact solutions on hypothetical quasicrystal-like spacetime structure, not a history of rho_DE vs z).
- Weirdness / Plausibility: 4 / 1

### Page-curve cusp Lambda
- Field and analogy: Quantum information / black-hole and de Sitter horizons. The Page curve of radiation entanglement entropy rises linearly, then turns over at the Page time and falls (a cusp-like kink, smoothed here).
- Cosmology story: Dark energy tracks a "horizon-radiation entanglement" quantity that grows until a Page redshift and then decreases, so rho_DE has a maximum (or minimum, for A<0) near the Page epoch. Honest: the mapping from entropy to energy density is assumed.
- Form: density f(z).
  ```python
  def make(A, xp, dl):
      g = lambda x: xp - np.sqrt((x - xp) ** 2 + dl ** 2)
      return lambda z: 1 + A * (g(np.log1p(np.asarray(z, dtype=float))) - g(0.0))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A  | 0.05 | 0.05 | -0.15 | 0.15 |
  | xp | 0.5  | 0.2  | 0.05  | 3.0 |
  | dl | 0.1  | 0.05 | 0.01  | 1.0 |

  LCDM limit: A=0.
- High-z behaviour (z up to 1100): g decreases linearly in x beyond xp, so f(1100) = 1 + A*(2*xp - 7 + O(dl)), >= about 0.1 for A=0.15, xp=0.5. Finite, positive.
- Impact if true: A turnover in dark energy at the horizon's Page time, i.e. quantum-gravity information-theoretic input into the late-time expansion. Weaker than the other ideas: it is a simple kinked bump and could be mimicked by a transient-bump model already in the catalogue.
- Beyond-background fingerprint: The Page time is tied to horizon area, hence to the Hubble scale; this could imprint a coincidence between the DE turnover and a fixed Hubble-radius threshold (a "coincidence problem" angle).
- Prior art: query "arXiv Page curve de Sitter horizon entanglement entropy dark energy late-time acceleration". None found connecting a Page curve to rho_DE(z) (hits are de Sitter holography: Dong, Silverstein, Torroba arXiv:2103.07477; Espindola and Miyashita arXiv:2607.08737 "The mini-Page Curve in Cosmology", opened and read: Hawking pairs and information escape from a dS horizon, no dark-energy fit).
- Weirdness / Plausibility: 3 / 2

---

## needs ODE

1. **Mittag-Leffler memory relaxation, exact version.** Replace the rational approximation with the true Caputo-fractional relaxation of the field-energy rho_DE: D^a_C rho_DE(N) = -lam (rho_DE - rho_inf) with N = ln a, solution rho_DE = rho_inf + (rho_0 - rho_inf) E_a(-lam N^a). Needs the Mittag-Leffler series or a quadrature (no ODE solver strictly, but a special function).
2. **Zeno-frozen decay with exact t(z).** Replace the (1+z)^(-3/2) proxy by the cosmic time in the self-consistent background: t(z) = int_z^inf dz'/((1+z')H(z')), with H including the decaying DE, and dP/dt = -Gamma0 t/(t+t_Z) P with energy transfer to matter: d rho_m/dt + 3 H rho_m = +Gamma(t) rho_DE_decaying. Requires an ODE for rho_m and rho_DE jointly.
3. **Modular quintessence, dynamical modulus.** Solve the modulus equation y'' + 3H y' + dV/dy = 0 with V(y) = c + Y^2 E_4(iY) (Y = max(y,1/y)) instead of the kinematic power law; the self-dual point then acts as an attractor/minimum.
4. **Kerr collapse-revival, true time.** Use the cosmic-time clock t(z) rather than ln(1+z); in the quantum version the energy expectation of an anharmonic field mode in a squeezed state obeys the Heisenberg equations, a 2-3 variable ODE for <n>, <a^2>.
