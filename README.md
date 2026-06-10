# PixelKin

<p align="center">
  <img src="assets/pixelkin-logo.png" alt="PixelKin Diamond logo" width="420">
</p>

A retro, handheld-era **creature-collecting adventure** — web-first, built to
port cleanly to mobile. PixelKin sells a feeling: the wide-eyed wonder of
late-'90s handheld gaming, for the millennials who grew up on it.

👉 Start with **[`VISION.md`](VISION.md)** — what we're making and why, plus the
originality/copyright rules every contributor (human or AI) must follow.
For working in the repo, see **[`CLAUDE.md`](CLAUDE.md)**.

> ⚠️ **This is an experiment, not a finished game.** PixelKin was built by
> [Scorchsoft](https://www.scorchsoft.com) as a **capability experiment** — to
> see how far an AI-assisted workflow could take a game from a blank repo. The
> result is a **working but early-stage slice**: a real, playable engine and a
> fully designed world, story, and roster, but only the *first* sliver of that
> world is actually built out (a couple of areas, the first battle, placeholder
> creature art). It is **not** a final release, a complete game, or a polished
> product. See **[Project status](#project-status)** below for exactly what is and
> isn't done.
>
> 📄 **Licence:** source-available, **all rights reserved** — © Scorchsoft Ltd.
> This is *not* open source. Want to build on it? **[Talk to us first](#licence).**

<p align="center">
  <img src="assets/concept-art/areas/tinderwick.webp" alt="Tinderwick concept art" width="200">
  <img src="assets/concept-art/areas/lowleaf-hollow.webp" alt="Lowleaf Hollow concept art" width="200">
  <img src="assets/concept-art/areas/pale-vault-glacier.webp" alt="Pale Vault Glacier concept art" width="200">
  <img src="assets/concept-art/areas/nightreach-observatory.webp" alt="Nightreach Observatory concept art" width="200">
  <br>
  <sub><i>Concept mood-pieces from <a href="docs/world/atlas.md">Vesperholm</a> — Tinderwick · Lowleaf Hollow · Pale Vault Glacier · Nightreach Observatory</i></sub>
</p>

## The game so far

The design is data-locked **and the engine to play it now exists** — the first
hour is playable end-to-end: attract demo → title (New Game / Continue / Settings)
→ story intro where you're given a vesperlamp and **choose a starter** → explore
**Tinderwick**, talk to townsfolk, read signs, step into its homes, shop and
Lumenary chamber → earn the first
**Gleam** from Lampwarden Brisa Tallow in a real turn-based battle → head north
onto **Dimglass Coast** with wild encounters, your rival Wren's first friendly
battle, and the night the dusk deepens → across the **Dimglass tidal flats**
(route trainers and rising wild kin bridge the levels) → on to **Pearlmoor Quay**, the
moonlit Tide port, where Lampwarden Reyl Wash grants the **Tide Gleam** and the
**Tidecall** Lantern Gift — which opens the harbour's gated water, the **Gullcry
Rock** backtrack (a rare kin + the Tide Charm), and the **Vesper Crossroads**
Lanternway hub. Along the way: catch-gated Lumenary etiquette (Brisa won't battle
until you've befriended a wild kin), inn and hearth **rest-heals**, free shop
kits, item caches on the routes, and festival crowds that fill each town after
its Gleam is relit. Progress autosaves (with JSON
export/import), and the screen can show as a handheld-device frame, fullscreen with
translucent touch controls, or plain. Run it with `npm install && npm run dev`.

What's already in the repo:

- **A playable game engine** (Phaser 3 + TypeScript). Tile maps from our own JSON
  schema, grid movement, NPCs/signs/warps/cutscenes, a data-driven turn-based battle
  system, a **pause menu** (a party screen to inspect a kin's stats/moves and reorder
  who leads, **the Hearth** for kin storage, and an items screen to heal), and a
  flag/save layer behind the platform seam — all built on
  one in-canvas **UI design language** ([`src/game/ui/theme.ts`](src/game/ui/theme.ts))
  every screen shares. Engine code is in [`src/game/`](src/game/), the DOM
  screen-shells in [`src/shell/`](src/shell/); map/level-design rules are binding in
  [`docs/world/level-design.md`](docs/world/level-design.md), with SNES-style
  interior rules in [`docs/world/interiors.md`](docs/world/interiors.md).
- **A world & story — *The Long Dusk*.** *Vesperholm*, a crescent of valleys
  around a darkened mountain where night fell and won't lift. You play a young
  lamp-tender's apprentice relighting the sky one constellation at a time,
  against **the Hollowing** — a sympathetic, never-cartoonish movement that wants
  a gentle permanent dark. Full cast, lore, and the 14-area world map live in
  [`docs/world/`](docs/world/) — each area illustrated with a pixel-art **concept
  mood-piece** ([`assets/concept-art/`](assets/concept-art/)).
- **Creatures & battles.** **153 original *kin*** across **10 elemental types**
  (Ember, Tide, Verdant, Stone, Storm, Frost, Solar, Lunar, Light, Dark), with
  six stats, ~94 moves + 28 abilities, capture via **Lamps**, and evolution via
  **Kindling**. The roster was curated from ~463 concepts (151) and rounded out by
  the third starter line (Cloverkit → Cloverhart), all **empirically
  balanced** with a Monte Carlo simulator (every type lands a fair win-rate). The
  data is the source of truth in [`src/game/data/`](src/game/data/); the design
  and tooling are in [`docs/mechanics/`](docs/mechanics/) and
  [`tools/balance/`](tools/balance/). Battles read their backdrop from the map —
  subtle, per-area scenes (with a few variants each) instead of flat black.
- **An original soundtrack.** Loop-ready area and battle music for the world,
  composed via the repo's music skills into
  [`public/assets/audio/music/`](public/assets/audio/music/); the per-area plan
  is in [`docs/world/music-direction.md`](docs/world/music-direction.md).
- **A visual rulebook.** Canvas sizes, palette, anchors, and the sprite pipeline
  are binding in [`docs/art-style.md`](docs/art-style.md).

Everything here is **original** — inspired by the monster-collecting genre, a
copy of nothing. See the copyright rules in [`VISION.md`](VISION.md).

## Project status

PixelKin is an **early-stage capability experiment**, not a shippable game.
Treat the design docs as the *finished blueprint* and the code as a *first
vertical slice* that proves the engine works — most of the world described in
those docs has not been built yet.

**Done / works today:**

- A real, playable **engine** (Phaser 3 + TypeScript): tile maps, grid movement,
  NPCs/signs/warps, data-driven cutscenes, a turn-based **battle system**, the
  pause menu (party, the Hearth, items), and the save/flag layer.
- A complete, **data-locked design**: full story and world bible (14 areas), the
  153-kin roster with empirically balanced battle maths, the type chart, moves,
  and abilities — all authored and validated.
- A **playable opening slice**: attract demo → title → intro and starter choice →
  explore **Tinderwick** → first **Gleam** battle → north onto **Dimglass Coast**.
- An **original soundtrack** (area + battle loops) and the art/sprite pipeline.

**Not built yet / known gaps:**

- Only the **first ~2 of 14 areas** are actually built and walkable; the other
  regions, Lumenaries, and the late-game exist on paper (in `docs/`) only.
- **Creature sprites are still placeholder squares** in the title/starter/battle
  screens — the art pipeline exists but the in-game creature art isn't wired in.
- Only the **first Gleam / Lampwarden** is implemented; the rest of the gym/badge
  progression, Lantern-Gift gating, and the central hub are not.
- No mobile build yet (Capacitor is planned, not present), and many systems are
  first-pass rather than balanced-for-feel or content-complete.

In short: the **bones are real and the plan is complete**, but this is a demo of
*what the workflow can do*, not a finished product.

## Tech

TypeScript · [Vite](https://vitejs.dev) · [Phaser 3](https://phaser.io) —
with [Capacitor](https://capacitorjs.com) planned for the eventual mobile build
(the web `dist/` bundle becomes the mobile app).

## Quick start

```bash
npm install      # install dependencies
npm run dev      # dev server at http://localhost:5173
npm run build    # typecheck + production build to dist/
```

## Asset generation skills

Original art and music are generated via repo skills in `.claude/skills/`
(keys provided via environment; locally copy `.env.example` → `.env`):

```bash
python3 -m venv venv && ./venv/bin/pip install -r requirements.txt   # one-time

# original game music (ElevenLabs) into public/assets/audio/music/
./venv/bin/python .claude/skills/generate-music/scripts/generate_music.py --list-presets

# original art (Google Nano Banana Pro / OpenAI)
./venv/bin/python .claude/skills/generate-image/scripts/generate.py --list-styles
```

> All generated content must be **original** — inspired by the genre, a copy of
> nothing. See the copyright section in [`VISION.md`](VISION.md).

## Design & content docs

| Topic | Where |
|-------|-------|
| Vision & copyright rules | [`VISION.md`](VISION.md) |
| Story, cast, lore | [`docs/world/story-bible.md`](docs/world/story-bible.md) |
| World map (14 areas, routes, gating) | [`docs/world/atlas.md`](docs/world/atlas.md) |
| Area concept art (mood-pieces) | [`assets/concept-art/`](assets/concept-art/README.md) |
| Full walkthrough / user journey | [`docs/world/walkthrough/`](docs/world/walkthrough/README.md) |
| Soundtrack plan | [`docs/world/music-direction.md`](docs/world/music-direction.md) |
| Mechanics & balance (start here) | [`docs/mechanics/00-overview.md`](docs/mechanics/00-overview.md) |
| The full dex (all 151 kin) | [`docs/mechanics/dex.md`](docs/mechanics/dex.md) |
| Art & sprite standards | [`docs/art-style.md`](docs/art-style.md) |

## Project layout

See [`CLAUDE.md`](CLAUDE.md) for the full directory map and conventions.

## Licence

**Source-available, all rights reserved.** © 2026 **Scorchsoft Ltd**.

The code is public so you can read, learn from, and run it locally — but
publishing it here does **not** make it open source. No licence to copy, modify,
redistribute, or build a product on top of this code or its content (art, music,
text, world, and game data) is granted. See [`LICENSE`](LICENSE) for the full
terms.

Want to build on it, use it in your own project, or licence it? **Please get in
touch first** — [scorchsoft.com](https://www.scorchsoft.com).
