# PixelKin — Art & Sprite Bible

The single source of truth for how PixelKin *looks*. If `VISION.md` defines the
**feeling** we sell, this document defines the **pixels** that sell it. Every
sprite, tile, icon, and portrait — hand-made or generated — follows the rules
here so 151 creatures and a whole overworld read as one coherent, authentic
handheld-era game instead of a bag of mismatched assets.

> **Read `VISION.md` first.** The originality/copyright rules there are
> non-negotiable and they bind every asset. This document never overrides them;
> it operationalises the *look* described in VISION's "The look" section.

---

## 1. The era we're emulating

A loving continuation of **1999–2001 handheld pixel art**, not a parody of it.

- **Anchor register: Game Boy Color.** Tight palette, 16×16 tiles, bold
  readable sprites with personality over detail.
- **Allowed to grow toward Game Boy Advance.** As the game builds out we lean
  into the slightly richer GBA register — more colours per sprite, smoother
  animation, gentle light effects — "the same world, a bit more advanced."
  Start GBC-restrained; grow GBA-richer only where it earns delight.
- **Fixed internal resolution: 240×160** (`GAME_WIDTH`/`GAME_HEIGHT` in
  `src/game/config.ts`), nearest-neighbour upscaled by Phaser's `Scale.FIT`.
  Every pixel stays a crisp, deliberate square at any screen size.

### Copyright, restated for artists

Inspired by the monster-collecting genre; a copy of **nothing**. No existing
creature, silhouette, name, pose, palette signature, town, character, font, or
UI motif from any commercial game. In every brief, describe by **genre and
mood**, never by another brand. When in doubt, make it *more* original. (Full
rules: VISION.md → "Originality & copyright".)

---

## 2. The two-system principle

Keep these mentally separate — conflating them is how asset libraries rot:

1. **Art spec** (this document, §4–§7) — strict per-type rules: canvas size,
   palette, lighting, pose, anchor. The *source of truth*.
2. **Packing/loading spec** (§9) — how source images get assembled into atlases
   and loaded by Phaser.

**Do not treat a giant hand-built master sheet as the source of truth.** The
source of truth is a set of small, rule-bound source images plus metadata. Code
assembles atlases from them. Models make art; code does layout. AI image models
are good at *art* and bad at *deterministic grids* — so we never ask them to be
an atlas compiler.

---

## 3. Universal art rules

These apply to **every** asset type. They are where consistency actually comes
from.

- **Pixel art only.** Hard 1-pixel edges. **No anti-aliasing**, no blur, no soft
  gradients (a small, deliberate *dithered* pixel gradient is allowed; a smooth
  one is not).
- **Limited palette.** Roughly **8–16 colours per sprite** (excluding
  transparency), GBC-restrained. Lean on the brand anchors below; introduce new
  hues only with intent.
- **Dark outline** around the outer silhouette; lighter internal linework for
  interior forms. Avoid pure black (`#000000`) outlines — use the deep ink
  `#1a1430` so it sits in the palette.
- **Light source: top-left**, consistently, on every asset. Highlights up-left,
  shadow down-right.
- **Strong readable silhouette.** If the shape isn't recognisable as a flat
  black blob, it isn't finished.
- **Cute, stylised proportions** — slightly oversized heads/eyes for
  readability at small sizes. Not realistic, not gritty.
- **Consistent saturation and perspective** across a type. Creatures share one
  ¾-front "battle" viewpoint; the overworld shares one top-down-ish viewpoint.
- **No semi-transparent shading.** Shade with palette colours, not opacity.

### Brand palette anchors

Pulled from the PixelKin logo (`src/game/config.ts → COLORS`). Treat these as
the gravitational centre of every palette; type accents (grass/fire/water) cue a
creature's element.

| Token      | Hex        | Role                                   |
|------------|------------|----------------------------------------|
| `night`    | `#0b1026`  | Deepest backdrop / darkest shadow      |
| `deepBlue` | `#13205a`  | UI panels, night-blue fields           |
| `diamond`  | `#9fe7ff`  | Bright cyan highlight / sparkle accent  |
| `grass`    | `#7bdc6b`  | Leaf-type / foliage accent             |
| `fire`     | `#ff8a3d`  | Fire-type / warm accent                |
| `water`    | `#4fb4ff`  | Water-type / cool accent               |
| `ink`      | `#1a1430`  | Outlines, darkest linework             |
| `bone`     | `#f5f0e1`  | Light text, paper, bright highlights   |

---

## 4. Canvas standards (the v1 sprite spec)

**Every asset type lives on its own fixed canvas.** No creature is 57×61, none
is 71×70. One standard per type, no exceptions — that discipline is the whole
point.

| Asset type          | Frame size | Sheet (cols×rows) | Anchor         | Subject fills |
|---------------------|-----------:|:-----------------:|----------------|--------------:|
| World tile          |      16×16 | 1×1               | top-left       | 100%          |
| Human overworld     |      32×32 | 3×4               | bottom-centre  | ~20–24px wide |
| Creature overworld  |      32×32 | 1×1 (opt. 3×4/4×1)| bottom-centre  | ~75%          |
| Creature battle front |    64×64 | 1×1               | bottom-centre  | ~80% height   |
| Creature battle back  |    64×64 | 1×1               | bottom-centre  | ~80% height   |
| Creature icon       |      32×32 | 1×1               | centre         | ~85%          |
| Creature portrait   |      96×96 | 1×1               | centre         | ~85%          |
| Battle effect       |      32×32 | grid (e.g. 4×4)   | centre         | per-frame     |

Total sheet pixel size = frame × cols/rows (e.g. human overworld = 96×128;
4×4 effect at 32px = 128×128).

### Anchors / pivots

Every type has a defined pivot so a short creature and a tall creature still
**stand on the same battle plane** and walk on the same baseline.

- **Bottom-centre:** human overworld, creature overworld, creature battle
  front, creature battle back. (Game logic positions by the feet.)
- **Centre:** icons, portraits, effects.
- **Top-left:** tiles (they pack into a grid).

---

## 5. Per-type specs

### A) Human / NPC overworld walking sheets

Walking around towns and routes.

- Sheet **3 columns × 4 rows**, 32×32 frames (96×128 total).
- **Rows = directions:** row 1 down, row 2 left, row 3 right, row 4 up.
- **Columns = animation:** col 1 idle, col 2 step-1, col 3 step-2.
- **Feet sit on the same baseline in every frame.** Body centred horizontally.
  Character ~20–24px wide inside the 32px frame, 2–4px padding all round.
- Head height and proportions identical across frames — only limbs/feet move.
- Pivot: **bottom-centre**.

### B) Creature overworld mini-sprites

PixelKin roaming the overworld. Keep them **very simple** — retro charm beats
detail at 32px.

- 32×32 frame. Default a single idle frame; optional 4-frame idle/step sheet
  (`idle1, step1, idle2, step2` as 4×1) or a 3×4 directional sheet if it roams.
- Same creature identity as its battle sprite, simplified.
- Pivot: **bottom-centre**.

### C) Creature battle sprites — the important ones

**Front (64×64):** ¾-front battle-ready pose, centred horizontally, lowest
visible pixel near y≈56–58, a few px top padding. Creature fills ~80% of the
frame. Pivot **bottom-centre**.

**Back (64×64):** the same creature seen from behind (player's-side view). Same
baseline logic. Must read as the *same species*, not a different one — same
palette, proportions, and signature features.

**Optional battle animation frames:** `idle, attack, hurt, faint`. Store as
separate images or a small sheet; each frame obeys the 64×64 front spec.

### D) Creature icon (32×32)

Menu/party/box icon. **Simplified, readable head/silhouette focus** — drop any
detail that vanishes at 32px. Centre-anchored. Reads instantly as "which kin."

### E) Creature portrait (96×96)

Profile/dex art. Richer than the battle sprite (more palette latitude toward the
GBA register) but the **same character, palette, and personality**. Centre.

### F) Battle effects (32×32 frame grid)

Sparks, slashes, bursts, splashes, level-up sparkles. **Kept entirely separate
from creatures** so they're reusable across all of them. Lay out as a grid
(e.g. 4×4 or 8×4) of equal frames; centre-anchored. One effect = one sheet
(`fire_hit`, `water_splash`, `leaf_burst`, `hit_sparkle`, `levelup_sparkle`…).

### G) World tiles (16×16)

The classic handheld RPG tile. Top-left anchored so they pack edge-to-edge into
a tileset with no seams. Design tiles to tessellate; keep interior detail low so
they don't visually buzz when tiled across a field.

### H) Battle backdrops (240×160, full canvas)

The scene *behind* a battle — what fills the screen instead of flat black. One
per area, with **a few variants** so repeat fights in the same place don't all
look identical. Unlike everything above these are **opaque, full-canvas, and not
sprites**: a single 240×160 image (the whole internal resolution), shipped as
**lossless-ish WebP** under `public/assets/backgrounds/battle/`, no alpha, no
chroma-key.

The hard rule is **subtlety** — the backdrop sits *under* the creatures and the
UI plates, so it must never compete with them:

- **Dark and low-contrast.** Anchor on `night`/`deepBlue`; keep the brightest
  notes small (a lantern, a star, a line of foam). If a battler sprite or an HP
  plate gets hard to read against it, it's too busy.
- **Keep the lower-middle empty.** The player battler stands bottom-left, the foe
  top-right; leave those zones as a calm, near-flat ground plane and push scenery
  to the upper half and the edges. A gentle vignette down to deep night-blue at
  the bottom helps the sprites pop.
- **In-world mood, not a photo.** Cosy *Long Dusk* — lanterns in the dark,
  constellations overhead (the thing you're out here to relight). Same palette and
  chunky-pixel feel as the matching area's tiles.
- **No characters, creatures, text, UI, or frames** baked in.

These are generated with the **generate-image** skill (no brand preset; the
pixel-art direction lives in the prompt), then **downscaled to exactly 240×160**
and saved as WebP. Naming: `area-slug-a.webp`, `-b.webp`, … (e.g.
`tinderwick-a.webp`, `dimglass-coast-b.webp`). Register the variant list on the
map in `src/game/data/world/maps.ts` (`battle_backdrops`); the BattleScene picks
one at random and falls back to the plain night fill if a map has none.

---

## 6. Transparency & the chroma-key pipeline

**Shipped assets are PNG with a real alpha channel.** That is the correct,
engine-friendly answer — Phaser handles alpha natively.

Image models, however, can't reliably emit alpha. So generation uses a flat
**chroma-key** background that post-processing strips:

- Key colour: **pure magenta `#FF00FF`** — it practically never appears in a
  natural sprite palette, so keying it out never eats real art. (Pure green is
  the fallback; magenta is preferred.)
- **Never allow the key colour inside a sprite's palette.**
- Background must be perfectly flat — no checkerboard, no gradient, no plate.
- Pipeline: **generate on magenta → strip magenta → export transparent PNG**.

The `generate-sprite-sheet` skill handles this automatically. Its default model,
**Google Nano Banana Pro**, renders on a magenta field that gets keyed out to a
transparent PNG before snapping to the exact canvas. The optional **OpenAI
`gpt-image-2`** path (`--provider openai`) does the same magenta chroma-key, but
in-skill — gpt-image-2 has no native transparent mode.

---

## 7. Metadata spec

Never rely on the image alone. Each creature carries a `metadata.json` so minor
alignment fixes are a data edit, not a repaint:

```json
{
  "id": 1,
  "name": "Sproutle",
  "slug": "sproutle",
  "types": ["Leaf"],
  "sprites": {
    "battle_front": { "file": "battle_front.png", "width": 64, "height": 64, "anchor": "bottom-center" },
    "battle_back":  { "file": "battle_back.png",  "width": 64, "height": 64, "anchor": "bottom-center" },
    "icon":         { "file": "icon.png",         "width": 32, "height": 32, "anchor": "center" },
    "overworld":    { "file": "overworld.png",    "width": 32, "height": 32, "anchor": "bottom-center" },
    "portrait":     { "file": "portrait.png",     "width": 96, "height": 96, "anchor": "center" }
  },
  "scale": 1.0,
  "offsets": { "battleX": 0, "battleY": 0, "iconX": 0, "iconY": 0 }
}
```

`scale` and `offsets` let you nudge a too-tall or off-centre creature in code
without touching the art. This keeps content **data-driven** (CLAUDE.md), the
same posture as `src/game/data/`.

---

## 8. Folder structure

**Source of truth** lives under the master `assets/` tree (not served — it's the
brand/source kit). One folder per creature, one image per asset type:

```
assets/
  creatures/
    001_sproutle/
      battle_front.png  battle_back.png  icon.png  overworld.png  portrait.png
      metadata.json
    002_pyrel/ …
  trainers/
    player.png  professor.png  rival_01.png        # 3×4 walk sheets
  effects/
    fire_hit.png  water_splash.png  leaf_burst.png # frame grids
  tiles/
    grass.png  path.png  water_edge.png            # 16×16 tiles
```

A future **build step** assembles these into runtime atlases under the served
`public/assets/` tree (see CLAUDE.md layout):

```
public/assets/sprites/   creature_front_atlas.png  creature_icon_atlas.png …
public/assets/tilesets/  overworld_tileset.png
```

Until that build step exists you can also point the skill straight at
`public/assets/sprites/` for quick in-game use — but treat `assets/` as the
canonical source.

---

## 9. Packing / loading (the second system)

- **Source stage: one image per asset.** Do **not** ask a model to generate one
  giant master sheet of many creatures — it drifts on spacing, scale, and
  repetition, and you'll hand-fix dozens of cells. Generate one creature pack at
  a time.
- **Build stage: code assembles atlases** from the standardised source images,
  emitting a texture atlas + JSON frame map Phaser can load with
  `this.load.atlas(...)`.
- Phaser renders with `pixelArt: true` already on — nearest-neighbour, no
  smoothing. Keep source art at its true small size; let the engine upscale.

---

## 10. Generation workflow (how to actually make these)

Use the **`generate-sprite-sheet` skill** (`.claude/skills/generate-sprite-sheet/`).
It encodes every rule above as prompt templates plus deterministic
post-processing, so output lands on the exact canvas every time.

The robust workflow, per asset:

1. **Generate** a source sprite from the type's locked template + your original
   subject brief.
2. **Snap** to the exact standard canvas + anchor (the skill does this).
3. **Validate — automated.** The skill runs `validate_sprites.py` on every
   output (size, alpha, anchor, fill, sheet baselines) and reports a
   `validation` block; run `validate_sprites.py --all` as a repo-wide spec gate.
4. **Inspect — by eye.** Open the file; check silhouette, palette, no artifacts,
   no franchise resemblance. The validator measures geometry; only you can judge
   art and originality.
5. **Iterate** if needed (max 3 attempts per asset — naming the specific
   problem each time).
6. Later, **pack** into atlases with the build step.

Do **not** try to get the model to emit the final 151-creature sheet directly.
Generate sources, standardise with code, pack with code. That division of labour
is what makes a consistent dex achievable.
