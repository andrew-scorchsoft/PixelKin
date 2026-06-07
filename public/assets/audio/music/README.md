# Music (served `.mp3` loops)

The game-ready background tracks Phaser loads at runtime via
`this.load.audio(...)`. These are **built output**, not masters: the current
tracks here are **renders of the `.mid` masters in
[`../../../../assets/audio/midi/`](../../../../assets/audio/midi/)**, produced by
the **generate-midi** skill. To change a track, edit its `.mid`/spec master and
re-render — don't hand-edit the `.mp3`.

```bash
# re-render an existing master (the engine repeats the loop)
./venv/bin/python .claude/skills/generate-midi/scripts/midi.py render \
  --input assets/audio/midi/tinderwick-a.mid \
  --output public/assets/audio/music/tinderwick-a.mp3
```

The per-area/route music plan and briefs are in
[`../../../../docs/world/music-direction.md`](../../../../docs/world/music-direction.md).

> **Alternative source — text-prompt music.** For tracks composed from a text
> prompt rather than note-by-note MIDI, use the **generate-music** skill
> (ElevenLabs Music API), which writes its `.mp3` straight here. Either way the
> served output lands in this folder; keep tracks instrumental and loop-friendly.
> See `.claude/skills/generate-midi/SKILL.md` and
> `.claude/skills/generate-music/SKILL.md`.
