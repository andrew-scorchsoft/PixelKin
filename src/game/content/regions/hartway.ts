/**
 * THE HARTWAY (2026-11) — the old climbers' road up the Hartshoulder, the mountain
 * behind Wayward Rise, walked with GREG. Paul content: post-Chickenpig by
 * construction (it hangs off the Rise) and SHIPS SILENTLY like the rest — never in
 * the changelog, the guide or the website. Spec: docs/world/walkthrough/12-the-hartway.md.
 * Builders: tools/maps/build_hartway_foot.py, build_hartway_climb.py; art
 * hartforge.py + hartway_set; stills assets/backgrounds/cinematic/hartway/.
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
 * In the game the PLAYER takes Paul's end of the rope. Greg hasn't climbed since Paul
 * stopped ("nobody to tell me no"). The herd is the SUNSTAGS (#121), the light of old
 * summers in their antlers: the Hartway is the harts' own way up.
 *
 * The loop (all flags):
 *   flag:q_hartway        the rule heard (Hollis) or Greg met: "find Greg" opens — JOURNAL
 *   flag:greg_met         you've talked to Greg in the far Wanderwood
 *   flag:greg_token       Paul gave you his ROPE-END (the knot Greg will know)
 *   flag:greg_found       Greg said yes -> he waits at Hartway Foot
 *   flag:greg_roped       tied in -> the steps open (the warp's requires_flag)
 *   flag:hart_p1_done     the Staircase is behind you
 *   flag:hart_ladder_1    Greg's rope ladder down band A (a flag-gated span + object)
 *   flag:hart_b1_done     the chimney beat (flag:hart_sense_1 if you said "No, Greg")
 *   flag:hart_p2_done     the Whiteback is behind you (flag:hart_sense_2: roped short)
 *   flag:hart_ladder_2    the second rope ladder (band B, east)
 *   flag:hart_b3_begun/_done  the cornice beat at the Seat (flag:hart_sense_3)
 *   flag:hart_sense_all   DERIVED (FlagStore COUNT_AT_LEAST flag:hart_sense_ x3)
 *   flag:hart_mist_seen   you sat on the Seat and the herd came up in the mist
 *   flag:q_hartway_done   you told Paul
 *
 * Never progression; a lost choice costs nothing (Greg is embarrassed, never hurt).
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
  h('Hollis. I keep the ropes at the foot of the Hartshoulder. That road up the crag is the Hartway: the old climbers\' road.'),
  h('One rule, older than me: [[nobody goes up alone]]. Two on a rope. One with the nerve, one with the sense.'),
  h('And the ridges want someone who knows them. There\'s one left who does: [[Greg]]. He\'s not been up since his partner hung up his boots.'),
  h('Find him and the steps are yours. His old partner will know where he\'s got to: [[the walking man, at the dark lamp on Pearlmoor\'s breakwater]].'),
  { op: 'setFlag', flag: HOOK },
];

export const HARTWAY_SCRIPTS: ScriptRegistry = {
  // ---- Hartway Foot: the rope-warden and the gate ----------------------------------------
  ...chain(
    'script.hartway_hollis',
    [
      [DONE, [h('You sat on the Seat, then. And the harts came up? Eleven winters I\'ve kept these ropes dry for that.')]],
      [MIST, [h('You\'ve a look on you. You saw something up there. Don\'t tell me. [[Tell the walking man]]. It\'s his hill too.')]],
      [ROPED, [h('Two on a rope. Mind him on the ridges. He\'ll say it\'s fine. "Fine" is his favourite word.')]],
      [FOUND, [h('Well, I never. He\'s over by the steps, pretending he isn\'t nervous. Go and [[rope up]].')]],
      [TOKEN, [h('Is that Paul\'s knot? Then you\'ve all you need but the man himself. [[Find Greg]] and show him that.')]],
      [HOOK, [h('No Greg, no steps. Ask [[the walking man on Pearlmoor\'s breakwater]] where his old rope partner\'s hiding.')]],
    ],
    HOLLIS_HOOK,
  ),
  // the steps' blocked_ref: the warden calls over (or Greg's waiting to tie you in)
  ...chain(
    'script.hartway_gate',
    [
      [FOUND, [n('Greg is waiting by the steps with a rope in his hands. Best not go up without it.')]],
      [HOOK, [h('Not alone! [[Find Greg]] first. The walking man on the breakwater will know where he is.')]],
    ],
    [n('You\'ve one foot on the steps when a voice calls across the grass.'), ...HOLLIS_HOOK],
  ),
  'script.hartway_foot_rest': rest('Hollis\'s fire, banked low under the awning. Bedrolls, a kettle, rope drying on a line.'),
  'script.hartway_camp': rest('A walkers\' camp against the cliff, the fire still lit. Somebody keeps it going. You never see who.'),

  // ---- Paul at his lamp: "Greg?" (content/scripts.ts booji_paul_lamp options) ------------
  'script.hartway_paul_greg': [
    p('Greg! Hollis sent you, did she? Is he STILL not climbing? Daft old goat.'),
    p('We did the high country together for years. Greg had the nerve. He\'d look at a cliff and see a staircase.'),
    p('I was the one who said "No, Greg." That was the whole job. Nerve at the front of the rope, sense at the back.'),
    p('Then my knees took a vote, and I stopped. And he wouldn\'t go up with anybody else. Nobody to tell him no, he said.'),
    n('He digs in his coat and comes out with a short end of old climbing rope, tied in one fat knot.'),
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'paul_rope_end', count: 1 },
    { op: 'say', text: 'Got PAUL\'S ROPE-END!' },
    p('Give him that. He\'ll know the knot. Tell him the one holding it [[has got the sense now]].'),
    p('He\'ll be somewhere he can see the hill and not climb it. Start at [[the Wayward Arms]]. He never could walk past a slate.'),
    { op: 'setFlag', flag: TOKEN },
  ],
  'script.hartway_paul_greg_again': [
    p('Not found him? [[The Wayward Arms]] first, then wherever his slate says he\'s gone. Show him the knot.'),
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

  // ---- the trail: the slate at the Wayward Arms -------------------------------------------
  'script.hartway_arms_slate': [
    n('A slate of tabs, propped on the long table. One name has more chalk marks than all the others put together: GREG.'),
    n('Under his tally, in a cheerful hand: "Gone to look at the hill from [[the far side of the wood]]. Back when I\'ve stopped looking. Put it on the slate. G."', { if_flag: HOOK }),
  ],

  // ---- Greg, on his stump in the far Wanderwood --------------------------------------------
  ...chain(
    'script.greg_wood',
    [
      [
        TOKEN,
        [
          n('You hold out the knotted rope-end.'),
          { op: 'emote', actor: 'greg_wood', emote: 'alert', holdMs: 800 },
          g('...Where did you get that.'),
          g('That\'s Paul\'s knot. He tied it wrong for thirty years and it never once slipped.'),
          n('You tell him what Paul said: the one holding it has got the sense now.'),
          g('Did he. DID he.'),
          { op: 'shakeActor', actor: 'greg_wood', ms: 700 },
          g('Ha! Cheeky old sod. All right. ALL right.'),
          { op: 'takeItem', item: 'paul_rope_end', count: 1 },
          g('Same deal as ever: I go first, and you say "No, Greg" when I need it. You\'ll know when. Paul always did.'),
          g('[[Meet me at Hartway Foot]], west off Wayward Rise. I need to find my boots.'),
          { op: 'setFlag', flag: 'flag:greg_met' },
          { op: 'setFlag', flag: HOOK },
          { op: 'setFlag', flag: FOUND },
          { op: 'hideActor', actor: 'greg_wood' },
        ],
      ],
      [
        'flag:greg_met',
        [
          g('Still looking. It\'s still there. That\'s the trouble with hills.'),
          g('Hollis sent you? Kind of her. No. Not without someone to tell me no.', { if_flag: HOOK }),
        ],
      ],
    ],
    [
      n('A stocky man in a red jacket sits on a stump, looking up through a gap in the trees. Up there, a very long way up, is a mountain.'),
      g('Evening. Don\'t mind me. Just looking at the hill.'),
      g('The Hartshoulder. I\'ve been up it more times than I\'ve had hot dinners. Not for years, mind.'),
      g('My rope partner packed it in. Walks now, on the flat. Keeps a dark lamp on [[Pearlmoor\'s breakwater]], last I heard.'),
      g('And I don\'t climb without someone to tell me no. So. I look.'),
      { op: 'setFlag', flag: 'flag:greg_met' },
      { op: 'setFlag', flag: HOOK },
    ],
  ),
  'script.greg_rope_up': [
    g('Found the boots. One had a mouse in it. We\'ve come to an arrangement.'),
    n('Greg ties you in: a bowline, checked twice. Then checked again by Hollis, who doesn\'t trust either of you.'),
    g('Right. [[Up the steps]]. I\'ll be at the top of them before you are. I go first. That\'s the deal.'),
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
    g('The Staircase. A rib of rock with the night on both sides of it. Paul hated this bit.'),
    g('I go first. You watch where I put my feet, and you put yours there. Nowhere else.'),
    { op: 'move', actor: 'player', to: { tx: 19, ty: 46 } },
    { op: 'face', actor: 'player', facing: 'right' },
    { op: 'cameraFocus', to: { tx: 22, ty: 42 }, ms: 700 },
    { op: 'move', actor: 'greg_t0', to: { tx: 20, ty: 46 }, speed: 1.4 },
    { op: 'move', actor: 'greg_t0', to: { tx: 20, ty: 43 }, speed: 1.4 },
    { op: 'move', actor: 'greg_t0', to: { tx: 23, ty: 43 }, speed: 1.4 },
    { op: 'move', actor: 'greg_t0', to: { tx: 23, ty: 41 }, speed: 1.4 },
    { op: 'hop', actor: 'greg_t0', times: 1 },
    { op: 'move', actor: 'greg_t0', to: { tx: 25, ty: 41 }, speed: 1.4 },
    { op: 'move', actor: 'greg_t0', to: { tx: 25, ty: 37 }, speed: 1.4 },
    { op: 'move', actor: 'greg_t0', to: { tx: 26, ty: 36 }, speed: 1.4 },
    { op: 'face', actor: 'greg_t0', facing: 'down' },
    g('See? Nothing to it! Your turn! Don\'t look down!'),
    g('...You looked down.'),
    { op: 'cameraReset', ms: 600 },
    { op: 'letterbox', on: false },
    { op: 'setFlag', flag: 'flag:hart_p1_done' },
  ],
  // the top of the Staircase: the first rope ladder
  'script.hart_ladder_one': [
    g('There. You\'re a climber. Don\'t tell Hollis I said so.'),
    g('Now. So nobody ever has to do that again...'),
    { op: 'move', actor: 'greg_t1', to: { tx: 17, ty: 36 }, speed: 2 },
    { op: 'cameraFocus', to: { tx: 12, ty: 37 }, ms: 700 },
    { op: 'move', actor: 'greg_t1', to: { tx: 9, ty: 36 }, speed: 2 },
    { op: 'move', actor: 'greg_t1', to: { tx: 9, ty: 38 }, speed: 2 },
    { op: 'face', actor: 'greg_t1', facing: 'left' },
    n('Greg knocks two iron pegs into the lip of the shelf and kicks a rope ladder over the edge. It unrolls all the way down to the Landing.'),
    { op: 'sfx', key: 'world-chest' },
    { op: 'setFlag', flag: 'flag:hart_ladder_1' },
    g('A ladder! I never used to bother. I used to think ladders were cheating.'),
    { op: 'move', actor: 'greg_t1', to: { tx: 9, ty: 36 }, speed: 2 },
    { op: 'move', actor: 'greg_t1', to: { tx: 6, ty: 36 }, speed: 2 },
    { op: 'move', actor: 'greg_t1', to: { tx: 6, ty: 34 }, speed: 2 },
    { op: 'face', actor: 'greg_t1', facing: 'left' },
    { op: 'cameraReset', ms: 600 },
    n('He waves from the far end of the shelf, by [[the iron ladder]].'),
  ],
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
            g('...That is EXACTLY the face Paul used to make. Fine. Ladder.'),
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
    g('I wouldn\'t take you if it wasn\'t fine. Paul wouldn\'t have crossed it alone in a month of Sundays. With me, he did.'),
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
    { op: 'move', actor: 'greg_uw', to: { tx: 11, ty: 22 }, speed: 1 },
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
    g('Don\'t tell Paul. ...No. DO tell Paul. He\'ll want to know I haven\'t changed.'),
    g('Same thing happened with him, you know. A ridge just like it. My legs went then, too. I said "table" then, too.'),
    g('Right. I\'m putting a ladder on this shelf before either of us has another idea.'),
    { op: 'move', actor: 'greg_ue', to: { tx: 25, ty: 21 }, speed: 2 },
    { op: 'move', actor: 'greg_ue', to: { tx: 25, ty: 26 }, speed: 2 },
    { op: 'face', actor: 'greg_ue', facing: 'down' },
    n('Two pegs, one kick. A second rope ladder unrolls down the face to the camp shelf.'),
    { op: 'sfx', key: 'world-chest' },
    { op: 'setFlag', flag: 'flag:hart_ladder_2' },
    g('There. From now on the Whiteback\'s for looking at. [[The trail\'s safe from here: north, up to the Seat]]. After you, for once.'),
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
    g('The Seat. Top of the Hartway. Paul and I must have sat on that bench a hundred times.'),
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
    g('[[Come and sit]]. You\'ve earned the bench.'),
    { op: 'setFlag', flag: 'flag:hart_b3_done' },
  ],
  ...chain(
    'script.greg_bench',
    [
      [DONE, [g('Paul laughed? Good. And he kept the stone? Ha. Tell him there\'s room on the bench. I\'ll be here a while yet.')]],
      [MIST, [g('I\'m stopping up here a bit. You go on down and [[tell Paul]]. He\'s at his lamp. He\'s always at his lamp.')]],
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
      [
        'flag:hart_b3_done',
        [
          { op: 'letterbox', on: true },
          n('You sit. Greg sits. The bench creaks at both of you.'),
          { op: 'run', ref: 'script.hart_mist_reel' },
          g('The Hartway. That\'s why it\'s called that. It was never our road. It\'s theirs. We borrowed it, same as the bothy.'),
          g('Eleven winters of dark, and they still know the way up.'),
          g('They\'ll have left a fawn or two in [[the high grass]] behind us, mind. They always did.'),
          g('Climbers\' custom: you take one stone down from the Seat. Paul never would. Said he\'d only have to carry it back up.'),
          { op: 'sfx', key: 'world-keyitem' },
          { op: 'giveItem', item: 'seat_stone', count: 1 },
          { op: 'say', text: 'Got a STONE FROM THE SEAT!' },
          g('[[Take that down to Paul]]. Tell him the hill\'s still here. Tell him about the legs, if you must.'),
          { op: 'run', ref: 'script.hart_sense_gift', if_flag: 'flag:hart_sense_all' },
          { op: 'setFlag', flag: MIST },
          { op: 'letterbox', on: false },
        ],
      ],
    ],
    [n('An old bench, silver with weather, facing out over the drop. There is a small brass plate on the top slat, worn quite smooth.')],
  ),
  'script.hart_sense_gift': [
    g('And you said no. Three times out of three. That\'s better than Paul managed in his first ten years.'),
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
          'GREG: That\'s Pearlmoor, with the Old Light. And that one beacon, off on its own? Tinderwick.',
          'From up here the towns are only lamps. Small ones. Somebody has kept every one of them lit.',
          'GREG: Paul used to say you can\'t see anybody\'s troubles from up here. Only that they\'ve left a light on.',
        ],
        [
          'GREG: ...Hello. See that? Mist, coming in off the fen. Watch the bottom of it.',
          'Something is moving inside the mist. Lights. Dozens of them, low and golden, all going the same way.',
        ],
        [
          'The mist climbs the mountain like a tide coming in. The lights climb with it.',
          'GREG (whispering): Sit still. Not a word. Paul and I saw this once. I\'ve spent years half sure I dreamed it.',
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
  'script.pickup_hartway_foot': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'A climber\'s tin, wedged under the crag. Two WARM BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_hartway_foot' },
  ],
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
  'sign.wayward_hartway': [{ text: 'WEST: [[the Hartway]], and the foot of the Hartshoulder.' }],
  'sign.hartway_foot': [
    { text: 'HARTWAY FOOT\nNORTH: the steps up to [[the Hartway]]. EAST: Wayward Rise.' },
  ],
  'sign.hartway_steps': [
    { text: 'THE HARTWAY\nThe old climbers\' road up the Hartshoulder. [[Nobody climbs alone]]: see the rope-warden.' },
    { text: 'Scratched underneath: "To the Seat: one day. To the Seat with Greg: quicker, and you\'ll wish it wasn\'t."' },
  ],
  'sign.hartway_bothy': [
    { text: 'The rope-warden\'s bothy. Coils of rope on every peg, each one tagged with a name and a year. The newest tag is eleven winters old.' },
  ],
  'sign.hartway_staircase': [{ text: 'THE STAIRCASE\nOne at a time. Leader first.' }],
  'sign.hartway_whiteback': [
    { text: 'THE WHITEBACK\nThe trail goes ROUND. This sign is here so you can\'t say nobody told you.' },
  ],
  'sign.hartway_seat': [{ text: 'THE SEAT\nTop of the Hartway. Sit. Look. Take one stone down.' }],
  'sign.hartway_hut': [
    { text: 'The climbers\' old bothy. Moss on the walls, a nest in the roof, and something small breathing slowly in the cold hearth.' },
    { text: 'You leave the door exactly as it is.' },
  ],
};
