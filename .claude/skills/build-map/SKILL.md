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
(composition §11, the dungeon scale ladder §2a, **§2b — the region is the
level** (how maps chain into a scene), and **§3a — the structural
principles of the greats**: loops not corridors, asymmetry by direction,
see-it-before-you-walk-it, braided risk-reward, one new idea per screen,
pressure-then-relief, lost-locally-never-globally, gates rhyme with rewards,
trainers are geometry, the map remembers) and the area's file in
`docs/world/walkthrough/` (the **Validation hooks** are the acceptance spec).
The §3a pass is now EXECUTED, not just eyeballed: `finalize()` runs
`audit_flow.py` (reachability, choke triggers, free-pass, loops, dead-end
payoff, screen pacing) on every build, and `audit_region.py` judges the
scene the map joins.

## The flow (every map)

1. **Read the spec first** — the atlas card (`docs/world/atlas.md`), the
   walkthrough region file's section for this map (main path beats, story
   beats, validation hooks), and `graph.ts` for the declared warp ids/edges.
   Name the area's **three signature touches** (level-design §8) before
   writing a line.
2. **Design the SCENE before the map** (level-design §2b): where this map
   sits in its region's loop, the level band it must bridge (neighbouring
   maps' tables ±4), the terrain its borders must continue (sand exits land
   on sand), which neighbour landmark gets a sight-line tease, and which
   Gift-gated promise this map plants or pays. Run
   `./venv/bin/python tools/maps/audit_region.py` before AND after — it
   prints the unlock waves, band borders, region topology and route lengths.
3. **Copy the nearest worked example** from `tools/maps/`:
   - town → `build_tinderwick.py` · route → `build_dimglass.py` /
     `build_saltreach_fen_i.py` (the pattern-library showcase)
   - cave floor → `build_glowmoss_deep.py` (+ `_b1f.py` for a lower floor)
   - interior → `build_interiors.py` (all five room types, on **roomkit**)
     · tower floor → `build_beacon.py` · hub → `build_crossroads.py`
4. **Paint terrain as presence grids** (`mapkit`: `blob`/`rect`/`hline`/
   `organic_border`), **stamp features** (`patterns`, below), assemble the
   dict, and end with `mk.finalize(m)` — write → autotile expand → strip →
   render → `validate_map` → `audit_warps` → `audit_flow`. **All must
   PASS**; flow WARNs need a justification in the builder's comments (e.g.
   `fenn_wave` is cosmetic — the NPC is directly interactable).
5. **Pay the content debts.** Stamps return the registry refs they create
   (`pt.report(owed)` prints them): scripts in `content/scripts.ts`, dialogue
   in `content/dialogue.ts`, trainers in `content/trainers.ts` (payout = class
   rate × ace, 10-economy §4 — and mirror into `BUILT_PAYOUTS` in
   `tools/balance/progression.mjs`). Register the map in `data/world/maps.ts`
   (+ edges in `graph.ts` if new — `audit_region.py` FAILS on a warp/graph
   mismatch and WARNs on undeclared geometry). Run `npx tsc --noEmit` and
   `node tools/balance/progression.mjs` — both must pass.
6. **Eyeball the render** (`/tmp/<map_id>.png`) against the §11 bar: no flat
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
| `gift_tease(m, deco, w, wid=…, at, ability, to_map, to, sign_id, sign_at, breadcrumbs)` | the GATED SPUR PROMISE (§3a rule 8): `requires_ability` warp + the why/come-back sign + a buoy/lamp breadcrumb line. Target may be unauthored (safe inert tease) — but declare it in `graph.ts` |
| `cave_ladder(m, deco, w, kind='down'/'up', at, to_map, to)` | one half of a dungeon floor link (§2a): ladder tile + step_on warp, landing ON its mirror — stamp both floors, `audit_warps` proves the pair |
| `mandatory_band(tallgrass, path, w, h, y0=…, y1, x0, x1)` | a full-corridor encounter crossing with the lane paused through it (§11 rule 7) — the road itself rolls; flanking patches stay optional |

Plus `mapkit`: `gid(name[, set=…])`, `shared_tileset_ref()`,
`register_tileset(name, index=…, first_gid=…)` + `gid_at`/`next_first_gid`
(stack an area's ACCENT tileset above the shared set — the engine resolves
gids by range), `scatter_decor`, `fence_run`, `organic_border`, `finalize`.

## The audit stack (what proves a map)

| Tool | Scale | Judges |
|------|-------|--------|
| `validate_map.py` | one map's picture | layers, autotile vocab, meshing %, decoration, borders |
| `tools/maps/audit_warps.py` | the doors | wide-entrance coverage, landings, round trips |
| `tools/maps/audit_flow.py` | one map's PLAY | reachability (FAIL), choke triggers, free-pass, loop/return asymmetry, dead-end payoff, screen pacing |
| `tools/maps/audit_region.py` | the SCENE | graph⇄JSON sync (FAIL), Gift unlock waves, level-band cliffs, region topology (corridor vs circuit), route lengths |

`finalize()` runs the first three; run the region audit yourself whenever you
add/move a warp, an encounter table, or a graph edge. FAILs block; WARNs are
design debt — fix or justify in the builder's comments. The flow audit found
four real shipped bugs on its first run (a sealed cache pocket, a sign
sealing Pearlmoor's west spoke, a cavern door with no standable approach, and
two walk-aroundable story beats) — trust it over your mental walk.

## Interiors (the roomkit path)

Interiors don't use mapkit/terrain — they compose on **`tools/maps/roomkit.py`**
to `docs/world/interiors.md` (binding): `faced_room` (the SNES enclosure) →
**`partition_v`/`partition_h`** (rooms within the room — every interior bigger
than a cabin gets one: bed nook, storeroom, bunk room, shrine niches) →
**`wall_mount`** (flush wall furniture: hearth/bookcase/shelf/dresser/stove/
lamp-rack place with their top row OVER the wall face — never floated a tile
south of it) + **`place`** (manifest-driven free-standing pieces) →
`rk.finish()` (write → render → audit_flow). Furniture is DRAWN, never
AI-generated — the kit lives in `tools/maps/interiorforge.py`; a new piece =
a new draw function + re-run + `pack_objects.py`. If a room resizes, update
the town builder's door landing and re-run `audit_warps`.

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
- **Story step_on triggers go ON chokes** so they can't be walked around —
  and band EVERY walkable tile of the cut (a single trigger on a wide row is
  walk-aroundable; triggers on solid cells are inert, so over-banding is
  safe). Pair `sets_flags` + `hidden_when_flag` so the band hides after the
  first fire. `audit_flow` proves the cut.
- Spawn/NPC/trigger/warp tiles must be non-colliding; tall grass stays
  hard-edged fill-only; off-map = continuation.

## Env

Run builders with `./venv/bin/python` from the repo root (numpy/Pillow live in
the venv). `finalize()` shells out to node (`tools/autotile/expand.mjs`) and
the validators itself.
