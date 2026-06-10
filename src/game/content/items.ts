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
  vesperlamp: {
    id: 'vesperlamp',
    name: 'Vesperlamp',
    desc: 'Your lamp-tender\'s lantern. Coaxes a wild kin to walk with you.',
    category: 'lamp',
    catch_bonus: 1.0,
    price: 200,
  },
  bright_lamp: {
    id: 'bright_lamp',
    name: 'Bright Lamp',
    desc: 'A keener flame. Better odds of befriending a wild kin.',
    category: 'lamp',
    catch_bonus: 1.5,
    price: 600,
  },
  radiant_lamp: {
    id: 'radiant_lamp',
    name: 'Radiant Lamp',
    desc: 'A chandler\'s masterwork, near daylight in the hand. The surest catch wicks can buy.',
    category: 'lamp',
    catch_bonus: 2.0,
    price: 1500,
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
  tide_charm: {
    id: 'tide_charm',
    name: 'Tide Charm',
    desc: 'A wave-worn charm lashed to a lamp-frame; the sea trusts it. The surest catch in the South.',
    category: 'lamp',
    catch_bonus: 2.0,
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
};

export function getItem(id: string): ItemDef | undefined {
  return ITEMS[id];
}
