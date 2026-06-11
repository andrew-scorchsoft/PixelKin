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
};

export function getItem(id: string): ItemDef | undefined {
  return ITEMS[id];
}
