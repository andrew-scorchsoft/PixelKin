# PixelKin — Walkthrough: East (Gleams 3–4 → `crown_east`)

> Region file 2 of 6. Read the **[spine](./README.md)** first — it binds §0 rules, the §2
> flag strings, the §3 arcs, the §4 curve, the §5 cadence, the §7 per-area template, and the
> §10 voice. Pairs with [`atlas.md`](../atlas.md) (§2 cards 4–5 + Saltreach Fen route §3),
> [`story-bible.md`](../story-bible.md) (§7 the Hollowing, §8 null-lanterns), and
> [`graph.ts`](../../../src/game/data/world/graph.ts) (nodes/edges ~81–89, 123–129, 146–148,
> 154, 167). All content original per [`VISION.md`](../../../VISION.md). Canon vocabulary only.

## Region at a glance

The eastern crescent is where the journey turns from "a sleepy region with a flickering sky"
into "someone is *doing* this." It is the **first contact with the Hollowing** — a small,
gently drained site and a sleeping luminous kin you relight by hand — and the region that
hands you **Glimmerstep**, the Gift that re-opens half the early map. It ends on the
deliberate **Stone wall**, Otho Grist, the first Lampwarden who can genuinely stop an
under-prepared player.

- **Entry state (from South):** ~lv16, holds **Tidecall**; `gleam:ember` + `gleam:tide`;
  `flag:crown_south`. The Vesper Crossroads hub is known (Lanternway spoke from Pearlmoor /
  later Lowleaf), but its Spire roads are still sealed.
- **Exit state (handed to North):** ~lv28, holds **Tidecall + Glimmerstep**;
  `gleam:verdant` + `gleam:stone` → `flag:crown_east`; `flag:met_hollowing`;
  `flag:shortcut_mine`. Reaches Galehigh via `cinderhead_deep → galehigh_terraces` (ungated).
- **Gleams delivered:** **3 · Verdant** (Sable Quill, Lowleaf Hollow) and **4 · Stone**
  (Otho Grist, Cinderhead Mine).
- **Lantern Gift delivered:** **Glimmerstep** (earned at Lowleaf — enter dark caves/woods).
- **Arc beats landing here:** **A3** (Wren shaken — sympathy for the Hollowing after the
  drained site); **B2** (first Hollowing contact + first Còr foreshadow; `flag:met_hollowing`);
  **E** (the **Glowmoss Bloom** at Lowleaf, the **Lamp-down vigil** at Cinderhead). Arc **C** /
  Fenn does not recur here; Còr appears *in person* only in the North (B3) — East gives a
  foreshadow, not the man.
- **Mechanics introduced:** **Glimmerstep** + its mapwide "now accessible" callouts (Tideglass
  Cavern back in South; Spore Grotto here); **kindling** likely fires for the first time here
  (the starter kindles ~16–20 — teach it); **deep-cave navigation**; the **Stone bulk** wall.
- **Cinematic staging (PLANNED — build from South per [`cinematics.md`](../cinematics.md) / §0.4):**
  **B2 Glowmoss Deep** is East's marquee set-piece and the first real test of the toolkit —
  stage the drained chamber like `dusk_begins` writ large: `letterbox on` + `silence` as the
  colour drains (tiles grey, music gutters out), a slow `cameraFocus` onto the sleeping kin and
  the null-lantern, the **distant Còr glimpse** as a `cameraFocus` on a cowled actor who turns
  and withdraws (no battle, no name) — Còr/acolyte **portraits** (sorrowful, kind). Restoring the
  null-lantern is a quiet `gleam`-adjacent relight (a *small* warm `tint`, no festival swell —
  this is grief eased, not a Gleam). **A3 Wren shaken** uses Wren's `unsure` portrait. The two
  festivals (**Glowmoss Bloom**, **Lamp-down vigil**) reuse the South Gleam cadence (minor→major
  + `gleam-emotional`), but Cinderhead's vigil should stay the most *melancholy* swell (lean on
  `silence` before the lift). Assets owed: Còr + acolyte portraits, a "grey/drained" battle
  backdrop, optionally a darker drained-site cue.

**Arc D — lighting note (binding, §3 Arc D).** East must read **visibly lighter than South's
deep blue hour** — but it is still night. The register is **dewy bioluminescent dark**: the
fen glints with `diamond` glimmer-light on black water, Lowleaf glows green-gold from within
(glowmoss everywhere), and Cinderhead trades sky-light for **deep-earth gleam** — crystal
veins and miners' `fire` lamps in `ink`-black tunnels. As `gleam:verdant` then `gleam:stone`
relight, the fen and the forest-fringe warm a notch and the vesperlamp sits one tier brighter.
Tie any encounter-table shift to the **Gleam flag**, never to the tile the player walked in
from (spine §0 rule 2).

**The shape of the region** (atlas §3: segmented chain → town/Lumenary → spur → landmark →
hub spoke): Saltreach Fen I → II (Tidecall on the boundary) → **Lowleaf Hollow** (Verdant
Lumenary) ↔ Glowmoss Deep (Glimmerstep) → **Cinderhead Mine** (Stone Lumenary) ↔ Cinderhead
Deep (Glimmerstep) → onward to Galehigh. Spurs: **Sunkbell Shallows** (Tidecall, now),
**Spore Grotto** (Glimmerstep, once earned), **Crystoll Vault** (Starreach — `[LATER]`).

---

### Saltreach Fen I — *brackish reed marsh under glinting mist*

**At a glance** — `saltreach_fen_i` · route (open marsh) · east · enter from Pearlmoor
(`to_fen`) / exit north to Saltreach Fen II · **no entry gate** (Tidecall gates the *boundary*
to II, not this segment) · Gleam: none · rec. level ~16.

1. **Main path** — A wide, low marsh travelled **south→north**, reed islands strung together
   by raised plank causeways (the lit, walkable spine; the open black water off the planks
   collides). Beat by beat: (1) plank landing in from Pearlmoor, a dry rest pocket with a
   route sign; (2) first reed-bed `tall_grass` patch on a causeway-side island; (3) a
   fork — the wide lit causeway pushes north, a narrow side-plank tapers toward a **deep
   channel** you can *see* but not yet cross (the Tidecall boundary tease, framed with
   lantern-reeds); (4) a second, larger reed patch; (5) the boundary screen: a Tidecall-marked
   channel where the planks end, with a sign and the warp north to Fen II.
2. **Story beats** — No arc beat lands *in* this segment; it is the breather and the level
   on-ramp (16→18) between Pearlmoor and the Lowleaf cluster. A travelling fen-warden NPC
   foreshadows the marsh's mood and (lightly) that "the eastern woods have gone quiet of
   late" — a soft B-arc seed, not contact yet. *Sample:* "Mind the planks after dark — the
   fen's friendly, but it doesn't like to be hurried."
3. **Mechanic introductions** — Reinforces **Tidecall** as a *traversal* gate at the boundary
   (the player already holds it from Pearlmoor, so I→II is passable — no soft-lock). No new
   Gift here. Marsh/shallow-water terrain reads as a new biome.
4. **Optional content** —
   - Reed-island item cache (a Lamp / restorative) tucked off the causeway behind a reed
     screen — **[MISSABLE]** (easy to walk past; reachable now, no Gift needed).
5. **Don't-miss callouts** — The deep-channel tease toward Fen II: it visibly *wants*
   Tidecall, which the player has — stepping across it is the satisfying "oh, I can do this
   now" beat that justifies the South Gift one region on.
6. **Validation hooks**
   - map id `saltreach_fen_i`, kind `route`; entry land-in paired with Pearlmoor's `to_fen.to`
     near the south edge (`facing:'up'`); north exit warp `to_fen_ii` at the boundary
     (`facing:'up'`, `fade`).
   - edge **`saltreach_fen_i → saltreach_fen_ii requires_ability: tidecall`** (graph.ts:124) —
     held on entry; do **not** add a second copy of Tidecall content here.
   - encounter zones: `tall_grass` reed beds — **mudskip pup** (Tide), **reed-stalk heron**
     (Tide/Flying), low weight (atlas §3 Saltreach kin); level band **16–18**; rate ~0.10.
   - NPC: `fen_warden` (`look_around`, `dialogue_ref:'npc.fen_warden'`); route sign +
     boundary sign (`kind:'sign'`, `interact`).
   - no `sets_flags` triggers.

---

### Saltreach Fen II — *deep channels and lantern-reeds*

**At a glance** — `saltreach_fen_ii` · route (deep channels) · east · enter from Fen I across
the **Tidecall** boundary / exit to Lowleaf Hollow (`to_hollow`) · spur: Sunkbell Shallows ·
Gleam: none · rec. level ~18.

1. **Main path** — Deeper, wetter, more open than Fen I: now the player **uses Tidecall** to
   step the parted moon-channels between reed isles, the water itself becoming the route. Beats:
   (1) the parted-channel crossing in from Fen I; (2) a reed isle with the densest grass patch
   of the marsh; (3) a branch toward the **Sunkbell Shallows** spur (a flooded shrine roofline
   visible across the water); (4) the marsh thins to firm ground and a tree-line — the forest
   fringe of Lowleaf sight-lined ahead, lit green; (5) the north warp into Lowleaf Hollow.
2. **Story beats** — Still pre-contact; the dread is environmental. One snuffed lantern-reed
   (a single dead reed-lamp among the glowing ones) is a *quiet visual* foreshadow of the
   drained site to come — no dialogue needed. *Sample (a fisher on an isle):* "Lamp-reed's
   gone dark out there. Used to glow all season. …Probably nothing."
3. **Mechanic introductions** — Tidecall is now *load-bearing* for the path (not just a tease),
   teaching that Gifts re-shape routes, not only open spurs. Level band tops out the South-to-
   East ramp at ~18 before the Lowleaf Lumenary.
4. **Optional content** —
   - **Sunkbell Shallows** (`sunkbell_shallows`) — spur off Fen II, **[MISSABLE]** (reachable
     **now** with Tidecall; easy to overlook across the water). A half-flooded shrine: rare
     **Tide** kin (low-weight encounter) + an item cache (atlas §3 reward). Sign the
     turn-off so the *come-back* is explicit even if skipped.
   - Hidden item on a far reed isle reachable only by a parted channel — **[MISSABLE]**.

   **Named quests** (spine §5 kit):
   - **E1 "The Quiet Reeds"** — giver: the **fen fisher** on the channel jetty · steps:
     re-kindle three snuffed lantern-reeds along the channels (interact scripts) — the
     first two take; **the third will not light**, and the fisher has no answer for it
     (a SILENT B2 foreshadow: no one names the Hollowing — that belongs to Glowmoss Deep) ·
     flags: `flag:q_east_reeds` → `flag:q_east_reeds_done` (set on reporting back, third
     reed still dark) · reward: the **Marsh Lamp** · maps: `saltreach_fen_ii` ·
     `[MISSABLE]`.
5. **Don't-miss callouts** — Sunkbell Shallows is the region's "you can already get this"
   reward — it pays off Tidecall immediately and seeds the habit of detouring for spurs that
   the rest of East leans on hard.
6. **Validation hooks**
   - map id `saltreach_fen_ii`, kind `route`; south land-in paired with Fen I `to_fen_ii.to`;
     north exit `to_hollow` → `lowleaf_hollow` (graph.ts:125, ungated, `facing:'up'`).
   - spur edge **`saltreach_fen_ii → sunkbell_shallows requires_ability: tidecall`**
     (graph.ts:146) — warp `to_sunkbell`; tag **[MISSABLE]**.
   - encounter zones: `tall_grass` reed isles + `water` parted channels — **marsh-lantern frog**
     (Tide/Light), **mudskip pup** (Tide), **reed-stalk heron** (Tide/Flying); `sunkbell_shallows`
     carries a **low-weight rare Tide** entry; level band **17–19**; rate ~0.10 (spur ~0.08).
   - one dead-reed `deco` prop (the snuffed-lantern foreshadow); fisher NPC + turn-off sign.
   - no `sets_flags` triggers (Sunkbell's item cache may set a local boolean for the cache only).

---

### Lowleaf Hollow — *bioluminescent fern town, glowing green from within*

**At a glance** — `lowleaf_hollow` · route/town (forest) · east · enter from Fen II
(`to_hollow`) / exits to Glowmoss Deep (`to_deepwood`, **Glimmerstep**) and the Vesper
Crossroads (`to_crossroads`, Lanternway) · **Lumenary 3: Sable Quill (Verdant)**, ace ~22 ·
**Gleam: Verdant** + **Glimmerstep** · rec. level ~18.

> **§0 rule 1 (binding):** the Lumenary is **not** behind Glimmerstep — Glimmerstep is *earned
> here*. The town and Sable Quill's Lumenary are reachable with no Gift; Glimmerstep gates only
> the onward `to_deepwood` route into **Glowmoss Deep** and the Spore Grotto spur.

1. **Main path** — A cosy forest town in a fern hollow: `bone` cottages half-grown over with
   `diamond` glowmoss, lantern-strings between trunks, the **Glowmoss Bloom** festival in full
   swing (Arc E). **The earned loop — "The Tended Bed" (spine §5, shape #3: in-town tending;
   deliberately the LIGHTEST loop, a breath between the Causeway Bell and the Descent
   Vigil).** Beats:
   (1) arrive at the festival edge — stalls, dancing lights, NPCs; **the tease:** at the
   hollow's heart, the Bloom's centrepiece — the **Elder Bed**, the oldest moss-bed in
   town — lies **grey** amid all that glow. (A festival NPC fences the B-arc explicitly:
   *"not the Hollowing, love — just a tired old bed after a cold spring"* — first contact
   with the Hollowing still belongs to Glowmoss Deep; escalation stays monotonic.)
   (2) the town spine leads to **Sable Quill's Lumenary**, central and tallest, doors open —
   and Sable's hook: *"The Bloom won't crown over a grey bed. Warm the old moss first —
   then we'll see what your light's worth."* (`script.sable_quest` → `flag:q_east_bloom`;
   her bond-test trigger carries a `blocked_ref` in the same voice until the bed blooms.)
   (3) **the kilner's errand (collinear):** the festival kilner's kiln has gone out; dry
   **fen-wood** sits cached on the town map's own forest fringe (band 18–20, the lane
   watched by **two bloom-warden sight trainers**) → `flag:picked_fenwood` →
   `script.kiln_relight` → `flag:q_east_hearthspore` (the kilner fires a **hearth-spore**);
   (4) **warm the Elder Bed** (`script.warm_elder_bed` → `flag:q_east_bed_warm`) — the bed
   blooms grey→green (the §8 null-lantern data pattern reused warmly: deco/NPC swap), and
   the festival crowns around it;
   (5) the **Verdant Gleam** bond-test at the blooming bed; (6) Sable grants **Glimmerstep**
   and points you at the dark hollow-mouth she "can never get into"; (7) the now-lit
   `to_deepwood` mouth on the town's north edge, plus the Lanternway spoke west to the hub.
2. **Story beats** — **Arc E (Glowmoss Bloom):** the festival frames the Gleam as *belonging*,
   not conquest — Sable, a shy botanist, is more comfortable letting her glowmoss vouch for you
   than making a speech. **Arc A (A2→A3 setup):** Wren is here, but **A3 (Wren shaken) properly
   lands after the drained site at Glowmoss Deep** — in town Wren is still bright, ribbing you
   about the festival. **B-arc seed:** townsfolk mention the "quiet" deep-wood; a courteous,
   anonymous **letter** is pinned at the Lumenary notice-board — the first whisper of Còr's
   voice (the B2 foreshadow *starts* here, pays off in the Deep). *Samples* —
   - Sable Quill (granting the Gleam): "The moss doesn't shine *for* anyone. It just… keeps a
     little light where it can. Be like the moss. Here — this'll let you walk where it's dark."
   - The pinned letter (unsigned, courteous): "To whoever tends these lamps after me: do not
     grieve the dark. It asks nothing of you, and it never leaves."
3. **Mechanic introductions** — **Glimmerstep earned** (enter dark caves/woods). Place the
   **mapwide "now accessible" callout** here (spine §5): a town sign / Sable line that names
   what just opened — **Tideglass Cavern** back in Dimglass Coast (South landmark) and the
   **Spore Grotto** in the deep wood. **Kindling teach:** the starter is ~lv16–20 by now, so
   the **first kindling** likely fires around the Verdant fight — surface a gentle in-town
   explanation (an NPC or Sable: "your kin's ready to *kindle* — let it"). Kindling = evolution
   in canon; never call it that.
4. **Optional content** —
   - **Glowmoss Deep** (`glowmoss_deep`) — the forest interior, **[MUST-DO]** for progress
     (it's the route to Cinderhead) but written as a depth: gated by **Glimmerstep**, just
     earned.
   - **Spore Grotto** (`spore_grotto`) — spur off Glowmoss Deep, **[MISSABLE]** (needs
     **Glimmerstep**, which you now hold — so reachable *as soon as* you enter the Deep): rare
     **Bug/Verdant** kin + item (atlas §3).
   - **Now accessible elsewhere:** **Tideglass Cavern** (Dimglass II, South) — **[MISSABLE]**,
     a Glimmerstep landmark the player can backtrack to immediately.
   - Festival mini-rewards (a Glowmoss-Bloom Lamp from a stall; a glowmoss item from a child
     NPC) — **[MISSABLE]**.

   **Named quests** (spine §5 kit; East's slate, E1 over in Fen II, E3 in Cinderhead):
   - **E2 "Spores for the Stall"** — giver: the **Bloom stall-keeper** · steps: gather two
     spore caches in Glowmoss Deep → drive off the cross **Sporeling** squatting on the
     third (a scripted battle) → return · flags: `flag:q_east_spores` →
     `flag:q_east_spores_done` · reward: **Glow Salve** + the stall-keeper points out a
     **Fennlight** static catch · maps: `lowleaf_hollow`, `glowmoss_deep` ·
     `[LATER: Glimmerstep]` (held by then — a same-visit backtrack).
   - **R3 "Moss for the Quay"** — the Waykeeper's Round, leg 3: parcel (a living glowmoss
     plug) from the **Waykeeper** → the **Pearlmoor shrine-keep** · flags:
     `flag:q_round_moss` · reward: balm kit + a Lanternway line · maps:
     `vesper_crossroads`, `lowleaf_hollow`, `pearlmoor_quay` · `[wakes with spoke]`
     (the Lowleaf spoke wakes with `gleam:verdant`).
5. **Don't-miss callouts** — Catch a **Fennlight** (Verdant/Light) during the Bloom — the
   signature town kin and a strong early Light-typed answer for the road ahead. And read the
   pinned letter: it is the only Còr foreshadow a careful player gets before the Deep.
6. **Validation hooks**
   - map id `lowleaf_hollow`, kind `town` (route/town); interior `lowleaf_lumenary`.
   - warps: `to_hollow` land-in (paired with Fen II); **`to_deepwood` → `glowmoss_deep`,
     `requires_ability: 'glimmerstep'`** (graph.ts:126); `to_crossroads` Lanternway spoke
     (graph.ts:160, ungated); Lumenary door warp (no Gift gate — §0 rule 1).
   - triggers / flags: Gleam-grant cutscene at the Lumenary **`sets_flags:['gleam:verdant']`**
     (the engine derives `flag:crown_east` only once **both** Verdant + Stone are held — do
     **not** set `crown_east` here); a `kind:'script'` step that **grants the `glimmerstep`
     ability**; festival cutscene (`once:true`). The pinned letter is a `kind:'sign'` trigger,
     `dialogue_ref:'sign.cor_letter'`.
   - **The Tended Bed chain (rule 3):** `script.sable_quest` sets `flag:q_east_bloom`;
     fen-wood cache `flag:picked_fenwood`; `script.kiln_relight` sets
     `flag:q_east_hearthspore`; `script.warm_elder_bed` sets `flag:q_east_bed_warm`
     (+ the Elder Bed grey→green deco/NPC swap); the bond-test trigger
     `requires_flag:flag:q_east_bed_warm` with `blocked_ref:npc.sable_not_ready`.
     Two **bloom-warden sight trainers** (lv 19–21) on the fringe lane.
   - Lumenary battle: **Sable Quill**, Verdant, ace ~22; trainer entry + `dialogue_ref`.
   - encounter zones: `tall_grass` forest-fringe — **Sporeling** (Verdant), **Fennlight**
     (Verdant/Light), **Mossmole** (Verdant) (atlas card 4); level band **18–20**; rate ~0.10.
   - "now accessible" callout sign/NPC naming **Tideglass Cavern** + **Spore Grotto** (closes
     the spine §5 Glimmerstep back-reference).
   - festival NPCs (flag-gated to the Bloom cutscene); kindling-explainer NPC line.

---

### Glowmoss Deep — *the glowing dark interior; first Hollowing contact*

**At a glance** — `glowmoss_deep` · forest interior (cave-like) · east · enter from Lowleaf
(`to_deepwood`, **Glimmerstep**) / exit to Cinderhead Mine (`to_mine`) · spur: Spore Grotto ·
Gleam: none · rec. level ~20.

1. **Main path** — The hollow's dark, breathing interior — only walkable *because* you now hold
   Glimmerstep, your lamp the one moving light. Branchy, with 1–2-tile chokes between glowmoss
   chambers (level-design cave pattern). Beats: (1) enter the dark, lamp blooming a glow radius;
   (2) a chamber of dense glow-grass; (3) **the drained site** — a clearing where the glowmoss
   has gone *grey*, lanterns snuffed, colour drained from the tiles (the B2 set-piece); (4) the
   **sleeping luminous kin** at its heart — a dimmed Fennlight curled in a dead glow, beside a
   **null-lantern**; (5) the **null-lantern restoration** beat — relight it; the chamber blooms
   back to green, the kin wakes; (6) the far choke out to the Cinderhead mine mouth, plus the
   Spore Grotto turn-off.
2. **Story beats** — **B2 (first Hollowing contact + first Còr glimpse) — the region's heart.**
   At the drained site, **gentle acolytes** are at work — soft-spoken, apologetic, *certain they
   are helping* ("we only put it to sleep — no more loss, see?"). They name themselves: **"the
   Hollowing,"** and their **Warden Còr**. The **Còr foreshadow** lands as a **distant cowled
   figure** glimpsed at the chamber's far edge who withdraws without a word (paying off the
   Lowleaf letter; the *man himself* is North, B3 — no battle here). Restoring the null-lantern
   sets **`flag:met_hollowing`** and flips the site flag-gated from grey to green. **A3 (Wren
   shaken):** Wren is at the site (or just after it) and, for the first time, voices *sympathy*
   — "…what if they're not wrong? Nothing here got hurt." — then leaves unsettled. *Samples* —
   - Acolyte (kind, not cruel): "She isn't hurt. She's *resting*. Doesn't the quiet look
     gentle, after all that flickering?"
   - Wren (shaken): "You woke it up. Good. I think. …I don't know. Don't they have a point?"
3. **Mechanic introductions** — **Deep-cave / dark-interior navigation** taught here (the Gift
   in use: glow radius, chokepoint rooms, no map without your light). The **null-lantern
   restoration** mechanic introduced (a `script` trigger that sets a flag and swaps the
   encounter/NPC state of the site) — Arc B's recurring emotional beat, first instance.
4. **Optional content** —
   - **Spore Grotto** (`spore_grotto`) — spur, **[MISSABLE]** (gated by **Glimmerstep**, held):
     rare **Bug/Verdant** kin + item (atlas §3 reward).
   - A hidden glow-item in a side chamber off a choke — **[MISSABLE]**.
   - **[LATER]** none native here — but note the relit site's encounter table only blooms
     *after* `flag:met_hollowing`, so a player who skips restoration sees the grey (drained)
     table; that is intended, not a missable.
5. **Don't-miss callouts** — The restoration beat itself: it's the first time the game lets the
   player *physically undo* what the Hollowing did, and the grey→green table swap is the visual
   proof the world responds. Don't let the player tunnel straight to Cinderhead and miss it —
   put it on the only forward path.
6. **Validation hooks**
   - map id `glowmoss_deep`, kind `cave`/interior; entry paired with Lowleaf `to_deepwood`
     (**`requires_ability: 'glimmerstep'`**, graph.ts:126); exit **`to_mine` → `cinderhead_mine`**
     (graph.ts:127, ungated).
   - spur edge **`glowmoss_deep → spore_grotto requires_ability: 'glimmerstep'`** (graph.ts:147)
     — warp `to_grotto`; tag **[MISSABLE]**.
   - **B2 trigger:** `kind:'script'` at the drained site, `once:true`,
     **`sets_flags:['flag:met_hollowing']`**; flag-gated NPC/encounter swap (grey/drained table
     when unset → restored Verdant/Light table when set) — the §8 null-lantern pattern (no engine
     change). Còr-foreshadow cutscene (cowled figure) chained on the same trigger; acolyte NPCs.
   - Wren A3 cutscene (trainer NPC, dialogue-only or a light optional battle; ~lv18–20 if a
     battle — keep Wren ~2 under the player per Arc A).
   - encounter zones: `cave`/dark `tall_grass` — **Sporeling**, **Mossmole**, **Fennlight**
     (atlas card 4); `spore_grotto` low-weight rare **Bug/Verdant**; level band **20–22**;
     rate ~0.12 (cave). Drained-site zone: thinned/greyed table pre-restore (Light kin absent),
     blooms post-`met_hollowing` (atlas §4: Light kin thin in drained, bloom in relit).

---

### Cinderhead Mine — *abandoned gem mine, deep-earth gleam; the Stone wall*

**At a glance** — `cinderhead_mine` · cave town / mine mouth · east · enter from Glowmoss Deep
(`to_mine`) / exits to Cinderhead Deep (`to_deep`, **Glimmerstep**) and Galehigh via the Deep ·
**Lumenary 4: Otho Grist (Stone)**, ace ~28 — the deliberate **difficulty wall** · **Gleam:
Stone** (→ `flag:crown_east`) · rec. level ~22.

> **§0 rule 1:** Otho's Lumenary is at the **mine mouth** and needs **no Gift**; Glimmerstep
> gates only the onward `to_deep` galleries.
> **§4 (binding):** Otho Grist is the curve's **one deliberate wall** — the largest party-to-ace
> gap (rec. ~22 vs ace ~28). Cinderhead's deep encounters sit at the **top of band (24–27)** so
> a careful player can grind up to meet him. **Do not under-level the mine** or the wall becomes
> a cliff.

1. **Main path** — A miners' settlement at a mine mouth: timber headframe, cart rails,
   `fire`-lamp light against `ink` rock and `diamond` crystal veins; the **Lamp-down vigil**
   festival is underway (Arc E). **The earned loop — "The Descent Vigil" (spine §5, shape #4:
   mine descent — the HEAVY loop, and the §4 wall made diegetic).** Beats:
   (1) arrive at the lamplit mine-mouth town; **the tease:** the town's lamps hang
   **lowered and stay lowered** — the vigil cannot close until the old crew's vigil-lamp
   comes up from the deep — and the dark `to_deep` gallery mouth gapes at the town's back;
   (2) the vigil gathering — miners with lowered lamps, waiting;
   (3) **Otho Grist's Lumenary** at the mouth, and his hook: *"Down here, light's not
   given — it's kept. My crew left the vigil-lamp at the third gallery when the dark came
   up. Bring it back still lit — then we'll talk about a Gleam."* (`script.otho_quest` →
   `flag:q_east_vigil`; his bond-test trigger carries a `blocked_ref` in the same voice);
   (4) **descend `cinderhead_deep`** (Glimmerstep, held since Lowleaf — legal under §0
   rule 1: Stone grants no Gift) to the **vigil-lamp chamber** at mid-depth, through the
   top-of-band galleries (24–27) and **two gallery-miner sight trainers** (lv 24–26) —
   the §4 gap-closer is now the *mandatory* pre-battle leg, not optional grind;
   (5) **carry the lamp up still lit** (`script.take_vigil_lamp` →
   `flag:q_east_vigil_lamp`) — the vigil relights around it, lamps rising one by one;
   (6) the **Stone Gleam** wall battle against Otho (ace ~28, now met at ~26–27);
   (7) onward: the Deep again, this time crossing to its far side for Galehigh and the
   shortcut. *(Note: `to_deep` is **Glimmerstep-gated, full stop** — `graph.ts:128`. An
   earlier draft said it "opens on the win"; the graph is canon.)*
2. **Story beats** — **Arc E (Lamp-down vigil):** the most *melancholy* festival — miners dim
   their lamps together to honour the dark they work in, a quiet counterpoint to the Hollowing's
   argument (the town tends the dark *and* keeps its own light; it does not surrender to it).
   Otho embodies it: gruff, fair, "trusts what endures the dark." No new B-arc beat here — B2
   already landed at Glowmoss Deep; Cinderhead is the *consequence* (the wall) and the festival.
   *Samples* —
   - Otho Grist (pre-battle): "Down here, light's not given. It's *kept*. Show me you can hold
     yours when the rock leans in — then we'll talk about a Gleam."
   - Vigil elder: "We lower the lamps so we remember why we carry them. Then we light them again.
     That's the whole of it."
3. **Mechanic introductions** — **Stone bulk / strategy** — Otho is the first wall that punishes
   a glass-cannon team (high def/hp Stone kin; status/chip matters — the spine §5 status engine
   is assumed live by now). Reinforces **deep-cave navigation** (the Deep). The mine teaches the
   player to *prepare* before a Lumenary: catch, kindle, grind the deep galleries to close the gap.
4. **Optional content** —
   - **Cinderhead Deep** (`cinderhead_deep`) — **[MUST-DO]** for progress (the route on to
     Galehigh and the shortcut), gated by **Glimmerstep**.
   - **Crystoll Vault** (`crystoll_vault`) — spur off Cinderhead Deep, **[LATER]** — needs
     **Starreach**, the *endgame* Gift (earned at Nightreach, West). A very-late backtrack for a
     rare **Stone/Light** kin (atlas §3). Tease it (a void-gap you can't cross, signed) so the
     come-back is explicit.
   - A high-band crystal item in a deep gallery (deliberate grind reward to help beat Otho) —
     **[MISSABLE]**.
   - **Lamplight reveals (far galleries)** — `[LATER: Lamplight ≥ Starlight]` `[MISSABLE]`:
     the mine is first walked at **Warmlight**, so its far galleries and a late alcove sit beyond
     the lamp's reach; a brighter return (Starlight/Radiant, post-Gleam-6+ or post-game) lights
     them and their optional catches (spine §5). The crystal-vein-lit main route stays visible at
     any tier — additive only, never a gate.

   **Named quests** (spine §5 kit):
   - **E3 "The Foreman's Ledger"** — giver: the **lone miner** by the sealed shortcut door ·
     steps: recover the old crew's ledger from a side gallery in Cinderhead Deep → bring it
     back · flags: `flag:q_east_ledger` → `flag:q_east_ledger_found` · reward: a high-band
     **crystal item** (folds in the existing grind-reward bullet) · maps: `cinderhead_mine`,
     `cinderhead_deep` · `[MISSABLE]`; the ledger's last page hints at the far galleries —
     a second page sits beyond the lamp's reach `[LATER: Lamplight ≥ Starlight]`.
   - **E1 "The Quiet Reeds"** — see Saltreach Fen II's Named-quests entry (giver lives
     there); listed here for the regional slate count (E1 · E2 · E3 · R3).
5. **Don't-miss callouts** — **Grind the deep galleries before Otho.** The wall is intentional;
   the deep encounters (24–27) are how you beat it. Also: a **Glowpan** (Light) caught in the
   mine is a clean answer to the Stone/Dark threats of the deeper game. And on the Deep's far
   side, **open the mine shortcut** (below) — it makes every future hub trip from the east trivial.
6. **Validation hooks**
   - map id `cinderhead_mine`, kind `cave` (town/mine mouth); interior `cinderhead_lumenary`.
   - warps: `to_mine` land-in (paired with Glowmoss Deep); **`to_deep` → `cinderhead_deep`,
     `requires_ability: 'glimmerstep'`** (graph.ts:128); Lumenary door warp (no Gift gate).
   - triggers / flags: Stone-Gleam cutscene at the Lumenary **`sets_flags:['gleam:stone']`**
     — this is the **second** quadrant Gleam, so the engine now derives **`flag:crown_east`**
     (do not hand-set it). Lamp-down vigil cutscene (`once:true`, festival NPCs flag-gated).
   - **The Descent Vigil chain (rule 3):** `script.otho_quest` sets `flag:q_east_vigil`;
     the vigil-lamp chamber script in `cinderhead_deep` (`script.take_vigil_lamp`) sets
     `flag:q_east_vigil_lamp`; the vigil-relight cutscene + Otho's bond-test trigger
     `requires_flag:flag:q_east_vigil_lamp` with `blocked_ref:npc.otho_not_ready` consume
     it. Two **gallery-miner sight trainers** (lv 24–26) in the Deep on the chamber leg.
   - Lumenary battle: **Otho Grist**, Stone, ace ~28 (the wall); trainer entry + `dialogue_ref`.
   - encounter zones: `cave` — **Gravelo** (Stone), **Sparkrat** (Stone/Storm), **Glowpan**
     (Light) (atlas card 5); mine-mouth band **22–24**; rate ~0.12.

---

### Cinderhead Deep — *the deep galleries; the road on, and the shortcut home*

**At a glance** — `cinderhead_deep` · deep cave · east · enter from Cinderhead Mine
(`to_deep`, **Glimmerstep**) / exit to Galehigh Terraces (`to_terraces`, ungated → North) ·
spur: Crystoll Vault (`[LATER]`, Starreach) · sets **`flag:shortcut_mine`** · Gleam: none ·
rec. level ~24–27 (top of band).

1. **Main path** — The deepest, darkest galleries — Glimmerstep mandatory, encounters at the
   region's ceiling. Branchy cave layout (chokes, cart-rail rooms). Beats: (1) descend from the
   mine mouth into the high-band galleries; (1b) **the vigil-lamp chamber** at mid-depth,
   *before* the far-side door — the Descent Vigil's turnaround (see Cinderhead Mine §1:
   `script.take_vigil_lamp` → `flag:q_east_vigil_lamp`; two gallery-miner sight trainers
   hold the leg, and the first visit ends here, carrying the lamp back up to Otho);
   (2) cross a deep cavern with
   the Crystoll void-gap tease; (3) reach the **far side** — a sealed mine door; (4) **open it
   from the inside**, setting **`flag:shortcut_mine`** (the Cinderhead Deep → Vesper Crossroads
   re-link, spine §0 rule 3); (5) the gallery out to the **Galehigh Terraces** (the East→North
   boundary, **ungated** — the player simply walks on with Tidecall + Glimmerstep in hand).
2. **Story beats** — No new arc beat; this is the *traversal* payoff. The far-side door opening is
   a small, satisfying "I've connected the world" moment (the mine now feeds straight to the hub).
   Optional flavour: a lone miner near the sealed door who's "been meaning to clear it for years."
3. **Mechanic introductions** — Pure **deep-cave navigation** + the **late-shortcut pattern**
   (a one-way-feeling seal opened from the far side that permanently re-links to the hub). No new
   Gift. This is also where the spine §5 *exploration widens* note bites: with the shortcut set,
   the east hub trip collapses.
4. **Optional content** —
   - **Crystoll Vault** (`crystoll_vault`) — spur, **[LATER]** (needs **Starreach**, endgame).
     Rare **Stone/Light** kin (atlas §3). Frame the void-gap and sign it; the player will return
     after Nightreach.
   - The mine shortcut itself is **[MUST-DO]** to set on first reaching the far side (it's a
     forward beat, not optional content — but flag it so authors don't forget to wire the flag).
5. **Don't-miss callouts** — **Set the shortcut.** Reaching the far side must fire
   `flag:shortcut_mine`; missing it would leave the east permanently slow. And the Crystoll
   `[LATER]` tease — note it on your mental backtrack list for the Starreach run.
6. **Validation hooks**
   - map id `cinderhead_deep`, kind `cave`; entry paired with Cinderhead Mine `to_deep`
     (**`requires_ability: 'glimmerstep'`**, graph.ts:128); exit **`to_terraces` →
     `galehigh_terraces`** (graph.ts:129, **ungated** — the East→North handoff).
   - **far-side trigger:** `kind:'script'`, `once:true`, **`sets_flags:['flag:shortcut_mine']`**
     — this realises the shortcut edge **`cinderhead_deep → vesper_crossroads via shortcut_crossroads
     requires_flag:'flag:shortcut_mine'`** (graph.ts:167).
   - spur edge **`cinderhead_deep → crystoll_vault requires_ability: 'starreach'`**
     (graph.ts:148) — warp `to_crystoll`; tag **[LATER]** (Starreach earned at Nightreach, West —
     closes the spine §5 Starreach back-reference for Crystoll Vault).
   - encounter zones: `cave` — **Gravelo** (Stone), **Sparkrat** (Stone/Storm), **Glowpan**
     (Light) (atlas card 5); deep band **24–27** (top of band, §4 — the grind that beats Otho);
     rate ~0.13. `crystoll_vault` (post-Starreach): low-weight rare **Stone/Light**.

---

## Region exit checklist (handoff to North)

A player leaving East via `cinderhead_deep → galehigh_terraces` should hold:

- **Levels** ~lv28 (deep galleries grind ~24–27; party ~28 entering Galehigh — matches §4).
- **Lantern Gifts:** **Tidecall** (from South) **+ Glimmerstep** (Lowleaf).
- **Gleams:** `gleam:ember`, `gleam:tide` (South) **+ `gleam:verdant`** (Sable Quill) **+
  `gleam:stone`** (Otho Grist) → engine-derived **`flag:crown_east`** is now set.
- **Flags:** `flag:met_hollowing` (Glowmoss Deep), **`flag:shortcut_mine`** (Cinderhead Deep
  far side); `flag:crown_south` + `flag:crown_east` both held (the hub's south + east Spire
  approaches now armed — but the Spire stays sealed until all four `crown_*`).
- **Arc state delivered:** B2 done (Hollowing + Còr foreshadow seen); A3 done (Wren shaken);
  E festivals (Glowmoss Bloom, Lamp-down vigil) staged. **Not yet:** `flag:met_cor` (North,
  B3) and `flag:met_cor`'s in-person Còr scene are the North writer's; do not pre-empt them.
- **Mapwide "now accessible" still open as backtrack bait:** Tideglass Cavern (South, Glimmerstep
  — reachable now), Spore Grotto (here, Glimmerstep); Crystoll Vault flagged **[LATER]** for the
  Starreach return.

**Cross-region courtesies:** East does **not** introduce Fenn (Arc C), Còr in person (B3), or any
North/West content. The only edges East owns and gates are listed in the per-area Validation
hooks; the East→North boundary (`to_terraces`) is intentionally **ungated** so the curve crosses
cleanly with no level or Gift cliff.
