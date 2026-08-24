from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
SDK = ROOT / "portable" / "midi_formula_sdk.py"

spec = importlib.util.spec_from_file_location("midi_formula_portable", SDK)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_portable_sdk_generates_valid_midi(tmp_path):
    song = mod.Song("portable smoke", bpm=90)
    piano = song.add_track("Piano", channel=0, program=0)
    chords = mod.progression("Cmaj7 | Am7 | Fmaj7 | G7")
    mod.eighth_arpeggio(piano, 0, chords, bars=4)
    out = song.save(tmp_path / "portable.mid")

    info = mod.validate_midi(out)
    assert info["format"] == 1
    assert info["tracks"] == 2
    assert info["ppq"] == 480


def test_portable_sdk_embeds_composer_contract():
    text = mod.AI_COMPOSER_CONTRACT
    assert "60–85%" in text
    assert "do not rewrite MIDI serialization" in text
    assert "Signal MIDI" in text
