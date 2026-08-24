# Case study: Opus 5 / A Collection of Sweet Air

The source snapshot in `original/opus5/` already produced the nine MIDI files under `original/opus5/album/`. The goal here is to make the program's generation logic easier to inspect.

| Formula layer | Explicit source evidence | Musical effect |
|---|---|---|
| Form | `src/formula.py: ROLE_GAIN`, `layout()`; `src/songs.py: P_*` | Sections have named roles and variable lengths. |
| Section dynamics | `ROLE_GAIN` | Intro/verse/lift/peak/sustain/break/end scale note velocity. |
| Piano LH | eight-note `pat` in `build()` | Bass/chord-tone arpeggiation with beat weighting. |
| Ding register | `Chord.fold(79, 96)` + `figure()` | Sparkle figures stay in a fixed high register. |
| Pad automation | `cc_ramp(... CC11 ...)` | Pads fade in, rise toward peak, then withdraw. |
| Phrase expression | `phrase_arch()` | Melody velocity rises through the phrase and relaxes near the end. |
| Meter emphasis | `beat_weight()` | Downbeat > secondary beat > ordinary beat > syncopation. |
| Microtiming | `Track(... jitter, lead)` | Melody can sit slightly late, accompaniment stable, percussive layers slightly early. |
| Legato | `Track.play()` interval test | Steps connect more than leaps. |
| Pedal | `pedal_groups()` | Sustain changes with harmony rather than blindly each bar. |
| Ending | `role == "end"` branch + tempo map | Ten-bar staged thinning, roll and ritardando. |

This table is deliberately limited to rules that are visible in the preserved source. The accompanying Bibles add human-readable intent but are kept distinct from executable evidence.
