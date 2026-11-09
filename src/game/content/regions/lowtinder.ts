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
    { op: 'say', unless_flag: 'gleam:tide', speaker: 'OLD FISHER', text: 'See them roofs in the water? That\'s where the town WAS when I was a lad. Old Tinderwick. Lowtinder, we call it now.' },
    { op: 'say', unless_flag: 'gleam:tide', speaker: 'OLD FISHER', text: 'Water came up one winter and never went home. We moved up the bluff. Nearly all of us. You\'d need to [[swim like a seal]] to get out there.' },
    { op: 'say', if_flag: 'gleam:tide', unless_flag: MET, speaker: 'OLD FISHER', text: 'That\'s a Tidecall on you! Then go on: [[out past the bell-tower, east]]. The streets are still down there, and the tide\'s mostly out of them.' },
    { op: 'say', if_flag: 'gleam:tide', unless_flag: MET, speaker: 'OLD FISHER', text: 'A light in the old lamp-house... no. Can\'t be. Go and look, though.' },
    { op: 'run', if_flag: MET, ref: 'script.lowtinder_fisher_after' },
  ],
  'script.lowtinder_fisher_after': [
    { op: 'say', if_flag: HOME, speaker: 'OLD FISHER', text: 'Hear it ring? I cried like a gull. It rang me in for tea as a lad.' },
    { op: 'say', unless_flag: HOME, speaker: 'OLD FISHER', text: 'Ottery Tallow. ALIVE. Down there all these years with the lamp lit, and us not looking. Somebody looked. Good on you.' },
  ],

  // Andrew's Tide-stage aside (run from script.andrew_hint, guarded gleam:tide /
  // unless gleam:verdant there): only until you've met Gran Tallow.
  'script.andrew_hint_lowtinder': [
    { op: 'say', unless_flag: MET, speaker: 'ANDREW', text: 'And home\'s got a secret now you can swim. [[Off Tinderwick\'s beach]], past the old bell-tower in the water. Go and look. Bring a towel.' },
  ],

  // The square's bell-gallows: the empty frame's plaque, then the bell itself.
  'script.tinderwick_bell': [
    { op: 'narrate', unless_flag: HOME, text: 'An empty bell-gallows. A worn plaque: THE TOWN BELL OF TINDERWICK — LOST TO THE WATER THE WINTER IT ROSE. Scratched beneath: KEEP THE FRAME. IT\'LL WANT SOMEWHERE TO HANG. — O.T.' },
    { op: 'sfx', if_flag: HOME, key: 'world-moorbell' },
    { op: 'shake', if_flag: HOME, ms: 160, intensity: 0.002 },
    { op: 'narrate', if_flag: HOME, unless_flag: 'flag:dawn', text: 'The old bell of Lowtinder speaks across the square, deep and glad. Somewhere a window opens and someone laughs.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'The bell rings over a morning town. Under the bay, a small bell answers.' },
  ],

  // The garden's old well — the top of the drowned belfry's shaft.
  'script.tinderwick_well': [
    { op: 'narrate', unless_flag: CLIMBED, text: 'The old well. Cold air rises, and far below hums a very patient bell.' },
    { op: 'narrate', if_flag: CLIMBED, text: 'The old well: the drowned bell-tower\'s shaft, straight down to the Bell Cellar. A long climb up, a longer fall down. [[The bay]] is the way in.' },
  ],

  // "The Town Bell": Brisa hangs it, once it's raised below.
  'script.tinderwick_bell_ceremony': [
    { op: 'face', actor: 'brisa_bell', facing: 'right' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: 'You heard it too? One deep note up the well, right under the square. Half the town came out in their nightclothes.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'You\'ve been down to see Gran. ...Don\'t look like that, dear. I go every Sunday. I just never know what to SAY about it up here.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'The old bell-shaft runs straight up under our well. So. Ropes, everyone! Hester, put the knitting DOWN.' },
    { op: 'letterbox', on: true },
    { op: 'fade', dir: 'out', ms: 600 },
    { op: 'narrate', text: 'It takes the whole Lantern-fair, three ropes, a cart-winch and much advice. Up the well it comes, green and dripping.' },
    { op: 'setFlag', flag: HOME },
    { op: 'fade', dir: 'in', ms: 700 },
    { op: 'silence', ms: 600 },
    { op: 'tint', color: '#ffd9a0', alpha: 0.14, ms: 600 },
    { op: 'sfx', key: 'world-moorbell' },
    { op: 'shake', ms: 220, intensity: 0.003 },
    { op: 'narrate', text: 'The old bell of Lowtinder hangs in Tinderwick\'s square, and rings for the town it was cast for. The first time in forty years.' },
    { op: 'tint', color: '#ffd9a0', alpha: 0, ms: 900 },
    { op: 'letterbox', on: false },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'proud', text: 'Listen. That\'s the note I was born under. Gran will hear it down the shaft. She\'ll be insufferable.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'The town wants you to have the fair-chest, every wick. Ring it whenever you like, dear. A bell that isn\'t rung forgets its note.' },
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: 1500 },
    { op: 'narrate', text: 'Received 1,500 wicks from the Lantern-fair\'s chest!' },
  ],

  // ======================================================================== THE BAY
  'script.bay_diver': bout('bay_diver', 'LAMP-DIVER SKERRY',
    'I dive the drowned street for lamp-brass. You\'re swimming over my patch!',
    'Fair dive. The old streets go [[east, along the buoys]]. A light in the lamp-house isn\'t a ghost. It\'s worse. It\'s a grandmother.'),
  'script.bay_nethand': bout('bay_nethand', 'NET-HAND CORRA',
    'Mind my rock-pools! Mind my nets! Mind ME, actually. I\'m about to win.',
    'Fine. See the reef past the rocks? The deep starts there. Nobody swims that. Not even me.'),
  'script.pickup_bay_shoal': pickup('bay_shoal', 'warm_balm', 3,
    'In the sea-grass, a fisher\'s balm tin. Found 3 WARM BALMS!'),
  'script.pickup_bay_skerry_chart': pickup('bay_skerry_chart', 'chart_hearth_pulse', 1,
    'Behind the rocks, an oilskin roll, bone-dry inside. Found a STAR-CHART: HEARTH PULSE!', 'world-chart'),
  // Deep backtrack #5 — the west reef skerry, skiff only.
  'script.pickup_bay_reef': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'say', text: 'A sea-chest chained to the reef. Found a LUMEN DROP and a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_bay_reef' },
  ],
  // The DEEP BACKTRACK (10 Part III): buoy-caches on the old world's deep water,
  // rowed up to in the Farlamp skiff (hand_placed_data.py _DEEP_CACHES).
  'script.pickup_gullcry_deep': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'giveItem', item: 'bright_balm', count: 2 },
    { op: 'say', text: 'A float-cask, sealed with pitch. Found a LUMEN DROP and 2 BRIGHT BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_gullcry_deep' },
  ],
  'script.pickup_pearlmoor_deep': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'say', text: 'A strongbox on the far buoy. Found a STARGLASS SHARD and a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_pearlmoor_deep' },
  ],
  'script.pickup_dimglass_deep': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'A tethered crate past the shoal. Found a MOTH-AMBER and a LUMEN DROP!' },
    { op: 'setFlag', flag: 'flag:picked_dimglass_deep' },
  ],
  'script.pickup_hearthfall_deep': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'giveItem', item: 'beacon_charge', count: 3 },
    { op: 'say', text: 'A float on the star-warmed water. Found a LUMEN DROP and 3 BEACON CHARGES!' },
    { op: 'setFlag', flag: 'flag:picked_hearthfall_deep' },
  ],
  // The old Tinder Light, read from its islet.
  'script.lowtinder_tinder_light': [
    { op: 'narrate', unless_flag: ROWED, text: 'The old Tinder Light warned boats off this reef for two hundred years. The glass is cracked, the stair full of sea.' },
    { op: 'narrate', if_flag: ROWED, text: 'The old Tinder Light. On its lowest gallery step, a small lamp in a jar, lit and bobbing in the wind. It is very stubborn.' },
  ],
  // Gran on her reef (only while she's out there): fight again, or row her home.
  'script.lowtinder_reef_ottery': [
    {
      op: 'choice',
      speaker: OTTERY,
      prompt: 'Another round, duckling? I\'ve had all night for forty years.',
      options: [
        { label: 'Battle again', ops: [{ op: 'run', ref: 'script.lowtinder_reef_rematch' }] },
        { label: 'Row her home', ops: [{ op: 'run', ref: 'script.lowtinder_row_home' }] },
      ],
    },
  ],
  'script.lowtinder_reef_rematch': [
    { op: 'say', speaker: OTTERY, text: 'Mind, I\'ve been practising on the gulls.' },
    // the first win (the gift) is an ordinary bout; once she's been beaten the
    // rematch shares the sparrers' one rest (no wick farm)
    { op: 'battle', trainer: 'lowtinder_ottery', unless_flag: BEATEN },
    { op: 'spar', trainer: 'lowtinder_ottery', cooldown: 3, restingRef: 'npc.ottery_rematch_resting', if_flag: BEATEN },
    // (a first win that comes on a rematch — after losing the first bout — still earns the gift)
    { op: 'run', unless_flag: BEATEN, ref: 'script.lowtinder_reef_gift' },
    { op: 'say', speaker: OTTERY, text: 'Oh, that was LOVELY. My heart\'s going like a kettle.' },
  ],
  'script.lowtinder_row_home': [
    { op: 'say', speaker: OTTERY, text: 'Home, then. Mind the reef. It\'s waited forty years to bite someone.' },
    { op: 'setFlag', flag: AT_REEF, value: false },
    { op: 'fade', dir: 'out', ms: 500 },
    { op: 'travel', map: 'lowtinder_lamphouse', to: { tx: 5, ty: 7 }, facing: 'up' },
    { op: 'say', speaker: OTTERY, text: 'Kettle on. Shoes off. You\'re dripping on my good rug, which I found in the sea, so that\'s fair.' },
  ],

  // ======================================================================== LOWTINDER
  'script.lowtinder_tidewife': [
    { op: 'say', speaker: 'TIDE-WIFE MAB', text: 'I sit on my old step at low water. That\'s my house, weed in the windows. Left the kettle on forty years ago. It\'ll be stewed.' },
    { op: 'say', unless_flag: MET, speaker: 'TIDE-WIFE MAB', text: 'Not met Ottery yet? [[The lamp-house, up the old street]], with a light in it. Take her ANYTHING. She talks to the crabs.' },
    { op: 'say', if_flag: MET, speaker: 'TIDE-WIFE MAB', text: 'Ottery says the town\'s just having a lie-in. I\'ve started to believe her.' },
  ],
  'script.lt_mudlark': bout('lt_mudlark', 'MUDLARK PIP',
    'Everything down here\'s MINE. Finders keepers. That includes battles!',
    'Losers weepers. Free tip: the lamp-school\'s back door is too dark to open. I tried. I fell over a desk.'),
  'script.lt_lampwright': bout('lt_lampwright', 'LAMPWRIGHT HOLLIS',
    'I trim the street-lamps. They don\'t light; I trim them anyway. Nobody passes without a bout. The cellar\'s no place for the careless.',
    'Careful enough. [[The cellar steps]] are by the lamp-house. Mind the black water.'),
  'script.pickup_lowtinder_landing': pickup('lowtinder_landing', 'bright_balm', 2,
    'Under a lobster pot: a dry tin and a note, FOR WHOEVER SWIMS DOWN. — O. Found 2 BRIGHT BALMS!'),
  'script.pickup_lowtinder_rooftop': pickup('lowtinder_rooftop', 'beacon_charge', 2,
    'Behind a chimney pot: a lamp-tender\'s pouch. Found 2 BEACON CHARGES!'),
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
    { op: 'say', speaker: '???', text: 'Wet feet! Mind the rug. I found it in the sea; it\'s been through enough.' },
    { op: 'say', speaker: OTTERY, text: 'Ottery Tallow. Lampwarden of Tinderwick: the REAL one, the low one.' },
    { op: 'say', speaker: OTTERY, text: 'They say the town drowned. It did NOT. It\'s having a lie-in. Forty winters.' },
    { op: 'say', speaker: OTTERY, text: 'A lamp on your hip and the sea in your hair. First visitor in years who wasn\'t a crab or my granddaughter. The crabs have better manners.' },
    { op: 'say', speaker: OTTERY, text: 'Since you\'ve young knees: [[the town bell]]. It fell when the tower went under, and lies [[in the belfry pit]], two cellars down. It hums when the tide turns.' },
    { op: 'say', speaker: OTTERY, text: 'A winch on the belfry ledge will lift it. [[The winch-key\'s in the cellar stores]]. I put it somewhere SAFE. Then I forgot where safe was.' },
    { op: 'say', speaker: OTTERY, text: 'Steps are just along the street. Mind the black water. If you tire, my fire\'s lit. I\'ll talk at you; it\'s very restful.' },
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
    { op: 'say', if_flag: HOME, unless_flag: 'flag:dawn', speaker: OTTERY, text: 'I HEARD it, down the shaft. I cried into my tea, then drank the tea, because waste not. Thank you, duckling.' },
    { op: 'say', if_flag: HOME, unless_flag: 'flag:dawn', speaker: OTTERY, text: 'Brisa came down on a TUESDAY. Just sat with me. Best visit ever.' },
    { op: 'run', if_flag: HOME, ref: 'script.lowtinder_ottery_bell_dawn' },
    { op: 'run', unless_flag: HOME, ref: 'script.lowtinder_ottery_bell_2' },
  ],
  'script.lowtinder_ottery_bell_dawn': [
    { op: 'say', if_flag: 'flag:dawn', speaker: OTTERY, text: 'They ring it every morning up top. A real MORNING, down the shaft with the bell. Two things I never thought I\'d get back.' },
  ],
  'script.lowtinder_ottery_bell_2': [
    { op: 'say', if_flag: RAISED, speaker: OTTERY, text: 'It\'s UP? Then it wants to go home, [[up the old shaft]] to the well. [[Tell our Brisa]]. She\'ll pretend she doesn\'t know what to do, and then she will.' },
    { op: 'run', unless_flag: RAISED, ref: 'script.lowtinder_ottery_bell_3' },
  ],
  'script.lowtinder_ottery_bell_3': [
    { op: 'say', if_flag: KEY, speaker: OTTERY, text: 'The winch-key! Behind the sacks, of course. Go on: [[down the ladder to the belfry pit]], and give the winch a turn.' },
    { op: 'say', unless_flag: KEY, speaker: OTTERY, text: 'No winch-key? Try [[the cellar stores]]. I hid it from a thief. Possibly me.' },
  ],
  // after the dawn: the old Tinder Light
  'script.lowtinder_ottery_reef': [
    { op: 'setFlag', flag: 'flag:q_lowtinder_light' }, // JOURNAL "The Old Tinder Light"
    { op: 'say', unless_flag: SKIFF, speaker: OTTERY, text: 'Morning, up there! The old Tinder Light\'s still out on the reef. I\'d give my teeth to see it. Not that I\'ve many. But no boat crosses the deep.' },
    { op: 'run', if_flag: SKIFF, ref: 'script.lowtinder_ottery_reef_ask' },
  ],
  'script.lowtinder_ottery_reef_ask': [
    {
      op: 'choice',
      speaker: OTTERY,
      prompt: 'A boat for the DEEP? ...Would you row an old woman out to her lighthouse?',
      options: [
        { label: 'Row her out', ops: [{ op: 'run', ref: 'script.lowtinder_reef_row' }] },
        { label: 'Not today', ops: [{ op: 'say', speaker: OTTERY, text: 'Not today. I\'ve been not-going forty years. I can not-go a bit longer.' }] },
      ],
    },
  ],
  // the reef scene (post-game): rowed out, the Light, the battle, the gift
  'script.lowtinder_reef_row': [
    { op: 'setFlag', flag: AT_REEF },
    { op: 'letterbox', on: true },
    { op: 'fade', dir: 'out', ms: 600 },
    { op: 'narrate', text: 'You hand her into the skiff. She sits in the bow, a lamp in a jar on her knees, steering. It is always "left a bit".' },
    { op: 'travel', map: 'tinderwick_bay', to: { tx: 17, ty: 24 }, facing: 'right' },
    { op: 'fade', dir: 'in', ms: 600 },
    { op: 'say', speaker: OTTERY, text: 'There she is. I lit her every night for thirty-one years. I lit her the night the water came, up the stair with the wick while the sea climbed after me.' },
    { op: 'say', speaker: OTTERY, text: 'She went out the next dawn. Everything did. I always thought she\'d look at me like I\'d left her.' },
    { op: 'silence', ms: 900 },
    { op: 'tint', color: '#ffe0a8', alpha: 0.12, ms: 900 },
    { op: 'say', speaker: OTTERY, text: '...She doesn\'t, does she. She just looks tired. Same as me. We did our shift.' },
    { op: 'tint', color: '#ffe0a8', alpha: 0, ms: 900 },
    { op: 'letterbox', on: false },
    { op: 'say', speaker: OTTERY, text: 'Enough. I was a Lampwarden before Brisa had teeth. Let\'s see what the Wayfarer who relit the SKY has got. Don\'t go easy!' },
    { op: 'battle', trainer: 'lowtinder_ottery' },
    { op: 'run', unless_flag: BEATEN, ref: 'script.lowtinder_reef_gift' },
  ],
  'script.lowtinder_reef_gift': [
    { op: 'say', speaker: OTTERY, text: 'Ha! GRAND. Forty years waiting for a proper bout. The crabs never commit.' },
    { op: 'say', speaker: OTTERY, text: 'Here: the Tinder Light\'s last lamp-drops. I kept them for a rainy day, and it\'s rained forty years, so.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'lumen_drop', count: 3 },
    { op: 'narrate', text: 'Gran Tallow gave you 3 LUMEN DROPS!' },
    { op: 'setFlag', flag: ROWED },
    { op: 'setFlag', flag: BEATEN },
    { op: 'say', speaker: OTTERY, text: 'I\'ll sit a while. Row me home whenever you like. Or come and lose to me again. Sorry, BEAT me. Old woman\'s joke.' },
  ],
  'script.lowtinder_ottery_rest': [
    {
      op: 'choice',
      speaker: OTTERY,
      prompt: 'Sit by the fire a while? Your kin want a nap. So do you.',
      options: [
        {
          label: 'Rest by the fire',
          ops: [
            { op: 'heal' },
            { op: 'say', speaker: OTTERY, text: 'You snored, your kin snored, I hushed the crabs. Off you go, warm as toast.' },
          ],
        },
        { label: 'Not now', ops: [{ op: 'say', speaker: OTTERY, text: 'Suit yourself. The fire\'s not going anywhere. Neither am I.' }] },
      ],
    },
  ],
  'script.lowtinder_lamp_rack': [
    { op: 'narrate', text: 'The old street-lamps, raised from the water onto a rack, each tagged: BAKER\'S CORNER. THE STEPS. MAB\'S DOOR. All trimmed.' },
  ],
  'script.lowtinder_chalkboard': [
    { op: 'narrate', text: 'Half a lesson on the board: A LAMP IS NOT KEPT FOR ITS OWN SAKE. IT IS KEPT FOR WHOEVER IS STILL OUT IN THE DARK. Under it, in a much later hand: STILL TRUE. — O.T.' },
  ],
  'script.pickup_lowtinder_school_purse': purse('lowtinder_school_purse', 600,
    'In the teacher\'s desk: the lamp-school\'s fee-tin, never collected. Found 600 wicks!'),
  'script.pickup_lowtinder_garden': pickup('lowtinder_garden', 'lumen_drop', 1,
    'Under the moss, the school\'s lamp-oil has set into one bright bead. Found a LUMEN DROP!', 'world-gleam-a'),

  // ======================================================================== THE BELL CELLAR
  'script.lt_cellar_keeper': bout('lt_cellar_keeper', 'OLD WICKMAN',
    'Not the sea, then. The sea doesn\'t knock. I mind these stores. Show me you\'re no thief.',
    'No thief. A thief would\'ve run. Gran\'s winch-key? Try [[the winter store, south-west]], past the flood.'),
  'script.lowtinder_winch_key': [
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'setFlag', flag: KEY },
    { op: 'say', text: 'Behind rotten sacks, on a nail, a label in Gran Tallow\'s hand: SAFE. Got the WINCH-KEY!' },
  ],
  'script.pickup_cellar_oil': pickup('cellar_oil', 'glow_charge', 3,
    'A crate of lamp-charges, still sealed in wax. Found 3 GLOW CHARGES!'),
  'script.lowtinder_winch': [
    { op: 'narrate', if_flag: RAISED, text: 'The bell-winch, chain run out to the bell. The crank\'s still warm.' },
    { op: 'run', unless_flag: RAISED, ref: 'script.lowtinder_winch_try' },
  ],
  'script.lowtinder_winch_try': [
    { op: 'narrate', unless_flag: KEY, text: 'The old bell-winch. Its chain runs down into black water. The crank won\'t move: there\'s a keyhole, and [[no key]].' },
    { op: 'run', if_flag: KEY, ref: 'script.lowtinder_raise_bell' },
  ],
  'script.lowtinder_raise_bell': [
    { op: 'letterbox', on: true },
    { op: 'narrate', text: 'You fit the winch-key. It turns with a groan like an old man getting up.' },
    { op: 'musicFade', ms: 800 },
    { op: 'shake', ms: 400, intensity: 0.004 },
    { op: 'sfx', key: 'world-splash' },
    { op: 'narrate', text: 'The bell rises out of the silt, green with forty years of sea, and settles, ringing faintly, on the belfry floor.' },
    { op: 'setFlag', flag: RAISED },
    { op: 'silence', ms: 700 },
    { op: 'sfx', key: 'world-moorbell' },
    { op: 'narrate', text: 'One note. It climbs the old shaft over your head and out into the night.' },
    { op: 'letterbox', on: false },
    { op: 'narrate', text: 'Far too heavy to carry. But [[in the north-west corner]], a rope hangs down the old shaft, with lamplight at the top.' },
  ],
  'script.lowtinder_bell_read': [
    { op: 'narrate', unless_flag: RAISED, text: 'The town bell of old Tinderwick, on its lip in the silt, humming when the tide turns. On the [[north ledge]], a winch\'s chain runs to its crown.' },
    { op: 'narrate', if_flag: RAISED, text: 'The bell drips on the floor. On its shoulder: I RING THE TOWN HOME.' },
  ],
  // the old shaft: up into Tinderwick's square (a one-way travel — the way out)
  'script.lowtinder_well_climb': [
    {
      op: 'choice',
      prompt: 'A knotted rope hangs down the bell-shaft. Lamplight, far up. Climb it?',
      options: [
        {
          label: 'Climb',
          ops: [
            { op: 'fade', dir: 'out', ms: 600 },
            { op: 'narrate', text: 'Up past stone and brick, to a bucket-chain, a well-lip, a flowerbed.' },
            { op: 'setFlag', flag: CLIMBED },
            { op: 'travel', map: 'tinderwick', to: { tx: 19, ty: 11 }, facing: 'right' },
            { op: 'fade', dir: 'in', ms: 600 },
            { op: 'narrate', text: 'Tinderwick\'s square. Home. The well was the bell-tower\'s shaft all along.' },
          ],
        },
        { label: 'Stay', ops: [] },
      ],
    },
  ],
  'script.pickup_belfry_lumen': pickup('belfry_lumen', 'lumen_drop', 1,
    'In the south vault, the bell-ringers\' tin. Found a LUMEN DROP!', 'world-gleam-a'),
  'script.pickup_belfry_ledge': pickup('belfry_ledge', 'warm_balm', 3,
    'A ringer\'s kit-bag on the east gallery. Found 3 WARM BALMS!'),
};

export const LOWTINDER_DIALOGUE: DialogueRegistry = {
  'npc.ottery_rematch_resting': [
    { speaker: 'GRAN TALLOW', text: 'Give an old woman a breather, duckling. Win {remaining} more elsewhere, then come and lose to me properly.' },
  ],
  'sign.tinderwick_bay': [
    { text: 'TIDEPOOL SKERRY. [[Old Tinderwick]] lies east, under the water. Swim kindly: people lived here.' },
  ],
  'sign.lowtinder_landing': [
    { text: 'LOWTINDER QUAY. (Painted over, by hand:) NOT DROWNED. HAVING A LIE-IN. — O.T.' },
  ],
  'sign.lowtinder_school': [
    { text: 'THE LAMP-SCHOOL. A wick well trimmed is a promise well kept. (The door\'s been propped open forty years.)' },
  ],
  'npc.lowtinder_notice': [
    { text: 'The last notice: FAIR NIGHT — LANTERNS AT THE BELL-TOWER — ALL WELCOME. Newer chalk beneath: STILL WELCOME. — O.' },
  ],
  'npc.bay_diver_after': [
    { speaker: 'LAMP-DIVER SKERRY', text: 'Every roof out there\'s a street I could name. My nan was born under that one.' },
  ],
  'npc.bay_nethand_after': [
    { speaker: 'NET-HAND CORRA', text: 'See the old lighthouse on the reef? Unlit since the water rose. Too deep to swim, and boats can\'t cross the deep. Not NORMAL boats.' },
  ],
  'npc.lt_mudlark_after': [
    { speaker: 'MUDLARK PIP', text: 'If you find a silver spoon, it\'s mine. If you find a golden spoon, it\'s also mine.' },
  ],
  'npc.lt_lampwright_after': [
    { speaker: 'LAMPWRIGHT HOLLIS', text: 'Trimmed. Every one. Some day they\'ll light. Gran Tallow says that\'s the job.' },
  ],
  'npc.lt_cellar_keeper_after': [
    { speaker: 'OLD WICKMAN', text: 'The bell\'s [[down the ladder, south-east]]. I sit by it. It hums. Nice company.' },
  ],
  'sign.lowtinder_lamphouse_shelf': [
    { text: 'Jars: SEA-GLASS. BUTTONS. MORE BUTTONS. BRISA\'S MILK TOOTH. A note: DO NOT THROW AWAY, THIS MEANS YOU BRISA.' },
  ],
  'sign.lowtinder_primers': [
    { text: 'WICK-PRIMERS: "Lesson One: the flame is a guest. Lesson Two: never leave a guest alone." Someone has dried the pages one by one.' },
  ],
  'door.lowtinder_garden_dark': [
    { text: 'Pitch dark past the back door. Something green breathes out there. [[A BRIGHTER lamp]] would show the way.' },
  ],
  'sign.lowtinder_garden': [
    { text: 'THE SCHOOL GARDEN. "Plant a light and see what grows." The moss kept the lesson.' },
  ],
  'sign.lowtinder_cellar': [
    { text: 'LAMP-HOUSE STORES. OIL — ROPE — WINTER. BELFRY PIT BELOW: MIND THE BLACK WATER.' },
  ],
};
