"""Best-fit (MAP) search and Gaussian error estimates for chi2 functions.

Search loops need the minimum chi2 per model, not full posteriors, so this is a
robust Nelder-Mead with restarts. Any ValueError from the model (unphysical
history) counts as a rejected point.
"""

from __future__ import annotations

from typing import Callable

import numpy as np
from scipy.optimize import minimize

Chi2Fn = Callable[[np.ndarray], float]
REJECT = 1e10


def safe(f: Chi2Fn) -> Chi2Fn:
    def g(p):
        try:
            v = f(np.asarray(p, dtype=float))
        except ValueError:
            return REJECT
        return v if np.isfinite(v) else REJECT
    return g


def best_fit(f: Chi2Fn, x0, scale, restarts: int = 4):
    """Minimise chi2 from x0; `scale` sets the initial simplex size per parameter.
    Restarts from the current best until chi2 stops improving."""
    f = safe(f)
    x, best = np.asarray(x0, dtype=float), np.inf
    scale = np.asarray(scale, dtype=float)
    for _ in range(restarts):
        simplex = np.vstack([x] + [x + np.eye(len(x))[i] * scale[i] for i in range(len(x))])
        res = minimize(f, x, method="Nelder-Mead",
                       options={"initial_simplex": simplex, "xatol": 1e-8, "fatol": 1e-7,
                                "maxiter": 40000, "maxfev": 40000})
        improved = best - res.fun
        x, best = res.x, res.fun
        if improved < 1e-4:
            break
    return x, float(best)


def gaussian_errors(f: Chi2Fn, x, steps) -> np.ndarray:
    """1-sigma errors from the numerical Hessian of chi2/2 at the minimum."""
    f = safe(f)
    x, steps = np.asarray(x, dtype=float), np.asarray(steps, dtype=float)
    n = len(x)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            ei, ej = np.eye(n)[i] * steps[i], np.eye(n)[j] * steps[j]
            H[i, j] = H[j, i] = (f(x + ei + ej) - f(x + ei - ej) - f(x - ei + ej)
                                 + f(x - ei - ej)) / (4 * steps[i] * steps[j])
    return np.sqrt(np.diag(np.linalg.inv(H / 2)))
