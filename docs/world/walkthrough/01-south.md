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

- **Entry state:** brand-new game. NO kin and NO lamp yet — the opening is the **satchel
  errand** (below): the player spawns at the door of their house in Tinderwick, is turned
  back at the warded north gate, finds **Fenn at the Vesper Crossroads waystone**, fetches
  his satchel from the store, and receives the **vesperlamp** + level-5 **starter** at the
  waystone ceremony. No Gleams, no flags.
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

### Cinematic staging (BUILT — the worked reference for every later region)

South is the **built example** of the [`cinematics.md`](../cinematics.md) standard; later
regions copy its scripts. What's wired (`src/game/content/scripts.ts` + `cinematics.ts`):

- **Cold open (`coldopen_south`).** New Game opens on a 4-panel illustrated prologue
  (`CinematicScene`) before Tinderwick: the constellation-full sky → a star **winks out**
  (`silence` → gutter sting → `flash`) → the lamplit doorway / the calling → a distant cowled
  figure under the dead sky (the Hollowing **seed**). Foreboding **and** aspirational; skippable
  (Cancel). Music: `coldopen-foreboding`.
- **C1 the satchel errand → `intro_mentor`.** C1 is a small LOOP, not a tile-touch: the
  north **gate-warden intercepts** an unstarted player (`script.gate_warden` — emote, warning,
  walked back a step; the coast warps are `has_starter`-gated), every early voice points EAST,
  Fenn **hails the player across the plaza** (`script.fenn_wave`, camera focus) and asks for his
  forgotten satchel (`script.fenn_crossroads` → `flag:fenn_errand`); the store counter holds it
  (`script.take_satchel` → `flag:has_satchel`); the ceremony (`script.intro_mentor`) then runs
  **at the waystone** — portraits (grave→warm→smile), a warm `tint` bloom on the vesperlamp
  gift, the cosy bed holding (dread only in Fenn's face on the lost-star line).
- **B1 `dusk_begins`** — the load-bearing dread set-piece: `letterbox on → silence(hold) →
  narrate → world-star-gutter sting + cold `tint` + `shake` → narrate → crossfade the bed back,
  uneasier → letterbox off`. **This staging is binding for every later "a light fails" beat.**
- **Gleam payoffs (`beacon_battle` Ember, `lumenary_pearlmoor` Tide)** — minor→major: `musicFade`
  to silence → warm/cool `tint` bloom + lamp sfx → `gleam` → **crossfade to the festival swell**
  (`gleam-emotional`) → Brisa/Reyl portrait `proud`. A Gleam is belonging; the music says so.
- **Early Hollowing seeds (foreboding only — B2 still formally lands in East):** cold-open panel
  4; `sign.dimglass_pinned_letter` (the Hollowing's courteous unsigned voice, name scratched out,
  "DO NOT LISTEN" added beneath); the old lamplighter's grave aside in `give_wick`.
- **Assets:** panels `public/assets/backgrounds/cinematic/coldopen-0{1..4}.webp`; portraits
  `public/assets/portraits/{fenn,wren,brisa,reyl,lamplighter}.png`; cues `coldopen-foreboding`,
  `gleam-emotional`, sfx `world-star-gutter-*`. All degrade silently if absent.

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

1. **Main path** (the satchel errand + the beacon loop):
   1. **Step out of the house.** Spawn at the door tile; movement taught by doing.
      (Optional: the warm interior, with a free **bed rest-heal**, first — Gran points
      east to Fenn.)
   2. **Try the north gate (most players will).** The **gate-warden** runs the intercept:
      it's dangerous out there without a lit lamp, and Star-tender Fenn went EAST to the
      Crossroads waystone, asking after you. (Band `gate_warden`, hidden once
      `flag:has_starter`; both coast warps gated on the same flag.) **Wren** wanders by
      the garden on the way east — A1's meet-the-rival beat.
   3. **Walk the Lanternway to the waystone.** The lit east lane is safe (and pre-starter,
      wild encounters can't fire anyway). Fenn hails you into the plaza (`fenn_wave`),
      then asks the favour: his **satchel**, forgotten on the Tinderwick store counter
      (`script.fenn_crossroads` → `flag:fenn_errand`). The Pearlmoor spoke east is
      `has_starter`-gated, so the errand can't be wandered past.
   4. **Fetch the satchel** (the store, beside the counter — an item_cache;
      `flag:has_satchel`), and bring it back to the waystone.
   5. **The ceremony (`script.intro_mentor`).** Out of the satchel: the **vesperlamp**,
      then the **starter** — chosen at the crossroads where every Wayfaring in
      Vesperholm begins. Fenn points you home: verge grass, the keeper's kit, Brisa.
   6. **Catch a kin in the verge** (the band straddling the north exit lane). Any catch
      sets `flag:caught_first_kin` — until then Brisa only teases (`npc.brisa_not_ready`).
   7. **Brisa's errand (the hall).** In the Lumenary hall Brisa explains: the Ember is
      relit from the **beacon**, whose **wick-key was lost on the coast road**
      (`script.brisa_quest` → `flag:beacon_quest`). The wick-locked tower door + sign
      are visible from the square — the goal stands over the town the whole time.
   8. **Walk Dimglass Coast I** — Wren's sight-challenge, the mandatory grass
      crossings, the `dusk_begins` omen — and receive the **BEACON WICK-KEY** from the
      **old lamplighter** near the north boundary (`script.give_wick` →
      `flag:has_beacon_wick`). The player returns at ~lv 7–8, not 5.
   9. **Climb the beacon.** The foot door answers the key; floors I–II are held by
      wick-tender **sight trainers** (Tansy lv7, Cole lv7/8); the spiral stairs land in
      the **lantern room**.
   10. **Earn the Ember Gleam at the lantern** — `script.beacon_battle`: Brisa's
       bond-test (ace 10, now a fair fight), then the great lamp blooms and the
       constellation answers. Down in the square, the **Lantern-fair** (Arc E) is live.
   11. **North to the coast again** — onward past the flats to Pearlmoor.

2. **Story beats**
   - **C1 — the satchel errand → Fenn gifts the lamp & starter at the waystone.** Warm,
     unhurried; Fenn is a *Star-tender*, never a "Professor" — and a little forgetful, which
     is what makes the opening a favour between friends rather than a hand-out.
     > Fenn: "Every Wayfarer leaves with two things, and they have been riding in this old
     > bag all along... And fitting, is it not — every Wayfaring in Vesperholm begins at a
     > crossroads."
   - **A1 — Meet & choose (Wren).** Wren is warm and competitive and picks the starter that
     *beats* yours along the Ember→Verdant→Tide→Ember triangle.
     > Wren: "Whatever you pick, I'm taking the one that'll give you trouble. Race you to
     > complete the map!"
   - **E — the Lantern-fair.** Brisa's Gleam is given inside the town's lantern festival —
     belonging, not conquest.
     > Brisa: "A small flame's no lesser thing, dear. You've kept yours steady — let it
     > stand up in the sky a while."

3. **Mechanic introductions** — **move · talk · interact · enter buildings** · **the
   fetch-quest loop, twice and rising** (the satchel errand in miniature, then Brisa's
   wick-key at route scale — the pattern the Waykeeper's Round scales up) · **first wild
   battle + catch** in the verge (`flag:caught_first_kin` is engine-set on any catch) ·
   **sight trainers** (first met as Wren on the coast, then formalised on the beacon
   stairs) · **vertical ascent** (the beacon's three stacked floors — the game's first
   "going up").

4. **Optional content**
   - **`tinderwick_house` interior** — `[MISSABLE]` cosy cottage, a parent/keepsake line and
     the opening warmth; nothing gated.
   - **Town signs (square / dock / Lumenary / mentor)** — `[MISSABLE]` the "interact" lessons;
     the dock sign teases the sea-shallows ("the buoys only answer a lit lamp").
   - **Lanternway spoke to Vesper Crossroads** — **[BUILT, and now on the main path]** the
     `to_crossroads` lane leaves Tinderwick's east edge (and Pearlmoor's west); the hub
     (`vesper_crossroads`) is live with the Waykeeper, the Waystone plaza, **Fenn's opening
     stages at the waystone**, and signed sleeping roads. The Pearlmoor spoke is
     `has_starter`-gated; the inward Spire road needs `flag:hub_unlocked` (West/endgame)
     and the north marsh road is an inert tease.

   **Named quests** (spine §5 kit):
   - **S2 "A Letter for Fenn"** — **[BUILT]** giver: the **house parent** (`tinderwick_house`;
     her shaken post-omen stage IS the hook — the F2 witness beat lands on a face) · steps:
     take Gran's letter (`script.gran_letter`, post-`dusk_begins`) → hand it to **Fenn** at
     his sky-watcher spot on the flats (`script.fenn_letter`; his crossroads placement hides
     and the flats placement appears on the same `flag:dusk_begins`) → return for her thanks
     (`script.gran_thanks`) · flags: `flag:q_south_letter` → `flag:q_south_letter_given`
     (→ `flag:q_south_letter_done` closes the giver swap) · reward: 2 Tallow + 1 Warm Balm +
     a warm line · maps: `tinderwick_house`, `dimglass_coast_ii` · `[MISSABLE]` — deliberately
     the game's first delivery quest, teaching the pattern the Waykeeper's Round scales up.
     *(Pre-omen, Gran also keeps the **warm keepsake beat** — `npc.house_parent_warm`, the
     grandfather's brass wick-trimmer — so `dusk_begins` threatens a kitchen, not a town name.)*

5. **Don't-miss callouts**
   - **Catch your first kin in the verge before Brisa will even talk quests** — the
     catch-first gate is the tutorial's natural "go make a friend first" beat.
   - **The Lantern-fair** — the warmest set-piece of the opening hour; it sets the whole game's
     "lanterns in the dark" tone.

6. **Validation hooks** (against built `tinderwick.json` + the beacon maps)
   - **Map id / kind:** `tinderwick` · town. Interiors: `tinderwick_house`,
     `tinderwick_lumenary` (the hall), `tinderwick_beacon_i/_ii/_top` (the tower).
   - **Entry/exit:** spawn `start_at {tx:6,ty:17}`; north edge-warps `to_coast`/`to_coast_e`
     → `dimglass_coast`, both **`requires_flag:flag:has_starter`**; east `to_crossroads
     {tx:27,ty:16}` → `vesper_crossroads` (ungated — the opening's road); beacon foot door
     `to_beacon` `interact {tx:24,ty:6}` **`requires_flag:flag:has_beacon_wick`**
     → `tinderwick_beacon_i`.
   - **The opening errand chain (all data):** north gate band `gate_warden` `cutscene`
     `step_on {tx:13,ty:1}` `hidden_when_flag:flag:has_starter` (warden body at `{14,1}`
     blocks the twin column) → crossroads: `fenn_wave` once-band, `script.fenn_crossroads`
     sets `flag:fenn_errand` → shop: item_cache `fenn_satchel` (`script.take_satchel` gives
     `fenn_satchel`, sets `flag:has_satchel`) → waystone ceremony `script.intro_mentor` sets
     `flag:has_vesperlamp` + `flag:has_starter`.
   - **Fenn's waystone stages (flag-disjoint placements on one tile):** `fenn_pre`
     (`script.fenn_crossroads`) → `fenn_waiting` (`npc.fenn_waiting`) → `fenn_ready`
     (`script.intro_mentor`) → `fenn_after` (`npc.fenn_waystone_after`, until
     `flag:dusk_begins` moves him to the coast for C2).
   - **The shop counter stages:** `shopkeeper_early` (points east) → `shopkeeper_errand`
     (the satchel) → `shopkeeper_kit` (`requires_flag:flag:has_starter` — the one-time kit)
     → `shopkeeper` (plain).
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
   - **NPCs / festival:** gate-warden pair `gatewarden_pre`/`gatewarden_post` (swap on
     `flag:has_starter`); **Wren** wanders near the garden until `flag:has_starter`
     (`npc.wren_intro`); Lantern-fair NPCs (`fair_piper`, `fair_kid`)
     `requires_flag:'gleam:ember'`. Fenn is at `vesper_crossroads`, not in town.

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
   - **The netmender's net-floats** — **[BUILT]** the cache at `{11,4}` on the flats
     (`script.pickup_net_floats` → `flag:picked_net_floats`; appears once
     `flag:q_south_bell` is set, band 8–10): the collinear errand leg of Pearlmoor's
     **Causeway Bell** loop (see Pearlmoor §1).
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

6. **Validation hooks** (against built `dimglass_coast_ii.json`)
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
   - **Quest hooks on this map (BUILT):** the **net-floats cache** `{11,4}`
     (`requires_flag:flag:q_south_bell`, `script.pickup_net_floats` → `flag:picked_net_floats`);
     **S1's three buoys** — interact `cutscene` triggers on the buoy line, lit **in order
     quay-outward** (a boolean chain with the netmender's rule as each `blocked_ref`):
     `buoy_first {14,9}` (`requires_flag:flag:q_south_buoys` → `flag:q_south_buoy_a`) →
     `buoy_second {16,12}` (→ `flag:q_south_buoy_b`) → `buoy_last {16,20}` (→
     `flag:q_south_buoys_lit`); **Fenn's flats stages** — `sky_watcher` (C2,
     `requires_flag:flag:dusk_begins`, hides on `flag:q_south_letter`) →
     `sky_watcher_letter` (`script.fenn_letter` → `flag:q_south_letter_given`) →
     `sky_watcher_after`.

---

### Pearlmoor Quay — *moonlit fishing port; the second Gleam and the first Gift*

**At a glance** — `pearlmoor_quay` (+ the breakwater `pearlmoor_breakwater` **[BUILT]**) ·
town · south · entry: south from `dimglass_coast_ii`, exit: onward to `saltreach_fen_i`
(via `to_fen`, East) + Lanternway `to_crossroads` · gate: **Tidecall** (its own islets &
sea-shrine — but the Lumenary itself is **not** gated, per spine §0 rule 1; the breakwater
is walked **on foot**) · **Gleam: Tide** (Reyl Wash, ace ~16, at his **sea-altar** — the
bond-test waits on the **Moor-bell**) + **Tidecall** · rec. level: 12, bond-test ~13–14.

**The earned loop — "The Causeway Bell" (spine §5, shape #2: breakwater walk) — [BUILT].**
The Tide-blessing cannot begin until the Moor-bell rings — and the bell-rope is in the
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
      blessing begins behind you: boats light, the quay sings, and Reyl steps to his
      **sea-altar** (the netmender's swap stage sends you to him).
   6. **Face Lampwarden Reyl Wash at the sea-altar (Tide, ace ~16).** His bond-test
      trigger answers only the rung bell (`blocked_ref` in his voice until then). Winning
      earns **Gleam: Tide** and the **Tidecall** Lantern Gift — and the walk back onto the
      quay lands the **Tide-blessing set-piece** (`script.tide_blessing`, its own cool
      moon-on-water cue `pearlmoor-blessing`, the bell as its signature note). Heal/restock
      first: **[BUILT]** the inn rest (`script.inn_rest`) + the chandlery's one-time
      crossing-kit.
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
   - **Lanternway → Vesper Crossroads** — already known: the hub is where the Wayfaring
     BEGAN (the satchel errand); from Pearlmoor it now reads as South's fast-travel anchor.
     Its inward Spire roads remain `[LATER]` (`flag:hub_unlocked`, West/endgame).

   **Named quests** (spine §5 kit; South's slate, with S2 over in Tinderwick):
   - **S1 "The Last Buoy Out"** — **[BUILT]** giver: the **netmender** (her post-Gleam
     swap stage, `script.netmender_buoys`) · steps: relight her three storm-dark buoys in
     the Dimglass II water **in order, quay-outward** (`buoy_first` → `buoy_second` →
     `buoy_last` — a boolean chain; out-of-order interacts answer with her rule as the
     `blocked_ref`) → return · flags: `flag:q_south_buoys` → `flag:q_south_buoy_a/_b` →
     `flag:q_south_buoys_lit` (→ `flag:q_south_buoys_done` closes the swap) · reward: the
     **Drift Charm** (the game's first **conditional charge**: catch ×3.0 on water-met kin,
     plain ×1.0 ashore — `04-capture.md`) · maps: `pearlmoor_quay`, `dimglass_coast_ii` ·
     `[LATER: Tidecall]` (a "now accessible" callout the moment the Gift lands).
   - **S3 "The Cavern Keeps a Light"** — **[BUILT: giver + reward]** giver: the **old
     fisher** (inn; his tale opens once the bell rings — `script.fisher_wrecklamp`) ·
     steps: relight his boat's wreck-lamp deep in **Tideglass Cavern** → tell him it still
     burns (`script.fisher_thanks`) · flags: `flag:q_south_wrecklamp` →
     `flag:q_south_wrecklamp_lit` (→ `flag:q_south_wrecklamp_done`) · reward: the
     **Wrecklight Charm** (the Tide Charm re-blessed, ×2.5) · maps: `pearlmoor_quay`,
     `tideglass_cavern` · `[LATER: Glimmerstep]` — **the wreck-lamp trigger itself ships
     with `tideglass_cavern`** (it must set `flag:q_south_wrecklamp_lit`); a deeper page
     beyond the lamp's reach `[LATER: Lamplight ≥ Starlight]`.
   - **S4 "The Booji-Wooji Man"** — **[BUILT]** giver: **Andy** at the **Lifting House**
     (`pearlmoor_lifting_house`, the quayside gym tucked behind the inn — door on the
     quay's NE bluff; Andy talks, Abdul and Sid bench) · steps: Andy's tale of the old
     strongman the quay calls the Booji-Wooji Man (`script.booji_andy`) → Abdul's clue
     (`script.booji_abdul`) → Sid's three words (`script.booji_sid`) → find **Paul** at
     the dark lamp past the moor-bell, take his question and his one-time route-class
     bout (`script.booji_paul`, `breakwater_paul`, 240w) → back to Andy
     (`script.booji_andy_done`) · flags: `flag:q_south_booji` → `_abdul` → `_sid` →
     `_met` (→ `flag:q_south_booji_done`) · reward: the **Booji Folio** (key item — the
     gift inside the gift) + 2 Tallow Balms · maps: `pearlmoor_lifting_house`,
     `pearlmoor_breakwater` · `[LATER-gated only by the moor-gate]` (Paul's stage waits
     on the bell loop's `flag:q_south_has_rope` path being open). Tone note: mystery and
     non-conformance, never the Hollowing — the Registry story is NEVER confirmed.
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

6. **Validation hooks** (against built `pearlmoor_quay.json` + `pearlmoor_breakwater.json`
   + `pearlmoor_lumenary.json`)
   - **Map id / kind:** `pearlmoor_quay` · town; **`pearlmoor_breakwater`** **[BUILT]** ·
     route/causeway, 12×28, walked on foot (no Tidecall anywhere on it — §0 rule 1: the
     causeway is carved SAND under the boards, never gated water; no encounters — its
     battles are the two posted net-hands).
   - **Entry/exit:** south land-in from `dimglass_coast_ii` (paired with its `to_quay`); onward
     **`to_fen`** → `saltreach_fen_i` (graph edge, ungated); **`to_crossroads`** → `vesper_crossroads`
     (Lanternway spoke, bidirectional); the breakwater root (cols 24–25, rows 18–23) ends in
     the moor-gate pair **`to_breakwater`/`to_breakwater_e`** `{24–25,23}`
     **`requires_flag:flag:q_south_has_rope`** with **`blocked_ref:npc.netmender_gate`**
     (Warp.blocked_ref is engine-supported, step_on included) → `pearlmoor_breakwater {5–6,0}`,
     landing ON its return pair.
   - **The bell quest chain (all data, BUILT):** `script.reyl_quest` (hall, Reyl's dais
     stage) sets `flag:q_south_bell` → net-floats cache on `dimglass_coast_ii` `{11,4}`
     (`flag:picked_net_floats`) → netmender swap `script.netmender_rope` gives the
     MOOR-BELL ROPE (`flag:q_south_has_rope`) → breakwater walk (net-hand SIGHT trainers
     **Maren** lv 12/12 + **Cob** lv 13/14 on one-tile boulder chokes, payouts 192/224 —
     route 16 × ace, mirrored in `progression.mjs BUILT_PAYOUTS`) → `script.ring_moorbell`
     at the shrine's bell (interact, both base tiles) sets `flag:q_south_bell_rung`.
   - **Lumenary (ungated) + Gift + flags:** the bond-test trigger `lumenary_battle` `{8,6}`,
     **`requires_flag:flag:q_south_bell_rung`** with **`blocked_ref:npc.reyl_blocked`**
     ("the moor-bell waits on you"), runs `script.lumenary_pearlmoor` — **earns `gleam:tide`**
     and **grants ability `tidecall`**; the engine sets **`flag:crown_south`** once
     `gleam:ember`+`gleam:tide` are both held. Lampwarden **Reyl Wash** (Tide, ace ~16);
     his dais runs four flag-disjoint stages (`reyl_quest` → `reyl_waiting` → `reyl` →
     `reyl_after`).
   - **The Tide-blessing set-piece (Arc E, BUILT):** `script.tide_blessing` banded across
     every walkable tile of quay row 10 (the one cut between the Lumenary forecourt and
     town), `requires_flag:'gleam:tide'`, self-hiding via `flag:tide_blessing_seen`; its
     cue is **`pearlmoor-blessing`** (SNES-register festival waltz — the anchor's lead/bass
     note-for-note, the moor-bell tolling through it; master
     `assets/audio/midi/pearlmoor-blessing.mid`) and its signature sfx **`world-moorbell`**.
   - **Quest-chain hooks (rule 3):** opened `flag:q_south_bell` / `q_south_has_rope` /
     `q_south_bell_rung` are consumed by the breakwater gate, the netmender stage chain and
     the bond-test trigger; S1/S3 flags as listed in their Named-quests entries (S3's
     `flag:q_south_wrecklamp_lit` is the one ref owed by a future map — the wreck-lamp
     trigger in `tideglass_cavern`); R1/R2 (the Waykeeper's Round legs) remain to wire at
     `vesper_crossroads`.
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
