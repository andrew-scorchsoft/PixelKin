# PixelKin — Build Progress Log

> **What this is.** A living checklist of how far the *built game* has come against the
> canonical journey in this folder (the [spine](./README.md) + the six region files). The
> walkthrough is the **acceptance spec**; this file tracks which of its beats, maps, Gleams,
> Gifts and kit are actually wired in the engine — so any run (or human) can see at a glance
> what's done and what's next without re-deriving it from the map JSONs.
>
> **Keep it current.** When you build or extend an area, tick its row here **in the same
> commit** (the CLAUDE.md "keeping docs current" rule). One line per area; link the builder
> and note the delivering commit where useful. Status keys: ✅ built · 🟡 partial · ⬜ not started.

Legend — **Gleam** = the region's constellation reward; **Gift** = the Lantern Gift earned.

---

## Region roll-up

| Region | Gleams | Status | What's left |
|--------|--------|--------|-------------|
| **South** (01) | 1 Ember · 2 Tide | ✅ **complete** | — |
| **East** (02) | 3 Verdant · 4 Stone | ✅ **complete** | — (Cinderhead built 2026-06) |
| **North** (03) | 5 Storm · 6 Frost | ✅ **complete** (built 2026-06) | — |
| **West** (04) | 7 Solar · 8 Lunar | ✅ **complete** (W1–W4 maps + W5 content wiring, 2026-06; encounter mirrors verified in the R5 S/E sync) | — |
| **Central/Endgame** (05) | — | ✅ **complete** (C1 maps + C2 Spire + C3 wiring, 2026-06; panel SHIP-READY; C6 polish landed c15217d) | — |
| **The Three Hours** (07) | — | ✅ **complete** (sites + wiring + encounters + the hour-bell music, 2026-06) | — |
| **Post-game** (06) | — | 🟡 **Dawnstead + Starfall Vigils built** (R2+R3, 2026-06) | day-form pass (R4) |

**Playable runway today: the game is COMPLETABLE — cold open → dawn.** A continuous
main-path journey from the prologue through all eight Gleams and all four crowns,
across the parted Penumbra (Starreach), up the Umbral Spire's four floors, through
Warden Còr's final asking (out-remembered, not defeated), the Keylumen relight
(`flag:keystar_relit`), and the dawn (`flag:dawn`) — into the dawn-break panels +
credits roll, with the save persisted first so Continue resumes at the summit for
the post-game. (The in-map West encounter tables are live; the EXTRA_ENCOUNTERS
dex-side mirrors are the species lane's remaining bookkeeping.)

---

## South — Gleams 1–2 (`crown_south`) ✅

| Area | map id(s) | Status | Builder |
|------|-----------|--------|---------|
| Tinderwick (Ember · Brisa) | `tinderwick` + house/shop/lumenary | ✅ | `build_tinderwick*.py` |
| Tinderwick Beacon (earned Gleam loop) | `tinderwick_beacon_i/ii/top` | ✅ | `build_beacon.py` |
| Dimglass Coast I→II | `dimglass_coast`, `dimglass_coast_ii` | ✅ | `build_dimglass*.py` |
| Vesper Crossroads (Lanternway hub) | `vesper_crossroads` | ✅ | `build_crossroads.py` |
| Pearlmoor Quay (Tide · Reyl · Tidecall) | `pearlmoor_quay` + inn/shop/lumenary/breakwater | ✅ | `build_pearlmoor*.py` |
| Gullcry Rock (Tidecall spur) | `gullcry_rock` | ✅ | `build_gullcry.py` |

Festivals: Lantern-fair, Tide-blessing. Arcs delivered: A1/A2 (Wren), B1 (`dusk_begins`), C1/C2 (Fenn).

## East — Gleams 3–4 (`crown_east`) ✅

| Area | map id(s) | Status | Builder |
|------|-----------|--------|---------|
| Saltreach Fen I | `saltreach_fen_i` | ✅ | `build_saltreach_fen_i.py` |
| Saltreach Fen II (+ E1 reeds) | `saltreach_fen_ii` | ✅ | `build_saltreach_fen_ii.py` |
| Sunkbell Shallows (Tidecall spur) | `sunkbell_shallows` | ✅ | `build_sunkbell.py` |
| Lowleaf Hollow (Verdant · Sable · Glimmerstep) | `lowleaf_hollow` + lumenary/bower | ✅ | `build_lowleaf*.py` |
| Glowmoss Deep (B2 first Hollowing contact) + B1F | `glowmoss_deep`, `glowmoss_deep_b1f` | ✅ | `build_glowmoss_deep*.py` |
| Spore Grotto (Glimmerstep spur) | `spore_grotto` | ✅ | `build_spore_grotto.py` |
| **Cinderhead Mine (Stone · Otho · Lamp-down vigil)** | `cinderhead_mine` + lumenary | ✅ 2026-06 | `build_cinderhead_mine*.py` |
| **Cinderhead Deep — a 3-floor ladder maze** (fork → descent → vigil-lamp; `shortcut_mine`, → Galehigh) | `cinderhead_deep` + `_b1f` + `_b2f` | ✅ 2026-06 | `build_cinderhead_deep{,_b1f,_b2f}.py` |

Festivals: Glowmoss Bloom, **Lamp-down vigil**. Arcs delivered: A3 (Wren shaken), B2
(`met_hollowing` + Còr foreshadow), E. Earned loops: The Tended Bed (#3), **The Descent
Vigil (#4)**. Quests: E1 Quiet Reeds, E2 Spores for the Stall, **E3 The Foreman's Ledger**,
R3 Moss for the Quay. Crystoll Vault left as a `[LATER]` Starreach tease (void-gap signed).

## North — Gleams 5–6 (`crown_north`) ✅ (built 2026-06)

| Area | map id(s) | Status | Builder |
|------|-----------|--------|---------|
| Galehigh Terraces (Storm · Mira · Updraft Kite) | `galehigh_terraces` + lumenary/inn/home/kitemaker | ✅ | `build_galehigh_*.py` |
| Galehigh Skyloft (earned Gleam loop venue) | `galehigh_skyloft` | ✅ | `build_galehigh_skyloft.py` |
| Windward Stair I→II (`shortcut_windward`) | `windward_stair_i/ii` | ✅ | `build_windward_stair_*.py` |
| Wind-Eye (Updraft landmark · Cumulance) | `wind_eye` | ✅ | `build_wind_eye.py` |
| Thunderroost (Updraft spur · Strikeaven) | `thunderroost` | ✅ | `build_thunderroost.py` |
| Pale Vault Glacier (Frost · Ysolde · Emberward) | `pale_vault_glacier` + lumenary/inn/home | ✅ | `build_pale_vault_*.py` |
| Pale Vault Undercroft (the Lamp-Line trial) | `pale_vault_undercroft` | ✅ | `build_pale_vault_undercroft.py` |

Festivals: Kite-rising, Aurora-watch (all 8 festivals now have LORE codex entries).
Arcs delivered: B3 (Còr in person, `met_cor` — un-walk-aroundable on the oil leg),
A4 (Wren's wobble, ace 41, unresolved exit), C3 (Fenn–Còr shared past, `fenn_c3`).
Earned loops: the Kite-Rising Winch (#5), the Lamp-Line (#6). Quests: N1 Kettle,
N2 Aurora Sketcher (Aurora Charm = conditional charge ×2.5 on Frost-met kin),
N3 Wren's Ribbon (pays off at Nightreach lamp 6 — West owes the line), R4 Waystone Kite.
Expert panel: **SHIP-READY** (`docs/reviews/north-region-panel.md`); all minors fixed
(Lumenary re-skins, Windward rest shelf, 32–34 entry verge, Wind-Eye starglints).

## West — Gleams 7–8 (`crown_west`) ✅ (maps; wiring pass owed)

| Area | map id(s) | Status | Builder |
|------|-----------|--------|---------|
| Hushfrost Pass I (snow canyon; coldfog throat = first REQUIRED Emberward) | `hushfrost_pass_i` | ✅ 2026-06 | `build_hushfrost_pass_i.py` |
| Hushfrost Pass II (X1 caretaker's shelter + numbed Hearthkit w/ `flag:dawn` swap; first blight fingers; gold-mouth sight-line) | `hushfrost_pass_ii` | ✅ 2026-06 | `build_hushfrost_pass_ii.py` |
| Aurora Hollow (Emberward spur; X1 aurora-oil; Frostholm's only wild bed) | `aurora_hollow` | ✅ 2026-06 | `build_aurora_hollow.py` |
| Sunken Solarium (Solar · Lucan · Sunsketch; the Lit Stage loop #7 + Last-Warm-Day + X2 sun-mask; 24 designed encounter rows reconciled dry/flooded) | `sunken_solarium` + `sunken_solarium_lumenary` | ✅ 2026-06 | `build_sunken_solarium.py`, `build_solarium_interiors.py` |
| Sunvault Climb I→II (Sunsketch boundary; X3 viewpoint leg 1 + the Vigil Striker cache on II) | `sunvault_climb_i/ii` | ✅ 2026-06 | `build_sunvault_climb_*.py` |
| Helia Vault (Sunsketch PUZZLE micro-dungeon: 3 sequential blooms + the sun-mirror redirect; Heliovast's first wild bed) | `helia_vault` | ✅ 2026-06 | `build_helia_vault.py` |
| Coldfog Marches I→II + Drownlight Beacon + Hollowfen Stillworks (B4 shown half: the drained land; X3 leg 3 cairn; the charged-husk Whorlix cradle; first ACCENT tileset `coldfog_set`/fogcrag; NO trainers/rest by design) | `coldfog_marches_i/ii`, `drownlight_beacon`, `hollowfen_stillworks` | ✅ 2026-06 | `build_coldfog_*.py`, `build_drownlight_beacon.py`, `build_hollowfen_stillworks.py` (objects: `draw_coldfog_objects.py`) |
| Nightreach Observatory (Lunar · Nessa · Starreach; the Vigil of the Seven loop #8 — seven watch-lamps `flag:q_west_lamp_1..7` carrying C4 Fenn / A5 Wren / B4 the Great Null at lamps 5/6/7; Star-vigil; X3 giver + roof viewpoint; R5 giver; the Lanternway spoke landed at the crossroads, gleam:lunar-gated) | `nightreach_observatory` + `nightreach_lumenary`/`_inn`/`_home` | ✅ 2026-06 | `build_nightreach.py`, `build_nightreach_interiors.py` (objects: `draw_nightreach_objects.py` + the image-gen dome) |

**W5 WIRING ✅ (2026-06):** every script./npc./sign./trainer. ref the sixteen West maps (and
the crossroads spoke) place now resolves — scripts (the Lit Stage chain, the Vigil of the
Seven with C4/A5/B4 at lamps 5/6/7, the B4 Stillworks band, both Gleam ceremonies, the
Last-Warm-Day + Star-vigil festivals), dialogue, 12 trainers (`lucan_pyre` 2760w /
`nessa_cole` 3120w + the sight roster), items (`caretaker_lamp` "Bright Lamp" — the SaveCodec
rename trap dodged — Sun Charm ×2.5 Solar-met, Sunburst Nova chart, Embergloss/Murk Pearl),
glossary (Last-Warm-Day, Star-vigil, Sunsketch, Starreach, the Great Null), and the
progression model's West legs + BUILT_PAYOUTS (PASS). R5's delivery half is BUILT: the
crossroads Waykeeper is now a three-stage flag-disjoint trio (`script.round_chart_deliver`
→ `flag:q_round_chart`). The cutscene runner gained a per-step **`if_flag` guard**
(optional colour only — Wren's ribbon line + the Stillworks-witness line in B4 ride it).
**Still owed: the EXTRA_ENCOUNTERS mirrors** (tools/balance/build_species.py is another
lane's file — see each builder's encounter notes for the exact rows).
W2 contracts for W4 (in `build_sunvault_climb_ii.py`'s docstring): `to_observatory` lands
nightreach (15,28)/(16,28) — W4's return pair must land at climb II's (22,1)/(23,1);
X3's giver sets `flag:q_west_chart` (the Sunvault viewpoint then sets `_1`). The region
audit's "west is a pure corridor" WARN clears when W4 lands the Nightreach hub spoke.
W3 contracts for W4 (in `build_coldfog_marches_ii.py`'s docstring): the back-door
`to_observatory_fog` lands nightreach (28,14)/(28,15) facing left (map ≥29 wide, east-edge
entry walkable, Emberward-gated both sides) — W4's return pair must land at Coldfog II's
(1,3)/(1,4). Coldfog's X3 cairn sets `flag:q_west_chart_3` (the OPTIONAL bravest leg —
W4's done-stage must not hard-require `_3`). Stillworks' band sets only `flag:seen_stillworks`;
`flag:great_null_known` stays Nessa's at Nightreach.
W4 honoured all three contracts (handshakes verified by `audit_warps`): the rim pair lands
climb II (22,1)/(23,1), the fog pair lands Coldfog II (1,3)/(1,4) (Emberward both sides), and
the Nightreach hub spoke landed at the crossroads' NW corner (`to_nightreach`, gleam:lunar-gated
— the LAST Lanternway spoke; the crossroads diff was the spoke only). The west-corridor WARN now
clears: `audit_region`'s topology check gained a warp-backed RING fallback (a region's circuit
may close through the outer ring — nightreach → crossroads → coldfog I/II → nightreach — and
counts only once every authored side carries its warp). W4's done-stage requires `_1`+`_2`
only; the X3 chart NAMES STARWELL; R5's DELIVERY half (the crossroads Waykeeper's flag-staggered
trio, `flag:q_round_chart_taken` → `flag:q_round_chart`) landed with the W5 wiring above.

## Central / Endgame — the climax (no Gleams; convergence) ✅ (built 2026-06)

| Area | map id(s) | Status | Builder |
|------|-----------|--------|---------|
| Vesper Crossroads — endgame stages (C4 Fenn counsel · A5 Wren-joins band w/ the Starlamp · C1 Lampling's Trail · C2 inn + `crossroads_inn` counter · C3 Long Round · "now accessible" sign swap) | `vesper_crossroads` | ✅ | `build_crossroads.py` |
| Penumbra Ring (the last dark, Starreach crossings; threshold band, two reads, two priced pockets) | `penumbra_ring` | ✅ | `build_penumbra_ring.py` |
| Starwell (landmark — **Lunaveil #132** lv 54 `legendaryBattle`, cooldown 12) | `starwell` | ✅ | `build_starwell.py` |
| Umbral Spire (4 floors: gatehouse → null-works → high gallery → summit; 5 acolyte keepers lv52–55 · Wren per-floor · the shaft compressor) | `umbral_spire` + `_f2`/`_f3`/`_summit` | ✅ | `build_umbral_spire.py` |

**C3 WIRING ✅ (2026-06):** every ref the Central maps place resolves — the summit chain
(`script.great_null` → **`script.warden_cor_final`** (ace 56, 6,720w, out-remembered not
defeated) → **`script.keystar_relight`** (Keylumen #149 lv 55, `legendaryBattle` cooldown 0,
Fenn's Starlamp the intended asking) → **`script.dawn_breaks`** (sets `flag:dawn`, persists,
then the new `cinematic` op hands to the dawnbreak panels + real credits roll → Title;
Continue resumes at the summit). Quests C1/C2/C3 live (Lampling #148 set-piece, the
four-festival lamp-token chain riding the festival NPCs in Pearlmoor/Cinderhead/Pale
Vault/Nightreach, the Way-lamp); items `radiant_lamp`/`way_lamp`/`lamp_token_*`; glossary
+5 (Keystar, Penumbra, Ninth Lantern, Keylumen, First True Dawn); economy mirrored
(BUILT_PAYOUTS + the built Central leg — progression PASS).

See [`05-central-endgame.md`](./05-central-endgame.md) for the region spec.
Expert panel verdict (2026-06): **SHIP-READY**, no blockers — full review at
`docs/reviews/central-endgame-panel.md`. The whole main journey (cold open → 8 Gleams →
Spire → out-remembering → Keystar → dawn → credits → Continue) is built, audited
(0 warnings world-wide) and verified persist-safe.

## The Three Hours — legendary trio (07) ✅ (sites + wiring, 2026-06)

Species #160 Gloamber / #161 Tollhart / #162 Erstmorn are in the roster with full art
(162/162 packed). The `legendaryBattle` engine (battles-won cooldowns, `{remaining}`
hint token) is live. All four site maps are built + committed (2026-06): `tideglass_cavern`
+ `tideglass_gallery` (the Lampwright's Relay lens puzzle), `pale_vault_hourfold` (the
Unstruck Toll brazier puzzle), `unrisen_stair` (the First-Light bloom ascent). The content
wiring (site scripts/dialogue, the three giver chains, encounter mirrors, the
`battle-hours`/`sting-hour` music, LORE entries) landed in c5f36a9 (2026-06).
Spec: [`07-the-three.md`](./07-the-three.md).

---

## Remaining work — DOCUMENTED, NOT BUILT (the handoff roadmap)

> 2026-06 decision: build effort stops at the main game + the Three Hours; everything
> below is **specified, ready to execute, and deliberately deferred** (API budget).
> Ordering matters — packages are listed in execution order with their lane constraints.

### R1 — C6 endgame polish ✅ DONE (2026-06)
From the Central panel's ledger (`docs/reviews/central-endgame-panel.md`):
1. **MAJOR: in-Spire heal point.** A blackout at the climax respawns at Tinderwick — the
   harshest re-traverse in the game. Fix: a rest trigger at the Spire gatehouse (floor 1),
   the `script.*` + `heal` op pattern (`script.solarium_rest` is the worked example), staged
   diegetically (an acolyte who "still keeps the kettle", post-`cor_answered` swap optional).
   One trigger in `umbral_spire.json` + one script + audit_warps/audit_flow re-run.
2. **MINOR: Keylumen fallback hardening.** If the Starlamp was spent (e.g. on Lunaveil),
   the ending catch falls back to catchRate-6 throws (~23%/throw best case; free retries,
   never strands, but RNG at the most loaded moment). Preferred fix: in
   `script.keystar_relight`, before the `legendaryBattle` op, an `if_flag`-style guard that
   re-grants `starlamp` ×1 when the player holds none (Fenn "sent a second wick by the
   waykeeper" — one `giveItem` step gated on a has-item check; needs a small `unless_item`
   step guard in the runner, or an interact NPC at the dais doing the same in content only).
3. Re-run: typecheck + the 4 balance gates + audit_region.

Both fixes landed (commit c15217d): Wren keeps the gatehouse fire on Spire f1
(`script.spire_wren_camp`, the inn-rest kit), and a new `ensureItem` cutscene op
re-offers the Starlamp at the dais if it was spent. `npm run build` verified green.

### R2 — Dawnstead ✅ DONE (2026-06)
Spec: [`06-postgame.md`](./06-postgame.md) §Dawnstead. The C2 builder's contract (in
`build_umbral_spire.py`'s docstring): summit `to_dawn`/`to_dawn_e` warp from (16,20)/(17,20)
→ dawnstead (15,28)/(16,28) facing up; the return pair must land ON those summit coords.
Daylit register (the frozen set's `dawngrass/dawnpath/dawntuft` families are already drawn);
Tinderwick-silhouette layout; A6 Wren rematch (lv 55–65, `wren_resolved` portrait); Còr
tending a lamp (`at_peace`); the first-dawn festival; quests P1–P3. Backdrop `dawnstead-01`
and the town music loop are already rendered. Graph node exists (`unlocked_by_flag flag:dawn`).

**Delivered (2026-06):** `build_dawnstead.py` → `dawnstead.json` (C2 summit handshake honoured;
all audits 0 failures), A6 Wren talk + re-runnable rematch (`wren_rematch`, ace 62, rival
24×ace), `cutscene.cor_resolution` (un-walk-aroundable band, sets only `flag:cor_greeted`),
first-dawn festival, the sunlit-verge day-form table (55–65, Ember/Light), P1 First-Dawn
Letters (giver + all ten recipients incl. one NPC per warden town; quadrant stamps at the
four seats), P2 A Wick for Còr (beacon-top cache → lamp deco swap), P3 Day-form Survey
(boolean-chain fallback — no party-check op). **Owed:** the Waykeeper's "all ten delivered"
thanks (needs the quest-counter extension); `wren_rematch`/dawnstead mirrors into
`progression.mjs` + `EXTRA_ENCOUNTERS` (lands with R3's economy/species pass).

### R3 — The Starfall Vigils ✅ DONE (2026-06)
Full spec: [`06-postgame.md`](./06-postgame.md) §Starfall Vigils (written 2026-06, panel-grade):
5 escalating trial sites (lv 58→70, first full 6-kin smart-AI battles) opened by riddle
star-readings from the Nightreach junior watcher (Oriel), one-per-game rewards, and the
ultimate gauntlet at the Spire summit — Fenn at full strength (ace ~70, payout class 80×ace).
Build as region-style packages: V-maps (annex sites, Fable builders) → V-wiring (content) →
encounter/economy mirror → panel review. 6 new items specced in 06.

**Delivered (2026-06), both lanes:** the five annex maps (`build_vigil_*.py`; one-shape stamp —
trial band on every mouth tile, three flag-disjoint keeper placements, cache, no rest; code-drawn
`vigil_star_shard/scar` objects, no image-gen spend) + host warps/graph (audit_warps handshake
table in the builders); the full content chain (Oriel's eight terrace placements, the five trial
+ `_again` scripts, `script.starfall_round` → Dawnbrael (`legendaryBattle` lv 70, re-approachable)
→ `cutscene.startender_named`); nine smart six-kin trainers (Fenn ace 70 at `cor` class, on
`battle-boss-eclipse`); items (note: `chart_sunburst_nova` reused — Sunfall grants a second copy);
the `vigilant` 80w class in all three economy homes + the POSTGAME progression leg (incl. the R2
`wren_rematch` mirror); annex + dawnstead encounter mirrors (cross-checked table-for-table vs the
built maps). All gates green: typecheck, validate 0/0, chart_check, progression, simulate,
audit_region 0/0, audit_warps 0 failures. Owed to a panel pass: copy-editing review of the
readings/keeper dialogue (spine §10 tone gate).

### R4 — Day-form pass (LAST and ALONE; species + map lanes together)
Post-`flag:dawn` world changes: day-form encounter zone pairs (`requires_flag:'flag:dawn'`
rows beside the night tables — engine already supports this), Light-kin re-bloom in Coldfog,
the Hushfrost numbed-kin awake swap (pre-wired `_awake` twins exist), drained-zone deco swaps.
Re-runs EVERY region builder — that's why it must run last, alone, after all other map edits,
then one `build_species.py` regen + the 4 gates.

### R5 — Release ladder (verification, mostly cheap)
- `npm run build` (typecheck + prod build) — should already be green.
- `npm run build:dist` needs **ffmpeg** (not installed in the managed env) — install or add
  a CI job for the shrunk-audio bundle.
- ~~Reconcile the ~71 stale S/E generated encounter rows~~ ✅ DONE (2026-06): `dimglass_coast`,
  `dimglass_coast_ii`, `lowleaf_hollow` curated + mirrored; West/Hours mirrors verified in
  the same pass. Still on the generic generated-default path (works, but unmirrored):
  `tinderwick`, `gullcry_rock`, `spore_grotto`, `glowmoss_deep(_b1f)`, `cinderhead_mine`,
  `cinderhead_deep(_b1f/_b2f)` — sync when convenient.
- Full-game expert panel playing the dev build; golden-thread playtest (cold open → dawn →
  save export/import); README outside-in rewrite.
- **Human-only:** first-timer playtest (G8), touch QA on real hardware (F8).

---

## Standing engine dependencies (assumed-live, tracked)

- **Status conditions** — ✅ live (BattleEngine Part B, 2026-06).
- **Move-learn prompt / kindling** — ✅ live.
- **Wick economy / shops / Star-charts** — ✅ live.
- **Lamplight (vesperlamp brightness tiers, dark-map reveal mask)** — ⚠️ **designed, not built**
  (spine §5/§8). Region files author optional `[LATER: Lamplight ≥ …]` reveals toward it; the
  render feature is still on the engine roadmap. Cinderhead's far-gallery reveals are tagged
  for it, not gated on it.
- **Sunsketch light-puzzle (timed bloom)** — ⚠️ proposed (West). Sequential/redirect work now.
- **Quest counters (N-of-M)** — ⚠️ small `FlagStore` extension; all current quests use the
  boolean-chain fallback.
