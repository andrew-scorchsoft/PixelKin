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
    { op: 'say', unless_flag: lamp(n), text: 'It\'s one of the names from the shutter-wall. You\'ll tell the hall-keeper you found it.' },
    { op: 'setFlag', flag: lamp(n) },
  ];
  return [
    { op: 'say', unless_flag: WALL, text: 'A doused lamp, its glass grey. There\'s a small brass plate at its foot, too tarnished to read without knowing what to look for.' },
    { op: 'run', ref: read, if_flag: WALL },
  ];
};

export const STILLWATER_SCRIPTS: ScriptRegistry = {
  // ===========================================================================
  //  STILLWATER — the village (people + the square)
  // ===========================================================================
  'script.still_greeter': [
    { op: 'say', speaker: 'ACOLYTE', unless_flag: DAWN, text: 'Oh. A lamp. ...No, keep it, it\'s all right. We know who you are. You\'re the one relighting the sky.' },
    { op: 'say', speaker: 'ACOLYTE', unless_flag: DAWN, text: 'This is Stillwater. Nobody here will stop you. We only ask that you keep your voice down. The kin are sleeping, and they sleep so lightly now.' },
    { op: 'say', speaker: 'ACOLYTE', if_flag: DAWN, text: 'You can talk at a normal volume now. I keep forgetting. We all keep forgetting.' },
  ],
  'script.still_elder': [
    { op: 'say', speaker: 'ELDER ASHE', unless_flag: DAWN, text: 'Sit a moment, if you like. Everyone who comes to Stillwater lost something to the cycle. A star, a season, a person. Out there the light keeps promising it\'ll come back. In here, nothing promises anything.' },
    { op: 'say', speaker: 'ELDER ASHE', unless_flag: DAWN, text: 'You think we\'re wrong. Perhaps we are. But nobody in this village has cried at a sunrise in eleven winters, and I\'m not sure you can say the same for yours.' },
    { op: 'say', speaker: 'ELDER ASHE', if_flag: DAWN, text: 'Morning. I said I\'d never say that word again. It turns out I don\'t mind it as much as I feared.' },
    { op: 'say', speaker: 'ELDER ASHE', if_flag: DAWN, text: 'The Warden came home for a night, after. He opened his own shutter first, then went door to door asking if we\'d like ours opened. Some of us said not yet. He said that was all right.' },
  ],
  'script.still_blanket_folder': [
    { op: 'say', speaker: 'GRETE', text: 'Every morning I fold their blankets back and every evening I fold them up to the chin. They don\'t notice. I do it anyway.' },
    { op: 'say', speaker: 'GRETE', unless_flag: DAWN, text: 'Asleep isn\'t gone. That\'s what I tell myself. You can hear them breathing, if you stand still.' },
    { op: 'say', speaker: 'GRETE', if_flag: DAWN, text: 'Two of them woke up this week and wanted breakfast. I\'d forgotten how loud they are. I\'ve been smiling about it all day.' },
  ],
  'script.still_sweeper': [
    { op: 'say', speaker: 'ODO', text: 'Swept twice a day, these flags. Nobody walks on them much. But a swept lane says somebody still cares how things are, and we do. That\'s the part people get wrong about us.' },
  ],
  'script.still_shore_watcher': [
    { op: 'say', speaker: 'LISBET', unless_flag: DAWN, text: 'The water went still the winter the dark came, and it never moved again. Not a ripple. That\'s how the village got its name.' },
    { op: 'say', speaker: 'LISBET', unless_flag: DAWN, text: 'Some nights I think it\'s waiting. Most nights I think that\'s a silly thing to think about water.' },
    { op: 'say', speaker: 'LISBET', if_flag: DAWN, text: 'It rippled this morning. Only once, when a moth landed on it. I\'ve been standing here for an hour in case it does it again.' },
  ],
  'script.still_doubter': [
    { op: 'say', speaker: 'CORWEN', unless_flag: DAWN, text: 'Can I tell you something I haven\'t told the hall? I dream about colours. Every night. Orange, mostly. The orange of a lamp through a window when you\'re walking home.' },
    { op: 'say', speaker: 'CORWEN', unless_flag: DAWN, text: 'I came here so I\'d stop missing things. I don\'t miss them any less. I just do it quietly now.' },
    { op: 'say', speaker: 'CORWEN', if_flag: DAWN, text: 'I\'m going home next month, to the coast. I wrote to my sister. She wrote back three pages, and the third page was just the word YES, very large.' },
  ],
  'script.still_water_carrier': [
    { op: 'say', speaker: 'HALLAM', text: 'The well\'s the only water in Stillwater that moves. Funny, that. We draw it for the hearths. A hearth with its face to the wall still keeps a house warm; it just doesn\'t make anyone look up.' },
  ],
  'script.still_meadow_keeper': [
    { op: 'say', speaker: 'NELL', unless_flag: DAWN, text: 'Mind the grey meadow. The kin out there aren\'t asleep, they\'re just... quiet. The moths keep the others dreaming. They\'re gentle about it.' },
    { op: 'say', speaker: 'NELL', unless_flag: DAWN, text: 'There\'s a cold lamp round the far side of the water, on the shore under the crags. The first lamp this village ever had. Nobody goes round there now.' },
    { op: 'say', speaker: 'NELL', if_flag: DAWN, text: 'The meadow\'s full of wisps today, glowing like they\'ve something to prove. Go and look. Take your time. We\'ve got time now.' },
  ],
  'script.still_shore_lamp': [
    { op: 'say', unless_flag: DAWN, text: 'A lamp-post with its lantern boxed in by two grey shutters, latched. Not broken. Not even out, perhaps. Just... put to sleep.' },
    { op: 'say', if_flag: DAWN, text: 'The shutters stand open. Somebody has lit the wick, and trimmed it carefully, the way you do when you haven\'t done it in years.' },
  ],
  'script.still_notice': [
    { op: 'say', text: 'A notice in a careful hand: "STILLWATER WELCOMES THE WEARY. Speak softly. Leave lamps as you find them. Supper in the hall on the darkest night of every month, and every night is the darkest, so come whenever you like."' },
  ],
  'script.still_sleeper': [
    { op: 'say', unless_flag: DAWN, text: 'A kin asleep under a folded grey blanket. Its breathing is slow and even. Someone has tucked the blanket round its paws.' },
    { op: 'say', if_flag: DAWN, text: 'A kin under a grey blanket, dozing. One eye opens, finds you, and closes again, perfectly content. This sleep is the ordinary kind.' },
  ],
  'script.still_willow_hollow': [
    { op: 'run', ref: 'script.still_willow_hide', if_flag: CANDLE, unless_flag: CANDLE_DONE },
    { op: 'say', unless_flag: CANDLE, text: 'An old willow with a dry hollow in its trunk, just big enough to keep something secret in.' },
    { op: 'say', if_flag: HIDDEN, text: 'Deep in the willow\'s hollow, the little candle burns in its jar. You can only see it from right here.' },
    { op: 'say', if_flag: SHOWN, text: 'An old willow with a dry hollow in its trunk. Empty now. The candle lives in a window.' },
  ],
  'script.still_willow_hide': [
    { op: 'run', ref: 'script.still_willow_offer', unless_flag: HIDDEN, if_flag: CANDLE },
  ],
  'script.still_willow_offer': [
    { op: 'say', unless_flag: SHOWN, text: 'The hollow is dry and deep, and it faces the crags. Nobody in the village would see a light in here.' },
    {
      op: 'choice',
      unless_flag: SHOWN,
      prompt: 'Hide Linnet\'s candle in the hollow?',
      options: [
        {
          label: 'HIDE IT HERE',
          ops: [
            { op: 'takeItem', item: 'still_candle', count: 1 },
            { op: 'narrate', text: 'You set the jar deep in the hollow. The little flame steadies and leans toward you, as if it\'s glad of the shelter.' },
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
    { op: 'say', speaker: 'LINNET', text: 'Shh! Are you the lamp person? You are. You\'ve got a lamp. Can you keep a secret if it\'s a lamp sort of secret?' },
    { op: 'narrate', text: 'She opens her coat. Inside, in a stoppered jar, a stub of candle is burning: a small, steady, entirely forbidden flame.' },
    { op: 'say', speaker: 'LINNET', text: 'I found it in Gran\'s things. I lit it with the hall\'s tinder when nobody was looking. I know we\'re not meant to. But I like looking at it. It\'s the only thing in Stillwater that moves when you breathe on it.' },
    { op: 'say', speaker: 'LINNET', text: 'If Mam finds it she\'ll be sad, not cross. That\'s worse. Will you keep it for me? You could hide it somewhere only I know. The old willow by the water has a hole in it.' },
    { op: 'say', speaker: 'LINNET', text: 'Or... you could show it to Mam. She used to have a candle in every window. Maybe she\'d remember she liked them. I don\'t know. You choose. You\'re the lamp person.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'still_candle', count: 1 },
    { op: 'say', text: 'You got LINNET\'S CANDLE! Hide it in the willow\'s hollow, or show it to her mother, Maren.' },
    { op: 'setFlag', flag: CANDLE },
  ],
  'script.still_candle_waiting': [
    { op: 'say', speaker: 'LINNET', text: 'Is it still lit? Don\'t let it go out! The willow by the water, or Mam\'s house, the one with the dormer. You choose.' },
  ],
  'script.still_candle_thanks': [
    { op: 'say', speaker: 'LINNET', if_flag: HIDDEN, text: 'You hid it? In the willow? I went and looked and I could see it, only from right up close. It\'s like having a window nobody else knows about.' },
    { op: 'say', speaker: 'LINNET', if_flag: SHOWN, unless_flag: HIDDEN, text: 'Mam came and found me. She didn\'t say anything. She just held my hand and looked at the candle for ages. Then she said we could keep it in my nook, if I promise to be careful.' },
    { op: 'say', speaker: 'LINNET', text: 'This was Gran\'s too. She said it fell out of the sky before I was born, warm as toast. I want you to have it. Lamp people should have the shiny things.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'You got a STARGLASS SHARD!' },
    { op: 'setFlag', flag: CANDLE_DONE },
  ],
  'script.still_candle_child_after': [
    { op: 'say', speaker: 'LINNET', if_flag: DAWN, text: 'Look up! Mam opened the shutter upstairs. There\'s a lamp in the window now, and my little brother won\'t stop pressing his nose on the glass.' },
    { op: 'say', speaker: 'LINNET', if_flag: HIDDEN, text: 'I visit the willow every evening. I tell the candle about my day. It doesn\'t say anything back, but it flickers in the good places.' },
    { op: 'say', speaker: 'LINNET', unless_flag: HIDDEN, text: 'Mam trims the wick for me now. She does it very slowly, like she\'s remembering how.' },
  ],
  'script.still_maren': [
    { op: 'run', ref: 'script.still_maren_offer', if_flag: CANDLE, unless_flag: HIDDEN },
    { op: 'run', ref: 'script.still_maren_talk', unless_flag: CANDLE },
    { op: 'run', ref: 'script.still_maren_talk', if_flag: HIDDEN },
  ],
  'script.still_maren_talk': [
    { op: 'say', speaker: 'MAREN', unless_flag: DAWN, text: 'Linnet\'s father kept the ferry-lamp at Saltreach. The winter it went dark, so did he. I brought Linnet here so she\'d never have to watch a light go out.' },
    { op: 'say', speaker: 'MAREN', unless_flag: DAWN, text: 'She\'s never seen a candle in a window. I used to put one in every window we had. ...Mind the step on your way out.' },
    { op: 'say', speaker: 'MAREN', if_flag: DAWN, text: 'I opened the shutter upstairs this morning. Linnet asked if she could put a candle there. I said yes before I\'d even thought about it. It was the easiest yes of my life.' },
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
            { op: 'narrate', text: 'You set the jar on the table. The flame stands up straight, the way small flames do in a quiet room.' },
            { op: 'say', speaker: 'MAREN', text: '...That\'s my mother\'s jar. Linnet found it, didn\'t she. Of course she did.' },
            { op: 'musicFade', ms: 700 },
            { op: 'say', speaker: 'MAREN', text: 'I came here so she\'d never lose anything. I didn\'t think about what she\'d never have.' },
            { op: 'say', speaker: 'MAREN', text: 'Leave it with me. I won\'t put it out. I\'ll go and find her. I think I\'d like to watch it with her.' },
            { op: 'takeItem', item: 'still_candle', count: 1 },
            { op: 'setFlag', flag: SHOWN },
          ],
        },
        { label: 'SOMETHING ELSE', ops: [{ op: 'run', ref: 'script.still_maren_talk' }] },
      ],
    },
  ],
  'script.still_child_bed': [
    { op: 'say', unless_flag: SHOWN, text: 'A small bed in a small room of its own. The shelf beside it is bare, swept, and very carefully kept empty.' },
    { op: 'say', if_flag: SHOWN, text: 'A small bed in a small room of its own. On the shelf beside it, a candle in a jar, burning with great care.' },
  ],

  // ---- "The Way Home" — Tessaly, walked through the fog to Pale Vault ---------
  'script.still_tessaly': [
    { op: 'say', speaker: 'TESSALY', text: 'You came up through the marsh? On your own? ...I came the other way, three winters ago. From Pale Vault. I had a lamp-shop on the glacier road. I put the lamps out myself, one a night, and then I walked here.' },
    { op: 'say', speaker: 'TESSALY', text: 'I want to go home. I\'ve wanted to for a year. But the fog is so thick between here and the Rimeway, and every time I reach the edge of the village my feet just... stop.' },
    {
      op: 'choice',
      speaker: 'TESSALY',
      prompt: 'Would you walk me home? Just through the fog. I\'ll be all right after that.',
      options: [
        {
          label: 'WALK HER HOME',
          ops: [
            { op: 'say', speaker: 'TESSALY', text: 'Thank you. Go on ahead and I\'ll follow your light. I find it easier, following something. I\'ll wait for you by the old set table in the fog.' },
            { op: 'setFlag', flag: TESS },
          ],
        },
        { label: 'NOT YET', ops: [{ op: 'say', speaker: 'TESSALY', text: 'No, of course. I\'ve waited a year. I can wait for you.' }] },
      ],
    },
  ],
  'script.still_tessaly_fog1': [
    { op: 'say', speaker: 'TESSALY', text: 'There you are. I sat by that table for a while. Somebody laid it for three and never came back to it. I laid my shop out like that, once. Every lamp in its place.' },
    { op: 'say', speaker: 'TESSALY', text: 'I\'m all right. Keep going south, down into the deep fog. I\'ll follow your light.' },
    { op: 'setFlag', flag: TESS1 },
  ],
  'script.still_tessaly_fog2': [
    { op: 'say', speaker: 'TESSALY', text: 'This is the worst of it. I walked through here three winters ago with my eyes shut, so I wouldn\'t have to see what we\'d done.' },
    { op: 'say', speaker: 'TESSALY', text: 'I\'ll keep them open this time. The Rimeway road starts east of here. From there I know every step. Meet me at home, at Pale Vault. I\'ll be the one crying in the street.' },
    { op: 'setFlag', flag: TESS2 },
  ],
  'script.still_tessaly_home': [
    { op: 'say', speaker: 'TESSALY', text: 'You came. I\'m home. The shop\'s still there, shutters and all. Somebody\'s been sweeping the step. Three winters, and somebody swept my step.' },
    { op: 'say', speaker: 'TESSALY', text: 'These were my own lamps, the three I used to sing the sleeping kin quiet with. I want you to carry them now. Hold one up to a kin that\'s dozing and it won\'t lull it any deeper. It\'ll call it home.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'tessalys_lamp', count: 3 },
    { op: 'say', text: 'You got three TESSALY\'S LAMPS! Each one burns threefold on a dozing kin.' },
    { op: 'setFlag', flag: TESS_DONE },
  ],
  'script.still_tessaly_after': [
    { op: 'say', speaker: 'TESSALY', unless_flag: DAWN, text: 'I\'ve opened one shutter on the shop. Just one. It\'s a start.' },
    { op: 'say', speaker: 'TESSALY', if_flag: DAWN, text: 'Every shutter\'s open now. I\'m making lamps again. Bright ones. I\'ve a waiting list as long as the glacier.' },
  ],

  // ---- "The Shutter-wall" — the names of the lamps they put out ---------------
  'script.still_shutter_wall': [
    { op: 'say', text: 'A wall of small grey shutters, row on row. On each, in careful paint: the name of a lamp the Hollowing put to sleep. THE WAYFARE LAMP. THE MARKET LAMP. THE FIRST LAMP OF STILLWATER. Dozens more.' },
    { op: 'say', text: 'Under some names, a date. Under a few, only a sprig of something dried, tucked into the louvres.' },
    { op: 'say', if_flag: WALL, unless_flag: WALL_DONE, text: 'You remember the hall-keeper\'s three: the Wayfare Lamp in the fog, the Market Lamp deeper in, and the First Lamp across the water.' },
  ],
  'script.still_hall_keeper': [
    { op: 'run', ref: 'script.still_hall_keeper_done', if_flag: WALL_DONE },
    { op: 'run', ref: 'script.still_hall_keeper_turnin', if_flag: WALL, unless_flag: WALL_DONE },
    { op: 'run', ref: 'script.still_hall_keeper_ask', unless_flag: WALL },
  ],
  'script.still_hall_keeper_ask': [
    { op: 'say', speaker: 'KEEPER WENNA', text: 'You\'ve been reading the wall. Everyone does, the first time. They expect a list of victories and find a list of goodbyes.' },
    { op: 'say', speaker: 'KEEPER WENNA', text: 'People outside think we put out the lamps because we hate the light. We put them out because we loved them, and couldn\'t bear what they kept promising.' },
    { op: 'say', speaker: 'KEEPER WENNA', text: 'I\'d like you to understand that, before you go relighting everything. Three of those lamps still stand where they were. The Wayfare Lamp in the near fog, the Market Lamp in the deep fog, and the First Lamp of Stillwater, across our own water. Each has a note left at its foot. Read them. Then come and tell me what you think.' },
    { op: 'setFlag', flag: WALL },
  ],
  // the turn-in: a three-level if/else ladder on the three found flags (one
  // branch per level), so Wenna always names exactly the lamps still MISSING
  'script.still_hall_keeper_turnin': [
    { op: 'run', ref: 'script.still_wall_1', if_flag: lamp(1) },
    { op: 'run', ref: 'script.still_wall_0', unless_flag: lamp(1) },
  ],
  'script.still_hall_keeper_reward': [
    { op: 'say', speaker: 'KEEPER WENNA', text: 'All three. So now you know. We weren\'t cruel. We were tired, and we were frightened of hoping, and the dark asked nothing of us.' },
    { op: 'say', speaker: 'KEEPER WENNA', text: 'And now you\'ll ask me whether we were right. ...I don\'t know any more. That\'s the truth. I didn\'t know it was the truth until I said it to you.' },
    { op: 'musicFade', ms: 800 },
    { op: 'narrate', text: 'She takes a small pot of paint from the shelf and, under THE FIRST LAMP OF STILLWATER, adds two words: NOT YET.' },
    { op: 'say', speaker: 'KEEPER WENNA', text: 'The hall keeps a little honey from the old days, pressed from a sky that was still lit. Take it. Somebody should.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'giveMoney', amount: 1500 },
    { op: 'say', text: 'You got a LUMEN DROP and 1,500 wicks!' },
    { op: 'setFlag', flag: WALL_DONE },
  ],
  'script.still_hall_keeper_done': [
    { op: 'say', speaker: 'KEEPER WENNA', unless_flag: DAWN, text: 'NOT YET. I look at those two words every morning. Some mornings they mean "not yet lit". Some mornings they mean "not yet given up".' },
    { op: 'say', speaker: 'KEEPER WENNA', if_flag: DAWN, text: 'We\'re taking the shutter-wall down, a shutter at a time. Each one goes back on the lamp it belongs to, open. We\'ll be at it for years. I hope we are.' },
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
    { op: 'say', text: 'A ledger on the vestry desk: who sleeps where, which kin needs its blanket changed, whose turn it is to sit with the elders. Every page is in a different hand. Every hand is careful.' },
  ],
  'script.still_hall_mourner': [
    { op: 'say', speaker: 'ROSALIND', unless_flag: DAWN, text: 'I come here to sit near the names. Mine\'s the fourth row up. A little garden lamp. I don\'t know why I painted it; nobody would have missed it but me.' },
    { op: 'say', speaker: 'ROSALIND', if_flag: DAWN, text: 'I\'ve taken my shutter down. I\'m going to plant something under that garden lamp. Something that likes the light.' },
  ],
  'script.still_hall_reader': [
    { op: 'say', speaker: 'ACOLYTE', unless_flag: DAWN, text: 'Supper\'s at the long table, when there is supper. We eat in the dark and talk about the people we\'ve lost. It helps more than you\'d think. It helps less than we pretend.' },
    { op: 'say', speaker: 'ACOLYTE', if_flag: DAWN, text: 'We still eat together. We\'ve just started lighting the table. Everybody looks so much older. And so much kinder.' },
  ],

  // ---- the three who'd rather talk first ---------------------------------------
  'script.still_acolyte_gethin': talkFirst('still_acolyte_gethin', 'GETHIN',
    ['I trained kin for battle, once, in the south. I was good at it. Then I couldn\'t bear watching them get hurt, so I brought mine here, where nothing is asked of them.',
      'They\'re awake, mine. I never put them to sleep. I just let them rest. ...You\'d like to see how they\'ve kept, wouldn\'t you. I can tell.'],
    'One gentle bout? For old times\' sake.',
    'They remembered. Every move. They looked... glad. I hadn\'t thought about whether they missed it.',
    'Of course. Some days talking is the braver thing.'),
  'script.still_acolyte_gethin_after': [
    { op: 'say', speaker: 'GETHIN', unless_flag: DAWN, text: 'I keep thinking about how they looked, after. Like they\'d been waiting for someone to ask.' },
    { op: 'say', speaker: 'GETHIN', if_flag: DAWN, text: 'I\'m going to start a little practice ring again. Gentle bouts only. Children welcome.' },
  ],
  'script.still_acolyte_vesna': talkFirst('still_acolyte_vesna', 'VESNA',
    ['I was a star-watcher at Nightreach. I counted the falls, one column, eleven winters. After a while I couldn\'t look up any more without counting.',
      'Here I don\'t look up at all. It\'s very restful. Do you look up, lamp-bearer? What do you see?'],
    'Show me what you see, then. In the old way.',
    'Bright. That\'s what you see. I\'d forgotten bright.',
    'No? That\'s all right. Look up for me, then, on your way out.'),
  'script.still_acolyte_vesna_after': [
    { op: 'say', speaker: 'VESNA', unless_flag: DAWN, text: 'I looked up last night. Only for a moment. Nothing fell. I counted that as something.' },
    { op: 'say', speaker: 'VESNA', if_flag: DAWN, text: 'I\'ve started a new column. Not falls. Things that came back. It\'s getting long.' },
  ],
  'script.still_lamplighter_grisel': talkFirst('still_lamplighter_grisel', 'GRISEL',
    ['Forty years I lit lamps. Forty years of the same ladder, the same wicks, the same lamps going out by morning. Then one winter they went out and stayed out, and I thought: there. Now I can rest.',
      'Don\'t look at me like that. I\'m not your enemy. I\'m just an old man who\'s very tired. ...Though I\'d like to see whether that lamp of yours burns as bright as they say.'],
    'Will you let an old lamplighter test your light?',
    'Ha. It does. Brighter. You\'ll wear yourself out, carrying that. ...Good. Someone should.',
    'Wise. I\'m a terrible loser. Forty years of practice.'),
  'script.still_lamplighter_grisel_after': [
    { op: 'say', speaker: 'GRISEL', unless_flag: DAWN, text: 'Trim your wick at the third knot, not the second. Old habit. Can\'t help myself.' },
    { op: 'say', speaker: 'GRISEL', if_flag: DAWN, text: 'They\'ve asked me to light the shore lamps. Me. On my knees, I said yes. My knees said no. I went anyway.' },
  ],

  // ---- the inn, the lamp-maker, the homes ----------------------------------------
  'script.still_inn_rest': [
    { op: 'say', speaker: 'INNKEEPER', unless_flag: DAWN, text: 'Welcome to the Shutter. A bed, a bowl of soup, and quiet. We have a great deal of quiet.' },
    { op: 'say', speaker: 'INNKEEPER', if_flag: DAWN, text: 'Welcome to the Shutter. We\'re thinking of changing the name. Suggestions in the jar.' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEPER', text: 'Slept? Good. Sleep\'s the one thing we\'ve always been good at here.' },
  ],
  'script.still_inn_guest': [
    { op: 'say', speaker: 'ACOLYTE', unless_flag: DAWN, text: 'I sit by the hearth with my back to it, the way we\'re meant to. But I can feel it. A fire doesn\'t need you to look at it to keep you warm. I think about that a lot.' },
    { op: 'say', speaker: 'ACOLYTE', if_flag: DAWN, text: 'I turned my chair round. Everyone stared. Then three more people turned theirs.' },
  ],
  'script.still_inn_pilgrim': [
    { op: 'say', speaker: 'TRAVELLER', unless_flag: DAWN, text: 'I only came for the night. That was two winters ago. It\'s very easy to stay somewhere nobody asks anything of you.' },
    { op: 'say', speaker: 'TRAVELLER', if_flag: DAWN, text: 'I\'m leaving in the morning. A real morning. I want to see what it looks like on a road.' },
  ],
  'script.still_lampmaker': [
    { op: 'say', speaker: 'OSRIC', unless_flag: DAWN, text: 'I was a lamplighter, and now I make hoods and shutters. Same hands. Same tools. You\'d be surprised how little a craft cares which way it\'s pointed.' },
    { op: 'say', speaker: 'OSRIC', unless_flag: DAWN, text: 'I sell to travellers too. A hooded lamp lets you pass the wild kin quietly. Balms. A coal or two. Even the bright cells, for the likes of you.' },
    { op: 'say', speaker: 'OSRIC', if_flag: DAWN, text: 'Hoods are going out of fashion. I\'m back to making lamps. My hands knew the way before I did.' },
    { op: 'shop', shop: 'stillwater_lampmaker' },
  ],
  'script.still_lamp_bench': [
    { op: 'say', text: 'A bench of lamp parts: hoods, caps, a half-made shutter. Every hinge has been oiled. Every hood fits its lamp exactly.' },
  ],
  'script.still_home_a_elder': [
    { op: 'say', speaker: 'EDWY', unless_flag: DAWN, text: 'Margery and I came up from the coast when our kin got old. We couldn\'t watch them fade a little more every season. Here they just sleep, and we sit with them.' },
    { op: 'say', speaker: 'EDWY', if_flag: DAWN, text: 'Old Bracken woke up. Our kin, the grey one by the bed. He\'s eleven winters older and he walked straight to the door and asked to go out. So we went out.' },
  ],
  'script.still_home_a_wife': [
    { op: 'say', speaker: 'MARGERY', unless_flag: DAWN, text: 'Would you like some tea? It\'s mostly hot water. We stopped growing the leaves. They wanted too much sun.' },
    { op: 'say', speaker: 'MARGERY', if_flag: DAWN, text: 'I\'ve put seeds in. Tea leaves, by the window. Come back in a year and I\'ll have a proper cup for you.' },
  ],
  'script.still_home_a_basket': [
    { op: 'say', unless_flag: DAWN, text: 'A wide wicker basket by the bed. Old Bracken is asleep in it, grey to the muzzle, a blanket over his haunch. A tag on the handle, in two hands: OURS.' },
    { op: 'say', if_flag: DAWN, text: 'Old Bracken\'s basket, empty and still warm. A trail of grey hairs leads to the door. He\'s out walking.' },
  ],

  // ===========================================================================
  //  COLDFOG — the road north (Part E density)
  // ===========================================================================
  'script.still_trader': [
    { op: 'say', speaker: 'SEFTON', unless_flag: DAWN, text: 'You\'re a long way from a fire. There\'s no inn in the fog. Stillwater\'s just north, through the gap, and they\'ll give you a bed whatever they think of your lamp.' },
    { op: 'say', speaker: 'SEFTON', unless_flag: DAWN, text: 'I carry what the road needs, for anyone who walks it. Balms, a coal, a few charges. The Hollowing don\'t mind. They like the road to be kind.' },
    { op: 'say', speaker: 'SEFTON', if_flag: DAWN, text: 'Business is up. People walk the fog road to look at it now, would you believe. Like visiting a grave that\'s turned out not to be one.' },
    { op: 'shop', shop: 'stillwater_trader' },
  ],
  'script.coldfog_fen_walker': [
    { op: 'say', speaker: 'FEN-WALKER', unless_flag: DAWN, text: 'I walk the edge of the fog every day. Here, where the grass is still green. I tell myself I\'m keeping it from creeping. I\'m not. It doesn\'t creep. It just... waits.' },
    { op: 'say', speaker: 'FEN-WALKER', unless_flag: DAWN, text: 'There\'s a village north, past the fog. Stillwater. My daughter went there. She writes that it\'s peaceful. I read the letters out loud to the reeds.' },
    { op: 'say', speaker: 'FEN-WALKER', if_flag: DAWN, text: 'She came home. Just for a visit. She stood right here and said, "Was it always this green?" No, love. It wasn\'t.' },
  ],
  'script.coldfog_acolyte_north': [
    { op: 'say', speaker: 'ACOLYTE', text: 'Wait. Please. Stillwater is north of here, and the people there are resting. I keep this road so nobody arrives there angry.' },
    { op: 'say', speaker: 'ACOLYTE', text: 'If you\'re angry, spend it on me. I would honestly rather that.' },
    { op: 'battle', trainer: 'coldfog_acolyte_north' },
    { op: 'say', speaker: 'ACOLYTE', text: 'There. You don\'t seem angry at all, actually. Go on, then. Speak softly in the village.' },
    { op: 'setFlag', flag: 'flag:coldfog_acolyte_north_beaten' },
  ],
  'script.coldfog_acolyte_east': [
    { op: 'say', speaker: 'ELDER FENWICK', text: 'East of here are the fallow fields. We quieted them first, before the village. The kin there sleep under the fog like it\'s a blanket.' },
    { op: 'say', speaker: 'ELDER FENWICK', text: 'You\'ll want to wake them, I suppose. Then let me see if you\'re strong enough to be trusted with that.' },
    { op: 'battle', trainer: 'coldfog_acolyte_east' },
    { op: 'say', speaker: 'ELDER FENWICK', text: 'Strong enough. Whether you\'re right is a different question. Go and look at the fields and decide.' },
    { op: 'setFlag', flag: 'flag:coldfog_acolyte_east_beaten' },
  ],
  'script.coldfog_acolyte_deep': [
    { op: 'say', speaker: 'ACOLYTE', text: 'Every lantern on these racks was lit by somebody\'s grandmother. We put each one to sleep with a word and a cloth over the glass. You won\'t see that in the stories about us.' },
    { op: 'battle', trainer: 'coldfog_acolyte_deep' },
    { op: 'say', speaker: 'ACOLYTE', text: 'You fight like someone who has never had to give anything up. I hope you never do.' },
    { op: 'setFlag', flag: 'flag:coldfog_acolyte_deep_beaten' },
  ],
  'script.coldfog_acolyte_west': [
    { op: 'say', speaker: 'ELDER MARROW', text: 'You walked the whole marsh with that lamp held up. It looks heavy.' },
    { op: 'say', speaker: 'ELDER MARROW', text: 'I carried one like it, once. I set it down here and never picked it up again. Let me show you how that felt.' },
    { op: 'battle', trainer: 'coldfog_acolyte_west' },
    { op: 'say', speaker: 'ELDER MARROW', text: '...Hm. You make it look less heavy than I remember.' },
    { op: 'setFlag', flag: 'flag:coldfog_acolyte_west_beaten' },
  ],
  'script.coldfog_camp_mourner': [
    { op: 'say', speaker: 'OLD WOMAN', unless_flag: DAWN, text: 'This was the wardens\' camp. They didn\'t leave in a hurry. They rolled their bedrolls, swept the ash, and walked north to Stillwater one at a time. I was the last. I come back to sit sometimes.' },
    { op: 'say', speaker: 'OLD WOMAN', if_flag: DAWN, text: 'I lit the camp fire this morning. Just to see. It took first time, as if it had been waiting.' },
  ],
  'script.pickup_coldfog_starlight': pickup('flag:picked_coldfog_starlight',
    [{ op: 'giveItem', item: 'hearth_coal', count: 1 }, { op: 'giveItem', item: 'beacon_charge', count: 2 }],
    'Your lamp\'s Starlight finds a nook the fog never let anyone see. A traveller\'s bundle: a HEARTH COAL and two BEACON CHARGES!'),
  'script.pickup_coldfog_deep_starlight': pickup('flag:picked_coldfog_deep_starlight',
    [{ op: 'giveItem', item: 'starglass_shard', count: 1 }],
    'Even here, at Starlight, your lamp pulls a glint out of the reeds: a STARGLASS SHARD, warm as a hand!'),

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
    { op: 'say', speaker: 'LAMPLIGHTER', text: 'Evening! Well, it\'s always evening. I keep this lane lit for the Lantern-car folk. Somebody has to.' },
    { op: 'say', speaker: 'LAMPLIGHTER', unless_flag: DAWN, text: 'If you\'re curious about the Hollowing, there\'s a village of them north of the Coldfog marshes. Stillwater. Walk the fog road north from the near marsh. They won\'t hurt you. They\'ll just look at your lamp like it\'s a sad song.' },
    { op: 'say', speaker: 'LAMPLIGHTER', if_flag: DAWN, text: 'Some of the Stillwater folk came down the lane last week. They asked if they could help me trim the lamps. I said yes. One of them cried. Happy crying, I think.' },
  ],
  'script.nightlane_lamplighter_b': [
    { op: 'say', speaker: 'WICK-TRIMMER', unless_flag: DAWN, text: 'Nightreach first, then the marshes, then the fog road north. My grandmother used to light lamps all the way to a fishing village up there. Stillwater. I\'ve never been. They\'d probably ask me to put my lamp out.' },
    { op: 'say', speaker: 'WICK-TRIMMER', if_flag: DAWN, text: 'I went to Stillwater! They gave me soup and asked me how to trim a wick. I\'m going back next week to teach a class.' },
  ],
  'script.sunvault_climber_ii': [
    { op: 'say', speaker: 'CLIMBER', text: 'Halfway up and my legs are already lodging a complaint. The trick is to look at the next ledge, not the top. The top just laughs at you.' },
  ],
  'script.sunvault_climber_iii': [
    { op: 'say', speaker: 'CLIMBER', text: 'The old sun-keepers built these terraces to catch the last light of every day. You can still feel it in the stone if you put your hand flat on it. Go on. Warm, isn\'t it?' },
  ],
  'script.sunvault_climber_iv': [
    { op: 'say', speaker: 'CLIMBER', text: 'From the top ledge you can see the observatory, and past it the fog where the marshes start. North of the fog there\'s a village nobody visits. My mother went. She sends me a letter every spring that says only "resting".' },
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
    return [{ op: 'say', speaker: 'KEEPER WENNA', text: 'Have you found them yet? The Wayfare Lamp in the near fog, the Market Lamp in the deep fog, and the First Lamp across the water. Read what they left. It\'s the only way I know to explain us.' }];
  }
  const missing = WALL_LAMPS.filter((_, i) => bits[i] === '0');
  const found = 3 - missing.length;
  const head = found === 2 ? 'Two of three. Only one left:' : 'One of three, then. Still to find:';
  return [{ op: 'say', speaker: 'KEEPER WENNA', text: `${head} ${missing.join(', and ')}. Read what was left at its foot, then come back to me.` }];
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
    { text: 'STILLWATER. The weary are welcome. Please speak softly; the kin are sleeping.' },
  ],
  'sign.stillwater_hall': [
    { text: 'THE QUIET HALL. Remembrance on any night. Supper on the darkest. All are welcome to sit with the names.' },
  ],
  'sign.stillwater_mourning': [
    { text: 'SOUTH-EAST: THE FALLOW FIELDS, quieted first. Walk gently; the kin there are dreaming. SOUTH-WEST: the fog road to the marshes.' },
  ],
  'sign.stillwater_waystone': [
    { text: 'A lamp-stone, its little lantern shuttered like every lamp in Stillwater. The Lanternway still knows it: from here the lit road can carry you anywhere you\'ve been.' },
  ],
  'sign.stillwater_inn': [
    { text: 'THE SHUTTER. Beds, soup, quiet. No lamps lit after dusk (it is always after dusk).' },
  ],
  'npc.coldfog_acolyte_north_after': [
    { speaker: 'ACOLYTE', text: 'Stillwater is just through the gap. Tell them Brin sent you, and that I wasn\'t angry either.' },
  ],
  'npc.coldfog_acolyte_east_after': [
    { speaker: 'ELDER FENWICK', text: 'The fallow fields are east. If you wake anything out there, be gentle with it. It\'s been dreaming a long time.' },
  ],
  'npc.coldfog_acolyte_deep_after': [
    { speaker: 'ACOLYTE', text: 'I\'ve started lifting the cloths off the racks. Only to dust the glass. That\'s what I tell myself.' },
  ],
  'npc.coldfog_acolyte_west_after': [
    { speaker: 'ELDER MARROW', text: 'Perhaps I\'ll pick it up again. My lamp. Not today. But I\'ve started thinking about where I left it.' },
  ],
};
