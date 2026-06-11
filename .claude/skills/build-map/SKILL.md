---
name: build-map
description: >
  Compose and build a PixelKin overworld/dungeon map — towns, routes, caves,
  interiors — from the area's atlas card + walkthrough spec, using the shared
  tileset, the mapkit/patterns toolkit, and the standing validation pipeline.
  Use whenever the user asks to build, extend, retune, or fix a map/area/route/
  dungeon/floor. For generating NEW art (tiles, objects, backdrops) it defers
  to the generate-sprite-sheet skill.
---

# build-map

Builds a map as **decisions, not coordinate bookkeeping**: read the area's
spec, choose its features, stamp them with the pattern library, and let
`finalize()` prove it. The binding rulebooks are `docs/world/level-design.md`
(composition §11, the dungeon scale ladder §2a, and **§3a — the structural
principles of the greats**: loops not corridors, asymmetry by direction,
see-it-before-you-walk-it, braided risk-reward, one new idea per screen,
pressure-then-relief, lost-locally-never-globally, gates rhyme with rewards,
trainers are geometry, the map remembers) and the area's file in
`docs/world/walkthrough/` (the **Validation hooks** are the acceptance spec).
Before calling a map done, walk it mentally against §3a — a map that
validates but plays as a corridor is not done.

## The flow (every map)

1. **Read the spec first** — the atlas card (`docs/world/atlas.md`), the
   walkthrough region file's section for this map (main path beats, story
   beats, validation hooks), and `graph.ts` for the declared warp ids/edges.
   Name the area's **three signature touches** (level-design §8) before
   writing a line.
2. **Copy the nearest worked example** from `tools/maps/`:
   - town → `build_tinderwick.py` · route → `build_dimglass.py` /
     `build_saltreach_fen_i.py` (the pattern-library showcase)
   - cave floor → `build_glowmoss_deep.py` (+ `_b1f.py` for a lower floor)
   - interior → `build_interiors.py` · hub → `build_crossroads.py`
3. **Paint terrain as presence grids** (`mapkit`: `blob`/`rect`/`hline`/
   `organic_border`), **stamp features** (`patterns`, below), assemble the
   dict, and end with `mk.finalize(m)` — write → autotile expand → strip →
   render → `validate_map` → `audit_warps`. **All must PASS.**
4. **Pay the content debts.** Stamps return the registry refs they create
   (`pt.report(owed)` prints them): scripts in `content/scripts.ts`, dialogue
   in `content/dialogue.ts`, trainers in `content/trainers.ts` (payout = class
   rate × ace, 10-economy §4 — and mirror into `BUILT_PAYOUTS` in
   `tools/balance/progression.mjs`). Register the map in `data/world/maps.ts`
   (+ edges in `graph.ts` if new). Run `npx tsc --noEmit` and
   `node tools/balance/progression.mjs` — both must pass.
5. **Eyeball the render** (`/tmp/<map_id>.png`) against the §11 bar: no flat
   voids, organic borders, an elevation accent, trainer beats on lanes,
   hard-edged encounter beds, buildings on aprons. A map that validates but
   reads flat is not done.

## The pattern library (`tools/maps/patterns.py`)

| Stamp | What it encodes |
|-------|-----------------|
| `Area(x0,y0,x1,y1)` | a named region handle — apply patterns to it (`.inset()`, `.cells()`) |
| `zones_from_grid(grid, …)` | encounter zones **from the paint**: each painted blob → a loose bounding-box zone. Safe because the engine fires tall_grass/water only ON matching tiles (cave/sand roll rect-wide) |
| `trainer_beat(m, tid=…, at, facing, sight)` | the SIGHT-trainer pair (challenge + beaten swap), standing flags wired; returns the script/dialogue/trainer refs you owe |
| `cache(m, cid=…, at)` | item cache (NPC + pickup-script ref + picked-flag). The **variety rule**: per map mix consumables with a valuable and/or loose wicks; better ones off the lane |
| `sign(m, deco, w, sid=…, at)` | sign tile + interact trigger; returns the dialogue ref |
| `ledge_run(deco, …, y, x0, x1)` | a one-way hop-down ledge line (`grass_ledge_s` variants). Always leave a **gap** where the long way returns |
| `terrace(cliff, deco, …, area, ledge_y, gap)` | a raised shelf: cliff mass + south ledge lip + the route gap — walk up around, hop back down |
| `building(m, path, …, oid, sprite, at, overhang, to_map)` | whole-object structure: footprint from the objects manifest, door warp, path apron; returns the door's approach tile |
| `crown_tree(m, oid=…, sprite, at)` | a walk-under tree object (manifest footprint) |

Plus `mapkit`: `gid(name)`, `shared_tileset_ref()`, `scatter_decor`,
`fence_run`, `organic_border`, `finalize`.

## Hard rules the stamps don't cover (memorise)

- **Terrain is DRAWN, never AI-generated** (`gbaforge.py`); image-gen is for
  OBJECTS only — and goes through **generate-sprite-sheet**. New drawn
  families are APPENDED to `build_shared_overworld.py` (stable tile order).
- **Caves are multi-floor** (level-design §2a): a floor is a map; ladders are
  mutual step_on warp pairs landing ON each other (`cave_ladder_down`/`_up`);
  spur mouths live on the lowest floor; only a region's first dungeon stays
  one floor (+ small B1F).
- **Water gates ride the tiles** (water/pond carry `requires_ability:
  tidecall`); an always-walkable jetty needs the water carved out under it.
  `AbilityGate` rects force-gate EVERYTHING they cover — keep them on pure water.
- **Wide entrances warp on EVERY walkable tile** of the opening; landings sit
  ON (or within 1 of) the return warp (`audit_warps` enforces).
- **Story step_on triggers go ON chokes** so they can't be walked around.
- Spawn/NPC/trigger/warp tiles must be non-colliding; tall grass stays
  hard-edged fill-only; off-map = continuation.

## Env

Run builders with `./venv/bin/python` from the repo root (numpy/Pillow live in
the venv). `finalize()` shells out to node (`tools/autotile/expand.mjs`) and
the validators itself.
