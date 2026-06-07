# PixelKin — Type System

> Authoritative data lives in `src/game/data/type-chart.json`. This doc is the
> human-readable companion (keep them in sync). Balance is verified empirically
> by the Monte Carlo simulator in `tools/balance/` — see
> `02-stats-and-balance.md`.

## Why ten types

The world (see `docs/world/story-bible.md`) is built on **eight constellation
elements**, each anchored by a Lampwarden, plus the universal **Light / Dark**
axis of the central plot (restoring dawn vs the Hollowing's null). That gives a
natural, lore-locked set of **ten types**:

| # | Type | Flavour | Region / Lampwarden |
|---|------|---------|---------------------|
| 1 | **Ember** | hearth-fire, warmth, char | South — Brisa Tallow |
| 2 | **Tide** | moonlit water, brine, current | South — Reyl Wash |
| 3 | **Verdant** | glowmoss, root, bloom | East — Sable Quill |
| 4 | **Stone** | deep-earth, crystal, ore | East — Otho Grist |
| 5 | **Storm** | lightning, gale, static | North — Mira Vael |
| 6 | **Frost** | ice, aurora, hush | North — Ysolde Frost |
| 7 | **Solar** | stored daylight, flare | West — Lucan Pyre |
| 8 | **Lunar** | dreamlight, moon, omen | West — Nessa Cole |
| 9 | **Light** | radiance, the Skyweave | universal (post-relight) |
| 10 | **Dark** | the null, shadow, the Hollowing | universal (Coldfog) |

Ten is deliberately leaner than the modern 18. It keeps the chart memorisable
(Game-Boy-era simplicity, our top value) while still giving real strategic
depth. We compensate for the smaller count with **liberal dual-typing** — most
of the 151 carry two types, so the *effective* matchup space is far richer than
ten rows suggest.

## The two mirror axes

Eight of the types form a conventional interlocking web. The celestial four
include two **mirror pairs** that deal **mutual super-effective** damage, on
purpose:

- **Solar ↔ Lunar** — day against night. Either side hitting the other for ×2
  makes these matchups fast and dramatic.
- **Light ↔ Dark** — radiance against the Hollowing's null. This *is* the
  endgame, mechanically: the climactic battles are knife-edge swings.

Mirror axes create high-variance, "anything can happen" fights that we reserve
for late / rare / legendary kin — exactly where the story wants its tension.

## The chart

Read it as **attacker (row) → defender (column)**. `²` = super-effective (×2),
`½` = resisted (×0.5), `0` = immune (×0), blank = neutral (×1).

```
            DEFENDER →
ATK ↓   Em   Ti   Ve   St   Sm   Fr   So   Lu   Li   Da
Ember   ½    ½    ²    ½    ·    ²    ½    ·    ·    ·
Tide    ²    ½    ½    ²    ½    ·    ·    ½    ·    ·
Verdant ½    ²    ½    ²    ·    ·    ·    ·    ·    ·
Stone   ²    ½    ½    ½    ²    ·    ·    ·    ·    ·
Storm   ·    ²    ²    0    ½    ½    ²    ·    ·    ·
Frost   ½    ½    ²    ²    ²    ½    ½    ·    ·    ·
Solar   ½    ½    ·    ½    ·    ²    ½    ²    ·    ²
Lunar   ·    ²    ·    ·    ·    ·    ²    ½    ·    0
Light   ·    ·    ·    ½    ·    ·    ·    ·    ½    ²
Dark    ·    ·    ·    ·    ·    ·    ½    ²    ²    ½
```

> This grid was **tuned empirically**: an earlier draft left Solar (61%) and
> Stone (59%) too strong and Verdant (39%) and Frost (43%) too weak in the
> `tools/balance/chart_check.mjs` Monte Carlo. The edits (Stone loses its Frost
> super-effectiveness and gains a Frost weakness; Storm now smothers Solar;
> Verdant's offense is no longer resisted by Storm/Frost; Solar no longer scorches
> Verdant) brought **all ten types into a 46.7%–53.3%** fair-fight band while
> keeping each type's intended character.

### Immunities (the two hard zeroes)

- **Storm → Stone = 0.** Earth grounds electricity. The classic "you can't
  shock what's earthed" rule; gives Stone a defining defensive identity.
- **Lunar → Dark = 0.** You cannot dream away the void. The Hollowing's null is
  untouched by dreamlight — a plot beat made mechanical (Lunar specialists
  struggle against the final foe, forcing party variety).

## Defensive & offensive profile summary

How many types are super-effective against each (defensive pressure), and how
many each hits for ×2 (offensive reach):

(Fair-fight win-rates from `chart_check.mjs`, 60k battles, in brackets.)

| Type | Weak to (×2 in) | Resists/immune (×½ or 0 in) | Hits ×2 (reach) | Read [WR] |
|------|:---:|:---:|:---:|------|
| Ember | 2 (Tide, Stone) | 4 | 2 | balanced [50.3%] |
| Tide | 3 (Verdant, Storm, Lunar) | 5 | 2 | balanced [49.1%] |
| Verdant | 3 (Ember, Storm, Frost) | 3 | 2 | **fragile common** [46.7%] |
| Stone | 3 (Tide, Verdant, Frost) | 4 (+1 immunity) | 2 | sturdy, modest reach [49.4%] |
| Storm | 2 (Stone, Frost) | 2 (+1 immunity dealt) | 3 | glass — strong but exposed [53.3%] |
| Frost | 2 (Ember, Solar) | 2 | 3 | solid attacker [51.2%] |
| Solar | 2 (Storm, Lunar) | 4 | 3 | **premium / rare** [52.2%] |
| Lunar | 2 (Solar, Dark) | 2 (+1 immunity dealt) | 2 | swingy specialist [49.8%] |
| Light | 1 (Dark) | 1 | 1 | **support type** [48.1%] |
| Dark | 2 (Solar, Light) | 1 (+immune to Lunar) | 2 | swingy specialist [50.0%] |

These asymmetries are intentional and map to where each type sits in the
journey:

- **Verdant** is the genre's fragile grass archetype (lowest WR, 3 weaknesses,
  narrow resists). It's an *early, common* type, so most Verdant kin are
  **dual-typed** (Verdant/Light glowmoss, Verdant/Stone, Verdant/Tide) to patch
  coverage, and the pure ones lean into bulk or speed stats.
- **Solar** is deliberately a **premium type**: wide reach, only two
  weaknesses, strong resists. It is *rare and late* (west region, 7th
  Lampwarden), expensive to catch, and assigned to few species — its scarcity is
  the balancing lever on top of its already-tamed chart profile. This is the
  "awe on sight" feeling by design. (Storm clouds smothering daylight give it a
  clean late-game answer: Storm ×2 vs Solar.)
- **Light** is the **support type**: little offensive reach, thin resistances.
  Light kin earn their place through **abilities, status, and bulk**, not raw
  type damage — they're the glue of a team, and the mascot (Lampling) is Light.
- **Lunar / Dark** are **high-variance specialists** tied to the endgame.

## Balance guardrails (enforced by the simulator)

The simulator (`tools/balance/simulate.mjs`) is the referee. After the roster
exists we require, across tens of thousands of random fair fights:

1. **No type's win-rate may sit outside ~45–55%** once species counts and
   stat tiers are accounted for. Solar/Light are allowed to skew on *raw type*
   because their **rarity and stat budgets** pull them back to centre — the sim
   checks the *as-distributed* win-rate (weighting by how often a player
   actually fields each type at a given point), not the naive type-vs-type rate.
2. **Every type must have at least one answer.** No type may be left without a
   super-effective counter that a player can realistically obtain before they'd
   need it (checked against the progression in `06-progression-and-distribution.md`).
3. **Coverage reachability:** by each Lampwarden, the player can have caught kin
   covering that warden's type weaknesses.

If a guardrail fails, the fix order is: (a) adjust *distribution/rarity*, then
(b) adjust *stat tiers* of outlier species, and only as a last resort (c) edit a
single chart cell here + in the JSON.

## Naming note

Type names are original and evocative rather than literal ("Ember" not "Fire",
"Tide" not "Water", "Storm" folds in electric+wind, "Stone" folds in
rock+earth+crystal). The two existing sample kin (`assets/creatures/`) were
authored as `Fire`/`Water`; their `metadata.json` is being migrated to
`Ember`/`Tide` to match this canonical set.
