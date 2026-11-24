"""Tabulate early-universe quantities from CAMB on an (omega_b, omega_bc) grid.

z_star, r_star and r_drag depend only on the physical densities when dark energy
is negligible before recombination (checked: < 1e-7 change with H0 or w0wa).
CAMB is what DESI and the Planck compression used, so tabulating it once keeps the
search loop fast and on the same footing as the published results.

Output: src/aicosmo/early_table.txt (committed). Re-run only if the grid changes.
"""

from pathlib import Path

import camb
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "aicosmo" / "early_table.txt"

OMEGA_B = np.linspace(0.0195, 0.0250, 12)
OMEGA_BC = np.linspace(0.115, 0.170, 12)


def early(omega_b: float, omega_bc: float) -> tuple[float, float, float]:
    p = camb.set_params(H0=67.0, ombh2=omega_b, omch2=omega_bc - omega_b,
                        mnu=0.06, nnu=3.044, num_massive_neutrinos=1)
    d = camb.get_background(p).get_derived_params()
    return d["zstar"], d["rstar"], d["rdrag"]


def main() -> None:
    rows = [(wb, wbc, *early(wb, wbc)) for wb in OMEGA_B for wbc in OMEGA_BC]
    header = (f"CAMB {camb.__version__}; mnu=0.06 (1 massive), Neff=3.044, TCMB=2.7255\n"
              "omega_b omega_bc z_star r_star[Mpc] r_drag[Mpc]")
    np.savetxt(OUT, rows, fmt="%.10g", header=header)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
