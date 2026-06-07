# PixelKin — the soundtrack as one score

Companion to `composer-panel.md` (*how to write iconic retro music*) and
`style-guide.md` (*era budgets, length, looping*). This doc is **PixelKin-specific**:
it says *what the whole soundtrack is trying to be*, how every area track stays a
**sibling** of the others, and how we **study the cartridge-era handheld
monster-RPG soundtracks without copying a single bar** of them.

> The per-area, ready-to-build briefs — **2–3 music options for every world-map
> area and route** — live in **[`docs/world/music-direction.md`](../../../../docs/world/music-direction.md)**.
> That file is the canonical brief list; this file is the *why* and the *rules*
> that keep those briefs cohesive. Read both before composing an area track.

---

## 1. The brief, in one breath

PixelKin's region is **Vesperholm — "The Long Dusk"**: a night-locked land the
player slowly relights, constellation by constellation, toward a final true
dawn. The feeling is **"lanterns in the dark"** — cosy and a little melancholy,
warm windows in cold valleys, the small heroism of relighting one stretch of sky
so the next road becomes visible. **Never grim**: every long night is a *promise
of morning*. The whole score should sound like *one composer* scored that arc,
on handheld hardware, with love.

Three things follow from that and bind every track:

1. **It's a chip soundtrack at heart** — every track renders through the one
   **chip engine**, and the 4-voice *roles* (lead / arp / bass / noise) carry the
   tune. But the register can open up: many shipping area tracks lift from the
   bare `gbc` band into the lusher **`snes`** voices (pads, real chords, a pluck
   harp, bell sparkle, warm reverb) — see §3.3. Same engine, same tune, more
   colour; the discipline is a *style*, not a ceiling.
2. **It's one journey from dusk to dawn.** The score *warms* over the game — the
   start is blue-hour wistful, the blighted areas are the darkest/least-resolved
   points, and the epilogue is radiant major. Each area sits where it falls on
   that gradient (see §5).
3. **Every track shares DNA** — the Vesper motif, a fixed voice palette, and a
   per-element sonic signature (§3–4). That shared DNA is what turns a folder of
   loops into *a score*.

---

## 2. Studying the cartridge era (the nod, never the copy)

We are openly inspired by the late-'90s / early-2000s handheld monster-RPG
soundtracks. **We copy nothing** — never transcribe, quote, or "make it sound
exactly like" any real game's actual theme, and never name a franchise, track, or
composer to mimic (this is a hard `VISION.md` rule). What we study is the
**craft and the function**: *what those scores did for the player*, then we write
our own original contours that do the same job. Concretely:

- **One hummable leitmotif per place.** Each town and route had its own short,
  singable theme you could whistle 30 years later. → Every PixelKin area gets a
  distinct, front-loaded hook. The loop point is heard constantly, so the **first
  two bars must announce the tune**.
- **Function by area-kind.** The era taught the ear what each kind of place
  sounds like. We honour those functions with original melodies:
  - **Town/village** — gentle, warm, mid-tempo, a touch wistful; a cosy loop you
    rest in. (96–120 BPM)
  - **Route/overworld** — brisk **walking-pace**, optimistic, propulsive
    "let's-go"; the freedom of the open road. (110–135 BPM)
  - **Cave/dungeon** — sparse, slow, minor, **silence as an instrument**;
    atmosphere over hook. (84–104 BPM)
  - **Special/sacred area** (glowing forest, star-temple) — **modal** colour
    (Lydian/Dorian/suspended) for wonder, not plain major or minor.
  - **Hub/waystation** — short, tight, friendly loop, because it's heard *very*
    often; never annoying.
  - **Blighted/cursed zone** — unsettling, detuned, near-silent; the genre's
    "tainted land" sound, here the Hollowing's drained valleys.
  - **Boss/climax** — a structured piece (tense intro → driving loop →
    triumphant resolve), the score's biggest moment.
- **Short loops, not "tracks."** Cartridge music was sequence data that looped
  forever. We compose **one clean loop** (16–32 bars for area music) whose last
  bar voice-leads back into the first, and let the engine repeat it.
- **The 4-channel band is the timbre.** Pulse lead, pulse arp/harmony, triangle
  bass, noise percussion. Chords are *implied by fast arpeggios* on chip eras —
  that broken-chord shimmer is the iconic handheld sound; lean into it.
- **Leitmotif transformation tells the story.** The era reprised a town theme in
  minor when danger came and in radiant major when the world was made whole. We
  do exactly this: the start-town lullaby (Tinderwick) returns transformed across
  the game and **blooms in full major at the dawn** (Dawnstead).
- **Day/night & "version" variation** → in PixelKin this is **diegetic**: as
  constellations relight, areas get **brightened/relit variants** of their theme
  (that's often the "Option C" in the per-area briefs).

The discipline, the pacing, the function — that's craft, and craft isn't
copyright. The notes are ours.

---

## 3. The cohesion system (use these on every track)

### 3.1 The Vesper motif — the score's spine

A single 4-note shape threads the whole soundtrack: **a hopeful rising leap that
slightly overshoots, then a gentle stepwise settle back home** — *"the lantern
lifted to the sky, then the warmth returning."*

A canonical statement in C major: `G3 → C4 → D4` (lift, overshooting past the
tonic to the 2nd) … `E4 → D4 → C4` (settle home). Reuse the **contour**,
transposed and transformed — don't reuse the literal pitches everywhere:

| Where | Transformation |
|-------|----------------|
| Start town (Tinderwick) | slow, tender, the **first full statement** — the source theme |
| Routes | **bounced** — same shape, springy and onward-leaning |
| Climbing routes | the leap **widened**, sequenced upward each phrase (it gains altitude) |
| Caves / blight | **fragmented** — only the rising leap survives; the settle is withheld / unresolved |
| Frost / glacier | **stretched & suspended** — long tones, the settle hangs on a sus chord |
| The Hollowing's zones | **detuned / guttering** — the motif tries to land and fails |
| Umbral Spire (climax) | **booms in minor**, then **resolves to triumphant major** at the Keystar relight |
| Dawnstead (epilogue) | **blooms in full radiant major** — the leap finally reaches the sky |

State in each brief *where and how* the track uses it.

### 3.2 Light-type sonic signatures (the elemental palette)

Vesperholm's ten lights each have a sonic fingerprint. An area leans on the
signature(s) of its element so a region "reads as one ecosystem" by ear:

| Light / element | Sonic signature |
|-----------------|-----------------|
| **Ember** (hearth-fire) | warm 25% pulse lead, soft triangle "hearth" pulse, lullaby sway |
| **Tide** (moonlit water) | lilting compound/triple meter, bell-buoy chimes, gentle rocking bass |
| **Verdant** (glowmoss) | Lydian-tinged (#4) glassy bells, breathy pad, dewy wonder |
| **Stone** (deep-earth gleam) | low pulse/wave drones, dry pick-tap percussion, sparse, warm-tense |
| **Storm** (lightning) | staccato pulse, noise-channel gust swells, driving bass, fast |
| **Frost** (aurora) | suspended/quartal arpeggios, slow glassy chimes, wide "aurora swoosh" swell |
| **Solar** (stored daylight) | warm major pads/arps, harp-like pluck, radiant-but-remembered |
| **Lunar** (dreamlight) | slow arpeggiated pads, a lonely lead, faint clockwork tick |
| **Light** (true starlight) | bright bell timbre, ascending sparkle |
| **Dark / Hollowing** (coldfog/null) | detuned/guttering pulses, a single faltering melody, long silences, unresolved minor |

### 3.3 Voice palette & era policy

- **`gbc` is the band, not the ceiling.** The 4-voice roles — **`pulse25` lead,
  arp/harmony, `tri_bass` bass, `drums` (noise) percussion** — define the score's
  *identity*: the tune lives here. Keep those roles (and the same voices for the
  same roles) on every track so timbres stay related. But the *register* the band
  plays in is a choice (see the next two bullets), and most shipping area tracks
  now open up from the bare 4-voice chip into the lusher **`snes`** register.
- **Ship the early-game "first impression" maps in the richer `snes` register.**
  The first areas the player actually walks (the start town, its interior, the
  first route) carry the game's whole first impression, so they get the lush
  16-bit treatment rather than the bare chip. The recipe (the **SNES enrichment**,
  used on `tinderwick-a`, `tinderwick-b`, `dimglass-coast-a`):
  1. **Keep the tune.** Take the `gbc` Option-A lead and bass **note-for-note** —
     that's the area's identity and the Vesper motif; don't rewrite it.
  2. **Open the band.** Add, within the 8-voice `snes` budget (aim for **≤7 peak
     voices**, clarity over density): a warm sustained **`strings`/`pad`** carrying
     the **real chords** the chip could only imply; the arp re-voiced from
     `pulse12` to a **`pluck`** harp/music-box (same notes); a **sparse `bell`**
     glint at phrase ends for the **Light** signature; and an optional **`flute`**
     counter-melody answering the lead in a B section (call-and-response).
  3. **Separate registers** so it never muds: **bass `tri_bass` oct 2**, **pad
     `strings` oct 3**, **lead oct 4**, **`bell`/sparkle oct 5**. Pad/strings gain
     low (~0.28–0.3) — a bed, not a wall.
  4. **`era: "snes"`** gives the warm reverb (0.18) and chord stacking; still
     **render through the default `--engine chip`** — the chip synth plays the
     `snes` voices with reverb, which is what keeps the lush tracks cohesive with
     the rest of the score.
- **`gba`/`snes` for the genuinely big rooms too** — Nightreach Observatory, the
  Umbral Spire climax — and the explicit **"richer register" Option C** variants
  (the glacier as lush ambient, Dawnstead's curtain-call). A bare `gbc` 4-voice
  reading still has its place for the sparsest, loneliest cues (deep caves, the
  Hollowing's drained zones) where silence and thinness *are* the point.
- **Keep rendering through the chip engine.** Even `snes` specs render on
  `--engine chip` — that one engine across the whole soundtrack is the cohesion
  (see `style-guide.md` §5). Only use `--engine soundfont` when the user
  explicitly asks for a lusher/orchestral render of a specific track.

### 3.4 Key & tempo bands

Routes **110–135 BPM** · towns/hub **96–120** · caves **84–104** ·
emotional/ambient/Frost **66–92** · boss/blight **60–80** building to **~150**
at the climax. Major = safe/bright; natural/harmonic minor = tension/loss;
Lydian/Dorian/suspended = wonder/mystery. Keep an area's 2–3 options in
**compatible keys**, and mind that an adjacent **town↔route** pair shouldn't
clash — the **relative major/minor** trick is the easy win (e.g. a town in C, its
route in A minor or G).

### 3.5 The dawn arc (where each area sits)

The global brightness of the score travels from **blue-hour wistful → radiant
dawn** across the game. Use it to place each area's key/mode/brightness:

```
south (start)    east            north           west (pre-climax)   central         epilogue
wistful major ── wonder/discovery ── energy + cold ── reaching for dawn ── darkest → resolve ── radiant major
Tinderwick       Lowleaf/Cinderhead  Galehigh/Glacier  Solarium/Observatory  Coldfog/Penumbra/Spire  Dawnstead
```

The Hollowing's areas (**Coldfog Marches, Penumbra Ring**) are the **darkest,
least-resolved** points in the entire score; the **Umbral Spire** is where dark
finally turns to the triumphant major that the **Dawnstead** epilogue completes.

---

## 4. How the 2–3 options per area work

Every area/route in `docs/world/music-direction.md` carries **2–3 options** so the
team can *audition and choose* — they are different **valid interpretations of the
same place**, not three drafts of one idea, and each still instantly reads as that
place. The recipe:

- **Option A — Anchor.** The canonical reading; matches the area's one-line brief
  in `atlas.md`. The safe default to build first.
- **Option B — Mood sibling.** A different emotional lean of the same place
  (more melancholy vs more playful; sparser vs warmer; a different meter).
- **Option C — Diegetic / structural variant.** A context variant where it makes
  sense: a **relit/brightened** version (the constellation lit), a **post-dawn
  day-form** version, a **festival** version, a sparser **"explore-light"**
  ambient take, or a richer **`gba`/`snes`** register for a big moment.

Each option in that doc is written as a **ready `generate-midi` brief**: *preset ·
era · tempo, meter, key/mood · lead / harmony-arp / bass / percussion · loop body
length*, plus its distinguishing concept, its Vesper-motif treatment, and the
era-function it nods to.

---

## 5. Producing the area tracks (workflow)

A first pass generates **one loop per area** straight from its **Option A** brief;
B/C variants are generated on demand when a place wants auditioning. Battle,
Lumenary (arena), and victory/level-up stings are **shared cross-region cues**
layered on top — compose those once and reuse, don't re-score per area.

For each track: pick the option, build the spec to the brief (honour the voice
budget and the cohesion rules above), `midi.py build` then `render` one pass
(`--loops 1`) to `public/assets/audio/music/`, and key it to the map's `music`
field. Keep the `.mid` in `assets/audio/midi/`. Audition the loop seam with
`--loops 2`. See `SKILL.md` for the exact commands.
