# Batch 2 harvest: geoscience, fluid dynamics, plasma, materials/rheology, climate

Harvester: field cluster "geoscience / fluids / plasma / materials / climate". 11 ideas.
No fits and no chi-squared were computed. All forms are proposals for the scorer.

Conventions used below:
- "uses Om" models are factories `make(<params>, Om)` returning f(z) = rho_DE(z)/rho_DE(0) (density) or w(z).
  `np` is numpy. f(0) = 1 is built in by dividing by the value at z = 0.
- Several ideas need a cosmic CLOCK. Shared helper (LCDM age in units of 1/H0, radiation neglected; it is
  a proxy for the true age, the error is second order and it removes the need for an ODE):

```python
def _t(z, Om):
    OL = 1 - Om
    return 2/(3*np.sqrt(OL))*np.arcsinh(np.sqrt(OL/Om)*(1+np.asarray(z, float))**-1.5)
```
  (t(0) is about 0.96 for Om = 0.3. At z = 1100, t is about 3e-5, so any f built from t is finite there.)
- Several ideas use the LCDM expansion rate E(z) = sqrt(Om (1+z)^3 + 1 - Om) as a PROXY "driving frequency".
  This avoids the implicit equation H(f(H)) and is exact in the limit where the model reduces to LCDM.
- High-z remark that applies to every density model here: rho_DE / rho_matter is about 1e-9 at z = 1100, so a
  bounded f cannot hurt the CMB through its own energy; the only danger is f going negative or non-finite.

---

### Omori aftershock DE
- Field and analogy: Omori-Utsu law of earthquake aftershocks. After a mainshock at time t_e the event rate decays as n(t) = K/(c + t - t_e)^p, and the cumulative number of events N(t) is the integral of that.
- Cosmology story: a single early "mainshock" (a transition at cosmic time t_e) leaves a vacuum that keeps releasing energy as a power-law-decaying aftershock sequence; the dark-energy density is Lambda plus the cumulative release. It is an analogy; the novelty is the heavy-tailed, non-exponential approach and a free p (p < 1 grows as a power, p = 1 as a log, p > 1 saturates).
- Form: density f(z), uses Om. Cumulative Omori count, with q = 1 - p (q = 0 is the logarithmic p = 1 case):
```python
def omori(A, te, c, q, Om):
    t0 = _t(0.0, Om)
    def N(t):
        x = np.maximum(t - te, 0.0); L = np.log1p(x/c); small = abs(q) < 1e-9
        return np.where(small, L, np.expm1(q*L)/(1.0 if small else q))
    return lambda z: (1 + A*N(_t(z, Om)))/(1 + A*N(t0))
```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A  | 0.3 | 0.3  | -0.05 | 5.0 |
  | te | 0.5 | 0.15 | 0.05  | 0.9 |
  | c  | 0.2 | 0.1  | 0.02  | 2.0 |
  | q  | 0.0 | 0.3  | -1.5  | 0.9 |

  LCDM limit: A = 0 (also te above the age of the universe).
- High-z behaviour (z up to 1100): for t < t_e, N = 0, so f = 1/(1 + A N(t0)), a constant. Finite and positive (A lower bound keeps 1 + A N > 0 given N(t0) <= about 18).
- Impact if true: dark energy would be the tail of ONE dated event (z_e is a measurable "mainshock" redshift), not a slow field; the expansion history would carry a kink at z_e. That is a new class of model: an event plus a universal relaxation law.
- Beyond-background fingerprint: a kink (not a jump) in w at z_e, hence a sudden change in the growth-rate slope and ISW at z_e; bursts of structure formation timed to z_e.
- Prior art: query "Omori law aftershock decay dark energy cosmology arXiv". Found only Faraoni, arXiv:2005.03428, "Lagrangian formulation of Omori's law and analogy with the cosmic Big Rip" (abstract read): an analogy between the Omori equation and the Friedmann equation, not an Omori-type dark-energy density. Dark-energy use of Omori decay: none found.
- Weirdness 4 / Plausibility 2

### Cole-Cole dispersion with Hubble rate as frequency
- Field and analogy: dielectric relaxation in materials. The real part of the Cole-Cole susceptibility Re[1/(1 + (i x)^alpha)] is a smooth step in frequency whose width is set by alpha (alpha = 1 is a Debye step; alpha < 1 is a broad, "non-Debye" step typical of glasses and polymers).
- Cosmology story: the vacuum is a causal linear-response medium and the "drive frequency" is the expansion rate H. As H drops below a relaxation scale H_s, the medium's static response switches on, so rho_DE gains a step in H, not in z. An analogy; the new feature is a fractional-exponent width and, by Kramers-Kronig, a necessary loss peak.
- Form: density f(z), uses Om; x = E/xs with E the LCDM-proxy expansion rate in units of H0.
```python
def colecole(A, xs, al, Om):
    ca = np.cos(al*np.pi/2)
    def D(e):
        s = (e/xs)**al
        return (1 + s*ca)/(1 + 2*s*ca + s*s)
    E = lambda z: np.sqrt(Om*(1+np.asarray(z, float))**3 + 1 - Om)
    return lambda z: (1 + A*D(E(z)))/(1 + A*D(1.0))
```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A  | 0.3 | 0.3 | -0.9 | 5.0 |
  | xs | 2.0 | 1.0 | 0.5  | 8.0 |
  | al | 0.7 | 0.2 | 0.1  | 1.0 |

  LCDM limit: A = 0.
- High-z behaviour: D -> 0 as E grows, so f -> 1/(1 + A D(1)), a finite constant. D lies in [0, 1], so positivity holds for A > -1.
- Impact if true: dark energy would be a dissipative medium with a relaxation rate near today's H; the DE budget at late times is the "static" part of a response function and the "dynamic" part is hidden at high H. It would tie w(z) behaviour to a causal loss mechanism.
- Beyond-background fingerprint: Kramers-Kronig requires an imaginary (loss) part peaking at H = H_s: damping of dark-energy perturbations and a dark-energy anisotropic-stress-like term at that epoch; scale-dependent dark-energy clustering because fast perturbation modes see the "high-frequency" response.
- Prior art: query "Cole-Cole Havriliak-Negami dielectric relaxation dark energy Hubble rate cosmology arXiv". None found: results were all dielectric physics (e.g. arXiv:2410.05219, 1611.06433), none with dark energy or H as frequency.
- Weirdness 5 / Plausibility 2

### Lorentz-resonance DE (Hubble sweeps through a natural frequency)
- Field and analogy: driven damped oscillator, as in ocean-tide resonance or Lorentz-oscillator optics. The in-phase response Re chi = (1 - x^2)/((1 - x^2)^2 + (x/Q)^2) rises, crosses zero at resonance and turns negative (anomalous dispersion).
- Cosmology story: the dark sector contains a bound mode of natural rate H_r (in units of H0) that is driven by the expansion; as H sweeps through H_r the DE density rises then dips, with the swing width set by a quality factor Q. Analogy; the point is that a resonance automatically gives a non-monotonic rho_DE and so a phantom crossing.
- Form: density f(z), uses Om; x = E/xr.
```python
def lorentz(A, xr, Q, Om):
    E = lambda z: np.sqrt(Om*(1+np.asarray(z, float))**3 + 1 - Om)
    chi = lambda e: (1 - (e/xr)**2)/((1 - (e/xr)**2)**2 + (e/(xr*Q))**2)
    return lambda z: (1 + A*chi(E(z)))/(1 + A*chi(1.0))
```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A  | 0.1 | 0.1 | -0.3 | 0.3 |
  | xr | 1.5 | 0.3 | 1.0  | 3.0 |
  | Q  | 2.0 | 1.0 | 0.3  | 4.0 |

  LCDM limit: A = 0. Resonance redshift: (xr^2 - 1 + Om)/Om = (1 + z_r)^3.
- High-z behaviour: chi -> -1/x^2 -> 0, so f -> 1/(1 + A chi(1)), finite. Positivity: |chi| <= about Q/2 near resonance, so 1 + A chi >= 0.4 with the stated bounds.
- Impact if true: the dark sector would have a characteristic frequency of order H0, i.e. a mass m of about 1e-33 eV, and DESI's phantom-crossing hint would be the resonance dip rather than a thawing field. That fixes a new scale of nature.
- Beyond-background fingerprint: a damped quasi-oscillation of the dark-energy sound speed and growth suppression within a narrow redshift window around z_r; a narrow feature in the ISW cross-correlation.
- Prior art: query "Lorentz oscillator resonance dark energy density Hubble rate resonance arXiv". None found for a Lorentz-susceptibility form in H. Related but different (abstracts seen in search): arXiv:1908.06995 (oscillating scalar fields, Hubble tension), arXiv:1703.00543 (parametric resonance in vacuum fluctuations).
- Weirdness 5 / Plausibility 2

### Andrade creep of space
- Field and analogy: Andrade creep in mantle rocks and ice. Strain under constant stress goes as eps(t) = eps0 [1 + beta t^n + t/tau_M], with a transient t^n term (n about 1/3 in Andrade's original fits) plus the steady viscous flow term.
- Cosmology story: treat the dark-energy density as the "strain" of the vacuum under the constant stress of expansion, so rho_DE creeps as 1 + A(t^n + gam t) in cosmic time, with the transient exponent as a universal number. Analogy; plain Maxwell and bulk viscosity are the n = 1 case and are already known.
- Form: density f(z), uses Om.
```python
def andrade(A, n, gam, Om):
    g = lambda t: t**n + gam*t
    t0 = _t(0.0, Om)
    return lambda z: (1 + A*g(_t(z, Om)))/(1 + A*g(t0))
```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A   | 0.3   | 0.3  | -0.3 | 3.0 |
  | n   | 0.333 | 0.15 | 0.05 | 1.5 |
  | gam | 0.2   | 0.2  | 0.0  | 1.0 |

  LCDM limit: A = 0.
- High-z behaviour: t -> 0, g -> 0, f -> 1/(1 + A g(t0)), finite and positive (bounds keep g(t0) <= 2, so 1 + A g > 0.4).
- Impact if true: a fitted n near 1/3 would be striking, since it is the rock-mechanics value; it would say the vacuum has a rheology with a transient creep exponent and that dark energy is a transient-plus-viscous process in cosmic time rather than in a field. Even n different from 1/3 gives a clock-based (not a-based) evolution law, a new class.
- Beyond-background fingerprint: Andrade creep has frequency-dependent dissipation Q^-1 proportional to omega^-n, so a speculative prediction is power-law frequency-dependent damping of tensor modes (GW distance versus EM distance), tiny at LIGO frequencies and not at nHz.
- Prior art: query "Andrade creep viscoelastic cosmic fluid dark energy arXiv". None found for Andrade creep. Related (abstracts read): Brevik, arXiv:1510.02280 (cosmic fluid as a Maxwell fluid, turbulent transition), Rousseaux and Mancas, arXiv:2002.12123 (visco-elastic cosmology, bubble-dynamics analogy).
- Weirdness 4 / Plausibility 2

### Stick-slip sawtooth DE (Poisson-kernel relaxation oscillator)
- Field and analogy: stick-slip earthquake cycles and glacial cycles (slow loading, fast release; Milankovitch-paced ice ages are sawtooth, not sinusoidal). The smooth sawtooth S(psi) = arctan(s sin psi/(1 - s cos psi)) = sum s^n sin(n psi)/n is closed form: s = 0 is a sine, |s| -> 1 a sawtooth.
- Cosmology story: dark energy loads up slowly and releases fast, periodically in ln(1+z) (equal e-fold spacing, as a scale-invariant clock). An analogy; the novelty over symmetric "oscillating dark energy" is the asymmetry, which makes w spend long stretches near -1 and crash quickly.
- Form: density f(z), no Om.
```python
def stickslip(A, om, ph, s):
    S = lambda psi: np.arctan2(s*np.sin(psi), 1 - s*np.cos(psi))
    psi = lambda z: om*np.log1p(np.asarray(z, float)) + ph
    return lambda z: (1 + A*S(psi(z)))/(1 + A*S(psi(0.0)))
```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A  | 0.2 | 0.2 | -0.4  | 0.4 |
  | om | 4.0 | 1.5 | 0.5   | 12.0 |
  | ph | 0.0 | 1.0 | -3.14 | 3.14 |
  | s  | 0.5 | 0.3 | -0.85 | 0.85 |

  LCDM limit: A = 0.
- High-z behaviour: |S| <= pi/2, so 1 + A S >= 0.37 and f is bounded for all z; at most om*ln(1101)/(2 pi) = 13 cycles by z = 1100. s capped at 0.85 so the maximum slope (about s/(1-s)) keeps |w + 1| inside the scorer's pathology threshold at moderate A.
- Impact if true: dark energy would be a relaxation oscillator with episodic "slips", so today's value is one phase of a cycle and the DESI-era "evolution" is a segment of a repeating pattern; future and past events are predicted by (om, ph).
- Beyond-background fingerprint: periodic comb of growth-rate steps equally spaced in ln(1+z); each slip is an energy release, so possible stochastic GW or heating signals at the slip redshifts.
- Prior art: query "sawtooth relaxation oscillation dark energy density asymmetric oscillating arXiv". PARTIAL. Symmetric oscillating dark energy is KNOWN: Linder, astro-ph/0511415 "On Oscillating Dark Energy" and Kurek et al., arXiv:0707.0292 "Constraints on oscillating dark energy models" (abstracts read). The asymmetric relaxation-oscillator (sawtooth) waveform with an asymmetry parameter: none found. Marked as not KNOWN, with the symmetric limit s = 0 being known.
- Weirdness 4 / Plausibility 2

### Burgers N-wave dipole in w(z)
- Field and analogy: the decaying N-wave of the viscous Burgers equation (Cole-Hopf solution): u(x, t) = (x/t)/(1 + sqrt(t/t0) exp(x^2/4 nu t)), a linear ramp through zero ending in two shocks, whose sign flips at the centre.
- Cosmology story: the departure of the equation of state from -1 is an N-wave in redshift, so w + 1 is odd about z_c and crosses -1 exactly once at z_c; the ramp slope A, the shock-edge sharpness B and the width sigma come from the Burgers structure. An analogy, chosen because the shape has a built-in sign change with no extra tuning.
- Form: w(z), no Om.
```python
def nwave(A, zc, sig, B):
    def w(z):
        xi = np.asarray(z, float) - zc
        g = np.exp(-(xi/sig)**2)
        return -1 + A*xi*g/(g + B)
    return w
```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A   | -0.3 | 0.3 | -1.5 | 1.5 |
  | zc  | 0.5  | 0.2 | 0.05 | 2.0 |
  | sig | 0.5  | 0.2 | 0.1  | 2.0 |
  | B   | 1.0  | 0.5 | 0.05 | 20.0 |

  LCDM limit: A = 0. (DESI-like sign: w < -1 at z > z_c and w > -1 at z < z_c is A < 0.)
- High-z behaviour: g -> 0 so w -> -1 faster than any power; the integral of (1 + w) over ln(1+z) converges, so rho_DE tends to a constant at z = 1100. Written with g (not exp(+xi^2)) to avoid overflow.
- Impact if true: the phantom crossing is exact and unique, a single "event" in w with an odd shape rather than a monotone CPL line; dark energy would be a transient with zero net effect on the high-z universe. It would favour hydrodynamic-shock-like (non-field) explanations.
- Beyond-background fingerprint: at z_c the perturbation equations for a single-fluid DE are singular (crossing -1), so a fluid with this shape needs non-adiabatic pressure; testable as a localised bump in the ISW and fsigma8 residuals around z_c.
- Prior art: query "Burgers equation N-wave dark energy equation of state w(z) arXiv". None found: results are generic w(z) parametrisations (Barboza et al., arXiv:0905.4052) and Burgers in dark matter (BEC, arXiv:1103.3219); no N-wave in w.
- Weirdness 4 / Plausibility 2

### Comoving-horizon Kolmogorov cascade DE
- Field and analogy: a turbulent inertial range with spectrum E(k) proportional to k^-(1+q'), so the energy above a wavenumber k_min is proportional to k_min^-q (Kolmogorov: spectrum k^-5/3, q = 2/3).
- Cosmology story: the energy density in a cascade of modes is set by the largest scale that has entered the causal "box", the comoving Hubble wavenumber k_H = aH; hence rho_DE = Lambda-part + a power of aH. Because aH has a minimum at the onset of acceleration, the DE density necessarily has an extremum there. An analogy, and the cascade exponent is simply a fit parameter.
- Form: density f(z), uses Om (LCDM-proxy aH in units of H0):
```python
def cascade(B, q, Om):
    kH = lambda z: np.sqrt(Om*(1+np.asarray(z, float))**3 + 1 - Om)/(1 + np.asarray(z, float))
    return lambda z: (B + kH(z)**(-q))/(B + 1.0)
```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | B | 1.0   | 1.0 | 0.0  | 20.0 |
  | q | 0.667 | 0.3 | -1.0 | 4.0 |

  LCDM limit: q = 0.
- High-z behaviour: kH grows as (1+z)^0.5, so the cascade term tends to 0 for q > 0 (f -> B/(1+B), finite) and grows at most as 33^|q| at z = 1100 for q >= -1 (still a ~1e-9-level fraction of matter). Positive for B >= 0.
- Impact if true: dark energy would not be a free function but follows the comoving Hubble scale, a one-parameter-shape model with a sharp prediction: the DE density peaks (q > 0) at the deceleration-acceleration turnaround, z of about 0.6 to 0.7. It would link dark energy to horizon-scale causal physics (like holographic models but with a different scale).
- Beyond-background fingerprint: since the energy lives at horizon-scale modes, it clusters only at k about aH, giving a scale-dependent DE perturbation and a low-ell feature in ISW; a Kolmogorov-like q = 2/3 would be a specific number.
- Prior art: query "dark energy density as power of comoving Hubble radius aH turbulence cascade Kolmogorov spectrum horizon modes arXiv". None found for the aH form. Related but different (abstract read): Brevik, Gorbunova, Nojiri, Odintsov, arXiv:1011.6255, "On Isotropic Turbulence in the Dark Fluid Universe" (decaying turbulence added to a phantom/quintessence fluid, effect fades at late times, not tied to aH).
- Weirdness 4 / Plausibility 2

### Granular-compaction DE (inverse-log aging)
- Field and analogy: tapped granular media densify as rho(t) = rho_inf - Delta/(1 + B ln(1 + t/tau)) (Knight et al.; Peng and Ohta, cond-mat/9707237), an inverse-logarithmic law from glassy "free-volume" dynamics.
- Cosmology story: the vacuum is a glassy medium that "compacts" (or "dilates", sign of D) logarithmically in cosmic time, so rho_DE ages slower than any power law; it is quiet for most of history, then drifts. An analogy.
- Form: density f(z), uses Om.
```python
def compaction(D, B, tau, Om):
    g = lambda t: 1 - D/(1 + B*np.log1p(t/tau))
    t0 = _t(0.0, Om)
    return lambda z: g(_t(z, Om))/g(t0)
```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | D   | 0.2 | 0.2 | -3.0  | 0.95 |
  | B   | 1.0 | 1.0 | 0.1   | 10.0 |
  | tau | 0.1 | 0.1 | 0.005 | 1.0  |

  LCDM limit: D = 0.
- High-z behaviour: t -> 0 gives g -> 1 - D, so f -> (1 - D)/g(t0), finite and positive for D < 1 (D <= 0 gives g >= 1). D > 0 means rho_DE grows with time (phantom-like), D < 0 decays.
- Impact if true: dark energy has glass-like aging with memory; the future expansion is predictable (log-slow drift toward a plateau, w tends to -1 like 1/ln t). It would put the vacuum in the universality class of aging systems and invite a Kovacs-effect test.
- Beyond-background fingerprint: history dependence: a tapping-like perturbation (a late-time event) would be "remembered", so a measured w(z) would show hysteresis-type response after structure-formation events; w slowly drifts toward -1 in the future (long-term forecast).
- Prior art: query "logarithmic compaction granular matter analogy dark energy relaxation inverse logarithm arXiv". None found: the results (cond-mat/9707237, cond-mat/9705195, cond-mat/0003455, ...) are condensed-matter only (abstract of 9707237 read).
- Weirdness 4 / Plausibility 1

### Adler ghost-bottleneck DE (saddle-node phase slip)
- Field and analogy: climate tipping points and Josephson-junction/Adler dynamics. Phase obeys theta_dot = omega (1 - r sin theta); for r < 1 it rotates with a long dwell at the "ghost" of a saddle-node (a bottleneck) and then a fast phase slip. This has an exact solution: tan(theta/2) = r + sqrt(1 - r^2) tan( omega sqrt(1 - r^2) (t - t_c)/2 ).
- Cosmology story: the dark-energy density is 1 + A cos theta(t) in cosmic time; for r close to 1 it sits almost exactly at Lambda for a long stretch (the ghost), then changes quickly, like a delayed tipping point, while r = 0 is a plain harmonic oscillation in cosmic time. Analogy, and the point is "Lambda-like plateau followed by a late kick" from one smooth ODE solution.
- Form: density f(z), uses Om. cos theta = (1 - u^2)/(1 + u^2) with u = tan(theta/2), which is finite even at the poles of the tangent.
```python
def adler(A, wr, r, tc, Om):
    s = np.sqrt(1 - r*r)
    def cth(t):
        u = r + s*np.tan(0.5*wr*s*(t - tc))
        return (1 - u*u)/(1 + u*u)
    t0 = _t(0.0, Om)
    return lambda z: (1 + A*cth(_t(z, Om)))/(1 + A*cth(t0))
```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A  | 0.2 | 0.2 | -0.5 | 0.5 |
  | wr | 3.0 | 1.5 | 0.5  | 12.0 |
  | r  | 0.8 | 0.2 | 0.0  | 0.98 |
  | tc | 0.5 | 0.4 | -1.0 | 2.0 |

  LCDM limit: A = 0.
- High-z behaviour: |cos theta| <= 1, so 1 + A cos theta >= 0.5; f bounded for all z. In the time range t in (0, 0.96) there are at most about two slips (wr up to 12).
- Impact if true: dark energy would be near-Lambda for most history with a single late phase slip (explains "Lambda fits well but a recent drift is hinted"); the same equation predicts the NEXT slip date, so the model is forecastable. It would make cosmic acceleration a tipping-point phenomenon.
- Beyond-background fingerprint: critical slowing down before the slip: dark-energy perturbations (sound speed and damping) show early-warning behaviour near the bottleneck; events are periodic in cosmic TIME (not ln a), so earlier slips are squeezed to high z (z > 3, within reach of Lyman-alpha BAO).
- Prior art: query "saddle-node ghost bottleneck slow passage dark energy scalar field Adler equation phase slip cosmology arXiv". None found for the Adler/phase-slip form. Related (abstract read): Cotsakis, arXiv:2502.20430, "Cosmic acceleration as a saddle-node bifurcation: background identities and structure" (acceleration as a saddle-node of the Friedmann flow, not a ghost-bottleneck density history).
- Weirdness 5 / Plausibility 2

### Percolation-onset DE
- Field and analogy: near a percolation threshold the strength of the connected cluster or the conductivity scales as (p - p_c)^mu, with universal exponents (3D: conductivity exponent about 2.0, cluster-strength exponent about 0.41).
- Cosmology story: dark energy "switches on" when collapsed structures percolate (a threshold in scale factor a_c), with a critical power-law onset (a - a_c)^mu. It is an analogy; the novelty is a non-analytic onset with a free universal exponent, not an exponential or tanh step.
- Form: density f(z), no Om.
```python
def percolation(A, ac, mu):
    g = lambda a: np.maximum(a - ac, 0.0)**mu
    return lambda z: (1 + A*g(1/(1 + np.asarray(z, float))))/(1 + A*g(1.0))
```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A  | 1.0 | 1.0  | -1.0 | 20.0 |
  | ac | 0.6 | 0.15 | 0.3  | 0.95 |
  | mu | 1.0 | 0.5  | 0.5  | 2.5  |

  LCDM limit: A = 0.
- High-z behaviour: for a < a_c, f = 1/(1 + A (1 - a_c)^mu), a constant; finite and positive for A >= -1. (mu >= 0.5 keeps the slope at a_c finite on the scorer's grid.)
- Impact if true: acceleration arises as a critical phenomenon with a universal exponent; a fitted mu near 0.41 or 2.0 would point to a percolation universality class and to the cosmic web as the order parameter.
- Beyond-background fingerprint: a kink (non-analytic point) in w at a_c, and a link to measurable cosmic-web connectivity statistics (the percolation threshold of galaxy or halo catalogues should coincide with z_c).
- Prior art: query "percolation threshold critical exponent emergence of dark energy late universe arXiv". None found for the DE mechanism. Related (abstract of 1903.07626 read): arXiv:1903.07626 (graph statistics of the cosmic web, degenerate across dark-energy states) and arXiv:2407.02574 (percolation statistics in MillenniumTNG), both structure-only.
- Weirdness 3 / Plausibility 2

### JMAK / Stefan-front vacuum conversion
- Field and analogy: Johnson-Mehl-Avrami-Kolmogorov kinetics of a phase transformation, X(t) = 1 - exp(-(t/tau)^n); n = 3/2 for diffusion-controlled growth from pre-existing nuclei (Stefan-type sqrt(t) front, volume proportional to t^(3/2)), n = 5/2 with continuous nucleation.
- Cosmology story: dark energy is the fraction X of space converted to a new vacuum phase, with the Avrami exponent carrying the growth mechanism. Analogy; honest caveat is that the transformed-fraction formula is already used for cosmological first-order transitions, the added piece is fitting n and using the cosmic clock.
- Form: density f(z), uses Om.
```python
def jmak(B, tau, n, Om):
    X = lambda t: 1 - np.exp(-(t/tau)**n)
    t0 = _t(0.0, Om)
    return lambda z: (1 + B*X(_t(z, Om)))/(1 + B*X(t0))
```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | B   | 0.3 | 0.3 | -0.9 | 5.0 |
  | tau | 0.8 | 0.3 | 0.05 | 5.0 |
  | n   | 1.5 | 0.5 | 0.5  | 4.0 |

  LCDM limit: B = 0.
- High-z behaviour: X -> 0 as t -> 0, f -> 1/(1 + B X(t0)), finite and positive for B > -1.
- Impact if true: a late first-order vacuum transition that percolates now; n would discriminate growth mechanisms. Overlaps with known late-time vacuum transition models, so the impact is modest unless n is far from the tanh-like shapes already scored.
- Beyond-background fingerprint: bubble-wall collisions produce nHz-band gravitational waves and CMB spectral or anisotropy signals (the late-transition bounds in arXiv:2509.07076).
- Prior art: query "Avrami JMAK kinetics late-time vacuum phase transition dark energy bubble nucleation fraction arXiv". KNOWN (partly): late-time vacuum transitions with JMAK-type false-vacuum fraction appear in the literature, e.g. arXiv:2305.02357 (review of cosmological phase transitions; abstract read, it covers transition rates and bubble dynamics) and arXiv:2605.30259 "Late-time Quantum Vacuum Decay and its Cosmological Implications" (abstract read, fits a recent vacuum transition to distance and CMB data). A fit with free Avrami exponent on the cosmic clock as a DE density: none found.
- Weirdness 3 / Plausibility 2

---

## Needs ODE (or special function / memory integral)

1. Fractional-memory (Riemann-Liouville / Scott-Blair springpot) dark energy. Rheology: stress follows a fractional derivative of strain. Cosmic version: rho_DE(t) = rho_L + kappa * I^alpha[H^2](t), with the fractional integral I^alpha[g](t) = (1/Gamma(alpha)) * integral_0^t (t - s)^(alpha - 1) g(s) ds, coupled to 3H^2 = rho_m + rho_DE. Needs a convolution integral at each step. alpha = 1 gives running-vacuum-like behaviour; alpha < 1 is a heavy-tailed memory of the expansion history. LCDM: kappa = 0.
2. Mittag-Leffler (fractional Maxwell) relaxation: rho_DE(t) = rho_L + A * E_alpha(-(t/tau)^alpha), with E_alpha the Mittag-Leffler function (not in numpy; needs a series or integral representation). Power-law tail instead of exponential decay; generalises Omori (p about 1) to a function derived from a fractional ODE. LCDM: A = 0.
3. Herschel-Bulkley (yield-stress) bulk pressure: P = -rho_L - zeta * (3H)^n with continuity d rho/dt + 3H (rho + P) = 0 and 3H^2 = rho_m + rho; below a yield rate the fluid behaves as a rigid Lambda, above it flows with power-law index n. Implicit in H, so an ODE in ln a for rho(a). LCDM: zeta = 0. (Related known family: inhomogeneous equation of state p = w rho + f(H), Nojiri-Odintsov; not verified here.)
4. Rate-and-state (Dieterich-Ruina) friction as a field: slip variable V and state theta with theta_dot = 1 - V theta/D_c and mu = mu_0 + a ln(V/V_0) + b ln(V_0 theta/D_c); coupling to expansion as a stick-slip cycle with an actual slow-loading rate. Gives genuine stick-slip event statistics instead of the Poisson-kernel sawtooth above.
5. Plasma bump-on-tail saturation with trapping oscillations: E_dot = gamma E (1 - E/E_s) with a bounce-frequency overshoot, omega_b proportional to sqrt(E); the DE follows the saturated amplitude plus ringing. Needs an ODE for the amplitude and phase.
