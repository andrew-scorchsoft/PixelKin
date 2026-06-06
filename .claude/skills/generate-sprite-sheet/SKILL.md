---
name: generate-sprite-sheet
description: Generate consistent, standard-compliant PixelKin sprites and sprite sheets (creature battle/icon/overworld/portrait art, NPC walk sheets, battle effects, world tiles) from original briefs. Drives the image-generation API (OpenAI gpt-image-2 / Google Nano Banana Pro) through the generate-image skill, then deterministically snaps every result to the exact canvas size, anchor, and transparent-PNG format defined in docs/art-style.md. Use whenever the user wants a creature sprite, character sprite, walk sheet, battle effect, tile, icon, or portrait for the game.
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

Do **not** use it for: UI chrome you can build in CSS/HTML, the logo (already in
`assets/`), or music/SFX (use `generate-music`).

## Prerequisites

- Run via the **project venv**: `./venv/bin/python …` from the repo root. The
  script needs Pillow (and numpy for clean edges) — both in `requirements.txt`.
  If the venv doesn't exist: `python3 -m venv venv && ./venv/bin/pip install -r requirements.txt`.
- An image-provider key in the environment — `GOOGLE_AI_STUDIO_API_KEY`
  (preferred, Nano Banana Pro) or `OPENAI_API_KEY` (gpt-image-2). The skill
  delegates the actual API call to the sibling `generate-image` skill, which
  handles provider choice and the transparent-background pipeline.

## How it works

For each asset the script:

1. Builds a prompt = shared **style preamble** + **originality clause** +
   the locked **per-type template** (`sprite-specs.json`) + your **subject**.
2. Calls `generate-image --transparent` to get a high-res transparent source
   (OpenAI native alpha, or Google magenta chroma-key — handled for you).
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

### Arguments worth knowing

- `--type` *(required)* — sprite type (see table / `--list-types`).
- `--subject` *(required unless `--from-image`)* — your **original** brief for
  the creature/character/effect. Describe by genre and mood; never reference a
  real franchise (VISION.md). The style/canvas/pose come from the template — you
  supply *what it is*.
- `--output` — explicit `.png` destination. **Or** use the creature convention:
- `--creature-id N` + `--creature-slug name` — auto-files under
  `assets/creatures/NNN_slug/<role>.png` and writes/updates `metadata.json`.
- `--provider google|openai` — force the provider (default: auto).
- `--resample lanczos|box|nearest` — downscale filter. **`lanczos` (default)**
  reads cleanest at tiny sizes; `nearest` gives the hardest edges. (Rendering
  stays crisp regardless — Phaser nearest-upscales the small source.)
- `--fill F` — override the subject's fill fraction (0–1) for this run.
- `--no-align` — for sheets, skip per-frame baseline alignment and just
  downscale the whole sheet (use if the model's own layout was already good and
  the per-cell trim is clipping something).
- `--from-image PATH` — skip the API call and just run the snap pipeline on an
  existing transparent PNG. Useful for cleaning up hand-made art or a sprite you
  already generated.
- `--keep-temp` — also save the raw high-res generation next to the output.
- `--list-types` — print all types and exit.

## The self-check loop — mandatory

The script standardises geometry; it does **not** judge the art. You do. Each
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
- This skill **does not** build atlases. That's the separate packing step (art
  bible §9), intentionally left to code, not the model.

## What it deliberately does *not* do

- **Does not auto-commit.** Show the user the result; let them decide what to
  keep.
- **Does not invent creature names, types, or lore** — that's data-driven
  content for `src/game/data/`. The skill fills sprite geometry into
  `metadata.json`; you fill `name`/`types`.
- **Does not produce one giant multi-creature master sheet.** By design. See the
  two-system principle above.
