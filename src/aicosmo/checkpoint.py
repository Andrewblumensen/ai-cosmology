"""Crash-safe progress files for long runs (mock calibrations take hours).

Each finished unit of work is appended as one JSON line and flushed to disk at once, so a
shutdown or crash loses at most the fits that were running. On restart, finished units are
read back and skipped. A half-written last line (power cut mid-write) is ignored.

Usage:
    ck = Checkpoint(ROOT / "runs" / "name.ckpt.jsonl")
    if "real" not in ck: ck.add("real", compute())
    todo = [job for job in jobs if key(job) not in ck]
"""

from __future__ import annotations

import json
import os
from pathlib import Path


class Checkpoint:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data: dict[str, object] = {}
        if self.path.exists():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                try:
                    rec = json.loads(line)
                    self.data[rec["k"]] = rec["v"]
                except (ValueError, KeyError, TypeError):
                    continue  # torn last line from an interrupted write
        self._f = open(self.path, "a", encoding="utf-8")
        if self.path.stat().st_size and not self.path.read_bytes().endswith(b"\n"):
            self._f.write("\n")  # start a fresh line after a torn one

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def __getitem__(self, key: str):
        return self.data[key]

    def __len__(self) -> int:
        return len(self.data)

    def add(self, key: str, value) -> None:
        self.data[key] = value
        self._f.write(json.dumps({"k": key, "v": value}) + "\n")
        self._f.flush()
        os.fsync(self._f.fileno())

    def close(self) -> None:
        self._f.close()
