#!/usr/bin/env python3
"""
Sprite-sheet generator for PixelKin.

This is the "code does the layout" half of the pipeline described in
docs/art-style.md. An image model makes the art; this script enforces the
deterministic part: every asset lands on the exact standard canvas, at the
right anchor, with a real alpha channel, plus metadata.

Pipeline per asset:
  1. Build a prompt = shared style preamble + originality clause + the locked
     per-type template (sprite-specs.json) + your original subject brief.
  2. Drive the sibling generate-image skill's generate.py with --transparent
     to get a high-res, transparent-background source PNG (OpenAI native alpha
     or Google magenta chroma-key — generate.py owns that choice).
  3. Snap that source to the type's exact pixel canvas: alpha-trim, scale to
     the fill fraction, composite at the type's anchor. For multi-frame sheets,
     do this per cell so every frame shares a baseline.
  4. Save the PNG and, for creatures, write/update metadata.json.

This script does NOT judge whether the art matches the brief or stays clear of
copyright — the calling agent (Claude) opens the result and runs the self-check
loop. See SKILL.md.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
SPECS_PATH = SCRIPT_DIR / "sprite-specs.json"
# The sibling generate-image skill does the actual API call.
GENERATE_IMAGE = SCRIPT_DIR.parent.parent / "generate-image" / "scripts" / "generate.py"

# Default provider. Google Nano Banana Pro is the default: it handles
# transparency and reference-image fidelity best and is reliable here. OpenAI
# gpt-image-2 is available via --provider openai, but it has no native
# transparent mode (we chroma-key a magenta field instead) and its safety
# filter can reject benign prompts, so it's a fallback rather than the default.
DEFAULT_PROVIDER = "google"

# When the OpenAI path IS used, gpt-image-2 has no native transparent-background
# mode (only the older gpt-image-1 does), so we render the sprite on a flat
# magenta chroma-key field and strip it ourselves. This preamble forces that
# field. Reuse the chroma-key implementation from the generate-image skill.
sys.path.insert(0, str(GENERATE_IMAGE.parent))
try:
    from generate import chroma_key_to_alpha  # type: ignore
except Exception:  # pragma: no cover - helper is optional at import time
    chroma_key_to_alpha = None  # type: ignore

CHROMA_PREAMBLE = (
    "Paint the sprite on a SOLID FLAT UNIFORM pure magenta background, hex "
    "#FF00FF (R=255 G=0 B=255), filling the whole canvas edge to edge. The "
    "magenta is a chroma-key colour removed in post-processing to make the "
    "background transparent. CRITICAL: do NOT use magenta, pink, or any "
    "near-magenta hue anywhere on the subject itself (those pixels get "
    "deleted); do not draw a checkerboard, transparency grid, frame, border, "
    "card, or cast-shadow plate — just the subject sitting directly on flat "
    "magenta, with crisp edges (no soft pink halo)."
)

# Aspect ratios generate-image / the underlying image APIs accept, as w/h.
ASPECTS = {
    "1:1": 1.0,
    "4:3": 4 / 3,
    "3:4": 3 / 4,
    "16:9": 16 / 9,
    "9:16": 9 / 16,
    "3:2": 3 / 2,
    "2:3": 2 / 3,
}


# --------------------------------------------------------------------------- #
# Spec loading & prompt building
# --------------------------------------------------------------------------- #
def load_specs() -> dict:
    with SPECS_PATH.open() as f:
        return json.load(f)


def nearest_aspect(canvas_w: int, canvas_h: int) -> str:
    """Pick the supported aspect string closest to the canvas proportions."""
    target = canvas_w / canvas_h
    return min(ASPECTS, key=lambda k: abs(ASPECTS[k] - target))


def build_prompt(specs: dict, spec: dict, subject: str) -> str:
    cols, rows = spec["cols"], spec["rows"]
    fw, fh = spec["frame_width"], spec["frame_height"]
    fields = {
        "subject": subject.strip(),
        "fw": fw,
        "fh": fh,
        "cols": cols,
        "rows": rows,
        "canvas_w": fw * cols,
        "canvas_h": fh * rows,
        "fill_pct": int(round(spec["fill"] * 100)),
    }
    style = specs["_style"].format(**fields)
    body = spec["prompt"].format(**fields)
    originality = specs["_originality"]
    return f"{style}\n\n{body}\n\n{originality}"


# --------------------------------------------------------------------------- #
# Generation (delegates to the generate-image skill)
# --------------------------------------------------------------------------- #
def generate_source(prompt: str, aspect: str, *, provider: str,
                    native_transparent: bool, max_retries: int, out_png: Path,
                    references: list[str] | None = None) -> dict:
    """Run generate-image to produce a high-res source PNG.

    With ``native_transparent`` (Google path) we pass --transparent and
    generate-image returns real alpha. Without it (OpenAI gpt-image-2 path) we
    render opaque on a magenta field — the prompt already carries the chroma
    preamble — and this script keys the magenta out afterwards.

    We disable generate-image's own downscale (--max-dim 0) so we keep the full
    resolution for our own pixel-art-aware snap step. Any `references` are
    passed through as --input-image so the model keeps a creature/character
    visually consistent with existing art (e.g. the logo).
    """
    if not GENERATE_IMAGE.is_file():
        raise SystemExit(f"Cannot find generate-image script at {GENERATE_IMAGE}")
    cmd = [
        sys.executable, str(GENERATE_IMAGE),
        "--prompt", prompt,
        "--output", str(out_png),
        "--aspect", aspect,
        "--max-dim", "0",
        "--max-retries", str(max_retries),
        "--provider", provider,
    ]
    if native_transparent:
        cmd += ["--transparent"]
    for ref in references or []:
        cmd += ["--input-image", ref]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(
            "generate-image failed:\n"
            f"  exit {proc.returncode}\n"
            f"  stderr: {proc.stderr.strip()[:800]}\n"
            f"  stdout: {proc.stdout.strip()[:400]}"
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"raw_stdout": proc.stdout.strip()[:400]}


# --------------------------------------------------------------------------- #
# Pixel-art-aware resize & canvas snapping
# --------------------------------------------------------------------------- #
def resize_rgba(src: Image.Image, size: tuple[int, int], resample: str) -> Image.Image:
    """Resize an RGBA image to `size`.

    For 'nearest' we use a plain nearest-neighbour resize (hardest edges).
    For 'lanczos'/'box' we resize on PREMULTIPLIED alpha so fully/partly
    transparent pixels don't bleed their (often magenta or black) RGB into the
    sprite's edges as a coloured halo, then un-premultiply.
    """
    src = src.convert("RGBA")
    if resample == "nearest":
        return src.resize(size, Image.NEAREST)

    pil_filter = Image.LANCZOS if resample == "lanczos" else Image.BOX
    try:
        import numpy as np  # type: ignore
    except ImportError:
        # Acceptable fallback: Pillow's own RGBA resize. May show a faint halo
        # on soft edges, but keeps the skill working without numpy.
        return src.resize(size, pil_filter)

    arr = np.asarray(src).astype(np.float32)
    a = arr[..., 3:4] / 255.0
    pm = np.concatenate([arr[..., :3] * a, arr[..., 3:4]], axis=-1).astype(np.uint8)
    resized = Image.fromarray(pm, "RGBA").resize(size, pil_filter)
    out = np.asarray(resized).astype(np.float32)
    oa = out[..., 3:4] / 255.0
    safe = np.where(oa > 0, oa, 1.0)
    rgb = np.clip(out[..., :3] / safe, 0, 255)
    res = np.concatenate([rgb, out[..., 3:4]], axis=-1).astype("uint8")
    return Image.fromarray(res, "RGBA")


def fit_to_frame(src: Image.Image, fw: int, fh: int, anchor: str,
                 fill: float, resample: str) -> Image.Image:
    """Trim transparent margins, scale to the fill fraction, composite at anchor."""
    src = src.convert("RGBA")
    bbox = src.split()[3].getbbox()  # bbox of non-transparent pixels
    if bbox:
        src = src.crop(bbox)
    cw, ch = src.size
    if cw == 0 or ch == 0:
        return Image.new("RGBA", (fw, fh), (0, 0, 0, 0))

    # Scale so the content fits inside fill*frame in both dimensions (aspect kept).
    scale = min((fw * fill) / cw, (fh * fill) / ch)
    nw, nh = max(1, round(cw * scale)), max(1, round(ch * scale))
    src = resize_rgba(src, (nw, nh), resample)

    canvas = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    if anchor == "bottom-center":
        pad = max(1, round(fh * 0.03))  # a couple of px of "ground" padding
        x = (fw - nw) // 2
        y = fh - nh - pad
    elif anchor == "top-left":
        x, y = 0, 0
    else:  # center
        x = (fw - nw) // 2
        y = (fh - nh) // 2
    canvas.alpha_composite(src, (max(0, x), max(0, y)))
    return canvas


def snap_single(src: Image.Image, spec: dict, resample: str) -> Image.Image:
    fw, fh = spec["frame_width"], spec["frame_height"]
    # Tiles fill their frame edge-to-edge; just resize, never trim/anchor.
    if spec["anchor"] == "top-left" and spec["fill"] >= 1.0:
        return resize_rgba(src, (fw, fh), resample)
    return fit_to_frame(src, fw, fh, spec["anchor"], spec["fill"], resample)


def snap_sheet(src: Image.Image, spec: dict, resample: str, align: bool) -> Image.Image:
    """Snap a multi-frame sheet to its exact grid.

    align=True (default): slice the generated image into cols x rows equal
    cells and fit each cell into its frame independently, so every frame shares
    a baseline (feet line up, bodies centre). align=False: just downscale the
    whole image to the exact grid size and trust the model's layout.
    """
    fw, fh = spec["frame_width"], spec["frame_height"]
    cols, rows = spec["cols"], spec["rows"]
    out = Image.new("RGBA", (fw * cols, fh * rows), (0, 0, 0, 0))
    if not align:
        return resize_rgba(src.convert("RGBA"), (fw * cols, fh * rows), resample)

    src = src.convert("RGBA")
    sw, sh = src.size
    cell_w, cell_h = sw // cols, sh // rows
    for r in range(rows):
        for c in range(cols):
            cell = src.crop((c * cell_w, r * cell_h,
                             (c + 1) * cell_w, (r + 1) * cell_h))
            frame = fit_to_frame(cell, fw, fh, spec["anchor"], spec["fill"], resample)
            out.alpha_composite(frame, (c * fw, r * fh))
    return out


# --------------------------------------------------------------------------- #
# Metadata
# --------------------------------------------------------------------------- #
def update_metadata(creature_dir: Path, cid: int, slug: str,
                    type_key: str, spec: dict, out_file: str) -> Path:
    meta_path = creature_dir / "metadata.json"
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text())
    else:
        meta = {
            "id": cid,
            "name": slug.replace("_", " ").replace("-", " ").title(),
            "slug": slug,
            "types": [],
            "sprites": {},
            "scale": 1.0,
            "offsets": {"battleX": 0, "battleY": 0, "iconX": 0, "iconY": 0},
        }
    meta.setdefault("sprites", {})
    # Key metadata by a stable sprite role derived from the type.
    role = type_key.replace("creature-", "").replace("-", "_")
    if role == "front":
        role = "battle_front"
    elif role == "back":
        role = "battle_back"
    meta["sprites"][role] = {
        "file": out_file,
        "width": spec["frame_width"] * spec["cols"],
        "height": spec["frame_height"] * spec["rows"],
        "anchor": spec["anchor"],
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    return meta_path


def find_repo_root(start: Path) -> Path:
    for d in (start, *start.parents):
        if (d / ".git").exists():
            return d
    return start


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> int:
    specs = load_specs()
    types = specs["types"]

    p = argparse.ArgumentParser(description="Generate a PixelKin sprite / sprite sheet.")
    p.add_argument("--type", choices=sorted(types), help="Sprite type (see --list-types).")
    p.add_argument("--subject", help="Original subject brief (the creature/character/effect).")
    p.add_argument("--output", help="Explicit output .png path. Overrides the creature convention.")
    p.add_argument("--creature-id", type=int, help="Creature dex id (with --creature-slug, auto-places under assets/creatures/NNN_slug/).")
    p.add_argument("--creature-slug", help="Creature slug, e.g. 'sproutle'.")
    p.add_argument("--provider", choices=["google", "openai"], default=DEFAULT_PROVIDER,
                   help="Image provider. 'google' (default) uses Nano Banana Pro's transparent "
                        "path. 'openai' uses gpt-image-2 with a magenta chroma-key for transparency.")
    p.add_argument("--resample", choices=["lanczos", "box", "nearest"], default="lanczos",
                   help="Downscale filter. lanczos (default) reads cleanest at tiny sizes; nearest is hardest-edged.")
    p.add_argument("--fill", type=float, help="Override the type's subject fill fraction (0-1).")
    p.add_argument("--no-align", action="store_true",
                   help="For sheets: skip per-frame baseline alignment; just downscale the whole sheet.")
    p.add_argument("--reference", action="append", metavar="PATH",
                   help="Reference image to keep the subject visually consistent (e.g. a logo crop). "
                        "Repeat for multiple. Passed to generate-image as --input-image. Ignored with --from-image.")
    p.add_argument("--from-image", help="Skip the API call and post-process this existing transparent PNG instead.")
    p.add_argument("--keep-temp", action="store_true", help="Keep the raw high-res generated PNG next to the output.")
    p.add_argument("--max-retries", type=int, default=2, help="API retry count passed to generate-image.")
    p.add_argument("--list-types", action="store_true", help="List sprite types and exit.")
    args = p.parse_args()

    if args.list_types:
        for key in sorted(types):
            t = types[key]
            grid = f"{t['cols']}x{t['rows']}" if t["cols"] * t["rows"] > 1 else "single"
            print(f"{key}: {t['label']}")
            print(f"  canvas: {t['frame_width']}x{t['frame_height']} ({grid})  anchor: {t['anchor']}")
            print(f"  use for: {t['use_for']}")
        return 0

    if not args.type:
        p.error("--type is required (use --list-types to see options).")
    spec = dict(types[args.type])
    if args.fill is not None:
        if not 0 < args.fill <= 1:
            p.error("--fill must be in (0, 1].")
        spec["fill"] = args.fill
    if not args.from_image and not (args.subject and args.subject.strip()):
        p.error("--subject is required unless --from-image is given.")

    # Resolve output path.
    if args.output:
        out_path = Path(args.output).expanduser().resolve()
    elif args.creature_id is not None and args.creature_slug:
        repo = find_repo_root(Path.cwd().resolve())
        creature_dir = repo / "assets" / "creatures" / f"{args.creature_id:03d}_{args.creature_slug}"
        out_path = creature_dir / spec["file"]
    else:
        p.error("Provide --output, or both --creature-id and --creature-slug.")
    if out_path.suffix.lower() != ".png":
        p.error("Output must be a .png (sprites need a real alpha channel).")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    is_sheet = spec["cols"] * spec["rows"] > 1
    gen_info: dict = {}
    # OpenAI gpt-image-2 has no native alpha: render on magenta and key it out.
    # Google's transparent path returns real alpha directly.
    chroma_path = args.provider == "openai"
    transparency_method = "chroma_key" if chroma_path else "native"

    with tempfile.TemporaryDirectory() as td:
        if args.from_image:
            src_path = Path(args.from_image).expanduser().resolve()
            if not src_path.is_file():
                raise SystemExit(f"--from-image not found: {src_path}")
            source = Image.open(src_path)
        else:
            prompt = build_prompt(specs, spec, args.subject)
            if chroma_path:
                prompt = f"{CHROMA_PREAMBLE}\n\n{prompt}"
            aspect = nearest_aspect(spec["frame_width"] * spec["cols"],
                                    spec["frame_height"] * spec["rows"])
            raw_png = Path(td) / "raw.png"
            gen_info = generate_source(prompt, aspect, provider=args.provider,
                                       native_transparent=not chroma_path,
                                       max_retries=args.max_retries, out_png=raw_png,
                                       references=args.reference)
            source = Image.open(raw_png)
            if chroma_path:
                if chroma_key_to_alpha is None:
                    raise SystemExit(
                        "chroma-key helper could not be imported from the generate-image "
                        "skill; cannot make the gpt-image-2 output transparent."
                    )
                source = chroma_key_to_alpha(source.convert("RGBA"))
            if args.keep_temp:
                keep = out_path.with_name(out_path.stem + ".raw.png")
                source.save(keep)
                gen_info["raw_kept"] = str(keep)

        if is_sheet:
            result = snap_sheet(source, spec, args.resample, align=not args.no_align)
        else:
            result = snap_single(source, spec, args.resample)

        result.save(out_path, format="PNG", optimize=True)

    summary = {
        "path": str(out_path),
        "type": args.type,
        "frame": [spec["frame_width"], spec["frame_height"]],
        "grid": [spec["cols"], spec["rows"]],
        "canvas": [spec["frame_width"] * spec["cols"], spec["frame_height"] * spec["rows"]],
        "anchor": spec["anchor"],
        "fill": spec["fill"],
        "resample": args.resample,
        "aligned": (not args.no_align) if is_sheet else None,
        "source": "from-image" if args.from_image else "generated",
        "references": args.reference or [],
        "provider": gen_info.get("provider") or (None if args.from_image else args.provider),
        "model": gen_info.get("model"),
        "transparency_method": None if args.from_image else transparency_method,
    }

    if args.creature_id is not None and args.creature_slug and not args.output:
        meta_path = update_metadata(out_path.parent, args.creature_id,
                                    args.creature_slug, args.type, spec, spec["file"])
        summary["metadata"] = str(meta_path)

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
