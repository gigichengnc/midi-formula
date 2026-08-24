"""Small harmony helpers designed for AI-written rough MIDI drafts."""
from __future__ import annotations

PC = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4,
      "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9,
      "A#": 10, "Bb": 10, "B": 11}
QUALITIES = {
    "": (0, 4, 7), "m": (0, 3, 7), "7": (0, 4, 7, 10),
    "maj7": (0, 4, 7, 11), "m7": (0, 3, 7, 10),
    "sus2": (0, 2, 7), "sus4": (0, 5, 7),
    "add9": (0, 4, 7, 14), "madd9": (0, 3, 7, 14),
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
