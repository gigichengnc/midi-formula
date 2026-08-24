# MIDI Formula

**Make AI-written MIDI generation logic editable, inspectable, and reusable — then hand the rough MIDI to a human editor.**

MIDI Formula started from a real Claude-assisted composition project where Claude wrote Python that directly emitted multitrack Standard MIDI Files. The project now has two connected layers:

1. **Evidence layer** — preserve and inspect the explicit composition logic Claude wrote in the original project.
2. **AI Composer SDK** — give future coding AIs a stable, zero-dependency API so they can write a readable song program, generate a useful rough `.mid`, and leave taste-level polishing to a human in Signal MIDI or another editor.

```text
human musical direction
        ↓
AI reads prompts/AI_COMPOSER.md
        ↓
AI writes readable song logic
(form / harmony / tracks / transitions / patterns)
        ↓
MIDI Formula raw SMF writer
        ↓
rough editable .mid
        ↓
Signal MIDI / DAW
        ↓
human refinement
```

## Why rough MIDI first

The goal is not `formula -> perfect finished song`. AI is useful for producing a coherent 60–85% first draft quickly. Once the MIDI exists, a human can often fix local musical choices faster in a piano roll: move one note, shorten a transition, lower one track, duplicate four bars, or change an instrument.

The formula layer therefore controls **how the first draft is generated**, while Signal remains the place for note-level and arrangement-level finishing.

## AI Composer SDK

The v0.2 SDK keeps MIDI serialization stable and lets the AI focus on composition:

```text
src/midi_formula/midi.py       raw Standard MIDI File writer
src/midi_formula/theory.py     note/chord helpers
src/midi_formula/structure.py  explicit sections and bar starts
src/midi_formula/patterns.py   reusable rough accompaniment/transition patterns
prompts/AI_COMPOSER.md         contract for Claude/Codex/Gemini-style coding agents
examples/rough_draft.py        complete rough-draft example
```

Generate and validate the example with ordinary Python:

```bash
PYTHONPATH=src python examples/rough_draft.py
python tools/validate_midi.py output/rough_draft.mid
```

No `mido`, `music21`, DAW plugin, or other MIDI-writing dependency is required.

## Transparent MIDI bytes

The writer emits the Standard MIDI File structure directly:

- `MThd` header and `MTrk` chunks;
- variable-length delta times;
- Note On / Note Off events;
- Program Change and Control Change events;
- tempo and time-signature meta-events;
- end-of-track markers.

This keeps the path from musical rule to MIDI bytes inspectable.

## Original case study

`original/opus5/` preserves the core of *A Collection of Sweet Air*, a nine-track Claude-assisted project. Its existing MIDI files are evidence of the earlier generation workflow; MIDI Formula does not need to regenerate those songs to study their source rules.

The normalized `formula/` artifacts and source extractor show explicit section plans, dynamics, accompaniment patterns, timing, articulation, pedal and automation rules found in that generated code.

## What this is not

- Not MP3-to-MIDI transcription.
- Not MIDI-to-audio synthesis.
- Not a replacement for Signal or a DAW.
- Not a claim to recover Claude's hidden internal reasoning.
- Not a claim that every music model exposes a readable formula layer.

## Research / product question

> Can a coding AI produce music as an editable program first, a rough MIDI second, and a human-polished performance third?

MIDI Formula explores that workflow with explicit generation logic rather than treating the AI-generated song as a single opaque artifact.
