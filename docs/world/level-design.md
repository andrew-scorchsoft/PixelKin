# PixelKin — Level-Design Guide (binding)

> The **map & level-design rulebook** for Vesperholm. When we generate tilesets and
> assemble maps from them, the level design must be *deliberately good*, not ad hoc.
> This is the doc you read before authoring any new area, and the checklist you run
> before calling an area done.
>
> Read alongside [`atlas.md`](./atlas.md) (what each area *is*), [`README.md`](./README.md)
> (the authoring flow + data model), the schema in
> [`../../src/game/data/world/types.ts`](../../src/game/data/world/types.ts), and the tone
> in [`../../VISION.md`](../../VISION.md) ("lanterns in the dark"). All content original.

This guide was settled by a design panel — three cartridge-era handheld creature-RPG
designers (the people who laid out cosy starter towns, tutorial routes, and readable
interiors on real hardware) plus a modern systems/UX designer. Each fork below records the
**debate**, then a **binding RECOMMENDATION**. The rest of the doc is the concrete toolkit.

---

## 0. The one constraint that governs everything: the 15×10 window

Internal resolution is **240×160**, tiles are **16×16**, so the camera shows exactly
**15 columns × 10 rows** at once. With the player centred, they see **~7 tiles** ahead and
**~5 tiles** to either side before the camera scrolls. Every rule below is downstream of
this. Design **screen-by-screen**: think in 15×10 "screenfuls", place a landmark or a
decision roughly every screen, and never hide a critical exit/NPC/sign more than one screen
beyond where the player first needs it.

Movement is **grid-based, 4-directional, tween-between-tiles**. No diagonal, no pixel-precise
or twitch layouts (it must play on a touch d-pad). The player sprite renders **between the
`deco` and `above` layers**.

---

## 1. The forks the panel settled

### Fork A — Map size: single-screen rooms vs larger scrolling areas

**Debate.** The GBC veterans wanted tight, legible spaces — a screen you can read at a
glance, the classic 1-screen room. The SNES/GBA veteran pushed for scrolling routes that
breathe and earn the "map keeps unfolding" feeling from VISION. The UX designer warned that
*too* large reads as empty filler on a 15×10 window, and that giant maps make camera bounds,
encounter tables, and warp reasoning hard to keep local.

**RECOMMENDATION — size by `MapKind`, never exceed the soft caps, compose big areas from
several maps.** Honour README's caps (overworld soft-cap 64×64, interior ~32×32, absolute
128×128) but tighten them to *design targets* per kind:

| `MapKind` | Target size (tiles) | Screens | Rule of thumb |
|-----------|---------------------|---------|---------------|
| `interior` (house, shop, boat) | **10×8 → 16×12** | ~1 | Single-screen or one short scroll. Door at the bottom edge. |
| `interior` (Lumenary, large shop) | **16×12 → 20×16** | 1–2 | One reveal of depth; arena/counter at the far end. |
| `town` | **24×20 → 32×28** | ~2×2–3×3 | Big enough for house + Lumenary + shop + verge + 2 exits, small enough to cross in under a minute. |
| `route` | **20×30 → 32×48** (one long axis) | 2–4 long | Linear with a dominant travel axis; one screen ≈ one "beat". Split into segments (`_i`/`_ii`) before it sprawls. |
| `cave` | **24×24 → 40×40** | 2–4 | Branchy not linear; rooms joined by 1–2-tile chokes. |
| `hub` | **20×20 → 28×28** | ~2×2 | A central signpost readable from spawn; spokes radiate to the edges. |

**A map should never need more than ~9 screens (3×3) of scrolling.** Past that, segment it
and connect through the world graph — exactly what `dimglass_coast_i`/`_ii` already does.

> **Status:** `tinderwick.json` has been **rebuilt to this 28×24 target** on the shared
> `vesper_overworld_set` (`tools/maps/build_tinderwick.py`) — organic tree-line, lit spine,
> shop + Lumenary plaza, cottage, tall-grass verge, inland pond, sand beach + sea, scatter
> decor — and passes `validate_map`. `dimglass_coast.json` likewise rebuilt to §7.3
> (`build_dimglass.py`). The §7 sketches below are the design targets the builders realise.

### Fork B — Guidance & gating without cheap invisible walls

**Debate.** The veterans were united that **invisible walls feel cheap** and break the cosy
trust. The fork was *how hard* to gate: hard diegetic barriers (water, cliffs, fences) vs
soft funnelling (the eye led by light and landmarks). The UX designer argued for "soft first,
hard only at true boundaries," and for making every barrier *legible as a reason*, not a wall.

**RECOMMENDATION — gate with diegetic geography; funnel with light; reserve hard map-edge
collision for the literal edge.**

- **Every barrier must read as a thing**, not a force field: **water** (sea, tide-channels),
  **cliff faces** (a cliff *top* tile is walkable, the *face* below collides), **fences /
  low walls**, **dense tree lines**, **buildings**, **rocks/rubble**, **coldfog/penumbra**
  for the late dark. The player should always be able to *say why* they can't pass.
- **Funnel the eye with the world's own vocabulary — light.** Vesperholm runs on lanterns;
  use **lantern-buoys, lamp-posts, lit windows, glowmoss, candle-glow** as breadcrumbs
  toward the next objective. A lit path in the dark is the most on-theme guidance there is.
- **Use the `above` layer for honest depth.** Tree canopies, roof eaves, archways, and
  bridge tops render *over* the player so they visibly walk *under* them — this both signals
  "you can go here" and hides nothing the player needs to navigate.
- **Path-funnelling beats walls.** Make the intended route the **widest, lit, paved** lane;
  let scenery taper side-options to dead-ends with a small reward or a clear "later" tease.
- **Future-gated areas are teased, never invisibly blocked** — see Fork D.
- **Hard collision is for:** building/cliff/water bodies, scenery, and a **1-tile solid
  border** at every map edge that isn't a warp, so the camera never shows the void.

### Fork C — The cozy-town starter layout pattern

**Debate.** Everyone agreed the opening hour must teach **move → talk → read a sign → enter
a building → first wild encounter** as a gentle ramp. The fork: free-roam sandbox town vs a
lightly-guided "spine". The UX designer won the room: a soft spine (the player can wander,
but the natural read leads them through the lessons in order) respects both nostalgia and
the "no tutorial pop-ups" cosy feel.

**RECOMMENDATION — the "lantern spine" starter layout** (realised in the §7 Tinderwick
sketch). Anchor placement, from spawn outward:

1. **Spawn at/near the player's house** (south end). The very first action is stepping out
   the door — movement taught by doing.
2. **Mentor stands on the only natural path** a few tiles north, beside a **sign** — the
   player can't help but reach them; talking is taught, the sign teaches "interact", and the
   mentor cutscene grants vesperlamp + starter (`flag:has_vesperlamp`, `flag:has_starter`).
3. **The Lumenary sits central and tallest** — the visual landmark of the town, readable
   from spawn, so the player's eye has a goal even before they can win it. (Lumenary 1 is
   gentle/optional-timing; its door can require `flag:has_starter`.)
4. **Shop/sign furniture** lines the main square so reading signs and entering a second
   building are available but not forced.
5. **The town's single tall-grass verge** sits *next to the exit*, so the first wild
   encounter happens naturally **as the player leaves** — the genre's classic "first step
   into the grass". Keep it small and low-rate (Fork F).
6. **Two exits, clearly ranked:** the **forward route** (north, lit, obvious) and a
   **return spoke** (the Lanternway to the hub) introduced later. The forward exit is the
   widest, most-lit lane.

Teaching ramp, in order, all without a single pop-up tutorial: *leave house (move) → meet
mentor (talk + cutscene) → read dock sign (interact) → optionally enter shop/Lumenary
(door warp) → step into the verge on the way out (first encounter).*

### Fork D — Tutorial route design (Dimglass Coast) & teasing locked gifts

**Debate.** How dense should the first route's encounters be? The veterans warned that a wall
of grass on Route 1 annoys; the UX designer wanted **safe pockets** alternating with grass so
the player chooses to engage. On locked content, all agreed: a gate the player *can see past*
is a promise they'll remember; an invisible block is forgotten.

**RECOMMENDATION — pace the first route as alternating beats; tease every locked spur.**

- **Alternating safe/grass beats.** A route reads as a sequence of ~1-screen beats: a
  **safe paved/sand strip** (rest, NPC, sign), then a **grass patch** (encounter), then safe,
  then grass. Never force the player through grass with no safe lane on the first route.
- **Always leave a safe path through.** On Dimglass there must be a walkable shore/path lane
  that *skirts* the grass, so a player low on health can pass. Funnel, don't trap.
- **First encounters are gentle** (Fork F): low rate, low levels, 1–2 common kin.
- **Tease the gated spurs you'll return for.** Dimglass shows, but does not yet open:
  - **Tidecall water** — visible shallows/lantern-buoys leading to **Gullcry Rock**; the
    tiles `requires_ability: 'tidecall'` (solid until earned). The player *sees* the buoys
    glow offshore and remembers.
  - **Glimmerstep cavern** — a dark **Tideglass Cavern** mouth in the cliff, framed and lit
    at the edges but too dark to enter; its warp `requires_ability: 'glimmerstep'`.
  - Each tease gets a **sign or NPC line** ("the buoys only answer a lit lamp…") so the
    *why* and the *come-back* are explicit, cosy, and diegetic.
- **One landmark sight-line per route.** Frame the next town or a notable structure on the
  horizon (within the `above`/scenery band) so travel has a visible destination.

### Fork E — Encounter-zone design & readability

**Debate.** Should grass be one big field or scattered tufts? The veterans liked **shaped
patches** (a player can choose to step in); the modern designer stressed the patch must
**read visually** as "this is wild terrain" and never be confused with decorative grass.

**RECOMMENDATION — shaped, readable, optional-to-enter encounter patches.**

- **Encounter terrain is a distinct tile** (`encounter_terrain` on the tileset) and must be
  **visually unmistakable** vs decorative ground grass — taller, with a darker base or a
  distinct animation cue. If the player can't tell grass-you-fight-in from grass-you-walk-on,
  the tileset is wrong (feed that back to the art workstream).
- **Patches are shaped and bordered**, 2–4 tiles deep, with a clear edge — the player decides
  to enter. Avoid 1-tile-wide grass corridors the player is forced down.
- **`EncounterZone.rect` must cover exactly the painted terrain** — no zone over plain
  ground, no terrain tiles outside a zone. Mismatch = invisible or phantom encounters.
- **Rate tuning (per-step `encounter_rate`):**

  | Context | `encounter_rate` |
  |---------|------------------|
  | Starter-town verge (first ever grass) | **0.06–0.08** |
  | First route (Dimglass) | **0.08–0.10** |
  | Standard mid-game route | 0.10–0.12 |
  | Cave / dungeon | 0.10–0.14 (denser, claustrophobic) |
  | Gift-gated rare-reward terrain (water/cave spur) | 0.06–0.10, rare kin at **low weight** |

  Keep the first hour at the **low end** — a battle every ~10–14 steps reads as "alive", not
  "nagging". A player crossing the first verge should average **1–2 encounters**, not five.
- **Tables:** first-route tables are **1–2 common kin**, narrow level range (see atlas per-area
  kin). Rare/gated kin are **low-weight entries** in the gated-terrain zone, never the common
  pool. Element matches the area's light (atlas §4).

### Fork F — Minimum tile vocabulary a good map needs

**Debate.** The panel noted that most ad-hoc-looking retro maps fail for a tooling reason:
the tileset lacks the **corner/edge** pieces, so authors paint blobby, ambiguous shapes.
Good level design is impossible without a good tile *kit*.

**RECOMMENDATION — this is the minimum tile vocabulary every area tileset must provide for
its terrain types.** (This *informs* the art workstream; we do not edit tilesets here.) For
any surface that has an inside and an outside, you need the **9-slice** (centre + 4 edges +
4 outer corners) **and** the **4 inner corners** — 13 pieces — or maps look blocky.

- **Ground/path:** fill + a 9-slice transition to the neighbouring ground (grass↔path,
  path↔sand), so paths curve instead of stair-stepping.
- **Water:** deep-water fill (collides by default), **shore/edge 9-slice** (water↔land),
  optional **foam/highlight** edge, and **shallow/tide tiles** flagged
  `requires_ability: 'tidecall'`.
- **Cliffs:** a **cliff-top** edge (walkable above) **distinct from the cliff-face** (the
  vertical wall below, collides) — including the L/R corner faces — so height reads honestly.
- **Buildings:** front wall, **roof** (an `above` piece), and at least one **door tile**
  (the warp target), plus a window/lit-window variant for cosy glow.
- **Tree/foliage:** trunk/base (`deco`, collides) + **canopy** (`above`, player walks under),
  and a tree-line edge so forests have a believable border.
- **Encounter terrain:** the unmistakable **tall-grass** tile (and `water`/`cave`/`sand`
  variants per area), visibly distinct from decorative grass.
- **Fences / low walls / signs / lamp-posts / lantern-buoys:** the funnelling + breadcrumb
  kit — small `deco` props that read as soft barriers and as light-guidance.
- **Interior kit:** the dedicated `interior_set` (faced wall 9-slice with visible
  height, patterned floor, doormat/exit, window) + furniture as `interior_*` objects.
  Interiors follow the SNES-enclosure convention — **see `docs/world/interiors.md`
  (binding)**; don't author an interior as a flat plan on the overworld tileset.
- **Caves:** floor, **wall-edge 9-slice**, rubble/rock blockers, and the **dark-cave tile**
  flagged `requires_ability: 'glimmerstep'`.

If a layout in this doc calls for a piece the tileset doesn't have, that's a tileset gap to
raise — not a reason to paint a worse map.

### Fork G — Layer discipline

**Debate.** Brief but decisive: maintainability dies when authors paint collision into the
art or scatter objects across the wrong layer.

**RECOMMENDATION — strict layer roles (matches README's stacking).**

| Layer | Put here | Never put here |
|-------|----------|----------------|
| `base` | Walkable/visible **ground**: grass, paths, water, sand, floors. One gid per cell, no holes (0) in walkable areas. | Anything the player walks *over* or *under*; props. |
| `deco`, `deco_2`… | Ground-level props & the **lower halves** of tall things: flowers, signs, fences, lamp-posts, tree trunks, building fronts, furniture. | Roof/canopy tops; ground fill. |
| *(player)* | — engine slots the player/NPCs here — | — |
| `above` | Only what the player walks **under**: tree **canopies**, **roofs**, bridge tops, archway tops, overhanging eaves. | Anything the player should collide with or stand on. |

- **Collision/gating/encounter are tile *properties*, not layers** (set on the tileset
  metadata: `collides`, `requires_ability`, `encounter_terrain`). Do **not** author a hand-
  painted `collision` layer per map — the role exists in the schema for tooling, but normal
  maps gate via tile properties + `gates`/`encounters`/`warps`. This keeps gating authored
  once per tileset and reused everywhere.
- **`depth` convention:** `base` 0, `deco` 5 (`deco_2` 6…), `above` 20 — leave headroom so
  the player depth (~10) always sits between deco and above.
- **A tall object is two pieces:** base on `deco` (collides), top on `above` (walk-under).
  A tree the player can stand behind *and* in front of is the single clearest readability win
  the layer system gives you — use it.

---

## 2. Per-`MapKind` size guidance (quick reference)

(Full reasoning in Fork A.)

- **interior:** 10×8–16×12 (Lumenary up to 20×16). Door on the **bottom edge**, exit warp
  there. One screen, maybe one scroll.
- **town:** 24×20–32×28. House + Lumenary + shop + verge + 2 exits, crossable in <1 min.
- **route:** 20×30–32×48 on the long axis; **segment before it sprawls past ~3×3 screens**.
- **cave:** 24×24–40×40, branchy, chokepoint rooms.
- **hub:** 20×20–28×28, central signpost readable from spawn.
- **Absolute cap 128×128**; anything bigger is multiple maps via the world graph.

---

## 3. The readability & guidance toolkit (reusable techniques)

- **Lead with light.** Lamp-posts, lit windows, lantern-buoys, glowmoss → breadcrumbs to the
  next objective. On-theme and never feels like a tutorial arrow.
- **Landmark per screen.** Each ~15×10 screenful gets one thing the eye locks onto (the
  Lumenary, a lighthouse, a big tree, a signpost) so the player always orients.
- **Widest-lit-paved = the way forward.** Rank routes by lane width + lighting + paving.
- **Diegetic barriers only** (water/cliff/fence/trees/buildings/fog) — every wall has a why.
- **`above`-layer depth** to show walk-under space and frame sight-lines.
- **Tease, don't block.** Gated content is visible and signed, gated by `requires_ability`
  tiles/warps, with a sign/NPC explaining the *why* and the *come back*.
- **Sight-line a destination.** Frame the next town/structure on the horizon band.
- **Solid 1-tile map border** on non-warp edges so the camera never reveals void.
- **Funnel, never trap.** Always a safe lane past grass on early maps.

---

## 4. Starter-town pattern (the "lantern spine")

See Fork C for the rules; §7.1 for the annotated Tinderwick sketch realising them. The
ordered anchors: **house/spawn (S) → mentor + sign on the path → central tall Lumenary →
shop/sign furniture → verge by the exit → forward route exit (+ later: hub spoke).**

## 5. Tutorial-route pattern (Dimglass Coast)

See Fork D; §7.3 for the sketch. **Alternating safe/grass beats, a safe lane through, gentle
first encounters, a Tidecall water tease (buoys → Gullcry Rock) and a Glimmerstep cavern
tease (dark cave mouth → Tideglass Cavern), each signed, and a sight-line to Pearlmoor.**

## 6. Encounter-design rules (summary)

See Fork E. **Distinct readable grass tile; shaped 2–4-deep patches with a safe lane;
`EncounterZone.rect` matches the painted terrain exactly; rate 0.06–0.10 in the first hour;
1–2 common kin early, rare kin as low-weight entries in gift-gated terrain; element matches
the area's light.**

---

## 7. Annotated layout sketches

These are **design targets for the JSON-authoring workstream**, faithful to the
`MapDefinition` schema. Symbols are *roles*, not literal gids — the author maps each role to
the real tile gid from the area's packed tileset. Origin `(0,0)` is **top-left**; coords are
`(tx, ty)`. Each sketch lists where **warps / triggers / NPCs / encounters / gates** go.

### Legend (shared)

```
.  walkable ground (base: grass/path/floor)     ~  deep water (base; collides)
,  path / paved lane (base; the lit "spine")    s  shallow/tide water (base; requires_ability tidecall)
"  TALL GRASS — encounter terrain (base)        =  sand / shore (base, walkable)
T  tree: trunk base (deco, collides)            ^  cliff FACE (deco/base; collides)
t  tree canopy over walkable (above)            v  cliff TOP edge (base; walkable)
H  house / building front wall (deco, collides) #  generic solid (wall/rock/fence)
R  roof (above; player walks behind/under)      |  fence / low wall (deco; collides)
D  door tile  -> a Warp                          L  lamp-post / lantern-buoy (deco; light breadcrumb)
N  NPC placement                                 G  sign (EventTrigger kind:'sign')
M  mentor NPC (cutscene trigger nearby)          C  dark CAVE mouth (warp; requires_ability glimmerstep)
S  player spawn / warp-in tile                   B  Lumenary (big building; door = D)
W  shop/PokéCenter-equivalent building          *  scenic / clutter (deco)
```

> Border convention: the outermost ring is solid scenery (trees/cliff/water/fence) except
> where a `D`/`S`/edge-warp breaks it. Roofs (`R`) sit on `above`; their building fronts
> (`H`,`B`,`W`) and doors (`D`) sit on `deco`/`base` below.

---

### 7.1 Tinderwick — starter town  (`kind: town`, **28×24**)

Cosy coastal village at the blue hour: `bone`-cream cottages, candle-`fire` windows,
`deepBlue` sea to the **south**, the route exit **north**. Spawn lower-mid (graph
`start_at` ≈ `{tx:8,ty:12}`-class, here normalised to the player's house). Mentor on the
path; Lumenary central & tall; verge by the north exit; sea (Tidecall-teased) to the south.

```
        col: 0         1         2 (tens)
             0123456789012345678901234567
   row 0   : TTTTTTTTTTTTT,,,TTTTTTTTTTTT   <- north EDGE-WARP to Dimglass at (13-15,0)
       1   : Ttttttttttttt,,,ttttttttttttT
       2   : T...........""""""..........T   verge straddles the exit lane
       3   : T....L.......""""""....L.....T
       4   : T...,,,,,,,,,,,,,,,,,,,,,....T   the lit "spine" runs N-S
       5   : T...,..RRRR.......RRRR..,....T
       6   : T...,..RRRR.......RRRR..,....T
       7   : T...,..HHWH.......HBBH..,....T   left: shop(W); right: Lumenary(B)
       8   : T...,..H.DH.......HB DH.,....T   shop door (8,8); Lumenary door (18,8)
       9   : T.G.,......G.........G..,.G..T   signs scattered for "interact" practice
      10   : T...,,,,,,,,,,,,,,,,,,,,,....T
      11   : T...,......M........L...,....T   M = mentor on the spine (cutscene tile nearby)
      12   : T...,......G............,....T   sign by mentor; intro cutscene fires here
      13   : T...,..RRRR............,.....T
      14   : T...,..RRRR....N.......,.....T   N = rival-friend / child NPC (wander)
      15   : T...,..H.DH............,.....T   player's HOUSE; door D at (8,15)
      16   : T...,..HHHH....S.......,.....T   S = spawn (16,16) just N of the house exit
      17   : T...,,,,,,,,,,,,,,,,,,,,,....T
      18   : T...........L........L.......T
      19   : T==========================T    shore/sand band
      20   : T===L==================L====T    lantern-buoys along the waterline
      21   : ~~~~~~~~~~ssssss~~~~~~~~~~~~~    shallows (s) = Tidecall tease
      22   : ~~~~~~~~~~ssssss~~~~~~~~~~~~~
      23   : ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    deep sea (collides), framed border
```

**Wiring:**
- **Warps:** `to_coast` — edge-warp, `step_on` tiles **(13–15, 0)** → `dimglass_coast_i`
  (land near its south edge), `facing:'up'`, `fade`. `to_house` — `interact` at door
  **(8,15)** → `tinderwick_house` `(landing tile near its door)`, `door`. `to_shop` —
  `interact` at **(8,8)**. `to_lumenary` — `interact` at **(18,8)** → `tinderwick_lumenary`
  (optionally `requires_flag:'flag:has_starter'`). *(Later: `to_crossroads` Lanternway spoke
  — add a west or north secondary exit when the hub is built.)*
- **Triggers:** `intro_mentor` — `cutscene`, `step_on` **(11,11)** beside the mentor,
  `once:true`, `sets_flags:['flag:has_vesperlamp','flag:has_starter']`. Signs (`kind:'sign'`,
  `interact`): dock/shore sign **(9,19)** area, square signs at **(2,9)/(11,9)/(20,9)** and a
  mentor sign **(10,12)** — these are the "press to read" lessons.
- **NPCs:** `mentor` at **(10,11)** `static`, `dialogue_ref:'npc.mentor_intro'`. `child_runner`
  / rival-friend at **(14,14)** `wander`. Keep NPC paths off the spine's choke tiles.
- **Encounters:** `verge_grass` `tall_grass`, `rect{tx:13,ty:2,w:6,h:2}` (the `"` band),
  `encounter_rate:0.07`, table = Wickmoth/Tallowpup (atlas kin), lv 2–4.
- **Gates / `shallows`:** the `s` shallows are a **Tidecall tease** — leave them gated; the
  data is a `water` `EncounterZone` `requires_ability:'tidecall'` + an `AbilityGate`
  (`tidecall`, `make_passable`) over the `s` tiles, but the *town* doesn't need to reward
  them — the real Tidecall water content lives on Dimglass. A shore sign explains the buoys.

### 7.2 Tinderwick house — interior  (`kind: interior`, **12×9**)

Single-screen cosy cottage. Exit door at the **bottom edge** (back to the town door tile).
Warm, a few props, the rival-friend or a parent NPC optional.

```
        col: 0         1
             012345678901
   row 0   : ############     # = interior wall (collides)
       1   : #..........#
       2   : #.BB....SS..#     BB = bed (deco, collides) ; SS = shelf (deco, collides)
       3   : #.BB....SS..#
       4   : #..........#
       5   : #...TT.....#     TT = table (deco, collides)
       6   : #...TT..N..#     N = parent / rival NPC (static)
       7   : #..........#
       8   : #####DD#####     DD = exit door (warp) at (4-5,8)
```

**Wiring:**
- **Warps:** `to_town` — `step_on` (or `interact`) at door **(4,8)/(5,8)** → `tinderwick`
  landing on the tile just **outside** the house door (≈ `(8,16)`), `facing:'down'`, `door`.
  *The town's `to_house.to` and this `to_town.at` must be a consistent pair.*
- **Triggers:** optional sign on a shelf (`interact`, **(9,2)**) for flavour; an optional
  one-time cutscene (`once:true`) if the opening narration starts indoors.
- **NPCs:** optional `npc.house_parent` / rival at **(8,6)** `static`.
- **Encounters / Gates:** none (interiors are safe).
- **Note:** interior `base` is floor (no 0-holes in walkable cells); furniture is `deco` and
  collides via tile property; no `above` layer needed unless a low rafter/loft overhangs.

### 7.3 Dimglass Coast (segment I) — first route  (`kind: route`, **18×34**, vertical)

Tidal cliffside route, travelled **south→north** (enter from Tinderwick at the **south edge**,
exit toward `dimglass_coast_ii`/Pearlmoor at the **north edge**). Cliff wall to the **west**,
sea to the **east**. Alternating **safe sand strip ↔ grass patch** beats; a safe lane the
whole way; a **Tidecall water tease** (buoys → Gullcry Rock) and a **Glimmerstep cavern**
tease (dark mouth in the cliff → Tideglass Cavern), each signed; Pearlmoor sight-lined north.

```
        col: 0         1
             012345678901234567
   row 0   : ^^^^^^,,,^^^^^^^^^^   north EDGE-WARP to dimglass_coast_ii at (6-8,0)
       1   : ^vvvv,,,,vvvvvv###
       2   : ^v..L.,,,.....L.v#     L = lamp/buoy breadcrumbs up the lit lane
       3   : ^v....,,,.......v#
       4   : ^v.""""..,,,...sv#     grass patch (left) + safe lane + tide tease (s) east
       5   : ^v.""""..,,,..ssv~    s s s = shallows -> Gullcry Rock (Tidecall)
       6   : ^v.""""..,,,...sv~     a buoy line leads offshore (visible, gated)
       7   : ^vG.....,,,....Gv#     G = signs: "buoys answer a lit lamp" / shore note
       8   : ^v......,,,.....v#
       9   : ^vCC....,,,.....v#     CC = dark CAVE mouth -> Tideglass Cavern (Glimmerstep)
      10   : ^vCC..N.,,,.....v#     N = travelling NPC (advice / heals flavour)
      11   : ^v......,,,.....v#
      12   : ^v...""""...,,..v#     grass patch shifts to the right side (variety)
      13   : ^v...""""...,,..v#
      14   : ^v...""""...,,..v#
      15   : ^v.G........,,..v#     sign: reminder of the route ahead
      16   : ^v.........,,,..v#
      17   : ^v....""""..,,..v#     a third gentle grass beat
      18   : ^v....""""..,,..v#
      19   : ^v.........,,,..v#
      20   : ^v...L.....,,L..v#     more buoy/lamp breadcrumbs
      21   : ^v.........,,,..v#
      22   : ^v....""""..,,..v#
      23   : ^v....""""..,,..v#
      24   : ^v.........,,,..v#
      25   : ^v.........,,,..v#
      26   : ^v.......===,,..v#     sand widens (safe rest pocket before the gate-boundary)
      27   : ^v......====,,..v#
      28   : ^vG.....====,,..v#     sign: Pearlmoor / segment boundary ahead
      29   : ^v......===,,,..v#
      30   : ^v.........,,,..v#
      31   : ^vvvvv,,,,vvvvv.v#
      32   : ^^^^^,,,,,^^^^^^^^   (south entry band)
      33   : ^^^^^=S=S=^^^^^^^^   south EDGE-WARP from Tinderwick; S = land-in tiles
```

**Wiring:**
- **Warps:** south edge `from_tinderwick` — land-in at **(5–7,33)** (paired with Tinderwick's
  `to_coast.to`), `facing:'up'`. North edge `to_coast_ii` — `step_on` **(6–8,0)** →
  `dimglass_coast_ii`, `facing:'up'`, `fade`. Spur warps (gated, the teases):
  `to_gullcry` at the buoy tile **(15,5)** `requires_ability:'tidecall'` → `gullcry_rock`;
  `to_tideglass` at the cave mouth **(2,9)** `requires_ability:'glimmerstep'` → `tideglass_cavern`.
- **Triggers (signs):** buoy sign **(2,7)** `sign.dimglass_buoys` ("the buoys only answer a
  lit lamp"); shore sign **(14,7)**; route sign **(3,15)**; boundary sign **(2,28)**
  `sign.dimglass_to_pearlmoor`. All `kind:'sign'`, `interact`.
- **NPCs:** a travelling Wayfarer at **(5,10)** `look_around`, `dialogue_ref` giving cosy
  route advice (teases the gifts in-character). Optionally a `patrol` NPC on the sand strip.
- **Encounters:** `EncounterZone`s matching each `"` patch exactly —
  `grass_a rect{3,4,4,3}`, `grass_b rect{5,12,4,3}`, `grass_c rect{6,17,4,2}`,
  `grass_d rect{6,22,4,2}` — all `tall_grass`, `encounter_rate:0.09`, table = Brinelet/Lumpin
  (atlas kin), lv 3–5. Plus a gated water zone `tide_shallows rect{14,4,2,3}` `water`,
  `requires_ability:'tidecall'`, low-weight rare Tide kin (the spur reward read).
- **Gates:** `AbilityGate` `tidecall`/`make_passable` over the `s` shallows tiles
  **(14–15,4–6)** so the buoy path becomes crossable once Tidecall is earned; the
  `glimmerstep` cave-mouth gating rides on the warp's `requires_ability` (no tile-clear needed).
- **Pacing check:** the lit `,` spine is continuous top-to-bottom — a player can **always**
  walk the route without entering a single grass tile (Fork D's "safe lane through").

---

## 8. Map-authoring checklist (every new area must pass)

### Pre-flight (before painting)

- [ ] **Atlas entry exists** — kind, region, gate, graphics, music brief, kin, terrain
      ([`atlas.md`](./atlas.md)).
- [ ] **Size chosen by `MapKind`** within §2 caps; segment if it would exceed ~3×3 screens.
- [ ] **Tileset provides the vocabulary** this layout needs (Fork F 9-slice/corners,
      cliff-top vs face, doors, water edges, distinct grass, fences/signs/lamps). Gaps raised
      to the art workstream — don't paint around a missing kit.
- [ ] **Entry/exit tiles agreed** with neighbouring maps & the **world graph** (`graph.ts`):
      every `Warp.to`/`to_map` has a matching land-in on the target; `start_at`/edge tiles in
      bounds.
- [ ] **Screen-by-screen plan**: a landmark + a decision roughly per 15×10 screen; the
      "spine" / dominant axis identified.

### Layout & readability

- [ ] **Spawn/first action** is clear (starter: step out of the house).
- [ ] **Lit, paved, widest = the way forward**; side-paths taper to dead-ends/rewards.
- [ ] **Every barrier is diegetic** (water/cliff/fence/tree/building/fog) — no invisible walls.
- [ ] **Solid 1-tile border** on all non-warp edges; camera never shows void.
- [ ] **Landmark sight-line** frames the next destination.
- [ ] **Gated content is teased, visible, and signed**, gated via `requires_ability`
      tiles/warps with a sign/NPC stating the *why* + *come back*.

### Layers & data

- [ ] **Layer discipline** (Fork G): `base` ground only; `deco` props + tall-thing bases;
      `above` only walk-under tops; depths 0/5/20 with player between.
- [ ] **Collision/gating/encounter via tile properties** (not a hand-painted collision
      layer); `gates`/`warps` carry the ability requirements.
- [ ] **`EncounterZone.rect` matches painted terrain exactly**; first-hour `encounter_rate`
      0.06–0.10; tables element-matched, 1–2 common kin early, rare kin low-weight in gated
      terrain.
- [ ] **Tall objects split** base(`deco`)/top(`above`).
- [ ] **`music` key set** to the area's rendered loop.
- [ ] **Flags consistent** — `requires_flag`/`sets_flags`/`once` match `graph.ts` and the
      progression (e.g. `flag:has_starter`, `crown_*`).

### Post-flight (before "done")

- [ ] **Walk it mentally screen-by-screen**: can you reach every exit, NPC, sign, item?
- [ ] **Safe lane through grass** exists on early maps; player can't be trapped.
- [ ] **No 1-wide forced grass corridors**; patches are 2–4 deep with a clear edge.
- [ ] **Warp round-trips** are consistent both ways (A→B land tile is just outside B→A).
- [ ] **Reward/tease cadence** matches the route conventions ([`atlas.md`](./atlas.md) §3:
      segmented chain, a spur, a landmark, a hub spoke).
- [ ] **Originality** ([`../../VISION.md`](../../VISION.md)): no layout, silhouette, or sign
      text evokes another franchise; canon vocabulary used (kin, Lumenary, Gleam, Lantern
      Gift, vesperlamp).
- [ ] **Validates & loads** once the runtime `MapLoader` exists; gids in range, layer lengths
      = width×height.

---

## 9. Should we build a `design-map` skill? — YES (scaffold below)

**Recommendation.** Map authoring repeats for **~30 areas** (14 area cards + segments, spurs,
landmarks, hubs, interiors in the world graph), and it's a multi-step, easy-to-do-
inconsistently activity (size, layers, warps↔graph, encounter rects, the readability
checklist). By the project's own principle — *"if an activity will repeat, invest in a
skill"* — this clears the bar comfortably. A skill turns this binding doc into an enforced,
repeatable pipeline and keeps every area on-pattern.

It should **assemble maps from already-generated tilesets** (it does not draw art — that's
`generate-sprite-sheet`), output `MapDefinition` JSON to the schema, and run the §8 checklist
as a lint pass. Scaffold (outline only — not built here):

```
.claude/skills/design-map/
  SKILL.md
  references/
    level-design.md        # symlink/pointer to docs/world/level-design.md (the rules)
    schema-cheatsheet.md   # the MapDefinition fields + snake_case JSON crib
  scripts/
    new_map.py             # scaffold a sized, bordered blank MapDefinition for a MapKind
    lint_map.py            # run the §8 checklist programmatically (sizes, layer lengths,
                           #   gid range, zone-vs-terrain match, warp round-trips vs graph)
    ascii_to_layers.py     # convert an annotated ASCII sketch (this doc's legend) -> gid layers
```

### `SKILL.md` outline (to fill in when built)

```markdown
---
name: design-map
description: Assemble a PixelKin MapDefinition (town/route/interior/cave/hub) from an
  already-generated tileset, following docs/world/level-design.md — sized by MapKind,
  layer-disciplined, warps wired to the world graph, encounter zones tuned, and linted
  against the authoring checklist. Composes maps; does NOT draw tiles (use
  generate-sprite-sheet) and does NOT touch engine code.
---

# design-map

## When to use
- Authoring or revising any map JSON in public/assets/maps/ for an atlas area.

## Read first (the craft)
- docs/world/level-design.md   (this guide — the binding rules & sketches)
- docs/world/atlas.md          (the area's kind/region/gate/kin/terrain)
- src/game/data/world/types.ts (the MapDefinition schema)
- src/game/data/world/graph.ts (the edges/warps this map must satisfy)

## Workflow
1. Confirm the atlas entry + the packed tileset exist (don't author without the kit).
2. Choose size by MapKind (level-design §2); scaffold a bordered blank (new_map.py).
3. Lay the spine/landmarks screen-by-screen (level-design §3, §7 patterns).
4. Paint base -> deco -> above with strict layer roles (§7 Fork G).
5. Place warps (matched to graph.ts), triggers, npcs, encounter zones, gates.
6. Tune encounter_rate + tables to the area (§6) and the first-hour ramp.
7. Run lint_map.py (the §8 checklist) and fix every failure.
8. Register in maps.ts + graph.ts; key the music; add dialogue refs.

## Guardrails
- Composes maps only; never edits assets/tilesets or src/game engine code.
- Diegetic barriers only; tease gated content; safe lane on early routes.
- Canon vocabulary (kin/Lumenary/Gleam/Lantern Gift/vesperlamp); originality per VISION.
```

---

## 10. The meshing standard — a tileset problem AND a map-design problem

The single biggest gap between our early maps and a polished handheld map is
**meshing**: in good maps *nothing sits in an isolated square*. Water wraps in a
continuous shoreline, grass/sand/path blend with soft transitions, cliffs have
lit tops over shadowed faces with corners, and forests are contiguous masses with
a clean border. This is **two problems that must be solved together** — fixing one
without the other still looks wrong:

**A) The tileset must PROVIDE the vocabulary** (art workstream — `generate-sprite-sheet`).
For every surface with an inside and an outside, the kit needs the **9-slice**
(fill + 4 edges + 4 outer corners) and ideally the **4 inner corners** (13-piece),
tagged with `terrain` + `autotile` role in the tileset manifest (Fork F). Without
this, *no amount of careful authoring can mesh* — `validate_map.py` reports
`autotile-vocab: FAIL`.

*Proven production recipe (it works — see the autotiled lake test):* describe the
9 pieces **cell by cell** to the image model as a 3×3 `tile-sheet`, then slice with
`slice_tileset.py --layout edges9 --terrain <name>`:

> "(1) water with foam shore on TOP+LEFT; (2) shore on TOP; (3) TOP+RIGHT; (4) LEFT;
> (5) plain fill; (6) RIGHT; (7) BOTTOM+LEFT; (8) BOTTOM; (9) BOTTOM+RIGHT"

Per area, the kit needs autotile sets for: **ground/grass**, **tall-grass**
(encounter, visibly distinct), **sand/dirt**, **water** (shoreline), and the
hardest — **cliffs/ledges** (a *vertical* set: walkable lit **top** edge distinct
from the colliding **face**, plus L/R + inner corners, and the hop-down ledge),
plus contiguous **tree-mass** edges and multi-tile **buildings**.

**B) The map must USE it** (this workstream). Author terrain as **regions, not
hand-placed corner gids**: paint a `terrain` layer (a 0/1 presence grid tagged
`terrain` + `set`) per material, then expand it so the blob rule stamps the right
edge/corner tile automatically:

```bash
node tools/autotile/expand.mjs public/assets/maps/<map>.json   # terrain layer -> meshed base gids
```

Then layer decoration (`deco`) and walk-under tops (`above`) per Fork G, shape
encounter patches (Fork E), and lead with light (§3).

**C) Validate both halves — the gate before "done":**

```bash
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/render_map.py  <map> --output /tmp/x.png --scale 4   # SEE it
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/validate_map.py <map>                                  # MEASURE it
```

`validate_map.py` checks layer discipline, **autotile vocabulary** (tileset half),
**meshing %** at terrain boundaries, water shorelines, decoration density, tree
depth, and the solid border (map half) — and fails the build if a map is below
standard. A map is not done until it renders to the bar **and** passes the
validator with no FAILs.

---

## 11. The composition standard (closing the gap to the genre's best maps)

A map can pass every mechanical check and still read as *empty* next to a classic
handheld route. Side-by-side comparison against reference-era maps shows the gap is
**composition**, and it reduces to seven enforceable rules. These were applied to
Tinderwick / Dimglass I+II / Pearlmoor in the 2026-06 rebuild; hold every new area
to them (the §8 checklist now includes this section by reference).

1. **No flat voids.** Every walkable screenful carries texture: ground fills are the
   *textured* grass variants (`grass1-3` carry blade texture; `grass0` is the plain
   anchor), `scatter_decor` density **0.14–0.16** (not 0.10), and any open meadow
   larger than ~5×4 gets a prop cluster (flowerbeds, boulder, tuft) or a reason to
   exist. The reference maps are ~70% "occupied"; ours were ~20%.
2. **Deep organic enclosure.** Borders are 2–3 deep with `organic_border` bumps of
   radius ≥2 (radius-1 bumps make plus-shaped pockets), and the camera margin is
   always forest/cliff/sea — never void. Object trees with real crowns are scattered
   ON the tree-line (3–6 per map) so the forest reads as overlapping canopies, not a
   repeating hedge tile.
3. **One elevation accent per outdoor map.** A cliff terrace, bluff or rock shelf
   (the `cliff` family's wall edges carry the lit-rim → face → contact-seam ladder)
   so the map has height, like the reference maps' terraces. Towns: behind the
   landmark building. Routes: the flanking wall itself, bulging organically.
4. **Organic shapes, not ruled rects.** Shores, encounter patches and terraces are
   `blob()`s (or rects with bitten corners). The tide *bites* the beach; dunes lap
   into the green. A dead-straight full-width shoreline is a fail.
5. **Buildings sit in a town, not on a lawn.** Every building front opens onto a
   real apron (the plaza street is ≥2 rows), and the town has at least one **fenced
   garden** (fence runs + end posts + flowerbeds) plus signs/lamps on the walked
   lanes. A building floating in grass is the old look.
6. **Encounter grass is hard-edged tufts, by design.** The `tallgrass` family ships
   fill(+variants) ONLY — staggered blade-fan clumps over a darkened bed, no
   transition ring — so a patch reads instantly as "grass you fight in" (the classic
   convention). Patches are shaped (rule 4), 2–4 deep, with the safe lane intact.
7. **Routes carry gameplay, not just terrain.** Per route segment: 1–3 **trainer
   beats** (static NPC + step_on cutscene tile on a choked lane — a boulder or the
   NPC closes the other column so the beat can't be skirted), wild bands that
   **bridge the towns' levels** (next Lampwarden's ace ≈ previous ace +5–6; the
   route's band fills the gap — e.g. Dimglass I 3–6 → II 8–10 → Pearlmoor 12), and
   the story beats the walkthrough pins (A2/B1 live on Dimglass I).

**Tile-kit notes backing the rules** (all deterministic, in `tools/maps/tileforge.py` —
no API needed): `texture_grass` (blade dashes), `tallgrass_tuft` (the encounter tile),
`grade`/`cliff_strata`/`cliff_wall_edge` (the lifted, stratified cliff with true wall
edges), `deglow` (kills baked highlight rims on pale fills), `inner_corner` (13-piece
completion for path/sand/tree/cliff — *not* water, where the synthetic bite reads as
a stray sand wedge), and the drawn props `draw_fence_h`/`draw_fence_post`/
`draw_boulder`/`draw_flowerbed`. `build_shared_overworld.py` applies them when packing
the shared set.

**The joints cure (the "every tile has a border" disease).** Generated fills carry a
baked per-tile vignette; tiled, it becomes a visible grid that `deborder` (outer ring
only) cannot reach. The cure is `flatten_vignette` (toroidal high-pass, keeps detail +
mean) on every FILL, and `flatten_axis` on every EDGE/strip (flattens the lighting bow
along the tiling axis only, preserving the designed transition across it). Edge
*variants* are mirror-flips + jitter, never `roll` (rolling a non-toroidal texture
drags its interior seam into view). Edge tiles are also **value-matched** to their
fill (`_sand_post` pattern) or the surface reads as a darker ring with a hard inner
line. Interior floors get the same cure via `tools/maps/cure_interior_floors.py`
(edits the masters + repacks both interior sets).

**No 1-tile lamps.** The lamp breadcrumb is the 1×3 `tinderwick_lamp_post` OBJECT
(walk-under, trunk *beside* the lane), never the legacy single `lamp` tile — a
one-tile prop on an opaque card is the "white bag" look (art-style §14b).

**Known gap (raise, don't paint around):** path/water cells punched through a sand
flat leave raw sand fill at the contact (the path's own edges carry the seam — a
cosmetic WARN in `validate_map`). The proper fix is a dedicated sand↔path FLAT
transition via `composite_overlay.py` when the flats biome gets its art pass.

---

> **In one line:** design screen-by-screen for the 15×10 window, lead the eye with light,
> gate with geography, teach the opening hour as a gentle ramp, keep layers and encounter
> zones disciplined, compose to §11 — and run the checklist every time.
