/**
 * Item registry. Inventory only stores counts; this maps an item id to its
 * definition. New item = an entry here. The vesperlamp is the player's core
 * capture device (PixelKin's original equivalent of the genre's capture tool).
 *
 * Prices are in WICKS and must match docs/mechanics/10-economy.md (the design
 * + tuning doc); after changing a price, re-run the progression model
 * (`node tools/balance/progression.mjs`). No price = never sold (key items,
 * quest charms); 'valuable' items exist to be sold and carry `sell` instead.
 */
import type { ItemDef, ItemRegistry } from './types';

export const ITEMS: ItemRegistry = {
  // --- The lamp & its charges ------------------------------------------------
  // The vesperlamp is THE device — given once at the ceremony, never spent. A
  // plain throw is always free (×1.0). Charges are waxed cells fed to the lamp
  // for ONE brighter throw; better charges, better odds (docs/mechanics/04-capture.md).
  vesperlamp: {
    id: 'vesperlamp',
    name: 'Vesperlamp',
    desc: 'Your lamp-tender\'s lantern, warm in the hand. Raised toward a wild kin, it coaxes them to walk with you.',
    category: 'key',
  },
  glow_charge: {
    id: 'glow_charge',
    name: 'Glow Charge',
    desc: 'A waxed charge cell for the vesperlamp. One throw burns keener — better odds of befriending a wild kin.',
    category: 'charge',
    catch_bonus: 1.5,
    price: 200,
  },
  beacon_charge: {
    id: 'beacon_charge',
    name: 'Beacon Charge',
    desc: 'A chandler\'s pressed cell, near daylight in the lamp. One blazing throw — the surest catch wicks can buy.',
    category: 'charge',
    catch_bonus: 2.5,
    price: 600,
  },
  starlamp: {
    id: 'starlamp',
    name: 'Starlamp',
    desc: 'A cell of caught starlight, the rarest of gifts. The kin it is raised toward always comes — no wild heart refuses a star.',
    category: 'charge',
    catch_bonus: 255,
  },
  tallow_balm: {
    id: 'tallow_balm',
    name: 'Tallow Balm',
    desc: 'A warm salve that mends a kin a little. Restores some health.',
    category: 'medicine',
    heal: 20,
    price: 120,
  },
  warm_balm: {
    id: 'warm_balm',
    name: 'Warm Balm',
    desc: 'A richer salve, kept soft by a coal in the tin. Restores a good deal of health.',
    category: 'medicine',
    heal: 60,
    price: 500,
  },
  bright_balm: {
    id: 'bright_balm',
    name: 'Bright Balm',
    desc: 'A chandler\'s cure-all, golden and lamp-warmed. Fully restores a kin\'s health.',
    category: 'medicine',
    heal: 999,
    price: 1200,
  },
  fenn_satchel: {
    id: 'fenn_satchel',
    name: "Fenn's Satchel",
    desc: 'The Star-tender\'s worn field-satchel, left on the store counter. Heavier than it looks — a Wayfaring lives in it.',
    category: 'key',
  },
  beacon_wick: {
    id: 'beacon_wick',
    name: 'Beacon Wick-key',
    desc: "The worn brass key to the Tinderwick beacon's foot door, carried home from the coast road.",
    category: 'key',
  },
  net_floats: {
    id: 'net_floats',
    name: 'Net-floats',
    desc: 'A string of cork floats stamped with the Pearlmoor netmender\'s mark, carried south by the storm and home by you.',
    category: 'key',
  },
  bell_rope: {
    id: 'bell_rope',
    name: 'Moor-bell Rope',
    desc: 'The netmender\'s bell-rope, salt-stiff and sound, spliced for the silent shrine at the breakwater\'s end.',
    category: 'key',
  },
  fenn_letter: {
    id: 'fenn_letter',
    name: "Gran's Letter",
    desc: 'A letter for Star-tender Fenn, sealed with candle-wax and pressed flat from a night under Gran\'s pillow.',
    category: 'key',
  },
  tide_charm: {
    id: 'tide_charm',
    name: 'Tide Charm',
    desc: 'A wave-worn charm lashed to a lamp-frame; the sea trusts it. One throw, and the surest catch in the South.',
    category: 'charge',
    catch_bonus: 2.0,
  },
  // The netmender's thanks for relighting her buoy line ("The Last Buoy Out") —
  // the game's first CONDITIONAL charge: it blazes over open water, and burns
  // plain anywhere else (docs/mechanics/04-capture.md, "Specialty charges").
  drift_charm: {
    id: 'drift_charm',
    name: 'Drift Charm',
    desc: 'A buoy-wick dipped in the going-out song. Over open water its throw burns threefold bright; ashore it is only a lamp.',
    category: 'charge',
    catch_bonus: 3.0,
    condition: { kind: 'terrain', terrain: 'water' },
  },
  // E1 "The Quiet Reeds" — the fen fisher's thanks for tending her lantern-reed
  // line (Saltreach Fen II). A reed-wick charge that blazes in deep growth —
  // reed beds, fringe grass, glowmoss — and burns plain on open ground.
  marsh_lamp: {
    id: 'marsh_lamp',
    name: 'Marsh Lamp',
    desc: 'A reed-wick lamp cell dipped in fen-oil. Thrown in deep growth its light doubles; on open ground it is only a lamp.',
    category: 'charge',
    catch_bonus: 2.0,
    condition: { kind: 'terrain', terrain: 'tall_grass' },
  },
  // E2 "Spores for the Stall" — the Bloom stall-keeper's thanks: a festival
  // salve pressed from glowmoss spores (quest-only, never sold).
  glow_salve: {
    id: 'glow_salve',
    name: 'Glow Salve',
    desc: 'A festival salve pressed from bloom-spores, faintly luminous in the tin. Restores a good deal of health.',
    category: 'medicine',
    heal: 60,
  },
  // The Tended Bed chain (Lowleaf): dry fen-wood for the kiln, and the
  // hearth-spore the kilner fires from it to warm the Elder Bed.
  fen_wood: {
    id: 'fen_wood',
    name: 'Fen-wood',
    desc: 'An armful of dry fen-wood from the forest fringe, light as paper and eager to burn.',
    category: 'key',
  },
  // E2 "Spores for the Stall" — the gatherer's bundles carried home from
  // Glowmoss Deep (three gives of the same key item; the flags track count).
  bloom_spores: {
    id: 'bloom_spores',
    name: 'Spore-bundle',
    desc: 'A gatherer\'s cloth bundle of glowing bloom-spores, bound for the festival stall. It hums very faintly, like a held bee.',
    category: 'key',
  },
  hearth_spore: {
    id: 'hearth_spore',
    name: 'Hearth-spore',
    desc: 'A kiln-fired glowmoss spore, warm as a held coal. The kilner says the old bed will remember what to do with it.',
    category: 'key',
  },
  // S3 "The Cavern Keeps a Light" — the old fisher's thanks once the wreck-lamp
  // burns again (completes post-Glimmerstep; the Tide Charm, re-blessed).
  wrecklight_charm: {
    id: 'wrecklight_charm',
    name: 'Wrecklight Charm',
    desc: 'A Tide Charm re-blessed at the wreck-lamp\'s flame. One throw, steady as a light that would not drown.',
    category: 'charge',
    catch_bonus: 2.5,
  },

  // --- The North (walkthrough/03-north) --------------------------------------
  // The Kite-Rising Winch chain (Galehigh, spine §5 shape #5): the kite-maker's
  // three storm-scattered pieces, found in order across the lower terraces.
  kite_spar: {
    id: 'kite_spar',
    name: 'Kite Spar',
    desc: 'A wind-tempered spar of mountain ash, light as a held breath. The bones of the kite-maker\'s best kite.',
    category: 'key',
  },
  kite_sail: {
    id: 'kite_sail',
    name: 'Kite Sail',
    desc: 'Oiled festival silk, lantern-orange, hemmed against the gusts. It tugs at your hands like something impatient to be sky again.',
    category: 'key',
  },
  kite_tail: {
    id: 'kite_tail',
    name: 'Kite Tail',
    desc: 'A long plaited tail strung with tiny wick-lamps. At the Kite-rising, every tail is lit — so the stars have something to answer.',
    category: 'key',
  },
  // R4 "A Kite for the Waystone Kid" — the Waykeeper's commissioned kite.
  round_kite: {
    id: 'round_kite',
    name: 'Waystone Kite',
    desc: 'A small, sturdy kite in Lanternway colours, commissioned by the Waykeeper for the kid at the Crossroads. Built to survive an owner of eight.',
    category: 'key',
  },
  // N1 "The Crag-tender's Kettle" — the herb and the flask it earns.
  ledge_herb: {
    id: 'ledge_herb',
    name: 'Ledge-herb',
    desc: 'A wind-burnt sprig from Galehigh\'s highest terrace, sharp and warm to the nose. The crag-tender swears by it for her kettle.',
    category: 'key',
  },
  warm_flask: {
    id: 'warm_flask',
    name: 'Warm Flask',
    desc: 'The crag-tender\'s own brew in a felt-wrapped flask, warm through the worst of the chill. Restores a good deal of health.',
    category: 'medicine',
    heal: 80,
  },
  // The Lamp-Line (Pale Vault, spine §5 shape #6): the doused hearth's kindling
  // and the oil the seven brackets burn.
  stormwood: {
    id: 'stormwood',
    name: 'Storm-kindling',
    desc: 'An armful of storm-felled wood off the Windward heights, dry under the snow-crust and eager to catch. A doused hearth\'s best friend.',
    category: 'key',
  },
  aurora_oil: {
    id: 'aurora_oil',
    name: 'Aurora-oil',
    desc: 'A stoppered jar of the tallow-keeper\'s pale rendering. It holds a faint moving light, like the sky above the glacier got in somehow.',
    category: 'key',
  },
  // N3 "Wren's Ribbon" — Mira's quiet errand after the wobble. No reward; the
  // payoff is one extra Wren line at Nightreach (the West writer's beat).
  wren_ribbon: {
    id: 'wren_ribbon',
    name: "Wren's Ribbon",
    desc: 'A kite-ribbon in Wren\'s colours, dropped at the Kite-rising. It still smells faintly of festival smoke.',
    category: 'key',
  },
  // N2 "The Aurora Sketcher" — the painter's thanks: an aurora-dipped charm
  // (a conditional charge, the Drift Charm pattern: blazes toward Frost-lit
  // hearts, burns plain toward everything else).
  aurora_charm: {
    id: 'aurora_charm',
    name: 'Aurora Charm',
    desc: 'A lamp-charm dipped in aurora-oil under a watching sky. Raised toward a Frost-hearted kin its throw burns brilliantly; toward any other it is only a lamp.',
    category: 'charge',
    catch_bonus: 2.5,
    condition: { kind: 'defender_type', types: ['Frost'] },
  },

  // --- The West (walkthrough/04-west) -----------------------------------------
  // X1 "The Caretaker's Lamp" (Hushfrost II): her thanks once the aurora-oil
  // fills her lamp. NOTE: the id is `caretaker_lamp`, never `bright_lamp` —
  // SaveCodec migrates that legacy id to glow_charge (the rename trap).
  caretaker_lamp: {
    id: 'caretaker_lamp',
    name: 'Bright Lamp',
    desc: "The caretaker's own lamp-cell, filled with aurora-oil and given away warm. One throw burns steady and sure — the way a lamp burns when somebody sits with it.",
    category: 'charge',
    catch_bonus: 2.5,
  },
  // The Lit Stage chain (Sunken Solarium, spine §5 shape #7): three phials of
  // stored daylight fetched up out of the flooded halls, one brazier at a time.
  sunmote_phial: {
    id: 'sunmote_phial',
    name: 'Sunmote Phial',
    desc: 'A stoppered phial of stored daylight, fetched up from the drowned halls. It is warm through the glass, like a hand held forty years.',
    category: 'key',
  },
  // X2 "The Troupe's Sun-mask": the gilt mask dived out of the flooded side room.
  sun_mask: {
    id: 'sun_mask',
    name: 'Gilt Sun-mask',
    desc: "The troupe's gilt sun-mask, silt-scoured and smiling. Forty years of 'The Sun Returns' have worn the inside soft.",
    category: 'key',
  },
  // X2's reward — a conditional charge (the Aurora Charm pattern, gold edition):
  // blazes toward Solar-hearted kin, burns plain toward everything else.
  sun_charm: {
    id: 'sun_charm',
    name: 'Sun Charm',
    desc: 'A lamp-charm pressed from the sun-mask\'s gilt. Raised toward a Solar-hearted kin its throw burns like a remembered noon; toward any other it is only a lamp.',
    category: 'charge',
    catch_bonus: 2.5,
    condition: { kind: 'defender_type', types: ['Solar'] },
  },
  // The Vigil of the Seven (Nightreach): the old watcher's striker, lost on the
  // Sunvault road — lamp 1 of the Astral Walk wants it.
  watch_striker: {
    id: 'watch_striker',
    name: "Watcher's Striker",
    desc: 'An old flint striker on a worn cord, lost on the Sunvault road. Seven watch-lamps on the Astral Walk have waited years for its spark.',
    category: 'key',
  },
  // R5 "A Chart for the Waykeeper" — the Round's last leg: the junior watcher's
  // fresh star-chart, carried home to the Waystone.
  round_chart: {
    id: 'round_chart',
    name: 'Fresh Star-chart',
    desc: 'A new-pressed chart of the relit sky, rolled and sealed for the Waykeeper at the Vesper Crossroads. The ink still smells of lamp-smoke.',
    category: 'key',
  },

  // --- The Central endgame (walkthrough/05-central-endgame) -------------------
  // C2 "The Inn's Empty Lamps" — one lamp-token from each quadrant's festival,
  // carried home to the crossroads inn. Key items; the chain is the quest.
  lamp_token_south: {
    id: 'lamp_token_south',
    name: 'Lamp-token (South)',
    desc: "A small wax token stamped at the Tide-blessing: a bell over water. The quay's festival, pressed small enough to carry home.",
    category: 'key',
  },
  lamp_token_east: {
    id: 'lamp_token_east',
    name: 'Lamp-token (East)',
    desc: 'A small wax token stamped at the Lamp-down vigil: a lamp dimmed, then relit. The mountain keeps its dark, and keeps its light.',
    category: 'key',
  },
  lamp_token_north: {
    id: 'lamp_token_north',
    name: 'Lamp-token (North)',
    desc: 'A small wax token stamped at the Aurora-watch: one held flame under a moving sky. Pressed in silence, given warm.',
    category: 'key',
  },
  lamp_token_west: {
    id: 'lamp_token_west',
    name: 'Lamp-token (West)',
    desc: 'A small wax token stamped at the Star-vigil: a watcher\'s lamp, lit the moment its star came home. The last of the four.',
    category: 'key',
  },
  // C2's reward — the best charge in the game short of the Starlamp itself:
  // four festivals' wax, one wick. Quest-only, never sold.
  radiant_lamp: {
    id: 'radiant_lamp',
    name: 'Radiant Lamp',
    desc: 'A charge cell pressed from four festivals\' token-wax around one inn-trimmed wick. One throw burns with a whole year\'s belonging.',
    category: 'charge',
    catch_bonus: 3.5,
  },
  // C3 "The Long Round" — the Waykeeper's keepsake for walking every leg of it.
  way_lamp: {
    id: 'way_lamp',
    name: 'Way-lamp',
    desc: "The Waykeeper's own hand-lamp, retired the year the Round was kept again. A lamp that has walked every road burns a little farther.",
    category: 'key',
  },

  // --- Valuables (found, never bought; exist to be sold for wicks) ----------
  wax_cake: {
    id: 'wax_cake',
    name: 'Wax Cake',
    desc: 'A pressed round of fine lamp-wax, stamped with an old chandler\'s mark. Any keeper will trade well for it.',
    category: 'valuable',
    sell: 250,
  },
  moth_amber: {
    id: 'moth_amber',
    name: 'Moth-amber',
    desc: 'A bead of old resin with a glow-moth caught mid-shimmer. It still holds a little light. Worth a fair purse.',
    category: 'valuable',
    sell: 600,
  },
  starglass_shard: {
    id: 'starglass_shard',
    name: 'Starglass Shard',
    desc: 'A sliver of sky-fallen glass that remembers a constellation. Collectors pay handsomely.',
    category: 'valuable',
    sell: 1500,
  },
  // Coldfog finds — what the drained fen still holds (West outer detour).
  embergloss: {
    id: 'embergloss',
    name: 'Embergloss',
    desc: 'A lacquered knot of old hearth-resin from a snuffed wayshrine, still faintly warm at the heart. Chandlers prize it for the finest wicks.',
    category: 'valuable',
    sell: 600,
  },
  murk_pearl: {
    id: 'murk_pearl',
    name: 'Murk Pearl',
    desc: 'A pearl grown in water that stopped saying anything. Lightless, flawless, and heavier than it should be. Collectors pay dearly — and keep it in a drawer.',
    category: 'valuable',
    sell: 1500,
  },

  // --- Star-charts (taught moves — see docs/mechanics/10-economy.md §6) -----
  // A pressed chart of one small constellation figure; a kin that studies it by
  // lamplight learns to draw that figure in battle. One tracing burns the glow
  // out, so each chart teaches once. Compatibility: the kin shares the move's
  // type, the move is Plain, or the move is already in its learnset.
  chart_cinder_spit: {
    id: 'chart_cinder_spit',
    name: 'Star-chart: Cinder Spit',
    desc: 'A pressed chart of the Ember\'s spark-figure. Teaches a willing kin CINDER SPIT (Ember). One study burns it out.',
    category: 'chart',
    teach_move: 'cinder_spit',
    price: 800,
  },
  chart_mist_spray: {
    id: 'chart_mist_spray',
    name: 'Star-chart: Mist Spray',
    desc: 'A pressed chart of the Tide\'s spray-figure. Teaches a willing kin MIST SPRAY (Tide). One study burns it out.',
    category: 'chart',
    teach_move: 'mist_spray',
    price: 800,
  },
  chart_gust_up: {
    id: 'chart_gust_up',
    name: 'Star-chart: Gust Up',
    desc: 'A plain-figure chart any kin can read. Teaches GUST UP (Plain). One study burns it out.',
    category: 'chart',
    teach_move: 'gust_up',
    price: 900,
  },
  chart_focus_mind: {
    id: 'chart_focus_mind',
    name: 'Star-chart: Focus Mind',
    desc: 'A meditative plain-figure chart any kin can read. Teaches FOCUS MIND (Plain). One study burns it out.',
    category: 'chart',
    teach_move: 'focus_mind',
    price: 1200,
  },
  chart_wave_crash: {
    id: 'chart_wave_crash',
    name: 'Star-chart: Wave Crash',
    desc: 'A pressed chart of the Tide\'s breaker-figure. Teaches a willing kin WAVE CRASH (Tide). One study burns it out.',
    category: 'chart',
    teach_move: 'wave_crash',
    price: 1400,
  },
  chart_hearth_pulse: {
    id: 'chart_hearth_pulse',
    name: 'Star-chart: Hearth Pulse',
    desc: 'A pressed chart of the Ember\'s hearth-figure. Teaches a willing kin HEARTH PULSE (Ember). One study burns it out.',
    category: 'chart',
    teach_move: 'hearth_pulse',
    price: 1400,
  },
  // The Lowleaf provisioner's slate (10-economy.md §5: Spore Puff / Root
  // Strike / Lifedrain — the East's Verdant pair + the drain utility).
  chart_spore_puff: {
    id: 'chart_spore_puff',
    name: 'Star-chart: Spore Puff',
    desc: 'A pressed chart of the Verdant\'s spore-figure. Teaches a willing kin SPORE PUFF (Verdant). One study burns it out.',
    category: 'chart',
    teach_move: 'spore_puff',
    price: 900,
  },
  chart_root_strike: {
    id: 'chart_root_strike',
    name: 'Star-chart: Root Strike',
    desc: 'A pressed chart of the Verdant\'s root-figure. Teaches a willing kin ROOT STRIKE (Verdant). One study burns it out.',
    category: 'chart',
    teach_move: 'root_strike',
    price: 1400,
  },
  chart_lifedrain: {
    id: 'chart_lifedrain',
    name: 'Star-chart: Lifedrain',
    desc: 'A pressed chart of the Verdant\'s drinking-figure. Teaches a willing kin LIFEDRAIN (Verdant). One study burns it out.',
    category: 'chart',
    teach_move: 'lifedrain',
    price: 1200,
  },
  // The Galehigh kite-stall's slate (10-economy.md §5: the Storm pair + the
  // late Heavy + a Plain utility — the North's tier; Pale Vault keeps no
  // counter, so the kite-stall carries the whole cold leg's stock).
  chart_thunder_kick: {
    id: 'chart_thunder_kick',
    name: 'Star-chart: Thunder Kick',
    desc: 'A pressed chart of the Storm\'s striding-figure. Teaches a willing kin THUNDER KICK (Storm). One study burns it out.',
    category: 'chart',
    teach_move: 'thunder_kick',
    price: 1400,
  },
  chart_volt_arc: {
    id: 'chart_volt_arc',
    name: 'Star-chart: Volt Arc',
    desc: 'A pressed chart of the Storm\'s leaping-figure. Teaches a willing kin VOLT ARC (Storm). One study burns it out.',
    category: 'chart',
    teach_move: 'volt_arc',
    price: 1400,
  },
  chart_gale_slam: {
    id: 'chart_gale_slam',
    name: 'Star-chart: Gale Slam',
    desc: 'A pressed chart of the Storm\'s great wheel-figure, heavy with held weather. Teaches a willing kin GALE SLAM (Storm). One study burns it out.',
    category: 'chart',
    teach_move: 'gale_slam',
    price: 2400,
  },
  chart_swift_step: {
    id: 'chart_swift_step',
    name: 'Star-chart: Swift Step',
    desc: 'A plain-figure chart any kin can read, quick as a kite-string paying out. Teaches SWIFT STEP (Plain). One study burns it out.',
    category: 'chart',
    teach_move: 'swift_step',
    price: 1400,
  },
  // Thunderroost's prize — a nuke chart, find-first per 10-economy §6 (the
  // storm-birds' aerie is the only place this figure was ever pressed).
  chart_tempest: {
    id: 'chart_tempest',
    name: 'Star-chart: Tempest',
    desc: 'A chart of the Storm\'s whole turning sky, pressed at the aerie itself. Teaches a willing kin TEMPEST (Storm). One study burns it out.',
    category: 'chart',
    teach_move: 'tempest',
    price: 4000,
  },
  // The Helia Vault's reliquary prize — find-first per 10-economy §6 (the
  // keepers sealed this figure away with the rest of the stored daylight).
  chart_sunburst_nova: {
    id: 'chart_sunburst_nova',
    name: 'Star-chart: Sunburst Nova',
    desc: 'A chart of the sun\'s own remembered blaze, sealed dry in the Helia Vault. Teaches a willing kin SUNBURST NOVA (Solar). One study burns it out.',
    category: 'chart',
    teach_move: 'sunburst_nova',
    price: 4000,
  },
};

export function getItem(id: string): ItemDef | undefined {
  return ITEMS[id];
}
