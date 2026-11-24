import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aicosmo.checkpoint import Checkpoint  # noqa: E402


def test_roundtrip_and_torn_line(tmp_path):
    p = tmp_path / "x.ckpt.jsonl"
    ck = Checkpoint(p)
    ck.add("real", [1.5, 2.5])
    ck.add("3,7", 1412.25)
    ck.close()
    with open(p, "a", encoding="utf-8") as f:
        f.write('{"k": "4,0", "v": 14')  # simulated power cut mid-write
    ck2 = Checkpoint(p)
    assert "real" in ck2 and ck2["real"] == [1.5, 2.5]
    assert ck2["3,7"] == 1412.25
    assert "4,0" not in ck2
    assert len(ck2) == 2
    ck2.add("4,0", 1.0)
    ck2.close()
    assert Checkpoint(p)["4,0"] == 1.0
