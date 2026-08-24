# MIDI Formula

**Make AI-written MIDI generation logic editable, inspectable, and reusable — not just the rendered notes.**

MIDI Formula is a research/engineering prototype built from a real Claude-assisted composition project. In that project, Claude wrote Python that generated a multitrack MIDI album. The MIDI files already exist and remain ordinary editable MIDI. This repository focuses on the layer *before* those files: the explicit composition and performance rules encoded in the source program.

```text
prompt / human direction
        ↓
AI-written source code
        ↓
explicit generation logic   ← MIDI Formula studies this layer
        ↓
already-generated .mid
        ↓
MIDI editor / player (for example Signal)
        ↓
audio export
```

## What this is

- A way to expose **section plans, dynamics, accompaniment patterns, track roles, timing, articulation, pedal and automation rules** that an AI wrote into code.
- A case study showing how those rules map to already-generated MIDI outputs.
- A small extractor that inventories explicit rules from Python source without regenerating the music.

## What this is not

- Not MP3-to-MIDI transcription.
- Not MIDI-to-audio synthesis.
- Not a replacement MIDI editor.
- Not a claim to recover Claude's hidden internal reasoning. We only expose rules that are actually present in the generated source and project documentation.

## Repository layout

```text
original/opus5/        preserved source + generated MIDI case study
formula/               normalized, inspectable rule description
docs/                  evidence mapping and project boundaries
tools/                  source-rule extractor
tests/                  extractor checks
```

## First case study

`original/opus5/` contains the core of *A Collection of Sweet Air*, a nine-track project whose MIDI files were already generated before this repository was created. The generated `.mid` files are preserved as output evidence. MIDI Formula does **not** rebuild them as part of its core workflow.

## Research question

> Can AI-written music programs expose a useful, editable generation layer between a natural-language request and the resulting MIDI file?

The current repository is a concrete first case, not evidence that every music model exposes such a layer.
