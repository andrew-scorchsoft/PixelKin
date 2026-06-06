# PixelKin — Kindling (the evolution system)

> We don't call it evolution. A kin grows by **kindling**: taking on more light
> and blazing into a brighter, stronger form — the same verb the whole game is
> about (you spend the story *re*kindling the constellations). It ties directly
> to the word "kin," to the lamp-tender theme, and to the central plot. A kin
> that has advanced has **kindled**; the act is a **Kindling**.
>
> (Alternatives considered and rejected: "Transmutation" — too alchemical/cold;
> "Glow-Up" — too modern/meme; "Waxing" — moon-only. "Kindling" won on theme
> fit. Changeable later via a single rename pass; the data field is `kindling`.)

## Line shapes

| Shape | Count target | BST path (tiers from `02`) | Example feel |
|-------|---:|----------------------------|--------------|
| **Single** (no kindling) | ~30 | one of C / D / E | standalone oddities, many rares & legendaries |
| **Two-stage** | most lines | B → D | starters and the bulk of the dex |
| **Three-stage** | ~18 lines | A → C → D (a few → E) | the "grew up with it" attachment lines |

Across the 151 this yields roughly: ~30 single + ~46 two-stage lines (92 kin) +
~10 three-stage lines (30 kin) ≈ 152 slots → trimmed to 151. (Tuned during
selection so the dex lands exactly on 151 with whole lines, never an orphaned
mid-stage.)

## Kindling triggers

Each kindling step lists a `trigger`. Supported kinds:

```jsonc
"kindling": {
  "into": 5,            // dex id of the next form
  "trigger": { "kind": "level", "level": 16 }
}
```

| `kind` | Params | Flavour / use |
|--------|--------|---------------|
| `level` | `level` | the default; kin kindles on reaching a level |
| `bond` | `min` | high **friendship** ("bonded" kin kindle out of trust) |
| `stone` | `item` | a **Kindlestone** is used (see below) |
| `location` | `area` | kindles inside a named area (e.g. Cinderhead crystals, the Starwell) |
| `time` | `level`, `when` | kindles at/after a level but only `day`/`night` |
| `linked` | `item:bond_lantern` | replaces the genre's *trade* evolutions for single-player (a **Bond Lantern** item, gifted by an NPC, completes the kindling) |

### Kindlestones

The genre's elemental evolution stones, themed as shards of fallen constellation
light. One per constellation element, sold/found near that element's region:

`Ember Kindlestone · Tide Kindlestone · Verdant Kindlestone · Stone Kindlestone ·
Storm Kindlestone · Frost Kindlestone · Solar Kindlestone · Lunar Kindlestone`

(No Light/Dark Kindlestones — those forms come from `bond`, `location`, or the
plot.)

## Branching kindlings — the Solar/Lunar hook

Some base kin **kindle in two directions**, and we lean the marquee branch into
the **day/night** axis, because it's pure Vesperholm flavour and teaches the
Solar↔Lunar type mirror:

```jsonc
"kindling": [
  { "into": 88, "trigger": { "kind": "time", "level": 28, "when": "day" } },   // Solar form
  { "into": 89, "trigger": { "kind": "time", "level": 28, "when": "night" } }  // Lunar form
]
```

A handful of lines branch by **Kindlestone** instead (e.g. a generic Sparkling
that becomes Ember *or* Frost depending on the stone). Branches are rare and
deliberate — they're collection bait ("you can only carry one path per save
unless you catch another base"), feeding the *collecting* pillar.

## Power & stat budget across a line

- Each stage sits in its tier band (`02`): the line's **role is preserved**, BST
  climbs A→C→D. A Special-Sweeper Sparkling grows into a Special-Sweeper final;
  stats scale by `targetBST/currentBST` then re-jitter.
- **Kindling level vs final BST**: higher-BST finals kindle **later** (so a
  Tier-E apex line might kindle at 36/54, a humble Tier-D line at 16/32). This
  keeps a freshly-kindled apex from steamrolling its level bracket.
- **No stage may exceed its tier ceiling**, and the **EPS** check (`02`) is
  applied to the *final* form (the one that sees competitive play).

## Learnset on kindling

- A kindled form may immediately learn its `kindling` move(s) (`03`).
- Kindled forms keep level-up moves they'd already have, and unlock higher-power
  band moves at later levels.
- Many lines gain their **signature move** only at the final stage — part of the
  payoff for sticking with a kin.

## Provenance & the "wow" curve

Kindling is the primary engine of the *attachment* and *awe* the brief asks for:

- Early lines kindle **early and visibly** (a cute Sparkling becomes a clearly
  cooler mid-form by ~L16), giving the player a fast first taste of growth.
- Apex/pseudo lines kindle **late and dramatically** (L36+), so a fully-kindled
  apex is a genuine flex — the kid-seeing-a-fully-grown-fire-lizard feeling,
  earned through the journey rather than handed over.
- A few **post-game** kindlings unlock only after the dawn returns (the story
  bible's Dawnstead day-forms), rewarding the long haul.

## Data hook

Per species in `src/game/data/species/`:

```jsonc
{
  "id": 4,
  "from": 3,                 // dex id this kindled from (null if base)
  "stage": 2,                // 1 = base, 2 = first kindling, 3 = second
  "kindling": { "into": 5, "trigger": { "kind": "level", "level": 32 } }  // null if final
}
```

`from`/`into` wire each line into a graph the engine and the simulator both
read; the validator (`tools/balance/`) checks every line is whole (no orphan
mid-stages, every `into` exists, BSTs climb monotonically, tiers legal).
