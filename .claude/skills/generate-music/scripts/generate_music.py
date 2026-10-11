#!/usr/bin/env python3
"""
Music generation helper for the generate-music skill.

Calls the ElevenLabs Music API to compose a track from a text prompt and writes
it to disk. Built for game music: instrumental by default, loop-minded prompts,
and a small preset library of moods that fit PixelKin's handheld-RPG world
(overworld, town, battle, victory, cave, title, ...).

API: POST https://api.elevenlabs.io/v1/music
  - Header:  xi-api-key: <ELEVENLABS_API_KEY>
  - Body:    { prompt, music_length_ms, model_id, force_instrumental, seed }
  - Returns: binary audio (mp3 by default) on success.

Model note (API reference re-checked 2026-10): model_id is one of `music_v1`
(the API default), `music_v2`, `music_v2_5`. We default to `music_v2_5`, the best
for prompt adherence and audio quality. Overridable via ELEVENLABS_MUSIC_MODEL or
--model. The account allows 2 concurrent requests; 429s are retried with backoff.
For loops, cut the render with tools/audio/make_loop.py. See SKILL.md.

The script does NOT judge the result. The calling agent (Claude) is expected to
listen to / inspect the output and re-invoke with an adjusted --prompt if it
doesn't fit the brief.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
PRESETS_PATH = SCRIPT_DIR / "presets.json"

MUSIC_ENDPOINT = "https://api.elevenlabs.io/v1/music"

DEFAULT_MODEL = os.environ.get("ELEVENLABS_MUSIC_MODEL", "music_v2_5")
# Default output format. mp3_44100_128 is available on all tiers; 192kbps needs
# Creator tier or above. Overridable via --output-format.
DEFAULT_OUTPUT_FORMAT = os.environ.get("ELEVENLABS_MUSIC_OUTPUT_FORMAT", "mp3_44100_128")

# API limits (compose-from-prompt): 3s .. 10min.
MIN_LENGTH_MS = 3_000
MAX_LENGTH_MS = 600_000


def _load_env_files() -> None:
    """Load .env from the nearest project root so the script works without the
    caller pre-exporting keys. Existing environment variables always win."""
    candidates: list[Path] = []
    cwd = Path.cwd().resolve()
    for d in (cwd, *cwd.parents):
        candidates.append(d / ".env")
        if (d / ".git").exists() or (d / "requirements.txt").exists():
            break
    for d in SCRIPT_DIR.parents:
        candidates.append(d / ".env")
        if (d / ".git").exists():
            break

    seen: set[Path] = set()
    try:
        from dotenv import load_dotenv  # type: ignore
        for path in candidates:
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            load_dotenv(path, override=False)
        return
    except ImportError:
        pass

    for path in candidates:
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        try:
            for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                if line.startswith("export "):
                    line = line[7:].lstrip()
                key, _, value = line.partition("=")
                key = key.strip()
                if not key or not key.replace("_", "").isalnum():
                    continue
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                    value = value[1:-1]
                os.environ.setdefault(key, value)
        except OSError:
            continue


_load_env_files()


def load_presets() -> dict:
    with PRESETS_PATH.open() as f:
        return json.load(f)["presets"]


def resolve_preset(preset: str | None, presets: dict) -> str:
    if not preset:
        return ""
    if preset not in presets:
        raise SystemExit(
            f"Unknown preset '{preset}'. Available: {', '.join(sorted(presets))}"
        )
    return presets[preset]["prompt_suffix"]


import contextlib
import fcntl
import tempfile

SLOT_DIR = Path(os.environ.get("ELEVENLABS_SLOT_DIR", Path(tempfile.gettempdir()) / "elevenlabs-music-slots"))
MAX_CONCURRENT = int(os.environ.get("ELEVENLABS_MAX_CONCURRENT", "2"))


@contextlib.contextmanager
def api_slot():
    """Machine-wide semaphore (flock on N slot files) so parallel agents/processes
    never exceed the account's concurrent-request cap (2) and 429 each other."""
    SLOT_DIR.mkdir(parents=True, exist_ok=True)
    while True:
        for i in range(MAX_CONCURRENT):
            f = open(SLOT_DIR / f"slot{i}.lock", "w")
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                f.close()
                continue
            try:
                yield
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
                f.close()
            return
        time.sleep(1.0)


def _backoff_seconds(attempt: int, retry_after_header: str | None) -> float:
    if retry_after_header:
        try:
            return max(0.0, min(60.0, float(retry_after_header.strip())))
        except ValueError:
            pass
    return float(5 * (attempt + 1))  # a 429 here is usually the 2-concurrent cap


def compose_music(
    prompt: str | None,
    *,
    plan: dict | None = None,
    store: bool = False,
    length_ms: int | None,
    model: str,
    output_format: str,
    force_instrumental: bool,
    seed: int | None,
    max_retries: int,
) -> tuple[bytes, str | None]:
    """Returns (audio, song_id). song_id comes from the `song-id` response header
    and is what a later composition plan's `conditioning_ref` points at."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise SystemExit(
            "ELEVENLABS_API_KEY is not set. Add it to the environment or a .env "
            "file at the project root."
        )

    body: dict = {"model_id": model}
    if plan is not None:
        # composition_plan mode: no prompt/length/force_instrumental allowed;
        # instrumental-ness rides the chunk styles (negative "vocals").
        body["composition_plan"] = plan
        if seed is not None:
            body["seed"] = seed
    else:
        body["prompt"] = prompt
        body["force_instrumental"] = force_instrumental
        if length_ms is not None:
            body["music_length_ms"] = length_ms
        if seed is not None:
            print("note: the API rejects seed with a prompt; ignoring --seed", file=sys.stderr)
    if store:
        body["store_for_inpainting"] = True

    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
    params = {"output_format": output_format}

    last_err: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            with api_slot():
                r = requests.post(
                    MUSIC_ENDPOINT,
                    headers=headers,
                    params=params,
                    json=body,
                    timeout=600,
                )
            if r.status_code >= 500 or r.status_code == 429:
                last_err = RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
                if attempt < max_retries:
                    time.sleep(_backoff_seconds(attempt, r.headers.get("Retry-After")))
                    continue
            if not r.ok:
                # Surface the API's own error message — it usually explains the
                # exact problem (bad length, tier-gated format, moderation, ...).
                raise SystemExit(
                    f"ElevenLabs Music API error {r.status_code}: {r.text[:500]}"
                )
            # Guard against an error JSON sneaking through with a 200.
            ctype = r.headers.get("Content-Type", "")
            if "application/json" in ctype:
                raise SystemExit(
                    f"Expected audio but got JSON: {r.text[:500]}"
                )
            return r.content, r.headers.get("song-id")
        except (requests.ConnectionError, requests.Timeout) as e:
            last_err = e
            if attempt < max_retries:
                time.sleep(_backoff_seconds(attempt, None))
                continue
            raise
    raise RuntimeError(f"All retries exhausted: {last_err}")


def upload_song(path: Path, model: str) -> dict:
    """POST /v1/music/upload — store OUR OWN audio (e.g. an approved theme) so plans
    can condition on it. Costs like a generation. Returns {song_id, composition_plan}."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise SystemExit("ELEVENLABS_API_KEY is not set.")
    with path.open("rb") as f, api_slot():
        r = requests.post(
            MUSIC_ENDPOINT + "/upload",
            headers={"xi-api-key": api_key},
            data={"extract_composition_plan": model},
            files={"file": (path.name, f, "audio/mpeg")},
            timeout=600,
        )
    if not r.ok:
        raise SystemExit(f"ElevenLabs upload error {r.status_code}: {r.text[:500]}")
    return r.json()


def main() -> int:
    p = argparse.ArgumentParser(description="Generate music via the ElevenLabs Music API.")
    p.add_argument("--prompt", help="The music brief. Required unless --list-presets.")
    p.add_argument("--output", help="Output path (.mp3). Required unless --list-presets.")
    p.add_argument("--preset", default=None, help="Mood preset key (see --list-presets).")
    p.add_argument(
        "--length", type=int, default=None, metavar="SECONDS",
        help="Track length in seconds (3..600). Omit to let the model decide.",
    )
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"Model id (default {DEFAULT_MODEL}).")
    p.add_argument(
        "--output-format", default=DEFAULT_OUTPUT_FORMAT,
        help=f"ElevenLabs output_format (default {DEFAULT_OUTPUT_FORMAT}).",
    )
    p.add_argument(
        "--vocals", action="store_true",
        help="Allow vocals. Default is instrumental, which is what game loops want.",
    )
    p.add_argument("--seed", type=int, default=None, help="Seed for reproducible output.")
    p.add_argument("--max-retries", type=int, default=6, help="Retry count for API errors.")
    p.add_argument("--plan", help="Composition-plan JSON file ({chunks:[...]} for v2/v2.5). Replaces --prompt.")
    p.add_argument("--store", action="store_true", help="store_for_inpainting: keep the song referenceable by song_id.")
    p.add_argument("--upload", metavar="AUDIO", help="Upload our own audio for conditioning/inpainting; prints song_id + extracted plan.")
    p.add_argument("--list-presets", action="store_true")
    args = p.parse_args()

    presets = load_presets()
    if args.list_presets:
        for key, meta in sorted(presets.items()):
            print(f"{key}: {meta['label']}")
            print(f"  use for: {meta['use_for']}")
        return 0

    if args.upload:
        res = upload_song(Path(args.upload), args.model)
        out = json.dumps(res, indent=2)
        if args.output:
            Path(args.output).write_text(out)
        print(out)
        return 0

    plan = None
    if args.plan:
        plan = json.loads(Path(args.plan).read_text())
        plan = plan.get("composition_plan", plan)
    if (not args.prompt and plan is None) or not args.output:
        p.error("--output and one of --prompt/--plan are required (use --list-presets to inspect presets).")
    if args.prompt is not None and not args.prompt.strip():
        p.error("--prompt must not be empty or whitespace.")

    length_ms: int | None = None
    if args.length is not None:
        length_ms = args.length * 1000
        if not MIN_LENGTH_MS <= length_ms <= MAX_LENGTH_MS:
            p.error(
                f"--length must be {MIN_LENGTH_MS // 1000}..{MAX_LENGTH_MS // 1000} seconds, "
                f"got {args.length}."
            )

    out_path = Path(args.output).expanduser().resolve()
    if out_path.suffix.lower() != ".mp3":
        # The default output_format is mp3; warn rather than hard-fail so custom
        # --output-format (pcm/opus) can still pick its own extension on purpose.
        print(
            f"warning: output extension is '{out_path.suffix}', expected '.mp3' "
            f"for the default mp3 output format.",
            file=sys.stderr,
        )

    preset_suffix = resolve_preset(args.preset, presets)
    full_prompt = None
    if plan is None:
        full_prompt = args.prompt if not preset_suffix else f"{args.prompt}. {preset_suffix}"

    audio, song_id = compose_music(
        full_prompt,
        plan=plan,
        store=args.store,
        length_ms=length_ms,
        model=args.model,
        output_format=args.output_format,
        force_instrumental=not args.vocals,
        seed=args.seed,
        max_retries=args.max_retries,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(audio)

    info = {
        "path": str(out_path),
        "bytes": out_path.stat().st_size,
        "model": args.model,
        "output_format": args.output_format,
        "preset": args.preset,
        "length_seconds": args.length,
        "instrumental": not args.vocals,
        "seed": args.seed,
        "song_id": song_id,
        "plan": args.plan,
        "prompt_chars": len(full_prompt or ""),
    }
    print(json.dumps(info, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
