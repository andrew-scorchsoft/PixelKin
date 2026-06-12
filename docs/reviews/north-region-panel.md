# PixelKin — N6 Expert Panel: The North Region

> A convened, independent review of PixelKin's newly built **North quadrant**
> (commits `56ab29c..1de0a04`): Galehigh Terraces + Skyloft, Windward Stair I→II,
> Wind-Eye, Thunderroost, Pale Vault Glacier + Undercroft, six interiors, the N4
> content layer (scripts/dialogue/trainers/shop/items/glossary), the N5 encounter
> tables, and the crossroads spoke. Judged against the binding acceptance specs:
> `walkthrough/03-north.md` (every validation hook + staging direction + §10 voice),
> the spine README (§0 rules, per-region kit, §5 Gleam-variation table),
> `level-design.md` §2a/§2b/§3a/§11, `interiors.md`, `cinematics.md`,
> `story-bible.md` §7, `10-economy.md` §4, and the humour style sheet.

## The panel

| Panelist | Discipline | Watches for |
|----------|------------|-------------|
| **Devs "Dee" Okonkwo** | Level & world design | route flow, the backtrack web, "funnel with light" |
| **Tomás Reic** | Narrative & quest design | tone, reveal pacing, whether attachment lands before stakes |
| **Mara Holloway** | Systems & balance | level bands, payouts, encounter math the player *feels* |
| **Ivo Castellan** | Producer / first-time player | scope, vision-alignment, the moment-to-moment first hour |

## How it was run

Audit first (what genuinely works), then the contested calls, then a
severity-tagged ledger. Evidence was *gathered*, not assumed: all 8 outdoor/cave
maps + 2 interiors re-rendered and eyeballed; `audit_region` / `audit_flow` (all
8 maps) / `audit_warps` run and read critically; both marquee quest chains traced
flag-by-flag from setter to consumer across map JSON + TS; the B3→C3→A4 sequence
walked in the actual `pale_vault_glacier.json` geometry; every North script and
sign read as prose; `progression.mjs` + `validate.mjs` run for the balance verdict.

---

## Part 1 — The audit (what's working, keep it)

1. **The character-drama peak lands.** The B3 (Còr) / C3 (Fenn) / A4 (Wren) cluster
   is the best-written sequence in the game to date. Còr is genuinely persuasive —
   grief dressed as mercy, never cartoonish — and the writing *knows* it ("It would
   be easier if he were wrong in some plain, loud way"). Fenn's "out-remember him"
   answer is the canon-locked rebuttal delivered with restraint. Wren's wobble
   escalates the A2 friendly-battle into something that hurts. **Tomás:** "Three
   faces, one question, and the staging *is* the argument. This is the spine."

2. **Both earned loops are fully wired and un-sequence-breakable.** The Kite-Rising
   Winch (boolean cache chain → festival → winch warp) and the Lamp-Line (oil leg →
   seven chained brackets → bond-test) trace cleanly setter-to-consumer with zero
   dangling flags. The undercroft door (`q_north_aurora_oil`) and the Còr choke sit
   so that the player *must* meet Còr before lighting the line. **Dee:** "I tried to
   break the order on paper and couldn't. The choke does the work."

3. **The §0 traps were both avoided.** Pale Vault's town and Lumenary are reachable
   on foot from the crags — no Emberward gate, no coldfog barrier between the
   entrance and Ysolde (`to_glacier` and the Lumenary door are ungated). And
   `flag:shortcut_windward` is set on reaching the Windward II crags, closing the
   flag this region opens. Exactly to spec.

4. **The balance is on the curve, and the warden delta is *consistent*.**
   `progression.mjs` PASSES. Mira's ace 34 vs predicted L32 = +2; Ysolde's 40 vs L38
   = +2. Placed against precedent (Brisa −1, Reyl 0, Sable 0, Otho +1, Mira +2,
   Ysolde +2, Lucan +3, Nessa +4) the warden-over-player gap escalates *smoothly* —
   the brief's worry that +2 is "wrong" is unfounded; it's the right rung on the
   ladder. **Mara:** "The escalating delta is a feature. Don't touch it."

5. **Encounter math respects the forced path (§3a r12).** Verge/main grass bands sit
   at 0.11, the *mandatory crossing lanes* at 0.05–0.055 — half-rate on the tiles the
   player can't avoid. Reward spurs weight their prize kin correctly (Wind-Eye:
   Hailwhirr 50%; Thunderroost: Strikeaven the storm-bird as the 15% rare). Bands run
   continuous (28–30 → 34–36 → 36–40) and `audit_region` confirms every border steps ≤4.

6. **Humour is inside its sanctioned homes at the right ratio.** Sign text carries the
   load — the winch's "the children keep count," the stair's "412 steps down... asks
   that you not make him do it again," the wind that "takes nobody it has not been
   introduced to." Trainer defeats are good-loser energy (the cabbages "saw
   everything"). And the sacred beats are *clinically* clean: Còr, Fenn, Wren, the
   seven lamps, and the Aurora-watch carry zero humour — the dialogue header even
   states "ZERO humour past the inn." Calibration is a smile, not a laugh.

7. **The art reads, and the Arc-D lighting handover is felt.** Galehigh's cross-roads
   town (winch, kite-maker, terraced cliffs, last-fire sunset) → Windward's grey climb
   bleeding green-to-snow → Pale Vault's aurora-lit ice (blue-ice Lumenary, the
   undercroft arch, blue-flame braziers, ice crystals) is a genuine visual journey
   "out of the warm into the high blue." The undercroft's seven brackets descend in a
   readable zig-zag line through clear ice. **Junko (in absentia, via render):** the
   region is on-palette and on-register.

8. **`validate.mjs` clean (0/0 on 159 species) — the N5 encounter-sync didn't
   regress the roster.** The "built maps become species truth" pass is honest.

---

## Part 2 — Findings ledger

### BLOCKER
*(none)*

### MAJOR
*(none)*

### MINOR

- **MIN-1 — The two Lumenary interiors are near-identical copies.**
  *Evidence:* `/tmp/n6/galehigh_lumenary.png` vs `/tmp/n6/pale_vault_lumenary.png` —
  same cool-stone register, same focal altar, same aisle runner, braziers, bookcase,
  apothecary shelf, benches, round table; the *only* difference is one bottom-left prop
  cluster (crates/eggs vs jars). *Spec:* `interiors.md` (each Lumenary should carry its
  warden's register — Storm/airy vs Frost/icy). Both correctly use the cool-stone
  Lumenary register and the proper `aisle_runner` (not the ladder-look doormat), so
  this is identity, not composition. *Fix:* re-skin Pale Vault's hall to the icy
  register (swap the warm braziers for the blue-flame brazier object already used
  outdoors; cool the floor tint; an ice-crystal focal accent), and give Galehigh an
  airy touch (a hung kite or open shutter). One object-swap pass each, no re-layout.

- **MIN-2 — Windward Stair I is a 93-step single climb — the region's longest leg by
  more than double.** *Evidence:* `audit_region` travel line: `windward_stair_i ≈93
  steps` (next longest North leg is 37); `audit_flow` notes the ledge-hops cut it to 45
  "the long way / 48%". *Spec:* `level-design.md` §2b (return-compressor ladder; heal
  spacing ≈2 legs). The down-hops are good, but the *first up-climb* before Updraft
  pays off is a long unbroken grey corridor. *Fix:* the down-shortcut already exists;
  consider one mid-climb rest-ledge "beat" (a cache or a one-line crag NPC) at the ~45-step
  mark to break the monotony the render shows (three near-identical grey switchback
  tiers). Low cost; pure pacing.

- **MIN-3 — Galehigh→Windward I band step is the region's steepest.** *Evidence:*
  Galehigh grass 28–30 → Windward I grass 34–36; worst-case cell-to-cell is 30→36
  (+6). *Spec:* §2b "band steps ≤4 / `audit_region` ≤4 at borders." The audit PASSES
  because the player exits Galehigh post-Mira (~L31–32, the warden on-ramp absorbs it),
  so the *felt* step is +2–3. *Fix:* none strictly required (it passes), but if a
  future tune wants headroom, seed Windward I's first ledge at 32–34 so the literal
  border step is gentler for a player who skips the skyloft wards.

### POLISH

- **POL-1 — Wind-Eye's central void reads slightly large/empty.** *Evidence:*
  `/tmp/n6/wind_eye.png` — the dark "eye" oculus is the dominant feature and the
  walkable ring is thin. It works as a landmark motif, but a first-timer may read the
  black centre as "unfinished" rather than "the sky-grotto's eye." *Fix:* a faint
  star-shimmer or updraft-mote decal in the void sells it as *sky seen through the
  mountain* rather than absence. Optional.

- **POL-2 — `script.kettle_done` sets `flag:q_north_kettle` again redundantly.**
  *Evidence:* `scripts.ts:1302–1303` sets both `q_north_kettle` and
  `q_north_kettle_done`; the first is already held (set by `kettle_quest`). Harmless
  (idempotent) but noise. *Fix:* drop the redundant `q_north_kettle` setFlag.

- **POL-3 — Comment drift on the Fenn C3 flag.** *Evidence:* `scripts.ts:1445–1446`
  comment says "the trigger sets flag:fenn_c3" (correct — the trigger does), while the
  walkthrough §6 says C3 is "narrative only, no flag required." The build's choice (set
  `fenn_c3` so the beat can't re-fire) is *better* than the spec; just update
  03-north.md §6 to match so the next reader isn't confused. Doc-only.

### PRAISE
*(carried in Part 1; the standouts: the Còr/Fenn/Wren cluster, the un-breakable
choke sequencing, the consistent escalating warden delta, and the surgically clean
humour discipline.)*

---

## Part 3 — The three weakest things (mandatory, even though all minor)

1. **The copy-paste Lumenary interiors (MIN-1).** The single most visible "built fast"
   tell in the region — two wardens of opposite elements meet you in the same room.
   Cheapest high-value polish available.
2. **Windward Stair I's long grey climb (MIN-2).** The one stretch where the
   moment-to-moment risks "bored," precisely because the art and the encounter table
   are uniform across a 93-step corridor before the Updraft payoff.
3. **No new glossary/codex anchor for the Aurora-watch or Kite-rising festivals
   (gap).** The North adds two festivals and they're beautifully scripted, but unlike
   Còr/Coldfog they leave no LORE-codex trace — a returning time-poor player has
   nothing to re-read them from. *(Consistent with prior regions, which is why it's a
   gap not a finding — but the North's festivals are strong enough to deserve one
   `unlock_flag: flag:aurora_watch_seen` / `gleam:storm` entry each.)*

---

## Part 4 — Verdict & consistency check

**Verdict: SHIP-READY (fix-then-ship on the three minors at leisure).** All four
balance/flow gates pass; both quest chains are airtight; the §0 traps are avoided;
the emotional spine lands. Nothing here blocks a build. The three minors are polish
the region would be *better* for, not bugs it ships broken with.

**What North did better than South/East:**
- The **emotional staging** is a clear step up — Còr in person is a harder, braver
  beat than anything South/East attempted, and it's executed with more `silence` and
  portrait-restraint (per cinematics.md) than the earlier regions' set-pieces.
- The **un-sequence-breakable choke** design (Còr's band forcing B3 before the
  undercroft) is tighter scene-graph craft than the South's flatter trigger layout.
- **Humour discipline** is the most precise in the game so far — the sacred-beat
  firewall is explicit in the source comments.

**What South/East did better:**
- **Interior variety.** South/East interiors carried more per-building identity; North
  reused the Lumenary shell (MIN-1).
- **Route-leg length discipline.** South's legs sat nearer the §2b heal-spacing ideal;
  Windward I overshoots (MIN-2).
- **Festival codex footprint.** Neither region nailed this, but South's first-hour
  Lantern-fair at least anchors the "festival = belonging" idea the player meets first;
  North's two stronger festivals deserve the same codex permanence and don't yet have it.

*All panelist names are original personas standing in for handheld-RPG disciplines,
per VISION.md — described by craft and era, never by any existing studio or person.*
