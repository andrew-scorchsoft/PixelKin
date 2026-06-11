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
}

export interface CinematicScript {
  id: string;
  beats: CinematicBeat[];
  /** Where to go when the sequence finishes (or is skipped). */
  next: { scene: string; data?: unknown };
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
        'And below them lived the kin: the bright-hearted creatures of valley and shore, each carrying a spark of that same sky.',
      ],
    },
    {
      panel: PANEL('coldopen-02'),
      sfx: 'world-star-gutter',
      fx: 'flash',
      music: null,
      lines: [
        'Then, one by one, the lights began to go out.',
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
 * The endgame send-off + credits roll. PLACEHOLDER COPY — a later content agent
 * replaces the prose and finalises the credited names; this exists so the
 * capability is real and routable (World → Cinematic('ending_credits') → Title).
 *
 * Shape worth keeping: a short held epilogue beat, then a `credits` scroll. The
 * `ending-credits` music key may not be rendered yet — MusicDirector loads it
 * tolerantly (missing → silence), so the roll plays regardless.
 */
export const ENDING_CREDITS: CinematicScript = {
  id: 'ending_credits',
  beats: [
    {
      panel: PANEL('ending-01'),
      music: 'ending-credits',
      lines: [
        '[PLACEHOLDER] The last constellation catches, and dawn climbs the eastern ridge over Vesperholm.',
        '[PLACEHOLDER] The Long Dusk lifts. The lamps you lit will keep — and the road home is warm.',
      ],
    },
    {
      // The roll holds the dawn panel and scrolls the credits up over it.
      creditsTitle: 'PixelKin',
      credits: [
        { role: 'Story & World', names: ['Andrew Ward Studios'] },
        { role: 'Game Design', names: ['Andrew Ward Studios'] },
        { role: 'Code & Engine', names: ['Andrew Ward Studios'] },
        { role: 'Art & Sprites', names: ['Andrew Ward Studios'] },
        { role: 'Music & Sound', names: ['Andrew Ward Studios'] },
        { role: 'Built with', names: ['TypeScript', 'Phaser 3', 'Vite'] },
        { role: 'For', names: ['Every lamp-tender on their Wayfaring'] },
      ],
    },
  ],
  next: { scene: 'Title' }, // the ending hands control back to the Title screen
};

export const CINEMATICS: Record<string, CinematicScript> = {
  [COLDOPEN_SOUTH.id]: COLDOPEN_SOUTH,
  [ENDING_CREDITS.id]: ENDING_CREDITS,
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
