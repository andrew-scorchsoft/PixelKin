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
    { op: 'say', speaker: 'WAYKEEPER', text: 'That winch is the [[LANTERN-CAR]]: cables up the mountain to Lowleaf, Galehigh and Nightreach. Days of walking, swung over in a breath.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'But a line runs only while its far lamp burns. [[Relight a valley\'s constellation]] and its car will carry you there.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'Till then, boots and the long way round. You\'ll find more on foot than any car could show you.' },
    { op: 'face', actor: 'waykeeper', facing: 'down' },
  ],
  'script.lantern_car': [
    { op: 'narrate', text: 'THE LANTERN-CAR. Three cables climb into the dark, each with a little lamp on the rail.' },
    { op: 'narrate', unless_flag: 'gleam:verdant', text: 'Every line-lamp is cold. No car runs until a valley\'s light is relit.' },
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
            { op: 'narrate', text: 'The green lamp catches. The car swings out over the bay, the Crossroads\' lights shrinking below...' },
            { op: 'travel', map: 'lanternway_lowleaf', to: { tx: 3, ty: 24 }, facing: 'up' },
          ],
        },
        {
          label: 'GALEHIGH',
          if_flag: 'gleam:storm',
          ops: [
            { op: 'sfx', key: 'world-lantern-light' },
            { op: 'narrate', text: 'The storm-lamp catches. The car climbs the eastern flank, rocking in the updraughts...' },
            { op: 'travel', map: 'lanternway_galehigh', to: { tx: 6, ty: 16 }, facing: 'up' },
          ],
        },
        {
          label: 'NIGHTREACH',
          if_flag: 'gleam:lunar',
          ops: [
            { op: 'sfx', key: 'world-lantern-light' },
            { op: 'narrate', text: 'The silver lamp catches. The longest line: over the mountain\'s dark shoulder, riding among the stars...' },
            { op: 'travel', map: 'lanternway_nightreach', to: { tx: 4, ty: 7 }, facing: 'down' },
          ],
        },
      ],
    },
  ],
  'script.lantern_car_down_lowleaf': [
    {
      op: 'choice',
      prompt: 'The Lantern-car waits. Ride down to the [[Vesper Crossroads]]?',
      options: [{ label: 'RIDE DOWN', ops: [
        { op: 'narrate', text: 'The car rolls off under its own weight, sinking toward the Crossroads\' lamps.' },
        { op: 'travel', map: 'vesper_crossroads', to: { tx: 17, ty: 8 }, facing: 'down' },
      ] }],
    },
  ],
  'script.lantern_car_down_galehigh': [
    {
      op: 'choice',
      prompt: 'The Lantern-car waits. Ride down to the [[Vesper Crossroads]]?',
      options: [{ label: 'RIDE DOWN', ops: [
        { op: 'narrate', text: 'The car drops off the shelf and runs down the long cable.' },
        { op: 'travel', map: 'vesper_crossroads', to: { tx: 17, ty: 8 }, facing: 'down' },
      ] }],
    },
  ],
  'script.lantern_car_down_nightreach': [
    {
      op: 'choice',
      prompt: 'The Lantern-car waits. Ride down to the [[Vesper Crossroads]]?',
      options: [{ label: 'RIDE DOWN', ops: [
        { op: 'narrate', text: 'The car slips off the observatory\'s shoulder and glides down to the Crossroads\' small warm lights.' },
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
    { op: 'say', unless_flag: EMBER, speaker: 'INNKEEP', text: "In you come, out of the dark. Bunks first, talk after — only the kettle argues." },
    { op: 'say', if_flag: EMBER, speaker: 'INNKEEP', text: "In you come! The Ember's back over Tinderwick — half my table's toasting it. Bunks first, talk after." },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: "There. Every road's shorter after a night's sleep. That's not lore, that's arithmetic." },
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
    { op: 'say', speaker: 'INNKEEP', text: "Mind the singers on the stair. They began the going-out song when the Tide stood up, and not one has gone out." },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: 'Morning! ...Have you ever considered taking a virtuous day?' },
    { op: 'say', speaker: 'INNKEEP', text: "A day off. Not because you're poorly — just virtuous to yourself. The road will keep." },
    { op: 'say', speaker: 'INNKEEP', text: "Kin bright-eyed, every room let, every guest awake. Never been so tired, or so glad of it." },
  ],
};

export const SOUTH_DIALOGUE: DialogueRegistry = {
  // --- The 2026-10 geometry fix: the bay road + the Lantern-car signs ---
  'sign.crossroads_lantern_car': [
    { text: 'THE LANTERN-CAR\nTo [[LOWLEAF]], [[GALEHIGH]] and NIGHTREACH. A car runs once its valley\'s lamp is relit. Down runs any time.' },
  ],
  'sign.crossroads_bay_road': [
    { text: 'NORTH-WEST: THE BAY ROAD\nLanternfall Road, the Sounding Cave and the Wrackline, round to [[Saltreach Fen]] and [[Pearlmoor]].' },
  ],
  'sign.fen_drowned_road': [
    { text: 'THE DROWNED ROAD\nSOUTH along the shore: Wrackline Path, the Sounding Cave, Lanternfall Road, to the [[Vesper Crossroads]].' },
  ],

  // --- AFTER-GLEAM · Tinderwick / the Lanternway / Dimglass (gleam:ember) -----
  'npc.gatewarden_after_lit': [
    { speaker: 'GATE-WARDEN', text: "All the dark years I watched under a cold beacon. Now I catch myself nodding to it, like a neighbour." },
    { speaker: 'GATE-WARDEN', text: "The coast road's yours. And now and then, keep a copy of your journey: [[SETTINGS, Backup / restore]]." },
  ],
  'npc.tinderwick_shopkeeper_lit': [
    { speaker: 'SHOPKEEPER', text: "Fair-week, dear! Sold out of tapers by second bell. Never been so pleased to be out of anything." },
    { speaker: 'SHOPKEEPER', text: "Charges and balms for the coast road. The dune grass is restless, Gleam or no Gleam." },
  ],
  'npc.lanternway_keeper_lit': [
    { speaker: 'WAYKEEPER', text: "The night the Ember stood up, the coast road's lamps burned warmer. I felt it in my trimmer before I saw it." },
    { speaker: 'WAYKEEPER', text: 'You will walk out and come back in at a gate you know. That is not going wrong — the way home is never the way out.' },
    { speaker: 'WAYKEEPER', text: 'Each Gleam wakes another road. One already has.' },
    { speaker: 'WAYKEEPER', text: 'The inward road wants all eight. Count them in the sky, not on your fingers.' },
  ],
  'npc.dimglass_witness_lit': [
    { speaker: 'OLD LAMPLIGHTER', text: "I saw the beacon from the dunes, burning as if it had never stopped. I took my cap off to it, like a boy." },
    { speaker: 'OLD LAMPLIGHTER', text: "Forty years I climbed those stairs. Glad yours were the last boots on them. Walk lit, young one." },
  ],
  'npc.dimglass_wayfarer_lit': [
    { speaker: 'WREN', text: "You lit the BEACON? The whole coast went orange. I said a word Gran would wash out of my mouth." },
    { speaker: 'WREN', text: "Fine. One–nil. If Mum's village watches the south sky, she saw it too. ...Race you to [[Pearlmoor]]." },
  ],
  'npc.dimglass_wayfarer_tide': [
    { speaker: 'WREN', text: "Two Gleams. I meant to be annoyed, then wasn't. I wrote Mum three pages. ...She'll write back short. But she'll write back." },
  ],
  // --- AFTER-GLEAM · the flats and Pearlmoor (gleam:tide) ---------------------
  'npc.flats_wayfarer_b_lit': [
    { speaker: 'ELSPETH', text: "The post doubled when the Tide came back. Everyone wrote inland that they could hear the singing. Half could." },
  ],
  'npc.flats_sky_watcher_lit': [
    { speaker: 'STAR-TENDER FENN', text: "Two Gleams, child, and the harbour singing. I walked down to hear it. The sky can mind itself one night." },
    { speaker: 'STAR-TENDER FENN', text: "Reyl will have said tides go out so they can come back. He has been right for sixty years. It is very trying." },
  ],
  'npc.pearlmoor_fisher_lit': [
    { speaker: 'FISHER', text: "Out past the buoys after dark, first time in eleven winters. The moon-water opened round my keel like it remembered me." },
    { speaker: 'FISHER', text: "Caught nothing. Just watched the quay lamps from the sea side, the way my father used to." },
  ],
  'npc.pearlmoor_fisher_inn_lit': [
    { speaker: 'FISHER', text: "Ask me how the night-fishing went. ...Terrible! Two sprats and a boot. Best night in years." },
  ],
  'npc.pearlmoor_shopkeeper_lit': [
    { speaker: 'CHANDLER', text: "Buoy-wicks! Every family's relighting its line, and I alone kept a crate through the dark. Prudence pays." },
    { speaker: 'CHANDLER', text: "Balms for the fen-road [[east]], if that's where the Tidecall walks you." },
  ],
  'npc.booji_andrew_lit': [
    { speaker: 'ANDREW', text: "Can't talk long. Mid-set. The Tide came back and I put ten kilos on overnight. Coincidence? The bench says no." },
    { speaker: 'ANDREW', text: "Paul stood at the window the night it rang and hummed something. Didn't spot me once. Didn't need to." },
  ],

  // --- Gullcry Rock (post-Chickenpig Tidecall spur): the wreck on the sand ---
  'npc.gullcry_wreck': [
    { text: 'A small boat sunk in the sand, a lamp painted on her bow. The gulls think she was built to be their nest.' },
  ],
  // --- Wrackline Path (§4 #8): three inspect-only finds in the wrack --------
  'npc.wrack_find_pots': [
    { text: 'Washed-up crab pots. One holds a very offended crab. You leave it be — it\'s had a long night too.' },
  ],
  'npc.wrack_find_drift': [
    { text: 'Silver driftwood, scratched with a tally: one mark for every star gone dark this winter.' },
    { text: 'The marks stop halfway, as if the counter would rather not.' },
  ],
  'npc.wrack_find_nest': [
    { text: 'A gull\'s nest of kelp and string, woven with a scrap of Pearlmoor festival ribbon.' },
  ],
  // --- Sounding Cave (§4 #8): the sounding stone answers -------------------
  'npc.sounding_stone': [
    { text: 'You knock. The cave knocks back — three, then one — from above and off to the west.' },
    { text: 'Echoes don\'t usually point. This one does: back up through the moss, then [[west to the side chamber]].' },
  ],
  // --- The Wanderwood (S5): the wayfarers' board -------------------------------
  'npc.wanderwood_board': [
    { text: 'A wayfarers\' board. FOUND: one glove, left. LOST: one glove, left. Same handwriting.' },
    { text: 'Newer: "If you are lost, stand still. Somebody kind will come by. They always have so far."' },
  ],
};
