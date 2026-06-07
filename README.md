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

## The game so far

The design is largely settled and data-locked; the engine to play it is still
being built. What's already in the repo:

- **A world & story — *The Long Dusk*.** *Vesperholm*, a crescent of valleys
  around a darkened mountain where night fell and won't lift. You play a young
  lamp-tender's apprentice relighting the sky one constellation at a time,
  against **the Hollowing** — a sympathetic, never-cartoonish movement that wants
  a gentle permanent dark. Full cast, lore, and the 14-area world map live in
  [`docs/world/`](docs/world/).
- **Creatures & battles.** **151 original *kin*** across **10 elemental types**
  (Ember, Tide, Verdant, Stone, Storm, Frost, Solar, Lunar, Light, Dark), with
  six stats, ~94 moves + 28 abilities, capture via **Lamps**, and evolution via
  **Kindling**. The roster was curated from ~463 concepts and **empirically
  balanced** with a Monte Carlo simulator (every type lands a fair win-rate). The
  data is the source of truth in [`src/game/data/`](src/game/data/); the design
  and tooling are in [`docs/mechanics/`](docs/mechanics/) and
  [`tools/balance/`](tools/balance/).
- **An original soundtrack.** Loop-ready area and battle music for the world,
  composed via the repo's music skills into
  [`public/assets/audio/music/`](public/assets/audio/music/); the per-area plan
  is in [`docs/world/music-direction.md`](docs/world/music-direction.md).
- **A visual rulebook.** Canvas sizes, palette, anchors, and the sprite pipeline
  are binding in [`docs/art-style.md`](docs/art-style.md).

Everything here is **original** — inspired by the monster-collecting genre, a
copy of nothing. See the copyright rules in [`VISION.md`](VISION.md).

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
| Soundtrack plan | [`docs/world/music-direction.md`](docs/world/music-direction.md) |
| Mechanics & balance (start here) | [`docs/mechanics/00-overview.md`](docs/mechanics/00-overview.md) |
| The full dex (all 151 kin) | [`docs/mechanics/dex.md`](docs/mechanics/dex.md) |
| Art & sprite standards | [`docs/art-style.md`](docs/art-style.md) |

## Project layout

See [`CLAUDE.md`](CLAUDE.md) for the full directory map and conventions.
