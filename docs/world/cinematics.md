# Cinematics & story delivery — the binding standard

> How PixelKin *tells* its story, not just where the story goes. This is the authoring
> contract for cold opens, cutscene staging, portraits, and music-as-drama. The
> [walkthrough](./walkthrough/) says **what** each beat is; this says **how** it lands.
> The first hour (South) is the **worked example** every later region copies — when you
> build a new region's beats, open the South scripts and this doc side by side.

PixelKin's design is rich; the job here is to make the *delivery* match it. The genre's
best openings (a dramatic narrated intro over music; a foreboding cold open before
control) sold a feeling before they sold a mechanic. We do the same: **dread in the
quiet, hope in the resolution.** Dark and adult, but aspirational — the Wayfaring is a
real calling, not a chore.

## The cinematic toolkit (engine primitives)

All story presentation is **data**: a cutscene is a `CutsceneStep[]` in
`src/game/content/scripts.ts`, a cold open is a `CinematicScript` in
`src/game/content/cinematics.ts`. Never write bespoke per-scene cutscene code — compose
these primitives. New ops are added once to `CutsceneStep` (`src/game/content/types.ts`)
+ the `CutsceneRunner` switch.

| Op | Use it for |
|----|------------|
| `say {speaker,text,portrait?,expr?}` | Attributed speech, optionally with a character bust + expression. |
| `narrate {text}` | Un-attributed prose (the "voice of the game"); softer, slower, no name. |
| `music {key\|null}` | Swap the bed — **crossfades** when one is already playing; `null` fades to silence. |
| `musicCrossfade {key,ms}` / `musicFade {ms}` | Explicit smooth swap / fade-out. |
| `musicSting {key,volume?}` | A one-shot cue over the bed (the Gleam fanfare is one). |
| `silence {ms}` | **The dread beat** — fade the bed out and hold on the quiet. |
| `letterbox {on}` | Cinematic bars in/out to frame a set-piece. |
| `shake {ms,intensity?}` / `flashColor {color,ms?}` / `tint {color,alpha?,ms?}` | Impact, a coloured flash, a held colour wash (warm for a Gleam, cold for the dusk omen). |
| `cameraFocus {actor?\|to?,zoom?,ms?}` / `cameraReset` | Pan/zoom onto a subject, then return to following the player. **Always `cameraReset` before the scene ends.** |
| `gleam {element}` | The diegetic constellation-relight cue (fanfare sting + flash). |

The **cold open** is a separate scene, `CinematicScene` (key `Cinematic`), playing a
`CinematicScript` of full-screen illustrated **panels** with narration and cross-dissolves.

## Hard rules

1. **Audio-unlock gate.** Browsers block sound until a user gesture; the `Splash` scene is
   that gate. Any cold open / music-first beat MUST sit **after** the player has passed a
   gesture (New Game is reached via the Title, which is post-Splash — so the cold open is
   safe there). Never put a music-led cinematic before the first gesture.
2. **Everything degrades silently.** A missing panel falls back to a starfield; a missing
   portrait to a name-only box; a missing music/sfx cue to silence (the `loadAudio` /
   `loadImage` pattern). A beat must never crash or block on a missing asset. So you can
   author scripts against assets that don't exist yet — they just play plainer.
3. **Skippable.** The cold open skips on `Cancel` (B/X). Long cinematics respect it.
4. **One input owner.** Narration is read through the shared `DialogueBox` (advance on
   Confirm); never also listen for Confirm in the host scene during a narration page, or
   it double-reads. The cold open watches **Cancel** (skip) on a *separate* controller.
5. **Canon vocabulary only** (kin, Lumenary, Gleam, Lantern Gift, vesperlamp, kindling,
   the Hollowing, Wren, Fenn, Còr). Never generic monster/gym/badge, never another
   franchise's terms — including in prompts and commit messages.

## Portraits

- One **32×32 spritesheet per character** under `public/assets/portraits/<id>.png`, frame
  index = expression, registered in `src/game/content/portraits.ts` (`PORTRAITS`). The
  DialogueBox draws the bust top-left and reflows the text beside it.
- Use a portrait for **named, story-bearing characters** in cutscenes (Fenn, Wren, Brisa,
  Reyl, the lamplighter, later Còr/Fenn/Nessa…). Pick the expression that does emotional
  work: `grave` when the sky loses a light, `warm`/`smile` for kindness, `proud` on a
  Gleam, `unsure` for Wren's wobble. Don't portrait incidental NPCs/signs — keep them
  name-only so the cast stands out.
- Preloaded eagerly in `PreloadScene` from `PORTRAIT_SHEETS`. Add a character = a sheet +
  a registry entry; no code.

## Music as drama (the cadence)

The score is designed to brighten minor→major across the game (the celestial calendar).
Punctuate it at the beats that matter:

- **Scene/track change → crossfade**, never a hard cut (the `music` op now crossfades for
  free).
- **Dread → `silence`.** Before a light fails (the dusk omen, a drained site), fade the
  bed out and hold. The quiet is the scare.
- **Impact → a one-shot sting** over a (possibly silent) bed: the `world-star-gutter` cue
  as a star dies; the Gleam fanfare as one relights.
- **Gleam → minor→major.** Hold a beat of silence, bloom the light (warm/cool `tint` +
  the lamp sfx), fire `gleam`, then **crossfade to the festival swell** (`gleam-emotional`)
  as the town begins to celebrate. A Gleam is *belonging*, not a trophy — let the music say
  so. (Recipes for `coldopen-foreboding` and `gleam-emotional` live in
  [music-direction.md](./music-direction.md).)

## The cold-open pattern (worked example: `coldopen_south`)

A new game opens on `CINEMATICS['coldopen_south']` (4 panels) before spawning into
Tinderwick. Its shape is the template for any later "chapter card":

1. **Establish the world + the want** — the sky full of constellation-lanterns; the
   Wayfaring as a calling. Music: the foreboding cue, soft.
2. **Land the threat** — a star *winks out*: `silence` → the gutter sting + `flash` → the
   thesis named ("the Long Dusk"). Foreboding.
3. **Name the hero's road** — the lamplit doorway, the lamp, the kin, the sky to relight.
   Aspirational; the music reaches (unresolved — the answer is the playthrough).
4. **Plant the shadow** — a distant, still, cowled figure under the dead sky; one grave,
   unexplained line. The early **Hollowing seed** (see below).

Each beat is `{ panel, lines[], music?, sfx?, fx? }`. Hold/auto-advance with `dwellMs`
when a beat has no lines.

## Dark-but-aspirational tone (and seeding the antagonist early)

The Hollowing is **never cartoonish** — grief dressed as mercy. We can seed *dread* in the
first hour without spending the formal B2 reveal (which the spine locks to East):

- A **distant figure** in the cold open (panel 4) — present, patient, unexplained.
- The **dusk omen** (`script.dusk_begins`) — staged as a quiet set-piece, not a text crawl.
- A **pinned letter** on Dimglass Coast (`sign.dimglass_pinned_letter`) — the Hollowing's
  *voice* (courteous, sorrowful, unsigned) before its face; a second hand has scratched the
  name out and written "DO NOT LISTEN."
- A **grave aside** from the old lamplighter — "a cold that follows the dark down off the
  north road… and it doesn't feel like weather."

This is the FF7-style move: something is wrong, and watching, long before you understand
it. Balance every dark beat with an aspirational one nearby (Fenn's warmth, the
Lantern-fair, the Gleam swell) — the game is melancholy, not bleak.

## When you build a later region

Each region's walkthrough file carries a **"Cinematic staging"** note per major beat
(which primitives + which assets it will use). Treat it as the acceptance spec: a Gleam
without the minor→major swell, or a Hollowing reveal without `silence`/`letterbox`, is a
content bug. Copy the nearest South script as your starting point, swap the words/assets,
and keep the cadence.
