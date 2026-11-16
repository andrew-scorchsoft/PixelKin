/**
 * THE HARTWAY (2026-11) — the climbers' road over the Hartshoulder: the last pitch of
 * the Windward pass, from the high crags (windward_stair_ii) over the top to Pale
 * Vault, walked with GREG. MAIN PATH, joined to the pass by its EDGES: the low road
 * is buried for good, the road comes round the Shoulder onto the Landing, and the
 * Seat's trail walks down into Pale Vault. The two RIDGES are solid crest tiles that
 * nobody can walk: the `edge` op takes Greg and then you across, a boot at a time, so
 * without Greg the mountain itself stops you (no gate, no closed road).
 * It is also Paul content, so it still SHIPS SILENTLY:
 * never in the changelog; the guide describes the step without the hidden names.
 * Spec: docs/world/walkthrough/12-the-hartway.md. Builders: build_hartway_climb.py +
 * the blocks in build_windward_stair_ii.py / build_pale_vault_glacier.py /
 * build_galehigh_terraces.py; art hartforge.py + hartway_set; stills
 * assets/backgrounds/cinematic/hartway/.
 *
 * The true story under it (Paul's, told to the owner): Paul went alpine hiking with
 * GREG, who was experienced and utterly confident; Greg went first, and Paul's job
 * was to stop Greg doing stupid things. Once, on a snow ridge Paul would never have
 * crossed alone, Greg's legs went shaky halfway and they both saw it was worse than
 * they'd thought; at the far end they sat down and laughed, then walked up to the
 * safe trail. And once, from a ridge the animals had taken back, they watched a mist
 * roll up the mountain with a great herd inside it, shadows all around them, using
 * the mist as cover to climb.
 *
 * In the game the PLAYER takes Paul's end of the rope. Greg hasn't climbed since his
 * partner stopped ("nobody to tell me no"). The herd is the SUNSTAGS (#121), the light
 * of old summers in their antlers: the Hartway is the harts' own way up.
 *
 * The loop (all flags):
 *   flag:q_hartway        the rule heard (Hollis / the drifted road) or Greg met — JOURNAL
 *   flag:greg_met         you've talked to Greg in Galehigh
 *   flag:greg_found       Greg said yes (you promised to say "No, Greg") -> he waits on the Landing
 *   flag:greg_roped       tied in -> the Staircase beat arms (he leads, you are edged across)
 *   flag:hart_p1_done     the Staircase is behind you
 *   flag:hart_ladder_1    Greg's rope ladder down band A (a flag-gated span + object)
 *   flag:hart_b1_done     the chimney beat (flag:hart_sense_1 if you said "No, Greg")
 *   flag:hart_p2_done     the Whiteback is behind you (flag:hart_sense_2: roped short)
 *   flag:hart_ladder_2    the second rope ladder (band B, east)
 *   flag:hart_b3_begun/_done  the lip beat at the Seat (flag:hart_sense_3)
 *   flag:hart_sense_all   DERIVED (FlagStore COUNT_AT_LEAST flag:hart_sense_ x3)
 *   flag:hart_mist_seen   you sat on the Seat and the herd came up in the mist
 *   flag:hart_rope_1/2    DERIVED (ANY_OF): Greg's ladder, or a milestone from beyond the
 *                         pass -> the rope-ladder spans + objects (old saves never locked out)
 *   flag:pass_open        DERIVED (FlagStore ANY_OF): the Seat reached, or you were
 *                         already past the pass (stages Hollis / Andrew / the NEXT panel)
 *
 * OPTIONAL, for players who know Paul (S4+): his lamp menu gains "Greg?" once the quest
 * is open -> PAUL'S ROPE-END (flag:greg_token) -> Greg knows the knot (extra lines);
 * and afterwards you can tell Paul (flag:q_hartway_done). None of it gates anything.
 *
 * A lost choice costs nothing (Greg is embarrassed, never hurt).
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

const HOOK = 'flag:q_hartway';
const TOKEN = 'flag:greg_token';
const FOUND = 'flag:greg_found';
const ROPED = 'flag:greg_roped';
const MIST = 'flag:hart_mist_seen';
const DONE = 'flag:q_hartway_done';
const CLIMB_MUSIC = 'windward-stair-a';
const STILL = (n: string): string => `assets/backgrounds/cinematic/hartway-${n}.webp`;

const g = (text: string, extra: Partial<CutsceneStep> = {}): CutsceneStep =>
  ({ op: 'say', speaker: 'GREG', text, ...extra }) as CutsceneStep;
const h = (text: string): CutsceneStep => ({ op: 'say', speaker: 'HOLLIS', text });
const p = (text: string, extra: Partial<CutsceneStep> = {}): CutsceneStep =>
  ({ op: 'say', speaker: 'PAUL', text, ...extra }) as CutsceneStep;
const n = (text: string, extra: Partial<CutsceneStep> = {}): CutsceneStep =>
  ({ op: 'narrate', text, ...extra }) as CutsceneStep;

/**
 * A precedence chain: stages listed LATEST FIRST as [flag, steps]; exactly one plays
 * for any mix of flags (the first whose flag is held), else `otherwise`.
 */
function chain(ref: string, stages: [string, CutsceneStep[]][], otherwise: CutsceneStep[]): ScriptRegistry {
  const out: ScriptRegistry = {};
  let name = ref;
  stages.forEach(([flag, steps], i) => {
    const hit = `${ref}__s${i}`;
    const rest = `${ref}__r${i}`;
    out[name] = [
      { op: 'run', ref: hit, if_flag: flag },
      { op: 'run', ref: rest, unless_flag: flag },
    ];
    out[hit] = steps;
    name = rest;
  });
  out[name] = otherwise;
  return out;
}

/** "Rest by the fire?" — a rest point you choose (never a forced sleep on a chat). */
const rest = (line: string): CutsceneStep[] => [
  n(line),
  {
    op: 'choice',
    prompt: 'Rest by the fire?',
    options: [
      { label: 'REST', ops: [{ op: 'heal' }] },
      { label: 'NOT NOW', ops: [] },
    ],
  },
];

const HOLLIS_HOOK: CutsceneStep[] = [
  h('Hollis, rope-warden. This is the Landing: the foot of the Hartway. The low road went under the drift, so Pale Vault is over the top now.'),
  h('One rule, older than me: [[nobody goes up alone]]. Two on a rope. One with the nerve, one with the sense.'),
  h('You don\'t WALK a ridge up here. You edge it, a boot at a time, behind someone who knows it. There\'s one left who does: [[Greg]].'),
  h('He\'s in [[Galehigh, at the top of the town]], staring up here like the hill owes him money. [[The drop-steps in the crags\' south-west corner]] put you out beside him.'),
  { op: 'setFlag', flag: HOOK },
];

/** The top of the Staircase: Greg fixes the first rope ladder (so nobody edges it twice). */
function ladderOne(greg: string): CutsceneStep[] {
  return [
    g('There. You\'re a climber. Don\'t tell Hollis I said so.'),
    g('Now. So nobody ever has to do that again...'),
    { op: 'move', actor: greg, to: { tx: 17, ty: 36 }, speed: 2 },
    { op: 'cameraFocus', to: { tx: 9, ty: 40 }, ms: 700 }, // the ladder's whole drop, clear of the text box
    { op: 'move', actor: greg, to: { tx: 9, ty: 36 }, speed: 2 },
    { op: 'move', actor: greg, to: { tx: 9, ty: 38 }, speed: 2 },
    { op: 'face', actor: greg, facing: 'left' },
    n('Greg knocks two iron pegs into the lip of the shelf and kicks a rope ladder over the edge. It unrolls all the way down to the Landing.', { unless_flag: 'flag:hart_rope_1' }),
    n('Greg kneels at the old rope ladder, tries both pegs, and gives it a kick. It holds.', { if_flag: 'flag:hart_rope_1' }),
    { op: 'sfx', key: 'world-chest' },
    { op: 'setFlag', flag: 'flag:hart_ladder_1' },
    g('A ladder! I never used to bother. I used to think ladders were cheating.'),
    { op: 'move', actor: greg, to: { tx: 9, ty: 36 }, speed: 2 },
    { op: 'move', actor: greg, to: { tx: 6, ty: 36 }, speed: 2 },
    { op: 'move', actor: greg, to: { tx: 6, ty: 34 }, speed: 2 },
    { op: 'face', actor: greg, facing: 'left' },
    { op: 'cameraReset', ms: 600 },
    n('He waves from the far end of the shelf, by [[the iron ladder]].'),
  ];
}

export const HARTWAY_SCRIPTS: ScriptRegistry = {
  // ---- Hartway Foot: the rope-warden and the gate ----------------------------------------
  ...chain(
    'script.hartway_hollis',
    [
      [MIST, [h('You sat on the Seat, then. And the harts came up? Eleven winters I\'ve kept these ropes dry for that.')]],
      [ROPED, [h('Two on a rope. Mind him on the ridges. He\'ll say it\'s fine. "Fine" is his favourite word.')]],
      [FOUND, [h('Well, I never. He\'s just along the shelf, pretending he isn\'t nervous. Go and [[rope up]].')]],
      // a save that was already past the pass: the ladders are theirs, and the quest still opens
      [
        'flag:pass_open',
        [
          h('You were over this pass before my ladders were news. They\'re yours. But the ridges are the real Hartway, and [[nobody edges one alone]].'),
          h('If you want it, fetch [[Greg]]. He\'s in [[Galehigh, top of the town]], staring up here like the hill owes him money.'),
          { op: 'setFlag', flag: HOOK },
        ],
      ],
      [HOOK, [h('No Greg, no ridges. He\'s in [[Galehigh, top of the town]], looking up at the Stair. Tell him Hollis says it\'s time.')]],
    ],
    HOLLIS_HOOK,
  ),
  // the foot of the Staircase, alone: the crest can't be walked, and the warden says so
  // (or Greg's waiting to tie you in, and leads you straight onto it)
  ...chain(
    'script.hartway_gate',
    [
      // gate-keepers come to YOU: he ties you in right here and leads off (the same-tile
      // travel re-enters the map mid-scene, so the roped Greg is there to be directed)
      [
        FOUND,
        [
          n('Greg comes along the shelf with a rope already in his hands.'),
          { op: 'run', ref: 'script.greg_rope_up' },
          { op: 'travel', map: 'hartway_climb', to: { tx: 21, ty: 46 }, facing: 'right' },
          { op: 'run', ref: 'script.hart_staircase' },
        ],
      ],
      [HOOK, [n('The rib of rock ahead is narrower than your boot.'), h('Not alone! [[Fetch Greg]] first. Galehigh, top of the town.')]],
      [
        'flag:pass_open',
        [
          n('The rib of rock ahead is narrower than your boot. A voice calls along the shelf.'),
          h('Not alone! That\'s the Staircase, and it takes two on a rope. Fetch [[Greg]] from [[Galehigh, top of the town]].'),
          { op: 'setFlag', flag: HOOK },
        ],
      ],
    ],
    [n('The rib of rock ahead is narrower than your boot, with the night on both sides. A voice calls along the shelf.'), ...HOLLIS_HOOK],
  ),
  // Andrew's Storm -> Frost wayfinding line, staged on the pass (exactly one plays)
  ...chain(
    'script.andrew_hint_frost',
    [
      ['flag:pass_open', [{ op: 'say', speaker: 'ANDREW', text: 'Ysolde Frost keeps the Frost at [[the Pale Vault Glacier]], [[over the Windward Stair and the Hartway]]. Wrap up.' }]],
      [ROPED, [{ op: 'say', speaker: 'ANDREW', text: 'Roped to that climber? Then it\'s [[the Hartway, east round the Shoulder from the Stair\'s high crags]]. He leads on the ridges. Mind them.' }]],
      [FOUND, [{ op: 'say', speaker: 'ANDREW', text: 'He said yes? He\'ll be [[on the Hartway\'s Landing, east round the Shoulder from the high crags]], by the rope-warden. Go and rope up.' }]],
      [HOOK, [{ op: 'say', speaker: 'ANDREW', text: 'Pale Vault\'s over the Hartway now, and nobody climbs it alone. The climber you want is [[at the top of Galehigh]]: red jacket, staring at the hill. Promise to tell him no.' }]],
    ],
    [{ op: 'say', speaker: 'ANDREW', text: 'Ysolde Frost keeps the Frost at [[the Pale Vault Glacier]], [[up the Windward Stair and over the Hartway]]. The Kite clears the crags. Wrap up.' }],
  ),
  'script.hartway_camp': rest('A walkers\' camp against the cliff, the fire still lit. Somebody keeps it going. You never see who.'),

  // ---- Paul at his lamp: "Greg?" (content/scripts.ts booji_paul_lamp options) ------------
  ...chain(
    'script.hartway_paul_router',
    [
      [FOUND, [{ op: 'run', ref: 'script.hartway_paul_climbing' }]],
      [TOKEN, [{ op: 'run', ref: 'script.hartway_paul_greg_again' }]],
    ],
    [{ op: 'run', ref: 'script.hartway_paul_greg' }],
  ),
  'script.hartway_paul_greg': [
    p('Greg! You\'ve met Greg? Up in the kite town? Is he STILL not climbing? Daft old goat.'),
    p('We did the high country together for years. Greg had the nerve. He\'d look at a cliff and see a staircase.'),
    p('I was the one who said "No, Greg." That was the whole job. Nerve at the front of the rope, sense at the back.'),
    p('Then my knees took a vote, and I stopped. And he wouldn\'t go up with anybody else. Nobody to tell him no, he said.'),
    n('He digs in his coat and comes out with a short end of old climbing rope, tied in one fat knot.'),
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'paul_rope_end', count: 1 },
    { op: 'say', text: 'Got PAUL\'S ROPE-END!' },
    p('Give him that. He\'ll know the knot. Tell him the one holding it [[has got the sense now]].'),
    { op: 'setFlag', flag: TOKEN },
  ],
  'script.hartway_paul_greg_again': [
    p('He\'s in [[Galehigh, top of the town]], you said. Show him the knot. Then stand well back.'),
  ],
  'script.hartway_paul_climbing': [
    p('He said yes? To YOU? Ha! Then go on. And when he says "it\'s fine", that\'s your cue.'),
  ],
  // the ending: you tell Paul
  'script.hartway_paul_told': [
    p('You went up. With GREG. And you\'re both in one piece. Sit down. Tell me everything.'),
    n('You tell him: the Staircase, the rope ladders, the snow ridge, and Greg\'s legs.'),
    p('His legs went? On the WHITEBACK? Ha! They went on me first, years back. A ridge just like it, out past the maple country.'),
    p('"Snow like a table," he says. "Good purchase." Halfway over he goes quiet and his knees start knocking.'),
    p('And I think: oh. This is a great deal worse than he said. Nothing to do but the next step.'),
    p('We got to the end, sat down in the snow, and laughed till it hurt. Then walked up to the safe trail like nothing had happened.'),
    n('Then you tell him about the mist. And what came up the mountain inside it.'),
    { op: 'wait', ms: 900 },
    n('Paul doesn\'t say anything for a while.'),
    p('...The harts. They still come up in the mist.'),
    p('We saw that once, him and me. Shadows all round us, tall as doors, going up under cover. Never told a soul. Who\'d believe it?'),
    p('And Greg says you told him no. Three times. THREE. It took me years to get to three.', { if_flag: 'flag:hart_sense_all' }),
    n('You hold out the stone from the Seat. He takes it, turns it over, and sets it on the foot of the dark lamp.'),
    { op: 'takeItem', item: 'seat_stone', count: 1 },
    p('First one I\'ve ever let come down. There. Now I don\'t have to carry it back up.'),
    p('Here. For whoever took my end of the rope. I always meant them for the top.'),
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'lumen_drop', count: 3 },
    { op: 'say', text: 'Got 3 LUMEN DROPS!' },
    p('And tell that daft old goat the bench has room for two. It always did.'),
    { op: 'setFlag', flag: DONE },
  ],
  'script.hartway_paul_after': [
    p('The hill\'s still there, then. Good. I like knowing somebody\'s sat on that bench.'),
  ],

  // ---- Greg, at the top of Galehigh, looking up at the Stair ------------------------------
  // Three stages (latest first): asked to come (HOOK) -> the promise; met; first meeting.
  // Paul's rope-end, if you happen to carry it, gets its own beat inside the promise.
  ...chain(
    'script.greg_town',
    [
      [
        HOOK,
        [
          g('Hollis sent you. Course she did. The low road\'s gone and she needs her ridges walked.'),
          g('I don\'t climb any more. I only ever had the nerve. My partner had the sense, and he packed it in.'),
          { op: 'run', ref: 'script.greg_knot', if_flag: TOKEN, unless_flag: 'flag:greg_knot_seen' },
          g('Unless. Tell me this. I say: "that snow bridge\'ll hold, I\'ll just nip across." What do YOU say?'),
          {
            op: 'choice',
            prompt: 'What do you say?',
            options: [
              { label: 'NO, GREG.', ops: [{ op: 'run', ref: 'script.greg_yes' }] },
              {
                label: 'After you?',
                ops: [g('...And that\'s how you get two people in a hole. Have a think. I\'ll be here. I\'m always here.')],
              },
            ],
          },
          { op: 'setFlag', flag: 'flag:greg_met' },
        ],
      ],
      ['flag:greg_met', [g('Still looking. It\'s still there. That\'s the trouble with hills.')]],
    ],
    [
      n('A stocky man in a red jacket stands at the top of the town with his hands in his pockets, looking up at the Stair.'),
      g('Evening. Don\'t mind me. Just looking at the hill.'),
      g('The Hartshoulder, top of the Stair. I\'ve been over it more times than I\'ve had hot dinners. Not for years, mind.'),
      g('My rope partner packed it in. Walks on the flat now, down south somewhere. And I don\'t climb without someone to tell me no.'),
      g('So. I look.'),
      { op: 'setFlag', flag: 'flag:greg_met' },
    ],
  ),
  'script.greg_yes': [
    { op: 'emote', actor: 'greg_town', emote: 'alert', holdMs: 700 },
    g('...Say that again. No, don\'t. I heard it. Haven\'t heard it in years.'),
    { op: 'shakeActor', actor: 'greg_town', ms: 600 },
    g('Ha! All right. ALL right. Same deal I always had: I go first, and you say that when I need it. You\'ll know when.'),
    g('[[Meet me on the Landing, the foot of the Hartway]], by Hollis: east round the Shoulder from the high crags. I need to find my boots.'),
    { op: 'setFlag', flag: 'flag:greg_met' },
    { op: 'setFlag', flag: FOUND },
    { op: 'hideActor', actor: 'greg_town' },
  ],
  // only if you carry Paul's rope-end (a player who knows the walking man)
  'script.greg_knot': [
    n('You hold out the knotted rope-end.'),
    { op: 'emote', actor: 'greg_town', emote: 'alert', holdMs: 800 },
    g('...Where did you get that.'),
    g('That\'s Paul\'s knot. He tied it wrong for thirty years and it never once slipped.'),
    n('You tell him what Paul said: the one holding it has got the sense now.'),
    g('Did he. DID he. Cheeky old sod.'),
    { op: 'takeItem', item: 'paul_rope_end', count: 1 },
    g('Well. If HE vouches for you. Still. I\'ll hear it from you.'),
    { op: 'setFlag', flag: 'flag:greg_knot_seen' },
  ],
  'script.greg_rope_up': [
    g('Found the boots. One had a mouse in it. We\'ve come to an arrangement.'),
    n('Greg ties you in: a bowline, checked twice. Then checked again by Hollis, who doesn\'t trust either of you.'),
    g('Right. [[The east end of the shelf: the Staircase]]. You don\'t walk it, you edge it. I go first. That\'s the deal.'),
    { op: 'setFlag', flag: ROPED },
    { op: 'hideActor', actor: 'greg_foot' },
  ],
  'script.greg_wait': [g('Go on. I\'m watching your feet.')],

  // ---- the Landing: THE STAIRCASE -------------------------------------------------------------
  'script.greg_t0': [
    g('See the gap at the east end of the shelf? That\'s [[the Staircase]]. One boot wide. Walk up to it when you\'re ready, and I\'ll lead.'),
  ],
  'script.hart_staircase': [
    { op: 'letterbox', on: true },
    g('The Staircase. A rib of rock with the night on both sides of it. My old partner hated this bit.'),
    g('I go first. You watch where I put my feet, and you put yours there. Nowhere else.'),
    { op: 'move', actor: 'player', to: { tx: 20, ty: 46 } },
    { op: 'face', actor: 'player', facing: 'right' },
    { op: 'cameraFocus', to: { tx: 22, ty: 42 }, ms: 700 },
    { op: 'move', actor: 'greg_t0', to: { tx: 21, ty: 46 }, speed: 1.4 },
    // the crest is SOLID ground-for-nobody: only the `edge` op crosses it
    { op: 'edge', actor: 'greg_t0', path: [{ tx: 21, ty: 43 }, { tx: 23, ty: 43 }, { tx: 23, ty: 41 }, { tx: 25, ty: 41 }, { tx: 25, ty: 37 }], speed: 0.8, teeter: [2] },
    { op: 'move', actor: 'greg_t0', to: { tx: 26, ty: 36 }, speed: 1.4 },
    { op: 'face', actor: 'greg_t0', facing: 'down' },
    g('See? Nothing to it! Your turn! Arms out! Don\'t look down!'),
    { op: 'move', actor: 'player', to: { tx: 21, ty: 46 }, speed: 0.6 },
    { op: 'edge', actor: 'player', path: [{ tx: 21, ty: 43 }, { tx: 23, ty: 43 }, { tx: 23, ty: 41 }, { tx: 25, ty: 41 }, { tx: 25, ty: 37 }], speed: 0.42, teeter: [1, 3] },
    { op: 'face', actor: 'player', facing: 'right' },
    g('...You looked down.'),
    { op: 'setFlag', flag: 'flag:hart_p1_done' },
    ...ladderOne('greg_t0'),
    { op: 'letterbox', on: false },
  ],
  // a save from before the two scenes were one: the ladder beat on its own, at the rib's top
  'script.hart_ladder_one': ladderOne('greg_t1'),
  'script.greg_t1b': [
    g('[[Iron ladder]], just here. Camp\'s behind me if your kin want a sit-down first. Somebody always leaves the fire in.'),
  ],
  // the foot of the iron ladder: "No, Greg" #1
  'script.hart_chimney': [
    g('Hang on. See that crack in the face? I could be up that chimney in ten minutes. Save us the ladder.'),
    n('The ladder is right there. It would take about one minute.'),
    {
      op: 'choice',
      prompt: 'What do you say?',
      options: [
        {
          label: 'NO, GREG.',
          ops: [
            { op: 'setFlag', flag: 'flag:hart_sense_1' },
            g('...That is EXACTLY the face my partner used to make. Fine. Ladder.'),
          ],
        },
        {
          label: 'Go on, then.',
          ops: [
            n('Greg gets three body-lengths up the chimney. There is a pause. Then a lot of snow comes down, and Greg with it.'),
            { op: 'shake', ms: 450, intensity: 0.004 },
            { op: 'hop', actor: 'greg_t1b', times: 1 },
            g('Right. Ladder. Good talk.'),
          ],
        },
      ],
    },
    n('Greg goes up the iron ladder like a man half his age.'),
    { op: 'hideActor', actor: 'greg_t1b' },
    { op: 'setFlag', flag: 'flag:hart_b1_done' },
  ],

  // ---- the High Shelf: THE WHITEBACK (the story ridge) ------------------------------------------
  'script.greg_uw': [
    g('There she is. [[The Whiteback]]. Walk out to the edge of the shelf and have a look at her.'),
  ],
  'script.hart_whiteback': [
    { op: 'letterbox', on: true },
    g('The Whiteback. Now, the proper trail goes round the back of the mountain. Three hours. Safe as a sofa.'),
    g('Or: straight over the top of that. Half an hour. The snow\'s frozen hard as a table. Good purchase.'),
    n('It is a ridge of snow one boot wide, with nothing at all on either side of it.'),
    g('I wouldn\'t take you if it wasn\'t fine. My partner wouldn\'t have crossed it alone in a month of Sundays. With me, he did.'),
    {
      op: 'choice',
      prompt: 'What do you say?',
      options: [
        {
          label: 'ROPE IN SHORTER.',
          ops: [
            { op: 'setFlag', flag: 'flag:hart_sense_2' },
            g('We ARE roped. ...Oh. Shorter. Yes. All right. Shorter. Fusspot.'),
          ],
        },
        { label: 'After you.', ops: [g('That\'s the spirit.')] },
      ],
    },
    { op: 'move', actor: 'player', to: { tx: 7, ty: 21 } },
    { op: 'face', actor: 'player', facing: 'down' },
    { op: 'move', actor: 'greg_uw', to: { tx: 6, ty: 22 }, speed: 1 },
    { op: 'move', actor: 'greg_uw', to: { tx: 7, ty: 22 }, speed: 1 },
    { op: 'cameraFocus', to: { tx: 11, ty: 21 }, ms: 700 },
    { op: 'edge', actor: 'greg_uw', path: [{ tx: 12, ty: 22 }], speed: 0.9 },
    // ...and you are edged out after him, onto a line of snow no wider than your hand
    { op: 'move', actor: 'player', to: { tx: 7, ty: 22 }, speed: 0.6 },
    { op: 'edge', actor: 'player', path: [{ tx: 10, ty: 22 }], speed: 0.42, teeter: [0] },
    { op: 'musicFade', ms: 900 },
    {
      op: 'frames',
      frames: [STILL('ridge-1'), STILL('ridge-2'), STILL('ridge-3')],
      holdMs: 900,
      fadeMs: 800,
      captions: [
        [
          'Hard snow, squeaking under your boots. Greg strides out like a man crossing his own kitchen.',
          'GREG: See? Table! You could play cards on it!',
        ],
        [
          'Halfway. Greg stops talking. Then Greg stops walking.',
          'His legs have started to shake. Both of them. Quite a lot.',
          'GREG: ...Don\'t mind the legs. The legs do that. Give us a minute.',
          'You look left. Then right. It is a very long way down, both ways. Much further than it looked from the shelf.',
          'This is a lot more dangerous than either of you thought. You keep the rope tight and say the only useful thing there is.',
          '"One step. Then the next one."',
        ],
        [
          'The far end. Solid rock. You both sit down in the snow, all at once, like puppets with the strings cut.',
          'And then, for no reason at all, you start to laugh. Both of you. For a long time.',
          'GREG: Ha! HA! Oh, that was STUPID. That was so stupid. "Table!" I said TABLE!',
        ],
      ],
    },
    { op: 'setFlag', flag: 'flag:hart_p2_done' },
    { op: 'travel', map: 'hartway_climb', to: { tx: 22, ty: 20 }, facing: 'right' },
    g('Don\'t tell anyone. ...No. DO. If you ever meet a man who walks everywhere, tell HIM. He\'ll want to know I haven\'t changed.'),
    g('Same thing happened with him, you know. A ridge just like it. My legs went then, too. I said "table" then, too.'),
    g('Right. I\'m putting a ladder on this shelf before either of us has another idea.'),
    { op: 'cameraFocus', to: { tx: 24, ty: 29 }, ms: 700 }, // Greg AND the ladder's top rungs above the text box
    { op: 'move', actor: 'greg_ue', to: { tx: 25, ty: 21 }, speed: 2 },
    { op: 'move', actor: 'greg_ue', to: { tx: 25, ty: 26 }, speed: 2 },
    { op: 'face', actor: 'greg_ue', facing: 'down' },
    n('Two pegs, one kick. A second rope ladder unrolls down the face to the camp shelf.', { unless_flag: 'flag:hart_rope_2' }),
    n('Greg tries the pegs on the old rope ladder down to the camp shelf. They hold.', { if_flag: 'flag:hart_rope_2' }),
    { op: 'sfx', key: 'world-chest' },
    { op: 'setFlag', flag: 'flag:hart_ladder_2' },
    g('There. From now on the Whiteback\'s for looking at. [[The trail\'s safe from here: north, up to the Seat]]. After you, for once.'),
    { op: 'cameraReset', ms: 600 },
    { op: 'letterbox', on: false },
    { op: 'music', key: CLIMB_MUSIC },
  ],
  'script.greg_ue2': [
    g('Go on up. [[North along the trail]]. I\'m coiling this rope, and then I\'m right behind you.'),
  ],

  // ---- THE SEAT -----------------------------------------------------------------------------------
  'script.hart_cornice': [
    { op: 'setFlag', flag: 'flag:hart_b3_begun' },
    { op: 'travel', map: 'hartway_climb', to: { tx: 24, ty: 10 }, facing: 'left' },
    n('Greg comes puffing up the trail behind you, and stops dead.'),
    g('The Seat. Top of the Hartway. My partner and I must have sat on that bench a hundred times.'),
    g('See the bothy? Climbers built it. Nobody\'s been up in eleven winters, so the kin moved in. A nest in the roof. Something asleep in the hearth.'),
    g('Good. It\'s theirs. We only ever borrowed the place.'),
    g('Now, the BEST view is off the snow lip, out past the cairn. Sticks right out over the drop. I\'ll just nip out and—'),
    {
      op: 'choice',
      prompt: 'What do you say?',
      options: [
        {
          label: 'NOT THE LIP, GREG.',
          ops: [
            { op: 'setFlag', flag: 'flag:hart_sense_3' },
            g('It\'s perfectly—'),
            { op: 'shake', ms: 500, intensity: 0.004 },
            n('A piece of the snow lip the size of a cart quietly lets go, and falls away into the dark.'),
            g('...The bench. The bench has a lovely view.'),
          ],
        },
        {
          label: 'Is it safe?',
          ops: [
            g('Course it\'s safe.'),
            n('He takes two steps. The snow under the third one simply leaves.'),
            { op: 'shake', ms: 500, intensity: 0.004 },
            { op: 'hop', actor: 'greg_seat', times: 2 },
            n('Greg walks backwards, very slowly, until he is standing next to you again.'),
            g('...The bench. The bench has a lovely view.'),
          ],
        },
      ],
    },
    { op: 'move', actor: 'greg_seat', to: { tx: 15, ty: 10 }, speed: 1.5 },
    { op: 'face', actor: 'greg_seat', facing: 'down' },
    { op: 'move', actor: 'player', to: { tx: 16, ty: 10 } },
    { op: 'face', actor: 'player', facing: 'down' },
    g('Come and sit. You\'ve earned the bench.'),
    { op: 'setFlag', flag: 'flag:hart_b3_done' },
    { op: 'run', ref: 'script.hart_seat_first' },
  ],
  ...chain(
    'script.greg_bench',
    [
      [DONE, [g('Paul laughed? Good. And he kept the stone? Ha. Tell him there\'s room on the bench. I\'ll be here a while yet.')]],
      [MIST, [g('I\'m stopping up here a bit. [[Pale Vault\'s down the trail, north-east corner]]. Go on. I\'ll catch you up in a year or two.')]],
    ],
    [g('Sit down! [[The bench]]. Go on. It\'s the best seat in Vesperholm and nobody\'s used it in eleven winters.')],
  ),
  ...chain(
    'script.hart_seat',
    [
      [
        MIST,
        [
          {
            op: 'choice',
            prompt: 'Sit a while?',
            options: [
              {
                label: 'JUST THE VIEW',
                ops: [
                  {
                    op: 'frames',
                    frames: [STILL('mist-1')],
                    fadeMs: 800,
                    captions: [['The whole valley, all the way down to the sea. Every lamp somebody\'s kept lit.']],
                  },
                ],
              },
              { label: 'WAIT FOR THE MIST', ops: [{ op: 'run', ref: 'script.hart_mist_reel' }] },
              { label: 'NOT NOW', ops: [] },
            ],
          },
        ],
      ],
      ['flag:hart_b3_done', [{ op: 'run', ref: 'script.hart_seat_first' }]],
    ],
    [n('An old bench, silver with weather, facing out over the drop. There is a small brass plate on the top slat, worn quite smooth.')],
  ),
  'script.hart_seat_first': [
    { op: 'letterbox', on: true },
    n('You sit. Greg sits. The bench creaks at both of you.'),
    { op: 'run', ref: 'script.hart_mist_reel' },
    g('The Hartway. That\'s why it\'s called that. It was never our road. It\'s theirs. We borrowed it, same as the bothy.'),
    g('Eleven winters of dark, and they still know the way up.'),
    g('They\'ll have left a fawn or two in [[the high grass]] behind us, mind. They always did.'),
    g('Climbers\' custom: you take one stone down from the Seat. My partner never would. Said he\'d only have to carry it back up.'),
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'seat_stone', count: 1 },
    { op: 'say', text: 'Got a STONE FROM THE SEAT!' },
    g('Pale Vault\'s [[down the trail, west off the Seat]]. You can see its lamps from here. And the ladders are fixed behind us: nobody edges a ridge twice.'),
    { op: 'say', speaker: 'GREG', if_flag: TOKEN, text: 'And [[take that stone to Paul]], when you\'re next south. Tell him the hill\'s still here. Tell him about the legs, if you must.' },
    { op: 'run', ref: 'script.hart_sense_gift', if_flag: 'flag:hart_sense_all' },
    { op: 'setFlag', flag: MIST },
    { op: 'letterbox', on: false },
  ],
  'script.hart_sense_gift': [
    g('And you said no. Three times out of three. That\'s better than my partner managed in his first ten years.'),
    g('These were for the day I met someone with more sense than me. Low bar. Still. You cleared it.'),
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'Got 2 BEACON CHARGES!' },
  ],
  // THE HERD IN THE MIST — the scene the mountain was built for
  'script.hart_mist_reel': [
    { op: 'musicFade', ms: 900 },
    {
      op: 'frames',
      frames: [STILL('mist-1'), STILL('mist-2'), STILL('mist-3'), STILL('mist-4'), STILL('mist-5')],
      holdMs: 900,
      fadeMs: 1100,
      frameSfx: { 3: 'world-mist-herd' },
      captions: [
        [
          'The whole valley, all the way down to the sea.',
          'GREG: All the way south. That\'s Pearlmoor, with the Old Light. And that one beacon, off on its own? Tinderwick.',
          'From up here the towns are only lamps. Small ones. Somebody has kept every one of them lit.',
          'GREG: My partner used to say you can\'t see anybody\'s troubles from up here. Only that they\'ve left a light on.',
        ],
        [
          'GREG: ...Hello. See that? Mist, coming up out of the valleys. Watch the bottom of it.',
          'Something is moving inside the mist. Lights. Dozens of them, low and golden, all going the same way.',
        ],
        [
          'The mist climbs the mountain like a tide coming in. The lights climb with it.',
          'GREG (whispering): Sit still. Not a word. I saw this once, years back, with my partner. I\'ve been half sure I dreamed it.',
        ],
        [
          'Then the mist is all around you. And so are they.',
          'Sunstags. A whole herd, tall as doorways, passing on every side, the light of old summers caught in their antlers.',
          'They use the mist as cover to reach the high grass. Nothing hunts what it cannot see.',
          'One stops beside the bench. It looks at you for a long moment. Then it goes on up with the others.',
        ],
        [
          'The mist sinks back down the mountain. The stars come out again, one valley at a time.',
          'GREG: ...Well. I didn\'t dream it.',
        ],
      ],
    },
    { op: 'music', key: CLIMB_MUSIC },
  ],

  // ---- caches ------------------------------------------------------------------------------------
  'script.pickup_hartway_shelf': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'say', text: 'Tucked behind a rock at the end of the shelf: two GLOW CHARGES!' },
    { op: 'setFlag', flag: 'flag:picked_hartway_shelf' },
  ],
  'script.pickup_hartway_high': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'say', text: 'An oilcloth bundle in the snow, tied with rope. Inside, still warm: a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_hartway_high' },
  ],
  'script.pickup_hartway_seat': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'On the wall by the high grass, left like an offering: a LUMEN DROP!' },
    { op: 'setFlag', flag: 'flag:picked_hartway_seat' },
  ],
};

export const HARTWAY_DIALOGUE: DialogueRegistry = {
  'sign.hartway_steps': [
    { text: 'THE SHOULDER\n[[Down and east: the Hartway]], the climbers\' road over the Hartshoulder to Pale Vault. [[Nobody climbs alone]]: see the rope-warden.' },
    { text: 'Scratched underneath: "To the Seat: one day. To the Seat with Greg: quicker, and you\'ll wish it wasn\'t."' },
  ],
  'sign.hartway_top': [
    { text: 'THE HARTWAY\n[[East]]: the Seat, and the climbers\' road down to the Windward Stair. [[West]]: Pale Vault.' },
  ],
  'sign.hartway_foot': [
    { text: 'THE LANDING\nFoot of the Hartway. [[East: the Staircase.]] Nobody goes up alone.' },
  ],
  'sign.hartway_low_road': [
    { text: 'THE LOW ROAD\nUnder the drift, and staying there. [[The way is over the Hartway.]]' },
  ],
  'sign.hartway_staircase': [{ text: 'THE STAIRCASE\nOne at a time. Leader first.' }],
  'sign.hartway_whiteback': [
    { text: 'THE WHITEBACK\nThe trail goes ROUND. This sign is here so you can\'t say nobody told you.' },
  ],
  'sign.hartway_seat': [
    { text: 'THE SEAT\nTop of the Hartway. Sit. Look. Take one stone down.' },
    { text: 'Pale Vault: [[the trail west]].' },
  ],
  'sign.hartway_pegs': [
    { text: 'Old iron pegs, hammered into the lip of the rock. Whatever used to hang from them is long gone.' },
  ],
  'sign.hartway_hut': [
    { text: 'The climbers\' old bothy. Moss on the walls, a nest in the roof, and something small breathing slowly in the cold hearth.' },
    { text: 'You leave the door exactly as it is.' },
  ],
};
