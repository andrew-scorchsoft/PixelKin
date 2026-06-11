# PixelKin — Scale-Out Readiness Review (2026-06, re-convened panel)

> The question this review answers, put by production: **"We set out to get the
> first hour right before building anything else. Is the first hour — and the
> system that produced it — now good enough that we can author the remaining
> regions to the same standard? Or do we refine further first?"**
>
> This re-convenes the two prior panels (`first-hour-expert-panel.md`,
> `full-game-expert-panel.md`). The full-game audit issued a **conditional
> green light** gated on four engine P0s; this review verifies, **in code and
> with every gate re-run live**, whether those conditions are met and whether
> anything new blocks the scale-out. Findings keep the established tags:
> **[DESIGN]**, **[BUILD GAP]**, **[PROCESS]**. All panelist personas are
> original, described by craft and era per `VISION.md`.

---

## Live evidence (re-run on this tree, 2026-06-11)

Every gate the project binds itself to was re-run for this review:

| Gate | Result |
|---|---|
| `tsc --noEmit` | clean |
| `validate.mjs` | 159 species, **0 errors / 0 warnings** |
| `chart_check.mjs` | all 10 types **47.8–53.2%** (45–55 guardrail) |
| `simulate.mjs` | **no gate failures**; one waived utility-kit outlier (Wisprestored, documented) |
| `progression.mjs` | **PASS** — curve continuous, all wallets solvent, payouts on formula |
| `audit_region.py` | **PASS** — 19 authored maps, 54 graph edges all backed; 2 forward topology notes on *unbuilt* regions (central, west — corridors until their late re-links are authored) |
| `audit_flow.py` (per map) | **PASS on all 19 maps**, 0 failures |
| `audit_warps.py` | **PASS** — 0 failures; 5 minor open-edge border notes (future spokes); 12 *intentional* inert teases |

The acceptance machinery is not aspirational: it runs, it bites (CI is
binding), and the shipped content passes it.

---

## Executive verdict

**GREEN LIGHT TO SCALE — after one region-sized condition: finish South to
South's own acceptance spec first.**

The prior audit's blocker was the **engine**. That condition is now met — all
four P0s (and both P1 engine items) are verifiably closed in code (Part 1).
The map production line is proven across every pattern the world needs (town,
route, tower, multi-floor cave, multi-room interiors), and the audit stack
catches real bugs before a human ever walks the map.

What remains is **content, and it is concentrated in one place**: the second
half of South. The Tinderwick→Beacon arc (~the true first 50 minutes) is built
to standard and the panel signs it off as *representative*. But the Pearlmoor /
Tide Gleam half is built **below the bar the project set for itself** — the
Gleam hands over flat against the spine's own binding "earned loop" rule, and
the side-quest layer the spine mandates for every region exists nowhere yet.

That matters more than its size suggests, because **South is the template**.
Every later region will be authored by copying the worked example. A worked
example that ships 60% of its own spec quietly re-baselines the standard for
the next seven regions — exactly the magnification risk this "first hour
first" strategy was designed to prevent. Close the gap (roughly one focused
sprint), and the scale-out becomes a production schedule with no open design
risks.

| Pillar | 2026-06 verdict |
|---|---|
| Engine (battle, statuses, kindling, dex, AI, saves) | ✅ Ready — all prior P0s closed in code |
| Map/level pipeline + audit stack | ✅ Ready — every map pattern proven, gates PASS |
| Balance, economy, level curve | ✅ Ready — re-validated live |
| Storytelling & cinematic toolkit | ✅ Ready — first hour is the worked example |
| First ~50 minutes (Tinderwick→Ember Gleam) | ✅ To standard — sign-off |
| South's second Gleam (Pearlmoor) | ⚠️ Below its own spec — finish before scaling |
| Side-quest layer (spine: 3+ per region) | ⚠️ Unbuilt anywhere — prove the kit in South |

---

## Part 1 — The conditions are met: prior P0/P1 closures, verified in code

The full-game panel's engine sprint was executed essentially in full. Each
item was re-verified against the current tree, not taken from notes:

1. **Status conditions are real. [CLOSED]** All seven canon statuses run in
   `BattleEngine.ts` — pre-move gates (doze turns, chill thaw-roll, numb/drench
   skip-chance, dazzle self-hit), end-of-turn chip (scorch 1/16; blight
   escalating stacks), stat hooks, cures, screens, caltrops, flinch, pivot,
   selfDoze. The catch `statusBonus` (×2.5 doze/chill, ×1.5 others) is applied
   in `catch.ts`. The sim was re-run post-change and passes.
2. **Kindling is live. [CLOSED — level/stone; bond pending]** `kindleReady()`
   fires on level-up, `KindlePrompt` stages the ceremony (accept / "cup the
   flame" defer, re-offer next level), kindling moves teach, `kindleByItem()`
   covers stone triggers. The **bond** path remains data-only (see Part 4).
3. **The Register (dex) exists. [CLOSED]** `RegisterMenu` (windowed list +
   detail, silhouettes until caught, SEEN/KEPT tallies), `SaveGame.dex` in
   schema v3 with a working v2→v3 migration, seen/caught tracked live in
   battle. The collection retention loop is in the game.
4. **Catch formula ↔ doc aligned. [CLOSED]** The quadratic four-shake check in
   `catch.ts` matches `04-capture.md`'s math and worked examples.
5. **Boss AI tier. [CLOSED]** `ai:'smart'` scores type matchups, finishes
   kills, uses the status kit contextually, heals low — wired on wardens.
6. **Gift-use flourish. [CLOSED]** `playGiftFlourish`: raise-lamp action +
   per-Gift tint + sfx + one diegetic line, once per Gift.
7. **CI gates. [CLOSED]** `.github/workflows/checks.yml` runs typecheck + all
   four balance validators on every PR; `chart_check`/`simulate` exit non-zero.
8. **The cave-dungeon pattern is proven. [CLOSED]** Glowmoss Deep + B1F ship as
   multi-floor blob-room caves through `finalize()`; the binding dungeon-scale
   ladder is documented and exercised.

Beyond the asked-for list, the system also grew: the QoL trio (pace,
text-speed, save glyph), the LORE glossary, the Wayfarer's Charts gallery, the
Hearth (real storage with overflow-on-catch), real walk-sheets and **all 159
kin packed in 5 views**, the interiors v2 standard, the retro-map research +
the executable §3a audits (`audit_flow`/`audit_region`), and the
satchel-errand opening. None of this existed at the last audit.

**Okafor (production):** "Last time I said 'don't author on top of a gap.'
The gaps are closed, and closed properly — with gates so they stay closed.
This is the part most teams never finish. The machine is ready."

---

## Part 2 — The first hour as played: the panel's experience read

The panel walked the built content beat-by-beat (cold open → satchel errand →
starter → verge catch → Brisa's errand → Dimglass I → `dusk_begins` → wick-key
→ beacon ascent → Ember Gleam → Lantern-fair), against the walkthrough as
acceptance spec.

**What the hour does at the level of the era's best:**

- **Onboarding is diegetic end-to-end.** The satchel errand replaces the
  classic tile-touch opening; the gate warden and `has_starter`-gated warps
  make pre-starter wandering safe *by construction*; the catch-first soft-gate
  teaches catching by making the warden ask for it. No tutorial popups
  anywhere in the hour. **Holloway:** "Every system is taught by an errand
  somebody in the world would actually run. That's the era's craft, done
  better than the era usually did it."
- **The difficulty curve is data-locked and modelled.** Starter 5 → wilds 3–6
  → Wren (friendly, 2-under, a teaching board for the triangle) → wilds 8–10 →
  stair trainers 7–8 → Brisa ace 10, and `progression.mjs` walks the whole
  journey with the engine's real formulas as a release gate. The genre's
  classic first-warden cliff is designed out, and the fix is *content*.
- **The level design is now audit-proven, not just well-intentioned.** Flow
  audits measure reachability, chokes, loops and dead-ends per map; the region
  audit checks topology, gate waves, and level-band cliffs; the warp audit
  enforces the landing conventions. On first run these caught four shipped
  bugs a mental walkthrough had missed. **Rell:** "I have never reviewed a
  hobby-scale project — and few shipped ones — where the route grammar is
  *executable*. The §3a rules aren't a style guide, they're a test suite."
- **The storytelling lands in the right register.** A 4-panel cold open behind
  the audio gate; the Hollowing seeded in three wordless touches before it is
  ever named; `dusk_begins` banded across the whole choke so it cannot be
  walked around; the Gleam ceremony's minor→major grammar (silence → tint →
  sfx → festival swell). All of it data, all of it on the cinematic toolkit —
  later regions inherit the staging for free.
- **Presentation sells the collecting pillar.** Real creature sprites in the
  first battle, portraits and expressions on the principals, SNES-register
  area music with the first-encounter maps already compliant, the full
  priority SFX set, the parallax attract duel, and the Charts gallery turning
  concept art into a collectible. The first battle makes a promise the rest of
  the roster can keep — all 159 are packed.

**Lindqvist (narrative):** "The hour has a face, a place, an omen, and a
payoff, in that order, and the payoff is *belonging* rather than victory. It
is the vision document, playable."

**Residual polish notes carried forward (none blocking):** F2 — the warm
Tinderwick thread before the omen exists (the house-parent beat) but is one
beat thinner than the panel wants; F8 — the full-hour **touch** playthrough
remains un-run as a QA pass; first-timer playtesting (real hands, no
designers) has still never happened and should be scheduled with the demo
boundary at the Ember Gleam.

---

## Part 3 — The gap: South's second Gleam is below South's own bar

This is the review's one substantive finding, and it was verified in code,
not inferred from docs.

**The Tide Gleam currently hands over flat. [BUILD GAP — the blocking one]**
The walkthrough's binding spec for Pearlmoor (01-south §"The Causeway Bell",
spine §5 shape #2) is: Reyl's hall sets `flag:q_south_bell` → the netmender's
net-floats cache on Dimglass II → the rope (`flag:q_south_has_rope`) gates the
**`pearlmoor_breakwater`** foot-causeway (2 net-hand sight trainers, lv 12–14)
→ `script.ring_moorbell` → *then* the bond-test, with the loop carrying the
player from 12 to ~13–14 against ace 16. What is built: Reyl is placed, his
ceremony script is excellent (the moor-bell narration, Tide Gleam + Tidecall
grant via `reward_abilities`) — but his battle trigger is gated only on
`flag:has_starter`. There is no breakwater map, no `script.reyl_quest`, no
`ring_moorbell`, and **no `q_*` flag anywhere in built content**. A player
walks off Dimglass II into the Lumenary and takes the second Gleam cold.

Three things break at once: the spine's binding "all 8 Gleams are EARNED via
varied loops" rule (locked 2026-06); the 12→16 level on-ramp the curve
expects; and prior finding F7 (the bell loop *is* the verb variation that
stops South's two loops reading as one trick twice). The walkthrough itself
flags these refs as "to add when built" — the spec is honest; the content is
simply not there yet.

**The side-quest layer exists nowhere. [BUILD GAP]** The spine requires 3+
named side quests per region; South's are fully specified (S1 "The Last Buoy
Out", S2 "A Letter for Fenn", S3, with flags, givers, rewards) and none are
built. This is also the first appearance of a *pattern* (quest-flag pair +
giver swap + reward) that every region will need — it should be proven once,
in the template region, before seven regions author it in parallel.

**The Tide-blessing is skeletal next to the Lantern-fair. [DESIGN — F5,
still open]** Both festivals' NPCs exist, but the second has no swell
cutscene, no distinct cue, no signature interaction (the bell — which the
unbuilt loop provides). South currently teaches "festival = a few flag-gated
townsfolk" the second time it shows one; the differentiation rule exists
precisely to prevent that.

**Why the panel rates this P0 for the scale-out, despite being "one map and
some scripts":** the magnification argument cuts both ways. The user's
strategy — perfect the first hour because its flaws multiply — has *worked*
for everything the first 50 minutes touch. But the template a region author
will copy is *all of South*, and right now the template demonstrates a flat
Gleam and zero side quests. Finish the worked example to its own spec and the
standard that propagates is the right one.

---

## Part 4 — Small engine/process items to slot before parallelising

None of these block finishing South; all are cheaper now than after eight
regions of content assume them.

1. **Bond/affection. [BUILD GAP]** Species data already carries bond kindling
   triggers (the Hearthkit line, in the player's first-hour catch pool);
   `KinInstance` tracks no bond value and the save has no field. Add the field
   to `KinInstanceData` + save *now* (dormant, avoids a v4 migration later) and
   wire the bond-kindle check before any region whose content leans on it.
2. **Charge condition hook. [BUILD GAP]** `04-capture.md` specifies
   conditional charges (time-of-night, HP-threshold, terrain); the engine
   applies only `catch_bonus` unconditionally. Today's shipped charges are all
   unconditional, so nothing is wrong *yet* — build the condition check before
   the first conditional charge is authored, or it will silently apply always.
3. **Touch QA pass. [PROCESS — F8]** One full first-hour playthrough on the
   touch shell, checking every verb (sign-interact, catch, menus, cutscene
   skip, the new Register/LORE/Charts screens). The architecture is right;
   nobody has walked it.
4. **Lamplight mask decision point. [DESIGN — unchanged]** Still additive-only
   by rule and correctly unbuilt; the decision lands when East needs to *feel*
   dark. The glossary already pre-seeds the framing line (F6).
5. **Process disciplines to keep binding. [PROCESS]** Append-only shared
   tileset ordering; the three-way economy mirror sync; signature moves
   excluded from generic pools; the walkthrough validation hooks as per-region
   acceptance. All already documented — this is a reminder that they are the
   reason the gates stay green at scale.

---

## Part 5 — Recommendation: the Finish-South sprint, then crack on

**Do not broaden the polish.** The panel found no design-level rework anywhere
— not in mechanics, balance, economy, story, level grammar, or pipeline. More
generalised "refinement" of the first 50 minutes would now be sanding paint.
The remaining work is a *specific, listable completion* of the template
region, roughly one focused sprint:

1. **Build the Causeway Bell loop** — `pearlmoor_breakwater` (route/causeway,
   ~12×28, on foot, 2 sight trainers), `script.reyl_quest` /
   `script.ring_moorbell`, the net-floats cache on Dimglass II, the netmender
   swap, and re-gate Reyl's bond-test on `flag:q_south_bell_rung`. Re-run
   `progression.mjs` (the 12→16 on-ramp) + the full audit stack. *Closes F7.*
2. **Build South's three named side quests (S1–S3)** to the walkthrough spec —
   this proves the side-quest kit (flag pair + giver swap + reward) every
   later region copies. *Establishes the missing per-region pattern.*
3. **Stage the Tide-blessing properly** — its own cue (cool, open,
   moon-on-water vs the fair's warm amber), the bell as its signature
   interaction, a short swell script on `gleam:tide`. *Closes F5.*
4. **One warm Tinderwick beat pre-omen** — deepen the house-parent thread by a
   single scene so `dusk_begins` threatens a face, not a town name. *Closes F2.*
5. **Engine half-day:** bond field in the save (dormant) + the charge
   condition hook. *(Part 4, items 1–2.)*
6. **QA:** the full touch playthrough, and the project's **first true
   first-timer playtest** with the demo cut at the Ember Gleam (the panel
   re-affirms that boundary as the official "first hour").

**Then scale, without further gatekeeping:** East's opening (Saltreach Fen II
→ Lowleaf, where level-kindling debuts on content that already works) → the
remaining regions in walkthrough order, each authored against its validation
hooks with CI and the audit stack as the per-map acceptance test. At that
point the panel's answer to "good to go?" is an **unconditional yes** — the
risk left in this project is schedule, not design.

### What the panel explicitly re-affirms NOT to change

The 10-type chart and mirror axes; the roster and EPS budget; the catch math;
the wick economy and its binding model; the story, arcs, Gleam cadence and
gating order; the canon vocabulary; maps-as-JSON and the data-driven
architecture; the audit-gated map pipeline. All re-validated live this
review. Touch them only through the pipeline + validators.

---

## Findings at a glance

| # | Finding | Tag | Priority |
|---|---------|-----|----------|
| G1 | Build the Causeway Bell earned loop (breakwater + quest chain); re-gate Reyl | BUILD GAP | **P0 (pre-scale)** |
| G2 | Build South's three named side quests — prove the per-region kit | BUILD GAP | **P0 (pre-scale)** |
| G3 | Differentiate + stage the Tide-blessing festival | DESIGN | P1 |
| G4 | One warm pre-omen Tinderwick beat (carried F2) | DESIGN | P1 |
| G5 | Bond field in save now; bond-kindle check before content assumes it | BUILD GAP | P1 |
| G6 | Charge condition hook before first conditional charge ships | BUILD GAP | P1 |
| G7 | Full first-hour touch playthrough (carried F8) | PROCESS | P1 |
| G8 | First-timer playtest, demo cut at the Ember Gleam | PROCESS | P1 |
| G9 | Lamplight mask decision at East; Sunsketch blooms ticket for West | DESIGN | P2 |

**One-line summary:** *The machine that makes the game is ready — engine
closed, pipeline proven, gates green — and the first 50 minutes meets the bar
it was built to set. Finish the template region to its own written spec
(Pearlmoor's earned loop, the side-quest layer, the second festival — about a
sprint), then build the rest of the game at full speed.*

*Prepared by the re-convened joint panel. Every gate re-run live on this
tree; every prior finding re-verified in code. No recommendation herein
requires a canon change.*
