# PixelKin — From 500 Concepts to the Final 151

> How we overshoot then curate. Generate ~500 concepts, score them like a panel
> of veteran designers, then run a **distribution-constrained** selection so the
> final 151 are not just individually great but collectively balanced and
> well-placed. Cut concepts are archived, never deleted.

## Pipeline overview

```
 [ commission slots ] → [ ~14 generation sub-agents ] → pool/*.json (~500)
        │                                                      │
        ▼                                                      ▼
 region/type/role/tier/rarity quotas                  [ panel scoring ]  (rubric, 0–100)
                                                              │
                                                              ▼
                                          [ constrained selection ]  (hit quotas, keep whole lines)
                                                              │
                                            ┌─────────────────┴─────────────────┐
                                            ▼                                     ▼
                                 src/game/data/species/ (151)        concepts/archive/ (the rest)
```

## Stage 1 — Commissioned generation (overshoot to ~500)

Concepts are not generated blind. Each generation sub-agent gets a **slot
brief** derived from `06`'s region/type/level/rarity tables, so the pool already
clusters where the world needs creatures. We commission **~150% of every slot**
so selection always has 2–4 strong candidates to choose between.

Each sub-agent: writes a `pool/batch-NN.json` array of concepts (schema in `08`),
returns only a count + the slot it covered (keeps orchestration context small).

## Stage 2 — Panel scoring (the "veterans in a room")

We emulate a panel of senior monster-RPG + JRPG designers via **scoring
sub-agents**, each grading whole batches against a fixed rubric so scores are
comparable. Every concept gets a score **0–100**:

| Criterion | Weight | What earns marks |
|-----------|:---:|------------------|
| **Originality / IP-safety** | 25 | reads as its own thing; no franchise echo (VISION.md). A hard gate: anything that smells derivative is scored ≤40 and effectively cut. |
| **Charm / awe** | 20 | the "kid would love this" factor; right emotional register for its tier (cute early, awesome late). |
| **World fit** | 15 | belongs in Vesperholm's lamplight/constellation/Hollowing setting and its commissioned region. |
| **Design clarity** | 15 | strong readable silhouette at 32–64px; a clear role identity. |
| **Mechanical interest** | 15 | type/role/ability/signature combo is fun and not broken (EPS-sane). |
| **Name quality** | 10 | original, pronounceable, evocative, fits the syllable-meld house style (Vulpyre, Brinix…). |

Rules to keep scoring honest:

- Each batch is scored by **two independent scorer agents**; we average, and
  flag any concept where the two disagree by >20 for a tie-break pass.
- Scorers must **rank within each commissioned slot** as well as score, so
  selection has an ordinal preference even when raw scores cluster.
- Pre-named atlas kin (Wickmoth, Sporeling, Glostern, etc. — ~30 already in
  `docs/world/atlas.md`) enter the pool **pre-seeded** and get a +world-fit
  nudge: they're already canon, so they're strongly favoured for their slots.
- The two existing starters (Vulpyre #1, Brinix #2) are **auto-included** (not
  scored out) — they have art and metadata already.

## Stage 3 — Constrained selection (balance, not just quality)

A picker script (`tools/balance/select.mjs`) reads all scored concepts and
chooses 151 subject to hard constraints — because the best-scoring 151
individually would *not* be a balanced dex (too many cool late apexes, not
enough humble early commons, lopsided types).

Hard constraints:

1. **Primary-type quotas** from `06` (Verdant 17, Storm 17, … Dark 13 = 151),
   ±1 tolerance.
2. **BST-tier quotas** from `02` (A≈22, B≈34, C≈26, D≈50, E≈13, F≈6).
3. **Whole lines only** — selecting a final pulls in its base/mid; never an
   orphan mid-stage. (Lines are scored as a unit = avg of members + bonus for a
   coherent arc.)
4. **Region coverage** — every area in `06` gets enough common/uncommon kin to
   fill its encounter tables; every region's two anchor types are represented.
5. **Coverage reachability** — the `01`/`06` guarantee: each Lampwarden has an
   obtainable super-effective answer before it.
6. **Fixed slots** — Vulpyre #1, Brinix #2, the 8 Constellation Wardens, the
   legendaries (Keylumen, the Null apex), the Lampling mascot.

Within those constraints, the picker **maximises total panel score** (a greedy
fill by descending score per slot, with backtracking when a quota would be
violated). Output: the 151 chosen lines + a selection report
(`selection-report.md`) showing every quota hit and why each cut line lost to
its slot winner.

## Stage 4 — Flesh-out & archive

- **Survivors** are expanded from concept → full species record (`08`) by
  flesh-out sub-agents (stats per role/tier template, learnsets from the move
  pool, wired kindling chains, dex/size/weight, art direction, encounter
  placement). Written to `src/game/data/species/NNN_slug.json`, dex ids assigned
  by region order so the dex *reads* as a journey (1–~40 south/east, etc.).
- **Cut concepts** are moved verbatim to
  `docs/mechanics/concepts/archive/` (grouped by why-cut: `lost-slot`,
  `off-quota`, `low-score`) with their scores — a reusable idea bank for future
  regions/DLC, never thrown away.

## Stage 5 — Validate & iterate

- `validate.mjs` checks every species against the `08` schema + budget rules.
- `simulate.mjs` runs the Monte Carlo (see `02`, `09`) on the final 151; any
  type/species outlier is fixed per the `02` fix-order and re-run until the
  guardrails pass.
- The final balance report ships as `docs/mechanics/balance-report.md`.

## Why overshoot at all

500→151 means **every** dex slot is a *winner of a small contest*, not the first
idea that fit. It also leaves a 349-strong, pre-scored idea bank for later
content. The cost is bounded: concepts are lightweight (schema in `08`), agents
write to disk and return summaries, and scoring is batched — so the orchestrator
never holds 500 records in context at once.
