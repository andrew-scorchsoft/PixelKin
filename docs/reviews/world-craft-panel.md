# World-Craft Panel — pacing, density, and the little touches

*Audit, 2026-10-11. Read-only analysis of the shipped maps (`public/assets/maps/*.json`),
the world graph, the engine (`WorldScene`, `Actor`/`Player`/`Npc`, `MapRenderer`,
`CutsceneRunner`), the content registries, and the map renders in `docs/maps/renders/`.
The measuring script lives outside the repo (session scratchpad); the method is
described in §1 so it can be re-run.*

**The owner's brief:** "Some areas feel quite quick to go from section to section, or
the gameplay might be thin." The owner also asked what made the best 16-bit RPG of the
1990s feel so rich (judged by its craft, not copied), and for the next twenty "little
touches" in the vein of the once-missing swim sprite.

**Verdict in one paragraph.** The South is dense and works: it has 5.5–6.2 beats per
ten steps, about one stop every two seconds. From the East onwards, density falls to
1.4–2.6 beats per ten steps, and the drop is worst on the biggest maps. Most maps take
**4–15 seconds of walking** to cross (a step is 160 ms; running is 96 ms), so a thin map
feels like a corridor between two fades. The fix is more reasons to stop, not more
ground. On the engine side, the world is **static apart from the water**. Four tiles
animate, objects never move, nothing falls from the sky, nothing flies, no actor casts
a shadow, every `above` tile layer is empty, and only 1 of 1,385 cutscene lines uses
an action pose. Most of the 16-bit craft we want can be built on hooks the engine
already has (`HEAL_ENTRANCE_MAPS`-style code-drawn overlays, `Npc` wander/patrol, the
packed overworld kin sprites, the emote sheet, `Actor.hop`), so the work is cheap.
Prototype it on **Dimglass Coast I** (§5).

---

## 1. Measurement

### 1.1 Method

For every map JSON, `tools/maps/worldmodel.MapModel` (the engine-faithful collision model)
was used to count:

- **foot**: walkable tiles with no Lantern Gifts held;
- **encT**: painted encounter tiles;
- **zones**: encounter zones, with their mean rate;
- **trn**: trainers, counted as distinct `defeated_flag`/`sight_range` placements;
- **ppl**: NPC ids, excluding caches (flag-swap pairs inflate this a little);
- **cache**: `item_cache` placements;
- **sign** and **cut**: sign triggers and the other triggers;
- **obj**: map objects;
- **exits**: distinct warp targets;
- **cross**: the shortest walk between the two farthest-apart exits, all Gifts held.
  This is the "how quickly do I leave this section" number. Multiply it by 0.16 s for
  walking time.

Deco coverage (the share of tiles with a `deco` gid) and the number of distinct base gids
were measured separately as visual-density proxies. **Every map's `above` layer has 0
painted tiles.** Walk-behind comes only from object overhangs: 396 `walk_under` objects.

### 1.2 Overworld maps (towns, hub, routes, caves; interiors summarised below)

| Map | Size | foot | encT | zones · rate | band | trn | ppl | cache | sign | cut | obj | cross | deco% |
|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **South** |
| tinderwick | 28×24 | 318 | 46 | 2 · .07 | 2–4 | 0 | 10 | 2 | 6 | 1 | 17 | 34 | 6.8 |
| duskapple_orchard | 22×18 | 195 | 30 | 2 · .08 | 2–4 | 0 | 7 | 3 | 1 | 2 | 14 | — | 7.8 |
| lanternway_tinderwick | 24×18 | 269 | 18 | 1 · .07 | 2–3 | 0 | 1 | 1 | 1 | 0 | 5 | 29 | 4.6 |
| vesper_crossroads (hub) | 20×18 | 194 | 2 | — | — | 0 | 20 | 1 | 7 | 12 | 8 | 27 | 4.7 |
| dimglass_coast | 18×34 | 311 | 175 | 16 · .084 | 3–6 | 1 | 9 | 3 | 5 | 10 | 8 | 39 | 5.9 |
| dimglass_coast_ii | 18×32 | 277 | 138 | 10 · .084 | 8–11 | 2 | 10 | 4 | 3 | 3 | 5 | 37 | 7.8 |
| pearlmoor_quay | 28×24 | 269 | 117 | 6 · .073 | 8–12 | 0 | 18 | 1 | 9 | 13 | 17 | 35 | 8.9 |
| pearlmoor_point | 20×14 | 75 | 45 | — | — | 0 | 1 | 1 | 4 | 0 | 6 | 17 | 5.4 |
| pearlmoor_breakwater | 12×28 | 105 | 135 | — | — | 2 | 7 | 2 | 2 | 6 | 9 | — | 10.1 |
| pearlmoor_allotment | 20×16 | 126 | 0 | — | — | 0 | 3 | 1 | 1 | 2 | 9 | 15 | 8.8 |
| pearlmoor_wanderwood | 28×24 | 244 | 16 | 2 · .10 | 14–17 | 0 | 4 | 1 | 7 | 0 | 7 | 19 | 1.9 |
| pearlmoor_wanderwood_far | 30×24 | 235 | 38 | 8 · .10 | 14–17 | 0 | 1 | 1 | 15 | 2 | 7 | — | 3.5 |
| wrackline_path | 16×26 | 236 | 78 | 2 · .11 | 15–18 | 1 | 2 | 1 | 2 | 0 | 6 | 28 | 2.9 |
| sounding_cave | 20×14 | 103 | 18 | 1 · .13 | 16–19 | 0 | 0 | 1 | 1 | 0 | 0 | 19 | 5.7 |
| lanternfall_road | 16×26 | 240 | 57 | 3 · .11 | 18–20 | 1 | 2 | 1 | 2 | 0 | 6 | 28 | 4.1 |
| gullcry_rock (spur) | 16×13 | 49 | 121 | 2 · .09 | 10–13 | 0 | 0 | 1 | 1 | 0 | 0 | — | 6.7 |
| tideglass_cavern (spur) | 26×20 | 221 | 16 | 4 · .09 | 20–24 | 0 | 0 | 3 | 3 | 6 | 11 | 27 | 4.0 |
| **East** |
| saltreach_fen_i | 32×44 | **742** | 164 | 8 · .10 | 16–18 | 2 | 6 | 4 | 3 | **0** | **3** | 52 | 6.2 |
| saltreach_fen_ii | 32×44 | 418 | 540 | 10 · .09 | 17–19 | 1 | 6 | 3 | 6 | 3 | 13 | 45 | 3.4 |
| sunkbell_shallows (spur) | 20×16 | 39 | 54 | 2 · .08 | 17–20 | 0 | 0 | 2 | 2 | 0 | 1 | — | 2.5 |
| lowleaf_hollow | 30×32 | 507 | 32 | 2 · .10 | 18–20 | 2 | 23 | 5 | 8 | 33 | 17 | 40 | 6.0 |
| glowmoss_deep | 30×28 | 221 | 41 | 4 · .10 | 20–22 | 2 | 10 | 7 | 2 | 4 | 4 | 47 | 4.4 |
| glowmoss_deep_b1f | 24×20 | 97 | 22 | 2 · .12 | 21–23 | 0 | **0** | 1 | 1 | 0 | 1 | 47 | 3.1 |
| cinderhead_mine | 28×24 | 330 | — | 1 · .12 | 22–24 | 0 | 16 | 3 | 3 | 0 | 12 | 23 | 4.0 |
| cinderhead_deep | 28×22 | 138 | — | 2 · .12 | 24–26 | 1 | 3 | 1 | 2 | 4 | 3 | 31 | 3.6 |
| cinderhead_deep_b1f | 24×20 | 125 | — | 1 · .13 | 25–27 | 1 | 2 | 2 | 0 | 0 | 1 | 20 | 3.1 |
| cinderhead_deep_b2f | 22×18 | 111 | — | 1 · .13 | 26–27 | 0 | **0** | 3 | 0 | 0 | 1 | — | 3.0 |
| lanternway_lowleaf | 26×30 | 496 | 0 | — | — | 0 | **0** | 1 | 1 | 0 | 6 | 30 | 8.6 |
| **North** |
| galehigh_terraces | 32×32 | 475 | 49 | 8 · .08 | 28–30 | 2 | 26 | 7 | 6 | 2 | 21 | 51 | 3.1 |
| windward_stair_i | 24×40 | 488 | 110 | 10 · .09 | 32–36 | 2 | 8 | 3 | 2 | **0** | 11 | **93** | 2.4 |
| windward_stair_ii | 28×24 | 358 | 62 | 8 · .08 | 34–36 | 1 | 3 | 2 | 1 | 10 | 6 | 36 | 1.8 |
| pale_vault_glacier | 32×30 | 455 | 70 | 8 · .09 | 36–40 | 1 | 25 | 5 | 4 | 9 | 16 | 42 | 2.3 |
| lanternway_galehigh | 14×24 | 142 | 0 | — | — | 0 | **0** | 1 | 1 | 0 | 4 | 23 | 5.4 |
| **West** |
| hushfrost_pass_i | 32×28 | 494 | 80 | 12 · .09 | 40–42 | 2 | 6 | 4 | 2 | **0** | 12 | 60 | 2.0 |
| hushfrost_pass_ii | 30×28 | 437 | 27 | 8 · .10 | 40–42 | 1 | 6 | 2 | 2 | 4 | 11 | 51 | 2.3 |
| sunken_solarium | 31×34 | 440 | 86 | 6 · .08 | 42–46 | 2 | 24 | 9 | 4 | 11 | 32 | 55 | 1.7 |
| sunvault_climb_i | 30×26 | 421 | 57 | 8 · .10 | 46–48 | 1 | 4 | 2 | 2 | **0** | 11 | 36 | 5.4 |
| sunvault_climb_ii | 30×28 | 446 | 92 | 12 · .10 | 47–48 | 1 | 3 | 3 | 2 | 1 | 25 | 62 | 3.9 |
| nightreach_observatory | 30×30 | 454 | 79 | 4 · .10 | 48–52 | 2 | 34 | 4 | 4 | 15 | 48 | 38 | 3.9 |
| lanternway_nightreach | 24×18 | 271 | 0 | — | — | 0 | **0** | 1 | 1 | 0 | 5 | 30 | 10.0 |
| **Outer / Central** |
| coldfog_marches_i | 20×30 | 260 | 68 | 10 · .10 | 46–48 | **0** | 1 | 2 | 2 | 1 | 10 | 29 | 4.8 |
| coldfog_marches_ii | 30×26 | 411 | 98 | 10 · .10 | 48–50 | **0** | **0** | 3 | 3 | 3 | 16 | 45 | 4.1 |
| penumbra_ring | 28×34 | 352 | 0 | — | — | 0 | 1 | 2 | 2 | 5 | 17 | 43 | 2.7 |
| umbral_spire / f2 / f3 | — | 632 | — | — | 52–55 | 5 | 13 | 3 | 1 | 24 | 40 | 79 | ~2 |

**Interiors (33).** These are healthy: 7–17 objects on 39–98 walkable tiles, and the
Old Light floors carry 3–7 signs or triggers each. One gap stands out: 32 of 33
interiors have **no ambient motion at all** (no hearth flicker, no light shafts).

### 1.3 Journey legs (main path, graph order)

The **beats/10** column is (trainers + caches + NPCs + scripted triggers) per ten steps
of crossing. The **props/100** column is objects per 100 walkable tiles.

| Leg | Maps | Cross (steps) | Walk / run time | trn | cache | ppl | cut | beats/10 | props/100 | Read |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| S · Lanternway home → Fenn | 2 | 56 | 9 s / 5 s | 0 | 2 | 21 | 12 | 6.2 | 2.8 | rich |
| S · Dimglass I+II | 2 | 76 | 12 s / 7 s | 3 | 7 | 19 | 13 | **5.5** | 2.2 | rich: the model |
| S · Pearlmoor spoke (opt) | 3 | 75 | 12 s / 7 s | 2 | 3 | 4 | 0 | 1.2 | 2.1 | **thin** |
| E · Saltreach Fen I+II | 2 | 97 | 16 s / 9 s | 3 | 7 | 12 | 3 | 2.6 | **1.4** | **thin + bare** |
| E · Glowmoss Deep + B1F | 2 | 94 | 15 s / 9 s | 2 | 8 | 10 | 4 | 2.6 | 1.6 | ok, B1F empty |
| E · Cinderhead Deep ×3 | 3 | 51 | 8 s / 5 s | 2 | 6 | 5 | 4 | 3.3 | 1.3 | ok (Vigil errand) |
| N · Windward Stair I+II | 2 | **129** | 21 s / 12 s | 3 | 5 | 11 | 10 | 2.2 | 2.0 | **over-long + thin** |
| W · Hushfrost I+II | 2 | 111 | 18 s / 11 s | 3 | 6 | 12 | 4 | 2.3 | 2.5 | **thin** |
| W · Sunvault I+II | 2 | 98 | 16 s / 9 s | 2 | 5 | 7 | 1 | **1.5** | 4.2 | **thin** |
| O · Coldfog I+II | 2 | 74 | 12 s / 7 s | **0** | 5 | 1 | 4 | **1.4** | 3.9 | **thin** (desolate by design, but empty rather than authored) |
| C · Penumbra Ring | 1 | 43 | 7 s / 4 s | 0 | 2 | 1 | 5 | 1.9 | 4.8 | **thin** |
| C · Spire F1–F3 | 3 | 79 | 13 s / 8 s | 5 | 3 | 13 | 24 | 5.7 | 6.3 | rich |
| Spokes ×4 (safe lanes) | 4 | 83 | 13 s / 8 s | 0 | 4 | **0** | 0 | **0.5** | 1.6 | thinnest (safe by design) |

**Reading the numbers.**

- The South's density is the bar, and it was earned through playtests. Everything after
  it runs at **one-quarter to one-half of that density**, and most of the gap is in
  scripted triggers (`cut`): the South has 13 per leg, the later legs 0–4. Hushfrost I,
  Windward I, Sunvault I and Saltreach Fen I each have **zero** step-on or interact
  beats.
- **Over-long:** Windward Stair I (93 steps, the longest crossing in the game, with no
  scripted beat) and Sunvault Climb II (62 steps).
- **Too quick:** the 1–2-screen connectors (Wrackline 28, Lanternfall 28, Sounding Cave
  19, the spokes 23–30, Pearlmoor Point 17). They are not too short. They have nothing
  in them, so the player meets a fade, then a fade, then a fade.
- **Bare on sight:** Saltreach Fen I is the biggest walkable map in the game and has the
  fewest props (3).

### 1.4 What the renders show

Renders viewed: tinderwick, dimglass_coast, pearlmoor_quay, saltreach_fen_i,
windward_stair_i, hushfrost_pass_i, sunvault_climb_i and coldfog_marches_i.

- **Tinderwick and Pearlmoor Quay are at the bar.** They have crown trees, lit windows,
  lamp posts, a fenced garden, boats, beach scatter and roofs with real eaves. Only
  motion is missing.
- **Dimglass Coast I is good.** Its lane meanders, the grass has hard edges, there are
  buoys and the sea is a real edge. Again, only motion is missing.
- **Saltreach Fen I reads as a lawn with rectangles in it.** The pools are cross- and
  plus-shaped boxes, not blob shores (this breaks level-design §11 "blob shores"). There
  are two crown trees on 742 tiles and one stone L-wall. A marsh should be the busiest
  texture in the game (reeds, stilt-walks, nets, herons, lantern-reeds), and here it is
  one of the emptiest.
- **Hushfrost Pass I is a grey-slab maze.** Its rectangular snow plateaux carry three
  identical ice-crystal props and lamp posts. It has no drifts, no tree line, no
  wreckage and no frozen waterfall, so it reads as a switchback diagram.
- **Windward Stair I is three wide empty plates** stacked with one camp vignette. There
  is no wind made visible: no prayer-flags, no bent grass, no cairns at the turns.
- **Sunvault Climb I is three gold terraces**: an even scatter of boulders, two columns
  and grass patches. The ruin promised by its name (fallen colonnades, sun-dials,
  overgrowth over masonry) is barely present.
- **Coldfog Marches I is sparse in a deliberate way**, but its emptiness looks unfinished
  rather than authored. Drained land needs to show what was lost: abandoned things,
  doused lamps, a table set for nobody.

---

## 2. 16-bit craft worth borrowing (described by technique)

The 1990s 16-bit RPG the brief points at had an opera set-piece and a world that breaks
in half. Its richness came from a handful of repeatable techniques. Each is listed below
with what our engine already has.

**Status key:** **S+U** = supported and used · **S+u** = supported but underused ·
**M** = missing.

| # | Technique (as craft) | What it did there | Our engine today | Status |
|---|---|---|---|---|
| 1 | **Sprite acting**: a pose library (nod, shake head, laugh, collapse, kneel, arms up, back turned with shoulders shaking, little jumps of surprise), performed on the map in place of portraits | Cutscenes were stage plays. Small sprites carried enormous emotion through timing and pose. | `move`/`face`/`emote`/`action` ops exist and `Actor.hop()` exists. Across all content there are **1,007 `say` + 378 `narrate`** lines against **5 `move`, 22 `face`, 23 `emote` and 1 `action`**. Only `player_indi` has an action sheet. `hop` is not a cutscene op. | **S+u** (the biggest gap in the table) |
| 2 | **Walk-behind layers**: canopies, roof eaves, arches, tall-grass front blades | The map has depth, and the player is *in* it, not on top of it. | Object `overhang`/`walk_under` is used (396 objects). The `above` tile layer exists on 68 maps but **is empty on all of them**. Grass never covers the player's legs. | **S+u** |
| 3 | **Animated tiles and props**: water shimmer, waterfalls, torches, chimney smoke, flags, flickering windows | Every screen moves a little, so the world feels alive while you stand still. | `AnimatedTiles` works, but only **4 tiles** animate (the water, pond, sunpool and void fills). All of them tick in lockstep, and shore edges do not animate. `MapObject` has no frames, so the 91 lamp posts, chimneys and boats are frozen. | **S+u / M** |
| 4 | **Translucent overlay layers**: drifting fog and cloud shadows, rain or snow sheets in a parallax layer, colour-math washes for flashbacks and ruined-world tints | Mood was carried by a layer *over* the map, independent of the tiles. | The `tint` op covers full-screen washes and is used 141 times. `LamplightMask` is a per-map overlay on 10 dark maps. `AttractScene` already scrolls seamless parallax strips. **There is no persistent per-map overlay, fog drift or weather layer.** | **M** (the parts exist) |
| 5 | **Ambient actors**: birds lifting off, townsfolk on circuits, critters on roads, a dog that runs to you | Towns had *routines*, and routes had life between battles. | `Npc` has `wander`/`patrol`/`look_around`. Across 615 NPC placements, `patrol` is used **0** times and `wander` 20 times (with no leash). Overworld sprites are packed for all 162 kin, but only 3 are placed (the Three Hours). There are no fliers. | **S+u** |
| 6 | **Light pools at night**: torch glow on walls, lit windows, a lamp-carrier's halo | Night scenes read as *lit*, not as dark-tinted. | The heal-lantern and Lumenary-crest code-drawn glows exist. `LamplightMask` covers the player's radius on dark maps. **Lamp posts, windows, braziers and hearths cast nothing.** | **M** (one pattern to generalise) |
| 7 | **Screen grammar**: shake for impacts, a white flash for magic, fade-to-black for time skips, a held silence before the big line | Drama comes from rhythm, not from text volume. | `shake` (6), `flashColor` (8), `silence` (54), `letterbox` (70), `cameraFocus` (8). | **S+U**. Shake is underused for impacts (the fallen star, the bell). |
| 8 | **Area-name card on entry** | The player always knows where they are, and each arrival feels like an event. | `flashLocationBanner` shows plain accent text, bottom-left, for 1.6 s. It has no plate and no region subtitle. | **S+u** |
| 9 | **The re-dressed world**: the same map after the catastrophe, with a new palette, new NPC lines and new paths | The world's change is told by places you already know. | Flag-gated objects and NPCs, the day-forms and the `flag:dawn` re-dress. | **S+U** (our strength; keep it) |
| 10 | **Interior density and secrets**: every house enterable, clutter that says who lives there, walls you can slip through, treasure in odd corners | Exploring pays off at every scale. | roomkit plus the binding interiors.md, 103 invisible interact triggers (inspectables and finds) and 141 caches. **There is no "secret passage" convention** (a hidden walkable gap in a wall or treeline). | **S+U**, minus secrets |
| 11 | **Set-piece staging with moving scenery** (a stage that swaps backdrops, an airship deck, a collapsing tower) | Spectacle is made from tiles plus timing. | `cameraFocus`, flag-swapped objects and the `cinematic` op. | **S+u** |
| 12 | **Per-surface audio**: footsteps change on wood, stone and grass; ambient loops (wind, surf, mine drips) under the music | You hear where you are. | One `world-footstep` sound on every surface. **No ambient beds.** | **M** |

**Craft rules to adopt (style, not content):**

- **Act before you speak.** Every story scene should open with a beat of
  movement (a turn, an emote, a step) before the first line, and close with one.
  The budget is at least **one acting op per four lines** in any new or polished scene.
- **Every screen moves somewhere.** Each 15×10 window should hold at least one live
  element: water, a flame, a drifting particle, a bird or a wandering NPC.
- **Mood belongs in a layer, not in tiles.** Fog, snow, ash and motes are overlay data per
  map. They are never painted into the frozen tileset.
- **Light is a prop.** Anything that burns casts a pool, and the pool flickers.
- **Desolation is authored.** Empty places show what is *missing* (a doused lamp, a set
  table, a dropped toy), never just blank floor.

---

## 3. The little touches: inventory (each verified against the code)

**Effort:** S is under half a day, M is 1–2 days, L is 3 days or more.

**Kind:**
- **D** = data only (map JSON, content or the registry);
- **E** = needs engine code;
- **E+A** = engine code plus a small shared art or SFX asset.

| # | Touch | Present? | Where | Effort | Kind |
|---|---|---|---|---|---|
| 1 | **Area-name plate on entry.** A framed theme plate with the region underneath ("DIMGLASS COAST · the South") that slides in top-left on first entry per session and is quieter on re-entry. | Partial: plain text only (`WorldScene.flashLocationBanner`) | All maps | S | E |
| 2 | **Tall grass hides your legs.** A grass-blade overlay over the bottom third of an actor standing on an `encounter_terrain` tile. This is *the* genre cue that you are "in" the grass. | Missing | `Player`/`Npc` + `map.hasTerrainAt` | M | E+A |
| 3 | **Grass rustle on step.** The tuft does a 2-frame shake and kicks a fleck or two of leaf, with a soft rustle SFX. | Missing | `onPlayerArrive` | S | E+A |
| 4 | **Encounter tell.** The grass tile you step on shudders for one beat before the battle swoosh. | Missing (the swoosh exists in `Transitions`) | `EncounterSystem` → `startBattle` | S | E |
| 5 | **Footprints in sand and snow** that fade over about 4 s. They key on the sidecar's `sand`/`snowpatch`/`snowtrail`/`dunegrass` terrains, which already exist. | Missing | `onPlayerArrive` | S | E+A |
| 6 | **Footsteps by surface** (grass, sand, snow, stone, wood, interior floor), chosen from the terrain tag. | Partial: one footstep sound for every surface | `onPlayerArrive` + generate-midi | S | E+A |
| 7 | **Swim ripples.** An expanding ring on each swim step, plus a splash when you enter water. | Partial: the wake ellipse breathes (`Player.setSwimming`) | `Player` | S | E |
| 8 | **Water out of lockstep.** Offset each animated tile's phase by `(x+y)` so the sea glitters instead of blinking all at once. | Present, but in lockstep | `MapRenderer.tickAnimatedTiles` (a one-line change) | S | E |
| 9 | **Lamp-post light pools.** A code-drawn warm stepped halo under every `*_lamp_post`/brazier/window object, with a slow flicker. This generalises `markHealEntrances` into a `LIGHT_SOURCES` sprite→{offset, radius, colour} table. | Missing (91 lamp posts, 30 braziers) | `WorldScene` | S | E (no art) |
| 10 | **Chimney smoke.** 3–4 grey puffs rising and fading from each house sprite, keyed by a sprite→chimney-offset table. | Missing | `WorldScene` (crest pattern) | S | E |
| 11 | **Falling-star streak** across the sky at random 40–90 s intervals on outdoor maps: a code-drawn 1px line with a glow head, cold blue-grey. After `flag:dawn` it turns warm gold (the Starfall mirror). This is the game's own motif (peril thread §1), and it never appears in normal play. | Missing | New `systems/world/Ambience.ts` | S | E (no art) |
| 12 | **Region particles**: snow (north and west), ash and embers (Cinderhead), glowmotes (Glowmoss and Lowleaf), spores (Spore Grotto), sea spray (the coast), drifting cold motes (Coldfog). One emitter system plus a per-map `ambience.particles` block. | Missing (no world particles at all) | `Ambience.ts` + map data | M | E+A |
| 13 | **Drifting mist and cloud shadows**: a seamless translucent strip scrolling slowly over the map, reusing the AttractScene parallax technique. Fog for Coldfog, Hushfrost and the fen; cloud shadow for Galehigh. | Missing | `Ambience.ts` | M | E+A |
| 14 | **Ambient kin on routes.** A non-battle, non-colliding wandering overworld kin (the route's own encounter-table species) that hops away when you come near. The art is already packed for all 162 kin; the engine needs an `ambient: true` flag (no collision, no interact, leash). | Supported in part (creature NPCs), used on 3 maps | Map NPC data + `Npc` | M | D+E |
| 15 | **Gulls and birds.** A flock that lifts off when you approach (beach, quay, Galehigh crags), and an occasional single bird crossing the screen. | Missing | `Ambience.ts` | M | E+A |
| 16 | **Drop shadows** under every walk-sheet actor: a soft 1px oval at the feet that shrinks during a ledge hop. | Missing (only the placeholder bundle draws one) | `Actor` | S | E |
| 17 | **Idle life**: standing NPCs do a 1px breathing bob every few seconds; the player looks around after 8 s idle. | Missing | `Actor`/`Npc` | S | E |
| 18 | **NPCs turn back** to their post facing after a talk; `look_around` NPCs glance at you when you pass within 2 tiles. | Partial: they face you on talk (`npc.facePoint`) | `Npc` | S | E |
| 19 | **Town routines**: lamplighters on `patrol` circuits lighting posts, a child chasing a kin, a fisher walking quay to boat, and a `wander_radius` leash so wanderers stay put. | `patrol` supported but used **0** times; `wander` has no leash | Map NPC data + `Npc` | S | D (+S E for the leash) |
| 20 | **Door-open beat**: the door tile darkens to an open doorway for about 120 ms before the fade (code-drawn rect, no art), and `world-door-close` plays on exit. | Partial: SFX only | `executeWarp` | S | E |
| 21 | **Caches sparkle**: an uncollected `item_cache` glints every few seconds and pops open with a puff when taken. | Missing (it just vanishes) | `Npc` (cache sprite) + pickup | S | E |
| 22 | **Ledge-hop dust**: a 2-puff landing cloud plus a shadow during the arc. | Missing (the hop exists) | `Actor.hop` | S | E+A |
| 23 | **Sprite-acting ops**: expose `hop` (surprise jump) and add `shakeActor` (a shudder), `spin` (look around), a speed parameter on `move`, and parallel moves. Then give the key scenes a pass. | `hop` exists but is not an op | `CutsceneRunner` + content | M | E then D |
| 24 | **Emote dressing on talk**: sleepy NPCs show `sleep`, hummers `music`, worried folk `sweat`, all through the existing `emote` op on their interact scripts. | Sheet exists; 8 emotes; 23 uses | Content scripts | S | D |
| 25 | **Ambient sound beds** (surf, wind, crickets, mine drips, crackle) at low volume under the music, per map. | Missing | `Sfx`/MusicDirector + generate-midi | M | E+A |
| 26 | **Boats bob and flags flutter**: a 1px sine bob on `*_boat`/buoy objects and a 2-frame flutter on banners. | Missing | `MapRenderer` object tween table | S | E |
| 27 | **Window glow flicker**: the lit windows already in the house art get a faint additive flicker overlay (from the same `LIGHT_SOURCES` table). | Missing | `WorldScene` | S | E |
| 28 | **Your lead kin follows you**: the party lead walks one tile behind using its overworld sprite, and hides in cutscenes, on water and in interiors. This is the biggest charm win and the biggest risk (cutscene choreography, collision, doors). | Missing | `Player` + `WorldScene` | L | E |
| 29 | **Secret gaps**: a hidden walkable gap in a treeline or wall that leads to a nook, as a builder convention (`patterns.secret_gap`). `audit_flow` must accept it. | Missing as a convention | Builders + audits | M | D (+tooling) |
| 30 | **Persistent map tint** (`ambience.tint`): a cold wash for Coldfog, a warm one for Dawnstead and a green-gold one for Glowmoss, so a region reads at a glance. | Missing (only the transient `tint` op) | `Ambience.ts` | S | E |

**The top 12 by delight per effort**, in priority order. Items 8, 11, 9, 10, 16, 1 and
20 need no new art.

1. #2 legs hidden in grass
2. #9 lamp light pools
3. #11 the falling-star streak
4. #12 region particles
5. #14 ambient kin
6. #16 drop shadows
7. #3 grass rustle
8. #5 footprints
9. #8 the water phase offset
10. #10 chimney smoke
11. #1 the area plate
12. #23 the sprite-acting ops, plus the acting pass on key scenes

---

## 4. Pacing: the 10 thinnest places, fixed with richness, not length

**The hard rule.** Nothing on the pre-Chickenpig path may get longer or harder. That path
is Tinderwick, Duskapple Orchard, Lanternway Tinderwick, the Crossroads, Dimglass I and
II, and Pearlmoor through S4 at the breakwater. There, **only visual, ambient and feel
changes** are allowed:

- no new required beats, triggers, trainers or encounter-rate changes;
- no new lane-blocking objects;
- ambient kin set non-colliding;
- the area plate must not stall input.

Everything below is optional by construction: off-lane nooks, beats an NPC offers, or
things you can inspect. None of it adds a required step to any main path. Rewards should
avoid wicks; prefer lore, Charts, LORE entries, emote moments and existing items. Any
wick reward must be mirrored in `tools/balance/progression.mjs`.

| Rank | Place | Evidence | Richness fix (no added length) |
|---:|---|---|---|
| 1 | **Saltreach Fen I** (E) | The largest walkable map (742 tiles), 3 objects, **0** scripted beats, 1.4 props/100, and box-shaped pools in the render. | (a) Re-blob the pools in `build_saltreach_fen_i.py` (shore blobs, reed fringes, a stilt-walk across one pool) as visual density on the same footprint. (b) **The fishing-stilt nook**: a reed-hut off the lane with an old eel-fisher who tells one fen story and lets you *inspect his net-weights*, which reveal a hidden cache under the boards. (c) **Lantern-reeds**: three dark reed-lanterns, each lit with a one-line interact, light a sign that names the fen's lost village (lore + a Chart tease). (d) A heron-kin rookery, as ambient kin that scatter. |
| 2 | **Windward Stair I** (N) | The **longest crossing in the game (93 steps)**, 0 scripted beats, three wide empty plates. | Do not lengthen it. Make the climb *mean* something. (a) **The cairn-count**: each switchback has a cairn, and adding a stone (interact) plays a wind line from the stair-warden. The summit cairn notices if you added all four (cosmetic plus a LORE entry). (b) Prayer-flag objects and bent-grass deco at every turn, plus a gust particle. (c) A one-way **ledge shortcut back down** for the return trip, which *compresses* the leg (level-design §2b r2). |
| 3 | **Hushfrost Pass I** (W) | 60 steps, **0** scripted beats, slab maze, one ice-crystal prop repeated. | (a) **The ice-chime**: three icicle props tuned by a pass-walker's hummed phrase (an emote `music` hint). Strike them in order (interact choices) to free a cache frozen in a drift. (b) A frozen-over cart and a snowed-in shrine as vignette objects. (c) Snow particles plus footprints; the N2 crater sits in the snow and hisses with an ember particle. |
| 4 | **Sunvault Climb I+II** (W) | 1.5 beats/10, 1 scripted beat in 98 steps, an even boulder scatter. | (a) **The sun-dial**: a fallen dial on the I terrace. Sunsketch (already earned by the time you can return) casts its gnomon shadow onto an engraved tile, opening a sealed niche: an *optional* Gift-depth puzzle in the spine's §5 "Sunsketch light-puzzle" voice. (b) A terrace gardener who has kept one bed alive through the Dusk and gives a line plus a flower emote. (c) A fallen-colonnade overhang to walk under, giving depth. |
| 5 | **Coldfog Marches I+II** (Outer) | **0** trainers, 1 NPC on I, 0 on II, 1.4 beats/10. | Desolation, authored. (a) **The set table**: an abandoned cottage frame with a table laid for three; interacting gives one narrate line, and that is all. (b) Doused lamps you can relight (each gives one line). They go out again when you leave, because Coldfog resists Lamplight, and saying so makes the canon felt. (c) A single wandering **hollow-eyed villager** you can walk beside (patrol) who answers in half-sentences and is gone after `flag:dawn`. Persistent cold tint plus mist drift. |
| 6 | **Penumbra Ring** (C) | The last breath before the Spire: 0 encounters, 1 NPC, 43 steps. | (a) **The eight memorial lamps** around the ring, one per Lampwarden, each lit if that Gleam is held (flag-gated objects). Each one's interact plays that warden's parting line, an earned recap before the climax. (b) The C1 marsh-villagers' campfire as a rest point (heal) with an optional Wren/Fenn talk. (c) Starglint particles. |
| 7 | **The four Lanternway spokes** (Outer) | 0.5 beats/10; 0 NPCs on three of them. Safe lanes by design (no encounters is correct). | Life without danger: (a) a lamplighter on a **patrol circuit** who greets you differently per Gleam count; (b) a pedlar's cart (dialogue only); (c) fireflies or glowmotes plus ambient kin grazing off-lane; (d) a falling-star streak tuned more frequent here, since these are the night roads. **Lanternway Tinderwick is pre-Chickenpig**, so it gets ambience only (c, d) and no new NPC beats. |
| 8 | **Pearlmoor spoke** (Wrackline → Sounding Cave → Lanternfall) (S, optional) | 1.2 beats/10, 0 scripted beats in 75 steps. | It is off the pre-Chickenpig main path but reachable from it, so add **nothing that makes it harder or required**. (a) **The echo**: a hermit-less sounding stone in Sounding Cave. Interact and the cave answers with a line that names where a hidden cache sits (inspect-only find). (b) Tide-pool rummage spots on Wrackline: three inspectables with flavour finds. (c) Sea-spray and gull ambience. |
| 9 | **Cinderhead Deep B1F/B2F** (E) | 0 NPCs on B2F, 1 object per floor, 3.0 deco%. | (a) **The lost ledger**: three torn pages, one per floor, as inspectables. Together they tell the last shift's story, and Otho comments if you bring all three (the existing Vigil errand already walks these floors, so this follows the collinearity rule). (b) Ore-cart and rail props; ash and ember particles; drip ambience. |
| 10 | **Glowmoss Deep B1F** (E) | 97 tiles, 0 NPCs, 1 cache, the dark maze floor. | (a) A **glowshroom breadcrumb you light**: tapping a dim glowshroom makes it pulse brighter (a code-drawn light pool), so a player can leave their own trail. It is a comfort gate, not a puzzle. (b) Glowmote particles; one ambient Fennlight kin drifting near the ladder. |

Honourable mentions: Windward Stair II (1 cache, 1.8 deco%); Hushfrost II (27 grass
tiles); Wanderwood (1.9 deco%, optional S5 ground).

**South, ambient-only list.** This is the whole of the pre-Chickenpig allowance.

- **Tinderwick:** chimney smoke, lamp pools, window flicker, gulls on the beach, the
  water phase offset and drop shadows.
- **Duskapple Orchard:** falling leaves, and a cold-cinder glow in the crater (blue-grey
  pulse) that turns gold at dawn.
- **Dimglass I and II:** legs hidden in grass, rustle, sand prints, buoy bob, sea spray,
  and a gull flock.
- **The `dusk_begins` beat:** a falling star streaks across the sky in that scene's
  existing camera beat. This needs only an added `starfall` op or ambience call; it adds
  no lines and no length.
- **Pearlmoor:** boats bob, lantern pools on the quay, and the harbour gulls.
- **The Old Light:** dust motes in the window shafts. It stays the same length and
  difficulty.

---

## 5. Pilot recommendation: **Dimglass Coast I**

**Why this map.**

1. **Every player sees it within ten minutes.** It is the first route and the first
   encounter grass, so the "this feels alive" verdict is formed here.
2. **It has every surface the ambient kit has to handle**, in 18×34: tall grass
   (legs hidden, rustle, encounter tell), sand (prints, footstep timbre), sea (phase
   offset, spray, buoy bob, swim ripples via the Tidecall gate), trees (walk-under
   canopies), lamp posts (4, giving light pools), a ledge (dust), sight trainers
   (drop shadows on the march) and the `dusk_begins` omen (the falling-star debut,
   with the motif tied to story on first sight).
3. **It sits inside the hard constraint**, so it proves the core claim: richness through
   feel, with zero added length or difficulty. If the coast feels fuller without one
   extra step, the method is validated for the whole game.
4. **It is cheap to iterate.** One builder (`build_dimglass.py`), one shipped JSON and
   no interiors. The ambience lives in a new optional data block, so no rebuild is needed.

**The follow-up richness pilot** is **Saltreach Fen I**, the thinnest map with no
constraint. Use it to prove the *content* half (§4 #1) once the ambient kit is in.

**Pilot acceptance checklist (Dimglass I):**

- [ ] The plate shows "DIMGLASS COAST · the South" on first entry and does not block input.
- [ ] Legs are hidden on all tall-grass variants (and every `encounter_terrain` tile), and
  hidden on NPCs too.
- [ ] Rustle plus fleck on each grass step; the encounter tell plays before the swoosh.
- [ ] Sand prints fade within 4 s, with at most 12 alive at once.
- [ ] The sea shimmers out of phase; buoys bob 1px; spray particles along the shoreline.
- [ ] Four lamp pools flicker and sit below actors and above the ground.
- [ ] Drop shadows on the player, Wren, the witness and the sight trainers.
- [ ] A falling star crosses the sky during `script.dusk_begins` and then every 40–90 s;
  it is never more frequent than that.
- [ ] One ambient kin from the coast's own table grazes off-lane and hops away when you
  are within 2 tiles. It is non-colliding and never blocks the lane.
- [ ] No change to encounter rates, trainers, triggers, warps or walkable tiles:
  `audit_flow`, `audit_warps`, `audit_region` and `render_walkable` all pass unchanged.
- [ ] Performance: 60 fps on a mid phone in Chrome devtools throttling, with a particle
  cap of 40 on screen.
- [ ] Everything degrades silently when an art sheet is missing (the house rule).
- [ ] A `prefers-reduced-motion`-style Settings toggle, or reuse of an existing one,
  turns off particles and streaks. The settings list is at its 160px budget, so this
  goes in a sub-screen or folds into an existing row.

---

## 6. Roll-out: independent work packages

**Shared-file owners (single owner, serialised).** No regional package touches these:

- `src/game/scenes/WorldScene.ts`
- `src/game/entities/{Actor,Player,Npc}.ts`
- `src/game/systems/world/MapRenderer.ts`
- the new `src/game/systems/world/Ambience.ts`
- `src/game/data/world/types.ts`
- `src/game/systems/cutscene/CutsceneRunner.ts` and `src/game/content/types.ts`
- `src/game/scenes/PreloadScene.ts`
- `src/game/ui/SettingsMenu.ts`
- `public/assets/audio/sfx/sfx.manifest.json`
- `tools/maps/worldmodel.py` (and the audits that read it)
- `tools/balance/progression.mjs`
- `src/game/content/quests.ts` and `content/glossary.ts` (append-only, but one owner, to
  avoid merge churn)

**WP0 · Engine ambient kit (single owner; it blocks the others).**

- **Schema:** add `MapDefinition.ambience?` to `types.ts`, with these fields:
  `particles`, `mist`, `tint`, `starfall`, `birds`, `light_sources_extra`, `sound_bed`.
  Add `NpcPlacement.ambient?: boolean` and `NpcPlacement.wander_radius?: number`.
- **`Ambience.ts`:**
  - particles with a cap;
  - a mist strip;
  - a persistent tint;
  - the starfall streak, which warms after `flag:dawn`;
  - a bird flock;
  - `LIGHT_SOURCES` and `CHIMNEYS` sprite tables (the `HEAL_ENTRANCE_MAPS` pattern).
- **`Actor`/`Player`/`Npc`:**
  - drop shadow;
  - the grass-legs overlay;
  - idle bob;
  - turn-back after a talk;
  - the wander leash;
  - the `ambient` flag (no collision, no interact, flee-hop when you are within 2 tiles).
- **Other engine changes:**
  - `MapRenderer`: the animated-tile phase offset and the object bob table.
  - `WorldScene`: the area plate, door-open beat, cache sparkle, footprints, rustle and
    encounter tell, plus terrain-keyed footstep variants.
  - `CutsceneRunner`: the `hop`, `shakeActor`, `spin` and `starfall` ops, plus `move.speed`.
- **Tooling:** add the one-time spread hook in `content/scripts.ts`:
  `...REGION_EXTRA_SCRIPTS` from new `content/regions/*.ts` modules, following the
  `OLDLIGHT_SCRIPTS` precedent. Update `worldmodel.py`, `audit_flow` and
  `render_walkable` so `ambient` NPCs are ignored as blockers. Add
  `tools/maps/add_world_craft.py`, an id-keyed upsert runner in the `add_peril_thread.py`
  pattern that reads per-region modules from `tools/maps/worldcraft/<region>.py`. It is
  needed because shipped JSONs carry post-build additions their builders lack.
- **Docs:** add a §12b "Ambience" section to `docs/art-style.md`, a level-design §11 rule
  ("every screen moves"), and CLAUDE.md gotchas.

**WP1 · Shared art and SFX (single owner; it can run in parallel with WP0).**

- **Art:** in `assets/effects/`, then packed into `public/assets/sprites/effects/`:
  - grass-blade leg overlay;
  - leaf fleck;
  - footprint (sand and snow);
  - ripple ring;
  - dust puff;
  - a bird or gull 4-frame sheet;
  - particle glyphs (snowflake, ember, ash, glowmote, spore, spray);
  - two mist strips (fog, cloud shadow), made seamless with the AttractScene mirror trick.
- **SFX:** via generate-midi:
  - grass rustle;
  - splash;
  - footsteps for sand, snow, stone and wood;
  - gull;
  - looped beds for surf, wind, crickets, mine drips and hearth crackle.
- **Rule:** all of it is *drawn or composed new*. The frozen 386-tile overworld set is
  never appended.

**Regional packages WP2–WP6.** These can run in parallel once WP0's schema lands. Each
owns only:

- **(a)** its region's map JSON `ambience` blocks and new NPC/object/trigger entries, via
  its own `tools/maps/worldcraft/<region>.py` (run through `add_world_craft.py`);
- **(b)** its region's map **builders**, if a re-blob or re-dress is needed. Diff
  against HEAD and re-apply post-build additions, per the CLAUDE.md gotcha;
- **(c)** its own `src/game/content/regions/<region>.ts` (new scripts and dialogue
  only);
- **(d)** its own new objects under `assets/tilesets/<area>/objects/` plus
  `pack_objects.py` output for those stems.

Shared-registry additions (quests, glossary, progression wicks, `maps.ts` battle
backdrops) are written as a **request list** in the package's PR description and applied
by the integrator.

| WP | Region | Maps owned | Scope |
|---|---|---|---|
| **WP2** | **South, ambient only** | tinderwick, duskapple_orchard, lanternway_tinderwick, vesper_crossroads, dimglass_coast/_ii, pearlmoor_quay/_point/_breakwater/_allotment, the oldlight floors, gullcry_rock, tideglass_cavern | The `ambience` blocks plus ambient kin (non-colliding) only. No new triggers or NPC beats on the pre-Chickenpig path. The Pearlmoor spoke (wrackline, sounding_cave, lanternfall) may take §4 #8's optional inspect-only finds. **The pilot (Dimglass I) ships first, inside this package.** |
| **WP3** | **East** | saltreach_fen_i/_ii, sunkbell_shallows, lowleaf_hollow (+interiors), gloamwood_dell, glowmoss_deep/_b1f, spore_grotto, cinderhead_* , lanternway_lowleaf/_undercut | §4 #1 (the Fen re-blob + nooks; touches `build_saltreach_fen_i.py`), #9 and #10; motes, ash and fog ambience. |
| **WP4** | **North** | galehigh_* , windward_stair_i/_ii, thunderroost, wind_eye, pale_vault_* , lanternway_galehigh | §4 #2 (cairns + the ledge shortcut via `build_windward_stair*.py`); snow, cloud-shadow and gust ambience; Pale Vault aurora tint. |
| **WP5** | **West** | hushfrost_pass_i/_ii, aurora_hollow, sunken_solarium(+lumenary), unrisen_stair, sunvault_climb_i/_ii, helia_vault, nightreach_* , lanternway_nightreach | §4 #3 and #4; snow and sun-mote ambience; Nightreach star particles. |
| **WP6** | **Outer + Central + post-game** | coldfog_marches_i/_ii, drownlight_beacon, hollowfen_stillworks, penumbra_ring, starwell, umbral_spire_*, dawnstead, the vigil_* maps | §4 #5 and #6; Coldfog mist and tint; Spire null-motes; Dawnstead warm motes and gold streaks. |
| **WP7** | **Acting pass** (serial, single owner of `content/scripts.ts`) | none | After WP0's ops land, add face, emote, hop and move beats to existing key scenes (the Gleam relights, Wren's battles, Fenn's ceremony, `dusk_begins`, the Còr finale and the S4/S5 set-pieces) to a budget of at least one per four lines. **No new lines and no length**, so pre-Chickenpig scenes are eligible. |

**Per-package done-definition.**

- `node tools/maps/add_world_craft.py --region <r>` is idempotent.
- `audit_flow`, `audit_warps`, `audit_region` and `audit_spatial` pass.
- `render_walkable --report-only` shows no new orphan or softlock.
- `render_map` re-renders are committed for touched maps.
- `npm run typecheck` passes.
- `progression.mjs` still passes, if any wick was requested.
- The pre-Chickenpig invariants are checked for WP2: identical walkable set, triggers,
  trainers, encounter tables and rates (diff the JSON minus `ambience`/ambient NPCs
  against HEAD).

**Integration order.**

1. WP0 + WP1, in parallel.
2. The pilot (Dimglass I, inside WP2), then playtest.
3. WP2–WP6 in parallel.
4. WP7.
5. Integrator: shared registries, version bump, and README/CLAUDE.md lines.

---

## 7. Notes and caveats

- **Over-counts.** NPC counts include flag-swap pairs, so the true number on screen at
  any moment is lower. That makes the thin legs *thinner* than shown.
- **"Cross" assumes every Gift is held.** Early-visit walks can be longer through gated
  detours.
- **Caves roll encounters rect-wide** (encT 0 is correct for Cinderhead).
- **Render dates.** Renders in `docs/maps/renders/` may predate the latest surgical
  additions (for example the peril craters), so the visual verdicts are about layout
  and density, not individual props.
- **Asset budget.** The tileset is frozen at 386 tiles, so every animated or ambient
  element above is an overlay, object, code-drawn shape or effect sheet, never new
  overworld tiles.
