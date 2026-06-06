# Era, length & looping — the rules of the cartridge

Companion to `composer-panel.md`. The panel says *how to write the music*; this
says *how long it should be, how it loops, and what the hardware allowed*. The
goal is to stay **true to the platform of the era** while hitting a high bar of
craft. Pick the era that matches the feeling you want, then live inside its
budget — `midi.py build` will warn you when you break it.

---

## 1. Era profiles (the voice budget)

| era    | platform feel                | voices | chords? | reverb | typical use |
|--------|------------------------------|:------:|:-------:|:------:|-------------|
| `nes`  | NES / Famicom, brittle+bright | 4      | no      | none   | spartan, punchy chip |
| `gb`   | Game Boy DMG (mono)          | 4      | no      | none   | classic handheld monster-RPG |
| `gbc`  | Game Boy Color               | 4      | no      | light  | **PixelKin's house style** — confident 4-channel |
| `snes` | SNES sample voices + echo    | 8      | yes     | warm   | lush, cinematic, boss/emotional |
| `gba`  | GBA sampled sequencer        | 8      | yes     | some   | brighter, busier, more voices |
| `hifi` | PS1/GM-style sequenced MIDI  | 16     | yes     | some   | grand title/story, orchestral-leaning |

**Default to `gbc`** for in-world tracks (routes, towns, caves, wild battles):
it's the sweet spot of the handheld era and keeps the soundtrack cohesive.
Reach for `snes`/`hifi` for the big moments — title, bosses, story cutscenes —
where chords, pads, and reverb earn their cost.

**The 4-voice band (chip eras).** Assign every channel a job and don't exceed it:

- **Lead** — the melody (`pulse25` usually).
- **Harmony** — arpeggios / counter-line (`pulse12`, lower gain).
- **Bass** — the low end (`tri_bass` / `wave`).
- **Percussion** — `drums` (the noise channel).

On `snes`/`gba`/`hifi` you may add pads, real chords, a second lead, a
counter-melody — up to the voice budget. More voices is not better; **clarity is
better.** Most iconic tracks use far fewer voices than the hardware allowed.

**No chords on chip eras.** `nes`/`gb`/`gbc` cannot stack notes. Imply harmony
with fast arpeggios on one channel: `C4e E4e G4e E4e` *is* a C-major "chord" to
the ear, and it's the signature retro sound. The builder warns if you stack.

---

## 2. Length & looping (this is era-true, not arbitrary)

On real cartridges, music was **sequence data that looped forever** — there was
no "3-minute track", just a short body the hardware repeated until the scene
changed. We mirror that: compose **one clean loop**, and let the game engine
repeat it. So "length" means *how long before it repeats*, and the craft is
making that repeat invisible.

### Looping background music (the common case)

`loop: true`. Compose a **body that ends where it began**:

| track type            | loop body length | bars (4/4)  | feel |
|-----------------------|------------------|-------------|------|
| Overworld / route     | ~25–40 s         | 16–32       | hummable, never annoying |
| Town / village        | ~25–35 s         | 16–24       | cosy, relaxed |
| Wild battle           | ~20–35 s         | 16–32       | urgent, exciting |
| Boss / rival          | ~35–50 s         | 24–48       | heroic, a clear B-section |
| Cave / dungeon        | ~30–45 s         | 16–32       | sparse, atmospheric |
| Emotional / cutscene  | ~30–50 s         | 16–32       | slow, lyrical |
| Title screen          | ~30–60 s         | optional intro + loop body |

**Seamless-loop rules:**

- The **last bar must voice-lead into bar 1** — end on a chord/note that wants
  to resolve *to the downbeat of the start*, not on a dead-stopped tonic.
- Keep the loop **one self-contained musical sentence** (or two: AABA). Don't
  let a phrase straddle the seam unresolved in a jarring way.
- The builder writes `loopStart`/`loopEnd` markers into the `.mid`. For the
  **game asset, render one pass** (`--loops 1`): the body *is* the loop, and
  Phaser repeats it (`this.sound.add('overworld', { loop: true })`).
- To *audition* the seam, render `--loops 2` or `3` and listen at the join.
  If you hear a bump, fix the last bar — don't paper over it with a crossfade.

### One-shot jingles & fanfares (do **not** loop)

`loop: false`. These play once and stop, so they **must resolve** — land
firmly on the tonic and let it ring.

| jingle           | length   | shape |
|------------------|----------|-------|
| Victory fanfare  | 2–6 s    | ascending, triumphant, hard tonic resolution |
| Level-up         | 0.7–2 s  | tiny rising 3–5 note flourish |
| Item / key-get   | 1–3 s    | bright conclusive "ta-da" |
| Game-over / faint| 3–6 s    | descending, deflating cadence |
| Evolution        | ~8–14 s  | builds tension, releases; *may* loop under an animation |

Render one-shots with `--loops 1`; a small `--fade-out 0.3` is fine if a tail
rings too long, but a well-resolved jingle usually needs none.

---

## 3. Tempo, key & form quick-reference

- **Tempo (BPM):** routes 110–135 · towns 96–120 · wild battles 145–165 ·
  bosses 160–180 · caves 84–104 · emotional 66–92 · fanfares 130–150. The
  builder warns outside the era's range.
- **Key/mood:** major = safe/bright (towns, routes, victory); natural/harmonic
  minor = tension/drama (battles, caves, game-over); modal flavours (Dorian,
  Lydian) = wonder/mystery (special areas). The `key` field is documentation
  only — it doesn't constrain notes, but state it and compose to it.
- **Form:** state a phrase, repeat it, answer it. **AABA** (32 bars) and
  **ABAC** are the workhorses. Bosses earn a contrasting **B-section** that
  lifts before returning. Keep it tight — a loop is a sentence, not an essay.

---

## 4. Cohesion across the soundtrack (the whole-game brief)

The point of generating every track through this one skill is a soundtrack that
**sounds like one composer wrote it**. To get that:

- **Reuse a main motif.** Pick a 3–5 note theme for PixelKin and let it surface
  transformed across title, an emotional cue, maybe the final boss. That thread
  is what turns a folder of loops into *a score*.
- **Keep a consistent palette.** Prefer the same voices for the same roles
  (`pulse25` leads, `tri_bass` low end) so timbres feel related.
- **One reverb per era.** Let the era tag drive it (chip = dry, SNES = warm).
  Don't drench one track and leave its neighbour bone-dry.
- **Mind keys between adjacent scenes** so a town→route transition doesn't
  clash.

---

## 5. Rendering: chip synth vs. soundfont

- **`--engine chip` (default).** The built-in numpy synthesizer: authentic
  pulse/triangle/noise/wave timbres. Zero system dependencies, and it's *more*
  era-true than a generic GM soundfont — these chip timbres are the iconic
  sound. Use it for everything chip (`nes`/`gb`/`gbc`) and it's perfectly good
  for `snes`/`hifi` too.
- **`--engine soundfont --soundfont path/to.sf2`.** If you have `fluidsynth`
  and a quality `.sf2`, this renders the same `.mid` with sampled instruments —
  lusher strings/brass for `snes`/`hifi` showpieces. Optional; not installed by
  default. The `.mid` is the portable source of truth either way, so you can
  re-render any track through a better soundfont later without recomposing.
