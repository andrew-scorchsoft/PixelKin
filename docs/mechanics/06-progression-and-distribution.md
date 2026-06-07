# PixelKin — Progression, Distribution & the "Awe Curve"

> How the 151 are spread across Vesperholm so the journey *feels* right: humble
> kin early, jaw-dropping rares late, every Lampwarden beatable with what you
> could have caught by then. Grounded in `docs/world/atlas.md` and
> `docs/world/story-bible.md`.

## Region → type → level map

The eight Lampwardens already pin each region to elements; the level bands give
the difficulty ramp. (Areas from the atlas; "secondary" types appear as
dual-types or rarer spawns.)

| Order | Region / area | Primary types | Secondary | Wild levels | Lampwarden cap |
|------:|---------------|---------------|-----------|:-----------:|:--------------:|
| start | Tinderwick / Dimglass Coast | Ember, Tide | Light | 2–7 | — |
| 1 | Pearlmoor Quay & shoals | Tide | Ember, Light | 6–12 | Reyl ~L14 |
| — | (1st gym is Brisa/Ember in Tinderwick) | Ember | — | — | Brisa ~L11 |
| 2 | Lowleaf Hollow (forest) | Verdant | Light, Stone | 12–18 | Sable ~L20 |
| 3 | Cinderhead Mine (cave) | Stone | Storm, Ember | 16–24 | Otho ~L26 |
| 4 | Galehigh Terraces | Storm | Light, Stone | 24–32 | Mira ~L33 |
| 5 | Windward Stair / Pale Vault | Frost | Storm | 30–40 | Ysolde ~L40 |
| 6 | Sunken Solarium | Solar | Verdant, Tide | 38–46 | Lucan ~L47 |
| 7 | Nightreach Observatory | Lunar | Light, Frost | 44–50 | Nessa ~L52 |
| 8 | Coldfog Marches | Dark | Lunar, Storm | 46–54 | — |
| hub | Vesper Crossroads | Light | — | safe | (Lampling here only) |
| end | Penumbra Ring / Umbral Spire | Dark, Light | — | 55–62 | Warden Còr (boss) |
| post | Dawnstead (post-dawn) | day-forms | all | 50–70 | — |

Note the **gym order ≠ strict difficulty of types**: Ember/Tide bookend the easy
south; Solar/Lunar/Dark sit late, matching their premium/swingy chart profiles
(`01`). A player naturally meets the gentle types first and the high-variance
celestial types only once they can handle them.

## Primary-type roster targets (sums to 151)

Each kin has a **primary type** for distribution accounting (dual-types still
broaden coverage). Targets:

| Type | Count | | Type | Count |
|------|---:|--|------|---:|
| Verdant | 17 | | Frost | 15 |
| Storm | 17 | | Light | 15 |
| Ember | 16 | | Solar | 13 |
| Tide | 16 | | Lunar | 13 |
| Stone | 16 | | Dark | 13 |
| | | | **Total** | **151** |

Verdant/Storm run highest (big, varied early/mid biomes); Solar/Lunar/Dark
lowest (rare, late, premium). ~55–60% of the 151 are **dual-typed** to enrich
the matchup space beyond ten rows. Roughly **40 of the 151 are single-stage**,
the rest belong to kindling lines.

## Rarity tiers & encounter weighting

Every wild placement carries a rarity that sets its `weight` in the area's
`EncounterZone.table` (schema already in `src/game/data/world/types.ts`):

| Rarity | Table weight | Share of a zone | Typical BST tier | Catch feel |
|--------|:---:|:---:|:---:|------|
| Common | 45–60 | ~55% | A / B | bread-and-butter |
| Uncommon | 20–30 | ~30% | B / C | a nice find |
| Rare | 8–15 | ~12% | C / D | grin-inducing |
| Very rare | 2–5 | ~3% | D / E | "did I just see that?!" |
| Landmark/scripted | — | spurs only | E / F | the trophy |

Tier-E/F kin are **almost never** in open-route tables; they live in **optional
spurs, landmarks, and scripted encounters** (the atlas lists ~12 of these:
Gullcry Rock, Tideglass Cavern, Wind-Eye, Aurora Hollow, Helia Vault, Starwell,
Hollowfen Stillworks, …). Exploration, not grinding, is how you get the trophies
— serving the *exploration* + *collecting* pillars together.

## The "awe curve" (provenance)

The deliberate emotional ramp the brief asks for — a kid should *feel* a kin's
power before reading a stat:

1. **South (early):** rounded, cute, low-BST Sparklings & starter bases. Friendly
   silhouettes, warm palette. Big heads, small bodies (art bible's cuteness).
2. **East/North (mid):** kin start kindling into cooler mid-forms; first Tier-D
   finals appear as rares. Silhouettes get bolder, more spikes/wings/crystals.
3. **West/Coldfog (late):** Solar/Lunar/Dark apexes — large, dramatic, premium
   palettes (the diamond-cyan + accent pop). These read as "endgame" on sight.
4. **Spire/post-game:** legendaries and Dawnstead day-forms — singular,
   awe-first designs.

Levers that encode "awe" without just inflating numbers: **size/weight**
(apex kin are visibly bigger/heavier in their dex data), **encounter rarity**,
**catch difficulty**, **late kindling levels**, and **silhouette drama** in the
art brief. (Size & weight are real dex fields on every species — see the schema
in `08-data-schema.md`.)

## Starters

Three, given by Professor Fenn in Tinderwick, completing the classic triangle
(the type chart's core Ember→Verdant→Tide cycle, so the rival pick matters):

| Dex | Name | Type | Line | Notes |
|----:|------|------|------|-------|
| 1 | **Vulpyre** | Ember | 2-stage (B→D) | exists; Special Sweeper |
| 2 | **Brinix** | Tide | 2-stage (B→D) | exists; Special Wall |
| 3 | **(Verdant starter)** | Verdant | 2-stage (B→D) | to be chosen in selection |

(Vulpyre & Brinix also appear as low-level wild kin in Tinderwick's existing
encounter table — fine; their starter forms are the same species.)

## Legendary & sub-legendary framework

Maps the "relight 8 constellations" plot onto catchable kin:

- **8 Constellation Wardens** — one sub-legendary kin per element (Tier E),
  each the luminous anchor of its constellation, caught in that region's
  late/optional landmark. They're the "rare powerful one per area" the brief
  wants. (~8 of the Tier-E budget.)
- **Keylumen** (Light, **Tier F**) — the Keystar-kin, the story's central
  legendary, scripted in the Umbral Spire (already named in the atlas).
- **The Null apex** (Dark, **Tier F**) — Warden Còr's drained legendary, the
  final-boss kin.
- **1–2 post-game legendaries** (e.g. a Dawn legendary unlocked after the dawn
  returns) round out the ~6 Tier-F budget.

All legendaries: very low `catchRate`, scripted one-per-save, late levels.

## Coverage reachability (a balance guarantee)

The simulator + a static check confirm that **before each Lampwarden**, the
player could realistically have caught kin that hit that warden's types
super-effectively. Example: before Otho (Stone, gym 4), the player has had
access to Tide and Verdant kin (both ×2 vs Stone) since the south/east. No gym
is a type wall with no obtainable answer. Failures here are fixed by adjusting
**where** a counter-type kin spawns, not by nerfing the gym.

## This doc as a generation brief

The region→type→level→rarity tables above are the **input contract** for the
concept-generation phase: each batch of concepts is commissioned for a specific
region/type/role/tier/rarity slot, so the 500 concepts already cluster around
where the world needs them — and selection (`07`) only has to pick the best of
each cluster, not retrofit a pile of unplaceable creatures.
