---
name: generate-midi
description: Compose original, era-authentic retro game music AND retro sound effects as real MIDI (.mid) and render to .mp3. Music — overworld, town, battle, boss, cave, title, emotional cue, victory fanfare, level-up/item jingle, evolution or game-over theme — in the style of cartridge-era handhelds/consoles (NES, Game Boy/Color, SNES, GBA, PS1-era sequenced MIDI). Sound effects — the short one-shot chip cues a creature-RPG needs: menu blips/confirm/cancel, coin/item pickup, door, stairs, scene-transition whoosh, jump/bump, attack hits (incl. per-element), super-effective, faint, low-HP beep, lamp throw/catch, level-up, kindling, Gleam/sparkle. Claude composes a declarative spec applying classic rules; a Python toolkit builds the .mid (honouring the platform's voice budget, plus pitch-glide "sweeps" and a real noise channel for SFX) and renders it with a built-in chiptune synth. Produces .mid source + game-ready .mp3. Does NOT use a text-to-audio model (that's generate-music) and does NOT make speech.
---

# generate-midi

Make **iconic, high-standard retro music** for PixelKin as genuine MIDI — note
data you control — and render it to game-ready audio. This is how you get the
cartridge-era feeling (handheld monster-RPG, lush 16-bit, grand sequenced MIDI)
at a craft level worthy of the classics, while every melody stays **original**
(see `VISION.md`).

**You (Claude) are the composer.** The Python toolkit is your instrument and
your sound engine — it doesn't invent melodies. You write a small JSON *song
spec* applying the rules in `references/`; `midi.py build` turns it into a real
`.mid`; `midi.py render` turns that into `.wav`/`.mp3` with a built-in chiptune
synthesizer.

## When to use

- The user wants retro/chiptune/MIDI music, or any scored cue: overworld, town,
  route, battle, boss, cave/dungeon, title, emotional/cutscene, or a short
  jingle (victory, level-up, item-get, evolution, game-over).
- They want music that's authentically *of the platform/era* and note-level
  controllable — not a one-shot text-to-audio render.

- They want **sound effects** — the short one-shot chip cues (UI blips, coins,
  doors, stairs, hits, the catch, sparkles). See **§ Sound effects** below and
  **`references/sfx-cookbook.md`** for the full PixelKin SFX catalog and recipes.

Use **`generate-music`** instead when they want a text-prompt → audio render
from the ElevenLabs model (richer/“produced” timbres, less control). Use this
skill (`generate-midi`) when they want true chiptune/MIDI, editable note data,
and tight era authenticity. Neither makes **speech**.

## Read these first (the craft)

The quality bar lives in two short docs — read them before composing anything
non-trivial:

- **`references/composer-panel.md`** — the design panel: melody-first writing,
  leitmotif, arpeggio-as-chord, hardware-as-instrument, mixing for tiny
  speakers, and a pre-ship checklist. This is *how to make it iconic*.
- **`references/style-guide.md`** — era voice budgets, **clip lengths**,
  **looping vs. one-shot conventions**, tempo/key/form, and soundtrack
  cohesion. This is *how long it should be and how it should loop*.
- **`references/sfx-cookbook.md`** — read before making **sound effects**: the
  SFX discipline (short, dry, one-shot), the five chip-SFX primitives (blip,
  chirp, glide/sweep, noise burst, sparkle), the `sfx` era + glide + noise + tail
  knobs, and the **full PixelKin SFX catalog** (every effect the game needs,
  grounded in the mechanics, with a ready recipe for each).
- **`references/pixelkin-soundtrack.md`** — the **PixelKin score bible**: the
  "lanterns in the dark" brief, how we study the cartridge-era handheld
  monster-RPG soundtracks *without copying a bar*, and the **cohesion system**
  (the recurring *Vesper motif*, per-element sonic signatures, voice/era policy,
  the dusk→dawn key arc). Read it before scoring any **world-map area or route** —
  the ready-to-build, **2–3-options-per-area** brief list it points to lives in
  [`docs/world/music-direction.md`](../../../docs/world/music-direction.md).

## Prerequisites

Run everything through the project venv (per `CLAUDE.md`):

```bash
# first time:
python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
```

Dependencies (`mido`, `numpy`, `imageio-ffmpeg`) are in `requirements.txt`.
**No system packages, soundfonts, or API keys needed** — MIDI building, the chip
synth, and MP3 encoding (via the ffmpeg bundled by `imageio-ffmpeg`) all run
offline.

## Workflow

1. **Gather the brief.** Nail down *place + feeling + role* before composing:
   What scene/screen is this? What should the player feel (cosy, tense, heroic,
   lonely, triumphant)? Is it a **loop** (background music) or a **one-shot**
   (fanfare/jingle)? Which era fits — chip (`gbc`, the house default) or lush
   (`snes`/`hifi`)? If the user is vague, infer sensible defaults from the
   nearest form preset and say what you chose; ask only if it's genuinely
   ambiguous.
2. **Inspect the toolkit** (once per session is enough):
   ```bash
   ./venv/bin/python .claude/skills/generate-midi/scripts/midi.py presets
   ./venv/bin/python .claude/skills/generate-midi/scripts/midi.py schema
   ```
   `presets` lists eras, the voice catalog, drum kit, and form presets (with
   suggested era/tempo/length/loop). `schema` prints the song-spec format + note
   DSL. The worked example `examples/overworld-sunhaven.json` is a good template.
3. **Compose the spec.** Write a JSON song spec (see the format below and
   `schema`). Apply the panel's rules: a hummable lead first, assign the
   era's voice budget to roles (lead/harmony/bass/percussion), imply chords with
   arpeggios on chip eras, give the bass and drums motion, and make the **last
   bar lead back into the first** (loops) or **resolve on the tonic** (one-shots).
4. **Build the `.mid`:**
   ```bash
   ./venv/bin/python .claude/skills/generate-midi/scripts/midi.py build \
     --spec /tmp/route.json \
     --output assets/audio/midi/route.mid
   ```
   It prints bars/seconds/peak-voices and **warns** if you bust the era's voice
   budget, stack chords on a chip era, or stray outside its tempo range. Treat
   warnings seriously — fix the arrangement unless you're bending a rule on
   purpose.
5. **Render to audio:**
   ```bash
   # game-ready loop (one pass; the engine repeats it):
   ./venv/bin/python .claude/skills/generate-midi/scripts/midi.py render \
     --input assets/audio/midi/route.mid \
     --output public/assets/audio/music/route.mp3

   # audition the loop seam (2 passes) as a preview:
   ./venv/bin/python .claude/skills/generate-midi/scripts/midi.py render \
     --input assets/audio/midi/route.mid --output /tmp/route-preview.mp3 --loops 2
   ```
6. **Listen and iterate.** The toolkit does **not** judge musicality. Play the
   result, check it against the panel's checklist, and re-edit the spec → build
   → render until the hook lands and the loop is seamless. Iterating on note
   data is cheap — use that.
7. **Wire it into the game.** Queue the `.mp3` in `PreloadScene`
   (`this.load.audio('route', 'assets/audio/music/route.mp3')`) and play loops
   with `{ loop: true }`.

### Where files go

- **`.mid` source → `assets/audio/midi/`** (not served; the editable master).
- **`.mp3` game asset → `public/assets/audio/music/`** (what Phaser loads).

Keep the `.mid` — it's the portable source of truth. You can re-render any track
later (different era feel, or through a real soundfont) without recomposing.

## Song-spec format (quick reference)

`midi.py schema` prints the authoritative version. In short:

```json
{
  "title": "Sunhaven Route",
  "era": "gbc",                 // nes|gb|gbc|snes|gba|hifi (see style-guide)
  "tempo": 132,
  "time_signature": [4, 4],
  "loop": true,                 // true = loop body; false = one-shot jingle
  "key": "C major",             // documentation; compose to it
  "tracks": [
    { "name": "lead",  "voice": "pulse25", "octave": 4,
      "notes": "E4q G4q C5q B4q | A4q G4q E4h" },
    { "name": "harmony","voice": "pulse12", "octave": 4, "gain": 0.6,
      "notes": "C4e E4e G4e E4e C4e E4e G4e E4e" },
    { "name": "bass",  "voice": "tri_bass", "octave": 2,
      "notes": "C2q C3q G2q G3q" },
    { "name": "drums", "voice": "drums",
      "notes": "e kick+hat hat snare+hat hat kick+hat kick snare+hat hat" }
  ]
}
```

**Note DSL:** UPPER-case pitch letter + optional `#`/`b` + optional octave
(`C4`, `F#3`, `Bb5`; bare letter uses the track `octave`). Duration suffix
`w h q e s` (whole→sixteenth), dotted `.`/`..`, triplet `t`; **omit the suffix to
reuse the previous duration**, or write a duration on its own (`e`, `q.`) to set
the running duration for the notes after it. Chord = `C4+E4+G4q` (chord-capable
eras only). Rest = `r`/`-` (e.g. `re`, `rq`). Velocity = `@1..127`. `|` bar
separators are ignored. On a `drums` voice, tokens are kit names:
`kick snare hat ohat tom crash clap`.

## Sound effects

This skill makes **short one-shot sound effects** too — the chip cues a
creature-RPG lives on (menu blips, coin/item pickup, door, **stairs**, **scene
transitions**, jump/bump, attack hits — including per-element — super-effective,
faint, low-HP beep, the **Lamp** throw/catch, level-up, **Kindling**, **Gleam**
sparkle). Same `build`→`render` pipeline; you just compose a **tiny `loop:false`
spec in the `sfx` era**.

**Read `references/sfx-cookbook.md` first** — it's the SFX craft guide *and* the
full catalog of what the game needs (2–3 variants each), with a ready recipe per
effect. The essentials:

- **Era `sfx`, `loop: false`.** A workbench era: 8 voices, wide tempo, dry, short
  default ring-out. Keep most cues **under ~0.6 s**; thin (1–2 voices).
- **Glide / "sweep"** — join two pitches with `~`: `C4~C6e` slides C4 up to C6
  over the note (the chip sweep unit). Up = jump/positive, down = fall/zap. On the
  **`noise`** voice a glide becomes an airy **whoosh**; on a pulse it's a tonal
  **zap/boing**. Spans up to ±2 octaves.
- **`noise` voice** is real pitched noise now (its pitch = brightness) — use it
  for impacts, footsteps, whooshes, wind, transitions.
- **`--tail` (render flag)** sets the one-shot ring-out: `--tail 0.02` for snappy
  blips, `--tail 0.4`+ for `bell`/sparkle cues. (`sfx` default is 0.08.)

Files (mirror the music layout, namespaced under `sfx/`): spec →
`assets/audio/midi/sfx/specs/<name>-<v>.json`, master `.mid` →
`assets/audio/midi/sfx/<name>-<v>.mid`, game `.mp3` →
`public/assets/audio/sfx/<name>-<v>.mp3`. Play once in Phaser
(`this.sound.play('ui-confirm')`) — never loop a one-shot.

## Originality & licensing (non-negotiable)

- **Every melody must be original.** Never transcribe, quote, or "make it sound
  exactly like" a real game's actual theme, and never name a copyrighted track
  or composer's *work* as something to reproduce. We study the masters'
  *technique* (counterpoint, leitmotif, hardware economy) — that's craft, not
  copyright. See `references/composer-panel.md` and the originality section of
  `VISION.md`.
- Describe targets by **genre, era, mood, and platform**, never by another
  brand. "Bright Game-Boy-Color overworld in C major" — good. "Sounds like
  <franchise>'s town theme" — not allowed.

## Lush render path (opt-in only): real SoundFonts

> **Default to the chip engine for *every* track**, including `snes`/`hifi`
> ones. The lo-fi chip sound is PixelKin's house style, and rendering the whole
> soundtrack through one engine is what keeps it cohesive. **Only** use
> `--engine soundfont` when the user *explicitly* asks for a lusher / more
> orchestral / "high-fidelity" render of a specific track. Don't reach for it on
> your own, and never mix engines across the soundtrack without being asked.

When you *are* asked for it, render the **same `.mid`** through a real SoundFont
with `--engine soundfont`. It uses the pure-pip `tinysoundfont` synth (no system
libraries), so it's a two-step one-time setup:

```bash
# 1) install the optional engine (no-deps: skips a playback-only dependency)
./venv/bin/pip install --no-deps -r requirements-soundfont.txt
# 2) fetch a soundfont (GeneralUser GS by default; ~31 MB, freely redistributable)
./venv/bin/python .claude/skills/generate-midi/scripts/fetch_soundfont.py
# 3) render
./venv/bin/python .claude/skills/generate-midi/scripts/midi.py render \
  --input assets/audio/midi/boss.mid \
  --output public/assets/audio/music/boss.mp3 --engine soundfont
```

It auto-finds `GeneralUser-GS.sf2` in `assets/audio/midi/soundfonts/`, or pass
`--soundfont path/to.sf2` for your own. Soundfonts are gitignored (large) and
re-fetched per fresh container. The `.mid` is the portable source either way, so
you can switch engines or soundfonts anytime without recomposing. The chip path
needs none of this.

## Notes & limits

- Keep loop assets to **one rendered pass** (`--loops 1`); the game loops them.
  Use `--loops N` / `--fade-out` only for previews.
- This skill writes only `.mid`, `.wav`, and `.mp3`. For text-prompt audio use
  `generate-music`; for images use `generate-image`.
