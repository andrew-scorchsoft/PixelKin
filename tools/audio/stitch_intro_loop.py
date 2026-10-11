#!/usr/bin/env python3
"""
stitch_intro_loop.py — a CLASSIC (chip) cue with a play-once intro + a looping body.

The chip renders are normally one self-contained loop that the engine repeats
whole. Some cues want a head that plays ONCE and then a body that loops (the
trainer-spots-you startle → the "get ready" loop). This renders two generate-midi
masters through the same chip engine — the intro and the body, each a `loop:true`
spec so both are cut sample-exactly at their last bar line (no ring-out tail) —
normalises them TOGETHER (one gain, so the head and the body sit at the same
level), butts them into ONE file, and records where the body starts in
`src/game/data/music-classic.json`:

    { "tracks": { "<id>": { "loop_start": <s>, "duration": <s> } } }

`MusicDirector` reads that table for the classic score exactly like the remaster
manifest: intro [0, loop_start) once, then [loop_start, end) looped, gapless.

    python3 tools/audio/stitch_intro_loop.py --id trainer-eyes \\
        --intro assets/audio/midi/trainer-eyes-intro.mid \\
        --body  assets/audio/midi/trainer-eyes-loop.mid

writes public/assets/audio/music/<id>.mp3 and updates the table. `--preview out.mp3`
also renders intro + 3 body passes for a listen.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MIDI_PY = ROOT / ".claude/skills/generate-midi/scripts/midi.py"
TABLE = ROOT / "src/game/data/music-classic.json"
MUSIC_DIR = ROOT / "public/assets/audio/music"


def load_midi_module():
    spec = importlib.util.spec_from_file_location("pk_midi", MIDI_PY)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def render_raw(midi, profiles, path: Path):
    """One pass of a loop master, NOT normalised (midi._finalize normalises per
    file; we want one shared gain across the intro and the body)."""
    real = midi._finalize

    def raw(buf, body_sec, tail_sec, loops, fade_out):  # noqa: ARG001 — same signature
        n = max(1, int(body_sec * midi.SAMPLE_RATE))
        return buf[:n].copy()

    midi._finalize = raw
    try:
        buf, _rev, is_loop = midi.render_audio(path, profiles, reverb=None, loops=1, fade_out=0.0)
    finally:
        midi._finalize = real
    if not is_loop:
        raise SystemExit(f"{path}: build it from a loop:true spec so it is cut at the bar line")
    return buf


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", required=True, help="cue id: writes public/assets/audio/music/<id>.mp3")
    ap.add_argument("--intro", required=True, type=Path)
    ap.add_argument("--body", required=True, type=Path)
    ap.add_argument("--preview", type=Path, default=None, help="also write intro + 3 body passes here")
    ap.add_argument("--bitrate", default="160k")
    args = ap.parse_args()

    import numpy as np

    midi = load_midi_module()
    profiles = midi.load_profiles()
    intro = render_raw(midi, profiles, args.intro)
    body = render_raw(midi, profiles, args.body)

    # A 4 ms fade on the intro's last samples: its notes and echo are cut at the
    # bar line, and the body's downbeat lands right on top — no click at the join.
    fn = int(0.004 * midi.SAMPLE_RATE)
    intro[-fn:] *= np.linspace(1.0, 0.0, fn, dtype=np.float32)

    # The same normalise + soft-clip midi._finalize applies, once over both parts.
    peak = float(max(np.max(np.abs(intro)), np.max(np.abs(body)))) or 1.0
    shape = lambda x: np.tanh(x / peak * 0.89 * 1.1).astype(np.float32)  # noqa: E731
    intro, body = shape(intro), shape(body)

    out = MUSIC_DIR / f"{args.id}.mp3"
    midi.write_mp3(out, np.concatenate([intro, body]), args.bitrate)
    if args.preview:
        midi.write_mp3(args.preview, np.concatenate([intro, body, body, body]), args.bitrate)

    sr = midi.SAMPLE_RATE
    loop_start = round(len(intro) / sr, 4)
    duration = round((len(intro) + len(body)) / sr, 4)
    table = json.loads(TABLE.read_text()) if TABLE.exists() else {}
    tracks = table.get("tracks", {})
    tracks[args.id] = {"loop_start": loop_start, "duration": duration}
    table = {
        "_generated": "tools/audio/stitch_intro_loop.py — classic cues with a play-once intro",
        "tracks": dict(sorted(tracks.items())),
    }
    TABLE.write_text(json.dumps(table, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"path": str(out.relative_to(ROOT)), "loop_start": loop_start, "duration": duration,
                      "bytes": out.stat().st_size}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
