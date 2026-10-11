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

export const NORTH_SCRIPTS: ScriptRegistry = {
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
