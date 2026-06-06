# MIDI sources

Editable `.mid` masters composed with the **generate-midi** skill. These are the
*source of truth* — not served to the game. Render them to `.mp3` into
`public/assets/audio/music/` for Phaser to load, and keep the `.mid` here so any
track can be re-rendered later (different era feel, or through a real soundfont)
without recomposing.

```bash
# build a .mid from a song spec
./venv/bin/python .claude/skills/generate-midi/scripts/midi.py build \
  --spec /tmp/route.json --output assets/audio/midi/route.mid

# render the game-ready loop (one pass; the engine repeats it)
./venv/bin/python .claude/skills/generate-midi/scripts/midi.py render \
  --input assets/audio/midi/route.mid \
  --output public/assets/audio/music/route.mp3
```

`overworld-sunhaven.mid` is the rendered output of
`.claude/skills/generate-midi/examples/overworld-sunhaven.json` — a worked
template. See `.claude/skills/generate-midi/SKILL.md` for the full workflow.
