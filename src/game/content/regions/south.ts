/**
 * SOUTH world-craft content (docs/reviews/world-craft-panel.md §6): this region's
 * package OWNS this file — new optional scripts + dialogue only, spread into the
 * registries via regions/index.ts. Map placements that reference these refs ride
 * tools/maps/worldcraft/south.py (run through tools/maps/add_world_craft.py).
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

// ---------------------------------------------------------------------------
// AFTER-GLEAM (2026-10): the South answers its two Gleams. Plain townsfolk get a
// `<id>_lit` flag-pair twin (worldcraft/south.py `after`); NPCs whose flags are
// already spoken for (a shop's kit pair, a staged chain, an actor a cutscene
// addresses) are re-pointed (`talk`) at a staged script below. The pre-Gleam
// branch is the ORIGINAL ref, untouched, and no branch is longer than the line
// it replaces (the South rule: words may change, page counts may not).
// ---------------------------------------------------------------------------
const EMBER = 'gleam:ember';
const TIDE = 'gleam:tide';

export const SOUTH_SCRIPTS: ScriptRegistry = {
  // --- THE LANTERN-CAR (2026-10 geometry fix). The far valleys sit high on the
  // mountain's flanks, days from the Crossroads on foot; the kite-wrights'
  // cable-car swings you there once that valley's lamp is relit (the old
  // spoke rule: the ride UP waits on the town's own Gleam). The ride DOWN from
  // a valley always runs — the car rolls home by its own weight.
  'script.crossroads_car_intro': [
    { op: 'emote', actor: 'waykeeper', emote: 'alert' },
    { op: 'face', actor: 'waykeeper', facing: 'right' },
    { op: 'face', actor: 'player', facing: 'left' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'Found the cars, have you? Mind the platform edge, young Wayfarer.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'That winch is the LANTERN-CAR. The kite-wrights strung its cables up the mountain\'s flanks before the Dusk — to Lowleaf in the green, Galehigh in the wind, Nightreach under the stars. Days of walking, swung over in a breath.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'But a car only runs while the lamp at its far end burns, and every one of those went out with the sky. Relight a valley\'s constellation and its line wakes — then the car will carry you there whenever you like.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'Till then it\'s boots and the long way round. The roads were walked long before a cable was strung — and you\'ll find more on foot than any car could show you.' },
    { op: 'face', actor: 'waykeeper', facing: 'down' },
  ],
  'script.lantern_car': [
    { op: 'narrate', text: 'THE LANTERN-CAR. Three cables climb from the winch into the dark toward the mountain\'s shoulders. Each line keeps a little lamp on the platform rail.' },
    { op: 'narrate', unless_flag: 'gleam:verdant', text: 'Every line-lamp is cold. No car will run until a valley\'s light is relit.' },
    {
      op: 'choice',
      if_flag: 'gleam:verdant',
      prompt: 'Which line? (A car runs once its valley\'s lamp is lit.)',
      options: [
        {
          label: 'LOWLEAF',
          if_flag: 'gleam:verdant',
          ops: [
            { op: 'sfx', key: 'world-lantern-light' },
            { op: 'narrate', text: 'The green lamp catches. The car swings out over the bay and climbs, the Crossroads\' lights shrinking below, the fen-mist rolling past...' },
            { op: 'travel', map: 'lanternway_lowleaf', to: { tx: 3, ty: 24 }, facing: 'up' },
          ],
        },
        {
          label: 'GALEHIGH',
          if_flag: 'gleam:storm',
          ops: [
            { op: 'sfx', key: 'world-lantern-light' },
            { op: 'narrate', text: 'The storm-lamp catches. The car climbs the mountain\'s eastern flank, rocking in the updraughts, kites wheeling below...' },
            { op: 'travel', map: 'lanternway_galehigh', to: { tx: 6, ty: 16 }, facing: 'up' },
          ],
        },
        {
          label: 'NIGHTREACH',
          if_flag: 'gleam:lunar',
          ops: [
            { op: 'sfx', key: 'world-lantern-light' },
            { op: 'narrate', text: 'The silver lamp catches. The longest line of all: up over the dark shoulder of the mountain, the stars so close the car seems to ride among them...' },
            { op: 'travel', map: 'lanternway_nightreach', to: { tx: 4, ty: 7 }, facing: 'down' },
          ],
        },
      ],
    },
  ],
  'script.lantern_car_down_lowleaf': [
    {
      op: 'choice',
      prompt: 'The Lantern-car waits at the platform. Ride down to the Vesper Crossroads?',
      options: [{ label: 'RIDE DOWN', ops: [
        { op: 'narrate', text: 'The car rolls off the platform under its own weight and sinks toward the Crossroads\' lamps.' },
        { op: 'travel', map: 'vesper_crossroads', to: { tx: 17, ty: 8 }, facing: 'down' },
      ] }],
    },
  ],
  'script.lantern_car_down_galehigh': [
    {
      op: 'choice',
      prompt: 'The Lantern-car waits at the platform. Ride down to the Vesper Crossroads?',
      options: [{ label: 'RIDE DOWN', ops: [
        { op: 'narrate', text: 'The car drops off the shelf and runs down the long cable, the terraces folding away behind you.' },
        { op: 'travel', map: 'vesper_crossroads', to: { tx: 17, ty: 8 }, facing: 'down' },
      ] }],
    },
  ],
  'script.lantern_car_down_nightreach': [
    {
      op: 'choice',
      prompt: 'The Lantern-car waits at the platform. Ride down to the Vesper Crossroads?',
      options: [{ label: 'RIDE DOWN', ops: [
        { op: 'narrate', text: 'The car slips off the observatory\'s shoulder and glides down through the stars, a long way, to the Crossroads\' small warm lights.' },
        { op: 'travel', map: 'vesper_crossroads', to: { tx: 17, ty: 8 }, facing: 'down' },
      ] }],
    },
  ],

  // Tinderwick store: the open counter, fair-week edition.
  'script.shop_tinderwick_staged': [
    { op: 'dialogue', ref: 'npc.tinderwick_shopkeeper', unless_flag: EMBER },
    { op: 'dialogue', ref: 'npc.tinderwick_shopkeeper_lit', if_flag: EMBER },
    { op: 'shop', shop: 'tinderwick_general' },
  ],
  // The Waykeeper's come-round counsel, with the first woken road in it.
  'script.waykeeper_staged': [
    { op: 'dialogue', ref: 'npc.lanternway_keeper', unless_flag: EMBER },
    { op: 'dialogue', ref: 'npc.lanternway_keeper_lit', if_flag: EMBER },
  ],
  // The Crossroads inn before the token quest. The old line promised "four
  // festivals over the hearth" while the brackets still hung empty.
  'script.inn_rest_crossroads_early': [
    { op: 'say', unless_flag: EMBER, speaker: 'INNKEEP', text: "In you come, out of the dark. Bunks first, talk after. That's the house rule, and only the kettle argues with it." },
    { op: 'say', if_flag: EMBER, speaker: 'INNKEEP', text: "In you come! The news beat you down the Lanternway: the Ember's back over Tinderwick. Half my long table is toasting it. Bunks first, talk after." },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: "There. Rested, and your kin with you. Every road is shorter after a night's sleep. That's not lore, that's arithmetic." },
    { op: 'shop', shop: 'crossroads_inn' },
  ],
  // The old lamplighter who carried the wick-key, once the Beacon burns.
  'script.dimglass_witness_staged': [
    { op: 'dialogue', ref: 'npc.dimglass_witness', unless_flag: EMBER },
    { op: 'dialogue', ref: 'npc.dimglass_witness_lit', if_flag: EMBER },
  ],
  // Wren on Dimglass Coast I: three stages (before the Beacon, after it, after the Tide).
  'script.wren_dimglass_staged': [
    { op: 'dialogue', ref: 'npc.dimglass_wayfarer', unless_flag: EMBER },
    { op: 'dialogue', ref: 'npc.dimglass_wayfarer_lit', if_flag: EMBER, unless_flag: TIDE },
    { op: 'dialogue', ref: 'npc.dimglass_wayfarer_tide', if_flag: TIDE },
  ],
  // Elspeth the letter-runner, once Reyl's battle is behind you.
  'script.flats_wayfarer_b_staged': [
    { op: 'dialogue', ref: 'npc.flats_wayfarer_b', unless_flag: TIDE },
    { op: 'dialogue', ref: 'npc.flats_wayfarer_b_lit', if_flag: TIDE },
  ],
  // Fenn on the flats, once the harbour is singing.
  'script.flats_sky_watcher_staged': [
    { op: 'dialogue', ref: 'npc.flats_sky_watcher_after', unless_flag: TIDE },
    { op: 'dialogue', ref: 'npc.flats_sky_watcher_lit', if_flag: TIDE },
  ],
  // Pearlmoor's chandlery: the buoy-wick rush.
  'script.shop_pearlmoor_staged': [
    { op: 'dialogue', ref: 'npc.pearlmoor_shopkeeper', unless_flag: TIDE },
    { op: 'dialogue', ref: 'npc.pearlmoor_shopkeeper_lit', if_flag: TIDE },
    { op: 'shop', shop: 'pearlmoor_chandlery' },
  ],
  // Pearlmoor inn, the night of the Tide-blessing (the twin's rest; same shape).
  'script.pearlmoor_inn_rest_lit': [
    { op: 'say', speaker: 'INNKEEP', text: "Rest your feet, Wayfarer. Mind the singers on the stair. They started the going-out song when the Tide stood up, and not one of them has gone out." },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: "There. Lamps trimmed, kin bright-eyed. Every room let and every guest awake. I've never been so tired, or so glad of it." },
  ],
};

export const SOUTH_DIALOGUE: DialogueRegistry = {
  // --- The 2026-10 geometry fix: the bay road + the Lantern-car signs ---
  'sign.crossroads_lantern_car': [
    { text: 'THE LANTERN-CAR\nLines to LOWLEAF (the green lamp), GALEHIGH (the storm-lamp) and NIGHTREACH (the silver lamp). A car runs once its valley\'s lamp is relit. The ride down runs any time.' },
  ],
  'sign.crossroads_bay_road': [
    { text: 'NORTH-WEST: THE BAY ROAD\nLanternfall Road, the Sounding Cave and the Wrackline shore, round the bay to Saltreach Fen and Pearlmoor. Its lamps wake with the Tide.' },
  ],
  'sign.fen_drowned_road': [
    { text: 'THE DROWNED ROAD (what the lagoon left of it)\nSOUTH along the bay shore: Wrackline Path, the Sounding Cave and Lanternfall Road, down to the Vesper Crossroads.' },
  ],

  // --- AFTER-GLEAM · Tinderwick / the Lanternway / Dimglass (gleam:ember) -----
  'npc.gatewarden_after_lit': [
    { speaker: 'GATE-WARDEN', text: "From this post you can see the beacon on the bluff. All the dark years I stood watch under a cold one. Now I catch myself nodding to it, like a neighbour." },
    { speaker: 'GATE-WARDEN', text: "The coast road's yours, and the flats past it. And the kindness I'll keep repeating: in SETTINGS you can press a copy of your journey to keep somewhere safe. Do it now and then." },
  ],
  'npc.tinderwick_shopkeeper_lit': [
    { speaker: 'SHOPKEEPER', text: "Fair-week, dear, and the whole square wants candles at once. I sold out of tapers by second bell. I've never been so pleased to be out of anything." },
    { speaker: 'SHOPKEEPER', text: "The counter's open. Charges and balms for the coast road. The flats are wide and the dune grass is restless, Gleam or no Gleam." },
  ],
  'npc.lanternway_keeper_lit': [
    { speaker: 'WAYKEEPER', text: "Every road in Vesperholm touches this stone sooner or later. The night the Ember stood up, the coast road's lamps burned a shade warmer. I felt it in my trimmer before I saw it." },
    { speaker: 'WAYKEEPER', text: 'You will walk a long way out and come back in at a gate you know. That is not you going wrong — the valleys sit in a crescent, and the way home is never the way you went out.' },
    { speaker: 'WAYKEEPER', text: 'Each Gleam that stands up wakes another road. One already has. That is how the Lanternway has always worked.' },
    { speaker: 'WAYKEEPER', text: 'The inward road still wants all eight. Count them in the sky, Wayfarer, not on your fingers. Do not hurry the dark.' },
  ],
  'npc.dimglass_witness_lit': [
    { speaker: 'OLD LAMPLIGHTER', text: "I saw it from the dunes: the Tinderwick beacon, burning on the bluff as if it had never stopped. I took my cap off to it. I haven't done that for a lamp since I was a boy." },
    { speaker: 'OLD LAMPLIGHTER', text: "Forty years I climbed those stairs with that key. I'm glad yours were the last boots on them. Walk lit, young one. The flats are long." },
  ],
  'npc.dimglass_wayfarer_lit': [
    { speaker: 'WREN', text: "You lit the BEACON? I was halfway up a dune when the whole coast went orange. I said a word Gran would wash out of my mouth." },
    { speaker: 'WREN', text: "Fine. One–nil to you. If Mum's village still watches the south sky, she'll have seen it too. ...Race you to Pearlmoor." },
  ],
  'npc.dimglass_wayfarer_tide': [
    { speaker: 'WREN', text: "Two Gleams. I meant to be annoyed about it, and then I just wasn't. I wrote Mum three pages about the harbour lights. ...She'll write back short. But she'll write back." },
  ],
  // --- AFTER-GLEAM · the flats and Pearlmoor (gleam:tide) ---------------------
  'npc.flats_wayfarer_b_lit': [
    { speaker: 'ELSPETH', text: "Pearlmoor's post doubled the night the Tide came back. Everyone wrote to someone inland to say they could hear the singing. Half of them could." },
  ],
  'npc.flats_sky_watcher_lit': [
    { speaker: 'STAR-TENDER FENN', text: "Two Gleams, child, and the harbour singing. I'll admit I walked down to the shore to hear it. The sky can mind itself for one night." },
    { speaker: 'STAR-TENDER FENN', text: "Reyl will have told you the tides go out so they can come back. He has been right about that for sixty years. It is very trying." },
  ],
  'npc.pearlmoor_fisher_lit': [
    { speaker: 'FISHER', text: "Out past the buoys last night, after dark, for the first time in eleven winters. The moon-water opened round my keel like it remembered me." },
    { speaker: 'FISHER', text: "Caught nothing. Didn't care. I just sat out there and looked at the quay lamps from the sea side, the way my father used to." },
  ],
  'npc.pearlmoor_fisher_inn_lit': [
    { speaker: 'FISHER', text: "Ask me how the night-fishing went. Go on. ...Terrible! Two sprats and a boot. Best night I've had in years." },
  ],
  'npc.pearlmoor_shopkeeper_lit': [
    { speaker: 'CHANDLER', text: "Buoy-wicks! The whole quay wants buoy-wicks. Every family's relighting its line, and I'm the only one who kept a crate through the dark. Prudence pays, Wayfarer." },
    { speaker: 'CHANDLER', text: "The counter is open. Balms for the fen-road east, if that's where the Tidecall walks you." },
  ],
  'npc.booji_andrew_lit': [
    { speaker: 'ANDREW', text: "Can't talk long. Mid-set. The Tide came back and I put ten kilos on overnight. Coincidence? The bench says no." },
    { speaker: 'ANDREW', text: "Paul stood at the window the night it rang and hummed something. Didn't spot me once. Didn't need to." },
  ],

  // --- Gullcry Rock (post-Chickenpig Tidecall spur): the wreck on the sand ---
  'npc.gullcry_wreck': [
    { text: 'The ribs of a small boat, sunk to the gunwales in sand. Someone painted a lamp on her bow, once.' },
    { text: 'The gulls have made a nest of her. They seem to think that is what she was for all along.' },
  ],
  // --- Wrackline Path (§4 #8): three inspect-only finds in the wrack --------
  'npc.wrack_find_pots': [
    { text: 'Crab pots, washed up and stacked by a tidy stranger. One still holds a very offended crab.' },
    { text: 'You leave it be. It has had a long night too.' },
  ],
  'npc.wrack_find_drift': [
    { text: 'Driftwood, worn silver. Someone has scratched a tally into it: one mark for every star gone dark this winter.' },
    { text: 'The marks stop halfway along, as if whoever kept count decided they would rather not.' },
  ],
  'npc.wrack_find_nest': [
    { text: 'A gull\'s nest of kelp and string. Woven through it, a scrap of lantern-ribbon from some Pearlmoor festival.' },
  ],
  // --- Sounding Cave (§4 #8): the sounding stone answers -------------------
  'npc.sounding_stone': [
    { text: 'You knock on the stone. The cave knocks back — three times, then once, from somewhere above you and off to the west.' },
    { text: 'Echoes don\'t usually point. This one does: back up through the moss, then west along the narrow way into the little side chamber.' },
  ],
  // --- The Wanderwood (S5): the wayfarers' board -------------------------------
  'npc.wanderwood_board': [
    { text: 'A wayfarers\' board, mossy at the corners. FOUND: one glove, left. LOST: one glove, left. Same handwriting.' },
    { text: 'Under them, newer: "If you are lost, stand still and somebody kind will come by. They always have so far."' },
  ],
};
