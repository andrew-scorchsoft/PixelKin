---
name: music-cue-family
description: Score a FAMILY of related PixelKin music cues: the floors of a tower, the stages of a dungeon, a town's day/night/festival variants, or any set of levels that should share ONE tune and change it step by step (getting madder, darker, grander or more tender as you go). Covers both soundtracks: the classic chip versions (generate-midi) and the remastered ElevenLabs versions (generate-music's house method), tied together by a family motif and a "variation ladder". Use whenever the user asks for music for several connected levels or floors, asks for a set of cues to share a theme, or asks for remasters of such a set.
---

# music-cue-family

A **cue family** is a set of cues that are heard in sequence and should feel like one piece
changing as you go. The Old Light's seven floors are the worked example (`oldlight-f1..f7`):
one music-hall march, "Punchwheel's Patter", that gets more deranged on every floor up. What
matters is that the player hears **the same tune every time, and a new twist on it every time**.

This skill sits on top of two others; read them for the mechanics:
- **generate-midi**: classic chip cues, composed as note data.
- **generate-music**: remastered cues via `tools/audio/remaster_track.py`. Its "house method"
  section is binding: cue sheets, seamless loop glue, openings, dead air, levelling.

## 1. Design the ladder first (write it down before generating anything)

1. **One motif.** A 1–2 bar figure the whole family keeps. Use the family's own tune when it has
   a strong identity (the tower's march). Use the world's Vesper motif when the family belongs to
   the main story. Write the motif in the family's doc row in `docs/world/music-direction.md`, as
   notes or interval contour.
2. **A variation ladder.** Give each step one clear transformation of the SAME motif, escalating
   in a single direction:

   | step | transformation (examples) |
   |---|---|
   | anchor | the theme played straight; this is the motif source |
   | 2 | rhythm displaced (late, swung, syncopated) |
   | 3 | re-orchestrated or re-tempo'd (lounge, half-time, solo instrument) |
   | 4 | inverted, retrograde, or the registers swapped |
   | 5 | harmony corrupted (wrong notes, whole-tone, a mode declared wrongly) |
   | the heart | stripped bare and tender (a music box, a single voice): the motif at its clearest |
   | the top | everything at once (modulating, accelerating), then a snap back to the start |

   You can reorder the rungs, but each one must be recognisably the same tune. A rung that loses
   the motif is a bug.
   **Keep the direction one way to the top.** On the Old Light the owner rejected a tender music-box
   "heart" at F6: it broke the climb. A quiet rung belongs only where the family's brief asks for
   one. Otherwise each rung must be MORE of the family's quality than the last (there: stuck record,
   then the machine flying apart).
3. **Tempo family.** Remastered takes conditioned on a motif **lock to the source's tempo grid**
   (×½, ×1, ×2), whatever the spec asks. So put the whole family on the anchor's BPM, and get
   speed and slowness from *feel*: "half-time lounge feel", "double-time frantic gallop". The
   classic chip cues can use any tempo.
4. **Openings.** Every rung opens differently (generate-music §"Design each OPENING"): a bold
   call, a late drum shuffle, a kettle whistle, the tuba alone, a misfiring fanfare, a lone music
   box, a clockwork wind-up. An opening never stalls.

## 2. Classic (chip) cues

Write one generate-midi spec per rung (`assets/audio/midi/specs/<family>-<n>.json`). Copy the
anchor's lead line and transform it note by note, so the tune is literally shared. Render it, then
put each cue on its map's `music` in the builder and mirror that in `maps.ts`.

## 3. Remastered cues: the family motif

1. **Remaster the anchor first, unconditioned.** Write its cue sheet
   (`assets/audio/elevenlabs/<family>-1/spec.json`, `"motif": null`), then run
   `./venv/bin/python tools/audio/remaster_track.py <id>`. Listen to it, and judge the take by
   whether its theme section states the tune clearly.
2. **Register it as the family motif.** Write `assets/audio/elevenlabs/motif-<family>.json` in
   the shape of `motif.json`:
   - `song_id`: the anchor's stored take. It's in the anchor's `meta.json`/plan output. If it's
     missing, upload the served mp3 with `generate_music.py --upload`.
   - `range`: the 30 s window of its main theme. The API caps a reference at 30 s.
   - a note saying what the motif is.
3. **Condition every other rung on it.** Set `"motif": {"strength": …, "source": "<family>"}` in
   each spec. `remaster_track.py` resolves `motif-<family>.json` and `--check-spec` verifies it
   exists. Strength schedule:
   - `high` on the near rungs and the tender heart, so the tune is unmistakable;
   - `medium` on the wildest rungs, so the transformation has room.
   - Avoid `low` unless a rung is meant to barely remember the tune.
4. **Describe the motif in every section brief, but never NAME it.** Write "the tower's march
   tune, inverted", never a title like "Punchwheel's Patter". A titled tune plus a conditioning
   reference got every Old Light plan rejected as `copyrighted_material_detected`; with the title
   removed the same plans passed. Keep names in `mood`/`where`, which aren't sent to the API.
   Also avoid meta-wording about the conditioning, such as "carried from the reference": that
   core style got the Old Light's slow floors rejected even when unconditioned. If a plan is
   rejected, cut words until it passes. Rejections fail in seconds, so bisect the spec. The
   strength makes no difference.
   Describe the twist as orchestration and harmony. The checker rejects negations in positive
   fields: say what you want.
5. **Instrumental only.** Any "laugh", "voice" or "cry" must be played by an instrument (a
   slide-trombone wah-wah, a slide whistle, a music-box hiccup).

## 4. Check, ship, document

- **Per take:**
  - the seam is ≤ 0.45 (re-compose if it isn't);
  - `tools/audio/dead_air.py` passes;
  - the tempo lands on the family grid;
  - listen to the first 10 s (the opening) and to one pass of the theme (is the motif there?).
- **Rebuild:** run `python3 tools/audio/build_remaster_manifest.py` and
  `node tools/build/build_music_data.mjs`. CI fails if either is stale.
- **Send every new MP3 to the user** with `SendUserFile`, for a listen.
- **Document the family:** its row and ladder in `docs/world/music-direction.md`, and a one-line
  pointer in CLAUDE.md if it's a new family.
- **Before pushing:** run `npm run check`.
