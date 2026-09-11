#!/usr/bin/env python3
"""Inventory explicit MIDI-generation rules from preserved Python source.

This tool parses source only. It never imports the album modules, executes the
builder, or writes MIDI files.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any


def literal_assignments(tree: ast.AST, wanted_prefixes: tuple[str, ...]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        value = node.value
        for target in targets:
            if isinstance(target, ast.Name) and target.id.startswith(wanted_prefixes):
                try:
                    out[target.id] = ast.literal_eval(value)
                except (ValueError, TypeError):
                    pass
    return out


def call_inventory(tree: ast.AST, source: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    interesting = {
        "Track", "figure", "pedal", "cc", "cc_ramp", "play", "note",
        "enforce_mono", "meta_track", "save", "_pack", "_vlq",
    }
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = fn.id if isinstance(fn, ast.Name) else fn.attr if isinstance(fn, ast.Attribute) else None
        if name not in interesting:
            continue
        rows.append({
            "call": name,
            "line": getattr(node, "lineno", None),
            "source": ast.get_source_segment(source, node),
        })
    return sorted(rows, key=lambda r: (r["line"] or 0, r["call"]))


def inspect_file(path: Path) -> dict[str, Any]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    return {
        "file": str(path),
        "constants": literal_assignments(tree, ("ROLE_GAIN", "PLAN_", "P_", "PPQ", "QUAL", "GM_RANGE")),
        "calls": call_inventory(tree, source),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", type=Path, required=True)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    candidates = ["formula.py", "midilib.py", "songs.py"]
    present = [args.source_root / name for name in candidates if (args.source_root / name).exists()]
    missing = [name for name in candidates if not (args.source_root / name).exists()]

    result = {
        "kind": "explicit-source-rule-inventory",
        "regenerates_midi": False,
        "executes_source": False,
        "files": [inspect_file(p) for p in present],
        "missing_from_local_snapshot": missing,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
