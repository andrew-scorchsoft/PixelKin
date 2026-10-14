/**
 * THE FARLAMP ISLES (docs/world/walkthrough/10-the-farlamp-isles.md, Part I) —
 * the surface: Lightkeeper's Point's seed + launch, the five driftletters, the
 * sea maps, Gullwrack + Kelpcrown, and Driftholm. (The Undertide, the Drowned
 * Lamp, Farlume and the relight are content/regions/undertide.ts.)
 * This lane OWNS this file: new scripts + dialogue only, spread into the
 * registries via regions/index.ts (a ref here must be NEW, never an override).
 *
 * Flags this file sets:
 *   flag:isles_rumour            first talk with Ione / a look through the glass
 *   flag:driftletter_1..5        a driftletter picked up (flag:driftletters_3 DERIVES
 *                                in FlagStore from three of them — never set it)
 *   flag:q_isles                 I1: Ione asks for the prow-lamp (needs flag:dawn + 3 letters)
 *   flag:q_isles_prow_lit        I2: Fenn lights it at Dawnstead
 *   flag:q_isles_afloat          I3: the Farlamp skiff (item + the `deepdive` ability)
 *   flag:q_isles_driftholm       I5: you've landed at Driftholm
 *   flag:q_isles_wellstair       I5: Nan Creel opens the well-stair
 *   flag:isles_letter_home_1..5  "Letters Home": a letter read back to its writer
 *   flag:q_isles_letters_done    all five home (Nan's gift)
 *   flag:isles_keeper_beaten     Bram Fathom, the isles' keeper (coda)
 *   flag:<trainer>_beaten        the two boat-trainers
 *   flag:picked_<cache>          the isles' caches
 * Read here, set by Lane C2 (undertide.ts): flag:q_isles_fogglass, flag:isles_dawn.
 *
 * Voice: cosy, a little melancholy, lanterns in the dark. The Star-tender's old
 * ladder-mate is never named here (the Senna thread is post-dawn and Fenn's own).
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

const DAWN = 'flag:dawn';
const IDAWN = 'flag:isles_dawn';
const RUMOUR = 'flag:isles_rumour';
const L3 = 'flag:driftletters_3';
const Q = 'flag:q_isles';
const PROW = 'flag:q_isles_prow_lit';
const AFLOAT = 'flag:q_isles_afloat';
const ARRIVED = 'flag:q_isles_driftholm';
const WELL = 'flag:q_isles_wellstair';
const KEEPER = 'flag:isles_keeper_beaten';
const LETTERS_DONE = 'flag:q_isles_letters_done';

/** The Letters Home read-backs + plain-line scripts, filled by letterHome() while
 *  FARLAMP_SCRIPTS is built (declared first: it's written to during that build). */
const READS: ScriptRegistry = {};

const letter = (n: number) => `flag:driftletter_${n}`;
const home = (n: number) => `flag:isles_letter_home_${n}`;

/** The five coasts, as Ione names them (the panel's clarity fix). */
const COASTS = [
  'the Dimglass strand, south of Pearlmoor;',
  'Gullcry Rock, out past the Dimglass buoys;',
  'the beach at the Wick-Run\'s foot, just west of here;',
  'the Glassmere shallows, out east past the fens;',
  'and the shingle under the Drownlight Beacon, up in the Coldfog marshes.',
];

const pickup = (flag: string, give: CutsceneStep[], text: string): CutsceneStep[] => [
  { op: 'sfx', key: 'world-pickup' },
  ...give,
  { op: 'say', text },
  { op: 'setFlag', flag },
];

/** A driftletter: a bottle that glints on the strand, a letter you can read. */
const driftletter = (n: number, where: string, lines: string[]): CutsceneStep[] => [
  { op: 'sfx', key: 'world-pickup' },
  { op: 'narrate', text: `A stoppered bottle, green glass gone milky with salt, wedged ${where}. There's a letter rolled inside.` },
  ...lines.map((text): CutsceneStep => ({ op: 'narrate', text })),
  { op: 'setFlag', flag: letter(n) },
  { op: 'setFlag', flag: RUMOUR },
  { op: 'say', text: 'You keep the letter. Somebody wrote it hoping it would be found.' },
];

export const FARLAMP_SCRIPTS: ScriptRegistry = {
  // ===========================================================================
  //  LIGHTKEEPER'S POINT — Ione Fathom, the boatwright (seed, I1, I3)
  // ===========================================================================
  // a nested if/else ladder (each level exactly one branch), latest stage first
  'script.ione': [
    { op: 'run', ref: 'script.ione_post_dawn', if_flag: DAWN },
    { op: 'run', ref: 'script.ione_seed', unless_flag: DAWN },
  ],
  'script.ione_post_dawn': [
    { op: 'run', ref: 'script.ione_after', if_flag: AFLOAT },
    { op: 'run', ref: 'script.ione_pre_afloat', unless_flag: AFLOAT },
  ],
  'script.ione_pre_afloat': [
    { op: 'run', ref: 'script.ione_launch', if_flag: PROW },
    { op: 'run', ref: 'script.ione_pre_prow', unless_flag: PROW },
  ],
  'script.ione_pre_prow': [
    { op: 'run', ref: 'script.ione_wait', if_flag: Q },
    { op: 'run', ref: 'script.ione_ask', unless_flag: Q },
  ],
  'script.ione_seed': [
    { op: 'say', speaker: 'IONE', text: 'Mind the shavings. This old girl was the Farlamp\'s lamp-boat once. I\'m giving her new strakes, a plank a winter. I\'ve the winters to spare.' },
    { op: 'say', speaker: 'IONE', text: 'See that bank of fog on the sea, south? There\'s a lamp in it, blinking. Look long enough and you\'ll catch it. That\'s where the Farlamp stood. The far lamp. My brother kept the isles\' light beside it.' },
    { op: 'say', speaker: 'IONE', text: 'It went quiet eleven winters back, the night the dark came down. The deep came up after it, and no boat\'s crossed since. The deep doesn\'t answer to a tide-song.' },
    { op: 'say', speaker: 'IONE', text: 'But bottles still come ashore, now and then. Letters. Keep an eye on the shores, will you? Five of them catch what the current brings:' },
    ...COASTS.map((c): CutsceneStep => ({ op: 'say', speaker: 'IONE', text: c })),
    { op: 'setFlag', flag: RUMOUR },
  ],
  'script.ione_ask': [
    { op: 'run', ref: 'script.ione_letters_needed', unless_flag: L3 },
    { op: 'run', ref: 'script.ione_i1', if_flag: L3 },
  ],
  'script.ione_letters_needed': [
    { op: 'say', speaker: 'IONE', text: 'You did it. The sky\'s lit from here to the mountain. Look at it. ...Everywhere but there.' },
    { op: 'say', speaker: 'IONE', text: 'The fog still sits on the isles like a lid. The sea keeps what it drowned, I think. I can\'t ask anyone to row into that on a hope. Bring me their letters. Three would do. Three, and I\'ll know someone\'s still writing.' },
    { op: 'say', speaker: 'IONE', text: 'Try the five shores:' },
    ...COASTS.map((c): CutsceneStep => ({ op: 'say', speaker: 'IONE', text: c })),
    { op: 'setFlag', flag: RUMOUR },
  ],
  'script.ione_i1': [
    { op: 'say', speaker: 'IONE', text: 'Letters? Show me. ...That\'s Marra Lowe\'s hand. And this is little Lorne Sallow, the lamp-boy. He\'d be a grown man now.' },
    { op: 'emote', actor: 'ione', emote: 'heart' },
    { op: 'say', speaker: 'IONE', text: 'Then they\'re alive. Eleven winters, and they\'re still writing.' },
    { op: 'say', speaker: 'IONE', text: 'Right. She\'s sound enough to float. But the deep won\'t carry a boat into dark it can\'t see through. The old keepers lit their prow-lamps from the Keystar\'s light. Nothing less ever crossed the Fogwall.' },
    { op: 'say', speaker: 'IONE', text: 'There\'s one lamp on the mainland lit from that light. The Star-tender carries it. You\'ll find him at Dawnstead, on the front. Take him the prow-lamp and ask him to light it. Then come back to me.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'narrate', text: 'Ione unhooks a small brass prow-lamp from the hull and puts it in your hands. It\'s cold, and its wick has never been lit.' },
    { op: 'setFlag', flag: Q },
  ],
  'script.ione_wait': [
    { op: 'say', speaker: 'IONE', text: 'Dawnstead, love. The Star-tender, on the front by the sea. Have him light the prow-lamp from his own. I\'ll have her caulked by the time you\'re back.' },
  ],
  'script.ione_launch': [
    { op: 'say', speaker: 'IONE', text: 'Let me see. ...Oh. Oh, look at that. It burns like a little piece of morning.' },
    { op: 'musicFade', ms: 800 },
    { op: 'narrate', text: 'Ione fits the lamp to the prow-post. The flame steadies, and the hull seems to sit up on its trestles, the way a dog lifts its head at a familiar step.' },
    { op: 'say', speaker: 'IONE', text: 'There. The Farlamp skiff. She\'s yours. Row her down the slip and she\'ll carry you over deep water no swimmer could cross. Keep the lamp lit and the deep will let you by.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'farlamp_skiff', count: 1 },
    { op: 'giveAbility', ability: 'deepdive' },
    { op: 'setFlag', flag: AFLOAT },
    { op: 'say', text: 'You got the FARLAMP SKIFF! You can row across deep water now.' },
    { op: 'say', speaker: 'IONE', text: 'South through the Sound, then west by the reefs to the Fogwall. In the fog you\'ll lose the buoys, everyone does. The old keepers read them through a glass. Find one, and you\'ll find Driftholm.' },
    { op: 'say', speaker: 'IONE', text: 'And if you see my brother Bram... tell him I kept his boat.' },
  ],
  'script.ione_after': [
    { op: 'say', speaker: 'IONE', unless_flag: IDAWN, text: 'Still dark out there? The blink\'s still going. Somebody\'s keeping it, whatever it is.' },
    { op: 'say', speaker: 'IONE', if_flag: IDAWN, unless_flag: KEEPER, text: 'The fog\'s gone. I can see the isles from my own trestles. Eleven winters... Go and give Bram a fright on the quay. He\'ll want a battle. He always does.' },
    { op: 'say', speaker: 'IONE', if_flag: KEEPER, text: 'Bram sent word on the first boat over: "beaten by a mainlander, fair and square, don\'t tell anyone." So I\'m telling everyone.' },
  ],
  'script.point_looking_glass': [
    { op: 'say', text: 'A brass looking-glass on a tripod, aimed south across the water. You put your eye to it.' },
    { op: 'narrate', unless_flag: IDAWN, text: 'Grey fog, a wall of it, lying on the sea. Then, deep inside it, a pinprick of light. It glows. It goes out. It glows again.' },
    { op: 'narrate', if_flag: IDAWN, text: 'Open sea, green islands, a little town by a harbour. And on its skerry, the Farlamp, burning steady in the daylight.' },
    { op: 'setFlag', flag: RUMOUR },
  ],

  // ===========================================================================
  //  DAWNSTEAD — I2: Fenn lights the prow-lamp. Each of Fenn's four staged
  //  placements runs its ORIGINAL ref through one of these wrappers; the isles'
  //  beat is offered as a choice only while it's live (q_isles, not prow_lit).
  // ===========================================================================
  'script.fenn_isles_meet': fennWrap('script.fenn_dawnstead'),
  'script.fenn_isles_survey': fennWrap('script.fenn_survey_wait'),
  'script.fenn_isles_done': fennWrap('script.fenn_survey_done'),
  'script.fenn_isles_after': fennWrap('script.fenn_dawnstead_after'),
  // the after-stage was a plain dialogue; a script wrapper for it
  'script.fenn_dawnstead_after': [{ op: 'dialogue', ref: 'npc.fenn_dawnstead_after' }],
  'script.fenn_prow_lamp': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'peace', text: 'A Farlamp prow-lamp. I haven\'t seen one of these since I was younger than you. Where did you... Ione Fathom. Of course.' },
    { op: 'musicFade', ms: 900 },
    { op: 'narrate', text: 'Fenn turns the little lamp over in his hands for a long moment. Then he opens his own old lantern, the one he\'s carried longer than you\'ve been alive, and tips its flame to the dry wick.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'tint', color: '#ffd58a', alpha: 0.18, ms: 700 },
    { op: 'narrate', text: 'It catches. A small, very clear flame.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'This light was filled for a ladder, a long time ago, by someone with steadier hands than mine. It doesn\'t mind being asked again. Light doesn\'t keep, apprentice. It\'s only good for passing on.' },
    { op: 'tint', color: '#ffd58a', alpha: 0, ms: 700 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'Go on. Ione will be pacing a groove in that headland.' },
    { op: 'setFlag', flag: PROW },
  ],

  // ===========================================================================
  //  THE FIVE DRIFTLETTERS (placed through tools/maps/hand_placed_data.py)
  // ===========================================================================
  'script.pickup_driftletter_1': driftletter(1, 'between two rocks on the strand', [
    '"Ama, if this finds you, the kelp still comes in thick, though the fog hasn\'t lifted in a year now. We dry it on the racks by lamplight.',
    'Keep a lamp in your window on the quay, the way Mam did. If I can\'t see it, I\'ll know it\'s there. Your sister, Marra Lowe, Driftholm."',
  ]),
  'script.pickup_driftletter_2': driftletter(2, 'in a crack of the high stone', [
    '"To whoever keeps the Point\'s light. Some nights we see your Old Light from our harbour wall. Ours went under, with the rock it stood on.',
    'I am the lamp-boy now. I trim all twelve lamps on the quay. I am eleven. Please keep yours burning so I know which way the mainland is. Lorne Sallow."',
  ]),
  'script.pickup_driftletter_3': driftletter(3, 'in the wrack at the tideline', [
    '"I am the schoolteacher at Driftholm. These are my pupils, so that somebody outside the fog knows their names:',
    'Wynn Lowe, Petra and Cass Dunnet, Bree Sallow, Ottar Creel, and the Fathom twins, who will not sit still. They are well. They are learning their letters by lamplight. Maudie Brack."',
  ]),
  'script.pickup_driftletter_4': driftletter(4, 'among the reeds at the water\'s edge', [
    '"Kelp bread, the Driftholm way, in case we\'re forgot: a measure of dried kelp, ground fine, two of barley, salt from the pans, warm water, and patience.',
    'Bake it on a hot stone. Eat it with your feet to a fire. Think of us. Hesk Dunnet, net-mender, who has mended every net on this island twice."',
  ]),
  'script.pickup_driftletter_5': driftletter(5, 'in the shingle below the old beacon', [
    '"To the Star-tender\'s house, by the Crossroads. The Farlamp is under the sea. The deep rose the night the dark came, and took the rock and the lamp and the keeper\'s stair.',
    'No boat can cross. If any lamp on the mainland still burns from the Keystar\'s own light, send us a flame. We will keep the small lamps lit until it comes. Nan Creel, elder of Driftholm."',
  ]),

  // ===========================================================================
  //  THE SEA + THE ISLES
  // ===========================================================================
  'script.fogwall_turned': [
    { op: 'musicFade', ms: 600 },
    { op: 'narrate', text: 'The fog closes round the skiff. The nearest buoy goes grey, then goes. You lose the buoys, one by one, and then you lose the blink.' },
    { op: 'narrate', text: 'You row a long time. When the fog thins, the open sea is on your left again, and you\'re back where you came in.' },
    { op: 'say', text: 'If only you had a glass to read the buoys by...' },
    { op: 'travel', map: 'farlamp_fogwall', to: { tx: 29, ty: 7 }, facing: 'left' },
  ],
  'script.sound_oarsman': [
    { op: 'say', speaker: 'CALDER', text: 'A boat! A real boat, with a lamp on it! I\'ve been fishing off this holm in a tub for three winters waiting for one. Show me what\'s in it!' },
    { op: 'battle', trainer: 'sound_oarsman' },
    { op: 'say', speaker: 'CALDER', text: 'Bested by a boat. Fair\'s fair. The reefs west are the Shelfwater: shallow as a puddle in places, so mind your keel.' },
    { op: 'setFlag', flag: 'flag:sound_oarsman_beaten' },
  ],
  'script.shelf_kelper': [
    { op: 'say', speaker: 'ROWAN', text: 'You\'re off the mainland? Then you\'re the first thing to come out of the north in eleven years that isn\'t a gull. Let\'s see your kin, then.' },
    { op: 'battle', trainer: 'shelf_kelper' },
    { op: 'say', speaker: 'ROWAN', text: 'Good. You\'ll want to be good where you\'re going. The fog west eats boats. The keepers used to read the buoys through some sort of glass.' },
    { op: 'setFlag', flag: 'flag:shelf_kelper_beaten' },
  ],
  'script.pickup_sound_stack': pickup('flag:picked_sound_stack',
    [{ op: 'giveItem', item: 'bright_balm', count: 2 }],
    'Tucked under a gannet\'s nest, a keeper\'s oilskin bundle. Found 2 BRIGHT BALMS!'),
  'script.pickup_sound_cove': pickup('flag:picked_sound_cove',
    [{ op: 'giveItem', item: 'hearth_coal', count: 1 }],
    'At the foot of the sea-cliff, a lamp-tender\'s tin, still dry inside. Found a HEARTH COAL!'),
  'script.pickup_shelf_hull': pickup('flag:picked_shelf_hull',
    [{ op: 'giveItem', item: 'hearth_coal', count: 1 }, { op: 'giveMoney', amount: 800 }],
    'In the wrecked lamp-tender\'s stern locker: a sealed coal-box and a purse. Found a HEARTH COAL and 800 WICKS!'),
  'script.pickup_shelf_holm': pickup('flag:picked_shelf_holm',
    [{ op: 'giveItem', item: 'beacon_charge', count: 2 }],
    'Hung on the kelp-rack, a pair of lamp-cells in a net. Found 2 BEACON CHARGES!'),
  'script.pickup_fog_reef': pickup('flag:picked_fog_reef',
    [{ op: 'giveItem', item: 'bright_balm', count: 3 }],
    'Wedged in the rocks, a fog-bound keeper\'s satchel. Found 3 BRIGHT BALMS!'),
  'script.pickup_gull_spur': pickup('flag:picked_gull_spur',
    [{ op: 'giveItem', item: 'beacon_charge', count: 3 }],
    'Under the bent pine, a fisher\'s cache of lamp-cells. Found 3 BEACON CHARGES!'),
  'script.pickup_gull_meadow': pickup('flag:picked_gull_meadow',
    [{ op: 'giveItem', item: 'bright_balm', count: 2 }],
    'In the long sea-grass, a keeper\'s forgotten kit-bag. Found 2 BRIGHT BALMS!'),
  'script.pickup_kelpcrown_purse': pickup('flag:picked_kelpcrown_purse',
    [{ op: 'giveMoney', amount: 2000 }],
    'Behind the old quarter\'s wall, a strongbox the keepers left when the water came. Found 2,000 WICKS!'),
  'script.pickup_kelp_terrace': pickup('flag:picked_kelp_terrace',
    [{ op: 'giveItem', item: 'chart_tempest', count: 1 }],
    'Rolled in oilcloth on the drying rack: a keeper\'s Star-chart. Found the STAR-CHART: TEMPEST!'),
  'script.pickup_kelp_pool': pickup('flag:picked_kelp_pool',
    [{ op: 'giveItem', item: 'beacon_charge', count: 2 }],
    'On the pool\'s little island, a jar of lamp-cells weighted with a stone. Found 2 BEACON CHARGES!'),
  'script.pickup_driftholm_boathouse': pickup('flag:picked_driftholm_boathouse',
    [{ op: 'giveItem', item: 'bright_balm', count: 1 }, { op: 'giveItem', item: 'beacon_charge', count: 1 }],
    'A shipwright\'s chest of spares. Found a BRIGHT BALM and a BEACON CHARGE!'),
  'script.gullwrack_hut_rest': [
    { op: 'say', speaker: 'SORREL', text: 'A visitor! On Gullwrack! Sit down before the gulls take your hat. There\'s a cot and a fire, and the kettle\'s always on.' },
    { op: 'heal' },
    { op: 'say', speaker: 'SORREL', text: 'There. I keep the bothy for anyone who washes up. Eleven winters, and you\'re the first who washed up on purpose.' },
  ],

  // ===========================================================================
  //  DRIFTHOLM
  // ===========================================================================
  'script.driftholm_arrival': [
    { op: 'letterbox', on: true, ms: 400 },
    { op: 'narrate', text: 'Your keel bumps the quay steps. Up and down the harbour, doors open. Lamps come to windows.' },
    { op: 'say', speaker: 'LORNE', text: 'A boat. A BOAT. Out of the fog, with a lamp lit on its prow!' },
    { op: 'say', speaker: 'BRAM', text: '...That\'s the Farlamp\'s lamp-boat. I\'d know her lines anywhere. My sister\'s been patching her for eleven winters, the stubborn old article.' },
    { op: 'emote', actor: 'bram', emote: 'heart' },
    { op: 'say', speaker: 'BRAM', text: 'You\'d best see the elder, mainlander. Nan Creel. Blue door, south of the square. She\'ll want to know who\'s come, and what you\'ve brought.' },
    { op: 'letterbox', on: false, ms: 400 },
    { op: 'setFlag', flag: ARRIVED },
  ],
  'script.creel_well_locked': [
    { op: 'narrate', text: 'The well-head is chained, and the chain sealed with old lamp-wax. Steps are cut into its side, going down into the dark. A tag hangs from the lock: OPEN BY THE ELDER\'S WORD.' },
    { op: 'say', if_flag: ARRIVED, text: 'Nan Creel\'s house is the one with the blue door.' },
  ],
  'script.nan_creel': [
    { op: 'run', ref: 'script.letter_home_5' },
    { op: 'run', ref: 'script.nan_letters_tally' },
    { op: 'run', ref: 'script.nan_after', if_flag: WELL },
    { op: 'run', ref: 'script.nan_wellstair', unless_flag: WELL },
  ],
  'script.nan_wellstair': [
    { op: 'say', speaker: 'NAN CREEL', text: 'So you\'re the boat. Sit, sit. I\'m too old to be surprised standing up.' },
    { op: 'say', speaker: 'NAN CREEL', text: 'The night the dark came, the deep came up a fathom and took the Farlamp\'s rock. The lamp went down still burning. We watched it through the water for a week before it went out. The fog came in after, and never left.' },
    { op: 'say', speaker: 'NAN CREEL', text: 'The old keepers cut a stair down from our well to the sea-caves under the isles. The Undertide. It runs all the way out to the lamp\'s rock. We sealed it when the water rose. Nobody had the light to go down.' },
    { op: 'say', speaker: 'NAN CREEL', text: 'You have. I can see it on you. Here.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'narrate', text: 'She presses a heavy iron key into your hand, worn smooth.' },
    { op: 'say', speaker: 'NAN CREEL', text: 'Mind the bells down there. The keepers tuned the tides with them. And if the Farlamp can be lit again... light it. We\'d like to see the morning too.' },
    { op: 'setFlag', flag: ARRIVED },
    { op: 'setFlag', flag: WELL },
  ],
  'script.nan_after': [
    { op: 'say', speaker: 'NAN CREEL', unless_flag: IDAWN, text: 'The well-stair\'s open. Down, and out under the sea. Take a light you trust.' },
    { op: 'say', speaker: 'NAN CREEL', if_flag: IDAWN, text: 'Look at it out there. Morning on the water. I\'d forgotten it moved like that.' },
  ],
  // the Letters Home tally: nested guards = "all five home", then Nan's gift once
  'script.nan_letters_tally': [{ op: 'run', ref: 'script.nan_tally_2', if_flag: home(1) }],
  'script.nan_tally_2': [{ op: 'run', ref: 'script.nan_tally_3', if_flag: home(2) }],
  'script.nan_tally_3': [{ op: 'run', ref: 'script.nan_tally_4', if_flag: home(3) }],
  'script.nan_tally_4': [{ op: 'run', ref: 'script.nan_tally_5', if_flag: home(4) }],
  'script.nan_tally_5': [{ op: 'run', ref: 'script.nan_letters_gift', if_flag: home(5), unless_flag: LETTERS_DONE }],
  'script.nan_letters_gift': [
    { op: 'say', speaker: 'NAN CREEL', text: 'All five letters home. Every one we threw, and you brought them back. Do you know, the whole island\'s been talking about nothing else?' },
    { op: 'say', speaker: 'NAN CREEL', text: 'Take these. The chandlery minted them for the deep, and the first ones go to the one who brought our words home.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'deep_charm', count: 3 },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'You got 3 DEEP CHARMS and a LUMEN DROP!' },
    { op: 'setFlag', flag: LETTERS_DONE },
  ],

  // ---- Letters Home: each writer reads her or his own letter back ------------
  'script.letter_home_1': letterHome(1, 'MARRA', [
    'That\'s... that\'s my letter to Ama. You found it. On the Dimglass strand? Then the current runs north after all. I always said it did.',
    'Here. Kelp-wrapped, the way we pack them for the long boats.',
  ], [{ op: 'giveItem', item: 'bright_balm', count: 2 }], 'You got 2 BRIGHT BALMS!', [
    { unless: IDAWN, text: 'We dry the kelp by lamplight now. Eleven winters of lamplight. It comes out grey, but it keeps.' },
    { if: IDAWN, text: 'Kelp in the sun! It dries green again. I\'d forgotten it was ever green.' },
  ], [
    { text: 'If you ever row past Pearlmoor, look for a lamp in a quay window. That\'s my sister. Ama.' },
  ]),
  'script.letter_home_2': letterHome(2, 'LORNE', [
    'Oh, no. Is that the one I wrote to the Point? I was ELEVEN. I spelled "lighthouse" with two H\'s. Don\'t look at it.',
    '...You found it on Gullcry Rock. Then somebody on the mainland might have seen our lamps after all. Here, have the good lamp-cells. I\'ve kept them for best.',
  ], [{ op: 'giveItem', item: 'beacon_charge', count: 3 }], 'You got 3 BEACON CHARGES!', [
    { unless: IDAWN, text: 'Twelve lamps on the quay, and I trim every one, every night. Somebody has to, until the big one\'s lit.' },
    { if: IDAWN, text: 'I trimmed the lamps this morning out of habit and then just stood there. They\'re not needed. Nan says that\'s the best kind of lamp.' },
  ], [
    { text: 'Your Old Light on the Point, the one we could see? Tell whoever keeps it that a lamp-boy said thank you.' },
  ]),
  'script.letter_home_3': letterHome(3, 'MAUDIE', [
    'My register. You found my register! Wynn, Petra, Cass, Bree, Ottar, the twins... someone out there knew their names all this time.',
    'They\'re great lumps now, the lot of them. Please take this. A teacher\'s salary is mostly coal.',
  ], [{ op: 'giveItem', item: 'hearth_coal', count: 1 }], 'You got a HEARTH COAL!', [
    { unless: IDAWN, text: 'We do our letters by lamplight. Ottar asked me once what the sun looked like, and I had to draw it on a slate.' },
    { if: IDAWN, text: 'School is cancelled. Nobody can sit still. I can\'t sit still. Look at the SEA.' },
  ], [
    { text: 'Ottar wants to be a lamp-keeper. Bram says he\'s too short. Bram said that about me too.' },
  ]),
  'script.letter_home_4': letterHome(4, 'HESK', [
    'My kelp bread! The Glassmere? Inland? Then it went round the whole coast and up the fen. That bottle\'s seen more of Vesperholm than I have.',
    'Here. A mender gets paid in odd coin, but it all spends.',
  ], [{ op: 'giveMoney', amount: 1500 }], 'You got 1,500 WICKS!', [
    { unless: IDAWN, text: 'Every net on Driftholm\'s been mended twice. Some of them three times. There\'s been nowhere to fish but the harbour.' },
    { if: IDAWN, text: 'The boats are going out! The nets are going to tear on real fish. I\'ve never been so pleased about anything in my life.' },
  ], [
    { text: 'Did you try the bread? Hot stone, feet to the fire. It\'s the fire that makes it.' },
  ]),
  'script.letter_home_5': [
    { op: 'run', ref: 'script.letter_home_5_read', if_flag: letter(5), unless_flag: home(5) },
  ],
  'script.letter_home_5_read': [
    { op: 'say', speaker: 'NAN CREEL', text: 'My own hand. "Send us a flame." I wrote that on the worst night of the first winter, and threw it as far as these arms would throw.' },
    { op: 'say', speaker: 'NAN CREEL', text: 'And here you are, with the flame. Well. Some letters take their time.' },
    { op: 'setFlag', flag: home(5) },
  ],

  // ---- the bell-ringers' child (Lane C2's "Tide-bell Tuning": the skipping rhyme
  // is the puzzle's hint; once the Bell Galleries are tuned she thanks you — the
  // Lumen Drop is in the ringers' tin down there, so no second prize up here) ----
  'script.driftholm_child': [
    { op: 'say', speaker: 'OTTAR', unless_flag: 'flag:q_isles_bells_tuned', text: 'Mam says I\'m not to go past the quay lamps. She says the fog has teeth. Has it got teeth?' },
    { op: 'say', speaker: 'OTTAR', unless_flag: 'flag:q_isles_bells_tuned', text: 'We skip to the old bells. "Deep calls, shoal answers, harbour brings them home!" Nobody\'s heard them ring in AGES.' },
    { op: 'say', speaker: 'OTTAR', if_flag: 'flag:q_isles_bells_tuned', text: 'It was YOU! We heard the bells come up the well, deep and shoal and harbour, just like the rhyme. Gran cried. Thank you!' },
  ],
  'script.driftholm_child_day': [
    { op: 'say', speaker: 'OTTAR', text: 'I can see ALL the way to the mainland! There\'s a lighthouse! And it\'s got a big brass face on it!' },
    { op: 'say', speaker: 'OTTAR', if_flag: 'flag:q_isles_bells_tuned', text: 'And the bells! Did you hear the bells this morning? Deep, shoal, harbour!' },
  ],

  // ---- Driftholm's counter, inn and keeper -----------------------------------
  'script.driftholm_chandler': [
    { op: 'say', speaker: 'TESS CREEL', unless_flag: IDAWN, text: 'Creel and Daughter. I\'m the daughter. Mam\'s the elder, so the chandlery\'s mine. Balms, coals, lamp-cells. We\'ve plenty of lamp-cells.' },
    { op: 'say', speaker: 'TESS CREEL', if_flag: IDAWN, text: 'Morning! Look at me, saying morning. New on the shelf: Deep Charms. A lamp-cell steeped in sea-light. Over open deep water it\'s worth three of anything else.' },
    { op: 'shop', shop: 'driftholm_chandlery' },
  ],
  'script.driftholm_inn_rest': [
    { op: 'say', speaker: 'INNKEEPER', text: 'The Lamplighters\' Rest! There\'s a bed, a fire and a pot of kelp broth. You look like you need all three.' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEPER', unless_flag: IDAWN, text: 'Slept well? Good. The fog\'s still out there, but it can wait till you\'ve had your breakfast.' },
    { op: 'say', speaker: 'INNKEEPER', if_flag: IDAWN, text: 'Slept well? Sun\'s up. I keep saying it to people. Sun\'s up!' },
  ],
  'script.bram_fathom': [
    { op: 'run', ref: 'script.bram_rematch', if_flag: KEEPER },
    { op: 'run', ref: 'script.bram_unbeaten', unless_flag: KEEPER },
  ],
  'script.bram_unbeaten': [
    { op: 'run', ref: 'script.bram_challenge', if_flag: IDAWN },
    { op: 'run', ref: 'script.bram_wait', unless_flag: IDAWN },
  ],
  'script.bram_wait': [
    { op: 'say', speaker: 'BRAM', text: 'Bram Fathom. I kept the isles\' light beside the Farlamp, before the water took it. These days I keep the quay bell and a grudge.' },
    { op: 'say', speaker: 'BRAM', unless_flag: 'flag:isles_dawn', text: 'Old Edda Marrow kept the Farlamp itself. Since the night it went down she sits with her back to the sea and won\'t speak of it. Her log stayed down there with the lamp.' },
    { op: 'say', speaker: 'BRAM', if_flag: 'flag:isles_dawn', text: 'Edda went down the long stair this morning, first time in eleven winters, and came back up asking who\'d been at her log. I had to sit down on the quay.' },
    { op: 'say', speaker: 'BRAM', unless_flag: ARRIVED, text: 'You came over in my sister\'s boat, didn\'t you? Ione. She always said she\'d finish it.' },
    { op: 'say', speaker: 'BRAM', text: 'You want a battle? Not in the dark, mainlander. My kin fight best by a lit lamp. Light the Farlamp, and I\'ll give you the best bout on these isles.' },
  ],
  'script.bram_challenge': [
    { op: 'say', speaker: 'BRAM', text: 'You lit it. You actually lit it. Look at that water, all gold to the horizon.' },
    { op: 'say', speaker: 'BRAM', text: 'Right. A promise is a promise, and I\'ve been saving my best kin for eleven winters. Keeper\'s rules: no quarter, no regrets.' },
    { op: 'battle', trainer: 'bram_fathom' },
    { op: 'say', speaker: 'BRAM', text: 'Ha! Beaten on my own quay, by daylight. Best thing that\'s happened to me in years. Come back whenever you like. I\'ll be training.' },
    { op: 'setFlag', flag: KEEPER },
  ],
  'script.bram_rematch': [
    {
      op: 'choice',
      speaker: 'BRAM',
      prompt: 'Another bout, mainlander?',
      options: [
        {
          label: 'BATTLE',
          ops: [
            { op: 'say', speaker: 'BRAM', text: 'That\'s the spirit. The tide\'s turning, so am I.' },
            { op: 'battle', trainer: 'bram_fathom_rematch' },
            { op: 'say', speaker: 'BRAM', text: 'Again! You\'re worse than the gulls. Same quay, any day.' },
          ],
        },
        { label: 'NOT TODAY', ops: [{ op: 'say', speaker: 'BRAM', text: 'Suit yourself. The bell\'s here when you want me.' }] },
      ],
    },
  ],
};

/** Fenn's wrapper: the original stage runs unless the prow-lamp beat is live,
 *  in which case it's offered first (the choice can still fall through). */
function fennWrap(original: string): CutsceneStep[] {
  // if/else ladder: no isles errand -> the stage; errand live -> offer the lamp;
  // lamp lit -> the stage again
  const asked = `${original}_isles_asked`;
  READS[asked] = [
    { op: 'run', ref: original, if_flag: PROW },
    {
      op: 'choice',
      unless_flag: PROW,
      speaker: 'FENN',
      prompt: 'Fenn looks at the brass lamp in your hands.',
      options: [
        { label: 'THE PROW-LAMP', ops: [{ op: 'run', ref: 'script.fenn_prow_lamp' }] },
        { label: 'SOMETHING ELSE', ops: [{ op: 'run', ref: original }] },
      ],
    },
  ];
  return [
    { op: 'run', ref: original, unless_flag: Q },
    { op: 'run', ref: asked, if_flag: Q },
  ];
}

type Line = { text: string; if?: string; unless?: string };

/** A Letters Home writer: after-line once home; the read-back when you hold
 *  their letter; otherwise their ordinary (night/day) lines. */
function letterHome(n: number, speaker: string, read: string[], give: CutsceneStep[],
  gotText: string, plain: Line[], after: Line[]): CutsceneStep[] {
  const say = (l: Line): CutsceneStep => ({
    op: 'say', speaker, text: l.text,
    ...(l.if ? { if_flag: l.if } : {}), ...(l.unless ? { unless_flag: l.unless } : {}),
  });
  registerRead(n, speaker, read, give, gotText);
  // an if/else ladder: home -> the after-lines; else holding the letter -> the
  // read-back; else the ordinary (night/day) lines
  const pre = `script.letter_home_${n}_pre`;
  READS[pre] = [
    { op: 'run', ref: `script.letter_home_${n}_read`, if_flag: letter(n) },
    ...plainLines(n, plain, say),
  ];
  return [
    ...after.map((l): CutsceneStep => ({ ...say(l), if_flag: home(n) })),
    { op: 'run', ref: pre, unless_flag: home(n) },
  ];
}

function registerRead(n: number, speaker: string, read: string[], give: CutsceneStep[], gotText: string): true {
  READS[`script.letter_home_${n}_read`] = [
    ...read.map((text): CutsceneStep => ({ op: 'say', speaker, text })),
    { op: 'sfx', key: 'world-pickup' },
    ...give,
    { op: 'say', text: gotText },
    { op: 'setFlag', flag: home(n) },
    { op: 'run', ref: 'script.letters_home_hint' },
  ];
  return true;
}

/** Ordinary lines play only while you don't hold the writer's letter. A line
 *  can't carry two `unless` guards, so a day/night line (if/unless isles_dawn)
 *  is nested in a tiny run step guarded on the letter. */
function plainLines(n: number, plain: Line[], say: (l: Line) => CutsceneStep): CutsceneStep[] {
  const ref = `script.letter_home_${n}_plain`;
  READS[ref] = plain.map(say);
  return [{ op: 'run', ref, unless_flag: letter(n) }];
}

Object.assign(FARLAMP_SCRIPTS, READS, {
  'script.letters_home_hint': [
    { op: 'say', if_flag: 'flag:isles_letter_home_5', unless_flag: LETTERS_DONE, text: 'Nan Creel will want to hear the letters are home.' },
  ],
} as ScriptRegistry);

export const FARLAMP_DIALOGUE: DialogueRegistry = {
  'sign.point_slip_end': [
    { text: 'The slip runs down into black water. Past it the sea goes deep, far too deep to swim. Only a boat could cross here.' },
  ],
  'sign.foot_slip_end': [
    { text: 'An old launch slip, its planks green with weed. The deep starts a stone\'s throw out. Only a boat could cross here.' },
  ],
  'sign.farlamp_sound': [
    { text: 'FARLAMP SOUND. The lamp-road to the isles: keep the buoys to port and the Fogwall ahead. (Somebody has scratched underneath: "STILL HERE".)' },
  ],
  'sign.fogwall_warning': [
    { text: 'TURN BACK IF YOU CANNOT SEE THE BUOYS. The keepers\' glass reads the lane. Without it, the fog will walk you in circles till you\'re home again.' },
  ],
  'sign.gullwrack_hut': [
    { text: 'GULLWRACK BOTHY. Fire lit. Kettle on. Knock loud, the gulls are louder.' },
  ],
  'sign.kelpcrown_ruins': [
    { text: 'The old keepers\' quarter. Their names are cut in the lintel, worn almost smooth. Kelp grows in the doorways now.' },
  ],
  'sign.driftholm': [
    { text: 'DRIFTHOLM. Keepers of the Farlamp. Mind the bell.' },
  ],
  'sign.driftholm_waystone': [
    { text: 'A Driftholm lamp-stone, lit and humming. It knows the other waystones of Vesperholm. TRAVEL from the pause menu takes you home from here.' },
  ],
  'sign.driftholm_schoolhouse': [
    { speaker: 'MAUDIE', text: '(Through the door:) School\'s out! Find me in the square, or at the bottom of the lane.' },
  ],
  'sign.driftholm_cottage_marra': [
    { text: 'The door\'s on the latch. Kelp hangs drying from the lintel, and the house smells of salt and smoke.' },
  ],
  'sign.driftholm_cottage_hesk': [
    { text: 'Nets, nets and more nets, heaped against the door. Somebody inside is mending them.' },
  ],
  'sign.driftholm_inn': [
    { text: 'THE LAMPLIGHTERS\' REST. Broth on the fire. Beds by the night or the week. No credit for mainlanders. (There have been no mainlanders.)' },
  ],
  'sign.driftholm_chandlery': [
    { text: 'A board of hooks and floats, ropes priced by the fathom, and a jar marked SPARE WICKS, DON\'T ASK.' },
  ],
  'sign.driftholm_elder_shelf': [
    { text: 'Eleven years of tide-books, one for every winter. The last one is half full.' },
  ],
  'sign.driftholm_boathouse_hull': [
    { text: 'A boat on the stocks, half-built. Its maker stopped the year the fog came in, with nowhere to sail it.' },
  ],
  'sign.gullwrack_hut_log': [
    { text: 'The bothy log. "Day 4,016. Fog. Gulls. Kettle." "Day 4,017. Fog. Gulls. Kettle." The keeper has a steady hand.' },
  ],
  'npc.sound_oarsman_after': [
    { speaker: 'CALDER', text: 'I\'m going to build a boat like yours. With a lamp on it. Twice the size.' },
  ],
  'npc.shelf_kelper_after': [
    { speaker: 'ROWAN', text: 'The kelp on these reefs is the best in the isles. I come out at low water and nobody bothers me. Except you.' },
  ],
  'npc.driftholm_kelper': [
    { text: 'Eleven winters of kelp by lamplight. You get so you can tell the good fronds by feel.' },
  ],
  'npc.driftholm_cat': [
    { text: 'The cat watches the harbour with enormous patience. It has been waiting for fishing boats for most of its life.' },
  ],
  'npc.driftholm_inn_fisher': [
    { speaker: 'FISHER', text: 'Haven\'t fished past the harbour mouth since the fog came. Too easy to lose your way and row into the deep.' },
  ],
  'npc.driftholm_inn_fisher_day': [
    { speaker: 'FISHER', text: 'Went out past the mouth this morning! Caught nothing at all. Best day\'s fishing of my life.' },
  ],
  'npc.driftholm_apprentice': [
    { speaker: 'APPRENTICE', text: 'Master Fathom started that one before I was born. I\'m going to finish her. Mister Bram says I can, if I learn to plane straight.' },
  ],
};
