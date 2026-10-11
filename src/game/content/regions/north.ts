/**
 * NORTH world-craft content (docs/reviews/world-craft-panel.md §6): this region's
 * package OWNS this file — new optional scripts + dialogue only, spread into the
 * registries via regions/index.ts. Map placements that reference these refs ride
 * tools/maps/worldcraft/north.py (run through tools/maps/add_world_craft.py).
 *
 * Everything here is OPTIONAL colour on the Windward Stair (the game's longest
 * crossing, which had no beats of its own): the cairn-count, the rest shelter,
 * the lookout spyglass. None of it gates a lane, a warp or a story step.
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

/** One climber's stone on one switchback cairn: the first time adds it, later visits see it. */
function cairnStone(flag: string, first: string, wind: string, after: string): ScriptRegistry[string] {
  return [
    { op: 'action', actor: 'player', action: 'gift', holdMs: 300, unless_flag: flag },
    { op: 'sfx', key: 'world-pickup', unless_flag: flag },
    { op: 'narrate', text: first, unless_flag: flag },
    { op: 'say', speaker: 'THE WIND', text: wind, unless_flag: flag },
    { op: 'narrate', text: after, if_flag: flag },
    { op: 'setFlag', flag },
  ];
}

// ---------------------------------------------------------------------------
// AFTER-GLEAM (2026-10): Galehigh and Pale Vault answer their Gleams. Placements
// ride tools/maps/worldcraft/north.py (`after` twins, `talk` re-points); the
// pre-Gleam branch of every staged script is the original ref, untouched.
// ---------------------------------------------------------------------------
const STORM = 'gleam:storm';
const FROST = 'gleam:frost';

/** One NPC, two pages: the original ref until `gleam`, the lit one after. */
function staged(orig: string, lit: string, gleam: string): ScriptRegistry[string] {
  return [
    { op: 'dialogue', ref: orig, unless_flag: gleam },
    { op: 'dialogue', ref: lit, if_flag: gleam },
  ];
}

const NORTH_AFTER_SCRIPTS: ScriptRegistry = {
  // --- Cinderwind Scarp (2026-10): the climb out of Cinderhead Deep ---
  'script.scarp_hauler': [
    { op: 'say', speaker: 'HOBB-REE', text: 'Up out of the Deep, are you? Then you\'ve earned a breather — and I\'ve earned a bout. Thirty years hauling ore up this scarp. Let\'s see what YOUR lot can carry.' },
    { op: 'battle', trainer: 'scarp_hauler' },
    { op: 'say', speaker: 'HOBB-REE', text: 'Ha! Strong backs, the lot of them. Galehigh\'s at the top — follow the wind. If your hat leaves first, let it go.' },
    { op: 'setFlag', flag: 'flag:scarp_hauler_beaten' },
  ],
  'script.scarp_kiterunner': [
    { op: 'say', speaker: 'RUE', text: 'Oi, mine-dust! Nobody comes up onto MY ridge without a race. Kites up, kin out!' },
    { op: 'battle', trainer: 'scarp_kiterunner' },
    { op: 'say', speaker: 'RUE', text: 'Outflown. Fine. The terraces are just through the gate — tell the kite-maker Rue sent you, and she\'ll laugh at you.' },
    { op: 'setFlag', flag: 'flag:scarp_kiterunner_beaten' },
  ],
  'script.pickup_scarp_amber': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'Wedged behind the crystal spoil, where the haulers never looked: a lump of MOTH-AMBER. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_scarp_amber' },
  ],
  'script.pickup_scarp_balm': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'A hauler\'s tin left on the ledge for whoever comes up next. Found 2 WARM BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_scarp_balm' },
  ],

  // Galehigh's festival trio are actors in the Kite-rising, so they keep their ids.
  'script.galehigh_piper_staged': staged('npc.galehigh_festival_piper', 'npc.galehigh_festival_piper_lit', STORM),
  'script.galehigh_festival_kid_staged': staged('npc.galehigh_festival_kid', 'npc.galehigh_festival_kid_lit', STORM),
  'script.galehigh_festival_goer_staged': staged('npc.galehigh_festival_goer', 'npc.galehigh_festival_goer_lit', STORM),
  'script.shop_galehigh_staged': [
    ...staged('npc.galehigh_shopkeeper', 'npc.galehigh_shopkeeper_lit', STORM),
    { op: 'shop', shop: 'galehigh' },
  ],
  'script.galehigh_inn_rest_lit': [
    { op: 'say', speaker: 'INNKEEP', text: "In out of the gusts, Wayfarer. Gentler gusts tonight, if you can believe it. Half my guests are up on the roof watching the Storm-star." },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: "There. Kin bright-eyed and boots warm. I let the shutters rattle as much as they like now. It sounds like applause." },
  ],
  // Pale Vault: the watcher is an actor in the Aurora-watch; the tallow-keeper's
  // last stage already hangs on her oil.
  'script.aurora_watcher_b_staged': staged('npc.aurora_watcher_b', 'npc.aurora_watcher_b_lit', FROST),
  'script.tallow_keeper_staged': staged('npc.tallow_keeper_after', 'npc.tallow_keeper_lit', FROST),
  'script.pale_vault_inn_rest_lit': [
    { op: 'say', speaker: 'INNKEEP', text: "Come in quiet, Wayfarer. The hearth is low, but the brackets are lit at last, and I've moved the good chair to the window." },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: "Rested, and your kin with you. Sleep if you can. The sky is keeping its own watch tonight." },
  ],
};

const NORTH_AFTER_DIALOGUE: DialogueRegistry = {
  // --- Cinderwind Scarp (2026-10) ---
  'sign.cinderwind_scarp': [
    { text: 'CINDERWIND SCARP\nWEST: the Deep\'s mouth and the Cinderhead galleries. UP and EAST: Galehigh Terraces. Mind the gusts on the top tier.' },
  ],
  'npc.scarp_cairn': [
    { text: 'A wind cairn, every stone wrapped in a faded kite-ribbon. Galehigh folk build one wherever they first feel the updraught. This is where the mountain starts to breathe.' },
  ],
  'npc.scarp_hauler_after': [
    { speaker: 'HOBB-REE', text: 'The carts used to run right up to the terraces. Then the dark came, and the rail-lamps went, and now it\'s legs. Good legs, mind.' },
  ],
  'npc.scarp_kiterunner_after': [
    { speaker: 'RUE', text: 'You can see the whole Deep\'s spoil-heap from up here. And the kites. Mostly the kites.' },
  ],

  // --- Galehigh Terraces (gleam:storm) ----------------------------------------
  'npc.galehigh_festival_piper_lit': [
    { speaker: 'FESTIVAL PIPER', text: "Still playing! The kites came down hours ago, but the Storm's up there now, and somebody ought to keep it company." },
    { speaker: 'FESTIVAL PIPER', text: "Mira flew the launch ledge twice after your bout: once for the Gleam, and once, she says, so the wind wouldn't feel left out." },
  ],
  'npc.galehigh_festival_kid_lit': [
    { speaker: 'FESTIVAL KID', text: "Talo says his kite touched the Storm-star. It DIDN'T. But it looked like it did, so I'm letting him have it. Once." },
  ],
  'npc.galehigh_festival_goer_lit': [
    { speaker: 'FESTIVAL-GOER', text: "My gran's ladder of little lights worked, then. Or the Storm was only waiting for an excuse. Either way, my tail-lamp stays lit till it gutters on its own." },
  ],
  'npc.galehigh_farmer_lit': [
    { speaker: 'TERRACE FARMER', text: "Three nights since the Storm came back, and the wind's turned honest: steady off the north-west, no tricks. The cabbages don't know which way to lean. Neither do I." },
  ],
  'npc.galehigh_hall_keeper_lit': [
    { speaker: 'HALL-KEEPER', text: "Looking for Mira? Off the launch ledge again, dear, teaching the Wind-Eye's name to anyone who'll hold a string." },
    { speaker: 'HALL-KEEPER', text: "The hall is quiet. I've swept it twice and polished the ledger-case. A hall may be proud, so long as it doesn't say so out loud." },
  ],
  'npc.galehigh_inn_guest_lit': [
    { speaker: 'INN GUEST', text: "I came up for the room out of the wind and stayed for the Rising. Now they tell me the best room is the ROOF, with a blanket, under the Storm. It is not out of the wind. I'm staying anyway." },
  ],
  'npc.galehigh_home_elder_lit': [
    { speaker: 'TERRACE ELDER', text: "Seventy years I've flown the Rising, and last night I flew one more: a little kite off the doorstep, the Storm overhead and my knees objecting the whole way. Worth every objection." },
  ],
  'npc.galehigh_home_kid_lit': [
    { speaker: 'TERRACE KID', text: "Da says this year's impossible thing is DONE. The Storm came back! So next year I get two. I've already picked them." },
  ],
  'npc.galehigh_shopkeeper_lit': [
    { speaker: 'KITE-KEEPER', text: "The Rising cleared my shelf of string and filled my till with wicks. A fair trade, the wind would say. Storm charts still in: Thunder Kick, Volt Arc, Gale Slam." },
    { speaker: 'KITE-KEEPER', text: "And stock your balms HERE, Wayfarer. Pale Vault keeps no counter, Gleam or no Gleam." },
  ],
  'npc.lanternway_galehigh_lamplighter_lit': [
    { speaker: 'LAMPLIGHTER', text: "Since the Storm stood up, the posts on this road hold their flame in the gusts. I trimmed every one twice anyway, out of pure suspicion." },
    { speaker: 'LAMPLIGHTER', text: "The road is only a road while you can see it. Tonight you can see it all the way to the top bend." },
  ],
  // --- Pale Vault Glacier (gleam:frost) ---------------------------------------
  'npc.pale_vault_townsfolk_lit': [
    { speaker: 'GLACIER-DWELLER', text: "We still do not shout in Pale Vault. But when the brackets lit, someone at the watch laughed, once, softly. The glacier is carrying it still. I hope it keeps that one." },
  ],
  'npc.aurora_watcher_b_lit': [
    { speaker: 'WATCHER', text: "My mother stood this ice, and hers, and neither of them saw all seven brackets burn. Tonight I stood here and counted them for the three of us." },
  ],
  'npc.pale_vault_home_elder_lit': [
    { speaker: 'GLACIER ELDER', text: "The aurora crossed my window as it always has. But tonight there was a second light under it, from the vault. I am old, child, and the sky can still surprise me with company." },
  ],
  'npc.pale_vault_home_kid_lit': [
    { speaker: 'GLACIER KID', text: "I said the undercroft hums something. Now I know what: the brackets. Seven notes, low to high, in the order you lit them. I hummed them back. It didn't mind." },
  ],
  'npc.pale_vault_inn_guest_lit': [
    { speaker: 'INN GUEST', text: "The ice creaked TWICE last night. Third bell, and again at fourth. We have talked of nothing else. We are all very excited, in our way." },
  ],
  'npc.pale_vault_hall_keeper_lit': [
    { speaker: 'HALL-KEEPER', text: "Begin wherever you like now, Wayfarer. The undercroft door stands open and the brackets are burning. I sent the children down to look. They came back whispering, which in this town is a kind of cheering." },
  ],
  'npc.tallow_keeper_lit': [
    { speaker: 'TALLOW-KEEPER', text: "Seven brackets burning, child, and every one of them smells of my pans. I've rendered the vault's oil all my life and never been this proud of a smell." },
  ],
};

export const NORTH_SCRIPTS: ScriptRegistry = {
  ...NORTH_AFTER_SCRIPTS,
  // --- Windward Stair I: the cairn-count (world-craft panel §4 #2) -----------
  // Every switchback keeps a cairn, and every climber adds a stone. Four on the
  // way up; the summit cairn notices whether you added all four.
  'script.windward_cairn_foot': cairnStone(
    'flag:windward_cairn_foot',
    'Climbers have stacked this cairn a stone at a time, each from their own road. You find a flat one in the grass and set it on top.',
    'Hhhh — a long way up. Begin it anyway.',
    'Your stone is still on top, a little crooked. The wind has not argued with it.',
  ),
  'script.windward_cairn_kettle': cairnStone(
    'flag:windward_cairn_kettle',
    'The kettle-camp cairn is warm on its sheltered side. You add a stone from your pocket, still warm from the walk.',
    'Hhh. Sit if you must. The stair waits. I do not.',
    'Your stone sits where you left it, rimed now, part of the cairn.',
  ),
  'script.windward_cairn_mid': cairnStone(
    'flag:windward_cairn_mid',
    'Halfway. The cairn here leans into the slope like a climber catching breath. You wedge your stone where it will stop the lean.',
    'Hhhhh. Halfway is where the legs make up their minds.',
    'The cairn still leans. Your stone is still holding it up.',
  ),
  'script.windward_cairn_head': cairnStone(
    'flag:windward_cairn_head',
    'The last cairn below the wind-gap is old and wide, its lowest stones furred with lichen. You add yours to the top.',
    'HHHHH— there. You are nearly mine now.',
    'Your stone is one of a great many up here. You know which one.',
  ),
  // The summit cairn: a nested precedence chain (the andrew_hint_tide pattern),
  // so exactly one line plays whichever cairns were skipped.
  'script.windward_cairn_summit': [
    { op: 'run', ref: 'script.windward_summit_1', if_flag: 'flag:windward_cairn_foot' },
    { op: 'run', ref: 'script.windward_summit_short', unless_flag: 'flag:windward_cairn_foot' },
  ],
  'script.windward_summit_1': [
    { op: 'run', ref: 'script.windward_summit_2', if_flag: 'flag:windward_cairn_kettle' },
    { op: 'run', ref: 'script.windward_summit_short', unless_flag: 'flag:windward_cairn_kettle' },
  ],
  'script.windward_summit_2': [
    { op: 'run', ref: 'script.windward_summit_3', if_flag: 'flag:windward_cairn_mid' },
    { op: 'run', ref: 'script.windward_summit_short', unless_flag: 'flag:windward_cairn_mid' },
  ],
  'script.windward_summit_3': [
    { op: 'run', ref: 'script.windward_summit_all', if_flag: 'flag:windward_cairn_head' },
    { op: 'run', ref: 'script.windward_summit_short', unless_flag: 'flag:windward_cairn_head' },
  ],
  'script.windward_summit_short': [
    { op: 'narrate', text: 'The summit cairn is taller than you are. A stone for every switchback, the crag-tender says — and some of yours are missing somewhere below.' },
  ],
  'script.windward_summit_all': [
    { op: 'narrate', text: 'The summit cairn is taller than you are, and the wind has gone round it so long that it hums.', unless_flag: 'flag:windward_cairns_all' },
    { op: 'action', actor: 'player', action: 'gift', holdMs: 400, unless_flag: 'flag:windward_cairns_all' },
    { op: 'sfx', key: 'world-gleam-a', unless_flag: 'flag:windward_cairns_all' },
    { op: 'narrate', text: 'You set your fifth stone on top. Somewhere below, four smaller cairns each hold one of yours, and for a moment the whole Stair feels like a single long sentence you have finished writing.', unless_flag: 'flag:windward_cairns_all' },
    { op: 'say', speaker: 'THE WIND', text: 'Hhhh. Every turn. Not many do. Go on, then — up.', unless_flag: 'flag:windward_cairns_all' },
    { op: 'narrate', text: 'Five stones of yours on the Windward Stair. The wind hums round the top one.', if_flag: 'flag:windward_cairns_all' },
    { op: 'setFlag', flag: 'flag:windward_cairns_all' },
  ],

  // The climbers' shelter on the halfway shelf — a sit, not a heal (the kettle
  // camp above and the Stair II rest shelf keep their jobs).
  'script.windward_shelter': [
    { op: 'narrate', text: 'A dry-stone shelter, roofed in slate and snow. Inside: a bench, a lantern on a nail, a coil of rope nobody has needed this year.' },
    { op: 'action', actor: 'player', action: 'sit', holdMs: 1400 },
    { op: 'narrate', text: 'You sit. The wind goes over the roof instead of through you. Your kin lean in close, and the climb gets a little shorter while you are not doing it.' },
    { op: 'narrate', text: 'Someone has scratched tallies into the lintel — climbers counting days up, or nights out. The newest are a long way from the oldest.', unless_flag: 'flag:windward_shelter_seen' },
    { op: 'setFlag', flag: 'flag:windward_shelter_seen' },
  ],

  // The lookout spyglass at the head of the Stair: a fall, seen from the heights.
  // It goes down south, towards the mountain (the peril thread, North register).
  'script.windward_spyglass': [
    { op: 'narrate', text: 'A brass spyglass on a frosted tripod, aimed south over the terraces. Someone has scratched beside the eyepiece: FOR THE FALLS.' },
    { op: 'letterbox', on: true, ms: 320, unless_flag: 'flag:windward_spyglass_seen' },
    { op: 'cameraFocus', to: { tx: 12, ty: 37 }, ms: 1200, unless_flag: 'flag:windward_spyglass_seen' },
    { op: 'narrate', text: 'Down past Galehigh\'s little fires the land goes dark, and past the dark rises the mountain — a black shape cut out of the stars.', unless_flag: 'flag:windward_spyglass_seen' },
    { op: 'starfall', from: 'right', wait: true, unless_flag: 'flag:windward_spyglass_seen' },
    { op: 'narrate', text: 'As you watch, one star lets go. It crosses half the sky without a sound and goes down on the mountain\'s flank, and the place where it was is simply empty.', unless_flag: 'flag:windward_spyglass_seen' },
    { op: 'wait', ms: 700, unless_flag: 'flag:windward_spyglass_seen' },
    { op: 'narrate', text: 'They fall nearer the mountain. Everyone up here knows it. Nobody says it twice.', unless_flag: 'flag:windward_spyglass_seen' },
    { op: 'cameraReset', ms: 900, unless_flag: 'flag:windward_spyglass_seen' },
    { op: 'letterbox', on: false, ms: 320, unless_flag: 'flag:windward_spyglass_seen' },
    { op: 'narrate', text: 'Through the glass, the mountain. The sky above it is a little thinner than the sky above you.', if_flag: 'flag:windward_spyglass_seen' },
    { op: 'setFlag', flag: 'flag:windward_spyglass_seen' },
  ],

  // Wind-shrines: small stone niches along the Stair; a line each, read-only.
  'script.windward_shrine': [
    { op: 'narrate', text: 'A wind-shrine: a stone niche, a stub of candle, three iron chimes that never quite stop. Climbers leave a pebble for a kind wind.' },
    { op: 'narrate', text: 'You leave one. The chimes go on about it for some time.' },
  ],
};

export const NORTH_DIALOGUE: DialogueRegistry = {
  ...NORTH_AFTER_DIALOGUE,
  // B3's silent company: one of Còr's people keeps the drained shelf with him.
  'npc.cor_acolyte': [
    { text: 'A cowled figure in Hollowing grey, a little behind the other one. It keeps its eyes on the valley and its hands folded round an unlit lantern.', style: 'narrate' },
    { text: 'When you speak, it only bows its head — as if to say the answer is not its to give.', style: 'narrate' },
  ],
  // The Galehigh spoke finally has a soul on it: the lane's lamplighter.
  'npc.lanternway_galehigh_lamplighter': [
    { speaker: 'LAMPLIGHTER', text: 'Up to Galehigh? Mind the gusts at the top bend — they take hats, kites and the occasional opinion.' },
    { speaker: 'LAMPLIGHTER', text: 'I trim these posts every dusk, which these days is every hour. Somebody has to. The road is only a road while you can see it.' },
  ],
};
