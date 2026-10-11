#!/usr/bin/env python3
"""
remaster_track.py — one music spec in, one game-ready REMASTERED track out.

The "remastered" soundtrack is composed by the ElevenLabs Music API from a
per-track spec (assets/audio/elevenlabs/<id>/spec.json) written like a
composer's cue sheet: tempo, metre, palette, and a FORM — a play-once intro
followed by contrasting sections. The pipeline:

  1. spec -> composition plan (music_v2_5 chunks). If the spec opts into the
     shared MOTIF (assets/audio/elevenlabs/motif.json — the Tinderwick theme),
     the first chunk is conditioned on it, so the whole soundtrack shares a tune.
  2. compose (stored for inpainting) -> raw take.
  3. LOOP GLUE: re-render the take + a short generated [Turnaround] + the
     opening of the theme, so the end leads back into the loop by construction.
  4. make_loop.py --keep-intro finds the exact seam: the file is intro + body,
     and the engine loops back to `loop_start` (the intro never replays).
  5. writes public/assets/audio/music/remaster/<id>.mp3 + meta.json beside the
     spec. Then run build_remaster_manifest.py.

  python3 tools/audio/remaster_track.py dimglass-coast-a           # spec by id
  python3 tools/audio/remaster_track.py dimglass-coast-a --reglue  # redo only the loop glue
  python3 tools/audio/remaster_track.py --check-spec dimglass-coast-a

Spec shape (JSON):
  {
    "id": "dimglass-coast-a", "kind": "loop" | "oneshot",
    "where": "Dimglass Coast", "mood": "one line for the music page",
    "bpm": 120, "beats_per_bar": 4,
    "motif": {"strength": "low|medium|high|xhigh"} | null,
    "core_styles": [...6-12 styles, the whole cue's palette...],
    "negative_styles": [...],
    "sections": [
      {"name": "Intro", "bars": 4, "text": "{inline direction}", "styles": [...], "adherence": "high"},
      {"name": "Theme", "bars": 8, ...}, ...
    ]
  }
For a loop the FIRST section is the play-once intro. A oneshot (sting, fanfare,
cinematic cue) is composed straight through, trimmed, and never loops.

API calls go through generate_music.py's machine-wide slot lock (2 at a time),
so any number of these can run in parallel.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/generate-music/scripts"))
import generate_music as gm  # noqa: E402

SPECS = ROOT / "assets/audio/elevenlabs"
SERVED = ROOT / "public/assets/audio/music/remaster"
MOTIF = SPECS / "motif.json"
MODEL = "music_v2_5"
SEAM_OK = 0.45          # make_loop seam distance; hand-built loops ~0.03, good glue ~0.1-0.2
TURNAROUND_MS = 4000
STRENGTHS = {"low", "medium", "high", "xhigh"}


def bar_ms(spec: dict) -> float:
    return spec.get("beats_per_bar", 4) * 60000.0 / spec["bpm"]


def check_spec(spec: dict) -> list[str]:
    errs = []
    for k in ("id", "kind", "where", "mood", "bpm", "core_styles", "sections"):
        if k not in spec:
            errs.append(f"missing '{k}'")
    if spec.get("kind") not in ("loop", "oneshot"):
        errs.append("kind must be loop|oneshot")
    secs = spec.get("sections", [])
    if not secs or len(secs) > 25:
        errs.append("1..25 sections")
    if spec.get("kind") == "loop" and len(secs) < 3:
        errs.append("a loop needs an intro + at least two body sections (contrast + return)")
    bm = bar_ms(spec) if spec.get("bpm") else 0
    total = 0
    for s in secs:
        d = s.get("bars", 0) * bm
        total += d
        if not 3000 <= d <= 120000:
            errs.append(f"section {s.get('name')}: {d:.0f} ms outside 3000..120000 (bars x tempo)")
        if s.get("adherence", "high") not in ("low", "medium", "high"):
            errs.append(f"section {s.get('name')}: adherence low|medium|high")
    if spec.get("kind") == "loop" and not 40000 <= total <= 240000:
        errs.append(f"loop total {total/1000:.0f}s; aim 60-150s (40-240 allowed)")
    m = spec.get("motif")
    if m and m.get("strength") not in STRENGTHS:
        errs.append("motif.strength low|medium|high|xhigh")
    if len(spec.get("core_styles", [])) < 6:
        errs.append("give at least 6 core_styles (the first chunk sets the whole cue)")
    blob = json.dumps(spec).lower()
    for brand in ("pokemon", "pokémon", "nintendo", "zelda", "final fantasy", "uematsu", "masuda", "kondo",
                  "square", "capcom", "sega", "donkey kong", "mario", "chrono", "game freak"):
        if brand in blob:
            errs.append(f"brand/composer name '{brand}' in spec — describe the era/craft instead (and the API rejects it)")
    return errs


def build_plan(spec: dict) -> dict:
    bm = bar_ms(spec)
    core = list(spec["core_styles"])
    neg = list(spec.get("negative_styles", [])) or ["vocals"]
    if "vocals" not in neg:
        neg.append("vocals")
    motif = json.loads(MOTIF.read_text()) if spec.get("motif") else None
    chunks = []
    for i, s in enumerate(spec["sections"]):
        text = f"[{s['name']}]"
        if s.get("text"):
            text += "\n" + s["text"]
        c = {
            "text": text,
            "duration_ms": int(round(s["bars"] * bm)),
            "positive_styles": core + list(s.get("styles", [])),
            "negative_styles": neg + list(s.get("negative", [])),
            "context_adherence": s.get("adherence", "high"),
        }
        if i == 0 and motif:
            c["conditioning_ref"] = {"song_id": motif["song_id"], "range": motif["range"]}
            c["condition_strength"] = spec["motif"]["strength"]
        chunks.append(c)
    return {"chunks": chunks}


def compose(plan: dict, out: Path, store: bool) -> str | None:
    audio, song_id = gm.compose_music(
        None, plan=plan, store=store, length_ms=None, model=MODEL,
        output_format="mp3_44100_128", force_instrumental=True, seed=None, max_retries=6,
    )
    out.write_bytes(audio)
    return song_id


def duration(path: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip())


TAIL_MS = 20000         # how much of the take's ending the glue pass re-renders as context
SPLICE_AT_S = 6.0       # where in the glue output we splice back onto the original take
SPLICE_XF_S = 1.5       # equal-power crossfade at the splice


def glue_plan(spec: dict, song_id: str, total_ms: int, intro_ms: int) -> dict:
    """Cheap loop glue: only the take's last TAIL_MS as context, a generated
    [Turnaround], then the theme's opening — ~34 s of audio instead of re-rendering
    the whole song. The output is spliced back onto the original take."""
    tail0 = max(intro_ms, total_ms - TAIL_MS)
    return {"chunks": [
        {"song_id": song_id, "range": {"start_ms": tail0, "end_ms": total_ms}},
        {
            "text": "[Turnaround]\n{a short turnaround that leads smoothly straight back into the main theme, same tempo and key}",
            "duration_ms": TURNAROUND_MS,
            "positive_styles": list(spec["core_styles"]) + ["seamless transition back to the theme"],
            "negative_styles": ["vocals", "ending", "fade out", "silence", "ritardando", "final cadence"],
            "context_adherence": "high",
        },
        {"song_id": song_id, "range": {"start_ms": intro_ms, "end_ms": min(total_ms, intro_ms + 10000)}},
    ]}


def _pcm(path: Path, sr: int = 44100) -> "np.ndarray":
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


def splice(raw: Path, glue: Path, out_wav: Path, total_ms: int) -> None:
    """raw[0 : tail0+SPLICE_AT] ⊕ glue[SPLICE_AT:] with the glue aligned to the take
    by cross-correlation (re-rendered reference audio drifts by tens of ms)."""
    import numpy as np
    sr = 44100
    R, G = _pcm(raw), _pcm(glue)
    tail0 = max(0, total_ms - TAIL_MS) / 1000
    g_at = int(SPLICE_AT_S * sr)
    r_guess = int((tail0 + SPLICE_AT_S) * sr)
    probe = G[g_at:g_at + sr, 0]
    lo = max(0, r_guess - int(0.25 * sr))
    seg = R[lo:r_guess + int(0.25 * sr) + sr, 0]
    n = len(seg) + len(probe)
    c = np.fft.irfft(np.fft.rfft(seg, n) * np.conj(np.fft.rfft(probe, n)), n)[: len(seg) - len(probe)]
    r_at = lo + int(np.argmax(c))
    xf = int(SPLICE_XF_S * sr)
    ramp = np.linspace(0, 1, xf, dtype=np.float32)[:, None]
    head = R[:r_at].copy()
    blend = R[r_at:r_at + xf] * np.sqrt(1 - ramp) + G[g_at:g_at + xf] * np.sqrt(ramp)
    out = np.concatenate([head, blend, G[g_at + xf:]])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(sr), "-i", "-", str(out_wav)],
                   input=np.clip(out, -1, 1).astype(np.float32).tobytes(), check=True)


def make_loop(raw: Path, out: Path, intro_s: float, body_s: float) -> dict:
    cmd = [sys.executable, str(ROOT / "tools/audio/make_loop.py"), str(raw), str(out),
           "--keep-intro", "--min-start", f"{max(0.0, intro_s - 2.5):.3f}", "--max-start", f"{intro_s + 4:.3f}",
           "--min-len", f"{max(20.0, body_s - 8):.3f}", "--bars-per", "1", "--bitrate", "128k"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"make_loop failed: {r.stderr[-800:]}")
    rep = json.loads(r.stdout[: r.stdout.rindex("}") + 1])
    return rep


def oneshot_finish(raw: Path, out: Path) -> None:
    # trim trailing silence, short tail fade, 128k stereo
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af",
                    "areverse,silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.15,areverse",
                    "-c:a", "libmp3lame", "-b:a", "128k", str(out)], check=True)
    d = duration(out)
    tmp = out.with_suffix(".tmp.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-af", f"afade=t=out:st={max(0, d - 0.25):.3f}:d=0.25",
                    "-c:a", "libmp3lame", "-b:a", "128k", str(tmp)], check=True)
    tmp.replace(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--check-spec", action="store_true")
    ap.add_argument("--reglue", action="store_true", help="reuse the stored take (meta.song_id), redo glue + cut")
    ap.add_argument("--work", default=None, help="scratch dir for raw takes (default: system temp)")
    ap.add_argument("--glue-tries", type=int, default=2)
    a = ap.parse_args()

    d = SPECS / a.id
    spec = json.loads((d / "spec.json").read_text())
    errs = check_spec(spec)
    if errs:
        print("SPEC ERRORS:\n  " + "\n  ".join(errs))
        return 1
    if a.check_spec:
        plan = build_plan(spec)
        print(f"spec OK: {len(plan['chunks'])} chunks, {sum(c['duration_ms'] for c in plan['chunks'])/1000:.1f}s")
        return 0

    work = Path(a.work or tempfile.gettempdir()) / "remaster" / a.id
    work.mkdir(parents=True, exist_ok=True)
    SERVED.mkdir(parents=True, exist_ok=True)
    out = SERVED / f"{a.id}.mp3"
    meta_path = d / "meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    plan = build_plan(spec)
    (d / "plan.json").write_text(json.dumps(plan, indent=1) + "\n")
    t0 = time.time()

    if spec["kind"] == "oneshot":
        raw = work / "raw.mp3"
        song_id = compose(plan, raw, store=False)
        oneshot_finish(raw, out)
        meta = {"id": a.id, "kind": "oneshot", "where": spec["where"], "mood": spec["mood"],
                "duration": round(duration(out), 3), "loop_start": None, "song_id": song_id}
    else:
        raw = work / "raw.mp3"
        if a.reglue and meta.get("song_id"):
            if not raw.exists():
                raise SystemExit(f"--reglue needs the original take at {raw} (it lives in the scratch dir only)")
            song_id = meta["song_id"]
            total_ms = meta["raw_ms"]
        else:
            song_id = compose(plan, raw, store=True)
            if not song_id:
                raise SystemExit("no song-id header returned; cannot glue")
            total_ms = int(round(duration(raw) * 1000))
        intro_ms = plan["chunks"][0]["duration_ms"]
        body_s = (total_ms - intro_ms) / 1000
        best = None
        for k in range(a.glue_tries):
            g = glue_plan(spec, song_id, total_ms, intro_ms)
            (d / "glue_plan.json").write_text(json.dumps(g, indent=1) + "\n")
            graw = work / f"glue{k}.mp3"
            compose(g, graw, store=False)
            joined = work / f"joined{k}.wav"
            splice(raw, graw, joined, total_ms)
            cand = work / f"cut{k}.mp3"
            rep = make_loop(joined, cand, intro_ms / 1000, body_s)
            print(f"  glue try {k}: seam {rep['seam_distance']} loop {rep['loop_start']}->{rep['loop_end']}")
            if best is None or rep["seam_distance"] < best[0]["seam_distance"]:
                best = (rep, cand)
            if rep["seam_distance"] <= SEAM_OK:
                break
        rep, cand = best
        cand.replace(out)
        meta = {"id": a.id, "kind": "loop", "where": spec["where"], "mood": spec["mood"],
                "duration": round(duration(out), 3), "loop_start": rep["loop_start"],
                "seam": rep["seam_distance"], "bpm_est": rep["bpm_est"],
                "song_id": song_id, "raw_ms": total_ms,
                "motif": (spec.get("motif") or {}).get("strength")}
        if rep["seam_distance"] > SEAM_OK:
            meta["warning"] = f"seam {rep['seam_distance']} > {SEAM_OK}: listen to the join, consider --reglue"
    meta_path.write_text(json.dumps(meta, indent=1) + "\n")
    print(json.dumps(meta, indent=1))
    print(f"done in {time.time() - t0:.0f}s -> {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
