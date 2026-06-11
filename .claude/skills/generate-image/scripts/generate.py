#!/usr/bin/env python3
"""
Image generation helper for the generate-image skill.

Picks provider from environment:
  - GOOGLE_AI_STUDIO_API_KEY -> Google Gemini "Nano Banana Pro"  (preferred)
  - OPENAI_API_KEY           -> OpenAI gpt-image-2               (fallback)

Supports optional --input-image flags for image-as-context workflows: edit,
restyle, composition, or pure visual reference. Google routes input images
through Gemini's multimodal contents.parts API. OpenAI has two routes,
selectable with --openai-route:

  - "edits" (default) -> /v1/images/edits with gpt-image-2. One-shot. The
    endpoint name is misleading — with gpt-image-1/2 it accepts multiple
    images and the *prompt* decides whether they're edited, restyled, or
    used as pure visual reference.
  - "responses"       -> /v1/responses with the image_generation tool. The
    input images go in as conversational multimodal context on a text model
    (default gpt-5); the model then calls the image_generation tool to
    produce the output. Better mental model when the images are background
    context rather than the subject.

Pipeline: request -> decode -> strip standard metadata (EXIF/XMP/PNG text
chunks; SynthID and C2PA Content Credentials are intentionally preserved) ->
re-encode to WebP -> write to disk.

The script does NOT do semantic verification. The calling agent (Claude) is
expected to open the saved image, judge whether it matches the brief, and
re-invoke this script with an adjusted --prompt if not. See SKILL.md.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import requests
from PIL import Image

# Chroma-key colour for --transparent mode. Pure magenta is the standard
# choice: it practically never appears in line illustrations or brand
# palettes, so keying it out doesn't eat real content. RGB (255, 0, 255).
CHROMA_KEY_RGB = (255, 0, 255)
CHROMA_KEY_HEX = "#FF00FF"

# Anti-checkerboard preamble for --transparent. Image models tend to *draw*
# the checkerboard "transparency" indicator into the pixels when asked for a
# transparent background — this preamble forbids that explicitly and
# substitutes a known chroma-key colour we strip in post-processing.
TRANSPARENT_PREAMBLE = (
    f"Render the artwork on a SOLID FLAT UNIFORM background of pure magenta, "
    f"hex {CHROMA_KEY_HEX} (R=255 G=0 B=255), edge-to-edge. The magenta is a "
    f"chroma-key fill that will be removed in post-processing to produce a "
    f"transparent PNG. CRITICAL RULES: "
    f"(1) The background must be a single flat colour — not a checkerboard, "
    f"not a transparency grid, not chequered squares, not a pattern of any "
    f"kind. "
    f"(2) Do not use magenta, pink, or any near-magenta hue anywhere inside "
    f"the foreground subject — those pixels will be deleted. "
    f"(3) Do not draw a frame, border, card, vignette, or shadow plate around "
    f"the subject. The subject sits directly on the magenta. "
    f"(4) Avoid soft pink/lavender halos around the subject — keep edges "
    f"crisp."
)

SCRIPT_DIR = Path(__file__).resolve().parent
STYLES_PATH = SCRIPT_DIR / "styles.json"


def _load_env_files() -> None:
    """Load .env from the nearest project root so the script works without
    the caller pre-exporting keys. Prefers python-dotenv if installed; falls
    back to a minimal parser that ignores comments, blank lines, and decorative
    separator lines (no `=`). Existing environment variables always win."""
    candidates: list[Path] = []
    cwd = Path.cwd().resolve()
    for d in (cwd, *cwd.parents):
        candidates.append(d / ".env")
        if (d / ".git").exists() or (d / "pyproject.toml").exists() or (d / "requirements.txt").exists():
            break
    # Also check upward from the script itself (covers `python /abs/path/generate.py` from anywhere).
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

_OPENAI_MODEL_OVERRIDE = os.environ.get("OPENAI_IMAGE_MODEL")
DEFAULT_OPENAI_MODEL = _OPENAI_MODEL_OVERRIDE or "gpt-image-2"
# gpt-image-2 does not support background=transparent; gpt-image-1 does. When
# --transparent is requested and the caller hasn't hard-pinned a model (via
# OPENAI_IMAGE_MODEL), fall back to gpt-image-1 automatically.
TRANSPARENT_OPENAI_MODEL = _OPENAI_MODEL_OVERRIDE or "gpt-image-1"
DEFAULT_GOOGLE_MODEL = os.environ.get("GOOGLE_IMAGE_MODEL", "gemini-3-pro-image-preview")
# Multimodal text model used by the --openai-route=responses path. It needs
# to be a model that "sees" input_image parts and supports the
# image_generation tool — i.e. a current GPT-5-family text model, not an
# image model. Overridable via env for new releases.
DEFAULT_OPENAI_RESPONSES_MODEL = os.environ.get("OPENAI_RESPONSES_MODEL", "gpt-5")

OPENAI_ENDPOINT = "https://api.openai.com/v1/images/generations"
OPENAI_EDIT_ENDPOINT = "https://api.openai.com/v1/images/edits"
OPENAI_RESPONSES_ENDPOINT = "https://api.openai.com/v1/responses"
GOOGLE_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# Recognised input-image MIME types. The image endpoints on both providers
# accept a small, well-known set; anything else gets rejected server-side
# with an opaque error, so we filter at the client. GIF is deliberately
# excluded — neither OpenAI's /v1/images/edits (gpt-image-1/2) nor Gemini's
# image-generation endpoint document it as a supported input MIME.
_INPUT_IMAGE_MIME = {
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}

# Per-input file size limits. OpenAI caps each image at 50MB on /edits;
# Gemini caps inline data at roughly 20MB before requiring the Files API.
# We pick the tighter of the two so the same input works on either provider
# without a surprise switch-by-switch failure. The min guards against
# 0-byte / truncated files that look like images by extension.
_MIN_INPUT_BYTES = 100
_MAX_INPUT_BYTES = 20 * 1024 * 1024  # 20 MiB

# Aspect-ratio -> OpenAI size string. OpenAI gpt-image-* accepts a fixed set
# of sizes (square, portrait, landscape). Non-square aspect requests map to
# the closest available canvas — the model composes for that canvas.
OPENAI_SIZES = {
    "1:1":   "1024x1024",
    "4:3":   "1536x1024",
    "3:4":   "1024x1536",
    "16:9":  "1536x1024",
    "9:16":  "1024x1536",
    "3:2":   "1536x1024",
    "2:3":   "1024x1536",
}


@dataclass
class GenResult:
    png_bytes: bytes
    provider: str
    model: str


@dataclass
class InputImage:
    path: Path
    data: bytes
    mime_type: str


def load_input_images(paths: list[str] | None) -> list[InputImage]:
    """Read input-image paths into memory and tag each with a MIME type.

    The image endpoints on both providers want a small, well-known set of
    MIME types and have file-size caps — anything outside those gets
    rejected server-side with a vague error, so filter at the client.
    """
    if not paths:
        return []
    out: list[InputImage] = []
    for raw in paths:
        path = Path(raw).expanduser().resolve()
        if not path.is_file():
            raise SystemExit(f"--input-image not found: {path}")
        mime = _INPUT_IMAGE_MIME.get(path.suffix.lower())
        if not mime:
            raise SystemExit(
                f"--input-image must be .png/.jpg/.jpeg/.webp, got '{path.suffix}' ({path})"
            )
        try:
            size = path.stat().st_size
        except OSError as e:
            raise SystemExit(f"--input-image stat failed for {path}: {e}")
        if size < _MIN_INPUT_BYTES:
            raise SystemExit(
                f"--input-image {path} is {size} bytes — looks empty or truncated."
            )
        if size > _MAX_INPUT_BYTES:
            raise SystemExit(
                f"--input-image {path} is {size / 1024 / 1024:.1f} MiB — "
                f"exceeds the {_MAX_INPUT_BYTES // 1024 // 1024} MiB inline limit. "
                f"Downscale or re-encode (e.g. cwebp -q 80) before passing."
            )
        try:
            data = path.read_bytes()
        except OSError as e:
            raise SystemExit(f"--input-image read failed for {path}: {e}")
        out.append(InputImage(path=path, data=data, mime_type=mime))
    return out


def load_styles() -> dict:
    with STYLES_PATH.open() as f:
        return json.load(f)["presets"]


def resolve_style(style: str | None, styles: dict) -> str:
    if not style:
        return ""
    if style not in styles:
        raise SystemExit(
            f"Unknown style '{style}'. Available: {', '.join(sorted(styles))}"
        )
    return styles[style]["prompt_suffix"]


def pick_provider(explicit: str | None, *, transparent: bool = False) -> str:
    if explicit:
        if explicit not in ("google", "openai"):
            raise SystemExit(f"--provider must be 'google' or 'openai', got '{explicit}'")
        return explicit
    # When transparency is requested, prefer OpenAI: it returns a real alpha
    # channel natively, whereas Google requires a chroma-key workaround that
    # can leave faint halos. Only fall back to Google if no OpenAI key is set.
    if transparent and os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("GOOGLE_AI_STUDIO_API_KEY"):
        return "google"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    raise SystemExit(
        "No image provider key found. Set GOOGLE_AI_STUDIO_API_KEY "
        "(preferred, Nano Banana Pro) or OPENAI_API_KEY (gpt-image-2)."
    )


def _backoff_seconds(attempt: int, retry_after_header: str | None) -> float:
    """Prefer Retry-After (seconds, integer) when the server provides it."""
    if retry_after_header:
        try:
            return max(0.0, min(60.0, float(retry_after_header.strip())))
        except ValueError:
            pass  # http-date form — ignore, fall back to exponential
    return float(2 ** attempt)


def _post_with_retry(
    url: str,
    *,
    headers: dict,
    json_body: dict | None = None,
    files: list | None = None,
    timeout: int,
    max_retries: int,
) -> requests.Response:
    last_err: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            if files is not None:
                # Non-file form fields ride in the same `files` list as
                # (name, (None, value)) tuples — `requests` treats those as
                # regular multipart text fields. Simpler than splitting into
                # data= and files= for this small a payload.
                r = requests.post(url, headers=headers, files=files, timeout=timeout)
            else:
                r = requests.post(url, headers=headers, json=json_body, timeout=timeout)
            if r.status_code >= 500 or r.status_code == 429:
                last_err = RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
                if attempt < max_retries:
                    time.sleep(_backoff_seconds(attempt, r.headers.get("Retry-After")))
                    continue
            return r
        except (requests.ConnectionError, requests.Timeout) as e:
            last_err = e
            if attempt < max_retries:
                time.sleep(_backoff_seconds(attempt, None))
                continue
            raise
    raise RuntimeError(f"All retries exhausted: {last_err}")


def generate_openai(
    prompt: str,
    *,
    aspect: str,
    model: str,
    max_retries: int,
    transparent: bool = False,
    input_images: list[InputImage] | None = None,
) -> GenResult:
    api_key = os.environ["OPENAI_API_KEY"]
    size = OPENAI_SIZES.get(aspect, "1024x1024")

    if input_images:
        # /v1/images/edits is the *only* OpenAI image-API endpoint that
        # accepts image input — but its name is misleading. With gpt-image-1
        # / gpt-image-2 it handles edits, restyles, composition references,
        # and pure visual reference; the prompt decides which. The endpoint
        # takes multipart/form-data, not JSON.
        form: dict = {
            "model": (None, model),
            "prompt": (None, prompt),
            "size": (None, size),
            "n": (None, "1"),
            "quality": (None, "high"),
        }
        if transparent:
            form["background"] = (None, "transparent")
        files: list = list(form.items())
        for img in input_images:
            # Multiple input images use the repeated "image[]" field per the
            # /images/edits multipart spec; a single image can use "image".
            field = "image[]" if len(input_images) > 1 else "image"
            files.append((field, (img.path.name, img.data, img.mime_type)))
        r = _post_with_retry(
            OPENAI_EDIT_ENDPOINT,
            headers={"Authorization": f"Bearer {api_key}"},
            files=files,
            timeout=180,
            max_retries=max_retries,
        )
    else:
        body = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "n": 1,
            "quality": "high",
        }
        if transparent:
            # gpt-image-* natively renders a transparent alpha channel when this
            # is set. The returned bytes are a PNG with real alpha — no
            # chroma-key post-processing required.
            body["background"] = "transparent"
        r = _post_with_retry(
            OPENAI_ENDPOINT,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json_body=body,
            timeout=180,
            max_retries=max_retries,
        )
    if not r.ok:
        raise RuntimeError(f"OpenAI image API error {r.status_code}: {r.text[:500]}")
    data = r.json()["data"][0]
    if "b64_json" in data and data["b64_json"]:
        return GenResult(png_bytes=base64.b64decode(data["b64_json"]), provider="openai", model=model)
    if "url" in data and data["url"]:
        img = requests.get(data["url"], timeout=60)
        img.raise_for_status()
        return GenResult(png_bytes=img.content, provider="openai", model=model)
    raise RuntimeError(f"OpenAI response missing image data: {data}")


def generate_openai_responses(
    prompt: str,
    *,
    aspect: str,
    model: str,
    max_retries: int,
    transparent: bool = False,
    input_images: list[InputImage] | None = None,
) -> GenResult:
    """OpenAI Responses API + image_generation tool route.

    The input images go in as multimodal context on a text model (default
    gpt-5); the model then calls the image_generation tool to produce the
    output. Better mental model when the images are *context* (lighting
    mood, brand reference, layout inspiration) rather than the subject of
    an edit. The tool itself runs the same image-gen pipeline as the
    /images/edits and /images/generations endpoints.
    """
    api_key = os.environ["OPENAI_API_KEY"]
    content: list[dict] = [{"type": "input_text", "text": prompt}]
    for img in input_images or []:
        # input_image accepts an image_url (URL or base64 data URL) or a
        # file_id from the Files API. Base64 keeps everything inline — no
        # separate upload round-trip. Fine for the file sizes we deal with.
        b64 = base64.b64encode(img.data).decode("ascii")
        content.append({
            "type": "input_image",
            "image_url": f"data:{img.mime_type};base64,{b64}",
        })

    tool_config: dict = {
        "type": "image_generation",
        "size": OPENAI_SIZES.get(aspect, "1024x1024"),
    }
    if transparent:
        tool_config["background"] = "transparent"

    body = {
        "model": model,
        "input": [{"role": "user", "content": content}],
        "tools": [tool_config],
    }
    r = _post_with_retry(
        OPENAI_RESPONSES_ENDPOINT,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json_body=body,
        timeout=240,
        max_retries=max_retries,
    )
    if not r.ok:
        raise RuntimeError(f"OpenAI Responses API error {r.status_code}: {r.text[:500]}")
    payload = r.json()

    # The image lands in an output item with type=image_generation_call; the
    # base64 PNG is on the .result field. Scan because other output items
    # (text, reasoning) may appear alongside it.
    text_replies: list[str] = []
    for item in payload.get("output") or []:
        if item.get("type") == "image_generation_call":
            result = item.get("result")
            if result:
                return GenResult(
                    png_bytes=base64.b64decode(result),
                    provider="openai",
                    model=model,
                )
        # Collect any text the model said instead of generating an image —
        # usually a refusal or clarifying question. Shape varies by API
        # version; cover both `content[].text` and a flat `text` field.
        if item.get("type") == "message":
            for c in item.get("content") or []:
                txt = c.get("text") if isinstance(c, dict) else None
                if txt:
                    text_replies.append(txt)
        elif isinstance(item.get("text"), str):
            text_replies.append(item["text"])

    if text_replies:
        joined = " ".join(text_replies).strip()
        raise RuntimeError(
            f"OpenAI Responses returned text instead of an image: {joined[:400]}"
        )
    raise RuntimeError(
        f"OpenAI Responses output had no image_generation_call result. "
        f"Payload (truncated): {json.dumps(payload)[:500]}"
    )


def generate_google(
    prompt: str,
    *,
    aspect: str,
    model: str,
    max_retries: int,
    input_images: list[InputImage] | None = None,
) -> GenResult:
    api_key = os.environ["GOOGLE_AI_STUDIO_API_KEY"]
    # Gemini takes multimodal input as an ordered list of parts. Putting the
    # image parts first and the text last matches Google's own examples for
    # "edit this image" style prompts and gives the model the visual context
    # before the instruction.
    parts: list[dict] = []
    for img in input_images or []:
        parts.append({
            "inlineData": {
                "mimeType": img.mime_type,
                "data": base64.b64encode(img.data).decode("ascii"),
            }
        })
    parts.append({"text": prompt})
    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect},
        },
    }
    url = GOOGLE_ENDPOINT.format(model=model)
    r = _post_with_retry(
        url,
        headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
        json_body=body,
        timeout=180,
        max_retries=max_retries,
    )
    if not r.ok:
        raise RuntimeError(f"Google image API error {r.status_code}: {r.text[:500]}")
    payload = r.json()

    # Safety/policy refusal — promptFeedback.blockReason set, no candidates.
    feedback = payload.get("promptFeedback") or {}
    if feedback.get("blockReason"):
        raise RuntimeError(
            f"Google refused the prompt (blockReason={feedback['blockReason']}). "
            f"Rephrase the brief; do not retry the same prompt."
        )

    candidates = payload.get("candidates") or []
    if not candidates:
        raise RuntimeError(f"Google response had no candidates: {payload}")
    cand = candidates[0]

    # Per-candidate refusal — finishReason in {SAFETY, RECITATION, PROHIBITED_CONTENT, ...}.
    finish = cand.get("finishReason")
    if finish and finish not in ("STOP", "MAX_TOKENS", None):
        raise RuntimeError(
            f"Google declined to generate (finishReason={finish}). "
            f"Rephrase the brief; do not retry the same prompt."
        )

    parts = (cand.get("content") or {}).get("parts") or []
    for part in parts:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            return GenResult(
                png_bytes=base64.b64decode(inline["data"]),
                provider="google",
                model=model,
            )

    # No image part — surface any text the model returned instead, it usually
    # explains why (e.g. "I can't generate that").
    text_reply = " ".join(p.get("text", "") for p in parts if p.get("text")).strip()
    if text_reply:
        raise RuntimeError(f"Google returned text instead of an image: {text_reply[:300]}")
    raise RuntimeError(f"Google response contained no image part: {payload}")


def _warn_if_opaque_transparent(img: Image.Image, *, threshold: float = 0.90) -> None:
    """Print a loud stderr warning if a `--transparent` result is almost all
    opaque (i.e. transparency failed — the model baked a solid/checkerboard
    background the chroma-key couldn't remove). No mutation: a wrong auto-strip
    would eat a same-coloured subject, so we flag and let the caller regenerate.
    """
    try:
        import numpy as np  # type: ignore
        a = np.asarray(img.convert("RGBA"))[..., 3]
        opaque = float((a > 110).mean())
        corners = float(np.mean([a[:12, :12].mean(), a[:12, -12:].mean(),
                                 a[-12:, :12].mean(), a[-12:, -12:].mean()]))
    except Exception:
        return
    if opaque >= threshold and corners > 40:
        sys.stderr.write(
            f"\n  ⚠️  TRANSPARENCY LIKELY FAILED: {opaque:.0%} of the image is opaque and "
            f"the corners aren't clear — the model probably baked an opaque background "
            f"(white/grey/checkerboard) instead of true alpha.\n"
            f"      Regenerate with NATIVE alpha (omit --provider so OpenAI gpt-image-1 is "
            f"used), and/or add 'fully transparent background, render nothing behind it, NO "
            f"checkerboard/grey squares/grid' to the prompt.\n\n")


def chroma_key_to_alpha(
    img: Image.Image,
    *,
    key_rgb: tuple[int, int, int] = CHROMA_KEY_RGB,
    tolerance: int = 60,
    feather: int = 30,
) -> Image.Image:
    """Replace a chroma-key colour with transparency on an RGBA image.

    Pixels within ``tolerance`` of ``key_rgb`` (Chebyshev distance) become
    fully transparent. Pixels in the ``feather`` band beyond that get a
    proportional alpha so edges anti-alias smoothly rather than producing
    a hard, jagged cut-out. The pixel's own RGB is left intact — only
    alpha changes — so we don't bake the magenta into semi-transparent
    edges (which would produce pink fringing on dark backgrounds).

    Implemented with NumPy when available (much faster on 1024² images);
    falls back to a pure-Pillow path so the skill still works without it.
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    try:
        import numpy as np  # type: ignore
    except ImportError:
        return _chroma_key_pillow(img, key_rgb=key_rgb, tolerance=tolerance, feather=feather)

    arr = np.array(img)  # H x W x 4, uint8
    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
    kr, kg, kb = key_rgb
    # Chebyshev distance from the key colour, channel-wise.
    dist = np.maximum.reduce([
        np.abs(r.astype(np.int16) - kr),
        np.abs(g.astype(np.int16) - kg),
        np.abs(b.astype(np.int16) - kb),
    ])
    # alpha = 0 inside tolerance; ramps to 255 across `feather`; 255 beyond.
    new_alpha = np.where(
        dist <= tolerance,
        0,
        np.where(
            dist >= tolerance + feather,
            255,
            ((dist - tolerance) * (255.0 / max(1, feather))).astype(np.int16),
        ),
    ).astype(np.uint8)
    # Combine with any existing alpha so we never make a pixel *more* opaque.
    arr[..., 3] = np.minimum(a, new_alpha)
    return Image.fromarray(arr, mode="RGBA")


def _chroma_key_pillow(
    img: Image.Image,
    *,
    key_rgb: tuple[int, int, int],
    tolerance: int,
    feather: int,
) -> Image.Image:
    """Pure-Pillow fallback for ``chroma_key_to_alpha``. Slow but dependency-free."""
    kr, kg, kb = key_rgb
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            dist = max(abs(r - kr), abs(g - kg), abs(b - kb))
            if dist <= tolerance:
                new_a = 0
            elif dist >= tolerance + feather:
                new_a = 255
            else:
                new_a = int((dist - tolerance) * (255.0 / max(1, feather)))
            pixels[x, y] = (r, g, b, min(a, new_a))
    return img


def strip_metadata_and_encode(
    png_bytes: bytes,
    *,
    out_path: Path,
    fmt: str,
    quality: int,
    lossless: bool,
    max_dim: int | None,
    transparent: bool = False,
) -> dict:
    """Re-decode pixels only, drop standard metadata, re-encode.

    EXIF, XMP, and PNG tEXt/iTXt/zTXt chunks are dropped by virtue of opening
    the image and saving a fresh one without forwarding `info`. SynthID lives
    in pixel space and is preserved. C2PA Content Credentials live in a
    separate sidecar chunk that we deliberately do NOT re-attach if absent —
    note that re-encoding will break a C2PA signature; that's an accepted
    trade-off for repo-friendly file sizes.
    """
    src = Image.open(io.BytesIO(png_bytes))
    if transparent:
        # We need an alpha channel to write into; force RGBA before keying.
        src = src.convert("RGBA")
    elif src.mode not in ("RGB", "RGBA"):
        src = src.convert("RGBA" if "A" in src.mode else "RGB")
    # Rebuild from raw pixel bytes so nothing in src.info propagates
    # (EXIF, XMP, ICC profile, PNG tEXt/iTXt/zTXt chunks).
    clean = Image.frombytes(src.mode, src.size, src.tobytes())

    if transparent:
        # Resize *before* keying so the feather band stays the right thickness
        # at the final pixel scale.
        if max_dim and max(clean.size) > max_dim:
            ratio = max_dim / max(clean.size)
            new_size = (int(clean.size[0] * ratio), int(clean.size[1] * ratio))
            clean = clean.resize(new_size, Image.LANCZOS)
        clean = chroma_key_to_alpha(clean)
        # Safety signal: if a transparent gen comes back almost fully opaque, the
        # model likely baked an OPAQUE background (white/grey/checkerboard) the
        # magenta key couldn't strip — common on the Google path. Don't silently
        # ship a dirty box; warn loudly so the caller regenerates (preferably with
        # native alpha — omit --provider so OpenAI gpt-image-1 is used).
        _warn_if_opaque_transparent(clean)

    if not transparent and max_dim and max(clean.size) > max_dim:
        ratio = max_dim / max(clean.size)
        new_size = (int(clean.size[0] * ratio), int(clean.size[1] * ratio))
        clean = clean.resize(new_size, Image.LANCZOS)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs: dict = {}
    if fmt == "webp":
        save_kwargs.update(quality=quality, method=6, lossless=lossless)
    elif fmt == "png":
        save_kwargs.update(optimize=True)
    elif fmt in ("jpg", "jpeg"):
        if clean.mode == "RGBA":
            clean = clean.convert("RGB")
        save_kwargs.update(quality=quality, optimize=True, progressive=True)
    else:
        raise SystemExit(f"Unsupported output format: {fmt}")

    clean.save(out_path, format=fmt.upper() if fmt != "jpg" else "JPEG", **save_kwargs)
    return {
        "path": str(out_path),
        "width": clean.size[0],
        "height": clean.size[1],
        "bytes": out_path.stat().st_size,
        "format": fmt,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Generate an image via OpenAI or Google.")
    p.add_argument("--prompt", help="The image brief. Required unless --list-styles.")
    p.add_argument("--output", help="Output path (extension implies format). Required unless --list-styles.")
    p.add_argument("--style", default=None, help="Style preset key (see --list-styles).")
    p.add_argument("--aspect", default="1:1",
                   choices=["1:1", "4:3", "3:4", "16:9", "9:16", "3:2", "2:3"])
    p.add_argument("--provider", default=None, choices=["google", "openai"],
                   help="Override provider selection.")
    p.add_argument("--quality", type=int, default=85, help="WebP/JPEG quality (1-100).")
    p.add_argument("--lossless", action="store_true", help="Use lossless WebP.")
    p.add_argument("--max-dim", type=int, default=2048,
                   help="Resize so longest edge <= this. 0 disables.")
    p.add_argument("--max-retries", type=int, default=2, help="Retry count for API errors.")
    p.add_argument(
        "--transparent", action="store_true",
        help=(
            "Produce a transparent-background image. "
            "OpenAI: uses the native background=transparent API. "
            "Google: prompts the model to render on pure magenta then "
            "chroma-keys it out in post-processing (Google does not support "
            "native alpha-channel output)."
        ),
    )
    p.add_argument(
        "--input-image", action="append", default=None, metavar="PATH",
        help=(
            "Local image file to feed into the model as visual context "
            "(edit, restyle, compose, use as reference). Repeat the flag for "
            "multiple inputs. Accepts .png/.jpg/.jpeg/.webp/.gif. "
            "Google routes through Gemini's multimodal input; OpenAI routes "
            "via --openai-route (default 'edits')."
        ),
    )
    p.add_argument(
        "--openai-route", default="edits", choices=["edits", "responses"],
        help=(
            "Only used when --input-image is set and the provider is OpenAI. "
            "'edits' (default): /v1/images/edits with gpt-image-2 — one-shot, "
            "model specified explicitly. 'responses': /v1/responses with the "
            "image_generation tool — input images become multimodal context "
            "on a text model (default gpt-5, override with OPENAI_RESPONSES_MODEL)."
        ),
    )
    p.add_argument("--list-styles", action="store_true")
    args = p.parse_args()

    styles = load_styles()
    if args.list_styles:
        for key, meta in sorted(styles.items()):
            print(f"{key}: {meta['label']}")
            print(f"  use for: {meta['use_for']}")
        return 0

    if not args.prompt or not args.output:
        p.error("--prompt and --output are required (use --list-styles to inspect presets).")
    if not args.prompt.strip():
        p.error("--prompt must not be empty or whitespace.")
    if not 1 <= args.quality <= 100:
        p.error(f"--quality must be in 1..100, got {args.quality}.")

    style_suffix = resolve_style(args.style, styles)
    full_prompt = args.prompt if not style_suffix else f"{args.prompt}\n\nStyle: {style_suffix}"

    input_images = load_input_images(args.input_image)

    provider = pick_provider(args.provider, transparent=args.transparent)
    chroma_keyed = False
    if args.transparent and provider == "google":
        # Google's image endpoint has no native alpha output, so we render
        # on a chroma-key background and strip it in post. Prepend the
        # anti-checkerboard preamble *before* the user's brief so it sets
        # the canvas expectation up front.
        full_prompt = f"{TRANSPARENT_PREAMBLE}\n\n{full_prompt}"
        chroma_keyed = True

    openai_route_used: str | None = None
    if provider == "google":
        result = generate_google(full_prompt, aspect=args.aspect,
                                 model=DEFAULT_GOOGLE_MODEL,
                                 max_retries=args.max_retries,
                                 input_images=input_images)
    elif input_images and args.openai_route == "responses":
        openai_route_used = "responses"
        result = generate_openai_responses(
            full_prompt, aspect=args.aspect,
            model=DEFAULT_OPENAI_RESPONSES_MODEL,
            max_retries=args.max_retries,
            transparent=args.transparent,
            input_images=input_images,
        )
    else:
        openai_route_used = "edits" if input_images else "generations"
        openai_model = TRANSPARENT_OPENAI_MODEL if args.transparent else DEFAULT_OPENAI_MODEL
        result = generate_openai(full_prompt, aspect=args.aspect,
                                 model=openai_model,
                                 max_retries=args.max_retries,
                                 transparent=args.transparent,
                                 input_images=input_images)

    out_path = Path(args.output).expanduser().resolve()
    ext = out_path.suffix.lower().lstrip(".") or "webp"
    if ext not in ("webp", "png", "jpg", "jpeg"):
        raise SystemExit(f"Output extension must be .webp/.png/.jpg/.jpeg, got '.{ext}'")
    if args.transparent and ext in ("jpg", "jpeg"):
        raise SystemExit(
            "--transparent requires an alpha-capable format. Use .png or .webp."
        )

    info = strip_metadata_and_encode(
        result.png_bytes,
        out_path=out_path,
        fmt=ext,
        quality=args.quality,
        lossless=args.lossless,
        max_dim=args.max_dim if args.max_dim > 0 else None,
        transparent=chroma_keyed,
    )
    info.update(
        provider=result.provider,
        model=result.model,
        style=args.style,
        aspect=args.aspect,
        prompt_chars=len(full_prompt),
        style_suffix_applied=bool(style_suffix),
        transparent=args.transparent,
        transparency_method=(
            None if not args.transparent
            else "chroma_key" if chroma_keyed
            else "native"
        ),
        input_images=[str(img.path) for img in input_images],
        openai_route=openai_route_used,
    )
    print(json.dumps(info, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
