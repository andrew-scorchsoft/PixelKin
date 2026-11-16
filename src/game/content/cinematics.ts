/**
 * Cinematic scripts — the cold-open prologue and any later "chapter card" sequences.
 *
 * A CinematicScript is a list of full-screen panel beats played by CinematicScene
 * (a dedicated scene, NOT the world cutscene runner): illustrated key-art stills with
 * narration over them, cross-dissolves between panels, and music as drama. It is data,
 * so a new prologue / interstitial = an entry here, never new scene code.
 *
 * Placed AFTER the Title (so the Splash audio-unlock gesture has happened — the
 * foreboding cue is audible from frame one). Missing panel art falls back to a
 * night-fill + starfield, so the sequence always plays.
 *
 * Tone contract (see docs/world/cinematics.md): dread lives in the quiet, hope in the
 * resolution. Dark and adult, but aspirational — the Wayfaring is a real calling.
 * Canon vocabulary only (kin, Lumenary, Gleam, Lantern Gift, vesperlamp, the Hollowing).
 */

/** One block of the credits roll: a role heading over the names that filled it. */
export interface CreditsSection {
  /** The credited role/department, e.g. 'Story & World'. */
  role: string;
  /** The people/studios/tools credited under it (one per line). */
  names: string[];
}

export interface CinematicBeat {
  /** Panel image key/path (served), e.g. 'assets/backgrounds/cinematic/coldopen-01.webp'.
   *  Omit to hold the previous panel. */
  panel?: string;
  /** Narration pages shown (typewriter, advance on Confirm). Empty = an atmospheric hold. */
  lines?: string[];
  /** Music on entering this beat: a key to crossfade to, or null to fade to silence. */
  music?: string | null;
  /** One-shot sfx key at beat start (e.g. the star-gutter cue). */
  sfx?: string;
  /** Optional emphasis at beat start. */
  fx?: 'shake' | 'flash';
  /** Auto-advance after this hold when the beat has no lines to read. */
  dwellMs?: number;
  /**
   * A credits roll for this beat: a slow upward scroll of role/name sections,
   * rendered over the held panel (or starfield). Skippable like any beat (Cancel
   * ends the whole sequence). When set, the beat shows the scroll instead of
   * narration lines. Optional `creditsTitle` heads the scroll.
   */
  credits?: CreditsSection[];
  /** Heading shown at the top of a `credits` scroll (e.g. the game's name). */
  creditsTitle?: string;
  /** A short line held along the bottom during the credits roll (beside the skip prompt). */
  creditsNote?: string;
}

export interface CinematicScript {
  id: string;
  beats: CinematicBeat[];
  /** Where to go when the sequence finishes (or is skipped). */
  next: { scene: string; data?: unknown };
  /** false = Cancel does not skip this sequence (the last scene of the game is watched). */
  skippable?: boolean;
}

const PANEL = (n: string): string => `assets/backgrounds/cinematic/${n}.webp`;

/** The opening prologue for a new game — the Long Dusk, the calling, the shadow. */
export const COLDOPEN_SOUTH: CinematicScript = {
  id: 'coldopen_south',
  beats: [
    {
      panel: PANEL('coldopen-01'),
      music: 'coldopen-foreboding',
      dwellMs: 1200,
      lines: [
        'Long ago, the night sky over Vesperholm was full of lanterns.',
        'Eight constellations, burning steady — the light that kept the dark a friend, and not a grave.',
        'And below them lived the kin: bright-hearted creatures of valley and shore, each carrying a spark of that same sky.',
      ],
    },
    {
      panel: PANEL('coldopen-02'),
      sfx: 'world-star-gutter',
      fx: 'flash',
      music: null,
      lines: [
        'Then, one by one, the lights began to go out. Some only dimmed. Some, going out, fell.',
        'They call it the Long Dusk: a night that fell, and will not lift.',
      ],
    },
    {
      panel: PANEL('coldopen-03'),
      music: 'coldopen-foreboding',
      lines: [
        'But where a light fails, the lamp-tenders answer.',
        'In the coast-town of Tinderwick, a child wakes to their Wayfaring — the long walk every lamp-tender\'s apprentice must one day make.',
        'A lamp to carry. A kin to walk beside. And a whole sky to relight, one constellation — one Gleam — at a time.',
      ],
    },
    {
      panel: PANEL('coldopen-04'),
      sfx: 'world-star-gutter',
      music: null,
      dwellMs: 900,
      lines: [
        'Yet something walks the roads where the lights have failed.',
        'It does not hurry. It is not cruel. It only waits — kindly, patiently — for the last star to go dark.',
        'That road is not yours. Not yet. Yours begins with a single lit lamp.',
      ],
    },
  ],
  next: { scene: 'World' }, // data filled in by the caller (TitleScene) so spawn stays canon
};

/**
 * THE ENDING — the dawn-break epilogue + credits roll, fired by the summit's
 * `script.dawn_breaks` via the `cinematic` op (the host persists FIRST, so a
 * Continue after the roll resumes at the summit with `flag:dawn` held — the
 * post-game's door). Bookends the cold open: that sequence watched the lights
 * go out; this one watches Vesperholm wake. The remembrance voice, in PAST
 * tense — the journey, already become a story. Routed → Title when done.
 */
export const ENDING_CREDITS: CinematicScript = {
  id: 'ending_credits',
  beats: [
    {
      panel: PANEL('dawnbreak-01'),
      music: 'dawn-breaks',
      dwellMs: 1400,
      lines: [
        'The Keystar caught — and the sky remembered itself.',
        'Light ran the Skyweave like flame along a wick: eight constellations blazing whole, and beneath them, for the first time in years, an east with colour in it.',
      ],
    },
    {
      panel: PANEL('dawnbreak-02'),
      lines: [
        'The morning came down the mountain the long way, the way you had gone up: by every road, to every door.',
        'In Tinderwick they rang the fair-bell at sunrise, for no reason anyone would write down. In Pearlmoor the boats put out unlit, and nobody minded.',
        'Lowleaf\'s moss bloomed out of season, embarrassed and glorious. In Cinderhead the miners came up squinting, and dimmed not one lamp all day.',
      ],
    },
    {
      panel: PANEL('dawnbreak-03'),
      lines: [
        'Galehigh flew every kite it owned with no flame on a single tail — daylight carried them. On the Pale Vault ice, the silent watch finally talked, all at once, about nothing.',
        'The Solarium\'s drowned garden steamed gold, its stored warmth giving way to the real thing. And at Nightreach the watchers slept — actually slept — under a sky that could mind itself for one morning.',
      ],
    },
    {
      panel: PANEL('dawnbreak-04'),
      sfx: 'world-lantern-light',
      lines: [
        'Two old star-tenders walked down a mountain together, one ladder\'s width apart, the way they had always worked.',
        'A rival lit out for the coast road, to see a particular harbour in daylight. A Waykeeper trimmed lamps that, for the first time in forty years, did not need him. He did it anyway. That is what tending is.',
        'And the long night ended the only way it ever could: not in a victory — in a morning. Dusk will come again. The lamps are ready. So are you.',
      ],
    },
    {
      // The roll holds the dawn panel and scrolls the credits up over it.
      music: 'ending-credits',
      creditsTitle: 'PixelKin',
      // shown along the bottom for the whole roll, beside the "B: SKIP" prompt
      creditsNote: 'ONE MORE SCENE AFTER',
      credits: [
        { role: 'A game by', names: ['Andrew Ward Studios'] },
        { role: 'Published by', names: ['Scorchsoft'] },
        { role: 'Story & World', names: ['Andrew Ward Studios'] },
        { role: 'Game & Battle Design', names: ['Andrew Ward Studios'] },
        { role: 'Code & Engine', names: ['Andrew Ward Studios'] },
        { role: 'Art & Sprites', names: ['Andrew Ward Studios'] },
        { role: 'Music & Sound', names: ['Andrew Ward Studios'] },
        { role: 'The 162 kin of Vesperholm', names: ['Themselves'] },
        { role: 'Built with', names: ['TypeScript', 'Phaser 3', 'Vite'] },
        { role: 'And for', names: ['Every lamp-tender who kept a light', 'through a long dark'] },
        { role: '', names: ['The dawn is worth the dusk.', 'Thank you for walking it.'] },
        { role: '', names: ['Don\'t go yet.', 'There is one more stop.'] },
      ],
    },
  ],
  // the credits hand on to THE DEPOT (its own script, so skipping the roll never skips it)
  next: { scene: 'Cinematic', data: { scriptId: 'the_depot' } },
};

/**
 * THE DEPOT (2026-11) — after the credits, the very last thing the game says. An old
 * walker's theory of where a road goes when it runs out of world: a coach depot, a
 * board of departures, and the discovery that the journey you just finished was one
 * you CHOSE, sitting on this same bench, before it began. Then you choose the next —
 * and the scene hands back to the Title (NEW GAME is the board). Stills:
 * assets/backgrounds/cinematic/depot/ -> tools/assets/pack_depot_frames.py.
 */
export const THE_DEPOT: CinematicScript = {
  id: 'the_depot',
  skippable: false, // skipping the credits lands here; this one you sit through
  beats: [
    {
      panel: PANEL('depot-01'),
      music: 'interior-lamplit',
      dwellMs: 1400,
      lines: [
        'There is a story some walkers tell, about where a road goes when it has run out of world.',
        'They say it comes to a depot. An old one. Wooden benches, a stove, a clock in no hurry at all.',
        'And along one wall, a board of departures as long as the room.',
      ],
    },
    {
      panel: PANEL('depot-02'),
      lines: [
        'Every line on the board is a whole journey: where it sets out, every stop along the way, and where it lets you down.',
        'Some are short. Some are hard. Some have a great deal of weather in them.',
        'Nobody hurries you. You sit as long as you like, reading the stops, working out which one is yours.',
      ],
    },
    {
      panel: PANEL('depot-03'),
      sfx: 'world-lantern-light',
      lines: [
        'And in your pocket there is a ticket you do not remember buying. Used. Punched eight times, each hole the shape of a star.',
        'Because the journey you have just finished was never handed to you. You chose it.',
        'You sat on this very bench, a long time ago, and read the stops: a dark that would not lift, a small lamp, a long climb. And you said: that one.',
      ],
    },
    {
      panel: PANEL('depot-04'),
      lines: [
        'An old walker on the next bench lifts a tin cup to you. He has been through here before. He says everybody has.',
        '"Took me a few goes to pick one with decent hills," he says. "No regrets. Well. One or two. They were the best bits."',
      ],
    },
    {
      panel: PANEL('depot-05'),
      lines: [
        'So you look up at the board again. All those roads. All those stops.',
        'There is no wrong one. There is only the next one.',
        'When you are ready, you stand up, and choose.',
      ],
    },
  ],
  next: { scene: 'Title' }, // the last scene hands control back to the Title screen
};

export const CINEMATICS: Record<string, CinematicScript> = {
  [COLDOPEN_SOUTH.id]: COLDOPEN_SOUTH,
  [ENDING_CREDITS.id]: ENDING_CREDITS,
  [THE_DEPOT.id]: THE_DEPOT,
};

export function getCinematic(id: string): CinematicScript | undefined {
  return CINEMATICS[id];
}

/** Every panel path across all cinematics, for PreloadScene to queue eagerly. */
export const CINEMATIC_PANEL_PATHS: readonly string[] = Array.from(
  new Set(
    Object.values(CINEMATICS).flatMap((c) => c.beats.map((b) => b.panel).filter((p): p is string => Boolean(p))),
  ),
);
