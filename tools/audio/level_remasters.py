#!/usr/bin/env python3
"""
level_remasters.py — bring every remastered cue to one loudness, so flipping
Settings → Soundtrack (or walking from a sparse cave cue into a busy town cue)
never jumps in volume.

Each ElevenLabs render comes out at its own level (measured -11.8 … -22 LUFS) and
some peak at 0 dBFS. This applies a single static gain per file to hit TARGET_LUFS
(the classic chip renders sit at about -15 LUFS), with a brick-wall limiter at
-1 dBFS only as a safety net — no compression, so the dynamics the cue was written
with survive. Durations are preserved exactly, so meta.json loop_start stays valid.

Idempotent: the measured result is written to meta.json ("lufs"), and files within
TOLERANCE of the target are skipped.

  python3 tools/audio/level_remasters.py            # level everything that needs it
  python3 tools/audio/level_remasters.py --report   # measure only
  python3 tools/audio/level_remasters.py <id> ...   # just these cues
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SERVED = ROOT / "public/assets/audio/music/remaster"
SPECS = ROOT / "assets/audio/elevenlabs"
TARGET_LUFS = -15.0
# Deliberately sparse cues (a lone drone, a held-breath cold open) would sound
# pushed at the house level: they sit a little under it, still within reach of a
# neighbouring cue so a crossfade never drops away.
QUIET = {"coldopen-foreboding": -19.0, "penumbra-ring-a": -18.0, "coldfog-marches-a": -18.0,
         # The stock indoor set: stepping through a door should feel like the room got
         # smaller, so rooms sit under the outdoor house level (a crossfade, not a drop).
         "interior-hearth": -16.5, "interior-sunny": -16.5, "interior-lamplit": -17.0,
         "interior-study": -17.0, "interior-hush": -18.0, "interior-unease": -18.0,
         "shop-counter": -16.0, "inn-rest": -16.5, "lumenary-hall": -16.0,
         # The Wild Ways (09-the-wild-ways): the sparse places sit under the house level.
         "mirelight": -16.5, "old-seams": -17.5}
TOLERANCE = 0.5
CEILING = 0.89  # ~ -1 dBFS sample peak for the safety limiter


def measure(path: Path) -> tuple[float, float]:
    """(integrated LUFS, true peak dBTP)"""
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", tail).group(1))
    p = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail).group(1))
    return i, p


def duration(path: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True, check=True).stdout)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    files = [SERVED / f"{i}.mp3" for i in a.ids] if a.ids else sorted(SERVED.glob("*.mp3"))
    for f in files:
        lufs, peak = measure(f)
        gain = QUIET.get(f.stem, TARGET_LUFS) - lufs
        line = f"{f.stem:28s} {lufs:6.1f} LUFS  peak {peak:5.1f}"
        if a.report or (abs(gain) <= TOLERANCE and peak <= -0.9):
            print(line + ("" if a.report else "  ok"))
            continue
        d0 = duration(f)
        tmp = f.with_suffix(".lvl.mp3")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-af",
                        f"volume={gain:.2f}dB,alimiter=limit={CEILING}:level=false:attack=2:release=60",
                        "-c:a", "libmp3lame", "-b:a", "128k", str(tmp)], check=True)
        d1 = duration(tmp)
        if abs(d1 - d0) > 0.03:
            tmp.unlink()
            print(f"{line}  !! duration changed {d0:.3f} -> {d1:.3f}; left untouched")
            continue
        tmp.replace(f)
        l2, p2 = measure(f)
        meta_p = SPECS / f.stem / "meta.json"
        if meta_p.exists():
            m = json.loads(meta_p.read_text())
            m["lufs"] = round(l2, 1)
            meta_p.write_text(json.dumps(m, indent=1) + "\n")
        print(f"{line}  -> {l2:6.1f} LUFS  peak {p2:5.1f}  ({gain:+.1f} dB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
