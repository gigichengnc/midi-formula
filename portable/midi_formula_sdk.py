"""MIDI Formula — portable single-file AI Composer SDK.

Give this file to a coding AI together with a musical brief. The AI should write
a readable Python song script that imports this module and produces a rough,
editable Standard MIDI File for later refinement in Signal MIDI or another MIDI
editor.

No third-party packages are required. MIDI serialization, harmony helpers,
section primitives, rough accompaniment patterns, and structural validation all
live in this file.

Composer rule: generate a coherent 60–85% MIDI draft; do not try to replace the
human editing stage.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
import struct
from typing import Iterable

PPQ = 480

AI_COMPOSER_CONTRACT = r"""
You are writing a rough, editable MIDI draft, not a finished audio master.
A human will open the resulting .mid in Signal MIDI or another MIDI editor and
refine notes, transitions, velocities, lengths, instrumentation and arrangement.

Rules:
- Use this existing SDK; do not rewrite MIDI serialization.
- Use ordinary Python only; do not add mido, music21 or DAW plugins.
- Keep tempo, form, harmony, section starts and major intensity decisions readable.
- Create separate named tracks for musically distinct roles.
- Prefer reusable patterns over hundreds of unexplained raw note calls.
- Make transitions explicit in code.
- Save one .mid file as the result.
- Treat the MIDI as a 60–85% draft for human editing, not a final master.

A useful song script normally declares:
1. tempo and meter;
2. FORM using Section objects;
3. harmony/chord material;
4. named tracks with explicit channels and GM programs;
5. section-by-section patterns and transition rules;
6. song.save(...).

Quality target:
- coherent form;
- sensible note ranges;
- recognizable melody/harmony roles;
- audible section contrast;
- an editable transition;
- valid MIDI with no stuck notes.
""".strip()


def _vlq(value: int) -> bytes:
    if value < 0:
        raise ValueError("VLQ cannot encode a negative value")
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    return bytes(reversed(out))


def _chunk(kind: bytes, payload: bytes) -> bytes:
    return kind + struct.pack(">I", len(payload)) + payload


def _tempo_event(bpm: float) -> bytes:
    micros = int(round(60_000_000 / bpm))
    return b"\xff\x51\x03" + micros.to_bytes(3, "big")


def _time_signature_event(numer: int, denom: int) -> bytes:
    power = 0
    d = denom
    while d > 1 and d % 2 == 0:
        d //= 2
        power += 1
    if d != 1:
        raise ValueError("MIDI time-signature denominator must be a power of two")
    return bytes([0xFF, 0x58, 0x04, numer, power, 24, 8])


@dataclass(order=True)
class Event:
    tick: int
    priority: int
    data: bytes = field(compare=False)


class Track:
    """A named MIDI track with one channel and optional GM program."""

    def __init__(self, name: str, channel: int, program: int | None = None):
        if not 0 <= channel <= 15:
            raise ValueError("channel must be 0..15")
        if program is not None and not 0 <= program <= 127:
            raise ValueError("program must be 0..127")
        self.name = name
        self.channel = channel
        self.program = program
        self.events: list[Event] = []
        encoded = name.encode("utf-8")
        self.events.append(Event(0, 0, b"\xff\x03" + _vlq(len(encoded)) + encoded))
        if program is not None:
            self.events.append(Event(0, 1, bytes([0xC0 | channel, program])))

    def note(self, beat: float, duration: float, pitch: int, velocity: int = 80) -> None:
        if duration <= 0:
            raise ValueError("duration must be positive")
        if not 0 <= pitch <= 127:
            raise ValueError("pitch must be 0..127")
        velocity = max(1, min(127, int(round(velocity))))
        start = max(0, int(round(beat * PPQ)))
        end = max(start + 1, int(round((beat + duration) * PPQ)))
        self.events.append(Event(start, 2, bytes([0x90 | self.channel, pitch, velocity])))
        self.events.append(Event(end, 0, bytes([0x80 | self.channel, pitch, 0])))

    def chord(self, beat: float, duration: float, pitches: Iterable[int], velocity: int = 72) -> None:
        for pitch in pitches:
            self.note(beat, duration, int(pitch), velocity)

    def cc(self, beat: float, controller: int, value: int) -> None:
        if not 0 <= controller <= 127:
            raise ValueError("controller must be 0..127")
        value = max(0, min(127, int(round(value))))
        tick = max(0, int(round(beat * PPQ)))
        self.events.append(Event(tick, 1, bytes([0xB0 | self.channel, controller, value])))

    def cc_ramp(self, beat0: float, beat1: float, controller: int,
                value0: float, value1: float, steps: int = 8) -> None:
        if steps < 1:
            raise ValueError("steps must be >= 1")
        for i in range(steps + 1):
            f = i / steps
            self.cc(
                beat0 + (beat1 - beat0) * f,
                controller,
                round(value0 + (value1 - value0) * f),
            )

    def pedal(self, beat: float, duration: float) -> None:
        self.cc(beat, 64, 127)
        self.cc(beat + duration, 64, 0)

    def _render(self) -> bytes:
        payload = bytearray()
        last_tick = 0
        for event in sorted(self.events):
            payload.extend(_vlq(event.tick - last_tick))
            payload.extend(event.data)
            last_tick = event.tick
        payload.extend(b"\x00\xff\x2f\x00")
        return _chunk(b"MTrk", bytes(payload))


class Song:
    """A Type-1 Standard MIDI File composition."""

    def __init__(self, title: str, bpm: float = 100.0, numerator: int = 4,
                 denominator: int = 4):
        if bpm <= 0:
            raise ValueError("bpm must be positive")
        self.title = title
        self.bpm = float(bpm)
        self.numerator = numerator
        self.denominator = denominator
        self.tracks: list[Track] = []

    def add_track(self, name: str, channel: int, program: int | None = None) -> Track:
        track = Track(name, channel, program)
        self.tracks.append(track)
        return track

    def _meta_track(self) -> bytes:
        name = self.title.encode("utf-8")
        payload = bytearray()
        payload.extend(b"\x00\xff\x03" + _vlq(len(name)) + name)
        payload.extend(b"\x00" + _tempo_event(self.bpm))
        payload.extend(b"\x00" + _time_signature_event(self.numerator, self.denominator))
        payload.extend(b"\x00\xff\x2f\x00")
        return _chunk(b"MTrk", bytes(payload))

    def to_bytes(self) -> bytes:
        ntracks = 1 + len(self.tracks)
        header = b"MThd" + struct.pack(">IHHH", 6, 1, ntracks, PPQ)
        return header + self._meta_track() + b"".join(t._render() for t in self.tracks)

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.to_bytes())
        return path


PC = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4,
    "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9,
    "A#": 10, "Bb": 10, "B": 11,
}

QUALITIES = {
    "": (0, 4, 7),
    "m": (0, 3, 7),
    "7": (0, 4, 7, 10),
    "maj7": (0, 4, 7, 11),
    "m7": (0, 3, 7, 10),
    "sus2": (0, 2, 7),
    "sus4": (0, 5, 7),
    "add9": (0, 4, 7, 14),
    "madd9": (0, 3, 7, 14),
}


def note_number(name: str) -> int:
    split = 2 if len(name) > 2 and name[1] in "#b" else 1
    pc = PC[name[:split]]
    octave = int(name[split:])
    return 12 * (octave + 1) + pc


def chord(symbol: str, octave: int = 4) -> list[int]:
    split = 2 if len(symbol) > 1 and symbol[1] in "#b" else 1
    root = symbol[:split]
    quality = symbol[split:]
    if quality not in QUALITIES:
        raise ValueError(f"unsupported chord quality: {symbol}")
    base = 12 * (octave + 1) + PC[root]
    return [base + interval for interval in QUALITIES[quality]]


def progression(text: str, octave: int = 4) -> list[list[int]]:
    return [chord(s.strip(), octave) for s in text.split("|") if s.strip()]


@dataclass(frozen=True)
class Section:
    name: str
    bars: int
    energy: float = 1.0
    note: str = ""


def starts(sections: list[Section]) -> dict[str, int]:
    bar = 0
    out: dict[str, int] = {}
    for section in sections:
        out[section.name] = bar
        bar += section.bars
    return out


def total_bars(sections: list[Section]) -> int:
    return sum(s.bars for s in sections)


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
        second_beat = min(2, max(1, beats_per_bar // 2))
        track.note(beat + second_beat, max(0.5, beats_per_bar - second_beat - 0.4), root + 7,
                   max(1, velocity - 5))


def rising_transition(track: Track, start_bar: int, chords: Sequence[Sequence[int]],
                      bars: int = 2, velocity0: int = 50, velocity1: int = 78,
                      beats_per_bar: int = 4) -> None:
    total_steps = bars * beats_per_bar * 2
    for step in range(total_steps):
        f = step / max(1, total_steps - 1)
        bar = start_bar + step // (beats_per_bar * 2)
        chord_notes = chords[(bar - start_bar) % len(chords)]
        pitch = chord_notes[step % len(chord_notes)] + 12
        track.note(
            start_bar * beats_per_bar + step * 0.5,
            0.42,
            pitch,
            round(velocity0 + (velocity1 - velocity0) * f),
        )


def validate_midi(path: str | Path) -> dict[str, int]:
    """Perform lightweight structural validation of an SMF file.

    Returns format, track count, PPQ and byte size. This does not attempt full
    semantic MIDI parsing; it verifies the header and declared track chunks.
    """
    path = Path(path)
    data = path.read_bytes()
    if len(data) < 14 or data[:4] != b"MThd":
        raise ValueError("not a Standard MIDI File: missing MThd")
    header_len, fmt, ntracks, division = struct.unpack(">IHHH", data[4:14])
    if header_len != 6:
        raise ValueError(f"unexpected MIDI header length: {header_len}")
    if fmt not in (0, 1):
        raise ValueError(f"unsupported MIDI format: {fmt}")
    if division & 0x8000:
        raise ValueError("SMPTE time division is not supported by this SDK")
    found = data.count(b"MTrk")
    if found != ntracks:
        raise ValueError(f"declared {ntracks} tracks but found {found} MTrk chunks")
    return {"format": fmt, "tracks": ntracks, "ppq": division, "bytes": len(data)}


__all__ = [
    "AI_COMPOSER_CONTRACT",
    "PPQ",
    "Song",
    "Track",
    "Section",
    "note_number",
    "chord",
    "progression",
    "starts",
    "total_bars",
    "block_chords",
    "eighth_arpeggio",
    "bass_roots",
    "rising_transition",
    "validate_midi",
]
