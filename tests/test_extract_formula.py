from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("extract_formula", ROOT / "tools" / "extract_formula.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


def test_formula_source_exposes_role_gain_and_plans():
    row = mod.inspect_file(ROOT / "original" / "opus5" / "src" / "formula.py")
    assert row["constants"]["ROLE_GAIN"]["peak"] == 1.10
    assert "PLAN_INSTRUMENTAL" in row["constants"]
    assert any(c["call"] == "cc_ramp" for c in row["calls"])


def test_existing_midi_outputs_are_preserved():
    album = ROOT / "original" / "opus5" / "album"
    mids = sorted(album.glob("*.mid"))
    assert len(mids) == 9
    assert all(p.read_bytes()[:4] == b"MThd" for p in mids)
