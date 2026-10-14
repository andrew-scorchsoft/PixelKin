# PixelKin Walkthrough — 10 · The Farlamp Isles + the Ashfall Shelf (2026-10)

> Region-crossing file under the [spine](./README.md); its §0 rules, §2 flag strings, §4
> curve, §5 optional-content web and §10 voice are binding here. Geometry is binding too:
> [`../geometry.md`](../geometry.md). Every new outdoor map below is placed at exact tile
> coordinates so `world_geometry.py --check` still closes. Use canon vocabulary only.
>
> **Why this round exists.** A level-design review of the stitched world
> (`tools/maps/render_world.py`) found two things:
> 1. **The main path's thinnest stretch** is Lowleaf → Cinderhead → Galehigh. That's three
>    dark caves in a row, then a single map (Cinderwind Scarp) carrying the whole
>    Otho 28 → Mira 34 jump. **Part II** fixes it.
> 2. **The empty sea under the lighthouse** (south of Wick-Run Foot, Lightkeeper's Point and
>    Pearlmoor Quay) is the best unused space in the world. Deep water already exists there,
>    gated on the reserved `deepdive`. **Part I** fills it with an after-the-dawn archipelago.
>
> Deliberately NOT expanded: the bay road home (Wrackline → Sounding Cave → Lanternfall) is a
> shortcut home, and padding it would slow down "coming round". The empty middle of the
> world map is the dark central mountain, and the empty space is what makes it read.

---

## Part I — The Farlamp Isles (post-game, optional, hidden)

### 0. The player promise

1. **Seen from the first visit, opened at the end.** From Lightkeeper's Point a fog bank sits
   on the southern horizon with a lamp blinking inside it, at every hour of the journey.
   Five **driftletters** (messages in bottles) wash up on shores across the world. Nobody can
   reach the isles until the dawn, and the game keeps saying so.
2. **A place, not a corridor.** The isles are a sprawl you sail, land on, dive under and get
   lost in: three sea maps, two wild isles, an island town and a four-floor sea-cave maze,
   the **Undertide**, whose tide-races switch with the tide-bells.
3. **Worth it.** A new kin family that lives nowhere else, a catchable set-piece guardian, a
   unique charge, a hoard of the rare things (Lumen Drops, Hearth Coals, signature
   Star-charts), the island keeper's super-battle, and a story payoff: **the isles get their
   own dawn.**

### 1. Lore

The **Farlamp** was Vesperholm's outermost sea-light, built on a skerry at the edge of the
**Fogwall**, a bank of sea-fog that has always lain off the south coast. **Driftholm**, a
town of lamp-keepers and kelp-farmers, lived in its light. The night the Long Dusk fell, *the
deep came up*: the sea rose a fathom, the Farlamp's rock went under, and the lamp drowned
still burning, then went out. The fog closed over the isles. No boat could cross the open
deep, because Tidecall parts moon-tides and the deep doesn't answer to the moon. For eleven
winters Driftholm kept small lamps alone and threw letters into the sea.

When the Keystar is relit the mainland gets its morning, but **the Fogwall keeps its own
dusk**. The sea holds what it drowned, so the isles stay dark until the Farlamp burns again.

*The deep answers a lamp lit from the Keystar's light.* That's why the crossing waits for the
dawn, and why no Lampwarden's Gift could ever have done it.

### 2. Crossing the deep: the Farlamp skiff (not a Gift)

Canon has **six** Lantern Gifts, each given by a Lampwarden, so the deep crossing is a **key
item**, the **Farlamp Skiff**. It's the old lamp-boat from under the lighthouse, rebuilt.
Holding it grants the reserved `deepdive` ability (new op `{op:'giveAbility', ability}`).
On deep water the player **rows the skiff**: a boat sprite replaces the swim sheet, and deep
water rolls its own sea encounters. Tidecall still swims the shallows, as now.

Rejected alternatives: a 7th Gift (breaks the six-Gift canon, and there's no warden left
after the dawn to give it); riding a kin across the sea (too close to the genre's trademark
move); a Lamplight-tier Tidecall upgrade (canon-safe, but you'd get it for free, with no
quest).

### 3. The unlock chain (`flag:q_isles_*`)

| Step | Where | What | Flags |
|---|---|---|---|
| Seed (any time) | Lightkeeper's Point | A fog bank + blinking lamp on the horizon (ambience + a looking-glass you can read). **Ione Fathom**, an old boatwright mending a hull under the tower, says the far lamp "went quiet eleven winters back". | `flag:isles_rumour` (first talk) |
| Letters (any time) | 5 shores | Driftletters: Dimglass Coast I strand, Gullcry Rock, the Wick-Run Foot beach, the Glassmere shallows, the Drownlight Beacon shingle. Each is readable lore and a pickup. | `flag:driftletter_1..5`; `flag:driftletters_3` **derives** (FlagStore: ≥3 of 5) |
| I1 (after the dawn) | Point | Ione: the sky's lit everywhere *but* there. With ≥3 letters she says "Then they're alive", fetches the hull and asks for the prow-lamp to be lit "from the Star-tender's light". | `flag:q_isles` (needs `flag:dawn` + `flag:driftletters_3`) |
| I2 | Dawnstead | Fenn lights the prow-lamp from the Starlamp. One quiet beat, never naming its first keeper. | `flag:q_isles_prow_lit` |
| I3 | Point | Ione hands over the **Farlamp Skiff**, and you launch from the slip below the tower. | `flag:q_isles_afloat`; item `farlamp_skiff`; ability `deepdive` |
| I4 | Undertide II | The **fog-glass** (the old keeper's lens) lets you read the buoy lane through the Fogwall. | `flag:q_isles_fogglass` |
| I5 | Driftholm | Arrival: a town that hasn't seen a boat in eleven winters. Elder **Nan Creel** opens the well-stair down to Undertide III. | `flag:q_isles_driftholm`, `flag:q_isles_wellstair` |
| I6 | the Drowned Lamp | Relight the Farlamp. The **isles' dawn**: the fog lifts, Driftholm's day-forms wake, the minor→major Gleam cadence plays (no Gleam is given). | `flag:isles_dawn` = `flag:q_isles_done` |
| I7 | the Drowned Lamp | **Farlume** (#177), the drowned lamp's guardian, rises as a catchable set-piece (`legendaryBattle`, cooldown like the Three Hours). | `flag:farlume_met` / caught |
| Coda | Driftholm | Keeper **Bram Fathom** (Ione's brother, the isles' best) is the super-trainer: ace lv 70, rematchable. | `flag:isles_keeper_beaten` |

Old-save safety: every gate keys off flags set inside this chain or `flag:dawn`, so nothing
can lock out a save that's already past the dawn.

### 4. Maps (placements are binding; tiles; north-up; `world_geometry` coordinates)

| id | name | kind | at (x,y) | size | links / role | levels |
|---|---|---|---|---|---|---|
| `farlamp_sound` | Farlamp Sound | route (sea) | (-21,-69) | 27×33 | Top edge = Lightkeeper's Point's south beach (the slip). Deep sea with islets, two boat-trainers, sea encounters. West → `farlamp_shelfwater`; south → `farlamp_gullwrack`. | 58–61 |
| `farlamp_shelfwater` | The Shelfwater | route (sea) | (-51,-66) | 30×30 | Top edge = Wick-Run Foot's beach (a second launch). Reef islets, mixed shallow and deep water, a sunken-hull cache. West → Fogwall; south → Kelpcrown. | 59–62 |
| `farlamp_fogwall` | The Fogwall | route (sea) | (-83,-66) | 32×36 | Heavy mist. Without the fog-glass a step_on band turns you round ("you lose the buoys…"). With it, a lantern-buoy lane (MapObjects `requires_flag`) leads south to Driftholm. The blinking lamp is here. | 60–63 |
| `farlamp_gullwrack` | Gullwrack Isle | route | (-21,-36) | 27×34 | Gull-cliffs, ledges and tall sea-grass. **Undertide I** mouth. A keeper's hut (rest point). | 60–62 |
| `farlamp_kelpcrown` | Kelpcrown Isle | route | (-51,-36) | 30×34 | Ruins of the old keepers' quarter, kelp-terraces. **Undertide II** mouth; Tidecall pools. | 60–63 |
| `driftholm` | Driftholm | town | (-83,-30) | 32×30 | Island town: inn (rest), chandlery shop, elder's house, the boathouse, the well-stair (→ Undertide III, gated `q_isles_wellstair`), a TRAVEL waystone (`content/waystones.ts`) so the way home is one menu away. | — |
| `undertide_i` **(BUILT, C2)** | The Undertide | cave | portal | 30×28 | Under Gullwrack. Shallow channels + **tide-races** (`flows` rail on water, flag-switched by tide-bells). Ladder down to II. | 61–63 |
| `undertide_ii` **(BUILT, C2)** | The Undertide — Kelp Vaults | cave | portal | 30×30 | Joins Gullwrack to Kelpcrown underground. The **fog-glass** at its heart. | 61–64 |
| `undertide_iii` **(BUILT, C2)** | The Undertide — Bell Galleries | cave | portal | 30×30 | From Driftholm's well-stair. The big tide-bell maze: three bells, every race ends on a ledge in every bell state (the Old Seams invariant). | 62–65 |
| `undertide_iv` **(BUILT, C2)** | The Undertide — the Drowned Stair | cave | portal | 26×30 | The last descent; the keeper's logbook pages; the door to the lamp. | 63–66 |
| `farlamp_drowned` **(BUILT, C2)** | The Drowned Lamp | cave | portal | 20×22 | The sunken lighthouse floor, an air pocket under the sea. Relight → Farlume. | set-piece |

Interiors (roomkit): `driftholm_inn`, `driftholm_chandlery`, `driftholm_elder`,
`driftholm_boathouse`, `gullwrack_hut`.

**Kin** (appended ids; roster pipeline: `selected.json` → `build_species.py` → validators →
`simulate.mjs` → `gen_docs.py`; sprites from each species' `art` block):

| # | name | types | notes |
|---|---|---|---|
| 172 | **Fathomote** | Tide/Light | a lantern-fish fry; sea encounters everywhere on the deep → kindles at lv 40 |
| 173 | **Fathomere** | Tide/Light | its lure lights a fathom of sea |
| 174 | **Hermiwick** | Stone/Tide | a hermit crab wearing a broken lamp-glass → kindles at lv 42 |
| 175 | **Beaconclaw** | Stone/Light | the glass is whole now and it shines |
| 176 | **Fogwisp** | Frost/Dark | a moth made of fog; the Fogwall and Undertide only |
| 177 | **Farlume** | Tide/Light | the drowned lamp's keeper-kin; set-piece catch, lv 68, F-tier register |

Each map's table also mixes in existing Tide/Stone/Frost kin, mirrored in
`build_species.py EXTRA_ENCOUNTERS` + `CURATED_AREAS`.

**Prizes:** the **Deep Charm** (`catch_bonus` ×3.0 on deep-water kin, conditional charge, sold
at the chandlery once `isles_dawn`); 3 Lumen Drops (Undertide II/III/IV); 2 Hearth Coals; two
signature Star-charts; a 2,000w purse; Bram Fathom's rematch payout; and Farlume.

**Side quests (3+, journal `content/quests.ts`):**
- **Letters Home**: Driftholm's letter-writers want to know theirs were found. Bring each found
  driftletter back to its writer (5 small payoffs, a gift for all five).
- **The Keeper's Log**: four logbook pages in the Undertide tell how the Farlamp drowned. The
  last one opens the Drowned Lamp's side room (a Star-chart).
- **Tide-bell Tuning**: a bell-ringer's child wants the three Bell Galleries bells rung in the
  old order; it pays a Lumen Drop and unlocks the shortcut race back to Driftholm.

**Panel revisions (v2, adopted):**
- **Ione names the coasts** (one line per shore). The journal entry reads letters n/5 with shore
  hints. Bottles carry the cache glint.
- **Sea-map density:** every 15×10 screen of a sea map carries an islet, wreck, trainer,
  buoy-cache or ambient kin, and `audit_visual.py` must pass.
- The **Fogwall turn-round** names its fix: "if only you had a glass to read the buoys by…"
- **Deep backtrack** (lane E): 4–5 skiff-only caches in existing deep water (Gullcry,
  Pearlmoor harbour, Dimglass II, Hearthfall, Tinderwick's outer reef). The skiff reopens the
  old world like a Gift.
- The Driftholm → Tinderwick sea strait is **cut** (padding); the Driftholm waystone does that job.

**Audio** (classic chip via generate-midi + a remaster via `remaster_track.py`; battles stay
classic-only): `farlamp-sound` (rowing on a long swell), `driftholm` (an island town hymn
in a minor mode that turns major after `isles_dawn` via `music_when`), `undertide` (sea-cave
drips and bells), `farlamp-relit` (the relight, the emotional cue). Farlume uses the
Three Hours' legendary battle cue.

**Art:** skiff walk-sheet (`player_indi_skiff`, the 4×4 layout; procedural fallback), Driftholm
buildings + boathouse + well-stair, the drowned lighthouse, lantern-buoys, bottle pickup,
tide-bell, fog-glass, battle backdrops (sea, isle, Undertide, the Drowned Lamp).

### 5. BUILT (lane C2, 2026-10): the Undertide + the Drowned Lamp

**Status: BUILT.** Five portal caves (`kind:'cave'`, region `outer`, registered in
`world/maps.ts` + `world/graph.ts`), scripts in `content/regions/undertide.ts`, all on a new
drawn accent kit.

**The kit.** `tools/maps/undertideforge.py` draws `undertide_set` (an accent set on the
seams_set pattern) and the `undertide_*` objects (own master folder
`assets/tilesets/undertide/objects/`, packed by `pack_objects.py`):
- `surge_*`: white water churning over a drop. It collides and is never swum; it forms the maze's walls.
- `tidepool_*`: sea shallows over wet stone (Tidecall, `water` encounters).
- `race_<dir>` / `race_fork`: the **tide-races**, calm lanes with drifting chevrons. A
  `kind:'rail'` flow rides on each. They're tagged `water` so you swim them, and they're
  `surge` for the autotiler so the churn wraps them seamlessly.
- `wetstone_*` and decor (barnacles, shells, wrack, drowned lamp-glass).
- Objects: the tide-bell (still/rung), the race-post (white/red), the logbook chest, the
  fog-glass stand (full/empty), **the Farlamp** (4×5, dark/lit), the keeper's camp, kelp, a
  fallen masonry pillar and a glass heap. (The sea-door pair is drawn but unused.)

`tools/maps/undertidekit.py` authors a floor from a char plan and **proves it**. In every
bell-flag state, every race entered from any free cell must end on a free cell, and every
pocket must race home. Each builder adds its own puzzle assertions on top
(`check_traversal.mjs` re-walks every flag combination).

| map | built | what's there |
|---|---|---|
| `undertide_i` (30×28) | the mouth | The lesson: one junction with **one bell** on the landing (still → west ledge, rung → ladder ledge). Page 1, a Hearth Coal, lamp-diver Ness. Both ledges race home unswitched. The **bell-ringers' islet** sits mid-basin, seen on the first visit. Its race off the west return only wakes once the Bell Galleries are tuned, and it holds a **Starglass Shard** (the come-back). |
| `undertide_ii` (30×30) | Kelp Vaults | The **kelp walk** on foot joins the ladder (I) to the Kelpcrown stair through a wading kelp forest and its pools, so passing through never needs a puzzle. The **fog-glass** sits on an island you see from the stair. Ride to the bell vault (Lumen Drop, lamp-diver Corin), ring the bell, ride again, and the junction turns you onto the island. Page 2. |
| `undertide_iii` (30×30) | Bell Galleries | Seven galleries in one hall of surge. Three bells: **Deep** (NW), **Shoal** (west gallery), **Harbour** (landing). Three junctions plus the tuned shortcut J4. The goal (the stair gallery's ladder) needs Deep + Shoal rung, and the Harbour bell opens the **keeper's ledge** (camp = the **rest point**, a sleeping `heal`). Page 3 (the hint: *"Deep calls, shoal answers, harbour brings them home"*). Net-hand Bryn and keeper Isolde (the Farlamp's second keeper, keeper class). |
| `undertide_iv` (26×30) | the Drowned Stair | No bells. Every race runs **down**, terrace to terrace, with side lanes into two nooks. One long **up-race** on the east wall carries you from the foot to the top in one ride. Page 4, a Hearth Coal, the **2,000w keeper's purse**, the floor's Lumen Drop, lamp-diver Marlo. |
| `farlamp_drowned` (20×22) | the Drowned Lamp | The lantern-room's air pocket: dressed flagstones round the fallen lamp, a moat of shallows, the keeper's desk. **The store** sits behind the sluice: a junction race that only runs inward with `flag:isles_log_4`. Inside is the **Star-chart: Maelstrom** (`chart_maelstrom`, chart_end tier, find-first). |

**Tide-bell Tuning.** The old order is Deep → Shoal → Harbour with nothing rung between
(`flag:undertide_tune_1/2` track the peal). Racing home from the Deep bell passes the Shoal
bell and then the Harbour bell, so the order is the way the tide comes in. Tuned
(`flag:q_isles_bells_tuned`):
- the bell-ringers' tin rises on the landing. It holds III's **Lumen Drop**, so C1's child
  should thank you rather than pay a second drop.
- J4 opens the **shortcut race** from the stair gallery straight home to the well-stair.

**The Keeper's Log.** Keeper **Edda Marrow**'s four pages (`flag:isles_log_1..4`, plus
`flag:isles_log_begun` for the journal) tell the night the deep came up, eleven winters ago.
She sent Driftholm's boats home, kept the lamp, left her fog-glass for whoever came next, and
went up the long stair with a small lamp. She is never said to have drowned. Page 4 opens the
sluice. Both quests are in the journal (`isles_keepers_log`, `isles_bell_tuning`).

**I4.** `script.undertide_fogglass` gives `fog_glass` (key item) and sets
`flag:q_isles_fogglass`.

**I6 + I7.** `script.farlamp_lamp` → `script.farlamp_relight` is the minor→major cadence:
1. Letterbox, then silence.
2. Your vesperlamp carries the prow-flame Fenn lit from the Keystar; you raise the lamp.
3. Warm tint and the lantern sfx. The `undertide_lamp_dark` object swaps to `_lit` mid-scene.
4. `flag:isles_dawn` and `flag:q_isles_done` are set. Flash, shake, then a crossfade to
   `farlamp-relit`. The fog lifts, and the scene says no Gleam is granted ("it isn't that
   kind of light").
5. **Farlume** (#177) rises: `legendaryBattle` lv 68, cooldown 12 (`npc.farlume_resting`),
   terrain `water`, `flag:farlume_caught`.

A miss leaves Farlume by the lamp (`script.farlume_wake`, `requires_flag: isles_dawn`). The
room's ambience swaps on `isles_dawn` (`MapAmbience.when`: warm light pool, motes), and its
music swaps through `music_when`.

**Beds (lv 61–66).** Cave zones sit rect-wide on the galleries; water zones sit on the pools.
`undertidekit.zone` asserts no zone ever covers a race lane. The isles' own kin are Hermiwick,
Fogwisp, Fathomote, rare Beaconclaw and Fathomere. Existing Tide/Stone/Frost/Dark kin fill the
rest: Glostern, Glostrael, Brinewrath, Tidalarch, Prismare, Tideveil (very rare, IV),
Lithonyx, Ferrolith, Stillwarden and Voidmantle. The tables are mirrored in `build_species.py`
`UNDERTIDE_TABLES` and `CURATED_AREAS`, and listed in `progression.mjs TREND_SKIP_AREAS`. The
purse is counted in the post-game leg's `finds`, and the 5 trainers in `BUILT_PAYOUTS`.

**Handshake with C1:** exactly the contract table (`to_gullwrack` (15,27), `to_kelpcrown`
(14,29), `to_driftholm` (15,29) with the contract landings). The cave side owns the three
surface edges in `graph.ts` (bidirectional), so C1 should not add reverse edges.

**Audio/art from D:** `undertide.mp3`, `farlamp-relit.mp3`, `undertide-a.webp` and
`farlamp-drowned-a.webp` are referenced; until D lands, the music is silent and the battle
backdrop is blank.

---

## Part II — The Ashfall Shelf (main path, Cinderhead → Galehigh)

> **BUILT (2026-10, Lane A).** As specced, plus the v3 panel revisions. Details and validation
> hooks: [`03-north.md`](./03-north.md) "The Ashfall Shelf". Mira's recommended party is now 30
> (the Scarp and the shelf carry 28–33).

### Problem
After Otho (ace 28) the player walks Cinderhead Deep (cave) → **one** map, Cinderwind Scarp
(24×28, lv 28–31) → Galehigh (Mira, ace 34). That's three caves in a row, then six levels of
curve on a single screen of climbing. It's the thinnest stretch of the main path.

### Fix: Scarp I → Ashfall Shelf → Galehigh, with a return compressor + a come-back spur

| id | name | at | size | role | levels |
|---|---|---|---|---|---|
| `cinderwind_scarp` (kept) | Cinderwind Scarp | (93,-203) | 24×28 | Its north edge now opens into the Ashfall Shelf. Its east cut to Galehigh is blocked by a **rockfall** (gated warps + boulder objects, `blocked_ref` = a hauler's script: "up and round by the Ashfall, love"). | 28–30 |
| `cinderwind_ashfall` (new) | The Ashfall Shelf | (93,-231) | 24×28 | Daylight after the caves: a high shelf where Cinderhead's slag was tipped for a century, so the grass grows grey out of the ash. The haulers' camp (brazier **rest point**), two sight trainers, a ledge loop, a cache. East edge joins Galehigh's west edge, Ashfall rows 18–27 ↔ Galehigh rows 0–9. | 30–33 |
| `cinderwind_kiln` (new) | Kiln Gully | portal | 22×18 | An old lamp-glass kiln in the shelf's cliff, behind an **updraft vent** (`updraft_kite`), so you come back after Galehigh. Stone/Ember kin lv 33–35, a Beacon charge, a Star-chart, kiln lore. | 33–35 |

**Panel revisions (v3, [`expansion-panel.md`](../../reviews/expansion-panel.md), adopted):**
- **Stonebark (#63, Verdant/Stone, never wild until now)** is the Ashfall rare (about 5%).
- **"The Last Pane"** side quest. The kiln-wright's family keep the cold kiln. Kiln Gully's last
  pane of lamp-glass goes up to Galehigh's kite-maker; the reward is wicks plus the pane set in
  Galehigh's lamp (a visible change). Flags `flag:q_north_pane`, `flag:q_north_pane_done`.
- A **Windward vista** from the shelf, and a **Kite-gated crossing** from the shelf's upper east
  edge (Ashfall rows 0–17 ↔ Windward Stair I rows 22–39) as a later shortcut.
- A **hidden slag nook**: seen from the upper ledge, reached by a one-way drop, with an
  ash-buried cache.

**The rockfall is the return compressor.** The first time you reach Galehigh (the step_on band
on the new west landing) the Galehigh haulers clear it: `flag:scarp_rockfall_clear`, derived
ANY_OF with `gleam:storm` (FlagStore `ANY_OF` + `audit_journey.py DERIVED_ANY`), so old saves
past Galehigh find it open. After that, Cinderhead ↔ Galehigh is the short way again.

**Validation hooks:** `audit_journey` GOLDEN unchanged (no beat moves); `progression.mjs` gets the
Ashfall leg (2 route trainers + the new band); `audit_region` band step ≤4 (Deep 24–27 →
Scarp 28–30 → Ashfall 30–33 → Galehigh); `world_geometry --check` + `world_layout.py`; music
`cinderwind-ashfall` (classic + remaster); a battle backdrop.

---

## Build contract (the lanes that built this round agree on these exactly)

**Lanes:**
- **A** = Part II (Ashfall Shelf + Kiln Gully, its music/backdrop/trainers).
- **B** = kin #172–177.
- **C1** = isles overworld + Driftholm + interiors + mainland hooks.
- **C2** = Undertide I–IV + the Drowned Lamp + Farlume + the relight.
- **D** = isles audio + skiff sheet + isles battle backdrops.

**Cross-map warps (C1 owns the surface side, C2 the cave side; landings sit ON the return warp's neighbour per audit_warps):**

| From | Warp id @ tile | To | Landing |
|---|---|---|---|
| `farlamp_gullwrack` | `to_undertide` @ (13,9) | `undertide_i` | (15,26) facing up |
| `undertide_i` | `to_gullwrack` @ (15,27) | `farlamp_gullwrack` | (13,10) facing down |
| `farlamp_kelpcrown` | `to_undertide` @ (10,9) | `undertide_ii` | (14,28) facing up |
| `undertide_ii` | `to_kelpcrown` @ (14,29) | `farlamp_kelpcrown` | (10,10) facing down |
| `driftholm` | `to_wellstair` @ (16,12), `requires_flag: flag:q_isles_wellstair`, `blocked_ref` = Elder Creel's script | `undertide_iii` | (15,28) facing up |
| `undertide_iii` | `to_driftholm` @ (15,29) | `driftholm` | (16,13) facing down |

A lane may move its own side by ±2 tiles if the art forces it, and must then report the new tile.

**Files:**
- Scripts: A `content/regions/ashfall.ts`; C1 `content/regions/farlamp.ts`; C2 `content/regions/undertide.ts`.
- Music (served): `assets/audio/music/cinderwind-ashfall.mp3` (A); `farlamp-sound.mp3`, `driftholm.mp3`, `driftholm-dawn.mp3` (Driftholm's `music_when` after `flag:isles_dawn`), `undertide.mp3` and `farlamp-relit.mp3` (all D; maps reference them now and `MusicDirector` tolerates a missing file).
- Battle backdrops: A `ashfall-a.webp`, `kiln-a.webp`; D `farlamp-sea-a.webp`, `farlamp-isle-a.webp`, `undertide-a.webp`, `farlamp-drowned-a.webp`.
- Player skiff sheet: D `player_indi_skiff`.

**Items:**
- C1: `farlamp_skiff` (key), `deep_charm` (charge, `condition` = deep-water-met, priced 900w, sold at the Driftholm chandlery after `flag:isles_dawn`).
- C2: `fog_glass` (key item; giving it also sets `flag:q_isles_fogglass`).
- Driftletters are flags `flag:driftletter_1..5`, not items.

**Flags:** as in §3. C2 sets `flag:isles_dawn` + `flag:q_isles_done`. C1 maps react to `flag:isles_dawn`: fog-bank objects get `hidden_when_flag`, day-form NPC swaps, `music_when`.

**Levels:** as in §4. Isles beds go in `progression.mjs TREND_SKIP_AREAS` (optional post-game).

---

## Part III — Lowtinder & Tinderwick Bay (the reason to go home; Tidecall, mid-game)

> Panel plan v3, scored 87.5 ([`expansion-panel.md`](../../reviews/expansion-panel.md)).

### Lore
Old Tinderwick stood on the shore until **the winter the water rose** (about 40 years ago,
story-bible §12: the same winter the Sunken Solarium flooded). The town moved up the bluff and
the old one went under the bay: **Lowtinder**. Its last Lampwarden, **Grandmother Ottery
Tallow** (Brisa's grandmother), never left. She lives cosily in the dry upper floor of the old
lamp-house, keeping a small lamp the town above forgot. Brisa visits on Sundays and doesn't
talk about it.

### The player promise
1. **Seen from minute one.** Off Tinderwick's beach, roof-ridges and a drowned bell-tower show
   above the water (objects on the bay's edge), and an old fisher on the sand says "that's where
   the town *was*." Andrew's Tide-stage hint adds "and home's got a secret now you can swim."
2. **Tidecall opens it** (gift 2): the first reason to walk back to the start.
3. **Coming round at home:** the Bell Cellar's far end climbs up **Tinderwick's own old well**,
   a one-way shortcut into the home town square (step_on from the cellar; the well is a solid
   object in town).
4. **The bell comes home.** "The Town Bell": raise the old bell from Cellar B2 (it needs the
   cellar's winch-key from B1), and it hangs in Tinderwick's square. A flag-swapped object, a
   short ceremony, Brisa's line, and the bell rings on the town's festival.
5. **Three returns:**
   1. **Tidecall** (about lv 17–22).
   2. **Brightlight** (`flag:lamplight_brightlight`, 4 Gleams) reveals the lamp-school's
      moss-garden room, with **Mossmantle** (#39, Light/Verdant, never wild until now).
   3. **The skiff** (post-game) reaches the **outer deep reef**: row the grandmother out to see
      the old Tinder Light, then battle her (ace 66, rematchable).

### Maps (world coordinates; north-up)

| id | name | kind | at | size | role | levels |
|---|---|---|---|---|---|---|
| `tinderwick_bay` | Tinderwick Bay | route (sea) | (0,24) | 28×28 | Its top edge is Tinderwick's beach, so Tinderwick's south-edge swim warps need Tidecall; build_tinderwick.py owns that side. Shallow reef islets, tide-pools, sea-grass `water` beds, two swimmer trainers, caches, drowned roof-ridges. East → Lowtinder. The OUTER rows are DEEP (the reef, skiff-only) with the grandmother's reef scene at a rocky islet. | 17–20 |
| `lowtinder` | Lowtinder | route | (28,24) | 26×28 | Drowned streets on a tidal shelf: half-sunk houses, rooftops with one-way drops (a loop), the old lamp-school (Brightlight room) and the lamp-house with the grandmother. **Embrift** (#14) is the rare here. Bell Cellar mouth. | 18–21 |
| `lowtinder_cellar` | The Bell Cellar | cave | portal | 24×20 | Flooded cellars under the lamp-house, with the winch-key. Ladder down. | 19–22 |
| `lowtinder_cellar_b2` | The Bell Cellar — the Belfry Pit | cave | portal | 24×22 | The sunken belfry and the bell (the raise scene), a Lumen Drop, and the climb to **Tinderwick's well** (one-way out into the square). | 20–23 |
| `lowtinder_school` | the old lamp-school | interior | — | roomkit | Its moss-garden room is shown by Brightlight. | — |

Plus the grandmother's lamp-house interior (`lowtinder_lamphouse`, a rest point).

**Flags:**
- `flag:q_lowtinder` (first meeting with the grandmother)
- `flag:lowtinder_winch_key`
- `flag:q_lowtinder_bell` (bell raised)
- `flag:q_lowtinder_bell_home` (hung in Tinderwick)
- `flag:lowtinder_reef_rowed`
- `flag:lowtinder_grandmother_beaten`

Journal: "The Town Bell", "The Old Tinder Light" (post-game).

**Audio:**
- `lowtinder`: the Tinderwick theme drowned. The same melody, slowed and underwater-soft, with a
  music-box bell (classic + remaster).
- `bell-cellar` (sparse cave).
- The reef battle uses an existing warden theme.

**Art:**
- Drowned roofs and the bell-tower.
- Lowtinder houses (half-sunk).
- The old bell (raised and hung).
- The well (in Tinderwick).
- Battle backdrops `lowtinder-a.webp`, `bell-cellar-a.webp`.
- The grandmother's battle sprite (the trainer-intro beat, `content/trainerArt.ts`) and her walk-sheet.

**Balance:** optional mid-game beds go in `TREND_SKIP_AREAS`; prices and payouts follow the class
formula (her ace 66 = warden-class rematch).

### Deep backtrack (part of this lane)
Skiff-only caches in existing deep water. Each is an islet or a buoy-cache on deep water,
`requires` nothing but reachability by `deepdive`, placed through the owning builder plus the
four runners:
- Gullcry Rock's outer deep
- Pearlmoor harbour
- Dimglass Coast II
- Vigil Hearthfall
- Tinderwick Bay's reef

Lane: **E** (Tinderwick Bay, Lowtinder, cellar, the well, the bell, the grandmother, deep backtrack).
