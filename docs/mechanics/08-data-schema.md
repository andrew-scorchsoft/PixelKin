# PixelKin — Data Schemas

> The contracts that keep 500 concepts, a selection pipeline, and 151 final
> records all interoperable. Lightweight **concept** schema for the brainstorm
> pool; full **species** schema for survivors.

## 1. Concept (pool entry)

Used for the 500 brainstormed candidates in
`docs/mechanics/concepts/pool/*.json`. Cheap to produce, rich enough to vote on.
Each pool file is a JSON array of these.

```jsonc
{
  "concept_id": "B03-017",        // "<batch>-<n>", globally unique
  "name": "Cindermote",           // original; no franchise echo (VISION.md)
  "types": ["Ember"],             // 1 or 2 of the 10 canonical types
  "role": "Glass Cannon",         // a role from 02-stats-and-balance.md
  "tier": "B",                    // target BST tier A..F
  "line": {
    "shape": "two-stage",         // single | two-stage | three-stage
    "stage": 1,                   // this concept's position in its line
    "kindles_into": "B03-018",    // concept_id of next form, or null
    "kindle_trigger": "level 16"  // short human note; formalised later
  },
  "region": "south",              // south|east|north|west|outer|central|post
  "rarity": "common",            // common|uncommon|rare|very_rare|legendary
  "concept": "A drifting hearth-ash sprite that flares when startled.",
  "visual": "Round ash-grey body, single ember-orange eye, trailing spark motes; tiny, readable silhouette.",
  "size_cm": 30,                  // rough height/length
  "weight_kg": 4,
  "signature_idea": null,         // optional one-line signature move pitch
  "hook": "Why a kid would love it — the charm/awe angle."
}
```

Authoring rules for concepts (given to every generation sub-agent):

- **Original, always.** No name, silhouette, or gimmick that reads as an
  existing franchise creature. Describe by genre and nature, never by brand.
- **Fit the slot** you were commissioned for (region/type/role/tier/rarity).
- **Whole lines:** if you pitch a stage-1, pitch its kindling(s) too, with
  consistent role and climbing tier.
- **Lore-aware:** lean on Vesperholm flavour (lamplight, constellations, the
  Hollowing) where natural.

## 2. Species (final record)

One JSON file per survivor in `src/game/data/species/NNN_slug.json` (NNN =
zero-padded dex id 001–151). A bundler emits the combined `species.json` the
game and simulator load. Shape:

```jsonc
{
  "id": 1,
  "slug": "vulpyre",
  "name": "Vulpyre",
  "types": ["Ember"],                 // 1 or 2 canonical types
  "role": "Special Sweeper",
  "tier": "B",
  "stats": { "hp": 56, "atk": 61, "def": 50, "spa": 65, "spd": 52, "spe": 72 },
  "bst": 356,                         // must equal sum(stats); in tier band
  "eps": 366,                         // computed power-budget score (02)
  "ability": "emberheart",            // id into moves.json "abilities"
  "hidden_ability": "brisk",          // id or null
  "catchRate": 175,                   // 1..255 (04)
  "kindling": {                       // null if final/single
    "into": 0,                        // dex id of next form
    "trigger": { "kind": "level", "level": 30 }
  },
  "from": null,                       // dex id this kindled from, or null
  "stage": 1,                         // 1=base, 2, 3
  "learnset": {
    "levelup": [ { "level": 1, "move": "tuft_spark" }, { "level": 7, "move": "ember_jab" } ],
    "kindling": [],
    "tutor": []
  },
  "dex": {
    "entry": "It dozes on sun-warmed stones and bolts at the first drop of rain...",
    "category": "Hearth-Fox Kin",     // the genre's "species" tagline
    "size_cm": 60,
    "weight_kg": 9.4,
    "habitat": "south"                // primary region
  },
  "encounters": [                     // where it appears wild (matches world schema)
    { "area": "tinderwick", "terrain": "tall_grass", "rarity": "common", "min": 2, "max": 4 }
  ],
  "art": {
    "silhouette": "Flame-crest + big triangular ears; passes the black-blob test at 32px.",
    "palette": "Tangerine body, cream muzzle/belly, ink outline, fire-orange crest with yellow core (~12 colours).",
    "direction": "Upright, alert, warm; body language reads 'fast'."
  },
  "provenance_concept_id": "B01-003"  // which pool concept it came from (audit trail)
}
```

### Validation (enforced by `tools/balance/validate.mjs`)

- `bst === sum(stats)` and within the band for `tier`.
- `eps` within ±25 of tier peers (02).
- Every `kindling.into` / `from` references a real id; **lines are whole**
  (no orphan mid-stages), BST climbs monotonically, tiers are legal for stage.
- All `types` in the canonical 10; all `ability`/move ids exist.
- `catchRate` in the tier's band (04).
- Each species used by some area's encounter table **or** flagged
  scripted/legendary.

## 3. Items (lamps & kindlestones) — stub

Authored with the inventory system later; shapes are specified in `04-capture.md`
(lamps) and `05-kindling.md` (kindlestones). Listed here so the schema set is
complete; not blocking for the roster work.

## 4. Type chart

Already authored: `src/game/data/type-chart.json` (see `01-type-system.md`).

## 5. Moves & abilities

Already authored: `src/game/data/moves.json` (see `03-moves.md`).
