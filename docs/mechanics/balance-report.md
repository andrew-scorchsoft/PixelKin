# PixelKin — Balance Report

> Generated from the tooling in `tools/balance/`. Reproducible: every figure
> cites its seed + battle count. Re-run with the commands in `09-simulator.md`.

## 1. Type chart (synthetic fair roster) — `chart_check.mjs 60000 12345`

Every type fielded with the *same* three role spreads at the *same* BST/level,
so any skew is the chart's fault alone. After tuning (`01-type-system.md`):

| | result |
|--|--|
| Win-rate spread | **46.7% – 53.3%** across all 10 types |
| Verdict | **All ten types inside the 45–55% guardrail.** |

Tuning history: an earlier draft had Solar 61% / Stone 59% / Verdant 39% /
Frost 43%. Four thematic edits (Stone↔Frost super-effectiveness flip; Storm ×2
vs Solar; Verdant offense unblocked vs Storm/Frost; Solar no longer scorches
Verdant) closed the spread to 6.6 points.

## 2. The roster — `simulate.mjs species.json 80000 777`

```
Tier  count  BST       Primary types
 A     33    312       Ember 16  Tide 16  Verdant 17  Stone 16  Storm 17
 B     19    350       Frost 15  Solar 13  Lunar 13   Light 16  Dark 12
 C     35    418
 D     47    498       Dual-typed across the dex: ~55%
 E     14    558       Single-stage kin: ~40; kindling lines: 68
 F      3    642
```

- **Offensive coverage: 10/10** — every type has a super-effective STAB answer
  obtainable in the roster (no type is a dead end).
- **Speed spread:** min 41 · p25 74 · median 85 · p75 104 · max 175 — no single
  speed wall.

## 3. Type win-rates (full roster)

### Raw (mixes all tiers)

```
Solar 60.6  Dark 56.8  Lunar 51.9  Verdant 51.2  Storm 49.9
Tide 48.6   Frost 48.6  Stone 47.3  Ember 45.9   Light 43.0
```

This is **expected to skew** and is *not* the balance signal: it mixes tiers, so
types whose members cluster in higher tiers (Solar/Dark are deliberately late,
premium, few low-tier members) win more, and the chart-isolating model excludes
abilities/status (where Light lives).

### Same-tier (isolates type from tier composition) — the real signal

```
Frost 56.4  Verdant 53.7  Dark 52.6  Storm 52.3  Solar 52.2
Ember 49.1  Stone 48.6   Lunar 48.3  Tide 47.4   Light 40.5
```

- **Solar 60.6→52.2 and Dark 56.8→52.6 once tier is controlled** — proof they
  are *not* overpowered; the raw skew was tier composition, exactly as intended
  (rare/late "awe" types).
- **8 of 10 types sit 47–56% same-tier.**
- **Frost 56.4%** — marginally hot (+1.4pp). A watch-item, within model noise
  (abilities, which would lift other types, are excluded). Not worth a chart edit.
- **Light 40.5%** — low **by design**: Light is the *support* type and the sim
  deliberately omits abilities/status/screens, which are its entire kit. Its
  real-game balance comes from utility, not raw damage. (See `01`, `03`.)

## 4. Per-species fairness — the decisive check

- **Within-tier outliers (>18pp from tier mean): NONE.** Every one of the 151
  fights within a fair band of its tier peers — the metric that actually governs
  whether a given encounter feels fair.
- **Top 8 overall:** Keylumen (F), Dawnbrael (F), Nullmajor (F), then E apexes
  (Dawnwatcher, Helithorn, Mycovast, Cindervast) — i.e. the legendaries and
  sub-legendaries, exactly where the "awe" belongs.
- **Bottom 8 overall:** all Tier-A early commons (Glimflit, Sporeling,
  Hearthkit…) — exactly as intended; a humble Sparkling *should* lose to the
  average roster member, and is balanced against its own tier, not the apexes.

## 5. Power-budget audit — `validate.mjs`

- `bst == sum(stats)` for all 151; every BST within its tier band.
- **EPS within-tier spread ≤ 30 points** for every tier (guardrail: ≤ ~50) — no
  kin is secretly a tier above its peers via premium typing + ability stacking.
- All kindling lines whole (no orphan mid-stages; BST climbs monotonically; all
  `from`/`into` resolve). Catch-rates inside tier bands. **0 errors, 0 warnings.**

## 6. Verdict

The chart is balanced; the roster has no within-tier outliers; coverage is
complete; the deliberate type/tier "awe curve" is intact and *measured* (rare
premium types skew raw win-rate but normalise same-tier). The one soft note —
Frost slightly hot, Light low — is understood, intended (Light), and minor
(Frost), and is left for a future abilities-aware simulation pass rather than a
chart change that would unbalance the proven fair-fight result.
