/**
 * THE SERE + THE RIO TOWER (2026-11) — Galehigh's dry side: the rain-shadow desert
 * east of the terraces, the old storm-watchers' tower on the rim, and the canyon
 * beyond it, the THOUSANDFOLD (a thousand folds of stone, one for every age the old
 * river cut). Optional, mid-game (band 30-34), off Galehigh's east gap. Builders:
 * tools/maps/build_the_sere.py, build_rio_tower.py; art kit sereforge.py + sere_set.
 *
 * SHIPS SILENTLY (owner's call): never in the changelog, the guide or the website.
 *
 * The lore: Galehigh's terraces catch every cloud that climbs the Windward side, so
 * none are left to rain on the Sere — its storms are DRY, all thunder and lightning
 * and no rain to speak of. The storm-callers stood copper rods across the sand with
 * lamps in their cages, so the summer storms could find their road over the dark
 * land to the canyon; and folk came from all over to eat at the top of the Rio Tower
 * and watch them roll. When the Long Dusk came the callers went home, the rod-lamps
 * went out, and the storms lost their road: they still grumble on the horizon, but
 * they never cross. Relight the three CALLING RODS and the storm walks again.
 *
 * The loop (gamified, all flags):
 *   flag:sere_rod_1..3       a rod relit (vesperlamp) -> FlagStore COUNT_AT_LEAST derives
 *   flag:sere_storm_called   all three lit: the storm has its road
 *   flag:sere_rods_hook      the rods quest begun (sign / Calder / any rod) — JOURNAL
 *   flag:rio_met             Ottoline's hello
 *   flag:rio_dish_1..3       each dish tried once -> derives flag:rio_menu_full
 *   flag:rio_menu_gift       the full-menu gift given
 *   flag:rio_paid            scratch: the `pay` op's outcome for this order
 *   flag:rio_thunder_seen    you've watched the rolling thunder from the Thunder Table
 *   flag:rio_log_signed      Calder wrote it in the Storm Log (his Star-chart)
 *   milagro:emergent         the painted card found on the wet tablecloth (first storm)
 *
 * Prices (the `pay` op) mirror tools/balance/progression.mjs PRICES.rio_* and
 * docs/mechanics/10-economy.md. A meal is a courtesy heal, never a rest point.
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

/** Wicks per dish at the Thunder Table (mirror: progression.mjs PRICES). */
export const RIO_PRICES = { flatbread: 120, stew: 240, supper: 480 } as const;

const OTTO = 'OTTOLINE';
const CALDER = 'CALDER';
const HESK = 'HESK';
const PAID = 'flag:rio_paid';
const CALLED = 'flag:sere_storm_called';
const SEEN = 'flag:rio_thunder_seen';
const HOOK = 'flag:sere_rods_hook';

const o = (text: string): CutsceneStep => ({ op: 'say', speaker: OTTO, text });
const c = (text: string): CutsceneStep => ({ op: 'say', speaker: CALDER, text });

/** One dish off the Thunder Table's slate: pay -> the plate -> the meal's end. */
function order(dish: keyof typeof RIO_PRICES): CutsceneStep[] {
  return [
    { op: 'setFlag', flag: PAID, value: false },
    { op: 'pay', amount: RIO_PRICES[dish], flag: PAID },
    { op: 'run', ref: `script.rio_dish_${dish}`, if_flag: PAID },
    { op: 'run', ref: 'script.rio_meal_end', if_flag: PAID },
    {
      op: 'say',
      speaker: OTTO,
      unless_flag: PAID,
      text: `Short, love? Come back with [[${RIO_PRICES[dish]} wicks]]. The pot's not going anywhere.`,
    },
  ];
}

/** A Calling Rod: relight it (once), then say how many burn. */
function rod(n: 1 | 2 | 3, where: string): ScriptRegistry {
  const flag = `flag:sere_rod_${n}`;
  return {
    [`script.sere_rod_${n}`]: [
      { op: 'run', ref: `script.sere_rod_${n}_lit`, if_flag: flag },
      { op: 'run', ref: `script.sere_rod_${n}_light`, unless_flag: flag },
    ],
    [`script.sere_rod_${n}_lit`]: [
      { op: 'narrate', text: `The ${where} rod's lamp burns steady in its cage, and the copper hums faintly.` },
    ],
    [`script.sere_rod_${n}_light`]: [
      { op: 'narrate', text: `A storm-caller's rod: a copper mast on a cairn, a lamp-cage at the top. The ${where} one. Its wick is cold.` },
      { op: 'narrate', text: 'You open the little cage and hold your vesperlamp to the wick. It takes, slow and blue.' },
      { op: 'sfx', key: 'world-lantern-light' },
      { op: 'setFlag', flag },
      { op: 'setFlag', flag: HOOK },
      { op: 'run', ref: 'script.sere_rods_tally' },
    ],
  };
}

export const SERE_SCRIPTS: ScriptRegistry = {
  // ---- the Calling Rods ----------------------------------------------------------------
  ...rod(1, 'north-west'),
  ...rod(2, 'dry-wash'),
  ...rod(3, 'rim'),
  'script.sere_rods_tally': [
    { op: 'run', ref: 'script.sere_rods_called', if_flag: CALLED },
    { op: 'narrate', text: 'Far off east, something grumbles, low and lost. The other rods still stand dark.', unless_flag: CALLED },
  ],
  'script.sere_rods_called': [
    { op: 'shake', ms: 600, intensity: 0.004 },
    { op: 'sfx', key: 'world-thunder-crack' },
    { op: 'narrate', text: 'Three lamps burn across the Sere. Out on the horizon the thunder answers, long and rolling. The storm has found its road.' },
    { op: 'narrate', text: 'It will cross tonight. Best seat for it: [[the Thunder Table]], at [[the top of the Rio Tower]].' },
  ],

  // ---- the drovers' camp (a rest point) ----------------------------------------------------
  'script.sere_hesk': [
    { op: 'say', speaker: HESK, text: 'Drovers\' rule on the Sere: nobody passes a fire without sitting by it. Sit. Your kin look parched.' },
    { op: 'heal' },
    { op: 'say', speaker: HESK, text: 'We drive the wool-goats down to Galehigh and back. Water\'s in the jars, shade\'s under the wagon.' },
    { op: 'say', speaker: HESK, text: 'The callers\' rods? My gran remembers them lit. Said the storms walked right past our fires to the canyon.', unless_flag: CALLED },
    { op: 'say', speaker: HESK, text: 'You lit the rods, didn\'t you. First proper thunder in years. The goats hate it. I\'ve never been happier.', if_flag: CALLED },
  ],

  // ---- the rim lookout ---------------------------------------------------------------------
  'script.sere_spyglass': [
    { op: 'narrate', text: 'You put your eye to the old brass glass. The Thousandfold opens under you: band on band of stone, rust and bone and violet, stepping down into the dark.' },
    { op: 'narrate', text: 'Far below, a pale thread winds along the bottom. The river that cut all this. Dry now, for longer than anyone remembers.' },
    { op: 'narrate', text: 'Away to the east, a bruise of cloud sits on the horizon, flickering, going nowhere.', unless_flag: CALLED },
    { op: 'narrate', text: 'Away to the east, the storm shelf is moving now, slow and certain, rolling this way.', if_flag: CALLED },
  ],
  'script.sere_surveyor': [
    { op: 'say', speaker: 'LIO', text: 'Count the bands, if you like. I\'ve got to nine hundred and forty. Each one\'s an age of the old river, laid down and cut through.' },
    { op: 'say', speaker: 'LIO', text: 'The drovers call it the Thousandfold. I\'m trying to find out if they\'re right. I suspect they rounded up.' },
    { op: 'say', speaker: 'LIO', text: 'The tower\'s named for that river, you know: the Rio. Went underground ages ago. Now only the storms come down the canyon.' },
  ],

  // ---- the route trainers ----------------------------------------------------------------------
  'script.sere_runner': [
    { op: 'say', speaker: 'TAVI', text: 'Kite-runner! I sail the dunes on a ground-kite when the wind\'s up. Today it isn\'t. So: a bout!' },
    { op: 'battle', trainer: 'sere_runner' },
    { op: 'say', speaker: 'TAVI', text: 'Blown flat! If you\'re after the callers\' rods, one\'s [[behind the scrub, north-west]].' },
    { op: 'setFlag', flag: 'flag:sere_runner_beaten' },
  ],
  'script.sere_chaser': [
    { op: 'say', speaker: 'BRANNOCK', text: 'Storm-chaser. I chase them, they never come. Thirty years. Fancy a fight while we wait?' },
    { op: 'battle', trainer: 'sere_chaser' },
    { op: 'say', speaker: 'BRANNOCK', text: 'Ha! There\'s a rod down [[in the wash]] behind me. Light it, would you? I\'d like to see one before I\'m done.' },
    { op: 'setFlag', flag: 'flag:sere_chaser_beaten' },
  ],
  'script.rio_chaser': [
    { op: 'say', speaker: 'ESME', text: 'Up for the Thunder Table? So am I. Every night. A bout while you climb — it passes the time!' },
    { op: 'battle', trainer: 'rio_chaser' },
    { op: 'say', speaker: 'ESME', text: 'Good kin. Go on up. Ottoline\'s stew is worth the stairs, storm or no storm.' },
    { op: 'setFlag', flag: 'flag:rio_chaser_beaten' },
  ],

  // ---- caches ------------------------------------------------------------------------------
  'script.pickup_sere_beacon': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'Wedged in a cairn, a caller\'s tin, still sealed. Inside: a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_sere_beacon' },
  ],
  'script.pickup_sere_balm': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'A drover\'s saddle-bag, dropped in the wash. Two WARM BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_sere_balm' },
  ],
  'script.pickup_sere_wicks': [
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: 'A wick-purse in the scrub, gone stiff with dust. 300 wicks.' },
    { op: 'setFlag', flag: 'flag:picked_sere_wicks' },
  ],

  // ---- the Rio Tower: the foot and the watch -------------------------------------------------
  'script.rio_porter': [
    { op: 'say', speaker: 'AMSEL', text: 'Welcome to the Rio Tower! Up the stairs, all the way, for [[the Thunder Table]]. Best supper on the rim.' },
    { op: 'say', speaker: 'AMSEL', text: 'Storms? Not for years, love. They grumble out east and never cross. Ask [[Calder, one floor up]]. He keeps the log.', unless_flag: CALLED },
    { op: 'say', speaker: 'AMSEL', text: 'Did you hear it out there? The storm\'s coming! Get up those stairs and get a seat by the window!', if_flag: CALLED },
  ],
  // a precedence chain (latest stage first): exactly one stage plays for any flag mix
  'script.rio_calder': [
    { op: 'run', ref: 'script.rio_calder_after', if_flag: 'flag:rio_log_signed' },
    { op: 'run', ref: 'script.rio_calder_unsigned', unless_flag: 'flag:rio_log_signed' },
  ],
  'script.rio_calder_unsigned': [
    { op: 'run', ref: 'script.rio_calder_sign', if_flag: SEEN },
    { op: 'run', ref: 'script.rio_calder_unseen', unless_flag: SEEN },
  ],
  'script.rio_calder_unseen': [
    { op: 'run', ref: 'script.rio_calder_waiting', if_flag: CALLED },
    { op: 'run', ref: 'script.rio_calder_hook', unless_flag: CALLED },
  ],
  'script.rio_calder_hook': [
    c('Calder Voss, last of the storm-watchers. That book is the Storm Log. Two hundred years of storms, and then... nothing.'),
    c('The callers had three copper rods out on the Sere, lamps in their cages, so the storms could find their road across the dark.'),
    c('The lamps went out with the Long Dusk. Light [[the three rods]] with that lamp of yours, and I\'ll have something to write again.'),
    { op: 'setFlag', flag: HOOK },
  ],
  'script.rio_calder_waiting': [
    c('All three rods! I heard it roll. Don\'t stand here with me — get up to [[the Thunder Table]] and order something. That\'s the custom.'),
  ],
  'script.rio_calder_sign': [
    c('You watched it from the Table? Every band of the canyon lit up? Then it goes in the Log, in your name.'),
    { op: 'narrate', text: 'Calder writes, slow and careful, and blots it. Beside your name he draws a small lightning bolt.' },
    c('Two hundred years we kept this. Take this. The callers left it for whoever brought the storms back.'),
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'chart_thunder_kick', count: 1 },
    { op: 'say', text: 'Got a STAR-CHART: THUNDER KICK!' },
    { op: 'setFlag', flag: 'flag:rio_log_signed' },
  ],
  'script.rio_calder_after': [
    c('Storm on the Log again. You can watch it any night: order at the Table and she comes rolling.'),
    c('Mira Vael used to sit on those stairs as a girl, counting the seconds between flash and roll. That\'s where it started for her.'),
  ],
  'script.rio_storm_log': [
    { op: 'narrate', text: 'THE STORM LOG. Columns of dates, flash-to-roll counts, little drawn bolts. Then a page that just says "No storm."' },
    { op: 'narrate', text: 'Then hundreds of pages more, every one the same. "No storm." "No storm." "No storm."', unless_flag: SEEN },
    { op: 'narrate', text: 'And at the very end, in fresh ink: a storm, a long roll, and your name beside a small lightning bolt.', if_flag: 'flag:rio_log_signed' },
  ],

  // ---- the Thunder Table ----------------------------------------------------------------------
  'script.rio_ottoline': [
    { op: 'run', ref: 'script.rio_hello', unless_flag: 'flag:rio_met' },
    {
      op: 'choice',
      speaker: OTTO,
      prompt: 'What can I bring you?',
      options: [
        { label: `OCHRE FLATBREAD ${RIO_PRICES.flatbread}W`, ops: order('flatbread') },
        { label: `THUNDER STEW ${RIO_PRICES.stew}W`, ops: order('stew') },
        { label: `THE RIO SUPPER ${RIO_PRICES.supper}W`, ops: order('supper') },
        { label: 'ABOUT THE STORMS', ops: [{ op: 'run', ref: 'script.rio_about' }] },
        { label: 'JUST LOOKING', ops: [o('Look all you like. The view\'s free. The food isn\'t.')] },
      ],
    },
  ],
  'script.rio_hello': [
    { op: 'narrate', text: 'Lamplight, woodsmoke and spice. A broad woman in a flour-dusted apron leans on the pass, under the slate.' },
    o('Ottoline Bask. Welcome to the Thunder Table: the highest supper in Vesperholm, and the best view of the Thousandfold.'),
    o('Folk used to queue down the stairs on storm nights. Now it\'s the quiet ones, and the drovers. Sit anywhere.'),
    { op: 'setFlag', flag: 'flag:rio_met' },
  ],
  'script.rio_about': [
    o('Storms come up out of the east, dry as bone, and roll right across the Sere to the canyon. Thunder you feel in your teeth.'),
    { op: 'say', speaker: OTTO, text: 'Or they did. The rods went dark and the storms lost their road.', unless_flag: CALLED },
    { op: 'say', speaker: OTTO, text: 'Calder says if somebody lit [[the callers\' rods]], they\'d find their way again. Somebody with a lamp. Hint, hint.', unless_flag: CALLED },
    { op: 'say', speaker: OTTO, text: 'And now they\'re back! Order something and sit by the window. She\'ll come when you\'re settled. She always did.', if_flag: CALLED },
  ],
  'script.rio_dish_flatbread': [
    { op: 'narrate', text: 'Flatbread straight off the hot stone, blistered and ochre with toasted spice, and a pot of tart red thornberry jam.' },
    o('Thornberries grow in the scrub out there. The drovers pick them on the way past, and pay me in jam.'),
    { op: 'setFlag', flag: 'flag:rio_dish_1' },
  ],
  'script.rio_dish_stew': [
    { op: 'narrate', text: 'A clay bowl of dark bean-and-root stew, smoky and slow, with a heel of bread to chase the last of it.' },
    o('Thunder Stew. On storm nights we\'d bang the lids when the roll came. That\'s the only reason for the name.'),
    { op: 'setFlag', flag: 'flag:rio_dish_2' },
  ],
  'script.rio_dish_supper': [
    { op: 'narrate', text: 'The whole table fills: flatbread, stew, roast squash with honey and chilli, salted goat\'s cheese, and a slab of date cake.' },
    o('The Rio Supper. A bit of everything, the way the storm-callers ate before a long night out on the sand.'),
    { op: 'setFlag', flag: 'flag:rio_dish_3' },
  ],
  // every plate: a courtesy heal (never a rest point), then the sky decides
  'script.rio_meal_end': [
    { op: 'heal', rest: false, sleep: false },
    { op: 'say', text: 'Warm and full. Your kin lick the bowls clean and settle by your feet.' },
    { op: 'run', ref: 'script.rio_quiet_sky', unless_flag: CALLED },
    { op: 'run', ref: 'script.rio_thunder', if_flag: CALLED },
    { op: 'run', ref: 'script.rio_menu_gift', if_flag: 'flag:rio_menu_full', unless_flag: 'flag:rio_menu_gift' },
  ],
  'script.rio_quiet_sky': [
    { op: 'narrate', text: 'Out past the windows the Sere lies dark. A bruise of cloud flickers far off east. It never comes any closer.' },
    o('No storm again. Calder says it\'s [[the callers\' rods]]. Three of them, out on the sand, gone dark.'),
    { op: 'setFlag', flag: HOOK },
  ],
  // THE ROLLING THUNDER — the scene the tower was built for
  'script.rio_thunder': [
    { op: 'letterbox', on: true },
    { op: 'narrate', text: 'You take your bowl to the window seat. Out east, a low line of cloud is coming, flickering from inside.' },
    o('Here she comes. Lids ready, everybody.'),
    { op: 'musicFade', ms: 900 },
    {
      op: 'frames',
      frames: [
        'assets/backgrounds/cinematic/thunder-1.webp',
        'assets/backgrounds/cinematic/thunder-2.webp',
        'assets/backgrounds/cinematic/thunder-3.webp',
        'assets/backgrounds/cinematic/thunder-4.webp',
        'assets/backgrounds/cinematic/thunder-5.webp',
        'assets/backgrounds/cinematic/thunder-6.webp',
      ],
      holdMs: 1600,
      fadeMs: 700,
      flash: [2, 4],
      sfx: 'world-thunder-roll',
      flashSfx: 'world-thunder-crack',
    },
    { op: 'narrate', text: 'The roll goes on and on, from one end of the Thousandfold to the other, and every lid in the room bangs with it.' },
    { op: 'narrate', text: 'Above the storm\'s tail, the Storm\'s own stars burn steady. It knows its road now.', if_flag: 'gleam:storm' },
    { op: 'narrate', text: 'The storm rolls on north, grumbling, and the stars come out over the wet sand.' },
    { op: 'run', ref: 'script.rio_thunder_first', unless_flag: SEEN },
    { op: 'letterbox', on: false },
    { op: 'music', key: 'inn-rest' },
  ],
  'script.rio_thunder_first': [
    o('Oh, that\'s what I missed. Years of it. Thank you, love.'),
    { op: 'narrate', text: 'When the rain on the window clears, there is a little painted card stuck to the wet tablecloth, face up. Nobody at the Table will own it.' },
    { op: 'milagroCard', card: 'emergent' },
    o('Blown in on the storm, I expect. Keep it. And [[tell Calder]], one floor down: this goes in his Log.'),
    { op: 'setFlag', flag: SEEN },
  ],
  // all three dishes tried: the regular's gift
  'script.rio_menu_gift': [
    o('Flatbread, stew AND the Supper? You\'re a regular now. Regulars get the callers\' charges. We kept a box.'),
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'Got 2 BEACON CHARGES!' },
    { op: 'setFlag', flag: 'flag:rio_menu_gift' },
  ],
  'script.rio_window': [
    { op: 'narrate', text: 'The great windows look out over the Thousandfold: band on band of stone, rust and bone and violet, falling into the dark.' },
    { op: 'narrate', text: 'Far off east, a bruise of cloud flickers on the horizon and goes nowhere.', unless_flag: CALLED },
    { op: 'narrate', text: 'Far off east, the storm shelf is moving. Order something, and sit. It will come.', if_flag: CALLED },
  ],
};

export const SERE_DIALOGUE: DialogueRegistry = {
  'sign.sere_welcome': [
    { text: 'THE SERE\nGalehigh\'s dry side. EAST: [[the Rio Tower]] and the canyon rim.' },
    { text: 'Burnt into the board: "Carry water. Mind the edge. Don\'t argue with the goats."' },
  ],
  'sign.sere_rio_tower': [
    { text: 'THE RIO TOWER\n[[The Thunder Table]] at the top. Suppers served dusk till late.' },
  ],
  'sign.sere_rods': [
    { text: 'THE CALLERS\' ROAD\nThree rods stand on the Sere. Keep their lamps lit and [[the storms will find their way]].' },
    { text: 'Someone has scratched under it: "Nobody has, for years."' },
  ],
  'sign.sere_wash': [
    { text: 'THE DRY WASH\nWhen it rains, this is a river for an hour. It has not rained.' },
  ],
  'sign.galehigh_to_sere': [
    { text: 'EAST: THE SERE. The drovers\' track to [[the Rio Tower]].' },
  ],
  'npc.sere_drover_kid': [
    { text: 'DROVER\'S KID: I\'ve never heard proper thunder. Gran says it shakes your teeth. I want my teeth shook.' },
  ],
  'npc.sere_runner_after': [{ text: 'TAVI: No wind. No wind for days. I\'m going to start blowing on the kite myself.' }],
  'npc.sere_chaser_after': [{ text: 'BRANNOCK: Thirty years watching that horizon. Still here. Still watching.' }],
  'npc.rio_chaser_after': [{ text: 'ESME: Every night I climb up here. One of these nights, it\'ll be worth it.' }],
  'npc.rio_drover': [
    { text: 'DROVER: Down off the terraces with the wool-goats. They get the Sere, I get Ottoline\'s stew. Fair trade.' },
  ],
  'npc.rio_diner_a': [
    { text: 'DINER: We came up for the view. Then we came back for the stew. Then we just kept coming back.' },
  ],
  'npc.rio_diner_b': [
    { text: 'STAR-WATCHER: The canyon\'s best just after a storm. The wet stone shines like the stars are down there too.' },
  ],
  'sign.rio_plaque': [
    { text: 'THE RIO TOWER\nRaised by the storm-callers on the rim of the Thousandfold, and named for the river that cut it.' },
    { text: 'Below, in smaller letters: "Supper at the top. Storms at no extra charge."' },
  ],
  'sign.rio_barometer': [
    { text: 'A storm-glass. The needle has sat at FAIR so long it has rusted there.' },
  ],
};
