#!/usr/bin/env python3
"""
Validator for PixelKin sprites — the testing mechanism for the art spec.

Where generate_sprite.py *enforces* geometry at creation time, this script
*verifies* it after the fact: run it over a single file, a creature folder, or
the whole asset tree to assert every sprite still matches its locked spec
(docs/art-style.md / sprite-specs.json). It is import-safe, so generate_sprite.py
calls validate_sprite_image() automatically after each generation.

Checks per sprite:
  - correct canvas dimensions for its type (frame x cols/rows);
  - has a real alpha channel and an actually-transparent background;
  - no leftover magenta chroma-key bleed on the subject;
  - subject sits at the right anchor (bottom-centre / centre / top-left);
  - subject fills a sensible fraction and isn't clipped at the frame edges;
  - sheets: every frame is non-empty and all frames share a baseline.
Creature folders also check metadata.json matches the files on disk.

Exit code: 0 if no errors (with --strict, also no warnings); 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
SPECS_PATH = SCRIPT_DIR / "sprite-specs.json"

# metadata.json sprite role -> sprite-specs type key.
ROLE_TO_TYPE = {
    "battle_front": "creature-front",
    "battle_back": "creature-back",
    "icon": "creature-icon",
    "overworld": "creature-overworld",
    "portrait": "creature-portrait",
}

ALPHA_CONTENT = 32          # alpha above this counts as "content"
MAGENTA = (255, 0, 255)
MAGENTA_TOL = 50


@dataclass
class Report:
    target: str
    errors: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warns.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_specs() -> dict:
    return json.loads(SPECS_PATH.read_text())["types"]


def _visible_magenta(img: Image.Image, alpha_min: int = 64) -> int:
    """Count pixels that are near-magenta AND visible (alpha >= alpha_min)."""
    try:
        import numpy as np  # type: ignore
        arr = np.asarray(img)  # H x W x 4
        r, g, b, al = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
        mask = ((al >= alpha_min) &
                (np.abs(r.astype(int) - 255) <= MAGENTA_TOL) &
                (g <= MAGENTA_TOL) &
                (np.abs(b.astype(int) - 255) <= MAGENTA_TOL))
        return int(mask.sum())
    except ImportError:
        n = 0
        for r, g, b, al in img.getdata():
            if (al >= alpha_min and abs(r - 255) <= MAGENTA_TOL
                    and g <= MAGENTA_TOL and abs(b - 255) <= MAGENTA_TOL):
                n += 1
        return n


def _thresh_alpha(a: Image.Image):
    """Binarise an alpha band to content/no-content and return its bbox."""
    return a.point(lambda p: 255 if p > ALPHA_CONTENT else 0).getbbox()


def _edge_has_content(a: Image.Image, box) -> bool:
    return _thresh_alpha(a.crop(box)) is not None


def validate_sprite_image(img: Image.Image, spec: dict, *, label: str = "") -> Report:
    """Validate one already-loaded image against a sprite-type spec."""
    rep = Report(target=label)
    fw, fh = spec["frame_width"], spec["frame_height"]
    cols, rows = spec["cols"], spec["rows"]
    anchor, fill = spec["anchor"], spec["fill"]
    W, H = fw * cols, fh * rows
    is_sheet = cols * rows > 1
    is_tile = anchor == "top-left" and fill >= 1.0

    # 1) alpha channel present
    if img.mode != "RGBA":
        rep.err(f"not RGBA (mode={img.mode}); sprites need a real alpha channel")
        img = img.convert("RGBA")

    # 2) canvas dimensions
    if img.size != (W, H):
        rep.err(f"wrong size {img.size[0]}x{img.size[1]}, expected {W}x{H}")
        return rep  # geometry checks below assume the right canvas

    a = img.split()[3]
    content = _thresh_alpha(a)
    if content is None:
        rep.err("image is fully transparent (no subject)")
        return rep

    # 3) background actually transparent (tiles are allowed to be opaque)
    lo, hi = a.getextrema()
    if not is_tile and hi > 0 and lo > ALPHA_CONTENT:
        rep.err("no transparent pixels — background was not removed")

    # 4) no leftover magenta chroma *visible* on the subject. Only count pixels
    #    that are both near-magenta AND opaque enough to see — transparent
    #    pixels may keep magenta RGB under alpha=0, which is invisible.
    mag_count = _visible_magenta(img)
    if mag_count > (W * H) * 0.004:
        rep.warn(f"{mag_count}px of visible magenta chroma fringe on the subject")

    if is_sheet:
        _check_sheet(img, spec, rep)
    else:
        _check_single(a, content, spec, rep, is_tile)
    return rep


def _check_single(a, content, spec, rep, is_tile) -> None:
    fw, fh = spec["frame_width"], spec["frame_height"]
    anchor, fill = spec["anchor"], spec["fill"]
    x1, y1, x2, y2 = content
    cw, ch = x2 - x1, y2 - y1
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

    pos_tol = max(3, round(min(fw, fh) * 0.12))

    if is_tile:
        if not (x1 <= 1 and y1 <= 1 and x2 >= fw - 1 and y2 >= fh - 1):
            rep.warn("tile does not fill the frame edge-to-edge")
        return

    # fill fraction (longest content side vs frame)
    frac = max(cw / fw, ch / fh)
    if frac < 0.40:
        rep.warn(f"subject small ({frac:.0%} of frame); expected ~{fill:.0%}")
    if frac > 1.001:
        rep.err("subject larger than the frame")

    # anchor alignment
    if anchor == "bottom-center":
        pad = max(1, round(fh * 0.03))
        if abs(y2 - (fh - pad)) > pos_tol + pad:
            rep.warn(f"subject base at y={y2}, expected near {fh - pad} (bottom-centre)")
        if abs(cx - fw / 2) > pos_tol:
            rep.warn(f"subject horizontal centre at x={cx:.0f}, expected ~{fw // 2}")
        # clipping: content should not touch top/left/right edges
        if _edge_has_content(a, (0, 0, fw, 1)):
            rep.warn("content touches the TOP edge (possible clipping)")
        if _edge_has_content(a, (0, 0, 1, fh)) or _edge_has_content(a, (fw - 1, 0, fw, fh)):
            rep.warn("content touches a SIDE edge (possible clipping)")
    elif anchor == "center":
        if abs(cx - fw / 2) > pos_tol or abs(cy - fh / 2) > pos_tol:
            rep.warn(f"subject centre at ({cx:.0f},{cy:.0f}), expected ~({fw // 2},{fh // 2})")
        for name, box in [("TOP", (0, 0, fw, 1)), ("BOTTOM", (0, fh - 1, fw, fh)),
                          ("LEFT", (0, 0, 1, fh)), ("RIGHT", (fw - 1, 0, fw, fh))]:
            if _edge_has_content(a, box):
                rep.warn(f"content touches the {name} edge (possible clipping)")


def _check_sheet(img, spec, rep) -> None:
    fw, fh = spec["frame_width"], spec["frame_height"]
    cols, rows = spec["cols"], spec["rows"]
    anchor = spec["anchor"]
    a = img.split()[3]
    baselines: list[int] = []
    centres: list[float] = []
    empty: list[str] = []
    for r in range(rows):
        for c in range(cols):
            cell = a.crop((c * fw, r * fh, (c + 1) * fw, (r + 1) * fh))
            bbox = _thresh_alpha(cell)
            if bbox is None:
                empty.append(f"r{r}c{c}")
                continue
            x1, y1, x2, y2 = bbox
            baselines.append(y2)
            centres.append((x1 + x2) / 2)
    if empty:
        rep.err(f"empty frame(s): {', '.join(empty)}")
    if baselines and anchor == "bottom-center":
        spread = max(baselines) - min(baselines)
        if spread > max(2, round(fh * 0.12)):
            rep.warn(f"frame baselines vary by {spread}px (feet not aligned)")
    if centres:
        cspread = max(centres) - min(centres)
        if cspread > max(2, round(fw * 0.20)):
            rep.warn(f"frame horizontal centres vary by {cspread:.0f}px")
    # Directional walk sheets (human-overworld): rows must be distinct
    # down/left/right/up viewpoints, or the walk animation faces the wrong way.
    if spec.get("viewpoint_rows") and rows == 4:
        _check_walk_viewpoints(img, spec, rep)


# --------------------------------------------------------------------------- #
# Walk-sheet viewpoint compliance (the down/left/right/up rows)
# --------------------------------------------------------------------------- #
def _row_signature(img, fw, fh, cols, r):
    """Average luma + union mask of a row's frames (left to right), taken AS DRAWN
    — no per-frame re-centring, so a true left/right mirror pair compares as an
    exact mirror (the snap step already bottom-centre-aligns the frames). Returns
    (luma[H,W] float, mask[H,W] bool) or (None, None) if the row is empty."""
    import numpy as np
    lsum = msum = None
    for c in range(cols):
        cell = img.crop((c * fw, r * fh, (c + 1) * fw, (r + 1) * fh)).convert("RGBA")
        arr = np.asarray(cell, dtype=np.float32)
        m = arr[..., 3] > ALPHA_CONTENT
        if m.sum() < 20:
            continue
        luma = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
        lm, mm = np.where(m, luma, 0.0), m.astype(np.float32)
        lsum = lm if lsum is None else lsum + lm
        msum = mm if msum is None else msum + mm
    if msum is None:
        return None, None
    mask = msum >= 1
    avg = np.zeros_like(lsum)
    avg[mask] = lsum[mask] / msum[mask]
    return avg, mask


def _masked_mae(la, ma, lb, mb):
    both = ma & mb
    if both.sum() < 20:
        return None
    import numpy as np
    return float(np.abs(la[both] - lb[both]).mean())


def _check_walk_viewpoints(img, spec, rep) -> None:
    """A 4×4 directional walk sheet should read as four distinct views — row 0
    down (full face), row 1 LEFT, row 2 RIGHT, row 3 up (back of the head). This
    guards the two ways the in-game walk animation breaks:

      * ERROR — two rows are near-identical: a facing direction that shows the
        wrong/duplicate pose. Reliable (no shipped sheet trips it).
      * WARN — the RIGHT row isn't the horizontal mirror of the LEFT row. The
        generator authors side walks as exact mirrors so left and right always
        face opposite ways; a mismatch usually means that step was skipped (the
        "georgina faces you while walking sideways" bug). Only a WARN because a
        hand-drawn sheet may use two separately drawn opposite profiles
        (npc_old_man, lifter_rod), which is also correct — eyeball, don't fail.

    Whether a side row is a true left/right PROFILE or a front view can't be told
    apart reliably by pixels across characters (size, detail and the walk cycle
    confound every metric), so the generator's deterministic left→right mirror is
    the real guarantee and this is the verification. Skips if numpy is missing."""
    try:
        import numpy as np  # noqa: F401
    except Exception:
        return
    fw, fh, cols = spec["frame_width"], spec["frame_height"], spec["cols"]
    names = spec.get("viewpoint_rows", ["down", "left", "right", "up"])
    sigs = [_row_signature(img, fw, fh, cols, r) for r in range(4)]
    if any(s[0] is None for s in sigs):
        return  # empty frames already errored in _check_sheet
    (_dl, _dm), (ll, lm), (rl, rm), (_ul, _um) = sigs
    # ERROR: no two rows may be near-duplicates (a repeated pose kills a direction)
    for i in range(4):
        for j in range(i + 1, 4):
            d = _masked_mae(sigs[i][0], sigs[i][1], sigs[j][0], sigs[j][1])
            if d is not None and d < 4.0:
                rep.err(
                    f"walk sheet: the '{names[i]}' and '{names[j]}' rows are "
                    f"near-identical (diff {d:.1f}px) — each facing direction "
                    f"must be its own distinct viewpoint."
                )
    # WARN: the RIGHT row should be the horizontal mirror of the LEFT row.
    flip = _masked_mae(ll, lm, rl[:, ::-1], rm[:, ::-1])
    if flip is not None and flip > 6.0:
        rep.warn(
            f"walk sheet: the '{names[2]}' row is not the horizontal mirror of "
            f"the '{names[1]}' row (off by {flip:.0f}px). Generated sheets mirror "
            f"the right row from the left so the side walks face opposite ways — "
            f"if this was generated, re-run/mirror it; if it's hand-drawn opposite "
            f"profiles, ignore."
        )


# --------------------------------------------------------------------------- #
# File / folder / tree entry points
# --------------------------------------------------------------------------- #
def validate_file(path: Path, type_key: str, specs: dict) -> Report:
    if type_key not in specs:
        r = Report(str(path))
        r.err(f"unknown type '{type_key}'")
        return r
    try:
        img = Image.open(path)
        img.load()
    except Exception as e:
        r = Report(str(path))
        r.err(f"cannot open image: {e}")
        return r
    rep = validate_sprite_image(img.convert("RGBA"), specs[type_key], label=str(path))
    return rep


def validate_creature_dir(d: Path, specs: dict) -> list[Report]:
    reports: list[Report] = []
    meta_path = d / "metadata.json"
    meta = json.loads(meta_path.read_text()) if meta_path.is_file() else None
    if meta is None:
        r = Report(str(d))
        r.warn("no metadata.json")
    for role, type_key in ROLE_TO_TYPE.items():
        # Prefer the filename recorded in metadata, else the spec default.
        fname = specs[type_key]["file"]
        if meta and role in meta.get("sprites", {}):
            fname = meta["sprites"][role].get("file", fname)
        f = d / fname
        if not f.is_file():
            continue
        rep = validate_file(f, type_key, specs)
        # cross-check metadata dims
        if meta and role in meta.get("sprites", {}):
            ms = meta["sprites"][role]
            img = Image.open(f)
            if (ms.get("width"), ms.get("height")) != img.size:
                rep.err(f"metadata says {ms.get('width')}x{ms.get('height')} but file is "
                        f"{img.size[0]}x{img.size[1]}")
        reports.append(rep)
    return reports


def validate_tree(repo: Path, specs: dict) -> list[Report]:
    reports: list[Report] = []
    creatures = repo / "assets" / "creatures"
    if creatures.is_dir():
        for d in sorted(p for p in creatures.iterdir() if p.is_dir()):
            reports.extend(validate_creature_dir(d, specs))
    trainers = repo / "assets" / "trainers"
    if trainers.is_dir():
        for f in sorted(trainers.glob("*.png")):
            # `<stem>_actions.png` is a layer-3 action sheet (4×2); the rest are walk sheets.
            kind = "human-actions" if f.stem.endswith("_actions") else "human-overworld"
            reports.append(validate_file(f, kind, specs))
    emotes = repo / "assets" / "effects" / "emotes.png"
    if emotes.exists():
        reports.append(validate_file(emotes, "emote", specs))
    return reports


def find_repo_root(start: Path) -> Path:
    for d in (start, *start.parents):
        if (d / ".git").exists():
            return d
    return start


def main() -> int:
    specs = load_specs()
    p = argparse.ArgumentParser(description="Validate PixelKin sprites against the art spec.")
    p.add_argument("--all", action="store_true", help="Validate the whole assets/ tree.")
    p.add_argument("--creature-dir", help="Validate one assets/creatures/NNN_slug folder.")
    p.add_argument("--file", help="Validate a single sprite file (needs --type).")
    p.add_argument("--type", choices=sorted(specs), help="Sprite type for --file.")
    p.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    p.add_argument("--quiet", action="store_true", help="Only print failures.")
    args = p.parse_args()

    if args.file:
        if not args.type:
            p.error("--file requires --type")
        reports = [validate_file(Path(args.file), args.type, specs)]
    elif args.creature_dir:
        reports = validate_creature_dir(Path(args.creature_dir), specs)
    elif args.all:
        reports = validate_tree(find_repo_root(Path.cwd().resolve()), specs)
    else:
        p.error("choose one of --all / --creature-dir / --file")

    n_err = n_warn = 0
    for rep in reports:
        n_err += len(rep.errors)
        n_warn += len(rep.warns)
        failed = rep.errors or (args.strict and rep.warns)
        if args.quiet and not failed and not rep.warns:
            continue
        status = "FAIL" if rep.errors else ("WARN" if rep.warns else "OK")
        print(f"[{status}] {rep.target}")
        for e in rep.errors:
            print(f"    error: {e}")
        for w in rep.warns:
            print(f"    warn:  {w}")

    print(f"\n{len(reports)} sprite(s): {n_err} error(s), {n_warn} warning(s)")
    if n_err or (args.strict and n_warn):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
