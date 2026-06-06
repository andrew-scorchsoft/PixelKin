# Sample Kin & Characters

Worked examples that exercise the **Art & Sprite Bible** (`art-style.md`) and the
`generate-sprite-sheet` skill end to end. These two kin and two characters are
drawn from the three creatures above the PixelKin logo, given names, types,
stats, and a full sprite set — a reference for how a real dex entry comes
together, and a smoke-test for the asset pipeline.

> Example content. Stats/lore here are illustrative; the canonical game data
> will live in `src/game/data/` once the battle system firms up. All original
> to PixelKin (VISION.md).

---

## #001 Vulpyre — the Ember Fox

*Fire kin. The brave, restless one.*

A spark-tailed fox cub whose flame-crest flares brighter the more excited it
gets. Loyal and impatient in equal measure.

- **Type:** Fire
- **Role:** fast special attacker (a "glass-cannon" starter)
- **Ability:** *Emberheart* — Fire moves hit harder when Vulpyre is below half
  HP. *(Hidden: Brisk — speed rises in bright sun.)*
- **Signature move:** *Tuft Spark* — a quick, low-power Fire jab that almost
  always strikes first.

| HP | Atk | Def | Sp.Atk | Sp.Def | Spd | Total |
|---:|----:|----:|-------:|-------:|----:|------:|
| 56 |  61 |  50 |     65 |     52 |  72 |   356 |

**Dex entry:** *"It dozes on sun-warmed stones and bolts at the first drop of
rain. When a Vulpyre trusts you, its mane burns a steadier gold."*

### Asset-design notes
- **Silhouette:** the flame-crest + big triangular ears give an instantly
  readable outline — passes the "black blob" test even at the 32px icon size.
- **Palette:** tangerine body, cream muzzle/belly, ink outline, with the
  flame-crest using the brand `fire` accent (`#ff8a3d`) and a brighter yellow
  core. ~12 colours, GBC-restrained.
- **Anchor:** bottom-centre on the battle sprites so the cub "stands" on the
  battle line; the icon is head-focused (crest + face) since the body detail
  vanishes at 32px.

---

## #002 Brinix — the Finling

*Water kin. The calm, buoyant one.*

A round little water-sprite with a swept-back fin-crest and fan-shaped cheek
fins. Where Vulpyre rushes, Brinix drifts.

- **Type:** Water
- **Role:** bulky special wall (soaks hits, wears foes down)
- **Ability:** *Tidecaller* — restores a sliver of HP each turn in rain or
  water terrain. *(Hidden: Mistveil — harder to hit on the turn it switches in.)*
- **Signature move:** *Bubble Hum* — a soothing Water pulse that can lower the
  target's Attack.

| HP | Atk | Def | Sp.Atk | Sp.Def | Spd | Total |
|---:|----:|----:|-------:|-------:|----:|------:|
| 62 |  53 |  58 |     60 |     64 |  55 |   352 |

**Dex entry:** *"Its side-fins glow softly in deep water. Brinix hums a bubbling
tune that settles nervous kin, and rides fast currents purely for the fun of
it."*

### Asset-design notes
- **Silhouette:** the single horn-like fin-crest is the signature read; the
  orange cheek-fins add a warm contrast spot against the cool blue body.
- **Palette:** sky-blue body, white belly, ink outline, brand `water` accent
  (`#4fb4ff`) for shading and the `fire`-adjacent orange on the fins for pop.
- **Anchor:** bottom-centre; sits a touch lower and rounder than Vulpyre, which
  reads as "heavier / bulkier" — a subtle way stats echo in the art.

---

## Vulpyre vs Brinix — the starter contrast

They're deliberately a study in opposites, so a new player *feels* the choice:

| | Vulpyre | Brinix |
|---|---|---|
| Tempo | fast, aggressive | slow, defensive |
| Stat lean | Speed / Sp.Atk | HP / Sp.Def |
| Body language | upright, alert | rounded, settled |
| Colour temperature | warm | cool |

---

## Characters (overworld)

### Indi — the player
A plucky young kin-catcher, around twelve. Hood down over tousled brown hair, a
teal jacket with a bright yellow zip, red boots, a small olive backpack. The
**hood-not-a-cap** choice is deliberate — it keeps the protagonist clearly
*ours* and away from genre-cliché trainer silhouettes (VISION.md).

- Asset: `human-overworld` walk sheet (3×4, bottom-centre anchor). Feet share a
  baseline across all twelve frames so the walk cycle reads cleanly.

### Professor Fenn — the mentor
A warm, scholarly researcher in his fifties: grey swept-back hair, round
spectacles, a long olive field coat. The long coat gives a distinct,
instantly-readable overworld silhouette next to the smaller player sprite.

- Asset: `human-overworld` walk sheet (3×4, bottom-centre anchor).

---

## How these were generated

Every asset came from the `generate-sprite-sheet` skill (Google Nano Banana Pro),
using a **crop of each creature from the logo as a `--reference`** so the
sprites stay faithful to the established art, e.g.:

```bash
./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/generate_sprite.py \
  --type creature-front --reference <logo-crop>.png \
  --creature-id 1 --creature-slug vulpyre \
  --subject "Vulpyre, an original fire-type fox cub: …"
```

Sprites land under `assets/creatures/NNN_slug/` with a `metadata.json` carrying
each sprite's geometry and anchor. Fill in `types` and (later) wire the stats
above into `src/game/data/`.
