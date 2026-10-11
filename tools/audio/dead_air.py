#!/usr/bin/env python3
"""
dead_air.py — find stalls in a music cue: long near-silent stretches and fades.

A generated take often FADES OUT at its end even when told not to; glued into a
loop that becomes 10-30 s of near-silence mid-cue (the boss battle went quiet for
25 s). Used by remaster_track.py (to end a take before its fade, and to fail a
cut with dead air), recut_loop.py, and the CI audit.

  python3 tools/audio/dead_air.py [ids...]    # report every remaster (exit 1 on dead air)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SERVED = ROOT / "public/assets/audio/music/remaster"
WIN = 0.5            # seconds per level window
DROP_DB = 12.0       # "near-silent" = this far under the cue's median level
MAX_STALL = 3.0      # longest such stretch allowed inside a loop body, seconds
SR = 22050


def levels(path: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    w = int(WIN * SR)
    m = len(x) // w
    return 20 * np.log10(np.sqrt((x[: m * w].reshape(m, w) ** 2).mean(1)) + 1e-9)


def longest_low(db: np.ndarray, start_s: float = 0.0, end_s: float | None = None) -> tuple[float, float]:
    """(seconds, at) of the longest stretch DROP_DB under the median, within [start, end)."""
    med = np.median(db)
    a = int(start_s / WIN)
    b = len(db) if end_s is None else min(len(db), int(end_s / WIN))
    best = cur = 0
    at = st = a
    for k in range(a, b):
        if db[k] < med - DROP_DB:
            if cur == 0:
                st = k
            cur += 1
            if cur > best:
                best, at = cur, st
        else:
            cur = 0
    return best * WIN, at * WIN


def music_end(db: np.ndarray, min_s: float = 0.0) -> float:
    """Where the music proper ends: the start of a trailing fade/silence, if any —
    the last window still within 8 dB of the median, plus one window."""
    med = np.median(db)
    k = len(db) - 1
    while k > int(min_s / WIN) and db[k] < med - 8:
        k -= 1
    return (k + 1) * WIN


def main() -> int:
    import json
    ids = sys.argv[1:] or sorted(p.stem for p in SERVED.glob("*.mp3"))
    bad = 0
    for i in ids:
        meta_p = ROOT / "assets/audio/elevenlabs" / i / "meta.json"
        meta = json.loads(meta_p.read_text()) if meta_p.exists() else {}
        db = levels(SERVED / f"{i}.mp3")
        ls = meta.get("loop_start") or 0.0
        lead = 0.0
        while lead / WIN < len(db) and db[int(lead / WIN)] < np.median(db) - 30:
            lead += WIN
        secs, at = longest_low(db, ls if meta.get("kind") == "loop" else 0.0)
        spec_p = ROOT / "assets/audio/elevenlabs" / i / "spec.json"
        allow = json.loads(spec_p.read_text()).get("max_stall", MAX_STALL) if spec_p.exists() else MAX_STALL
        flag = []
        if meta.get("kind") == "loop" and secs > allow:
            flag.append(f"DEAD AIR {secs:.1f}s at {at:.1f}s")
        if lead > 1.0:
            flag.append(f"LEAD SILENCE {lead:.1f}s")
        bad += bool(flag)
        print(f"{i:26s} {'; '.join(flag) if flag else 'ok'}")
    print(f"\n{len(ids) - bad}/{len(ids)} cues clean")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
