#!/usr/bin/env python3
"""
trim_intro.py — make a remastered cue start PUNCHY by trimming its head, losslessly
in musical terms (no new generation), and keep meta.json's loop point valid.

  python3 tools/audio/trim_intro.py <id> --silence      # drop leading near-silence only
  python3 tools/audio/trim_intro.py <id> --drop-intro   # start ON the loop (theme from beat one;
                                                        #   loop_start becomes 0 = whole-file loop)
  python3 tools/audio/trim_intro.py <id> --to 2.5       # cut the first N seconds

Battles and the title must hit from the first beat (owner's steer, 2026-10): when a
generated intro builds or sags, drop it and open on the theme rather than re-rolling.
Afterwards run build_remaster_manifest.py (+ build_music_data.mjs).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SERVED = ROOT / "public/assets/audio/music/remaster"
SPECS = ROOT / "assets/audio/elevenlabs"
SR = 44100


def pcm(path: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--silence", action="store_true")
    g.add_argument("--drop-intro", action="store_true")
    g.add_argument("--to", type=float)
    a = ap.parse_args()

    f = SERVED / f"{a.id}.mp3"
    meta_p = SPECS / a.id / "meta.json"
    meta = json.loads(meta_p.read_text())
    x = pcm(f)
    ls = meta.get("loop_start") or 0.0
    if a.drop_intro:
        cut = int(round(ls * SR))
    elif a.to is not None:
        cut = int(round(a.to * SR))
    else:
        loud = np.flatnonzero(np.abs(x).max(1) > 10 ** (-40 / 20))
        cut = max(0, int(loud[0]) - int(0.01 * SR)) if len(loud) else 0
    if cut <= 0:
        print(f"{a.id}: nothing to trim")
        return 0
    if ls and cut > int(round(ls * SR)) + 1:
        raise SystemExit(f"{a.id}: cut {cut / SR:.3f}s is past loop_start {ls}s — would break the loop")
    y = x[cut:].copy()
    fade = int(0.005 * SR)
    if not a.drop_intro:  # a cut mid-intro gets a tiny fade-in; ON the loop it must stay sample-exact
        y[:fade] *= np.linspace(0, 1, fade, dtype=np.float32)[:, None]
    tmp = f.with_suffix(".trim.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-",
                    "-c:a", "libmp3lame", "-b:a", "128k", str(tmp)], input=y.tobytes(), check=True)
    tmp.replace(f)
    new_ls = round(max(0.0, ls - cut / SR), 3) if ls else None
    meta["loop_start"] = new_ls if new_ls else (0.0 if a.drop_intro else meta.get("loop_start"))
    meta["duration"] = round(len(y) / SR, 3)
    meta.setdefault("edits", []).append(
        "intro dropped: opens on the theme" if a.drop_intro else f"trimmed {cut / SR:.3f}s of head")
    meta_p.write_text(json.dumps(meta, indent=1) + "\n")
    print(f"{a.id}: cut {cut / SR:.3f}s -> loop_start {meta['loop_start']}  duration {meta['duration']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
