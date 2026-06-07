#!/usr/bin/env bash
# Concept-art mood pieces for every Vesperholm area & route.
# Usage: gen.sh <slug> "<subject brief>"
# Bakes the shared PixelKin "Long Dusk" pixel-art style into every prompt so the
# whole set reads as one cohesive game. These are inspiration/key-art thumbnails,
# NOT tilesets and NOT top-down maps.
set -euo pipefail
cd "$(dirname "$0")/../.."

SLUG="$1"
SUBJECT="$2"

STYLE='Retro 2D pixel-art landscape illustration in the style of a late-1990s/early-2000s \
handheld console (Game Boy Color register growing toward early-GBA/SNES mood painting). \
Chunky deliberate pixels, hard 1-pixel edges, NO anti-aliasing, no blur, no smooth gradients \
(only deliberate dithered shading), a tight cohesive palette of roughly 16-24 colours, deep \
ink outlines, top-left light source. This is an atmospheric ESTABLISHING wide shot / box-art \
thumbnail that captures the MOOD and feel of the place as a painterly pixel scene with a clear \
horizon and depth — it is NOT a tileset, NOT a top-down map grid, and NOT a UI screen. \
World: Vesperholm during The Long Dusk, a perpetual blue-hour twilight where night fell and \
will not lift; cosy and a little melancholy, "lanterns in the dark," with a deep starfield and \
faint constellations overhead waiting to be relit. Anchor palette: night #0b1026, deep blue \
#13205a, bright cyan #9fe7ff, leaf green #7bdc6b, warm fire orange #ff8a3d, water blue #4fb4ff, \
ink #1a1430, bone cream #f5f0e1. Fully ORIGINAL — inspired by the creature-collecting genre but \
a copy of nothing; no real-world brands, no franchise references. No text, no words, no logos, \
no UI, no HUD, no frame, no watermark, no creatures and no people (at most tiny distant \
silhouettes).'

exec ./venv/bin/python .claude/skills/generate-image/scripts/generate.py \
  --prompt "$SUBJECT $STYLE" \
  --aspect 3:2 \
  --quality 90 \
  --output "assets/concept-art/areas/${SLUG}.webp"
