# Music

Generated background music tracks (`.mp3`) live here, loaded by Phaser at
runtime via `this.load.audio(...)`.

Generate new tracks with the **generate-music** skill (ElevenLabs Music API):

```
./venv/bin/python .claude/skills/generate-music/scripts/generate_music.py \
  --prompt "overworld theme" --preset overworld \
  --output public/assets/audio/music/overworld.mp3
```

Keep tracks instrumental and loop-friendly for in-game use. See
`.claude/skills/generate-music/SKILL.md` for presets and guidance.
