"""Order-of-magnitude kills for two cross-connection ideas (ID-017, ID-018).

All inputs are round textbook-level values, stated below. These are back-of-envelope
checks meant to kill ideas cheaply, not precision results.
"""

import numpy as np

GEV_PER_GAUSS2 = 1.95e-20   # 1 Gauss = 1.95e-20 GeV^2 (natural units)
GEV_INV_PER_M = 5.068e15    # 1 m = 5.068e15 GeV^-1
MPC_M = 3.086e22
M_PL = 2.435e18             # reduced Planck mass [GeV]


def id017_axion_triple():
    """One axion-like field: dark energy + CMB birefringence + SN dimming
    (distance-duality violation via photon->axion conversion in IGM magnetic fields)."""
    print("ID-017: one axion for dark energy + birefringence + SN dimming")
    beta = np.radians(0.34)            # birefringence angle (WMAP+Planck)
    # Birefringence from a field excursion: beta = g * dphi / 2
    # (a) If the axion IS the dark energy, dphi ~ 0.1-1 M_pl (thawing quintessence).
    for frac in (0.1, 1.0):
        g_needed = 2 * beta / (frac * M_PL)
        print(f"  DE field excursion {frac} M_pl -> coupling for beta=0.34 deg: g ~ {g_needed:.1e} GeV^-1")
    # (b) SN dimming by photon->axion conversion: random magnetic domains, P per domain
    #     = (g B s / 2)^2, N = L/s domains. Needed: ~2% distance (~0.04 mag) by z ~ 0.6.
    B = 1e-9 * GEV_PER_GAUSS2          # 1 nG, roughly the upper limit on IGM fields
    s = 1 * MPC_M * GEV_INV_PER_M      # 1 Mpc domains
    L_over_s = 2000                    # ~2 Gpc path
    for g in (1e-19, 6e-13, 3e-12):
        p_tot = L_over_s * (g * B * s / 2) ** 2
        dmag = -2.5 * np.log10(1 - (2 / 3) * min(p_tot, 0.99))
        print(f"  g = {g:.0e} GeV^-1 -> conversion dimming ~ {abs(dmag):.1e} mag (need ~0.04)")
    print("  Verdict: a DE-sized field excursion needs g ~ 1e-20..1e-19 for the birefringence,")
    print("  which gives no measurable dimming (needs g ~ 1e-12, near or above existing bounds")
    print("  of order 1e-12 GeV^-1 for very light axions). One field cannot do all three.\n")


def id018_black_holes_lensing():
    """Could unmodelled black-hole mass (LRDs, overmassive BHs) cause the CMB lensing excess?"""
    print("ID-018: black-hole mass as the source of excess CMB lensing")
    rho_bh = 5e5                        # local SMBH mass density ~ 5e5 Msun/Mpc^3 (approx.)
    rho_crit = 2.775e11 * 0.68 ** 2     # Msun/Mpc^3
    om_bh = rho_bh / rho_crit
    print(f"  Omega_BH ~ {om_bh:.0e}  vs  Omega_m ~ 0.3  ->  fraction ~ {om_bh/0.3:.0e}")
    print("  The lensing excess behind 'negative neutrino mass' is a few-percent effect")
    print("  (comparable to the ~0.06 eV neutrino suppression, a few % of power).")
    print("  Black holes are ~1e-5 of the matter and trace existing halos. Dead by ~3-4 orders.\n")


if __name__ == "__main__":
    id017_axion_triple()
    id018_black_holes_lensing()
