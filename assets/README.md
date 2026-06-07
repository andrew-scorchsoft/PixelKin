# assets/ — source of truth (not served)

This is the **editable master** tree. Nothing here is shipped to the player.
Vite only serves [`../public/`](../public/), so the game loads its **rendered /
packed** copies from `public/assets/` at runtime. Think of it as
**source → built output**:

| Source (here, `assets/`) | Built/served (`public/assets/`) | Made by |
|--------------------------|---------------------------------|---------|
| `audio/midi/*.mid` + `audio/midi/specs/*.json` | `audio/music/*.mp3` (rendered loops) | `generate-midi` |
| `creatures/NNN_slug/*.png` + `metadata.json` (layered sprite masters) | `sprites/…` (packed sheets) | `generate-sprite-sheet` |
| tile source art → `pack_tileset.py` | `tilesets/*.png` + `*.tileset.json` | `generate-sprite-sheet` |
| `pixelkin-logo.png` (logo master) | `ui/logo.png` (served copy) | brand kit |

> **Why two `assets/` folders, not one?** `public/` is the shipped bundle. Source
> `.mid` files, composition specs, and layered PNG masters must **not** bloat the
> player's download — but we must keep them so any track or sprite can be
> re-rendered later without recomposing. Keeping the masters out of `public/` is
> the whole point. (Standard Vite convention; the names match on purpose so a
> source file and its served output share a path tail.)

## What lives here

- **`audio/midi/`** — `.mid` masters + `specs/` (the JSON song specs) +
  `soundfonts/` (gitignored, re-fetched). See [`audio/midi/README.md`](audio/midi/README.md).
- **`creatures/NNN_slug/`** — per-kin sprite masters (`battle_front`, `battle_back`,
  `icon`, `overworld`, `portrait`) + `metadata.json` (canvas/anchor record). Only
  the first few exist; the full 151 are designed in `docs/mechanics/`.
- **`trainers/`** — player & NPC sprite masters (e.g. `player_indi`, `professor_fenn`).
- **`tilesets/world-palette.json`** — the shared world palette; derive per-area
  palettes from it so areas stay cohesive.
- **`pixelkin-logo.png`** — the logo master (the served copy is `public/assets/ui/logo.png`).
- **`concept-art/`** — inspiration **mood pieces** (one wide pixel-art key-art per
  area/route) — not shipped, not tilesets; a cohesive visual reference for each
  place, usable as an `--input-image` when generating that area's tiles. See
  [`concept-art/README.md`](concept-art/README.md).

## Rule of thumb

If a human edits or re-generates it, it belongs **here**. If the running game
loads it over HTTP, it belongs in **`public/assets/`**. Never hand-edit a file in
`public/assets/` that has a master here — change the master and re-render/re-pack.
