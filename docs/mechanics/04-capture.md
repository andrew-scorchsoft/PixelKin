# PixelKin — Capture: the Lamp system

> The genre's "ball," reimagined to fit Vesperholm. The player is a **lamp-
> tender's apprentice**; you don't *trap* a wild kin, you **coax its light to
> rest inside a lantern**. The villains (the Hollowing) do the cruel inverse —
> tearing light out into **null-lanterns** — so the player's lamps are the
> warm, consensual mirror of the antagonist's tech. This is a core thematic
> beat made mechanical.

## The item line

The throwable capture item is a **Lamp**. Tiers (the genre's
Poké/Great/Ultra/Master rung, renamed and re-flavoured):

| Lamp | Bonus (`lampBonus`) | Where it comes from | Notes |
|------|:---:|---------------------|-------|
| **Spark Lamp** | ×1.0 | buyable everywhere, cheap | the basic workhorse |
| **Glow Lamp** | ×1.5 | shops from Pearlmoor on | reliable mid-tier |
| **Beacon Lamp** | ×2.5 | shops from Galehigh on, pricey | for tough catches |
| **Starlamp** | **guaranteed** | 1–2 in the whole game (gift/quest) | the "master" lamp |

### Specialty lamps (conditional, the fun ones)

| Lamp | Effect |
|------|--------|
| **Dusklamp** | ×3.0 at night, or vs **Lunar**/**Dark** kin (else ×1.0) |
| **Hearthlamp** | ×3.5 if the target is **Dozing** or below 25% HP (else ×1.0) — rewards the proper "weaken then catch" loop |
| **Tidelamp** | ×3.0 on kin encountered in **water** terrain (else ×1.0) |
| **Mosslamp** | ×3.0 on kin in **tall_grass**/forest (else ×1.0) |
| **Cinderlamp** | ×3.0 on kin in **cave** terrain (else ×1.0) |
| **Swiftlamp** | ×4.0 on the **first turn** of an encounter (else ×1.0) — gamble for a fast catch before the kin acts |
| **Kindred Lamp** | bonus scales with how many of that **species** you've already lamped: ×1.0 + 0.3 per prior catch, capped ×4.0 — the completionist's friend |

Specialty lamps are found in optional spurs/landmarks (see
`06-progression-and-distribution.md`), so exploration directly improves your
catching toolkit — feeding the *exploration* and *collecting* pillars at once.

## The catch formula

Transparent and easy to simulate (no opaque shake-byte maths):

```
hpTerm   = (3*HPmax - 2*HPcur) / (3*HPmax)      // 1/3 at full HP, →1 near faint
chance   = clamp01( hpTerm * (catchRate / 255) * lampBonus * statusBonus )
caught   = random() < chance
```

- **`catchRate`** is a per-species stat, **1–255** (higher = easier). It scales
  inversely with the kin's rarity/tier (table below).
- **`hpTerm`** means a full-HP kin is caught at *one-third* effectiveness, so
  weakening it first roughly triples your odds — the loop the genre trained
  players to love.
- **`statusBonus`**: Dozing/Chill ×2.5; Scorch/Numb/Blight/Drench/Dazzle ×1.5;
  none ×1.0. (Status + Hearthlamp is the power-combo for hard catches.)
- The on-screen lantern "wobbles" are cosmetic, derived from `chance` (more
  wobbles = closer) — pure juice, no hidden second roll.

### Catch-rate by tier

| Tier (from `02`) | catchRate | Feel |
|------|----------:|------|
| A — Sparkling | 190–235 | catch on a Spark Lamp most throws |
| B — Starter base | 150–200 | easy with a little chip damage |
| C — Middle | 90–150 | want it weakened + a Glow Lamp |
| D — Final | 45–90 | weaken to red, status it, Beacon Lamp |
| E — Apex / pseudo-rare | 20–45 | a genuine multi-lamp battle of attrition |
| F — Legendary | 3–10 | Doze + Hearthlamp + patience, or a Starlamp |

Wild-caught kin appear at the tier-appropriate level for their biome
(`06`), so you rarely meet a wild Tier-E/F at full strength early — the catch
*and* the encounter level gate the "wow" kin behind progress.

## Worked examples

- **Sparkling in the starting grass** (catchRate 210), full HP, Spark Lamp:
  `chance = 0.333 · (210/255) · 1.0 · 1.0 ≈ 0.27` per throw — a couple of tries.
- **Tier-D final at ~15% HP, Dozing, Beacon Lamp** (catchRate 60):
  `chance = clamp01(0.90 · (60/255) · 2.5 · 2.5) ≈ clamp01(1.32) = 1.0` — the
  weaken-status-and-throw loop reliably lands even tough catches.
- **Legendary at red HP, Dozing, Hearthlamp** (catchRate 5):
  `chance ≈ 0.95 · (5/255) · 3.5 · 2.5 ≈ 0.16` per throw — tense, repeated
  attempts, exactly the legendary-encounter fantasy.

## Story & rules hooks

- You receive your **Vesperlamp** (the master tool, not a throwable) and your
  first **Spark Lamps** in the Tinderwick intro — already wired as
  `flag:has_vesperlamp` in `tinderwick.json`.
- Legendaries (Keylumen and Warden Còr's drained kin) use **scripted**
  encounters; their low catchRate plus a one-per-save flag preserves their
  uniqueness.
- Field stat used by the engine/sim: each species carries `"catchRate": <n>`.

## Data hook

Lamps live in the items data (to be authored alongside the inventory system) as:

```jsonc
{ "id": "beacon_lamp", "name": "Beacon Lamp", "lampBonus": 2.5,
  "condition": null, "price": 900, "desc": "Brass-and-glass; its steady beam
  invites even a wary kin to settle." }
```

Conditional lamps carry a `condition` the catch routine evaluates
(`time:night`, `defenderType:Lunar|Dark`, `hpBelow:0.25`, `status:doze`,
`terrain:water`, `firstTurn:true`, `speciesCaught`).
