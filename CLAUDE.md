# CLAUDE.md

Guidance for Claude Code (and humans) working in this repository.

## What this is

**PixelKin** — a retro, handheld-era creature-collecting adventure game.
Web-first, built to port cleanly to mobile later. Read **`VISION.md`** first:
it defines the feeling we're selling (nostalgia, collecting, exploration,
delight) and the **originality/copyright rules that are non-negotiable**.

> **Copyright, in one line:** inspired by the monster-collecting genre, a copy
> of nothing. Every creature, name, sprite, track, and line of text is
> original. Describe things by genre and mood, never by another brand. See the
> "Originality & copyright" section of `VISION.md`.

## Tech stack

- **TypeScript** + **Vite** (build/dev server).
- **Phaser 3** — 2D game framework (Canvas/WebGL), great fit for tile-based
  retro RPGs and runs inside a mobile webview unchanged.
- **Mobile (future):** the plan is **Capacitor** wrapping the same static
  `dist/` build. Nothing is installed for it yet — but we code for it now
  (see "Web-first, mobile-ready" below).
- **Python** — only for the asset-generation skills, isolated in `venv/`.

## Commands

```bash
npm install            # install JS deps (first time)
npm run dev            # Vite dev server at http://localhost:5173
npm run build          # typecheck + production build to dist/
npm run preview        # serve the production build
npm run typecheck      # tsc --noEmit
```

Python skills (image/music generation):

```bash
python3 -m venv venv && ./venv/bin/pip install -r requirements.txt   # first time
./venv/bin/python .claude/skills/generate-music/scripts/generate_music.py --list-presets
./venv/bin/python .claude/skills/generate-image/scripts/generate.py --list-styles
./venv/bin/python .claude/skills/generate-midi/scripts/midi.py presets
```

## Layout

```
assets/                     # master/source brand kit (logo). Not served.
public/                     # static files served as-is by Vite (base './')
  assets/
    sprites/  tilesets/  maps/  fonts/  ui/
    audio/music/  audio/sfx/   # generated audio lands here
src/
  main.ts                   # entry: boots Phaser
  game/
    config.ts               # resolution (240×160), tile size, palette
    scenes/                 # Boot -> Preload -> Title (World/Battle next)
    entities/               # Player, NPC, Kin classes
    systems/                # battle, party, inventory, save, dialogue
    data/                   # data-driven defs: species, moves, type chart
    ui/                     # HUD, dialogue boxes, menus
  platform/                 # platform seam (storage now; input/audio later)
  styles/                   # global.css
docs/                       # design docs as mechanics firm up
.claude/skills/             # repo skills (see below)
VISION.md                   # the game's vision + copyright rules
```

Path aliases (see `tsconfig.json` / `vite.config.ts`): `@/*` → `src`,
`@game/*` → `src/game`, `@platform/*` → `src/platform`.

## Asset generation skills

Four skills live in `.claude/skills/`. Use them instead of hand-rolling:

- **generate-image** — creature/UI/tileset art via Google Nano Banana Pro
  (preferred) or OpenAI. Briefs must be original; never reference another
  franchise. Output as repo-friendly WebP/PNG.
- **generate-music** — original background music/jingles via the ElevenLabs
  Music API (text-prompt → produced audio). Instrumental, loop-minded,
  preset-driven. Writes mp3 into `public/assets/audio/music/`.
- **generate-midi** — original, era-authentic **chiptune/MIDI** music that
  Claude *composes* as note data. Builds real `.mid` (honouring each platform's
  voice budget and looping conventions) and renders it with a built-in chip
  synth to `.mp3`. Offline, no API key. Use for true retro/MIDI; use
  generate-music when you want a text-prompt render instead.
- **copy-editing** — for any prose deliverable (docs, dialogue review,
  marketing copy).

API keys are provided as environment variables in this project's managed
environment (`GOOGLE_AI_STUDIO_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`).
Locally, copy `.env.example` to `.env`. **Never commit `.env` or keys.**

## Web-first, mobile-ready conventions

The point is that the web build *is* the mobile build later. So:

- Render at the fixed internal resolution and let `Scale.FIT` upscale —
  never hard-code window pixel sizes.
- Support **both** keyboard and pointer/touch input for anything interactive.
- Go through the **`src/platform/`** seam for anything device-specific (saves
  via `platform/storage.ts`, not `localStorage` directly). When we add
  Capacitor, we swap the backend, not the game.
- Keep the build a self-contained static bundle (`base: './'` in Vite) so a
  webview can serve it from a file origin.

## Conventions

- Pixel art only; `pixelArt: true` is on — keep art crisp, no smoothing.
- Game content is **data-driven** (`src/game/data/`): a new kin/move is a data
  edit, not new code. This also keeps original content cleanly separated.
- Match the surrounding code's style. Strict TypeScript is on.

## Git

- Develop on the feature branch you were given; commit with clear messages;
  push to that branch. Don't open PRs unless asked.
