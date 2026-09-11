# MIDI Formula

**Prompt → readable Python → editable MIDI → human refinement.**

> **Research preview — All rights reserved.** This public repository is currently shared for inspection, academic discussion, provenance, and faculty/research review. It is **not currently an open-source or open-content release**. See [`RIGHTS.md`](RIGHTS.md) and [`LICENSING.md`](LICENSING.md).

MIDI Formula is an active research/engineering prototype exploring whether general-purpose coding LLMs can act as transparent symbolic-music co-creators through a very small fixed interface.

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
editable .mid
    ↓
Signal MIDI / DAW
    ↓
human refinement
```

## Research question

The current research direction is broader than “can AI generate MIDI?” Existing systems already do that.

> **How reliably can different general-purpose coding LLMs use the same small transparent interface to turn musical intent into executable, editable symbolic-music programs; where do they fail; and what is the value of keeping a readable program between the prompt and the MIDI output?**

The SDK is research apparatus, not the sole novelty claim.

## Current status

This repository is **public but still a work in progress**.

- **PR #1 — evidence / case-study layer:** studies explicit AI-written composition rules from an earlier Claude-assisted nine-song project.
- **PR #2 — rough-first AI Composer SDK:** adds a model-agnostic zero-dependency SDK and a one-file portable mode for coding-AI tests.
- **Signal handoff:** generated rough MIDI has been opened and edited successfully in Signal MIDI.
- **Pilot B01 — Night Train:** initial fixed-brief tests have been run with Grok, ChatGPT, and DeepSeek. The pilot demonstrates feasibility and has already exposed a concrete meter/timing interpretation failure, but it is far too small for statistical or publication claims.
- **Research release:** not frozen yet. Audit hardening, benchmark structure, and experiment documentation are still being consolidated.

For a faculty/research-oriented summary, see [`RESEARCH_PREVIEW.md`](RESEARCH_PREVIEW.md).

## Try the current portable SDK

The current one-file SDK lives on the active SDK branch:

[`portable/midi_formula_sdk.py`](https://github.com/gigichengnc/midi-formula/blob/feature/ai-composer-sdk/portable/midi_formula_sdk.py)

A coding AI can be given that file plus a musical brief and asked to create a readable song script and rough editable `.mid` without adding `mido`, `music21`, or another MIDI-writing dependency.

The intended user workflow is:

```text
midi_formula_sdk.py + musical brief
        ↓
ChatGPT / Claude / Grok / DeepSeek / other coding LLM
        ↓
song.py
        ↓
song.mid
        ↓
Signal MIDI / DAW
```

## What this project is testing

MIDI Formula currently focuses on three questions:

1. **Reliability:** can different coding LLMs produce valid, prompt-conforming MIDI through one fixed interface?
2. **Failure modes:** where do models diverge in meter, duration, form, instrumentation, transitions, dependencies, and executable correctness?
3. **Human editability:** does exposing readable generation logic plus editable MIDI support understandable and controllable refinement?

The third question is **not yet proven**. Signal compatibility is demonstrated; editing efficiency, user agency, and human-participant outcomes still require a proper study and, where applicable, ethics approval.

## What this is not

- Not MP3-to-MIDI transcription.
- Not MIDI-to-audio synthesis.
- Not a replacement for a DAW or MIDI editor.
- Not a claim to recover hidden chain-of-thought or model-internal reasoning.
- Not a claim to be the first AI system that generates editable MIDI.
- Not yet a completed benchmark or publication-ready dataset.

## Development structure

Because the project is being built in layers, `main` currently serves as the research-facing landing page while the implementation remains in open PRs:

- [PR #1 — Establish explicit AI-to-MIDI formula layer](https://github.com/gigichengnc/midi-formula/pull/1)
- [PR #2 — Add rough-first AI Composer SDK](https://github.com/gigichengnc/midi-formula/pull/2)

The planned next milestone is a frozen pilot/research release with a stable SDK, documented benchmark protocol, preserved model outputs, machine-readable metrics, and a clear experimental boundary.

## Reproducibility principle

The project deliberately separates:

```text
AI composition capability
        from
chat-platform file/execution capability
```

For example, a model can still succeed at the composition task by producing a runnable song program even if its chat interface cannot directly execute Python or return a binary `.mid` file.

That distinction is part of the planned cross-model evaluation rather than being treated as an automatic model failure.

## Rights and current licensing status

The current research-preview version is **All Rights Reserved** unless a file explicitly states otherwise.

- The SDK/software is visible for review, but the current/future research-preview revisions are not being newly offered under an open-source license.
- MIDI Formula research/project documentation is likewise rights-reserved for the current research-preview state.
- Opus 5 and related creative case-study material remains rights-reserved.
- Future benchmark/model/human-participant data will receive separate release terms only if and when it is appropriate to publish them.

Earlier revisions were briefly released under Apache-2.0 and CC BY 4.0; those earlier grants are not retroactively revoked. See [`LICENSING.md`](LICENSING.md) for the version boundary and [`RIGHTS.md`](RIGHTS.md) for the current notice.
