#!/usr/bin/env python3
"""
build_remaster_manifest.py — collect every remastered track into the engine's
manifest (src/game/data/music-remaster.json, bundled by Vite) and the website's
music-page data.

A track is listed only when BOTH its meta.json (assets/audio/elevenlabs/<id>/)
and its served file (public/assets/audio/music/remaster/<id>.mp3) exist, so a
half-finished remaster can never reach players — MusicDirector simply keeps the
classic track for anything unlisted. Run after any remaster_track.py run.

  python3 tools/audio/build_remaster_manifest.py [--check]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPECS = ROOT / "assets/audio/elevenlabs"
SERVED = ROOT / "public/assets/audio/music/remaster"
OUT = ROOT / "src/game/data/music-remaster.json"


def build() -> dict:
    tracks = {}
    for meta_path in sorted(SPECS.glob("*/meta.json")):
        m = json.loads(meta_path.read_text())
        tid = m["id"]
        if not (SERVED / f"{tid}.mp3").exists():
            continue
        tracks[tid] = {
            "loop_start": m.get("loop_start"),
            "duration": m["duration"],
            "where": m.get("where", ""),
            "mood": m.get("mood", ""),
        }
    return {"_generated": "tools/audio/build_remaster_manifest.py — do not hand-edit", "tracks": tracks}


def main() -> int:
    data = json.dumps(build(), indent=1, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        cur = OUT.read_text() if OUT.exists() else ""
        if cur != data:
            print("music-remaster.json is stale: run python3 tools/audio/build_remaster_manifest.py")
            return 1
        print("music-remaster.json up to date")
        return 0
    OUT.write_text(data)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(json.loads(data)['tracks'])} tracks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
