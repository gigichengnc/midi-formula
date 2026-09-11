# -*- coding: utf-8 -*-
"""
《甜空氣標本》全專輯建置腳本。

    python build_album.py

從 src/songs.py 的樂譜資料重新產生全部九首 MIDI，
並寫出 manifest.json（段落位置與曲式資料，供品管與匯出程式使用）。
"""
import os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))

from formula import build          # noqa: E402
from songs import ALBUM            # noqa: E402

BUILD_KEYS = {"title", "bpm", "roll_low", "roll_minor", "a_ch", "b_ch",
              "end_ch", "a_mel", "b_mel", "end_mel", "chord_list",
              "mel_map", "vocal", "plan"}


def main():
    t0 = time.time()
    rows, manifest, total = [], {}, 0.0
    for spec, extras in ALBUM:
        kw = {k: v for k, v in spec.items() if k in BUILD_KEYS}
        if extras:
            kw["extra_tracks"] = extras()
        name, sec, starts, nbars = build(os.path.join(HERE, spec["file"]), **kw)
        total += sec
        form = " ".join(f"{n}:{c}" for n, c, r in spec.get("plan", []))
        manifest[spec["file"]] = dict(
            title=spec["title"], bpm=spec["bpm"], bars=nbars,
            vocal=bool(spec.get("vocal")), starts=starts, form=form)
        rows.append((name, sec, nbars, form,
                     os.path.getsize(os.path.join(HERE, spec["file"]))))

    with open(os.path.join(HERE, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    w = max(len(r[0]) for r in rows)
    print(f"\n{'檔案'.ljust(w)}  {'時長':>5} {'小節':>4}  {'大小':>7}")
    print("-" * (w + 24))
    for name, sec, nbars, form, size in rows:
        print(f"{name.ljust(w)}  {int(sec // 60)}:{int(sec % 60):02d} "
              f"{nbars:4d}  {size / 1024:6.1f}K")
    print("-" * (w + 24))
    print(f"{'九首合計'.ljust(w)}  {int(total // 60)}:{int(total % 60):02d}")

    forms = sorted({r[2] for r in rows})
    print(f"\n曲式長度分佈：{forms}（{len(forms)} 種）")
    print(f"建置完成，耗時 {time.time() - t0:.1f} 秒 → manifest.json")


if __name__ == "__main__":
    main()
