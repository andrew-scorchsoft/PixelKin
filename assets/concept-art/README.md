# Concept art — area mood pieces

Inspiration **key-art / mood thumbnails** for every area and route in
*Vesperholm — The Long Dusk*. One wide pixel-art establishing shot per place,
all generated to one cohesive style so the whole world reads as a single game.

> **These are inspiration, not game assets.** They are *not* tilesets, *not*
> top-down maps, and *not* battle backdrops (those live in
> `public/assets/backgrounds/battle/`). They set the mood/feel of each place and
> serve as a **visual reference** for downstream art — most usefully as an
> `--input-image` reference when generating that area's **tileset** so the tiles
> inherit the right palette, lighting and atmosphere.

## What's here

`areas/<slug>.webp` — one 3:2 mood piece per area/route. Slugs match the area
cards in [`docs/world/atlas.md`](../../docs/world/atlas.md):

| Region | Pieces |
|--------|--------|
| south | `tinderwick`, `dimglass-coast`, `pearlmoor-quay`, `dawnstead` |
| east | `saltreach-fen`, `lowleaf-hollow`, `cinderhead-mine` |
| north | `galehigh-terraces`, `windward-stair`, `pale-vault-glacier`, `hushfrost-pass` |
| west | `sunken-solarium`, `sunvault-climb`, `nightreach-observatory` |
| outer | `vesper-crossroads`, `coldfog-marches`, `lanternway` |
| central | `penumbra-ring`, `umbral-spire` |

(19 total — the 14 area cards plus the 5 connective routes that aren't cards.)

## How they were made / how to regenerate

[`gen.sh`](./gen.sh) wraps the **generate-image** skill with the shared
"Long Dusk" pixel-art style preamble (palette anchors, GBC→GBA register, no
anti-aliasing, original-only) baked in, so the set stays cohesive. To redo or
add one:

```bash
bash assets/concept-art/gen.sh <slug> "<subject brief drawn from the area card>"
```

Each area's subject brief is paraphrased from its **Graphics** line in
`atlas.md`. Inspect every result by eye (the model occasionally bakes in a
colour-palette swatch strip or a paper border — regenerate naming that problem).

## Using one as tileset reference

When generating an area's tiles, pass its mood piece as a reference so the
tileset matches the concept:

```bash
./venv/bin/python .claude/skills/generate-image/scripts/generate.py \
  --prompt "<tile brief> … Match the palette, lighting and mood of the reference image." \
  --input-image assets/concept-art/areas/<slug>.webp \
  --output <tile output>
```
