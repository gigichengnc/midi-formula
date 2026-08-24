# -*- coding: utf-8 -*-
"""
《甜空氣標本》MIDI 核心程式庫（v2 · 演奏表情版）

相對於初版的升級：
  · 樂句級力度弧線（phrase arch）——樂句中段推上去，收尾放掉
  · 拍點層級的輕重（強拍重、弱拍輕），不再整段同一個力度
  · 有方向的微時值——旋律稍微落後拍點（表情），左手穩住
  · 依音程決定連奏程度——級進黏、大跳斷
  · 踏板跟著和聲換，不是每小節硬切
  · CC11 表情曲線，讓襯底有呼吸
"""
import struct, random, math

PPQ = 480

PC = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "Fb": 4,
      "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9,
      "A#": 10, "Bb": 10, "B": 11, "Cb": 11}

QUAL = {
    "": [0, 4, 7], "m": [0, 3, 7], "dim": [0, 3, 6], "aug": [0, 4, 8],
    "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11], "m7": [0, 3, 7, 10],
    "m7b5": [0, 3, 6, 10], "6": [0, 4, 7, 9], "m6": [0, 3, 7, 9],
    "add9": [0, 4, 7, 14], "madd9": [0, 3, 7, 14], "sus4": [0, 5, 7],
    "madd11": [0, 3, 7, 17], "m6add9": [0, 3, 7, 9, 14],
    "sus2": [0, 2, 7], "7sus4": [0, 5, 7, 10], "add11": [0, 4, 7, 17],
    "m9": [0, 3, 7, 10, 14], "9": [0, 4, 7, 10, 14],
    "maj9": [0, 4, 7, 11, 14], "m11": [0, 3, 7, 10, 14, 17],
}

# 各 GM 音色的合理音域（品管用）
GM_RANGE = {
    0: (21, 108), 8: (60, 108), 10: (60, 105), 12: (45, 96), 24: (40, 88),
    41: (48, 88), 42: (36, 76), 45: (36, 88), 49: (36, 96), 54: (48, 84),
    71: (50, 91), 73: (60, 96), 88: (36, 96), 92: (36, 96),
}


def nm(s):
    """'Ab4' -> midi number"""
    i = 2 if len(s) > 2 and s[1] in "b#" else 1
    return 12 * (int(s[i:]) + 1) + PC[s[:i]]


class Chord:
    """根音位置和弦（C3=48 起算）＋ 低音"""

    def __init__(self, sym):
        bass_sym = None
        if "/" in sym:
            sym, bass_sym = sym.split("/")
        i = 2 if len(sym) > 1 and sym[1] in "b#" else 1
        root, q = sym[:i], sym[i:]
        if q not in QUAL:
            raise ValueError("unknown chord quality: " + sym)
        self.sym = sym + ("/" + bass_sym if bass_sym else "")
        self.root_pc = PC[root]
        self.tones = [48 + self.root_pc + x for x in QUAL[q]]
        bpc = PC[bass_sym] if bass_sym else self.root_pc
        self.bass = 36 + bpc
        if self.bass > 45:
            self.bass -= 12

    def near(self, target=62, n=3):
        pool = sorted({t + o for t in self.tones for o in (-12, 0, 12, 24)})
        pool = [p for p in pool if 45 <= p <= 88]
        pool.sort(key=lambda p: abs(p - target))
        return sorted(pool[:n])

    def up(self, k=1):
        return [t + 12 * k for t in self.tones]

    def fold(self, lo, hi, n=4):
        """摺進固定音域窗，永遠上行（閃光琶音專用）"""
        out = []
        for t in self.tones:
            p = t
            while p < lo:
                p += 12
            while p > hi:
                p -= 12
            if lo <= p <= hi:
                out.append(p)
        out = sorted(set(out))
        while len(out) < n:
            out.append(out[0] + 12)
        return out[:n]


def prog(text):
    return [Chord(s.strip()) for s in text.replace("\n", "|").split("|")
            if s.strip()]


def parse_mel(text, bar_beats, bar0=0):
    """
    mini-notation:  b12  r0.5 F4:1 Eb4:1 Db4:2
    回傳 [(絕對拍, 長度, pitch, 力度比例)]
    """
    out = []
    for line in text.strip().splitlines():
        tok = line.split()
        if not tok or not tok[0].startswith("b"):
            continue
        bar = int(tok[0][1:]) + bar0
        cur = bar * bar_beats
        for t in tok[1:]:
            if t.startswith("r"):
                cur += float(t[1:])
                continue
            vel = 1.0
            if "@" in t:
                t, v = t.split("@")
                vel = float(v) / 100.0
            names, dur = t.rsplit(":", 1)
            dur = float(dur)
            for n in names.split("+"):
                out.append((cur, dur, nm(n), vel))
            cur += dur
    return out


# ───────────────────────── 演奏表情 ─────────────────────────
def phrase_arch(pos):
    """0..1 的樂句位置 → 力度倍率。中段推上去，收尾放掉。"""
    return 0.90 + 0.20 * math.sin(math.pi * min(max(pos, 0.0), 1.0)) \
        - 0.06 * max(0.0, pos - 0.82) / 0.18


def beat_weight(beat, bar_beats=4.0):
    """拍點輕重：強拍重、次強拍中、弱拍與切分輕"""
    b = beat % bar_beats
    if abs(b) < 0.05:
        return 1.00
    if bar_beats >= 4 and abs(b - 2) < 0.05:
        return 0.94
    if abs(b - round(b)) < 0.05:
        return 0.88
    return 0.80


class Track:
    def __init__(self, name, ch, program, jitter=6, lead=0):
        """
        jitter: 微時值抖動幅度（tick）
        lead:   系統性提前/落後（tick）。旋律用 +4~+8（略後＝有表情），
                低音用 0，打擊類用 -2。
        """
        self.ev, self.ch, self.jit, self.lead = [], ch, jitter, lead
        self.program = program
        b = name.encode("utf-8")
        self.name = name
        self.ev.append((0, 0, b"\xff\x03" + _vlq(len(b)) + b))
        self.ev.append((0, 0, bytes([0xC0 | ch, program])))
        self.rng = random.Random(sum(bytearray(b)) * 7919 + ch)

    def note(self, beat, dur, pitch, vel, jitter=None, legato=0.96):
        if not 0 <= pitch <= 127 or dur <= 0:
            return
        j = self.jit if jitter is None else jitter
        off = self.lead + (self.rng.randint(-j, j) if j else 0)
        v = max(1, min(127, int(round(vel + self.rng.uniform(-3, 3)))))
        s = max(0, int(beat * PPQ) + off)
        e = s + max(24, int(dur * PPQ * legato))
        self.ev.append((s, 1, bytes([0x90 | self.ch, pitch, v])))
        self.ev.append((e, 0, bytes([0x80 | self.ch, pitch, 0])))

    def pedal(self, beat, dur):
        self.ev.append((int(beat * PPQ) + 6, 2, bytes([0xB0 | self.ch, 64, 127])))
        self.ev.append((int((beat + dur) * PPQ) - 16, 0,
                        bytes([0xB0 | self.ch, 64, 0])))

    def cc(self, beat, num, val):
        self.ev.append((int(beat * PPQ), 2,
                        bytes([0xB0 | self.ch, num, max(0, min(127, int(val)))])))

    def cc_ramp(self, beat0, beat1, num, v0, v1, steps=8):
        """CC 漸變——讓襯底有呼吸，而不是一個死值"""
        for i in range(steps + 1):
            t = beat0 + (beat1 - beat0) * i / steps
            self.cc(t, num, v0 + (v1 - v0) * i / steps)

    def enforce_mono(self, gap=12):
        """
        保證同一時間只有一個音——SynthV 的硬性要求。
        表情功能（連奏 0.99、微時值偏移）會讓前一個音壓到下一個音上，
        這裡在寫檔前把所有重疊截掉。
        """
        ons, notes = {}, []
        for idx, (tick, prio, msg) in enumerate(self.ev):
            if len(msg) < 3:
                continue
            st = msg[0] & 0xF0
            if st == 0x90 and msg[2] > 0:
                ons.setdefault(msg[1], []).append((idx, tick))
            elif st == 0x80 or (st == 0x90 and msg[2] == 0):
                q = ons.get(msg[1])
                if q:
                    oidx, otick = q.pop(0)
                    notes.append([otick, tick, msg[1], oidx, idx])
        notes.sort(key=lambda n: n[0])
        fixed = 0
        for i in range(len(notes) - 1):
            nxt = notes[i + 1][0]
            if notes[i][1] > nxt - gap:
                notes[i][1] = max(notes[i][0] + 24, nxt - gap)
                fixed += 1
        ev = list(self.ev)
        for st, en, p, oidx, offidx in notes:
            tick, prio, msg = ev[offidx]
            ev[offidx] = (en, prio, msg)
        self.ev = ev
        return fixed

    def play(self, notes, base_vel=76, transpose=0, octave=0, gain=1.0,
             shape=True, bar_beats=4.0):
        """
        shape=True 時套用樂句弧線＋拍點輕重＋依音程決定連奏程度。
        notes 需為同一個樂句（mel_map 的一段），弧線以整段為範圍。
        """
        if not notes:
            return
        b0 = notes[0][0]
        span = max(1e-6, notes[-1][0] + notes[-1][1] - b0)
        prev_pitch = None
        for idx, (beat, dur, pitch, vs) in enumerate(notes):
            p = pitch + transpose + 12 * octave
            v = base_vel * vs * gain
            leg = 0.96
            if shape:
                v *= phrase_arch((beat - b0) / span) * beat_weight(beat, bar_beats)
                if prev_pitch is not None:
                    step = abs(p - prev_pitch)
                    leg = 0.99 if step <= 2 else (0.94 if step <= 4 else 0.88)
                if idx == len(notes) - 1:
                    leg = 0.99
            self.note(beat, dur, p, v, legato=leg)
            prev_pitch = p


def _vlq(n):
    b = [n & 0x7F]
    n >>= 7
    while n:
        b.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(b))


def _pack(events):
    events = sorted(events, key=lambda e: (e[0], e[1]))
    data, last = b"", 0
    for tick, _, msg in events:
        data += _vlq(tick - last) + msg
        last = tick
    return b"MTrk" + struct.pack(">I", len(data) + 4) + data + b"\x00\xff\x2f\x00"


def meta_track(title, tempos, sigs=((0, 4, 2),)):
    ev = []
    t = title.encode("utf-8")
    ev.append((0, 0, b"\xff\x03" + _vlq(len(t)) + t))
    for beat, bpm in tempos:
        ev.append((int(beat * PPQ), 0,
                   b"\xff\x51\x03" + struct.pack(">I", int(6e7 / bpm))[1:]))
    for beat, num, dp in sigs:
        ev.append((int(beat * PPQ), 0,
                   b"\xff\x58\x04" + bytes([num, dp, 24, 8])))
    return _pack(ev)


def save(path, meta, tracks):
    chunks = [meta] + [_pack(t.ev) for t in tracks]
    with open(path, "wb") as f:
        f.write(b"MThd" + struct.pack(">IHHH", 6, 1, len(chunks), PPQ)
                + b"".join(chunks))
    return path


def duration_sec(tempos, total_beats):
    tempos = sorted(tempos)
    s, prev_b, prev_bpm = 0.0, 0.0, tempos[0][1]
    for b, bpm in tempos[1:]:
        if b >= total_beats:
            break
        s += (b - prev_b) * 60.0 / prev_bpm
        prev_b, prev_bpm = b, bpm
    s += (total_beats - prev_b) * 60.0 / prev_bpm
    return s
