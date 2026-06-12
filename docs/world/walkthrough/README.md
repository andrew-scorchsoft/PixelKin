# PixelKin — Walkthrough Blueprint: *The Long Dusk*

> The **canonical user-journey** for PixelKin, written before the game is built. It is two
> things at once: the **"spirit of things"** — the cohesive playthrough every future map,
> cutscene, trainer, and encounter table should add up to — and an **acceptance spec** every
> generated area is validated against. If the journey here is strong and cohesive, the game
> mechanic around it is strong.
>
> Read **after** [`story-bible.md`](../story-bible.md) (the plot & cast),
> [`atlas.md`](../atlas.md) (the 14 areas + the 43-node graph), and
> [`level-design.md`](../level-design.md) (how a map is authored). All content original per
> [`../../VISION.md`](../../../VISION.md). Canon vocabulary throughout: **kin, Lumenary,
> Lampwarden, Gleam, Lantern Gift, vesperlamp, kindling, the Hollowing**.

This file is the **spine**. The region files carry the beat-by-beat walkthrough:

- [`01-south.md`](./01-south.md) — Tinderwick · Dimglass Coast · Pearlmoor Quay (+ spurs)
- [`02-east.md`](./02-east.md) — Saltreach Fen · Lowleaf Hollow · Cinderhead Mine (+ spurs)
- [`03-north.md`](./03-north.md) — Galehigh Terraces · Windward Stair · Pale Vault Glacier (+ spurs)
- [`04-west.md`](./04-west.md) — Hushfrost Pass · Sunken Solarium · Sunvault Climb · Nightreach (+ spurs)
- [`05-central-endgame.md`](./05-central-endgame.md) — Vesper Crossroads · Penumbra Ring · Umbral Spire
- [`06-postgame.md`](./06-postgame.md) — Dawnstead · day-forms · Còr's resolution
- [`07-the-three.md`](./07-the-three.md) — the Three Hours · legendary triad offshoots (Tideglass Cavern · the Hourfold · the Unrisen Stair)

---

## 0. Three rules that prevent drift (read first)

These three were the highest-risk traps in the design audit. They are **binding** on every
region file:

1. **A Lumenary is never gated by the ability it grants.** The gate ability named for an area
   (atlas "Gate:" line) applies only to that area's **onward route-segment II and its
   spurs/depths — never to the town or Lumenary itself.** (Pale Vault's Lumenary grants
   Emberward, so it *must* be reachable without Emberward; Lowleaf's grants Glimmerstep; etc.)
   Corollary for the **earned Gleam loops** (§5): the earned thing is always a *key, pass,
   errand or trial* — never the region's own Gift. A loop MAY lean on a Gift earned in an
   EARLIER region that the main path already requires (e.g. Tidecall at the Solarium).
2. **Geography ≠ progress; the eight Gleams are the clock.** A few back-door edges exist (e.g.
   the Coldfog detour can reach Nightreach with only Emberward — `graph.ts:141`). The **main
   path is the rim** (always reach Nightreach via Sunvault Climb / the Solar Gleam first);
   **Coldfog Marches is an optional outer detour** taken late. So **never assume an area's
   neighbour-state from its map position** — tie lighting (Arc D), curve, and dialogue to the
   player's **Gleam count / progression flags**, not to which tile they walked in from.
3. **Close every flag and gate you open.** Use the exact flag strings in §2. The two late
   shortcuts use `flag:shortcut_windward` (set on reaching the Windward Stair II crags — a
   ledge-drop back to Galehigh) and `flag:shortcut_mine` (set on reaching Cinderhead Deep's
   far side — a sealed door opened from inside, re-linking the mine to the hub). Whichever
   region introduces a shortcut/spur must set its flag. **Quest flags** follow the
   convention `flag:q_<region>_<short>` (e.g. `flag:q_south_bell`) and the same discipline:
   every `flag:q_*` a region file opens must be consumed by a named trigger/NPC swap in
   that file. (South's built Beacon flags — `flag:beacon_quest`, `flag:has_beacon_wick` —
   predate the convention and stay grandfathered.)

> **Counts, reconciled (so the numbers don't trip you):** **9 valleys** (the lore framing) =
> 8 Lumenary towns + Dawnstead; **14 area cards** in `atlas.md` §2; **43 graph nodes** in
> `graph.ts` (the cards split into segments + spurs + landmarks + hub + central). All three
> describe the same world at different resolutions.

> **4. Tell it cinematically — delivery is part of the spec.** A beat isn't done when the
> words are written; it's done when it *lands*. [`cinematics.md`](../cinematics.md) is
> **binding**: cold opens, portraits, the music-as-drama cadence (crossfade on change,
> `silence` for dread, `gleam`→minor-major festival swell), and the dark-but-aspirational
> tone rules. The **South first hour is the built worked example** — copy its scripts
> (`src/game/content/scripts.ts`, `cinematics.ts`) when staging any later beat. Each region
> file carries a **"Cinematic staging"** note per major beat (§7); a Gleam without the swell,
> or a Hollowing reveal without the quiet, is a content bug.

---

## 1. How to use this document

- **For writers/designers:** the spine fixes the *plot beats, the five interlocking arcs, the
  level curve, and the order mechanics come online*. Region files must honour all of it.
  Anything not fixed here is the region's to invent — in voice with §10.
- **For map/content authors & validators:** each area section in the region files ends with
  **Validation hooks** — the concrete `map id`s, `requires_ability` / `requires_flag` /
  `sets_flags`, encounter terrain + element + level band, and NPC/Lumenary placements a built
  area must contain. To "validate a map against the walkthrough" is to check those hooks
  against the map JSON, `graph.ts`, and the content registries (see §9).
- **Source of truth precedence:** `src/game/data/world/graph.ts` and `types.ts` win on
  *connectivity and schema*; `atlas.md`/`story-bible.md` win on *lore*; this file wins on
  *sequence, pacing, and which beat lands where*.

---

## 2. The golden thread (plot beats → flags)

The plot is the journey. Eight Gleams relight eight constellations; each pair completes a
quadrant of the **Skyweave Crown**; the completed Crown parts the **Penumbra** and opens the
**Umbral Spire**. The whole arc warms from blue-hour dusk toward true dawn.

| # | Beat | Where | Earns | Sets flags (canon) |
|---|------|-------|-------|--------------------|
| 0 | Wayfaring begins — the **satchel errand**: Fenn waits at the Crossroads waystone; fetch his satchel from town and he gifts the vesperlamp + starter at the waystone | Tinderwick → Vesper Crossroads | starter, vesperlamp | `flag:fenn_errand`, `flag:has_satchel`, `flag:has_vesperlamp`, `flag:has_starter` |
| 1 | **Ember Gleam** — Brisa Tallow vouches your bond (gentle first Lumenary) | Tinderwick | Gleam: Ember | `gleam:ember` |
| — | **Inciting incident** — a constellation winks out on your first night | Dimglass Coast | — | `flag:dusk_begins` |
| 2 | **Tide Gleam** + **Tidecall** | Pearlmoor Quay | Gleam: Tide, Tidecall | `gleam:tide`, ability `tidecall`, → `flag:crown_south` |
| 3 | **Verdant Gleam** + **Glimmerstep** | Lowleaf Hollow | Gleam: Verdant, Glimmerstep | `gleam:verdant`, ability `glimmerstep` |
| — | **First Hollowing contact** — a drained site; restore a sleeping luminous kin | east region | — | `flag:met_hollowing` |
| 4 | **Stone Gleam** | Cinderhead Mine | Gleam: Stone | `gleam:stone`, → `flag:crown_east` |
| 5 | **Storm Gleam** + **Updraft Kite** | Galehigh Terraces | Gleam: Storm, Updraft Kite | `gleam:storm`, ability `updraft_kite` |
| — | **Còr appears** — courteous, sad, persuasive; makes his case (no battle) | north region | — | `flag:met_cor` |
| 6 | **Frost Gleam** + **Emberward** | Pale Vault Glacier | Gleam: Frost, Emberward | `gleam:frost`, ability `emberward`, → `flag:crown_north` |
| 7 | **Solar Gleam** + **Sunsketch** | Sunken Solarium | Gleam: Solar, Sunsketch | `gleam:solar`, ability `sunsketch` |
| — | **The Great Null named** — Coldfog/Stillworks reveal the stakes | west region | — | `flag:great_null_known` |
| 8 | **Lunar Gleam** + **Starreach** | Nightreach Observatory | Gleam: Lunar, Starreach | `gleam:lunar`, ability `starreach`, → `flag:crown_west`, → `flag:hub_unlocked` |
| 9 | **The Spire opens** — Crown complete, Penumbra parts, four roads | Vesper Crossroads → Penumbra Ring | — | (hub roads live on `hub_unlocked`) |
| 10 | **Climax** — confront Còr's Great Null; relight the **Keystar** (Keylumen) | Umbral Spire | — | `flag:keystar_relit` |
| 11 | **Dawn** — the long night breaks; Vesperholm wakes | → Dawnstead | — | `flag:dawn` |

> **Flag-naming note.** `flag:crown_south/east/north/west` and `flag:hub_unlocked` are the
> only names already wired in `graph.ts`; the engine sets `crown_*` when both of a quadrant's
> Gleams are held. The `gleam:*`, `flag:dusk_begins`, `flag:met_hollowing`, `flag:met_cor`,
> `flag:great_null_known`, `flag:keystar_relit`, `flag:dawn` keys are **introduced by this
> blueprint** — region files must use these exact strings so beats and gates line up. Two
> more already in `graph.ts`, owned by region files: **`flag:shortcut_windward`** (north) and
> **`flag:shortcut_mine`** (east) — see §0 rule 3 for where each is set.

---

## 3. The five interlocking arcs

Five threads run through the eight-Gleam spine. Each beat is assigned to an area so the
region files stay consistent — **a region file may not move or duplicate another region's
arc beat.**

### Arc A — Wren, the Rival-Friend
A warm, competitive fellow Wayfarer from Tinderwick. **Name: Wren** (gender-neutral). Wren
picks the starter that beats yours (the Ember→Verdant→Tide→Ember triangle), and keeps
crossing your path. Wren externalises the game's moral question: *do the Hollowing have a
point?*

| Beat | Area | Note |
|------|------|------|
| A1 Meet & choose | Tinderwick | Friendly; "race you to complete the map" |
| A2 First friendly battle | Dimglass Coast | Teaches trainer battles; Wren ~2 levels under you |
| A3 Shaken | Lowleaf/Cinderhead (east) | After the first drained site, Wren voices sympathy for the Hollowing |
| A4 The wobble | Pale Vault (north) | At a low point Wren *nearly* joins the Hollowing; a hard battle (Wren is deliberately **at/above** the player's level here — the one beat that breaks the usual "Wren ~2 under you" pattern; don't "correct" it), then they walk off unsure |
| A5 Return | West / Spire approach | Wren comes back having reasoned it through; helps at the Spire |
| A6 Resolved | Dawnstead (post-game) | Wren in daylight, at peace; optional rematch |

### Arc B — The Hollowing & Warden Còr (monotonic escalation)
Never cartoonish; grief dressed as mercy. The threat ramps strictly forward — no region may
show the Hollowing *weaker* than an earlier region.

| Stage | Area | What the player sees |
|-------|------|----------------------|
| B1 Rumour | South | A far constellation winks out (`dusk_begins`); NPCs speak of towns "gone quiet" |
| B2 First contact + first glimpse of Còr | East | A small drained site + a sleeping luminous kin; gentle acolytes who *believe they help*; learn the names "the Hollowing", "Warden Còr"; **a Còr foreshadow** — a distant cowled figure, or a left-behind letter in his courteous voice (so the North reveal pays off a build-up, not a cold open) (`met_hollowing`) |
| B3 The man himself | North | Còr appears in person — courteous, sad, persuasive; states his case; **no battle** (`met_cor`) |
| B4 Full scale | West | Coldfog Marches (the drained land) + Hollowfen Stillworks (the null-works set-piece); the **Great Null** aimed at the **Keystar** is named (`great_null_known`) |
| B5 Climax | Umbral Spire | Confront the Great Null; relight the Keystar; resolve by *out-remembering*, not force |

### Arc C — Star-tender Fenn (the mentor) & the shared past *(canon extension — see §8)*
Fenn (reuse/rename the `professor_fenn` sprite) gifts the lamp and starter, then recurs at
milestones to explain the **Skyweave** and the celestial calendar, and to hand over better
Lamps/key items. **Canon extension locked here:** Fenn and Còr were once fellow star-tenders
— two answers to the same loss (Fenn's quiet hope, Còr's grief). This gives the climax its
weight and a reason Fenn understands Còr.

| Beat | Area |
|------|------|
| C1 Gift the lamp & starter (the satchel errand; ceremony at the waystone) | Tinderwick → Vesper Crossroads |
| C2 Explain the Skyweave & the winking-out | South (after `dusk_begins`) |
| C3 Reveal the shared past with Còr | North (around `met_cor`) |
| C4 Counsel before the Spire | Vesper Crossroads / Nightreach |

### Arc D — The Celestial Calendar (dusk → dawn)
The global lighting warms one quadrant at a time. **Each region file must open visibly
lighter than the previous region** (south = deep blue hour → west = near-dawn pallor), the
vesperlamp brighter, and note any flag-gated encounter-table shift when its constellation
relights. Day-forms arrive only post-`dawn` (see [`06-postgame.md`](./06-postgame.md)). The
arc's **mechanical, player-held expression is Lamplight** (§5): the vesperlamp's reveal-radius
climbs a tier roughly every two Gleams, so the player literally *carries the returning dawn* —
the world brightens both overhead (constellations) and in-hand (the lamp).

### Arc E — Town Festivals
Every Lumenary town wraps its Gleam in a festival — *belonging, not conquest*. Each is a
small, missable-but-don't-miss set-piece the region file stages around the Lumenary:

| Town | Festival |
|------|----------|
| Tinderwick | the **Lantern-fair** |
| Pearlmoor Quay | the **Tide-blessing** |
| Lowleaf Hollow | the **Glowmoss Bloom** |
| Cinderhead Mine | the **Lamp-down vigil** (miners' light) |
| Galehigh Terraces | the **Kite-rising** |
| Pale Vault Glacier | the **Aurora-watch** |
| Sunken Solarium | the **Last-Warm-Day** |
| Nightreach Observatory | the **Star-vigil** |

---

## 4. Global pacing & level curve

A ~+6-levels-per-Gleam curve. **Recommended party** = where a prepared player sits on entry;
**Lumenary ace** = the Lampwarden's strongest kin. Region files set encounter level bands to
keep this continuous across boundaries (no cliffs, no dead zones).

| Stop | Recommended party | Lumenary (type) — ace | Gift earned |
|------|------------------|------------------------|-------------|
| Tinderwick | start 5 | **Brisa Tallow** (Ember) — ~10 | — |
| Dimglass Coast I→II | 5 → 10 | — | (teases Tidecall/Glimmerstep) |
| Pearlmoor Quay | 12 | **Reyl Wash** (Tide) — ~16 | **Tidecall** |
| Saltreach Fen I→II | 16 → 18 | — | — |
| Lowleaf Hollow | 18 | **Sable Quill** (Verdant) — ~22 | **Glimmerstep** |
| Cinderhead Mine/Deep | 22 | **Otho Grist** (Stone) — ~28 | — |
| Galehigh Terraces | 28 | **Mira Vael** (Storm) — ~34 | **Updraft Kite** |
| Windward Stair I→II | 34 → 36 | — | — |
| Pale Vault Glacier | 36 | **Ysolde Frost** (Frost) — ~40 | **Emberward** |
| Hushfrost Pass I→II | 40 → 42 | — | — |
| Sunken Solarium | 42 | **Lucan Pyre** (Solar) — ~46 | **Sunsketch** |
| Sunvault Climb I→II | 46 → 48 | — | — |
| Nightreach Observatory | 48 | **Nessa Cole** (Lunar) — ~52 | **Starreach** |
| Umbral Spire | 52 → 56 | **Warden Còr** — ~56; **Keylumen** (Keystar) ~55 | — |
| Dawnstead / post-game | 55 – 65 | (rematches, day-forms) | — |

**Soft-gate the first Lumenary:** Brisa won't hold the bond-test until the player has caught
at least one wild kin (sets a small flag in the region file) — so a lone level-5 starter
never faces an ace-10 Lumenary. This is the tutorial's natural "go catch a kin first" beat.

**The one deliberate wall:** Otho Grist (Stone, ~28) is the first genuinely punishing
Lumenary — the largest party-to-ace gap in the curve. This is intentional (Cinderhead's
"trusts what endures the dark" theme), so Cinderhead's deep-gallery encounters should sit at
the upper end of their band (24–27) to let a careful player close the gap; do not under-level
the mine or it becomes a cliff. *(The Descent Vigil earned loop — §5 — institutionalises
this: Otho's vigil-lamp errand sends the player into exactly that 24–27 band before the
bond-test, the same way the Beacon fixed the 5-vs-10 gap.)*

**The collinearity rule (binding on earned loops and quests):** every errand reuses ground
the player walks anyway — the region's own routes, dungeon legs and town maps, inside that
stop's existing level band from the table above. An earned loop must never force a route
traversal the main path doesn't already require; if a design wants one, it's the wrong
design for that region.

**The curve is now economically modelled (2026-06).** This table's reachability — and the
wick economy that rides on it — is validated end-to-end by `tools/balance/progression.mjs`
against the **per-region battle & earnings budget** in
[`docs/mechanics/10-economy.md`](../../mechanics/10-economy.md) §8 (binding on region
authors: trainer counts/classes per segment, quest wicks, valuables, shop stock). Change a
band, a roster, a price, or a payout → update the model's JOURNEY leg and re-run; it fails
loudly when the curve or the wallet breaks. (Tuning fallout already locked: XP yield is
`bst·level/20`, trainer battles ×1.5, **a catch pays like a knock-out** — and at Otho the
post-Vigil expectation is ~26 vs his ace 28, the designed wall.)

---

## 5. Mechanic-introduction cadence & how exploration widens

The genre's joy is *the map reopening itself* as you gain Lantern Gifts. Each Gift is
introduced **locally** (it solves the area you're in) and then **retroactively** unlocks
spurs/landmarks/shortcuts across the *whole* map — the reason to keep a mental list and
backtrack. Region files must place a **"now accessible"** callout wherever a just-earned Gift
opens old content, and a **"come back later"** tag wherever content waits on a Gift not yet
earned.

### What teaches what

| Stop | New player-facing mechanic |
|------|----------------------------|
| Tinderwick | move · talk · interact · enter buildings · first wild battle (verge) |
| Dimglass Coast | **catching** (vesperlamp) · type basics · first trainer battle (Wren) · Gift *teases* |
| Pearlmoor | **Tidecall** (cross shallow night-water) |
| Lowleaf | **Glimmerstep** (enter dark caves/woods) · **kindling** likely first fires here (starter ~16–20) |
| Cinderhead | deep-cave navigation · Stone bulk/strategy |
| Galehigh | **Updraft Kite** (scale terraces, glide gaps) |
| Pale Vault | **Emberward** (burn through coldfog) |
| Sunken Solarium | **Sunsketch** (bloom sun-vine bridges) |
| Nightreach | **Starreach** (step across voids of pure dark — the endgame traversal) |

### Exploration-widening table (ability → what it reopens, mapwide)

From `graph.ts` edges + atlas §3. Each Gift, once earned, opens these — region files cross-link them.

| Gift (earned at) | Opens immediately | Reopens earlier/later content |
|------------------|-------------------|-------------------------------|
| **Tidecall** (Pearlmoor) | Pearlmoor shoals; Saltreach Fen II | **Gullcry Rock** (Dimglass spur); **Sunkbell Shallows** (Saltreach spur); flooded halls in Sunken Solarium |
| **Glimmerstep** (Lowleaf) | Glowmoss Deep; Cinderhead Mine/Deep | **Tideglass Cavern** (Dimglass landmark); **Spore Grotto** (Glowmoss spur) — (Hollowfen Stillworks' *inner door* is Glimmerstep too, but it's a late outer landmark — see the dedicated row below) |
| **Updraft Kite** (Galehigh) | Windward Stair II; high terraces | **Wind-Eye** (Galehigh landmark); **Thunderroost** (Windward spur); the *Windward→Galehigh* drop **shortcut** |
| **Emberward** (Pale Vault) | Hushfrost Pass II; Pale Vault *deep ice & spurs* (**not** the Lumenary — §0 rule 1) | **Aurora Hollow** (Hushfrost spur); **Coldfog Marches II** (the deep coldfog past the hub-side segment I); **Drownlight Beacon** (Coldfog II spur) |
| **Sunsketch** (Sunken Solarium) | Sunvault Climb II; sun-vine routes | **Helia Vault** (Sunvault spur) |
| **Glimmerstep** (also, late) | — | **Hollowfen Stillworks** (its inner door opens with Glimmerstep, but the works sit off **Coldfog Marches II**, so you need **Emberward** to be there at all — a late outer landmark, not an east-game one) |
| **Starreach** (Nightreach) | Penumbra Ring final crossings; Umbral Spire ascent | **Crystoll Vault** (Cinderhead late spur, `[LATER]`); **Starwell** (Penumbra Ring landmark, `[LATER]`) |
| **`shortcut_mine`** flag | — | *Cinderhead Deep → Vesper Crossroads* permanent re-link |
| **`hub_unlocked`** flag | four cardinal roads Crossroads → Spire | the slow outer loop becomes a fast four-way wheel |

### Engine mechanics the journey assumes (dependencies, not new design)
The battle beats from ~Pearlmoor on assume **status conditions** (`scorch · drench · numb ·
doze · blight · dazzle · chill`) are live — still on the engine roadmap
(`docs/mechanics/battle-runtime-plan.md` Part B), so region files may write battles that
*use* status but should flag the dependency. The **move-learning prompt IS live** (Part A,
2026-06: `ui/MoveLearnPrompt`, shared by level-ups and Star-charts), as are the **wick
economy, shops and Star-charts** (`10-economy.md`).

### The standing per-region kit (BUILT in South — every region copies it)
South established the small, repeatable mechanics every region is expected to ship, all
pure data (see `tools/maps/build_*.py` + `src/game/content/` for the worked patterns):
- **Rest points** — each town keeps one full-heal: an inn keeper or hearth/bed whose
  NPC/trigger `dialogue_ref` is a *script* ending in the `heal` op (`script.inn_rest`,
  `script.home_rest`). Never leave a Lumenary town without one.
- **Shop kits + the open counter (coin is WIRED — wicks)** — the keeper still hands the
  one-time kit via a script + flag pair, but the post-kit keeper now *trades*: their
  dialogue_ref is a script ending in `{ op: 'shop', shop: '<id>' }` (ShopDef in
  `content/shops.ts`; prices on the ItemDefs). Trainer wins pay wicks
  (`TrainerDef.payout` = class rate × ace level), quests/valuables top up the purse, and
  **Star-charts** (single-use taught-move items) are the aspirational sink. Stocking rules,
  payout classes and the per-region budget: [`10-economy.md`](../../mechanics/10-economy.md).
- **Item caches** — 2–3 ground pickups per route: `sprite:'item_cache'` NPCs whose script
  gives the item, says the find, sets `flag:picked_*`; `hidden_when_flag` removes them live.
  **Vary the contents** (2026-06): most caches hold consumables (balms, lamp charges), but
  each region should also place **1–2 valuable caches** (Wax Cake / Moth-amber / Starglass
  Shard — found-to-sell, the genre's nugget) and **one loose-wicks cache** (`giveMoney`,
  ~half a route-trainer payout) — finding money in the grass is half the joy of poking
  about. Caches off the lane > caches on it; dungeons hide the better ones a choke away.
- **Festival payoff NPCs** — each Gleam adds 2+ `requires_flag:'gleam:<element>'` townsfolk
  (Arc E: belonging, not conquest). Cheap, and the town visibly *answers* the victory.
- **Witness beats** — pair every story `step_on` cutscene with a flag-gated NPC who reacts
  afterwards, so the beat lands on a person.
- **The catch-first gate** — the engine sets `flag:caught_first_kin` on any successful
  catch; the first Lumenary's battle trigger requires it, with a `blocked_ref` line in the
  warden's own voice.
- **Multi-floor caves (2026-06, BINDING)** — caves are ladder mazes, not single rooms:
  floors are maps joined by mutual ladder-warp pairs, dead ends pay in caches, spur mouths
  sit on the lowest floor, and only a region's *first* dungeon stays small. The full scale
  table (first dungeon → mid wall → landmark → the Spire) is `level-design.md` §2a;
  Glowmoss Deep + B1F is the built worked example.
- **Sight trainers** — route (and dungeon-floor) trainers carry `sight_range` +
  `defeated_flag` on their placement: they alert (!), march up and run their script when
  the player crosses their line. Post a trainer in a corridor's end row facing down their
  own column and the floor crossing is unavoidable; beside a route lane it is the classic
  "they saw you" beat. Beaten trainers swap to a plain-dialogue placement by flag pair.
- **Mandatory grass crossings** — each route carries 1–2 full-corridor encounter bands
  (the lit lane carved out across them; use the context-correct grass family — `dunegrass`
  on sand) so travel itself rolls encounters; the larger flanking patches stay optional
  grind spots (level-design §11 rule 7).
- **The earned Gleam loop (BINDING — every Lumenary).** No Gleam is handed over at the door:
  every bond-test sits at the end of a loop with the same grammar — **tease** (something
  visible and locked/dark/silent in town) → **hook** (the errand asked in the warden's own
  voice, with a `blocked_ref` line until it's done) → **collinear errand** (on ground the
  main path already walks, inside the §4 band) → **key / pass / trial** (a flag chain —
  NEVER the region's own Gift, §0 rule 1) → **bond-test**. The SHAPE must vary region to
  region so the loop never goes formulaic; weights alternate full-loop ↔ light. The eight
  canonical shapes (each specified in its region file):

  | # | Gleam · Warden | Shape (weight) | Locked tease | Earned thing | New-map cost |
  |---|---|---|---|---|---|
  | 1 | Ember · Brisa | tower ascent (full) | the wick-locked Beacon | wick-key from the Dimglass lamplighter | BUILT (3) |
  | 2 | Tide · Reyl | breakwater walk (medium) | the silent Moor-bell shrine | the netmender's bell-rope (net-floats errand) | BUILT (1: `pearlmoor_breakwater`) |
  | 3 | Verdant · Sable | in-town tending (light) | the grey Elder Bed amid the Bloom | warm the bed (kiln + fen-wood chain) | 0 |
  | 4 | Stone · Otho | mine descent (heavy) | the dark `to_deep` mouth; lamps lowered | the crew's still-lit vigil-lamp from the deep | 0 |
  | 5 | Storm · Mira | festival winch climb (medium) | the launch ledge, kite-strings rising | a town-built kite flown at the Kite-rising | 1 (`galehigh_skyloft`) |
  | 6 | Frost · Ysolde | ice lamp-line (single-map trial) | the undercroft door, seven dark brackets | aurora-oil, then seven brackets lit in line | 1 (`pale_vault_undercroft`) |
  | 7 | Solar · Lucan | flooded gathering (light-medium) | the dark Heliarium stage | three sunmote phials from the Tidecall halls | 0 |
  | 8 | Lunar · Nessa | ceremony walk (capstone) | seven unlit watch-lamps under a relit sky | keep the Star-vigil: one lamp per held Gleam | 0 |

- **Named side quests (BINDING — every region ships 3+).** Each region file's "Optional
  content" carries a *Named quests* sub-block: quest name · giver NPC · 2–4 steps · flags
  (`flag:q_*`) · reward · maps touched · tags (`[MISSABLE]`/`[LATER]`). Always including
  that region's leg of **the Waykeeper's Round** — the cross-region delivery line anchored
  at the Waykeeper (`vesper_crossroads`): a parcel per spoke, each leg waking with its
  spoke's flag (tag `[wakes with spoke]`), closing post-`hub_unlocked` with "The Long
  Round". Side quests are pure data: flag chains + NPC swaps + script dialogue_refs +
  item caches.

### The vesperlamp's growing light — the *continuous* exploration axis ("Lamplight")

The six Lantern Gifts are **discrete** keys: each crosses a *specific* barrier, and they're
mostly earned early-to-mid, so they front-load the "map reopens" thrill. Running underneath
them is a second, **continuous** axis that grows to the very end and back-loads it: the
**vesperlamp's brightness itself**. This is already canon — the lamp "catches and holds the
light you restore, *grows brighter as you progress*" (`story-bible.md` §2). This blueprint
promotes it from flavour to a designed mechanic, **Lamplight**.

> **THE BINDING RULE — Lamplight is additive, never blocking.** Lamplight only ever
> *reveals* or *eases* **optional** content. It never gates a Gleam, a Lantern Gift, a
> main-path warp, or any required step. The audited soft-lock chain, level curve, and arc
> beats of §2–§4 are **untouched**. A first-timer with a dim lamp completes everything
> required; a brighter lamp simply *shows more*. (This is what keeps the addition from ever
> damaging the existing playthrough.)

**How it works.** In **dark terrain** (caves, deep woods, coldfog, the Spire), the world
falls away beyond a **reveal radius** centred on the player; the radius is the lamp's current
brightness. The intended route is always **diegetically lit** — lamp-posts, glowmoss, crystal
veins, lantern-buoys (per `level-design.md` "funnel with light") — so the critical path is
visible at *any* brightness. What hides in the unlit dark beyond your radius is **optional**:
side alcoves, hidden items, the mouths of optional spurs, and quiet foreshadow detail.

**The tiers (keyed to Gleam count — each relit constellation feeds the lamp):**

| Tier | Gleams | Reach |
|------|--------|-------|
| **Ember-glow** | 0–1 | a candle's circle — the cosy, close opening |
| **Warmlight** | 2–3 | a lantern's reach |
| **Brightlight** | 4–5 | a strong, confident lamp |
| **Starlight** | 6–7 | a far, clean reach |
| **Radiant** | 8 / post-Crown | near-daylight in its circle — you carry the dawn |

**The late-game backtrack engine (this is the point).** Because early dark areas are first
walked at low Lamplight, **returning to them later, brighter, reveals new optional content** —
spread across the *whole* early map, not bottlenecked behind one late Gift. This is the
elegant resolution of the front-load problem: **Gifts front-load reopening; Lamplight
back-loads it.** Tideglass Cavern (Warmlight) hides nooks you only see at Starlight; Cinderhead
Deep's far galleries open new alcoves once Radiant; the Spire is darkest exactly when your lamp
is brightest (thematic peak). Region files place a **"return brighter"** callout on dark areas
that hold tier-gated optional content, tagged `[LATER: Lamplight ≥ <tier>]`.

**Where it applies (per-area spec for map authors):**

| Area (dark terrain) | First seen at ~ | Reveals at higher Lamplight |
|---------------------|-----------------|------------------------------|
| Tideglass Cavern (South landmark) | Warmlight | Starlight: deeper nook + a hidden item |
| Glowmoss Deep / Spore Grotto (East) | Warmlight | Brightlight: glow-shadowed side-cells |
| Cinderhead Mine / Deep (East) | Warmlight | Starlight/Radiant: far galleries, a late alcove |
| Hushfrost Pass / Coldfog Marches (West) | Brightlight | Radiant: fog-shrouded caches (the drained dark resists — see below) |
| Umbral Spire (Central) | Starlight→Radiant | the climax dark, met with your fullest light |

**Two honest caveats.** (1) **Coldfog/blighted dark resists Lamplight** — the Hollowing's
drained dark stays oppressive regardless of tier (Arc D rule: it doesn't brighten with your
progress), so its reveals lean on Emberward/Glimmerstep, not brightness. (2) **Engine cost:**
one contained render feature — a radial light/dark mask on maps flagged "dark," radius bound to
a brightness value derived from Gleam count, plus optional `reveal_at_tier` markers on hidden
content. Designed here; not built by this blueprint (see §8).

### Sunsketch as an optional light-puzzle — depth on one Gift

The Gifts are all "cross this barrier" keys; **Sunsketch** is the natural one to also carry a
light *puzzle* dimension, because Solar's fantasy is **stored, placeable daylight**. Sunsketch
releases a "pocket of daylight" that blooms shut night-flowers into bridges — extend that so
the daylight is **directional and fading**:

- **Sequential bloom** — blooming one vine reaches a sunnier spot from which you can bloom the
  next, *routing* a path across a gap a single bloom can't span.
- **Timed bloom** — a bloomed bridge slowly closes again; you bloom-and-cross, or bloom two to
  hold a longer span — light the path before it fades.
- **Redirect** — bloom a "sun-mirror" flower that bends the pocket of daylight to a vine you
  can't reach directly.

> **Same binding rule.** **Main-path Sunsketch bridges stay simple** — a single bloom that
> stays open — so required progress is *never* a puzzle. The puzzle dimension lives **only in
> optional rooms**: a back-fold in the Sunken Solarium, an optional Sunvault Climb terrace, and
> above all **Helia Vault** (promote that spur from a plain locked room to a proper Sunsketch
> puzzle micro-dungeon — it makes the West's signature Solar reward earned, not just gated).
> Engine: chains of `AbilityGate` (`make_passable`/`remove_tile`) cover sequential/redirect
> now; the *timed* variant is a small addition (flag it).

### How the two axes share the work (the curve, restated)

- **Discrete Lantern Gifts** (Tidecall → Starreach) front-load exploration: most of the
  "go back and reopen the early map" payoff lands in the first two-thirds.
- **Continuous Lamplight** back-loads it: the brighter your lamp, the more the *already-visited*
  dark gives up — so the late game keeps the discovery thrill spread across the whole world,
  not crammed behind the finale.
- **Starreach** stays the **finale key** (Gleams 8): its two payoffs (Crystoll Vault, Starwell)
  are intentionally endgame, and that's now *fine* — it isn't carrying the late-game exploration
  load alone, Lamplight is.

---

## 6. Region map & reading order

Play (and read) clockwise around the rim, then inward:

**South** (Gleams 1–2 → `crown_south`) → **East** (3–4 → `crown_east`) → **North**
(5–6 → `crown_north`) → **West** (7–8 → `crown_west`, → `hub_unlocked`) → **Central/Endgame**
→ **Post-game**. The **Vesper Crossroads** hub (Lanternway spokes to Tinderwick, Pearlmoor,
Lowleaf, Galehigh, Nightreach) becomes the fast-travel anchor once discovered in the south;
its four roads to the Spire open only on `hub_unlocked`.

Every region follows the same shape (atlas §3): a **segmented main route** (I→II, gift-gated
on the boundary) → a **town/Lumenary** → an **optional spur** (gated by a *later* Gift —
backtrack bait) → a **landmark micro-dungeon** → a **hub spoke**. The Lanternway also
carries **the Waykeeper's Round** (§5): each spoke wakes its delivery leg as its region is
authored, so the hub accumulates purpose all game long.

---

## 7. Per-area section template (the contract for region files)

**Every** area (including segments, spurs, landmarks) is written to this exact shape so it is
scannable and validatable:

```
### <Area name> — <one-line mood>
**At a glance** — map id(s) · kind · region · entry/exit · gate ability · Gleam · rec. level
1. **Main path** — ordered beats; one screen-decision per beat in spirit (per level-design §15×10)
2. **Story beats** — which arc beats (A1/B2/…) land here; 1–3 *signature* sample lines that set tone
   - **Cinematic staging** — for each major beat, the [`cinematics.md`](../cinematics.md) primitives + assets it uses (portraits/expr · music crossfade/`silence`/sting · `letterbox`/`tint`/`shake` · `gleam`→swell · any cold-open/chapter panel). The South scripts are the worked reference. **Binding** per §0.4.
3. **Mechanic introductions** — Gift earned / capture-or-kindling teaching / new terrain
4. **Optional content** — spurs · landmarks · hidden items, each tagged:
      [MUST-DO] don't-leave-without · [MISSABLE] easy to walk past · [LATER] needs a Gift you don't have yet (name it)
      PLUS a **Named quests** sub-block (mandatory for town/route areas — §5 kit):
      - <Quest name> — giver: <NPC> · steps (2–4) · flags (`flag:q_*`) · reward · maps touched · tags
5. **Don't-miss callouts** — the exploration payoffs a first-timer shouldn't pass
6. **Validation hooks** — the data a built map MUST contain:
      - map id(s) and kind; entry/exit warp coords agreed with neighbours
      - key warps with their `requires_ability` / `requires_flag`
      - key triggers with their `sets_flags` (use the canon flag strings in §2)
      - encounter zones: terrain · element-matched kin (atlas) · level band (§4)
      - NPC / Lumenary / festival placements + dialogue/script refs
      - quest-chain hooks: every `flag:q_*` the area sets or consumes, with the NPC
        swap pairs / blocked_refs that carry it (rule 3: opened ⇒ consumed)
```

Tag discipline: **[MUST-DO]/[MISSABLE]/[LATER]** are mandatory on every optional entry so the
"come back later" web is machine-checkable against the exploration table in §5.

---

## 8. Proposed mechanics & canon extensions

Surfaced by gaps the journey needs. **Nothing here is implemented by this blueprint** — each
is a proposal with how cheaply it lands. Region files may *write toward* the ✅ ones (pure
data) freely; ⚠️ ones are written as flavour until the system exists.

| Proposal | Why the journey needs it | Cost / "expressible now?" |
|----------|--------------------------|---------------------------|
| **Null-lantern restoration** beats (relight a drained site / wake a sleeping kin) | Arc B's emotional core; makes the Hollowing tangible | ✅ **Now** — `EventTrigger(kind:'script')` + `setFlag` + flag-gated NPC/encounter swap; no engine change |
| **Town festivals** | Arc E warmth; "belonging not conquest" | ✅ **Now** — cutscene + flag-gated NPCs |
| **Còr foreshadow encounters** | So the climax isn't a cold open (B3) | ✅ **Now** — cutscene/dialogue only |
| **Wren rival battles** | Arc A | ✅ **Now (data)** — trainer-battle cutscene step + `reward_flags`; add trainer entries |
| **Earned Gleam loops** (§5 kit — all eight) | Gleams feel walked-for, not handed over; fixes ace-gap cliffs | ✅ **Now** — flag chains + NPC swaps + `requires_flag`/`blocked_ref` triggers + sight trainers + item caches (the built Beacon proves the whole stack) |
| **Side-quest chains / the Waykeeper's Round** | Towns feel alive; the hub accumulates purpose; dense optional content | ✅ **Now** — same data stack as above; parcels are key items via `giveItem` |
| **Fenn–Còr shared past** | Climax weight (Arc C) | ✅ **Now** — pure narrative; no mechanic |
| **Celestial calendar / day-forms** | Arc D payoff; post-game collecting | ⚠️ **Partial** — permanent "constellation relit" table swaps work via flag-gated `EncounterZone`s; true day/night *cycling* needs a small system → propose for post-MVP |
| **Lamplight** (vesperlamp brightness tiers — the continuous exploration axis, §5) | Makes Arc D legible *and* is the late-game backtrack engine (early dark areas give up more as the lamp brightens) | ⚠️ **Designed** (§5), one contained render feature: a radial light/dark mask on "dark" maps, radius from Gleam count, + optional `reveal_at_tier` markers. **Additive/non-blocking by rule** — safe to author optional reveals toward it now |
| **Sunsketch light-puzzle** (directional/timed/redirect blooming, §5) | Adds genuine puzzle depth on one Gift without touching the main path | ⚠️ Sequential/redirect **expressible now** (chained `AbilityGate`); the *timed* bloom is a small addition. Optional rooms only (Helia Vault, Solarium back-fold, a Sunvault terrace) |
| **Status conditions + move-learn prompt** | Mid-game battle depth (assumed from Pearlmoor on) | ⚠️ Already roadmapped (`battle-runtime-plan.md`) — flag as dependency, don't author around its absence |
| **Quest counters** (multi-step fetch/track beyond booleans) | Exactly three quests want "N of M" state (*The Inn's Empty Lamps*, *The Long Round*, *The Day-form Survey*) | ⚠️ Small `FlagStore` extension (shadow `Record<string,number>`); **each of the three has a written boolean-chain fallback** (step B's giver only appears once step A's flag is set), so nothing blocks on it |

**Canon extensions locked by this blueprint** (region files must use, consistently):
the rival is **Wren**; the mentor is **Star-tender Fenn**; **Fenn and Còr share a past as
star-tenders**; the eight **festivals** in §3 Arc E; the Keystar-kin is **Keylumen** (atlas);
**Lamplight** (the vesperlamp's brightness tiers — Ember-glow → Warmlight → Brightlight →
Starlight → Radiant — as the continuous, additive, non-blocking exploration axis of §5).
Locked 2026-06 by the economy design (`docs/mechanics/10-economy.md`): money is **wicks**
(waxed lamp-wicks, traded; Tinderwick minted the custom) and taught-move items are
**Star-charts** (pressed constellation figures, single-use) — never "gold/coins" or "TM/HM".

---

## 9. Validating a built map against this walkthrough

A generated/authored area passes when its **Validation hooks** (template §7.6) check out:

1. **References resolve** — every `map id`, `AbilityId`, and `flag:*`/`gleam:*` the section
   names exists in `src/game/data/world/graph.ts` / `types.ts` (or is one of the new canon
   strings in §2, added to the world types when first built). No orphan references.
2. **No soft-lock** — for the required main-path edges in `graph.ts`, the Gift/flag each edge
   needs is earned at an *earlier* stop in §2/§4 than the edge is crossed. (Walk §2 top to
   bottom; every `requires_*` must already be held.)
3. **Curve continuity** — the map's encounter level band matches §4 at that stop (±2), so
   crossing a region boundary has no level cliff.
4. **Ecosystem match** — encounter kin are element-matched to the area's light (atlas §4).
5. **Optional-content web** — every `[LATER]` tag names a Gift, and that Gift's row in §5
   lists this area among what it reopens (the back-reference closes).
6. **Tone & originality** — canon vocabulary; no silhouette/name/line evokes another
   franchise (run the `copy-editing` skill; re-check `VISION.md`).

---

## 10. Voice & originality (binding)

Cosy, a little melancholy: **"lanterns in the dark."** Never grim, never cute-for-cute's-sake;
the Hollowing are sympathetic and never lethal. Use only canon vocabulary — **never**
"monster/gym/badge/HM," and never the genre's role-titles as labels: **no "Professor"**
(Fenn is a *Star-tender*; "professor_fenn" is only an asset filename), no "Elite Four,"
"Champion," "Trainer" as a title, or "dex" used as a brand. Never another franchise's terms
(even in sample dialogue). Sample
lines are *flavour*, not full scripts: a few signature lines that set tone, no more. When in
doubt, **more original, not less** — and shorter.
