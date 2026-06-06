#!/usr/bin/env python3
"""
Fetch a SoundFont (.sf2) for the generate-midi skill's lush `--engine soundfont`
render path.

SoundFonts are too big to commit, so they're downloaded on demand into
assets/audio/midi/soundfonts/ (gitignored) and re-fetched per fresh container.
The chip engine needs none of this; only the optional soundfont render does.

  ./venv/bin/python .claude/skills/generate-midi/scripts/fetch_soundfont.py            # GeneralUser GS
  ./venv/bin/python .claude/skills/generate-midi/scripts/fetch_soundfont.py --name vintage
  ./venv/bin/python .claude/skills/generate-midi/scripts/fetch_soundfont.py --list

All entries are freely redistributable; the license note is printed on fetch.
"""
from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def repo_root() -> Path:
    for d in SCRIPT_DIR.parents:
        if (d / ".git").exists() or (d / "requirements.txt").is_file():
            return d
    return SCRIPT_DIR.parents[-1]


SOUNDFONT_DIR = repo_root() / "assets" / "audio" / "midi" / "soundfonts"

# Known-good, reachable, freely-redistributable soundfonts.
REGISTRY: dict[str, dict] = {
    "generaluser": {
        "filename": "GeneralUser-GS.sf2",
        "url": "https://github.com/mrbumpy409/GeneralUser-GS/raw/main/GeneralUser-GS.sf2",
        "approx_mb": 31,
        "license": "GeneralUser GS by S. Christian Collins — free to use and "
                   "redistribute (see the project's license). High-quality full "
                   "General MIDI bank; the recommended default.",
    },
    "vintage": {
        "filename": "VintageDreams.sf2",
        "url": "https://github.com/FluidSynth/fluidsynth/raw/master/sf2/VintageDreamsWaves-v2.sf2",
        "approx_mb": 0.3,
        "license": "Vintage Dreams Waves v2 by Ian Wilson — public domain. Tiny "
                   "128-preset, synth-flavoured GM set; a fast lightweight fallback.",
    },
}

DEFAULT = "generaluser"


def looks_like_sf2(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            head = f.read(16)
        return head[:4] == b"RIFF" and b"sfbk" in head
    except OSError:
        return False


def fetch(name: str, force: bool) -> int:
    entry = REGISTRY.get(name)
    if entry is None:
        raise SystemExit(f"unknown soundfont '{name}'. Options: {', '.join(REGISTRY)}")
    SOUNDFONT_DIR.mkdir(parents=True, exist_ok=True)
    dest = SOUNDFONT_DIR / entry["filename"]
    if dest.is_file() and not force and looks_like_sf2(dest):
        print(f"already present: {dest} ({dest.stat().st_size // 1024} KiB)")
        print(f"license: {entry['license']}")
        return 0

    print(f"downloading {name} (~{entry['approx_mb']} MB) -> {dest}")
    last_err: Exception | None = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(entry["url"], headers={"User-Agent": "pixelkin-midi"})
            with urllib.request.urlopen(req, timeout=120) as r, dest.open("wb") as f:
                while True:
                    chunk = r.read(1 << 16)
                    if not chunk:
                        break
                    f.write(chunk)
            break
        except Exception as e:  # noqa: BLE001 — network is best-effort, retry
            last_err = e
            wait = 2 ** attempt
            print(f"  attempt {attempt + 1} failed ({e}); retrying in {wait}s", file=sys.stderr)
            import time
            time.sleep(wait)
    else:
        raise SystemExit(f"download failed after retries: {last_err}")

    if not looks_like_sf2(dest):
        dest.unlink(missing_ok=True)
        raise SystemExit(
            "downloaded file isn't a valid .sf2 (RIFF/sfbk header missing). "
            "The host may have returned an error page; try --name vintage or "
            "pass your own .sf2 to `render --soundfont`."
        )
    print(f"done: {dest} ({dest.stat().st_size // 1024} KiB)")
    print(f"license: {entry['license']}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch a SoundFont for generate-midi.")
    p.add_argument("--name", default=DEFAULT, help=f"Which soundfont (default {DEFAULT}).")
    p.add_argument("--force", action="store_true", help="Re-download even if present.")
    p.add_argument("--list", action="store_true", help="List available soundfonts.")
    args = p.parse_args()

    if args.list:
        print(f"soundfonts (-> {SOUNDFONT_DIR}):")
        for key, e in REGISTRY.items():
            tag = " (default)" if key == DEFAULT else ""
            print(f"  {key}{tag}: {e['filename']} ~{e['approx_mb']} MB")
            print(f"      {e['license']}")
        return 0
    return fetch(args.name, args.force)


if __name__ == "__main__":
    sys.exit(main())
