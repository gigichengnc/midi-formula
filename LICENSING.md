# Licensing

MIDI Formula uses a split-licensing policy so that reusable software, research documentation, and the original creative case study are not accidentally treated as the same kind of material.

## 1. Software — Apache License 2.0

Copyright 2026 Gigi Cheng.

The following project software is licensed under the Apache License, Version 2.0 (`Apache-2.0`):

- `portable/**`
- `src/**`
- `tools/**`
- `tests/**`
- `examples/**`
- `.github/**`
- `pyproject.toml`

The full Apache-2.0 text is in [`LICENSE`](LICENSE).

This license is intended to let others inspect, run, modify, test, and redistribute the reusable SDK and supporting software while preserving the normal Apache-2.0 attribution and notice requirements.

## 2. Research and project documentation — CC BY 4.0

Unless a file is specifically excluded below, original MIDI Formula documentation is licensed under the Creative Commons Attribution 4.0 International license (`CC BY 4.0`):

- `README.md`
- `RESEARCH_PREVIEW.md`
- `FACULTY_NOTE.md`
- `docs/**`
- `prompts/**`
- `AGENTS.md`
- small project-orientation README files outside the excluded case-study directories

License: https://creativecommons.org/licenses/by/4.0/

When reusing this material, please attribute **Gigi Cheng / MIDI Formula**, link to the repository when practical, identify the CC BY 4.0 license, and indicate material changes.

The CC license applies to the documentation text and project-authored explanatory material only. It does **not** automatically license underlying music, lyrics, compositions, third-party material, model-provider content, or other excluded material merely because such material is described or quoted in the documentation.

## 3. Original creative case study — excluded from the open licenses

The following material is intentionally **not** covered by the Apache-2.0 or CC BY 4.0 grants above unless a file later states otherwise:

- `original/opus5/**`
- `formula/**` where the content is extracted from or derived from the Opus 5 composition project
- original compositions, melodies, lyrics, arrangement data, MIDI files, audio files, artwork, and other creative assets from the Opus 5 case study

For these materials, this repository grants no additional reuse permission beyond rights that already apply under law or the GitHub Terms of Service. Public visibility is for inspection, provenance, reproducibility discussion, and research review; it should not be read as a general open-content license for the underlying creative work.

## 4. Evidence and future research data

Factual hashes, file sizes, validation results, and similar non-creative metadata may be reproduced as facts. However, future benchmark datasets, model outputs, human-participant data, and evaluation exports are **not automatically licensed by this document**. Their release terms should be decided separately after methodology, provider terms, consent, privacy, and research-ethics requirements are clear.

## 5. Third-party material

Any third-party material remains subject to its own license or terms. Nothing in this repository grants rights that the maintainer is not authorized to grant.

## Why the split exists

The software needs an established open-source software license. Creative Commons itself recommends using software-specific licenses for software, while CC BY 4.0 is appropriate for separate documentation and research-facing explanatory material. The original musical case study is kept outside both grants so that publishing the code does not unintentionally open-license the underlying creative work.

If a future publication or archival release needs a different data/content license, that should be added explicitly at the relevant file or directory level rather than silently changing the scope of these existing grants.
