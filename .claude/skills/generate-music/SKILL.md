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
- `--length SECONDS` — 3–600. Omit to let the model choose. For an area LOOP,
  render LONGER than the loop you want (~80–90s) and cut the loop out with
  `tools/audio/make_loop.py` (see "Making it loop"); jingles ~5–10s.
- `--vocals` — off by default. Game loops should stay **instrumental**; only
  pass this if the user explicitly wants singing.
- `--seed` — reproducible output; reuse a seed to iterate on a near-identical track.
- `--model` — defaults to `music_v2_5` (checked against the API reference
  2026-10: `music_v1` | `music_v2` | `music_v2_5`; the API's own default is still
  v1, which is noticeably weaker). Override with `--model` or
  `ELEVENLABS_MUSIC_MODEL`. **Re-check the live API reference before relying on
  this** (`elevenlabs.io/docs/api-reference/music/compose`) — it moves fast.
- **Concurrency:** this account allows **2 requests at once** (a third gets 429
  `concurrent_limit_exceeded`). Generate in pairs; the script backs off on 429.
- `--output-format` — defaults to `mp3_44100_128` (works on all tiers).
  `mp3_44100_192` needs Creator tier or above.

## Workflow

1. Pick the closest `--preset` for the scene.
2. Write a short, concrete `--prompt` (the area/feeling), set a sensible
   `--length`, and write into `public/assets/audio/music/`.
3. The script prints JSON (path, size, model, settings). **Listen to / check the
   result.** If it doesn't fit the brief, adjust the prompt or preset and
   re-run. The script does not self-verify.
4. For an area loop, cut it seamlessly (below) and A/B it against the current
   track before wiring it in — never overwrite a served track unapproved.
5. Queue the track in `PreloadScene` (`this.load.audio('overworld', 'assets/audio/music/overworld.mp3')`).

## Making it loop

The engine loops the WHOLE file end→start, and a text-to-music render is a
performance (pickup, drifting level, a fade at the end) — not a loop. Prompt for
loop-friendliness anyway (state BPM, key, bar count; "starts directly on the
theme, no intro, no outro, no fade, no ritardando"; the docs' own loop advice is
"state the bars, BPM, key and what's excluded"), then:

```bash
python3 tools/audio/make_loop.py raw.mp3 --report          # tempo, best loop points, seam score, head/tail level
python3 tools/audio/make_loop.py raw.mp3 loop.mp3          # cut audio[s:e], blend the seam (250 ms)
```

It searches for a start/end pair whose next few seconds match (chroma + timbre +
loudness), preferring whole multiples of 4 bars. Seam distance: a hand-built loop
scores ~0.03; ≤0.4 is a clean ElevenLabs cut, >1 means pick another take. Ask for a
tempo the model can hold (it hit 92 BPM exactly on the Tinderwick test). Preview
the join by playing the loop twice (decode to PCM and concatenate — `-stream_loop`
re-encoding adds an MP3 gap that isn't in the game).

## Style & licensing notes

- Keep everything in the nostalgic handheld-RPG register described in
  `VISION.md`: chiptune-leaning, hummable, warm, loopable.
- **Never** prompt for "music that sounds exactly like <franchise>'s theme" or
  name a copyrighted track/composer to imitate. Describe the *mood and era*, not
  a specific existing work. This keeps the soundtrack original and clear of the
  copyright concerns set out in `VISION.md`.
