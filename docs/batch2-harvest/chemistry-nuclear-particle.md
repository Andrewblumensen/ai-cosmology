# Batch 2 harvest: chemistry, kinetics, atomic, nuclear and particle mechanisms

Field cluster: reaction kinetics, atomic/nuclear/particle mechanisms used outside their usual role.
Conventions: `z` is a numpy array or scalar; `a = 1/(1+z)`. "Matter-era clock" means cosmic time is replaced
by the proxy `t/t0 = a**1.5` (exact for matter domination, an approximation here; it is part of the model
definition, not a derivation). All forms below are density models f(z) = rho_DE(z)/rho_DE(0), f(0)=1, unless
stated. All expressions were checked only for finiteness and positivity over z in [0, 1100] at a few corner
parameter values (no fit, no chi-squared). Where a form needs `erf`, it uses `scipy.special.erf`.

Prior-art note: web searches were run (queries given per idea). Items marked KNOWN are known in concept.
Papers named were opened and their abstracts read; where an abstract did not give the equation, this is said.

---

### MSW level-crossing dark fluid
- Field and analogy: Mikheyev-Smirnov-Wolfenstein effect. Two states mix with an angle theta; a matter-dependent potential shifts the mixing angle, and at a resonance density the mixing is maximal, so the state populations switch (adiabatic level crossing).
- Cosmology story: a dark sector has a vacuum-like state and an inert state, mixed with angle theta; the "matter potential" is proportional to rho_m ~ (1+z)^3. The fraction in the inert state follows sin^2(theta_m), which sweeps through a resonance at redshift z_r, switching the Lambda-like part off at high z with a power-law tail (not a tanh). Honest analogy: no Lagrangian is given.
- Form: density f(z).
  ```python
  def msw(eps, s, zr):
      c = np.sqrt(1 - s**2)                       # s = sin 2theta, c = cos 2theta
      def p(z):                                   # sin^2(theta_m)
          d = c * ((1 + np.asarray(z, float)) / (1 + zr))**3
          return 0.5 * (1 - (c - d) / np.sqrt((c - d)**2 + s**2))
      return lambda z: (1 - eps * p(z)) / (1 - eps * p(0.0))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | eps | 0.3 | 0.2 | -2.0 | 0.95 |
  | s | 0.4 | 0.2 | 0.05 | 1.0 |
  | zr | 1.0 | 0.5 | 0.1 | 20.0 |

  LCDM limit: eps=0.
- High-z behaviour (z up to 1100): p -> 1 (d large), so f -> (1-eps)/(1-eps p(0)): finite, positive for eps<1. Approach to the plateau goes like d^-2, i.e. (1+z)^-6.
- Impact if true: the cosmological constant is only partly "on" today, and its effective size is set by a flavour-mixing phase, so "why now" becomes "where is the resonance"; the DE amplitude is tied to the matter density through a level-crossing condition.
- Beyond-background fingerprint: with a resonance in the DE-DM sector, growth rate and ISW would show a feature at z_r; mixing implies an energy transfer between sectors that changes the matter growth history.
- Prior art: query "arXiv Mikheyev-Smirnov-Wolfenstein resonance dark energy dark matter mixing level crossing cosmology expansion history". **KNOWN (concept)**: arXiv:2405.20478, "On the viability of the QCD axion - dark energy transition" (Muursepp; DE from non-adiabatic level crossing between axion-like fields); arXiv:astro-ph/0311131 "Cosmo MSW effect for mass varying neutrinos" (Hung and Pas). Neither gives a closed-form f(z) of this kind; the closed-form mixing-angle profile used as an expansion history appears new.
- Weirdness 4 / Plausibility 2

### Saha ionisation dark energy
- Field and analogy: Saha equilibrium x^2/(1-x) = S for ionisation, with S = (m T / 2 pi)^(3/2) n^-1 exp(-B/T). Here the number density n falls faster than the thermal phase space, so the ionised fraction behaves in an unusual direction.
- Cosmology story: a dark plasma where the vacuum-like energy lives in the "ionised" fraction x. With T ~ (1+z) and n ~ (1+z)^3, S = A a^(3/2) exp(-b a), which has a maximum at a = 3/(2b): ionisation rises, peaks and can fall again. Analogy only; recombination physics is borrowed, not derived.
- Form: density f(z).
  ```python
  def saha(eps, logA, b):
      def x(a):
          S = 10**logA * a**1.5 * np.exp(-b * a)
          return 2 * S / (S + np.sqrt(S * S + 4 * S))      # stable root of x^2/(1-x)=S
      return lambda z: 1 - eps + eps * x(1 / (1 + np.asarray(z, float))) / x(1.0)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | eps | 0.3 | 0.2 | 0.0 | 1.0 |
  | logA | 1.0 | 1.0 | -2.0 | 4.0 |
  | b | 2.0 | 1.0 | 0.1 | 6.0 |

  LCDM limit: eps=0. (eps restricted to >= 0 because eps<0 can make f negative when x peaked in the past.)
- High-z behaviour (z up to 1100): x ~ sqrt(S) ~ a^(3/4) -> 0, so f -> 1-eps, finite and positive. For b > 1.5 the peak of x is in the past and f is non-monotonic (can exceed 1 at intermediate z, bounded by a few).
- Impact if true: dark energy is an equilibrium thermodynamic quantity of a dark plasma, whose present value is set by atomic-physics-like constants (B/T0); it predicts a non-monotonic w(z) with a specific shape and no free "potential".
- Beyond-background fingerprint: any dark charge carriers imply dark-photon/plasma effects; a time-varying ionisation fraction changes the DE sound speed, visible in ISW-galaxy cross-correlations.
- Prior art: query "arXiv Saha equation dark sector ionization fraction dark energy density late-time cosmology". None found for dark energy. Related but different: Saha used for dark-atom dark matter recombination (e.g. arXiv:1209.5752 "The Cosmology of Atomic Dark Matter", appeared in the search, not opened).
- Weirdness 4 / Plausibility 2

### Eyring-Polanyi decaying vacuum
- Field and analogy: transition-state theory. A barrier-crossing rate Gamma = nu T exp(-E_a/T) (Eyring prefactor T, Arrhenius exponential), integrated over time as survival probability exp(-integral Gamma dt).
- Cosmology story: dark energy is a metastable state whose decay is thermally activated by a dark bath with T ~ (1+z). As the bath cools the rate freezes out, so most decay happened early and the DE density flattens to a constant today (a late-time freeze-out of decay, giving w -> -1 from above). Analogy; the decay product (dark radiation) is neglected.
- Form: density f(z). In the matter-era clock, integral Gamma dt ~ kappa sqrt(pi/E) erf(sqrt(E a)), exactly.
  ```python
  from scipy.special import erf
  def eyring(kappa, E):
      g = lambda a: np.sqrt(np.pi / E) * erf(np.sqrt(E * a))
      return lambda z: np.exp(kappa * (g(1.0) - g(1 / (1 + np.asarray(z, float)))))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | kappa | 0.1 | 0.1 | -0.5 | 3.0 |
  | E | 2.0 | 1.0 | 0.05 | 30.0 |

  LCDM limit: kappa=0 (kappa<0 is the "anti-decay"/phantom branch, allowed so data decide).
- High-z behaviour (z up to 1100): f -> exp(kappa g(1)) as a -> 0; g(1) <= ~2 in range, so at most exp(6): finite and positive. DE is negligible against matter at those z, so the CMB sees only the tiny absolute value.
- Impact if true: the vacuum energy is not eternal; it is a relic of thermally driven decay, so the data constrain a barrier height in units of the dark temperature; "w > -1 and approaching -1" becomes a decay-freeze-out signature.
- Beyond-background fingerprint: decay into dark radiation adds an N_eff-like component at early times; also a modified ISW from the decaying potential.
- Prior art: query "arXiv vacuum energy decay thermally activated Arrhenius rate dark energy decaying cosmological constant Lambda(t)". None found for a thermally activated (Eyring/Arrhenius) rate. Adjacent: arXiv:1202.0499 "A Model for Dark Energy decay" (Abdalla, Graef, Wang; non-perturbative DE decay into dark matter) and arXiv:2403.04970 "Constraints on Metastable Dark Energy Decaying into Dark Matter" (de Souza, Vicente, Graef; bubble-nucleation decay). Neither has a thermal activation rate.
- Weirdness 4 / Plausibility 2

### Hulthen-Sommerfeld resonance ladder
- Field and analogy: Sommerfeld enhancement of annihilation by a Yukawa force. In the Hulthen approximation the enhancement has a ladder of resonances in velocity (zero-energy bound states), with a 1/v rise between them.
- Cosmology story: the energy transfer into/out of the DE sector scales with the Sommerfeld factor S(v) of a dark force, where the dark matter velocity dispersion redshifts as v = v0 (1+z) (free-streaming, decoupled). The DE density follows S, so it carries a ladder of narrow spikes in z when the resonance ladder is crossed. Phenomenological: S_eff = 1 + S_Hulthen to keep the large-v limit finite.
- Form: density f(z).
  ```python
  def somm(eps, ev0, ep):          # ev0 = v0/alpha today, ep = m_phi/(alpha m_chi)
      c6 = np.pi**2 * ep / 6
      def S(z):
          ev = np.minimum(ev0 * (1 + np.asarray(z, float)), 40 * c6)   # cap avoids overflow
          X = 2 * np.pi * ev / c6
          Y = 2 * np.pi * np.sqrt(np.asarray(1 / c6 - (ev / c6)**2, dtype=complex))
          e = np.exp(-X)
          return np.pi / ev * (1 - e * e) / (1 + e * e - 2 * e * np.real(np.cos(Y)))
      return lambda z: (1 + eps * S(z)) / (1 + eps * S(0.0))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | eps | 0.1 | 0.1 | 0.0 | 3.0 |
  | ev0 | 0.02 | 0.02 | 0.001 | 0.5 |
  | ep | 0.05 | 0.03 | 0.005 | 0.5 |

  LCDM limit: eps=0.
- High-z behaviour (z up to 1100): the cap makes ev constant at the largest z and S ~ pi/ev small, so f -> 1/(1 + eps S(0)): finite, positive. Corner values checked finite.
- Impact if true: dark energy tied to a dark-sector force with a resonant bound-state structure; a spike in H(z) at a calculable redshift would be a direct fingerprint of a dark Yukawa interaction. Low plausibility but unmistakable if seen.
- Beyond-background fingerprint: the same dark force gives velocity-dependent DM self-interaction (core sizes in dwarf galaxies) and a feature in growth at the resonance redshift.
- Prior art: query "arXiv Sommerfeld enhancement resonance interaction dark energy dark matter velocity dependent coupling cosmology". None found for dark energy. Sommerfeld enhancement is established for DM annihilation (e.g. arXiv:1008.1511 "Sommerfeld Enhancement of DM Annihilation: Resonance Structure, Freeze-Out and CMB Spectral Bound", listed in the search, not opened).
- Weirdness 5 / Plausibility 1

### Landau critical-exponent condensate
- Field and analogy: a second-order phase transition. The order parameter vanishes above T_c and grows as (1 - T/T_c)^beta below it, with beta = 1/2 (mean field / BCS), 0.326 (3D Ising), 0.125 (2D Ising). The condensation energy goes as the order parameter squared.
- Cosmology story: a dark sector with bath temperature T ~ (1+z) condenses at z_c (T = T_c). The DE density gets an extra term that switches on with a power-law kink at z_c and grows toward z=0. The critical exponent is a free parameter, so the data measure the universality class. Analogy; no microscopic model.
- Form: density f(z).
  ```python
  lambda eps, zc, beta: (lambda z:
      (1 + eps * np.clip(1 - (1 + np.asarray(z, float)) / (1 + zc), 0, None) ** (2 * beta))
      / (1 + eps * (zc / (1 + zc)) ** (2 * beta)))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | eps | 0.3 | 0.3 | -0.9 | 5.0 |
  | zc | 1.0 | 0.5 | 0.05 | 3.0 |
  | beta | 0.5 | 0.15 | 0.5 | 2.0 |

  LCDM limit: eps=0. (beta < 0.5 would give an integrable pole in w at z_c, so the lower bound is kept at the mean-field value.)
- High-z behaviour (z up to 1100): for z > z_c the extra term is exactly zero, so f = 1/(1 + eps (zc/(1+zc))^(2 beta)) constant: finite and positive for eps > -1.
- Impact if true: dark energy is a condensate with a measurable critical temperature and exponent; the kink at z_c is a sharp prediction (a jump in dw/dz) that distinguishes it from every smooth parametrisation.
- Beyond-background fingerprint: a second-order transition has a diverging susceptibility, so a spike in DE perturbations (sound speed) near z_c; also a latent-heat-free step in ISW.
- Prior art: query "arXiv dark energy second-order phase transition critical exponent order parameter late-time superconducting BCS dark sector". None found for a free critical exponent. Adjacent: arXiv:2511.19802 "Cold Dark Matter and Dark Energy Based on an Analogy with Superconductivity" (Liang; BCS-like condensate as dark matter, second-order transition, frustrated case gives a residual component); it does not use a critical exponent as an expansion-history parameter.
- Weirdness 4 / Plausibility 2

### Avrami-KWW vacuum conversion
- Field and analogy: JMAK/Avrami kinetics of phase transformations (transformed fraction 1 - exp(-(t/tau)^n), with n = 4 for constant-rate 3D nucleation and growth) and the same stretched exponential (n < 1) as the Kohlrausch relaxation of glasses, where it encodes a broad distribution of relaxation times.
- Cosmology story: the DE density is the remaining untransformed fraction of a false vacuum relaxing toward a lower true-vacuum value: rho = rho_true + (rho_false - rho_true) exp(-(t/tau)^n). One exponent n spans bubble percolation (n > 1), simple decay (n = 1) and a glassy broad-spectrum relaxation (n < 1). Analogy.
- Form: density f(z), matter-era clock t = a^1.5.
  ```python
  lambda eps, tau, n: (lambda z:
      (1 - eps + eps * np.exp(-((1 / (1 + np.asarray(z, float)))**1.5 / tau)**n))
      / (1 - eps + eps * np.exp(-(1 / tau)**n)))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | eps | 0.2 | 0.2 | -1.0 | 1.0 |
  | tau | 1.0 | 0.5 | 0.1 | 5.0 |
  | n | 1.0 | 0.5 | 0.3 | 4.0 |

  LCDM limit: eps=0.
- High-z behaviour (z up to 1100): t -> 0, the exponential -> 1, f -> 1/(1 - eps + eps exp(-tau^-n)): finite; positive for eps <= 1 (eps < 0 gives 1 + |eps|(1-S) >= 1).
- Impact if true: the data measure the kinetic exponent of the vacuum transition, i.e. whether DE decays like nucleation-and-growth (n>1), like a single rate (n=1) or like a glass (n<1): a statement about the dynamics of the vacuum, not only its density.
- Beyond-background fingerprint: bubble percolation (n>1) leaves patchy DE and superhorizon fluctuations in the transition time; glassy relaxation (n<1) implies slow, non-exponential late-time decay and scale-dependent DE perturbations.
- Prior art: query "arXiv stretched exponential Kohlrausch relaxation dark energy density Avrami vacuum decay late-time". None found for Avrami/KWW dark energy. Adjacent (late bubble-nucleation DE): arXiv:2403.04970 (de Souza, Vicente, Graef, metastable DE via first-order transition). The stretched-exponential cosmology papers returned (arXiv:1201.2948, arXiv:1606.06331) use it for the scale factor, not the DE density (not opened).
- Weirdness 3 / Plausibility 2

### Michaelis-Menten matter-to-vacuum conversion (KNOWN concept)
- Field and analogy: enzyme kinetics. A conversion rate V S/(Km + S) saturates (zero order) when the substrate is abundant and becomes first order when it is scarce.
- Cosmology story: matter is converted into vacuum-like energy at a saturable rate Q = V rho_m/(Km + rho_m), neglecting back-reaction on rho_m (valid for small conversion). In a matter-era clock the integral is exactly an arctan, so the DE gain is early-linear in time and then saturates as substrate dilutes. Analogy.
- Form: density f(z).
  ```python
  lambda eps, kappa: (lambda z:
      1 - eps + eps * np.arctan(kappa * (1 / (1 + np.asarray(z, float)))**1.5) / np.arctan(kappa))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | eps | 0.2 | 0.2 | -1.0 | 1.0 |
  | kappa | 3.0 | 2.0 | 0.05 | 50.0 |

  LCDM limit: eps=0. Recasting: derivation uses dt = a^(1/2) da /(H0 sqrt(Om)) and rho_m ~ a^-3, so d rho_DE/da ~ a^(1/2)/(1 + k a^3), integral = arctan(kappa a^1.5)/ (1.5 sqrt k) up to constants.
- High-z behaviour (z up to 1100): arctan -> 0, f -> 1 - eps: finite and positive.
- Impact if true: the DM-DE coupling has a half-saturation scale; the late-time DE growth is substrate-limited, which would explain a w < -1 apparent phase with no phantom field.
- Beyond-background fingerprint: matter loses mass to DE, shifting the matter growth rate and the matter-radiation equality inference; a growth-index deviation of definite sign.
- Prior art: query "arXiv Michaelis-Menten saturating interaction dark matter dark energy energy transfer Q rate saturation". **KNOWN**: arXiv:2604.21671, "Saturation Mechanisms in the Interacting Dark Sector" (Paliathanasis and Duffy; energy exchange regulated by a half-saturation "sparseness scale", fitted to SN, chronometers, DESI DR2 BAO, RSD; the abstract does not give the explicit equation, so the match with the arctan closed form here is by concept only).
- Weirdness 3 / Plausibility 3

### Time-dependent seesaw eigenvalue
- Field and analogy: type-I seesaw. For the mass matrix [[0, m],[m, M]], the light eigenvalue is |lambda| = 2 m^2/(M + sqrt(M^2 + 4 m^2)): equal to m when M << m (maximal mixing) and m^2/M when M >> m.
- Cosmology story: the DE scale is a light seesaw eigenvalue whose heavy partner M(z) = M0 (1+z)^p is driven by the cosmic temperature. DE is constant at late times and is power-law suppressed at high z once M exceeds m, with a calculable knee at z_s. Analogy.
- Form: density f(z) = (|lambda|(z)/|lambda|(0))^n.
  ```python
  def seesaw(zs, p, n):
      g = lambda x: 2 / (x + np.sqrt(x * x + 4))
      return lambda z: (g(((1 + np.asarray(z, float)) / (1 + zs))**p)
                        / g((1 / (1 + zs))**p))**n
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | zs | 1.0 | 0.5 | 0.05 | 10.0 |
  | p | 1.5 | 0.5 | 0.2 | 2.5 |
  | n | 0.3 | 0.3 | -0.2 | 3.0 |

  LCDM limit: n=0.
- High-z behaviour (z up to 1100): for n > 0, f ~ (1+z)^(-p n) -> 0 smoothly (no negative values); for n < 0 it grows at most as 1100^(0.5) at the bounds, still negligible against matter.
- Impact if true: DE emerges at late times because a heavy partner field decouples; its present value ties to a see-saw ratio, replacing fine tuning of rho_DE by a ratio of two scales.
- Beyond-background fingerprint: a light eigenvalue implies a very light scalar with mass ~ H0, i.e. fifth-force/screening constraints and a distinct DE sound speed.
- Prior art: query "arXiv seesaw mechanism cosmological constant dark energy scale mass matrix light eigenvalue time-dependent". None found with a redshift-dependent heavy entry as the expansion history. Adjacent: arXiv:hep-ph/0702236 "The Matrix Reloaded - on the Dark Energy Seesaw" (Enqvist, Hannestad, Sloth; extended seesaw for a light quintessence mass, a naturalness argument, no H(z) fit); also arXiv:0706.4427 "Growing neutrinos and cosmological selection" (Wetterich; time-dependent mass matrix, seen in search, not opened).
- Weirdness 4 / Plausibility 2

### Rydberg staircase
- Field and analogy: hydrogen-like level energies E_n = -R/n^2. Transitions from the ground state to n open one after another as the photon energy rises, at thresholds ~ (1 - 1/n^2), with oscillator strengths ~ n^-3, accumulating at the series limit.
- Cosmology story: a dark atom's levels each add a discrete increment to the vacuum-like energy when the dark bath cools below the n-th threshold, at 1+z_n = (1+z_inf)(1 - 1/n^2). The result is a staircase in rho_DE with steps crowding toward z_inf, widths set by a thermal smearing sigma. Analogy; the staircase is a deliberately discrete, non-smooth hypothesis.
- Form: density f(z).
  ```python
  def ryd(eps, zinf, sig):
      ns = np.arange(2, 13)
      zn = (1 + zinf) * (1 - 1 / ns**2) - 1
      w = ns**-3.0
      def G(z):
          z = np.asarray(z, float)
          return 1 + eps * np.sum(w * 0.5 * (1 - np.tanh((z[..., None] - zn) / sig)), axis=-1)
      return lambda z: G(z) / G(0.0)
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | eps | 0.5 | 0.5 | -4.0 | 20.0 |
  | zinf | 2.0 | 0.5 | 0.3 | 6.0 |
  | sig | 0.1 | 0.05 | 0.02 | 0.5 |

  LCDM limit: eps=0. (sum of weights for n=2..12 is about 0.19, so eps=-4 stays positive.)
- High-z behaviour (z up to 1100): all steps off for z > z_inf, so f = 1/G(0): constant, finite and positive.
- Impact if true: dark energy has discrete spectral structure, a "dark atom"; the first measured step redshift and the 1/n^2 spacing would fix a dark Rydberg constant. Data resolution is limited, so a first pass will see mainly a smoothed single step; the sharp version is a target for future surveys.
- Beyond-background fingerprint: discrete steps in w(z) show as correlated residuals in binned H(z); dark-atom lines could also appear as features in 21-cm-like dark bath observables.
- Prior art: query "arXiv Rydberg series hydrogen-like spectrum dark atom dark energy staircase transitions redshift". None found.
- Weirdness 5 / Plausibility 1

### Efimov log-periodic dark energy
- Field and analogy: Efimov effect. Three resonantly interacting particles have an infinite geometric tower of bound states with ratio exp(pi/s0), about 22.7 for s0 = 1.00624, i.e. discrete scale invariance and log-periodic observables.
- Cosmology story: a dark-sector three-body resonance imprints a log-periodic modulation on the vacuum energy as a function of the temperature scale (1+z), damped by a power law away from the unitary regime. The data constrain the discrete scaling factor directly, and s0 can be tested against the universal Efimov value. Analogy.
- Form: density f(z).
  ```python
  lambda eps, s0, phi, p: (lambda z:
      (1 + eps * (1 + np.asarray(z, float))**(-p) * np.cos(s0 * np.log1p(np.asarray(z, float)) + phi))
      / (1 + eps * np.cos(phi)))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | eps | 0.1 | 0.1 | -0.9 | 0.9 |
  | s0 | 1.0 | 0.3 | 0.3 | 6.0 |
  | phi | 0.0 | 0.8 | -3.14 | 3.14 |
  | p | 0.5 | 0.4 | 0.0 | 3.0 |

  LCDM limit: eps=0.
- High-z behaviour (z up to 1100): the envelope (1+z)^-p <= 1 and |eps| < 1 keep f in (0, 2); finite. At s0 = 1.006 a full log-period spans (1+z) ratio 22.7, so BAO/SN (z < 2.3) see well under one period.
- Impact if true: the Universe's dark sector has a hidden discrete scale symmetry; the signal would be a log-periodic oscillation in w(z) with a universal ratio, a smoking gun that no smooth parametrisation can mimic.
- Beyond-background fingerprint: log-periodic features in the matter power spectrum or primordial spectrum with the same period in ln k, and the same scale factor in gravitational-wave backgrounds.
- Prior art: query "arXiv Efimov discrete scale invariance log-periodic oscillations dark energy equation of state cosmology" (plus a second query "log-periodic oscillations dark energy equation of state oscillating dark energy discrete scale invariance"). None found on arXiv. One unverified lead, not an arXiv paper and not opened: an academia.edu document "Cyclic Tests v2" claiming cyclic dark energy from discrete scale invariance; also Efimov/DSI background (arXiv:cond-mat/0612123, "Efimov Physics in Cold Atoms", seen in the search, not opened).
- Weirdness 4 / Plausibility 1

### Bateman intermediate-daughter dark energy
- Field and analogy: radioactive decay chain A -> B -> C (Bateman). The intermediate population N_B(t) = N_A0 l1/(l2-l1) (exp(-l1 t) - exp(-l2 t)) rises, peaks and decays with a fast rise and a slow tail (transient equilibrium).
- Cosmology story: DE is the energy stored in the intermediate species of a two-step dark decay chain; the matter-era clock sets t. Compared with a symmetric Gaussian "bump", this shape is asymmetric with a fixed relation between rise and fall set by the ratio of the two decay constants. Analogy.
- Form: density f(z), matter-era clock t = a^1.5.
  ```python
  def bateman(A, lam1, r):
      lam2 = r * lam1
      P2 = lambda t: lam1 / (lam2 - lam1) * (np.exp(-lam1 * t) - np.exp(-lam2 * t))
      clock = lambda z: (1 / (1 + np.asarray(z, float)))**1.5
      return lambda z: (1 + A * P2(clock(z))) / (1 + A * P2(1.0))
  ```
  | name | x0 | scale | lo | hi |
  |---|---|---|---|---|
  | A | 0.2 | 0.2 | -0.95 | 3.0 |
  | lam1 | 2.0 | 1.0 | 0.2 | 20.0 |
  | r | 4.0 | 2.0 | 1.1 | 50.0 |

  LCDM limit: A=0. (r is bounded away from 1 to avoid the degenerate case lam2 = lam1.)
- High-z behaviour (z up to 1100): clock -> 0, P2 -> 0, f -> 1/(1 + A P2(1)): finite and positive (P2 in [0,1) so A > -1 keeps it positive).
- Impact if true: a dark sector with sequential decays (not only DM -> radiation) would give a fixed-shape transient in the expansion history, with two measurable lifetimes and a branching-like amplitude.
- Beyond-background fingerprint: sequential decay products (dark radiation or light species) leave a dark-radiation component at early times and a modified late-time growth.
- Prior art: query "arXiv radioactive decay chain Bateman equations dark sector sequential decays dark energy". None found as a Bateman-shape expansion history. Adjacent: arXiv:astro-ph/0405455 "Dark matter and dark energy production in quantum model of the universe" (Kuzmichev and Kuzmichev; dark energy as undecayed excitations, rate equations for a chain); not the same closed form.
- Weirdness 3 / Plausibility 2

---

## Needs ODE

1. **Axion with a temperature-switched mass (QCD-style).** Field phi with m(a) = m0 min(1, (a/a_c)^b) (mass grows as the bath cools, m ~ T^-b with b about 4 for QCD):
   `phi'' + 3 H phi' + m(a)^2 phi = 0`, with rho_phi = phi'^2/2 + m(a)^2 phi^2/2 (adjust for the time dependence of m), `w = (phi'^2/2 - V)/(phi'^2/2 + V)`, H from Friedmann. Free parameters: m0/H0, a_c, b, phi_i. DE stays frozen (w = -1) until 3H = m(a), then dilutes; the onset can be tuned to z ~ 0.5. Closest prior art found: arXiv:2405.20478 (Muursepp; confining pNGB with a temperature-dependent mass as DE).
2. **Full MSW non-adiabatic evolution (Landau-Zener).** Replace the equilibrium mixing angle by the two-state Schrodinger equation `i d/dt (c1,c2) = [[V(t)/2 - dm2/4E, g],[g, -V(t)/2 + dm2/4E]] (c1,c2)` with V ~ rho_m(t); the survival probability includes Stueckelberg oscillations after the crossing (chirped, damped), a distinctive wiggle in w(z).
3. **Dark Brusselator chemical clock.** Two coupled species X,Y with dX/dN = A - (B+1) X + X^2 Y, dY/dN = B X - X^2 Y (N = ln a); DE = alpha X(N) on a limit cycle, a self-sustained oscillation in w(z) whose amplitude does not depend on initial conditions. Parameters: A, B, alpha, phase.
4. **Peebles-type dark recombination.** Replace Saha equilibrium by `dx/dN = -(Gamma(T)/H) [x^2 n S_inv - (1-x)] ` with the rate coefficient Gamma(T) ~ T^-1/2: the departure from Saha at late times (known to be large in atomic dark matter) turns the DE-carrying fraction x into a frozen relic.
5. **Interacting Michaelis-Menten with back-reaction.** `d rho_DE/dN = +Q/H`, `d rho_m/dN = -3 rho_m - Q/H`, Q = V rho_m/(Km + rho_m): drops the small-conversion approximation used in the closed form above.
