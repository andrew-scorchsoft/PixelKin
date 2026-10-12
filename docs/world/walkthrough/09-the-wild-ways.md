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

### C · The Rimeway (north of Pale Vault → Coldfog Marches II)

**Lore.** The old star-tenders' high road between the Pale Vault and the Nightreach
watchers — a line of rime-lamps over the col. When the Hollowing drained the marshes they
**barred the Rime Gate from the marsh side** to keep the coldfog in and the curious out.

**Shape and the one-way unlock.** From Pale Vault you **climb** (ladders up ice bands, glare-ice
slide puzzles): `rimeway_ascent` (30×44, 118..148, -345..-301) → `rimeway_fold` (28×44, the high
plateau, 90..118, -365..-321; exclusive frost kin, the frozen falls with the clear-ice core,
a cairn cache) → the **Rime Gate** at the Fold's west edge, barred *from the other side*: you
see the descent and the fog through the grille. Later (West, from Coldfog Marches II, Emberward
held), `rimeway_descent` (28×28, 62..90, -341..-313) climbs east from the marsh to the gate's west
face; lift the bar (`flag:rime_gate_open`) and the Rimeway becomes a return compressor Coldfog ↔
Pale Vault. Bands: Ascent/Fold 39–42, Descent 46–48.

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

### S · Sunvault Climb, rebuilt as a mountain face

The climb gets taller and steeper: **four maps** instead of two. `sunvault_climb_i` and `_ii`
are rebuilt as terraced cliff faces (cliff bands with ladders, switchback ledges, a
Sunsketch vine bridge kept as the I→II boundary), and two new maps, `sunvault_climb_iii`
(the Gilt Face: ladder pitches, a trestle over a gully) and `sunvault_climb_iv` (the Sun
Ledges: the last exposed traverse to the observatory hill), sit between `_ii` and Nightreach.
Nightreach, its lane, Helia Vault and the marshes all move north by the added height; the
Rimeway is fitted to the result. Bands 46→49 (Nightreach 48–50, Nessa ace 52 unchanged).

## 3. Retrofits (existing routes that should *play*)

A small, careful pass — optional lines only, never the golden path's beats: a ladder
shortcut + ledge zig-zag on `cinderwind_scarp`, a glare-ice side pocket on `hushfrost_pass_i`,
and a bridge/underpass on one South/East route. Every retrofit goes in the map's **builder**
(check_rebuild), and `audit_journey` must still PASS unchanged.

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
