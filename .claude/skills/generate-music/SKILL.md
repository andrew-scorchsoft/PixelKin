---
name: generate-music
description: Generate background music and jingles for the game via the ElevenLabs Music API. Use whenever the user asks for music, a theme, a soundtrack, a loop, a battle/town/overworld track, a victory fanfare, or any musical audio asset that should be saved into the repo. Composes instrumental, loop-minded tracks from a text prompt, supports a mood preset library (overworld, town, battle, boss, victory, cave, title, emotional), and writes an mp3 ready for Phaser to load. Does NOT generate sound effects or speech.
---

# generate-music

A skill for producing music that fits PixelKin's handheld-era, nostalgic feel
(see `VISION.md`). The heavy lifting is a single Python script that calls the
ElevenLabs Music API; this document tells you when and how to use it.

## When to use

- The user asks for music, a theme, a soundtrack, a loop, or a jingle.
- A scene needs background music (overworld, town, battle, cave, title, etc.).
- An existing track needs regenerating in a different mood, tempo, or length.

Do **not** use this for: sound effects (menu blips, hit sounds, cries) or
spoken dialogue — those are different ElevenLabs products, not the Music API.

## Prerequisites

- `ELEVENLABS_API_KEY` must be set in the environment (or a `.env` at the repo
  root). It already is in this project's environment.
- The script needs `requests`, which comes in via the project's
  `requirements.txt`. **Always invoke via the project venv** —
  `./venv/bin/python ...` from the repo root. If the venv doesn't exist yet:
  `python3 -m venv venv && ./venv/bin/pip install -r requirements.txt`.

## Usage

List the mood presets:

```
./venv/bin/python .claude/skills/generate-music/scripts/generate_music.py --list-presets
```

Generate a looping overworld theme into the game's music folder:

```
./venv/bin/python .claude/skills/generate-music/scripts/generate_music.py \
  --prompt "bright route theme for the first grassland area" \
  --preset overworld \
  --length 40 \
  --output public/assets/audio/music/overworld.mp3
```

A short victory fanfare (jingle, not a loop):

```
./venv/bin/python .claude/skills/generate-music/scripts/generate_music.py \
  --prompt "win jingle after a creature battle" \
  --preset victory --length 7 \
  --output public/assets/audio/music/victory.mp3
```

### Options that matter

- `--preset` — appends a mood brief tuned to the game's style. Strongly
  preferred over free-form prompts so tracks stay consistent. See
  `scripts/presets.json`.
- `--length SECONDS` — 3–600. Omit to let the model choose. Keep loop tracks
  ~30–60s and jingles ~5–10s. (Composition plans cap at 300s; prompt mode at 600s.)
- `--vocals` — off by default. Game loops should stay **instrumental**; only
  pass this if the user explicitly wants singing.
- `--seed` — reproducible output; reuse a seed to iterate on a near-identical track.
- `--model` — defaults to `music_v1` (the only model on the public API today).
  Override with `--model` or `ELEVENLABS_MUSIC_MODEL` when Music v2 reaches the
  API on this account — no code change needed.
- `--output-format` — defaults to `mp3_44100_128` (works on all tiers).
  `mp3_44100_192` needs Creator tier or above.

## Workflow

1. Pick the closest `--preset` for the scene.
2. Write a short, concrete `--prompt` (the area/feeling), set a sensible
   `--length`, and write into `public/assets/audio/music/`.
3. The script prints JSON (path, size, model, settings). **Listen to / check the
   result.** If it doesn't fit the brief, adjust the prompt or preset and
   re-run. The script does not self-verify.
4. Queue the track in `PreloadScene` (`this.load.audio('overworld', 'assets/audio/music/overworld.mp3')`).

## Style & licensing notes

- Keep everything in the nostalgic handheld-RPG register described in
  `VISION.md`: chiptune-leaning, hummable, warm, loopable.
- **Never** prompt for "music that sounds exactly like <franchise>'s theme" or
  name a copyrighted track/composer to imitate. Describe the *mood and era*, not
  a specific existing work. This keeps the soundtrack original and clear of the
  copyright concerns set out in `VISION.md`.
