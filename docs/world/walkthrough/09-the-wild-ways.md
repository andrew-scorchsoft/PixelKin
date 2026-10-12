# PixelKin Walkthrough — 09 · The Wild Ways (non-linear expansion, 2026-10)

> Region-crossing file under the [spine](./README.md); its §0 rules, §2 flag strings, §4
> curve, §5 optional-content web and §10 voice are binding here. Geometry is binding too:
> [`../geometry.md`](../geometry.md) — every new outdoor map below is placed at exact tile
> coordinates so `world_geometry.py --check` still closes. Canon vocabulary only.
>
> **Scope.** Five pieces that make Vesperholm feel less like a corridor: a long downhill
> bike run with a cable car home (**A**), a visible-but-locked side quest marsh off the fens
> (**B**), a high frost road that loops the North back to the West (**C**), a mine that goes
> deeper and deeper (**D**), and a real mountain-face **Sunvault Climb** (**S**). Plus one
> shared **traversal kit** (slopes, ice, rails, bridges with underpasses, ladders, bike
> ramps) and a retrofit of a few existing routes that are "a map for the map's sake".

## 0. The player promise

1. **Seen early, earned later.** Every new area is *visible* (or rumoured) well before it
   opens, and opens from somewhere else in the world: the run's lift is chained at the top,
   the marsh's ferryman wants a lens from the ice village, the frost gate is barred from the
   marsh side, the mine's last chamber needs a brighter lamp. Each is a reason to come back.
2. **Maps you traverse, not just cross.** Each new route has a verb: coast and steer, slide
   on ice, ride rails and throw switches, climb ladders up cliff bands, cross over a trestle
   and come back *under* it. Barriers force zig-zags; ledges are one-way decisions.
3. **It's lore, not furniture.** Every area answers a question the main story raises: where
   the wicks came from, what the marsh-lights are, what the Hollowing walled in, what the
   miners heard breathing.

## 1. The traversal kit (engine, data-only per map)

All of it is **map data**, never tile metadata (the shared overworld set is frozen); the art is
the `traverse_set` accent tileset (drawn in code, `tools/maps/build_traverse_set.py`). The
audits' movement model (`tools/maps/worldmodel.py`) mirrors every rule below.

| Field | Shape | What the player feels |
|---|---|---|
| `flows[]` `kind:'slope'` | `{id, rect\|tiles, dir}` | A steep chute: you're carried `dir` every step; left/right steers; you can never step *up* into it. One-way by design — the Wick-Run. |
| `flows[]` `kind:'ice'` | `{id, rect\|tiles}` | Glare ice: you slide in the direction you stepped on until something stops you (the classic stopper-rock puzzle). |
| `flows[]` `kind:'rail'` | `{id, rect\|tiles, dir}` | An ore-cart rail: carried `dir`, no steering. A flow may carry `requires_flag`/`hidden_when_flag`, so a **lever** (a `script.*` that flips a flag) switches a junction — the Old Seams' puzzle. |
| `spans[]` `kind:'bridge'` | `{id, rect, axis, under?}` | A deck you walk along its axis (never off its sides). `under:true` lets you pass *beneath* it across the axis — walk over a trestle, loop round, come back under it. The deck is drawn above you while you're underneath. |
| `spans[]` `kind:'ladder'` | `{id, rect, axis:'v'}` | Climb a cliff band: up/down only, you face the rungs. Ladders make cliff faces walkable without warps. |
| `spans[]` `kind:'plank'` | `{id, rect, axis}` | A rope-plank over a chasm: along the axis only. |
| `jumps[]` | `{id, at, dir, length}` | A ramp: ride onto it heading `dir` and you clear `length` tiles (gaps, rocks). On foot it's just ground. |
| `ride` | `true` | The map is ridden: holding the rented **runner** you ride at bike speed (the `runner` sheet, or a procedural wheel). |

New cutscene op: `{op:'timer', id, action:'start'}` / `{op:'timer', id, action:'stop',
tiers:[{ms, flag, label}]}` — a run clock shown top-right while running (the Wick-Run time
trial). Every step that's forced (slope/ice/rail/underpass) still fires encounters, warps and
step_on triggers on arrival, exactly like a normal step.

## 2. The pieces

### A · The Wick-Run (west flank, Sunvault → Lightkeeper's Point)

**Lore.** Before the Long Dusk, the wax for Vesperholm's wicks was rendered from sun-vine
tallow in the Sunvault chandleries and run *down the mountain* on wax-carts along a graded
chute to Pearlmoor's quays for shipping. The empty carts went back up on the **Tallow Lift**,
a cable car. When the sun-vines shut (the Dusk), the wax stopped, the chandleries cooled and
the lift's brake was chained at the top. The run survives as a sport: the **Runners**, a club of
reckless young riders on *runner-wheels* (a two-wheeled bike), race it in the dark. It's
where wicks — the game's money — literally come from.

**Shape.** Six maps, ~200 tiles of descent, all `region:'west'` except the foot (`south`):

| Map | Size | Placement (x..x2, y..y2) | Role |
|---|---|---|---|
| `wickrun_crest` | 30×28 | -5..25, -266..-238 | Top station off Sunvault Climb I's south edge: the chandlery ruin, **runner rental** (300w, or free after a Runner beats you), the Tallow Lift's top house + brake (`flag:tallow_lift_freed`), the start gate (timer start). Flat, no encounters. |
| `wickrun_chute` | 28×44 | -8..20, -238..-194 | The upper chute: slope lanes with berms, a split (left line = grass + a trainer, right line = a ramp jump to an item ledge). |
| `wickrun_trestles` | 28×44 | -27..1, -194..-150 | The trestles: the run crosses OVER itself on a trestle bridge, hairpins, and passes back UNDER it. Two Runners on landings. |
| `wickrun_traverse` | 30×30 | -57..-27, -170..-140 | The traverse: the chute turns west across the slope (`slope dir:left`), a rock garden of stoppers and a ramp line; an old wax-cart wreck cache. |
| `wickrun_lower` | 28×44 | -57..-29, -140..-96 | The lower run: fast straights, ledges, the Runners' captain (Rook) on the last landing. |
| `wickrun_foot` | 30×30 | -51..-21, -96..-66 | The foot: the Tallow Lift's base station, the runner return, the finish (timer stop), a quiet wax-yard; east edge → **Lightkeeper's Point** west edge. **No encounters** (reachable from the South at lv ~14). |

**Gates.** From the bottom (early): the lift house is open but the car is *up top* — the
brakeman's sign and a lift-keeper explain it ("brake's chained at the crest"). You can't
walk up: the run is all slope. From the top (post-Solar, lv ~47): rent a runner, ride down.
Reaching the crest frees the brake → the lift runs **both ways** forever after (`script.tallow_lift`,
the `travel` op — a ride, not a graph edge, like the Lantern-car). Returning the runner at the
foot is automatic. Rest point: the foot's wax-yard bench (beside the lift).

**Kin / trainers / items.** Wilds 46–50 on the run's verges and landings; the Run's exclusive
kin are its slope-dwellers (see the encounter tables in `build_species.py EXTRA_ENCOUNTERS`).
Five Runners (route class) + Rook (route class, ace 50). Items: a Lumen Drop on a ramp-only
ledge, a Beacon charge in the cart wreck, a wick purse. **Time trial:** gold/silver/bronze
ribbons (`flag:wickrun_gold` …) pay wicks once each and Rook gives the **Runner's Ribbon** key
item for gold (cosmetic + bragging; the free rental).

**BUILT (2026-10) — what each map does.** Builders `tools/maps/build_wickrun_*.py`; content
`src/game/content/regions/wickrun.ts`.

| Map | The idea on it |
|---|---|
| `wickrun_trestles` | **The Slalom**: a full-width chute staked with three wax-barrel barriers, gaps alternating right/left/right (steer, you can't brake uphill). **The Spiral Trestle**: a flat trestle-head landing (Runner TAMSIN, grass, a sign), a 2-wide drop onto a vertical timber deck (`spans` bridge, `under:true`, in the `above` layer, shade below) that carries you OVER the gully; off its foot round the knoll (dry lane + grass, Runner OSSIE's sight line), back up the inside of the bend, and a west-carrying chute takes you UNDER the same deck. **The Steps**: three terraces dropped by one-way ledges whose hop-off is barred (boulders/fence) on alternating ends — the zig-zag down to the traverse; the wick-purse (300w) in a nook off terrace one. |
| `wickrun_traverse` | The road turns WEST (`slope dir:left`). **The Rock Garden**: a 12×14 west-carrying chute strewn with stopper boulders (spaced so every stop leaves a sidestep) funnelling to one gap; Runner PIP watches the entry pad. **The Cart-Wreck Shelf**: steer DOWN off the garden onto a flat grass pocket — the wax-cart wreck holds the **Beacon charge**. **The Ramp Line**: two kickers clear a rockfall, the road turns DOWN the west wall, two more clear a boulder bank (its flanks are wall, so you only ever meet a kicker head-on). |
| `wickrun_lower` | **The Long Straight** (14 rows, the run's fastest): a mid-road kicker over a boulder pair, and a side-kicker off the east verge onto the carters' brake-hut shelf (ramp-only cache: 2 Wax Cakes) that drains back into the run. **The Steps** (two full-width ledges) onto **the Cross-Slope** (`dir:right`) with a steer-down **cart siding** (grass, the rare Chandrek), round the corner down the second straight (another kicker) to **the Runners' Camp** — ROOK stands where every rider's arrival row is in his sight. |
| `wickrun_foot` | `region:'south'`, NO encounters. The last drop under a finish arch; its final row is the finish band (`script.wickrun_finish`: `timer` stop → tier flags → each tier's one-time prize → the lift-keeper takes the runner, `flag:wickrun_riding` cleared → Rook's ribbon if gold). The Tallow Lift's foot station (`script.tallow_lift_foot`: closed until `flag:tallow_lift_freed`, then the `travel` ride to `LIFT_TOP`), the yard bench (rest point), the wax-yard (yard-hand lore: every wick began on this mountain), Rook after he's beaten. East beach → Lightkeeper's Point's west edge (0,8)/(0,9). |

**One-way, proven.** Every map's upstream door is unreachable from below (a full-width chute
band, a west-carrying chute or a ledge line between them) and no reachable tile is a trap —
checked per map with the worldmodel (`moves_from` BFS from the exit tiles / from every
reached tile). The Tallow Lift is the only way up. On the lift's DOWN ride from the crest a
held runner is handed back to Pell (`script.wickrun_hand_in_top`), so nobody arrives at the
foot holding one.

**Time-trial tiers (measured).** The fastest line (Dijkstra over the worldmodel, 64 ms a tile
at runner speed — slope carry runs at min(ride, run) = 64 ms; leaps +60 ms) is chute 3.0 s +
trestles 7.1 s + traverse 2.9 s + lower 3.6 s + foot 0.5 s ≈ **17.1 s of riding**, plus four map
changes at ~1.5 s ≈ **23 s** flat out. Tiers (`WICKRUN_TIERS`): **gold ≤ 26.0 s**, **silver ≤
32.5 s** (+25%), **bronze ≤ 41.5 s** (+60%). Prizes once each: 600 / 400 / 200 wicks (modelled in
`progression.mjs`, West leg finds). A trainer battle mid-run counts against the clock — race
once the Runners are beaten. Rook's record is 24 s (the crest kid says so).

**Kin tables.** The same shape all the way down (bands rising 46–48 → 48–50; day twins 56–64):
Tallowcrest + Wickmere common, Solvyne/Dawnfawn/Helibud the Sunvault regulars, Warmantis rare,
Chandrek very rare; by day Warmantis, Chandrek and Wicklord come out. The average BST is kept
on the dex's level trend on purpose — `progression.mjs` fits wild BST against level over every
encounter row, and the Storm Gleam checkpoint sits on its +4 edge, so a heavy optional table
tips the whole curve.

### B · The Mirelights (east of Saltreach Fen I) — *seen early, opened from the ice village*

**Lore.** East of the fen lies the **Glassmere**, a drowned field where the fen-folk's old
causeway sank. Its lights are famous: wandering blue lamps over the water that lead boats
astray. The fen-folk say the lights were once *one* light — the fen's own lamp, a kin that led
travellers home — until the Hollowing's first experiments put it to sleep in a null-lantern
(cinder law rule 2: a sleeping luminous kin starves its star). What's left are its echoes:
false lights that lie. The eel-wife's boy, **Tobin**, rowed out after them last winter.

**The gate (visible early).** Saltreach Fen I's east edge is a ferry stage. The lights flicker
across the water (ambience). The ferryman, **Old Ansel**, won't cross: *"Half those lights are
lies. I'd want a true-eye — the frost-glass the Pale Vault grinders cut — before I'd trust my
oar to them."* The eel-wife asks you to look for Tobin. JOURNAL: "The Lights on the Glassmere".
In **Pale Vault Glacier** (the ice village, lv ~40), the lens-grinder **Isel** cuts you the
**Frostglass Lens** (key item) after a small errand (bring her a clear-ice core from the
Rimeway's frozen falls — piece C — so the two new areas reference each other). Show Ansel the
lens → he ferries you (`flag:mirelight_ferry`).

| Map | Size | Placement | Role |
|---|---|---|---|
| `mirelight_landing` | 30×44 | 59..89, -116..-72 | The far shore: stilt huts of the drowned causeway-village, Tobin's boat, wilds 38–41. |
| `mirelight_glassmere` | 30×44 | 89..119, -116..-72 | **The false-lights maze**: plank walks and causeway stones over the mere; with the Lens, false lights read as false (some plank walks are illusions that only exist in the lights' lie — flag-swapped spans/objects). Currents (`slope` on water) pull swimmers. |
| `mirelight_chapel` | 30×44 | 119..149, -116..-72 | The drowned bell-chapel: underpass/bridge loops, Tobin found (alive, lost, embarrassed), the null-lantern. |
| `lanthorne_hollow` | cave | (portal) | The legendary's rest: wake **Lanthorne** (#165, Tide/Light) from the null-lantern; `legendaryBattle` lv 45, cooldown 12 won. |

**As built (2026-10, Lane B).** Builders `tools/maps/build_mirelight_landing.py`,
`_glassmere.py`, `_chapel.py`, `build_lanthorne_hollow.py` (shared pieces in
`tools/maps/mirelight_common.py`); content `src/game/content/regions/mirelight.ts`.

- **The gate** (`build_saltreach_fen_i.py`): a ferry stage at Fen I's east edge (rows 23-24,
  `mirelight_ferry_stage`) on a carved inlet, marsh-lights over the water. **Old Ansel**
  (`script.mirelight_ansel`) names his price (`flag:q_mirelight_ansel`); with
  `flag:has_frostglass_lens` he looks through it and sets `flag:mirelight_ferry`. The edge
  warps `to_mirelight`/`_s` carry `requires_flag` + `blocked_ref: npc.mirelight_ansel_blocked`;
  the first crossing is a once-only step_on beat on the stage (`script.mirelight_ferry_ride`,
  `flag:mirelight_crossed`) that hands you across with the `travel` op. The eel-wife now runs
  `script.mirelight_eelwife` (her own `script.fen_eelwife`, then the Tobin ask,
  `flag:q_mirelight_begun`). `GRANTS["saltreach_fen_i"]` += `flag:mirelight_ferry`.
- **The deep.** Out here every early Gift is held, so the Glassmere is **deep water**
  (`deepwater_set`, the reserved `deepdive`): `mirelight_common.deep_layer` makes every pond
  cell deep unless it is within one tile of *walkable* shore (a tree border is not a shore,
  so no shelf sneaks round a channel's end). Tidecall swims the shelves; only boards cross.
  The Glassmere builder ASSERTS no island swims to another without a board.
- **The false lights.** Every walk is a `plank` span with a blue will-light at its far end
  (they all look alike). Through the Lens (objects `requires_flag: flag:has_frostglass_lens`)
  the causeway-reed at each walk's MOUTH tells the truth: LIT = sound boards, DEAD = a lie.
  A false walk stops short over the deep; its last board is a step_on beat
  (`script.mirelight_dunk_<id>`: splash, then `travel` back to the mouth). Landing: three
  walks over the first arm (the middle is true — the teaching screen). Glassmere: islands
  I0→I1→I2→I3→I4, ten walks (five true).
- **Currents** (`flows[]` `slope` over shallow water, `mirelight_common.current`): I3's south
  shelf runs DOWN to the diver's islet (the **Glassmere Pearl**, valuable, current-only) whose
  only way off is a long true walk back to I1 — a one-way loop; and the RETURN current sweeps
  from I2's west shelf back down to I0.
- **The chapel.** Over then under: the entry bank crosses the sunk street on a 7×2 trestle
  (`deck under=True`, `above` layer) — you see Tobin below in the street's north end — then
  the east bank, a **ladder** down its cliff, the acolyte's one-row shelf (Brother Ives,
  sight 1 — unavoidable), the meadow, and north up the street **under** the trestle to
  Tobin (`flag:mirelight_tobin_found`, 2 Beacon charges; he goes home to Fen I). The chapel's
  walk-onto door (on its flooded porch step) is held on Tobin's flag. The acolyte's camp is
  the Mirelights' **rest point** (`script.mirelight_camp_rest`).
- **The set-piece** (`script.mirelight_lanthorne`, 07's staging): letterbox, silence, the lens
  lets a TRUE light through the null-glass, `sting-hour` → `battle-hours`, `legendaryBattle`
  lanthorne #165 lv 45, cooldown 12, `npc.lanthorne_resting`; on the catch the lantern stands
  empty, a `starfall` and the star over the fen burns brighter.
- **Kin** (mirrored in `build_species.py` `_MIRE_TABLES`): night 38-43 — Lumpin, Fennlight,
  Brineroll, Poolfrond, Tidmaren, Glostern, + the Mirelights' own Tidwraith #22 / Lumplass
  #32 (rare-ish) and Lampling #148 (rare, Glassmere + chapel); by day the same species
  +17 levels. The grown D-tier forms are the trainers': Moss (eel-catcher, ace 40), Odo
  (lamp-diver, ace 42), Brother Ives (Hollowing acolyte, ace 43), all route class.
- **Flags** (owned): `flag:q_mirelight_begun`, `flag:q_mirelight_ansel`, `flag:mirelight_ferry`,
  `flag:mirelight_crossed`, `flag:mirelight_tobin_found`, `flag:lanthorne_caught` (+ the
  trainers' `_beaten` and caches' `picked_*`). Read: `flag:has_frostglass_lens` (Isel).
  LORE `mirelights` (unlock `flag:mirelight_ferry`) + `lanthorne`; JOURNAL
  `mirelight_lights`.

### C · The Rimeway (north of Pale Vault → Coldfog Marches II) — **BUILT 2026-10**

**Lore.** The old star-tenders' high road between the Pale Vault and the Nightreach
watchers — a line of rime-lamps over the col that a tender carried oil to every night.
When the Hollowing drained the marshes they **barred the Rime Gate from the marsh side**
to keep the coldfog in and the curious out; with no oil coming round, the lamps went out
one by one (cinder law: a light nobody keeps starves). Hale, the last rime-tender, still
keeps one lamp at the Fold; a Hollowing acolyte still keeps the bar — and lets you lift it.

**Shape (built).** Geometry is fitted to the rebuilt Sunvault (§S) (world_geometry's frame, Tinderwick at 0,0):

| Map | Size | Placement (x..x2, y..y2) | Role |
|---|---|---|---|
| `rimeway_ascent` | 30×56 | 118..148, -357..-301 | Off Pale Vault's new north road (cols 23-24). Three glacier-wall bands (`glacierwall` lip + `face_ice` rows) climbed on ladders; **the Glare** — a full-width glare-ice sheet (shelf 1) whose only way off is the north-west ladder pad: a stopper-stone slide puzzle, **5 slides minimum, no trap** (searched with `facekit.ice_solve`; a full snow strip at its foot is the reset lane); a cache pool (second, optional slide); the west-notch ledge home. Band 39-41; trainer Ivo (rime-walker, ace 41). |
| `rimeway_fold` | 32×44 | 94..126, -401..-357 | The high plateau. **The frozen falls** (`rimeway_frozen_falls`) above a plunge pool of glare ice (5-slide puzzle) — the falls' foot runs `script.rimeway_ice_core` → `flag:rimeway_ice_core`. **The tenders' refuge** (`rimeway_tender_waystation`, a rest point) + Hale. **The Rime Gate** at the north edge (cols 6-7; `rimeway_rime_gate_barred/_open` swap on `flag:rime_gate_open`): from here it's a locked door with a line. Vaultclaw #76's only wild bed; trainer Sef (ace 42). Band 40-42. |
| `rimeway_descent` | 42×28 | 62..104, -429..-401 | Out of Coldfog Marches II's new east road (rows 16-17). The drained fen → ladder up onto the col ridge → ladder down to the gate yard; walking onto the yard before the gate **lifts the bar** (`script.rime_gate_lift`, step_on band, `flag:rime_gate_open`) and every rime-lamp on the road wakes (dead/lit swap pairs on the same flag, all three maps). The acolyte at the bar; trainer Dunne (fog-walker, ace 48). Band 46-48. |

**The one-way unlock.** North era (~lv 40): climb from Pale Vault to the Fold, see the
descent and the fog through the grille, can't pass (`npc.rime_gate_barred`). West era
(Emberward held — Coldfog II needs it): come up from the marsh, lift the bar; from then the
Rimeway is a return compressor Coldfog ↔ Pale Vault. Graph: `rimeway_fold → rimeway_descent`
`requires_flag: flag:rime_gate_open` (GRANTS: the Descent).

**Isel and the true-eye (the B ↔ C link).** In Pale Vault (beside the new north road),
Isel the lens-grinder asks for clear ice from the Fold's falls (`flag:q_rimeway_lens` →
JOURNAL "A True-Eye"), mentioning "a ferryman down in the fens asked for one once"; with
`flag:rimeway_ice_core` she cuts the **Frostglass Lens** (key item) and sets
`flag:has_frostglass_lens` — the Mirelights' ferry key (Lane B reads it). JOURNAL "The Rime
Gate" (`flag:q_rimeway_gate`, Hale → `flag:rime_gate_open`); LORE "the Rimeway".
Music `rimeway`; backdrops `rimeway-a/b`. Builders: `build_rimeway_ascent/_fold/_descent.py`
(on `tools/maps/facekit.py`); content: `src/game/content/regions/rimeway.ts`.

### D · The Old Seams (deeper under Cinderhead)

**Lore.** Cinderhead's miners dug *cinder-coal*: warm black stone that never quite cools. The
old foremen knew why and sealed the deepest seams: at the bottom, the mountain is built
around **the first star that ever fell** — so long ago it was never a "fall" in anyone's
memory. Its kin, **Emberroot** (#166, Stone/Ember), sleeps there, and the coal is its slow
breath (cinder law rule 5: a cinder is never dead, only guttered). The Foreman's Ledger (E3)
already mentions "the seam we don't work".

**BUILT (2026-10).** Four dark caves (`dark: true`, `old-seams` music, `old-seams-a/-b`
backdrops), stacked by ladder portals under Cinderhead so they never touch surface geometry.
Builders `tools/maps/build_old_seams_{i,ii,iii}.py` + `build_emberroot_heart.py` on a small
shared kit (`seamskit.py`); the Seams' own surfaces are the **`seams_set`** accent tileset
(`build_seams_set.py`: open SHAFT autotile family whose fill breathes cinder-glints, cinder-coal
floor, raked scree, glowing veins, and redrawn ore-cart rails on true pixel rings) and the
code-drawn **`old_seams_first_star`** object. Content: `src/game/content/regions/oldseams.ts`.

| Map | Size | Band | What you do |
|---|---|---|---|
| `cinderhead_mine` (edited) | 28×24 | — | The **seam-door** in the north workings beside Otho's hall (`old_seams_sealed_door` ⇄ `_open`, a 3×3 flag swap). Locked line `npc.old_seams_sealed` ("THE SEAM WE DON'T WORK"). After `gleam:stone` Otho waits beside it (`script.old_seams_otho`, a beat for the E3 ledger if you returned it) and lifts the bar → `flag:old_seams_open`. |
| `old_seams_i` — the Shaft Benches | 30×30 | 27–29 | Three benches stepping down the seam, each cut by open shafts. Arrive under the **headframe**; walk **planks** over the pits (one to a pillar islet cache); **timber ladders** up/down the rock bands (zig-zag: east, west, east); a boulder wall turns you; a one-way **cinder-scree spill** (slope) drops B→C at the east end — fast down, the long zig-zag back up. Seam-miner Kester. |
| `old_seams_ii` — the Rail Yard | 32×32 | 29–31 | **The puzzle.** Four platforms round a sunk working, joined by ore-cart **rails** on rock ribs (rail flows: carried, no steering, never back up). Three **levers** (`flag:seams_lever_1..3`, `script.seams_lever_N`, a `traverse_lever_off/_on` swap) throw three **junctions** (a straight/turnout flow pair, `traverse_switch_a/_b` point-stands). Lever 3 is on the SW siding, which you only reach THROUGH the yard: throw 1 → ride to the siding → throw 3 → ride home → ride to the far platform. Every line ends on a platform in every lever state and every platform rails home (the builder asserts all 8 states). Seam-miners Wenna (siding), Tam (east stage); the siding's **Starglass Shard**. |
| `old_seams_iii` — the Scree Galleries | 30×30 | 31–33 | Cinder-coal floor, veins brightest. Two **scree slopes** run one way down (west, then east) with a **ladder home** at the far end of each gallery; steer hard left at the top of the west scree for a ledge only riders reach (**Lumen Drop**). The foremen's **camp** (a brazier the coal has kept warm seventy winters) is the descent's **rest point**. The foremen's last ladder down is gated `requires_flag: flag:lamplight_starlight` (derived at six Gleams) with `blocked_ref: npc.emberroot_dark` — a deliberate return at ~lv 40. Seam-miners Penhal, Jory. |
| `emberroot_heart` | 20×16 | — | The first star in its root-rock mound; the awe band (`script.emberroot_heart_enter`, once); **Emberroot** at its foot → `script.emberroot_wake` (letterbox, silence, `sting-hour`, `battle-hours`, `legendaryBattle` lv 46, cooldown 12 won, `npc.emberroot_resting`); the star answers Confirm before and after; the Foreman's Ledger's **last page**. |

Wild kin (night; the `flag:dawn` day twins run 55–65): floor I Oreling/Coalump/Riddlestone/
Gravelo + **Orebound**; floor II **Orebound**/Riddlestone/Sparkrat/**Pyrolith**/**Lithonyx** +
**Ferrolith** (rare); floor III **Orebound**/Coalump/**Pyrolith**/**Lithonyx** + Ferrolith (rare) +
**Prismara** (very rare). Mirrored in `build_species.py OLD_SEAMS_TABLES`; the three floors are in
`progression.mjs TREND_SKIP_AREAS` (optional rich beds must not bend the mainline's BST trend).
JOURNAL `wild_old_seams` ("The Seam We Don't Work"); LORE `old_seams` + `first_star`.

### S · Sunvault Climb, rebuilt as a mountain face — **BUILT 2026-10**

The climb is **four maps** of gilt sandstone face (I → II → III → IV → Nightreach), all on
`tools/maps/facekit.py` (ASCII-drawn faces over wildkit: `cliff` lip rows over
`face_gold` rows, `ladder` spans up them, `plank` spans over clefts, a trestle `deck`
with `under:true`, sand-ledge notches as one-way returns).

| Map | Size | Placement (x..x2, y..y2)* | Role |
|---|---|---|---|
| `sunvault_climb_i` | 30×26 (unchanged) | -5..25, -292..-266 | The foot: three tiers, ladders E (the first pitch) and W/E down to the old garden (a loop), the **west notch** ledge home; every handshake + runner placement kept (Solarium E, Wick-Run S, the vine gorge N). Band 46-47. |
| `sunvault_climb_ii` | 30×40 (was 28) | -5..25, -332..-292 | The **living sun-vine bridge** up band 1 (Sunsketch gate), a ladder pitch, the **cleft plank** across tier C, the long west ladder; the X3 viewpoint, Helia mouth, striker pocket + vigil scar, rest arbor all kept. Band 47-48. |
| `sunvault_climb_iii` | 30×44 (new) | -5..25, -376..-332 | **The Gilt Face**: four ladder pitches E/W/E/W, a mid-face ledge cache, **the trestle over the gully** (cross it going up; drop into the gully at its head and walk out UNDER it going home), the **keepers' shelter** rest point. Trainers Imma (sun-keeper) + Orrin (star-watcher), ace 49. Band 48-49. |
| `sunvault_climb_iv` | 30×36 (new) | -5..25, -412..-376 | **The Sun Ledges**: three two-tile ledges broken by clefts and rope-planks, four ladders, two notch-ledges home, the observatory hill (spyglass, watchers' camp). Trainer Pim (star-watcher) posted over a plank, ace 49. Band 48-49. |

*`world_geometry.py`'s frame (Tinderwick at 0,0; the Wick-Run joins the north to it). Nightreach and everything north of climb II
(its lane, Coldfog, Drownlight) moved north by 92 tiles; `world_geometry --check` closes.
Nightreach's south road (`to_sunvault`/`_e`) now lands on climb IV. Content (new signs,
the three trainers, four caches, the shelter + spyglasses): `content/regions/sunvault.ts`;
LORE "the sun-keepers". Climb III/IV music `sunvault-climb-b`.

## 3. Retrofits (existing routes that should *play*)

A small, careful pass — the golden path's beats untouched: every retrofit goes in the map's
**builder** (check_rebuild), and `audit_journey` still PASSes with no GOLDEN edits. No map
gained a Gift requirement; no warp, table, band or trainer roster changed.

**Built (2026-10), four routes in three regions** — the mechanic is on the MAIN lane each time:

| Map | Region | Mechanic | Before → after |
|---|---|---|---|
| `cinderwind_scarp` | North (Deep → Galehigh) | `spans` **ladders** up two tall scarp faces (wildkit `face_wall` foot rows); pitches at opposite ends; grass ledges at the other ends | walk-up gaps under the ledges, both ways ~37 steps → zig-zag climb 62 steps, two-hop descent 36 |
| `hushfrost_pass_i` | West | `flows` **glare ice**: the falls' plunge-pool across the north passage, three stopper stones | open snow → every mid↔west crossing slides; reading the falls = stop under them |
| `wrackline_path` | bay road (East → hub) | `spans` **trestle, `under:true`**: over the Wrack Cut, round the strand, back under it along the cut floor | straight grass corridor → the over/under loop (both directions) |
| `lanternfall_road` | bay road | **ledge + ramp zig-zag**: three cliff steps, ramps alternating E/W/E, one lit one-way drop | no ledges ("no loop") → 52 steps up vs 33 down |

Strand-proofing: every reachable tile on each map can reach every entrance again (a
`worldmodel` BFS from each tile), `render_walkable --all` reports no softlocks, and
`check_traversal.mjs` proves the engine and the audit model agree on all four. Signs on the
scarp, Wrackline and Lanternfall name the mechanic in one line. Shots: `tools/shots/shoot.mjs`
on the ladder pitches, the trestle deck and the underpass, the glare-pool slides, the drop.

## 4. Audio & art owed

| Cue | Where | Classic | Remaster |
|---|---|---|---|
| `wickrun` | the run (driving, fast) | chip `snes` | yes (never motif-conditioned) |
| `tallow-lift` | the lift ride sting | chip | — |
| `mirelight` | the Mirelights | chip | yes |
| `rimeway` | the Rimeway | chip | yes |
| `old-seams` | the Old Seams | bare `gbc` | yes |
| `battle-wild-legendary` reuse | Lanthorne / Emberroot | existing `battle-hours` | classic-only |

Battle backdrops (240×160 WebP): `wickrun`, `mirelight`, `rimeway`, `old_seams`. Sprites: the
two legendaries (5 views each + cries), Runner trainer sheets, the runner (bike) sheet.

**Built (2026-10):** both legendaries' 5 views + cries are packed; the backdrops are served as
`wickrun-a/-b`, `mirelight-a/-b`, `rimeway-a/-b`, `old-seams-a/-b` (`public/assets/backgrounds/battle/`,
raw masters `assets/backgrounds/battle/raw-*.webp`) and wait for their maps' `battle_backdrops`.

## 5. The two legendaries (dossiers for the species pipeline — BUILT)

The Three Hours' treatment ([07 §2](./07-the-three.md)): **tier E** · **BST 558** · **catchRate 24**
· `rarity: very_rare` → `scripted: true`, `encounters: []`. Stats are the deterministic
`make_stats(role, 558, name)` output (no stat pin); abilities, dex, kits and art are pinned in
`build_species.py` `CANON`. Kits come from the existing pool, no signature moves. All four
balance gates PASS with both in the roster.

### #165 Lanthorne — *the Mirelight* (Tide/Light · Special Wall)

- **Stats:** hp 112 · atk 44 · def 95 · spa 78 · spd 134 · spe 95
- **Ability:** `tidecaller` (it mends in its own mere) · hidden `mistveil` (the false lights:
  lowers the foe's accuracy on switch-in). *(CANON override; the Tide-E default is `phoenix`.)*
- **Battle kit (as met, lv 45):** `tide_pulse` · `dazzle_flash` · `light_pulse` · `mend`. Pinned
  rows: 1 `mist_spray` · 9 `spark_mote` · 16 `drench_song` · 24 `tide_pulse` · 30 `dazzle_flash`
  · 37 `light_pulse` · 42 `mend` · 50 `lightspire` · 56 `maelstrom`.
- **Catch design:** a special wall that dazzles and mends: physical pressure + a doze/chill for
  the ×2.5 bonus; whittle slowly and it heals the work away.
- **Dex:** "The Mirelight — the fen's own lamp, which once walked the drowned causeway ahead of
  lost boats and brought them home. A null-lantern put it to sleep long ago; the blue lights
  that still wander the Glassmere are only its dreams, and dreams do not know the way."
- **Category:** Mirelight Kin · 340 cm · 140 kg · habitat east

### #166 Emberroot — *the First Star* (Stone/Ember · Physical Bruiser)

- **Stats:** hp 112 · atk 128 · def 100 · spa 50 · spd 84 · spe 84
- **Ability:** `stonehide` (the mountain grown round it) · hidden `cinderveil` (Ember heals it:
  the coal is its own breath). *(CANON override; the Stone-E default is `phoenix`.)*
- **Battle kit (as met, lv 46):** `rock_hurl` · `stone_wall` · `pyre_slam` · `boulder_smash`.
  Pinned rows: 1 `pebble_toss` · 9 `cinderclaw` · 16 `gritfist` · 24 `flame_lash` · 30 `rock_hurl`
  · 36 `stone_wall` · 41 `pyre_slam` · 46 `boulder_smash` · 54 `throes`.
- **Catch design:** it hunkers (`stone_wall`) and hits like the mountain; special Tide pressure
  slips past `stonehide`, and the hidden `cinderveil` makes an Ember lead pointless.
- **Dex:** "The first star that ever fell into Vesperholm, so long ago the mountain grew up
  around it. It has slept at the root of Cinderhead ever since, and the warm black cinder-coal
  the miners dig is only its breath, cooling very slowly in the stone."
- **Category:** First-Star Kin · 640 cm · 2400 kg · habitat north

**Owed with the maps (not built):** LORE/glossary entries keyed to the sites' own flags
(`flag:mirelight_ferry` — adding them before content sets those flags fails `check_content`
E-FLAG), the `legendaryBattle` scripts, cooldown lines. *Emberroot's are BUILT with the Old
Seams (§2 D).*
