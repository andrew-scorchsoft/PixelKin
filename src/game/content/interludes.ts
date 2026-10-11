/**
 * CROWN INTERLUDES (story panel X-4): "meanwhile, on the mountain".
 *
 * The genre's between-chapters cut: when a quadrant's crown completes, the camera
 * leaves the player for twenty-odd seconds to show what the antagonist is doing
 * — short, quiet, never cartoonish. Four of them, one per crown, escalating with
 * the falling-star thread (story-bible §11): a cinder FETCHED (South), the hoard
 * KEPT (East), a fall WATCHED land nearer (North), the Great Null's lever NOT
 * pulled — yet (West).
 *
 * How they play (WorldScene.maybeRunCrownInterlude): on the first idle frame
 * where an entry's `requires` flags are all held and its `seen_flag` isn't, the
 * world letterboxes, the bed fades, the screen fades to black, and the scene is
 * staged on a REMOTE map the player usually can't stand on yet (the Spire's
 * floors, the far marsh road): the map is built with ONLY the `cast` below (its
 * own NPCs are left out), the player hidden, the camera parked on `camera`. The
 * script runs, then the world fades back to the player's exact tile and facing.
 * Nothing is saved while staged, and nothing in a script may set a flag.
 *
 * Policy: only ever ONE plays at a time — the LATEST due entry in table order —
 * and playing it banks every earlier entry's seen flag too. So an interlude
 * never plays after a later one, and an old save that already holds several
 * crowns gets just the current one (the vignette that points where they're going)
 * instead of a backlog. Once the player has set foot in the Spire (or the dawn
 * has come) they are all moot: `INTERLUDES_CLOSED_BY` banks them unplayed.
 *
 * Optional colour: they gate nothing. Canon guards: the South one plays only
 * once the Chickenpig is caught (the first hours are a held tutorial — crown_south
 * can complete before it), and keeps the man unnamed (the Hollowing are named in
 * the East's B2, Còr's face is the North's B3 — so his portrait is held until
 * `flag:met_cor`). No Senna name (post-dawn only). Còr courteous and grieving.
 */
import type { NpcPlacement, TileCoord, WorldFlag } from '@game/data/world/types';
import type { ScriptRegistry } from './types';

export interface CrownInterlude {
  id: string;
  /** All must be held for the interlude to be due (the crown + any canon guard). */
  requires: WorldFlag[];
  /** Banked once played (or skipped past) — never repeats. */
  seen_flag: WorldFlag;
  /** Script ref (registered below) run as the staged cutscene. */
  script: string;
  stage: {
    /** A registered map id to stage on (built without its own NPCs). */
    map: string;
    /** Where the camera rests (the hidden player is parked here too). */
    camera: TileCoord;
    /** The actors the script addresses, by placement id. */
    cast: NpcPlacement[];
  };
}

const cor = (id: string, tx: number, ty: number, facing: NpcPlacement['facing']): NpcPlacement => ({
  id,
  at: { tx, ty },
  facing,
  sprite: 'warden_cor',
  movement: 'static',
});

/** Any of these held = the player is past the point the interludes look ahead to. */
export const INTERLUDES_CLOSED_BY: readonly WorldFlag[] = [
  'flag:spire_crown_1_seen', // stood inside the Spire
  'flag:seen_great_null',
  'flag:cor_answered',
  'flag:dawn',
];

/** In journey order — "latest" means the LAST due entry here. */
export const CROWN_INTERLUDES: readonly CrownInterlude[] = [
  {
    id: 'south',
    requires: ['flag:crown_south', 'flag:chickenpig_caught'],
    seen_flag: 'flag:interlude_south_seen',
    script: 'script.interlude_south',
    stage: {
      map: 'coldfog_marches_i',
      camera: { tx: 9, ty: 15 },
      cast: [cor('interlude_cor', 9, 20, 'up')],
    },
  },
  {
    id: 'east',
    requires: ['flag:crown_east', 'flag:met_hollowing'],
    seen_flag: 'flag:interlude_east_seen',
    script: 'script.interlude_east',
    stage: {
      map: 'umbral_spire_f3',
      camera: { tx: 21, ty: 7 },
      cast: [
        cor('interlude_cor', 21, 6, 'up'),
        { id: 'interlude_acolyte', at: { tx: 21, ty: 13 }, facing: 'up', sprite: 'hollowing_acolyte', movement: 'static' },
      ],
    },
  },
  {
    id: 'north',
    requires: ['flag:crown_north', 'flag:met_cor'],
    seen_flag: 'flag:interlude_north_seen',
    script: 'script.interlude_north',
    stage: {
      map: 'umbral_spire_f3',
      camera: { tx: 6, ty: 10 },
      cast: [cor('interlude_cor', 4, 10, 'left')],
    },
  },
  {
    id: 'west',
    requires: ['flag:crown_west', 'flag:met_cor'],
    seen_flag: 'flag:interlude_west_seen',
    script: 'script.interlude_west',
    stage: {
      map: 'umbral_spire_summit',
      camera: { tx: 11, ty: 7 },
      cast: [cor('interlude_cor', 11, 10, 'up')],
    },
  },
];

/**
 * The four staged scripts. The ENGINE brackets each one (letterbox in + bed out
 * before the cut, fade back + letterbox out after), so a script is only the
 * scene itself: 4–6 lines, ~20–30 s. No `setFlag`, no `cameraReset` (the
 * hidden player is not the subject), no Senna.
 */
export const INTERLUDE_SCRIPTS: ScriptRegistry = {
  // SOUTH — seen after: a cinder fetched. He is not named; we are a long way off.
  'script.interlude_south': [
    { op: 'wait', ms: 700 },
    { op: 'narrate', text: 'Far from your lamp, on a marsh road nobody walks any more, a man in faded grey is out in the dark.' },
    { op: 'move', actor: 'interlude_cor', to: { tx: 9, ty: 14 }, speed: 0.6 },
    { op: 'face', actor: 'interlude_cor', facing: 'left' },
    { op: 'wait', ms: 500 },
    { op: 'action', actor: 'interlude_cor', action: 'kneel', holdMs: 1200 },
    { op: 'narrate', text: 'He kneels in the grey field and lifts a cold stone out of the ash. A blue-grey glow lives in its cracks.' },
    { op: 'narrate', text: 'He wraps it in a clean cloth, the way you would carry something asleep.' },
    { op: 'face', actor: 'interlude_cor', facing: 'up' },
    { op: 'wait', ms: 600 },
    { op: 'move', actor: 'interlude_cor', to: { tx: 9, ty: 10 }, speed: 0.6 },
    { op: 'narrate', text: 'Then he walks on north, towards the mountain, like a man who has made this walk many times.' },
    { op: 'wait', ms: 500 },
  ],

  // EAST — seen kept: the hoard shelves filling. "Because someone should."
  'script.interlude_east': [
    { op: 'wait', ms: 600 },
    { op: 'narrate', text: 'High in the mountain there is a swept room where no lamp is lit. The shelves in it are filling.' },
    { op: 'action', actor: 'interlude_cor', action: 'gift', holdMs: 1000 },
    { op: 'narrate', text: 'The Warden sets one more cold stone on the linen, and tags it: the valley, the night.' },
    // In by the doorway and round the linen rows to stand at the Warden's elbow.
    { op: 'move', actor: 'interlude_acolyte', to: { tx: 21, ty: 11 }, speed: 0.8 },
    { op: 'move', actor: 'interlude_acolyte', to: { tx: 23, ty: 11 }, speed: 0.8 },
    { op: 'move', actor: 'interlude_acolyte', to: { tx: 23, ty: 7 }, speed: 0.8 },
    { op: 'face', actor: 'interlude_acolyte', facing: 'left' },
    { op: 'say', speaker: 'ACOLYTE', text: "Warden? ...There's no room left on the west shelf. May I ask why we keep them?" },
    { op: 'wait', ms: 700 },
    { op: 'face', actor: 'interlude_cor', facing: 'right' },
    { op: 'wait', ms: 900 },
    { op: 'say', speaker: 'WARDEN CÒR', text: 'Because someone should.' },
    { op: 'action', actor: 'interlude_cor', action: 'sad', holdMs: 1300 },
    { op: 'narrate', text: 'He straightens the tag a little. Then he takes up the broom and sweeps a floor that is already clean.' },
  ],

  // NORTH — seen falling: alone at a high window, a fall lands nearer.
  'script.interlude_north': [
    { op: 'wait', ms: 600 },
    { op: 'narrate', text: 'The mountain again. Còr stands alone at a high window, the way he does most nights, watching the sky.' },
    { op: 'wait', ms: 400 },
    // The live fall (a no-op with Ambient motion off; the line still tells it).
    { op: 'starfall', from: 'right', wait: true },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'shake', ms: 280, intensity: 0.004 },
    { op: 'narrate', text: 'A star comes loose and falls. It comes down nearer than the last one did. They all do, now.' },
    { op: 'action', actor: 'interlude_cor', action: 'sad', holdMs: 1400 },
    { op: 'narrate', text: 'A thin chain at his collar runs down into his breast pocket. His hand goes there, and rests.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: "Another one. ...Rest. I'll come and fetch you home." },
    { op: 'action', actor: 'interlude_cor', action: 'turnAway', holdMs: 1200 },
  ],

  // WEST — the Great Null's lever, not pulled. Yet.
  'script.interlude_west': [
    { op: 'wait', ms: 600 },
    { op: 'narrate', text: 'The top of the mountain. Under the Great Null, one gauge rests at zero, and a lever waits beside it.' },
    { op: 'move', actor: 'interlude_cor', to: { tx: 11, ty: 8 }, speed: 0.5 },
    { op: 'wait', ms: 600 },
    { op: 'action', actor: 'interlude_cor', action: 'gift', holdMs: 900 },
    { op: 'narrate', text: 'Còr lays his hand on the lever and leaves it there a long time. The dark bell above him is silent.' },
    { op: 'wait', ms: 1000 },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'Not yet. The apprentice is still on the stair. I will wait for them.' },
    { op: 'action', actor: 'interlude_cor', action: 'bow', holdMs: 1100 },
    { op: 'narrate', text: 'He takes his hand away, one finger at a time.' },
    { op: 'wait', ms: 500 },
  ],
};
