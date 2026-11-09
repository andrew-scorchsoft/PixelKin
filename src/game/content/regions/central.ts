/**
 * CENTRAL world-craft content (docs/reviews/world-craft-panel.md §6): this region's
 * package OWNS this file — new optional scripts + dialogue only, spread into the
 * registries via regions/index.ts. Map placements that reference these refs ride
 * tools/maps/worldcraft/central.py (run through tools/maps/add_world_craft.py) or
 * the region's builders (build_penumbra_ring.py, build_umbral_spire.py).
 *
 * Story canon these lines rest on: docs/world/story-bible.md §11 (the cinder law)
 * and §12 (the dates). Register: cosy-melancholy, zero humour at the Spire, the
 * Hollowing gentle and half-right, Còr never gloated over.
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

/** One staged line: plays before the dawn, the other after (exactly one plays). */
const dawnPair = (speaker: string, before: string, after: string): CutsceneStep[] => [
  { op: 'say', unless_flag: 'flag:dawn', speaker, text: before },
  { op: 'say', if_flag: 'flag:dawn', speaker, text: after },
];

export const CENTRAL_SCRIPTS: ScriptRegistry = {
  // --- The Umbral Approach (2026-10): the mountain road up from the Crossroads.
  // Three acolytes keep its turns. They do not threaten — they ask, and only
  // fight because you won't turn round (the Hollowing: gentle, half-right).
  'script.approach_acolyte_a': [
    { op: 'say', speaker: 'ORLA', text: 'A lamp on the mountain road! Most folk see the dark and turn back.' },
    { op: 'say', speaker: 'ORLA', text: 'The sea took every net I mended. Up here, nothing is taken. Turn round, love, or show me why not.' },
    { op: 'battle', trainer: 'approach_acolyte_a' },
    { op: 'say', speaker: 'ORLA', text: '...Well. That was why not. Go gently above: the lamps give out there.' },
    { op: 'setFlag', flag: 'flag:approach_acolyte_a_beaten' },
  ],
  'script.approach_acolyte_b': [
    { op: 'say', speaker: 'BRENN', text: 'Past the last grass, the quiet starts. Nothing grows loud here; nothing grieves.' },
    { op: 'say', speaker: 'BRENN', text: 'We keep the road soft for those who come to rest. You did not come to rest.' },
    { op: 'battle', trainer: 'approach_acolyte_b' },
    { op: 'say', speaker: 'BRENN', text: 'No. ...One more of us waits on the shoulder. She\'ll ask you kinder.' },
    { op: 'setFlag', flag: 'flag:approach_acolyte_b_beaten' },
  ],
  'script.approach_acolyte_c': [
    { op: 'say', speaker: 'WYNNE', text: 'The last turn before the Ring. Past it, kin lie down in the old dark. Mine did. I stayed.' },
    { op: 'say', speaker: 'WYNNE', text: 'I won\'t stop you. I only ask, and mean it: is the light worth what it costs?' },
    { op: 'battle', trainer: 'approach_acolyte_c' },
    { op: 'say', speaker: 'WYNNE', text: '...You are sure. Then go up. Let the morning come slowly, for those of us who forgot how.' },
    { op: 'setFlag', flag: 'flag:approach_acolyte_c_beaten' },
  ],
  'script.pickup_approach_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Half-buried where the last grass grows: a STARGLASS SHARD, far from home. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_approach_shard' },
  ],
  'script.pickup_approach_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 500 },
    { op: 'say', text: 'A pilgrim\'s tin under the ledge, left for whoever needs it. Found 500 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_approach_wicks' },
  ],

  // NPCs only run `script.*` refs (WorldScene); Oriel's `cutscene.starfall_begins`
  // fell through to "..." and the whole Starfall Vigils chain was unreachable.
  'script.starfall_begins': [{ op: 'run', ref: 'cutscene.starfall_begins' }],
  // ===========================================================================
  // C-1 THE CINDER HOARD (story panel rank 1) — umbral_spire_f3's R5, straight
  // off the arrival room. Còr walks out after every fall and fetches the cinder
  // home; this is where he keeps them, "like a swept churchyard". The doorway
  // band plays once (flag:cinder_hoard_seen is bookkeeping only). The room's
  // payoff is in script.keystar_relight: at the catch, every stone here wakes.
  // ===========================================================================
  'cutscene.cinder_hoard': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'silence', ms: 1400 },
    { op: 'cameraFocus', to: { tx: 21, ty: 8 }, ms: 1100 },
    { op: 'wait', ms: 600 },
    { op: 'narrate', text: 'Dark stones on clean linen, each tagged in a careful hand. DUSKAPPLE ORCHARD. HUSHFROST, A SPLINTER OF THE FOURTH FALL. GALEHIGH, KITE-RISING NIGHT.' },
    { op: 'narrate', text: 'Shelves of them, dusted. Two niches, each with a single stone. A cot, its blanket squared. A brass lamp, polished and never lit.' },
    { op: 'narrate', if_flag: 'flag:orchard_strike_seen', text: "You find Wendel's without looking for it: a splinter only. The heart of that one would not leave its pit." },
    { op: 'emote', actor: 'player', emote: 'ellipsis' },
    { op: 'say', if_flag: 'flag:wren_joined', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: "He's been... collecting them. Like a churchyard. ...He sweeps in here too, look." },
    { op: 'cameraReset', ms: 900 },
    { op: 'letterbox', on: false, ms: 420 },
    { op: 'musicCrossfade', key: 'umbral-spire-b', ms: 1600 },
  ],

  // ===========================================================================
  // THE PENUMBRA RING — the gone-quiet, come in from the marsh villages to see
  // whether the Spire is real (peril thread C1's neighbours). Each is one
  // placement running one script; every stage is a dawn-staged pair.
  // ===========================================================================
  'script.penumbra_gone_quiet_elder': dawnPair(
    'GREY-ROBED ELDER',
    "I wore the grey six winters. I came to see if I'd stop him, if I could. ...I can't. You might.",
    "I took the grey off at first light. I may keep it, to remember I was wrong gently.",
  ),
  'script.penumbra_gone_quiet_walker': dawnPair(
    'MARSH WALKER',
    'The marsh lamps went out one by one, and nobody came. Then a lamp came up the road. Yours.',
    'Morning on the Ring. I keep feeling for the dark, like a tongue to a missing tooth.',
  ),
  'script.penumbra_gone_quiet_child': dawnPair(
    'MARSH CHILD',
    "Mum says the night lives in the mountain. I think it's only visiting.",
    "The night went HOME. Mum says it's back tonight, but only for a bit.",
  ),
  'script.penumbra_gone_quiet_mender': dawnPair(
    'LAMP-MENDER',
    'One lamp for every light you woke, set in a ring facing the mountain. [[Read their plaques]], if you like. We wrote them small.',
    'Eight lamps, and the sun come up behind them anyway. We will carry them home lit. A waste of oil. I do not care.',
  ),
  'script.penumbra_forecourt_sweeper': dawnPair(
    'GREY-ROBED SWEEPER',
    'Mind the row, please. The Warden says untidiness is only grief that has given up. ...He sweeps the high rooms himself.',
    "I came out at dusk to sweep, and there was no dusk. I've stood here an hour, watching the light on the stone.",
  ),
};

/** The eight memorial plaques (one per relit constellation) — warden + their lesson. */
const memorial = (el: string, warden: string, town: string, lesson: string) => [
  { text: `A lamp for the ${el}, set here by the marsh-folk. Its flame burns the colour of that sky.` },
  { text: `The little plaque: ${warden}, ${town}. Beneath it, scratched carefully: "${lesson}"` },
];

export const CENTRAL_DIALOGUE: DialogueRegistry = {
  // --- The Umbral Approach (2026-10) ---
  'sign.umbral_approach': [
    { text: 'THE UMBRAL APPROACH\nUP: [[the Penumbra Ring]]. Keep to the way-lamps.' },
  ],
  'sign.umbral_lookout': [
    { text: 'The whole crescent shows from here: every valley you relit, burning like a ring of hearths.' },
  ],
  'npc.approach_snuffed_shrine': [
    { text: 'A wayshrine, its lamp put out with care, like closing a door on someone sleeping.' },
  ],
  'npc.approach_notice': [
    { text: 'A Hollowing notice: "REST HERE IF YOU ARE TIRED. NO ONE WILL WAKE YOU." Beneath, in a less steady hand: "please".' },
  ],
  'npc.approach_vigil_camp': [
    { text: 'A tidy camp, bedrolls folded, three cups upturned. Its keepers went up and never came down.' },
  ],
  'npc.approach_acolyte_a_after': [
    { speaker: 'ORLA', text: 'The sea took every net. Still I mended them. Funny thing to remember, up here.' },
  ],
  'npc.approach_acolyte_b_after': [
    { speaker: 'BRENN', text: 'I keep listening for the quiet. It sounds less like peace since you came by.' },
  ],
  'npc.approach_acolyte_c_after': [
    { speaker: 'WYNNE', text: 'Slowly, mind. The morning. For those of us who forgot how.' },
  ],

  // --- the Cinder Hoard's reads (cold until the relight; woken after) --------
  'npc.hoard_shelf_w': [
    { text: 'Cinders on swept linen, each tagged in the same hand. DIMGLASS FLATS. SALTREACH, THE REED-BED, SPRING. LOWLEAF, BEHIND THE KILN.' },
    { text: 'No dust on any of them. Someone keeps it off.' },
  ],
  'npc.hoard_shelf_e': [
    { text: 'More tags. CINDERHEAD, A CHIP FROM THE ROOF-FAULT. COLDFOG, THIRD MARCH. NIGHTREACH, FELL DURING THE WATCH. NESSA DID NOT SEE.' },
    { text: "Beside that last one, smaller: 'Better she didn't.'" },
  ],
  'npc.hoard_niche': [
    { text: 'A niche to itself, a stone on folded cloth. The tag: HUSHFROST, FIRST OF THE FOURTH WINTER.' },
    { text: "Under it, in the same hand: 'Carried up warm. It was cold by the ladder.'" },
  ],
  'npc.hoard_linen_a': [
    { text: 'DUSKAPPLE ORCHARD: A SPLINTER, THE HEART WOULD NOT LEAVE ITS PIT. HUSHFROST, A SPLINTER OF THE FOURTH FALL. GALEHIGH, KITE-RISING NIGHT.' },
    { text: 'A hand apart each, the way graves are laid by someone who means to visit.' },
  ],
  'npc.hoard_linen_b': [
    { text: 'The second row. PEARLMOOR, NORTH SHORE. THE WINDWARD STAIR. SUNVAULT, THE FAMILY WHO CHOSE THE QUIET.' },
    { text: 'The linen between them has been swept until the weave went soft.' },
  ],
  'npc.hoard_lamp': [
    { text: 'A tall brass lamp, polished bright, wick trimmed, chimney clean.' },
    { text: 'It has never been lit. The oil in it is years old.' },
  ],
  'npc.hoard_cot': [
    { text: 'A narrow cot among the stones, so whoever sleeps here is not alone.' },
  ],
  'npc.hoard_shelf_w_woken': [
    { text: 'Every stone on the shelf glows gold through its cracks.' },
    { text: 'Not dead. They were never dead. Only guttered.' },
  ],
  'npc.hoard_shelf_e_woken': [
    { text: "The Nightreach stone burns brightest. 'Better she didn't.' She will see this one." },
  ],
  'npc.hoard_niche_woken': [
    { text: "The Hushfrost stone glows, warm as a held hand. Not cold by the ladder now." },
  ],
  'npc.hoard_linen_a_woken': [
    { text: 'Every stone on the linen has woken, like a churchyard on the night of the names.' },
  ],
  'npc.hoard_linen_b_woken': [
    { text: 'Somebody fetched each of these home. Now they\'ve come home all the way.' },
  ],
  'npc.hoard_lamp_woken': [
    { text: 'The brass lamp stands unlit, the only dark thing left. Nothing needs it now.' },
  ],
  'npc.hoard_cot_woken': [
    { text: 'The blanket\'s still square. Whoever slept here has gone down to the morning.' },
  ],

  // --- the Penumbra Ring's memorial lamps (one per Gleam, the marsh-folk's) --
  'npc.penumbra_memorial_ember': memorial('EMBER', 'BRISA TALLOW', 'TINDERWICK', 'A small flame is no lesser thing.'),
  'npc.penumbra_memorial_tide': memorial('TIDE', 'REYL WASH', 'PEARLMOOR QUAY', 'The sea keeps no lamps of its own. So we lend it ours.'),
  'npc.penumbra_memorial_verdant': memorial('VERDANT', 'SABLE QUILL', 'LOWLEAF HOLLOW', 'The moss was only ever waiting to be asked.'),
  'npc.penumbra_memorial_stone': memorial('STONE', 'OTHO GRIST', 'CINDERHEAD', 'Honour the dark. Then light every lamp again.'),
  'npc.penumbra_memorial_storm': memorial('STORM', 'MIRA VAEL', 'GALEHIGH', 'Give the sky something to answer.'),
  'npc.penumbra_memorial_frost': memorial('FROST', 'YSOLDE FROST', 'PALE VAULT', 'Every flame held in a bare hand is a flame chosen.'),
  'npc.penumbra_memorial_solar': memorial('SOLAR', 'LUCAN PYRE', 'SUNKEN SOLARIUM', 'Spend the warm day gladly. That it fades is the point.'),
  'npc.penumbra_memorial_lunar': memorial('LUNAR', 'NESSA COLE', 'NIGHTREACH', 'Watch, so the sky is never once alone.'),

  // --- the summit: Fenn waits at the dawn road's gate after the scene -------
  'npc.fenn_summit_dawn': [
    { speaker: 'STAR-TENDER FENN', text: "Go on down, child. I'll walk him home at his pace. We've time now. That's the strangest part." },
  ],
  'npc.fenn_summit_round': [
    { speaker: 'STAR-TENDER FENN', text: 'The lantern first, apprentice. Then the lesson. I\'ve waited forty years; I can wait three steps.' },
  ],
};
