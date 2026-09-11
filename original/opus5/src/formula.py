# -*- coding: utf-8 -*-
"""
《甜空氣標本》編曲配方（v3 · 可變曲式）

v2 的問題：九首共用寫死的 62 小節骨架，連續聽 30 分鐘會察覺形式重複。
v3 改成「段落計畫」——每首自己決定段落與長度，但共用同一套語言與收尾規則。

段落計畫格式：[(段落名, 小節數, 角色), ...]
角色決定織體密度與動態：
  intro   前奏，前兩小節只踩四分
  verse   標準織體
  lift    加密閃光層
  peak    全曲最強
  sustain 高原，略低於 peak
  break   幾乎全停，只剩長和弦（03 的中段留白）
  end     固定 10 小節收尾
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from midilib import (Track, prog, parse_mel, meta_track, save, duration_sec,
                     nm, beat_weight)

BB = 4.0

ROLE_GAIN = {"intro": 0.78, "verse": 0.94, "lift": 1.00, "peak": 1.10,
             "sustain": 1.03, "break": 0.68, "end": 0.90}

PLAN_INSTRUMENTAL = [("intro", 4, "intro"), ("A", 8, "verse"),
                     ("A2", 8, "lift"), ("B", 16, "peak"),
                     ("A3", 16, "sustain"), ("end", 10, "end")]

PLAN_VOCAL = [("intro", 4, "intro"), ("V1", 8, "verse"), ("Ch1", 8, "lift"),
              ("V2", 8, "verse"), ("Ch2", 8, "peak"), ("Br", 8, "sustain"),
              ("Ch3", 8, "lift"), ("end", 10, "end")]


def layout(plan):
    """回傳 (段落起始小節 dict, 角色 dict, 總小節數)"""
    starts, roles, bar = {}, {}, 0
    for name, n, role in plan:
        starts[name] = bar
        for b in range(bar, bar + n):
            roles[b] = role
        bar += n
    return starts, roles, bar


def chords_from_plan(plan, a_ch, b_ch, end_ch):
    """沒有給 chord_list 時，依計畫鋪和弦"""
    A, B, E = prog(a_ch), prog(b_ch), prog(end_ch)
    out = []
    for name, n, role in plan:
        if role == "end":
            assert len(E) == n, f"收尾和弦要 {n} 小節，給了 {len(E)}"
            out += E
        elif role == "peak":
            out += [B[i % len(B)] for i in range(n)]
        else:
            out += [A[i % len(A)] for i in range(n)]
    return out


def figure(tr, b0, fig, at, vel):
    for j in range(4):
        tr.note(b0 + at + j * .25, .3, fig[j],
                vel * (1.0 if j == 0 else 0.84 - j * 0.04))


def pedal_groups(P, end_bar):
    groups, start = [], 0
    for i in range(1, len(P) + 1):
        if i == len(P) or P[i].sym != P[start].sym or i >= end_bar:
            groups.append((start, i))
            start = i
    return groups


def build(path, title, bpm=82, roll_low="D2", roll_minor=False,
          a_ch=None, b_ch=None, end_ch=None,
          a_mel=None, b_mel=None, end_mel=None,
          chord_list=None, mel_map=None, vocal=False, extra_tracks=None,
          plan=None):
    plan = plan or (PLAN_VOCAL if vocal else PLAN_INSTRUMENTAL)
    starts, roles, nbars = layout(plan)
    end_bar = starts["end"]

    P = prog(chord_list) if chord_list else \
        chords_from_plan(plan, a_ch, b_ch, end_ch)
    assert len(P) == nbars, f"{title}: 需要 {nbars} 小節和弦，給了 {len(P)}"

    if vocal:
        voc = Track("1 VOCAL guide (Synth V)", 0, 54, jitter=3, lead=2)
        box = Track("2 Music Box (instrumental)", 1, 10, jitter=5, lead=4)
        pmel = Track("3 Piano melody (body)", 2, 0, jitter=6, lead=5)
        lh = Track("4 Piano LH", 3, 0, jitter=3, lead=0)
        d1 = Track("5a Ding CORE", 4, 8, jitter=3, lead=-2)
        d2 = Track("5b Ding EXTRA (mute me)", 5, 8, jitter=3, lead=-2)
        p1 = Track("6 Pad mid LONG", 6, 88, jitter=0)
        p2 = Track("7 Pad high LONG", 7, 88, jitter=0)
        heads = [voc, box, pmel]
    else:
        voc = None
        box = Track("1 Music Box MELODY", 0, 10, jitter=5, lead=4)
        pmel = Track("2 Piano melody (body)", 1, 0, jitter=6, lead=6)
        lh = Track("3 Piano LH", 2, 0, jitter=3, lead=0)
        d1 = Track("4a Ding CORE", 3, 8, jitter=3, lead=-2)
        d2 = Track("4b Ding EXTRA (mute me)", 4, 8, jitter=3, lead=-2)
        p1 = Track("5 Pad mid LONG", 5, 88, jitter=0)
        p2 = Track("6 Pad high LONG", 6, 88, jitter=0)
        heads = [box, pmel]

    pad_in = plan[2][1] and starts[plan[2][0]]
    pad_out = end_bar - 2

    for s, e in pedal_groups(P, end_bar):
        if s < end_bar:
            lh.pedal(s * BB, (e - s) * BB)

    for bar, c in enumerate(P):
        b0, role = bar * BB, roles[bar]
        g = ROLE_GAIN[role]
        n = c.near(58, 3)
        fig = c.fold(79, 96)

        if role == "break":
            if (bar - starts.get("break", bar)) % 2 == 0:
                for t in [c.bass] + c.near(60, 3):
                    lh.note(b0, 7.6, t, 32 * g)
                lh.pedal(b0, 8)
            continue

        if role != "end":
            pat = [c.bass, n[0], n[1], n[2], c.bass + 12, n[0], n[1], n[2]]
            for i, beat in enumerate([j * .5 for j in range(8)]):
                if role == "intro" and bar < 2 and i % 2:
                    continue
                base = 54 if i in (0, 4) else 38
                push = 1.0 + 0.05 * (i / 7.0)
                lh.note(b0 + beat, .55, pat[i],
                        base * g * push * beat_weight(beat, BB) * 1.08)
            figure(d1, b0, fig, 3.0, 32 * g)
            if role in ("lift", "peak", "sustain"):
                figure(d2, b0, fig, 1.0, 26 * g)
                figure(d2, b0, fig, 2.0, 24 * g)
            if pad_in <= bar < end_bar:
                for t in c.near(62, 3):
                    p1.note(b0, 3.9, t, 26 * g, jitter=0)
            if pad_in + 4 <= bar < pad_out:
                p2.note(b0, 3.9, fig[0], 22 * g, jitter=0)
                p2.note(b0, 3.9, fig[2], 20 * g, jitter=0)
            continue

        i_out = bar - end_bar
        if i_out <= 3:
            fade = [1.0, .88, .78, .68][i_out]
            pat = [c.bass, n[0], n[1], n[2], c.bass + 12, n[0], n[1], n[2]]
            for i, beat in enumerate([j * .5 for j in range(8)]):
                base = 54 if i in (0, 4) else 38
                lh.note(b0 + beat, .55, pat[i],
                        base * fade * g * beat_weight(beat, BB) * 1.08)
            figure(d1, b0, fig, 3.0, 30 * fade * g)
            for t in c.near(62, 3):
                p1.note(b0, 3.9, t, 24 * fade * g, jitter=0)
            lh.pedal(b0, 4)
        elif i_out <= 5:
            for i, beat in enumerate((0, 1, 2, 3)):
                lh.note(b0 + beat, .95, [c.bass, n[0], n[1], n[2]][i],
                        (46 if i == 0 else 28) * .8 * g)
            figure(d1, b0, fig, 3.0, 22 * g)
            for t in c.near(62, 3):
                p1.note(b0, 3.9, t, 18 * g, jitter=0)
            lh.pedal(b0, 4)
        elif i_out <= 7:
            lh.note(b0, 1.9, c.bass, 38 * g)
            lh.note(b0 + 2, 1.9, n[1], 24 * g)
            p1.note(b0, 3.9, c.near(62, 1)[0], 14 * g, jitter=0)
            lh.pedal(b0, 4)
        elif i_out == 8:
            base = nm(roll_low)
            third = 15 if roll_minor else 16
            roll = [base, base + 7, base + 12, base + third, base + 19,
                    base + 24, base + third + 12, base + 31]
            for j, p in enumerate(roll):
                lh.note(b0 + j * .25, 8 - j * .25, p, (46 - j * 2) * g)
            figure(d1, b0, fig, 2.0, 26 * g)
            p2.note(b0, 8, base + 36, 18, jitter=0)
            p2.note(b0, 8, base + 43, 15, jitter=0)
            p1.note(b0, 8, base + 24, 16, jitter=0)
            lh.pedal(b0, 8)

    peak_bar = next((starts[n] for n, _, r in plan if r == "peak"), pad_in + 8)
    for pad in (p1, p2):
        pad.cc(0, 11, 0)
        pad.cc_ramp(pad_in * BB, (pad_in + 4) * BB, 11, 0, 58)
        pad.cc_ramp((pad_in + 4) * BB, peak_bar * BB, 11, 58, 82)
        pad.cc_ramp(peak_bar * BB, pad_out * BB, 11, 82, 40)
        pad.cc_ramp(pad_out * BB, (end_bar + 4) * BB, 11, 40, 0)

    if mel_map is None:
        bars_of = {n: c for n, c, r in plan}
        mel_map = [(a_mel, "A", 82, "box"), (a_mel, "A2", 84, "box"),
                   (b_mel, "B", 90, "box"), (a_mel, "A3", 86, "box")]
        if bars_of.get("A3", 0) >= 16:
            starts["A3b"] = starts["A3"] + 8
            mel_map.append((a_mel, "A3b", 78, "box"))
        mel_map.append((end_mel, "end", 66, "box"))

    for text, where, vel, mode in mel_map:
        bar0 = starts[where] if isinstance(where, str) else where
        notes = parse_mel(text, BB, bar0)
        if mode == "vocal":
            voc.play(notes, vel, bar_beats=BB)
            pmel.play(notes, vel * .40, bar_beats=BB)
        else:
            box.play(notes, vel, octave=1, bar_beats=BB)
            pmel.play(notes, vel * .55, bar_beats=BB)

    if voc is not None:
        voc.enforce_mono()

    r = bpm / 82.0
    E = end_bar * BB
    tempos = [(0, bpm), (E, 78 * r), (E + 8, 72 * r), (E + 16, 64 * r),
              (E + 24, 54 * r), (E + 32, 46 * r)]
    tracks = heads + [lh, d1, d2, p1, p2] + (extra_tracks or [])
    save(path, meta_track(title, tempos), tracks)
    return (os.path.basename(path), duration_sec(tempos, nbars * BB + 8),
            starts, nbars)
