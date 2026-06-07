# PixelKin — Walkthrough: Central & Endgame Region

> The centre of the crescent and the climb that ends the long night. The slow outer loop
> collapses into a fast four-way wheel, the Penumbra parts, and the ascent of the **Ninth
> Lantern** confronts the **Great Null** and relights the **Keystar**. Written to the spine in
> [`README.md`](./README.md) — read its §0 rules, §2 flags (esp. beats 9–11), §3 arcs (B5,
> A5→A6, C4, Arc D), §4 curve (Spire ~52→56), §5 cadence, §7 template, §10 voice before editing
> this file. Lore in [`story-bible.md`](../story-bible.md) (§3 climax/resolution, §5 the Spire /
> Keystar / Ninth Lantern, §7 Còr); maps in [`atlas.md`](../atlas.md) §1 (the 4-way hub) + §2
> cards 11–13 + the Starwell landmark; connectivity in
> [`graph.ts`](../../../src/game/data/world/graph.ts) (the `hub` block + the central nodes/edges).
> All content original per [`VISION.md`](../../../VISION.md); canon vocabulary throughout
> (**kin, Lumenary, Lampwarden, Gleam, Lantern Gift, vesperlamp, kindling, the Hollowing, the
> Great Null, the Keystar, Keylumen**) — never "monster/gym/badge/Professor".

---

## Region at a glance

| | |
|---|---|
| **Areas** | Vesper Crossroads (outer-ring hub) · Penumbra Ring (dark-fog barrier) · Umbral Spire (climax dungeon) · landmark **Starwell** |
| **Reading order** | West hands off → **Vesper Crossroads** (hub, now fully open) → **Penumbra Ring** (Starreach final crossings) → **Umbral Spire** (ascent → climax) → `dawnstead` (handed to post-game) |
| **Entry state** (from West) | **~lv52** · holds **ALL SIX Lantern Gifts** (Tidecall, Glimmerstep, Updraft Kite, Emberward, Sunsketch, **Starreach**) · all **eight Gleams** · **`flag:hub_unlocked`** · `flag:crown_west` · narrative ledger `flag:dusk_begins` + `flag:met_hollowing` + `flag:met_cor` + `flag:great_null_known` · **Wren returned** (A5) |
| **Exit state** (to post-game) | **~lv56+** · **`flag:keystar_relit`** · **`flag:dawn`** set → hands to [`06-postgame.md`](./06-postgame.md) at `umbral_spire → dawnstead` |
| **Gleams / Gifts earned** | **None** — every Gleam and Gift is already in hand. This region is where they all *converge and pay off*, not where new ones are taught. |
| **Arc beats landing here** | **B5** climax (confront the Great Null, relight the Keystar, resolve by *out-remembering*) · **A5→A6 transition** (Wren helps at the Spire, side-by-side — full A6 is post-game) · **C4** Fenn's counsel before the Spire |
| **Festivals (Arc E)** | None — all eight town festivals landed in their regions. The Crossroads is the cosy *between* place, the warmth you return to; the festival here is the whole region lit at once, paid off as dawn. |
| **Curve** | Crossroads/Penumbra are transit (no encounters); **Umbral Spire ~52 → 56**, Còr's ace ~56, Keylumen ~55. Continuous with West's exit (~52); the **one true difficulty ramp of the endgame** is the Spire's drained Hollowing kin. |

**Arc D — lighting.** This region is the **brightest yet, then the darkest, then the brightest of
all** — the deliberate paradox §3 Arc D asks for. The **Vesper Crossroads** is the warmest the
overworld has been: eight relit constellations overhead, the vesperlamp at its fullest tier, lamp
windows golden. The **Penumbra Ring** is a near-total black — your lamp-glow the *only* colour
within — but it *recedes visibly* as you cross, hopeful notes leaking into the drone. The **Umbral
Spire** is black basalt and Còr's anti-light null-lanterns: the single darkest place in the game —
**yet the Skyweave Crown completes overhead as you ascend**, so the darkest place sits under the
greatest light. At the Keystar relight the boss theme resolves minor→major. **The actual dawn is
the post-game** (`flag:dawn` is *set* here at the climax; Dawnstead blooms in
[`06-postgame.md`](./06-postgame.md)). Tie every lighting beat to the player's progression flags,
not to which tile they walked in from (spine §0 rule 2).

> **The §0 traps for this region, called out up front:**
> 1. **Nothing new is gated *by* a Gift earned here** — there are no Gifts earned here, so spine
>    §0 rule 1 can't be tripped. The risk is the *opposite*: every gate in this region requires a
>    flag/Gift the player **already holds on entry** (`flag:hub_unlocked`, `starreach`), so author
>    no edge that needs something not yet earned — that would soft-lock the endgame.
> 2. **The Crossroads has no encounters (safe hub) but Lampling IS catchable here** — a fixed/rare
>    Light kin found **only** at the Crossroads. It is *not* a wild-grass encounter (there is no
>    encounter terrain); represent it as a one-off static `EventTrigger` catch / very-low-weight
>    fixed spawn (see atlas card 11 + §6). Don't add tall-grass to a safe hub to host it.
> 3. **`flag:dawn` is set at the climax, but the dawn *town* is the post-game writer's.** Set the
>    flag here; do **not** author Dawnstead. Hand off cleanly at `umbral_spire → dawnstead`.

---

## Vesper Crossroads — *the cosy nexus, the loop become a wheel*

**At a glance** — `vesper_crossroads` · kind hub · region outer · **enter** via the **Lanternway
spokes** from Tinderwick / Pearlmoor / Lowleaf / Galehigh / Nightreach (all ungated) and the
late mine shortcut · **→ exit** inward to `penumbra_ring` (**`requires flag:hub_unlocked`** — now
held) · **gate ability:** none on the rim; the inward roads ride the crown/hub flags · **Gleam:**
none · **rec. level ~52** (transit; no battles in the hub itself).

### 1. Main path

1. **The loop has become a wheel.** You arrive at the lantern-lit inn at the many-way fork — a
   great signpost readable from spawn, warm windows, the "between" place travellers always return
   to. Overhead the **Skyweave Crown is complete** (all eight Gleams), and around the
   waystation **the Penumbra has fully parted**: the four cardinal roads inward stand open at once.
   The slow outer rim has collapsed into the fast four-way hub exactly as earned (atlas §1).
2. **The Lanternway spokes (fast-travel pays off).** Five ungated grass-lane spokes connect the
   Crossroads to the rim towns — **Tinderwick, Pearlmoor, Lowleaf, Galehigh, Nightreach** — so the
   hub is the late-game fast-travel anchor. *(If the player discovered the Crossroads in the
   south/mid-game via a spoke, this is the moment it earns its keep — they can now resupply, heal,
   and reach any quadrant in one hop before the climb.)* The **Cinderhead Deep shortcut**
   (`flag:shortcut_mine`, set in the East) re-links the eastern cave straight here too.
3. **The four crown approaches, recapped.** Each cardinal road inward burned back its wedge of the
   Penumbra as that quadrant's two Gleams relit: **`flag:crown_south`** (Ember+Tide),
   **`flag:crown_east`** (Verdant+Stone), **`flag:crown_north`** (Storm+Frost),
   **`flag:crown_west`** (Solar+Lunar). All four set **`flag:hub_unlocked`** — the engine's
   summary flag that parts the fog entirely and opens the Crossroads → Penumbra Ring roads. By
   the time you stand here, all four are lit. Place a **"now accessible"** callout: the inward
   road to the Penumbra Ring is open for the first time.
4. **C4 — Fenn's counsel before the Spire.** Star-tender **Fenn** waits at the inn (or sends you
   on from Nightreach — see §2/atlas; either placement is canon for C4). This is the last quiet
   beat before the dark. (Detail in §2.)
5. **A5 — Wren, returned and resolved, falls in beside you.** Wren — who walked off *unsure* at
   Pale Vault (A4) and has since reasoned it through (A5, late West) — is here, settled, and offers
   to climb with you. This sets up the **side-by-side** Spire beat; full A6 (Wren at peace in
   daylight) is the post-game. (Detail in §2.)
6. **Catch Lampling (the hub mascot).** Lampling — a sentient little vesperlamp kin (Light) — is
   found **only here**. A cosy, fixed/rare catch tucked into the safe hub (§4). **[MUST-DO]** for
   collectors: it exists nowhere else in Vesperholm.
7. **Rest, resupply, then take the inward road.** Heal, top up Lamps and items at the inn, then
   step onto the road to `penumbra_ring` (`requires flag:hub_unlocked` — held).

### 2. Story beats

- **C4 — Fenn's counsel.** Drawing on the **shared past with Còr** revealed in the North (C3),
  Fenn gives the player the climax's frame: *you cannot out-fight Còr — he is not your enemy, and
  beating him proves nothing. You can only out-remember him.* Fenn names the stakes one last time
  (the Great Null aimed at the Keystar; if the Keystar is snuffed, no constellation can ever
  rekindle) and hands over a final key item / the best Lamp for the Keylumen set-piece. Warm,
  steady, a little afraid — Fenn has lost to this grief once already.
- **A5 — Wren returns.** Not the doubting Wren of Pale Vault. Wren has walked the argument all the
  way round and come back: *the Hollowing aren't wrong that the cycle hurts — they're wrong that
  the answer is to stop it.* Wren chooses to climb with you. This is the **A5→A6 transition** — a
  *side-by-side* beat, not a rival battle; the full A6 resolution (Wren at peace, optional rematch)
  belongs to the post-game writer.
- **The Crossroads as thesis.** The hub is the warmest place in the game right now — eight stars
  overhead, every lamp lit — set directly against the dark you're about to enter. It is the thing
  Còr would extinguish, shown plainly so the climb has something concrete to be *for*.

> *Signature lines (flavour, not script):*
> - Fenn, at the signpost: *"You can't win this with a stronger kin, apprentice. Còr has heard
>   every argument; he made most of them himself. Don't go up there to beat him. Go up there to
>   *remember louder than he can grieve.*"*
> - Wren, falling in beside you: *"I went all the way round it. They're right that it hurts. ...I
>   just don't think 'never again' is worth 'never at all.' Come on — I'm not letting you climb
>   that thing alone."*
> - An innkeeper, nodding at the open roads: *"Years the fog sealed the centre. Now look — every
>   way home lit at once. Whatever you do up the mountain, traveller, the lamp's on down here."*

### 3. Mechanic introductions

- **No new Gift or mechanic taught** — this region is *convergence*: every Gift and Gleam already
  earned now pays off. The hub itself teaches the **fast-travel wheel** (spokes) and is the
  staging ground (heal/resupply) before the climax.
- **"Now accessible" callouts:** the inward **Crossroads → Penumbra Ring** road (just opened on
  `flag:hub_unlocked`); the **Cinderhead Deep → Crossroads** shortcut (`flag:shortcut_mine`, set
  in East, re-links here); and — held since Nightreach — **Starreach** content now reachable
  (Starwell off the Penumbra Ring, and the **Crystoll Vault** backtrack in the East — see §4).
- **The Lampling catch** teaches nothing new mechanically; it's the cosy collectible reward for
  reaching the hub fully open.

### 4. Optional content

- **Lampling (hub mascot kin, Light)** — found **only** at the Crossroads; a fixed/rare static
  catch in the safe hub. **[MUST-DO]** — it's nowhere else in the game; a first-timer should not
  leave the Crossroads without it.
- **Starwell** — landmark off the **Penumbra Ring**, `requires_ability: starreach`; reward: a
  **near-legendary kin** (post-Crown). Covered in full under the Penumbra Ring section below;
  flagged here only as a **[MUST-DO]** Starreach payoff now reachable. *(Held since Nightreach.)*
- **Crystoll Vault** — spur off `cinderhead_deep` (East), `requires_ability: starreach`; reward:
  rare Stone/Light kin. **This is the EAST writer's map — do NOT cover it here.** Listed only so
  the cross-reference closes: it's the *other* Starreach reopening the West writer handed you,
  reachable now from the hub via the mine shortcut. **[LATER]** (different region) → effectively
  **[MISSABLE]** at this point (you hold Starreach; go back for it before or after the Spire).

### 5. Don't-miss callouts

- **Catch Lampling** before leaving the hub — the cosy mascot exists only here. **[MUST-DO]**
- **Hear Fenn (C4) and let Wren join (A5)** before taking the inward road — the climb means more
  with both beats landed.
- **Use the wheel:** heal, resupply, and consider the two **Starreach** payoffs (Starwell here,
  Crystoll Vault back east) *before* committing to the Spire — there's no shop on the mountain.

### 6. Validation hooks

- **Map id / kind:** `vesper_crossroads`, kind `hub`, region `outer`. **No encounter terrain**
  (safe hub) — central signpost readable from spawn (level-design §2 hub pattern).
- **Lanternway spoke warps (graph.ts, all ungated, bidir):** `tinderwick`, `pearlmoor_quay`,
  `lowleaf_hollow`, `galehigh_terraces`, `nightreach_observatory` ↔ `vesper_crossroads` via
  `to_crossroads`; plus `vesper_crossroads → coldfog_marches_i` via `to_marsh` (bidir).
- **Late shortcut in:** `cinderhead_deep → vesper_crossroads` via `shortcut_crossroads`,
  **`requires_flag: flag:shortcut_mine`**, bidir (set in East; re-links the mine to the hub).
- **Inward warp:** `vesper_crossroads → penumbra_ring` via `to_penumbra`, **`requires_flag:
  flag:hub_unlocked`** (held on entry), bidir. *(The four `crown_*` flags are engine-set when each
  quadrant's two Gleams are held and together set `hub_unlocked` — do not hand-set any of them
  here; this region only depends on `hub_unlocked` already being true.)*
- **Lampling catch:** one-off static `EventTrigger` (`kind: 'script'`) or a very-low-weight fixed
  spawn for **Lampling (Light)** at the Crossroads — represented per atlas card 11 + the data note
  in atlas §3 (rare-kin reward = low-weight zone or one-off static catch). **No `tall_grass`/`water`
  encounter zone** in this map.
- **NPC / cutscene:** Star-tender **Fenn** (C4 counsel) at the inn/signpost; **Wren** (A5 — joins,
  no battle); innkeeper(s); dialogue/script refs `npc.fenn_crossroads`, `cutscene.fenn_counsel`,
  `cutscene.wren_returns`, `npc.crossroads_inn`.
- **Flags:** depends on `flag:hub_unlocked` (and the four `crown_*`) being set; sets **no new
  progression flag** here (C4/A5 are narrative cutscenes; `reward_flags` only for Wren-arc
  bookkeeping if used).

---

## Penumbra Ring — *the last dark, crossed on starlight*

**At a glance** — `penumbra_ring` · kind route (barrier) · region central · **enter** from
`vesper_crossroads` (**`requires flag:hub_unlocked`**) **→ exit** to `umbral_spire`
(**`requires_ability: starreach`**) · **gate:** recedes wedge-by-wedge with the `crown_*` flags
(all held), final crossings need **Starreach** (held) · **Gleam:** none · **rec. level ~52**
(traversal; **no kin reside here**).

### 1. Main path

1. **Into the last dark.** The inward road from the Crossroads runs into a literal wall of swirling
   `ink`-and-shadow — the Penumbra, the unnatural fog that sealed the centre all game. **Most of it
   has already receded**: each relit constellation burned back a wedge as its `crown_*` flag set,
   so by now only the innermost band remains. Your **lamp-glow is the only colour within** — the
   single most "lanterns in the dark" screen in the game.
2. **Pure traversal.** No encounters, no kin (kin refuse the dark — atlas card 12). The Ring is
   gating space: read it as short, tense crossings rather than a dungeon. The drone gains hopeful
   notes as you push through the receding fog (Arc D).
3. **The final voids — Starreach pays off.** The last crossings are **voids of pure dark** with no
   floor; **Starreach** draws down faint starlight from the near-complete Skyweave to *step across
   nothing* (story-bible §6). This is the endgame traversal Gift's true purpose, and the
   `penumbra_ring → umbral_spire` edge requires it. Place a **"now accessible"** callout where the
   Spire's ascending road first becomes steppable.
4. **Starwell (optional, off the Ring).** A Starreach-gated landmark holding a near-legendary kin
   (§4). **[MUST-DO]** for collectors — it's a post-Crown payoff reachable only now.
5. **Exit inward** to `umbral_spire` across the final void (`requires_ability: starreach`, held).

### 2. Story beats

- **A held breath, not a plot beat.** The named climax beats (B5) land *inside* the Spire; the Ring
  is the threshold — the dark you've spent the whole game pushing back, crossed one last time on
  the light you gathered. Let the silence and the receding fog do the work (Arc D). A single line
  of Wren-at-your-shoulder (if Wren joined at the Crossroads) keeps the side-by-side beat warm.
- **The Ring as proof.** That the fog *recedes* — that you can cross at all — is the visible
  receipt of eight Gleams. It's the world conceding the night is ending, just before the place that
  doesn't want it to.

> *Signature line (flavour, not script):*
> - Wren, low, crossing a void on starlight: *"We're walking on *stars*, you realise that? A year
>   ago this was a wall nobody could pass. ...Keep your lamp up. Almost there."*

### 3. Mechanic introductions

- **No new mechanic** — but this is **Starreach's defining use**: stepping across voids of pure
  dark. Everything earlier was teaser; here the Gift is *required* to reach the climax.
- **"Now accessible" callouts (Starreach, all held):** the **Spire ascent** itself (the
  `penumbra_ring → umbral_spire` void crossing) and **Starwell** (this Ring's landmark). The
  cross-region partner payoff, **Crystoll Vault**, is the East writer's (named under the Crossroads
  §4).

### 4. Optional content

- **Starwell** — landmark off the Penumbra Ring, `requires_ability: starreach`; reward: a
  **near-legendary kin** (post-Crown). **[MUST-DO]** — one of the game's standout optional catches
  and reachable only after the Crown completes and Starreach is held; do not pass it. *(Map node
  `starwell`, `optional: true`, region central — author as a small Starreach-gated micro-dungeon
  with a single high-value fixed/low-weight catch.)*
- **No other content resides on the Ring** — no kin, no items beyond Starwell's reward (it's a
  barrier, not an explorable zone). Keep the backtrack web honest: the only optional node here is
  Starwell.

### 5. Don't-miss callouts

- **Starwell is a [MUST-DO] near-legendary catch** — the post-Crown payoff the West writer flagged;
  it's reachable only now, only with Starreach. Detour for it before the Spire (or remember it
  after).
- **Save / heal first** — there's no rest stop past the Crossroads; the Ring leads straight to the
  climax. Top up at the hub before crossing.

### 6. Validation hooks

- **Map id / kind:** `penumbra_ring`, kind `route` (barrier), region `central`. **No encounter
  zones** (kin refuse the dark — atlas card 12); no `tall_grass`/`water`/`cave` terrain.
- **Entry warp (graph.ts):** `vesper_crossroads → penumbra_ring` via `to_penumbra`,
  **`requires_flag: flag:hub_unlocked`** (held), bidir.
- **Exit warp:** `penumbra_ring → umbral_spire` via `to_spire`, **`requires_ability: starreach`**
  (held), bidir. *(Note: `umbral_spire` node also carries `unlocked_by_flag: flag:hub_unlocked` —
  the node shows once the hub is unlocked; the void crossing into it needs Starreach.)*
- **Optional landmark warp:** `penumbra_ring → starwell` via `to_starwell`, **`requires_ability:
  starreach`**, bidir. `starwell` node is `optional: true`, region `central`, reward "post-Crown
  landmark (Starreach): a near-legendary kin".
- **Lighting / Arc D:** fog recession is keyed to the `crown_*` flags (all set on entry); represent
  any visual swap via flag-gated `deco`/tint, not by which edge the player entered from
  (spine §0 rule 2).
- **No NPCs / no festival / no flags set** — pure traversal + the one Starwell catch. (Starwell's
  catch is a fixed/low-weight `EncounterZone` or one-off `EventTrigger` per atlas §3.)

---

## Umbral Spire — *the darkest place at the moment of the greatest light*

**At a glance** — `umbral_spire` · kind cave/hub · region central · node
**`unlocked_by_flag: flag:hub_unlocked`** · **enter** from `penumbra_ring`
(**`requires_ability: starreach`**) **→ exit** to `dawnstead` (**`requires_flag: flag:dawn`** —
set at the climax) · **gate:** Starreach + `flag:hub_unlocked` (both held) · **Gleam:** none ·
**boss:** **Warden Còr** (ace ~56); **Keylumen** (the Keystar-kin, Light, signature/legendary,
~lv55) · **rec. level ~52 → 56.**

### 1. Main path

1. **The ascent of the Ninth Lantern.** You step off the final void onto black basalt — the dead
   Lumenary at the heart of Vesperholm, the long-dead **Ninth Lantern** (story-bible §5). Còr's
   **null-lanterns leak anti-light**, snuffing colour in pools; the climb is a branchy cave/tower
   ascent (level-design cave pattern: rooms joined by chokes). **But look up** — through the
   basalt's open shafts the **Skyweave Crown completes overhead** as you climb (Arc D): the darkest
   place in the game, under the greatest light yet gathered.
2. **The Hollowing's drained kin (the dungeon trainers).** The Spire's encounters are scripted
   battles against Còr's **drained Hollowing kin (Dark)** and the acolytes tending the null-works —
   the genre's "team grunts," but sad and gentle, not cruel (they *believe they help*). This is the
   **endgame difficulty ramp**: Dark-typed, ~lv52→55, the hardest sustained run in the game. Keep
   them on the upper band so a prepared ~lv52 party is tested but not walled.
3. **A5→A6 — Wren at your side.** If Wren joined at the Crossroads, the ascent is **side-by-side**:
   Wren takes some of the drained-kin fights, trades a line each room, carries the warmth up into
   the dark. (This is the *transition* beat — full A6 is the post-game.)
4. **The summit — the Great Null aimed at the Keystar (B5).** At the peak: the **Great Null**, Còr's
   device, trained on the **Keystar** — the last anchoring star, the one whose light lets any other
   constellation rekindle at all (story-bible §3/§5). Còr stands between you and it, courteous and
   sad. (Climax beats in the **Climax & Resolution** subsection below.)
5. **Relight the Keystar — the Keylumen set-piece.** With Còr answered, the climax resolves into a
   **catch/relight set-piece**: the radiant **Keylumen** (Light, signature/legendary, ~lv55) is the
   Keystar's living heart — relight/befriend it to fire the Keystar back to life. Sets
   **`flag:keystar_relit`**. The boss theme resolves **minor→major** at the relight (Arc D / atlas
   card 13 music).
6. **Dawn breaks — `flag:dawn`.** The relit Keystar cascades light back into the whole Skyweave; the
   **long night breaks**. Sets **`flag:dawn`**. *(The dawn **town**, Dawnstead, blooms in the
   post-game — see hand-off.)* Place a **"now accessible"** callout at the
   `umbral_spire → dawnstead` road, which opens on `flag:dawn`.
7. **Exit** to `dawnstead` (`requires_flag: flag:dawn`) — hand off to
   [`06-postgame.md`](./06-postgame.md).

### 2. Story beats

*(The headline beats — B5 and the resolution — are written out in the **Climax & Resolution**
subsection below so they read as one piece. This section covers the ascent's supporting beats.)*

- **B4 paid off (named in West).** The **Great Null aimed at the Keystar** was *named* in the West
  (`flag:great_null_known`); the Spire is where the player finally *sees* it. No re-explaining —
  the player arrives knowing the stakes; the Spire makes them physical.
- **The drained kin as quiet tragedy.** Each Hollowing battle is a small grief — kin "put to sleep,"
  never harmed (story-bible §7); acolytes who think they're sparing the world pain. Never
  cartoonish. The dungeon's emotional texture is *sad people doing a careful, terrible kindness.*
- **A5→A6 transition.** Wren's presence is the counterweight — the friend who walked all the way
  round the Hollowing's argument and chose the dawn anyway, climbing the dark beside you.

> *Signature lines (flavour, not script):*
> - A Hollowing acolyte, gently, before a battle: *"You shouldn't be up here, apprentice. We're not
>   cruel — your kin will only *sleep*. No more guttering, no more loss. ...Won't you let us be kind
>   to it?"*
> - Wren, on a dark landing, lamp up: *"Sad, isn't it. They're not wrong that it hurts. ...Doesn't
>   make them right. Keep climbing."*

### 3. Mechanic introductions

- **No new Gift** — the Spire is where **all six** converge: Starreach got you here, and the whole
  party/Gleam toolkit is tested against the difficulty ramp. The new *set-piece* mechanic is the
  **Keylumen catch/relight** (a one-off legendary catch that doubles as the story climax — atlas
  card 13).
- **Endgame difficulty.** Drained Hollowing kin (Dark) ~lv52→55, Còr's ace ~56, Keylumen ~55. This
  is the curve's top (spine §4). Status conditions assumed live (spine §5); write Còr's team around
  Dark/Lunar pressure and a signature `doze`/`blight` threat to reward a prepared party.

### 4. Optional content

- **No spurs/landmarks inside the Spire** — it's a linear-with-chokes climax dungeon; the optional
  Starreach payoffs (**Starwell**, **Crystoll Vault**) live *outside* it and are flagged under the
  Penumbra Ring / Crossroads sections. Anything optional here is small flavour (a hidden item on a
  side landing — **[MISSABLE]** — reachable with the Gifts already held).
- **Keylumen** is **not** optional — it is the climax catch/relight (sets `flag:keystar_relit`),
  so it's main-path, not a tagged optional.

### 5. Don't-miss callouts

- **Arrive prepared** — there's no shop or rest past the Crossroads, and the Spire is the hardest
  sustained run in the game. Heal, resupply, and bring your best Lamp for Keylumen before crossing
  the Penumbra Ring.
- **Let the ascent breathe** — the completing Crown overhead is the visual thesis of the whole game
  (the greatest light over the darkest place). Don't rush past it to the boss.

### 6. Validation hooks

- **Map id / kind:** `umbral_spire`, kind `cave`/`hub`, region `central`,
  **`unlocked_by_flag: flag:hub_unlocked`** (node shown once the hub is unlocked).
- **Entry warp (graph.ts):** `penumbra_ring → umbral_spire` via `to_spire`,
  **`requires_ability: starreach`** (held), bidir.
- **Exit warp:** `umbral_spire → dawnstead` via `to_dawn`, **`requires_flag: flag:dawn`** (set at
  the climax), bidir. *(Author the warp; do **not** author the `dawnstead` map — post-game writer's;
  the `dawnstead` node itself carries `unlocked_by_flag: flag:dawn`.)*
- **Climax triggers `sets_flags`:** Keystar relight / Keylumen set-piece → **`flag:keystar_relit`**
  (`EventTrigger` kind `script`, `once: true`); dawn-break cutscene → **`flag:dawn`** (`script`,
  `once: true`). Order: Keystar relit → dawn. Use these exact spine §2 strings.
- **Boss trigger:** Warden Còr final battle (ace ~56) as a scripted trainer/cutscene battle;
  resolution is *narrative* (out-remembering), not a destroy-on-defeat — see Climax & Resolution.
  `reward_flags` only for bookkeeping; the progression flags are `keystar_relit` then `dawn`.
- **Keylumen set-piece:** one-off static catch/relight of **Keylumen (Light, signature/legendary,
  ~lv55)** — a fixed `EventTrigger` catch (atlas §3 data note), not a wild-grass roll. Drained
  **Hollowing kin (Dark)** are scripted dungeon battles, not a wild `EncounterZone` ecosystem
  (atlas card 13: "scripted encounters only").
- **No wild encounter terrain / no festival** — scripted encounters only (atlas card 13).
- **NPC / cutscene refs:** `trainer.warden_cor_final`, `cutscene.great_null`,
  `cutscene.keystar_relight`, `cutscene.dawn_breaks`, `trainer.hollowing_acolytes_spire`,
  `npc.wren_spire` (A5→A6 side-by-side). Music key = the Spire's structured boss track
  (intro → loop → minor→major resolve at the relight).

---

## Climax & Resolution — *out-remembering Warden Còr*

> The game's emotional summit, written as one piece. Follows story-bible §3 (Climax & Resolution)
> and spine §3 arc **B5**. **Beats**, not a full script — a few signature lines set the tone.

### The confrontation (B5)

1. **At the summit, the Great Null.** Còr stands before his device, the **Great Null**, trained on
   the **Keystar**. He is exactly as promised — **courteous, sad, persuasive**, never a cackling
   villain (story-bible §7). He does not gloat; he *explains*, one last time, gently. The tragedy is
   that he is partly right: the cycle of light and loss *does* hurt.
2. **He makes the case, not war.** Còr's offer is mercy: let the Keystar go out, let the long night
   settle soft and permanent — no more guttering lamps, no more goodbyes, the world held painless in
   the dark. He invites the player to simply *stop*, to agree the dawn isn't worth the dusk.
3. **The final battle — but it doesn't *win* anything.** You face Còr (ace ~56). Beating his kin is
   the *form* the confrontation takes, but the spine and story-bible are emphatic: **you do not
   defeat Còr by force.** Winning the battle only earns you the right to answer him.

### The resolution — you out-remember him

4. **Out-remembering, not out-fighting.** Through the kin you've befriended and the eight lights you
   carried up the dark, you *prove the cycle of loss is worth more than a flat, painless
   forever-dark* — that the dawn is worth the dusk **because** it can be lost. You don't argue Còr
   down; you **out-remember** him: every relit constellation, every town's festival, every kin that
   chose to walk beside you is a memory weighing against his grief. (Fenn's C4 framing — *remember
   louder than he can grieve* — pays off here.)
5. **Relight the Keystar (Keylumen).** Còr's certainty breaks — not into defeat, into *remembering*.
   The radiant **Keylumen** wakes; you relight/befriend the Keystar's living heart and fire the last
   anchoring star back to life. Sets **`flag:keystar_relit`**. The boss theme resolves
   **minor→major** (Arc D).
6. **The long night breaks (`flag:dawn`).** The relit Keystar cascades light through the whole
   Skyweave; the dusk that won't lift finally turns. Sets **`flag:dawn`**. The ending is
   deliberately **bittersweet and warm** (story-bible §3): the cycle *resumes* — which means dusk
   will come again — **and that is exactly the point.**
7. **Còr is not destroyed.** Undone but not broken, Còr is **quietly offered a place among the
   star-tenders again** — Fenn's old fellow, come back from grief. No punishment, no cage; mercy
   answered with mercy. (The post-game writer carries Còr's settled resolution further in
   [`06-postgame.md`](./06-postgame.md).)

> *Signature lines (flavour, not script):*
> - Còr, before the battle, gently: *"I had hoped you'd be tired enough to agree with me. You've
>   seen the quieted towns — you've seen how *peaceful* it is. I am not cruel, apprentice. I only
>   want the grieving to stop."*
> - Còr, as the Keystar wakes: *"...You're not arguing with me. You're *remembering* at me. All of
>   it — every lamp, every name, every small goodbye you'd have me erase. ...I had forgotten it was
>   worth the ache."*
> - The resolution beat: *"The night breaks. Not into a victory — into a morning. Dusk will come
>   again, and that is the whole of it: the dawn is worth the dark precisely because we can lose
>   it."*
> - Fenn, offering Còr a place again: *"You read the same sky I did, old friend. There's still a
>   lamp lit for you. ...Come down and tend it with me."*

### Validation hooks (climax)

- **Flag order (spine §2 beats 10→11):** `flag:keystar_relit` **then** `flag:dawn`, both via
  `once:true` `script` triggers in `umbral_spire`. No other map sets these.
- **Resolution is narrative, not mechanical** — winning Còr's battle gates the *cutscene*, but the
  win does not "destroy" Còr; the script offers him a place back (story-bible §3). No "defeat team"
  flag, no lethal/cruel framing (spine §10, story-bible §7).
- **Tone & originality:** canon vocabulary only (the Hollowing, the Great Null, the Keystar,
  Keylumen, Warden Còr, Star-tender Fenn); Còr courteous-sad throughout; cosy-melancholy, never
  grim (spine §10 / VISION). Run `copy-editing` on the final dialogue.

---

## Hand-off to post-game

The post-game writer ([`06-postgame.md`](./06-postgame.md)) picks up at
**`umbral_spire → dawnstead`** (`requires_flag: flag:dawn`) with the player at **~lv56+**, holding
**all six Lantern Gifts**, all eight Gleams, **`flag:keystar_relit`** and **`flag:dawn`** set. Owed
downstream: **A6** (Wren at peace in daylight, optional rematch — this region only ran the A5→A6
*transition*, the side-by-side Spire climb); **Còr's settled resolution** among the star-tenders;
**Dawnstead** itself blooming in full daylight; and the **celestial-calendar / day-form** swaps the
relit sky unlocks (atlas card 14, story-bible §8). The dawn flag is *set* here — the dawn *world* is
theirs to write.
