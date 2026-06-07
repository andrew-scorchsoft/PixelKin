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

**At a glance** — `tinderwick` (+ interior `tinderwick_house`) · town · south · entry:
spawn at house door `{tx:8,ty:16}`, exit: north edge to `dimglass_coast` · gate: none
(start) · **Gleam: Ember** (Brisa Tallow, ace ~10) · rec. level: start 5.

1. **Main path** (the "lantern spine", south→north per level-design §4/§7.1):
   1. **Step out of the house.** Spawn at the door tile; the only action is to move — movement
      taught by doing. (Optional: the warm interior `tinderwick_house` first.)
   2. **Meet Fenn + Wren on the spine.** A few tiles north the path narrows past **Star-tender
      Fenn** (the `intro_mentor` cutscene); Wren is here too, another young Wayfarer. Talking
      is taught; the cutscene gifts the **vesperlamp** and lets the player **choose a starter**.
   3. **Read a sign.** Square/dock/Lumenary/mentor signs along the spine teach "interact"
      (no pop-up tutorials).
   4. **The soft gate.** The **Lumenary** sits central and tallest as the visible goal — but
      Brisa won't hold the bond-test on a lone level-5 starter. The player is nudged: *go catch
      a kin first.* (The town's small verge does that; see below.)
   5. **First wild battle in the verge.** The tall-grass band straddles the north exit lane —
      the classic "first step into the grass" happens as the player heads out (and gives them
      a wild kin to catch toward the soft-gate).
   6. **Earn the Ember Gleam.** With a caught kin in tow, return to the Lumenary; **Brisa
      Tallow** vouches the player's bond. Earns **Gleam: Ember** — wrapped in the
      **Lantern-fair** festival (Arc E).
   7. **North to the coast** when ready (`to_coast` edge).

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

3. **Mechanic introductions** — **move · talk · interact · enter buildings** (the house +
   Lumenary door warps) · **first wild battle** in the verge. (Catching is *taught* here as
   intent — "go catch a kin first" — and *performed* properly on Dimglass; the engine soft-gate
   flag is set by catching at least one wild kin per spine §4.)

4. **Optional content**
   - **`tinderwick_house` interior** — `[MISSABLE]` cosy cottage, a parent/keepsake line and
     the opening warmth; nothing gated.
   - **Town signs (square / dock / Lumenary / mentor)** — `[MISSABLE]` the "interact" lessons;
     the dock sign teases the sea-shallows ("the buoys only answer a lit lamp").
   - **Lanternway spoke to Vesper Crossroads** — `[LATER]` a `to_crossroads` exit exists in the
     graph; the hub is discovered as the South fast-travel anchor but its inward roads need
     `flag:hub_unlocked` (West/endgame). Tag as a tease only.

5. **Don't-miss callouts**
   - **Catch your first kin in the verge before challenging Brisa** — the soft-gate is the
     tutorial's natural "go make a friend first" beat; skipping it just walls the Lumenary.
   - **The Lantern-fair** — the warmest set-piece of the opening hour; it sets the whole game's
     "lanterns in the dark" tone.

6. **Validation hooks** (against built `tinderwick.json`)
   - **Map id / kind:** `tinderwick` · town. Interior `tinderwick_house`.
   - **Entry/exit:** spawn `start_at {tx:8,ty:16}`; north edge-warps `to_coast` `{tx:14,ty:0}`
     (+ `to_coast_w` `{13,0}`, `to_coast_e` `{15,0}`) → `dimglass_coast` land-in `{tx:6,ty:32}`,
     `facing:up`, `fade`. House: `to_house` `interact` `{tx:8,ty:15}` → `tinderwick_house`
     `{tx:5,ty:7}`, `door`.
   - **Triggers / flags:** `intro_mentor` `cutscene` `step_on {tx:12,ty:10}`, `once:true`,
     `ref:script.intro_mentor`, **`sets_flags:[flag:has_vesperlamp, flag:has_starter]`**.
     `lumenary_battle` `cutscene` `interact {tx:18,ty:8}`, `ref:script.lumenary_tinderwick`,
     `once:true`, **`requires_flag:flag:has_starter`** — and must additionally require the
     "caught a wild kin" soft-gate flag (spine §4) before Brisa fights; **earns `gleam:ember`**.
     Signs: `sign_shop {6,9}`, `sign_lumenary {21,9}`, `sign_mentor {13,11}`, `sign_dock {9,18}`.
   - **Encounters:** `verge_grass` · `tall_grass` · `rect{tx:12,ty:2,w:6,h:2}` ·
     `encounter_rate 0.07` · table kin_id **16** (w60, lv2–4) + **10** (w40, lv2–3) — Ember /
     Light town kin (Wickmoth, Tallowpup, Glimflit per atlas), **level band 2–4** (§4 start-5).
   - **NPCs / Lumenary / festival:** `mentor` (Fenn) `{tx:12,ty:11}` `static`
     `dialogue_ref:npc.mentor_intro`; `child_runner` (repurpose as **Wren**) `{tx:20,ty:14}`
     `wander` `npc.child_lanterns`. Lumenary keeper **Brisa Tallow** (Ember) via
     `script.lumenary_tinderwick`; Lantern-fair staged around the Lumenary as a flag-gated
     festival cutscene + NPC swap.

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
   - **Gullcry Rock** (spur, off Dimglass **II**) — `[LATER]` needs **Tidecall** (earned at
     Pearlmoor this region). Visible from I as the offshore buoy line; reward: rare sea-bird
     kin + a Tide charm. Becomes a same-region backtrack the moment Tidecall is in hand.
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
   - **Encounters:** `grass_a rect{3,4,4,3}`, `grass_b rect{4,12,4,3}`, `grass_c rect{12,17,3,3}`,
     `grass_d rect{3,22,4,3}` — all `tall_grass`, `encounter_rate 0.09`, table kin_id **26**+**27**
     (Brinelet/Lumpin, Tide / Tide-Light), **level band 3–6** (§4 5→~8). Gated water:
     `tide_shallows rect{14,4,2,3}` `water` **`requires_ability:tidecall`**, kin_id **29** w100
     lv5–7 (low-weight rare read).
   - **NPCs / signs:** `wayfarer` `{tx:9,ty:10}` `look_around` `npc.dimglass_wayfarer` (carries
     route advice + the Gift teases in-character; the anchor for the **Wren A2** battle script and
     the **B1** sky cutscene). Signs: `sign_buoys {2,7}` (`sign.dimglass_buoys` — "buoys answer a
     lit lamp"), `sign_shore {13,8}`, `sign_route {3,16}`, `sign_boundary {2,28}`
     (`sign.dimglass_to_pearlmoor`).
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
   - **Gullcry Rock** (spur) — `[LATER]` **Tidecall** (this region, at Pearlmoor): rare sea-bird
     kin + Tide charm. **Becomes accessible the moment you earn Tidecall — backtrack here.**
   - **Tideglass Cavern** (landmark) — `[LATER]` **Glimmerstep** (East): signature rare water
     kin in a micro-dungeon. Long-game return.

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

**At a glance** — `pearlmoor_quay` · town · south · entry: south from `dimglass_coast_ii`,
exit: onward to `saltreach_fen_i` (via `to_fen`, East) + Lanternway `to_crossroads` ·
gate: **Tidecall** (its own islets & sea-shrine — but the Lumenary itself is **not** gated,
per spine §0 rule 1) · **Gleam: Tide** (Reyl Wash, ace ~16) + **Tidecall** · rec. level: 12.

1. **Main path:**
   1. **Arrive on the wet boardwalks** — moon on water, `bone` sails, lantern-strings between
      masts. The cosiest, saltiest town music in South.
   2. **The Lumenary is reachable on foot** (no Tidecall needed — §0 rule 1). The town's own
      *islets and sea-shrine* are the Tidecall-gated content, teased from the quay.
   3. **Heal, restock, build the party to ~12.** Bring an Ember or grassy partner — Reyl's team
      is Tide; the triangle matters.
   4. **Face Lampwarden Reyl Wash (Tide, ace ~16).** Winning earns **Gleam: Tide** and the
      **Tidecall** Lantern Gift, wrapped in the **Tide-blessing** festival (Arc E).
   5. **`flag:crown_south` sets** (engine-set once both Ember + Tide are held) — the South
      quadrant's two constellations are relit; the Vesper Crossroads' south approach is primed.
   6. **Now-accessible callout:** with **Tidecall** in hand, **backtrack to Dimglass II →
      Gullcry Rock** (rare sea-bird kin + Tide charm), cross Pearlmoor's own shallow islets to
      the sea-shrine, and the East road's **Saltreach Fen I→II** boundary is now passable.

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
   - **Gullcry Rock backtrack** (Dimglass II spur) — `[MUST-DO]` rare sea-bird kin + Tide charm,
     now reachable; the region's signature "the map reopened" payoff.
   - **Lanternway → Vesper Crossroads** — `[MISSABLE]` discover the hub as South's fast-travel
     anchor; its inward Spire roads remain `[LATER]` (`flag:hub_unlocked`, West/endgame).

5. **Don't-miss callouts**
   - **Run the Gullcry Rock backtrack before leaving South** — it is the clearest lesson the
     game ever teaches about *why you keep a list of teased spots*, and the Tide charm + sea-bird
     kin are a tidy reward right when the party wants depth.
   - **The Tide-blessing festival** — pair it with the Lantern-fair as South's two warm
     set-pieces; together they establish "Gleam = belonging" before the stakes harden in East.

6. **Validation hooks** (`pearlmoor_quay` — to be built)
   - **Map id / kind:** `pearlmoor_quay` · town.
   - **Entry/exit:** south land-in from `dimglass_coast_ii` (paired with its `to_quay`); onward
     **`to_fen`** → `saltreach_fen_i` (graph edge, ungated); **`to_crossroads`** → `vesper_crossroads`
     (Lanternway spoke, bidirectional, per `graph.ts:159`).
   - **Lumenary (ungated) + Gift + flags:** a `lumenary_pearlmoor` cutscene trigger,
     `requires_flag:flag:has_starter` (and reachable **without** Tidecall — §0 rule 1),
     **earns `gleam:tide`** and **grants ability `tidecall`**; the engine sets **`flag:crown_south`**
     once `gleam:ember`+`gleam:tide` are both held. Lampwarden **Reyl Wash** (Tide, ace ~16).
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
