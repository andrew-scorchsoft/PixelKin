/**
 * LOWTINDER & TINDERWICK BAY (walkthrough/10 Part III, Lane E, 2026-10) — the town
 * under the bay. This lane OWNS this file: new scripts + dialogue only, spread into
 * the registries via regions/index.ts (a ref here must be NEW, never an override).
 *
 * The lore (story-bible §12): old Tinderwick stood on the shore until THE WINTER THE
 * WATER ROSE (about forty years ago — the same winter the Sunken Solarium flooded).
 * The town moved up the bluff and the old one went under the bay: LOWTINDER. Its last
 * Lampwarden, GRANDMOTHER OTTERY TALLOW (Brisa's grandmother), never left — she lives
 * in the dry upper floor of the old lamp-house, keeping a small lamp the town above
 * forgot. Brisa visits on Sundays and doesn't talk about it. Cosy, a little
 * melancholy, and Ottery is FUNNY: the town didn't drown, it's "having a lie-in".
 *
 * Flags this file owns:
 *   flag:q_lowtinder                 first meeting with Ottery (JOURNAL "The Town Bell" opens)
 *   flag:lowtinder_winch_key         the cellar winch-key (Bell Cellar B1)
 *   flag:q_lowtinder_bell            the bell raised in the belfry pit (B2)
 *   flag:lowtinder_well_climbed      you've climbed the old shaft up into Tinderwick's well
 *   flag:q_lowtinder_bell_home       the bell hung in Tinderwick's square (Brisa's ceremony)
 *   flag:lowtinder_reef_rowed        Ottery rowed out to see the old Tinder Light (post-game)
 *   flag:lowtinder_grandmother_beaten  her reef battle won (her gift; rematchable after)
 *   flag:q_lowtinder_light           she first asks to see the old Tinder Light (post-dawn; JOURNAL)
 *   flag:lowtinder_at_reef           TRANSIENT: she's out on the reef right now (her NPC swap)
 * Read, set elsewhere: flag:dawn, flag:q_isles_afloat (the Farlamp skiff — Part I),
 * flag:lamplight_brightlight (FlagStore derive, 4 Gleams), gleam:tide.
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

const MET = 'flag:q_lowtinder';
const KEY = 'flag:lowtinder_winch_key';
const RAISED = 'flag:q_lowtinder_bell';
const HOME = 'flag:q_lowtinder_bell_home';
const CLIMBED = 'flag:lowtinder_well_climbed';
const ROWED = 'flag:lowtinder_reef_rowed';
const BEATEN = 'flag:lowtinder_grandmother_beaten';
const AT_REEF = 'flag:lowtinder_at_reef';
const SKIFF = 'flag:q_isles_afloat';
const OTTERY = 'GRAN TALLOW';

/** A found-item pickup: sfx, the item, the line, the picked flag. */
function pickup(id: string, item: string, count: number, text: string, sfx = 'world-pickup'): CutsceneStep[] {
  return [
    { op: 'sfx', key: sfx },
    { op: 'giveItem', item, count },
    { op: 'say', text },
    { op: 'setFlag', flag: `flag:picked_${id}` },
  ];
}

/** A found purse of wicks (mirrored in tools/balance/progression.mjs `finds`). */
function purse(id: string, amount: number, text: string): CutsceneStep[] {
  return [
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount },
    { op: 'say', text },
    { op: 'setFlag', flag: `flag:picked_${id}` },
  ];
}

/** A sight-trainer beat: challenge -> battle -> parting line -> beaten flag. */
function bout(tid: string, speaker: string, hello: string, bye: string): CutsceneStep[] {
  return [
    { op: 'say', speaker, text: hello },
    { op: 'battle', trainer: tid },
    { op: 'say', speaker, text: bye },
    { op: 'setFlag', flag: `flag:${tid}_beaten` },
  ];
}

export const LOWTINDER_SCRIPTS: ScriptRegistry = {
  // ======================================================================== TINDERWICK
  // The old fisher on the sand — the seed from minute one.
  'script.lowtinder_fisher': [
    { op: 'say', unless_flag: 'gleam:tide', speaker: 'OLD FISHER', text: 'See them roofs, sticking up out the water? And the tower, past the boat? That\'s where the town WAS, when I was a lad. Old Tinderwick. We just call it Lowtinder now, like it\'s gone somewhere.' },
    { op: 'say', unless_flag: 'gleam:tide', speaker: 'OLD FISHER', text: 'Water came up one winter and never went home. We all moved up the bluff. Well. Nearly all. You\'d need to swim like a seal to get out there, mind.' },
    { op: 'say', if_flag: 'gleam:tide', unless_flag: MET, speaker: 'OLD FISHER', text: 'That\'s a Tidecall on you, isn\'t it? I can tell by the way you look at the water. Then go on — out past the bell-tower, east. The streets are still down there, and the tide\'s mostly out of them.' },
    { op: 'say', if_flag: 'gleam:tide', unless_flag: MET, speaker: 'OLD FISHER', text: 'If there\'s a light on in the old lamp-house... no. Can\'t be. Go and look, though.' },
    { op: 'run', if_flag: MET, ref: 'script.lowtinder_fisher_after' },
  ],
  'script.lowtinder_fisher_after': [
    { op: 'say', if_flag: HOME, speaker: 'OLD FISHER', text: 'Hear it ring, did you? I cried like a gull. Don\'t tell anyone. That bell rang me in for my tea every night till I was fourteen.' },
    { op: 'say', unless_flag: HOME, speaker: 'OLD FISHER', text: 'Ottery Tallow. ALIVE. Down there all these years with the lamp lit, and us up here not looking. Well. Somebody looked. Good on you.' },
  ],

  // Andrew's Tide-stage aside (run from script.andrew_hint, guarded gleam:tide /
  // unless gleam:verdant there): only until you've met Gran Tallow.
  'script.andrew_hint_lowtinder': [
    { op: 'say', unless_flag: MET, speaker: 'ANDREW', text: 'And — home\'s got a secret now you can swim. Off Tinderwick\'s beach, past the old bell-tower in the water. Go and have a look. Bring a towel.' },
  ],

  // The square's bell-gallows: the empty frame's plaque, then the bell itself.
  'script.tinderwick_bell': [
    { op: 'narrate', unless_flag: HOME, text: 'An old timber bell-gallows, empty. A worn plaque on the foot: THE TOWN BELL OF TINDERWICK — LOST TO THE WATER THE WINTER IT ROSE. Underneath, scratched more recently: KEEP THE FRAME. IT\'LL WANT SOMEWHERE TO HANG. — O.T.' },
    { op: 'sfx', if_flag: HOME, key: 'world-moorbell' },
    { op: 'shake', if_flag: HOME, ms: 160, intensity: 0.002 },
    { op: 'narrate', if_flag: HOME, unless_flag: 'flag:dawn', text: 'You give the rope a pull. The old bell of Lowtinder speaks across the square, deep and green and glad, and somewhere a window opens and someone laughs.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'You give the rope a pull. The bell rings out over a morning town — and, far off under the bay, a smaller bell answers from an upstairs window.' },
  ],

  // The garden's old well — the top of the drowned belfry's shaft.
  'script.tinderwick_well': [
    { op: 'narrate', unless_flag: CLIMBED, text: 'The old well. You lean over: a long drop, cold air coming UP, and far below — water, and something like the hum of a very large, very patient bell.' },
    { op: 'narrate', if_flag: CLIMBED, text: 'The old well. You know where it goes now: straight down the drowned bell-tower\'s shaft into the Bell Cellar. It\'s a long climb up and a very long fall down. The bay is the way in.' },
  ],

  // "The Town Bell": Brisa hangs it, once it's raised below.
  'script.tinderwick_bell_ceremony': [
    { op: 'face', actor: 'brisa_bell', facing: 'right' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: 'You heard it too, then. Up the well — one great deep note, right under the square. Half the town came out in their nightclothes.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'You\'ve been down to see her. Gran. ...Don\'t look like that, dear. I go every Sunday. I just never know what to SAY about it up here.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'The old bell-shaft runs straight up under our well — they sank it right down the tower when they moved the town. So. Ropes, everyone! Hester, put the knitting DOWN.' },
    { op: 'letterbox', on: true },
    { op: 'fade', dir: 'out', ms: 600 },
    { op: 'narrate', text: 'It takes the whole Lantern-fair, three ropes, the store\'s cart-winch and a great deal of advice. Up the well it comes, green and dripping, turning slowly in the lamplight.' },
    { op: 'setFlag', flag: HOME },
    { op: 'fade', dir: 'in', ms: 700 },
    { op: 'silence', ms: 600 },
    { op: 'tint', color: '#ffd9a0', alpha: 0.14, ms: 600 },
    { op: 'sfx', key: 'world-moorbell' },
    { op: 'shake', ms: 220, intensity: 0.003 },
    { op: 'narrate', text: 'The old bell of Lowtinder hangs in Tinderwick\'s square, and rings — for the first time in forty years, in the town it was cast for.' },
    { op: 'tint', color: '#ffd9a0', alpha: 0, ms: 900 },
    { op: 'letterbox', on: false },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'proud', text: 'Listen to it. That\'s the note I was born under. Gran will have heard it too — sound carries down the shaft. She\'ll be insufferable about it.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'The town wants you to have this — the fair-chest, every wick of it. And ring it whenever you like, dear. A bell that isn\'t rung forgets its note.' },
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: 1500 },
    { op: 'narrate', text: 'Received 1,500 wicks from the Lantern-fair\'s chest!' },
  ],

  // ======================================================================== THE BAY
  'script.bay_diver': bout('bay_diver', 'LAMP-DIVER SKERRY',
    'I dive the drowned street for lamp-brass. You\'re swimming over my patch — and you\'re dripping on my shoal.',
    'Fair dive. The old streets go east — follow the buoys. And if you see a light on in the lamp-house, it\'s not a ghost. It\'s worse. It\'s a grandmother.'),
  'script.bay_nethand': bout('bay_nethand', 'NET-HAND CORRA',
    'Mind my rock-pools! Mind my nets! Mind ME, actually — I\'m about to win.',
    'Fine. Pools are yours to look at, not to paddle in. That reef out past the rocks? The deep starts there. Nobody swims that. Not even me.'),
  'script.pickup_bay_shoal': pickup('bay_shoal', 'warm_balm', 3,
    'Wedged in the sea-grass, a fisher\'s balm tin with a cork bung. Found 3 WARM BALMS!'),
  'script.pickup_bay_skerry_chart': pickup('bay_skerry_chart', 'chart_hearth_pulse', 1,
    'Behind the rocks, an oilskin roll tied with lamp-wick. Inside, a pressed chart, bone-dry. Found a STAR-CHART: HEARTH PULSE!', 'world-chart'),
  // Deep backtrack #5 — the west reef skerry, skiff only.
  'script.pickup_bay_reef': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'say', text: 'A lamp-keeper\'s sea-chest, chained to the reef rock where no swimmer could reach it. Found a LUMEN DROP and a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_bay_reef' },
  ],
  // The DEEP BACKTRACK (10 Part III): buoy-caches on the old world's deep water,
  // rowed up to in the Farlamp skiff (hand_placed_data.py _DEEP_CACHES).
  'script.pickup_gullcry_deep': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'giveItem', item: 'bright_balm', count: 2 },
    { op: 'say', text: 'A lantern-buoy\'s float-cask, sealed with pitch, bobbing past where any swimmer turns back. Found a LUMEN DROP and 2 BRIGHT BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_gullcry_deep' },
  ],
  'script.pickup_pearlmoor_deep': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'say', text: 'Moored to the harbour\'s outermost buoy, a harbourmaster\'s strongbox nobody could row out to. Found a STARGLASS SHARD and a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_pearlmoor_deep' },
  ],
  'script.pickup_dimglass_deep': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'Past the flats\' last shoal, a cork-ringed crate turning on its tether in the deep. Found a MOTH-AMBER and a LUMEN DROP!' },
    { op: 'setFlag', flag: 'flag:picked_dimglass_deep' },
  ],
  'script.pickup_hearthfall_deep': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'giveItem', item: 'beacon_charge', count: 3 },
    { op: 'say', text: 'Out where the star\'s hiss still warms the water, a lamp-tender\'s float, waiting for a boat. Found a LUMEN DROP and 3 BEACON CHARGES!' },
    { op: 'setFlag', flag: 'flag:picked_hearthfall_deep' },
  ],
  // The old Tinder Light, read from its islet.
  'script.lowtinder_tinder_light': [
    { op: 'narrate', unless_flag: ROWED, text: 'The old Tinder Light. It warned the boats off this reef for two hundred years. The glass is cracked, the lamp-room black, and the stair inside is full of sea.' },
    { op: 'narrate', if_flag: ROWED, text: 'The old Tinder Light. On the lowest step of its gallery someone has set a small lamp in a jar, lit — it bobs on the tide-wind, and it is very stubborn.' },
  ],
  // Gran on her reef (only while she's out there): fight again, or row her home.
  'script.lowtinder_reef_ottery': [
    {
      op: 'choice',
      speaker: OTTERY,
      prompt: 'Another round, duckling? I\'ve got all night. I\'ve had all night for forty years.',
      options: [
        { label: 'Battle again', ops: [{ op: 'run', ref: 'script.lowtinder_reef_rematch' }] },
        { label: 'Row her home', ops: [{ op: 'run', ref: 'script.lowtinder_row_home' }] },
      ],
    },
  ],
  'script.lowtinder_reef_rematch': [
    { op: 'say', speaker: OTTERY, text: 'Mind, I\'ve been practising on the gulls.' },
    { op: 'battle', trainer: 'lowtinder_ottery' },
    // (a first win that comes on a rematch — after losing the first bout — still earns the gift)
    { op: 'run', unless_flag: BEATEN, ref: 'script.lowtinder_reef_gift' },
    { op: 'say', speaker: OTTERY, text: 'Oh, that was LOVELY. My heart\'s going like a kettle.' },
  ],
  'script.lowtinder_row_home': [
    { op: 'say', speaker: OTTERY, text: 'Home, then. Mind the reef — it\'s been waiting forty years to bite someone.' },
    { op: 'setFlag', flag: AT_REEF, value: false },
    { op: 'fade', dir: 'out', ms: 500 },
    { op: 'travel', map: 'lowtinder_lamphouse', to: { tx: 5, ty: 7 }, facing: 'up' },
    { op: 'say', speaker: OTTERY, text: 'Kettle on. Shoes off. You\'re dripping on my good rug, which I found in the sea, so I suppose that\'s fair.' },
  ],

  // ======================================================================== LOWTINDER
  'script.lowtinder_tidewife': [
    { op: 'say', speaker: 'TIDE-WIFE MAB', text: 'I come down at low water to sit on my old step. That\'s my house there, with the weed in the windows. I left the kettle on. Forty years. It\'ll be stewed.' },
    { op: 'say', unless_flag: MET, speaker: 'TIDE-WIFE MAB', text: 'You\'ve not met Ottery yet? Lamp-house, up the old street, the one with a light in it. Take her something sweet. Take her ANYTHING. She talks to the crabs.' },
    { op: 'say', if_flag: MET, speaker: 'TIDE-WIFE MAB', text: 'Ottery says the town\'s not drowned, it\'s having a lie-in. She\'s been saying it so long I\'ve started to believe her.' },
  ],
  'script.lt_mudlark': bout('lt_mudlark', 'MUDLARK PIP',
    'Everything down here\'s MINE. Finders keepers. That includes battles!',
    'Losers weepers. ...Here\'s a free one: the lamp-school on the corner? The back door\'s too dark to open. Nobody\'s ever seen what\'s past it. I\'ve tried. I fell over a desk.'),
  'script.lt_lampwright': bout('lt_lampwright', 'LAMPWRIGHT HOLLIS',
    'I come down to trim the street-lamps. They don\'t light. I trim them anyway. And I don\'t let anybody past without a bout — the cellar\'s no place for the careless.',
    'Careful enough, then. The cellar steps are by the lamp-house. Mind the black water under the belfry.'),
  'script.pickup_lowtinder_landing': pickup('lowtinder_landing', 'bright_balm', 2,
    'Under a lobster pot on the old quay: a dry tin, with a note — FOR WHOEVER SWIMS DOWN. — O. Found 2 BRIGHT BALMS!'),
  'script.pickup_lowtinder_rooftop': pickup('lowtinder_rooftop', 'beacon_charge', 2,
    'Tucked behind a chimney pot on the dry rise: a lamp-tender\'s pouch. Found 2 BEACON CHARGES!'),
  'script.pickup_lowtinder_yard': purse('lowtinder_yard', 400,
    'In the flooded yard, a jar of old wicks someone hid from someone. Found 400 wicks!'),

  // ======================================================================== THE LAMP-HOUSE
  // Gran's whole voice in one staged script. Order matters: the STAGED part runs
  // first (if met), the first meeting last (unless met) — so a first talk plays
  // only the meeting, and every later talk only the stages.
  'script.lowtinder_ottery': [
    { op: 'run', if_flag: MET, ref: 'script.lowtinder_ottery_staged' },
    { op: 'run', unless_flag: MET, ref: 'script.lowtinder_ottery_first' },
  ],
  'script.lowtinder_ottery_first': [
    { op: 'emote', actor: 'ottery', emote: 'alert' },
    { op: 'say', speaker: '???', text: 'Wet feet on my stair! Don\'t drip on the rug. I found that rug in the sea, it\'s been through enough.' },
    { op: 'say', speaker: OTTERY, text: 'Ottery Tallow. Lampwarden of Tinderwick — the REAL one, the low one. Our Brisa keeps the upstairs town. I keep this.' },
    { op: 'say', speaker: OTTERY, text: 'Everyone says the old town drowned. It did NOT drown. It\'s having a lie-in. Forty winters. It\'s earned one.' },
    { op: 'say', speaker: OTTERY, text: 'You\'ve a lamp on your hip and the sea in your hair — a Tidecall, I\'ll bet. Well, well. First visitor in years who wasn\'t a crab or my granddaughter. And the crabs have better manners.' },
    { op: 'say', speaker: OTTERY, text: 'Since you\'re here and you\'ve got young knees: the town bell. It fell when the tower went under. It\'s lying in the belfry pit, two cellars down. I can hear it hum when the tide turns.' },
    { op: 'say', speaker: OTTERY, text: 'There\'s a winch on the belfry ledge that\'ll lift it. The winch-key\'s somewhere in the cellar stores. I put it somewhere SAFE. Then I forgot where safe was.' },
    { op: 'say', speaker: OTTERY, text: 'Steps are just along the street. Mind the black water. And if you get tired, my fire\'s always lit. Come and sit by it. I\'ll talk at you, it\'s very restful.' },
    { op: 'setFlag', flag: MET },
    { op: 'run', ref: 'script.lowtinder_ottery_rest' },
  ],
  'script.lowtinder_ottery_staged': [
    { op: 'run', ref: 'script.lowtinder_ottery_bell' },
    { op: 'run', if_flag: 'flag:dawn', ref: 'script.lowtinder_ottery_reef' },
    { op: 'run', ref: 'script.lowtinder_ottery_rest' },
  ],
  // the bell, latest stage first (one line plays)
  'script.lowtinder_ottery_bell': [
    { op: 'say', if_flag: HOME, unless_flag: 'flag:dawn', speaker: OTTERY, text: 'I HEARD it. Down the shaft, plain as anything. I sat in my chair and I cried into my tea, and then I drank the tea, because waste not. Thank you, duckling.' },
    { op: 'say', if_flag: HOME, unless_flag: 'flag:dawn', speaker: OTTERY, text: 'Our Brisa came down on a Tuesday. A TUESDAY. She just sat with me. Didn\'t say a word. Best visit we\'ve ever had.' },
    { op: 'run', if_flag: HOME, ref: 'script.lowtinder_ottery_bell_dawn' },
    { op: 'run', unless_flag: HOME, ref: 'script.lowtinder_ottery_bell_2' },
  ],
  'script.lowtinder_ottery_bell_dawn': [
    { op: 'say', if_flag: 'flag:dawn', speaker: OTTERY, text: 'They ring it every morning now, up top. A real MORNING. I hear it come down the shaft with the daylight. Two things I never thought I\'d get back, and they came together.' },
  ],
  'script.lowtinder_ottery_bell_2': [
    { op: 'say', if_flag: RAISED, speaker: OTTERY, text: 'It\'s UP? Out of the silt? Oh, my. Then it wants to go home, up the old shaft to the square. You\'ll find it comes out in the well. Tell our Brisa. She\'ll know what to do. She\'ll pretend she doesn\'t, and then she will.' },
    { op: 'run', unless_flag: RAISED, ref: 'script.lowtinder_ottery_bell_3' },
  ],
  'script.lowtinder_ottery_bell_3': [
    { op: 'say', if_flag: KEY, speaker: OTTERY, text: 'That\'s the winch-key! Where was it? ...The winter store. Behind the sacks. Of course it was. Go on, then — down the ladder to the belfry pit, and give the winch a turn.' },
    { op: 'say', unless_flag: KEY, speaker: OTTERY, text: 'No winch-key yet? Try the cellar stores. I think I hid it from a thief. Possibly the thief was me. I was very sneaky in those days.' },
  ],
  // after the dawn: the old Tinder Light
  'script.lowtinder_ottery_reef': [
    { op: 'setFlag', flag: 'flag:q_lowtinder_light' }, // JOURNAL "The Old Tinder Light"
    { op: 'say', unless_flag: SKIFF, speaker: OTTERY, text: 'Morning! Up there, I mean. I can see it down the shaft — a little square of real sky. The old Tinder Light\'s still out on the reef, though. I\'d give my teeth to see it again. Not that I\'ve many left. But nobody\'s boat can cross the deep.' },
    { op: 'run', if_flag: SKIFF, ref: 'script.lowtinder_ottery_reef_ask' },
  ],
  'script.lowtinder_ottery_reef_ask': [
    {
      op: 'choice',
      speaker: OTTERY,
      prompt: 'Is that a boat you\'ve got? A boat that crosses the DEEP? ...Would you row an old woman out to her lighthouse?',
      options: [
        { label: 'Row her out', ops: [{ op: 'run', ref: 'script.lowtinder_reef_row' }] },
        { label: 'Not today', ops: [{ op: 'say', speaker: OTTERY, text: 'Not today. That\'s fine. I\'ve been not-going for forty years, I can not-go a bit longer.' }] },
      ],
    },
  ],
  // the reef scene (post-game): rowed out, the Light, the battle, the gift
  'script.lowtinder_reef_row': [
    { op: 'setFlag', flag: AT_REEF },
    { op: 'letterbox', on: true },
    { op: 'fade', dir: 'out', ms: 600 },
    { op: 'narrate', text: 'You hand her down into the skiff. She sits in the bow like a figurehead, a lamp in a jar on her knees, and tells you which way to row. It is always "left a bit".' },
    { op: 'travel', map: 'tinderwick_bay', to: { tx: 17, ty: 24 }, facing: 'right' },
    { op: 'fade', dir: 'in', ms: 600 },
    { op: 'say', speaker: OTTERY, text: 'There she is. The old Tinder Light. I lit her every night for thirty-one years. I lit her the night the water came — I was up the stair with the wick while the sea came up it after me.' },
    { op: 'say', speaker: OTTERY, text: 'She went out at dawn, the next day. Everything did. I always thought, if I came out here, she\'d look at me like I\'d left her.' },
    { op: 'silence', ms: 900 },
    { op: 'tint', color: '#ffe0a8', alpha: 0.12, ms: 900 },
    { op: 'say', speaker: OTTERY, text: '...She doesn\'t, does she. She just looks tired. Same as me. We did our shift.' },
    { op: 'tint', color: '#ffe0a8', alpha: 0, ms: 900 },
    { op: 'letterbox', on: false },
    { op: 'say', speaker: OTTERY, text: 'Right! Enough of that. I was a Lampwarden before our Brisa had teeth. Let\'s see what the Wayfarer who relit the whole SKY has got. Don\'t you dare go easy on me.' },
    { op: 'battle', trainer: 'lowtinder_ottery' },
    { op: 'run', unless_flag: BEATEN, ref: 'script.lowtinder_reef_gift' },
  ],
  'script.lowtinder_reef_gift': [
    { op: 'say', speaker: OTTERY, text: 'Ha! Oh, that was GRAND. Forty years I\'ve been waiting for a proper bout. The crabs never commit.' },
    { op: 'say', speaker: OTTERY, text: 'Here — the last of the Tinder Light\'s lamp-drops. I kept them in a tin for a rainy day, and it\'s been raining for forty years, so.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'lumen_drop', count: 3 },
    { op: 'narrate', text: 'Gran Tallow gave you 3 LUMEN DROPS!' },
    { op: 'setFlag', flag: ROWED },
    { op: 'setFlag', flag: BEATEN },
    { op: 'say', speaker: OTTERY, text: 'I\'ll sit a while. Row me home whenever you like. Or come and lose to me again — sorry, BEAT me again. Old woman\'s joke.' },
  ],
  'script.lowtinder_ottery_rest': [
    {
      op: 'choice',
      speaker: OTTERY,
      prompt: 'Sit by the fire a while? Your kin look like they want a nap. So do you.',
      options: [
        {
          label: 'Rest by the fire',
          ops: [
            { op: 'heal' },
            { op: 'say', speaker: OTTERY, text: 'There. You snored, and so did your kin, and I told the crabs to hush. Off you go, warm as toast.' },
          ],
        },
        { label: 'Not now', ops: [{ op: 'say', speaker: OTTERY, text: 'Suit yourself. The fire\'s not going anywhere. Neither am I.' }] },
      ],
    },
  ],
  'script.lowtinder_lamp_rack': [
    { op: 'narrate', text: 'The town\'s old street-lamps, every one, brought up out of the water and hung on a rack. Each has a little paper tag: BAKER\'S CORNER. THE STEPS. MAB\'S DOOR. They\'ve all been trimmed this week.' },
  ],
  'script.lowtinder_chalkboard': [
    { op: 'narrate', text: 'Half a lesson, still on the board: A LAMP IS NOT KEPT FOR ITS OWN SAKE. IT IS KEPT FOR WHOEVER IS STILL OUT IN THE DARK. Under it, in a smaller, much later hand: STILL TRUE. — O.T.' },
  ],
  'script.pickup_lowtinder_school_purse': purse('lowtinder_school_purse', 600,
    'In the teacher\'s desk: the lamp-school\'s fee-tin, never collected. Found 600 wicks!'),
  'script.pickup_lowtinder_garden': pickup('lowtinder_garden', 'lumen_drop', 1,
    'Under the moss, a jar of the school\'s lamp-oil has set into a single bright bead. Found a LUMEN DROP!', 'world-gleam-a'),

  // ======================================================================== THE BELL CELLAR
  'script.lt_cellar_keeper': bout('lt_cellar_keeper', 'OLD WICKMAN',
    'Who\'s that? Not the sea, then — the sea doesn\'t knock. I mind these stores. Old habit. Show me you\'re no thief.',
    'No thief. A thief would\'ve run. Gran\'s winch-key? She hid it from me, I expect. Winter store, south-west, past the flood.'),
  'script.lowtinder_winch_key': [
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'setFlag', flag: KEY },
    { op: 'say', text: 'Behind a stack of rotten sacks, hung on a nail with a label in Gran Tallow\'s hand: SAFE. Got the WINCH-KEY!' },
  ],
  'script.pickup_cellar_oil': pickup('cellar_oil', 'glow_charge', 3,
    'A crate of lamp-charges, still sealed in wax. Found 3 GLOW CHARGES!'),
  'script.lowtinder_winch': [
    { op: 'narrate', if_flag: RAISED, text: 'The old bell-winch, its chain run out to the bell. The key\'s still in it, and the crank is warm from your hands.' },
    { op: 'run', unless_flag: RAISED, ref: 'script.lowtinder_winch_try' },
  ],
  'script.lowtinder_winch_try': [
    { op: 'narrate', unless_flag: KEY, text: 'The old bell-winch. Its chain runs down into the black water round the bell. The crank won\'t move — there\'s a keyhole in the boss, and no key.' },
    { op: 'run', if_flag: KEY, ref: 'script.lowtinder_raise_bell' },
  ],
  'script.lowtinder_raise_bell': [
    { op: 'letterbox', on: true },
    { op: 'narrate', text: 'You fit the winch-key. It turns with a groan like an old man getting up. The chain goes taut.' },
    { op: 'musicFade', ms: 800 },
    { op: 'shake', ms: 400, intensity: 0.004 },
    { op: 'sfx', key: 'world-splash' },
    { op: 'narrate', text: 'Turn by turn, the bell comes up out of the silt — streaming water, green with forty years of sea — and settles, ringing faintly, on the belfry floor.' },
    { op: 'setFlag', flag: RAISED },
    { op: 'silence', ms: 700 },
    { op: 'sfx', key: 'world-moorbell' },
    { op: 'narrate', text: 'One note. It goes up the old shaft over your head, all the way up, and out into the night.' },
    { op: 'letterbox', on: false },
    { op: 'narrate', text: 'It\'s far too heavy to carry. But high in the north-west corner, a rope hangs down the old shaft — and there is lamplight at the top of it.' },
  ],
  'script.lowtinder_bell_read': [
    { op: 'narrate', unless_flag: RAISED, text: 'The town bell of old Tinderwick, lying on its lip in the silt. Something hums inside it when the tide turns. Up on the north ledge, a winch\'s chain runs down to its crown.' },
    { op: 'narrate', if_flag: RAISED, text: 'The bell sits on the belfry floor, dripping. Cast on its shoulder: I RING THE TOWN HOME.' },
  ],
  // the old shaft: up into Tinderwick's square (a one-way travel — the way out)
  'script.lowtinder_well_climb': [
    {
      op: 'choice',
      prompt: 'A rope hangs down the old bell-shaft, knotted every arm\'s length. Lamplight, far up. Climb it?',
      options: [
        {
          label: 'Climb',
          ops: [
            { op: 'fade', dir: 'out', ms: 600 },
            { op: 'narrate', text: 'Up, and up, past old belfry stone and then newer brick, until your hand finds a bucket-chain, and then a well-lip, and then a flowerbed.' },
            { op: 'setFlag', flag: CLIMBED },
            { op: 'travel', map: 'tinderwick', to: { tx: 19, ty: 11 }, facing: 'right' },
            { op: 'fade', dir: 'in', ms: 600 },
            { op: 'narrate', text: 'Tinderwick\'s square. Home. The old well was the drowned bell-tower\'s shaft all along.' },
          ],
        },
        { label: 'Stay', ops: [] },
      ],
    },
  ],
  'script.pickup_belfry_lumen': pickup('belfry_lumen', 'lumen_drop', 1,
    'In the south vault, the bell-ringers\' tin: a single LUMEN DROP, bright as the day it was set down. Found a LUMEN DROP!', 'world-gleam-a'),
  'script.pickup_belfry_ledge': pickup('belfry_ledge', 'warm_balm', 3,
    'A ringer\'s kit-bag on the east gallery. Found 3 WARM BALMS!'),
};

export const LOWTINDER_DIALOGUE: DialogueRegistry = {
  'sign.tinderwick_bay': [
    { text: 'TIDEPOOL SKERRY. Old Tinderwick lies east, under the water. The roofs are the high street. Swim kindly — people lived here.' },
  ],
  'sign.lowtinder_landing': [
    { text: 'LOWTINDER QUAY. (Painted over, by hand:) NOT DROWNED. HAVING A LIE-IN. — O.T.' },
  ],
  'sign.lowtinder_school': [
    { text: 'THE LAMP-SCHOOL. A wick well trimmed is a promise well kept. (The door has been propped open with a brick for forty years.)' },
  ],
  'npc.lowtinder_notice': [
    { text: 'The old town notice-board. The last notice, swollen and pale: FAIR NIGHT — LANTERNS AT THE BELL-TOWER — ALL WELCOME. Under it, newer chalk on slate: STILL WELCOME. — O.' },
  ],
  'npc.bay_diver_after': [
    { speaker: 'LAMP-DIVER SKERRY', text: 'Every roof out there\'s a street I could name. My nan was born under that one.' },
  ],
  'npc.bay_nethand_after': [
    { speaker: 'NET-HAND CORRA', text: 'See the old lighthouse out on the reef? Nobody\'s lit it since the water rose. Too deep to swim to, and a boat can\'t cross the deep. Not a NORMAL boat.' },
  ],
  'npc.lt_mudlark_after': [
    { speaker: 'MUDLARK PIP', text: 'If you find a silver spoon, it\'s mine. If you find a golden spoon, it\'s also mine.' },
  ],
  'npc.lt_lampwright_after': [
    { speaker: 'LAMPWRIGHT HOLLIS', text: 'Trimmed. Every one. Some day they\'ll light. Gran Tallow says that\'s the job.' },
  ],
  'npc.lt_cellar_keeper_after': [
    { speaker: 'OLD WICKMAN', text: 'The bell\'s down the ladder, south-east. I go and sit by it. It hums. It\'s nice company.' },
  ],
  'sign.lowtinder_lamphouse_shelf': [
    { text: 'A shelf of jars: SEA-GLASS. BUTTONS. MORE BUTTONS. BRISA\'S MILK TOOTH. A note on the end jar: DO NOT THROW AWAY, THIS MEANS YOU BRISA.' },
  ],
  'sign.lowtinder_primers': [
    { text: 'WICK-PRIMERS for small hands: "Lesson One: the flame is a guest. Lesson Two: never leave a guest alone." The pages are stuck together, but someone has dried them one by one.' },
  ],
  'door.lowtinder_garden_dark': [
    { text: 'The back door opens on pitch dark — a black so thick your vesperlamp only finds the first step. Something green breathes beyond it. A BRIGHTER lamp would show the way.' },
  ],
  'sign.lowtinder_garden': [
    { text: 'THE SCHOOL GARDEN. "Plant a light and see what grows." The glass roof is long gone; the moss kept the lesson anyway.' },
  ],
  'sign.lowtinder_cellar': [
    { text: 'LAMP-HOUSE STORES. OIL — ROPE — WINTER. BELFRY PIT BELOW: MIND THE BLACK WATER.' },
  ],
};
