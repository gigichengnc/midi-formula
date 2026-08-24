# AGENTS.md

## Purpose

MIDI Formula studies explicit generation logic in AI-written symbolic-music programs and provides a small SDK for generating rough, editable MIDI drafts.

## Core workflow

```text
human direction
-> AI-written readable song logic
-> stable raw-MIDI SDK
-> rough .mid
-> Signal MIDI / DAW
-> human refinement
```

The generated MIDI is intentionally a draft. Do not optimize the project around one-shot final music generation.

## Composition rules for coding agents

- Read `prompts/AI_COMPOSER.md` before writing a new song.
- Put musical decisions in song code: form, harmony, track roles, transitions, patterns, dynamics and notes.
- Keep those decisions readable and editable near the top level of a song script.
- Reuse `midi_formula` primitives and patterns rather than expanding every passage into opaque raw note lists.
- Keep separate musical roles on separate tracks where practical so the MIDI remains easy to edit in Signal.
- Treat transitions as explicit generation logic rather than a vague hidden operation.

## MIDI engine boundary

- `src/midi_formula/midi.py` owns Standard MIDI File serialization.
- Do not rewrite the MIDI byte layer for every new song.
- Do not add `mido`, `music21`, DAW plugins, or other MIDI dependencies without a concrete need.
- The zero-dependency writer should remain inspectable: `MThd`, `MTrk`, VLQ, note events, CC, program changes and meta-events are emitted directly.

## Evidence boundaries

- Existing MIDI files under `original/` are evidence outputs. Do not silently regenerate or replace them.
- Do not describe extracted source rules as Claude's hidden chain of thought or true internal reasoning.
- Prefer claims such as "explicit source rule", "documented production rule", or "observed output".
- Do not add MP3-to-MIDI or audio-transcription scope unless a separate research question requires it.
- Keep source evidence linked to file paths and, where practical, line numbers.
- Preserve `original/` as a case-study snapshot; new abstractions belong outside it.

## Validation

For SDK changes, run:

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src python examples/rough_draft.py
python tools/validate_midi.py output/rough_draft.mid
```
