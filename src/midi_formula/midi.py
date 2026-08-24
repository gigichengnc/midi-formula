"""Tiny zero-dependency Standard MIDI File writer.

Song-generating AIs should compose with the public API and should not rewrite
MIDI serialization for each song.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import struct
from pathlib import Path
from typing import Iterable

PPQ = 480


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
            self.cc(beat0 + (beat1 - beat0) * f, controller,
                    round(value0 + (value1 - value0) * f))

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
