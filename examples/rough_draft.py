"""Example: AI-style rough MIDI draft with an explicit transition.

Run from repository root:
    PYTHONPATH=src python examples/rough_draft.py
"""
from midi_formula import Song, Section, starts, progression, note_number
from midi_formula.patterns import block_chords, eighth_arpeggio, bass_roots, rising_transition

FORM = [
    Section("intro", 4, 0.55, "sparse piano"),
    Section("verse", 8, 0.72, "piano + bass"),
    Section("transition", 2, 0.90, "rising density and expression"),
    Section("chorus", 8, 1.00, "fuller harmony"),
    Section("outro", 4, 0.60, "strip back"),
]
S = starts(FORM)
HARMONY = progression("Dmaj7 | A | Bm7 | Gmaj7", octave=4)

song = Song("Rough Draft Example", bpm=92)
piano = song.add_track("Piano", channel=0, program=0)
bass = song.add_track("Bass", channel=1, program=32)
strings = song.add_track("Strings", channel=2, program=48)
lead = song.add_track("Lead", channel=3, program=10)

block_chords(piano, S["intro"], HARMONY, 4, velocity=48, octave_shift=-1)

eighth_arpeggio(piano, S["verse"], HARMONY, 8, velocity=58, octave_shift=-1)
bass_roots(bass, S["verse"], HARMONY, 8, velocity=54)

motif = [note_number(n) for n in ("F#5", "E5", "D5", "A4")]
for bar in range(S["verse"], S["verse"] + 8):
    root_beat = bar * 4
    for i, pitch in enumerate(motif):
        lead.note(root_beat + i, 0.82, pitch, 64 if i < 3 else 57)

# Explicit transition logic: rising note density plus CC11 expression ramps.
rising_transition(piano, S["transition"], HARMONY, bars=2, velocity0=52, velocity1=82)
piano.cc_ramp(S["transition"] * 4, (S["transition"] + 2) * 4, 11, 60, 104, steps=8)
strings.cc_ramp(S["transition"] * 4, (S["transition"] + 2) * 4, 11, 35, 82, steps=8)
block_chords(strings, S["transition"], HARMONY, 2, velocity=44)

eighth_arpeggio(piano, S["chorus"], HARMONY, 8, velocity=72, octave_shift=-1)
bass_roots(bass, S["chorus"], HARMONY, 8, velocity=64)
block_chords(strings, S["chorus"], HARMONY, 8, velocity=55)
for bar in range(S["chorus"], S["chorus"] + 8):
    root_beat = bar * 4
    for i, pitch in enumerate(motif):
        lead.note(root_beat + i, 0.88, pitch + (12 if bar % 4 == 3 else 0), 74)

block_chords(piano, S["outro"], HARMONY, 4, velocity=45, octave_shift=-1)
lead.note(S["outro"] * 4, 7.5, note_number("D5"), 52)

song.save("output/rough_draft.mid")
print("wrote output/rough_draft.mid")
