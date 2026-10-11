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

## Ambient beds (`amb-*.mp3`, looping)

The quiet looping beds a map opts into with `ambience.sound_bed`
(`amb-surf`, `amb-marsh`, `amb-wind`, `amb-drips`, `amb-crickets`) are NOT chip
renders — they're synthesised by a small deterministic numpy script and are
seamless by construction (circular noise/events/reverb over the loop length):

```bash
./venv/bin/python tools/audio/ambient_beds.py            # re-render all beds (+ refresh sfx.manifest.json)
./venv/bin/python tools/audio/ambient_beds.py amb-surf   # just one
```

`Ambience.ts` loads the BARE stem (`assets/audio/sfx/<stem>.mp3`, no a/b
variants) only if it's in `sfx.manifest.json`, loops it at 0.22 × the SFX
volume, and pauses it while a battle has the World scene paused. Beds are
mastered to −23 dBFS RMS so they sit ~16 dB under the area music.

Surface footsteps (`world-footstep-<grass|sand|snow|stone|wood>-a/b`, picked by
`WorldScene.footstepKey`) and `world-grass-rustle-a/b` are ordinary chip renders
(specs in `assets/audio/midi/sfx/specs/`); the rustle is rendered to `.wav` and
dropped −8 dB before encoding (it plays under the footstep on every grass step).
Any new `.mp3` here must be added to `sfx.manifest.json` — the bed script
rewrites it from the folder listing.
