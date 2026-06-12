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
| **West** (04) | 7 Solar · 8 Lunar | 🟡 W1 built (Hushfrost cluster, 2026-06) | Sunken Solarium · Sunvault · Nightreach · Coldfog (+ spurs); W1 content refs (wiring) |
| **Central/Endgame** (05) | — | ⬜ not started | Penumbra Ring · Umbral Spire (`hub_unlocked` roads) |
| **Post-game** (06) | — | ⬜ not started | Dawnstead · day-forms · Còr's resolution |

**Playable runway today:** a continuous main-path journey from the cold open through the
**first six Gleams** (Ember → Tide → Verdant → Stone → **Storm → Frost**) and
`crown_south` + `crown_east` + `crown_north` — ending as the player leaves Pale Vault
west into Hushfrost Pass (the West boundary, intentionally ungated; Emberward in hand).

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

## West — Gleams 7–8 (`crown_west`) 🟡

| Area | map id(s) | Status | Builder |
|------|-----------|--------|---------|
| Hushfrost Pass I (snow canyon; coldfog throat = first REQUIRED Emberward) | `hushfrost_pass_i` | ✅ 2026-06 | `build_hushfrost_pass_i.py` |
| Hushfrost Pass II (X1 caretaker's shelter + numbed Hearthkit w/ `flag:dawn` swap; first blight fingers; gold-mouth sight-line) | `hushfrost_pass_ii` | ✅ 2026-06 | `build_hushfrost_pass_ii.py` |
| Aurora Hollow (Emberward spur; X1 aurora-oil; Frostholm's only wild bed) | `aurora_hollow` | ✅ 2026-06 | `build_aurora_hollow.py` |
| Sunken Solarium (Solar · Lucan · Sunsketch) | `sunken_solarium` | ⬜ | W2 |
| Sunvault Climb I→II + Helia Vault | — | ⬜ | W2 |
| Coldfog Marches + Drownlight + Stillworks (B4) | — | ⬜ | W3 |
| Nightreach Observatory (Lunar · Nessa · Starreach) | — | ⬜ | W4 |

W1 content refs (scripts/dialogue/trainers/items/EXTRA_ENCOUNTERS mirror) are owed to the
wiring pass — each builder prints its ledger. X1 reward item id must NOT be `bright_lamp`
(SaveCodec legacy rename) — use `caretaker_lamp`, display name "Bright Lamp".

See [`05-central-endgame.md`](./05-central-endgame.md), [`06-postgame.md`](./06-postgame.md)
for Central/Post-game. Not started.

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
