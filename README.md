# MIDI Formula

**Prompt → readable Python → editable MIDI → human refinement.**

MIDI Formula is an active research/engineering prototype exploring whether general-purpose coding LLMs can act as transparent symbolic-music co-creators through a small fixed interface.

Instead of asking an AI system to return only a finished audio artifact, the workflow asks it to write an inspectable Python composition program first. A zero-runtime-dependency SDK then renders ordinary multitrack Standard MIDI, which can be opened in Signal MIDI or another editor for human refinement.

```text
musical brief
    ↓
general-purpose coding LLM
    ↓
readable Python composition logic
(form / harmony / tracks / transitions / patterns)
    ↓
raw Standard MIDI File
    ↓
rough editable .mid
    ↓
Signal MIDI / DAW
    ↓
human refinement
```

## Research direction

The current question is broader than “can AI generate MIDI?” Existing systems already do that.

> **How reliably can different general-purpose coding LLMs use the same small transparent interface to turn musical intent into executable, editable symbolic-music programs; where do they fail; and what is the value of keeping a readable program between the prompt and the MIDI output?**

The SDK is research apparatus, not the sole novelty claim.

## Current pilot status

A first fixed *Night Train* brief has been tested with Grok, ChatGPT, and DeepSeek. This is a feasibility pilot, not yet a controlled benchmark.

- Grok independently understood the SDK and produced composition code; its chat environment could not return the binary MIDI file.
- ChatGPT produced a valid 6/8 multitrack draft close to the requested 90-second duration.
- DeepSeek produced valid MIDI when its script was executed locally, but interpreted the timing unit differently and generated a substantially longer piece. This exposed a concrete meter/time-unit ambiguity worth studying.

The next research phase is expected to use fixed briefs, repeated fresh generations, multiple models, automatic structural metrics, blind listening evaluation, and—only after appropriate ethics advice—a possible human refinement study.

## One-file mode — recommended

Most users and coding AIs only need:

```text
portable/midi_formula_sdk.py
+ a musical brief
```

The portable file contains the embedded AI Composer contract, raw Standard MIDI File writer, note/chord helpers, section primitives, rough accompaniment/transition patterns, and structural validation. It uses only the Python standard library.

Example instruction:

```text
Use midi_formula_sdk.py as the existing SDK.
Read AI_COMPOSER_CONTRACT inside it.
Do not rewrite the MIDI engine or add third-party MIDI libraries.
Write a new Python song script for this brief:

[describe the music here]

Generate a rough editable .mid for later human refinement in Signal MIDI.
```

A generated song can import directly from the one file:

```python
from midi_formula_sdk import Song, Section, progression, eighth_arpeggio, validate_midi
```

## Modular SDK

The maintainable development version is split into:

```text
src/midi_formula/midi.py       raw Standard MIDI File writer
src/midi_formula/theory.py     note/chord helpers
src/midi_formula/structure.py  explicit sections and bar starts
src/midi_formula/patterns.py   reusable accompaniment/transition patterns
prompts/AI_COMPOSER.md         coding-agent contract
examples/rough_draft.py        working rough-draft example
portable/midi_formula_sdk.py   self-contained user-facing SDK
```

Generate and validate the repository example with ordinary Python:

```bash
PYTHONPATH=src python examples/rough_draft.py
python tools/validate_midi.py output/rough_draft.mid
```

No `mido`, `music21`, DAW plugin, or other runtime MIDI-writing dependency is required.

## Evidence / Opus 5 case study

MIDI Formula grew from a Claude-assisted nine-song project, *A Collection of Sweet Air*. The evidence layer preserves explicit source rules from that project and records historical MIDI output hashes.

The current branch now restores the original nine-song source table that was missing in the first snapshot, but **audit hardening is still being consolidated**. Do not treat the current branch as a finished archival reconstruction or frozen research release yet.

The original Opus 5 code is also richer than this SDK: it contains performance-oriented behavior that the v0.2 rough-draft interface intentionally does not fully port.

## What this project is testing

1. **Reliability:** can different coding LLMs produce valid, prompt-conforming MIDI through one fixed interface?
2. **Failure modes:** where do models diverge in meter, duration, form, instrumentation, transitions, dependencies, and executable correctness?
3. **Human editability:** does readable generation logic plus editable MIDI support understandable and controllable refinement?

The third question is **not yet proven**. Signal compatibility is demonstrated; editing efficiency, agency, and human-participant outcomes still require a proper study.

## What this is not

- Not MP3-to-MIDI transcription.
- Not MIDI-to-audio synthesis.
- Not a replacement for Signal or a DAW.
- Not a claim to recover hidden chain-of-thought or model-internal reasoning.
- Not a claim to be the first AI system that generates editable MIDI.
- Not yet a completed benchmark or publication-ready dataset.

## License

MIDI Formula uses **split licensing**:

- **Software** (`portable/`, `src/`, `tools/`, `tests/`, `examples/`, CI/package files): **Apache License 2.0**.
- **Original MIDI Formula research/project documentation:** **CC BY 4.0** unless specifically excluded.
- **Opus 5 and related creative case-study material:** excluded from those open licenses unless a file explicitly says otherwise.
- **Future benchmark/model/human-participant data:** licensing will be decided separately before release.

See [`LICENSING.md`](LICENSING.md) for the exact scope, [`LICENSE`](LICENSE) for Apache-2.0, and [`original/opus5/RIGHTS.md`](original/opus5/RIGHTS.md) for the case-study boundary.

## Status for reviewers

This is PR #2, stacked on the evidence-layer PR #1. The current research-facing goal is to consolidate audit fixes, freeze a stable SDK version, document the pilot as research data, and define benchmark metrics before broader promotion or citation. The code/documentation/creative-material licensing boundary is now explicit; future benchmark and human-participant data will be handled separately.

See [`docs/README_FOR_REVIEWERS.md`](docs/README_FOR_REVIEWERS.md) for a short orientation.
