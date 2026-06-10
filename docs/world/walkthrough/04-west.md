# PixelKin — Walkthrough: West Region

> Gleams **7–8** → **`flag:crown_west`** → **`flag:hub_unlocked`**. The sunset quadrant: a
> frozen pass thawing into a drowned sun-garden, climbing to the densest starfield in the
> game — where the Crown completes and the Spire opens. Written to the spine in
> [`README.md`](./README.md) — read its §0 rules, §2 flags, §3 arcs, §4 curve, §5 cadence,
> §7 template, §10 voice before editing this file. Lore in
> [`story-bible.md`](../story-bible.md) (the Hollowing §7, the Great Null & Keystar §5);
> maps in [`atlas.md`](../atlas.md) §2 cards 8–10 + §3 Hushfrost / Sunvault / Coldfog;
> connectivity in [`graph.ts`](../../../src/game/data/world/graph.ts). All content original
> per [`VISION.md`](../../../VISION.md); canon vocabulary throughout
> (**kin, Lumenary, Lampwarden, Gleam, Lantern Gift, vesperlamp, kindling, the Hollowing**).

---

## Region at a glance

| | |
|---|---|
| **Areas** | Hushfrost Pass I → II (frozen route) · **Sunken Solarium** (ruin, Lumenary 7) · Sunvault Climb I → II (sun-garden route) · **Nightreach Observatory** (star-temple town, Lumenary 8) · outer detour **Coldfog Marches I → II** · spurs/landmarks **Aurora Hollow**, **Helia Vault**, **Drownlight Beacon**, **Hollowfen Stillworks** |
| **Reading order (MAIN PATH)** | `pale_vault_glacier` → **Hushfrost Pass I → II** → **Sunken Solarium** → **Sunvault Climb I → II** → **Nightreach Observatory** → `vesper_crossroads` (handed to Central). The **Coldfog Marches** detour is OPTIONAL and taken LATE, from the hub — not the road to Nightreach. |
| **Entry state** (from North) | ~lv40 · holds **Tidecall + Glimmerstep + Updraft Kite + Emberward** · `gleam:storm` + `gleam:frost` · `flag:crown_north` · `flag:shortcut_windward` · narrative ledger `flag:dusk_begins` + `flag:met_hollowing` + `flag:met_cor` |
| **Exit state** (to Central) | ~lv52 · holds **ALL SIX Lantern Gifts** (adds Sunsketch + Starreach) · **all eight Gleams** · `flag:crown_west` · `flag:hub_unlocked` · narrative ledger `flag:dusk_begins` + `flag:met_hollowing` + `flag:met_cor` + `flag:great_null_known`; the Spire is now openable |
| **Gleams earned** | **Solar** (Lucan Pyre, Sunken Solarium, ace ~46) · **Lunar** (Nessa Cole, Nightreach, ace ~52) — both relit → `flag:crown_west` → `flag:hub_unlocked` |
| **Lantern Gifts earned** | **Sunsketch** (Sunken Solarium) · **Starreach** (Nightreach) — the endgame traversal |
| **Arc beats landing here** | **B4** full-scale Hollowing (Coldfog Marches + Hollowfen Stillworks; the **Great Null** aimed at the **Keystar** is named → `flag:great_null_known`) · **A5** Wren returns resolved (late West / Spire approach) · **C4** Fenn's counsel before the Spire (Nightreach) · **E** Last-Warm-Day (Solarium), Star-vigil (Nightreach) |
| **Festivals (Arc E)** | Sunken Solarium **Last-Warm-Day** · Nightreach **Star-vigil** |
| **Curve** | Hushfrost 40→42 → Solarium ~42 (Lucan ace ~46) → Sunvault 46→48 → Nightreach ~48 (Nessa ace ~52) → exit ~52. ~+6/Gleam, continuous with North's exit (~40); Coldfog detour sits ~46–50 (late). |

**Cinematic staging (PLANNED — build from South per [`cinematics.md`](../cinematics.md) / §0.4).**
West is **the threshold of the endgame**; the staging escalates toward the Spire. **B4 the Great
Null named** (Nessa at the telescope) is an information set-piece — `letterbox`, a low uneasy bed,
Nessa's **portrait** (haunted), and on the words "aimed at the Keystar" a `silence` + a single cold
`tint`; this is the moment the stakes go concrete, so let it sit. **Coldfog Marches / Hollowfen** is
the **drained-zone** register: bare 4-voice `gbc` or `silence`-heavy, desaturated `tint` held over
the whole zone, no festival warmth — the visual cost of the Hollowing at scale. **A5 Wren returns
resolved** flips the North wobble: open on Wren's `neutral`/steady portrait, a warmer bed — the
argument walked all the way round. **C4 Fenn's counsel** is portrait + quiet. Festivals: **Last-
Warm-Day** (Solarium) is the emotional turn from cold to warmth — the swell should bloom `fire`-warm
after the coldest regions; **Star-vigil** (Nightreach) is the most reverent — `silence` cresting
exactly as the Lunar Gleam lights (each watcher's lamp a small `flashColor`). Assets owed: Nessa
portrait, a drained-zone cue + desaturated backdrop, the Solarium warm-swell variant.

**Arc D — lighting.** West is the **lightest pre-dawn region** — clearly lighter than North.
You leave Pale Vault's lonely aurora-ice and the cold thins: **Hushfrost Pass** is still cold
but warming at its mouth, the **Sunken Solarium** is "**warm light remembered**" (`fire` stored
daylight glowing up through `water`, the first real warmth since the south), **Sunvault Climb**
opens into golden, hopeful terraces, and **Nightreach** is the **densest starfield in the
game** — near-dawn pallor at the horizon, six then seven then eight constellations relit
overhead, the vesperlamp at its brightest. **Tie lighting to Gleam-count, not geography**
(spine §0 rule 2): the Coldfog detour and a back-door arrival at Nightreach still read **dark**
until you hold the Solar Gleam — Coldfog is the one *drained* place, the visual cost of the
Hollowing, and stays desaturated regardless of where you walked in from.

> **The §0 traps for this region, called out up front:**
> 1. **The Solarium's Lumenary is reachable WITHOUT Sunsketch.** Sunsketch is *earned* from
>    Lucan Pyre and gates only the **onward** `sunvault_climb_i → sunvault_climb_ii` segment +
>    the **Helia Vault** spur — **never** the ruin's Lumenary itself. The
>    `hushfrost_pass_ii → sunken_solarium` and `sunvault_climb_i → ...` *entry* edges are not
>    Sunsketch-gated. (The Solarium's *flooded halls* use **Tidecall**, which you already hold.)
> 2. **Nightreach's MAIN-PATH approach is the rim** — `sunvault_climb_ii → nightreach_observatory`
>    (ungated), reached after the Solar Gleam. The Coldfog back-door
>    (`coldfog_marches_ii → nightreach_observatory`, Emberward) exists but is an **optional late
>    detour**; do not write Nightreach as if the player normally arrives via the fog.
> 3. **`flag:crown_west` and `flag:hub_unlocked` BOTH fire at Nightreach** (Solar + Lunar
>    complete the west quadrant, the last quadrant). Don't hand-set them — the engine does — but
>    every "Spire opens" beat depends on them. This region hands off to
>    [`05-central-endgame.md`](./05-central-endgame.md).

---

## Hushfrost Pass I → II — *the cold thinning toward a remembered warmth*

**At a glance** — `hushfrost_pass_i` (snow canyon) → `hushfrost_pass_ii` (coldfog throat) ·
kind route · region west · **enter** from `pale_vault_glacier` (ungated) **→ exit** to
`sunken_solarium` (ungated) · **boundary gate:** Emberward (I→II — *already held*) · **Gleam:**
none · **rec. level 40 → 42.**

### 1. Main path

1. **Hushfrost Pass I — the snow canyon.** You step off Pale Vault's ice into a snowed canyon,
   `deepBlue` ice walls, your lamp the only warmth (atlas §3). Read as descending-then-narrowing
   15×10 beats: a sheltered hollow, a wind-blown stretch, a choke. Tall-grass in the sheltered
   pockets carries the cold roster (ice-burrower, frost-wisp). Cold still presses, but the light
   is *less lonely* than the glacier — the first hint the quadrant is warming.
2. **The boundary — the coldfog throat.** Segment I ends at a wall of **coldfog** (the
   Hollowing's creeping mist): the canyon's throat is choked with it, impassable to ordinary
   flame. This is where **Emberward pays off for the first time** — you already earned it from
   Ysolde, so burn through and into segment II. (`hushfrost_pass_i → hushfrost_pass_ii`,
   `requires_ability: emberward` — held on entry, so the West path is open from the start.)
3. **Hushfrost Pass II — the coldfog throat.** Past the burn the route runs through thinning
   fog; the **first numbed ex-Ember kin** appear near the mist (Frost/Dark — kin the Hollowing
   *quieted*, a cold foreshadow of Coldfog without naming it yet). The far mouth glows faintly
   gold ahead — the Solarium's stored daylight, sight-lined as the destination.
4. **Exit west** to `sunken_solarium` (ungated — the ruin and its Lumenary are reachable on
   foot; Sunsketch is earned *there*, not needed to arrive).

### 2. Story beats

- **Quiet transit beat, not a named plot beat** (West's named beats land at the Solarium,
  Nightreach, and the Coldfog detour). Use the Pass for **Arc D pacing**: the visible handover
  from Pale Vault's lonely cold to the Solarium's remembered warmth — the road *feels* like
  thawing.
- **Arc B foreshadow (light touch — B4 lands at Coldfog, do not pay it off here).** The numbed
  Frost/Dark kin near the fog are the first sight of what the Hollowing leaves behind. A
  pass-tender NPC notes the fog "wasn't here last winter." Plant unease; don't name the Great
  Null yet.

> *Signature lines (flavour, not script):*
> - Pass-tender, at the coldfog throat: *"It creeps further up the canyon every year now. My
>   lamp won't hold against it — but yours might, traveller. Warm it through, and mind the kin
>   on the far side. They've gone... quiet."*
> - A numbed kin's caretaker: *"It used to glow like a hearth. Now it just sleeps. They tell us
>   that's mercy. I light a lamp by it anyway."*

### 3. Mechanic introductions

- **Emberward in anger.** The coldfog throat is the first place Emberward is *required* to
  progress (Pale Vault's deep-ice was optional). The genre's "earned crossing," paid off one
  region after the Gift was earned.
- **"Now accessible" callout (Emberward, held).** Place one at the **Aurora Hollow** spur off
  Hushfrost II — you hold Emberward, so it opens the moment you reach the fog (§4).
- **Cold→warm type band turns over.** Frost still presses (status `chill` assumed, spine §5);
  the new **Frost/Dark** numbed kin foreshadow the Dark roster of Coldfog. The next region step
  flips to **Solar/Verdant** — flag the warming band.

### 4. Optional content

- **Aurora Hollow** — spur off `hushfrost_pass_ii`, `requires_ability: emberward`; reward: rare
  **Frost/Light kin + item**. **[MISSABLE]** — you already hold Emberward, so it's open the
  moment you reach segment II; a dead-end you must choose to detour to. Tag it hard so a
  first-timer sweeps it before the warmth of the Solarium pulls them on. (This is **West's** map
  — the North writer only cross-referenced it.)
- **Hidden item in a sheltered snow-hollow** off the main lane in segment I — **[MISSABLE]**.
- **Lamplight reveals (snow-hollow caches)** — `[LATER: Lamplight ≥ Radiant]` `[MISSABLE]`:
  wall-hollows along the canyon that sit beyond the lamp's reach now; a post-game **Radiant**
  return picks them out (spine §5). Optional only — the lit canyon route is visible at any tier.

**Named quests** (spine §5 kit):
- **X1 "The Caretaker's Lamp"** — giver: the **caretaker** in a segment-II shelter, sitting
  with a **numbed, sleeping kin** the coldfog touched · steps: fetch **aurora-oil** from
  Aurora Hollow (Emberward, held) → fill her lamp · flags: `flag:q_west_caretaker` →
  `flag:q_west_caretaker_done` · reward: a **Bright Lamp** — and the kin sleeps *easier*,
  not awake (keep B-arc's weight) · maps: `hushfrost_pass_ii`, `aurora_hollow` ·
  `[MISSABLE]` — **post-game payoff:** once `flag:dawn` is set, the kin is awake at her
  side (NPC swap; cross-ref 06-postgame) — the quietest B-arc echo in the game.

### 5. Don't-miss callouts

- **Aurora Hollow is the last Frost reward** before the quadrant warms — grab it while the cold
  roster is still in front of you. **[MISSABLE]**
- The faint **gold glow** at the far mouth is your sight-line to the Solarium — the first real
  warmth in many screens; let it pull the player forward.

### 6. Validation hooks

- **Map ids / kind:** `hushfrost_pass_i`, `hushfrost_pass_ii`, kind `route`, region `west`.
- **Boundary warp (graph.ts):** `hushfrost_pass_i → hushfrost_pass_ii` via `to_pass_ii`,
  **`requires_ability: emberward`** (held on entry), bidir.
- **Entry/exit warps:** in from `pale_vault_glacier` via `to_pass` (**ungated**, bidir); out to
  `sunken_solarium` via `to_solarium` (**ungated**, bidir — Solarium reachable without Sunsketch).
- **Spur warp:** `hushfrost_pass_ii → aurora_hollow` via `to_aurora`, `requires_ability:
  emberward`, bidir.
- **Encounter zones:** `tall_grass` (sheltered pockets) — ice-burrower (Frost), frost-wisp
  (Frost/Light), numbed ex-Ember kin near the fog (Frost/Dark); level band 40–42 (continuous
  with Pale Vault's 36–40 and the Solarium's ~42). Aurora Hollow carries rare Frost/Light kin at
  low weight.
- **NPC:** pass-tender + a numbed-kin caretaker near the coldfog throat; dialogue refs
  `npc.hushfrost_pass_tender`, `npc.numbed_kin_caretaker`.

---

## Sunken Solarium — *the drowned sun-garden where warmth is remembered*

**At a glance** — `sunken_solarium` · kind route/ruin · region west · **enter** from
`hushfrost_pass_ii` (ungated) **→ exit** to `sunvault_climb_i` (ungated) · **gate ability:**
Sunsketch — but it gates only **onward** content (Sunvault II + Helia Vault), **NOT** the ruin
or its Lumenary; the ruin's **flooded halls use Tidecall** (held) · **Gleam:** Solar (Lucan
Pyre, ace ~46) · **rec. level ~42 → 46.**

### 1. Main path

1. **Into the drowned garden.** The fog gives way to a half-flooded ruined sun-garden:
   submerged golden architecture, `fire` "stored daylight" glowing up through `water`, `bone`
   columns (atlas §2 card 8). The first genuine *warmth* since the south — a place that
   *remembers* the sun. The lit causeway leads in across the shallows.
2. **The flooded halls (Tidecall, held).** Inner halls are knee-deep in night-water; **Tidecall**
   (earned long ago at Pearlmoor) parts them so you cross to the inner ruin, and warm-water
   kin (Glentide, Tide/Solar) swim the flooded zones. *(A dry causeway to Lucan himself
   always exists — the Lumenary and the festival are never behind any Gift. The bond-test
   ERRAND, though, deliberately walks the Tidecall water: the old Gift made load-bearing —
   see the loop below.)*
3. **The Last-Warm-Day is underway.** The festival fills the sunlit upper terrace of the ruin
   (Arc E, below); Lucan Pyre is its theatrical ringleader. Sun-roster kin in the dry tall-grass
   (Sunsprout Verdant/Solar, Helibud Solar).
   **The earned loop — "The Lit Stage" (spine §5, shape #7: flooded gathering).**
   **The tease:** at the garden's heart, the **Heliarium stage** — a sunken performance
   terrace, its **three braziers dead**, the Last-Warm-Day troupe waiting in costume
   beside it. Lucan's hook: *"A bond that remembers the sun! Then prove the memory — the
   stage is dark and the daylight's drowned. Fetch it up, spark by spark."*
   (`script.lucan_quest` → `flag:q_west_stage`.)
4. **The sunmote errand (collinear, Tidecall).** Three **sunmote phials** — stored daylight —
   wait in the flooded inner halls (band 42–46; the existing flooded-hall content promoted
   from missable to quest), the water lanes worked by **two troupe-player sight trainers**
   (lv 43–45). Each phial lights its brazier in sequence (brazier scripts chained, each
   requiring its mote flag: `flag:q_west_mote_1..3`); each lighting **blooms a row of
   night-flowers** along the stage rim — a purely *visual* Sunsketch foreshadow, no
   Sunsketch required. Third brazier → `flag:q_west_stage_lit`; the troupe takes the stage
   and the festival crests.
5. **Lumenary 7 — Lucan Pyre (Solar), on the lit stage.** Reachable on foot / by the dry
   causeway — **no Sunsketch needed to enter** (spine §0 rule 1); the bond-test trigger
   requires `flag:q_west_stage_lit` (`blocked_ref` in Lucan's voice). A theatrical, warm,
   dramatic Solar fight; ace ~46 met at ~44–45. Win → **Solar Gleam** + **Sunsketch** +
   `gleam:solar`, ability `sunsketch`. (Solar relit; the west quadrant is now
   half-complete — `crown_west` waits on the Lunar Gleam at Nightreach.)
6. **The map reopens (Sunsketch).** Now sun-vine bridges bloom open. Place a **"now accessible"**
   callout at the **`sunvault_climb_i → sunvault_climb_ii`** boundary (the onward route, gated by
   Sunsketch) and at the **Helia Vault** reliquary (off Sunvault II) — both now openable. Also
   note any sun-vine bridges *within* the ruin that bloom into a back-fold reward.
7. **Exit west** to `sunvault_climb_i` (ungated — the lower terraces need no Gift; the *boundary*
   I→II is what Sunsketch gates).

### 2. Story beats

- **Arc E — the Last-Warm-Day.** The Solarium's festival: once a year the town gathers in the
  drowned garden to "spend the last warm day before the dark," sharing stored-daylight lanterns
  and warm bread on the sunlit terrace. Bittersweet, golden, a little defiant — *belonging, not
  conquest*. You share in it before you earn the Gleam. It quietly rebukes the Hollowing: warmth
  *worth* keeping even knowing it fades.
- **Lucan Pyre — voice.** Theatrical, grandiose, but deeply kind underneath the showmanship; he
  "keeps the last warm day" like an actor keeping a flame, half-aware it's a performance against
  the dark and proud of it anyway.
- **Arc D landmark.** The Solarium is the **emotional turn from cold to warm** — flag it as the
  region's pivot; everything after climbs toward dawn.

> *Signature lines (flavour, not script):*
> - Lucan, sweeping an arm at the drowned garden: *"They say the sun drowned here, apprentice.
>   I say it only went to sleep — and every warm day we spend is a promise we made to wake it.
>   Now: show me a bond that remembers the sun, and I'll let you light it."*
> - A festival-goer: *"Last warm day of the year, they call it. Been calling it that for as long
>   as the night's been long. We just keep spending warm days until one of them sticks."*

### 3. Mechanic introductions

- **Sunsketch earned** — releases a stored "pocket of daylight" that **blooms shut night-flowers
  into bridges**. Taught toward the *onward* journey (it opens the Sunvault Climb boundary and
  the Helia Vault), then retroactively reopens sun-vine content — **never** used to reach Lucan
  (spine §0 rule 1).
- **"Now accessible" callouts (Sunsketch):** the `sunvault_climb_i → sunvault_climb_ii` boundary
  and **Helia Vault** (off Sunvault II) — both newly openable. (Sunsketch's reopening web is
  small and West-local; no cross-region backtrack.)
- **Tidecall, still in service.** The flooded halls reward the old Gift — a "now accessible"-style
  read for content the player could *already* clear, reinforcing the spine §5 backtrack joy.

### 4. Optional content

- **Helia Vault** — spur off `sunvault_climb_ii`, `requires_ability: sunsketch`; reward: rare
  **Solar kin + item** in a sealed reliquary. **[MISSABLE]** — opens the moment you earn Sunsketch
  (you'll reach its mouth on the climb); a dead-end you must choose to bloom open. (Its warp is on
  the Sunvault II map — cross-referenced here because Sunsketch is earned at the Solarium.)
- **Flooded-hall item caches** (Tidecall, held) — **[MISSABLE]** rewards in the drowned inner
  ruin; sweep them before leaving.
- **Sun-vine back-fold within the ruin** (Sunsketch, just-earned) — **[MISSABLE]** a short
  **sequential-bloom** puzzle (bloom one vine to reach the next) opening to a hidden Solar kin /
  item — the gentle first taste of the Sunsketch puzzle dimension (spine §5) before Helia Vault.

**Named quests** (spine §5 kit; West's slate, X1 over in Hushfrost II, X3 at Nightreach):
- **X2 "The Troupe's Sun-mask"** — giver: a **troupe player** (post-stage, their swap NPC) ·
  steps: the troupe's gilt sun-mask sank in a side room off the flooded halls — dive the
  Tidecall water and bring it back for the closing scene · flags: `flag:q_west_mask` →
  `flag:q_west_mask_found` · reward: the **Sun Charm** · maps: `sunken_solarium` ·
  `[MISSABLE]`.
- **R5 "A Chart for the Waykeeper"** — the Waykeeper's Round, leg 5: the **Nightreach
  junior watcher** entrusts a fresh star-chart → carry it home to the **Waykeeper**
  himself; the Round comes full circle · flags: `flag:q_round_chart` · reward: the
  Waykeeper hangs it on the Waystone (deco/NPC swap) + a Lanternway line · maps:
  `nightreach_observatory`, `vesper_crossroads` · `[wakes with spoke]` (the Nightreach
  spoke wakes with `gleam:lunar`).

### 5. Don't-miss callouts

- **Spend the Last-Warm-Day** before facing Lucan — the festival is the warmth the Solar Gleam is
  wrapped in, and the region's tonal pivot.
- **Bloom the Helia Vault** while you're on the Sunvault Climb with fresh Sunsketch — the West's
  signature Solar reward. **[MISSABLE]**
- **Clear the flooded halls** with Tidecall before you go — easy to walk past the dry causeway and
  miss the water rewards. **[MISSABLE]**

### 6. Validation hooks

- **Map id / kind:** `sunken_solarium`, kind `route`/`ruin`, region `west`.
- **Entry/exit warps (graph.ts):** in from `hushfrost_pass_ii` via `to_solarium` (**ungated**,
  bidir); out to `sunvault_climb_i` via `to_climb` (**ungated**, bidir).
- **Lumenary is NOT ability-gated** (spine §0 rule 1) — door requires no Gift (at most
  `flag:has_starter`); Lucan reachable by a dry causeway. **Author no Sunsketch barrier between
  the entrance and Lucan**; the flooded *halls* use Tidecall (held), but a dry path to the
  Lumenary must exist.
- **Lumenary trigger `sets_flags`:** Lucan Pyre victory → `gleam:solar` + grants ability
  `sunsketch`. (Engine sets `flag:crown_west` only once **both** `gleam:solar` and `gleam:lunar`
  are held — NOT here; do not set it at the Solarium.)
- **Internal gating:** flooded-hall `water` `EncounterZone`s `requires_ability: tidecall` (held);
  any in-ruin sun-vine bridge `AbilityGate` `sunsketch` (`make_passable`).
- **The Lit Stage chain (rule 3):** `script.lucan_quest` sets `flag:q_west_stage`; the three
  sunmote phial scripts in the flooded halls set `flag:q_west_mote_1..3`; the brazier
  scripts (each requiring its mote + the previous brazier) chain to `flag:q_west_stage_lit`
  (+ the night-flower deco swaps per brazier); Lucan's bond-test trigger
  `requires_flag:flag:q_west_stage_lit` with `blocked_ref:npc.lucan_not_ready`. Two
  **troupe-player sight trainers** (lv 43–45) on the water lanes.
- **Encounter zones:** dry `tall_grass`/ruin — Sunsprout (Verdant/Solar), Helibud (Solar);
  `water` (flooded halls, Tidecall) — Glentide (Tide/Solar) at low weight; level band ~42–46
  (continuous with Hushfrost 40–42 and Sunvault 46–48).
- **NPC / Lumenary / festival:** Lucan Pyre (Solar Lampwarden); Last-Warm-Day festival cutscene +
  flag-gated festival NPCs; dialogue/script refs `npc.lucan_pyre`,
  `cutscene.solarium_last_warm_day`.

---

## Sunvault Climb I → II — *golden terraces blooming open toward the stars*

**At a glance** — `sunvault_climb_i` (overgrown terraces) → `sunvault_climb_ii` (sun-vine
bridges) · kind route · region west · **enter** from `sunken_solarium` (ungated) **→ exit** to
`nightreach_observatory` (ungated) · **boundary gate:** Sunsketch (I→II) · **Gleam:** none ·
**rec. level 46 → 48.**

### 1. Main path

1. **Sunvault Climb I — the overgrown terraces.** Out of the drowned ruin onto warm, ascending
   golden terraces: `bone` steps, `fire`-warm glows, overgrowth softening the old garden-roads
   (atlas §3). Read as climbing 15×10 beats. Tall-grass on the terraces carries the green-gold
   roster (sun-seedling Verdant/Solar, vine-serpent Verdant). The brightest, most *hopeful*
   stretch of road in the region.
2. **The boundary — the dead sun-vines.** Segment I ends where the path crosses a gorge on
   **withered, shut night-flowers** — a bridge that died when the long night fell. This is where
   **Sunsketch pays off** — bloom the sun-vines open and the bridge unfurls underfoot.
   (`sunvault_climb_i → sunvault_climb_ii`, `requires_ability: sunsketch`.)
3. **Sunvault Climb II — the sun-vine bridges.** Past the bloom, a sequence of living sun-vine
   bridges climbs to the observatory hill; glass-wing bees (Verdant/Light) catch the light. The
   **Helia Vault** reliquary mouth opens off this segment (Sunsketch, just-earned). Nightreach's
   domed observatory and the **densest starfield in the game** sight-line ahead and above.
4. **Exit west** to `nightreach_observatory` (ungated — the rim approach; this is the
   **MAIN-PATH** arrival at the eighth Lumenary, spine §0 rule 2).

### 2. Story beats

- **Quiet transit beat with Arc D as the star.** No named plot beat here (they land at Nightreach
  and Coldfog). The Climb is the region's **brightest pre-dawn light** — six constellations relit
  overhead by now, the sky paling toward the horizon, the vesperlamp at its warmest. Let the
  ascent *feel* like climbing into the returning light.
- A vine-tender NPC near the bloomed bridge marvels that the sun-vines "remembered how" — a small
  warm beat that the world is healing as you relight it.

> *Signature line (flavour, not script):*
> - Vine-tender, at the bloomed bridge: *"Forty years shut, and your little pocket of daylight
>   woke them like they'd only dozed. ...Maybe nothing's gone for good. Maybe it's all just
>   waiting for the right lamp."*

### 3. Mechanic introductions

- **Sunsketch in anger.** The dead sun-vine bridge is the first place Sunsketch is *required* to
  progress (the Solarium's in-ruin vines were optional). The genre's "earned crossing."
- **"Now accessible" callout (Sunsketch):** **Helia Vault** opens off this segment the moment you
  reach it (you hold Sunsketch) — flag it hard (§4).

### 4. Optional content

- **Helia Vault** — spur off `sunvault_climb_ii`, `requires_ability: sunsketch`; reward: rare
  **Solar kin + item** in a sealed reliquary. **[MISSABLE]** — open from the moment you reach the
  segment (Sunsketch held). **Promote it from a plain locked room to a Sunsketch *puzzle*
  micro-dungeon** (spine §5): a sealed reliquary you cross by **sequential blooming** (bloom a
  sun-vine to reach a sunnier ledge, from which you bloom the next) and **redirecting** a pocket
  of daylight off a sun-mirror flower to a vine you can't reach directly — so the West's signature
  Solar reward is *earned*, not merely gated. The puzzle is entirely optional; nothing on the main
  Sunvault path requires it.
- **High-terrace hidden item** reachable across a bloomed sun-vine off the main lane —
  **[MISSABLE]**.
- **Optional puzzle terrace** (Sunvault II) — a short, skippable detour using **timed blooming**
  (a bloomed bridge slowly closes; bloom-and-cross, or bloom two to hold the span) for a small
  reward. **[MISSABLE]** — a teaching room for the Helia Vault puzzle; never on the main lane.

### 5. Don't-miss callouts

- **Helia Vault** — the West's signature Solar reward; grab it on the climb while Sunsketch is
  fresh, before Nightreach pulls you into the endgame. **[MISSABLE]**
- This is the **last bright, calm road** before the eighth Lumenary and the Spire — a good place
  to top up and bond before the climb steepens.

### 6. Validation hooks

- **Map ids / kind:** `sunvault_climb_i`, `sunvault_climb_ii`, kind `route`, region `west`.
- **Boundary warp (graph.ts):** `sunvault_climb_i → sunvault_climb_ii` via `to_climb_ii`,
  **`requires_ability: sunsketch`**, bidir.
- **Entry/exit warps:** in from `sunken_solarium` via `to_climb` (**ungated**, bidir); out to
  `nightreach_observatory` via `to_observatory` (**ungated**, bidir — the MAIN-PATH rim approach).
- **Spur warp:** `sunvault_climb_ii → helia_vault` via `to_helia`, `requires_ability: sunsketch`,
  bidir.
- **Encounter zones:** `tall_grass` — sun-seedling (Verdant/Solar), vine-serpent (Verdant),
  glass-wing bee (Verdant/Light); level band 46–48 (continuous with Solarium ~46 and Nightreach
  ~48). Helia Vault carries rare Solar kin at low weight.
- **NPC:** vine-tender near the bloomed bridge; dialogue ref `npc.sunvault_vine_tender`.

---

## Nightreach Observatory — *the densest starfield, where the Crown completes*

**At a glance** — `nightreach_observatory` · kind town (star-temple) · region west · **enter**
on the **MAIN PATH** from `sunvault_climb_ii` (ungated); also a **late optional back-door** from
`coldfog_marches_ii` (Emberward) **→ exit** via Lanternway to `vesper_crossroads` (handed to
Central) · **gate ability:** Emberward (the Coldfog back-door only — **not** the rim approach,
**not** the Lumenary) · **Gleam:** Lunar (Nessa Cole, ace ~52) · **rec. level ~48 → 52.**

### 1. Main path

1. **Up to the star-temple.** The sun-vine bridges deliver you to a hilltop domed observatory in
   `bone` + `deepBlue`, telescope brass, the **densest `diamond` starfield in the game** (atlas
   §2 card 9) — the most "sky-forward" town, near-dawn pallor at the horizon with seven
   constellations relit overhead. The approach route carries `tall_grass` (Astrowl, Dreamoth).
2. **Walk straight in — no gate.** The observatory town and its Lumenary are reachable on foot
   from the rim (spine §0 rule 1). The **Star-vigil** festival glimmers across the temple steps
   (Arc E, below).
   **The earned loop — "The Vigil of the Seven" (spine §5, shape #8: ceremony walk — the
   capstone).** **The tease:** the **Astral Walk** — seven watch-lamps lining the telescope
   terrace, **all unlit**, while seven relit constellations burn overhead. The sky is lit;
   the lamps below are not. Nessa's hook, from the eyepiece: *"Seven watch-fires for seven
   stars you've already given back. Light their lamps along the walk — then come tell the
   eighth it's time."* (`script.nessa_quest` → `flag:q_west_vigil`.)
3. **The Walk of the Seven.** Each lamp's script keys on its constellation
   (`requires_flag` its `gleam:*`, ember→solar, plus the previous lamp — all necessarily
   held, this being the eighth town: the chain is a *remembrance*, not a fetch). Lamp 1
   has the loop's one collinear errand — the **old watcher's lost striker**, a single cache
   back on `sunvault_climb_ii` (band 48–50, the road just walked). Two **junior-watcher
   sight trainers** (lv 49–51) keep the walk. And the walk *sequences the cluster*:
   - **Lamp 5 (Frost) — C4, Fenn's counsel.** Fenn waits there and lights it with you:
     the Crown is nearly whole; the Keystar must be *out-remembered*, not destroyed.
   - **Lamp 6 (Storm) — A5, Wren returns, resolved.** Wren is sitting under it, easy
     again; a warm reunion (optionally a friendly battle), and they light it with you.
     *(If `flag:q_north_ribbon_placed` is set, Wren mentions the ribbon — N3's payoff.)*
   - **Lamp 7 (Solar) — B4, the Great Null named.** At the great telescope Nessa names
     what Còr is building — the **Great Null** aimed at the **Keystar** — setting
     **`flag:great_null_known`**.
   The seventh lamp lit → `flag:q_west_vigil_kept`; the Star-vigil crests around the walk.
4. **Lumenary 8 — Nessa Cole (Lunar), under the eyepiece.** A quiet insomniac astronomer,
   **the most powerful and most haunted Warden**; ace ~52, met at ~50–51. The bond-test
   trigger requires `flag:q_west_vigil_kept` (`blocked_ref` in her voice). A contemplative,
   dreamlight Lunar fight (write around `doze`, spine §5). Win → **Lunar Gleam** +
   **Starreach** + `gleam:lunar`, ability `starreach` — the eighth watch-lamp lights
   itself as the eighth constellation answers. With Solar + Lunar both held, the engine
   sets **`flag:crown_west`** and — this being the **last quadrant** —
   **`flag:hub_unlocked`**: the Crown completes, the Penumbra fully parts, and the four
   cardinal roads open inward at the Crossroads.
5. **The map reopens (Starreach) + hand-off.** Starreach — **step across short voids of pure
   dark** — is the **endgame traversal**. Place **"now accessible"** callouts at: the
   `penumbra_ring → starwell` landmark and `penumbra_ring → umbral_spire` ascent (Central's, via
   the now-open hub); and **[LATER]/cross-region** the **Crystoll Vault** (Cinderhead Deep, East)
   and **Starwell** (Penumbra Ring) — name them as Starreach reopenings but **hand them to the
   Central writer**. With `hub_unlocked` set, **exit via the Lanternway** to `vesper_crossroads`
   and hand off to [`05-central-endgame.md`](./05-central-endgame.md).

### 2. Story beats

- **B4 — the Great Null named.** Nightreach is where the threat's full shape lands in words.
  Nessa, haunted and precise, names what Còr is building: a **Great Null** aimed at the
  **Keystar** — the one anchoring star whose light lets any of the others rekindle. If the
  player has walked the **Coldfog Marches / Hollowfen Stillworks** detour, they've *seen* the
  works; here it's *named* and tied to the Spire. Sets **`flag:great_null_known`**. Keep it grave,
  not shrill — grief at industrial scale, never cackling villainy.
- **C4 — Fenn's counsel.** Fenn, beneath the densest stars in Vesperholm, tells you the Crown is
  nearly whole and that the Keystar must be *out-remembered*, not destroyed — closing the
  thread he opened in the North (the shared past with Còr). He does not march with you; he sends
  you up clear-eyed.
- **A5 — Wren resolved.** Wren returns settled: the quiet dark *is* peaceful, and that's exactly
  why it's not enough — peace without dawn is just a long forgetting. They choose the cycle, and
  you, and the climb. The warmth of A1 returns, tempered. (Resolution of the A4 wobble.)
- **Arc E — the Star-vigil.** Nightreach's festival: the town keeps a silent night-long watch at
  the telescopes as the Crown nears completion, each watcher lighting a single lamp when "their"
  star relights — the grandest, most reverent festival, *belonging as witness*. It crests exactly
  as you earn the Lunar Gleam and the eighth constellation lights.

> *Signature lines (flavour, not script):*
> - Nessa, not looking up from the eyepiece: *"He calls it the Great Null. A lantern that holds
>   no light — aimed at the Keystar, the one we all rekindle from. Snuff that, and the sky stops
>   being able to remember itself. ...I knew him, once. He was the gentlest of us. That's the
>   part that keeps me awake."*
> - Fenn, under the full starfield: *"Eight stars, nearly. When the Crown closes, the dark will
>   part and the Spire will open its roads. You won't beat him up there, apprentice. You'll just
>   have to remember harder than he's forgotten."*
> - Wren, easy again: *"I went and looked at the quiet, like Còr wanted. It's peaceful, all right.
>   Peaceful as a held breath. ...I'd rather breathe. Come on — let's go light the last one."*

### 3. Mechanic introductions

- **Starreach earned** — draws down faint starlight to **step across short voids of pure dark**:
  the **endgame traversal**. Taught toward the Spire (it opens the final Penumbra crossings),
  then retroactively reopens the deepest-gated content mapwide (spine §5).
- **"Now accessible" callouts (Starreach):** Penumbra Ring final crossings + the Umbral Spire
  ascent (Central, now reachable via `hub_unlocked`); and **[LATER]/cross-region** Crystoll Vault
  (Cinderhead Deep, East) and Starwell (Penumbra Ring) — named here, **owned by Central** — so the
  backtrack web closes.
- **`hub_unlocked` fires** — the slow outer rim collapses into a fast four-way wheel; the
  Crossroads → Spire roads open. This is the structural hand-off to the endgame.
- Lunar pressure peaks for this Lumenary — write Nessa around `doze` (spine §5 dependency).

### 4. Optional content

- **The Coldfog Marches detour** (Coldfog I → II + Drownlight Beacon + Hollowfen Stillworks) is
  the West's big optional block — **[MISSABLE]/[LATER]**, reached from the **hub**, covered in its
  own section below. It is **not** the path to Nightreach.
- **Star-vigil hidden item / telescope sight-quest** in town — **[MISSABLE]** flavour reward.
- **Crystoll Vault** (Cinderhead Deep, East) + **Starwell** (Penumbra Ring) — Starreach reopenings
  named here but **[LATER]/cross-region**; **the Central/East writers own them** — listed only so
  the §5 web closes.

**Named quests** (spine §5 kit):
- **X3 "Charting the Dark"** — giver: the **junior watcher** (post-walk, her swap NPC) ·
  steps: take star-readings at three high points — a Sunvault II terrace, the observatory
  roof, and (optional, bravest) the Coldfog Marches edge · flags: `flag:q_west_chart_1..3`
  → `flag:q_west_chart_done` · reward: her finished chart — which **names Starwell** (the
  tease-closer for the Penumbra landmark) · maps: `sunvault_climb_ii`,
  `nightreach_observatory`, (`coldfog_marches_i` optional) · `[MISSABLE]`.
- *(X1 is listed under Hushfrost Pass; X2 under the Solarium; R5 under the Solarium's
  slate block. West's slate: X1 · X2 · X3 · R5.)*

### 5. Don't-miss callouts

- **Don't skip the C4 / A5 / B4 cluster** — Fenn's counsel, Wren's return, and the naming of the
  Great Null are the emotional run-up to the whole climax; trigger them *before* facing Nessa so
  the eighth Gleam reads as the answer to Còr's question.
- **Keep the Star-vigil** as your eighth constellation lights — the festival and the Lunar Gleam
  are meant to crest together.
- Once `hub_unlocked` fires, **the four-way hub and fast travel are live** — note it for the player
  before they head to the Crossroads.

### 6. Validation hooks

- **Map id / kind:** `nightreach_observatory`, kind `town` (star-temple), region `west`.
- **Entry/exit warps (graph.ts):** **MAIN PATH** in from `sunvault_climb_ii` via `to_observatory`
  (**ungated**, bidir); **optional back-door** in from `coldfog_marches_ii` via `to_observatory_fog`
  (**`requires_ability: emberward`**, bidir); Lanternway spoke `nightreach_observatory ↔
  vesper_crossroads` via `to_crossroads` (bidir).
- **Lumenary is NOT ability-gated** (spine §0 rule 1) — door requires no Gift (at most
  `flag:has_starter`); Nessa reachable on the rim approach. **No Emberward/Starreach gate on the
  town or Lumenary.**
- **Lumenary trigger `sets_flags`:** Nessa Cole victory → `gleam:lunar` + grants ability
  `starreach`. With `gleam:solar` already held, the engine sets **`flag:crown_west`** AND (last
  quadrant) **`flag:hub_unlocked`** — do not hand-set, but every "Spire opens" beat depends on them.
- **Story triggers `sets_flags`:** B4 naming cutscene (Nessa at lamp 7, optionally reinforced
  by the Coldfog/Stillworks set-piece) → **`flag:great_null_known`** (`script`, `once: true`);
  C4 Fenn counsel (lamp 5, narrative only); A5 Wren return (lamp 6; `reward_flags` for the
  rival bookkeeping; optional friendly battle, no progression gate).
- **The Vigil of the Seven chain (rule 3):** `script.nessa_quest` sets `flag:q_west_vigil`;
  the striker cache on `sunvault_climb_ii` (`flag:picked_striker`) unlocks lamp 1; lamp
  scripts chain `flag:q_west_lamp_1..7` (each `requires_flag` its `gleam:*` + the previous
  lamp; lamps 5/6/7 wrap the C4/A5/B4 cutscene refs above), the seventh setting
  `flag:q_west_vigil_kept`; Nessa's bond-test trigger
  `requires_flag:flag:q_west_vigil_kept` with `blocked_ref:npc.nessa_not_ready`. Two
  **junior-watcher sight trainers** (lv 49–51) on the walk.
- **Encounter zones:** approach `tall_grass` — Astrowl (Lunar/Light), Dreamoth (Lunar), Tessel
  (Light); level band ~48–52 (continuous with Sunvault 46–48 and the Spire approach ~52). None in
  the town interior.
- **NPC / Lumenary / festival:** Nessa Cole (Lunar Lampwarden); Star-tender Fenn (C4); Wren (A5
  return, optional battle); Star-vigil festival cutscene + flag-gated NPCs. Dialogue/script refs:
  `npc.nessa_cole`, `cutscene.fenn_counsel`, `trainer.wren_nightreach`,
  `cutscene.great_null_named`, `cutscene.nightreach_star_vigil`.

---

## OUTER DETOUR — Coldfog Marches I → II *(optional, late)* — *the drained land, the cost made plain*

> **[MISSABLE] / [LATER] — OPTIONAL DETOUR, NOT THE MAIN PATH.** Coldfog is reached from the
> **hub** (`vesper_crossroads → coldfog_marches_i`, ungated), and is normally taken **late** —
> after the Solar Gleam, when you can see it for the drained place it is. It carries a back-door
> to Nightreach (`coldfog_marches_ii → nightreach_observatory`, Emberward), but **the proper
> arrival is the rim** (spine §0 rule 2). Everything in this section is optional collection +
> the **B4 set-piece**; nothing here is required to complete the West.

**At a glance** — `coldfog_marches_i` (blighted marsh) → `coldfog_marches_ii` (deep coldfog) ·
kind route · region outer · **enter** from `vesper_crossroads` (ungated, to I) **→** optional
back-door exit to `nightreach_observatory` (Emberward) · **boundary gate:** Emberward (I→II,
held) · **Gleam:** none · **rec. level ~46–50.**

### 1. Main path (of the detour)

1. **Coldfog Marches I — the blighted marsh.** From the hub, the one **drained** area in
   Vesperholm: sickly desaturated blues, snuffed lanterns, `ink` mist swallowing colour (atlas §2
   card 10) — **stays dark regardless of Gleam-count**, the visual cost of the Hollowing made
   plain. Blighted `tall_grass` carries the Dark roster (Nullmoth, Wispwane Dark/Light).
2. **The boundary — deep coldfog.** Segment I ends at a wall of deep coldfog; **Emberward**
   (held) burns through into segment II. (`coldfog_marches_i → coldfog_marches_ii`,
   `requires_ability: emberward`.)
3. **Coldfog Marches II — deep coldfog.** The drained heart of the marsh: snuffed lighthouses,
   ashen ex-Ember kin (Embergone, Dark). Two landmarks open off it (§4) — the **Drownlight
   Beacon** and the **Hollowfen Stillworks**. A back-door warp to Nightreach exists here
   (Emberward) but is the "wrong" way in story terms.
4. **Hollowfen Stillworks — the B4 set-piece.** The detour's heart: a derelict Hollowing
   **null-works** (the "old power-plant"), rows of dead null-lanterns, the machinery that drains
   the light. This is where the player **sees** the scale of the Hollowing — pairing with Nessa's
   *naming* of the Great Null at Nightreach. A powerful Storm/Dark **"charged husk"** kin guards
   the works (the reward). Its inner door is **Glimmerstep** (held) — but you need **Emberward**
   to be in Coldfog II at all.

### 2. Story beats

- **B4 (the *shown* half) — full-scale Hollowing.** Coldfog + the Stillworks reveal the works in
  the flesh: not capes, but industry — rows of snuffed lanterns, a quiet machine that eats light.
  This is the visual evidence that pays off the *naming* at Nightreach (`flag:great_null_known` is
  set at Nightreach via Nessa; the Stillworks set-piece *justifies* it). Keep it elegiac and
  unsettling — grief at scale, never cruelty; the kin are *asleep*, never harmed.
- **Arc D — the held-dark.** Coldfog is the deliberate counter-image to the brightening rim: it
  does **not** lighten with your Gleam-count. It is what Vesperholm becomes if Còr wins — make the
  contrast with the Solarium's warmth and Nightreach's stars land hard.

> *Signature lines (flavour, not script):*
> - A marsh-hermit at the works' edge: *"They didn't burn it. They didn't break it. They just...
>   turned the light down, lantern by lantern, until the whole fen forgot it was ever lit. Kindest
>   thing, they said. Kindest thing."*
> - Inside the Stillworks (sign or husk-keeper): *"Every lamp in here is sleeping, not dead. That's
>   the horror of it — and the mercy he believes in. One day the whole sky's meant to look like
>   this room."*

### 3. Mechanic introductions

- **No new Gift** (Coldfog is collection + set-piece). It exercises **Emberward** (to be here at
  all) and **Glimmerstep** (the Stillworks' inner door) — the spine §5 "old Gifts reopen new
  depths" payoff, late.
- **Type band — pure Dark.** The drained roster (Nullmoth, Wispwane, Embergone) is the game's
  densest Dark pocket — Light-typed kin thin out here (atlas §4) and bloom on the relit rim. Note
  the encounter-table contrast as a deliberate Arc-D read.
- **The drained dark resists Lamplight (spine §5 caveat).** Coldfog is the one place the
  vesperlamp's growing brightness does *not* push back the dark — even at Radiant the fog stays
  oppressive (Arc D: blighted zones don't brighten with your progress). Its secrets lean on
  **Emberward / Glimmerstep**, never on Lamplight — the deliberate counter-image to the rim.

### 4. Optional content

- **Drownlight Beacon** — spur off `coldfog_marches_ii`, `requires_ability: emberward`; reward:
  rare **Dark kin** in a snuffed lighthouse. **[MISSABLE]** — open once you're in Coldfog II
  (Emberward held).
- **Hollowfen Stillworks** — landmark off `coldfog_marches_ii`, `requires_ability: glimmerstep`
  (inner door), **reached via Emberward**; reward: a powerful **Storm/Dark "charged husk" kin** —
  the West's signature landmark and the **B4 set-piece**. **[MISSABLE]** (but a key story
  set-piece — flag it hard).
- **The Coldfog → Nightreach back-door** (`coldfog_marches_ii → nightreach_observatory`,
  Emberward) — **[MISSABLE]** convenience; the main path remains the rim.

### 5. Don't-miss callouts

- **Walk the Coldfog detour at least once for the Stillworks** — it's the West's signature
  landmark and the only place you *see* (not just hear) the full Hollowing. **[MISSABLE]** but
  thematically central; do it **late** (after the Solar Gleam) so the held-dark contrast lands.
- **Drownlight Beacon** — the West's optional Dark reward; sweep it while you're in the fog.
  **[MISSABLE]**
- Remember the **back-door to Nightreach** exists — a fast link if you came to Coldfog before
  finishing the rim, but **not** the intended first arrival at the eighth Lumenary.

### 6. Validation hooks

- **Map ids / kind:** `coldfog_marches_i`, `coldfog_marches_ii`, kind `route`, region `outer`.
- **Entry (from hub):** `vesper_crossroads → coldfog_marches_i` via `to_marsh` (**ungated**,
  bidir).
- **Boundary warp (graph.ts):** `coldfog_marches_i → coldfog_marches_ii` via `to_marsh_ii`,
  **`requires_ability: emberward`** (held), bidir.
- **Back-door warp:** `coldfog_marches_ii → nightreach_observatory` via `to_observatory_fog`,
  **`requires_ability: emberward`**, bidir — **optional**, NOT the main path (spine §0 rule 2).
- **Spur/landmark warps:** `coldfog_marches_ii → drownlight_beacon` via `to_beacon`,
  `requires_ability: emberward`, bidir; `coldfog_marches_ii → hollowfen_stillworks` via
  `to_stillworks`, **`requires_ability: glimmerstep`** (inner door; Emberward needed to be in
  Coldfog II at all), bidir.
- **Story trigger `sets_flags`:** the Stillworks set-piece is the *shown* half of B4; the
  `flag:great_null_known` flag is **set at Nightreach** (Nessa's naming, `script`, `once: true`) —
  Coldfog/Stillworks may carry narrative-only triggers but must not be required to set it (the
  detour is optional, so the flag can't depend on it).
- **Encounter zones:** blighted `tall_grass` — Nullmoth (Dark), Wispwane (Dark/Light), Embergone
  (Dark); level band ~46–50 (late detour). **Light-typed kin thinned/absent** (atlas §4 — drained
  area). Drownlight Beacon: rare Dark kin, low weight. Hollowfen Stillworks: the Storm/Dark
  "charged husk" kin as a low-weight/static reward.
- **NPC / landmark:** marsh-hermit at the works' edge; Hollowfen Stillworks set-piece (dead
  null-lanterns, husk-keeper). Dialogue/script refs `npc.coldfog_marsh_hermit`,
  `cutscene.hollowfen_stillworks`.

---

## Hand-off to Central

The Central writer picks up at **`nightreach_observatory → vesper_crossroads`** (Lanternway,
`to_crossroads`) with the player at **~lv52**, holding **ALL SIX Lantern Gifts** (Tidecall +
Glimmerstep + Updraft Kite + Emberward + **Sunsketch** + **Starreach**), **all eight Gleams**,
**`flag:crown_west`**, **`flag:hub_unlocked`**, **`flag:shortcut_windward`**, and the persistent
narrative ledger **`flag:dusk_begins`** + **`flag:met_hollowing`** + **`flag:met_cor`** +
**`flag:great_null_known`**. The Crown is complete, the Penumbra has parted,
and the four cardinal roads `vesper_crossroads → penumbra_ring` (`requires_flag:
flag:hub_unlocked`) are open; `penumbra_ring → umbral_spire` (`requires_ability: starreach` — now
held) is the final ascent. **Starreach** reopenings handed to Central/East: **Crystoll Vault**
(Cinderhead Deep, East) and **Starwell** (Penumbra Ring). Arc beats still owed downstream: **B5**
(confront the Great Null; relight the Keystar/Keylumen by *out-remembering*), and the **Dawn**
(`flag:dawn`) → [`06-postgame.md`](./06-postgame.md).
