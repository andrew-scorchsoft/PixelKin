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
| **North** (03) | 5 Storm · 6 Frost | ⬜ not started | Galehigh · Windward Stair · Pale Vault (+ spurs) |
| **West** (04) | 7 Solar · 8 Lunar | ⬜ not started | Hushfrost · Sunken Solarium · Sunvault · Nightreach (+ spurs) |
| **Central/Endgame** (05) | — | ⬜ not started | Penumbra Ring · Umbral Spire (`hub_unlocked` roads) |
| **Post-game** (06) | — | ⬜ not started | Dawnstead · day-forms · Còr's resolution |

**Playable runway today:** a continuous main-path journey from the cold open through the
**first four Gleams** (Ember → Tide → Verdant → **Stone**) and `flag:crown_south` +
`flag:crown_east` — roughly the first two-and-a-half hours, ending as the player walks the
Cinderhead Deep gallery on toward Galehigh (the North boundary, intentionally ungated).

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
| **Cinderhead Deep (vigil-lamp, `shortcut_mine`, → Galehigh)** | `cinderhead_deep` | ✅ 2026-06 | `build_cinderhead_deep.py` |

Festivals: Glowmoss Bloom, **Lamp-down vigil**. Arcs delivered: A3 (Wren shaken), B2
(`met_hollowing` + Còr foreshadow), E. Earned loops: The Tended Bed (#3), **The Descent
Vigil (#4)**. Quests: E1 Quiet Reeds, E2 Spores for the Stall, **E3 The Foreman's Ledger**,
R3 Moss for the Quay. Crystoll Vault left as a `[LATER]` Starreach tease (void-gap signed).

## North — Gleams 5–6 (`crown_north`) ⬜

Galehigh Terraces (Storm · Mira · Updraft Kite) · Windward Stair I→II · Pale Vault Glacier
(Frost · Ysolde · Emberward) + spurs (Wind-Eye, Thunderroost, Aurora Hollow). Arc B3 (Còr in
person, `met_cor`), Arc A4 (Wren's wobble), Arc C3 (Fenn–Còr shared past). **The East→North
boundary edge `cinderhead_deep → galehigh_terraces` is already in `graph.ts` and ungated** —
the first thing the North build inherits.

## West · Central · Post-game ⬜

See [`04-west.md`](./04-west.md), [`05-central-endgame.md`](./05-central-endgame.md),
[`06-postgame.md`](./06-postgame.md). Not started.

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
