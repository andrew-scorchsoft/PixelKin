# PixelKin — Vision

## The one-line pitch

PixelKin is a retro creature-collecting adventure that sells a feeling:
the warm, wide-eyed wonder of being a kid in the late '90s, hunched over a
handheld in the back of a car, discovering a whole world one tall-grass step
at a time.

## Who it's for

The millennial who grew up on monster-collecting RPGs and is now in their mid-
to-late thirties. They have a job, maybe kids, not much time — and a deep,
specific nostalgia for the era of the Game Boy and Game Boy Color. They don't
want a slot-machine mobile game. They want the *thing they remember*: the
quiet thrill of a new town, a full party of creatures they've grown attached
to, a map that keeps unfolding.

We are not chasing the hardcore-completionist or the modern-AAA player. We are
making the game our player wishes they could go back and play again for the
first time.

## The feeling we're selling

Every decision serves these feelings, in roughly this order:

1. **Nostalgia.** It should *feel* like 1999–2001 handheld gaming — not a
   parody of it, a loving continuation. Chunky pixels, a tight colour palette,
   chiptune-leaning music, menus that go *blip*.
2. **Collecting.** The core dopamine loop. Finding a new creature, completing a
   set, watching a favourite grow. The joy is in the gathering and the
   attachment, not the grind.
3. **Exploration.** A world that rewards curiosity. Routes, towns, caves,
   secrets behind a ledge you couldn't reach an hour ago. The map is the
   adventure.
4. **Delight.** Small, frequent moments of charm — an animation, a line of
   dialogue, a creature's idle wiggle. Cosy, never cynical.

If a feature doesn't strengthen one of these, it's probably not PixelKin.

## The look

Handheld-era pixel art, evolving across the journey of building the game the
same way the hardware did:

- **Anchor era:** Game Boy Color — limited palette, 16×16 tiles, bold readable
  sprites with personality.
- **Allowed to grow:** as we build, we lean toward the slightly richer Game Boy
  Advance register (more colours, smoother animation, light effects) — "the
  same world, a bit more advanced," mirroring how players' real handhelds got
  better over those years.
- **Internal resolution is fixed and small (240×160)** and scaled up with
  nearest-neighbour, so pixels stay crisp, square, and deliberate at any screen
  size. No smooth, modern, vector-y art. Ever.

The PixelKin logo (`assets/pixelkin-logo.png`) sets the palette and tone:
deep night-blue backdrops, a bright diamond cyan, and grass / fire / water
creature accents.

## The play (early sketch — to be padded out)

- Explore a connected overworld of routes, towns, and dungeons.
- Encounter wild **kin** (our creatures), befriend/collect them, build a party.
- Turn-based battles built on a simple, readable elemental type system.
- Grow your kin, complete your collection, uncover the world's story.
- Web-first, designed to feel just as natural with touch as with a keyboard,
  so the eventual mobile version is the same game — not a port that fights the
  controls.

(Detailed mechanics — type chart, capture loop, progression, story — get their
own design docs under `docs/` as they firm up.)

## Originality & copyright — read this before adding content

PixelKin is **inspired by** the monster-collecting genre. It is **not** a copy
of any existing game, and must never become one. The genre's *ideas* — collect
creatures, build a party, turn-based elemental battles, explore a region — are
not protectable. The specific *expression* of any one franchise absolutely is.
We borrow the feeling, never the assets.

**Hard rules:**

- **No existing creatures, names, characters, places, or logos.** Every kin,
  person, town, item, and move is original to PixelKin. No "looks just like
  <that one>." No recognisable silhouettes.
- **No copied art, sprites, tilesets, fonts, UI, or maps** from any commercial
  game. All visual assets are original (hand-made or generated via the
  `generate-image` skill from original briefs).
- **No copied or imitated music.** Compose original tracks via the
  `generate-music` skill. Describe *mood and era*, never "sounds like
  <franchise>'s theme" and never name a copyrighted track or composer to mimic.
- **No copied text or story.** Dex entries, dialogue, lore — all original.
- **No trademarked terms** in names, marketing, or code. We have our own
  vocabulary: creatures are **kin**, the world is **PixelKin's** own.
- **Describe by genre, not by brand.** In prompts, issues, and commits, say
  "monster-collecting RPG," not the name of a specific franchise.

When in doubt, make it more original, not less. The goal is for a player to
feel the nostalgia *and* recognise PixelKin as its own thing.

## Non-goals

- Not free-to-play, not built around microtransactions or energy timers.
- Not photorealistic, not 3D, not a modern art restyle of a retro idea.
- Not a clone trading on another game's specific content or identity.
