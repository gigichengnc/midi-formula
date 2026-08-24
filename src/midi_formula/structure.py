"""Human-readable song-structure primitives."""
from __future__ import annotations
from dataclasses import dataclass


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
