/**
 * Cutscene script registry — keyed by the `ref` cutscene/script triggers use
 * (EventTrigger.ref, e.g. 'script.intro_mentor'). Each is an ordered list of
 * CutsceneStep the CutsceneRunner interprets. Adding a scene is a data edit here.
 */
import type { ScriptRegistry } from './types';

export const SCRIPTS: ScriptRegistry = {
  // --- The opening: the satchel errand at the Vesper Crossroads -----------------
  // C1 (walkthrough/01-south §2) is now a small LOOP, not a tile-touch: the north
  // gate-warden turns you back (it's dangerous out there), everyone points EAST to
  // Star-tender Fenn at the Crossroads waystone, Fenn has left his satchel on the
  // Tinderwick store counter, and the lamp-and-starter ceremony happens at the
  // waystone once you bring it out to him. Warm, unhurried, never a "Professor".

  // The north gate, pre-starter: the warden (posted in the gap at (14,1)) spots the
  // player on the open column (13,1), warns them off, and walks them back a step.
  // The trigger band is hidden_when 'flag:has_starter'; the warden swaps for a
  // well-wisher (gatewarden_post) the moment the Wayfaring begins.
  'script.gate_warden': [
    { op: 'emote', actor: 'gatewarden_pre', emote: 'alert' },
    { op: 'face', actor: 'gatewarden_pre', facing: 'left' },
    { op: 'face', actor: 'player', facing: 'right' },
    { op: 'say', speaker: 'GATE-WARDEN', text: 'Whoa there, apprentice! Not one step up the coast road without a lit lamp — the grass out there is crawling with wild kin since the dusk.' },
    { op: 'say', speaker: 'GATE-WARDEN', text: 'Star-tender Fenn was asking after you this very morning. He walked out EAST, along the Lanternway — the Crossroads waystone wanted tending.' },
    { op: 'say', speaker: 'GATE-WARDEN', text: 'Go on, find him. He had that look about him. The one that means it is YOUR turn.' },
    { op: 'move', actor: 'player', to: { tx: 13, ty: 3 } },
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'gatewarden_pre', facing: 'down' },
  ],

  // Crossing into the waystone plaza for the first time: Fenn hails the player
  // from across the clearing so there's no "who do I talk to?" beat to fumble.
  'script.fenn_wave': [
    { op: 'emote', actor: 'fenn_pre', emote: 'alert' },
    { op: 'cameraFocus', actor: 'fenn_pre', ms: 500 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Ho — over here, apprentice! By the waystone!' },
    { op: 'cameraReset', ms: 500 },
  ],

  // Fenn at the waystone: delight, then the small ask — his satchel, forgotten on
  // the Tinderwick store counter, with the whole Wayfaring packed inside it.
  'script.fenn_crossroads': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'There you are. The sky lost another light in the small hours — I felt it go. So I came out to tend the waystone lamp... and to wait for you.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'It is time for your Wayfaring, at last. I have everything you need right here in my—' },
    { op: 'emote', actor: 'fenn_pre', emote: 'sweat' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: '...my satchel. Which is sitting on the counter of the Tinderwick store, sure as sunrise used to be. Old hands, old head.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Run it out to me, would you? Back west along the Lanternway — the lamps hold that road safe. Your Wayfaring can spare you one small errand first.' },
    { op: 'setFlag', flag: 'flag:fenn_errand' },
  ],

  // The satchel on the store counter (an item_cache placement in tinderwick_shop;
  // appears once Fenn asks, vanishes once taken).
  'script.take_satchel': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'fenn_satchel', count: 1 },
    { op: 'say', text: "The Star-tender's field-satchel, heavier than it looks. Took FENN'S SATCHEL!" },
    { op: 'setFlag', flag: 'flag:has_satchel' },
  ],

  // The ceremony at the waystone: the satchel comes home, and out of it come the
  // two things every Wayfarer leaves with. The cosy bed holds; the grave notes ride
  // portraits, not music changes — warmth held, dread only in Fenn's face.
  'script.intro_mentor': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'My satchel — and my apprentice. Both delivered by the same pair of feet. A tidy omen, that.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Now. Every Wayfarer leaves with two things, and they have been riding in this old bag all along.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'The first — a lamp, to carry the light home. Take it. Your vesperlamp.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.28, ms: 240 }, // a warm bloom as the lamp kindles
    { op: 'giveItem', item: 'vesperlamp', count: 1 },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 600 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'And the second — a friend, to share the walk through the dark. Go on. Choose.' },
    { op: 'giveStarter' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'Mind you tend them both, and they will tend you. And fitting, is it not — every Wayfaring in Vesperholm begins at a crossroads.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Back along the Lanternway with you now. Catch a kin in the verge by the north gate — the keeper holds a Wayfarer\'s kit for you, town custom — then go see Brisa at the Lumenary.' },
    { op: 'setFlag', flag: 'flag:has_vesperlamp' },
    { op: 'setFlag', flag: 'flag:has_starter' },
  ],

  // (The first Gleam moved from the Lumenary hall to the BEACON TOP —
  // script.beacon_battle below; the hall now stages Brisa's quest beats.)

  // The Beacon's wick-tenders — SIGHT trainers on the stair floors.
  'script.beacon_keeper_a': [
    { op: 'say', speaker: 'TANSY', text: 'A climber! Brisa said the key might come home today. Floor rule, though — every flame is tested.' },
    { op: 'battle', trainer: 'beacon_keeper_a' },
    { op: 'say', speaker: 'TANSY', text: 'Steady enough for the stairs. Up you go!' },
    { op: 'setFlag', flag: 'flag:beacon_keeper_a_beaten' },
  ],
  'script.beacon_keeper_b': [
    { op: 'say', speaker: 'COLE', text: 'Tansy let you past? Then one test left before the lantern room. Mine is not so gentle.' },
    { op: 'battle', trainer: 'beacon_keeper_b' },
    { op: 'say', speaker: 'COLE', text: 'Well burned. The lantern room is just above — Brisa is already there.' },
    { op: 'setFlag', flag: 'flag:beacon_keeper_b_beaten' },
  ],

  // Second Lumenary (pearlmoor_lumenary): the player crosses the sea-shrine chamber to
  // old ferryman Reyl Wash, hears him out, battles him, and on victory relights the Tide
  // constellation — the second Gleam, wrapped in the Tide-blessing festival (Arc E). The
  // trainer's reward_flags ('gleam:tide', 'crown_south') AND reward_abilities ('tidecall')
  // are applied by the BattleScene on a win; here we add the diegetic Gleam cue and the
  // closing beat handing over the Lantern Gift.
  'script.lumenary_pearlmoor': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'reyl', facing: 'down' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'weathered', text: 'Came on foot, did you — no need of the tides to reach my door. Good. The light should be free to all who seek it.' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'neutral', text: 'Now. Read the water with me, Wayfarer, and we shall see if the sea will listen to you.' },
    { op: 'battle', trainer: 'lampwarden_pearlmoor' },
    // The second Gleam, wrapped in the Tide-blessing — same minor→major payoff, in a
    // cool moon-on-water key rather than Tinderwick's ember-warm one.
    { op: 'musicFade', ms: 500 },
    { op: 'tint', color: '#4fb4ff', alpha: 0.36, ms: 600 },
    { op: 'narrate', text: 'Reyl rings the moor-bell. Out on the black water, buoy after buoy answers — and overhead, the Tide remembers how to shine.' },
    { op: 'gleam', element: 'tide' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'proud', text: 'The Tide Gleam stands up over Pearlmoor again. And the Tidecall is yours — go on, ask the shallows to part. The harbour keeps its secrets for those who can cross.' },
  ],

  // A2 (Dimglass Coast I): Wren's first FRIENDLY trainer battle. Wren is a SIGHT
  // trainer — spots the player on the lane, runs up (the engine plays the alert +
  // approach), and this script carries the words + battle. Low-stakes by design.
  'script.wren_dimglass': [
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'There you are! I was starting to think the grass ate you.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: "Listen — every Wayfarer's first proper battle should be with a friend. So?" },
    { op: 'battle', trainer: 'wren_dimglass' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'Same road, different lamps. See you up the coast!' },
    { op: 'setFlag', flag: 'flag:wren_dimglass_battled' },
  ],

  // B1 (Dimglass Coast I): the inciting incident — a far constellation winks out on the
  // first nightfall here. The dread is in the QUIET: letterbox in, fade the bed to
  // silence and hold, then the gutter sting + cold wash + shake as the star dies. This
  // is the first-hour's load-bearing foreboding beat (walkthrough/01-south; the
  // cinematic cadence is binding — see docs/world/cinematics.md).
  'script.dusk_begins': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'silence', ms: 1200 }, // the held quiet before the light fails
    { op: 'narrate', text: 'Far out over the water, a constellation flickers — and goes dark.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'tint', color: '#0b1026', alpha: 0.55, ms: 180 }, // the dark presses in
    { op: 'shake', ms: 320, intensity: 0.006 },
    { op: 'narrate', text: 'For a heartbeat, every lantern-buoy on the coast gutters, as if the sea itself flinched.' },
    { op: 'tint', color: '#0b1026', alpha: 0, ms: 700 },
    { op: 'narrate', text: "That's the third star gone south of here this month. The Long Dusk is getting deeper — and it is getting closer." },
    { op: 'musicCrossfade', key: 'dimglass-coast-a', ms: 900 }, // the bed returns, a shade uneasier
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // Dimglass Coast II route trainers (the XP bridge toward Pearlmoor's 12) —
  // SIGHT trainers: the engine plays the alert + walk-up, these carry the words.
  'script.flats_trainer_a': [
    { op: 'say', speaker: 'MORROW', text: 'Hold up there, Wayfarer! The flats test every lamp that crosses — mine first.' },
    { op: 'battle', trainer: 'flats_wayfarer_a' },
    { op: 'say', speaker: 'MORROW', text: 'Well fought. The dune grass ahead is livelier than it looks — good place to toughen up.' },
    { op: 'setFlag', flag: 'flag:flats_trainer_a_beaten' },
  ],
  'script.flats_trainer_b': [
    { op: 'say', speaker: 'ELSPETH', text: 'A letter-runner never passes a fellow lamp without a bout. Rules of the road!' },
    { op: 'battle', trainer: 'flats_wayfarer_b' },
    { op: 'say', speaker: 'ELSPETH', text: 'Ha! Reyl Wash at Pearlmoor — now THERE is a battle worth the walk. Go see.' },
    { op: 'setFlag', flag: 'flag:flats_trainer_b_beaten' },
  ],

  // --- The Beacon quest (Tinderwick's earned first Gleam) ---------------------
  // Brisa sends the new Wayfarer up the coast road for the beacon's lost
  // wick-key before she'll hold the bond-test at the lantern.
  'script.brisa_quest': [
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'So you have made your first friend. Good. Then hear the truth of it, dear — the Ember is not relit from this hall.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: 'It is relit from the OLD BEACON, on the bluff east of the square. And the beacon has stood dark since its wick-key was lost on the coast road.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: 'The old lamplighter who carried it walks Dimglass Coast still, up by the north boundary. Find him. Bring the key home.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'Mind the grass, mind the dark — and come back stronger than you leave. The lantern asks a steady flame.' },
    { op: 'setFlag', flag: 'flag:beacon_quest' },
  ],
  // The old lamplighter (Dimglass I, appears after dusk_begins) hands the key. His
  // closing aside is the first-hour's quiet Hollowing SEED — a cold that "follows the
  // dark down off the north road" — foreboding only, no name, no fight (B2 still
  // introduces the Hollowing formally in East; see docs/world/cinematics.md §tone).
  'script.give_wick': [
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'grave', text: 'You stood under it too, did you. One breath it was there — the next, a hole in the sky shaped like a star.' },
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'neutral', text: 'Third one this season. I am too old to climb the Tinderwick beacon now... but you are not, are you.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_wick', count: 1 },
    { op: 'say', text: 'The lamplighter presses a worn brass key into your hand. Received the BEACON WICK-KEY!' },
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'grave', text: "And mind yourself out past the north boundary. There's a cold that follows the dark down off that road — quiet, and patient, and it doesn't feel like weather." },
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'neutral', text: 'Tell Brisa Tallow the road is darker than she remembers. And walk LIT, young one.' },
    { op: 'setFlag', flag: 'flag:has_beacon_wick' },
  ],
  // The lantern room, beacon top: the bond-test, then the Ember Gleam relit FROM
  // THE TOWER — the first constellation answering the town's own light.
  'script.beacon_battle': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'brisa', facing: 'down' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'Up all those dark stairs with the wick-key in your hand. The lamp-tender chose well.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: 'This lantern lit the Ember for three hundred years, dear. Show me your flame is steady enough to wake it.' },
    { op: 'battle', trainer: 'lampwarden_tinderwick' },
    // The Gleam payoff: minor→major. Hold a beat of silence, the lantern blooms (warm
    // wash + the lamp sfx), the constellation answers (gleam sting + flash), then the
    // festival swell rises as the town below begins to dance (Arc E).
    { op: 'musicFade', ms: 500 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.4, ms: 600 },
    { op: 'narrate', text: 'Brisa turns the wick-key. The great lantern blooms — and far above, in the dark, a warm light answers.' },
    { op: 'gleam', element: 'ember' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'proud', text: 'There — the Ember Gleam burns again in the southern sky. Go down to the square, dear. I believe the town wants to dance with you.' },
  ],

  // --- Rest points (the genre's heal loop, diegetic) -------------------------
  // The inn: a paid-in-kindness full rest. The innkeep NPC's dialogue_ref runs this.
  'script.inn_rest': [
    { op: 'say', speaker: 'INNKEEP', text: 'Rest your feet, Wayfarer — and your kin. The hearth is warm and the boards are dry.' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'INNKEEP', text: 'There. Lamps trimmed, kin bright-eyed. The dusk can wait on you a while yet.' },
  ],
  // Home: the bed in the apprentice's house. Free, always — home is home.
  'script.home_rest': [
    { op: 'say', text: 'Your own bed, under the old quilt. The lamp hums low...' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', text: 'You wake warm. Your kin are rested and bright.' },
  ],

  // --- Wayfarer's kits + the open counters ------------------------------------
  // Each town keeper hands a starter bundle ONCE (the kit NPC swaps for the
  // trading keeper via flags), and thereafter keeps a live counter: the keeper's
  // script says its flavour line then opens the shop (content/shops.ts) with the
  // 'shop' op. Buying/selling is the ShopMenu; prices live on the ItemDefs.
  'script.shop_kit_tinderwick': [
    { op: 'say', speaker: 'SHOPKEEPER', text: 'Welcome in, out of the dusk. Off on your Wayfaring? Then the first kit is on the house — town custom.' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', speaker: 'SHOPKEEPER', text: 'Two spare lamps and a pot of tallow balm. Lamp catches a kin; balm mends one. The road north is long.' },
    { op: 'setFlag', flag: 'flag:tinderwick_kit' },
  ],
  'script.shop_kit_pearlmoor': [
    { op: 'say', speaker: 'CHANDLER', text: 'Welcome in off the boards. Facing Reyl, are you? Take the crossing-kit — the sea is kinder to the prepared.' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', speaker: 'CHANDLER', text: 'Feed a charge to your lamp before a throw — a charged flame holds a catch better than a plain one. And mind the triangle — his whole crew runs Tide.' },
    { op: 'setFlag', flag: 'flag:pearlmoor_kit' },
  ],

  // The open counters (the post-kit keepers' dialogue_refs point here).
  'script.shop_tinderwick': [
    { op: 'dialogue', ref: 'npc.tinderwick_shopkeeper' },
    { op: 'shop', shop: 'tinderwick_general' },
  ],
  'script.shop_pearlmoor': [
    { op: 'dialogue', ref: 'npc.pearlmoor_shopkeeper' },
    { op: 'shop', shop: 'pearlmoor_chandlery' },
  ],

  // --- Route item caches (sprite 'item_cache' NPCs; vanish via hidden_when_flag)
  'script.pickup_dimglass_balm': [
    { op: 'giveItem', item: 'tallow_balm', count: 1 },
    { op: 'say', text: 'A waxed bundle, left for whoever needs it. Found a TALLOW BALM!' },
    { op: 'setFlag', flag: 'flag:picked_dimglass_balm' },
  ],
  'script.pickup_dimglass_lamps': [
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'say', text: "A wayfarer's drop-cache under the lamp post. Found 2 GLOW CHARGES!" },
    { op: 'setFlag', flag: 'flag:picked_dimglass_lamps' },
  ],
  'script.pickup_flats_balm': [
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', text: 'Sea-wrapped and sound. Found 2 TALLOW BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_flats_balm' },
  ],
  'script.pickup_flats_lamp': [
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: 'Tucked dry in the dune grass. Found a GLOW CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_flats_lamp' },
  ],
  // The cache-variety finds (spine rule): a found-to-sell nugget in Tinderwick's
  // SW corner, and loose wicks west of the flats' lane.
  'script.pickup_tinderwick_waxcake': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'wax_cake', count: 1 },
    { op: 'say', text: 'Wrapped in oilcloth behind the hedgerow — a pressed WAX CAKE! Any keeper will trade well for it.' },
    { op: 'setFlag', flag: 'flag:picked_tinderwick_waxcake' },
  ],
  'script.pickup_flats_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 80 },
    { op: 'say', text: "A dropped courier's purse, half-buried in the sand. Found 80 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_flats_wicks' },
  ],
  // --- Glowmoss Deep (East) — the first cave dungeon + the B2 set-piece -------
  // The deep wood's sight keepers (level-design §11 rule 7): they hold the lane
  // into the moss chambers and the gallery out toward the mine.
  'script.glowmoss_keeper_a': [
    { op: 'say', speaker: 'DELL', text: 'Hold the lane, Wayfarer! Past me are the nursery beds — every moss-mound a hundred years of held light.' },
    { op: 'say', speaker: 'DELL', text: 'Show me your lamp walks soft before I let it walk far.' },
    { op: 'battle', trainer: 'glowmoss_keeper_a' },
    { op: 'say', speaker: 'DELL', text: 'Soft enough. Go on, then... and mind the grey chamber past the beds. Something has been TENDING it, and not kindly.' },
    { op: 'setFlag', flag: 'flag:glowmoss_keeper_a_beaten' },
  ],
  'script.glowmoss_keeper_b': [
    { op: 'say', speaker: 'MIRREL', text: 'Out of the grey chamber with your lamp still lit. Most come out quieter than they went in.' },
    { op: 'say', speaker: 'MIRREL', text: 'One more test before the mine road, then. Deepwood custom.' },
    { op: 'battle', trainer: 'glowmoss_keeper_b' },
    { op: 'say', speaker: 'MIRREL', text: 'Well held. The mine-mouth lies east — tell old Otho Grist the deep wood sent you.' },
    { op: 'setFlag', flag: 'flag:glowmoss_keeper_b_beaten' },
  ],

  // B2 — FIRST HOLLOWING CONTACT (walkthrough/02-east; cinematics.md cadence:
  // a "light fails" beat — letterbox, silence, the cold wash; the dread is the
  // gentleness). Fires on the only choke into the drained site; the cast are
  // NPC placements (acolyte_a/b, cowled_figure, sleeping_fennlight) that
  // withdraw via hidden_when_flag once the lantern is relit.
  'script.glowmoss_drained': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'silence', ms: 1400 }, // the moss-light dies at the choke-stone
    { op: 'narrate', text: 'The glow stops at the choke-stone, as if it had been told to. Past it, the moss lies GREY — a whole chamber of kept light, gone out.' },
    { op: 'tint', color: '#202430', alpha: 0.4, ms: 600 }, // the drained cold
    { op: 'cameraFocus', to: { tx: 17, ty: 8 }, ms: 900 },
    { op: 'narrate', text: 'At the heart of it a Fennlight lies curled in the dead moss, dim as a coal under ash. It is not hurt. It is not waking. Beside it stands a lantern built to hold nothing at all.' },
    { op: 'say', speaker: 'ACOLYTE', text: 'Oh — a Wayfarer. Please, tread soft. She is not hurt. She is RESTING.' },
    { op: 'say', speaker: 'ACOLYTE', text: 'Does the quiet not look gentle, after all that flickering? No more guttering. No more going out. Just... rest.' },
    { op: 'say', speaker: 'ACOLYTE', text: 'We are the Hollowing. Our Warden Còr teaches that the dark asks nothing of anyone. We only help the tired lights lie down.' },
    { op: 'cameraFocus', to: { tx: 20, ty: 7 }, ms: 800 },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'At the chamber\'s far edge a cowled figure stands very still, watching you. It bows its head — sorrowing, almost kind — then turns, and is gone into the dark.' },
    { op: 'cameraReset', ms: 600 },
    { op: 'tint', color: '#202430', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'The null-lantern waits beside the sleeping kin, holding its little piece of dark. Your vesperlamp leans toward it like a struck note.' },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // The null-lantern restoration — the first time the player UNDOES the
  // Hollowing's work. QUIET by design (a small warm bloom, no festival swell —
  // this is grief eased, not a Gleam). Sets flag:met_hollowing via the trigger;
  // the site's cast swaps grey→green on the flag (the §8 null-lantern pattern).
  'script.glowmoss_relight': [
    { op: 'cameraFocus', to: { tx: 18, ty: 8 }, ms: 700 },
    { op: 'narrate', text: 'The null-lantern stands cold at the chamber\'s heart. You raise your vesperlamp and touch flame to the hollow wick.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#9fe8b8', alpha: 0.3, ms: 600 }, // a small green-gold bloom
    { op: 'narrate', text: 'It takes — small, stubborn, certain. Colour climbs back through the moss-beds like water finding old roots.' },
    { op: 'tint', color: '#9fe8b8', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'In the green hush, the Fennlight stirs — blinks — and lifts into the air, trailing light like pollen.' },
    { op: 'narrate', text: 'The acolytes gather their grey bundles without a word. The last of them pauses at the passage mouth, bows to the waking glow, and follows the dark out.' },
    { op: 'setFlag', flag: 'flag:met_hollowing' },
    { op: 'cameraReset', ms: 600 },
  ],

  // Glowmoss Deep item caches (the standing kit: one valuable, one consumable,
  // one loose-wicks find — walkthrough README "Item caches").
  'script.pickup_glowmoss_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'Half-buried in the oldest moss-bed: a bead of resin with a glow-moth caught mid-shimmer. Found a MOTH-AMBER!' },
    { op: 'say', text: 'It still holds a little light. A keeper would trade a fair purse for it.' },
    { op: 'setFlag', flag: 'flag:picked_glowmoss_amber' },
  ],
  'script.pickup_glowmoss_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'A waxed tin left where the moss grows thickest, still warm to the touch. Found a WARM BALM!' },
    { op: 'setFlag', flag: 'flag:picked_glowmoss_balm' },
  ],
  'script.pickup_glowmoss_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 200 },
    { op: 'say', text: "A miner's drop-purse, stitched shut against the damp. Found 200 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_glowmoss_wicks' },
  ],
  // B1F dead-end A: the maze pays in kind — a Star-chart, dry in its tube.
  'script.pickup_b1f_chart': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'chart_focus_mind', count: 1 },
    { op: 'say', text: 'A chart-tube wedged in the rocks, sound and dry. Found a STAR-CHART: FOCUS MIND!' },
    { op: 'setFlag', flag: 'flag:picked_b1f_chart' },
  ],

  // --- Saltreach Fen I (East) — the marsh route's beats ------------------------
  'script.fen_wader_a': [
    { op: 'say', speaker: 'MARIGOLD', text: 'Hold the plank, friend! Fen custom — two lamps that meet on one causeway test their wicks.' },
    { op: 'battle', trainer: 'fen_wader_a' },
    { op: 'say', speaker: 'MARIGOLD', text: 'A dry flame in a wet country — well kept. The fen will let you by.' },
    { op: 'setFlag', flag: 'flag:fen_wader_a_beaten' },
  ],
  'script.fen_courier_b': [
    { op: 'say', speaker: 'OSPREY', text: 'Post for Lowleaf — and a standing toll for the north shore. Paid in a bout, not in wicks!' },
    { op: 'battle', trainer: 'fen_courier_b' },
    { op: 'say', speaker: 'OSPREY', text: 'Toll paid in full. The channel ahead answers Tidecall — Pearlmoor taught you that one, I hope.' },
    { op: 'setFlag', flag: 'flag:fen_courier_b_beaten' },
  ],
  'script.pickup_fen_reed': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: 'Tucked behind the reed screen, dry in its wax wrap. Found a GLOW CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_fen_reed' },
  ],
  'script.pickup_fen_bank_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 150 },
    { op: 'say', text: "A wader's purse, left high and dry on the bank. Found 150 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_fen_bank_wicks' },
  ],
  'script.pickup_grotto_starglass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Wedged in the spore-soft dark, a sliver of fallen sky. Found a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_grotto_starglass' },
  ],
  'script.pickup_fen_islet': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'Only the tide-walkers reach this islet — and whoever left a WARM BALM for them.' },
    { op: 'setFlag', flag: 'flag:picked_fen_islet' },
  ],

  // Gullcry Rock's prize: the Tide Charm (a sea-blessed lamp; see items.ts).
  'script.pickup_gullcry_charm': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'tide_charm', count: 1 },
    { op: 'say', text: 'Lashed to the highest stone, wave-worn and humming. Found the TIDE CHARM!' },
    { op: 'say', text: 'It beats softly in your hand, like a held breath of the sea.' },
    { op: 'setFlag', flag: 'flag:picked_gullcry_charm' },
  ],
};

export function getScript(ref: string): import('./types').CutsceneStep[] | undefined {
  return SCRIPTS[ref];
}
