# PixelKin — Moves & Abilities

> Authoritative move data lives in `src/game/data/moves.json`. This doc is the
> design spec. Each kin knows **up to four moves at once** (the genre rule we're
> keeping) and draws them from a per-species **learnset**.

## Move data shape

```jsonc
{
  "id": "ember_jab",          // stable slug, referenced by learnsets
  "name": "Ember Jab",
  "type": "Ember",            // one of the 10 types, or "Plain" (typeless)
  "category": "physical",     // "physical" | "special" | "status"
  "power": 40,                // base power; 0 for status
  "accuracy": 100,            // 0..100; 0 = never misses (e.g. status on self)
  "charges": 30,              // our "PP": uses before a rest restores them
  "priority": 0,              // higher acts first; ties broken by Speed
  "target": "foe",            // "foe" | "self" | "all_foes" | "field"
  "effect": null,             // optional structured effect (see below)
  "flags": ["contact"],       // contact, sound, guard_pierce, recharge, etc.
  "desc": "A fast swipe wreathed in hearth-sparks."
}
```

### The "Plain" move type

We have **no Normal creature type** — every kin is elemental/celestial. But kin
still need humble, universal starter moves (the genre's Tackle/Scratch). Those
are typed **`Plain`**: always ×1 effectiveness, **never** gets STAB, ignores the
type chart entirely. Plain moves keep early kin functional and give designers a
"neutral coverage" option without inflating the type count to eleven.

### Effects

`effect` is an optional structured object the engine reads. Common shapes:

```jsonc
{ "status": "scorch", "chance": 30 }              // burn-equivalent, 30% on hit
{ "stat": "spe", "stages": -1, "chance": 100, "to": "foe" }  // lower Speed
{ "stat": "atk", "stages": 2, "to": "self" }      // sharp self buff
{ "drain": 0.5 }                                  // heal 50% of damage dealt
{ "recoil": 0.33 }                                // user takes 33% of damage
{ "heal": 0.5, "to": "self" }                     // status heal move
{ "flinch": 30 }                                  // 30% flinch
{ "multi": [2, 5] }                               // hits 2–5 times
{ "highCrit": true }                              // boosted crit rate
{ "weather": "sun" }                              // sets field state
```

**Implementation status (2026-06):** stat stages, status, drain, recoil, heal,
flinch, highCrit, cure, screens, the caltrops hazard, pivot and Rest Up's
selfDoze all run in `BattleEngine`. `multi` and `weather` have **no moves in
the current 125-pool** and stay unimplemented until a move needs them (add the
engine support in the same change as the move).

### Status conditions (our names)

Original names, familiar functions — keeps the cosy lamplight tone. **BUILT
(2026-06):** these run in the engine (`BattleEngine` pre-move gates, end-of-turn
chip, stat hooks; the exact tuning constants below are the source of truth and
live at the top of `systems/battle/BattleEngine.ts`):

| Status | Slug | Effect (exact) | Genre analogue |
|--------|------|--------|----------------|
| Scorch | `scorch` | 1/16 max HP chip each turn; physical Atk ×0.5 | burn |
| Drench | `drench` | Speed ×0.5; 25% chance an action fails | (soak/slow) |
| Numb | `numb` | Speed ×0.5; 25% chance unable to act | paralysis |
| Doze | `doze` | asleep 1–3 turns (no charge spent on blocked turns) | sleep |
| Blight | `blight` | n/16 max HP chip, n+1 each turn it persists | bad poison |
| Dazzle | `dazzle` | 1/3 chance each turn to hit itself (40-power typeless, own atk vs def) | confusion |
| Chill | `chill` | can't act; 20%/turn thaw, or any Ember hit thaws | freeze |

One major status at a time (a second application fails); `fullHeal`/inn rest/
Cleanse cure; volatile counters (doze turns, blight stacks) reset on send-out;
status persists outside battle. Statuses also feed the catch `statusBonus`
(`04-capture.md`).

## Move-power bands

To keep numbers legible and balanceable, damaging moves snap to bands:

| Band | Power | Accuracy | Charges | Use |
|------|------:|--------:|--------:|-----|
| Quick | 40 | 100 | 30 | spammable, often +priority or rider effect |
| Light | 55–60 | 100 | 25 | reliable workhorse |
| Standard | 75–80 | 100 | 15–20 | the bread-and-butter STAB move |
| Heavy | 90–95 | 90–95 | 10–15 | strong, slightly risky |
| Nuke | 110–120 | 80–90 | 5–10 | big payoff, real downside |
| Desperate | 130–150 | 90–100 | 5 | recoil / recharge / self-debuff attached |

Status moves are costed by *impact*, not power (see ability/EPS scoring in
`02-stats-and-balance.md`).

## Coverage guarantee

The master pool guarantees, **for each of the 10 types**, a full ladder in
*both* damage channels (wave 2, 2026-06):

- physical: Quick (40) → Light (58) → Standard (78) → Heavy (92),
- special: Light (58) → Standard (78) → Heavy (92) → Nuke (115),
- plus 1 type-flavoured status/utility move.

Plus a shared bank of **Plain** moves and universal status/utility moves
(stat buffs, heals, hazards, screens, pivots) any kin may learn. This is what
lets us assign sensible 4-move sets to every species without inventing a move
per kin (signature moves excepted).

## Learnsets

Each species has:

```jsonc
"learnset": {
  "levelup": [ {"level": 1, "move": "ember_jab"}, {"level": 12, "move": "cinder_lash"}, ... ],
  "kindling": ["flare_crown"],     // moves taught on reaching this kindled form
  "tutor": ["ember_jab", "sun_nap"]// optional: extra Star-chart compatibility (see below)
}
```

Rules:

- A wild/caught kin comes with up to its last four level-up moves.
- On kindling, a kin may immediately learn its stage's `kindling` move(s).
- The **4-move cap** is enforced in the party UI: learning a 5th prompts the
  player to forget one (the genre's exact texture).
- **Signature moves** belong to one line only and are flagged
  `"signature": true` in `moves.json`. Thirteen exist: the starter pair
  (Vulpyre's *Tuft Spark*, Brinix's *Bubble Hum*) plus one per elemental apex —
  the Constellation Wardens and the story Tier-Fs (*Keystar Beam*, *Hollowing
  Hymn*, *Daybreak Lance*, …) — owners pinned in `build_species.py
  SIGNATURE_MOVES`, learned late (L44–52) so late bosses are hard through
  **kit**, not just level. Signatures are **excluded from the generic pools**
  in `autobuild.mjs`/`chart_check.mjs` (they'd skew fair fights) and from
  Star-chart printing; they count toward EPS movepoolScore.
- **Taught moves are Star-charts** (never "TMs"): single-use chart items that
  teach their move from the ITEMS menu. Compatibility is rule-based — the kin
  shares the move's type, the move is Plain, or it appears anywhere in the
  species learnset (the `tutor` array exists to grant *extra* compatibility
  beyond those rules, per species). Design, pricing tiers and distribution:
  [`10-economy.md`](./10-economy.md) §6.

## Abilities

Each kin has **one passive ability** (plus an optional **hidden ability**, the
genre's rare alt) — these gave the two sample kin (Emberheart, Tidecaller) much
of their identity. Abilities are scored for the power budget:

| Ability tier | EPS cost | Examples |
|--------------|---------:|----------|
| Minor | +10 | small conditional buffs (e.g. *Brisk*: +Speed in bright sun) |
| Standard | +20 | reliable edges (e.g. *Emberheart*: Ember moves stronger under ½ HP) |
| Strong | +30 | match-defining (weather setters, immunities, on-switch effects) |

Ability design rules:

- **No stacking two Strong effects** on one kin (ability + signature move).
- Abilities should reinforce the kin's **role and biome** (a Frost cave-dweller
  might have *Coldblood*: immune to Chill, heals in hail).
- Hidden abilities are rarer/stronger and reserved for kin caught in optional
  landmarks (ties into `06-progression-and-distribution.md`).

A starter bank of ~30 abilities ships in `moves.json` under an `"abilities"`
key (id, name, tier, effect, desc); species reference them by id.

## Why this is enough

The shipped pool (wave 2, 2026-06): 10 types × 9 moves (90) + 20
Plain/universal utility + 2 typed extras (Lifedrain, Sun Nap) + 13 signatures
= **125 moves** — the target this doc set, fully coverage-complete in both
channels, and small enough that every move can be hand-checked. Generated by
`tools/balance/gen_moves.py` into `moves.json`; after ANY pool change re-run
`validate.mjs`, `chart_check.mjs` and `simulate.mjs` (the fair-roster
guardrail is the binding gate). A second status move per type is deliberately
deferred until the status engine (battle-runtime-plan Part B) lands — the
simulator can't see status yet, so it would be uncosted.
