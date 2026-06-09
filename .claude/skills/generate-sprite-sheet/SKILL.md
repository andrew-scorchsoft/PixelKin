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
- An **NPC/human walking sheet** (4×4, directional — a real walk cycle).
- A **battle effect** animation sheet (sparks, slashes, bursts).
- A **world tile** (16×16, tileable).
- A **cohesive area tile set** — best built the modern way: paint a coherent
  terrain family / scene as ONE picture and **slice it into tiles with code**
  (see **The richer tile pipeline** below), which fixes the seam/flatness/drift
  problems isolated per-tile generation causes. The older per-tile recipe
  (**Generating a cohesive area tile set**) still works for one-off tiles.
- An **autotile terrain** (grass/water/cliff with clean corners & edges) and
  **animated tiles** (water ripple, lamp) — see **The richer tile pipeline**.

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

1. Builds a prompt = shared **style preamble** + **originality clause** + the
   locked **per-type template** (`sprite-specs.json`) + your **subject** (plus a
   magenta chroma-key preamble only on the OpenAI path).
2. Calls `generate-image`. **Default Google Nano Banana Pro** returns native
   transparency; the OpenAI path renders on flat magenta and **keys it out**.
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
| `human-overworld`    |  32×32 | 4×4  | bottom-centre |
| `human-pose`         |  32×32 | 1×1  | bottom-centre |
| `human-actions`      |  32×32 | 4×2  | bottom-centre |
| `emote`              |  32×32 | 4×2  | centre        |
| `effect`             |  32×32 | 4×4  | centre        |
| `tile`               |  16×16 | 1×1  | top-left      |
| `tile-ground` / `tile-soil` / `tile-sand` / `tile-floor` / `tile-path` / `tile-water` / `tile-water-edge` / `tile-cliff` / `tile-cliff-edge` / `tile-roof` / `tile-wall` / `tile-door` / `tile-fence` | 16×16 | 1×1 | top-left | 
| `tile-decor`         |  16×16 | 1×1  | centre        |

The `tile-*` subtypes are role-specific variants of `tile` for building a cohesive area
set (edge tiles are prompted to match their neighbours; `tile-decor` keeps transparency
around a small object). Use them with `--area`/`--palette` (see **Generating a map tile
set**).

### Character animation — three layers (docs/art-style.md §A/§A2/§A3)

A character animates from up to three sheets, all on the same 32×32 grid:

1. **`human-overworld`** (4×4) — the walk sheet. **Required** for every character.
   *Running* is free (same frames, faster), so don't expand this sheet.
2. **`emote`** (4×2) — the **one shared** reaction-bubble sheet for the whole
   game (alert/question/heart/…). Generate once into `assets/effects/emotes.png`;
   reused by every character. Don't bake emotes into per-character sheets.
3. **`human-actions`** (4×2) — **optional** bespoke event poses (raise-lamp,
   toss, gift, sit, hurt), mainly the player. **Build it the robust way:**
   generate each pose with `--type human-pose` (single 32×32, with the character's
   walk sheet as `--reference`), then assemble with `assemble_action_sheet.py` —
   do **not** ask the model for the whole 8-cell grid at once (it subdivides cells
   and repeats stances). Save as `assets/trainers/<stem>_actions.png`.

`pack_trainers.py` packs all three (walk + `<stem>_actions` + the shared
`emotes.png`) into `public/assets/sprites/trainers/` and one manifest; the engine
(`entities/Actor.ts`: `playAction`, `showEmote`) loads them via `PreloadScene`.

```bash
GEN=.claude/skills/generate-sprite-sheet/scripts
REF=assets/trainers/player_indi.png
# 8 poses in cell order (raise-start, raise-hold, toss-wind, toss-throw, gift-raise, gift-cast, sit, hurt)
$GEN/generate_sprite.py --type human-pose --reference $REF --subject "<char> holding a lantern aloft, glowing" --output /tmp/p1.png
# …generate the other 7…
$GEN/assemble_action_sheet.py --output assets/trainers/player_indi_actions.png /tmp/p0.png … /tmp/p7.png
$GEN/pack_trainers.py
```

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
- `--provider google|openai` — image provider. **`google` (default)** uses Nano
  Banana Pro's native transparent path. `openai` uses gpt-image-2 + magenta
  chroma-key (fallback; its safety filter can reject benign briefs).
- `--resample lanczos|box|nearest` — downscale filter. **`lanczos` (default)**
  reads cleanest at tiny sizes; `nearest` gives the hardest edges. (Rendering
  stays crisp regardless — Phaser nearest-upscales the small source.)
- `--fill F` — override the subject's fill fraction (0–1) for this run.
- `--no-align` — for sheets, skip per-frame baseline alignment and just
  downscale the whole sheet (use if the model's own layout was already good and
  the per-cell trim is clipping something).
- `--area NAME` — (with a `tile`/`tile-*` type) names the area's tile set: appends the
  shared **area-style cohesion clause** to the prompt and auto-files the tile under
  `assets/tilesets/<area>/<role>.png`. See **Generating a cohesive area tile set**.
- `--palette "desc"` — the area's shared palette description (derive it from
  `assets/tilesets/world-palette.json`). Used with `--area` so every tile in the set
  matches.
- `--from-image PATH` — skip the API call and just run the snap pipeline on an
  existing transparent PNG. Useful for cleaning up hand-made art or a sprite you
  already generated.
- `--keep-temp` — also save the raw high-res generation next to the output.
- `--list-types` — print all types and exit.

## The richer tile pipeline (paint together → slice) — PREFERRED

Isolated 16×16 tile generation is the root cause of flat, washed-out, seamy
maps: the model can't see the neighbour a tile must line up with, so edges don't
meet and the palette drifts. The fix (docs/art-style.md §11–§15) applies the
two-system rule one level up — **the model paints a coherent picture; code cuts
the tiles out of it.** Four scripts plus the autotile tooling:

| Script | Job |
|--------|-----|
| `generate_block.py` | Paint a coherent **block**: a terrain family, an area scene mockup, or an animation strip (kept full-res). |
| `slice_tileset.py` | Cut a block onto the 16px grid into tiles + a draft `tileset.manifest.json`; `--harvest` dedupes a scene; `--layout` tags autotile roles. |
| `quantize_to_palette.py` | Snap tiles to the area's locked `working_palette` (kills colour drift / flatness). |
| `make_tileable.py` | Toroidal seam fix for a uniform fill; `--axis h\|v` seam-matches a directional EDGE tile along its run. |
| `render_map.py` | Composite a finished map to a PNG for **by-eye QA** against the handheld bar. |
| `validate_map.py` | Automated gate: layers / autotile-vocab / **meshing** / decoration / border. Must PASS. |
| `tools/autotile/expand.mjs` | Expand a map's `terrain` layer into corner/edge/strip gids (blob autotiling; off-map = continuation). |
| `tools/autotile/composite_overlay.py` | Build a seamless 9-slice **+ strips** for a FLAT transition (dirt/blades over grass) from two uniform fills. |
| `tools/maps/build_tinderwick.py` | **Reference area builder** — copy it: procedural layout + the full tileset/seam pipeline, gold standard. |

### A) Autotile terrains — the seamless standard (PROVEN, hard-won)

Every special surface in an area (grass, path, sand, water, forest/tree-wall,
cliff) is an autotile **BODY** — a `terrain` presence layer meshed by
`tools/autotile/expand.mjs`, **never** independent fill tiles plonked down. Two
kinds of terrain, two methods — pick by whether the transition is flat or organic.

> **The deterministic finishing kit comes FIRST (no API).** Before generating new
> art, check `tools/maps/tileforge.py` — the 2026-06 quality pass lives there and
> closes most of the gap to the reference-era bar: `texture_grass` (blade dashes on
> flat ground fills), `tallgrass_tuft` (the encounter tile — **tall grass is now
> hard-edged fill-only by design**, classic-style, no transition ring), `grade` +
> `cliff_strata` + `cliff_wall_edge` (lifted stratified cliff whose S/W/E edges are
> complete wall tiles: lit rim → face → dark contact seam → ground), `deglow`
> (kills baked highlight rims on pale fills), **`flatten_vignette` on every fill +
> `flatten_axis` on every edge/strip** (the per-tile-border "joints" cure; edge
> variants are flips, never rolls; value-match edges to their fill — level-design
> §11), `key_alpha` (props generated on an opaque card — the "white bag" cure;
> better: place the 1×3 lamp-post OBJECT, never a 1-tile lamp), `inner_corner`
> (13-piece completion — good for path/sand/tree/cliff, **skip water**), and drawn
> props (`draw_fence_h`,
> `draw_fence_post`, `draw_boulder`, `draw_flowerbed`). `build_shared_overworld.py`
> applies all of these when packing the shared set. Compose maps to
> `docs/world/level-design.md` **§11** (the composition standard).

**FLAT transition (path-on-grass, tall-grass-on-grass) → COMPOSITE, do NOT AI-paint.**
AI-painting flat path cells gives mismatched dirt, per-tile banding, and a junction
tile that doesn't match the strips. Build the whole set deterministically from two
**uniform fills** with `tools/autotile/composite_overlay.py`:

```bash
# dirt16/blades16/grass16 = uniform fills (see "Seamless fills" below), make_tileable'd
python tools/autotile/composite_overlay.py /tmp/dirt16.png   /tmp/grass16.png /tmp/path_auto --depth 3
python tools/autotile/composite_overlay.py /tmp/blades16.png /tmp/grass16.png /tmp/tg_auto   --depth 3
```

→ a seamless 9-slice **+ strip_h/strip_v** with identical fill everywhere (so
crossroads/junctions match), a subtle dithered grass edge, inherently tileable
(16 % 4 == 0). Tall grass meshes into one body; the path connects cleanly.

**ORGANIC transition (foam shoreline, dense tree canopy, cliff face) → AI per-cell 9-slice.**
Here the drawn detail matters. Describe the **9 cells explicitly** as a 3×3
`tile-sheet`, slice with `edges9`, then **swap in the seamless fill** and
**seam-match the edges** (below):

```bash
GEN=.claude/skills/generate-sprite-sheet/scripts
$GEN/generate_block.py --type tile-sheet --cols 3 --rows 3 --area $A --palette "$PAL" \
  --output /tmp/shore.png --subject "a 9-piece WATER SHORELINE: wet sand OUTWARD, a \
soft foam line, calm water inward; (1) corner NW; (2) top edge; ... (9) corner SE"
$GEN/slice_tileset.py /tmp/shore.png --out .../water_blob --cols 3 --rows 3 --layout edges9 --terrain water
cp /tmp/water_fill.png .../water_blob/04_fill.png   # use the uniform CALM-water fill, not the painted cell
```

The cliff set is a *vertical* one (walkable lit top vs colliding face + corners).

**Seamless fills — applies to EVERY fill (kills "gridded / per-tile border / banding"):**
1. Generate the fill as a **single CONTINUOUS texture**: *"one uniform surface
   filling the whole frame, NO tiles, NO grid/cells, NO border/outline, NO
   vignette, NO bright corner."* Asking for *"a tile"* makes the model draw a
   bordered tile shape → the janky grid. (Google may return `IMAGE_RECITATION` on
   plain ground prompts — rephrase, or fall back to `--provider openai`.)
2. Derive the 16px tile by a **whole-image downscale** (`resize((16,16))`) —
   maximally uniform; this kills the left-right gradient that causes vertical
   banding. Keep faint grain (e.g. tall-grass blades) only via a 32px→center-crop-16.
3. `make_tileable.py <fill>` — **toroidal**: matches *opposite* edges so the seam
   vanishes when tiled. (The old 1px clamp left left≠right and a faint grid stayed.)

**Edges must seam-match along their run.** An edge tile repeats (edge_n/edge_s
left↔right, edge_w/edge_e top↔bottom); if its perpendicular ends don't agree it
shows cross-seams (the shoreline-of-blobs bug). Fix with
`make_tileable.py <edge> --axis h|v` (h = top/bottom edges, v = side edges). The
area builder applies this per-edge automatically.

**Always** tessellation-test a fill (tile it 5×5) *and* `render_map`+`validate_map`
the area before calling it done — verify, don't assume.

Then **author the map with a `terrain` layer** (a 0/1 presence grid tagged
`terrain` + `set`) instead of hand-placing corner gids, and expand it:

```bash
node tools/autotile/expand.mjs public/assets/maps/<map>.json   # stamps the right gids into base
node tools/autotile/blob.mjs --test                            # the classifier's self-test
```

The blob rule (`tools/autotile/blob.mjs`) picks fill / edge / outer-corner /
inner-corner per cell from its 8 neighbours; the expander resolves that role to a
tile by `(terrain, autotile)` and degrades gracefully if a set only has the
9-slice pieces.

**VARIANTS kill the "one tile stamped across the whole edge" repeat (the corduroy
tree-line, the single shoreline wave ×34).** A `(terrain, autotile)` role may have
SEVERAL tiles in the set — just tag 2–3 tiles with the same `terrain` + `autotile`.
`expand.mjs` scatters them deterministically per cell (`pickVariant`, a stable
hash of x/y/role), so edges and fills vary without flicker and stay reproducible.
One tile per role still works unchanged. Add variants to the *high-visibility*
roles first: water `edge_*` (shorelines), tree/cliff `edge_n` (wall tops), and
sand/path `fill`. Cheap deterministic variants: a horizontal/vertical **roll** of
a debordered edge (phase-shifts the foam/crest) or a small value **jitter** of a
fill — see `tools/maps/build_shared_overworld.py`.

**Role-aware DEBORDER is the real rim fix (supersedes `make_tileable --axis` for
autotile tiles).** The model bakes a 1px ink rim on *every* side; `make_tileable
--axis h|v` only *averages* two edges, leaving the rim as a consistent dark line —
the grid you still see. `deborder(im, role)` in `build_shared_overworld.py` strips
the rim on every side EXCEPT the designed transition side(s) (e.g. keep N for
`edge_n`, keep N+W for `corner_nw`, keep none for `fill`), then seams the tiling
axis. Deborder the BASE tile *before* deriving roll/jitter variants — rolling a
rimmed tile drags the border into the interior where no edge-pass can reach it.

### A2) Whole-object structures (buildings, lamps, big trees) — the visual hierarchy

Buildings, lamp-posts, signs, big trees are **NOT tiled** from wall/roof pieces
(that's what makes them read flat). Generate each as **ONE transparent multi-tile
object** with real shape, then slice only for placement (art-style §14b):

```bash
GI=.claude/skills/generate-image/scripts/generate.py
./venv/bin/python $GI --provider google --transparent --max-dim 0 --aspect 3:4 \
  --output /tmp/house.png --prompt "<pixel-art preamble> a single COSY COTTAGE as ONE \
building object on a TRANSPARENT background: peaked clay roof with OVERHANGING eaves + \
shadow line, shaded timber walls, door, glowing windows, a soft contact shadow at the base. \
Lit top-left. HARD 1px edges, NO anti-aliasing, NO soft glow/halo. Higher contrast than ground."
```

Then **declutter → snap to a tile multiple → slice → place** (body on `deco`
collides, the overhanging top row(s) on `above` so the player walks behind).

**Hard-won lessons (proven):**
- **No soft glows/halos/shadows on transparent objects.** Semi-transparent pixels
  pick up the magenta chroma key as a **pink/purple halo**. Keep all shading
  hard-edged; drop alpha < ~110 and kill magenta bleed in a declutter pass.
- **Multi-tile by default** — cottage ~5×6 tiles, lamp ~1×3. A one-tile lamp/house
  is the tell of a flat map.
- **Draw dominant** (higher contrast/saturation than the recessive ground) so the
  hierarchy reads.

### B) Scene mockup → harvest (cohesion + variety)

```bash
./venv/bin/python $GEN/generate_block.py --type scene-mockup \
  --subject "blue-hour coastal village green: grass, a soil path, a little sea with shoreline, flowers" \
  --cols 12 --rows 8 --area tinderwick --palette "$PAL" --output /tmp/scene.png
./venv/bin/python $GEN/slice_tileset.py /tmp/scene.png --out assets/tilesets/tinderwick_harvest \
  --cols 12 --rows 8 --harvest --quantize-area tinderwick
# -> distinct fill variants + decoration tiles, all sharing one palette/light.
```

### C) Animated tiles (water ripple, lamp, glowmoss)

```bash
./venv/bin/python $GEN/generate_block.py --type tile-anim \
  --subject "calm deep-blue sea water" --cols 3 --rows 1 \
  --area tinderwick --palette "$PAL" --output /tmp/water_anim.png
./venv/bin/python $GEN/slice_tileset.py /tmp/water_anim.png --out /tmp/water_frames \
  --cols 3 --rows 1 --layout anim3 --quantize-area tinderwick
```

Put the 3 frames in the set, then in the manifest give the base water tile
`"animation": { "frames": [<localIdxs>], "duration_ms": 700 }`. The engine
(`MapRenderer` + `WorldScene.tickAnimatedTiles`) cycles them live — keep it slow
and low-amplitude (docs/art-style.md §12).

### E) Combined tile-sheet (cheapest — one call, many materials)

For several DISTINCT materials at once, `--type tile-sheet` paints them as a
labelled-by-position grid in **one ~20¢ call** instead of one call per tile.
List the cells in reading order in `--subject`:

```bash
./venv/bin/python $GEN/generate_block.py --type tile-sheet --cols 4 --rows 4 \
  --area tinderwick --palette "$PAL" --output /tmp/sheet.png \
  --subject "(1) meadow grass; (2) dark grass; (3) soil path; (4) cobbled stone; \
(5) sand; (6) sea water; (7) wet shoreline; (8) clay roof; (9) timber wall; …"
./venv/bin/python $GEN/slice_tileset.py /tmp/sheet.png --out /tmp/sheet --cols 4 --rows 4
```

**Proven findings (cost vs quality), use these:**
- **Surfaces win big here.** Ground/water/floor/roof/wall fills come out cohesive
  and contrasty in one call — equal-or-better than per-tile, ~1/10th the cost.
- **Do NOT `--quantize` a combined sheet.** A single image is *already* one
  palette; quantising on top flattens the contrast you want. (Quantise only
  cross-checks tiles generated in *separate* calls.)
- **Always `make_tileable.py` the pure fills and tessellation-test 3×3** — the
  thumbnail can look great while the tiled fill buzzes or stripes. This pass is
  needed whatever the generation mode.
- **Decor/transparent objects don't belong on a combined sheet** — it's opaque,
  so a flower/lamp/tree comes out on a baked background. Generate those
  individually (`tile-decor`, native transparency), or background-remove.
- **Watch grid drift** on busy/structural cells (walls, doors); eyeball the slice
  and regenerate or re-slice if a cell is off the 16px grid.

So the rule of thumb: **one combined sheet for the area's surfaces; individual
transparent gens for decor; generate-together-then-slice for terrain families and
animation.**

### D) Map QA — render & audit (the standing gate)

```bash
./venv/bin/python $GEN/render_map.py public/assets/maps/<map>.json --output /tmp/<map>.png --scale 4
#   --layer deco    one layer in isolation     --no-above   without the over-player layer
#   --grid          overlay the 16px grid       --list-layers
```

Open the PNG and judge it against the Pokémon-era bar: clean terrain borders,
varied fills, decoration, depth, real contrast. If it doesn't read as
*designed*, iterate the tiles/layout and re-render. This is the map-level twin of
the sprite self-check loop (below).

**Then MEASURE it** — `validate_map.py` is the objective gate (the twin of
`validate_sprites.py`). It splits the two halves of the problem: `autotile-vocab`
(does the *tileset* provide edge/corner pieces?) and `meshing`/`water-shoreline`/
`decoration`/`tree-depth`/`border` (does the *map* use them well?):

```bash
./venv/bin/python $GEN/validate_map.py public/assets/maps/<map>.json   # FAILs if below standard
```

A map is "done" only when it renders to the bar AND `validate_map.py` passes with
no FAILs. (Running it on a map built from a kit with no terrain tags correctly
FAILs `autotile-vocab` — fix the tileset first.)

## Generating a cohesive area tile set (the turnkey recipe)

A map area (a town, a route, a cave) needs a *set* of tiles that read as one place. Same
two-system split: the model makes each tile, `pack_tileset.py` assembles them into the
exact atlas + sidecar the engine reads. Briefs and the world palette come from the world
docs (`docs/world/atlas.md`, `docs/world/README.md`, and the master
`assets/tilesets/world-palette.json`).

This recipe is **proven** — it built the first three sets (Tinderwick town, Dimglass Coast,
the cottage interior). Follow it and any future area is turnkey.

> **Gold standard (start here, don't re-derive it).** The fastest correct path is to
> **copy `tools/maps/build_tinderwick.py`** — the reference area builder — and adapt its
> layout. It already encodes everything below at the quality bar: every surface an autotile
> **body** (§A); **continuous-texture → whole-downscale → `make_tileable`** fills (no
> banding/grid); **`composite_overlay.py`** for FLAT transitions (path, tall-grass) and AI
> per-cell only for ORGANIC ones (shoreline foam, tree canopy, cliffs); per-edge
> `--axis` seam-matching; a 2-deep **tree-wall border** that runs off the map edges; a
> 3-row beach (edge/fill/edge) + a big sea; whole-object buildings/lamps/trees on the
> object layer. Then `expand.mjs` → strip terrain layers → `render_map` + `validate_map`
> (PASS) → tessellation-test any fill you doubt. A new area is: new layout + new
> area-specific *organic* sets (its shoreline/cliffs/canopy), reusing the compositor and
> seam tooling unchanged.

### The big cohesion win: ONE packed SHARED overworld set every map references

**This is now the standing convention (don't bake a bespoke atlas per area).** There is one
packed shared set — `vesper_overworld_set` — and every overworld map lists it in
`tilesets[]` by name + `first_gid` and just paints terrain layers. The engine resolves gids
across any number of tilesets by `first_gid` range (`MapLoader.ts`), and `tools/autotile`
keys terrain by `set` name, so a map can mix the shared set + a small area accent set at a
higher `first_gid` with zero engine changes. An area adds only its **objects** (buildings)
and, if it truly needs them, a few accent tiles — never a copy of the whole kit.

Build/refresh the shared set with the builder (REUSE-first; no per-tile API calls needed):

```bash
python3 tools/maps/build_shared_overworld.py   # -> public/assets/tilesets/vesper_overworld_set.{webp,tileset.json}
```

It promotes the proven Tinderwick autotile families (grass/path/sand/tree/tall-grass/water
9-slice + water anim + flowers/sign/fence), adds **de-repetition variants** + **scatter
decor**, reuses the Dimglass cliff/buoy/dock masters, applies the role-aware **deborder**,
and writes `assets/tilesets/_shared/vesper_overworld.index.json` (name → local index). Map
builders consume that via **`tools/maps/mapkit.py`** — `mk.shared_tileset_ref()`,
`mk.gid("flowers")`, grid/scatter helpers, and `mk.finalize()` (the standing pipeline:
expand → strip terrain → render → validate). See `build_tinderwick.py` / `build_dimglass.py`
as the two worked examples; copy one for a new area. The reusable seam tooling lives in
**`tools/maps/tileforge.py`** (`deborder(im, role)`, `jitter`, `roll`, `flip_h`,
`whole_downscale`) — import it in any builder; it's side-effect-free. (`build_shared_overworld.py`
runs its build on execution, so run it as a script, not as an import — get the helpers from
`tileforge`.)

> **When you DO need new tiles** (a new biome's organics — a cave, a snowfield, a different
> cliff), generate them with the prompting standard below, deborder/variant them, and append
> them to the shared set's builder (or a small accent set). The first three areas are
> REUSE; new biomes are targeted generation on top of the shared base.

**Build a NEW area — turnkey:**

```bash
# 0. (once) ensure the shared set exists / is current
python3 tools/maps/build_shared_overworld.py
# 1. copy a worked builder and edit the layout (size by MapKind, §7 sketch)
cp tools/maps/build_dimglass.py tools/maps/build_<area>.py    # or build_tinderwick.py
#    - paint terrain presence grids (mk.make_grid/rect/vline/organic_border)
#    - mk.shared_tileset_ref() in tilesets[]; mk.gid("flowers") etc. for deco/objects
#    - mk.scatter_decor(...) to break the field; objects[] for buildings/trees
# 2. build → expand (variant autotiling) → strip terrain → render → validate, one call:
python3 tools/maps/build_<area>.py     # mk.finalize() prints the QA report; aim for PASS
# 3. register the map in src/game/data/world/maps.ts + edges in world/graph.ts (content, not engine)
```

If the area needs a NEW organic tile (cliff/cave/biome edge), generate it (prompting standard
below), `tileforge.whole_downscale`/`deborder`/variant it, and append it in
`build_shared_overworld.py` (shared) or a small per-area accent set at a higher `first_gid`.

### Generating new tiles: the prompting standard (measured, not folklore)

The model paints "a tile" as a framed little picture — top-left light, a **vignette**, a 1px
border — *ignoring* "no border / tessellate". Measured: a single-tile raw has rim≈73 (outer
ring vs interior), and that rim *is* the grid when tiled. The fix is prompt + sampling:

- **Fills:** ask for a **large continuous swatch**, *"completely FLAT EVEN lighting, NO
  vignette, NO darkening at the edges, full-bleed, uniform density,"* then **downscale the
  WHOLE image** to 16px (or slice an interior cell of a block). Measured rim drops 73 → ~2
  (33×). The tile prompt templates now carry this wording.
- **Edges:** paint the transition as a long **strip** and slice a clean interior
  cross-section; keep lighting flat along the repeat axis. Then `deborder(im, role)`.
- **Model choice (measured A/B, corrected flat-lit prompt):** both models drop the rim hugely
  vs the old single-tile prompt (73 → single digits), so the *prompt* is the main lever. Split:
  - **Uniform FILLS (grass/sand/stone/water): gpt-image-2 is cleaner** — it draws a literal even
    texture (sand rim **0.6**), while Nano embellishes a fill with scene detail (rocks/puddles,
    rim **8.9**) that fights tiling. Use OpenAI for pure fills *when it's behaving*.
  - **EDGES / DECOR / OBJECTS / anything transparent: Nano** — cleaner edge (rim 0.7 vs gpt 18)
    and native transparency; gpt's edge picked up a vignette.
  - **Reliability caveat (today):** our sprite tooling routes OpenAI through opaque + magenta-
    chroma + the *creature* preamble + retries, so gpt tiles are **slow and frequently fail** in
    this env (the cliff fill fell back to Nano). Until the OpenAI tile path uses native
    `background:transparent` + a tile-specific preamble + no retries, **default `--provider
    google` for tiles**, and only reach for OpenAI on a stubborn uniform fill. Generate fills as
    a large flat field and `whole_downscale` regardless of model.

The legacy per-area `_shared/` recipe below still documents the from-scratch generate flow;
it remains valid for a brand-new biome, but the *default* is now "reference the packed
shared set."

### Step 1 — generate tiles, anchor-first, into `_shared/`

Generate the **ground (grass) tile first** as the cohesion anchor, then pass it as
`--reference` to **every** sibling so palette, value range, pixel density and top-left light
carry across the whole set. The `--reference` mechanism is confirmed working: Nano Banana
Pro honours it via Gemini's multimodal input, and it visibly keeps the palette tight.
Derive `--palette` from `assets/tilesets/world-palette.json` (area brief + brand anchors)
and pass the SAME string to every tile.

```bash
PAL="blue-hour coastal Vesperholm village at dusk: cool grass green and darker grass-green, bone-cream stone, soil brown paths, deepBlue (#13205a) sea, sandy tan, warm fire-orange (#ff8a3d) lamp accents, deep ink (#1a1430) outlines, diamond-cyan (#9fe7ff) highlights"
GEN=.claude/skills/generate-sprite-sheet/scripts/generate_sprite.py

# 1. anchor tile FIRST
./venv/bin/python $GEN --type tile-ground --area _shared --palette "$PAL" \
  --subject "short cool-green coastal meadow grass at blue hour" \
  --output assets/tilesets/_shared/grass.png

# 2. every other tile seeded with grass.png as --reference (fire these in parallel)
REF=assets/tilesets/_shared/grass.png
./venv/bin/python $GEN --type tile-path  --area _shared --palette "$PAL" --reference $REF \
  --subject "packed pale soil-brown footpath, fine gravel" --output assets/tilesets/_shared/path.png
./venv/bin/python $GEN --type tile-water --area _shared --palette "$PAL" --reference $REF \
  --subject "calm deepBlue sea, gentle cyan ripple glints" --output assets/tilesets/_shared/water.png
./venv/bin/python $GEN --type tile-water-edge --area _shared --palette "$PAL" --reference $REF \
  --subject "wet sandy shoreline, water at the bottom, sand at the top" --output assets/tilesets/_shared/water_edge.png
# …grass_dark, soil, sand, cliff, cliff-edge, wall, roof, door, fence (tile-*), and
#   flowers/lamp/sign/tree_top via --type tile-decor (transparent around the object).
# For an ANIMATED water tile, also generate water_2 / water_3 seeded with water.png.
```

Tile subtypes available (run `generate_sprite.py --list-types`): `tile-ground`, `tile-soil`,
`tile-sand`, `tile-floor` (plaza/board/wood floor), `tile-path`, `tile-water`,
`tile-water-edge`, `tile-cliff`, `tile-cliff-edge`, `tile-wall`, `tile-roof`, `tile-door`,
`tile-fence`, `tile-decor` (transparent standalone object), and the generic `tile`.

Run the self-check loop on each tile, and **eyeball a 3×3 montage** of each laid
edge-to-edge to confirm it tessellates without a visible seam or repeat hotspot (ground,
water, path, sand are the ones that buzz if wrong). The prior areas' ground tiles make good
extra `--reference`s so neighbouring regions stay one world.

### Step 2 — assemble each area's tile dir + manifest

For each map, copy the shared masters into `assets/tilesets/<area>/` **in the order the
map's gids expect** (numeric prefixes like `00_grass.png` keep the order obvious), add any
accent tiles, and write a `tileset.manifest.json`. Tile ORDER fixes the LOCAL 0-based index
(row-major); a map's gids map to indices via `gid - first_gid`.

```jsonc
// assets/tilesets/tinderwick/tileset.manifest.json
{ "name": "tinderwick_set", "columns": 8, "tiles": [
  { "file": "00_grass.png", "role": "ground", "encounter_terrain": "tall_grass" },
  { "file": "01_water.png", "role": "water", "collides": true,
    "requires_ability": "tidecall", "encounter_terrain": "water",
    "animation": { "frames": [1, 17, 18], "duration_ms": 700 } }, // frames = LOCAL indices
  { "file": "02_path.png", "role": "path" },
  // …index 3,4,… in gid order; extra vocab tiles can follow after the gid-pinned ones.
  { "file": "17_water_2.png", "role": "water" },
  { "file": "18_water_3.png", "role": "water" }
] }
```

Manifest per-tile keys (all optional, validated against the engine enums): `role` (info),
`collides`, `encounter_terrain` (`tall_grass|water|cave|sand`), `requires_ability`
(`glimmerstep|tidecall|emberward|updraft_kite|sunsketch|starreach`), and `animation`
(`{ frames:[localIdx…], duration_ms }`). A typo in a terrain/ability value fails the pack
loudly rather than producing a tile the engine silently ignores.

### Step 3 — pack into the atlas + sidecar

```bash
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_tileset.py \
  --tiles-dir assets/tilesets/tinderwick
# -> public/assets/tilesets/tinderwick_set.webp  +  tinderwick_set.tileset.json
```

`pack_tileset.py` composes the atlas in manifest index order and emits a **lossless WebP**
(`public/assets/tilesets/<name>.webp`) plus the `<name>.tileset.json` sidecar. It
**verifies** the WebP is visually lossless (alpha identical everywhere, RGB identical
everywhere alpha>0) and aborts if not — lossy WebP would smear the crisp 1px pixel edges.

The sidecar matches `PackedTileset` in `src/game/systems/world/tileset.ts` EXACTLY:

```jsonc
{ "name": "tinderwick_set",
  "image": "assets/tilesets/tinderwick_set.webp",   // served path (vite drops public/)
  "tile_width": 16, "tile_height": 16, "columns": 8, "tile_count": 19,
  "tiles": [ /* SPARSE TileMeta[]: only tiles with behaviour or an explicit role.
                each: { index, role?, collides?, encounter_terrain?,
                        requires_ability?, animation?{frames,duration_ms} } */ ] }
```

The engine reads tile *behaviour* (collision, encounter terrain, ability gating, animation)
only from this sidecar — never from the map JSON, which carries gids alone. Adding behaviour
to a tile is a manifest edit + re-pack, done.

### Step 4 — wire the map

Point the map JSON's `tilesets[].image` and `src/game/data/world/maps.ts`'s
`MAP_REGISTRY` tileset path at the `.webp`. Keep the map's `tile_count`/`columns` in sync
with the packed atlas. (The map references the atlas via a `TilesetRef` + its `first_gid`.)

Generated source tiles live at repo-root `assets/tilesets/<area>/` and `_shared/` (not
served); the packed atlas + sidecar land in `public/assets/tilesets/` (served by Vite).

## Packing creature sprites (`pack_creatures.py`)

The creature analogue of `pack_tileset.py`. The model makes each kin's five source PNGs
into `assets/creatures/NNN_slug/` (`battle_front.png`, `battle_back.png`, `icon.png`,
`overworld.png`, `portrait.png` + `metadata.json`); this script packs **every** creature
folder into served, lossless-WebP sprites plus one manifest the engine loads:

```bash
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_creatures.py
```

No args needed — it walks `assets/creatures/*`, writes per-view
`public/assets/sprites/creatures/NNN_slug/<view>.webp` (one lossless WebP per view, not an
atlas — battle loads one kin at a time), and emits
`public/assets/sprites/creatures/creatures.manifest.json` keyed by numeric kin `id` →
`{ slug, front, back, icon, overworld, portrait }` with each view's served path + width/
height. It asserts every master matches the art-bible canvas (64×64 battle, 32×32
icon/overworld, 96×96 portrait), verifies each WebP round-trips visually lossless (alpha +
visible RGB), and prints a JSON summary (counts, ids, warnings). Re-run it after generating
or fixing any kin's art — packing the rest of the dex is this one command.

The game reads the manifest through `src/game/systems/sprites/CreatureSprites.ts`
(`hasCreatureSprite` / `creatureTextureKey` / lazy `loadCreatureSprite`), which resolves
null for any kin/view not yet packed so callers can fall back to a placeholder.

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
  packing step that exists today — `pack_tileset.py`, see **Generating a cohesive area tile set**.)

## What it deliberately does *not* do

- **Does not auto-commit.** Show the user the result; let them decide what to
  keep.
- **Does not invent creature names, types, or lore** — that's data-driven
  content for `src/game/data/`. The skill fills sprite geometry into
  `metadata.json`; you fill `name`/`types`.
- **Does not produce one giant multi-creature master sheet.** By design. See the
  two-system principle above.
