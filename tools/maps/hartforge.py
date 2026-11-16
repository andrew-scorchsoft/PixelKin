#!/usr/bin/env python3
"""
hartforge — the Hartway's prop kit (the mountain behind Wayward Rise).

Its OWN master folder (like paulforge/sereforge), packed as `hartway_<stem>`:

    assets/tilesets/hartway/objects/<stem>.png

  rope_ladder (1x5)  DRAWN: the rope ladder Greg fixes down a cliff band once a ridge
                     is behind you. Never solid: the matching flag-gated `spans` ladder
                     (wildkit / SpanZone.requires_flag) is what makes it climbable.
  ruin_hut (4x4)     image-gen master (raw/ruin_hut.png, native alpha) snapped here: the
                     climbers' bothy at the Seat, taken back by the mountain's kin.
  bench (2x1)        image-gen master (raw/bench.png): the Seat itself.

Run:  python3 tools/maps/hartforge.py
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
RAW = REPO / "assets/tilesets/hartway/raw"
OBJ = REPO / "assets/tilesets/hartway/objects"

INK = (38, 30, 44, 255)
ROPE = (204, 170, 112, 255)
ROPE_D = (150, 116, 76, 255)
RUNG = (156, 110, 70, 255)
RUNG_L = (206, 160, 104, 255)
PEG = (120, 124, 140, 255)


def rope_ladder(th: int = 5) -> Image.Image:
    im = Image.new("RGBA", (16, th * 16))
    d = ImageDraw.Draw(im)
    h = th * 16
    for x in (4, 11):                                   # the two ropes (ink, rope, shade)
        d.line([(x - 1, 2), (x - 1, h - 3)], fill=INK)
        d.line([(x + 1, 2), (x + 1, h - 3)], fill=INK)
        d.line([(x, 2), (x, h - 3)], fill=ROPE)
        for y in range(4, h - 3, 4):                    # the lay of the rope
            d.point((x, y), fill=ROPE_D)
    for y in range(6, h - 4, 6):                        # rungs
        d.rectangle([3, y - 1, 12, y + 1], fill=INK)
        d.line([(4, y), (11, y)], fill=RUNG)
        d.line([(4, y - 1), (11, y - 1)], fill=RUNG_L)
    for x in (4, 11):                                   # iron pegs at the lip
        d.rectangle([x - 1, 0, x + 1, 2], fill=INK)
        d.point((x, 1), fill=PEG)
    return im


def snap(stem: str, tw: int, th: int, *, fill: float = 1.0) -> Image.Image:
    """Crop an image-gen master to its art, fit it bottom-centred on a tw x th canvas,
    hard alpha (no glow halo on the dark world)."""
    im = Image.open(RAW / f"{stem}.png").convert("RGBA")
    a = np.asarray(im)
    ys, xs = np.where(a[..., 3] > 160)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    k = min(tw * 16 * fill / im.width, th * 16 * fill / im.height)
    w, h = max(1, round(im.width * k)), max(1, round(im.height * k))
    im = im.resize((w, h), Image.BOX)
    arr = np.asarray(im).copy()
    arr[..., 3] = np.where(arr[..., 3] >= 140, 255, 0)
    out = Image.new("RGBA", (tw * 16, th * 16))
    out.alpha_composite(Image.fromarray(arr), ((tw * 16 - w) // 2, th * 16 - h))
    return out


def main() -> None:
    OBJ.mkdir(parents=True, exist_ok=True)
    rope_ladder(5).save(OBJ / "rope_ladder.png")
    snap("ruin_hut", 4, 4).save(OBJ / "ruin_hut.png")
    snap("bench", 2, 1).save(OBJ / "bench.png")
    for p in sorted(OBJ.glob("*.png")):
        print(f"  {p.relative_to(REPO)}  {Image.open(p).size}")


if __name__ == "__main__":
    main()
