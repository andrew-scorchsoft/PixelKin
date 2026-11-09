/**
 * STILLWATER — the Hollowing's village (docs/world/walkthrough/11-the-hollowing-country.md,
 * Part A) + the late-north density pass (Part E: Coldfog Marches I/II, the Nightreach lane,
 * Sunvault Climb II-IV). Lane N1 OWNS this file: new scripts + dialogue only, spread into
 * the registries via regions/index.ts (a ref here must be NEW, never an override).
 *
 * The register (binding): the Hollowing are tired, grieving, kind people who believe the
 * dark is mercy. Never cartoonish, never cruel, never lethal. Kin are ASLEEP, never harmed.
 * You are tolerated here, not attacked: "you're the one relighting the sky." Some of them
 * are beginning to doubt. Còr's past stays dosed (a lamp he once said goodbye to, no more),
 * and the Star-tender's old ladder-mate is never named here.
 *
 * Flags this file sets:
 *   flag:q_still_candle             "A Light Left On": the child hands you her candle-jar
 *   flag:q_still_candle_hidden      ... you hid it in the willow's hollow
 *   flag:q_still_candle_shown       ... you showed it to her mother, Maren
 *   flag:q_still_candle_done        ... the child thanks you (either ending)
 *   flag:q_still_tessaly            "The Way Home": you agree to walk Tessaly home
 *   flag:q_still_tessaly_fog1/_fog2 ... the escort stops in Coldfog I / Coldfog II
 *   flag:q_still_tessaly_done       ... she's home at Pale Vault (her old lamp)
 *   flag:q_still_wall               "The Shutter-wall": the hall-keeper asks you to find
 *                                   three of the cold lamps whose names are on the wall
 *   flag:q_still_lamp_1..3          ... a cold lamp found (Coldfog I, Coldfog II, the far shore)
 *   flag:q_still_wall_done          ... all three told back to the hall-keeper
 *   flag:<trainer>_beaten           the seven Hollowing trainers (Stillwater + Coldfog)
 *   flag:picked_<cache>             the caches (incl. the two Lamplight-starlight nooks)
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

const DAWN = 'flag:dawn';
const CANDLE = 'flag:q_still_candle';
const HIDDEN = 'flag:q_still_candle_hidden';
const SHOWN = 'flag:q_still_candle_shown';
const CANDLE_DONE = 'flag:q_still_candle_done';
const TESS = 'flag:q_still_tessaly';
const TESS1 = 'flag:q_still_tessaly_fog1';
const TESS2 = 'flag:q_still_tessaly_fog2';
const TESS_DONE = 'flag:q_still_tessaly_done';
const WALL = 'flag:q_still_wall';
const WALL_DONE = 'flag:q_still_wall_done';
const lamp = (n: number) => `flag:q_still_lamp_${n}`;

const pickup = (flag: string, give: CutsceneStep[], text: string): CutsceneStep[] => [
  { op: 'sfx', key: 'world-pickup' },
  ...give,
  { op: 'say', text },
  { op: 'setFlag', flag },
];

/** A Hollowing trainer who'd rather talk first: their words, THEN the offer. */
const talkFirst = (id: string, speaker: string, lines: string[], ask: string, after: string,
  decline: string): CutsceneStep[] => [
  ...lines.map((text): CutsceneStep => ({ op: 'say', speaker, text })),
  {
    op: 'choice',
    speaker,
    prompt: ask,
    options: [
      {
        label: 'BATTLE',
        ops: [
          { op: 'battle', trainer: id },
          { op: 'say', speaker, text: after },
          { op: 'setFlag', flag: `flag:${id}_beaten` },
        ],
      },
      { label: 'JUST TALK', ops: [{ op: 'say', speaker, text: decline }] },
    ],
  },
];

/** The cold lamps' read-backs, filled by coldLamp() while STILLWATER_SCRIPTS is
 *  built (declared first: it's written to during that build). */
const READS: ScriptRegistry = {};

/** A cold lamp from the shutter-wall: unreadable until you know whose it is. The
 *  progression step (the found flag) lives unguarded in its own read script. */
const coldLamp = (n: number, plate: string, note: string[]): CutsceneStep[] => {
  const read = `script.still_coldlamp_${n}_read`;
  READS[read] = [
    { op: 'say', text: `A brass plate at its foot, rubbed clean by a thumb: ${plate}` },
    ...note.map((text): CutsceneStep => ({ op: 'narrate', text })),
    { op: 'say', unless_flag: lamp(n), text: 'One of the names from the shutter-wall. [[Tell the hall-keeper]] you found it.' },
    { op: 'setFlag', flag: lamp(n) },
  ];
  return [
    { op: 'say', unless_flag: WALL, text: 'A doused lamp. Its brass plate is too worn to read, unless you know the name.' },
    { op: 'run', ref: read, if_flag: WALL },
  ];
};

export const STILLWATER_SCRIPTS: ScriptRegistry = {
  // ===========================================================================
  //  STILLWATER — the village (people + the square)
  // ===========================================================================
  'script.still_greeter': [
    { op: 'say', speaker: 'ACOLYTE', unless_flag: DAWN, text: 'Oh. A lamp. ...No, keep it. We know who you are: the one relighting the sky.' },
    { op: 'say', speaker: 'ACOLYTE', unless_flag: DAWN, text: 'This is Stillwater. Nobody will stop you. Only speak softly; the kin sleep lightly.' },
    { op: 'say', speaker: 'ACOLYTE', if_flag: DAWN, text: 'You can talk at a normal volume now. I keep forgetting. We all do.' },
  ],
  'script.still_elder': [
    { op: 'say', speaker: 'ELDER ASHE', unless_flag: DAWN, text: 'Sit, if you like. Everyone here lost something to the cycle: a star, a season, a person. Out there the light keeps promising. In here, nothing promises anything.' },
    { op: 'say', speaker: 'ELDER ASHE', unless_flag: DAWN, text: 'You think we\'re wrong. Perhaps we are. But nobody here has cried at a sunrise in eleven winters. Can you say the same for yours?' },
    { op: 'say', speaker: 'ELDER ASHE', if_flag: DAWN, text: 'Morning. I swore I\'d never say that word again. I mind it less than I feared.' },
    { op: 'say', speaker: 'ELDER ASHE', if_flag: DAWN, text: 'The Warden came home for a night. He opened his own shutter, then asked at each door about ours. Some said not yet. He said that was all right.' },
  ],
  'script.still_blanket_folder': [
    { op: 'say', speaker: 'GRETE', text: 'Mornings I fold their blankets back; evenings, up to the chin. They don\'t notice.' },
    { op: 'say', speaker: 'GRETE', unless_flag: DAWN, text: 'Asleep isn\'t gone. Stand still and you can hear them breathing.' },
    { op: 'say', speaker: 'GRETE', if_flag: DAWN, text: 'Two of them woke wanting breakfast. I\'d forgotten how loud they are. I\'ve smiled all day.' },
  ],
  'script.still_sweeper': [
    { op: 'say', speaker: 'ODO', text: 'Swept twice a day, these flags. Nobody walks them much. But a swept lane says somebody still cares. That\'s the part people get wrong about us.' },
  ],
  'script.still_shore_watcher': [
    { op: 'say', speaker: 'LISBET', unless_flag: DAWN, text: 'The water went still when the dark came. Not a ripple since. Hence the name.' },
    { op: 'say', speaker: 'LISBET', unless_flag: DAWN, text: 'Some nights I think it\'s waiting. Most nights that seems silly, for water.' },
    { op: 'say', speaker: 'LISBET', if_flag: DAWN, text: 'It rippled this morning, once, under a moth. I\'ve waited an hour for it to do it again.' },
  ],
  'script.still_doubter': [
    { op: 'say', speaker: 'CORWEN', unless_flag: DAWN, text: 'Can I tell you something I haven\'t told the hall? I dream in colours. Orange, mostly: a lamp in a window when you\'re walking home.' },
    { op: 'say', speaker: 'CORWEN', unless_flag: DAWN, text: 'I came here to stop missing things. I don\'t miss them less. Just quietly.' },
    { op: 'say', speaker: 'CORWEN', if_flag: DAWN, text: 'I\'m going home. My sister wrote back three pages. The third just said YES, very large.' },
  ],
  'script.still_water_carrier': [
    { op: 'say', speaker: 'HALLAM', text: 'The well\'s the only water here that moves. A hearth turned to the wall still warms a house; it just doesn\'t make anyone look up.' },
  ],
  'script.still_meadow_keeper': [
    { op: 'say', speaker: 'NELL', unless_flag: DAWN, text: 'Mind the grey meadow. The kin there aren\'t asleep, just quiet. Moths keep the rest dreaming.' },
    { op: 'say', speaker: 'NELL', unless_flag: DAWN, text: 'Our first lamp stands cold on [[the far shore, under the crags]]. Nobody goes there now.' },
    { op: 'say', speaker: 'NELL', if_flag: DAWN, text: 'The meadow\'s full of wisps, glowing like they\'ve something to prove. Go and look.' },
  ],
  'script.still_shore_lamp': [
    { op: 'say', unless_flag: DAWN, text: 'A lamp boxed in grey shutters. Not broken. Not even out, perhaps. Put to sleep.' },
    { op: 'say', if_flag: DAWN, text: 'The shutters stand open. Someone has lit the wick, carefully, as if for the first time in years.' },
  ],
  'script.still_notice': [
    { op: 'say', text: '"STILLWATER WELCOMES THE WEARY. Speak softly. Leave lamps as you find them. Supper on the darkest night of the month. Every night is; come any time."' },
  ],
  'script.still_sleeper': [
    { op: 'say', unless_flag: DAWN, text: 'A kin asleep under a grey blanket, tucked carefully round its paws.' },
    { op: 'say', if_flag: DAWN, text: 'A kin dozing under a blanket. One eye opens, finds you, closes. Ordinary sleep.' },
  ],
  'script.still_willow_hollow': [
    { op: 'run', ref: 'script.still_willow_hide', if_flag: CANDLE, unless_flag: CANDLE_DONE },
    { op: 'say', unless_flag: CANDLE, text: 'An old willow with a dry hollow in its trunk, just big enough for a secret.' },
    { op: 'say', if_flag: HIDDEN, text: 'Deep in the willow\'s hollow, the candle burns, seen only from here.' },
    { op: 'say', if_flag: SHOWN, text: 'The willow\'s hollow is empty now. The candle lives in a window.' },
  ],
  'script.still_willow_hide': [
    { op: 'run', ref: 'script.still_willow_offer', unless_flag: HIDDEN, if_flag: CANDLE },
  ],
  'script.still_willow_offer': [
    { op: 'say', unless_flag: SHOWN, text: 'The hollow is dry and deep, facing the crags. No one in the village would see a light here.' },
    {
      op: 'choice',
      unless_flag: SHOWN,
      prompt: 'Hide Linnet\'s candle in the hollow?',
      options: [
        {
          label: 'HIDE IT HERE',
          ops: [
            { op: 'takeItem', item: 'still_candle', count: 1 },
            { op: 'narrate', text: 'You set the jar deep in the hollow. The flame steadies, glad of the shelter.' },
            { op: 'setFlag', flag: HIDDEN },
          ],
        },
        { label: 'NOT YET', ops: [{ op: 'say', text: 'You keep the jar in your pack a while longer.' }] },
      ],
    },
  ],

  // ---- "A Light Left On" — Linnet and the forbidden candle -----------------------
  // a nested if/else ladder (each level exactly one branch), latest stage first
  'script.still_candle_child': [
    { op: 'run', ref: 'script.still_candle_thanks', if_flag: HIDDEN },
    { op: 'run', ref: 'script.still_candle_child_b', unless_flag: HIDDEN },
  ],
  'script.still_candle_child_b': [
    { op: 'run', ref: 'script.still_candle_thanks', if_flag: SHOWN },
    { op: 'run', ref: 'script.still_candle_child_c', unless_flag: SHOWN },
  ],
  'script.still_candle_child_c': [
    { op: 'run', ref: 'script.still_candle_waiting', if_flag: CANDLE },
    { op: 'run', ref: 'script.still_candle_ask', unless_flag: CANDLE },
  ],
  'script.still_candle_ask': [
    { op: 'say', speaker: 'LINNET', text: 'Shh! Are you the lamp person? You are. Can you keep a lamp sort of secret?' },
    { op: 'narrate', text: 'She opens her coat. In a stoppered jar, a candle burns: small, steady, entirely forbidden.' },
    { op: 'say', speaker: 'LINNET', text: 'It was in Gran\'s things. I lit it with the hall\'s tinder. It\'s the only thing in Stillwater that moves when you breathe on it.' },
    { op: 'say', speaker: 'LINNET', text: 'If Mam finds it she\'ll be sad, not cross. That\'s worse. Will you hide it in the old willow?' },
    { op: 'say', speaker: 'LINNET', text: 'Or show Mam. She once had a candle in every window. Maybe she\'d remember. You choose, lamp person.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'still_candle', count: 1 },
    { op: 'say', text: 'You got LINNET\'S CANDLE! [[Hide it in the willow]], or [[show her mother, Maren]].' },
    { op: 'setFlag', flag: CANDLE },
  ],
  'script.still_candle_waiting': [
    { op: 'say', speaker: 'LINNET', text: 'Still lit? [[The willow by the water]], or [[Mam\'s house]], the one with the dormer.' },
  ],
  'script.still_candle_thanks': [
    { op: 'say', speaker: 'LINNET', if_flag: HIDDEN, text: 'You hid it in the willow! You only see it from right up close. A window nobody else knows.' },
    { op: 'say', speaker: 'LINNET', if_flag: SHOWN, unless_flag: HIDDEN, text: 'Mam found me. She didn\'t say anything. She held my hand and watched the candle for ages, then said I can keep it in my nook, if I\'m careful.' },
    { op: 'say', speaker: 'LINNET', text: 'This was Gran\'s too. It fell from the sky before I was born, warm as toast. Lamp people get shiny things.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'You got a STARGLASS SHARD!' },
    { op: 'setFlag', flag: CANDLE_DONE },
  ],
  'script.still_candle_child_after': [
    { op: 'say', speaker: 'LINNET', if_flag: DAWN, text: 'Look up! Mam opened the shutter. There\'s a lamp, and my brother keeps pressing his nose to the glass.' },
    { op: 'say', speaker: 'LINNET', if_flag: HIDDEN, text: 'I tell the willow candle my day each evening. It flickers in the good bits.' },
    { op: 'say', speaker: 'LINNET', unless_flag: HIDDEN, text: 'Mam trims the wick for me now, very slowly, like she\'s remembering how.' },
  ],
  'script.still_maren': [
    { op: 'run', ref: 'script.still_maren_offer', if_flag: CANDLE, unless_flag: HIDDEN },
    { op: 'run', ref: 'script.still_maren_talk', unless_flag: CANDLE },
    { op: 'run', ref: 'script.still_maren_talk', if_flag: HIDDEN },
  ],
  'script.still_maren_talk': [
    { op: 'say', speaker: 'MAREN', unless_flag: DAWN, text: 'Linnet\'s father kept the ferry-lamp at Saltreach. The winter it went dark, so did he. I brought her here so she\'d never watch a light go out.' },
    { op: 'say', speaker: 'MAREN', unless_flag: DAWN, text: 'She\'s never seen a candle in a window. I used to light one in each. ...Mind the step.' },
    { op: 'say', speaker: 'MAREN', if_flag: DAWN, text: 'I opened the shutter upstairs this morning. Linnet asked to put a candle there. I said yes before I\'d thought. The easiest yes of my life.' },
  ],
  'script.still_maren_offer': [
    { op: 'run', ref: 'script.still_maren_talk', if_flag: SHOWN },
    {
      op: 'choice',
      unless_flag: SHOWN,
      speaker: 'MAREN',
      prompt: 'Maren looks up from the hearth.',
      options: [
        {
          label: 'SHOW HER THE CANDLE',
          ops: [
            { op: 'narrate', text: 'You set the jar down. The flame stands straight, as small flames do in a quiet room.' },
            { op: 'say', speaker: 'MAREN', text: '...That\'s my mother\'s jar. Linnet found it, didn\'t she. Of course she did.' },
            { op: 'musicFade', ms: 700 },
            { op: 'say', speaker: 'MAREN', text: 'I came so she\'d never lose anything. I never thought what she\'d never have.' },
            { op: 'say', speaker: 'MAREN', text: 'Leave it with me. I won\'t put it out. I\'ll find her. We\'ll watch it together.' },
            { op: 'takeItem', item: 'still_candle', count: 1 },
            { op: 'setFlag', flag: SHOWN },
          ],
        },
        { label: 'SOMETHING ELSE', ops: [{ op: 'run', ref: 'script.still_maren_talk' }] },
      ],
    },
  ],
  'script.still_child_bed': [
    { op: 'say', unless_flag: SHOWN, text: 'A small bed in its own room. The shelf beside it is bare, swept, carefully kept empty.' },
    { op: 'say', if_flag: SHOWN, text: 'A small bed. On the shelf beside it, a candle in a jar, burning with great care.' },
  ],

  // ---- "The Way Home" — Tessaly, walked through the fog to Pale Vault ---------
  'script.still_tessaly': [
    { op: 'say', speaker: 'TESSALY', text: 'Up through the marsh? Alone? ...I came the other way, from my lamp-shop at Pale Vault. I put the lamps out myself, one a night, then walked here.' },
    { op: 'say', speaker: 'TESSALY', text: 'I want to go home. But the fog to the Rimeway is so thick. At the village edge my feet just... stop.' },
    {
      op: 'choice',
      speaker: 'TESSALY',
      prompt: 'Would you walk me home? Just through the fog. I\'ll be all right after that.',
      options: [
        {
          label: 'WALK HER HOME',
          ops: [
            { op: 'say', speaker: 'TESSALY', text: 'Thank you. Go ahead. I\'ll wait by [[the old set table in the fog]].' },
            { op: 'setFlag', flag: TESS },
          ],
        },
        { label: 'NOT YET', ops: [{ op: 'say', speaker: 'TESSALY', text: 'No, of course. I\'ve waited a year. I can wait for you.' }] },
      ],
    },
  ],
  'script.still_tessaly_fog1': [
    { op: 'say', speaker: 'TESSALY', text: 'There you are. Somebody laid that table for three and never came back. I laid my shop out like that, once. Every lamp in its place.' },
    { op: 'say', speaker: 'TESSALY', text: 'I\'m all right. [[Keep going south]], into the deep fog. I\'ll follow your light.' },
    { op: 'setFlag', flag: TESS1 },
  ],
  'script.still_tessaly_fog2': [
    { op: 'say', speaker: 'TESSALY', text: 'The worst of it. I walked through here with my eyes shut, not to see what we\'d done.' },
    { op: 'say', speaker: 'TESSALY', text: 'I\'ll keep them open this time. The Rimeway road starts east of here; I know every step. [[Meet me at Pale Vault]]. I\'ll be the one crying in the street.' },
    { op: 'setFlag', flag: TESS2 },
  ],
  'script.still_tessaly_home': [
    { op: 'say', speaker: 'TESSALY', text: 'I\'m home. The shop\'s still here. Three winters, and somebody\'s been sweeping my step.' },
    { op: 'say', speaker: 'TESSALY', text: 'This lamp hung in my window so the lost could find the door. Carry it. Held to a kin on its last scrap, it\'ll call it home, and it never burns down. It brought me home, didn\'t it?' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'tessalys_lamp', count: 1 },
    { op: 'say', text: 'You got TESSALY\'S LAMP! Twice as bright on a kin [[below a quarter of its health]], and never spent.' },
    { op: 'setFlag', flag: TESS_DONE },
  ],
  'script.still_tessaly_after': [
    { op: 'say', speaker: 'TESSALY', unless_flag: DAWN, text: 'I\'ve opened one shutter on the shop. Just one. It\'s a start.' },
    { op: 'say', speaker: 'TESSALY', if_flag: DAWN, text: 'Every shutter\'s open. I make bright lamps again. The waiting list\'s as long as the glacier.' },
  ],

  // ---- "The Shutter-wall" — the names of the lamps they put out ---------------
  'script.still_shutter_wall': [
    { op: 'say', text: 'Rows of grey shutters, each painted with a lamp the Hollowing put to sleep. THE WAYFARE LAMP. THE MARKET LAMP. THE FIRST LAMP OF STILLWATER. Dozens more.' },
    { op: 'say', text: 'Under some names, a date. Under a few, a dried sprig tucked into the louvres.' },
    { op: 'say', if_flag: WALL, unless_flag: WALL_DONE, text: 'Wenna\'s three: the Wayfare Lamp [[in the near fog]], the Market Lamp [[in the deep fog]], the First across the water.' },
  ],
  'script.still_hall_keeper': [
    { op: 'run', ref: 'script.still_hall_keeper_done', if_flag: WALL_DONE },
    { op: 'run', ref: 'script.still_hall_keeper_turnin', if_flag: WALL, unless_flag: WALL_DONE },
    { op: 'run', ref: 'script.still_hall_keeper_ask', unless_flag: WALL },
  ],
  'script.still_hall_keeper_ask': [
    { op: 'say', speaker: 'KEEPER WENNA', text: 'You\'ve read the wall. People expect a list of victories. It\'s a list of goodbyes.' },
    { op: 'say', speaker: 'KEEPER WENNA', text: 'People think we doused the lamps out of hate. We loved them, and couldn\'t bear what they kept promising. Understand that, before you relight everything.' },
    { op: 'say', speaker: 'KEEPER WENNA', text: 'Three still stand: the Wayfare Lamp in the near fog, the Market Lamp in the deep fog, the First Lamp over our water. [[Read their notes]], then tell me.' },
    { op: 'setFlag', flag: WALL },
  ],
  // the turn-in: a three-level if/else ladder on the three found flags (one
  // branch per level), so Wenna always names exactly the lamps still MISSING
  'script.still_hall_keeper_turnin': [
    { op: 'run', ref: 'script.still_wall_1', if_flag: lamp(1) },
    { op: 'run', ref: 'script.still_wall_0', unless_flag: lamp(1) },
  ],
  'script.still_hall_keeper_reward': [
    { op: 'say', speaker: 'KEEPER WENNA', text: 'All three. We weren\'t cruel. We were tired, and afraid of hoping, and the dark asked nothing.' },
    { op: 'say', speaker: 'KEEPER WENNA', text: 'Were we right? ...I don\'t know any more. I didn\'t know that until I said it to you.' },
    { op: 'musicFade', ms: 800 },
    { op: 'narrate', text: 'Under THE FIRST LAMP OF STILLWATER, she paints two words: NOT YET.' },
    { op: 'say', speaker: 'KEEPER WENNA', text: 'Honey from the old days, under a lit sky. Take it. Somebody should.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'giveMoney', amount: 1500 },
    { op: 'say', text: 'You got a LUMEN DROP and 1,500 wicks!' },
    { op: 'setFlag', flag: WALL_DONE },
  ],
  'script.still_hall_keeper_done': [
    { op: 'say', speaker: 'KEEPER WENNA', unless_flag: DAWN, text: 'NOT YET. Some mornings that means "not yet lit". Some, "not yet given up".' },
    { op: 'say', speaker: 'KEEPER WENNA', if_flag: DAWN, text: 'Each shutter\'s going back on its own lamp, open. It\'ll take years. I hope it does.' },
  ],
  'script.still_coldlamp_1': coldLamp(1, 'THE WAYFARE LAMP. LIT FOR THOSE ON THE ROAD.', [
    'Folded under the plate, a note: "I put this one out myself. My brother walked this road every spring, and every spring I waited at this lamp to see him come over the rise.',
    'He stopped coming. A lit lamp on an empty road is a question nobody answers. I couldn\'t keep asking it. — H."',
  ]),
  'script.still_coldlamp_2': coldLamp(2, 'THE MARKET LAMP. FEN-FAIR, FIRST MOON OF SPRING.', [
    'A note, wrapped in oilcloth: "We dimmed the market lamp the year the fen-fairs ended. People kept walking out to it from habit, and finding nobody, and walking home again.',
    'It seemed kinder to let them stop coming. It was kinder. I still don\'t know if it was right. — W."',
  ]),
  'script.still_coldlamp_3': coldLamp(3, 'THE FIRST LAMP OF STILLWATER. IT BROUGHT THE BOATS IN.', [
    'A note in an old, steady hand: "We were a fishing village once. When the water went still and the boats stopped, this lamp went on calling them for a whole winter.',
    'The Warden asked whether we wanted it to stop. We said yes. He held my hand while I closed the shutter, and I think he was saying goodbye to a lamp of his own. — Ashe."',
  ]),
  'script.still_vestry_ledger': [
    { op: 'say', text: 'The vestry ledger: who sleeps where, which kin needs a fresh blanket, who sits with the elders. Every page a different, careful hand.' },
  ],
  'script.still_hall_mourner': [
    { op: 'say', speaker: 'ROSALIND', unless_flag: DAWN, text: 'Mine\'s fourth row up: a garden lamp. Nobody would have missed it but me.' },
    { op: 'say', speaker: 'ROSALIND', if_flag: DAWN, text: 'My shutter\'s down. I\'ll plant something under my garden lamp that likes light.' },
  ],
  'script.still_hall_reader': [
    { op: 'say', speaker: 'ACOLYTE', unless_flag: DAWN, text: 'We eat in the dark and talk of who we\'ve lost. It helps more than you\'d think. Less than we pretend.' },
    { op: 'say', speaker: 'ACOLYTE', if_flag: DAWN, text: 'We light the table now. Everyone looks so much older. And so much kinder.' },
  ],

  // ---- the three who'd rather talk first ---------------------------------------
  'script.still_acolyte_gethin': talkFirst('still_acolyte_gethin', 'GETHIN',
    ['I trained kin for battle once, in the south. Then I couldn\'t bear watching them hurt, so I brought mine here, where nothing is asked of them.',
      'They\'re awake. I never put them to sleep; I let them rest. ...You\'d like to see how they\'ve kept. I can tell.'],
    'One gentle bout? For old times\' sake.',
    'They remembered. Every move. They looked... glad. I hadn\'t thought about whether they missed it.',
    'Of course. Some days talking is the braver thing.'),
  'script.still_acolyte_gethin_after': [
    { op: 'say', speaker: 'GETHIN', unless_flag: DAWN, text: 'How they looked, after. Like they\'d been waiting for someone to ask.' },
    { op: 'say', speaker: 'GETHIN', if_flag: DAWN, text: 'I\'m starting a practice ring again. Gentle bouts only. Children welcome.' },
  ],
  'script.still_acolyte_vesna': talkFirst('still_acolyte_vesna', 'VESNA',
    ['I was a star-watcher at Nightreach. I counted the falls, eleven winters. After a while I couldn\'t look up without counting.',
      'Here I don\'t look up at all. It\'s very restful. Do you look up, lamp-bearer? What do you see?'],
    'Show me what you see, then. In the old way.',
    'Bright. That\'s what you see. I\'d forgotten bright.',
    'No? That\'s all right. Look up for me, then, on your way out.'),
  'script.still_acolyte_vesna_after': [
    { op: 'say', speaker: 'VESNA', unless_flag: DAWN, text: 'I looked up last night. Nothing fell. I counted that as something.' },
    { op: 'say', speaker: 'VESNA', if_flag: DAWN, text: 'I\'ve started a new column. Not falls. Things that came back. It\'s getting long.' },
  ],
  'script.still_lamplighter_grisel': talkFirst('still_lamplighter_grisel', 'GRISEL',
    ['Forty years I lit lamps. Same ladder, same wicks, same lamps out by morning. Then one winter they went out and stayed out, and I thought: there. Now I can rest.',
      'Don\'t look at me like that. I\'m not your enemy, just a tired old man. ...Though I\'d like to see if your lamp burns as bright as they say.'],
    'Will you let an old lamplighter test your light?',
    'Ha. It does. Brighter. You\'ll wear yourself out, carrying that. ...Good. Someone should.',
    'Wise. I\'m a terrible loser. Forty years of practice.'),
  'script.still_lamplighter_grisel_after': [
    { op: 'say', speaker: 'GRISEL', unless_flag: DAWN, text: 'Trim your wick at the third knot, not the second. Old habit. Can\'t help myself.' },
    { op: 'say', speaker: 'GRISEL', if_flag: DAWN, text: 'They asked me to light the shore lamps. My knees said no. I went anyway.' },
  ],

  // ---- the inn, the lamp-maker, the homes ----------------------------------------
  'script.still_inn_rest': [
    { op: 'say', speaker: 'INNKEEPER', unless_flag: DAWN, text: 'Welcome to the Shutter. A bed, soup, and quiet. We have a great deal of quiet.' },
    { op: 'say', speaker: 'INNKEEPER', if_flag: DAWN, text: 'Welcome to the Shutter. We may change the name. Suggestions in the jar.' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEPER', text: 'Slept? Good. Sleep\'s the one thing we\'ve always been good at here.' },
  ],
  'script.still_inn_guest': [
    { op: 'say', speaker: 'ACOLYTE', unless_flag: DAWN, text: 'I sit with my back to the hearth, as we\'re meant to. But I feel it. A fire needn\'t be looked at to keep you warm. I think about that a lot.' },
    { op: 'say', speaker: 'ACOLYTE', if_flag: DAWN, text: 'I turned my chair round. Everyone stared. Then three more people turned theirs.' },
  ],
  'script.still_inn_pilgrim': [
    { op: 'say', speaker: 'TRAVELLER', unless_flag: DAWN, text: 'I came for one night, two winters ago. It\'s easy to stay where nothing\'s asked.' },
    { op: 'say', speaker: 'TRAVELLER', if_flag: DAWN, text: 'I\'m leaving in the morning. A real one. I want to see how it looks on a road.' },
  ],
  'script.still_lampmaker': [
    { op: 'say', speaker: 'OSRIC', unless_flag: DAWN, text: 'I lit lamps; now I make hoods. Same hands. A craft hardly cares which way it\'s pointed.' },
    { op: 'say', speaker: 'OSRIC', unless_flag: DAWN, text: 'For travellers: hooded lamps to slip past wild kin, balms, coals. Even bright cells.' },
    { op: 'say', speaker: 'OSRIC', if_flag: DAWN, text: 'Hoods are out. I\'m making lamps again. My hands knew the way before I did.' },
    { op: 'shop', shop: 'stillwater_lampmaker' },
  ],
  'script.still_lamp_bench': [
    { op: 'say', text: 'Lamp parts: hoods, caps, a half-made shutter. Every hinge oiled, every hood exact.' },
  ],
  'script.still_home_a_elder': [
    { op: 'say', speaker: 'EDWY', unless_flag: DAWN, text: 'We came up when our kin got old. We couldn\'t watch them fade. Here they sleep, and we sit by them.' },
    { op: 'say', speaker: 'EDWY', if_flag: DAWN, text: 'Old Bracken woke! Eleven winters older, he walked straight to the door. So we went out.' },
  ],
  'script.still_home_a_wife': [
    { op: 'say', speaker: 'MARGERY', unless_flag: DAWN, text: 'Tea? It\'s mostly hot water. The leaves wanted too much sun, so we stopped.' },
    { op: 'say', speaker: 'MARGERY', if_flag: DAWN, text: 'I\'ve put tea seeds in by the window. Come back in a year for a proper cup.' },
  ],
  'script.still_home_a_basket': [
    { op: 'say', unless_flag: DAWN, text: 'Old Bracken sleeps in a basket, grey to the muzzle. A tag, in two hands: OURS.' },
    { op: 'say', if_flag: DAWN, text: 'Old Bracken\'s basket, empty and warm. Grey hairs lead to the door. He\'s out walking.' },
  ],

  // ===========================================================================
  //  COLDFOG — the road north (Part E density)
  // ===========================================================================
  'script.still_trader': [
    { op: 'say', speaker: 'SEFTON', unless_flag: DAWN, text: 'No inn in the fog. [[Stillwater\'s just north]]. They\'ll bed you, whatever they think of your lamp.' },
    { op: 'say', speaker: 'SEFTON', unless_flag: DAWN, text: 'I carry what the road needs. The Hollowing don\'t mind. They like the road to be kind.' },
    { op: 'say', speaker: 'SEFTON', if_flag: DAWN, text: 'Folk walk the fog road just to look now. Like visiting a grave that turned out not to be one.' },
    { op: 'shop', shop: 'stillwater_trader' },
  ],
  'script.coldfog_fen_walker': [
    { op: 'say', speaker: 'FEN-WALKER', unless_flag: DAWN, text: 'I walk the fog\'s edge daily, where the grass is still green. I tell myself I keep it from creeping. It doesn\'t creep. It just... waits.' },
    { op: 'say', speaker: 'FEN-WALKER', unless_flag: DAWN, text: 'My daughter went to Stillwater. She writes that it\'s peaceful. I read her letters to the reeds.' },
    { op: 'say', speaker: 'FEN-WALKER', if_flag: DAWN, text: 'She visited. Stood here and said, "Was it always this green?" No, love. It wasn\'t.' },
  ],
  'script.coldfog_acolyte_north': [
    { op: 'say', speaker: 'ACOLYTE', text: 'Wait. Stillwater\'s north, and its people are resting. I keep this road so nobody arrives angry.' },
    { op: 'say', speaker: 'ACOLYTE', text: 'If you\'re angry, spend it on me. I would honestly rather that.' },
    { op: 'battle', trainer: 'coldfog_acolyte_north' },
    { op: 'say', speaker: 'ACOLYTE', text: 'There. You don\'t seem angry at all. Go on, then. Speak softly in the village.' },
    { op: 'setFlag', flag: 'flag:coldfog_acolyte_north_beaten' },
  ],
  'script.coldfog_acolyte_east': [
    { op: 'say', speaker: 'ELDER FENWICK', text: 'East are the fallow fields, quieted first. Their kin sleep under the fog like a blanket.' },
    { op: 'say', speaker: 'ELDER FENWICK', text: 'You\'ll want to wake them. Let me see if you can be trusted with that.' },
    { op: 'battle', trainer: 'coldfog_acolyte_east' },
    { op: 'say', speaker: 'ELDER FENWICK', text: 'Strong enough. Whether you\'re right is another matter. Look at the fields and decide.' },
    { op: 'setFlag', flag: 'flag:coldfog_acolyte_east_beaten' },
  ],
  'script.coldfog_acolyte_deep': [
    { op: 'say', speaker: 'ACOLYTE', text: 'Somebody\'s grandmother lit every lantern on these racks. We put each to sleep with a word and a cloth. That\'s not in the stories about us.' },
    { op: 'battle', trainer: 'coldfog_acolyte_deep' },
    { op: 'say', speaker: 'ACOLYTE', text: 'You fight like someone who\'s never had to give anything up. I hope you never do.' },
    { op: 'setFlag', flag: 'flag:coldfog_acolyte_deep_beaten' },
  ],
  'script.coldfog_acolyte_west': [
    { op: 'say', speaker: 'ELDER MARROW', text: 'You walked the whole marsh with that lamp held up. It looks heavy.' },
    { op: 'say', speaker: 'ELDER MARROW', text: 'I carried one like it once, and set it down here for good. Let me show you how that felt.' },
    { op: 'battle', trainer: 'coldfog_acolyte_west' },
    { op: 'say', speaker: 'ELDER MARROW', text: '...Hm. You make it look less heavy than I remember.' },
    { op: 'setFlag', flag: 'flag:coldfog_acolyte_west_beaten' },
  ],
  'script.coldfog_camp_mourner': [
    { op: 'say', speaker: 'OLD WOMAN', unless_flag: DAWN, text: 'This was the wardens\' camp. They rolled their bedrolls, swept the ash, and walked north to Stillwater one at a time. I was the last. I come back to sit.' },
    { op: 'say', speaker: 'OLD WOMAN', if_flag: DAWN, text: 'I lit the camp fire this morning. It took first time, as if it had been waiting.' },
  ],
  'script.pickup_coldfog_starlight': pickup('flag:picked_coldfog_starlight',
    [{ op: 'giveItem', item: 'hearth_coal', count: 1 }, { op: 'giveItem', item: 'beacon_charge', count: 2 }],
    'Your lamp\'s Starlight finds a nook the fog hid: a traveller\'s bundle! A HEARTH COAL and two BEACON CHARGES!'),
  'script.pickup_coldfog_deep_starlight': pickup('flag:picked_coldfog_deep_starlight',
    [{ op: 'giveItem', item: 'starglass_shard', count: 1 }],
    'At Starlight, your lamp pulls a glint from the reeds: a STARGLASS SHARD, warm as a hand!'),

  // ---- Stillwater's caches ------------------------------------------------------
  'script.pickup_stillwater_meadow': pickup('flag:picked_stillwater_meadow',
    [{ op: 'giveItem', item: 'bright_balm', count: 2 }],
    'Tucked in the grey meadow: a basket somebody meant to bring home. Two BRIGHT BALMS!'),
  'script.pickup_stillwater_far_shore': pickup('flag:picked_stillwater_far_shore',
    [{ op: 'giveMoney', amount: 2000 }],
    'Under the First Lamp, a fisher\'s tin, eleven winters dry. 2,000 wicks!'),

  // ===========================================================================
  //  THE NIGHTREACH LANE + SUNVAULT CLIMB (Part E): the lamplighters and climbers
  // ===========================================================================
  'script.nightlane_lamplighter_a': [
    { op: 'say', speaker: 'LAMPLIGHTER', text: 'Evening! Always evening. I keep this lane lit for the Lantern-car folk. Somebody has to.' },
    { op: 'say', speaker: 'LAMPLIGHTER', unless_flag: DAWN, text: 'The Hollowing\'s village, Stillwater, is up [[the fog road north]] from the near marsh. They won\'t hurt you. They\'ll just look at your lamp like a sad song.' },
    { op: 'say', speaker: 'LAMPLIGHTER', if_flag: DAWN, text: 'Stillwater folk came to help trim the lamps. One cried. Happy crying, I think.' },
  ],
  'script.nightlane_lamplighter_b': [
    { op: 'say', speaker: 'WICK-TRIMMER', unless_flag: DAWN, text: 'Nightreach, the marshes, then the fog road north. My gran lit lamps all the way to Stillwater up there. I\'ve never been. They\'d ask me to put my lamp out.' },
    { op: 'say', speaker: 'WICK-TRIMMER', if_flag: DAWN, text: 'I went to Stillwater! They fed me soup and asked how to trim a wick. I\'m going back to teach.' },
  ],
  'script.sunvault_climber_ii': [
    { op: 'say', speaker: 'CLIMBER', text: 'Halfway, and my legs complain. Watch the next ledge, not the top. The top just laughs.' },
  ],
  'script.sunvault_climber_iii': [
    { op: 'say', speaker: 'CLIMBER', text: 'These terraces caught the sun\'s last light. Put a hand on the stone. Warm, isn\'t it?' },
  ],
  'script.sunvault_climber_iv': [
    { op: 'say', speaker: 'CLIMBER', text: 'From the top you can see the observatory, then the fog. North of it, a village nobody visits. My mother went. Every spring she writes one word: "resting".' },
  ],
};

// the cold lamps' read-backs (written by coldLamp() above)
Object.assign(STILLWATER_SCRIPTS, READS);

// Keeper Wenna's turn-in ladder: `script.still_wall_<bits>`, one bit per lamp in
// order (1 = found). Each inner node branches on the next lamp's flag; each leaf
// names what's still missing, or (all three) runs the reward.
const WALL_LAMPS = [
  'the Wayfare Lamp in the near fog, just south of the gap',
  'the Market Lamp, deeper in, in the deep fog',
  'the First Lamp of Stillwater, across our own water',
];
const wallLeaf = (bits: string): CutsceneStep[] => {
  if (bits === '111') return [{ op: 'run', ref: 'script.still_hall_keeper_reward' }];
  if (bits === '000') {
    return [{ op: 'say', speaker: 'KEEPER WENNA', text: 'Found them? The Wayfare Lamp in the near fog, the Market Lamp in the deep fog, the First over the water. [[Read what they left]]. It\'s how I can explain us.' }];
  }
  const missing = WALL_LAMPS.filter((_, i) => bits[i] === '0');
  const found = 3 - missing.length;
  const head = found === 2 ? 'Two of three. Only one left:' : 'One of three, then. Still to find:';
  const tail = missing.length === 1 ? '[[Read the note at its foot]]' : '[[Read the notes at their feet]]';
  return [{ op: 'say', speaker: 'KEEPER WENNA', text: `${head} ${missing.join(', and ')}. ${tail}, then come back to me.` }];
};
for (const bits of ['0', '1', '00', '01', '10', '11']) {
  const n = bits.length + 1;
  STILLWATER_SCRIPTS[`script.still_wall_${bits}`] = [
    { op: 'run', ref: `script.still_wall_${bits}1`, if_flag: lamp(n) },
    { op: 'run', ref: `script.still_wall_${bits}0`, unless_flag: lamp(n) },
  ];
}
for (const bits of ['000', '001', '010', '011', '100', '101', '110', '111']) {
  STILLWATER_SCRIPTS[`script.still_wall_${bits}`] = wallLeaf(bits);
}

export const STILLWATER_DIALOGUE: DialogueRegistry = {
  'sign.stillwater': [
    { text: 'STILLWATER. The weary are welcome. Speak softly; the kin are sleeping.' },
  ],
  // Coldfog I's gold pocket (build_coldfog_marches_i.py): the curio and why it's here.
  'sign.coldfog_gold': [
    { text: 'A survey peg, paint gone grey. Scratched under it: "Gold grass, in all this. The Solarium\'s light came this far once, down the old water, and soaked in."' },
    { text: '"Something big, slow and golden roots here some nights, petals shut against the fog. Sun-vine, I\'d swear. Walk the gold quietly."' },
  ],
  'sign.stillwater_hall': [
    { text: 'THE QUIET HALL. Remembrance any night. Supper on the darkest.' },
  ],
  'sign.stillwater_mourning': [
    { text: 'SOUTH-EAST: [[THE FALLOW FIELDS]]. SOUTH-WEST: [[the fog road]] to the marshes.' },
  ],
  'sign.stillwater_waystone': [
    { text: 'A lamp-stone, shuttered like every lamp in Stillwater. The Lanternway still knows it: the lit road can carry you anywhere you\'ve been.' },
  ],
  'sign.stillwater_inn': [
    { text: 'THE SHUTTER. Beds, soup, quiet. No lamps after dusk (it is always after dusk).' },
  ],
  'npc.coldfog_acolyte_north_after': [
    { speaker: 'ACOLYTE', text: '[[Stillwater\'s through the gap]]. Tell them Brin sent you. I wasn\'t angry either.' },
  ],
  'npc.coldfog_acolyte_east_after': [
    { speaker: 'ELDER FENWICK', text: 'The fallow fields are east. Wake things gently. They\'ve been dreaming a long time.' },
  ],
  'npc.coldfog_acolyte_deep_after': [
    { speaker: 'ACOLYTE', text: 'I\'ve started lifting the cloths off the racks. To dust the glass, I tell myself.' },
  ],
  'npc.coldfog_acolyte_west_after': [
    { speaker: 'ELDER MARROW', text: 'Perhaps I\'ll pick my lamp up again. Not today. But I\'m thinking where I left it.' },
  ],
};
