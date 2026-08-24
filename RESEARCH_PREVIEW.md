# Research preview

This repository is an active research/engineering prototype exploring a transparent workflow for symbolic music co-creation with general-purpose coding LLMs.

The current research direction asks:

> How reliably can general-purpose coding LLMs turn the same musical brief into executable, editable symbolic-music programs through a small fixed interface, where do they fail, and what is the value of leaving a readable program between the prompt and the MIDI output?

## Pilot status

A first fixed *Night Train* brief has been tested with multiple general-purpose models. The pilot is not yet a controlled benchmark and no statistical claims are made.

- **Grok:** independently understood the SDK and produced composition code; its chat environment could not return the binary MIDI file.
- **ChatGPT:** produced a valid 6/8 multitrack draft close to the requested 90-second duration.
- **DeepSeek:** produced valid MIDI when its script was executed locally, but interpreted the 6/8 timing unit differently and generated a substantially longer piece. This exposed a useful interface-semantics failure mode.

## Proposed study

The next research phase is expected to use fixed briefs, repeated fresh generations, multiple coding LLMs, automatic structural checks, blind listening measures, and—only after appropriate ethics advice—a possible human refinement study in a MIDI editor.

The SDK itself is research apparatus rather than the sole novelty claim. The project does **not** claim to invent text-to-MIDI generation or to recover hidden model reasoning.

## Current repository state

- `main` is currently the public landing page.
- PR #1 develops the original evidence/case-study layer.
- PR #2 develops the portable rough-first AI Composer SDK on top of PR #1.
- Audit hardening and pilot documentation are still being consolidated before a frozen research release/tag.

Until that release is frozen, treat the repository as a work in progress rather than a citable benchmark dataset.
