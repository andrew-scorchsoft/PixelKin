# PixelKin — Balance Tooling

> All in `tools/balance/`. Pure Node.js (ESM `.mjs`) + Python, **zero npm
> dependencies** — runs anywhere Node 18+ and Python 3 are present. The JSON
> data files are the single source of truth for both the game and these tools.

## Files

| File | Lang | What it does |
|------|------|--------------|
| `gen_moves.py` | py | generates `src/game/data/moves.json` from the spec in `03` |
| `lib.mjs` | js | shared engine: type chart, stat/damage formulas, a compact 1v1 battle, seeded RNG |
| `autobuild.mjs` | js | auto-assigns a sensible 4-move set to a species (so the roster is testable before/with hand-authored learnsets) |
| `chart_check.mjs` | js | validates the **type chart** on a synthetic fair roster (used to tune `01`) |
| `aggregate_pool.py` | py | validates + combines the ~500 concept pool, dedupes, checks lines |
| `select.py` | py | constrained 500→151 selection (panel scores + quotas) → `selected.json`, archive, report |
| `simulate.mjs` | js | **full-roster Monte Carlo**: per-type win-rates, outliers, tiers, coverage |
| `validate.mjs` | js | schema + power-budget + whole-line checks on the final 151 |

## Running

```bash
# 1. (re)generate the move pool
python3 tools/balance/gen_moves.py

# 2. sanity-check the type chart itself (synthetic fair fights)
node tools/balance/chart_check.mjs 60000 12345

# 3. aggregate + validate the concept pool
python3 tools/balance/aggregate_pool.py

# 4. select the 151 (after panel scoring)
python3 tools/balance/select.py

# 5. validate + simulate the final roster
node tools/balance/validate.mjs src/game/data/species.json
node tools/balance/simulate.mjs src/game/data/species.json 80000 777
```

## The battle model (deliberately compact)

`battle1v1` runs a turn loop: faster base Speed acts first; each side's "AI"
picks the move with the highest **expected damage** (type chart × STAB × accuracy
× stat ratio); damage uses the canonical formula from `02` with the `[0.85,1.0]`
roll; a turn cap resolves stalls by remaining HP%. Status moves and abilities are
**excluded from the chart-balance harness on purpose** — so a win-rate skew is
attributable to the *type chart and stats*, not to a clever ability. The full
roster sim can layer abilities/status in later without changing the core proof.

Everything fights at a **flat level on base stats** (no IV/EV/temperament). That
is intentional: we balance the *structural* core; per-individual variance (`02`)
is seasoning applied only in the live game.

## What "balanced" means here (the guardrails)

From `02`, enforced by `chart_check.mjs` / `simulate.mjs`:

1. **Type win-rate spread** within ~45–55%. (The tuned chart lands every type at
   46.7–53.3% on the synthetic fair roster — see `01`.)
2. **No within-tier species outlier** more than ~18pp from its tier mean.
3. **Offensive coverage**: every type has a super-effective STAB answer present
   in the roster.
4. **Speed not clustered** at a single value.

When a guardrail fails, fix in this order (from `02`): distribution/rarity →
outlier species stats → (last resort) one type-chart cell. Re-run and repeat.

## Reproducibility

All randomness goes through a **seeded** mulberry32 RNG (`rng(seed)`), so every
report is reproducible: same seed + same data ⇒ same numbers. Reports cite their
seed and battle count.
