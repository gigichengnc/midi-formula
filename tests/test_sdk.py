from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from midi_formula import Song, note_number

SPEC = importlib.util.spec_from_file_location("validate_midi", ROOT / "tools" / "validate_midi.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


def test_zero_dependency_writer_emits_valid_type1_midi(tmp_path):
    song = Song("test", bpm=100)
    piano = song.add_track("piano", 0, 0)
    piano.note(0, 1, note_number("C4"), 80)
    path = song.save(tmp_path / "test.mid")
    info = validator.inspect(path)
    assert info["format"] == 1
    assert info["tracks"] == 2
    assert info["ppq"] == 480


def test_example_generates_rough_draft(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = (ROOT / "examples" / "rough_draft.py").read_text(encoding="utf-8")
    exec(compile(source, "rough_draft.py", "exec"), {"__name__": "__main__"})
    path = tmp_path / "output" / "rough_draft.mid"
    info = validator.inspect(path)
    assert info["tracks"] == 5
    assert info["bytes"] > 500
