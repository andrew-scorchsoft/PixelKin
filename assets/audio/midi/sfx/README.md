# Sound-effect MIDI sources

Editable `.mid` masters for the game's **sound effects**, composed with the
**generate-midi** skill (era `sfx`, `loop:false`). Same role as the music
masters one level up: these are the *source of truth*, not served. Render each to
`.mp3` into `public/assets/audio/sfx/` for Phaser, and keep the `.mid` here so any
cue can be re-rendered later.

```bash
# build a .mid from an SFX spec
./venv/bin/python .claude/skills/generate-midi/scripts/midi.py build \
  --spec assets/audio/midi/sfx/specs/ui-confirm-a.json \
  --output assets/audio/midi/sfx/ui-confirm-a.mid

# render the game-ready one-shot (pick --tail to taste: tight blip vs sparkle)
./venv/bin/python .claude/skills/generate-midi/scripts/midi.py render \
  --input assets/audio/midi/sfx/ui-confirm-a.mid \
  --output public/assets/audio/sfx/ui-confirm-a.mp3 --tail 0.03
```

Specs live in `specs/`; names follow the catalog in
[`.claude/skills/generate-midi/references/sfx-cookbook.md`](../../../../.claude/skills/generate-midi/references/sfx-cookbook.md)
(`ui-*`, `world-*`, `battle-*`, `atk-*`, `capture-*`, `kindle-*`, `progress-*`,
`dex-*`), each with 2–3 variants `-a`/`-b`/`-c`. The cookbook is both the craft
guide and the master list of what the game needs. Worked templates:
`.claude/skills/generate-midi/examples/sfx-pickup.json` and `sfx-gleam.json`.
