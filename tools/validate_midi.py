#!/usr/bin/env python3
"""Small structural validator for Standard MIDI Files produced by MIDI Formula."""
from __future__ import annotations
import argparse
import struct
from pathlib import Path


def inspect(path: Path) -> dict[str, int]:
    data = path.read_bytes()
    if len(data) < 14 or data[:4] != b"MThd":
        raise ValueError("missing MThd header")
    header_len, fmt, tracks, division = struct.unpack(">IHHH", data[4:14])
    if header_len != 6:
        raise ValueError(f"unexpected MIDI header length: {header_len}")
    pos = 8 + header_len
    seen = 0
    while pos + 8 <= len(data):
        kind = data[pos:pos+4]
        length = struct.unpack(">I", data[pos+4:pos+8])[0]
        pos += 8
        if pos + length > len(data):
            raise ValueError("chunk length exceeds file size")
        if kind == b"MTrk":
            seen += 1
        pos += length
    if pos != len(data):
        raise ValueError("trailing or truncated bytes")
    if seen != tracks:
        raise ValueError(f"header says {tracks} tracks but file contains {seen}")
    return {"format": fmt, "tracks": tracks, "ppq": division, "bytes": len(data)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    print(inspect(args.path))


if __name__ == "__main__":
    main()
