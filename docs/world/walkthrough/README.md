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

---

## 0. Three rules that prevent drift (read first)

These three were the highest-risk traps in the design audit. They are **binding** on every
region file:

1. **A Lumenary is never gated by the ability it grants.** The gate ability named for an area
   (atlas "Gate:" line) applies only to that area's **onward route-segment II and its
   spurs/depths — never to the town or Lumenary itself.** (Pale Vault's Lumenary grants
   Emberward, so it *must* be reachable without Emberward; Lowleaf's grants Glimmerstep; etc.)
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
   region introduces a shortcut/spur must set its flag.

> **Counts, reconciled (so the numbers don't trip you):** **9 valleys** (the lore framing) =
> 8 Lumenary towns + Dawnstead; **14 area cards** in `atlas.md` §2; **43 graph nodes** in
> `graph.ts` (the cards split into segments + spurs + landmarks + hub + central). All three
> describe the same world at different resolutions.

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
| 0 | Wayfaring begins — Star-tender **Fenn** gifts the vesperlamp + starter | Tinderwick | starter, vesperlamp | `flag:has_vesperlamp`, `flag:has_starter` |
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
| C1 Gift the lamp & starter | Tinderwick |
| C2 Explain the Skyweave & the winking-out | South (after `dusk_begins`) |
| C3 Reveal the shared past with Còr | North (around `met_cor`) |
| C4 Counsel before the Spire | Vesper Crossroads / Nightreach |

### Arc D — The Celestial Calendar (dusk → dawn)
The global lighting warms one quadrant at a time. **Each region file must open visibly
lighter than the previous region** (south = deep blue hour → west = near-dawn pallor), the
vesperlamp brighter, and note any flag-gated encounter-table shift when its constellation
relights. Day-forms arrive only post-`dawn` (see [`06-postgame.md`](./06-postgame.md)).

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
the mine or it becomes a cliff.

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
doze · blight · dazzle · chill`) and a **move-learning prompt** are live — both are on the
engine roadmap (`docs/mechanics/battle-runtime-plan.md`) but not yet wired. Region files may
write battles that *use* status (e.g. a Lampwarden built around `doze`), and should flag
where a beat depends on these so they're prioritised.

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
backtrack bait) → a **landmark micro-dungeon** → a **hub spoke**.

---

## 7. Per-area section template (the contract for region files)

**Every** area (including segments, spurs, landmarks) is written to this exact shape so it is
scannable and validatable:

```
### <Area name> — <one-line mood>
**At a glance** — map id(s) · kind · region · entry/exit · gate ability · Gleam · rec. level
1. **Main path** — ordered beats; one screen-decision per beat in spirit (per level-design §15×10)
2. **Story beats** — which arc beats (A1/B2/…) land here; 1–3 *signature* sample lines that set tone
3. **Mechanic introductions** — Gift earned / capture-or-kindling teaching / new terrain
4. **Optional content** — spurs · landmarks · hidden items, each tagged:
      [MUST-DO] don't-leave-without · [MISSABLE] easy to walk past · [LATER] needs a Gift you don't have yet (name it)
5. **Don't-miss callouts** — the exploration payoffs a first-timer shouldn't pass
6. **Validation hooks** — the data a built map MUST contain:
      - map id(s) and kind; entry/exit warp coords agreed with neighbours
      - key warps with their `requires_ability` / `requires_flag`
      - key triggers with their `sets_flags` (use the canon flag strings in §2)
      - encounter zones: terrain · element-matched kin (atlas) · level band (§4)
      - NPC / Lumenary / festival placements + dialogue/script refs
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
| **Fenn–Còr shared past** | Climax weight (Arc C) | ✅ **Now** — pure narrative; no mechanic |
| **Celestial calendar / day-forms** | Arc D payoff; post-game collecting | ⚠️ **Partial** — permanent "constellation relit" table swaps work via flag-gated `EncounterZone`s; true day/night *cycling* needs a small system → propose for post-MVP |
| **Vesperlamp brightness tiers** | Make Arc D legible (lamp brightens per Gleam) | ⚠️ Art/flavour now; a real map-light radius is a small render proposal |
| **Status conditions + move-learn prompt** | Mid-game battle depth (assumed from Pearlmoor on) | ⚠️ Already roadmapped (`battle-runtime-plan.md`) — flag as dependency, don't author around its absence |
| **Quest counters** (multi-step fetch/track beyond booleans) | A few side-quests want "3 of 3" state | ⚠️ Small `FlagStore` extension (shadow `Record<string,number>`); keep side-quests boolean-only for MVP |

**Canon extensions locked by this blueprint** (region files must use, consistently):
the rival is **Wren**; the mentor is **Star-tender Fenn**; **Fenn and Còr share a past as
star-tenders**; the eight **festivals** in §3 Arc E; the Keystar-kin is **Keylumen** (atlas).

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
