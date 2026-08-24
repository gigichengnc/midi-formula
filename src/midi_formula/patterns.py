"""Reusable rough-draft accompaniment patterns.

These helpers deliberately stay simple. The generated MIDI is intended to be
refined later in Signal or another MIDI editor.
"""
from __future__ import annotations
from collections.abc import Sequence
from .midi import Track


def block_chords(track: Track, bar0: int, chords: Sequence[Sequence[int]],
                 bars: int, beats_per_bar: int = 4, velocity: int = 62,
                 octave_shift: int = 0) -> None:
    for i in range(bars):
        pitches = [p + 12 * octave_shift for p in chords[i % len(chords)]]
        track.chord((bar0 + i) * beats_per_bar, beats_per_bar * 0.92, pitches, velocity)


def eighth_arpeggio(track: Track, bar0: int, chords: Sequence[Sequence[int]],
                    bars: int, beats_per_bar: int = 4, velocity: int = 58,
                    octave_shift: int = 0) -> None:
    for i in range(bars):
        pitches = [p + 12 * octave_shift for p in chords[i % len(chords)]]
        order = list(range(len(pitches))) + list(range(max(0, len(pitches) - 2), 0, -1))
        if not order:
            continue
        for step in range(beats_per_bar * 2):
            pitch = pitches[order[step % len(order)]]
            track.note((bar0 + i) * beats_per_bar + step * 0.5, 0.46, pitch, velocity)


def bass_roots(track: Track, bar0: int, chords: Sequence[Sequence[int]],
               bars: int, beats_per_bar: int = 4, velocity: int = 58) -> None:
    for i in range(bars):
        root = chords[i % len(chords)][0] - 24
        beat = (bar0 + i) * beats_per_bar
        track.note(beat, 1.8, root, velocity)
        track.note(beat + 2, 1.6, root + 7, max(1, velocity - 5))


def rising_transition(track: Track, start_bar: int, chords: Sequence[Sequence[int]],
                      bars: int = 2, velocity0: int = 50, velocity1: int = 78,
                      beats_per_bar: int = 4) -> None:
    total_steps = bars * beats_per_bar * 2
    for step in range(total_steps):
        f = step / max(1, total_steps - 1)
        bar = start_bar + step // (beats_per_bar * 2)
        chord_notes = chords[(bar - start_bar) % len(chords)]
        pitch = chord_notes[step % len(chord_notes)] + 12
        track.note(start_bar * beats_per_bar + step * 0.5, 0.42, pitch,
                   round(velocity0 + (velocity1 - velocity0) * f))
