# Dreaming to Dream — Reference Strategy Pilot

## Goal

Test whether a copyrighted reference family can be used only to extract **abstract composition strategy**, then generate a new editable MIDI composition without transcribing or copying the reference melody.

## Reference analysis

Source analysed locally: `Doraemon movie best sad soundtrack` (AM Hafidz Vibes), 15:42.816.

The source audio itself is **not included** in this repository.

Automatic segmentation found seven principal musical cues plus trailing silence. Snapped boundaries:

| Cue | Start | End | Duration |
|---|---:|---:|---:|
| 1 | 0:00.00 | 1:26.47 | 86.47 s |
| 2 | 1:26.47 | 3:57.77 | 151.30 s |
| 3 | 3:57.77 | 5:53.31 | 115.54 s |
| 4 | 5:53.31 | 7:55.78 | 122.46 s |
| 5 | 7:55.78 | 8:45.10 | 49.32 s |
| 6 | 8:45.10 | 11:30.00 | 164.91 s |
| 7 | 11:30.00 | 15:36.42 | 246.41 s |

Approximate cue-level tonal estimates included F major, Bb major, E minor/C major, D major/B minor, and A minor/A major regions. Surface tempo estimates clustered around ~108 and ~162 BPM, supporting a useful design principle: **faster surface motion over a slower emotional pulse**.

These estimates are deliberately treated as approximate because the source is polyphonic orchestral audio and a compilation.

## Extracted strategy

The profile is named **Dreaming to Dream**. Its main rules are:

- warm-major tonal home with relative-minor shadow;
- 6/8 rocking pulse;
- two-bar singable motif;
- mostly stepwise motion;
- state → repeat → mutate → answer → recombine;
- one chord per bar most of the time;
- sparse piano/bell opening;
- woodwind answer in the middle;
- delayed string entry;
- emotional peak through density/register expansion rather than impact hits;
- ending returns to the opening identity in a thinner texture;
- strong tonic closure is delayed; final harmony keeps add-tone colour.

## Generated piece

`songs/dreaming_to_dream.py` creates a new 48-bar piece at MIDI quarter-note BPM 96 in 6/8. Because 6/8 contains 3 quarter-note units per bar, the resulting duration is approximately 90 seconds.

Form:

1. First Light — 8 bars
2. Curious Corridor — 12 bars
3. Memory Room — 8 bars
4. Window Opens — 4 bars
5. Dream Within a Dream — 12 bars
6. Afterglow — 4 bars

Track roles:

- Piano Lantern — Acoustic Grand Piano
- Dream Bells — Celesta
- Woodwind Answer — Flute
- Soft Bass — Acoustic Bass
- Late Strings — String Ensemble 1
- Soft Pulse — GM percussion

A local prototype rendered as valid Type-1 MIDI with PPQ 480, seven tracks including the meta track, approximately 89.875 seconds duration, and 735 paired note-on/note-off events. The generated MIDI is deliberately not committed yet; it should first be listened to and edited as pilot evidence.

## Copyright / research boundary

This pilot does **not** store a note-level transcription of the reference recording and does not attempt to reproduce a specific Doraemon melody or chord sequence. The reference is used to derive high-level musical properties such as density, tonal contrast, phrase strategy, instrumentation roles, and emotional arc.

Exact cue identities inside the YouTube compilation are not asserted here because the accessible video description does not provide a timestamped track list, and duration matching alone is insufficient evidence.
