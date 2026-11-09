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
    { op: 'narrate', if_flag: F, text: `You lean on ${name}. A louvre swings over with an iron sigh: ${thrown} The pennant shows RED.` },
    { op: 'narrate', unless_flag: F, text: `You wind ${name} back. The louvre settles home: ${rest} The pennant shows WHITE.` },
    { op: 'setFlag', flag: TMP, value: false },
  ];
}

/** Walking into the glare: you throw up an arm and step back the way you came. */
function glare(tx: number, ty: number, facing: 'up' | 'down' | 'left' | 'right'): CutsceneStep[] {
  return [
    { op: 'sfx', key: 'world-bump' },
    { op: 'flashColor', color: '#fff4d0', ms: 220 },
    { op: 'narrate', unless_flag: 'flag:drownlight_glare_seen', text: 'Light pours from the well in the wall: the old lamp, leaking down the tower. After so long in the dark it blinds you. You stagger back.' },
    { op: 'narrate', unless_flag: 'flag:drownlight_glare_seen', text: '[[A shutter-crank on this floor]] swings that louvre, but the light only pours out somewhere else. Pennants: [[WHITE at rest, RED thrown]].' },
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
  { op: 'say', speaker: KEEPER, text: 'Well. Go on, then. It\'s heavier than it looks. Fourteen winters will do that.' },
  { op: 'narrate', text: 'You set your hands on the great crank. Hers come down beside yours, cold and certain. Together you lean.' },
  { op: 'sfx', key: 'world-door-close' },
  { op: 'shake', ms: 500, intensity: 0.003 },
  { op: 'narrate', text: 'The first shutter folds back with a groan the whole tower feels. A blade of gold falls across the floor. Then the next, and the next, like a hand uncurling.' },
  { op: 'tint', color: '#ffd890', alpha: 0.28, ms: 800 },
  { op: 'sfx', key: 'world-lantern-light' },
  { op: 'setFlag', flag: RELIT },
  { op: 'flashColor', color: '#fff2c8', ms: 520 },
  { op: 'musicCrossfade', key: 'drownlight-relit', ms: 1300 },
  { op: 'narrate', text: 'THE DROWNLIGHT BURNS. Its beam swings over the dead shallows, the first light on this coast in fourteen winters, and the fog does what fog always does before a lamp: it gives way.' },
  { op: 'narrate', text: 'Out on the water the old buoys answer, their little lamps waking down the coast one by one.' },
  { op: 'tint', color: '#ffd890', alpha: 0, ms: 1200 },
  { op: 'say', speaker: KEEPER, text: '...I\'d forgotten it was warm. All those winters keeping it, and I\'d forgotten it was warm.' },
  { op: 'say', speaker: KEEPER, text: 'It isn\'t one lamp alone this time, lying to the sea. It\'s one of a great many. That promise I can keep.' },
  { op: 'say', speaker: KEEPER, text: 'Here. The first shutter\'s latch. I worked it off the night I bolted her and carried it every winter since. I meant to throw it in the sea. I\'m glad I didn\'t.' },
  { op: 'sfx', key: 'world-keyitem' },
  { op: 'giveItem', item: 'shutter_charm', count: 1 },
  { op: 'narrate', text: 'She presses the SHUTTER CHARM into your hand: an iron latch, warm from the lamp. It never gets used up.' },
  { op: 'say', speaker: KEEPER, text: 'For [[the kin who love the dark]]. Not every kin wants waking, apprentice. A light that meets them gently, where they are, they\'ll follow home. That\'s the light I mean to keep now.' },
  { op: 'letterbox', on: false },
];

/** Her post-dawn stage when the lamp is still shuttered: she asks; you may decline.
 *  Only ever reached once she's BEATEN (the lamp's own offer is guarded on it), so
 *  her "where I said" always follows a talk that happened. */
const RELIGHT_OFFER: CutsceneStep[] = [
  { op: 'say', speaker: KEEPER, text: 'You came back. And look at that sky. I watched it go pink from that window, and didn\'t know what to do with my hands.' },
  { op: 'say', speaker: KEEPER, text: 'The crank\'s where I said it would be. Will you open her up?' },
  { op: 'run', ref: 'script.drownlight_relight_ask' },
];

/** The same ask, straight after her tale on a post-dawn first meeting. */
const RELIGHT_OFFER_NOW: CutsceneStep[] = [
  { op: 'say', speaker: KEEPER, text: 'And you came up with that sky at your back. I watched it go pink from that window, and didn\'t know what to do with my hands.' },
  { op: 'say', speaker: KEEPER, text: 'It isn\'t one lamp alone any more. I\'ve taken the chain off [[the great crank]]. Will you open her up?' },
  { op: 'run', ref: 'script.drownlight_relight_ask' },
];

const RELIGHT_ASK: CutsceneStep[] = [
  {
    op: 'choice',
    options: [
      { label: 'Open the shutters', ops: [{ op: 'run', ref: 'script.drownlight_relight' }] },
      { label: 'Not yet', ops: [{ op: 'say', speaker: KEEPER, text: 'No. Take your time. Fourteen winters it\'s waited; it can wait for you.' }] },
    ],
  },
];

export const DROWNLIGHT_SCRIPTS: ScriptRegistry = {
  // ---- the foot -------------------------------------------------------------------
  'script.drownlight_quay': [
    { op: 'narrate', text: 'The keepers\' quay, half drowned in the blight, its steps going down into water that has stopped moving. The iron mooring ring is still polished where a rope ran.' },
    { op: 'narrate', if_flag: RELIT, text: 'In the lamp\'s sweep the water is grey-green again, and very slightly, unmistakably, moving.' },
  ],
  'script.drownlight_buoys': [
    { op: 'narrate', unless_flag: RELIT, text: 'Channel buoys on the dead shallows, their lamps dark, leaning where the last tide left them. Nobody has needed the channel in a long time.' },
    { op: 'narrate', if_flag: RELIT, text: 'The buoys are lit again, nodding on moving water. Each time the beam passes they wink back, as if waiting to be asked.' },
  ],

  // ---- F1: the Oil Stores --------------------------------------------------------
  'script.drownlight_first_steps': [
    { op: 'narrate', text: 'The door gives easily; someone oils its hinges. Inside, the Drownlight smells of lamp-oil, cold stone and the sea. It is very quiet.' },
    { op: 'narrate', text: 'High overhead, something still burns. You feel it more than see it: a warmth in the walls, like a hand closed round a match.' },
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
    { op: 'narrate', text: 'The watch rota, in a keeper\'s square chalk: thirty-one winters, the oldest names rubbed to ghosts. The last line has one name on every night.' },
    { op: 'narrate', text: 'Under it, in a tidier hand: "Rota discontinued. With thanks for every night. — your friends of the Quiet."' },
  ],
  'script.drownlight_log': [
    { op: 'sfx', key: 'world-chart' },
    { op: 'narrate', text: 'THE DROWNLIGHT LOG: thirty-one winters in one hand. Wind, sea, oil burned, boats home. Every night, boats home.' },
    { op: 'narrate', text: 'The last entry: "Lamp banked. Shutters bolted. Wick trimmed and left long, as it should be. No boats out. None will be." A line ruled under it, very straight.' },
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
    { op: 'narrate', text: 'The keepers\' watch-cot, its grey blanket folded square. Someone still makes it each morning, though nobody keeps the watch.' },
    { op: 'heal' },
    { op: 'narrate', text: 'You wake to the tower\'s hush and the warm walls. Your kin are rested.' },
  ],
  'script.drownlight_log_two': [
    { op: 'sfx', key: 'world-chart' },
    { op: 'narrate', text: 'Under the lectern, the old logs, one per winter, spines dated in white paint. Thirty-one of them. Then a gap where a thirty-second would go, and dust.' },
    { op: 'narrate', text: 'The one on the lectern lies open. Inside the cover: a pressed sea-pink, and a child\'s drawing of this tower lit, in far too much yellow.' },
  ],
  'script.drownlight_slate_shutters': [
    { op: 'narrate', text: 'A slate in the tidy hand: lamps, each with a date and a tick. THE DROWNLIGHT is first, fourteen winters back. The list runs on onto a second slate tied under with string.' },
    { op: 'narrate', text: 'Beside the first line, much smaller, in a keeper\'s square chalk: "mine."' },
  ],

  // ---- the Lantern Room: the Shutterkeeper ------------------------------------------
  'script.drownlight_keeper_hail': [
    { op: 'face', actor: 'shutterkeeper', facing: 'up', unless_flag: BEATEN },
    { op: 'say', unless_flag: BEATEN, speaker: KEEPER, text: 'Mind the top step; I never mended it. ...Don\'t trouble about the light in the wells. It only leaks. It always did.' },
    { op: 'say', unless_flag: BEATEN, speaker: KEEPER, text: 'You\'ll be the apprentice putting the stars back. I wondered when you\'d climb up. [[Come by the lamp]], where I can see you.' },
    { op: 'setFlag', flag: 'flag:drownlight_keeper_hailed' },
  ],
  'script.drownlight_keeper': [
    { op: 'face', actor: 'shutterkeeper', facing: 'down' },
    { op: 'say', speaker: KEEPER, text: 'This is the Drownlight. Thirty-one winters I kept it: trimmed it, fed it, wound the lens. I could do it with my eyes shut. Some nights I did.' },
    { op: 'say', speaker: KEEPER, text: 'Fourteen winters ago, three before the sky went dark, I banked it and bolted the shutters. The first light we put out, apprentice. I did it myself. Maudry Kell. Some call me the Shutterkeeper, and I let them.' },
    { op: 'say', speaker: KEEPER, text: 'You want me to light it. I won\'t. But you\'ve climbed a long way in the dark, and that wants an answer. Show me how you climbed.' },
    { op: 'battle', trainer: 'drownlight_shutterkeeper' },
    { op: 'say', speaker: KEEPER, text: 'There. A steady light. I see why the sky listens to you. Sit. I\'ll tell you why, and you can carry it down with you.' },
    { op: 'silence', ms: 700 },
    { op: 'say', speaker: KEEPER, text: 'My girl rowed the sound for herring. One night the fog came thick as wool, and I burned this lamp brighter than ever. She saw it. I know she did. She was rowing straight for it when the swell took her, a cable\'s length off the quay.' },
    { op: 'say', speaker: KEEPER, text: 'Every winter after, the sea took somebody, and every night I burned the lamp anyway. A light is a promise, apprentice: come home, it\'s safe, someone\'s watching. I\'d told it the whole coast for thirty years, and couldn\'t keep it.' },
    { op: 'say', speaker: KEEPER, text: 'Then a man climbed those stairs one winter. A quiet sky-watcher, with a grief the size of mine. He didn\'t argue. He sat where you\'re sitting and said: what if we stopped promising?' },
    { op: 'say', speaker: KEEPER, text: 'Shutting the lamp was my idea. He only told me I was allowed. That was the winter his grief became a way of seeing the world. I watched it happen, right there by the lamp. We both thought it was mercy. Some of us still do.' },
    { op: 'say', speaker: KEEPER, unless_flag: DAWN, text: 'So, no. Not while the sky\'s dark. One light alone on a dark coast is the cruellest promise of all.' },
    { op: 'say', speaker: KEEPER, unless_flag: DAWN, text: 'But if you mean what you\'re doing up there... [[if the sky ever wakes]], come back and ask me again. I\'ll leave the crank where you can reach it.' },
    { op: 'setFlag', flag: BEATEN },
    // RELIT can't be held here (the lamp's offer waits on BEATEN, and this script
    // hides once she's beaten); the guard keeps one relight, one gift, regardless
    { op: 'run', ref: 'script.drownlight_relight_offer_now', if_flag: DAWN, unless_flag: RELIT },
  ],
  'script.drownlight_keeper_after': [
    { op: 'face', actor: 'shutterkeeper_after', facing: 'down' },
    { op: 'say', speaker: KEEPER, if_flag: RELIT, text: 'Thirty-one winters, fourteen dark, and now this. I trim it every evening, and the log says who comes home.' },
    { op: 'say', speaker: KEEPER, if_flag: RELIT, text: 'Some of my friends of the Quiet came to the quay to look. Nobody spoke. One brought a flask. We stood a long while.' },
    { op: 'say', speaker: KEEPER, unless_flag: DAWN, text: 'The crank isn\'t going anywhere. Nor am I. Go and do what you\'re doing up there, apprentice. I\'ll be watching the sky. I can\'t help it.' },
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
    { op: 'narrate', if_flag: RELIT, text: 'The great lamp burns behind its folded shutters, its lens turning. Warm as a hearth to stand by.' },
    { op: 'run', ref: 'script.drownlight_lamp_dark', unless_flag: RELIT },
  ],
  'script.drownlight_lamp_dark': [
    { op: 'run', ref: 'script.drownlight_lamp_shut', unless_flag: BEATEN },
    { op: 'narrate', if_flag: BEATEN, unless_flag: DAWN, text: 'The chain lies coiled off the great crank. Her words stay with you: [[not while the sky\'s dark]].' },
    { op: 'run', ref: 'script.drownlight_lamp_offer', if_flag: BEATEN },
  ],
  'script.drownlight_lamp_shut': [
    { op: 'narrate', unless_flag: DAWN, text: 'The great lamp, bolted in iron shutters, a thread of light still showing, low and patient. A keeper never kills a lamp. The great crank is chained to its post.' },
    { op: 'narrate', if_flag: DAWN, text: 'The great lamp, bolted in iron, light at the seams. Even with morning in the glass, the crank stays chained; the key hangs at the Shutterkeeper\'s belt. It is her lamp. [[Ask her first]].' },
  ],
  'script.drownlight_lamp_offer': [
    { op: 'run', ref: 'script.drownlight_relight_offer', if_flag: DAWN, unless_flag: RELIT },
  ],
  'script.drownlight_slate_lost': [
    { op: 'narrate', text: 'A slate of names in square chalk. Not the rota: the lost. One or two a year for thirty-one winters, each beside a boat\'s name.' },
    { op: 'narrate', text: 'The chalk is kept fresh, every name gone over again and again by the same hand.' },
    { op: 'narrate', if_flag: RELIT, text: 'At the bottom, in new chalk, a second column: HOME. It already has three names.' },
  ],
  'script.drownlight_pane': [
    { op: 'narrate', unless_flag: DAWN, text: 'Storm-glass, salted white. Outside: coldfog, the dead shallows, the dark mass of the mountain. No stars this side of the sky.' },
    { op: 'narrate', if_flag: DAWN, text: 'Through the salted glass, the sky has a morning in it. The fog thins off the shallows like breath off a cup.' },
  ],

  // ---- the acolytes ------------------------------------------------------------------
  'script.drownlight_acolyte_odell': acolyte('drownlight_acolyte_odell', 'ODELL',
    'Shh. You\'ll wake the kin. ...Oh, the lamp-tender\'s apprentice. Maudry said you might come. She asked us to test you, gently.',
    'Gently, I said. You don\'t do anything gently, do you? Go on up. She\'s at the top. She always is.'),
  'script.drownlight_acolyte_prue': acolyte('drownlight_acolyte_prue', 'PRUE',
    'I sit with the shutters, or Maudry would do it all herself, and she\'s not young. A bout before you go turning them?',
    'Turn them how you like. Everything swings back in the end. That used to comfort me.'),
  'script.drownlight_acolyte_hask': acolyte('drownlight_acolyte_hask', 'HASK',
    'You\'re climbing toward her. Everyone does, with that face. Let me stand in the way a moment. It\'s what I\'m for.',
    'She once wished someone would climb those stairs and argue with her properly. I think she\'s been waiting for you.'),

  // ---- the caches ----------------------------------------------------------------
  'script.pickup_drownlight_shard': find('flag:picked_drownlight_shard', [{ op: 'giveItem', item: 'starglass_shard', count: 1 }],
    'In a wick-tin, wrapped in oilcloth: a STARGLASS SHARD, fallen long before the Dusk. Someone kept it for luck, then stopped believing in luck.'),
  'script.pickup_drownlight_drop': find('flag:picked_drownlight_drop', [{ op: 'giveItem', item: 'lumen_drop', count: 1 }],
    'Behind the oil cistern, a honey-jar with one bead left: a LUMEN DROP!'),
};

export const DROWNLIGHT_DIALOGUE: DialogueRegistry = {
  'sign.drownlight_stair_fog': [
    { text: 'Coldfog pools in the stairwell, heavy as wet wool. Your flame shrinks to a bead. Only [[a tended ember]] would push through.' },
  ],
  'sign.drownlight_wick_shelf': [
    { text: 'Oil filler-cans, labelled in a square hand fourteen winters ago. Wiped this week.' },
  ],
  'sign.drownlight_oil_jars': [
    { text: 'A copper oil cistern, half full. Enough to burn the Drownlight a winter, if anybody wanted to.' },
  ],
  'sign.drownlight_weights': [
    { text: 'The weight-shaft: two chains down to an iron weight on its block. Wound up, it turned the great lens all night. It has rested a long time.' },
  ],
  'sign.drownlight_buoy_repair': [
    { text: 'A channel buoy on trestles, fresh-painted red and white. Somebody is mending it for a sea nobody sails.' },
  ],
  'sign.drownlight_crank_notice': [
    { text: '"SHUTTER-CRANKS. Each crank swings one louvre. [[The light leaves one doorway and floods another]]; it is never put out, only sent elsewhere."' },
    { text: '"Pennant WHITE: louvre at rest. Pennant RED: louvre thrown. Mind where the light goes, not where it is."' },
  ],
  'sign.drownlight_clockwork': [
    { text: 'The turning-gear: chain drum, brass wheels, a governor\'s fan. It turned the lens all night for thirty-one winters. It is oiled. It is still.' },
  ],
  'sign.drownlight_grind_bench': [
    { text: 'The lens-grinding bench. A blank of glass sits in the clamp, half ground, a thumbprint still on it.' },
  ],
  'sign.drownlight_foghorn': [
    { text: 'The fog-horn, wound every half minute on thick nights so boats could steer by ear. Its crank is tied down with a neat bow of string.' },
  ],
  'sign.drownlight_lamp_rack': [
    { text: 'The keepers\' hand-lamps, each with a name burned in its handle. All trimmed, filled, unlit.' },
  ],
  'sign.drownlight_shutter_plate': [
    { text: 'A spare shutter-leaf on a nail, labelled: "No. 7 — west louvre. Keep oiled. — Q."' },
  ],
  'sign.drownlight_shutter_plate_b': [
    { text: 'A spare shutter-leaf: "For the gallery wells. The light gets out regardless. Let it. It has nowhere to go."' },
  ],
  'sign.drownlight_shutter_plate_c': [
    { text: 'A shutter-leaf, never hung. Its label has been written, crossed out and written again: "spare." "Not needed." "spare."' },
  ],
  'sign.drownlight_stove': [
    { text: 'A stove, banked low, a kettle kept warm on top. Whoever lives up here comes down for tea.' },
  ],
  'sign.drownlight_oil_barrels': [
    { text: 'Oil barrels stencilled DROWNLIGHT, a tally of winters chalked on one. It stops, then starts again in another hand.' },
  ],
  'sign.drownlight_sand_sacks': [
    { text: 'Sandbags for the spring tides. The sea hasn\'t come in for years. The bags are kept dry.' },
  ],
  'sign.drownlight_glass_crates': [
    { text: 'Crates of chimney-glasses and wicks, packed in straw. Enough to light the tower a dozen winters. None opened.' },
  ],
  'sign.drownlight_mess_table': [
    { text: 'The mess table, scrubbed pale. A candle burns in a saucer. The Hollowing don\'t snuff candles. Only lamps that make promises.' },
  ],
  'sign.drownlight_lens_store': [
    { text: 'The spare lens, ringed like the inside of a shell. Hold your lamp to it and the room fills with little bright ladders.' },
  ],
  'sign.drownlight_watch_bench': [
    { text: 'A bench worn smooth by people waiting for boats. A cushion at one end is newer than the rest.' },
  ],
  'sign.drownlight_gallery_lens': [
    { text: 'Prism segments racked like plates in a dresser. Light from the wells lies on the floor through them in pale gold ladders.' },
  ],
  'sign.drownlight_keeper_table': [
    { text: 'One cup, a pot under a knitted cosy, wick scissors, and the log open at a fresh page.' },
  ],
  'sign.drownlight_keeper_cot': [
    { text: 'A narrow iron cot, blanket folded square. She sleeps up here by the lamp. Of course she does.' },
  ],
  'sign.drownlight_wick_basket': [
    { text: 'Hundreds of trimmed wicks, cut to the old length. A keeper\'s habit outlasts the evenings.' },
  ],
  'sign.drownlight_sea_pink': [
    { text: 'A sea-pink in a pot, watered. It has no business growing in the dark, and does anyway.' },
  ],
  'npc.drownlight_acolyte_odell_after': [
    { speaker: 'ODELL', text: 'Sweeping is a kind of praying. Mind the cranks: [[they swing the light, not stop it]].' },
  ],
  'npc.drownlight_acolyte_prue_after': [
    { speaker: 'PRUE', text: 'Stuck? [[Think where the light goes]], not where it is. Maudry taught me that. She meant something else, I think.' },
  ],
  'npc.drownlight_acolyte_hask_after': [
    { speaker: 'HASK', text: 'Fourteen winters I\'ve stood here, being quiet. If she lights it... go home, I suppose. I\'ve nearly forgotten where that is.' },
  ],
};
