/**
 * THE HOLLOWING'S COUNTRY (2026-10, docs/world/walkthrough/11-the-hollowing-country.md
 * Part B), lane N2 — THE DROWNLIGHT, the first lamp the Hollowing put out. This lane
 * OWNS this file: new scripts + dialogue only, spread into the registries via
 * regions/index.ts.
 *
 * Maps: drownlight_beacon (the foot: the ruined quay + the door), drownlight_f1 (the
 * Oil Stores), drownlight_f2 (the Lens Gallery), drownlight_lantern (the Lantern
 * Room). Builders: tools/maps/build_drownlight_beacon.py, build_drownlight_tower.py.
 *
 * The keeper: MAUDRY KELL, the SHUTTERKEEPER, kept the Drownlight thirty-one winters.
 * Fourteen winters ago (three before the sky went dark — story-bible §12's 20 -> 11
 * window) she banked its lamp low and bolted iron shutters round it: the Hollowing's
 * first. A quiet astronomer sat with her that winter; she tells it as the winter his
 * grief became a way of seeing the world. She never names him, and nobody here names
 * the one he lost. A keeper never kills a lamp, so it still burns behind the iron, and
 * its light still leaks down the tower's old light-wells as the glare the shutter
 * puzzles route. She does NOT relight it when beaten; after the dawn, the player may.
 *
 * Flags this file owns:
 *   flag:drownlight_shutter_1/2 (F1), _a/_b/_c (F2)   the shutter-cranks (thrown = set)
 *   flag:drownlight_shutter_<n>_tmp transient: that crank's previous state, cleared at once
 *   flag:drownlight_entered         first steps inside (the journal + LORE hook)
 *   flag:drownlight_glare_seen      the glare's first explanation has played
 *   flag:drownlight_keeper_hailed   the Shutterkeeper's hail at the stairhead
 *   flag:drownlight_keeper_beaten   the bout (+ her reasons) — she still won't relight it
 *   flag:drownlight_relit           post-dawn: the relight (the foot's lamp + buoys wake)
 *   flag:drownlight_acolyte_<name>_beaten   the three acolytes (sight trainers)
 *   flag:picked_drownlight_shard / _drop    the two caches
 * Reads flag:dawn (the relight waits on it).
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

const DAWN = 'flag:dawn';
const BEATEN = 'flag:drownlight_keeper_beaten';
const RELIT = 'flag:drownlight_relit';
const KEEPER = 'THE SHUTTERKEEPER';

/** A shutter-crank: flips its flag (via a transient copy so the two guarded setFlags
 *  can't both fire) and says where the light went. */
function crank(n: string, name: string, thrown: string, rest: string): CutsceneStep[] {
  const F = `flag:drownlight_shutter_${n}`;
  // a PER-CRANK transient (not one shared TMP): audit_journey replays add-only, so a
  // shared TMP left "held" by one crank would read as stuck in every other crank
  const TMP = `flag:drownlight_shutter_${n}_tmp`;
  return [
    { op: 'setFlag', flag: TMP, if_flag: F },
    { op: 'setFlag', flag: F, unless_flag: TMP },
    { op: 'setFlag', flag: F, value: false, if_flag: TMP },
    { op: 'sfx', key: 'world-door-close' },
    { op: 'shake', ms: 200, intensity: 0.0018 },
    { op: 'narrate', if_flag: F, text: `You lean on ${name}. Somewhere in the walls a louvre swings over with an iron sigh, and the leaked light goes with it: ${thrown} The little pennant on the housing shows RED.` },
    { op: 'narrate', unless_flag: F, text: `You wind ${name} back. The louvre settles home, and the light runs the old way again: ${rest} The pennant shows WHITE.` },
    { op: 'setFlag', flag: TMP, value: false },
  ];
}

/** Walking into the glare: you throw up an arm and step back the way you came. */
function glare(tx: number, ty: number, facing: 'up' | 'down' | 'left' | 'right'): CutsceneStep[] {
  return [
    { op: 'sfx', key: 'world-bump' },
    { op: 'flashColor', color: '#fff4d0', ms: 220 },
    { op: 'narrate', unless_flag: 'flag:drownlight_glare_seen', text: 'Light pours out of the well in the wall: the old lamp\'s light, leaking down the tower. After so long in the dark it is blinding. You throw up an arm and stagger back.' },
    { op: 'narrate', unless_flag: 'flag:drownlight_glare_seen', text: 'Somewhere on this floor a shutter-crank must swing that louvre. Shut it here, and the light will only pour out somewhere else. Each crank wears a pennant: WHITE at rest, RED once thrown.' },
    { op: 'setFlag', flag: 'flag:drownlight_glare_seen' },
    { op: 'move', actor: 'player', to: { tx, ty } },
    { op: 'face', actor: 'player', facing },
  ];
}

function find(flag: string, gives: CutsceneStep[], text: string): CutsceneStep[] {
  return [{ op: 'sfx', key: 'world-pickup' }, ...gives, { op: 'say', text }, { op: 'setFlag', flag }];
}

function acolyte(id: string, name: string, before: string, after: string): CutsceneStep[] {
  return [
    { op: 'emote', actor: id, emote: 'alert' },
    { op: 'say', speaker: name, text: before },
    { op: 'battle', trainer: id },
    { op: 'say', speaker: name, text: after },
    { op: 'setFlag', flag: `flag:${id}_beaten` },
  ];
}

/** The relight itself (post-dawn; the minor -> major lamp beat. No Gleam: this
 *  is a coast's lamp, not a star). */
const RELIGHT: CutsceneStep[] = [
  { op: 'letterbox', on: true },
  { op: 'silence', ms: 1000 },
  { op: 'say', speaker: KEEPER, text: 'Well. Go on, then. It\'s heavier than it looks. Fourteen winters will do that to a crank.' },
  { op: 'narrate', text: 'You set your hands on the great crank. After a moment, hers come down beside yours, cold and certain. Together you lean.' },
  { op: 'sfx', key: 'world-door-close' },
  { op: 'shake', ms: 500, intensity: 0.003 },
  { op: 'narrate', text: 'The first shutter folds back with a groan the whole tower feels. A blade of gold falls across the floor. Then the second, and the third, and the iron leaves open one after another like a hand uncurling.' },
  { op: 'tint', color: '#ffd890', alpha: 0.28, ms: 800 },
  { op: 'sfx', key: 'world-lantern-light' },
  { op: 'setFlag', flag: RELIT },
  { op: 'flashColor', color: '#fff2c8', ms: 520 },
  { op: 'musicCrossfade', key: 'drownlight-relit', ms: 1300 },
  { op: 'narrate', text: 'THE DROWNLIGHT BURNS. Its beam swings out over the dead shallows and the coldfog, the first light on this coast in fourteen winters, and the fog does what fog has always done in front of a lamp: it gives way.' },
  { op: 'narrate', text: 'Out on the water the old buoys answer, one after another, their little lamps waking down the coast the way they used to.' },
  { op: 'tint', color: '#ffd890', alpha: 0, ms: 1200 },
  { op: 'say', speaker: KEEPER, text: '...I\'d forgotten it was warm. All those winters keeping it, and I\'d forgotten it was warm.' },
  { op: 'say', speaker: KEEPER, text: 'It isn\'t a promise this time, is it. Not one lamp alone, lying to the sea. It\'s one of a great many. That I can keep.' },
  { op: 'say', speaker: KEEPER, text: 'Here. The first shutter\'s own latch. I worked it off the night I bolted her, and I\'ve carried it every winter since. I meant to throw it in the sea. I\'m glad I didn\'t.' },
  { op: 'sfx', key: 'world-keyitem' },
  { op: 'giveItem', item: 'shutter_charm', count: 1 },
  { op: 'narrate', text: 'She presses the SHUTTER CHARM into your hand: a little iron latch, warm from the lamp. It is not the kind of thing you use up.' },
  { op: 'say', speaker: KEEPER, text: 'For the kin who love the dark. Not every kin wants waking, apprentice. A light that\'s gentle with them, that comes to them where they are, they\'ll follow it home. That\'s the kind of light I mean to keep now.' },
  { op: 'letterbox', on: false },
];

/** Her post-dawn stage when the lamp is still shuttered: she asks; you may decline.
 *  Only ever reached once she's BEATEN (the lamp's own offer is guarded on it), so
 *  her "where I said" always follows a talk that happened. */
const RELIGHT_OFFER: CutsceneStep[] = [
  { op: 'say', speaker: KEEPER, text: 'You came back. And look at that sky. I sat at that window and watched it go pink, and I didn\'t know what to do with my hands.' },
  { op: 'say', speaker: KEEPER, text: 'The crank\'s where I said it would be. Will you open her up?' },
  { op: 'run', ref: 'script.drownlight_relight_ask' },
];

/** The same ask, straight after her tale on a post-dawn first meeting. */
const RELIGHT_OFFER_NOW: CutsceneStep[] = [
  { op: 'say', speaker: KEEPER, text: 'And you came up here with that sky at your back. I sat at that window and watched it go pink, and I didn\'t know what to do with my hands.' },
  { op: 'say', speaker: KEEPER, text: 'It isn\'t one lamp alone any more, is it. The great crank\'s by the lamp; I\'ve taken the chain off. Will you open her up?' },
  { op: 'run', ref: 'script.drownlight_relight_ask' },
];

const RELIGHT_ASK: CutsceneStep[] = [
  {
    op: 'choice',
    options: [
      { label: 'Open the shutters', ops: [{ op: 'run', ref: 'script.drownlight_relight' }] },
      { label: 'Not yet', ops: [{ op: 'say', speaker: KEEPER, text: 'No. Take your time. It has waited fourteen winters, it can wait for you to be ready.' }] },
    ],
  },
];

export const DROWNLIGHT_SCRIPTS: ScriptRegistry = {
  // ---- the foot -------------------------------------------------------------------
  'script.drownlight_quay': [
    { op: 'narrate', text: 'The keepers\' quay: a run of dressed stone, half drowned in the blight, and steps going down into water that has stopped moving. An iron ring is still set in the wall, polished where a rope used to run.' },
    { op: 'narrate', if_flag: RELIT, text: 'In the lamp\'s sweep the water shows its colour again: grey-green, and very slightly, unmistakably, moving.' },
  ],
  'script.drownlight_buoys': [
    { op: 'narrate', unless_flag: RELIT, text: 'Channel buoys, out on the dead shallows, their little lamps dark. They lean where the last tide left them. Nobody has needed telling where the channel is for a long time.' },
    { op: 'narrate', if_flag: RELIT, text: 'The buoys are lit again, nodding on water that moves. Every time the great beam passes they wink back at it, as if they\'d been waiting to be asked.' },
  ],

  // ---- F1: the Oil Stores --------------------------------------------------------
  'script.drownlight_first_steps': [
    { op: 'narrate', text: 'The door gave easily. Someone oils its hinges. Inside, the Drownlight smells of lamp-oil and cold stone and the sea, and it is very, very quiet.' },
    { op: 'narrate', text: 'High overhead, something is still burning. You can feel it more than see it: a held warmth in the walls, like a hand kept closed round a match.' },
    { op: 'setFlag', flag: 'flag:drownlight_entered' },
  ],
  'script.drownlight_crank_1': crank('1', 'the store crank', 'the glare leaves the stair-room door and floods the door down to the hall.', 'the glare crosses the stair-room door again, and the hall door is dark.'),
  'script.drownlight_crank_2': crank('2', 'the hall crank', 'the glare leaves the door between the store and the stair room and pours into the little nook by the hall.', 'the glare crosses the store\'s far door again, and the nook falls dark.'),
  'script.drownlight_glare_f1_E0': glare(16, 6, 'down'),
  'script.drownlight_glare_f1_E1': glare(16, 9, 'up'),
  'script.drownlight_glare_f1_W0': glare(7, 6, 'down'),
  'script.drownlight_glare_f1_W1': glare(7, 9, 'up'),
  'script.drownlight_glare_f1_N0': glare(9, 4, 'right'),
  'script.drownlight_glare_f1_N1': glare(12, 4, 'left'),
  'script.drownlight_glare_f1_K0': glare(3, 12, 'right'),
  'script.drownlight_glare_f1_K1': glare(6, 12, 'left'),
  'script.drownlight_slate_keepers': [
    { op: 'narrate', text: 'A slate on the wall in a keeper\'s square chalk: the watch rota. Thirty-one winters of it, the oldest names rubbed to ghosts. The last line has only one name on every night of the week.' },
    { op: 'narrate', text: 'Under it, in a different, tidier hand: "Rota discontinued. With thanks for every night. — your friends of the Quiet."' },
  ],
  'script.drownlight_log': [
    { op: 'sfx', key: 'world-chart' },
    { op: 'narrate', text: 'THE DROWNLIGHT LOG, open on the desk, the pen laid neatly across it. The entries run thirty-one winters in one hand: wind, sea, oil burned, boats home. Every night, boats home.' },
    { op: 'narrate', text: 'The last entry is short. "Lamp banked. Shutters bolted. Wick trimmed and left long, as it should be. No boats out. None will be." Then a line ruled under it, very straight.' },
  ],

  // ---- F2: the Lens Gallery ----------------------------------------------------------
  'script.drownlight_crank_a': crank('a', 'the arrival crank', 'the glare leaves the door to the lens store and floods the door down to the east gallery.', 'the glare crosses the lens-store door again, and the east gallery door is dark.'),
  'script.drownlight_crank_b': crank('b', 'the east gallery crank', 'the glare leaves the south gallery door and floods the doorway up from the west gallery to the stair room.', 'the glare crosses the south gallery door again, and the west gallery\'s doorway is dark.'),
  'script.drownlight_crank_c': crank('c', 'the south gallery crank', 'the glare leaves the door between the lens store and the stair room and floods the west gallery\'s door.', 'the glare crosses the stair-room door again, and the west gallery door is dark.'),
  // push tiles mirror build_drownlight_tower.py floor_2()'s door() rows
  'script.drownlight_glare_f2_d0': glare(16, 4, 'right'),
  'script.drownlight_glare_f2_d1': glare(19, 4, 'left'),
  'script.drownlight_glare_f2_e0': glare(6, 4, 'right'),
  'script.drownlight_glare_f2_e1': glare(9, 4, 'left'),
  'script.drownlight_glare_f2_a0': glare(22, 8, 'down'),
  'script.drownlight_glare_f2_a1': glare(22, 11, 'up'),
  'script.drownlight_glare_f2_c0': glare(3, 6, 'down'),
  'script.drownlight_glare_f2_c1': glare(3, 9, 'up'),
  'script.drownlight_glare_f2_b0': glare(17, 14, 'right'),
  'script.drownlight_glare_f2_b1': glare(20, 14, 'left'),
  'script.drownlight_glare_f2_f0': glare(6, 13, 'right'),
  'script.drownlight_glare_f2_f1': glare(9, 13, 'left'),
  // the watch-cot: the tower's rest point (a bed, so it sleeps)
  'script.drownlight_cot': [
    { op: 'narrate', text: 'The keepers\' watch-cot, made up under a grey blanket with the corners folded square. Someone still makes it every morning, though nobody keeps the watch.' },
    { op: 'heal' },
    { op: 'narrate', text: 'You wake to the tower\'s hush and the warmth in the walls. Your kin are rested.' },
  ],
  'script.drownlight_log_two': [
    { op: 'sfx', key: 'world-chart' },
    { op: 'narrate', text: 'The watch-room lectern, and stacked on the shelf under it the old logs, one per winter, the spines dated in white paint. Thirty-one of them. Then a gap where a thirty-second would go, and dust.' },
    { op: 'narrate', text: 'The one on the lectern is open, as if somebody keeps meaning to read it again. Inside the front cover: a pressed sea-pink and a child\'s drawing of this tower with its light on, done in far too much yellow.' },
  ],
  'script.drownlight_slate_shutters': [
    { op: 'narrate', text: 'A slate in the tidy hand: a list of lamps, each with a date and a tick. THE DROWNLIGHT is the first line, fourteen winters back. The list runs on down the slate and onto a second piece of slate tied under it with string.' },
    { op: 'narrate', text: 'Beside the first line, much smaller, in a keeper\'s square chalk: "mine."' },
  ],

  // ---- the Lantern Room: the Shutterkeeper ------------------------------------------
  'script.drownlight_keeper_hail': [
    { op: 'face', actor: 'shutterkeeper', facing: 'up', unless_flag: BEATEN },
    { op: 'say', unless_flag: BEATEN, speaker: KEEPER, text: 'Mind the top step. It\'s the one I never mended. ...Don\'t trouble about the light in the wells. It only leaks. It always did, a little.' },
    { op: 'say', unless_flag: BEATEN, speaker: KEEPER, text: 'You\'ll be the apprentice who\'s been putting the stars back. I wondered when you\'d climb up here. Come over by the lamp, where I can see you.' },
    { op: 'setFlag', flag: 'flag:drownlight_keeper_hailed' },
  ],
  'script.drownlight_keeper': [
    { op: 'face', actor: 'shutterkeeper', facing: 'down' },
    { op: 'say', speaker: KEEPER, text: 'This is the Drownlight. Thirty-one winters I kept it. Trimmed it, fed it, wound the clockwork that turned the lens. I could do it with my eyes shut. Some nights I did.' },
    { op: 'say', speaker: KEEPER, text: 'Fourteen winters ago I banked it low and bolted the shutters round it. Three winters before the sky went dark. This was the first light we put out, apprentice. I put it out myself. Maudry Kell. Some call me the Shutterkeeper, and I let them.' },
    { op: 'say', speaker: KEEPER, text: 'You want to know if I\'ll light it for you. I won\'t. But you\'ve climbed a long way in the dark, and that wants an answer. Show me how you climbed it.' },
    { op: 'battle', trainer: 'drownlight_shutterkeeper' },
    { op: 'say', speaker: KEEPER, text: 'There. That\'s a steady light. I can see why the sky listens to you. Sit a moment. I\'ll tell you why, and you can carry it down with you.' },
    { op: 'silence', ms: 700 },
    { op: 'say', speaker: KEEPER, text: 'My girl rowed the sound for herring. One winter night the fog came in thick as wool, and I stood up here and burned this lamp brighter than I ever had. She saw it. I know she saw it. She was rowing straight for it when the swell took her, a cable\'s length off the quay.' },
    { op: 'say', speaker: KEEPER, text: 'Every winter after, the sea took somebody, and every night I burned the lamp anyway. A light is a promise, apprentice. It says: come home, it\'s safe, someone\'s watching. I couldn\'t keep that promise. I\'d been telling it to the whole coast for thirty years.' },
    { op: 'say', speaker: KEEPER, text: 'Then a man climbed those stairs one winter. A quiet man, a sky-watcher, with a grief in him the size of mine. He didn\'t argue with me. He sat where you\'re sitting and said: what if we stopped promising?' },
    { op: 'say', speaker: KEEPER, text: 'Shutting the lamp wasn\'t his idea. It was mine. He only told me I was allowed. That was the winter his grief turned into a way of seeing the world. I watched it happen, sat right there by the lamp. We both thought it was mercy. Some of us still do.' },
    { op: 'say', speaker: KEEPER, unless_flag: DAWN, text: 'So, no. Not while the sky\'s dark. One light alone on a dark coast is the cruellest promise there is.' },
    { op: 'say', speaker: KEEPER, unless_flag: DAWN, text: 'But if you mean what you\'re doing up there... if the sky ever wakes, and it isn\'t one lamp alone any more, come back up and ask me again. I\'ll leave the crank where you can reach it.' },
    { op: 'setFlag', flag: BEATEN },
    // RELIT can't be held here (the lamp's offer waits on BEATEN, and this script
    // hides once she's beaten); the guard keeps one relight, one gift, regardless
    { op: 'run', ref: 'script.drownlight_relight_offer_now', if_flag: DAWN, unless_flag: RELIT },
  ],
  'script.drownlight_keeper_after': [
    { op: 'face', actor: 'shutterkeeper_after', facing: 'down' },
    { op: 'say', speaker: KEEPER, if_flag: RELIT, text: 'Thirty-one winters, then fourteen dark, and now this. I trim it every evening. I still keep the log, only now I write down who comes home.' },
    { op: 'say', speaker: KEEPER, if_flag: RELIT, text: 'Some of my friends of the Quiet came to the quay to look at it. Nobody said anything. One of them brought a flask. We stood there a long while.' },
    { op: 'say', speaker: KEEPER, unless_flag: DAWN, text: 'The crank isn\'t going anywhere. Neither am I. Go on and do what you\'re doing up there, apprentice. I\'ll be watching the sky. I find I can\'t help it.' },
    { op: 'run', ref: 'script.drownlight_relight_offer', if_flag: DAWN, unless_flag: RELIT },
  ],
  'script.drownlight_relight_offer': RELIGHT_OFFER,
  'script.drownlight_relight_offer_now': RELIGHT_OFFER_NOW,
  'script.drownlight_relight_ask': RELIGHT_ASK,
  'script.drownlight_relight': RELIGHT,
  // THE GREAT LAMP (fix pass B: the relight waits on her tale). Exactly one branch
  // plays: RELIT -> it burns; else unbeaten -> shut (+ "ask her first" once the sky's
  // awake); beaten pre-dawn -> the chain's off, not yet; beaten at dawn -> the offer.
  // A step carries one if + one unless, so the stages nest through `run`s.
  'script.drownlight_lamp': [
    { op: 'narrate', if_flag: RELIT, text: 'The great lamp burns behind its folded shutters, its lens turning on clockwork somebody winds every evening. Warm as a hearth to stand by.' },
    { op: 'run', ref: 'script.drownlight_lamp_dark', unless_flag: RELIT },
  ],
  'script.drownlight_lamp_dark': [
    { op: 'run', ref: 'script.drownlight_lamp_shut', unless_flag: BEATEN },
    { op: 'narrate', if_flag: BEATEN, unless_flag: DAWN, text: 'The chain is off the great crank now, left coiled on the floor. The Shutterkeeper\'s words stay with you: not while the sky\'s dark.' },
    { op: 'run', ref: 'script.drownlight_lamp_offer', if_flag: BEATEN },
  ],
  'script.drownlight_lamp_shut': [
    { op: 'narrate', unless_flag: DAWN, text: 'The great lamp, bolted inside iron shutters. Between the leaves a thread of light still shows, low and patient. A keeper never kills a lamp. Beside it, the great crank is chained to its post.' },
    { op: 'narrate', if_flag: DAWN, text: 'The great lamp, bolted inside iron shutters, a thread of light at the seams. Even with the morning in the glass, the great crank stays chained to its post. Its padlock key hangs at the Shutterkeeper\'s belt, and she is watching you from beside the lamp. It is her lamp. Ask her first.' },
  ],
  'script.drownlight_lamp_offer': [
    { op: 'run', ref: 'script.drownlight_relight_offer', if_flag: DAWN, unless_flag: RELIT },
  ],
  'script.drownlight_slate_lost': [
    { op: 'narrate', text: 'A slate of names in a keeper\'s square chalk. Not the watch rota: the lost. Thirty-one winters of them, one or two a year, each with the name of a boat beside it.' },
    { op: 'narrate', text: 'The chalk has been kept fresh. Every name has been gone over again and again, carefully, by the same hand.' },
    { op: 'narrate', if_flag: RELIT, text: 'At the bottom, in new chalk, someone has begun a second column. It is headed HOME, and it already has three names in it.' },
  ],
  'script.drownlight_pane': [
    { op: 'narrate', unless_flag: DAWN, text: 'Storm-glass, salted white at the corners. Outside: coldfog, the dead shallows, and far off the dark mass of the mountain. No stars this side of the sky.' },
    { op: 'narrate', if_flag: DAWN, text: 'Through the salted glass, the sky over the mountain has a morning in it. The coldfog is thinning off the shallows like breath off a cup.' },
  ],

  // ---- the acolytes ------------------------------------------------------------------
  'script.drownlight_acolyte_odell': acolyte('drownlight_acolyte_odell', 'ODELL',
    'Shh. You\'ll wake the kin. ...Oh, it\'s you. The lamp-tender\'s apprentice. Maudry said you might come. She asked us to see what you\'re made of, gently.',
    'Gently, I said. You don\'t do anything gently, do you? Go on up. She\'s at the top. She always is.'),
  'script.drownlight_acolyte_prue': acolyte('drownlight_acolyte_prue', 'PRUE',
    'I sit with the shutters. Somebody has to, or Maudry would do it all herself, and she\'s not young. Will you have a bout before you go turning them?',
    'Turn them how you like. They swing back. Everything swings back, in the end. That\'s what I used to find comforting.'),
  'script.drownlight_acolyte_hask': acolyte('drownlight_acolyte_hask', 'HASK',
    'You\'re climbing toward her. I can tell by your face. Everyone climbs toward her with that face. Let me stand in the way a moment. It\'s what I\'m for.',
    'She told me once she wished someone would come up those stairs and argue with her properly. I think she\'s been waiting for you.'),

  // ---- the caches ----------------------------------------------------------------
  'script.pickup_drownlight_shard': find('flag:picked_drownlight_shard', [{ op: 'giveItem', item: 'starglass_shard', count: 1 }],
    'In a wick-tin in the nook, wrapped in oilcloth: a STARGLASS SHARD, a warm fall from long before the Dusk. Somebody here kept it for luck, and then stopped believing in luck.'),
  'script.pickup_drownlight_drop': find('flag:picked_drownlight_drop', [{ op: 'giveItem', item: 'lumen_drop', count: 1 }],
    'Tucked behind the oil cistern, a keeper\'s honey-jar with one bead left in the bottom: a LUMEN DROP!'),
};

export const DROWNLIGHT_DIALOGUE: DialogueRegistry = {
  'sign.drownlight_stair_fog': [
    { text: 'Coldfog has pooled in the stairwell, grey and heavy as wet wool. Your flame shrinks to a bead in it. Only a tended ember would push through this.' },
  ],
  'sign.drownlight_wick_shelf': [
    { text: 'Filler-cans with long spouts, for carrying oil up the stair. Every one is labelled in a square hand. The labels are fourteen winters old. The cans have been wiped this week.' },
  ],
  'sign.drownlight_oil_jars': [
    { text: 'An oil cistern, riveted copper, its sight-glass still showing amber halfway up. Enough to keep the Drownlight burning a winter, if anybody wanted it to.' },
  ],
  'sign.drownlight_weights': [
    { text: 'The foot of the weight-shaft. Two chains come down a timber chute in the wall to a cast-iron weight, resting on its block. Wound to the top, it would have turned the great lens all night. It has been resting a long time.' },
  ],
  'sign.drownlight_buoy_repair': [
    { text: 'A channel buoy up on trestles, its red and white stripes fresh-painted, its lamp-cage unbolted and set down beside it. Somebody has been mending it for a sea nobody sails.' },
  ],
  'sign.drownlight_crank_notice': [
    { text: 'An enamel notice in the keepers\' blue: "SHUTTER-CRANKS. Each crank swings one louvre in the light-wells. The light leaves one doorway and floods another; it is never put out, only sent somewhere else."' },
    { text: '"Pennant WHITE: louvre at rest. Pennant RED: louvre thrown. Mind where the light goes, not where it is."' },
  ],
  'sign.drownlight_clockwork': [
    { text: 'The turning-gear: a chain drum, a train of brass wheels, a governor\'s fan on top to keep the turn steady. It turned the great lens once a minute, all night, for thirty-one winters. It is oiled. It is still.' },
  ],
  'sign.drownlight_grind_bench': [
    { text: 'The lens-grinding bench: a treadle wheel, a clamp, a pot of grit gone hard. A blank of glass sits in the clamp, half ground, a keeper\'s thumbprint still on it.' },
  ],
  'sign.drownlight_foghorn': [
    { text: 'The fog-signal: a brass horn on a bellows-box with a hand crank. On a thick night the keepers wound it every half minute, so the boats could steer by ear. The crank is tied down with a neat bow of string.' },
  ],
  'sign.drownlight_lamp_rack': [
    { text: 'The keepers\' hand-lamps on their hooks, each with a name burned into its handle. All of them trimmed, filled and unlit.' },
  ],
  'sign.drownlight_shutter_plate': [
    { text: 'A spare shutter-leaf, hung neatly on a nail. Its paper label reads: "No. 7 — west louvre. Keep oiled. — Q."' },
  ],
  'sign.drownlight_shutter_plate_b': [
    { text: 'A spare shutter-leaf with a label: "For the gallery wells. The light gets out regardless. Let it. It has nowhere to go."' },
  ],
  'sign.drownlight_shutter_plate_c': [
    { text: 'A shutter-leaf, never hung. Its label has been written, crossed out and written again: "spare." "Not needed." "spare."' },
  ],
  'sign.drownlight_stove': [
    { text: 'A stove, banked low and tended, a kettle kept warm on top of it. Whoever lives up this tower comes down here for their tea.' },
  ],
  'sign.drownlight_oil_barrels': [
    { text: 'Oil barrels, bunged and stencilled DROWNLIGHT. Somebody has chalked a tally of winters on the nearest one. The tally stops, and then, in a different hand, it starts again.' },
  ],
  'sign.drownlight_sand_sacks': [
    { text: 'Sandbags, stacked by the door for the spring tides. The sea has not come in here for years. The bags are still kept dry.' },
  ],
  'sign.drownlight_glass_crates': [
    { text: 'Crates packed in straw: spare chimney-glasses, a box of wicks, a lamp-maker\'s mark on every lid. Enough to keep the tower lit a dozen winters. None of them opened.' },
  ],
  'sign.drownlight_mess_table': [
    { text: 'The keepers\' mess table, scrubbed pale. A single candle stands on it in a saucer, lit. The Hollowing don\'t snuff candles. Only lamps that make promises.' },
  ],
  'sign.drownlight_lens_store': [
    { text: 'The great lamp\'s spare lens, alone on its cradle in the round room, ringed like the inside of a shell. Hold your lamp up to it and the whole room fills with little bright ladders.' },
  ],
  'sign.drownlight_watch_bench': [
    { text: 'A long bench under the gallery wall, worn smooth where people sat to wait for boats. There is a cushion at one end, newer than the rest.' },
  ],
  'sign.drownlight_gallery_lens': [
    { text: 'A rack of prism segments, slotted upright like plates in a dresser, each one a curved sliver of the great lens. Light from the wells catches in them and lies on the floor in pale gold ladders.' },
  ],
  'sign.drownlight_keeper_table': [
    { text: 'A small table: one cup, a pot under a knitted cosy, a pair of scissors for trimming wicks, and the Drownlight log open at a fresh page.' },
  ],
  'sign.drownlight_keeper_cot': [
    { text: 'A narrow iron cot with a grey blanket folded square. She sleeps up here by the lamp. Of course she does.' },
  ],
  'sign.drownlight_wick_basket': [
    { text: 'A basket of trimmed wicks, cut to the old length, hundreds of them. A keeper\'s evening habit outlasts the evenings.' },
  ],
  'sign.drownlight_sea_pink': [
    { text: 'A sea-pink in a pot by the stair, watered. It has no business growing in the dark and is doing it anyway.' },
  ],
  'npc.drownlight_acolyte_odell_after': [
    { speaker: 'ODELL', text: 'We keep the floors swept for her. It\'s a kind of praying, sweeping. Mind the cranks. They swing the light, they don\'t stop it.' },
  ],
  'npc.drownlight_acolyte_prue_after': [
    { speaker: 'PRUE', text: 'If you\'re stuck, think about where the light goes, not where it is. Maudry taught me that. She meant something else by it, I think.' },
  ],
  'npc.drownlight_acolyte_hask_after': [
    { speaker: 'HASK', text: 'Fourteen winters I\'ve stood here. I came to be quiet. I don\'t know what I\'ll do if she lights it. Go home, I suppose. I\'ve nearly forgotten where that is.' },
  ],
};
