"""ID-024: if the CMB lensing excess is a real amplitude excess, what does it do to
the abundance of the rare early halos that host JWST's bright z ~ 10 galaxies?

Rare halos respond exponentially to the fluctuation amplitude, so a few-percent
amplitude excess could matter a lot. This is a "what if" sizing calculation:

- A_lens = 1.083 +/- 0.032 (excess CMB lensing power; Planck-based)
- lensing power scales ~ sigma8^2, so a matching amplitude boost is sqrt(A_lens) - 1 ~ 4%
- Assumption to be stated loudly: that boost also applies at z ~ 10. The lensing kernel
  is at z ~ 1-3; extrapolating to z ~ 10 is model-dependent.

Model: Eisenstein & Hu (1998) no-wiggle transfer function, top-hat sigma(M),
linear growth from the growth ODE in flat LCDM, Sheth-Tormen mass function.
Planck-like parameters. Expected accuracy: ~10-20% on abundances; fine for a sizing check.
"""

import numpy as np
from scipy.integrate import quad, solve_ivp

h, Om, Ob, ns, sigma8 = 0.674, 0.315, 0.049, 0.965, 0.811
rho_m = 2.775e11 * h**2 * Om  # Msun / Mpc^3


def T_eh_nowiggle(k):
    """Eisenstein & Hu 1998 no-wiggle transfer, k in 1/Mpc."""
    ombh2, omh2 = Ob * h**2, Om * h**2
    theta = 2.7255 / 2.7
    fb = Ob / Om
    s = 44.5 * np.log(9.83 / omh2) / np.sqrt(1 + 10 * ombh2**0.75)
    alpha = 1 - 0.328 * np.log(431 * omh2) * fb + 0.38 * np.log(22.3 * omh2) * fb**2
    gamma_eff = Om * h * (alpha + (1 - alpha) / (1 + (0.43 * k * s) ** 4))
    q = k * theta**2 / (gamma_eff * h)
    L0 = np.log(2 * np.e + 1.8 * q)
    C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q**2)


def sigma_R(R, norm=1.0):
    f = lambda lnk: (np.exp(lnk) ** (3 + ns) * T_eh_nowiggle(np.exp(lnk)) ** 2
                     * (3 * (np.sin(np.exp(lnk) * R) - np.exp(lnk) * R * np.cos(np.exp(lnk) * R)) / (np.exp(lnk) * R) ** 3) ** 2)
    return np.sqrt(norm * quad(f, np.log(1e-5), np.log(1e3), limit=400)[0] / (2 * np.pi**2))


NORM = (sigma8 / sigma_R(8 / h)) ** 2


def sigma_M(M):
    return sigma_R((3 * M / (4 * np.pi * rho_m)) ** (1 / 3), NORM)


def growth(z):
    """Linear growth D(z)/D(0) from the ODE in flat LCDM (radiation neglected)."""
    def rhs(lna, y):
        a = np.exp(lna)
        E2 = Om / a**3 + 1 - Om
        dlnE = -1.5 * Om / a**3 / E2
        return [y[1], -(2 + dlnE) * y[1] + 1.5 * Om / a**3 / E2 * y[0]]
    a0 = 1e-3
    sol = solve_ivp(rhs, [np.log(a0), 0], [a0, a0], dense_output=True, rtol=1e-8)
    return sol.sol(np.log(1 / (1 + z)))[0] / sol.sol(0.0)[0]


def st_f(nu):
    A, a, p = 0.3222, 0.707, 0.3
    return A * np.sqrt(2 * a / np.pi) * (1 + (a * nu**2) ** -p) * nu * np.exp(-a * nu**2 / 2)


def n_ratio(M, z, boost):
    """Abundance ratio dn/dlnM (boosted / standard); the dlnsigma/dlnM factor cancels."""
    s = sigma_M(M) * growth(z)
    nu0, nu1 = 1.686 / s, 1.686 / (s * (1 + boost))
    return st_f(nu1) / st_f(nu0)


def main():
    A_lens, dA = 1.083, 0.032
    for label, A in [("A_lens central", A_lens), ("A_lens - 1 sigma", A_lens - dA)]:
        boost = np.sqrt(A) - 1
        print(f"{label}: amplitude boost = {100*boost:.1f}%")
        for z in (8, 10, 12):
            row = []
            for logM in (10.0, 10.5, 11.0, 11.5):
                row.append(f"M=1e{logM:.1f}: x{n_ratio(10**logM, z, boost):.2f}")
            nu = 1.686 / (sigma_M(1e11) * growth(z))
            print(f"  z={z:2d} (nu(1e11)={nu:.1f})  " + "  ".join(row))
        print()


if __name__ == "__main__":
    main()
