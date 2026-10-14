/**
 * THE FARLAMP ISLES (2026-10, docs/world/walkthrough/10-the-farlamp-isles.md Part I),
 * lane C2 — the UNDERTIDE (the four sea-cave floors under the isles) and THE DROWNED
 * LAMP (the relight, the isles' own dawn, Farlume). This lane OWNS this file: new
 * scripts + dialogue only, spread into the registries via regions/index.ts.
 *
 * Maps: undertide_i (the mouth, under Gullwrack), undertide_ii (the Kelp Vaults,
 * Gullwrack <-> Kelpcrown), undertide_iii (the Bell Galleries, from Driftholm's
 * well-stair), undertide_iv (the Drowned Stair), farlamp_drowned (the lamp-room).
 * Builders: tools/maps/build_undertide_*.py, build_farlamp_drowned.py (undertidekit).
 *
 * The keeper: KEEPER EDDA MARROW kept the Farlamp the night the deep came up, eleven
 * winters ago (story-bible §12). She sent Driftholm's boats home, kept the lamp as
 * long as it would burn, and went up the long stair with a small lamp. Her four
 * logbook pages are "The Keeper's Log" — read in order they tell the night; read out
 * of order they still make sense. Never grim: she is never said to have drowned.
 *
 * Flags this file owns:
 *   flag:undertide_bell_mouth / _vaults           the teaching bells (I, II)
 *   flag:undertide_bell_harbour / _shoal / _deep  the Bell Galleries' three (III)
 *   flag:undertide_bell_tmp                       transient: a bell's previous state
 *   flag:undertide_tune_1 / _2 / _tmp             the old-order peal, part-rung
 *   flag:q_isles_bells_tuned                      "Tide-bell Tuning" done (the shortcut)
 *   flag:isles_log_begun, flag:isles_log_1..4      the Keeper's Log pages read
 *   flag:undertide_bells_heard                    any tide-bell rung (the journal's hook)
 *   flag:q_isles_fogglass                         the fog-glass taken (I4)
 *   flag:isles_dawn, flag:q_isles_done            the relight (I6)
 *   flag:farlume_met, flag:farlume_caught         Farlume (I7)
 *   flag:picked_*                                 caches (+ the two dawn islets, III/IV)
 * After `flag:isles_dawn` (pass 2): the tide-lamps light, the day-form tables
 * swap in, Ondine dives the stair (a re-runnable bout), Edda waits by the lamp.
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

const DAWN = 'flag:isles_dawn';
const TMP = 'flag:undertide_bell_tmp';
const TUNED = 'flag:q_isles_bells_tuned';
const T1 = 'flag:undertide_tune_1';
const T2 = 'flag:undertide_tune_2';
const TT = 'flag:undertide_tune_tmp';
const CAUGHT = 'flag:farlume_caught';

/** A tide-bell: flips its flag (via a transient copy, so the two guarded setFlags
 *  can't both fire), rings, and says which way the race at its junction now runs. */
function bell(flag: string, name: string, swung: string, still: string): CutsceneStep[] {
  return [
    { op: 'setFlag', flag: 'flag:undertide_bells_heard' },
    { op: 'setFlag', flag: TMP, if_flag: flag },
    { op: 'setFlag', flag, unless_flag: TMP },
    { op: 'setFlag', flag, value: false, if_flag: TMP },
    { op: 'sfx', key: 'world-moorbell' },
    { op: 'shake', ms: 180, intensity: 0.0015 },
    { op: 'narrate', if_flag: flag, text: `You swing the ${name}. Its note goes out over the surge — and out at the junction, ${swung} The race-post there shows RED.` },
    { op: 'narrate', unless_flag: flag, text: `You ring the ${name} back to rest. Out at the junction, ${still} The race-post there shows WHITE.` },
    { op: 'setFlag', flag: TMP, value: false },
  ];
}

function find(flag: string, gives: CutsceneStep[], text: string): CutsceneStep[] {
  return [{ op: 'sfx', key: 'world-pickup' }, ...gives, { op: 'say', text }, { op: 'setFlag', flag }];
}

function diver(id: string, name: string, before: string, after: string): CutsceneStep[] {
  return [
    { op: 'say', speaker: name, text: before },
    { op: 'battle', trainer: id },
    { op: 'say', speaker: name, text: after },
    { op: 'setFlag', flag: `flag:${id}_beaten` },
  ];
}

/** A logbook page: read it (always), mark it read (first time). */
function page(n: number, lines: string[]): CutsceneStep[] {
  return [
    { op: 'sfx', key: 'world-chart' },
    { op: 'narrate', text: `A sea-chest, barnacled shut, and on its lid a logbook swollen with damp. Most of it has run to blue. One page still reads. THE FARLAMP LOG — page ${n} of the last night.` },
    ...lines.map((text): CutsceneStep => ({ op: 'say', speaker: 'KEEPER EDDA MARROW', text })),
    { op: 'setFlag', flag: 'flag:isles_log_begun' },
    { op: 'setFlag', flag: `flag:isles_log_${n}` },
  ];
}

const HARBOUR = 'flag:undertide_bell_harbour';
const SHOAL = 'flag:undertide_bell_shoal';
const DEEP = 'flag:undertide_bell_deep';

export const UNDERTIDE_SCRIPTS: ScriptRegistry = {
  // ---- the teaching bells (I, II) ------------------------------------------------
  'script.undertide_bell_mouth': bell('flag:undertide_bell_mouth', 'mouth bell',
    'the race swings EAST, toward the ladder ledge.', 'the race settles back WEST, toward the keeper\'s ledge.'),
  'script.undertide_bell_vaults': bell('flag:undertide_bell_vaults', 'vault bell',
    'the race turns WEST, round the corner onto the island.', 'the race runs EAST again, to this vault.'),

  // ---- the Bell Galleries: three bells + the old-order peal (Tide-bell Tuning) ----
  // The old order is the way the tide comes in: DEEP, then SHOAL, then HARBOUR,
  // nothing rung between. T1 = the Deep has opened the peal; T2 = the Shoal answered.
  'script.undertide_bell_deep': [
    ...bell(DEEP, 'DEEP bell', 'the north race turns EAST, to the stair gallery.', 'the north race drops SOUTH again, to the keeper\'s ledge.'),
    { op: 'setFlag', flag: T1, unless_flag: TUNED },
    { op: 'setFlag', flag: T2, value: false },
  ],
  'script.undertide_bell_shoal': [
    ...bell(SHOAL, 'SHOAL bell', 'the west race turns EAST, up to the diver\'s gallery.', 'the west race runs NORTH again, to the deep bell.'),
    { op: 'setFlag', flag: TT, if_flag: T1, unless_flag: T2 },
    { op: 'setFlag', flag: T1, value: false, unless_flag: TT },
    { op: 'setFlag', flag: T2, value: false, unless_flag: TT },
    { op: 'setFlag', flag: T2, if_flag: TT },
    { op: 'narrate', if_flag: TT, text: 'The Shoal\'s note doesn\'t die away. It hangs under the Deep\'s, the two of them humming together, waiting.' },
    { op: 'setFlag', flag: TT, value: false },
  ],
  'script.undertide_bell_harbour': [
    ...bell(HARBOUR, 'HARBOUR bell', 'the landing race turns NORTH, to the keeper\'s ledge.', 'the landing race runs WEST again, to the shoal bell.'),
    { op: 'setFlag', flag: TT, if_flag: T2, unless_flag: TUNED },
    { op: 'setFlag', flag: TUNED, if_flag: TT },
    { op: 'setFlag', flag: T1, value: false },
    { op: 'setFlag', flag: T2, value: false },
    { op: 'run', ref: 'script.undertide_tuned', if_flag: TT },
    { op: 'setFlag', flag: TT, value: false },
  ],
  'script.undertide_tuned': [
    { op: 'silence', ms: 700 },
    { op: 'tint', color: '#9fe8e0', alpha: 0.22, ms: 600 },
    { op: 'narrate', text: 'Deep. Shoal. Harbour. The three notes meet in the dark and ring TRUE — one long chord rolling out across the galleries, the way the tide comes in.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'shake', ms: 500, intensity: 0.003 },
    { op: 'narrate', text: 'Far off by the north-east wall, something heavy turns over in the water. A race that has slept eleven winters wakes and runs, fast and sure, toward the well-stair.' },
    { op: 'tint', color: '#9fe8e0', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'And on the landing below, where the bell-ringers used to sit, a tin box you never noticed glints in the wet.' },
    { op: 'narrate', text: 'All through the Undertide, old races stir. Somewhere up near the mouth, a lane to the bell-ringers\' islet has woken too.' },
  ],

  // ---- the Keeper's Log ----------------------------------------------------------
  'script.undertide_log_1': page(1, [
    'Dusk came in at the usual hour. It did not go out again. By the ninth bell there was no grey in the east at all, and the sea had a sound I have not heard in thirty years of keeping. A low sound. Like the floor of the world breathing in.',
    'Lit the great lamp an hour early and set the small ones in the gallery. If ever a night wanted a light, it\'s this one.',
  ]),
  'script.undertide_log_2': page(2, [
    'The deep came up at midnight. Not a wave: the whole sea, a fathom higher and still rising. The Sound\'s boats came running in under my light. I sent every one on to Driftholm, kelp-wives, children and all. Told them to keep small lamps till morning.',
    'The fog closed behind them. I\'ve left my fog-glass on its stand in the vaults. Whoever comes after me, take it: the buoy lane through the Fogwall reads true through it, and the town will want visitors.',
  ]),
  'script.undertide_log_3': page(3, [
    'The water is in the galleries. I rang the bells so the races would carry me, and I rang them wrong, of course, in a hurry. The old keepers hung them to tell the tide\'s order.',
    'Ring them the way the tide comes in, they used to say: the DEEP first, then the SHOAL, then the HARBOUR, and nothing between. The Driftholm children skip to it. "Deep calls, shoal answers, harbour brings them home."',
  ]),
  'script.undertide_log_4': page(4, [
    'The water is on the stair. She is still burning down there, my lamp, a fathom under the sea, lighting fish. I\'ve never seen anything so stubborn or so lovely.',
    'I\'ve put the things that matter in the store and run the sluice shut. Its wheel is on the bell-post: turn it toward the lamp and the race will carry you in.',
    'I\'m going up the long way now, with a small lamp. If you are reading this, the morning is coming back somewhere. Light her again for me.',
  ]),

  // ---- the fog-glass (I4) --------------------------------------------------------
  'script.undertide_fogglass': [
    { op: 'narrate', if_flag: 'flag:q_isles_fogglass', text: 'The stand\'s brass cradle is empty, polished bright where the lens sat. A little ring of clean stone shows how long it waited.' },
    { op: 'run', ref: 'script.undertide_fogglass_take', unless_flag: 'flag:q_isles_fogglass' },
  ],
  'script.undertide_fogglass_take': [
    { op: 'narrate', text: 'On a stone stand in the middle of the island, out of reach of the surge: a lens in a brass ring, glowing faintly to itself, like a coin of moonlight somebody forgot to spend.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'fog_glass', count: 1 },
    { op: 'setFlag', flag: 'flag:q_isles_fogglass' },
    { op: 'say', text: 'You take the keeper\'s FOG-GLASS. Held to your eye, the dark in the vaults goes thin and grey, and the far wall shows through it.' },
    { op: 'narrate', text: 'Out on the open sea, the Fogwall\'s buoys will read true through this. Driftholm is waiting on the other side.' },
  ],

  // ---- the keeper's ledge (III): the rest point ------------------------------------
  'script.undertide_camp_rest': [
    { op: 'narrate', text: 'The keeper\'s dry ledge: a crate, a rolled oilskin bed, a kettle on three stones. Somebody laid a fire here and never lit it. You light it.' },
    { op: 'heal' },
    { op: 'narrate', text: 'You wake to the bells humming in the dark and the kettle ticking as it cools. Your kin are curled warm against the crate. Rested.' },
  ],

  // ---- caches ------------------------------------------------------------------
  'script.pickup_undertide_i_coal': find('flag:picked_undertide_i_coal', [{ op: 'giveItem', item: 'hearth_coal', count: 1 }],
    'In a tin by the keeper\'s pool, wrapped in oilcloth and still faintly warm: a HEARTH COAL!'),
  'script.pickup_undertide_i_islet': find('flag:picked_undertide_i_islet', [{ op: 'giveItem', item: 'starglass_shard', count: 1 }],
    'On the little islet in the surge, where the bell-ringers used to row out to listen: a tin box, and in it a STARGLASS SHARD — a warm fall from long before the Dusk.'),
  'script.pickup_undertide_ii_drop': find('flag:picked_undertide_ii_drop', [{ op: 'giveItem', item: 'lumen_drop', count: 1 }],
    'Behind the vault bell, in a niche cut for a lamp: a little jar of light. Found a LUMEN DROP!'),
  'script.pickup_undertide_iii_nw': find('flag:picked_undertide_iii_nw', [{ op: 'giveItem', item: 'beacon_charge', count: 2 }],
    'Under the Deep bell\'s post, a bell-ringer\'s satchel. Found 2 BEACON CHARGES!'),
  'script.pickup_undertide_iii_dg': find('flag:picked_undertide_iii_dg', [{ op: 'giveItem', item: 'bright_balm', count: 2 }],
    'A diver\'s kit-roll, tied to a ring in the rock. Found 2 BRIGHT BALMS!'),
  'script.pickup_undertide_iii_eg': find('flag:picked_undertide_iii_eg', [{ op: 'giveItem', item: 'glow_charge', count: 3 }],
    'A net-hand\'s float-box, snagged on the rocks. Found 3 GLOW CHARGES!'),
  'script.pickup_undertide_tuned': find('flag:picked_undertide_tuned', [{ op: 'giveItem', item: 'lumen_drop', count: 1 }],
    'The bell-ringers\' tin, on the landing where they sat to listen. Inside, on a bed of dry wrack, a LUMEN DROP — and a scrap of paper in a child\'s hand: "DEEP CALLS".'),
  'script.pickup_undertide_iv_coal': find('flag:picked_undertide_iv_coal', [{ op: 'giveItem', item: 'hearth_coal', count: 1 }],
    'On the west landing, a keeper\'s fire-pot with its lid wired down. A HEARTH COAL, still glowing!'),
  'script.pickup_undertide_purse': [
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: 2000 },
    { op: 'say', text: 'In the west nook, tucked in a crack above the tide-line: the keeper\'s purse, eleven winters of Farlamp pay never spent. Found 2,000 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_undertide_purse' },
  ],
  'script.pickup_undertide_iv_drop': find('flag:picked_undertide_iv_drop', [{ op: 'giveItem', item: 'lumen_drop', count: 1 }],
    'At the back of the east nook, set in the rock where the light from the stair-foot reaches: a LUMEN DROP!'),
  'script.pickup_farlamp_store_chart': find('flag:picked_farlamp_store_chart', [{ op: 'giveItem', item: 'chart_maelstrom', count: 1 }],
    'In the keeper\'s store, dry as a cupboard, rolled in waxed silk: the Farlamp\'s own sea-chart, the one they used to teach the boats by. A STAR-CHART: MAELSTROM!'),

  // ---- trainers ------------------------------------------------------------------
  'script.undertide_diver_ness': diver('undertide_diver_ness', 'NESS',
    'A boat! Out here! Then the fog really is — never mind, battle first, ask after. I dive the mouth for lamp-glass and I\'m not losing my spot.',
    'The races carry you, they don\'t ask. Ring the mouth bell on the landing and see which way they change their mind.'),
  'script.undertide_diver_corin': diver('undertide_diver_corin', 'CORIN',
    'This is the bell vault, and that\'s my bell, and I\'ve been ringing it for practice. You can have a turn when you\'ve had a battle.',
    'There\'s a lens on the island, sat on a stand, glowing at nothing. My nan says it was the keeper\'s. Ring the bell and ride back round.'),
  'script.undertide_nethand_bryn': diver('undertide_nethand_bryn', 'BRYN',
    'You came by the races, didn\'t you? Nobody walks to the east gallery. Nobody leaves without a bout, either.',
    'The galleries sang once, when they were rung true. My gran could do it. Deep first, she\'d say, and then the rest come in on their own.'),
  'script.undertide_keeper_isolde': diver('undertide_keeper_isolde', 'ISOLDE',
    'I was the Farlamp\'s second keeper, the night it went. I came down the long stair to see if she\'d left anything burning. Let me see what you carry first.',
    'You\'ve the Star-tender\'s light in that lamp. I can see it from here. Go on down, then. Edda would want it to be you.'),
  'script.undertide_diver_marlo': diver('undertide_diver_marlo', 'MARLO',
    'The Drowned Stair. Every race goes down, and the long one goes all the way back up. I\'ve ridden it eighty times today. Battle?',
    'Below the stair-foot there\'s air, and stone, and the lamp. Don\'t mind the fish. They\'ve been keeping her company.'),

  // ---- the Drowned Lamp: the relight (I6) + Farlume (I7) ---------------------------
  'script.farlamp_lamp': [
    { op: 'narrate', if_flag: DAWN, text: 'The Farlamp burns, steady and warm, a fathom under the sea. Fish hang in its light like moths. Far above, the isles are having their morning.' },
    { op: 'run', ref: 'script.farlamp_relight', unless_flag: DAWN },
  ],
  'script.farlamp_relight': [
    { op: 'letterbox', on: true },
    { op: 'silence', ms: 1100 },
    { op: 'narrate', text: 'The great lamp lies where it fell, on the floor of its own tower. Its glass has gone sea-green. Weed hangs from the gallery rail. At its heart the wick is black and cold, and the whole room is waiting for something.' },
    { op: 'narrate', text: 'In your vesperlamp burns the flame Star-tender Fenn lit at the skiff\'s prow, lit in turn from the Keystar. The deep answers a lamp lit from the Keystar\'s light.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd890', alpha: 0.3, ms: 700 },
    { op: 'narrate', text: 'You set your flame to the old wick. It takes slowly, the way a sleeper wakes. Then the lens catches it, and the light goes everywhere at once.' },
    { op: 'setFlag', flag: DAWN },
    { op: 'setFlag', flag: 'flag:q_isles_done' },
    { op: 'flashColor', color: '#fff2c8', ms: 500 },
    { op: 'shake', ms: 600, intensity: 0.003 },
    { op: 'musicCrossfade', key: 'farlamp-relit', ms: 1200 },
    { op: 'narrate', text: 'THE FARLAMP BURNS. Its beam goes up through a fathom of water and out across the sea, and the Fogwall, which has lain on these isles eleven winters, begins to lift.' },
    { op: 'tint', color: '#ffd890', alpha: 0, ms: 1100 },
    { op: 'narrate', text: 'All the way up the Undertide, the keepers\' tide-lamps flicker on along the races, one after another, like a held breath let go.' },
    { op: 'narrate', text: 'Up in Driftholm they will be at their windows with their small lamps. They will see the old light out on the water. Some of them will cry, and say it\'s the salt.' },
    { op: 'narrate', text: 'No new star rises for this. It isn\'t that kind of light. It is the isles\' own morning, and it\'s enough.' },
    { op: 'letterbox', on: false },
    // I7 — Farlume rises in the new light
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'In the ring of water round the room, something answers the beam. A shape comes up through the light — finned, lantern-bellied, gold as the lamp — and turns to look at you with the patience of something that kept watch here alone.' },
    { op: 'setFlag', flag: 'flag:farlume_met' },
    { op: 'musicSting', key: 'sting-hour' },
    { op: 'music', key: 'battle-hours' },
    {
      op: 'legendaryBattle',
      name: 'farlume',
      kin: 177,
      level: 68,
      caughtFlag: CAUGHT,
      cooldownBattles: 12,
      cooldownRef: 'npc.farlume_resting',
      terrain: 'water',
    },
    { op: 'run', ref: 'script.farlume_caught' },
  ],
  'script.farlume_wake': [
    { op: 'narrate', text: 'FARLUME drifts in the lamp\'s light by the water\'s edge, gold through and through. It watches your vesperlamp the way a keeper watches a boat come in.' },
    { op: 'musicSting', key: 'sting-hour' },
    { op: 'music', key: 'battle-hours' },
    {
      op: 'legendaryBattle',
      name: 'farlume',
      kin: 177,
      level: 68,
      caughtFlag: CAUGHT,
      cooldownBattles: 12,
      cooldownRef: 'npc.farlume_resting',
      terrain: 'water',
    },
    { op: 'run', ref: 'script.farlume_caught' },
  ],
  'script.farlume_caught': [
    { op: 'silence', ms: 1000 },
    { op: 'narrate', text: 'Farlume comes into your lamp like a boat into harbour: slowly, sure of the way. Your vesperlamp burns a shade warmer, and does not go back.' },
    { op: 'musicCrossfade', key: 'farlamp-relit', ms: 1400 },
    { op: 'narrate', text: 'The Farlamp keeps burning without it. It never needed watching once it was lit. It only needed someone to come all the way down.' },
  ],

  // ---- pass 2: the rest before the lamp, the dawn's islets, Ondine, Edda ---------
  // IV's stair-foot niche: the floor's REST POINT, a bed before the Drowned Lamp.
  'script.undertide_niche_rest': [
    { op: 'narrate', text: 'A keeper\'s niche cut into the rock above the tide-line: a bunk, a blue blanket gone stiff with salt, a little lamp on a hook. Dry as a cupboard.' },
    { op: 'heal' },
    { op: 'narrate', text: 'You sleep to the sound of the up-race, and wake rested. Your kin are warm in the blanket. Somewhere below, the lamp-room waits.' },
  ],
  'script.pickup_undertide_iii_dawn': find('flag:picked_undertide_iii_dawn', [{ op: 'giveItem', item: 'starglass_shard', count: 1 }],
    'The little islet the race never used to reach. Tucked in the rock, where the new light falls on it: a STARGLASS SHARD, warm as a hand.'),
  'script.pickup_undertide_iv_dawn': find('flag:picked_undertide_iv_dawn', [{ op: 'giveItem', item: 'beacon_charge', count: 3 }],
    'The dawn race carried you to an islet halfway down the stair. A keeper\'s spare-box, wired to a ring. Found 3 BEACON CHARGES!'),
  // After the dawn: Ondine dives the Drowned Stair for the joy of it and races
  // anyone who'll have her. A re-runnable bout (she never stands on a sight-line).
  'script.undertide_diver_ondine': [
    { op: 'say', speaker: 'ONDINE', text: 'You lit her! You lit the Farlamp! I came straight down the well-stair to see. Every race in the Undertide is running warm.' },
    {
      op: 'choice', speaker: 'ONDINE', prompt: 'Fancy a bout, while the lamps are lit?',
      options: [
        { label: 'A bout', ops: [
          { op: 'battle', trainer: 'undertide_rematch_ondine' },
          { op: 'say', speaker: 'ONDINE', text: 'Ha! Again tomorrow. I\'ll be here. I\'m always going to be here now.' },
        ] },
        { label: 'Not now', ops: [
          { op: 'say', speaker: 'ONDINE', text: 'Suit yourself. The races\'ll keep.' },
        ] },
      ],
    },
  ],
  // The old keeper, come down the long stair once the light was back.
  'script.farlamp_edda': [
    { op: 'say', speaker: 'KEEPER EDDA MARROW', text: 'I felt it from Driftholm. Eleven winters I\'ve slept with my back to the sea, and this morning I woke facing it.' },
    { op: 'say', speaker: 'KEEPER EDDA MARROW', text: 'I came down the long stair the way I went up it, with a small lamp. Didn\'t need it. Every tide-lamp on the races was burning.' },
    { op: 'say', speaker: 'KEEPER EDDA MARROW', text: 'You read my log, I expect. All my hurrying. Look at her. Stubborn and lovely, same as ever. Thank you for coming all the way down.' },
    { op: 'say', speaker: 'KEEPER EDDA MARROW', text: 'Tell Ione Fathom her lamp-boat came home, will you? Her and Bram learned their knots on my stair, the pair of them, forever fighting over the oars.' },
    { op: 'say', speaker: 'KEEPER EDDA MARROW', text: 'The light\'s woken the old races, too. There were islets on the Galleries and the Stair we used to row out to for the quiet. Go and see what the sea\'s kept on them.' },
  ],

  // ---- the keeper's desk + the store's sluice ------------------------------------
  'script.farlamp_keeper_desk': [
    { op: 'narrate', unless_flag: DAWN, text: 'The keeper\'s chest-desk, swept clear. Scratched into the lid with a knife-point: E.M., and a little drawing of a lamp with lines coming off it.' },
    { op: 'narrate', if_flag: DAWN, text: 'In the new light you can read what else is scratched into the lid, under the keeper\'s initials, in a dozen different hands over thirty years: the names of boats. Every one that ever came home by the Farlamp.' },
  ],
  'script.farlamp_sluice': [
    { op: 'narrate', unless_flag: 'flag:isles_log_4', text: 'A sluice of barnacled iron, wheeled shut, the race behind it pushing back at you. A keeper\'s mark is chalked on it: a lamp, and the number four.' },
    { op: 'narrate', if_flag: 'flag:isles_log_4', text: 'The sluice stands open. Its wheel is on the bell-post, the way the keeper wrote, turned toward the lamp. The race runs in to the store.' },
  ],
};

export const UNDERTIDE_DIALOGUE: DialogueRegistry = {
  'sign.undertide_mouth': [
    { text: 'THE UNDERTIDE. Mind the SURGE: white water does not swim. Ride the RACES — they run one way and never back.' },
    { text: 'The mouth bell turns the junction race. White on the race-post: the race runs on. Red: it turns.' },
  ],
  'sign.undertide_vaults': [
    { text: 'THE KELP VAULTS. Kelp walk west for the ladder to the mouth. The island is the keeper\'s; the vault bell turns its race.' },
  ],
  'sign.undertide_galleries': [
    { text: 'THE BELL GALLERIES. Three bells: DEEP, SHOAL, HARBOUR. Each turns one race. Every race runs home to this stair, whatever the bells.' },
    { text: 'Underneath, in chalk, a child\'s hand: DEEP CALLS. SHOAL ANSWERS. HARBOUR BRINGS THEM HOME.' },
  ],
  'sign.undertide_stair': [
    { text: 'THE DROWNED STAIR. Every race runs down. The long race on the east wall runs all the way back up. Below: the lamp-room.' },
  ],
  'npc.farlume_resting': [
    { text: 'Farlume has sunk back into the ring of water round the lamp, a gold shape turning slowly in the deep. It won\'t come up for you again until you\'ve won {remaining} more battles in the world above.' },
  ],
  'npc.undertide_diver_ness_after': [{ speaker: 'NESS', text: 'Lamp-glass, lamp-glass everywhere. The sea\'s been keeping it for us.' }],
  'npc.undertide_diver_corin_after': [{ speaker: 'CORIN', text: 'One ring, the race goes one way. Ring again, it goes back. Bells are fair like that.' }],
  'npc.undertide_nethand_bryn_after': [{ speaker: 'BRYN', text: 'Deep, shoal, harbour. Say it till it\'s a song.' }],
  'npc.undertide_keeper_isolde_after': [{ speaker: 'ISOLDE', text: 'She always said the lamp would outlast her stubbornness. It was a close thing.' }],
  'npc.undertide_diver_marlo_after': [{ speaker: 'MARLO', text: 'Eighty-one. Eighty-two after this one.' }],
};
