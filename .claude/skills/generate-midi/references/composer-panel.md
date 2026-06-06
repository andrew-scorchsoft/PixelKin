# The Panel — principles for iconic retro MIDI

This skill was designed by convening an imaginary panel of master craftspeople
from the cartridge era and distilling *how they made small music feel huge*.
We name the legends as **influences on technique**, never as works to copy.
Counterpoint, leitmotif, call-and-response, hardware economy — these are craft,
not copyright. PixelKin's melodies must be **original** (see `VISION.md`); what
we borrow from these masters is the *discipline*, not a single bar of their music.

Each panellist owns one chair. When you compose, you are channelling all of them.

---

## Chair 1 — The Melodist (the hook above all)

*Influence: the overworld/route writers who made a six-note phrase you can hum
30 years later.*

- **The melody is the asset.** A retro track lives or dies on a singable lead
  line. Before you place a single chord, write a melody you could whistle with
  no accompaniment. If it isn't memorable naked, no production will save it.
- **Small range, strong shape.** Stepwise motion with one or two bold leaps.
  The ear remembers contour, not complexity.
- **Repeat, then reward.** State a phrase, repeat it nearly identically, then
  answer it with a variation (AABA / ABAC). Repetition is what makes it stick;
  the small change is what keeps it alive on the 50th loop.
- **Front-load the hook.** The first two bars must announce the tune. Players
  hear the loop point far more often than the bridge.

## Chair 2 — The Storyteller (MIDI that sets the scene)

*Influence: the grand-RPG composer whose sequenced, sample-based music made
players feel a place even through a tinny speaker — "it's only MIDI, but it
sets the whole tone".*

- **Mood first, notes second.** Decide the *feeling* (cosy, anxious, lonely,
  triumphant) and the *place* (sunlit meadow, dripping cave, rival's arena)
  before choosing a key or tempo. Every later decision serves that one feeling.
- **A theme is a character.** Give important places/people a short **motif**
  (a 3–5 note shape) and reuse it transformed — major in town, minor in the
  cave, slow and tender at a parting. This is leitmotif; it's how a soundtrack
  becomes a *world* instead of a playlist.
- **Harmony carries emotion.** Major = safe/bright; minor = tense/sad; a
  borrowed/modal chord = wonder or unease. The lead tells you *what*; the
  chords tell you *how to feel about it*.
- **Silence is an instrument.** Rests and space read as tension and depth.
  Don't fill every sixteenth.

## Chair 3 — The Groove Architect (rhythm and the lush sample sound)

*Influence: the platform-action composer who got funk, swing and atmosphere out
of a handful of SNES sample voices.*

- **Bass is half the song.** A walking or syncopated bassline gives retro music
  its forward motion. On chip hardware this is the triangle/wave channel — never
  leave it idle.
- **Percussion is colour, not metronome.** Even one noise channel doing
  kick/snare/hat transforms energy. Vary the pattern across the loop so it
  breathes; add a crash or fill at the loop seam.
- **Groove from placement.** Syncopation, anticipations, and light swing make a
  4-voice piece feel alive. Tempo sets adrenaline: ~150–170 BPM battles, ~110–
  135 routes, ~70–96 emotional/cave.
- **Texture within the budget.** Pads, echo, and arpeggios make 8 sample voices
  sound orchestral. Reverb (the SNES echo unit) glues everything — use it on
  SNES/hi-fi tracks, keep it off pure chip tracks.

## Chair 4 — The Constraintsmith (the hardware is the instrument)

*Influence: the chip composers who treated 4 channels not as a limit but as a
style.*

- **Know your voice budget and honour it.** NES/GB/GBC = ~4 voices. Decide the
  roles up front: **lead, harmony, bass, percussion.** That's the whole band.
- **Fake chords with arpeggios.** No chord channels on chip hardware. Imply a
  triad by playing its notes in fast succession on one pulse channel
  (`C4e E4e G4e E4e ...`). This rapid broken chord *is* the classic chip sound —
  lean into it, don't apologise for it.
- **Duty cycle = timbre.** 12.5% is thin/sparkly (good for second lead/arps),
  25% is the classic singing lead, 50% is round and hollow (organ/pads). Switch
  duties to differentiate two pulse channels.
- **Constraint breeds identity.** The triangle's fixed volume, the noise
  channel's grit, the wavetable's hollow tone — these "limitations" are exactly
  what makes the era *sound like the era*. A track that ignores them sounds like
  generic MIDI, not like a handheld classic.

## Chair 5 — The Sound Designer (it must read on a tiny speaker)

*Influence: every engineer who mixed for a mono piezo the size of a coin.*

- **Mix for the worst speaker.** Phones and handhelds have no bass and no
  stereo. Keep the lead in a register that cuts (~C4–C6); don't bury the tune.
- **Avoid mud.** Two mid-range voices fighting in the same octave turns to
  porridge. Separate by register and rhythm.
- **Loudness ≠ quality.** Leave headroom; let the synth normalise. Clipping a
  chip track just sounds broken, not loud.
- **Consistency is cohesion.** A whole soundtrack should feel like one hand
  wrote it: a shared palette of voices, a consistent reverb amount per era, a
  recurring main motif. That cohesion is the brief — every track a sibling.

---

## The panel's checklist (run before you ship a track)

1. Can you hum the lead with the music off? If not, rewrite the melody.
2. Does it state → repeat → answer (a clear A/B form), not wander?
3. Do you stay within the era's voice budget, with roles assigned
   (lead / harmony / bass / percussion)?
4. On chip eras: harmony via arpeggios, *not* stacked chords?
5. Does the bass move and the percussion vary across the loop?
6. Does the **last bar lead back into the first** with no bump? (loops)
7. Does a one-shot (fanfare/jingle) **resolve on the tonic** and stop?
8. Does it match the rest of the soundtrack — same palette, same reverb, the
   recurring motif where it belongs?
9. Is every note **original** — no quoting an existing game's actual melody?
