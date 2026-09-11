from midi_formula_sdk import Song, Section, note_number, starts, total_bars, validate_midi

TITLE = "Dreaming to Dream — Lonely Memory"
BPM = 54            # quarter-note BPM; in 6/8 this feels like dotted-quarter ≈ 36
BEATS_PER_BAR = 3.0 # SDK time unit is quarter notes
FORM = [
    Section("Distant Room", 4, 0.24, "air before the memory"),
    Section("A — Remembering", 8, 0.40, "flute tells the first sentence"),
    Section("B — Falling Inward", 8, 0.48, "piano and clarinet take over"),
    Section("C — Acceptance", 8, 0.58, "warmer answer, still restrained"),
    Section("Coda — Afterimage", 4, 0.25, "first idea returns almost alone"),
]
START = starts(FORM)

song = Song(TITLE, bpm=BPM, numerator=6, denominator=8)

flute    = song.add_track("Flute — Distant Memory", 0, 73)
clarinet = song.add_track("Clarinet — Inner Voice", 1, 71)
harp     = song.add_track("Harp — Memory Surface", 2, 46)
piano    = song.add_track("Piano — Inner Room", 3, 0)
violin   = song.add_track("Violin — Held Light", 4, 40)
cello    = song.add_track("Cello — Time Holder", 5, 42)

def n(name): return note_number(name)
def beat(bar, pos=0.0): return (bar * BEATS_PER_BAR) + pos

# Voice-led, manually voiced harmonic field. Each tuple is low->high.
VOICINGS = [
    [n("D3"), n("A3"), n("C#4"), n("F#4")],
    [n("C#3"), n("A3"), n("D4"), n("F#4")],
    [n("B2"), n("F#3"), n("A3"), n("D4")],
    [n("G2"), n("D3"), n("F#3"), n("B3")],
    [n("E3"), n("B3"), n("D4"), n("G4")],
    [n("A2"), n("E3"), n("G3"), n("C#4")],
]

def soft_harp_bar(bar_no, voicing, velocity=36, upward=True):
    """A short broken gesture, then air. Never fills the whole bar."""
    notes = voicing[1:] if upward else list(reversed(voicing[1:]))
    for i, pitch in enumerate(notes[:3]):
        harp.note(beat(bar_no, i * 0.5), 0.42, pitch + 12, velocity + i)
    harp.pedal(beat(bar_no), 2.2)

def piano_memory_bar(bar_no, voicing, velocity=43):
    """Bass has contour; right hand gives only a brief answer."""
    low = voicing[0]
    piano.note(beat(bar_no, 0.0), 0.72, low, velocity)
    piano.note(beat(bar_no, 0.75), 0.50, voicing[1], velocity - 2)
    piano.note(beat(bar_no, 1.50), 0.72, voicing[2], velocity)
    piano.chord(beat(bar_no, 2.25), 0.55, [voicing[2]+12, voicing[3]+12], velocity-4)
    piano.pedal(beat(bar_no), 2.65)

def held_field(bar_no, voicing, vv=26, cv=29, duration=2.85):
    violin.note(beat(bar_no), duration, voicing[-1] + 12, vv)
    cello.note(beat(bar_no), duration, voicing[0] - 12, cv)

def phrase(track, start_bar, events, base_velocity):
    """events = (bar_offset, beat_offset, note_name, duration, velocity_delta)"""
    for bo, po, name, dur, dv in events:
        track.note(beat(start_bar + bo, po), dur, n(name), base_velocity + dv)

# Distant Room — almost nothing happens. Harp and strings establish distance.
for i in range(4):
    v = VOICINGS[[0, 2, 3, 0][i]]
    if i in (0, 2):
        soft_harp_bar(i, v, 30 + i*2)
    held_field(i, v, 20, 24)

# Flute pickup at the very end of the room.
flute.note(beat(3, 2.0), 0.42, n("A4"), 42)
flute.note(beat(3, 2.5), 0.42, n("B4"), 45)

# A — Remembering
A0 = START["A — Remembering"]
A_phrase = [
    (0,0.0,"D5",1.40, 2), (0,1.5,"C#5",0.42,0), (0,2.0,"B4",0.42,-2),
    (1,0.0,"A4",0.92,-3), (1,1.25,"F#4",0.42,-4), (1,2.0,"A4",0.72,-2),
    (2,0.0,"B4",0.42,-1), (2,0.5,"D5",0.72,1), (2,1.5,"C#5",0.42,-1),
    (2,2.0,"A4",0.72,-3),
    (3,0.0,"F#4",1.35,-4), (3,1.75,"E4",0.42,-5),
]
phrase(flute, A0, A_phrase, 48)

# A' keeps rhythmic identity but changes destination/register.
A_prime = [
    (4,0.0,"D5",1.35,2), (4,1.5,"E5",0.42,0), (4,2.0,"F#5",0.42,1),
    (5,0.0,"E5",0.92,0), (5,1.25,"C#5",0.42,-2), (5,2.0,"B4",0.72,-3),
    (6,0.0,"A4",0.42,-2), (6,0.5,"B4",0.72,-1), (6,1.5,"D5",0.42,0),
    (6,2.0,"C#5",0.72,-2),
    (7,0.0,"B4",1.20,-3), (7,1.75,"A4",0.42,-4),
]
phrase(flute, A0, A_prime, 50)

for i in range(8):
    barno = A0 + i
    v = VOICINGS[[0,1,2,3,4,5,2,0][i]]
    if i not in (1, 5):
        soft_harp_bar(barno, v, 33 + (i%3))
    held_field(barno, v, 22 + (i//4)*2, 26 + (i//4)*2)

# B — Falling Inward
B0 = START["B — Falling Inward"]
for i in range(8):
    v = VOICINGS[[2,3,4,5,2,1,3,5][i]]
    piano_memory_bar(B0+i, v, 40 + (2 if i in (3,6) else 0))
    if i in (0,2,4,6):
        held_field(B0+i, v, 24, 28)

B_phrase = [
    (0,0.5,"F#4",0.72,-2), (0,1.5,"A4",0.72,0),
    (1,0.0,"B4",1.35,1), (1,1.75,"A4",0.42,-1),
    (2,0.0,"F#4",0.92,-2), (2,1.25,"E4",0.42,-3), (2,2.0,"D4",0.72,-4),
    (3,0.0,"E4",1.75,-2),
    (4,0.5,"F#4",0.42,-1), (4,1.0,"A4",0.72,0), (4,2.0,"B4",0.72,1),
    (5,0.0,"A4",1.35,-1), (5,1.75,"F#4",0.42,-2),
    (6,0.0,"E4",0.92,-3), (6,1.25,"F#4",0.42,-2), (6,2.0,"A4",0.72,-1),
    (7,0.0,"D4",2.20,-4),
]
phrase(clarinet, B0, B_phrase, 46)

# One brief glimmer near the end, not constant decoration.
for p, off in zip(["D5","E5","F#5"], [0.0,0.5,1.0]):
    harp.note(beat(B0+6, off), 0.38, n(p), 34)

# C — Acceptance; flute and clarinet answer each other rather than doubling.
C0 = START["C — Acceptance"]
C_flute = [
    (0,0.0,"A4",0.72,-1), (0,1.0,"B4",0.42,0), (0,1.5,"D5",1.20,2),
    (1,0.0,"C#5",0.92,0), (1,1.25,"B4",0.42,-1), (1,2.0,"A4",0.72,-2),
    (2,0.0,"F#4",0.72,-2), (2,1.0,"A4",0.72,-1), (2,2.0,"D5",0.72,1),
    (3,0.0,"E5",1.65,2),
    (4,0.0,"D5",0.92,1), (4,1.25,"C#5",0.42,0), (4,2.0,"B4",0.72,-1),
    (5,0.0,"A4",1.35,-2), (5,1.75,"F#4",0.42,-3),
    (6,0.0,"A4",0.72,-1), (6,1.0,"B4",0.42,0), (6,1.5,"D5",0.92,1),
    (7,0.0,"C#5",2.15,-1),
]
phrase(flute, C0, C_flute, 52)

C_cl = [
    (1,1.5,"F#4",0.92,-3), (2,0.5,"E4",0.92,-4),
    (3,1.0,"A4",1.20,-2), (4,0.5,"F#4",0.72,-3),
    (5,1.5,"E4",0.92,-4), (6,0.5,"F#4",0.72,-3),
    (7,1.25,"A4",1.25,-2),
]
phrase(clarinet, C0, C_cl, 44)

for i in range(8):
    v = VOICINGS[[3,0,2,4,3,5,2,0][i]]
    if i % 2 == 0:
        soft_harp_bar(C0+i, v, 35)
    else:
        piano_memory_bar(C0+i, v, 42)
    held_field(C0+i, v, 26 + (2 if i in (3,7) else 0), 30)

# Coda — Afterimage; remove most accompaniment and return a fragment.
D0 = START["Coda — Afterimage"]
for i, v in enumerate([VOICINGS[0], VOICINGS[2], VOICINGS[3], VOICINGS[0]]):
    held_field(D0+i, v, 18, 22, 2.85)
    if i in (0,2):
        soft_harp_bar(D0+i, v, 28)

coda = [
    (0,0.0,"D5",1.45,-2), (0,1.75,"C#5",0.42,-4),
    (1,0.0,"B4",1.15,-4), (1,1.5,"A4",0.72,-5),
    (2,0.0,"F#4",1.35,-6), (2,1.75,"E4",0.42,-7),
    (3,0.0,"D4",2.60,-8),
]
phrase(flute, D0, coda, 43)

# Expression curves: restrained, not cinematic.
flute.cc_ramp(beat(A0), beat(A0+7,2.5), 11, 52, 72, 12)
clarinet.cc_ramp(beat(B0), beat(B0+7,2.5), 11, 45, 62, 10)
violin.cc_ramp(0, beat(C0+7,2.5), 11, 32, 54, 16)
cello.cc_ramp(0, beat(C0+7,2.5), 11, 36, 56, 16)

out = song.save("dreaming_to_dream_lonely_memory.mid")
print("saved", out)
print("bars", total_bars(FORM))
print("approx_seconds", round(total_bars(FORM) * BEATS_PER_BAR * 60 / BPM, 1))
print("validation", validate_midi(out))
