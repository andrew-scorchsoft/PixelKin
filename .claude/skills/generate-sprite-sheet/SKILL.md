---
name: generate-sprite-sheet
description: Generate consistent, standard-compliant PixelKin sprites and sprite sheets (creature battle/icon/overworld/portrait art, NPC walk sheets, battle effects, world tiles) from original briefs. Uses Google Nano Banana Pro by default (best for transparency and reference fidelity), with OpenAI gpt-image-2 as a selectable fallback, via the generate-image skill — then deterministically snaps every result to the exact canvas size and anchor defined in docs/art-style.md. Use whenever the user wants a creature sprite, character sprite, walk sheet, battle effect, tile, icon, or portrait for the game.
---

# generate-sprite-sheet

Produces game sprites that obey the **PixelKin Art & Sprite Bible**
(`docs/art-style.md`). Read that doc — it is the source of truth for every rule
this skill enforces. The skill is the mechanical arm of it: a model makes the
art, a Python script makes it land on the exact canvas, every time.

## The core idea (read this first)

There are **two systems**, kept deliberately separate:

1. **The art spec** — strict per-type rules (canvas, palette, lighting, pose,
   anchor). Lives in `docs/art-style.md` + `scripts/sprite-specs.json`.
2. **Packing/loading** — assembling source images into atlases for Phaser
   (a future build step; see the art bible §9).

This skill owns generating **standardised source images** for system 1. **Do
not** ask the image model to produce one giant master sheet of many creatures —
models drift on grids and you'll hand-fix dozens of cells. One creature pack at
a time; code does the layout.

## When to use

- The user wants any creature art: **battle front/back, icon, overworld
  mini-sprite, or portrait**.
- An **NPC/human walking sheet** (3×4, directional).
- A **battle effect** animation sheet (sparks, slashes, bursts).
- A **world tile** (16×16, tileable).
- A **cohesive area tile set** — many related 16×16 tiles (ground, path, water, edges,
  cliff, roof, wall, decor) generated to share one palette, then packed into a tileset
  atlas + metadata. See **Generating a map tile set** below.

Do **not** use it for: UI chrome you can build in CSS/HTML, the logo (already in
`assets/`), or music/SFX (use `generate-music`).

## Image model

**Default: Google Nano Banana Pro** (`gemini-3-pro-image-preview`). It renders
on a magenta field that the generate-image skill keys out to a transparent PNG,
and it's the most reliable here — it handles transparency cleanly and stays
faithful to a **reference image** (important for matching the logo creatures).

**Fallback: OpenAI `gpt-image-2`** (`--provider openai`). Two caveats made it
the fallback rather than the default:

- gpt-image-2 has **no native transparent mode** (only the older gpt-image-1
  does), so the skill renders it on a flat **magenta `#FF00FF`** field and
  chroma-keys it out itself.
- its **safety filter can reject benign prompts** (it blocked plain
  cute-creature briefs in testing). If you hit a `400 rejected by the safety
  system`, that's why — switch to the default Google path.

See docs/art-style.md §6 for the transparency pipeline.

## Prerequisites

- Run via the **project venv**: `./venv/bin/python …` from the repo root. The
  script needs Pillow (and numpy for clean edges) — both in `requirements.txt`.
  If the venv doesn't exist: `python3 -m venv venv && ./venv/bin/pip install -r requirements.txt`.
- **`GOOGLE_AI_STUDIO_API_KEY`** in the environment for the default path (or
  `OPENAI_API_KEY` for `--provider openai`). The skill delegates the actual API
  call to the sibling `generate-image` skill.

## How it works

For each asset the script:

1. Builds a prompt = magenta chroma-key preamble + shared **style preamble** +
   **originality clause** + the locked **per-type template**
   (`sprite-specs.json`) + your **subject**.
2. Calls `generate-image` with **gpt-image-2** to render the sprite on flat
   magenta, then **keys the magenta out** to a transparent source.
3. **Snaps** it to the type's exact pixel canvas: alpha-trim → scale to the fill
   fraction → composite at the type's anchor. Multi-frame sheets are aligned
   **per cell**, so every frame shares a baseline (feet line up).
4. Saves a transparent **PNG**, and for creatures writes/updates `metadata.json`.

## How to call it

```bash
# A creature battle front sprite, auto-filed under assets/creatures/001_sproutle/
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/generate_sprite.py \
  --type creature-front \
  --subject "a small round sprout creature, leaf-tail, big friendly eyes, leaf-green and cream palette" \
  --creature-id 1 --creature-slug sproutle
```

```bash
# An NPC walk sheet to an explicit path
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/generate_sprite.py \
  --type human-overworld \
  --subject "a young traveller in a red cap and blue jacket, satchel on one shoulder" \
  --output assets/trainers/player.png
```

```bash
# A battle effect sheet
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/generate_sprite.py \
  --type effect \
  --subject "a burst of leaf shards spinning outward then fading" \
  --output assets/effects/leaf_burst.png
```

Always `./venv/bin/python` — bare `python` isn't on PATH and `python3` lacks the
deps.

### Sprite types

Run `--list-types` for the live list. Current types (all defined in
`scripts/sprite-specs.json`, canvases per `docs/art-style.md` §4):

| Type                 | Canvas | Grid | Anchor        |
|----------------------|-------:|:----:|---------------|
| `creature-front`     |  64×64 | 1×1  | bottom-centre |
| `creature-back`      |  64×64 | 1×1  | bottom-centre |
| `creature-icon`      |  32×32 | 1×1  | centre        |
| `creature-overworld` |  32×32 | 1×1  | bottom-centre |
| `creature-portrait`  |  96×96 | 1×1  | centre        |
| `human-overworld`    |  32×32 | 3×4  | bottom-centre |
| `effect`             |  32×32 | 4×4  | centre        |
| `tile`               |  16×16 | 1×1  | top-left      |
| `tile-ground` / `tile-path` / `tile-water` / `tile-water-edge` / `tile-cliff` / `tile-cliff-edge` / `tile-roof` / `tile-wall` | 16×16 | 1×1 | top-left | 
| `tile-decor`         |  16×16 | 1×1  | centre        |

The `tile-*` subtypes are role-specific variants of `tile` for building a cohesive area
set (edge tiles are prompted to match their neighbours; `tile-decor` keeps transparency
around a small object). Use them with `--area`/`--palette` (see **Generating a map tile
set**).

### Arguments worth knowing

- `--type` *(required)* — sprite type (see table / `--list-types`).
- `--subject` *(required unless `--from-image`)* — your **original** brief for
  the creature/character/effect. Describe by genre and mood; never reference a
  real franchise (VISION.md). The style/canvas/pose come from the template — you
  supply *what it is*.
- `--output` — explicit `.png` destination. **Or** use the creature convention:
- `--creature-id N` + `--creature-slug name` — auto-files under
  `assets/creatures/NNN_slug/<role>.png` and writes/updates `metadata.json`.
- `--reference PATH` — a reference image to keep the subject visually
  consistent (e.g. a crop of the same creature from the logo, or its own front
  sprite when generating its back/icon). Repeat for multiple. Routed to
  `generate-image --input-image`; gpt-image-2 honours references via its edits
  route.
- `--provider openai|google` — image provider. **`openai` (default)** uses
  **gpt-image-2** + magenta chroma-key. `google` uses Nano Banana Pro's native
  transparent path.
- `--resample lanczos|box|nearest` — downscale filter. **`lanczos` (default)**
  reads cleanest at tiny sizes; `nearest` gives the hardest edges. (Rendering
  stays crisp regardless — Phaser nearest-upscales the small source.)
- `--fill F` — override the subject's fill fraction (0–1) for this run.
- `--no-align` — for sheets, skip per-frame baseline alignment and just
  downscale the whole sheet (use if the model's own layout was already good and
  the per-cell trim is clipping something).
- `--area NAME` — (with a `tile`/`tile-*` type) names the area's tile set: appends the
  shared **area-style cohesion clause** to the prompt and auto-files the tile under
  `assets/tilesets/<area>/<role>.png`. See **Generating a map tile set**.
- `--palette "desc"` — the area's shared palette description (derive it from
  `assets/tilesets/world-palette.json`). Used with `--area` so every tile in the set
  matches.
- `--from-image PATH` — skip the API call and just run the snap pipeline on an
  existing transparent PNG. Useful for cleaning up hand-made art or a sprite you
  already generated.
- `--keep-temp` — also save the raw high-res generation next to the output.
- `--list-types` — print all types and exit.

## Generating a map tile set

A map area (a town, a route, a cave) needs a *set* of tiles that read as one place. Same
two-system split: the model makes each tile, `pack_tileset.py` assembles them. Briefs and
the world palette come from the world docs (`docs/world/atlas.md`, `docs/world/README.md`,
and the master `assets/tilesets/world-palette.json`).

**Step 1 — generate the tiles, anchor-first for cohesion.** Generate the area's **ground
tile first**, then pass it as `--reference` to every sibling tile so palette and pixel
density carry across the set. Give every tile the same `--area` and `--palette`:

```bash
AREA=tinderwick
PAL="blue-hour coastal village: bone-cream walls, warm fire-orange candlelight, deepBlue sea, grass verges, soil paths, ink outlines"
GEN=.claude/skills/generate-sprite-sheet/scripts/generate_sprite.py

# anchor tile first (auto-files to assets/tilesets/tinderwick/ground.png)
./venv/bin/python $GEN --type tile-ground --area $AREA --palette "$PAL" \
  --subject "short coastal meadow grass, cool morning green"

# then the rest, seeded with the ground tile as a reference (fire in parallel)
./venv/bin/python $GEN --type tile-path  --area $AREA --palette "$PAL" \
  --reference assets/tilesets/$AREA/ground.png --subject "packed sandy footpath"
./venv/bin/python $GEN --type tile-water --area $AREA --palette "$PAL" \
  --reference assets/tilesets/$AREA/ground.png --subject "calm deepblue sea, gentle cyan ripples"
./venv/bin/python $GEN --type tile-water-edge --area $AREA --palette "$PAL" \
  --reference assets/tilesets/$AREA/ground.png --subject "wet sand shoreline meeting the sea"
# …roof, wall, cliff, cliff-edge, decor as the area needs
```

Run the self-check loop on each tile (and eyeball that a few laid edge-to-edge don't seam
or buzz). The two prior areas' ground tiles make good extra `--reference`s so neighbouring
regions read as one world.

**Step 2 — pack into an atlas + tileset metadata.** Write a manifest in the area's tile
folder that fixes tile order and the per-tile properties the game reads (`collides`,
`requires_ability`, `encounter_terrain`), then pack:

```jsonc
// assets/tilesets/tinderwick/tileset.manifest.json
{ "name": "tinderwick_set", "columns": 8, "tiles": [
  { "file": "ground.png", "role": "ground", "encounter_terrain": "tall_grass" },
  { "file": "path.png",   "role": "path" },
  { "file": "wall.png",   "role": "wall",  "collides": true },
  { "file": "water.png",  "role": "water", "collides": true,
    "requires_ability": "tidecall", "encounter_terrain": "water" }
] }
```

```bash
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_tileset.py \
  --tiles-dir assets/tilesets/tinderwick
# -> public/assets/tilesets/tinderwick_set.png  +  tinderwick_set.tileset.json
```

The emitted `<name>.tileset.json` is consumed directly by the game's map loader (its
per-tile `collides` / `requires_ability` / `encounter_terrain` drive collision,
ability-gating, and encounters — see `src/game/data/world/types.ts`). A map JSON then
references the atlas via a `TilesetRef` and assigns its `first_gid`.

Generated source tiles live at repo-root `assets/tilesets/<area>/` (not served); the packed
atlas + metadata land in `public/assets/tilesets/` (served by Vite).

## Two layers of checking

Generation is checked at **two** levels — keep them distinct:

1. **Geometry — automated** (`validate_sprites.py`). Deterministic, free, and
   **baked in**: it asserts the *measurable* spec — canvas size, real alpha,
   anchor position, fill, no visible magenta, and per-frame baselines on sheets.
2. **Art — the self-check loop** (you, below). The *judgement* calls a script
   can't make: subject, style, artifacts, **originality**.

The validator can't tell you a sprite looks like another franchise; the
self-check can't measure a 1px baseline drift across 12 frames. You need both.

## Validation — the automated test

`scripts/validate_sprites.py` is the testing mechanism for the art spec. It runs
**automatically after every generation** (the JSON summary carries a
`validation: { ok, errors, warnings }` block — if `ok` is false, fix it before
moving on), and you can also run it standalone as a CI/spec gate:

```bash
# Validate the whole asset tree (exit non-zero on any error)
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/validate_sprites.py --all

# One creature folder (also cross-checks metadata.json against the files)
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/validate_sprites.py \
  --creature-dir assets/creatures/001_vulpyre

# A single file against a type
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/validate_sprites.py \
  --file assets/trainers/player_indi.png --type human-overworld
```

It checks each sprite for: correct **dimensions** for its type; a real **alpha
channel** with an actually-transparent background; no visible **magenta** chroma
bleed; correct **anchor** (bottom-centre / centre / top-left) and a sensible
**fill** with no edge **clipping**; and for sheets, that **every frame is
non-empty and all frames share a baseline**. Creature folders also assert
`metadata.json` matches the files on disk. Errors fail the run; softer issues are
warnings (`--strict` promotes warnings to failures). Wire `--all` into CI to keep
the whole dex spec-compliant as it grows.

## The self-check loop — mandatory

The validator covers geometry; it does **not** judge the art. You do. Each
call costs money — be deliberate.

After every generation:

1. **Open the saved PNG** with `Read` (it renders visually).
2. **Verify against the brief and the art bible:**
   - Subject, pose, and viewpoint match the type (e.g. front sprite is a
     ¾-front view; back sprite reads as the *same species* from behind).
   - **Pixel-art rules honoured** — hard edges, no anti-aliasing/blur, limited
     palette (~8–16 colours), dark non-black outline, top-left light.
   - **No artifacts** — extra limbs, fused shapes, melted features.
   - **Originality** — does **not** resemble any existing franchise's creature,
     silhouette, or palette signature. If it drifts toward something
     recognisable, regenerate with a more distinctive brief. (This is a hard
     gate — see VISION.md.)
   - Silhouette reads at the target size (especially icons at 32px).
3. **For sheets**, check every frame: directions correct (down/left/right/up
   rows), walk cycle reads, and **feet share a baseline** across frames. If one
   cell is off, try `--no-align` or regenerate.
4. **If it passes**, report the path + summary. Done.
5. **If it fails**, regenerate naming the *specific* problem (e.g. *"left-facing
   row is facing right; mirror it"*, or *"palette is too noisy — cut to ~12
   flat colours, harder outline"*). **Max 3 attempts** per asset, then stop and
   report what's wrong rather than burning budget.

## Generating many — parallel & background

One invocation = one asset. For a batch (a creature's full set, or several
creatures), fire **one `Bash` call per asset in a single response** so the
harness runs them concurrently, or use `run_in_background: true` and continue
other work while they render. Then run the self-check loop per file.

Rules that still apply:
- **Plan briefs up front** (type, subject, output for each).
- **Distinct output paths** — concurrent calls to the same `--output` clobber.
- The **3-attempt cap is per asset**, not per batch.
- **Don't parallelise regenerations of the same asset** — inspect, adjust, retry.

## Honest limitations

- Image models are weak at exact grids. **Single-frame types are the robust
  path.** For sheets, per-frame alignment helps a lot but can't fix a model that
  drew the wrong number of frames or the wrong directions — inspect and iterate.
- Getting truly crisp, grid-aligned pixel art from a 1024px generation is hard.
  The output reads as authentic pixel art because the final canvas is tiny, but
  it won't be hand-pixelled perfection. For hero assets, treat generation as a
  strong base and clean up by hand if needed (then re-run with `--from-image`).
- This skill **does not** build creature/sprite atlases. That's the separate packing step
  (art bible §9), intentionally left to code, not the model. (Map **tilesets** are the one
  packing step that exists today — `pack_tileset.py`, see **Generating a map tile set**.)

## What it deliberately does *not* do

- **Does not auto-commit.** Show the user the result; let them decide what to
  keep.
- **Does not invent creature names, types, or lore** — that's data-driven
  content for `src/game/data/`. The skill fills sprite geometry into
  `metadata.json`; you fill `name`/`types`.
- **Does not produce one giant multi-creature master sheet.** By design. See the
  two-system principle above.
