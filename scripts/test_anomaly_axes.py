"""ID-022: do reported anomaly axes cluster on the sky? (pre-registered in IDEAS.md)"""

import itertools
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from aicosmo.sn import unit  # noqa: E402

AXES = {
    "CMB dipole": (264.0, 48.3),
    "CatWISE quasar dipole": (238.2, 28.8),
    "CMB hemispherical asymmetry": (230.0, -16.0),
    "CMB quadrupole": (240.0, 63.0),
    "CMB octopole": (308.0, 63.0),
    "Quasar polarisation alignment": (267.0, 69.0),
    "Fine-structure dipole": (330.0, -15.0),
    "Cluster H0 anisotropy": (280.0, -15.0),
    "Pantheon+ z<0.1 dipole": (334.5, 16.0),
    "Kashlinsky bulk flow": (283.0, 11.0),
}
CMB_DERIVED = {"CMB dipole", "CatWISE quasar dipole"}
N_MC = 1_000_000
rng = np.random.default_rng(20261124)


def stat(v):
    c = np.abs(v @ v.T)
    iu = np.triu_indices(len(v), 1)
    return c[iu].mean()


def mc_pvalue(n, s_obs, chunk=50_000):
    hits = 0
    iu = np.triu_indices(n, 1)
    for _ in range(N_MC // chunk):
        x = rng.normal(size=(chunk, n, 3))
        x /= np.linalg.norm(x, axis=2, keepdims=True)
        c = np.abs(np.einsum("kij,klj->kil", x, x))[:, iu[0], iu[1]].mean(axis=1)
        hits += (c >= s_obs).sum()
    return (hits + 1) / (N_MC + 1)


def run(names, label):
    v = np.array([unit(*AXES[k]) for k in names])
    s = stat(v)
    p = mc_pvalue(len(names), s)
    print(f"{label:38s} N={len(names):2d}  mean|cos|={s:.3f} (isotropic ~0.500)  p={p:.2e}")
    return p


def main():
    cmb = unit(*AXES["CMB dipole"])
    print("Angle of each axis to the CMB dipole axis (sign-less):")
    for k, lb in AXES.items():
        ang = np.degrees(np.arccos(min(1.0, abs(unit(*lb) @ cmb))))
        print(f"  {k:32s} {ang:5.1f} deg")
    print()
    names = list(AXES)
    p_all = run(names, "All 10 axes")
    rest = [k for k in names if k not in CMB_DERIVED]
    p_rest = run(rest, "Without CMB-dipole-derived axes")
    print("\nLeave-one-out (all 10):")
    ps = {k: run([n for n in names if n != k], f"  drop {k}") for k in names}
    print(f"\nLeave-one-out p range: {min(ps.values()):.2e} .. {max(ps.values()):.2e}")
    verdict = "interesting" if (p_all < 0.003 and p_rest < 0.003) else "not significant"
    print(f"Verdict (pre-registered): {verdict}")


if __name__ == "__main__":
    main()
