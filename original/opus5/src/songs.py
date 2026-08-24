# -*- coding: utf-8 -*-
"""
《甜空氣標本》九首歌的全部樂譜資料。這是專輯的原始碼。

v3：每首有自己的曲式計畫，不再共用寫死的 62 小節。
    50 / 54 / 62 / 66 / 70 小節五種長度，避免連續聽 30 分鐘時的形式重複。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from midilib import Track, prog, nm

# ── 曲式計畫 ────────────────────────────────────────────────
P_STD = [("intro", 4, "intro"), ("A", 8, "verse"), ("A2", 8, "lift"),
         ("B", 16, "peak"), ("A3", 16, "sustain"), ("end", 10, "end")]        # 62

P_SHORT = [("intro", 4, "intro"), ("A", 8, "verse"), ("A2", 8, "lift"),
           ("B", 16, "peak"), ("A3", 8, "sustain"), ("end", 10, "end")]       # 54

P_BREAK = [("intro", 4, "intro"), ("A", 8, "verse"), ("A2", 8, "lift"),
           ("B", 8, "peak"), ("break", 4, "break"), ("A3", 8, "sustain"),
           ("end", 10, "end")]                                                # 50

P_VOC = [("intro", 4, "intro"), ("V1", 8, "verse"), ("Ch1", 8, "lift"),
         ("V2", 8, "verse"), ("Ch2", 8, "peak"), ("Br", 8, "sustain"),
         ("Ch3", 8, "lift"), ("end", 10, "end")]                              # 62

P_VOC_LONGBR = [("intro", 4, "intro"), ("V1", 8, "verse"), ("Ch1", 8, "lift"),
                ("V2", 8, "verse"), ("Ch2", 8, "peak"), ("Br", 12, "sustain"),
                ("Ch3", 8, "lift"), ("end", 10, "end")]                       # 66

P_VOC_EXTRA = [("intro", 4, "intro"), ("V1", 8, "verse"), ("Ch1", 8, "lift"),
               ("V2", 8, "verse"), ("Ch2", 8, "peak"), ("Br", 8, "sustain"),
               ("Ch3", 8, "lift"), ("Ch4", 8, "peak"), ("end", 10, "end")]    # 70


# ════════════════════════════════════════════════════════════
#  01  The First Breath of Winter    D♭ major · 78 BPM · 62 小節
# ════════════════════════════════════════════════════════════
S01 = dict(
    file="01_first_breath_of_winter.mid",
    title="The First Breath of Winter", bpm=78, roll_low="Db2", plan=P_STD,
    a_ch="Dbadd9 | Ab/C | Bbm7 | Gbmaj7 | Db/F | Ebf7 | Absus4 | Ab",
    b_ch="Gbmaj7 | Ab7 | Fm7 | Bbm7 | Ebm7 | Ab7 | Db | Ab",
    end_ch=("Gbmaj7 | Ebm7 | Db/F | Absus4 | Bbm7 | Gbmaj7 | Ebm7 "
            "| Ab7sus4 | Db | Db"),
    a_mel="""
    b0  r0.5 F4:0.5 Ab4:0.5 Bb4:1.5 Ab4:1
    b1  Eb4:2 F4:1 Ab4:1
    b2  Bb4:0.5 Db5:0.5 Eb5:1.5 Db5:0.5 Bb4:1
    b3  Ab4:2 F4:2
    b4  r0.5 Ab4:0.5 Bb4:0.5 Db5:0.5 F5:1 Eb5:1
    b5  Db5:0.5 Eb5:0.5 Db5:1 Bb4:1 Ab4:1
    b6  Bb4:0.5 Db5:0.5 Eb5:1.5 F5:0.5 Eb5:1
    b7  Db5:2 C5:2
    """,
    b_mel="""
    b0  r0.5 Bb4:0.5 Db5:0.5 Eb5:0.5 Gb5:1.5 r0.5
    b1  F5:0.5 Eb5:0.5 F5:1 Ab5:1 Gb5:1
    b2  F5:1 Eb5:1 Db5:1 C5:1
    b3  Db5:2 F5:2
    b4  r0.5 Gb5:0.5 F5:0.5 Eb5:0.5 Db5:1 Bb4:1
    b5  C5:0.5 Db5:0.5 Eb5:1.5 Gb5:0.5 F5:1
    b6  Eb5:1 Db5:1 F5:2
    b7  Eb5:2 C5:2
    b8  r0.5 Db5:0.5 F5:0.5 Ab5:0.5 Bb5:1.5 r0.5
    b9  Ab5:0.5 Gb5:0.5 Ab5:1 Bb5:1 Ab5:1
    b10 Gb5:1 F5:1 Eb5:1 Db5:1
    b11 F5:2 Eb5:2
    b12 r0.5 Bb4:0.5 Db5:0.5 F5:0.5 Ab5:1 Gb5:1
    b13 F5:0.5 Eb5:0.5 F5:1.5 Ab5:0.5 Gb5:1
    b14 F5:1 Eb5:1 Db5:2
    b15 C5:2 Ab4:2
    """,
    end_mel="""
    b0  r0.5 Bb4:0.5 Db5:0.5 Eb5:1 Db5:1 Bb4:0.5
    b1  Ab4:2 F4:2
    b2  r0.5 Ab4:0.5 Bb4:0.5 Db5:0.5 C5:2
    b3  Db5:4
    b4  r1 F4:1 Ab4:1 Bb4:1
    b5  Ab4:2 r2
    b6  r1 Bb4:1 Ab4:2
    b7  r2 Eb4:2
    b8  Db5:1 F5:1 Ab5:2
    b9  Db5:8
    """)

# ════════════════════════════════════════════════════════════
#  02  The Evening Air Tasted Sweet   A major · 86 BPM · 54 小節
#  刻意做短——它是行進曲，不該拖
# ════════════════════════════════════════════════════════════
_A02 = "A | E/G# | F#m7 | D | A/C# | Bm7 | Dmaj7 | E"
S02 = dict(
    file="02_the_evening_air_tasted_sweet.mid",
    title="The Evening Air Tasted Sweet", bpm=86, roll_low="A1",
    plan=P_SHORT, a_ch=_A02,
    b_ch="Dmaj7 | E7 | C#m7 | F#m7 | Bm7 | E7 | A | E",
    end_ch=("Dmaj7 | Bm7 | A/C# | Esus4 | F#m7 | Dmaj7 | Bm7 "
            "| E7sus4 | A | A"),
    a_mel="""
    b0  r0.5 E5:0.5 F#5:0.5 C#5:1 B4:0.5 C#5:1
    b1  A4:1 C#5:1 E5:2
    b2  F#5:0.5 E5:0.5 C#5:1 B4:1 A4:1
    b3  B4:2 C#5:2
    b4  r0.5 C#5:0.5 E5:0.5 F#5:1 A5:1 F#5:0.5
    b5  E5:1 C#5:1 B4:2
    b6  C#5:0.5 E5:0.5 F#5:1.5 E5:0.5 C#5:1
    b7  B4:2 A4:2
    """,
    b_mel="""
    b0  r0.5 F#5:0.5 A5:0.5 B5:1.5 A5:1
    b1  F#5:0.5 E5:0.5 F#5:1 A5:1 G#5:1
    b2  F#5:1 E5:1 C#5:1 B4:1
    b3  C#5:2 E5:2
    b4  r0.5 A5:0.5 G#5:0.5 F#5:0.5 E5:1 C#5:1
    b5  D5:0.5 E5:0.5 F#5:1.5 A5:0.5 G#5:1
    b6  F#5:1 E5:1 A5:2
    b7  F#5:2 D5:2
    b8  r0.5 E5:0.5 A5:0.5 B5:1.5 A5:1
    b9  A5:0.5 G#5:0.5 A5:1 B5:1 A5:1
    b10 G#5:1 F#5:1 E5:1 C#5:1
    b11 E5:2 D5:2
    b12 r0.5 C#5:0.5 E5:0.5 A5:0.5 B5:1 A5:1
    b13 A5:0.5 G#5:0.5 A5:1.5 F#5:0.5 E5:1
    b14 F#5:1 E5:1 C#5:2
    b15 B4:2 E5:2
    """,
    end_mel="""
    b0  r0.5 F#5:0.5 A5:0.5 B5:1 A5:1 F#5:0.5
    b1  E5:2 C#5:2
    b2  r0.5 E5:0.5 F#5:0.5 A5:0.5 G#5:2
    b3  A5:4
    b4  r1 C#5:1 E5:1 F#5:1
    b5  E5:2 r2
    b6  r1 F#5:1 E5:2
    b7  r2 B4:2
    b8  A4:1 C#5:1 E5:2
    b9  A5:8
    """)


def extras_02():
    """單簧管長音＝店舖裡的暖氣。B 段位於第 20–35 小節"""
    cla = Track("8 Clarinet warm (mute me)", 8, 71, jitter=0)
    P = prog(_A02)[:4] + prog(_A02) * 2 + prog(S02["b_ch"]) * 2 \
        + prog(_A02) + prog(S02["end_ch"])
    for bar in list(range(24, 28)) + list(range(32, 36)):
        c = P[bar]
        pool = [t for t in (c.tones[1], c.tones[2]) if 55 <= t <= 68]
        if pool:
            cla.note(bar * 4.0, 3.8, pool[0], 34)
    return [cla]


# ════════════════════════════════════════════════════════════
#  03  Cold Outside, Warm in the Bowl   G major · 94 BPM · 50 小節
#  唯一有 break 段的一首——中段木質全停，只剩湯的聲音
# ════════════════════════════════════════════════════════════
_A03 = "Gadd9 | D/F# | Em7 | Cmaj7 | G/B | Am7 | Dsus4 | D"
_B03 = "Cmaj7 | D7 | Bm7 | Em7 | Am7 | D7 | G | D"
_K03 = "Cmaj7 | Cmaj7 | Am7 | Am7"
_E03 = "Cmaj7 | Am7 | G/B | Dsus4 | Em7 | Cmaj7 | Am7 | D7sus4 | G | G"
S03 = dict(
    file="03_cold_outside_warm_in_the_bowl.mid",
    title="Cold Outside, Warm in the Bowl", bpm=94, roll_low="G1",
    plan=P_BREAK,
    chord_list=" | ".join(["Gadd9 | D/F# | Em7 | Cmaj7", _A03, _A03,
                           _B03, _K03, _A03, _E03]),
    a_mel="""
    b0  r0.5 B4:1 D5:1 E5:1.5
    b1  D5:1.5 r0.5 A4:2
    b2  r0.5 C5:1 E5:1 G5:1.5
    b3  F#5:1.5 r0.5 D5:2
    b4  r0.5 B4:1 D5:1 E5:1.5
    b5  G5:2 F#5:2
    b6  E5:1 D5:1 C5:1 B4:1
    b7  A4:4
    """,
    b_mel="""
    b0  r0.5 D5:1 E5:1 G5:1.5
    b1  F#5:1.5 r0.5 D5:2
    b2  r0.5 E5:1 G5:1 B5:1.5
    b3  A5:1.5 r0.5 F#5:2
    b4  r0.5 G5:1 F#5:1 E5:1.5
    b5  D5:2 B4:2
    b6  C5:1 B4:1 A4:1 B4:1
    b7  G4:4
    """,
    end_mel="""
    b0  r0.5 B4:0.5 D5:0.5 E5:1 D5:1 B4:0.5
    b1  A4:2 G4:2
    b2  r0.5 A4:0.5 B4:0.5 D5:0.5 C5:2
    b3  D5:4
    b4  r1 G4:1 B4:1 D5:1
    b5  B4:2 r2
    b6  r1 D5:1 B4:2
    b7  r2 A4:2
    b8  G4:1 B4:1 D5:2
    b9  G5:8
    """)


def extras_03():
    """筷子與碗。第 28–31 小節（break 段）完全停掉"""
    mar = Track("8 Marimba (chopsticks)", 8, 12, jitter=5, lead=-2)
    piz = Track("9 Pizz Cello (bowls)", 9, 45, jitter=4, lead=-1)
    P = prog(S03["chord_list"])
    for bar, c in enumerate(P):
        if bar < 2 or bar >= 44 or 28 <= bar < 32:
            continue
        n = c.near(62, 3)
        wood = [n[0] + 12, n[2] + 12]
        fade = 1.0 if bar < 40 else (1 - (bar - 40) / 5.0)
        for i, beat in enumerate((0, .75, 1.5, 2, 2.75, 3.5)):
            mar.note(bar * 4.0 + beat, .4, wood[i % 2],
                     (46 if i % 2 == 0 else 36) * fade)
        pb = c.bass if c.bass >= 36 else c.bass + 12
        piz.note(bar * 4.0, .5, pb, 48 * fade)
        piz.note(bar * 4.0 + 2, .5, pb + 7, 38 * fade)
    return [mar, piz]


# ════════════════════════════════════════════════════════════
#  04  A Little House, Not a Hotel   C major · 76 BPM · 62 小節
# ════════════════════════════════════════════════════════════
_V04 = "C | G/B | Am7 | F | C/E | Dm7 | Fmaj7 | G"
_C04 = "Fmaj7 | G | Em7 | Am7 | F | G | C | G"
_B04 = "Am7 | F | Cmaj7 | G | Am7 | Dm7 | G | Gsus4"
_E04 = "Fmaj7 | Dm7 | C/E | Gsus4 | Am7 | Fmaj7 | Dm7 | G7sus4 | C | C"
_VERSE04 = """
b0  r0.5 E4:0.5 G4:0.5 G4:0.5 A4:0.5 G4:1 r0.5
b1  C5:0.5 A4:0.5 G4:0.5 E4:0.5 G4:1 r1
b2  r0.5 E4:0.5 G4:0.5 G4:0.5 A4:0.5 C5:0.5 C5:0.5 r0.5
b3  A4:0.5 G4:0.5 A4:0.5 C5:0.5 A4:0.5 G4:1.5
b4  r0.5 G4:0.5 A4:0.5 C5:0.5 C5:0.5 D5:1 r0.5
b5  C5:0.5 A4:0.5 G4:0.5 A4:0.5 G4:2
b6  r0.5 G4:0.5 G4:0.5 F4:0.5 E4:0.5 D4:1 r0.5
b7  E4:0.5 G4:0.5 F4:0.5 E4:1.5 r1
"""
_CHOR04 = """
b0  r0.5 C5:0.5 C5:0.5 D5:0.5 E5:0.5 E5:0.5 D5:0.5 r0.5
b1  C5:0.5 A4:0.5 C5:0.5 A4:0.5 G4:1.5 r0.5
b2  r0.5 A4:0.5 A4:0.5 C5:0.5 D5:0.5 C5:0.5 r1
b3  A4:0.5 C5:0.5 A4:0.5 G4:1.5 r1
b4  r0.5 G4:0.5 A4:0.5 C5:0.5 C5:0.5 D5:0.5 r1
b5  E5:0.5 D5:0.5 C5:0.5 A4:0.5 G4:1.5 r0.5
b6  r0.5 C5:0.5 C5:0.5 A4:0.5 G4:0.5 A4:0.5 r1
b7  G4:0.5 E4:0.5 G4:0.5 C5:2 r0.5
"""
_BR04 = """
b0  r0.5 E4:0.5 G4:0.5 A4:0.5 A4:0.5 G4:1 r0.5
b1  A4:0.5 G4:2 r1.5
b2  r0.5 G4:0.5 A4:0.5 C5:0.5 C5:1 r1
b3  A4:0.5 G4:2.5 r1
b4  r0.5 C5:0.5 C5:0.5 D5:0.5 E5:0.5 E5:0.5 r1
b5  D5:0.5 C5:0.5 D5:0.5 C5:1.5 r1
b6  r0.5 A4:0.5 C5:0.5 C5:0.5 D5:1 r1
b7  C5:0.5 A4:0.5 G4:2 r1
"""
_END04 = """
b0  r0.5 G4:0.5 A4:0.5 C5:1 A4:1 G4:0.5
b1  E4:2 G4:2
b2  r0.5 G4:0.5 A4:0.5 C5:0.5 B4:2
b3  C5:4
b4  r1 E4:1 G4:1 A4:1
b5  G4:2 r2
b6  r1 A4:1 G4:2
b7  r2 D4:2
b8  C4:1 E4:1 G4:2
b9  C5:8
"""
S04 = dict(
    file="04_a_little_house_not_a_hotel.mid",
    title="A Little House, Not a Hotel", bpm=76, roll_low="C2", vocal=True,
    plan=P_VOC,
    chord_list=" | ".join(["C | G/B | Am7 | F", _V04, _C04, _V04,
                           _C04, _B04, _C04, _E04]),
    mel_map=[(_VERSE04, "V1", 74, "vocal"), (_CHOR04, "Ch1", 80, "vocal"),
             (_VERSE04, "V2", 74, "vocal"), (_CHOR04, "Ch2", 82, "vocal"),
             (_BR04, "Br", 78, "vocal"), (_CHOR04, "Ch3", 82, "vocal"),
             (_END04, "end", 66, "box")])

# ════════════════════════════════════════════════════════════
#  05  They Were Still Arguing   B minor · 74 BPM · 66 小節
#  橋段加長到 12 小節——最後 4 小節沒有歌詞，讓被打斷的動機再試一次
# ════════════════════════════════════════════════════════════
_V05 = "Bm | Bmadd11 | Gmaj7 | F#m7 | Em7 | Gm6 | Bm | F#7sus4"
_C05 = "Gmaj7 | A | F#m7 | Bm7 | Gmaj7 | A | D | F#7sus4"
_B05 = ("Em7 | Bm | Gm6 | F#7sus4 | Em7 | Gmaj7 | F#7sus4 | F#7sus4 "
        "| Gm6 | Bm | F#7sus4 | F#7sus4")
_E05 = "Gmaj7 | D | Bm/D | F#sus4 | Gm6 | Gmaj7 | Em7 | F#7sus4 | Bm | Bm"
_V1_05 = """
b0  r0.5 F#4:0.5 F#4:0.5 F#4:0.5 G4:0.5 G4:0.5 A4:0.5 r0.5
b1  F#4:0.5 E4:0.5 F#4:0.5 E4:0.5 D4:1 r1
b2  r0.5 F#4:0.5 F#4:0.5 G4:0.5 G4:0.5 F#4:0.5 r1
b3  E4:0.5 F#4:0.5 G4:0.5 F#4:0.5 D4:1 r1
b4  r0.5 A4:0.5 A4:0.5 B4:0.5 B4:0.5 A4:0.5 r1
b5  G4:0.5 A4:0.5 B4:0.5 A4:0.5 F#4:1 r1
b6  r0.5 F#4:0.5 E4:0.5 F#4:0.5 G4:1 r1
b7  F#4:0.5 E4:0.5 D4:1.5 r1.5
"""
_V2_05 = """
b0  r0.5 F#4:0.5 F#4:0.5 E4:0.5 F#4:0.5 G4:0.5 r1
b1  A4:0.5 G4:0.5 F#4:0.5 E4:0.5 D4:1 r1
b2  r0.5 D4:0.5 E4:0.5 F#4:0.5 F#4:0.5 G4:0.5 A4:0.5 r0.5
b3  B4:0.5 A4:0.5 G4:0.5 F#4:0.5 E4:1 r1
b4  r0.5 A4:0.5 A4:0.5 A4:0.5 B4:0.5 A4:0.5 G4:0.5 F#4:0.5
b5  E4:1 r3
b6  r1 F#4:0.5 G4:0.5 A4:0.5 G4:1 r0.5
b7  F#4:0.5 D4:2 r1.5
"""
_CH05 = """
b0  r0.5 D5:0.5 D5:0.5 C#5:0.5 B4:0.5 A4:0.5 r1
b1  B4:0.5 D5:0.5 C#5:0.5 A4:0.5 B4:1 r1
b2  r0.5 B4:0.5 B4:0.5 A4:0.5 B4:0.5 D5:1 r0.5
b3  C#5:0.5 B4:0.5 A4:0.5 F#4:1.5 r1
b4  r0.5 F#5:0.5 F#5:0.5 E5:0.5 D5:0.5 D5:0.5 r1
b5  C#5:0.5 B4:0.5 A4:1.5 r1.5
b6  r1 B4:0.5 A4:0.5 B4:1 r1
b7  F#4:2 r2
"""
_BR05 = """
b0  r0.5 D4:0.5 D4:0.5 E4:0.5 F#4:1 r1
b1  E4:0.5 D4:0.5 B3:2 r1
b2  r0.5 F#4:0.5 F#4:0.5 G4:0.5 A4:0.5 G4:0.5 r1
b3  F#4:0.5 E4:0.5 D4:1.5 r1.5
b4  r0.5 G4:0.5 A4:0.5 B4:0.5 B4:0.5 A4:0.5 r1
b5  B4:0.5 A4:0.5 F#4:1.5 r1.5
b6  r1 A4:0.5 G4:0.5 A4:1 r1
b7  F#4:2 r2
"""
_END05 = """
b0  r0.5 F#4:0.5 A4:0.5 B4:1 A4:1 F#4:0.5
b1  E4:2 D4:2
b2  r0.5 D4:0.5 F#4:0.5 A4:0.5 G4:2
b3  F#4:4
b4  r1 D4:1 F#4:1 G4:1
b5  F#4:2 r2
b6  r1 A4:1 G4:2
b7  r2 C#4:2
b8  B3:1 D4:1 F#4:2
b9  B4:8
"""
S05 = dict(
    file="05_they_were_still_arguing.mid",
    title="They Were Still Arguing", bpm=74, roll_low="B1",
    roll_minor=True, vocal=True, plan=P_VOC_LONGBR,
    chord_list=" | ".join(["Bm | Bmadd11 | Gmaj7 | F#m7", _V05, _C05,
                           _V05, _C05, _B05, _C05, _E05]),
    mel_map=[(_V1_05, "V1", 70, "vocal"), (_CH05, "Ch1", 80, "vocal"),
             (_V2_05, "V2", 74, "vocal"), (_CH05, "Ch2", 82, "vocal"),
             (_BR05, "Br", 72, "vocal"), (_CH05, "Ch3", 82, "vocal"),
             (_END05, "end", 64, "box")])


def extras_05():
    """① 甜空氣動機只走到第 4 個音　② B♭ 與 B 的半音摩擦"""
    cut = Track("10 Cut-off motif (from 02)", 10, 10, jitter=0)
    rub = Track("11 Semitone rub Bb/B (mute me)", 11, 41, jitter=0)
    # 前奏一次；橋段延長的最後 4 小節（第 44、46 小節）再試兩次，都沒說完
    for base in (4, 176, 184):
        for off, dur, n in [(0, 1, "F#5"), (1, 1, "G5"), (2, 1.5, "D5"),
                            (3.5, 1.5, "C#5")]:
            cut.note(base + off, dur, nm(n), 44)
    for bar in (9, 25, 38, 44, 60):
        rub.note(bar * 4.0 + 1, 3.0, nm("Bb3"), 34)
        rub.note(bar * 4.0 + 1, 3.0, nm("B3"), 30)
    return [cut, rub]


# ════════════════════════════════════════════════════════════
#  06  Ten Years Without Leaving   E minor → G · 72 BPM · 70 小節
#  全專輯最長——情感核心多唱一次副歌
# ════════════════════════════════════════════════════════
_V06 = "Em | Cmaj7 | G | D | Em | Am7 | Cmaj7 | D"
_C06 = "Em | G | Cmaj7 | D | Em | G | Cmaj7 | D"
_B06 = "Cmaj7 | G/B | Am7 | D | Cmaj7 | Am7 | D | Dsus4"
_E06 = "Cmaj7 | Am7 | G/B | Dsus4 | Em | Cmaj7 | Am7 | D7sus4 | G | G"
_VERSE06 = """
b0  r0.5 E4:0.5 E4:0.5 G4:0.5 G4:1 r1
b1  A4:0.5 G4:0.5 E4:2 r1
b2  r0.5 E4:0.5 G4:0.5 G4:0.5 A4:0.5 B4:1 r0.5
b3  A4:0.5 G4:0.5 A4:0.5 G4:1.5 r1
b4  r0.5 B4:0.5 B4:0.5 A4:0.5 B4:1 r1
b5  D5:0.5 B4:0.5 A4:0.5 G4:1.5 r1
b6  r0.5 G4:0.5 G4:0.5 A4:1 r1.5
b7  B4:0.5 A4:0.5 G4:0.5 E4:1.5 r1
"""
_CHOR06 = """
b0  r0.5 B4:0.5 B4:0.5 D5:0.5 D5:0.5 E5:0.5 D5:0.5 r0.5
b1  B4:0.5 A4:0.5 B4:0.5 A4:0.5 G4:1.5 r0.5
b2  r0.5 G4:0.5 A4:0.5 B4:0.5 D5:0.5 D5:0.5 E5:0.5 r0.5
b3  D5:0.5 B4:0.5 A4:0.5 B4:0.5 G4:1.5 r0.5
b4  r0.5 A4:0.5 A4:0.5 B4:0.5 D5:1 r1
b5  E5:0.5 D5:0.5 B4:0.5 A4:1.5 r1
b6  r1 B4:0.5 D5:0.5 E5:1 r1
b7  D5:1 G4:2 r1
"""
_BR06 = """
b0  r0.5 E4:0.5 G4:0.5 G4:0.5 A4:0.5 B4:1 r0.5
b1  A4:0.5 G4:0.5 A4:0.5 G4:1.5 r1
b2  r0.5 B4:0.5 B4:0.5 D5:0.5 D5:1 r1
b3  B4:0.5 A4:0.5 G4:2 r1
b4  r0.5 G4:0.5 A4:0.5 B4:1 r1.5
b5  A4:0.5 G4:0.5 E4:2 r1
b6  r1 E4:0.5 G4:0.5 A4:1 r1
b7  B4:2 r2
"""
_END06 = """
b0  r0.5 B4:0.5 D5:0.5 E5:1 D5:1 B4:0.5
b1  A4:2 G4:2
b2  r0.5 A4:0.5 B4:0.5 D5:0.5 C5:2
b3  D5:4
b4  r1 E4:1 G4:1 A4:1
b5  G4:2 r2
b6  r1 B4:1 A4:2
b7  r2 E4:2
b8  G4:1 B4:1 D5:2
b9  G5:8
"""
S06 = dict(
    file="06_ten_years_without_leaving.mid",
    title="Ten Years Without Leaving", bpm=72, roll_low="G1", vocal=True,
    plan=P_VOC_EXTRA,
    chord_list=" | ".join(["Em | Cmaj7 | G | D", _V06, _C06, _V06,
                           _C06, _B06, _C06, _C06, _E06]),
    mel_map=[(_VERSE06, "V1", 74, "vocal"), (_CHOR06, "Ch1", 82, "vocal"),
             (_VERSE06, "V2", 76, "vocal"), (_CHOR06, "Ch2", 84, "vocal"),
             (_BR06, "Br", 76, "vocal"), (_CHOR06, "Ch3", 84, "vocal"),
             (_CHOR06, "Ch4", 88, "vocal"), (_END06, "end", 66, "box")])


def extras_06():
    """橋段引用 01 的五音動機（在 G 上＝B–D–E–D–A）。橋段＝第 36–43 小節"""
    q = Track("8 Motif from 01", 8, 8, jitter=0)
    for beat, dur, n in [(160, 2, "B5"), (162, 2, "D6"), (164, 3, "E6"),
                         (168, 2, "D6"), (172, 4, "A5")]:
        q.note(beat, dur, nm(n), 34)
    return [q]


# ════════════════════════════════════════════════════════════
#  07  A Town Above the Clouds   E major · 84 BPM · 62 小節
# ════════════════════════════════════════════════════════
_V07 = "E | C#m7 | Amaj7 | B | E/G# | F#m7 | Amaj7 | B"
_C07 = "Amaj7 | B | G#m7 | C#m7 | Amaj7 | B | E | B"
_B07 = "C#m7 | Amaj7 | E/G# | B | C#m7 | F#m7 | B | Bsus4"
_E07 = "Amaj7 | F#m7 | E/G# | Bsus4 | C#m7 | Amaj7 | F#m7 | B7sus4 | E | E"
_VERSE07 = """
b0  r0.5 B4:0.5 B4:0.5 C#5:0.5 B4:0.5 A4:1 r0.5
b1  G#4:0.5 A4:0.5 B4:0.5 A4:1.5 r1
b2  r0.5 G#4:0.5 A4:0.5 B4:0.5 B4:1 r1
b3  C#5:0.5 B4:0.5 A4:0.5 G#4:1.5 r1
b4  r0.5 A4:0.5 A4:0.5 B4:0.5 C#5:0.5 C#5:1 r0.5
b5  E5:0.5 C#5:0.5 B4:0.5 A4:1.5 r1
b6  r0.5 B4:0.5 B4:0.5 A4:0.5 B4:1 r1
b7  G#4:0.5 F#4:0.5 E4:2 r1
"""
_CHOR07 = """
b0  r0.5 E5:0.5 E5:0.5 D#5:1 r1.5
b1  C#5:0.5 B4:0.5 A4:2 r1
b2  r0.5 C#5:0.5 C#5:0.5 B4:1 r1.5
b3  A4:0.5 B4:0.5 C#5:2 r1
b4  r0.5 B4:0.5 C#5:0.5 D#5:0.5 E5:1 r1
b5  D#5:0.5 C#5:0.5 B4:2 r1
b6  r0.5 A4:0.5 B4:0.5 C#5:1 r1.5
b7  B4:0.5 A4:0.5 G#4:2 r1
"""
_BR07 = """
b0  r0.5 G#4:0.5 A4:0.5 B4:0.5 B4:1 r1
b1  C#5:0.5 B4:0.5 A4:0.5 G#4:1.5 r1
b2  r0.5 A4:0.5 A4:0.5 B4:0.5 C#5:1 r1
b3  B4:0.5 A4:0.5 B4:0.5 A4:1.5 r1
b4  r0.5 B4:0.5 C#5:0.5 D#5:0.5 E5:1 r1
b5  D#5:0.5 C#5:0.5 B4:0.5 C#5:1.5 r1
b6  r0.5 C#5:0.5 B4:0.5 A4:1 r1.5
b7  B4:0.5 A4:0.5 F#4:2 r1
"""
_END07 = """
b0  r0.5 B4:0.5 C#5:0.5 E5:1 C#5:1 B4:0.5
b1  A4:2 F#4:2
b2  r0.5 A4:0.5 B4:0.5 C#5:0.5 B4:2
b3  E5:4
b4  r1 G#4:1 B4:1 C#5:1
b5  B4:2 r2
b6  r1 C#5:1 B4:2
b7  r2 F#4:2
b8  E4:1 G#4:1 B4:2
b9  E5:8
"""
S07 = dict(
    file="07_a_town_above_the_clouds.mid",
    title="A Town Above the Clouds", bpm=84, roll_low="E2", vocal=True,
    plan=P_VOC,
    chord_list=" | ".join(["E | C#m7 | Amaj7 | B", _V07, _C07, _V07,
                           _C07, _B07, _C07, _E07]),
    mel_map=[(_VERSE07, "V1", 74, "vocal"), (_CHOR07, "Ch1", 82, "vocal"),
             (_VERSE07, "V2", 76, "vocal"), (_CHOR07, "Ch2", 84, "vocal"),
             (_BR07, "Br", 78, "vocal"), (_CHOR07, "Ch3", 84, "vocal"),
             (_END07, "end", 66, "box")])

# ═══════════════════════════════════════════════════════════
#  08  That Morning Never Left   D♭ major · 76 BPM · 62 小節 · 拼貼
# ════════════════════════════════════════════════════════════
_CH08 = " | ".join([
    "Dbadd9 | Ab/C | Bbm7 | Gbmaj7",
    "Dbadd9 | Ab/C | Bbm7 | Gbmaj7 | Db/F | Ebf7 | Absus4 | Ab",
    "Db | Ab/C | Bbm7 | Gb | Db/F | Ebf7 | Gbmaj7 | Ab",
    "Gbmaj7 | Ab | Db | Bbm7 | Gbmaj7 | Ab | Db | Ab",
    "Bbm | Bbmadd11 | Gbmaj7 | Fm7 | Ebm7 | Gbm6 | Bbm | F7sus4",
    "Bbm | Db | Gbmaj7 | Ab | Bbm | Db | Gbmaj7 | Ab",
    "Db | Bbm7 | Gbmaj7 | Ab | Db/F | Ebm7 | Gbmaj7 | Ab",
    "Gbmaj7 | Ebm7 | Db/F | Absus4 | Bbm7 | Gbmaj7 | Ebf7 | Ab7sus4 | Db | Db"])
S08 = dict(
    file="08_that_morning_never_left.mid",
    title="That Morning Never Left", bpm=76, roll_low="Db2",
    plan=P_STD, chord_list=_CH08,
    mel_map=[("""
    b0  r0.5 F4:0.5 Ab4:0.5 Bb4:1.5 Ab4:1
    b1  Eb4:2 r2
    b2  r0.5 F4:0.5 Ab4:0.5 Bb4:1.5 Db5:1
    b3  Ab4:2 F4:2
    b4  r0.5 Ab4:0.5 Bb4:0.5 Db5:1 Eb5:1 r0.5
    b5  Db5:2 Bb4:2
    b6  Ab4:1 Gb4:1 F4:2
    b7  Eb4:4
    """, "A", 78, "box"),
             ("""
    b0  r0.5 Ab4:0.5 Bb4:0.5 F4:1 Eb4:0.5 F4:1
    b1  Db4:1 F4:1 Ab4:2
    b2  Bb4:0.5 Ab4:0.5 F4:1 Eb4:1 Db4:1
    b3  Eb4:2 F4:2
    b4  r0.5 F4:0.5 Ab4:0.5 Bb4:1 Db5:1 Bb4:0.5
    b5  Ab4:1 F4:1 Eb4:2
    b6  F4:0.5 Ab4:0.5 Bb4:1.5 Ab4:0.5 F4:1
    b7  Eb4:2 Db4:2
    """, "A2", 76, "box"),
             ("""
    b0  r1 F5:1 Ab5:2
    b1  r1 F5:1 Ab5:2
    b2  r0.5 Db5:0.5 F5:1 Ab5:1 Gb5:1
    b3  F5:2 Db5:2
    b4  r1 Ab5:1 Bb5:2
    b5  r1 Ab5:1 F5:2
    b6  Db5:1 F5:1 Ab5:1 Bb5:1
    b7  Ab5:4
    b8  r0.5 Ab4:0.5 Bb4:0.5 F4:1.5 Eb4:1
    b9  r4
    b10 r0.5 Ab4:0.5 Bb4:0.5 F4:1.5 Eb4:1
    b11 r4
    b12 r0.5 Ab4:0.5 Bb4:0.5 F4:2
    b13 r4
    b14 r0.5 Ab4:0.5 Bb4:1.5
    b15 r4
    """, "B", 74, "box"),
             ("""
    b0  r0.5 F5:0.5 F5:0.5 Ab5:0.5 Ab5:0.5 Bb5:0.5 Ab5:0.5 r0.5
    b1  F5:0.5 Eb5:0.5 F5:0.5 Eb5:0.5 Db5:1.5 r0.5
    b2  r0.5 Db5:0.5 Eb5:0.5 F5:0.5 Ab5:0.5 Ab5:0.5 Bb5:0.5 r0.5
    b3  Ab5:0.5 F5:0.5 Eb5:0.5 F5:0.5 Db5:1.5 r0.5
    b4  r0.5 Eb5:0.5 Eb5:0.5 F5:0.5 Ab5:1 r1
    b5  Bb5:0.5 Ab5:0.5 F5:0.5 Eb5:1.5 r1
    b6  r1 F5:0.5 Ab5:0.5 Bb5:1 r1
    b7  Ab5:1 Db5:2 r1
    b8  r0.5 Bb5:0.5 Bb5:0.5 Ab5:1 r1.5
    b9  Gb5:0.5 F5:0.5 Eb5:2 r1
    b10 r0.5 Gb5:0.5 Gb5:0.5 F5:1 r1.5
    b11 Eb5:0.5 F5:0.5 Gb5:2 r1
    b12 r0.5 F5:0.5 Gb5:0.5 Ab5:0.5 Bb5:1 r1
    b13 Ab5:0.5 Gb5:0.5 F5:2 r1
    b14 r0.5 Eb5:0.5 F5:0.5 Gb5:1 r1.5
    b15 F5:0.5 Eb5:0.5 Db5:2 r1
    """, "A3", 82, "box"),
             ("""
    b0  r0.5 F4:0.5 Ab4:0.5 Bb4:1 Ab4:1 F4:0.5
    b1  Eb4:2 Db4:2
    b2  r0.5 Ab4:0.5 Bb4:0.5 Db5:0.5 C5:2
    b3  Db5:4
    b4  r1 F4:1 Ab4:1 Bb4:1
    b5  Ab4:2 r2
    b6  r1 Bb4:1 Ab4:2
    b7  r2 Eb4:2
    b8  Db4:1 F4:1 Ab4:2
    b9  Db5:8
    """, "end", 66, "box")])


def extras_08():
    """引用 03 的木質兩音、04 的三拍搖晃、05 的半音摩擦"""
    mar = Track("8 Marimba (from 03)", 8, 12, jitter=5, lead=-2)
    gtr = Track("9 Guitar sway (from 04)", 10, 24, jitter=4)
    rub = Track("10 Semitone rub (from 05)", 11, 41, jitter=0)
    P = prog(_CH08)
    for bar in range(20, 24):
        for i, beat in enumerate((0, .75, 1.5, 2, 2.75, 3.5)):
            mar.note(bar * 4.0 + beat, .4,
                     nm("F5") if i % 2 == 0 else nm("Ab5"),
                     40 if i % 2 == 0 else 32)
    for bar in range(24, 28):
        tones = P[bar].near(64, 3)
        for i, beat in enumerate((0, 1.5, 3)):
            gtr.note(bar * 4.0 + beat, 1.3, tones[i % 3], 40)
    for bar in (29, 33):
        rub.note(bar * 4.0 + 1, 3.0, nm("A3"), 32)
        rub.note(bar * 4.0 + 1, 3.0, nm("Ab3"), 28)
    return [mar, gtr, rub]


# ════════════════════════════════════════════════════════════
#  09  Where We Start（bonus）   D major · 82 BPM · 62 小節
# ═════════════════════════════════════════════════════════════
S09 = dict(
    file="09_bonus_where_we_start.mid",
    title="Where We Start (bonus)", bpm=82, roll_low="D2", plan=P_STD,
    a_ch="D | A/C# | Bm7 | G | D/F# | Em7 | Gmaj7 | A",
    b_ch="Gmaj7 | A7 | F#m7 | Bm7 | Em7 | A7 | D | A",
    end_ch=("Gmaj7 | Em7 | D/F# | Asus4 | Bm7 | Gmaj7 | Em7 "
            "| A7sus4 | D | D"),
    a_mel="""
    b0  r0.5 F#4:0.5 A4:0.5 B4:0.5 D5:1.5 r0.5
    b1  C#5:0.5 D5:0.5 E5:1 D5:1 A4:1
    b2  B4:0.5 D5:0.5 F#5:1.5 E5:0.5 D5:1
    b3  B4:2 A4:2
    b4  r0.5 A4:0.5 B4:0.5 D5:0.5 F#5:1 E5:1
    b5  D5:0.5 E5:0.5 D5:1 B4:1 A4:1
    b6  B4:0.5 D5:0.5 E5:1.5 F#5:0.5 E5:1
    b7  D5:2 C#5:2
    """,
    b_mel="""
    b0  r0.5 B4:0.5 D5:0.5 E5:0.5 G5:1.5 r0.5
    b1  F#5:0.5 E5:0.5 F#5:1 A5:1 G5:1
    b2  F#5:1 E5:1 D5:1 C#5:1
    b3  D5:2 F#5:2
    b4  r0.5 G5:0.5 F#5:0.5 E5:0.5 D5:1 B4:1
    b5  C#5:0.5 D5:0.5 E5:1.5 G5:0.5 F#5:1
    b6  E5:1 D5:1 F#5:2
    b7  E5:2 C#5:2
    b8  r0.5 D5:0.5 F#5:0.5 A5:0.5 B5:1.5 r0.5
    b9  A5:0.5 G5:0.5 A5:1 B5:1 A5:1
    b10 G5:1 F#5:1 E5:1 D5:1
    b11 F#5:2 E5:2
    b12 r0.5 B4:0.5 D5:0.5 F#5:0.5 A5:1 G5:1
    b13 F#5:0.5 E5:0.5 F#5:1.5 A5:0.5 G5:1
    b14 F#5:1 E5:1 D5:2
    b15 C#5:2 A4:2
    """,
    end_mel="""
    b0  r0.5 B4:0.5 D5:0.5 E5:1 D5:1 B4:0.5
    b1  A4:2 F#4:2
    b2  r0.5 A4:0.5 B4:0.5 D5:0.5 C#5:2
    b3  D5:4
    b4  r1 F#4:1 A4:1 B4:1
    b5  D5:2 r2
    b6  r1 F#4:1 E4:2
    b7  r2 B4:2
    b8  D4:1 F#4:1 A4:2
    b9  D5:8
    """)

ALBUM = [
    (S01, None), (S02, extras_02), (S03, extras_03), (S04, None),
    (S05, extras_05), (S06, extras_06), (S07, None), (S08, extras_08),
    (S09, None),
]
