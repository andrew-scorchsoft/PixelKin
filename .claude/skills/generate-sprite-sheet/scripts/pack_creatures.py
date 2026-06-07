#!/usr/bin/env python3
"""
Creature-sprite packer for PixelKin.

The "code does the layout" half of creature-sprite generation. `generate_sprite.py`
makes each kin's source PNGs (battle_front/battle_back/icon/overworld/portrait) on the
exact standard canvas (see docs/art-style.md §4); this script packs every creature folder
under assets/creatures/ into served, lossless-WebP sprites plus a single manifest the game
loads.

Source (read-only masters, NOT served):

    assets/creatures/NNN_slug/
      battle_front.png  battle_back.png  icon.png  overworld.png  portrait.png
      metadata.json     # id, name, slug, types, sprites{ <view>: {file,width,height,anchor} }

Output (served — vite drops the public/ prefix at runtime):

    public/assets/sprites/creatures/NNN_slug/<view>.webp      # one file per view
    public/assets/sprites/creatures/creatures.manifest.json   # id -> packed views

Per-creature files (not an atlas) are deliberate: battle loads one kin at a time, so a
small per-view fetch is simpler than slicing an atlas, and the loader hides the layout
either way.

WebP is written LOSSLESS (lossless=True, quality=100, method=6). Lossy WebP destroys the
crisp 1px pixel-art edges the art bible requires, so the script decodes each written WebP
and asserts it round-trips visually identical to the source (alpha matches everywhere; RGB
matches everywhere alpha > 0) and that dimensions match the metadata — failing loudly
otherwise. Generation (the model) and packing (this script) stay separate, mirroring the
two-system principle in SKILL.md.

Manifest shape (consumed by src/game/systems/sprites/CreatureSprites.ts):

  {
    "creatures": {
      "1": {
        "slug": "vulpyre",
        "front":     { "path": "assets/sprites/creatures/001_vulpyre/battle_front.webp", "width": 64, "height": 64 },
        "back":      { ... }, "icon": { ... }, "overworld": { ... }, "portrait": { ... }
      },
      ...
    }
  }

Run from the repo root (no args packs every creature):

    ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_creatures.py
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

# Maps a manifest view key -> the metadata.json sprite key + served output filename stem.
# The metadata file names are battle_front/battle_back; the served + manifest view keys are
# the shorter front/back the engine asks for (CreatureView in CreatureSprites.ts).
VIEWS: dict[str, str] = {
    "front": "battle_front",
    "back": "battle_back",
    "icon": "icon",
    "overworld": "overworld",
    "portrait": "portrait",
}

EXPECTED_SIZE: dict[str, tuple[int, int]] = {
    "battle_front": (64, 64),
    "battle_back": (64, 64),
    "icon": (32, 32),
    "overworld": (32, 32),
    "portrait": (96, 96),
}


def find_repo_root(start: Path) -> Path:
    for d in (start, *start.parents):
        if (d / ".git").exists():
            return d
    return start


def verify_lossless(src: Image.Image, webp_path: Path) -> None:
    """Decode the written WebP and assert it is VISUALLY lossless vs the source.

    Visually lossless = alpha matches everywhere and RGB matches everywhere alpha > 0.
    RGB under fully-transparent pixels is never rendered and lossless WebP may store any
    value there, so comparing it would yield false failures. Every *visible* pixel must
    round-trip exactly, which is what keeps the crisp pixel-art edges intact.
    """
    decoded = Image.open(webp_path).convert("RGBA")
    src = src.convert("RGBA")
    if decoded.size != src.size:
        raise SystemExit(
            f"WebP verification FAILED for {webp_path}: size {decoded.size} != source {src.size}."
        )
    try:
        import numpy as np  # type: ignore

        a = np.asarray(src)
        b = np.asarray(decoded)
        if not np.array_equal(a[..., 3], b[..., 3]):
            raise SystemExit(
                f"WebP lossless verification FAILED for {webp_path}: alpha channel differs."
            )
        visible = a[..., 3] > 0
        if not np.array_equal(a[..., :3][visible], b[..., :3][visible]):
            raise SystemExit(
                f"WebP lossless verification FAILED for {webp_path}: visible RGB differs from source."
            )
    except ImportError:
        sp = list(src.getdata())
        dp = list(decoded.getdata())
        for (sr, sg, sb, sa), (dr, dg, db, da) in zip(sp, dp):
            if sa != da or (sa > 0 and (sr, sg, sb) != (dr, dg, db)):
                raise SystemExit(
                    f"WebP lossless verification FAILED for {webp_path}: a visible pixel differs."
                )


def pack_creature(
    cdir: Path, out_root: Path, image_prefix: str, warnings: list[str]
) -> tuple[int, str, dict]:
    """Pack one creature folder; return (id, slug, manifest entry). Skips missing views."""
    meta_path = cdir / "metadata.json"
    if not meta_path.is_file():
        raise SystemExit(f"{cdir} has no metadata.json.")
    meta = json.loads(meta_path.read_text())
    kin_id = meta.get("id")
    slug = meta.get("slug") or cdir.name.split("_", 1)[-1]
    if not isinstance(kin_id, int):
        raise SystemExit(f"{meta_path}: 'id' must be an integer, got {kin_id!r}.")
    sprites = meta.get("sprites", {})

    out_dir = out_root / cdir.name
    out_dir.mkdir(parents=True, exist_ok=True)

    entry: dict = {"slug": slug}
    for view, meta_key in VIEWS.items():
        spec = sprites.get(meta_key)
        src_name = spec.get("file") if isinstance(spec, dict) else f"{meta_key}.png"
        src_path = cdir / src_name
        if not src_path.is_file():
            warnings.append(f"{cdir.name}: {src_name} missing; '{view}' view skipped.")
            continue
        img = Image.open(src_path).convert("RGBA")

        exp = EXPECTED_SIZE[meta_key]
        if img.size != exp:
            raise SystemExit(
                f"{src_path} is {img.size}, expected {exp} (art-style.md canvas standard). "
                f"Refusing to pack a non-standard master."
            )
        # Cross-check the metadata's declared dimensions too, if present.
        if isinstance(spec, dict) and "width" in spec and "height" in spec:
            declared = (spec["width"], spec["height"])
            if declared != exp:
                warnings.append(
                    f"{cdir.name}/{meta_key}: metadata size {declared} != standard {exp}."
                )
        if img.getchannel("A").getbbox() is None:
            warnings.append(f"{cdir.name}/{meta_key}: fully transparent.")

        webp_path = out_dir / f"{meta_key}.webp"
        img.save(webp_path, format="WEBP", lossless=True, quality=100, method=6)
        verify_lossless(img, webp_path)

        entry[view] = {
            "path": f"{image_prefix.rstrip('/')}/{cdir.name}/{meta_key}.webp",
            "width": img.size[0],
            "height": img.size[1],
        }

    return kin_id, slug, entry


def main() -> int:
    p = argparse.ArgumentParser(
        description="Pack assets/creatures/* into served lossless-WebP sprites + a manifest."
    )
    p.add_argument(
        "--creatures-dir",
        help="Directory of per-creature master folders (default <repo>/assets/creatures).",
    )
    p.add_argument(
        "--out-dir",
        help="Served output dir (default <repo>/public/assets/sprites/creatures).",
    )
    p.add_argument(
        "--image-prefix",
        default="assets/sprites/creatures",
        help="Served path prefix recorded in the manifest (default 'assets/sprites/creatures'; "
        "vite drops the public/ prefix at runtime).",
    )
    args = p.parse_args()

    repo = find_repo_root(Path.cwd().resolve())
    creatures_dir = (
        Path(args.creatures_dir).expanduser().resolve()
        if args.creatures_dir
        else repo / "assets" / "creatures"
    )
    if not creatures_dir.is_dir():
        raise SystemExit(f"--creatures-dir not found: {creatures_dir}")
    out_root = (
        Path(args.out_dir).expanduser().resolve()
        if args.out_dir
        else repo / "public" / "assets" / "sprites" / "creatures"
    )
    out_root.mkdir(parents=True, exist_ok=True)

    cdirs = sorted(d for d in creatures_dir.iterdir() if d.is_dir())
    if not cdirs:
        raise SystemExit(f"No creature folders found in {creatures_dir}.")

    warnings: list[str] = []
    creatures: dict[str, dict] = {}
    for cdir in cdirs:
        kin_id, _slug, entry = pack_creature(cdir, out_root, args.image_prefix, warnings)
        creatures[str(kin_id)] = entry

    manifest = {"creatures": creatures}
    manifest_path = out_root / "creatures.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    view_count = sum(
        sum(1 for v in VIEWS if v in entry) for entry in creatures.values()
    )
    summary = {
        "manifest": str(manifest_path),
        "out_dir": str(out_root),
        "creatures_packed": len(creatures),
        "views_packed": view_count,
        "ids": sorted(int(k) for k in creatures),
        "format": "webp-lossless",
        "lossless_verified": True,
        "warnings": warnings,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
