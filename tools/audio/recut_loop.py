#!/usr/bin/env python3
"""
recut_loop.py — re-cut a remastered loop so it ENDS BEFORE a fade / dead air, with
no new generation.

ElevenLabs takes tend to fade out at the end even when told not to; the glue pass
then kept that fade inside the loop (10-30 s of near-silence before the wrap). This
finds where the music actually fades, searches for the best seam that closes the
loop before it (same intro, same loop_start ± a beat), re-cuts, and re-levels.

  python3 tools/audio/recut_loop.py <id> [<id> ...]     # re-cut, keep only if clean
  python3 tools/audio/recut_loop.py --all-flagged       # every cue dead_air.py flags

Accepts a re-cut only when: seam <= 0.45, no dead air left in the body, loop >= 30 s.
Otherwise it leaves the file alone and says so (that cue needs a re-compose).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dead_air as da  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SERVED = ROOT / "public/assets/audio/music/remaster"
SPECS = ROOT / "assets/audio/elevenlabs"
PY = sys.executable
SEAM_OK = 0.45
MIN_LOOP = 30.0


def fade_start(db: np.ndarray, at: float) -> float:
    """Walk back from the start of a low stretch to where the level began falling."""
    med = np.median(db)
    k = int(at / da.WIN)
    while k > 0 and db[k - 1] < med - 4:
        k -= 1
    return k * da.WIN


def recut(cid: str) -> bool:
    meta_p = SPECS / cid / "meta.json"
    meta = json.loads(meta_p.read_text())
    if meta.get("kind") != "loop":
        return True
    f = SERVED / f"{cid}.mp3"
    db = da.levels(f)
    ls = meta.get("loop_start") or 0.0
    secs, at = da.longest_low(db, ls)
    if secs <= da.MAX_STALL:
        print(f"{cid}: body clean")
        return True
    end = fade_start(db, at)
    if end - ls < MIN_LOOP:
        print(f"{cid}: music fades at {end:.1f}s — only {end - ls:.1f}s of loop before it; needs a re-compose")
        return False
    tmpd = Path(tempfile.mkdtemp())
    out = tmpd / "cut.mp3"
    r = subprocess.run([PY, str(ROOT / "tools/audio/make_loop.py"), str(f), str(out), "--keep-intro",
                        "--min-start", f"{max(0.0, ls - 0.3):.3f}", "--max-start", f"{ls + 0.3:.3f}",
                        "--max-end", f"{end:.3f}", "--min-len", f"{max(MIN_LOOP, (end - ls) * 0.6):.3f}",
                        "--bars-per", "1", "--bitrate", "128k"], capture_output=True, text=True)
    if r.returncode:
        print(f"{cid}: make_loop failed: {r.stderr[-300:]}")
        return False
    rep = json.loads(r.stdout[: r.stdout.rindex("}") + 1])
    db2 = da.levels(out)
    s2, a2 = da.longest_low(db2, rep["loop_start"])
    ok = rep["seam_distance"] <= SEAM_OK and s2 <= da.MAX_STALL and rep["loop_len"] >= MIN_LOOP
    verdict = "ACCEPT" if ok else "REJECT"
    print(f"{cid}: fade at {end:.1f}s -> loop {rep['loop_start']}->{rep['loop_end']} ({rep['loop_len']}s) "
          f"seam {rep['seam_distance']} stall {s2:.1f}s  {verdict}")
    if not ok:
        return False
    shutil.copy(out, f)
    meta.update({"loop_start": rep["loop_start"], "seam": rep["seam_distance"],
                 "duration": float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                   "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout)})
    meta.setdefault("edits", []).append(f"re-cut to end before the take's fade at {end:.1f}s")
    meta_p.write_text(json.dumps(meta, indent=1) + "\n")
    subprocess.run([PY, str(ROOT / "tools/audio/level_remasters.py"), cid], check=True)
    return True


def main() -> int:
    args = sys.argv[1:]
    if args == ["--all-flagged"]:
        args = []
        for p in sorted(SERVED.glob("*.mp3")):
            meta = json.loads((SPECS / p.stem / "meta.json").read_text())
            if meta.get("kind") != "loop":
                continue
            secs, _ = da.longest_low(da.levels(p), meta.get("loop_start") or 0.0)
            if secs > da.MAX_STALL:
                args.append(p.stem)
    failed = [c for c in args if not recut(c)]
    if failed:
        print("\nneeds a re-compose:", " ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
