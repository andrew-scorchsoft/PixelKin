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
    { op: 'narrate', text: 'Rows of dark stones on clean linen, each with a paper tag in a careful hand. DUSKAPPLE ORCHARD. HUSHFROST, A SPLINTER OF THE FOURTH FALL. GALEHIGH, KITE-RISING NIGHT. Dozens of them.' },
    { op: 'narrate', text: 'Shelves of them, dusted. Two niches, each holding a single stone as if it might wake. A cot with its blanket squared. A brass lamp, polished bright and never lit.' },
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
    "I wore the grey six winters. I came to see whether he'd really do it. ...I think I came to see whether I'd stop him, if I could. I can't. You might.",
    "I took the grey off at first light. It's folded in my pack. I may keep it, to remember that I was wrong gently.",
  ),
  'script.penumbra_gone_quiet_walker': dawnPair(
    'MARSH WALKER',
    'The marsh lamps went out one by one, and nobody came. We stopped expecting anybody. Then a lamp came up the road from the crossroads. Yours.',
    'Morning on the Ring. I keep feeling for the dark, the way your tongue goes to a missing tooth.',
  ),
  'script.penumbra_gone_quiet_child': dawnPair(
    'MARSH CHILD',
    "Mum says the mountain is where the night lives. I don't think it lives there. I think it's only visiting.",
    "The night went HOME. Mum says it's coming back tonight, but only for a bit, and then it has to go again.",
  ),
  'script.penumbra_gone_quiet_mender': dawnPair(
    'LAMP-MENDER',
    'We brought one lamp for every light you woke, and set them in a ring facing the mountain. It seemed the right shape. Go and read them, if you like. We wrote the plaques small, so they would fit.',
    'Eight lamps, and the sun come up behind them anyway. We will carry them home lit. It seems a waste of oil, and I do not care.',
  ),
  'script.penumbra_forecourt_sweeper': dawnPair(
    'GREY-ROBED SWEEPER',
    'Mind the row, please. I sweep it every dusk. The Warden says untidiness is only grief that has given up. ...He sweeps the high rooms himself. He will not let anyone else.',
    "I came out at dusk to sweep, and there was no dusk. I've been standing here with the broom for an hour, watching the light on the stone.",
  ),
};

/** The eight memorial plaques (one per relit constellation) — warden + their lesson. */
const memorial = (el: string, warden: string, town: string, lesson: string) => [
  { text: `A lamp for the ${el}, set here by the marsh-folk. Its flame burns the colour of that sky.` },
  { text: `The little plaque: ${warden}, ${town}. Beneath it, scratched carefully: "${lesson}"` },
];

export const CENTRAL_DIALOGUE: DialogueRegistry = {
  // --- the Cinder Hoard's reads (cold until the relight; woken after) --------
  'npc.hoard_shelf_w': [
    { text: 'A shelf of cinders on swept linen, each tagged in the same careful hand. DIMGLASS FLATS. SALTREACH, THE REED-BED, SPRING. LOWLEAF, BEHIND THE KILN.' },
    { text: 'There is no dust on any of them. Someone has been keeping it off.' },
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
    { text: 'Rows of dark stones on clean linen. DUSKAPPLE ORCHARD: A SPLINTER, THE HEART WOULD NOT LEAVE ITS PIT. HUSHFROST, A SPLINTER OF THE FOURTH FALL. GALEHIGH, KITE-RISING NIGHT.' },
    { text: 'Each one lies exactly a hand from the next, the way graves are laid out by somebody who means to visit.' },
  ],
  'npc.hoard_linen_b': [
    { text: 'The second row. PEARLMOOR, NORTH SHORE. THE WINDWARD STAIR. SUNVAULT, THE FAMILY WHO CHOSE THE QUIET.' },
    { text: 'The linen between the stones has been swept so often that the weave has gone soft.' },
  ],
  'npc.hoard_lamp': [
    { text: 'A tall brass lamp, polished bright, its wick trimmed and its chimney clean.' },
    { text: 'It has never been lit. The oil in it is years old.' },
  ],
  'npc.hoard_cot': [
    { text: 'A narrow cot, the blanket folded square. Someone sleeps here, among the stones, so that they will not be alone.' },
  ],
  'npc.hoard_shelf_w_woken': [
    { text: 'Every stone on the shelf is glowing gold through its cracks, and the paper tags have gone warm in the light.' },
    { text: 'Not dead. They were never dead. Only guttered.' },
  ],
  'npc.hoard_shelf_e_woken': [
    { text: "The Nightreach stone burns brightest of the row. 'Better she didn't,' says its tag. She will see this one." },
  ],
  'npc.hoard_niche_woken': [
    { text: "The Hushfrost stone has woken in its niche, warm as a held hand. 'It was cold by the ladder,' says the tag. It isn't now." },
  ],
  'npc.hoard_linen_a_woken': [
    { text: 'Every stone on the linen has woken. Row on row of small gold lights, like a churchyard on the night the lamps are lit for the names.' },
  ],
  'npc.hoard_linen_b_woken': [
    { text: 'The second row glows too, each light beside its tag. Somebody walked out and fetched every one of these home. Now they have come home all the way.' },
  ],
  'npc.hoard_lamp_woken': [
    { text: 'The brass lamp still stands unlit, the only dark thing left in the room. Nothing here needs it lit any more.' },
  ],
  'npc.hoard_cot_woken': [
    { text: 'The blanket is still folded square. Whoever slept among the stones has gone down to the morning.' },
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
    { speaker: 'STAR-TENDER FENN', text: "Go on down ahead, child. I'll walk him home at his own pace. We've time now. That's the strangest part." },
  ],
  'npc.fenn_summit_round': [
    { speaker: 'STAR-TENDER FENN', text: 'The lantern first, apprentice. Then the lesson. I have waited forty years; I can wait while you climb three more steps.' },
  ],
};
