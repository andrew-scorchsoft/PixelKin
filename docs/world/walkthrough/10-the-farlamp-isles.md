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
| Letters (any time) | 5 shores | Driftletters: Dimglass Coast I strand, Gullcry Rock, the Pearlmoor breakwater foot, the Glassmere shallows, the Drownlight Beacon shingle. Each is readable lore and a pickup. | `flag:driftletter_1..5`; `flag:driftletters_3` **derives** (FlagStore: ≥3 of 5) |
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
| `undertide_i` | The Undertide | cave | portal | 30×28 | Under Gullwrack. Shallow channels + **tide-races** (`flows` rail on water, flag-switched by tide-bells). Ladder down to II. | 61–63 |
| `undertide_ii` | The Undertide — Kelp Vaults | cave | portal | 30×30 | Joins Gullwrack to Kelpcrown underground. The **fog-glass** at its heart. | 61–64 |
| `undertide_iii` | The Undertide — Bell Galleries | cave | portal | 30×30 | From Driftholm's well-stair. The big tide-bell maze: three bells, every race ends on a ledge in every bell state (the Old Seams invariant). | 62–65 |
| `undertide_iv` | The Undertide — the Drowned Stair | cave | portal | 26×30 | The last descent; the keeper's logbook pages; the door to the lamp. | 63–66 |
| `farlamp_drowned` | The Drowned Lamp | cave | portal | 20×22 | The sunken lighthouse floor, an air pocket under the sea. Relight → Farlume. | set-piece |

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

**Audio** (classic chip via generate-midi + a remaster via `remaster_track.py`; battles stay
classic-only): `farlamp-sound` (rowing on a long swell), `driftholm` (an island town hymn
in a minor mode that turns major after `isles_dawn` via `music_when`), `undertide` (sea-cave
drips and bells), `farlamp-relit` (the relight, the emotional cue). Farlume uses the
Three Hours' legendary battle cue.

**Art:** skiff walk-sheet (`player_indi_skiff`, the 4×4 layout; procedural fallback), Driftholm
buildings + boathouse + well-stair, the drowned lighthouse, lantern-buoys, bottle pickup,
tide-bell, fog-glass, battle backdrops (sea, isle, Undertide, the Drowned Lamp).

---

## Part II — The Ashfall Shelf (main path, Cinderhead → Galehigh)

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

**The rockfall is the return compressor.** The first time you reach Galehigh (the step_on band
on the new west landing) the Galehigh haulers clear it: `flag:scarp_rockfall_clear`, derived
ANY_OF with `gleam:storm` (FlagStore `ANY_OF` + `audit_journey.py DERIVED_ANY`), so old saves
past Galehigh find it open. After that, Cinderhead ↔ Galehigh is the short way again.

**Validation hooks:** `audit_journey` GOLDEN unchanged (no beat moves); `progression.mjs` gets the
Ashfall leg (2 route trainers + the new band); `audit_region` band step ≤4 (Deep 24–27 →
Scarp 28–30 → Ashfall 30–33 → Galehigh); `world_geometry --check` + `world_layout.py`; music
`cinderwind-ashfall` (classic + remaster); a battle backdrop.
