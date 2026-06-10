# PixelKin — Walkthrough: North Region

> Gleams **5–6** → **`flag:crown_north`**. The mountain quadrant: fire-sunset cliff-farms
> climbing into lonely aurora ice. Written to the spine in
> [`README.md`](./README.md) — read its §0 rules, §2 flags, §3 arcs, §4 curve, §5 cadence,
> §7 template, §10 voice before editing this file. Lore in
> [`story-bible.md`](../story-bible.md) (Còr §7, calendar §8); maps in
> [`atlas.md`](../atlas.md) §2 cards 6–7 + §3 Windward Stair; connectivity in
> [`graph.ts`](../../../src/game/data/world/graph.ts). All content original per
> [`VISION.md`](../../../VISION.md); canon vocabulary throughout
> (**kin, Lumenary, Lampwarden, Gleam, Lantern Gift, vesperlamp, kindling, the Hollowing**).

---

## Region at a glance

| | |
|---|---|
| **Areas** | Galehigh Terraces (cliff town, Lumenary 5) · Windward Stair I → II (mountain route) · Pale Vault Glacier (ice town, Lumenary 6) · spurs **Wind-Eye**, **Thunderroost** |
| **Reading order** | `cinderhead_deep` → **Galehigh Terraces** → **Windward Stair I → II** → **Pale Vault Glacier** → `hushfrost_pass_i` (handed to West) |
| **Entry state** (from East) | ~lv28 · holds **Tidecall + Glimmerstep** · `gleam:verdant` + `gleam:stone` · `flag:crown_east` · narrative ledger `flag:dusk_begins` + `flag:met_hollowing` |
| **Exit state** (to West) | ~lv40 · holds **Tidecall + Glimmerstep + Updraft Kite + Emberward** · `gleam:storm` + `gleam:frost` · `flag:crown_north` · `flag:shortcut_windward` · narrative ledger `flag:dusk_begins` + `flag:met_hollowing` + `flag:met_cor` (all persistent, carried forward) |
| **Gleams earned** | **Storm** (Mira Vael, Galehigh, ace ~34) · **Frost** (Ysolde Frost, Pale Vault, ace ~40) — both relit → `flag:crown_north` |
| **Lantern Gifts earned** | **Updraft Kite** (Galehigh) · **Emberward** (Pale Vault) |
| **Arc beats landing here** | **B3** Còr appears in person (`flag:met_cor`, near Pale Vault — no battle) · **A4** Wren's wobble (hard rival battle near Pale Vault) · **C3** Fenn reveals the shared past with Còr |
| **Festivals (Arc E)** | Galehigh **Kite-rising** · Pale Vault **Aurora-watch** |
| **Curve** | Galehigh ~28 → Windward 34→36 → Pale Vault ~36 → exit ~40. ~+6/Gleam, continuous with East's exit (~28) and West's entry (~40). |

**Cinematic staging (PLANNED — build from South per [`cinematics.md`](../cinematics.md) / §0.4).**
North is the **character-drama peak** of the midgame; lean hard on **portraits + `silence`**, not
spectacle. **B3 Còr in person** (no battle) is the inverse of a boss reveal: `letterbox`, fade the
aurora bed to near-`silence`, hold long on Còr's **portrait** (grave, sorrowful, *reasonable*) as
he states his case over a quieted valley — a `cameraFocus`/`tint`-cool on the peaceful drained
vista he gestures to. **C3 Fenn's revelation** lands immediately after on Fenn's `grave` portrait,
no music swell — just two faces and the quiet. **A4 Wren's wobble** is the hard rival battle: open
on Wren's `unsure` portrait, and afterward a `silence` beat before they walk off unresolved (this
is the one rival fight at *equal* level — let the staging feel heavier than A2). Festivals
(**Kite-rising**, **Aurora-watch**) use the Gleam swell, but **Aurora-watch is a silent vigil** —
stage it as `silence` + a slow `tint`/`flashColor` as each lamp lights, deliberately rhyming with
(and refuting) Còr's vision. Assets owed: Còr portrait (the marquee new face), Fenn `grave`
already exists, a quieted-valley/aurora backdrop.

**Arc D — lighting.** North is **visibly lighter than East**. You arrive out of Cinderhead's
ink-black deep into **Galehigh's last fire**: a long, warm `fire`-orange sunset bleeding into
`night`-blue, kite-silhouettes against banded cloud. As you climb the Windward Stair the
sunset thins to a cold high-altitude blue, and **Pale Vault** is a lonely **aurora-lit ice
field** — `diamond` and faint `grass`-green ribbons over `bone` snow. Colder than East, but
*brighter*: two more constellations relit overhead by the time you leave, the vesperlamp a
step brighter again. Tie all lighting/encounter shifts to the player's **Gleam count**, not to
the map walked in from (spine §0 rule 2).

> **The two §0 traps for this region, called out up front:**
> 1. **Pale Vault's Lumenary is reachable WITHOUT Emberward.** Emberward is *earned* from Ysolde
>    and gates only the **onward** `hushfrost_pass_i → hushfrost_pass_ii` segment (West) and
>    Pale Vault's deep-ice spurs — **never** the town or the Frost Lumenary. The
>    `windward_stair_ii → pale_vault_glacier` edge is **ungated**. Do **not** write a
>    coldfog/thin-ice gate between the glacier town entrance and Ysolde.
> 2. **Set `flag:shortcut_windward`** on reaching the Windward Stair II crags (the ledge-drop
>    back to Galehigh). This region opens that shortcut, so this region closes that flag.

---

## Galehigh Terraces — *the last fire before the climb*

**At a glance** — `galehigh_terraces` · kind route/town · region north · **enter** from
`cinderhead_deep` (ungated) **→ exit** to `windward_stair_i` (ungated) · **gate ability:**
Updraft Kite (its own high ledges + the Wind-Eye landmark only) · **Gleam:** Storm (Mira Vael,
ace ~34) · **rec. level ~28.**

### 1. Main path

1. **Out of the dark, into the wind.** You step from Cinderhead's pitch-black gallery onto a
   stepped cliff-farm catching the **last of the sunset** — the first colour in screens. One
   screen: a banner of climbing terraces, kites snapping overhead, `diamond` updraft motes
   rising off the ledges. The lit, paved switchback is the way up and in.
2. **The lower terraces (town proper).** Wind-break cottages, a kite-maker's stall, the
   relit-Stone Gleam (East) reading clearly in a slightly brighter sky than the mine. Tall-grass
   verges on the low terraces carry the common Storm kin (Kiteling, Thrumvane). A **clearly
   higher ledge** is framed and reachable-looking but a half-tile too high to step — the game's
   first **Updraft Kite tease** (signed: *"the high terraces only open to a kin that rides the
   thermals"*).
3. **The Kite-rising is in full swing.** The festival fills the central terrace (Arc E, below).
   **The earned loop — "The Kite-Rising Winch" (spine §5, shape #5: festival winch climb).**
   **The tease:** above the festival terrace, kite-strings run all the way up to the
   **launch ledge** — and the great timber **winch** that hauls riders up to it stands
   idle. *(Distinct from the Updraft-tease ledges of beat 2: those are Gift-gated and keep
   their sign; the launch ledge is festival-gated — the winch, not the wind, takes you up.)*
   Mira is up there, flying, and shouts the hook down: *"You want the Storm Gleam? Then
   fly! Nobody meets the wind from the ground — raise a kite with the town, and meet me at
   the launch ledge."* (`script.mira_quest` → `flag:q_north_kite`.)
4. **The kite-maker's errand (collinear).** The kite-maker's three best kites blew loose in
   last night's squall and snagged across the **lower terraces** (band 28–30, ground the
   player crosses anyway): three **chained caches** — finding the spar reveals the sail's
   giver, the sail the tail's (`flag:picked_kite_a` → `picked_kite_b` → `picked_kite_c`;
   a boolean chain, no counters) → `script.kite_built` → `flag:q_north_kite_ready`.
5. **Fly at the Kite-rising** — the festival cutscene takes your kite up with the town's
   (`flag:q_north_kite_blessed`); the winch-keeper starts the drum, and the winch warp
   opens to **`galehigh_skyloft`** **[NEW MAP]**: a wind-raked top terrace held by **two
   wind-ward sight trainers** (lv 29–31), the launch ledge at its head.
6. **Lumenary 5 — Mira Vael (Storm), at the launch ledge** (the skyloft is winch-gated by
   the festival flag, never by Updraft — spine §0 rule 1; Updraft is the *reward*, not the
   gate). A fast, adrenaline-keyed Storm fight; ace ~34 met at ~30–31. Win → **Storm
   Gleam** + **Updraft Kite** + `gleam:storm`, ability `updraft_kite` — and the **glide
   down** from the ledge is the Gift's first taste.
7. **The map reopens.** With Updraft Kite in hand, the teased high ledges click open: the
   **Wind-Eye** landmark warp, the Galehigh→Windward high route, and (later) the
   Windward→Galehigh drop shortcut. Place a **"now accessible"** callout at the first
   high-ledge you couldn't reach in step 2.
8. **Exit north** to `windward_stair_i` (ungated — the lower switchbacks need no Gift; the
   *boundary* I→II is what Updraft gates).

### 2. Story beats

- **Arc E — the Kite-rising.** Galehigh's festival: on the windiest dusk of the year the whole
  town flies lit kites so the relit constellations have "something to answer." Warm, communal,
  a little daft; Mira is its ringleader. *Belonging, not conquest* — you fly a kite before you
  earn the Gleam.
- **Arc A foreshadow (light touch — A4 lands at Pale Vault, do not resolve it here).** Wren is
  here, buzzing off the festival but quieter underneath; a single line that the towns the
  Hollowing have "quieted" sounded *peaceful*. Plant the doubt; don't pay it off yet.
- **Mira Vael — voice.** Brave, breathless, generous; treats the storm as a friend, not a foe.

> *Signature lines (flavour, not script):*
> - Mira, mid-flight: *"You don't fight the wind, apprentice. You ask it to lift you — and you
>   thank it when it does."*
> - A festival-goer: *"We fly the kites so the stars have something to climb back up. Daft,
>   maybe. But the night's a little less long when the whole hill's lit."*
> - Wren, too lightly: *"Quiet towns. No more lamps guttering, no more goodbyes. ...Doesn't
>   sound like the worst thing, does it?"*

### 3. Mechanic introductions

- **Updraft Kite earned** — a storm-kin lifts you on warm thermals to **scale terraces and
  glide short gaps**. Taught locally (it opens Galehigh's own high ledges), then retroactively
  reopens content mapwide (spine §5).
- **"Now accessible" callouts (this Gift):** Wind-Eye (here), Thunderroost (Windward II), and
  the Windward→Galehigh drop shortcut.
- **Type pressure shift.** From here the world is **Storm-saturated** then **Frost-saturated** —
  the start of the North/cold band. Flag the assumed status conditions (`numb` from Storm,
  `chill` from Frost) per spine §5; write Mira around `numb`.

### 4. Optional content

- **Wind-Eye** — landmark sky-grotto micro-dungeon off Galehigh, `requires_ability: updraft_kite`;
  reward: a **unique Storm kin**. **[MISSABLE]** — once Updraft is earned it is open and easy to
  fly past on the way to Windward; flag it hard so a first-timer detours. (Earlier than Updraft
  it is a **[LATER]** tease — visible updraft column you can't yet ride.)
- **High-terrace hidden item** reachable only with Updraft — **[MISSABLE]**.
- The Windward→Galehigh drop **shortcut** appears later (set at Windward II) — **[LATER]** here.

**Named quests** (spine §5 kit; North's slate, N2 over at Pale Vault, N3 given by Mira):
- **N1 "The Crag-tender's Kettle"** — giver: the **crag-tender** on the upper switchbacks
  (Windward Stair I) · steps: pick the wind-burnt **ledge-herb** (cache on a Galehigh high
  terrace, post-Updraft) → carry it up to her kettle · flags: `flag:q_north_kettle` →
  `flag:q_north_kettle_done` · reward: the **Warm Flask** (a `chill`-flavoured comfort
  item) · maps: `galehigh_terraces`, `windward_stair_i` · `[LATER: Updraft Kite]`.
- **N3 "Wren's Ribbon"** — giver: **Mira**, after the A4 beat at Pale Vault · steps: Mira
  found Wren's dropped kite-ribbon from the Kite-rising; carry it to the quiet Windward II
  ledge where Wren sat · place it (a wordless interact — no dialogue by design) · flags:
  `flag:q_north_ribbon` → `flag:q_north_ribbon_placed` · reward: none here — paid off by
  one extra Wren line at Nightreach's lamp 6 (see 04-west) · maps: `galehigh_terraces`,
  `windward_stair_ii` · `[MISSABLE]` — the A4→A5 connective tissue.
- **R4 "A Kite for the Waystone Kid"** — the Waykeeper's Round, leg 4: the **kite-maker**
  hands the Waykeeper's commissioned kite → deliver to the **Waystone kid**
  (`vesper_crossroads`) · flags: `flag:q_round_kite` · reward: balm kit + the kid flies it
  on the plaza thereafter (NPC swap) · `[wakes with spoke]` (the Galehigh spoke wakes with
  `gleam:storm`).

### 5. Don't-miss callouts

- **Wind-Eye is the region's signature optional reward** — do not leave Galehigh's airspace
  without it once Updraft is earned. **[MISSABLE]**
- **Fly a kite at the Kite-rising** before facing Mira — the festival beat is the warmth the
  Gleam is wrapped in.

### 6. Validation hooks

- **Map id / kind:** `galehigh_terraces`, kind `route`/`town`, region `north`.
- **Entry/exit warps (graph.ts):** in from `cinderhead_deep` via `to_terraces` (ungated, bidir);
  out to `windward_stair_i` via `to_stair` (ungated, bidir); Lanternway spoke
  `galehigh_terraces ↔ vesper_crossroads` via `to_crossroads` (bidir).
- **Gated warp:** `to_windeye` → `wind_eye`, `requires_ability: updraft_kite`, bidir.
  Late shortcut **back** lives on Windward II: `windward_stair_ii → galehigh_terraces` via
  `shortcut_galehigh`, `requires_flag: flag:shortcut_windward`.
- **Lumenary trigger `sets_flags`:** Mira Vael victory → `gleam:storm` + grants ability
  `updraft_kite` (engine sets `flag:crown_north` only once **both** `gleam:storm` and
  `gleam:frost` are held — do not set it here).
- **Lumenary entry is NOT ability-gated** (spine §0 rule 1) — the winch warp keys on the
  festival flag, never `updraft_kite`.
- **The Kite-Rising Winch chain (rule 3):** `script.mira_quest` sets `flag:q_north_kite`;
  the three chained kite caches (`flag:picked_kite_a/b/c` — each reveals the next giver);
  `script.kite_built` sets `flag:q_north_kite_ready`; the festival fly cutscene sets
  `flag:q_north_kite_blessed`; consumed by the winch warp to **`galehigh_skyloft`**
  **[NEW MAP]** (landmark, ~18×12; 2 wind-ward SIGHT trainers lv 29–31; the launch ledge +
  Mira's bond-test at its head, `blocked_ref:npc.mira_not_ready` until blessed).
- **Encounter zones:** `tall_grass` (terraces) — Kiteling (Storm), Thrumvane (Storm), Cirruff
  (Storm/Light); level band ~28–30 (continuous with Cinderhead Deep's 24–27 and Windward's 34+).
- **NPC / Lumenary / festival:** Mira Vael (Storm Lampwarden) on a high reachable terrace;
  Kite-rising festival cutscene + flag-gated festival NPCs; Wren NPC (A4 foreshadow line);
  dialogue refs `npc.mira_vael`, `cutscene.galehigh_kite_rising`.

---

## Windward Stair I → II — *climbing out of the warm into the high blue*

**At a glance** — `windward_stair_i` (lower switchbacks) → `windward_stair_ii` (high crags) ·
kind route · region north · **enter** from `galehigh_terraces` **→ exit** to
`pale_vault_glacier` (ungated) · **boundary gate:** Updraft Kite (I→II) · **Gleam:** none ·
**rec. level 34 → 36.**

### 1. Main path

1. **Windward Stair I — the lower switchbacks.** A vertical mountain route, travelled
   **south→north / up**; `stone` greys, the sunset now thin and cold behind you, `diamond`
   updraft motes catching the high light. Read as climbing 15×10 beats: a switchback, a ledge
   rest, a gust. Tall-grass on the wider ledges (crag-climber ram, slate-wing moth, gust-finch).
2. **The boundary — the first real gap.** Segment I ends at a **sheer wind-gap**: the path
   resumes across an updraft column you cannot reach on foot. This is where **Updraft Kite pays
   off** — ride the thermal across into segment II. (`windward_stair_i → windward_stair_ii`,
   `requires_ability: updraft_kite`.)
3. **Windward Stair II — the high crags.** Bare, bright, windy; the warmest colour gone, the
   first thin patches of `bone` snow on the high crags hinting at the glacier ahead. **On
   reaching the crags, set `flag:shortcut_windward`** — a ledge directly above Galehigh opens
   as a one-glide drop-shortcut back down (spine §0 rule 3). Place a **"now accessible"**
   callout naming the Galehigh return.
4. **Exit north** to `pale_vault_glacier` (ungated — you arrive at the glacier town with only
   Updraft + your earlier Gifts; Emberward is earned *there*, not needed to get there).

### 2. Story beats

- **Quiet transit beat, not a plot beat** (the North's named beats land at Galehigh and Pale
  Vault). Use the Stair for **Arc D pacing**: the visible, gradual handover from Galehigh's last
  fire to the cold high blue — the climb *feels* like leaving warmth behind, setting up Pale
  Vault's loneliness.
- A lone crag-tender NPC near the shortcut ledge marks the drop home.

> *Signature line:*
> - Crag-tender, at the shortcut ledge: *"Cold up here, isn't it. If your lamp gutters, just
>   step off that ledge — it's a short glide home to Galehigh's fires. Knowing the way back is
>   half of going on."*

### 3. Mechanic introductions

- **Updraft Kite in anger.** The boundary gap is the first place the Gift is *required* to
  progress (Galehigh's ledges were optional). The genre's "Route 1 → Route 2 earned crossing."
- **Shortcut taught.** `flag:shortcut_windward` opens the drop home — the region's contribution
  to the "map collapses into faster loops" cadence (spine §5).

### 4. Optional content

- **Thunderroost** — spur off Windward II, `requires_ability: updraft_kite`; reward: a **rare
  Storm/Flying kin + item**. **[MISSABLE]** — open the moment you reach the crags (you already
  hold Updraft), a dead-end you must choose to fly to. Tag it hard.
- **Windward→Galehigh drop shortcut** — **[MUST-DO]** to *trigger* (it sets the flag just by
  reaching the crags); using it is optional convenience.

### 5. Don't-miss callouts

- **Thunderroost** — the North's second optional Storm reward; grab it while you're already on
  Updraft, before the cold leg. **[MISSABLE]**
- Remember the **drop home** exists before committing to Pale Vault — a fast resupply line.

### 6. Validation hooks

- **Map ids / kind:** `windward_stair_i`, `windward_stair_ii`, kind `route`, region `north`.
- **Boundary warp (graph.ts):** `windward_stair_i → windward_stair_ii` via `to_stair_ii`,
  **`requires_ability: updraft_kite`**, bidir.
- **Onward warp:** `windward_stair_ii → pale_vault_glacier` via `to_glacier` — **ungated**,
  bidir (critical: Pale Vault town reachable without Emberward).
- **Spur warp:** `windward_stair_ii → thunderroost` via `to_roost`, `requires_ability:
  updraft_kite`, bidir.
- **Shortcut warp:** `windward_stair_ii → galehigh_terraces` via `shortcut_galehigh`,
  `requires_flag: flag:shortcut_windward`, bidir.
- **Trigger `sets_flags`:** on first reaching the Windward II crags → **`flag:shortcut_windward`**
  (`EventTrigger` kind `script`, `once: true`).
- **Encounter zones:** `tall_grass` (sheltered ledges) — crag-climber ram (Stone/Storm),
  slate-wing moth (Stone/Flying), gust-finch (Storm); level band 34–36.
- **NPC:** crag-tender near the shortcut ledge; dialogue ref `npc.windward_crag_tender`.

---

## Pale Vault Glacier — *the lonely aurora, where the cold man speaks*

**At a glance** — `pale_vault_glacier` · kind route/town · region north · **enter** from
`windward_stair_ii` (ungated) **→ exit** to `hushfrost_pass_i` (ungated, handed to West) ·
**gate ability:** Emberward — but it gates only **onward** content (Hushfrost II + Pale Vault's
deep-ice spurs), **NOT** the town or Lumenary · **Gleam:** Frost (Ysolde Frost, ace ~40) ·
**rec. level ~36 → 40.**

### 1. Main path

1. **Out onto the ice.** The high crags open to a wide aurora-lit glacier — cold `deepBlue` ice,
   `diamond`/`grass`-green ribbons across the sky, `bone` snow, `ink` crevasses. Lonely and
   beautiful; the lowest emotional point of the region's road. The lit path leads in across
   sheltered hollows (Frostkit, Snowtoll in the tall-grass).
2. **Walk straight into town — no gate.** The glacier town and its Lumenary are reachable on
   foot from the crags (spine §0 rule 1). **Do not** place a coldfog/thin-ice barrier between
   the town entrance and Ysolde. The Aurora-watch festival glimmers on the ice (Arc E, below).
   **The earned loop — "The Lamp-Line" (spine §5, shape #6: ice lamp-line, a single-map
   trial).** **The tease:** beneath the Lumenary, the **undercroft door** — and through the
   clear blue ice beside it, **seven dark lamp-brackets** visible in a descending line.
   *(The undercroft is dark blue ICE, never coldfog — Emberward stays out of this loop and
   no barrier ever stands between the town entrance and Ysolde herself.)*
   Ysolde's hook, at the door: *"Cold does not hate the flame, wanderer. It only waits to
   see if the flame means it. Walk my vault, light the seven brackets — and let me see the
   light hold."* (`script.ysolde_quest` → `flag:q_north_lampline`.)
3. **The tallow-keeper's errand (collinear).** The brackets burn **aurora-oil**, and the
   tallow-keeper in the sheltered approach hollows (band 36–38, the same hollows the lit
   path crosses) cannot render it — her hearth is doused. Relight it with the cached
   **storm-kindling** nearby (`flag:picked_stormwood`) → `script.render_oil` →
   `flag:q_north_aurora_oil`.
4. **B3 — Còr appears, in person** — on the open ice during the oil leg, where the calm
   lands hardest. Courteous, sad, *persuasive*; pays off the East foreshadow. **No battle.**
   Sets **`flag:met_cor`**. (Detail in §2.)
5. **C3 — Fenn and the shared past.** On Còr's heels, **Star-tender Fenn** finds you and
   reveals the canon-locked truth: **Fenn and Còr were once fellow star-tenders** — two
   answers to the same loss.
6. **A4 — Wren's wobble — at the undercroft door.** Wren stands where you are about to
   prove a light can hold, and **nearly joins the Hollowing**. The **hard rival battle**
   (Wren's toughest yet), and afterward they walk off **unsure**. *(The staging is the
   argument: Wren wavers at the exact threshold of the light-holding trial.)*
7. **The Lamp-Line** — the undercroft door takes the oil (`requires_flag`, blocked line in
   Ysolde's voice) → **`pale_vault_undercroft`** **[NEW MAP]**: one blue-ice floor, the
   seven brackets lit **in line** (each script requires the previous —
   `flag:q_north_lamp_1..7`, the seventh setting `flag:q_north_lamps_held`), **two
   frost-ward sight trainers** (lv 37–39) between brackets.
8. **Lumenary 6 — Ysolde Frost (Frost), at the vault's heart.** A serene, riddling
   glaciologist; ace ~40, met at ~38–39. The bond-test trigger requires
   `flag:q_north_lamps_held` (`blocked_ref` in her voice). Win → **Frost Gleam** +
   **Emberward** + `gleam:frost`, ability `emberward`. With Storm + Frost both held, the
   engine sets **`flag:crown_north`** — the North quadrant of the Skyweave Crown completes
   overhead, the Aurora-watch lifting its lamps around you.
9. **The map reopens (Emberward).** Now the onward path and the deep-ice spurs open. Place a
   **"now accessible"** callout at the **`hushfrost_pass_i → hushfrost_pass_ii`** coldfog throat
   (the West writer's onward segment, gated by Emberward — which you now hold) and at Pale
   Vault's own deep-ice / Aurora-watch back-folds.
10. **Exit west** to `hushfrost_pass_i` (ungated) — hand off to West at ~lv40 holding
   Tidecall + Glimmerstep + Updraft Kite + Emberward, `crown_north`, `met_cor`, `shortcut_windward`.

### 2. Story beats

- **B3 — the man himself.** Place it on the cold, still ice where his philosophy lands hardest:
  a world held forever in soft, painless dark *looks* like this calm. He is never cartoonish —
  grief dressed as mercy. He knows your name, knows Fenn, and **does not fight you**; he simply
  shows you a quieted, peaceful thing and asks whether the cycle of loss is really worth the
  dawn. He leaves you to decide. (`flag:met_cor`.)
- **C3 — Fenn's confession.** Fenn arrives shaken to have just missed Còr. Reveal: they tended
  the stars together, long ago; the same loss broke them in opposite directions — **Fenn into
  quiet hope, Còr into grief**. Fenn doesn't ask you to hate him, only to *out-remember* him.
- **A4 — Wren nearly turns.** Wren, raw from the cold and Còr's words, says the Hollowing might
  be *kind*. The battle is the argument — you don't beat sense into Wren, you bond hard enough
  that they *feel* what's worth keeping. They walk off **unsure**, not resolved (resolution is
  Arc A5, West/Spire). Make this Wren's hardest fight.
- **Arc E — the Aurora-watch.** Pale Vault's festival: the town gathers on the ice in silence to
  watch the aurora, each holding a single lit lamp — the quietest, most melancholy festival,
  belonging as *stillness*. Ysolde keeps it. It deliberately rhymes with Còr's vision of a calm
  dark — and quietly refutes it (the lamps are *lit*).

> *Signature lines (flavour, not script):*
> - Còr, gently: *"Look at it. No lamp guttering, no goodbye, nothing lost. I am not your enemy,
>   apprentice. I am only tired of grief — and I think, if you're honest, so is everyone."*
> - Fenn, quietly: *"He and I read the same sky once, you and I. We lost the same thing. He chose
>   to stop the cycle so it could never hurt again. I chose to keep lighting lamps. ...I still
>   think I was right. But I never stopped understanding him."*
> - Wren, after the battle, not meeting your eye: *"You fight like you've got something the dark
>   can't take. I don't know if I've got that. ...I need to walk a while."*
> - Ysolde, before the Gleam: *"Cold does not hate the flame, wanderer. It only waits to see if
>   the flame means it. Warm your kin — and let me see the light hold."*

### 3. Mechanic introductions

- **Emberward earned** — burns a path through **coldfog** (the Hollowing's creeping mist).
  Taught toward the *onward* journey: it opens the West's Hushfrost coldfog throat and Pale
  Vault's deep-ice spurs — **never** used to reach Ysolde (spine §0 rule 1).
- **"Now accessible" callouts (this Gift):** the `hushfrost_pass_i → hushfrost_pass_ii` boundary
  (West), Pale Vault deep-ice back-folds, and (cross-region, **[LATER]** by area) the Coldfog
  Marches deep + Aurora Hollow — all Emberward content the West writer owns; mention only as
  *now-held-Gift* callouts, do not author them here.
- **Frost type pressure peaks.** Status `chill` assumed (spine §5); write Ysolde around it.

### 4. Optional content

- **Aurora Hollow** — spur off `hushfrost_pass_ii`, `requires_ability: emberward`; reward: rare
  Frost/Light kin + item. **This is the WEST writer's map — do NOT cover it here.** Listed only
  so the cross-reference closes: it's an Emberward reopening you hold the Gift for. **[LATER]**
  (different region).
- **Pale Vault deep-ice / Aurora-watch back-folds** — Emberward-gated within the glacier;
  rare Frost kin. **[MISSABLE]** once Emberward is earned (don't leave the glacier without
  sweeping them). *(If authored as a separate node later, gate it `emberward`, not the town.)*

**Named quests** (spine §5 kit):
- **N2 "The Aurora Sketcher"** — giver: a **painter NPC** at the Aurora-watch · steps:
  stand with her at three sketching viewpoints (interacts: a Windward II crag, the glacier
  shore, the festival ice) while she works · flags: `flag:q_north_sketch_1..3` →
  `flag:q_north_sketch_done` · reward: the **Aurora Charm** · maps: `windward_stair_ii`,
  `pale_vault_glacier` · `[MISSABLE]` — pure stillness; the quiet sibling of the
  Lamp-down vigil.
- *(N1 and N3 are listed under Galehigh's Named quests; R4 under Galehigh. North's slate:
  N1 · N2 · N3 · R4.)*
- **No Galehigh/Windward content waits on Emberward** — its reopenings are all West-region or
  Pale-Vault-deep, keeping this region's backtrack web honest.

### 5. Don't-miss callouts

- **Don't skip the B3/C3/A4 cluster** — the emotional spine of the whole game lands on this ice.
  Trigger Còr, hear Fenn, fight Wren *before* the Gleam so the Lumenary reads as the quiet
  answer to Còr's question.
- **Sweep the Emberward-gated deep-ice** before crossing to West. **[MISSABLE]**
- **Attend the Aurora-watch** — the festival's silent lit lamps are the region's thesis.

### 6. Validation hooks

- **Map id / kind:** `pale_vault_glacier`, kind `route`/`town`, region `north`.
- **Entry/exit warps (graph.ts):** in from `windward_stair_ii` via `to_glacier` (**ungated**,
  bidir); out to `hushfrost_pass_i` via `to_pass` (**ungated**, bidir). **No Emberward gate on
  either** — Emberward gates only `hushfrost_pass_i → hushfrost_pass_ii` (via `to_pass_ii`,
  `requires_ability: emberward`, West-region edge).
- **Lumenary is NOT ability-gated** (spine §0 rule 1) — door requires no Gift; Ysolde is
  reachable on foot from the crags. **Author no coldfog/thin-ice barrier between the town
  entrance and Ysolde.**
- **Lumenary trigger `sets_flags`:** Ysolde victory → `gleam:frost` + grants ability `emberward`.
  With `gleam:storm` already held, the engine sets **`flag:crown_north`** (do not hand-set it,
  but the section depends on it).
- **Story triggers `sets_flags`:** Còr-in-person cutscene → **`flag:met_cor`** (`script`,
  `once: true`, staged on the oil leg); Fenn C3 cutscene (narrative only, no flag required);
  Wren A4 trainer battle **at the undercroft door** (`reward_flags` for the rival-battle
  bookkeeping — Arc A4, no progression gate).
- **The Lamp-Line chain (rule 3):** `script.ysolde_quest` sets `flag:q_north_lampline`;
  kindling cache `flag:picked_stormwood`; `script.render_oil` sets
  `flag:q_north_aurora_oil`; the undercroft door warp `requires_flag:flag:q_north_aurora_oil`
  (blocked line in Ysolde's voice) → **`pale_vault_undercroft`** **[NEW MAP]** (cave
  interior, ~20×16; bracket scripts chained `flag:q_north_lamp_1..7`, the seventh setting
  `flag:q_north_lamps_held`; 2 frost-ward SIGHT trainers lv 37–39); Ysolde's bond-test
  trigger `requires_flag:flag:q_north_lamps_held` with `blocked_ref:npc.ysolde_not_ready`.
- **Encounter zones:** `tall_grass` (sheltered hollows) — Frostkit (Frost), Auralisk
  (Frost/Light), Snowtoll (Frost); level band 36–40 (continuous with Windward 34–36 and West's
  Hushfrost entry ~40). Emberward-gated deep-ice zones carry rarer Frost kin at low weight.
- **NPC / Lumenary / festival:** Ysolde Frost (Frost Lampwarden); Warden Còr (B3, in person, no
  battle); Star-tender Fenn (C3); Wren (A4 hard battle); Aurora-watch festival cutscene +
  flag-gated NPCs. Dialogue/script refs: `npc.ysolde_frost`, `cutscene.cor_appears`,
  `cutscene.fenn_shared_past`, `trainer.wren_pale_vault`, `cutscene.pale_vault_aurora_watch`.

---

## Hand-off to West

The West writer picks up at **`pale_vault_glacier → hushfrost_pass_i`** (ungated) with the player
at **~lv40**, holding **Tidecall + Glimmerstep + Updraft Kite + Emberward**, `gleam:storm` +
`gleam:frost`, **`flag:crown_north`**, **`flag:shortcut_windward`**, and the persistent narrative
ledger **`flag:dusk_begins`** + **`flag:met_hollowing`** + **`flag:met_cor`** (all carried forward). The
**Hushfrost Pass I → II** boundary (`to_pass_ii`) is gated by **Emberward — now held** — so the
West onward path is open the moment the player arrives. **Aurora Hollow** (off Hushfrost II,
Emberward) is West's to write. Arc beats still owed downstream: **A5** (Wren returns, resolved),
**B4** (Great Null named), **C4** (Fenn's counsel before the Spire).
