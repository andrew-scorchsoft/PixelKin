# PixelKin Walkthrough — 01 · South (Gleams 1–2 → `crown_south`)

> Region file under the [spine](./README.md). Read its §0 rules, §2 flag strings, §3 arcs,
> §4 curve, §5 cadence, §7 template, and §10 voice first — they are binding here. Areas
> follow the §7 template exactly. Canon vocabulary only: **kin, Lumenary, Lampwarden,
> Gleam, Lantern Gift, vesperlamp, kindling, the Hollowing.**

## Region header

**The opening hour and the first two Gleams.** South is the threshold of the Wayfaring:
the cosy coastal start at **Tinderwick**, the tutorial coast through **Dimglass Coast I→II**,
and the moonlit port of **Pearlmoor Quay**. It teaches every base verb (move, talk,
interact, enter buildings, fight a wild kin, catch with the vesperlamp, the type triangle,
the first trainer battle), lands the story's inciting incident, and hands the player their
first traversal Gift, **Tidecall**.

- **Entry state:** brand-new game. Level-5 starter, a freshly gifted **vesperlamp**, an
  empty party of one, no Gleams, no flags. Player spawns at the door of their house in
  Tinderwick (`start_at {tx:8, ty:16}`).
- **Exit state handed to East:** ~level 16, party of **2–3** bonded kin, holding
  **Tidecall**, `gleam:ember` + `gleam:tide` earned, **`flag:crown_south` set** (the engine
  sets it once both South constellations relight). The East writer assumes Tidecall is held,
  so **Saltreach Fen I→II** is passable.
- **Gleams delivered:** 1 **Ember** (Brisa Tallow, Tinderwick) · 2 **Tide** (Reyl Wash,
  Pearlmoor Quay).
- **Lantern Gift delivered:** **Tidecall** (Pearlmoor Quay) — opens shallow night-water and
  immediately reopens **Gullcry Rock** back on Dimglass II.
- **Arc beats delivered:** **C1** (Fenn gifts lamp + starter, Tinderwick) · **A1** (meet
  Wren, choose starter, Tinderwick) · **A2** (first friendly Wren battle, Dimglass) ·
  **B1** (a constellation winks out — `flag:dusk_begins`, Dimglass) · **C2** (Fenn explains
  the Skyweave & the winking-out, after `dusk_begins`) · **E**: Tinderwick **Lantern-fair**,
  Pearlmoor **Tide-blessing**.
- **Arc-D lighting note:** South is the **deepest blue hour** — the darkest, coziest region
  in the game, lit almost entirely by candle-windows, lantern-buoys, and moon-on-water. Each
  Gleam earned here nudges the wash a half-shade warmer and the vesperlamp a notch brighter;
  every region after this opens visibly lighter than South.

---

### Tinderwick — *cosy coastal village at the blue hour; the Wayfaring begins*

**At a glance** — `tinderwick` (+ interiors `tinderwick_house` · `tinderwick_lumenary` hall ·
the **BEACON** `tinderwick_beacon_i/_ii/_top`) · town · south · entry: spawn at house door
`{tx:8,ty:16}`, exit: north edge to `dimglass_coast`, east Lanternway to `vesper_crossroads` ·
gate: the beacon's foot door needs **`flag:has_beacon_wick`** · **Gleam: Ember** (Brisa
Tallow, ace ~10, at the **beacon top**) · rec. level: start 5, bond-test ~8–9.

**The earned first Gleam (the 2026-06 restructure; spine §5, shape #1: tower ascent —
the BUILT worked example every region's loop varies from).** Tinderwick's tower — the
**old beacon** on the NE bluff — is where the Ember is actually relit. Brisa's bond-test no
longer happens in the hall five minutes in; it is *earned* via a loop that sends the
player up the coast road and back, which also fixes the old lv-5-vs-ace-10 cliff:

1. **Main path** (the "lantern spine" + the beacon loop):
   1. **Step out of the house.** Spawn at the door tile; movement taught by doing.
      (Optional: the warm interior, with a free **bed rest-heal**, first.)
   2. **Meet Fenn + Wren on the spine.** The `intro_mentor` cutscene gifts the
      **vesperlamp** and the **starter**; signs teach "interact".
   3. **Catch a kin in the verge** (the band straddling the north exit lane). Any catch
      sets `flag:caught_first_kin` — until then Brisa only teases (`npc.brisa_not_ready`).
   4. **Brisa's errand (the hall).** In the Lumenary hall Brisa explains: the Ember is
      relit from the **beacon**, whose **wick-key was lost on the coast road**
      (`script.brisa_quest` → `flag:beacon_quest`). The wick-locked tower door + sign
      are visible from the square — the goal stands over the town the whole time.
   5. **Walk Dimglass Coast I** — Wren's sight-challenge, the mandatory grass
      crossings, the `dusk_begins` omen — and receive the **BEACON WICK-KEY** from the
      **old lamplighter** near the north boundary (`script.give_wick` →
      `flag:has_beacon_wick`). The player returns at ~lv 7–8, not 5.
   6. **Climb the beacon.** The foot door answers the key; floors I–II are held by
      wick-tender **sight trainers** (Tansy lv7, Cole lv7/8); the spiral stairs land in
      the **lantern room**.
   7. **Earn the Ember Gleam at the lantern** — `script.beacon_battle`: Brisa's
      bond-test (ace 10, now a fair fight), then the great lamp blooms and the
      constellation answers. Down in the square, the **Lantern-fair** (Arc E) is live.
   8. **North to the coast again** — onward past the flats to Pearlmoor.

2. **Story beats**
   - **C1 — Fenn gifts the lamp & starter.** Warm, unhurried; Fenn is a *Star-tender*, never a
     "Professor."
     > Fenn: "Every Wayfarer leaves Tinderwick with two things — a lamp to carry the light
     > home, and a friend to share the walk. Mind you tend them both."
   - **A1 — Meet & choose (Wren).** Wren is warm and competitive and picks the starter that
     *beats* yours along the Ember→Verdant→Tide→Ember triangle.
     > Wren: "Whatever you pick, I'm taking the one that'll give you trouble. Race you to
     > complete the map!"
   - **E — the Lantern-fair.** Brisa's Gleam is given inside the town's lantern festival —
     belonging, not conquest.
     > Brisa: "A small flame's no lesser thing, dear. You've kept yours steady — let it
     > stand up in the sky a while."

3. **Mechanic introductions** — **move · talk · interact · enter buildings** · **first wild
   battle + catch** in the verge (`flag:caught_first_kin` is engine-set on any catch) ·
   **the fetch-quest loop** (errand → route → return) · **sight trainers** (first met as
   Wren on the coast, then formalised on the beacon stairs) · **vertical ascent** (the
   beacon's three stacked floors — the game's first "going up").

4. **Optional content**
   - **`tinderwick_house` interior** — `[MISSABLE]` cosy cottage, a parent/keepsake line and
     the opening warmth; nothing gated.
   - **Town signs (square / dock / Lumenary / mentor)** — `[MISSABLE]` the "interact" lessons;
     the dock sign teases the sea-shallows ("the buoys only answer a lit lamp").
   - **Lanternway spoke to Vesper Crossroads** — **[BUILT]** the `to_crossroads` lane leaves
     Tinderwick's east edge (and Pearlmoor's west); the hub (`vesper_crossroads`) is live with
     the Waykeeper, the Waystone plaza and signed sleeping roads. Its inward Spire road needs
     `flag:hub_unlocked` (West/endgame) and the north marsh road is an inert tease.

   **Named quests** (spine §5 kit):
   - **S2 "A Letter for Fenn"** — giver: the **house parent** (`tinderwick_house`) · steps:
     take Gran's keepsake letter → hand it to **Fenn** at his sky-watcher spot on the flats
     (post-C2 placement) → return for her thanks · flags: `flag:q_south_letter` →
     `flag:q_south_letter_given` · reward: balms + a warm line about the Wayfaring ·
     maps: `tinderwick_house`, `dimglass_coast_ii` · `[MISSABLE]` — deliberately the
     game's first delivery quest, teaching the pattern the Waykeeper's Round scales up.

5. **Don't-miss callouts**
   - **Catch your first kin in the verge before Brisa will even talk quests** — the
     catch-first gate is the tutorial's natural "go make a friend first" beat.
   - **The Lantern-fair** — the warmest set-piece of the opening hour; it sets the whole game's
     "lanterns in the dark" tone.

6. **Validation hooks** (against built `tinderwick.json` + the beacon maps)
   - **Map id / kind:** `tinderwick` · town. Interiors: `tinderwick_house`,
     `tinderwick_lumenary` (the hall), `tinderwick_beacon_i/_ii/_top` (the tower).
   - **Entry/exit:** spawn `start_at {tx:8,ty:16}`; north edge-warps `to_coast`/`to_coast_e`
     → `dimglass_coast`; east `to_crossroads {tx:27,ty:16}` → `vesper_crossroads`; beacon
     foot door `to_beacon` `interact {tx:24,ty:6}` **`requires_flag:flag:has_beacon_wick`**
     → `tinderwick_beacon_i`.
   - **The beacon quest chain (all data):** verge catch → `flag:caught_first_kin` (engine,
     any catch) → hall: `script.brisa_quest` sets `flag:beacon_quest` → Dimglass I:
     `script.give_wick` (the old lamplighter, post-`dusk_begins`) gives item `beacon_wick`
     + sets `flag:has_beacon_wick` → beacon floors: sight trainers `beacon_keeper_a/b`
     (flags `flag:beacon_keeper_*_beaten`) → top: `beacon_battle` `cutscene`
     `step_on`, `once:true`, `requires_flag:flag:caught_first_kin`,
     `blocked_ref:npc.brisa_not_ready`, `ref:script.beacon_battle` — **earns
     `gleam:ember`** (+ `crown_south` half) via trainer `lampwarden_tinderwick`.
   - **Brisa's hall stages (flag-pair NPC swaps on the dais):** `npc.brisa_not_ready` →
     `script.brisa_quest` → `npc.brisa_meet_beacon` → `npc.brisa_after` (post-Gleam).
   - **Encounters:** `verge_grass` · `tall_grass` · `encounter_rate 0.07` · kin **16**
     (w60, lv2–4) + **10** (w40, lv2–3) — level band 2–4 (§4 start-5).
   - **NPCs / festival:** `mentor` (Fenn) static `npc.mentor_intro`; **Wren** wanders the
     square (`npc.wren_intro`); Lantern-fair NPCs (`fair_piper`, `fair_kid`)
     `requires_flag:'gleam:ember'`.

---

### Dimglass Coast I — *tidal cliffside route; the first road, and the first dark omen*

**At a glance** — `dimglass_coast` · route · south · entry: south edge from Tinderwick
`{tx:6,ty:32–33}`, exit: north edge to `dimglass_coast_ii` `{tx:7,ty:0}` · gate: none
(ungated boundary) · Gleam: — (teases Tidecall + Glimmerstep) · rec. level: 5 → ~8.

1. **Main path** (south→north, alternating safe-strip ↔ grass beats per level-design §5):
   1. **Land on the south sand strip** from Tinderwick; cliff wall west, sea east. A continuous
      lit `,` spine runs the whole length — a safe lane past every grass patch.
   2. **First grass patch (`grass_a`)** — gentle wild Tide kin; the place to **practise
      catching properly** with the vesperlamp and meet the **type triangle** in earnest.
   3. **The teases.** Offshore **lantern-buoys** glow over shallows leading to **Gullcry Rock**
      (Tidecall, not yet) and a dark **cavern mouth** in the cliff → **Tideglass Cavern**
      (Glimmerstep, not yet). Both are signed: the *why* and the *come back* are explicit.
   4. **Meet Wren again (A2).** The travelling Wayfarer NPC anchors the route; Wren's first
      friendly battle teaches **trainer battles** (Wren ~2 levels under the player).
   5. **The inciting incident (B1).** On the first nightfall here, a far constellation **winks
      out**; the buoys gutter for a beat. Sets the tone — and the plot — in motion.
   6. **Continue through `grass_b/c/d`** to the north boundary and on to **Dimglass Coast II**.

2. **Story beats**
   - **A2 — First friendly Wren battle.** Teaches trainer battles in a low-stakes, cosy frame.
     > Wren: "No Lamps, no stakes — just us and our partners. Show me what your bond's worth."
   - **B1 — A constellation winks out (`flag:dusk_begins`).** Quiet, not loud; the dread is in
     the *quiet*.
     > NPC (watching the sky): "…that's the third star gone south of here this month. Folk say
     > whole towns have gone quiet. Lamps just… stop."
   - **C2 — Fenn explains the Skyweave.** After `dusk_begins`, Fenn finds the player (here or
     just into II) and names what's happening: stars anchored to gleaming kin, the long night,
     why relighting constellations matters. (This is the only spot C2 may land — South.)
     > Fenn: "The sky and the ground hold hands here, child. Snuff a kin's light and a star
     > goes dark with it. That's what we walk against."

3. **Mechanic introductions** — **catching** (the vesperlamp, on a wild Tide kin) ·
   **type basics / the triangle** · **first trainer battle** (Wren) · **Gift *teases*** (the
   gated buoy-water and cavern-mouth, deliberately unsolvable yet).

4. **Optional content**
   - **Gullcry Rock** (spur, off Dimglass **II**) — **[BUILT]** needs **Tidecall** (earned at
     Pearlmoor this region). Visible from I as the offshore buoy line; reward: the rare
     **harbour-light kin (#29 Glostern)** in the surf + the **Tide Charm** (the South's best
     lamp, catch ×2.0) at the high stone. *(The old "sea-bird kin" note predates the locked
     dex, which has no Tide bird — Glostern's drifting harbour-lantern read carries the same
     "the rock keeps a light" promise.)* A same-region backtrack the moment Tidecall lands.
   - **Tideglass Cavern** (landmark, off Dimglass **II**) — `[LATER]` needs **Glimmerstep**
     (earned at Lowleaf, *East*). The dark cliff-mouth `to_tideglass` warp; signature rare
     water kin. A long-game backtrack — tag and move on.
   - **`tide_shallows` water zone** — `[LATER]` **Tidecall**: a low-weight rare Tide kin in the
     gated shallows, the spur-reward read.

5. **Don't-miss callouts**
   - **Catch a second kin here** — you want a party of 2 before Pearlmoor's Tide Lumenary; the
     coast's wild Tide kin are exactly the answer to Reyl's water team is *not* — bring an Ember
     or grassy partner along the triangle.
   - **Note the buoys and the cave-mouth.** They are promises. Keep a mental list — the spine's
     whole pleasure is the map reopening itself when Tidecall (and later Glimmerstep) lands.

6. **Validation hooks** (against built `dimglass_coast.json`)
   - **Map id / kind:** `dimglass_coast` · route, 18×34, vertical.
   - **Entry/exit:** south land-in from Tinderwick `to_tinderwick` `{tx:6,ty:33}` (+ `_w {5,33}`,
     `_e {7,33}`) → `tinderwick {tx:14,ty:3}`; north `to_coast_ii` `step_on {tx:7,ty:0}` →
     `dimglass_coast_ii {tx:7,ty:31}`, `facing:up`, `fade`.
   - **Gated warps (teases):** `to_gullcry` `step_on {tx:14,ty:5}` **`requires_ability:tidecall`**
     → `gullcry_rock {tx:4,ty:8}`; `to_tideglass` `interact {tx:2,ty:9}`
     **`requires_ability:glimmerstep`** → `tideglass_cavern {tx:4,ty:8}`, `door`.
   - **Gates:** `AbilityGate` `shallows_tide` (`ability:tidecall`, `effect:make_passable`) over
     shallows tiles `{14–15, 4–6}`.
   - **Encounters:** four optional patches (`grass_a–d`, `tall_grass`, rate 0.09, band 3–6)
     PLUS the two **[BUILT] mandatory crossings** — `crossing_a rect{3,9,11,2}` and
     `crossing_b rect{3,26,11,2}`, rate 0.10 — full-corridor bands (tallgrass on the green,
     **dunegrass** over the beach) with the lit lane carved out, so the road north passes
     *through* encounter ground (level-design §11 rule 7). Gated water:
     `tide_shallows rect{14,5,2,4}` `water` **`requires_ability:tidecall`** (rare read).
   - **NPCs / signs:** **[BUILT] Wren is a SIGHT trainer** at `{5,11}` facing the lane
     (`sight_range:4`, `script.wren_dimglass`, swap to `npc.dimglass_wayfarer` once
     `flag:wren_dimglass_battled`). The **old lamplighter** appears post-`dusk_begins` at
     `{10,29}` and hands the **beacon wick-key** (`script.give_wick` →
     `flag:has_beacon_wick`; the Tinderwick beacon quest's route leg), then swaps to the
     plain witness. Item caches `cache_balm`/`cache_lamps` beside the lane. Signs:
     buoys / cave / route / boundary.
   - **New refs to add when built:** a `flag:dusk_begins` cutscene trigger (B1) and a `script`
     ref for the Wren A2 trainer-battle cutscene (`reward_flags`); the C2 Fenn cutscene may sit
     here or at the head of `dimglass_coast_ii`.

---

### Dimglass Coast II — *tidal flats; the boundary that opens later*

**At a glance** — `dimglass_coast_ii` · route · south · entry: south from `dimglass_coast`
`{tx:7,ty:31}`, exit: north to `pearlmoor_quay` (via `to_quay`) · gate: **none** (the
boundary is ungated; the *spurs* off it are gift-gated) · Gleam: — · rec. level: ~8 → ~10.

1. **Main path** (continues south→north over tidal flats):
   1. **Cross the flats** — wider, lower, wetter than segment I; lantern-buoys thicker offshore.
      Still a safe lane; encounter band a touch higher to bridge toward Pearlmoor.
   2. **The two spur warps live here.** This is the segment the §3 example diagram hangs the
      Gullcry Rock (Tidecall) and Tideglass Cavern (Glimmerstep) branches off — both visible,
      both gated, both signed.
   3. **Sight-line Pearlmoor.** Frame the moonlit port's masts and lantern-strings on the north
      horizon so the next town is a visible destination.
   4. **North to Pearlmoor Quay** (`to_quay`, ungated).

2. **Story beats** — South carries no *new* arc beat unique to II (B1/A2/C2 land on segment I /
   the boundary); II is the cooldown stretch that *delivers the teases into reach*. If C2 (Fenn)
   was held back, it may open here. Keep the tone the deepest blue-hour cosy in the game.

3. **Mechanic introductions** — none new; reinforces catching + trainer battles, and **stages
   the "come back later" web**: this is where the player physically stands beside content they
   can't yet open and learns to remember it.

4. **Optional content**
   - **The netmender's net-floats** — a single item cache on the flats
     (`flag:picked_net_floats`, band 8–10): the collinear errand leg of Pearlmoor's
     **Causeway Bell** loop (see Pearlmoor §1). New ref to add when wired.
   - **Gullcry Rock** (spur) — **[BUILT]** **Tidecall** (this region, at Pearlmoor): the rare
     harbour-light kin (#29 Glostern) + the Tide Charm. **Becomes accessible the moment you
     earn Tidecall — backtrack here.** (Post-Tidecall it also hosts S1's three dark buoys —
     see Pearlmoor's Named quests.)
   - **Tideglass Cavern** (landmark) — `[LATER]` **Glimmerstep** (East): signature rare water
     kin in a micro-dungeon. Long-game return. **Also the canonical Lamplight exemplar** (spine
     §5): first explored at **Warmlight**, the cavern keeps a deeper nook + a hidden item beyond
     the lamp's reach until a **Starlight+** return reveals them — `[LATER: Lamplight ≥ Starlight]`
     `[MISSABLE]`, additive only (the glowmoss/water-lit route is visible at any tier).

5. **Don't-miss callouts**
   - **Remember this junction.** It is the South region's single richest backtrack node: one
     Gift (Tidecall) you'll hold within the hour reopens Gullcry Rock right here.

6. **Validation hooks** (`dimglass_coast_ii` — to be built; mirror segment I's conventions)
   - **Map id / kind:** `dimglass_coast_ii` · route, vertical tidal-flats.
   - **Entry/exit:** south land-in `{tx:7,ty:31}` from `dimglass_coast.to_coast_ii`; north warp
     **`to_quay`** → `pearlmoor_quay` (matches graph edge `dimglass_coast_ii → pearlmoor_quay`,
     ungated, bidirectional).
   - **Gated spur warps (graph-pinned):** `to_gullcry` **`requires_ability:tidecall`** →
     `gullcry_rock`; `to_tideglass` **`requires_ability:glimmerstep`** → `tideglass_cavern`.
     (Both edges already declared in `graph.ts:144–145` *off `dimglass_coast_ii`* — the built
     segment-I teases are the visible promise; the actual gated warps belong on II to match the
     graph.)
   - **Encounters:** `tall_grass` + gated `water` zones, Tide / Tide-Light kin (Brinelet, Lumpin,
     Mooncatch-adjacent), **level band ~8–10** (§4, no cliff into Pearlmoor's 12).
   - **Signs/NPC:** a boundary sign sight-lining Pearlmoor; a route NPC reiterating the buoy/cave
     teases. Originality + canon-vocabulary pass per spine §9.

---

### Pearlmoor Quay — *moonlit fishing port; the second Gleam and the first Gift*

**At a glance** — `pearlmoor_quay` (+ the breakwater `pearlmoor_breakwater` **[NEW MAP]**) ·
town · south · entry: south from `dimglass_coast_ii`, exit: onward to `saltreach_fen_i`
(via `to_fen`, East) + Lanternway `to_crossroads` · gate: **Tidecall** (its own islets &
sea-shrine — but the Lumenary itself is **not** gated, per spine §0 rule 1; the breakwater
is walked **on foot**) · **Gleam: Tide** (Reyl Wash, ace ~16, at the **Moor-bell shrine**)
+ **Tidecall** · rec. level: 12, bond-test ~13–14.

**The earned loop — "The Causeway Bell" (spine §5, shape #2: breakwater walk).** The
Tide-blessing cannot begin until the Moor-bell rings — and the bell-rope is in the
netmender's keeping.

1. **Main path:**
   1. **Arrive on the wet boardwalks** — moon on water, `bone` sails, lantern-strings between
      masts. The cosiest, saltiest town music in South. **The tease:** out along the
      breakwater, visible from the first screen, stands the **Moor-bell shrine** — bell
      silent, the Tide-blessing boats idle at their moorings.
   2. **The Lumenary hall is reachable on foot** (no Tidecall needed — §0 rule 1). Reyl
      meets you there with the hook: *"Tides go out so they can come back — but the
      blessing waits on the moor-bell, and the moor-bell waits on you."*
      (`script.reyl_quest` → `flag:q_south_bell`; until the bell rings his bond-test
      trigger answers with a `blocked_ref` in the same voice.)
   3. **The netmender's errand (collinear).** The quay netmender keeps the bell-rope, but
      her **net-floats** drifted south in the last storm — a single item cache one screen
      back on **Dimglass Coast II** (band 8–10, ground just walked). Return them →
      `flag:q_south_has_rope` (NPC swap hands the rope).
   4. **Walk the breakwater** (`pearlmoor_breakwater` — the foot gate needs the rope;
      blocked line in the netmender's voice). Two **net-hand sight trainers** (lv 12–14)
      work the causeway; the bell platform and shrine stand at its end over open water.
   5. **Ring the Moor-bell** (`script.ring_moorbell` → `flag:q_south_bell_rung`) — the
      Tide-blessing begins behind you: boats light, the quay sings, and **Reyl walks out
      to the shrine** (hall ↔ shrine NPC swap).
   6. **Face Lampwarden Reyl Wash at the shrine (Tide, ace ~16).** Winning earns
      **Gleam: Tide** and the **Tidecall** Lantern Gift, inside the festival (Arc E) —
      heal/restock first: **[BUILT]** the inn rest (`script.inn_rest`) + the chandlery's
      one-time crossing-kit.
   7. **`flag:crown_south` sets** (engine-set once both Ember + Tide are held) — the South
      quadrant's two constellations are relit; the Vesper Crossroads' south approach is primed.
   8. **Now-accessible callout:** with **Tidecall** in hand, **backtrack to Dimglass II →
      Gullcry Rock** (the rare harbour-light kin + Tide Charm), cross Pearlmoor's own shallow
      islets to the sea-shrine, and the East road's **Saltreach Fen I→II** boundary is now
      passable.
   9. **The 12→16 on-ramp.** The bell loop carries the player to ~13–14 against Reyl's ace 16
      (the same cliff-softening the Beacon did for 5-vs-10); the remaining levels are earned
      in Pearlmoor's Tidecall islet/sea-shrine loop and the Gullcry Rock backtrack before
      Saltreach Fen — so East opens with no level cliff.

2. **Story beats**
   - **E — the Tide-blessing.** Reyl's Gleam is given inside the port's tide festival; warm,
     communal, a little melancholy at the water's edge.
     > Reyl: "Tides go out so they can come back, see. Same with the light. You read that
     > rhythm well — go on, ask the sea to part for you."
   - (No A/B/C beat is *owned* by Pearlmoor in the spine — keep Wren/Fenn to their assigned
     spots; Pearlmoor's weight is the Gift, the festival, and the quadrant closing.)

3. **Mechanic introductions** — **Tidecall earned** (cross shallow night-water to lantern-buoys
   and islets). Its **immediate "now accessible" reopening:** Gullcry Rock (Dimglass II) +
   Pearlmoor's sea-shrine + the Saltreach Fen II channels. From here on, battles may assume
   **status conditions** are live (spine §5 dependency) — write Reyl's team to lean on Tide's
   `drench`/`doze` flavour but flag it as roadmap-dependent.

4. **Optional content**
   - **Pearlmoor sea-shrine / islets** — `[MUST-DO]` once Tidecall lands: the town's own
     Tidecall content, a short rewarding loop and the cleanest demonstration of the new Gift.
   - **Gullcry Rock backtrack** (Dimglass II spur) — `[MUST-DO]` **[BUILT]** the rare
     harbour-light kin (Glostern) + the Tide Charm, now reachable; the region's signature
     "the map reopened" payoff.
   - **Lanternway → Vesper Crossroads** — `[MISSABLE]` discover the hub as South's fast-travel
     anchor; its inward Spire roads remain `[LATER]` (`flag:hub_unlocked`, West/endgame).

   **Named quests** (spine §5 kit; South's slate, with S2 over in Tinderwick):
   - **S1 "The Last Buoy Out"** — giver: the **netmender** (post-bell, her swap NPC) ·
     steps: relight the three dark buoys in the Dimglass II shallows (interact scripts on
     the buoy line, Tidecall water) → return · flags: `flag:q_south_buoys` →
     `flag:q_south_buoys_lit` · reward: the **Drift Charm** · maps: `pearlmoor_quay`,
     `dimglass_coast_ii` · `[LATER: Tidecall]` (a "now accessible" callout the moment the
     Gift lands).
   - **S3 "The Cavern Keeps a Light"** — giver: the **old fisher** (inn) · steps: relight
     the wreck-lamp deep in **Tideglass Cavern** → tell him it still burns · flags:
     `flag:q_south_wrecklamp` → `flag:q_south_wrecklamp_lit` · reward: a **Tide Charm
     upgrade** · maps: `pearlmoor_quay`, `tideglass_cavern` · `[LATER: Glimmerstep]`, with
     a deeper page beyond the lamp's reach `[LATER: Lamplight ≥ Starlight]`.
   - **R1 "Wicks for the Lamplighter"** — the Waykeeper's Round, leg 1 (live now): parcel
     from the **Waykeeper** (`vesper_crossroads`) → the **old lamplighter** (Dimglass I) ·
     flags: `flag:q_round_lamplighter` · reward: bright-lamp kit · `[wakes with spoke]`
     (south spokes are live).
   - **R2 "Salt-glass for the Chandler"** — Round leg 2 (live now): Waykeeper parcel → the
     **Pearlmoor chandler** · flags: `flag:q_round_chandler` · reward: balm kit ·
     `[wakes with spoke]`.

5. **Don't-miss callouts**
   - **Run the Gullcry Rock backtrack before leaving South** — it is the clearest lesson the
     game ever teaches about *why you keep a list of teased spots*, and the Tide Charm +
     harbour-light kin are a tidy reward right when the party wants depth.
   - **The Tide-blessing festival** — pair it with the Lantern-fair as South's two warm
     set-pieces; together they establish "Gleam = belonging" before the stakes harden in East.

6. **Validation hooks** (`pearlmoor_quay` is built; the bell loop + `pearlmoor_breakwater`
   are new refs to add when built)
   - **Map id / kind:** `pearlmoor_quay` · town; **`pearlmoor_breakwater`** **[NEW MAP]** ·
     route/causeway, ~12×28, walked on foot (no Tidecall anywhere on it — §0 rule 1).
   - **Entry/exit:** south land-in from `dimglass_coast_ii` (paired with its `to_quay`); onward
     **`to_fen`** → `saltreach_fen_i` (graph edge, ungated); **`to_crossroads`** → `vesper_crossroads`
     (Lanternway spoke, bidirectional, per `graph.ts:159`); breakwater foot gate
     **`to_breakwater`** `requires_flag:flag:q_south_has_rope` with a `blocked_ref` in the
     netmender's voice.
   - **The bell quest chain (all data):** `script.reyl_quest` (hall) sets `flag:q_south_bell`
     → net-floats item cache on `dimglass_coast_ii` (`flag:picked_net_floats`) → netmender
     NPC swap gives the rope (`flag:q_south_has_rope`) → breakwater walk (2 net-hand SIGHT
     trainers, lv 12–14) → `script.ring_moorbell` sets `flag:q_south_bell_rung` (festival
     NPC wave + Reyl hall↔shrine swap).
   - **Lumenary (ungated) + Gift + flags:** the bond-test trigger at the **Moor-bell shrine**,
     `requires_flag:flag:q_south_bell_rung` with `blocked_ref` (Reyl's "the moor-bell waits
     on you"), **earns `gleam:tide`** and **grants ability `tidecall`**; the engine sets
     **`flag:crown_south`** once `gleam:ember`+`gleam:tide` are both held. Lampwarden
     **Reyl Wash** (Tide, ace ~16).
   - **Quest-chain hooks (rule 3):** opened `flag:q_south_bell` / `q_south_has_rope` /
     `q_south_bell_rung` are consumed by the breakwater gate, the netmender swap pair and
     the bond-test trigger; S1/S3/R1/R2 flags as listed in their Named-quests entries.
   - **Tidecall-gated town content:** islet/sea-shrine warps + `water` `EncounterZone`s with
     **`requires_ability:tidecall`**; an `AbilityGate` (`tidecall`,`make_passable`) over the
     harbour shallows.
   - **Encounters:** harbour/islet `water` (Tidecall-gated) — Mooncatch (Tide), Glostern
     (Tide/Light) per atlas; **level band ~12–16** (§4, continuous into Saltreach's 16).
   - **NPCs / festival:** Reyl Wash keeper NPC + `script.lumenary_pearlmoor`; the **Tide-blessing**
     staged as a flag-gated festival cutscene + NPC swap around the Lumenary. Originality +
     canon-vocabulary pass (kin/Lumenary/Lampwarden/Gleam/Lantern Gift/vesperlamp) per spine §9/§10.

---

## Region handoff (to [`02-east.md`](./02-east.md))

Player leaves South at **~level 16**, party of **2–3**, holding **Tidecall**, with
`gleam:ember` + `gleam:tide` and **`flag:crown_south` set**. `flag:dusk_begins` is set (B1
fired on Dimglass). The next region opens **lighter** than South's deep blue hour, and may
assume Tidecall is in hand to pass **Saltreach Fen I→II** (`graph.ts:124`). Still tagged
`[LATER]` from South and owed to East/late-game: **Tideglass Cavern** (Glimmerstep, East) and
the hub's inward Spire roads (`flag:hub_unlocked`, West/endgame).
