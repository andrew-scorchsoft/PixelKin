# PixelKin — Full-Game Expert Panel Audit (2026-06)

> A convened review of the **whole game**: vision, story, world structure, the
> walkthrough blueprint, mechanics & balance, the wick economy, the map/level
> pipeline, the built South region, and the engine — judged against one
> question: **is PixelKin ready to spin out the remaining regions and finish
> the game, or should anything change first?**
>
> **Scope reviewed:** `VISION.md`, `docs/world/` (story-bible, atlas, the full
> walkthrough spine + all region files, level-design, interiors, cinematics),
> `docs/mechanics/00–10` + `balance-report.md` + `battle-runtime-plan.md`, the
> full `src/game/` engine (scenes, systems, ui, content, data), all 15 built
> maps + `tools/maps/`, and `tools/balance/` — with every validator **re-run
> live** on the current tree (post the 159-roster register merge):
> `validate.mjs` (159 species, 0 errors / 0 warnings), `chart_check.mjs`
> (all 10 types 47.8–53.2%), `simulate.mjs` (no within-tier outliers),
> `progression.mjs` (PASS — curve continuous, wallet solvent), `tsc` (clean).
>
> Findings are tagged **[DESIGN]** (a call on the blueprint), **[BUILD GAP]**
> (the spec assumes something the engine doesn't do yet), or **[PROCESS]**
> (discipline/tooling). Same convention as the first-hour panel review.

---

## The panel

Five veterans of the cartridge-and-disc era, convened for their scar tissue:

- **Mara Voss** — lead designer on two 8-bit handheld creature-collecting
  RPGs; owns the catch loop, the collection drive, and "why players keep
  playing after the credits."
- **Tomas Rell** — overworld/route designer from the 16-bit-handheld golden
  age; owns map grammar, gating, route pacing, and dungeon shape.
- **Dr. Imogen Hale** — battle-systems designer from the 32-bit JRPG era;
  owns the turn engine, status depth, boss AI, and difficulty curves.
- **Petra Lindqvist** — narrative designer of cosy-melancholy handheld
  adventures; owns tone, arc delivery, and "does the ending land."
- **Saul Okafor** — production lead on three retro revivals; owns the
  pipeline, the schedule, and "what breaks at scale."

---

## Executive verdict

**CONDITIONAL GREEN LIGHT.** The panel's unanimous view: the *design* is
finished and unusually good — the canon, the balance, the economy, the story
blueprint, and the map pipeline are all proven, validated, and ready to
scale. **Do not change the game's design, story, progression, or economy.**

But **do not mass-produce the remaining regions yet.** The engine has **four
gaps** that every later region's content will be authored *on top of* — and
authoring on top of a gap multiplies the cost of closing it later. Close the
P0 list first (~2–3 weeks of engine work), prove one unproven map pattern
with East's first dungeon, then spin out the world at full speed.

| Pillar | Verdict |
|---|---|
| Vision & originality | ✅ Ship it — discipline is exemplary |
| Story / arcs / walkthrough | ✅ Ship it — execution-discipline notes only |
| Type system / roster / balance | ✅ Ship it — empirically validated, re-run live |
| Economy & level curve | ✅ Ship it — keep the model as a release gate |
| Map pipeline & built maps | ✅ Ship it — one pattern (cave dungeon) still unproven |
| Engine | ⚠️ Four P0 gaps before content scale-out |

---

## What the panel found genuinely excellent

**Voss (collection):** "The roster work is the best I've audited. 159 kin,
every line whole, every starter now a true three-stage line, a shared
125-move pool with full physical/special ladders per type, and — this is the
rare part — *empirical* balance: every type lands 47.8–53.2% in fair fights,
no species sits more than 18pp from its tier mean, and the validators fail
loudly. Most teams *claim* this; this repo *proves* it on every run. The
catch-rate bands (A 190–235 down to F 3–10) produce exactly the right feel
per tier."

**Rell (world):** "The walkthrough is an acceptance spec, not a wish list —
14 areas, 8 earned Gleams with a *binding variation table* so no two Gleam
loops share a shape, 6 Lantern Gifts on a clean gate cadence, per-region
validation hooks down to flag names and encounter bands. And the map pipeline
is turnkey: `mapkit.finalize()` runs autotile → render → validate →
warp-audit in one call, terrain is *drawn in code* to a stable GBA register,
and the 15 built maps actually follow the binding composition rules. The
marginal cost of a map is a known quantity (~4–7 focused hours). That's a
production line, not a pile of hand-crafted one-offs."

**Hale (systems):** "The battle maths is genre-correct and matches the docs
line for line — damage, STAB 1.5, crit 1/16×1.5, stat stages ±6, priority,
flee odds, the lot. The economy is the standout: `progression.mjs` walks the
whole journey with the engine's real formulas across three player profiles
and binds region authors to a solvency contract. The numbers match the
narrative."

**Lindqvist (story):** "The Long Dusk is a real premise, not a reskin. The
light-as-progress metaphor is load-bearing across four axes at once (Gleams
in the sky, Gift gates, Lamplight radius, the world literally warming). The
Hollowing is the rare sympathetic antagonist that actually argues its case,
and the climax — out-*remember* Còr, don't out-hit him — is the bravest call
in the design. The festivals reframe badges as belonging. None of this drifts
within a mile of another franchise; the originality rules are kept."

**Okafor (production):** "Save system is versioned with working migrations,
content is data all the way down (a new area is JSON + registry entries, no
engine code), the cutscene toolkit covers everything the story needs and
degrades silently when assets are missing, and the register merge just
shipped packed sprites for the *entire* roster. The foundation scales."

---

## P0 — Close these BEFORE spinning out the remaining regions

### 1. Kindling never happens in gameplay — [BUILD GAP], the big one

**Voss:** "This is the genre's core promise after catching: *your kin grows
up*. The data is complete — all 159 species carry `kindling` triggers (level,
bond, stone, location, time, linked), lines are validated whole — and the
engine consumes **none of it**. `KinInstance.gainExp()` learns moves but
never checks a kindling threshold; there is no prompt, no animation, no
script op. Vulpyre hits 16 and… nothing. The walkthrough says the starter's
first kindle lands in Lowleaf (East) — the *next* region to be built. You
cannot author East without this."

**Do:** wire a kindling check into the level-up flow (return
`pending_kindling` alongside pending moves), add a KindlingPrompt + a short
ceremony animation (the canon says a kindle is a *minor Gleam moment* — stage
it with the existing tint/sting primitives), teach kindling moves, and add a
cancel/defer (hold-B convention) plus Kindlestone/bond paths for the
non-level triggers used by lines South already hands the player. ~2–3 days.

### 2. Status conditions are narration-only — [BUILD GAP]

**Hale:** "`BattleEngine` applies stat stages correctly but statuses are
explicitly out of scope — Scorch deals no chip, Doze skips no turns, Numb
cuts no speed, and the catch `statusBonus` the capture doc promises is never
applied. Two reasons this can't wait until after the content push: (a)
**Light's identity depends on it** — Light sims at 40.6% same-tier precisely
because its kit is status/utility the sim and the engine can't see; (b) eight
regions of trainer movesets are about to be authored, and they'll be authored
*assuming statuses work*. Author them on a stub and you'll re-balance every
region later."

**Do:** ship Part B of `docs/mechanics/battle-runtime-plan.md` (pre-move
gates, end-of-turn chip, stat hooks, cures, catch bonus) — the plan already
exists and is well-sequenced. Then **re-run `simulate.mjs`** and re-check
Light. ~3–4 days. While in there, decide the fate of the other documented
move effects (drain / recoil / flinch / multi-hit / heal): the pool's
Desperate-tier moves carry recoil riders *in data*, so either implement the
small set with Part B or strip the riders so the dex never promises what a
battle doesn't do.

### 3. There is no dex / collection screen — [BUILD GAP]

**Voss:** "A collect-a-thon with no way to see the collection. No seen/caught
tracking, no browsable register, no completion count. This is the retention
engine of the genre and it's absent — and it's now *cheap*, because the
register merge packed sprites and a manifest for the whole roster. It also
needs a save field, so do it before save data ossifies across testers."

**Do:** a VESPERLAMP/REGISTER entry in the pause menu — windowed list +
detail pane (the `StarterSelect`/`GlossaryMenu` pattern already in the UI
kit): dex number, name, types, icon/front sprite, entry text, line view,
seen/caught counts. Track `seen`/`caught` sets in the save (schema v3 + one
migration). ~2 days. **[DESIGN]** note: keep it diegetic — it's the
vesperlamp's register, kept with the Hearthkeeper's blessing, not a
spreadsheet.

### 4. The catch formula contradicts its own doc — [PROCESS]

**Voss:** "`catch.ts` implements the classic quadratic shake-check;
`docs/mechanics/04-capture.md` documents a simple linear roll with a status
multiplier. Both are defensible designs — but the worked examples, the
catch-rate bands, and the Tide Charm tuning were costed against *one* of
them. Pick one (the panel leans **keep the quadratic** — the wobble drama is
beloved for a reason and the bands were validated against it), rewrite the
doc to match, and wire `statusBonus` in with Part B." ~half a day.

---

## P1 — Prove these early in the scale-out (East is the proving ground)

### 5. The cave-dungeon pattern is unproven — [BUILD GAP]

**Rell:** "South proved towns, routes, interiors, and a vertical tower. It
did **not** prove a branchy multi-room cave — and East opens with two
(Glowmoss Deep, Cinderhead Mine), the walkthrough's first Hollowing set-piece
included. Build **Glowmoss Deep first**, before parallelising East: it
exercises dark-room presentation (Glimmerstep), choke-room composition, the
drained-kin centrepiece, and the interior register at dungeon scale. If it
passes `finalize()` + a manual run, the remaining ~32 maps are a production
schedule, not a risk."

Related: the **Lamplight radial mask** (spine §5) is designed-not-built. It's
additive-only by rule, so don't block on it — author dark-area reveals as
flag-gated alcoves now (the documented fallback) and ship the mask when East
needs to *feel* dark. **Sunsketch's timed blooms** (West) are flagged "small
addition" — file the engine ticket now, build West's chained-`AbilityGate`
version regardless.

### 6. Wardens need a boss-AI tier — [DESIGN→BUILD]

**Hale:** "The foe AI is max-expected-damage with a 20% wobble and
status-moves-as-last-resort. For routes that's period-correct and fine. For
the eight Wardens and Còr it's exploitable — a player who's noticed the
pattern stalls them with stat drops and switches. Add an `ai: 'smart'` flag
on `TrainerDef`: type-matchup awareness, use the status kit Part B just made
real, and a 'heal/priority when low' check. One day of work, and the late
aces stop being free."

### 7. Lantern Gifts need their *moment* — [DESIGN]

**Lindqvist:** "The gates work mechanically (collision honours abilities),
but earning a Gift is a story beat and *using* it is silent — you just walk
onto water. The genre's field moves always had a beat of ceremony. Give each
Gift a two-second diegetic flourish on first-blocked-tile use — raise-lamp
action frame (the action sheet already exists), a tint, the sfx. Pure
polish, big feel. Do it once, data-drive it per Gift."

### 8. Region tilesets are the real schedule item — [PROCESS]

**Okafor:** "East glowmoss/marsh, North storm/ice, West sun-garden/coldfog —
none exist yet, and every one is a `gbaforge` family + shared-set append +
object gens. Budget tileset week *per region pair* ahead of map authoring,
and keep the append-only ordering rule so existing maps never reflow."

---

## P2 — Worth doing, not blocking

- **[PROCESS] CI the gates.** `validate.mjs` + `simulate.mjs` +
  `progression.mjs` + per-map `finalize()` checks should run on every PR —
  the economy contract only protects you if it's impossible to forget.
- **[BUILD GAP] Preload review at 159.** Featured-preload + lazy-load is
  fine, but batch-preload a region's encounter table on map entry so a first
  wild battle never hitches.
- **[DESIGN] QoL trio:** persistent run toggle, text-speed setting, a quiet
  autosave glyph. Period-authentic games lacked them; period-authentic
  *revivals* don't.
- **[PROCESS] Story-discipline checklist** (from the narrative read; the
  blueprint is sound, these are execution risks for region authors):
  - The Còr climax is **out-remember, not out-fight** — stage per
    `05-central-endgame.md` §2, never as a boss spectacle.
  - The Fenn–Còr shared past lands **once**, on the North ice (C3) — it is
    the climax's only foundation; don't soften it.
  - **Pin Wren's A5 beat to a named map** in West (Nightreach or the
    Crossroads) — it's currently the one arc beat without an address.
  - Festivals are **binding Arc E beats**, not décor — every Gleam gets its
    festival staging.
  - Signpost the Coldfog detour as the *wrong* way to Nightreach so
    first-timers take the Sunvault approach and the Great Null reveal lands
    at the telescope.

---

## What the panel explicitly recommends NOT changing

- **The 10-type chart, the mirror axes, the EPS budget, the roster.** It's
  balanced, it's validated, and the 2026-06 register update (three-stage
  starters + apex kindlings, 159 total) closed the panel's only roster note
  before it was raised. Touch it only through the pipeline + validators.
- **The 4-move cap and last-4-learned rule.** A deliberate, period-correct
  clarity trade; Star-charts already provide the override valve.
- **The economy.** Solvent across all three player profiles to the climax;
  the faint tithe is gentle and diegetic. Keep the model binding.
- **The story, the arcs, the Gleam cadence, the gating order.** The
  blueprint is the strongest artefact in the repo.
- **The web-first/data-driven architecture.** Maps-as-JSON, content-as-data,
  the platform seam, the theme-driven UI kit — all pulling their weight.

---

## Sequenced recommendation

1. **Engine sprint (~2–3 weeks, before or alongside East tilesets):**
   kindling flow → status Part B (+ re-sim, re-check Light) → dex/register
   screen (+ save v3) → catch doc/code alignment → boss-AI tier → Gift-use
   flourish.
2. **Prove East's opening:** glowmoss/marsh tileset → **Glowmoss Deep**
   (the cave proof) → Saltreach Fen I → Lowleaf (where kindling debuts) —
   full `finalize()` + manual playthrough of the entry sequence.
3. **Then scale:** parallelise the remaining regions against the walkthrough
   hooks with CI running the validators. At that point the panel's answer to
   "good to go?" becomes an unconditional yes.

*Validator evidence (re-run on this tree, post-merge): 159 species, 0
errors/0 warnings; fair-fight type spread 47.8–53.2%; full-roster same-tier
spread 40.6–55.0% with no within-tier outliers; progression model PASS
(mainline within −1/+4 of every recommended level, all wallets solvent);
`tsc --noEmit` clean.*
