# Dreaming to Dream — Lonely Memory Variant

## Goal

Compose an original childhood-memory sadness cue using only abstract strategies observed from reference material. Do **not** copy any literal melody, bar-by-bar harmony, exact orchestration sequence, or key-change scheme.

## Direct observations from the uploaded score

The score used for this profile visibly contains:

- a compound 6/8-like pulse with dotted-quarter tempo markings;
- section labels A, B and C at approximately dotted-quarter = 34, 41 and 35;
- sparse orchestration for flute, clarinet, glockenspiel, piano, harp, violin and cello;
- many sustained string notes and long rests;
- short harp/piano broken-note gestures rather than continuous filling;
- changing lead roles across sections.

These observations are source-derived. The emotional labels and generator rules below are working interpretations rather than claims about the composer's intent.

## Working emotional arc

1. **Distant remembrance** — the room exists before the melody fully speaks.
2. **Falling inward** — a lower, warmer inner voice replaces the distant lead.
3. **Acceptance** — two voices begin to answer each other rather than simply deepen the sadness.
4. **Afterimage** — most material disappears and an earlier idea returns in thinner form.

## Composition rules

- Use 6/8 with a very slow felt dotted-quarter pulse.
- Write long phrases, not one- or two-bar loops.
- Flute begins as a distant lead; clarinet later becomes the inner voice.
- Harp and piano provide brief memory surfaces, then leave air.
- Strings mostly sustain time and harmonic space instead of carrying continuous melody.
- Silence and sustained notes count as musical events.
- A return must change at least one of destination, register, bass or harmony.
- A climax should become warmer, wider or more connected — not merely denser.
- The coda should strip material away and return only a fragment of the opening thought.

## Prototype implementation

The current experiment is in:

`research/experiments/dreaming_to_dream_lonely_memory/song.py`

Form:

- Distant Room — 4 bars
- A — Remembering — 8 bars
- B — Falling Inward — 8 bars
- C — Acceptance — 8 bars
- Coda — Afterimage — 4 bars

The prototype uses the existing portable MIDI Formula SDK rather than a separate music engine.

## Known SDK limitation

The current portable SDK writes one global tempo event. The reference score visibly uses different section tempos, but this prototype cannot yet represent a true tempo map. It therefore uses one global quarter-note BPM of 54, which gives a felt dotted-quarter pulse of approximately 36 BPM in 6/8.

This limitation is recorded rather than hidden; tempo-map support is a candidate SDK improvement driven by observed musical need.

## Copyright / research boundary

The uploaded reference score and audio are **not** stored in this repository. This profile stores only abstract observations and newly authored composition rules. The experiment source uses newly written melodic and harmonic material.
