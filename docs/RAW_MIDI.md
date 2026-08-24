# Raw MIDI byte layer

The first MIDI Formula case study does not rely on a third-party MIDI-writing package. `original/opus5/src/midilib.py` writes a Standard MIDI File directly with Python standard-library byte operations.

## File structure

The writer emits a format-1 SMF header:

```python
b"MThd" + struct.pack(">IHHH", 6, 1, len(chunks), PPQ)
```

Each track is encoded as:

```python
b"MTrk" + struct.pack(">I", len(data) + 4) + data + b"\x00\xff\x2f\x00"
```

Event times are converted to delta times and encoded with `_vlq()` (MIDI variable-length quantities).

## Explicit event types in the source

- Note On: `0x90 | channel`
- Note Off: `0x80 | channel`
- Program Change: `0xC0 | channel`
- Control Change: `0xB0 | channel`
- Track name meta-event: `FF 03`
- Tempo meta-event: `FF 51 03`
- Time-signature meta-event: `FF 58 04`
- End of track: `FF 2F 00`

`PPQ = 480` maps musical beats into MIDI ticks.

## Why this matters to MIDI Formula

The project's target is not merely an editable MIDI file. The useful layer is the explicit path:

```text
section / harmony / expression rule
        ↓
Python event construction
        ↓
absolute tick events
        ↓
delta-time + MIDI message encoding
        ↓
MThd / MTrk bytes
        ↓
.mid
```

Because this path is source-visible, a person can inspect where a musical decision enters the generated artifact. Signal or another MIDI editor can then open the already-generated `.mid`, but the generation logic remains separately visible and editable upstream.

This does not reveal a model's hidden chain of thought. It documents the executable program the model wrote.
