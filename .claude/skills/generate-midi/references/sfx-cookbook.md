# Sound effects — the chip SFX cookbook

Companion to `style-guide.md` (*music length & looping*) and `composer-panel.md`
(*how to write iconic music*). This doc is about the **other** half of the
cartridge soundscape: the **short one-shot sound effects** — the coin chirp, the
menu blip, the door, the stair-step, the hit, the catch. Same toolkit, same chip
synth, same `.mid → .mp3` pipeline; you just compose **tiny `loop:false` cues in
the `sfx` era**.

> SFX are 90% **function and length**, 10% melody. A good retro SFX is *instantly
> readable* (you know what happened before you've thought about it), **short**
> (most are well under half a second), **dry**, and made of the same handful of
> chip voices as the music — so the effects feel like they belong to the same
> little machine that's playing the score. That cohesion is the whole point.

---

## 1. How SFX differ from music (the discipline)

| | Music | Sound effects |
|---|---|---|
| era | `gbc` (house) / `snes`… | **`sfx`** (a workbench era: 8 voices, wide tempo, dry) |
| loop | `true` | **always `false`** — they fire once and stop |
| length | 25–50 s loop body | **~0.05–0.6 s** (a few cues ring out to ~1 s) |
| reverb | per-era | **none** (SFX are dry; they punch and get out) |
| voices | a 4-voice band | usually **1–2 voices**, occasionally 3 |
| the craft | a hummable hook | **a readable gesture**: a shape, not a tune |

The `sfx` era exists so the validator doesn't fight you: it allows fast tempos
(up to 400 BPM), layering, and a short default ring-out. **Use it for every
effect**, with `loop:false`.

---

## 2. The five SFX primitives (this is the whole vocabulary)

Almost every retro effect is one of these, or a stack of two:

1. **Blip** — one to three very short pulse notes. The atom of UI. Up = positive
   (confirm), down = negative (cancel). `pulse25`/`pulse12`, 16th/32nd notes.
   *Recipe:* `C6s` · `C6s G6s` (confirm up) · `G5s C5s` (cancel down).
2. **Chirp / coin** — a short blip immediately into a higher, slightly longer
   held note. The "got something" sound. *Recipe:* `B5s E6e`.
3. **Glide / sweep** (the hardware "sweep" unit) — a single note that slides with
   `~`. **Up** = jump / power / positive; **down** = fall / zap / fail. On the
   **`noise`** voice it becomes an airy **whoosh**; on a **pulse** it's a tonal
   **zap/laser/boing**. *Recipe:* `C4~C6e` (jump) · `C7~C4e` (zap) ·
   `C3~C6q` on `noise` (rising whoosh). A glide spans up to **±2 octaves**; for
   more, chain two glide notes.
4. **Noise burst** — the `noise` voice (real pitched noise now) or a `drums`
   `kick`/`snare`, very short. Impacts, bumps, footsteps, explosions. Add a
   **downward glide on the noise** for weight (a "whump"). *Recipe:*
   `D3s` on `noise` (tick) · `C5~C2s` on `noise` (impact whump).
5. **Sparkle / arpeggio** — a quick rising run of short notes that *resolves up*,
   often with a `bell` ring-out via `--tail`. The "good thing happened" cue:
   get, heal, catch, level, kindle. *Recipe:* `C6s E6s G6s C7e` + `bell`.

Stack a pulse over a `tri_bass` thunk for body, or a `bell` over a pulse for
shine. Two voices is plenty; three is a lot for an SFX.

---

## 3. Knobs that matter for SFX

- **Tempo + note value = timing.** Pick a high tempo (180–280) and write 16ths
  (`s`) / 32nds. A 32nd at 240 BPM is ~31 ms — a crisp tick.
- **`~` glide** — the single biggest "retro SFX" lever. See primitive 3.
- **`noise` voice** — real pitched noise; its **pitch sets the brightness**
  (high = hiss/spark, low = rumble/thud). Glide it to sweep.
- **`@velocity`** — accent the first note (`C6s@120`) for attack, drop later
  notes for a softer tail.
- **`--tail` (render flag)** — one-shot ring-out length. Default for `sfx` is a
  tight **0.08 s**. Use **`--tail 0.02`** for snappy blips, **`--tail 0.4`** (or
  more) for `bell`/sparkle cues that should shimmer out. *This is set at render
  time, not in the spec.*
- **Keep peak voices ≤ 2–3.** SFX read better thin.

---

## 4. Length & character targets

| feel | length | shape |
|------|--------|-------|
| UI tick / cursor / text-blip | 0.03–0.10 s | one tiny blip |
| confirm / cancel / toggle | 0.08–0.20 s | 1–2 blips, up or down |
| coin / pickup / get | 0.15–0.35 s | chirp into a held note |
| footstep / bump / tick | 0.04–0.12 s | one noise/thunk |
| door / chest / stairs | 0.15–0.45 s | gesture (creak, step-run) |
| jump / hop / flee / transition | 0.12–0.40 s | a glide (or two) |
| hit / impact / zap | 0.06–0.25 s | noise burst ± glide |
| stat up/down · status | 0.15–0.35 s | short rising / falling run |
| faint / break-out / error | 0.20–0.45 s | descending / deflating |
| catch · heal · level · sparkle | 0.30–0.70 s | rising arpeggio + ring |
| Gleam / kindle bloom (the big ones) | 0.6–1.2 s | wider arpeggio, bell ring-out |

Most of the game's effects should be in the **top half** of this table. The big
diegetic moments (earning a **Gleam**, a **Kindling** completing) are the only
ones allowed to luxuriate.

---

## 5. Originality (same rule as the music)

Every effect is **original**. We're inspired by the *function* of cartridge-era
SFX — the readable coin chirp, the descending faint, the rising catch — never a
copy of a specific game's actual sound. Don't try to clone a known sound by ear;
write our own gesture that does the same job. Use the **canon vocabulary** (kin,
Lamp, Gleam, kindling, Lantern Gift, vesperlamp) in names and notes — these are
*PixelKin's* sounds. (See `VISION.md`.)

---

## 6. The PixelKin SFX catalog

The set the game needs, grounded in the mechanics (`docs/mechanics/`) and the
world (`docs/world/`). Build **2–3 variants** of each (`-a`, `-b`, `-c`) so the
team can audition and pick. Each line is a ready brief: *what it's for ·
character · a recipe sketch*. Voices in **`sfx`** era unless noted; all
`loop:false`.

### A · UI / system  (dry, tiny, the most-heard sounds in the game)
- **ui-cursor** — menu cursor moves. One neutral tick. `E6s` · `--tail 0.02`.
- **ui-confirm** — A-button / accept. Two-note **up** blip. `C6s G6s`.
- **ui-cancel** — B-button / back. Two-note **down** blip. `G5s C5s`.
- **ui-menu-open** — open pause/menu. Quick rising 2–3 notes. `C5s E5s G5e`.
- **ui-menu-close** — close menu. The reverse, falling. `G5s E5s C5e`.
- **ui-error** — invalid / can't-do. A low, flat **buzz** (`pulse50` low, or a
  short down-glide). `C3e~B2e` / `pulse50 C3q@90`.
- **ui-toggle** — flip an option on/off. Tiny two-state click. `A5s D6s`.
- **ui-text-blip** — per-character dialogue print tick (played rapidly). Barely-
  there `pulse12` tick. `C6s@70` · `--tail 0.015`.
- **ui-save** — saving to the journal. A small, reassuring 3-note resolve +
  light `bell`. `G5s C6s E6e` + bell · `--tail 0.3`.

### B · World / traversal  (Lantern Gifts, doors, stairs, pickups)
- **world-footstep** — a single soft step (low, short `noise`/`tri_bass` tick;
  vary pitch for grass vs stone). `noise D3s` · `--tail 0.03`.
- **world-stairs** — stepping up stairs: a quick **rising run of equal ticks**
  (3–5 notes climbing). `pulse25 C5s D5s E5s F5s`.
- **world-bump** — walking into a wall. One dull low thunk. `tri_bass C2s` +
  `noise C2s`.
- **world-door-open** — entering a building. A soft `noise` up-glide (creak) into
  a small click. `noise A2~D3e` + `pulse25 G4s`.
- **world-door-close** — the reverse: down-glide + click.
- **world-transition** — area/scene change. A short airy **whoosh** on `noise`
  (up for entering brighter, down for descending). `noise C3~C6q`.
- **world-ledge-hop** — hopping down a ledge. A small **down-glide** boing.
  `pulse25 G5~C5e`.
- **world-pickup** — grabbing a small item/coin on the ground. The classic
  **chirp**. `pulse25 B5s E6e` (+ optional `pulse12` octave sparkle).
- **world-chest** — opening a treasure chest / spur reward. Creak (noise glide)
  then a small sparkle. `noise C3~F3e` then `pulse25 C6s E6s G6e` · `--tail 0.3`.
- **world-warp** — vesperlamp fast-travel / waypoint. A shimmering rising glide
  + `bell`. `pulse12 C5~C6q` + bell · `--tail 0.4`.
- **world-lantern-light** — **using a Lantern Gift / lighting a lamp** (a signature
  PixelKin verb). A warm *flare*: soft up-glide that blooms, `wave`/`pulse25` +
  `bell` glint. `wave C4~G4e` + `bell C6q` · `--tail 0.4`.
- **world-heal** — full restore at a hearth/inn (**Hearthrest**). A gentle,
  complete rising arpeggio that resolves home. `pulse25 C5s E5s G5s C6e` + bell ·
  `--tail 0.4`.
- **world-gleam** — **a constellation is relit / a Gleam is earned** (the game's
  big diegetic reward — see `docs/mechanics`/`atlas`). The grandest SFX: a wide,
  bright rising arpeggio with a long `bell` shimmer; can hint the **Vesper motif**
  (`G→C→D … E→D→C`). `pulse25 G4s C5s D5s G5s C6e` + `bell C6h+E6h` ·
  `--tail 0.7`. *Allowed to be ~1 s.*

### C · Battle (core, type-agnostic)
- **battle-encounter** — wild battle starts. A rising tension **swoosh/sting**
  (noise up-glide + a pulse stab). `noise C3~C5e` + `pulse25 G3s C4s`.
- **battle-hit-physical** — a melee/contact hit lands. Short **noise burst** with
  a downward glide for impact (+ `tri_bass` thunk). `noise C5~C2s` + `tri_bass C2s`.
- **battle-hit-special** — an energy/elemental hit lands (the neutral version). A
  tonal **zap**: pulse down-glide. `pulse25 C6~C3s`.
- **battle-super-effective** — the hit was super-effective. A **brighter, bigger**
  impact: hit + a quick up-flick / extra noise crack. `noise C6~C3e` + `pulse25 C5s G5s`.
- **battle-not-effective** — resisted. A **dull, muffled** low thunk, no sparkle.
  `pulse50 C3s` + `noise C2s@70`.
- **battle-critical** — critical hit. A **sharp, high accent** on top of the hit.
  `pulse25 C7s@127` + `noise C6~C3s`.
- **battle-miss** — attack misses / kin dodges. A quick **whoosh past** (noise
  up-glide, no impact). `noise A3~A5e@90`.
- **battle-stat-up** — a stat rose (buff). A short **rising** 3-note run / up-glide.
  `pulse25 C5s E5s G5e` or `pulse25 C5~C6e`.
- **battle-stat-down** — a stat fell (debuff). The **falling** mirror.
  `pulse25 G5s E5s C5e` or `pulse25 C6~C5e`.
- **battle-status** — a status is inflicted (Scorch/Drench/Numb/Chill/Dozing/
  Blight/Dazzle — see `04-capture.md`). An unsettled, wavering low sting (down-
  glide on `pulse12` + a noise hiss). `pulse12 E4~C4e` + `noise C4~C3e@80`.
- **battle-faint** — a kin faints. A **deflating descending** glide/run (cousin of
  the game-over cue, but a quick SFX). `pulse25 C5~C3q`.
- **battle-hp-low** — low-HP warning **beep** (the game repeats it). **One** sharp
  high beep. `pulse25 A6s@110` · `--tail 0.02`.
- **battle-hp-heal** — HP restoring (potion / heal tick). A soft **bubbly rising**
  tick or short arpeggio. `pulse12 C5s E5s G5s` or a gentle `pulse25 C5~G5e`.
- **battle-xp** — XP bar filling (played as a loop-ish tick; keep it a single
  short tick the game repeats). `pulse12 E6s@80` · `--tail 0.015`.
- **battle-flee** — successfully fled. A quick **down-and-away whoosh**.
  `noise C5~C3e` + `pulse25 C5~C4e`.

### D · Elemental attack hits  (`atk-*`, lean on each light's signature)
The 10 lights (`docs/mechanics/01-type-system.md`) each get a flavoured impact,
echoing their **sonic signature** from `references/pixelkin-soundtrack.md §3.2`.
Keep them all roughly the same length/loudness as `battle-hit-special` so they're
interchangeable; the *character* differs:
- **atk-ember** — warm crackle: short noise burst + a `pulse25` flicker.
  `noise C6~C4e` + `pulse25 C5s G5s`.
- **atk-tide** — splash/lilt: a rounded `wave` down-glide + soft noise wash.
  `wave G5~C4e` + `noise C5~C3e@70`.
- **atk-verdant** — dewy/Lydian: bright `bell`/`pulse12` ping (use a #4 colour).
  `pulse12 C6s F#6s C6e` (Lydian shimmer).
- **atk-stone** — heavy: deep `tri_bass` thunk + low noise. `tri_bass C2s` +
  `noise C3~C2s`.
- **atk-storm** — fast staccato **zap** + noise gust. `pulse25 C7~C4s` + `noise C6~C4s`.
- **atk-frost** — glassy crack: high `bell` + a thin downward shard.
  `bell C7s` + `pulse12 C7~G6e`.
- **atk-solar** — radiant warm flash: a bright **up**-glint `pulse25` + bell.
  `pulse25 G5~C6e` + bell C6s.
- **atk-lunar** — cool dreamlike: slow `wave` glide + faint clockwork tick.
  `wave C5~G4e` + `pulse12 C6s@60`.
- **atk-light** — bright ascending sparkle (true starlight). `pulse25 C6s E6s G6s C7e`.
- **atk-dark** — guttering/null: a **detuned, faltering** down-glide that doesn't
  resolve (the Hollowing's sound). `pulse12 C5~B3e@90` + `noise C4~C2e@70`.

### E · Capture (Lamp system) & progression / Kindling
- **capture-throw** — throwing a **Lamp**. A light underhand **whoosh** into a
  soft tap. `noise A3~D4e@90` + `pulse25 D4s`.
- **capture-wobble** — the lamp wobbles (cosmetic, see `04-capture.md`; the game
  plays it 1–3×). **One** small mechanical tick. `pulse50 G4s` + `noise G3s@70` ·
  `--tail 0.03`.
- **capture-success** — the kin's light comes to rest: a satisfying **click-lock**
  then a warm confirming rise (the game's most-wanted reward chirp). `pulse25 C4s`
  (lock) then `pulse25 G4s C5s E5e` + bell · `--tail 0.4`.
- **capture-break** — break-out / catch failed: the lamp pops, light escapes — a
  **deflating pop + down-flick**. `noise C5~C3e` + `pulse25 E5~C5e@90`.
- **progress-levelup** — a quick SFX accent for a level gained (the longer jingle
  is the music skill's `level_up`; this is the snappy on-hit cue). `pulse25 C5s E5s G5e`.
- **progress-learn** — a move is learned. A bright confirming sparkle. `pulse12 G5s C6s E6e` + bell.
- **kindle-start** — a **Kindling** begins (`05-kindling.md`): a mysterious
  **rising shimmer** (the music skill scores the full `evolution` cue; this is the
  trigger sting). `wave C4~C5q` + `pulse12 C6s E6s G6s` · `--tail 0.4`.
- **kindle-complete** — the Kindling lands: a **bloom/flare** that resolves bright
  (a kin blazed into its brighter form). Wide rising arpeggio + long bell.
  `pulse25 C5s G5s C6s E6e` + `bell C6h` · `--tail 0.6`.
- **dex-register** — a new kin is recorded in the **vesperlamp**. A small "data"
  blip then a confirming ping. `pulse12 C6s C6s` (blip-blip) + `bell G6e` · `--tail 0.25`.

---

## 7. Naming & where files go

Mirror the music layout, namespaced under `sfx/`:

- **spec JSON → `assets/audio/midi/sfx/specs/<name>-<v>.json`**
- **`.mid` master → `assets/audio/midi/sfx/<name>-<v>.mid`**
- **`.mp3` game asset → `public/assets/audio/sfx/<name>-<v>.mp3`**

`<name>` is the catalog key above (`ui-confirm`, `battle-hit-physical`,
`atk-ember`, `capture-success`, …); `<v>` is `a` / `b` / `c`. Keep the `.mid` —
it's the editable master, same rule as music. Don't hand-edit the `.mp3`.

---

## 8. Workflow (per effect)

```bash
# 1. write the spec  -> assets/audio/midi/sfx/specs/ui-confirm-a.json   (era "sfx", loop:false)
# 2. build the .mid
./venv/bin/python .claude/skills/generate-midi/scripts/midi.py build \
  --spec assets/audio/midi/sfx/specs/ui-confirm-a.json \
  --output assets/audio/midi/sfx/ui-confirm-a.mid
# 3. render the .mp3 (pick a --tail to taste: tight for blips, long for sparkles)
./venv/bin/python .claude/skills/generate-midi/scripts/midi.py render \
  --input assets/audio/midi/sfx/ui-confirm-a.mid \
  --output public/assets/audio/sfx/ui-confirm-a.mp3 \
  --tail 0.03
```

Then audition, tweak the spec, rebuild. In Phaser, preload the `.mp3` and play it
**once** (no `loop`) on the event: `this.sound.play('ui-confirm')`. SFX render as
a single one-shot, so `--loops` is never needed.
