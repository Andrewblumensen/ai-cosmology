"""DESI DR2 BAO Gaussian likelihood (13 measurements, full covariance).

Data: CobayaSampler/bao_data, desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_*.txt
Paper: DESI Collaboration, arXiv:2503.14738
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .background import Background

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "desi_dr2_bao"
MEAN_FILE = "desi_gaussian_bao_ALL_GCcomb_mean.txt"
COV_FILE = "desi_gaussian_bao_ALL_GCcomb_cov.txt"


class DesiDR2BAO:
    def __init__(self, data_dir: Path = DATA_DIR):
        rows = [ln.split() for ln in (data_dir / MEAN_FILE).read_text().splitlines()
                if ln.strip() and not ln.startswith("#")]
        self.z = np.array([float(r[0]) for r in rows])
        self.value = np.array([float(r[1]) for r in rows])
        self.kind = [r[2] for r in rows]
        cov = np.loadtxt(data_dir / COV_FILE)
        self.inv_cov = np.linalg.inv(cov)
        known = {"DV_over_rs", "DM_over_rs", "DH_over_rs"}
        if set(self.kind) - known:
            raise ValueError(f"Unknown BAO quantities: {set(self.kind) - known}")

    def predict(self, bg: Background, hrd: float) -> np.ndarray:
        out = np.empty_like(self.value)
        for i, (z, k) in enumerate(zip(self.z, self.kind)):
            if k == "DV_over_rs":
                out[i] = bg.dv_over_rd(z, hrd)
            elif k == "DM_over_rs":
                out[i] = bg.dm_over_rd(z, hrd)
            else:
                out[i] = bg.dh_over_rd(z, hrd)
        return out

    def chi2(self, bg: Background, hrd: float) -> float:
        r = self.predict(bg, hrd) - self.value
        return float(r @ self.inv_cov @ r)
