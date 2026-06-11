# PixelKin — Capture: the Lamp & its Charges

> The genre's "ball," reimagined to fit Vesperholm. The player is a **lamp-
> tender's apprentice**; you don't *trap* a wild kin, you **coax its light to
> rest inside a lantern**. The villains (the Hollowing) do the cruel inverse —
> tearing light out into **null-lanterns** — so the player's lamp is the
> warm, consensual mirror of the antagonist's tech. This is a core thematic
> beat made mechanical.
>
> **Status: BUILT (2026-06).** One vesperlamp + consumable charges, the
> shake-check roll, and the status bonus are live (`systems/battle/catch.ts`,
> `BattleScene.lampMenu`). Specialty charges beyond the Tide Charm are design
> for later regions' spur rewards.

## One lamp, many charges

You carry **one vesperlamp** — the device Fenn gives you at the ceremony, never
spent, never replaced. A **plain throw is always free** (raise the lamp, ×1.0).
What you buy are **charges**: waxed cells fed to the lamp for **one brighter
throw**. The LAMP action in a wild battle offers PLAIN THROW plus any charges
you carry; using a charge consumes it.

| Throw | Bonus (`lampBonus`) | Price | Where |
|------|:---:|---:|---------------------|
| **Plain throw** | ×1.0 | free | always — the vesperlamp itself |
| **Glow Charge** | ×1.5 | 200w | shops from the start |
| **Beacon Charge** | ×2.5 | 600w | appears on shelves once you hold the **Ember Gleam** (`requires_flag` shop stock) |
| **Starlamp** | **guaranteed** | — | 1–2 in the whole game (gift/quest) — a cell of caught starlight |

### Specialty charges (conditional, the fun ones)

| Charge | Effect |
|------|--------|
| **Tide Charm** | ×2.0 — wave-worn, lashed to the lamp-frame; the South's spur reward (**BUILT**, Gullcry Rock) |
| **Dusk Charge** | ×3.0 at night, or vs **Lunar**/**Dark** kin (else ×1.0) |
| **Hearth Charge** | ×3.5 if the target is **Dozing** or below 25% HP (else ×1.0) — rewards the proper "weaken then catch" loop |
| **Moss / Cinder / Tideglass Charges** | ×3.0 on kin met in tall-grass / cave / water terrain (else ×1.0) |
| **Swift Charge** | ×4.0 on the **first turn** of an encounter (else ×1.0) — gamble for a fast catch |
| **Kindred Charge** | scales with prior catches of that species: ×1.0 + 0.3 each, capped ×4.0 — the completionist's friend |

Specialty charges are found in optional spurs/landmarks (see
`06-progression-and-distribution.md`), so exploration directly improves your
catching toolkit — feeding the *exploration* and *collecting* pillars at once.
The Tide Charm is the built worked example; later regions add theirs as data
(`content/items.ts`, `category: 'charge'`).

## The catch roll

The engine uses the genre's classic **four-shake check**
(`systems/battle/catch.ts`): the wobbles you see are the real rolls, not
cosmetics. The maths reduce to a transparent per-throw chance:

```
hpTerm  = (3*HPmax - 2*HPcur) / (3*HPmax)      // 1/3 at full HP, →1 near faint
a       = hpTerm * catchRate * lampBonus * statusBonus
caught  = guaranteed when a ≥ 255; otherwise four shake checks,
          overall P(caught) ≈ a / 255
```

- **`catchRate`** is a per-species stat, **1–255** (higher = easier). It scales
  inversely with the kin's rarity/tier (table below).
- **`hpTerm`** means a full-HP kin is caught at *one-third* effectiveness, so
  weakening it first roughly triples your odds — the loop the genre trained
  players to love.
- **`statusBonus`** (live): Doze/Chill ×2.5; Scorch/Numb/Blight/Drench/Dazzle
  ×1.5; none ×1.0. (Status + a strong charge is the power-combo for hard
  catches.)
- A break shows 0–3 wobbles (how close you came); a catch shows all four.

### Catch-rate by tier

| Tier (from `02`) | catchRate | Feel |
|------|----------:|------|
| A — Sparkling | 190–235 | catch on a plain throw most tries |
| B — Starter base | 150–200 | easy with a little chip damage |
| C — Middle | 90–150 | want it weakened + a Glow Charge |
| D — Final | 45–90 | weaken to red, status it, Beacon Charge |
| E — Apex / pseudo-rare | 20–45 | a genuine multi-charge battle of attrition |
| F — Legendary | 3–10 | Doze + a specialty charge + patience, or a Starlamp |

Wild-caught kin appear at the tier-appropriate level for their biome
(`06`), so you rarely meet a wild Tier-E/F at full strength early — the catch
*and* the encounter level gate the "wow" kin behind progress.

## Worked examples (per-throw odds ≈ a/255)

- **Sparkling in the starting grass** (catchRate 210), full HP, plain throw:
  `a = 0.333 · 210 · 1.0 · 1.0 ≈ 70 → P ≈ 27%` — a couple of tries.
- **Tier-D final at ~15% HP, Dozing, Beacon Charge** (catchRate 60):
  `a = 0.90 · 60 · 2.5 · 2.5 ≈ 338 ≥ 255` — **guaranteed**; the
  weaken-status-and-throw loop reliably lands even tough catches.
- **Legendary at red HP, Dozing, Hearth Charge** (catchRate 5):
  `a ≈ 0.95 · 5 · 3.5 · 2.5 ≈ 42 → P ≈ 16%` per throw — tense, repeated
  attempts, exactly the legendary-encounter fantasy.

## Story & rules hooks

- You receive your **vesperlamp** (the device, a key item) at Fenn's ceremony —
  wired as `flag:has_vesperlamp`; your first **Glow Charges** come from the
  Tinderwick shop kit and roadside caches.
- Legendaries (Keylumen and Warden Còr's drained kin) use **scripted**
  encounters; their low catchRate plus a one-per-save flag preserves their
  uniqueness.
- Field stat used by the engine/sim: each species carries `"catchRate": <n>`.

## Data hook (as built)

Charges live in `src/game/content/items.ts`:

```jsonc
{ "id": "beacon_charge", "name": "Beacon Charge", "category": "charge",
  "catch_bonus": 2.5, "price": 600,
  "desc": "A chandler's pressed cell, near daylight in the lamp. One blazing
  throw — the surest catch wicks can buy." }
```

Future conditional charges carry a `condition` the catch routine evaluates
(`time:night`, `defenderType:Lunar|Dark`, `hpBelow:0.25`, `status:doze`,
`terrain:water`, `firstTurn:true`, `speciesCaught`) — not yet implemented;
add alongside the first specialty charge beyond the Tide Charm.
