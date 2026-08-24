# AI Composer SDK workflow

MIDI Formula v0.2 treats generated MIDI as a **draft**, not the final artifact.

```text
human musical direction
        ↓
AI reads AI_COMPOSER.md + SDK
        ↓
AI writes a readable song script
        ↓
zero-dependency raw Standard MIDI File writer
        ↓
rough .mid
        ↓
Signal MIDI / DAW
        ↓
human taste-level editing
```

The SDK separates two responsibilities:

- `src/midi_formula/midi.py` owns MIDI byte serialization and should remain stable.
- song scripts own form, harmony, track roles, transitions, patterns and notes.

This lets an AI focus on composition rather than reinventing SMF encoding for every song.

## Why rough first

The intended workflow is not `formula -> perfect final song`. AI should create a coherent first draft quickly. A human can then fix local musical decisions faster in a piano roll: shorten a transition, move one note, reduce a track velocity, duplicate four bars, or change an instrument.

## Minimal use

```bash
PYTHONPATH=src python examples/rough_draft.py
python tools/validate_midi.py output/rough_draft.mid
```

Then open `output/rough_draft.mid` in Signal MIDI or another MIDI editor.
