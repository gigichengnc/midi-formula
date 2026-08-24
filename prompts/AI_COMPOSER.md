# AI Composer Contract

You are writing a **rough, editable MIDI draft**, not a finished audio master.
The human will open the resulting `.mid` in Signal MIDI (or another MIDI editor)
and refine notes, transitions, velocities, lengths, instrumentation and arrangement.

## Use the repository as an SDK

- Import from `midi_formula` and `midi_formula.patterns`.
- Put new compositions in `songs/` or `examples/`.
- Create separate tracks for musically distinct roles.
- Keep the song form, harmony, section starts and major intensity decisions readable near the top of the file.
- Prefer reusable patterns over hundreds of unexplained raw note calls.
- Use comments to explain musical intent, especially transitions.

## Do not

- Rewrite `src/midi_formula/midi.py` for a new song.
- Add `mido`, `music21`, DAW plugins or other MIDI dependencies.
- Render MP3/WAV as part of composition.
- Hide the whole composition in one enormous literal note list when a pattern or section rule would be clearer.
- Treat the generated MIDI as final. It is a draft for human editing.

## Required output

A song script should:

1. declare tempo and form;
2. declare harmony or chord material;
3. create named tracks with explicit GM programs/channels;
4. make transitions explicit in code;
5. save one `.mid` under `output/`;
6. run with ordinary Python and no third-party packages.

## Recommended structure

```python
FORM = [
    Section("intro", 4, 0.55),
    Section("verse", 8, 0.75),
    Section("transition", 2, 0.90),
    Section("chorus", 8, 1.00),
]

HARMONY = "Dmaj7 | A | Bm7 | Gmaj7"

song = Song("...", bpm=92)
# create tracks
# write section-by-section rules
# explicitly write the transition rule
song.save("output/my_song.mid")
```

## Quality target

Aim for a musically coherent **60–85% draft**:

- useful form;
- sensible note ranges;
- recognizable melody/harmony roles;
- audible section contrast;
- a transition that can be heard and edited;
- no stuck notes or invalid MIDI.

Leave taste-level polishing to the human MIDI-editing stage.
