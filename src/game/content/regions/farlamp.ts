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
  '[[the Dimglass strand]], south of Pearlmoor;',
  '[[Gullcry Rock]], out past the Dimglass buoys;',
  'the beach at [[the Wick-Run\'s foot]], just west of here;',
  '[[the Glassmere shallows]], east past the fens;',
  'and the shingle under [[the Drownlight Beacon]], up in the Coldfog marshes.',
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
  { op: 'narrate', text: `A stoppered bottle, milky with salt, wedged ${where}. A letter is inside.` },
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
    { op: 'say', speaker: 'IONE', text: 'Mind the shavings. She was the Farlamp\'s lamp-boat once. A new plank a winter. I\'ve the winters to spare.' },
    { op: 'say', speaker: 'IONE', text: 'See the fog on the sea, south? There\'s a lamp in it, blinking. The Farlamp stood there. My brother kept the isles\' light beside it.' },
    { op: 'say', speaker: 'IONE', text: 'It went quiet eleven winters back, the night the dark came. The deep rose after it. No boat\'s crossed since, and the deep won\'t answer a tide-song.' },
    { op: 'say', speaker: 'IONE', text: 'Bottles wash ashore. Letters! [[Watch the shores]] for me? Five catch the current:' },
    ...COASTS.map((c): CutsceneStep => ({ op: 'say', speaker: 'IONE', text: c })),
    { op: 'setFlag', flag: RUMOUR },
  ],
  'script.ione_ask': [
    { op: 'run', ref: 'script.ione_letters_needed', unless_flag: L3 },
    { op: 'run', ref: 'script.ione_i1', if_flag: L3 },
  ],
  'script.ione_letters_needed': [
    { op: 'say', speaker: 'IONE', text: 'You did it. The sky\'s lit to the mountain. ...Everywhere but there.' },
    { op: 'say', speaker: 'IONE', text: 'The fog sits on the isles like a lid. I won\'t row into that on a hope. [[Bring me their letters]]. Three, and I\'ll know they\'re still writing.' },
    { op: 'say', speaker: 'IONE', text: 'Try the five shores:' },
    ...COASTS.map((c): CutsceneStep => ({ op: 'say', speaker: 'IONE', text: c })),
    { op: 'setFlag', flag: RUMOUR },
  ],
  'script.ione_i1': [
    { op: 'say', speaker: 'IONE', text: 'Marra Lowe\'s hand! And Lorne Sallow, the lamp-boy. He\'d be grown now.' },
    { op: 'emote', actor: 'ione', emote: 'heart' },
    { op: 'say', speaker: 'IONE', text: 'Then they\'re alive. Eleven winters, and they\'re still writing.' },
    { op: 'say', speaker: 'IONE', text: 'She\'ll float. But the deep won\'t carry a boat into dark it can\'t see through. The old keepers lit their prow-lamps from the Keystar\'s light.' },
    { op: 'say', speaker: 'IONE', text: 'One lamp on the mainland was lit from that light. [[The Star-tender]] carries it, [[at Dawnstead]] on the front. Have him light the prow-lamp, then come back.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'narrate', text: 'Ione hands you a small brass prow-lamp. Its wick has never been lit.' },
    { op: 'setFlag', flag: Q },
  ],
  'script.ione_wait': [
    { op: 'say', speaker: 'IONE', text: '[[Dawnstead]], love. Have [[the Star-tender]] light the prow-lamp from his own. I\'ll have her caulked by then.' },
  ],
  'script.ione_launch': [
    { op: 'say', speaker: 'IONE', text: 'Let me see. ...Oh. Oh, look at that. It burns like a little piece of morning.' },
    { op: 'musicFade', ms: 800 },
    { op: 'narrate', text: 'Ione fits the lamp to the prow-post. The flame steadies, and the hull seems to lift its head, like a dog at a familiar step.' },
    { op: 'say', speaker: 'IONE', text: 'The Farlamp skiff. She\'s yours. Keep her lamp lit and she\'ll carry you over deep water no swimmer could cross.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'farlamp_skiff', count: 1 },
    { op: 'giveAbility', ability: 'deepdive' },
    { op: 'setFlag', flag: AFLOAT },
    { op: 'say', text: 'You got the FARLAMP SKIFF! You can [[row across deep water]] now.' },
    { op: 'say', speaker: 'IONE', text: '[[South through the Sound]], [[west by the reefs]], to the Fogwall. In the fog you lose the buoys; the keepers read them through a glass. Find one, find Driftholm.' },
    { op: 'say', speaker: 'IONE', text: 'And if you see my brother Bram... tell him I kept his boat.' },
  ],
  'script.ione_after': [
    { op: 'say', speaker: 'IONE', unless_flag: IDAWN, text: 'Still dark out there? The blink\'s still going. Somebody\'s keeping it.' },
    { op: 'say', speaker: 'IONE', if_flag: IDAWN, unless_flag: KEEPER, text: 'Fog\'s gone! Go give [[Bram]] a fright on the quay. He\'ll want a battle. He always does.' },
    { op: 'say', speaker: 'IONE', if_flag: KEEPER, text: 'Bram sent word on the first boat over: "beaten by a mainlander, fair and square, don\'t tell anyone." So I\'m telling everyone.' },
  ],
  'script.point_looking_glass': [
    { op: 'say', text: 'A brass looking-glass on a tripod, aimed south. You put your eye to it.' },
    { op: 'narrate', unless_flag: IDAWN, text: 'Grey fog. Deep inside, a pinprick of light. It glows. It goes out. It glows again.' },
    { op: 'narrate', if_flag: IDAWN, text: 'Open sea, green islands, a harbour town. The watch-light blinks on its rock, and under the water beside it glows the Farlamp, burning where it drowned.' },
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
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'peace', text: 'A Farlamp prow-lamp. I haven\'t seen one since I was a boy. Ione Fathom. Of course.' },
    { op: 'musicFade', ms: 900 },
    { op: 'narrate', text: 'Fenn turns the little lamp over for a long moment. Then he opens his own old lantern, carried longer than you\'ve been alive, and tips its flame to the wick.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'tint', color: '#ffd58a', alpha: 0.18, ms: 700 },
    { op: 'narrate', text: 'It catches. A small, very clear flame.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'This light was filled for a ladder, by steadier hands than mine. Light doesn\'t keep, apprentice. It\'s only good for passing on.' },
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
    '"To whoever keeps the Point\'s light. Some nights we see your Old Light from our harbour wall. Ours went under, with its rock.',
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
    '"To the Star-tender\'s house, by the Crossroads. The Farlamp is under the sea. The deep rose the night the dark came, and took the rock, the lamp and the keeper\'s stair.',
    'No boat can cross. If any lamp on the mainland still burns from the Keystar\'s own light, send us a flame. We will keep the small lamps lit until it comes. Nan Creel, elder of Driftholm."',
  ]),

  // ===========================================================================
  //  THE SEA + THE ISLES
  // ===========================================================================
  'script.fogwall_turned': [
    { op: 'musicFade', ms: 600 },
    { op: 'narrate', text: 'Fog closes round the skiff. The buoys go grey, then go. Then the blink goes too.' },
    { op: 'narrate', text: 'You row a long time. When the fog thins, you\'re back where you came in.' },
    { op: 'say', text: 'If only you had [[a glass to read the buoys]] by...' },
    { op: 'travel', map: 'farlamp_fogwall', to: { tx: 29, ty: 7 }, facing: 'left' },
  ],
  'script.sound_oarsman': [
    { op: 'say', speaker: 'CALDER', text: 'A boat, with a lamp on it! I was out egging the night the deep came up. Eleven winters on this holm, waving at gulls. Show me what\'s in it!' },
    { op: 'battle', trainer: 'sound_oarsman' },
    { op: 'say', speaker: 'CALDER', text: 'Bested by a boat! The reefs [[west]] are the Shelfwater: mind your keel. Tell Rowan out there Calder says hello. Loudly.' },
    { op: 'setFlag', flag: 'flag:sound_oarsman_beaten' },
  ],
  'script.shelf_kelper': [
    { op: 'say', speaker: 'ROWAN', text: 'Off the mainland? In a BOAT? Eleven winters marooned here: kelp to eat, kelp to sleep on, Calder to shout at. Let\'s see your kin!' },
    { op: 'battle', trainer: 'shelf_kelper' },
    { op: 'say', speaker: 'ROWAN', text: 'Good. The fog west eats boats. The keepers read buoys through [[a glass]].' },
    { op: 'setFlag', flag: 'flag:shelf_kelper_beaten' },
  ],
  // pass 2: the Shelfwater's SE flat and the Fogwall's wreck bar
  'script.shelf_salvager': [
    { op: 'say', speaker: 'DUNSTAN', text: 'Mind the ribs! The GANNET, a Driftholm cutter. She broke here the night the deep rose.' },
    { op: 'say', speaker: 'DUNSTAN', text: 'I was aboard. Waded ashore and never left. Eleven winters stacking her planks for Driftholm\'s doors. A salvager tests what he finds. Let\'s see yours.' },
    { op: 'battle', trainer: 'shelf_salvager' },
    { op: 'say', speaker: 'DUNSTAN', text: 'Sound timber. For the Foot, row [[between the two long bars]].' },
    { op: 'setFlag', flag: 'flag:shelf_salvager_beaten' },
  ],
  'script.fog_pilot': [
    { op: 'say', speaker: 'WILLA', text: 'The lamp-boat! The deep let my coracle through in your lit wake.' },
    { op: 'say', speaker: 'WILLA', text: 'This is the GREYLAG, Dad\'s old cutter. She grounded in the fog the night the deep came up. He\'s never stopped talking about her.' },
    { op: 'say', speaker: 'WILLA', text: 'Pilot\'s custom: nobody shares a wreck without a battle first.' },
    { op: 'battle', trainer: 'fog_pilot' },
    { op: 'say', speaker: 'WILLA', text: 'Fair. The fog south of here turns boats round like a hand on your shoulder. [[Find the keepers\' glass]] and you\'ll find the lane.' },
    { op: 'setFlag', flag: 'flag:fog_pilot_beaten' },
  ],
  // the blink the player has watched from the mainland since the first visit: not
  // the Farlamp (that lies drowned), but Driftholm's own watch-light on the Teeth
  'script.fogwall_watch_light': [
    { op: 'narrate', text: 'A white lamp-tower on a black skerry, hardly twice your height. Its small lamp is wiped and trimmed square.' },
    { op: 'say', text: 'A tin plate is riveted to the door: WATCH-LIGHT OF DRIFTHOLM. TRIMMED NIGHTLY. L. SALLOW.' },
    { op: 'narrate', unless_flag: IDAWN, text: 'So this is the blink you watched from the Point. Not the Farlamp: somebody keeps it lit, so anything lost in the fog has a light to steer by.' },
    { op: 'narrate', if_flag: IDAWN, text: 'The watch-light still burns, out of habit. Under the water beside it glows the Farlamp, gold and steady on the sea-bed.' },
  ],
  'script.pickup_sound_stack': pickup('flag:picked_sound_stack',
    [{ op: 'giveItem', item: 'lumen_drop', count: 1 }],
    'Under the gannets, a keeper\'s oilskin bundle with a sweet in it. Found a LUMEN DROP!'),
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
    [{ op: 'giveItem', item: 'starglass_shard', count: 1 }],
    'At the end of the gull walk, a shard of old starglass in a nest. Found a STARGLASS SHARD!'),
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
    { op: 'say', speaker: 'SORREL', text: 'A visitor! Sit down before the gulls take your hat. The kettle\'s on.' },
    { op: 'heal' },
    { op: 'say', speaker: 'SORREL', text: 'Eleven winters, and you\'re the first to wash up here on purpose.' },
  ],

  // ===========================================================================
  //  DRIFTHOLM
  // ===========================================================================
  'script.driftholm_arrival': [
    { op: 'letterbox', on: true, ms: 400 },
    { op: 'narrate', text: 'Your keel bumps the quay steps. Doors open. Lamps come to windows.' },
    { op: 'say', speaker: 'LORNE', text: 'A boat. A BOAT. Out of the fog, with a lamp lit on its prow!' },
    { op: 'say', speaker: 'BRAM', text: '...That\'s the Farlamp\'s lamp-boat. I\'d know her lines anywhere. My sister\'s been patching her eleven winters, the stubborn old article.' },
    { op: 'emote', actor: 'bram', emote: 'heart' },
    { op: 'say', speaker: 'BRAM', text: 'See [[the elder, Nan Creel]], mainlander. [[Blue door, south of the square]].' },
    { op: 'letterbox', on: false, ms: 400 },
    { op: 'setFlag', flag: ARRIVED },
  ],
  'script.creel_well_locked': [
    { op: 'narrate', text: 'The well-head is chained and sealed with lamp-wax. Steps go down into the dark. A tag: OPEN BY THE ELDER\'S WORD.' },
    { op: 'say', if_flag: ARRIVED, text: '[[Nan Creel\'s house]] is the one with the blue door.' },
  ],
  // Return visits first (guarded on WELL), then the first visit (which SETS WELL),
  // so exactly one branch plays — and on a first visit her greeting comes before
  // any read-back of her own letter (review 2026-10).
  'script.nan_creel': [
    { op: 'run', ref: 'script.nan_creel_return', if_flag: WELL },
    { op: 'run', ref: 'script.nan_creel_first', unless_flag: WELL },
  ],
  'script.nan_creel_return': [
    { op: 'run', ref: 'script.letter_home_5' },
    { op: 'run', ref: 'script.nan_letters_tally' },
    { op: 'run', ref: 'script.nan_after' },
  ],
  'script.nan_creel_first': [
    { op: 'run', ref: 'script.nan_wellstair' },
    { op: 'run', ref: 'script.letter_home_5' },
    { op: 'run', ref: 'script.nan_letters_tally' },
  ],
  'script.nan_wellstair': [
    { op: 'say', speaker: 'NAN CREEL', text: 'So you\'re the boat. Sit, sit. I\'m too old to be surprised standing up.' },
    { op: 'say', speaker: 'NAN CREEL', text: 'The night the dark came, the deep rose and took the Farlamp\'s rock. The lamp burned under the water a week, then went out. Then the fog came.' },
    { op: 'say', speaker: 'NAN CREEL', text: 'A stair runs from our well down to the sea-caves, [[the Undertide]], and out to the lamp\'s rock. We sealed it. Nobody had the light to go down.' },
    { op: 'say', speaker: 'NAN CREEL', text: 'You have. I can see it on you. Here.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'narrate', text: 'She presses a heavy iron key into your hand, worn smooth.' },
    { op: 'say', speaker: 'NAN CREEL', text: '[[Mind the bells]] down there: they tune the tides. And if the Farlamp can be lit... [[light it]]. We\'d like to see the morning too.' },
    { op: 'setFlag', flag: ARRIVED },
    { op: 'setFlag', flag: WELL },
  ],
  'script.nan_after': [
    { op: 'say', speaker: 'NAN CREEL', unless_flag: IDAWN, text: 'The well-stair\'s open. [[Down, and out under the sea]].' },
    { op: 'say', speaker: 'NAN CREEL', if_flag: IDAWN, text: 'Morning on the water. I\'d forgotten it moved like that.' },
  ],
  // the Letters Home tally: nested guards = "all five home", then Nan's gift once
  'script.nan_letters_tally': [{ op: 'run', ref: 'script.nan_tally_2', if_flag: home(1) }],
  'script.nan_tally_2': [{ op: 'run', ref: 'script.nan_tally_3', if_flag: home(2) }],
  'script.nan_tally_3': [{ op: 'run', ref: 'script.nan_tally_4', if_flag: home(3) }],
  'script.nan_tally_4': [{ op: 'run', ref: 'script.nan_tally_5', if_flag: home(4) }],
  'script.nan_tally_5': [{ op: 'run', ref: 'script.nan_letters_gift', if_flag: home(5), unless_flag: LETTERS_DONE }],
  'script.nan_letters_gift': [
    { op: 'say', speaker: 'NAN CREEL', text: 'All five letters home! The island talks of nothing else.' },
    { op: 'say', speaker: 'NAN CREEL', text: 'Take these. The chandlery minted them for the deep.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'deep_charm', count: 3 },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'You got 3 DEEP CHARMS and a LUMEN DROP!' },
    { op: 'setFlag', flag: LETTERS_DONE },
  ],

  // ---- Letters Home: each writer reads her or his own letter back ------------
  'script.letter_home_1': letterHome(1, 'MARRA', [
    'That\'s my letter to Ama! On the Dimglass strand? Then the current runs north after all. I always said it did.',
    'Here. Kelp-wrapped, the way we pack them for the long boats.',
  ], [{ op: 'giveItem', item: 'bright_balm', count: 2 }], 'You got 2 BRIGHT BALMS!', [
    { unless: IDAWN, text: 'Eleven winters drying kelp by lamplight. It comes out grey, but it keeps.' },
    { if: IDAWN, text: 'Kelp in the sun! It dries green again. I\'d forgotten it was ever green.' },
  ], [
    { text: 'Row past Pearlmoor, look for a lamp in a quay window. That\'s my sister. Ama.' },
  ]),
  'script.letter_home_2': letterHome(2, 'LORNE', [
    'Oh, no. Is that the one I wrote to the Point? I was ELEVEN. I spelled "lighthouse" with two H\'s. Don\'t look at it.',
    '...On Gullcry Rock? Then someone on the mainland might have seen our lamps. Have the good lamp-cells. I kept them for best.',
  ], [{ op: 'giveItem', item: 'beacon_charge', count: 3 }], 'You got 3 BEACON CHARGES!', [
    { unless: IDAWN, text: 'Twelve quay lamps and the watch-light, and I trim every one, every night. Somebody has to, till the big one\'s lit.' },
    { if: IDAWN, text: 'I trimmed the lamps this morning out of habit, then just stood there. Nan says an unneeded lamp is the best kind.' },
  ], [
    { text: 'The Old Light on the Point? Tell its keeper a lamp-boy said thank you.' },
  ]),
  'script.letter_home_3': letterHome(3, 'MAUDIE', [
    'My register. You found my register! Wynn, Petra, Cass, Bree, Ottar, the twins... someone out there knew their names all this time.',
    'They\'re great lumps now, the lot of them. Please take this. A teacher\'s salary is mostly coal.',
  ], [{ op: 'giveItem', item: 'hearth_coal', count: 1 }], 'You got a HEARTH COAL!', [
    { unless: IDAWN, text: 'Ottar asked me once what the sun looked like. I had to draw it on a slate.' },
    { if: IDAWN, text: 'School is cancelled. Nobody can sit still. I can\'t sit still. Look at the SEA.' },
  ], [
    { text: 'Ottar wants to be a lamp-keeper. Bram says he\'s too short. Bram said that about me too.' },
  ]),
  'script.letter_home_4': letterHome(4, 'HESK', [
    'My kelp bread! The Glassmere? Then it went round the whole coast and up the fen. That bottle\'s seen more of Vesperholm than I have.',
    'Here. A mender gets paid in odd coin, but it all spends.',
  ], [{ op: 'giveMoney', amount: 1500 }], 'You got 1,500 WICKS!', [
    { unless: IDAWN, text: 'Every net on Driftholm\'s been mended twice. Nowhere to fish but the harbour.' },
    { if: IDAWN, text: 'The boats are going out! The nets will tear on real fish. I\'ve never been so pleased.' },
  ], [
    { text: 'Did you try the bread? Hot stone, feet to the fire. The fire makes it.' },
  ]),
  'script.letter_home_5': [
    { op: 'run', ref: 'script.letter_home_5_read', if_flag: letter(5), unless_flag: home(5) },
  ],
  'script.letter_home_5_read': [
    { op: 'say', speaker: 'NAN CREEL', text: 'My own hand. "Send us a flame." I threw that on the worst night of the first winter.' },
    { op: 'say', speaker: 'NAN CREEL', text: 'And here you are, with the flame. Well. Some letters take their time.' },
    { op: 'setFlag', flag: home(5) },
  ],

  // ---- the bell-ringers' child (Lane C2's "Tide-bell Tuning": the skipping rhyme
  // is the puzzle's hint; once the Bell Galleries are tuned she thanks you — the
  // Lumen Drop is in the ringers' tin down there, so no second prize up here) ----
  'script.driftholm_child': [
    { op: 'say', speaker: 'OTTAR', unless_flag: 'flag:q_isles_bells_tuned', text: 'Mam says the fog has teeth. Has it got teeth?' },
    { op: 'say', speaker: 'OTTAR', unless_flag: 'flag:q_isles_bells_tuned', text: 'We skip to the old bells: "[[Deep calls, shoal answers, harbour]] brings them home!"' },
    { op: 'say', speaker: 'OTTAR', if_flag: 'flag:q_isles_bells_tuned', text: 'It was YOU! We heard the bells come up the well: deep, shoal, harbour! Gran cried. Thank you!' },
  ],
  'script.driftholm_child_day': [
    { op: 'say', speaker: 'OTTAR', text: 'I can see ALL the way to the mainland! There\'s a lighthouse with a brass face!' },
    { op: 'say', speaker: 'OTTAR', if_flag: 'flag:q_isles_bells_tuned', text: 'And the bells! Did you hear the bells this morning? Deep, shoal, harbour!' },
  ],

  // ---- Driftholm's counter, inn and keeper -----------------------------------
  'script.driftholm_chandler': [
    { op: 'say', speaker: 'TESS CREEL', unless_flag: IDAWN, text: 'Creel and Daughter. I\'m the daughter. Balms, coals, lamp-cells. Plenty of lamp-cells.' },
    { op: 'say', speaker: 'TESS CREEL', if_flag: IDAWN, text: 'Morning! Look at me, saying morning. New: Deep Charms. Over deep water they\'re worth three of anything.' },
    { op: 'shop', shop: 'driftholm_chandlery' },
  ],
  'script.driftholm_inn_rest': [
    { op: 'say', speaker: 'INNKEEPER', text: 'The Lamplighters\' Rest! Bed, fire, kelp broth. You look like you need all three.' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEPER', unless_flag: IDAWN, text: 'Slept well? The fog can wait till you\'ve had breakfast.' },
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
    { op: 'say', speaker: 'BRAM', unless_flag: 'flag:isles_dawn', text: 'Old Edda Marrow kept the Farlamp itself. She sits with her back to the sea now. Her log went down with the lamp.' },
    { op: 'say', speaker: 'BRAM', if_flag: 'flag:isles_dawn', text: 'Edda went down the long stair this morning, first time in eleven winters. Came up asking who\'d been at her log!' },
    { op: 'say', speaker: 'BRAM', unless_flag: ARRIVED, text: 'You came in my sister\'s boat? Ione always said she\'d finish it.' },
    { op: 'say', speaker: 'BRAM', text: 'Not in the dark, mainlander. [[Light the Farlamp]], and I\'ll give you the best bout on these isles.' },
  ],
  'script.bram_challenge': [
    { op: 'say', speaker: 'BRAM', text: 'You lit it. You actually lit it. Look at that water, all gold to the horizon.' },
    { op: 'say', speaker: 'BRAM', text: 'A promise is a promise. I\'ve saved my best kin eleven winters. No quarter, no regrets.' },
    { op: 'battle', trainer: 'bram_fathom' },
    { op: 'say', speaker: 'BRAM', text: 'Ha! Beaten on my own quay, by daylight. Best thing in years. I\'ll be training.' },
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
            // Repeatable bouts share the sparrers' one rest (2026-10 review: a 5,760w
            // rematch with no rest was a farm that dwarfed the Lumenary sparring).
            { op: 'spar', trainer: 'bram_fathom_rematch', cooldown: 3, restingRef: 'npc.bram_rematch_resting' },
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
  // Only once ALL five are home (a step takes one guard, so the AND is a chain).
  'script.letters_home_hint': [
    { op: 'run', ref: 'script.letters_home_hint_2', if_flag: 'flag:isles_letter_home_1' },
  ],
  'script.letters_home_hint_2': [
    { op: 'run', ref: 'script.letters_home_hint_3', if_flag: 'flag:isles_letter_home_2' },
  ],
  'script.letters_home_hint_3': [
    { op: 'run', ref: 'script.letters_home_hint_4', if_flag: 'flag:isles_letter_home_3' },
  ],
  'script.letters_home_hint_4': [
    { op: 'run', ref: 'script.letters_home_hint_5', if_flag: 'flag:isles_letter_home_4' },
  ],
  'script.letters_home_hint_5': [
    { op: 'say', if_flag: 'flag:isles_letter_home_5', unless_flag: LETTERS_DONE, text: 'Nan Creel will want to hear the letters are home.' },
  ],
} as ScriptRegistry);

export const FARLAMP_DIALOGUE: DialogueRegistry = {
  'npc.bram_rematch_resting': [
    { speaker: 'BRAM', text: 'My lot are still drying their fins. Win {remaining} more out there and I\'m yours.' },
  ],
  'sign.point_slip_end': [
    { text: 'The slip runs into black water, far too deep to swim. Only a boat could cross here.' },
  ],
  'sign.foot_slip_end': [
    { text: 'An old launch slip, green with weed. Deep water a stone\'s throw out. Only a boat could cross.' },
  ],
  'sign.farlamp_sound': [
    { text: 'FARLAMP SOUND. Lamp-road to the isles: buoys to port, the Fogwall ahead. (Scratched underneath: "STILL HERE".)' },
  ],
  'sign.fogwall_warning': [
    { text: 'TURN BACK IF YOU CANNOT SEE THE BUOYS. Without the keepers\' glass, the fog walks you in circles.' },
  ],
  'sign.gullwrack_hut': [
    { text: 'GULLWRACK BOTHY. Fire lit. Kettle on. Knock loud, the gulls are louder.' },
  ],
  'sign.kelpcrown_ruins': [
    { text: 'The old keepers\' quarter. Their names are worn almost smooth. Kelp grows in the doorways.' },
  ],
  'sign.driftholm': [
    { text: 'DRIFTHOLM. Keepers of the Farlamp. Mind the bell.' },
  ],
  'sign.driftholm_waystone': [
    { text: 'A Driftholm lamp-stone, humming. [[TRAVEL]] from the pause menu takes you home.' },
  ],
  'sign.driftholm_schoolhouse': [
    { speaker: 'MAUDIE', text: '(Through the door:) School\'s out! Find me in the square.' },
  ],
  'sign.driftholm_cottage_marra': [
    { text: 'The door\'s on the latch. Kelp dries on the lintel. Salt and smoke.' },
  ],
  'sign.driftholm_cottage_hesk': [
    { text: 'Nets heaped against the door. Somebody inside is mending them.' },
  ],
  'sign.driftholm_inn': [
    { text: 'THE LAMPLIGHTERS\' REST. Broth on the fire. No credit for mainlanders. (There have been no mainlanders.)' },
  ],
  'sign.driftholm_chandlery': [
    { text: 'Hooks, floats, rope by the fathom, and a jar: SPARE WICKS, DON\'T ASK.' },
  ],
  'sign.driftholm_elder_shelf': [
    { text: 'Eleven years of tide-books, one for every winter. The last one is half full.' },
  ],
  'sign.driftholm_boathouse_hull': [
    { text: 'A boat on the stocks, half-built. Its maker stopped when the fog came.' },
  ],
  'sign.gullwrack_hut_log': [
    { text: 'The bothy log. "Day 4,016. Fog. Gulls. Kettle." "Day 4,017. Fog. Gulls. Kettle." The keeper has a steady hand.' },
  ],
  'npc.sound_oarsman_after': [
    { speaker: 'CALDER', text: 'I\'m going to build a boat like yours. With a lamp on it. Twice the size.' },
  ],
  'npc.shelf_salvager_after': [
    { speaker: 'DUNSTAN', text: 'Her stern-post goes home as the schoolhouse lintel. Children like a door with a story.' },
  ],
  'npc.fog_pilot_after': [
    { speaker: 'WILLA', text: 'I\'m drawing her lines for Dad. He\'ll want to know she still sits proud.' },
  ],
  'npc.shelf_kelper_after': [
    { speaker: 'ROWAN', text: 'Eleven winters of kelp and I still like it. Mostly.' },
  ],
  'npc.driftholm_kelper': [
    { text: 'Eleven winters of kelp. You can tell good fronds by feel.' },
  ],
  'npc.driftholm_cat': [
    { text: 'The cat watches the harbour with enormous patience, waiting for fishing boats.' },
  ],
  'npc.driftholm_inn_fisher': [
    { speaker: 'FISHER', text: 'No fishing past the harbour mouth since the fog. Too easy to row into the deep.' },
  ],
  'npc.driftholm_inn_fisher_day': [
    { speaker: 'FISHER', text: 'Out past the mouth this morning! Caught nothing. Best day\'s fishing of my life.' },
  ],
  'npc.driftholm_apprentice': [
    { speaker: 'APPRENTICE', text: 'Master Fathom started her before I was born. I\'ll finish her, if I learn to plane straight.' },
  ],
};
