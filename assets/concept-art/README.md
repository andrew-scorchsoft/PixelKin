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

One 3:2 mood piece per place, in three sets. Slugs match
[`docs/world/atlas.md`](../../docs/world/atlas.md).

**`areas/<slug>.webp`** — the world-map areas & routes (19):

| Region | Pieces |
|--------|--------|
| south | `tinderwick`, `dimglass-coast`, `pearlmoor-quay`, `dawnstead` |
| east | `saltreach-fen`, `lowleaf-hollow`, `cinderhead-mine` |
| north | `galehigh-terraces`, `windward-stair`, `pale-vault-glacier`, `hushfrost-pass` |
| west | `sunken-solarium`, `sunvault-climb`, `nightreach-observatory` |
| outer | `vesper-crossroads`, `coldfog-marches`, `lanternway` |
| central | `penumbra-ring`, `umbral-spire` |

(The 14 area cards plus the 5 connective routes that aren't cards.)

**`lumenaries/<element>.webp`** — the 8 Lumenary (gym) interiors, one per
constellation element, each an empty arena-shrine with its constellation in the
domed ceiling: `ember` (Tinderwick), `tide` (Pearlmoor), `verdant` (Lowleaf),
`stone` (Cinderhead), `storm` (Galehigh), `frost` (Pale Vault), `solar`
(Solarium), `lunar` (Nightreach).

**`landmarks/<slug>.webp`** — distinct micro-dungeons & set-pieces beyond the
area cards: `glowmoss-deep` (glowing cave interior), `tideglass-cavern`
(sea-cave), `wind-eye` (sky-grotto), `hollowfen-stillworks` (derelict null-works
— the "old power-plant"), `drownlight-beacon` (snuffed lighthouse), `starwell`
(post-Crown shrine).

(41 pieces total. The remaining minor optional spurs — Gullcry Rock, Sunkbell
Shallows, Spore Grotto, Crystoll Vault, Thunderroost, Aurora Hollow, Helia
Vault — aren't done yet; add them the same way if/when they want art.)

## How they were made / how to regenerate

[`gen.sh`](./gen.sh) wraps the **generate-image** skill with the shared
"Long Dusk" pixel-art style preamble (palette anchors, GBC→GBA register, no
anti-aliasing, original-only) baked in, so the set stays cohesive. To redo or
add one:

```bash
bash assets/concept-art/gen.sh <subdir>/<slug> "<subject brief drawn from the area card>"
# e.g.  areas/tinderwick   lumenaries/ember   landmarks/wind-eye
```

The `<slug>` may include its subfolder (`areas/…`, `lumenaries/…`,
`landmarks/…`); `gen.sh` creates the folder and writes `assets/concept-art/<slug>.webp`.

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
