# Sound effects (served `.mp3` one-shots)

The game-ready sound effects Phaser loads at runtime via `this.load.audio(...)`
and plays **once** (no `loop`) on an event: `this.sound.play('ui-confirm')`.

These are **built output**, not masters — renders of the `.mid` masters in
[`../../../../assets/audio/midi/sfx/`](../../../../assets/audio/midi/sfx/),
produced by the **generate-midi** skill (era `sfx`). To change a cue, edit its
`.mid`/spec master and re-render — don't hand-edit the `.mp3`.

```bash
# re-render an existing SFX master (one-shot; --tail sets the ring-out)
./venv/bin/python .claude/skills/generate-midi/scripts/midi.py render \
  --input assets/audio/midi/sfx/ui-confirm-a.mid \
  --output public/assets/audio/sfx/ui-confirm-a.mp3 --tail 0.03
```

The full catalog (every effect the game needs, with recipes) and naming
convention are in
[`.claude/skills/generate-midi/references/sfx-cookbook.md`](../../../../.claude/skills/generate-midi/references/sfx-cookbook.md).
