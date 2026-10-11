# PixelKin — Music Remaster Panel (pilot)

> The owner's brief: *make the music feel more like the classic handheld
> creature-collecting games, without copying them and in keeping with our game.
> Imagine the great 16-bit RPG composers together: what would they do to bring it
> to life? SNES-level is fine. Retro, iconic, not modern.*
>
> This doc is the panel's diagnosis of the current score, the agreed technique
> toolkit, the acceptance bar, and a **3-track pilot** for owner approval. The
> pilot masters are a **parallel set** (`*-r2`), **not wired into the game**: the
> shipped `tinderwick-a` / `dimglass-coast-a` / `battle-main-dusk-duel` stay
> untouched for A/B listening.
>
> Originality (VISION.md): every note is new. The panel studies **technique**
> (form, voicing, leitmotif, arrangement, the echo-unit sound) and names no
> composer, franchise or track. No melody is quoted or paraphrased.

## The panel

| Chair | Role | Listens for |
|-------|------|-------------|
| **The orchestral melodist** | the 16-bit RPG melodist who wrote small tunes that feel like whole orchestras | hummable motifs, long-line form (AABA, a real bridge), leitmotif, harmony that *moves* and carries feeling |
| **The atmospheric layerer** | the 16-bit composer known for lush, watery ambience built from a handful of sample voices | echo-buffer depth, layered entries, pads that breathe, space and register |
| **The handheld creature-game sound designer** | knows what the genre's town/route/battle cues *do* for a player | function by area-kind, front-loaded hooks, the loop point heard 200 times, the battle "hook + engine" |
| **The chip-register purist** | the 4-channel conscience | voice budget (≤8, SNES-style), roles, timbre, clarity on a phone speaker, seamless loops, no modern gloss |

## How it was run

The panel did not guess. It read the shipped specs (`assets/audio/midi/specs/*.json`)
for the three most-heard cues, mapped every bar's harmony, voicing, register,
rhythm and velocity, and rendered the shipped `.mid`s through the same chip engine
to measure loudness and seam behaviour. Then it built the pilot with the same
toolkit (`generate-midi`, chip engine, `snes` era) and checked it with the same
measurements, plus a semitone-clash scan of every bar.

## Diagnosis of the current score

What the shipped area/battle tracks share (Tinderwick A, Dimglass Coast A, the
wild-battle duel — and most siblings follow the same recipe):

1. **Flat dynamics.** No note in any of the three specs carries a velocity: every
   note of every voice plays at the same level, start to finish. Phrases cannot
   swell, downbeats cannot lean, a bridge cannot lift. *(The melodist's first
   note: "it's being sung by a machine that never breathes.")*
2. **The accompaniment is one pattern.** The arp/harp is the same eighth-note
   `1-3-5-3` block broken chord in every bar of every track (town, route *and*
   battle). It is the most generic chip gesture there is; it gives no place its
   own fingerprint.
3. **Static, root-position harmony.** Tinderwick A sits on C major for more than half
   its 16 bars; Dimglass A is mostly I–IV–V. Almost no sevenths, no suspensions, no
   ii–V motion, no borrowed chords. Pads stack root-position triads in the same
   octave as the lead.
4. **Register mud.** Tinderwick's lead sits G3–F4 — *inside* the pad (C3–E4) and
   the harp (F3–G4). Dimglass's harp (E3–A4) sits right under its lead (D4–D5).
   On a phone speaker the tune is fighting its own accompaniment.
5. **No real B-section / bridge.** Tinderwick's "B" is four bars that drift to A minor and back;
   Dimglass has none (ABAC variants of the same phrase); the battle's lift is a
   chord change under the same rhythm. There is no contrast to come home *from*.
6. **The bass never walks.** Every bass part is a root–fifth ostinato
   (half notes in town, quarters on the route, eighths in battle) with no approach
   tones, so chord changes arrive unannounced and the music doesn't *go anywhere*.
7. **Square rhythm.** Tinderwick's lead is entirely quarters and halves; no
   dotted figures, no syncopation, no swing. Hooks are recognised by rhythm first,
   pitch second — this one has no rhythmic identity.
8. **Dynamics by entry are missing.** Every voice plays from bar 1 to bar 16; the
   loop has one texture, so the 20th repeat sounds exactly like the 1st.
9. **The leitmotif exists on paper, not in the ear.** The Vesper contour is
   present (G–C–D / E–D–C) but in equal note values buried in the low register;
   it has no rhythmic signature, so it can't be recognised when it returns in
   another key, tempo or mode.
10. **The battle shares the title's DNA too closely.** Same key (A minor), same
    `Am–F–G` loop, the same arp and the same brass stabs — the fight doesn't have
    its own colour or a hook you'd hum.

What is already good and must be kept: the one-engine cohesion (everything renders
on the chip synth), the snes-register policy for first-impression maps, the
Vesper contour as the score's spine, the dusk→dawn key arc, the per-element
signatures, and clean levels (≈ −2.6 dBFS peak, no clipping).

## The agreed toolkit (era-authentic, SNES-plausible)

Everything below is achievable inside the existing `generate-midi` toolkit — no
renderer change was needed for the pilot.

| # | Technique | How we do it in our toolkit |
|---|-----------|-----------------------------|
| 1 | **A hummable 4–8 bar motif per place**, stepwise with one leap, front-loaded in bars 1–2, with a *rhythmic* signature (dotted / syncopated) | composed lead; the leap is saved for the consequent phrase |
| 2 | **The Lantern Call leitmotif** (the game's own theme — see below) stated in every place, reharmonised per region | the Vesper contour given a fixed rhythm |
| 3 | **Real form**: AABA / A A′ B A″ with a **B-section/bridge** that changes key area, register and texture | 24–32-bar loops |
| 4 | **Harmony that moves**: ii–V, secondary dominants (V/ii, V/vi), sevenths and ninths, **borrowed iv** (melancholy warmth), **bVI–bVII** (modal lift), harmonic-minor dominants in battle | chord tables per bar |
| 5 | **Guide-tone pads**: 2-note 3rd/7th voicings, voice-led, *below* the lead | saves voices, removes mud, sounds expensive |
| 6 | **Counter-melodies** that move against the tune (contrary motion, long tones), and **octave doubling** of the tune on its last return | `flute` / second `pulse25` |
| 7 | **Call-and-response**: the lead phrases in 2-bar spans and another voice answers in the gaps | flute (towns/routes), brass stabs (battle) |
| 8 | **Bass lines that walk**: chromatic and diatonic approach tones into every chord change; a "boom-ba" skip on routes; an octave gallop in battle | composed per bar |
| 9 | **Echo-unit depth** on the lead (the 16-bit hardware echo sound) | an `echo` track: the lead a dotted eighth late at ~55% velocity, **wrapped round the loop seam** so the echo of the last bar sounds at the top of the next pass |
| 10 | **Swing where apt** (lullabies, cosy towns) | triplet long-short (`qt et`) harp and kit |
| 11 | **Dynamics** — phrase-shaped velocities (downbeat lean, climb into a peak, soften at cadences) **and by voice entries** (A sparse → B new colour → A′ full) | `@vel` on every note; voices enter by section |
| 12 | **Accompaniment idioms per place** instead of one block arp: music-box rolls, open-voiced swung harp rolls, offbeat "bell-buoy" chimes, rising/falling harp waves, 16th chip arps | composed patterns |
| 13 | **Per-region instrument colour** (the element signatures in the score bible §3.2) | voice choice per role |
| 14 | **Proper loop seams**: last bar voice-leads into bar 1 (pickups, leading-tone bass, a drum fill), echo wrapped, nothing ringing across the cut | checked by measurement |
| 15 | **Mix for the worst speaker**: lead highest and clearest (C5–A5 region), pads low (gain ≈ 0.3), bass alone in octave 2 | register plan per track |

What the panel **rejected** as off-era or modern: side-chain pumping, wide stereo
tricks, risers/drops, dense 9+ voice stacks, real-instrument soundfont renders as
the default, and any "cinematic trailer" percussion. The chip-register purist's
rule held: *if a 16-bit cartridge couldn't play it in eight voices, we don't write
it.*

## The Lantern Call — the score's leitmotif

The Vesper motif from the score bible, now with a **fixed rhythm** so the ear can
recognise it anywhere:

- **Lift** — *sol → do → re* on a dotted rhythm (*long-short-held*): the lantern
  raised to the sky. In C: `G4 q.` `C5 e` `D5 h`.
- **Settle** — *mi → re → do*: the warmth returning. In C: `E5 q.` `D5 e` `C5 …`.

Reharmonised per place (pilot rows are built; the rest is the roll-out plan):

| Place | Statement | Harmony under the lift / settle |
|-------|-----------|---------------------------------|
| **Tinderwick** (built) | slow, tender, the *source* statement | C → Fmaj7; later the borrowed **Fm6** sigh |
| **Dimglass Coast** (built) | **bounced** — `q e q.` syncopated stride, octave up | G → Cmaj7 (the settle lands on the maj7) |
| **Wild battle** (built) | **fighter** — minor, two eighths + a syncopated hold, then a bar of space the brass answers; in the B-section the lift returns in **heroic major** | Em (i); in B: G major |
| Routes (roll-out) | bounced, as Dimglass | I → IV maj7 |
| Caves / blight | lift only, settle withheld | i → bVI, unresolved |
| Frost | lift stretched over sus chords | Isus2 → IVsus |
| Hollowing zones | the lift falters a semitone flat | i → bII |
| Lumenary duel | fighter, as battle, in each element's key | i → bVII |
| Spire → Dawnstead | minor → finally full major, lift reaching the octave | i → I (Picardy) |

## Acceptance criteria (every remastered track)

1. **Singable after two loops** — a listener can hum the first two bars.
2. **Distinct per place** — its own hook, key area, accompaniment idiom and
   instrument colour; no two tracks share an arp pattern or chord loop.
3. **Real form** — at least one contrasting section (B/bridge) and dynamics by
   entry.
4. **The Lantern Call** is audible (or deliberately withheld, for blight).
5. **Voice budget ≤ 8** (SNES-style), as reported by `midi.py build` (`peak_voices`).
6. **Clean mix** — peak ≈ −3 dBFS, no clipped samples, integrated loudness within
   ±1 LU of the track it replaces, lead clearly on top.
7. **Seamless loop** — last bar leads into bar 1; the sample step at the seam is
   no larger than the track's ordinary 99.9th-percentile step (no click).
8. **No semitone rubs** between the tune and the accompaniment except deliberate
   passing tones (checked with a clash scan).
9. **Mood matches** the place's brief in `docs/world/music-direction.md` and the
   dusk→dawn arc — "lanterns in the dark", cosy-melancholy, never grim.
10. **Original** — nothing quoted or paraphrased; no names in files.

## The pilot

Masters (committed, parallel set; not wired in):

| Pilot | Spec | Master |
|-------|------|--------|
| Tinderwick | `assets/audio/midi/specs/tinderwick-r2.json` | `assets/audio/midi/tinderwick-r2.mid` |
| Dimglass Coast | `assets/audio/midi/specs/dimglass-coast-r2.json` | `assets/audio/midi/dimglass-coast-r2.mid` |
| Wild battle | `assets/audio/midi/specs/battle-wild-r2.json` | `assets/audio/midi/battle-wild-r2.mid` |

Audition renders (scratch, two loops each so the seam is audible) are not
committed. Re-render any of them with
`./venv/bin/python .claude/skills/generate-midi/scripts/midi.py render --input assets/audio/midi/<name>-r2.mid --output /tmp/<name>.mp3 --loops 2`.

### (a) Tinderwick — "Lantern Lullaby" r2

- **96 BPM, 4/4, C major** with a borrowed **iv** (Fm6). **A(8) B(8) A′(8)**,
  24 bars, 60 s (was 92 BPM, 16 bars, 42 s).
- **Motif:** the first full Lantern Call — G4-C5-D5 lift, E5-D5-C5 settle — as a
  4+4 antecedent/consequent. The consequent saves its one leap (to G5) for bar 6,
  then sighs A→A♭ over F→Fm6 into a plagal-minor cadence. The lead moved **up an
  octave** out of the accompaniment.
- **B (bridge):** turns to the IV (Fmaj7–Em7–Dm7–G7, then Em7–A7 into Dm7). The lead
  *calls*, the flute *answers*; the phrase climbs to an A♭5 peak over Fm6 — the
  homesick catch, and the loudest moment in the loop.
- **A′:** the tune comes home fuller: walking bass, a flute guide-tone
  counter-line moving against the lead, a soft rim backbeat.
- **Instruments:** pulse25 lead + composed echo; strings (2-note guide tones);
  pluck harp (music-box rolls in A, a swung open-voiced harp roll from B); flute;
  bell glints that quote the lift at the A-phrase ends; tri_bass; a fireside
  clock-tick that grows into a swung kit. Peak 8 voices.

### (b) Dimglass Coast — "Lanterns Along the Tide" r2

- **126 BPM, 4/4, G major** (was 120). **A(8) A′(8) B(8) A″(8)**, 32 bars, 61 s
  (was 16 bars, 32 s).
- **Motif:** the Lantern Call **bounced** — D5-G5-A5 on a syncopated *q e q.*
  stride, settling B5-A5-G5 over Cmaj7; sequenced up through Em7; the one leap to
  D6 in bar 6; a ii–V home; an A4-B4 pickup throws the loop back to the top.
- **A′** detours through B7 (V/vi) and A7 (V/V). **B** is a modal-mixture bridge
  — Cmaj7–Bm7–Am7–D7–**E♭maj7–F**–Am7–D7 — the borrowed ♭VI–♭VII "open sea" lift,
  with the lead calling in 2-bar spans and the flute answering in the gaps.
  **A″** brings the tune back doubled by the flute an octave below.
- **Instruments:** pulse25 lead + echo; harp chimes on the **offbeats** (the
  forward push, the bell-buoys) in A, rising/falling harp waves in B; strings
  enter at A′; tri_bass "boom-ba" skip with chromatic approach tones, walking in B;
  bell buoys at phrase ends; the kit builds A (no snare) → A′ backbeat → B open-hat
  "sea spray" → A″, with fills on every 8-bar seam. Peak 8 voices.

### (c) Wild battle r2

- **160 BPM, 4/4, E minor** (moved off the title's A minor so the fight has its
  own colour) with a **B7** harmonic-minor dominant, lifting to **G major**.
  **A(8) A′(8) B(8)**, 24 bars, 36 s (was 158 BPM, 16 bars, 24 s).
- **Hook:** the Lantern Call as a fighter — B4-E5-F#5 launched on two eighths
  and a syncopated dotted hold, a stab down to B4, then a **bar of space the
  brass answers** (call-and-response). It sequences up to C and D, climbs to C6
  over ♭VI, and cadences on a D♯ leading tone.
- **B:** the leitmotif in **heroic major** (D5-G5-A5 over G) with a twin lead a
  third/sixth below and sustained brass, climbing to D6; a B7 run (D♯) slams the
  loop back to E minor.
- **Instruments:** saw lead (dry — no echo, so hits punch); pulse25 twin lead (B
  only); brass alternating call-hits and answering stabs, sustained in B; a 16th
  pulse12 arp that **enters at bar 5**; a punchy bass with an octave-pumping
  gallop and chromatic approaches; a backbeat with a pushed kick on the and-of-3,
  four-on-the-floor + open hat in B, fills at 8/16/24. Peak 7 voices.

### Measurements (chip engine, same as shipped)

| Track | Loop | Peak | RMS | Integrated | Clipped | Seam step (99.9th-pct step) |
|-------|------|------|-----|------------|---------|-----------------------------|
| tinderwick-a (shipped) | 41.7 s | −2.60 dBFS | −12.6 dBFS | −14.5 LUFS | 0 | 0.156 (0.430) |
| **tinderwick-r2** | 60.0 s | −2.78 dBFS | −13.3 dBFS | −15.3 LUFS | 0 | 0.064 (0.443) |
| dimglass-coast-a (shipped) | 32.0 s | −2.61 dBFS | −13.2 dBFS | −14.9 LUFS | 0 | 0.041 (0.413) |
| **dimglass-coast-r2** | 61.0 s | −2.73 dBFS | −13.6 dBFS | −15.1 LUFS | 0 | 0.191 (0.458) |
| battle-main-dusk-duel (shipped) | 24.3 s | −2.93 dBFS | −14.5 dBFS | −15.6 LUFS | 0 | 0.169 (0.275) |
| **battle-wild-r2** | 36.0 s | −2.71 dBFS | −15.4 dBFS | −16.0 LUFS | 0 | 0.121 (0.283) |

All three pass criteria 5–8: ≤ 8 voices, within ±1 LU of the track each would
replace, no clipping, seam steps inside the ordinary sample-step range (no click),
and zero semitone rubs between tune and accompaniment apart from two passing
eighths in the battle.

## What the owner should listen for

- **Tinderwick:** can you hum bars 1–2 after the second loop? Does the A♭ at the
  end of the bridge (around 0:38) catch in the throat and then feel like coming
  home? The echo should read as *space*, not as a second melody.
- **Dimglass:** does the offbeat harp make it *walk* forward? The bridge's
  E♭–F lift (around 0:38) is the "open sea" moment. The flute doubling on the
  last A should feel bigger, not louder.
- **Battle:** is the hook catchy and do the brass answers land in the gaps? Does
  the major B-section make a random fight feel winnable? Compare the bass drive
  against the shipped duel.
- **All:** listen at the seam (the middle of each two-loop file) for any bump.

## Known toolkit limits (for the roll-out)

- **No native echo, pan or swing** in the chip renderer; echo and swing are
  composed into the note data (above). It works, but costs one voice per echoed
  line. A renderer-level echo send would free that voice. It would change the
  sound of every existing track, so it needs its own decision.
- **The renderer cuts at the loop end**: note releases and reverb tails past
  `loopEnd` are not wrapped to the start. The pilot avoids audible bumps by
  composing the last bar to land cleanly, but the first ~50 ms of a pass lacks
  the previous pass's reverb tail.

## Roll-out plan (after approval)

1. On approval, swap the three pilots in, either by rendering `*-r2` over the
   served file names (no code change) or by pointing `data/world/maps.ts` /
   `BattleScene` at new keys. Keep the old masters as the archive.
2. Record the Lantern Call's rhythm and the toolkit table in the score bible
   (`pixelkin-soundtrack.md` §3.1 / §3.3) so every future cue inherits them.
3. Remaster in order of play-time: Vesper Crossroads (hub) → Lanternway →
   Pearlmoor → Lumenary duel → East/North/West towns and routes → caves → the
   Spire/Dawnstead arc. Re-derive each track's Lantern Call row from the table above.
4. Each remaster must meet the acceptance criteria above, with the measurements
   table updated.
