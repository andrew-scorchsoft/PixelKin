# PixelKin — Stats, Power Budget & Balance

> This is the backbone of roster balance. Every one of the 151 kin is costed
> against the rules here, and the whole roster is then stress-tested by the
> Monte Carlo simulator in `tools/balance/`.

## The six stats

We keep the six the genre taught players to read at a glance (the two sample
kin in `docs/sample-kin.md` already use them):

| Stat | Code | What it does |
|------|------|--------------|
| Health | `hp` | hit points; how much damage a kin endures |
| Attack | `atk` | power of **physical** moves |
| Defense | `def` | reduces **physical** damage taken |
| Special Attack | `spa` | power of **special** moves |
| Special Defense | `spd` | reduces **special** damage taken |
| Speed | `spe` | who moves first each turn |

Six stats, two damage channels (physical / special), one speed axis. Familiar,
readable, and enough depth for real teambuilding without GBA-era overwhelm.

## Base Stat Total (BST) tiers

A kin's **BST** is the sum of its six base stats. BST is the master power dial,
bracketed into tiers tied to a kin's place in its **kindling** line
(see `05-kindling.md`). Reference points from the existing starters:
Vulpyre = 356, Brinix = 352 (both starter-base, i.e. Tier B).

| Tier | Label | BST range | Typical role in a line |
|------|-------|-----------|------------------------|
| **A** | Sparkling | 280–340 | base form of a 3-stage line; weak early critters |
| **B** | Kindled-I / Starter base | 320–375 | base form of a 2-stage line; starter first form |
| **C** | Middle | 390–445 | middle form of a 3-stage line; strong standalone |
| **D** | Final | 470–525 | final form of a 2- or 3-stage line; standalone apex |
| **E** | Apex / Pseudo-rare | 535–580 | rare standalone "wow" kin; pseudo-legendary finals |
| **F** | Legendary | 590–680 | story/box legendaries; one-of-a-kind |

Distribution target across the **151** (roughly genre-authentic):

- Tier A: ~22 · Tier B: ~34 · Tier C: ~26 · Tier D: ~50 · Tier E: ~13 · Tier F: ~6
- That's ~151. (Finals dominate because most lines terminate in a D, and many
  single-stage kin are C/D.)

## Stat distribution: role archetypes

BST says *how strong*; the **role** says *how the points are spent*. Every kin
is tagged with one of these. Templates below are normalised to **BST 500**
(a typical Tier-D final); scale each stat by `targetBST / 500` then round, and
jitter individual stats ±8 for personality (keeping the total on-tier).

| Role | hp | atk | def | spa | spd | spe | Identity |
|------|---:|---:|---:|---:|---:|---:|----------|
| Physical Sweeper | 70 | 115 | 65 | 50 | 65 | 135 | fast, hits hard physically, frail |
| Special Sweeper | 70 | 50 | 60 | 125 | 70 | 125 | fast nuker (Vulpyre's grown-up role) |
| Glass Cannon | 55 | 130 | 50 | 60 | 55 | 150 | extreme offense, paper bulk |
| Physical Wall | 95 | 70 | 120 | 45 | 85 | 85 | soaks physical hits, stalls |
| Special Wall | 100 | 40 | 85 | 70 | 120 | 85 | soaks special hits (Brinix's role) |
| Physical Bruiser | 100 | 110 | 90 | 50 | 75 | 75 | slow, bulky, heavy hitter |
| Special Tank | 100 | 45 | 70 | 110 | 90 | 85 | bulky special attacker |
| Balanced / Pivot | 85 | 85 | 85 | 85 | 85 | 75 | jack-of-all-trades, switches well |
| Utility / Speedster | 75 | 75 | 75 | 75 | 75 | 125 | fast support, status/hazard setter |
| Disruptor / Status | 80 | 70 | 90 | 70 | 90 | 100 | defined by movepool, not raw stats |

Earlier line stages use the **same role**, scaled to a lower tier, so a line has
a consistent feel as it kindles (a Sparkling Special Sweeper grows into a
final-stage Special Sweeper).

## The damage formula (engine + simulator)

Canonical, well-understood, easy to balance against:

```
base = floor( ( (2*L/5 + 2) * Power * A / D ) / 50 ) + 2
damage = floor( base * STAB * TypeEff * Roll )
```

- `L` = attacker level.
- `Power` = the move's base power.
- `A` = attacker `atk` (physical move) or `spa` (special move).
- `D` = defender `def` (physical) or `spd` (special).
- `STAB` (Same-Type Attack Bonus) = **1.5** if the move's type matches one of
  the attacker's types, else 1.0.
- `TypeEff` = product of `type-chart.json` multipliers vs each defender type
  (dual-type defenders multiply both, e.g. ×2 · ×2 = ×4; ×2 · ×0 = 0).
- `Roll` = random in `[0.85, 1.00]` (the genre's damage spread). The simulator
  uses a seeded RNG so runs are reproducible.

Status moves deal no damage and instead apply effects (see `03-moves.md`).

### Stat-at-level

From base stat `B` at level `L` (IV/EV-free baseline used by the sim for fair
comparisons; the live game layers in per-individual variance — see "Individual
variance" below):

```
HP    = floor( 2*B*L / 100 ) + L + 10
other = floor( 2*B*L / 100 ) + 5
```

## The power-budget model (designer-facing cost check)

BST + the sim catch most problems, but to stop designers stacking a great
typing **and** a great ability **and** a great movepool on one kin, each
species also gets an **Effective Power Score (EPS)** used during selection and
validation:

```
EPS = BST
    + typingScore        (see table)
    + abilityScore       (0 / +10 / +20 / +30 by tier — see 03-moves.md)
    + movepoolScore      (+0..+25 for unusually wide/strong coverage)
    - rarityDiscount     (rarer/later kin may run hotter; common early kin may not)
```

**typingScore** (rough, from the profile table in `01-type-system.md`):

| Type | score | | Type | score |
|------|---:|---|------|---:|
| Solar | +25 | | Frost | +5 |
| Stone | +15 | | Verdant | −5 |
| Dark | +10 | | Light | −10 |
| Lunar | +10 | | (dual-typing) | +5 net avg |
| Ember/Tide/Storm | +5 | | | |

Guardrail: **within a tier, EPS spread should stay within ±25**. A kin that
busts the ceiling must either drop a tier, lose stats, or trade its premium
typing/ability. This keeps "a Tier-D Solar glass cannon with a top ability"
from quietly being a Tier-E in disguise.

## Individual variance (live game only, not the sim)

To preserve the genre's collecting texture without unbalancing fights, the live
game adds light per-individual variance on top of base stats:

- **Gleam values** (our IVs): 0–15 per stat, rolled on encounter. Small enough
  (~max +15 at L100) to reward hunting "good" individuals without dominating.
- **Training drift** (our EVs): a soft cap (≈128 per stat, 320 total) earned
  through battle, so investment matters but can't 6×-max everything.
- **Temperaments** (our natures): +10% / −10% to one stat each. Flavourful, and
  reads as personality (Bold, Brisk, Timid…).

The **simulator deliberately ignores all three** and fights at flat base stats,
so the roster is balanced at its *structural* core; variance is seasoning, not
the foundation.

## Level & progression anchors

- Level cap **100** (genre-authentic ceiling; most players finish the main
  story in the 50s).
- Wild encounter levels and Lampwarden team levels are specified in
  `06-progression-and-distribution.md`. The short version: starter at L5,
  1st Lampwarden tops ~L14, scaling to ~L55–60 at the Umbral Spire, with
  legendaries and post-game rares above that.

## What the simulator checks

`tools/balance/simulate.mjs` runs tens of thousands of seeded fights and reports:

1. **Type win-rates** (raw, and *as-distributed* by where players field them).
2. **Per-species outliers** — kin winning/losing far more than their tier peers.
3. **Stat-tier sanity** — BST histogram vs the targets above.
4. **Coverage gaps** — any type with no reachable super-effective answer.
5. **Speed-tier clustering** — to avoid a single "everything outspeeds at 130"
   wall.

Failing checks are fixed in this order: distribution/rarity → outlier stats →
(last resort) a single type-chart cell. See `06` for the distribution levers.
