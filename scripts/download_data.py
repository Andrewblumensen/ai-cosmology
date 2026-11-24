"""Fetch public likelihood data into data/. Safe to re-run."""

from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW = "https://raw.githubusercontent.com/CobayaSampler/bao_data/master"
PP = ("https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
      "Pantheon%2B_Data/4_DISTANCES_AND_COVAR")

# DES-SN5YR / DES-Dovekie are deliberately NOT downloaded: they are the held-out set.
FILES = {
    "desi_dr2_bao": [
        f"{RAW}/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt",
        f"{RAW}/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt",
    ],
    "desi_dr1_bao": [
        f"{RAW}/desi_2024_gaussian_bao_ALL_GCcomb_mean.txt",
        f"{RAW}/desi_2024_gaussian_bao_ALL_GCcomb_cov.txt",
    ],
    "pantheon_plus": [
        f"{PP}/Pantheon%2BSH0ES.dat",
        f"{PP}/Pantheon%2BSH0ES_STAT%2BSYS.cov",
    ],
}


def main() -> None:
    for folder, urls in FILES.items():
        out = ROOT / "data" / folder
        out.mkdir(parents=True, exist_ok=True)
        for url in urls:
            dest = out / url.rsplit("/", 1)[-1].replace("%2B", "+")
            if dest.exists():
                print(f"have  {dest.relative_to(ROOT)}")
                continue
            with urlopen(url, timeout=60) as r:
                dest.write_bytes(r.read())
            print(f"got   {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
