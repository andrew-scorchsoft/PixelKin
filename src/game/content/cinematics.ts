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
        'In the coast-town of Tinderwick, a child wakes to their Wayfaring —',
        'a lamp to carry, a kin to walk beside, and a whole sky to relight, one Gleam at a time.',
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

export const CINEMATICS: Record<string, CinematicScript> = {
  [COLDOPEN_SOUTH.id]: COLDOPEN_SOUTH,
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
