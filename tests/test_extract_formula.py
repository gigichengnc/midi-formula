from pathlib import Path
import importlib.util
import json

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


def test_raw_midi_writer_is_standard_library_only():
    source = (ROOT / "original" / "opus5" / "src" / "midilib.py").read_text(encoding="utf-8")
    assert "import struct, random, math" in source
    assert 'b"MThd"' in source
    assert 'b"MTrk"' in source
    assert 'open(path, "wb")' in source
    assert "mido" not in source
    assert "music21" not in source


def test_existing_midi_outputs_are_recorded_as_evidence():
    rows = json.loads((ROOT / "evidence" / "generated_midi.json").read_text(encoding="utf-8"))
    assert len(rows) == 9
    assert all(row["header"] == "MThd" for row in rows)
    assert all(len(row["sha256"]) == 64 for row in rows)
