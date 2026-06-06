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

Model note: the public API currently exposes only `music_v1`. Music v2 exists
but is early-access-only on the API as of mid-2026. The model is therefore
overridable without a code change via ELEVENLABS_MUSIC_MODEL or --model, so the
day v2 opens up you just flip the env var. See SKILL.md.

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

DEFAULT_MODEL = os.environ.get("ELEVENLABS_MUSIC_MODEL", "music_v1")
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


def _backoff_seconds(attempt: int, retry_after_header: str | None) -> float:
    if retry_after_header:
        try:
            return max(0.0, min(60.0, float(retry_after_header.strip())))
        except ValueError:
            pass
    return float(2 ** attempt)


def compose_music(
    prompt: str,
    *,
    length_ms: int | None,
    model: str,
    output_format: str,
    force_instrumental: bool,
    seed: int | None,
    max_retries: int,
) -> bytes:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise SystemExit(
            "ELEVENLABS_API_KEY is not set. Add it to the environment or a .env "
            "file at the project root."
        )

    body: dict = {
        "prompt": prompt,
        "model_id": model,
        "force_instrumental": force_instrumental,
    }
    if length_ms is not None:
        body["music_length_ms"] = length_ms
    if seed is not None:
        body["seed"] = seed

    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
    params = {"output_format": output_format}

    last_err: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            r = requests.post(
                MUSIC_ENDPOINT,
                headers=headers,
                params=params,
                json=body,
                timeout=300,
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
            return r.content
        except (requests.ConnectionError, requests.Timeout) as e:
            last_err = e
            if attempt < max_retries:
                time.sleep(_backoff_seconds(attempt, None))
                continue
            raise
    raise RuntimeError(f"All retries exhausted: {last_err}")


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
    p.add_argument("--max-retries", type=int, default=2, help="Retry count for API errors.")
    p.add_argument("--list-presets", action="store_true")
    args = p.parse_args()

    presets = load_presets()
    if args.list_presets:
        for key, meta in sorted(presets.items()):
            print(f"{key}: {meta['label']}")
            print(f"  use for: {meta['use_for']}")
        return 0

    if not args.prompt or not args.output:
        p.error("--prompt and --output are required (use --list-presets to inspect presets).")
    if not args.prompt.strip():
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
    full_prompt = args.prompt if not preset_suffix else f"{args.prompt}. {preset_suffix}"

    audio = compose_music(
        full_prompt,
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
        "prompt_chars": len(full_prompt),
    }
    print(json.dumps(info, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
