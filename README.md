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

## Project layout

See [`CLAUDE.md`](CLAUDE.md) for the full directory map and conventions.
