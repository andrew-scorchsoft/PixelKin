#!/usr/bin/env node
/**
 * progression.mjs — the journey-long XP + wick-economy model.
 *
 * Walks the canonical journey (docs/world/walkthrough/ §4 level curve) leg by
 * leg with the engine's real formulas (exp = L³; yield = bst·level/20 to the
 * active battler, ×1.5 in trainer battles, catches pay like knock-outs;
 * payouts/prices from docs/mechanics/10-economy.md) and reports,
 * for three player profiles, the lead's level and the wallet at every
 * checkpoint against the spine's recommended level.
 *
 *   node tools/balance/progression.mjs           # report + checks
 *   node tools/balance/progression.mjs --verbose # per-leg ledger
 *
 * The JOURNEY table below is the binding battle & earnings budget per region:
 * built South legs mirror src/game/content/trainers.ts exactly (a drift check
 * recomputes their payouts); unbuilt legs are the DESIGN budget that region
 * authors must ship (trainer counts/levels, quest wicks, cache valuables).
 * Change a price, payout, band, or trainer roster → re-run this; the checks
 * fail loudly when the curve or the wallet breaks. Tuning rules live in
 * docs/mechanics/10-economy.md §8.
 *
 * Profiles:
 *   rusher   — fights only what the lanes force (mandatory crossings + trainers)
 *   mainline — fights what it meets, does the earned loops (the target player)
 *   explorer — optional grass, all named quests, sells every valuable
 */
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const SPECIES = JSON.parse(readFileSync(join(ROOT, 'src/game/data/species.json'), 'utf8')).species;
const MOVES = JSON.parse(readFileSync(join(ROOT, 'src/game/data/moves.json'), 'utf8'));
const VERBOSE = process.argv.includes('--verbose');

// ---------------------------------------------------------------------------
// Engine formulas (mirror KinInstance.ts / BattleScene.ts — keep in sync)
// ---------------------------------------------------------------------------
const expForLevel = (l) => l * l * l;
const levelForExp = (e) => Math.min(100, Math.floor(Math.cbrt(Math.max(1, e))));
/** Tuned by this model (2026-06): /60 left the curve unreachable (-18 by the
 *  climax); /20 with the trainer bonus + catch XP lands every checkpoint. */
const YIELD_DIVISOR = 20;
const TRAINER_XP_MULT = 1.5; // the genre's trainer-battle bonus
const expYield = (bst, level) => Math.max(1, Math.floor((bst * level) / YIELD_DIVISOR));

// ---------------------------------------------------------------------------
// Economy constants (mirror src/game/content/economy.ts + items.ts)
// ---------------------------------------------------------------------------
const STARTING_WICKS = 250;
/** payout-per-ace-level by trainer class (10-economy.md §4). */
const PAYOUT_RATE = { route: 16, keeper: 20, rival: 24, warden: 60, cor: 120 };
const PRICES = {
  tallow_balm: 120, warm_balm: 500, bright_balm: 1200,
  glow_charge: 200, beacon_charge: 600,
  chart_early: 800, chart_mid: 1400, chart_late: 2400, chart_end: 4000,
};

// ---------------------------------------------------------------------------
// Wild BST per area, from the dex's own encounter data (rarity-weighted),
// with a level-trend fallback for areas the dex hasn't placed kin in yet.
// ---------------------------------------------------------------------------
const RARITY_W = { common: 55, uncommon: 30, rare: 12, very_rare: 3, 'very rare': 3 };
const areaBst = new Map(); // area -> { bstSum, wSum }
const trend = []; // [midLevel, bst, weight]
for (const s of SPECIES) {
  for (const e of s.encounters ?? []) {
    const w = RARITY_W[e.rarity] ?? 10;
    const cur = areaBst.get(e.area) ?? { bstSum: 0, wSum: 0 };
    cur.bstSum += s.bst * w;
    cur.wSum += w;
    areaBst.set(e.area, cur);
    trend.push([(e.min + e.max) / 2, s.bst, w]);
  }
}
// Weighted linear fit bst ≈ a + b·level over every dex encounter record.
const fit = (() => {
  let sw = 0, sx = 0, sy = 0, sxx = 0, sxy = 0;
  for (const [x, y, w] of trend) { sw += w; sx += w * x; sy += w * y; sxx += w * x * x; sxy += w * x * y; }
  const b = (sw * sxy - sx * sy) / (sw * sxx - sx * sx);
  const a = (sy - b * sx) / sw;
  return (level) => a + b * level;
})();
/** Avg wild BST for a leg: dex data for its areas if placed, else the trend. */
function wildBst(areas, band) {
  let bstSum = 0, wSum = 0;
  for (const area of areas ?? []) {
    const cur = areaBst.get(area);
    if (cur) { bstSum += cur.bstSum; wSum += cur.wSum; }
  }
  if (wSum > 0) return bstSum / wSum;
  return fit((band[0] + band[1]) / 2);
}
/** Trainer kin run a notch above the local wild average (raised, kindled). */
const trainerBst = (level, klass) => fit(level) * (klass === 'warden' || klass === 'cor' ? 1.22 : 1.12);
const speciesBst = (id) => SPECIES.find((s) => s.id === id)?.bst ?? fit(20);

// ---------------------------------------------------------------------------
// THE JOURNEY — the binding battle & earnings budget (see file header).
// Each leg: wild {areas?, band, fights per profile}, trainers, income, spend.
//   trainer: { name, class, kin: [{level, species?}] }  (species = built roster)
//   income:  { quests, valuables, finds }  — wicks from named quests, sellable
//            valuables found, and loose giveMoney finds, per profile reach
//   spend:   the planned core kit purchases at this stop (mainline; rusher
//            buys half the balms and no charts; explorer buys all + a spare)
// checkpoint: { name, rec, ace } — the spine §4 row this leg ends on.
// ---------------------------------------------------------------------------
const T = (name, klass, kin) => ({ name, class: klass, kin });
const K = (level, species) => ({ level, species });

/**
 * leadShare — what fraction of a leg's XP lands on the player's strongest kin
 * (the one the spine's "recommended party" tracks). Engine XP goes to the
 * active battler only, so this models *who the player sends out*: in the South
 * and East the team is still being built (fresh catches eat most XP); from the
 * North the core is set and the ace absorbs it. Rusher solo-aces (+0.2);
 * explorer spreads the love (−0.05). These are design assumptions — tune here,
 * never per-profile fudge factors elsewhere.
 */
const shareFor = (leg, profile) => {
  const base = leg.leadShare;
  if (profile === 'rusher') return Math.min(1, base + 0.2);
  if (profile === 'explorer') return Math.max(0.3, base - 0.05);
  return base;
};

const JOURNEY = [
  // ---- SOUTH (built through Pearlmoor; breakwater loop is planned data) ----
  {
    name: 'Tinderwick & the verge',
    leadShare: 0.70,
    wild: { areas: ['dimglass_coast'], band: [2, 4], fights: { rusher: 3, mainline: 6, explorer: 10 } },
    trainers: [],
    income: { quests: 0, valuables: 0, finds: 0 },
    spend: { tallow_balm: 2 },
  },
  {
    name: 'Dimglass Coast I + Beacon ascent',
    leadShare: 0.55,
    wild: { areas: ['dimglass_coast'], band: [3, 6], fights: { rusher: 4, mainline: 9, explorer: 14 } },
    trainers: [
      T('Wren (A2)', 'rival', [K(5, 8), K(6, 26)]),
      T('Tansy', 'keeper', [K(7, 16)]),
      T('Cole', 'keeper', [K(7, 10), K(8, 16)]),
      T('Brisa Tallow', 'warden', [K(7, 10), K(10, 18)]),
    ],
    income: { quests: 150, valuables: 250, finds: 0 }, // beacon errand thanks + a wax cake cache
    spend: { tallow_balm: 2, glow_charge: 2 },
    checkpoint: { name: 'Ember Gleam (Brisa)', rec: 10, ace: 10 },
  },
  {
    name: 'Dimglass Coast II (the flats)',
    leadShare: 0.45,
    wild: { areas: ['dimglass_coast'], band: [8, 10], fights: { rusher: 4, mainline: 8, explorer: 13 } },
    trainers: [
      T('Morrow', 'route', [K(9, 26), K(9, 31)]),
      T('Elspeth', 'route', [K(10, 27), K(11, 31)]),
    ],
    income: { quests: 200, valuables: 0, finds: 100 },
    spend: { tallow_balm: 2 },
    checkpoint: { name: 'Pearlmoor arrival', rec: 12 },
  },
  {
    name: 'Pearlmoor Quay + breakwater loop',
    leadShare: 0.42,
    wild: { areas: ['pearlmoor_quay'], band: [8, 11], fights: { rusher: 2, mainline: 6, explorer: 10 } },
    trainers: [
      // BUILT (the Causeway Bell loop): the breakwater's two net-hand sight
      // trainers — mirror src/game/content/trainers.ts exactly.
      T('Maren (net-hand)', 'route', [K(12, 26), K(12, 31)]),
      T('Cob (net-hand)', 'route', [K(13, 31), K(14, 27)]),
      T('Reyl Wash', 'warden', [K(12, 26), K(13, 31), K(14, 27), K(16, 24)]),
    ],
    income: { quests: 400, valuables: 250, finds: 0 }, // bell-rope quest + Round leg
    spend: { warm_balm: 1, beacon_charge: 2, chart_mid: 1 },
    checkpoint: { name: 'Tide Gleam (Reyl)', rec: 12, ace: 16 },
  },

  // ---- EAST ----------------------------------------------------------------
  {
    name: 'Saltreach Fen I→II',
    leadShare: 0.42,
    // BUILT (fen I + II + Sunkbell): trainers mirror src/game/content/trainers.ts;
    // quests = E1 "The Quiet Reeds" wick thanks (200); finds = the two fen
    // wicks tins (150 + 150); valuables = the tide-walk Moth-amber (600).
    wild: { areas: ['saltreach_fen_i', 'saltreach_fen_ii', 'sunkbell_shallows'], band: [16, 19], fights: { rusher: 5, mainline: 10, explorer: 16 } },
    trainers: [
      T('Marigold (fen-wader)', 'route', [K(16, 59), K(17, 27)]),
      T('Osprey (plank-courier)', 'route', [K(17, 31), K(18, 60)]),
      T('Tarn (reed-lamplighter)', 'route', [K(17, 31), K(18, 59)]),
    ],
    income: { quests: 200, valuables: 600, finds: 300 },
    spend: { tallow_balm: 3 },
    checkpoint: { name: 'Lowleaf arrival', rec: 18 },
  },
  {
    name: 'Lowleaf Hollow (tending loop)',
    leadShare: 0.45,
    // BUILT (the Tended Bed): trainers mirror trainers.ts; quests = the
    // kiln-fee (150) + E2 stall takings (300); finds = the town's wicks tin
    // (120); valuables = Glowmoss Deep's Moth-amber (600, found this leg).
    wild: { areas: ['lowleaf_hollow'], band: [17, 20], fights: { rusher: 3, mainline: 7, explorer: 12 } },
    trainers: [
      T('Ivy (bloom-warden)', 'keeper', [K(19, 56), K(20, 65)]),
      T('Fern (bloom-warden)', 'keeper', [K(20, 38), K(21, 67)]),
      T('Sable Quill', 'warden', [K(18, 56), K(19, 59), K(20, 65), K(22, 66)]),
    ],
    income: { quests: 450, valuables: 600, finds: 120 },
    spend: { warm_balm: 2, beacon_charge: 1, chart_mid: 1 },
    checkpoint: { name: 'Verdant Gleam (Sable)', rec: 18, ace: 22 },
  },
  {
    name: 'Glowmoss Deep → Cinderhead galleries',
    leadShare: 0.50,
    wild: { band: [22, 27], fights: { rusher: 6, mainline: 12, explorer: 18 } },
    trainers: [
      T('Deep prospector', 'keeper', [K(23), K(23)]),
      T('Cartlamp hauler', 'keeper', [K(24), K(24)]),
      T('Gallery surveyor', 'keeper', [K(25), K(25)]),
      T('Vigil miner A', 'keeper', [K(26), K(26)]),
      T('Vigil miner B', 'keeper', [K(26), K(27)]),
    ],
    income: { quests: 600, valuables: 600, finds: 200 }, // vigil-lamp errand pays
    spend: { warm_balm: 2, tallow_balm: 2 },
    checkpoint: { name: 'Cinderhead arrival', rec: 22 },
  },
  {
    name: 'Otho Grist (the wall)',
    leadShare: 0.55,
    wild: { band: [24, 27], fights: { rusher: 3, mainline: 7, explorer: 11 } },
    trainers: [T('Otho Grist', 'warden', [K(24), K(25), K(26), K(28)])],
    income: { quests: 300, valuables: 0, finds: 0 },
    spend: { chart_mid: 1 },
    // rec 26, not the §4 entry-level 22: the wall design sends the player
    // through the 24–27 deep galleries (the Descent Vigil) before the test.
    checkpoint: { name: 'Stone Gleam (Otho)', rec: 26, ace: 28 },
  },

  // ---- NORTH (BUILT — N4 wiring 2026-06; trainers mirror trainers.ts) -------
  {
    name: 'Galehigh Terraces + skyloft',
    // North onward the core team is set (see shareFor's design note) — the
    // built roster's species-true XP runs leaner than the old placeholder
    // budget, and the lead's share carries the difference.
    leadShare: 0.70,
    // BUILT (the Kite-Rising Winch loop): two terrace route trainers, the two
    // skyloft wind-wards, Mira. quests = the R4 Round-leg carriage fee (300);
    // finds = the festival takings-tin (200); valuables = the terrace
    // Moth-amber (600).
    wild: { areas: ['galehigh_terraces'], band: [27, 31], fights: { rusher: 5, mainline: 10, explorer: 16 } },
    trainers: [
      T('Perrin (kite-hand)', 'route', [K(28, 88), K(29, 97)]),
      T('Sorrel (terrace-farmer)', 'route', [K(29, 91), K(30, 45)]),
      T('Tamsin (wind-ward)', 'keeper', [K(29, 97), K(30, 98)]),
      T('Bran (wind-ward)', 'keeper', [K(30, 91), K(31, 89)]),
      T('Mira Vael', 'warden', [K(30, 98), K(31, 95), K(32, 89), K(34, 90)]),
    ],
    income: { quests: 300, valuables: 600, finds: 200 },
    spend: { warm_balm: 3, beacon_charge: 2, chart_late: 1 },
    checkpoint: { name: 'Storm Gleam (Mira)', rec: 28, ace: 34 },
  },
  {
    name: 'Windward II → Pale Vault (+ Wren A4)',
    leadShare: 0.70,
    // BUILT (the Stair + the Lamp-Line + A4): three stair route trainers,
    // Wren at the undercroft door (at/above the player — by design), the two
    // frost-wards, Ysolde. quests = the rendering-fee (200) + the sketcher's
    // colour-fund (400); finds = the two wicks caches (250 + 300); valuables =
    // the stair/wind-eye/glacier Starglass Shards (3 × 1,500) + the crag and
    // undercroft Moth-ambers (2 × 600) — the cold leg pays its explorers.
    // (Stair I's 3-tile SE foot verge rolls 32-34 — N6 MIN-3 border softener;
    // an optional entry pocket, too small to move the leg's grind band.)
    wild: { band: [34, 38], fights: { rusher: 6, mainline: 11, explorer: 17 } },
    trainers: [
      T('Edda (crag-hand)', 'route', [K(34, 45), K(35, 89)]),
      T('Rowan (gale-watch)', 'route', [K(34, 98), K(35, 95)]),
      T('Merle (crag-watch)', 'route', [K(35, 89), K(36, 94)]),
      T('Wren (A4 — the wobble)', 'rival', [K(39, 9), K(39, 95), K(41, 28)]),
      T('Sela (frost-ward)', 'keeper', [K(37, 72), K(38, 84)]),
      T('Orrin (frost-ward)', 'keeper', [K(38, 81), K(39, 84)]),
      T('Ysolde Frost', 'warden', [K(36, 72), K(37, 81), K(38, 84), K(38, 95), K(40, 87)]),
    ],
    income: { quests: 600, valuables: 5700, finds: 550 },
    spend: { warm_balm: 2, bright_balm: 1, chart_late: 1 },
    checkpoint: { name: 'Frost Gleam (Ysolde)', rec: 36, ace: 40 },
  },

  // ---- WEST (BUILT — W5 wiring 2026-06; trainers mirror trainers.ts) --------
  {
    name: 'Hushfrost Pass I→II → Solarium',
    leadShare: 0.80,
    // BUILT (X1 caretaker + the Lit Stage): three Hushfrost route trainers,
    // the two troupe-player sight trainers on the flooded lanes, Lucan.
    // quests = X2's troupe takings (300); finds = the Hushfrost + Solarium
    // wicks caches (300 + 250); valuables = 3 Starglass Shards (Hushfrost
    // wall-hollow, Aurora Hollow, the flooded halls) + 2 Moth-ambers.
    wild: { areas: ['sunken_solarium'], band: [40, 44], fights: { rusher: 5, mainline: 10, explorer: 15 } },
    trainers: [
      T('Dunstan (coldfog lampman)', 'route', [K(41, 84), K(41, 78)]),
      T('Hesper (pass survivor)', 'route', [K(42, 82)]),
      T('Tilda (thaw-tender)', 'route', [K(42, 75), K(42, 87)]),
      T('Calla (troupe player)', 'route', [K(43, 114), K(44, 117)]),
      T('Orsino (troupe player)', 'route', [K(44, 115), K(45, 120)]),
      T('Lucan Pyre', 'warden', [K(42, 117), K(43, 115), K(44, 104), K(44, 121), K(46, 123)]),
    ],
    income: { quests: 300, valuables: 5700, finds: 550 },
    spend: { bright_balm: 2, beacon_charge: 2, chart_late: 1 },
    checkpoint: { name: 'Solar Gleam (Lucan)', rec: 42, ace: 46 },
  },
  {
    name: 'Sunvault Climb → Nightreach',
    leadShare: 0.90,
    // BUILT (the Vigil of the Seven + X3 + R5): two Sunvault route trainers,
    // the two junior-watcher keepers on the Astral Walk, Wren's A5 friendly
    // (in the lamp-6 scene — everyone fights it), Nessa. quests = X3's
    // chart-fund (400) + R5's Round rates (400); finds = the Sunvault +
    // Nightreach wicks caches (250 + 300); valuables = the Sunvault
    // Moth-amber + the roof-terrace Starglass Shard.
    wild: { band: [45, 50], fights: { rusher: 6, mainline: 11, explorer: 16 } },
    trainers: [
      T('Bel (terrace-tender)', 'route', [K(46, 115), K(47, 121)]),
      T('Tam (sky-watcher)', 'route', [K(47, 126), K(48, 118)]),
      T('Lira (junior watcher)', 'keeper', [K(49, 106), K(50, 127)]),
      T('Os (junior watcher)', 'keeper', [K(50, 112), K(51, 125)]),
      T('Wren (A5 — resolved)', 'rival', [K(49, 9), K(49, 96), K(50, 28)]),
      T('Nessa Cole', 'warden', [K(48, 106), K(49, 112), K(50, 125), K(50, 127), K(52, 107)]),
    ],
    income: { quests: 800, valuables: 2100, finds: 550 },
    spend: { bright_balm: 2, chart_end: 1 },
    checkpoint: { name: 'Lunar Gleam (Nessa)', rec: 48, ace: 52 },
  },

  // ---- CENTRAL / ENDGAME (BUILT — C3 wiring 2026-06; trainers mirror
  // trainers.ts exactly). No wild zones live past the hub (the Ring and Spire
  // are scripted-only), so the wild band models the set-piece catches +
  // retries (Lampling/Lunaveil/Keylumen) and pre-climb spoke top-ups.
  // Income is item-shaped by design (Radiant Lamp, Way-lamp, the Lampling) —
  // quests pay 0 wicks; finds = the Penumbra satchel (600) + the gallery
  // toll-box (800); valuables = the Penumbra islet Starglass (1,500) + the
  // [MISSABLE] spire-landing Starglass (1,500) + the Starwell Moth-amber (600).
  {
    name: 'Penumbra Ring → Umbral Spire',
    leadShare: 1.00,
    wild: { areas: ['umbral_spire', 'coldfog_marches'], band: [52, 56], fights: { rusher: 6, mainline: 10, explorer: 14 } },
    trainers: [
      T('Merrin (Hollowing acolyte A)', 'keeper', [K(52, 136), K(53, 137)]),
      T('Tace (Hollowing acolyte B)', 'keeper', [K(52, 134), K(52, 133), K(53, 137)]),
      T('Ivorwen (Hollowing acolyte C)', 'keeper', [K(53, 141), K(54, 142)]),
      T('Harl (Hollowing acolyte D)', 'keeper', [K(54, 143), K(55, 138)]),
      T('Sefa (Hollowing acolyte E)', 'keeper', [K(54, 135), K(55, 139)]),
      T('Warden Còr', 'cor', [K(53, 113), K(54, 85), K(54, 135), K(55, 138), K(55, 142), K(56, 150)]),
    ],
    income: { quests: 0, valuables: 3600, finds: 1400 },
    spend: { bright_balm: 3, chart_end: 1 },
    checkpoint: { name: 'Warden Còr (climax)', rec: 54, ace: 56 },
  },
];

// ---------------------------------------------------------------------------
// Drift check: built trainers' authored payouts must match class rate × ace.
// (Mirrors src/game/content/trainers.ts — update BOTH when a roster changes.)
// ---------------------------------------------------------------------------
const BUILT_PAYOUTS = {
  lampwarden_tinderwick: ['warden', 10, 600],
  beacon_keeper_a: ['keeper', 7, 140],
  beacon_keeper_b: ['keeper', 8, 160],
  wren_dimglass: ['rival', 6, 144],
  flats_wayfarer_a: ['route', 9, 144],
  fen_wader_a: ['route', 17, 272],
  fen_courier_b: ['route', 18, 288],
  reed_lamplighter: ['route', 18, 288],
  bloom_warden_a: ['keeper', 20, 400],
  bloom_warden_b: ['keeper', 21, 420],
  lampwarden_lowleaf: ['warden', 22, 1320],
  flats_wayfarer_b: ['route', 11, 176],
  net_hand_a: ['route', 12, 192],
  net_hand_b: ['route', 14, 224],
  lampwarden_pearlmoor: ['warden', 16, 960],
  glowmoss_keeper_a: ['keeper', 20, 400],
  glowmoss_keeper_b: ['keeper', 21, 420],
  gallery_miner_a: ['keeper', 25, 500],
  gallery_miner_b: ['keeper', 26, 520],
  lampwarden_cinderhead: ['warden', 28, 1680],
  galehigh_kitehand: ['route', 29, 464],
  galehigh_terracer: ['route', 30, 480],
  skyloft_ward_a: ['keeper', 30, 600],
  skyloft_ward_b: ['keeper', 31, 620],
  mira_vael: ['warden', 34, 2040],
  windward_craghand: ['route', 35, 560],
  windward_galewatch: ['route', 35, 560],
  windward_cragwatch: ['route', 36, 576],
  wren_pale_vault: ['rival', 41, 984],
  undercroft_ward_a: ['keeper', 38, 760],
  undercroft_ward_b: ['keeper', 39, 780],
  ysolde_frost: ['warden', 40, 2400],
  hushfrost_lampman: ['route', 41, 656],
  hushfrost_survivor: ['route', 42, 672],
  hushfrost_thawtender: ['route', 42, 672],
  troupe_player_a: ['route', 44, 704],
  troupe_player_b: ['route', 45, 720],
  lucan_pyre: ['warden', 46, 2760],
  sunvault_terracer: ['route', 47, 752],
  sunvault_skywatcher: ['route', 48, 768],
  junior_watcher_a: ['keeper', 50, 1000],
  junior_watcher_b: ['keeper', 51, 1020],
  wren_nightreach: ['rival', 50, 1200],
  nessa_cole: ['warden', 52, 3120],
  hollowing_acolyte_a: ['keeper', 53, 1060],
  hollowing_acolyte_b: ['keeper', 53, 1060],
  hollowing_acolyte_c: ['keeper', 54, 1080],
  hollowing_acolyte_d: ['keeper', 55, 1100],
  hollowing_acolyte_e: ['keeper', 55, 1100],
  warden_cor: ['cor', 56, 6720],
};
const failures = [];
for (const [id, [klass, ace, authored]] of Object.entries(BUILT_PAYOUTS)) {
  const expect = PAYOUT_RATE[klass] * ace;
  if (expect !== authored) failures.push(`payout drift: ${id} authored ${authored}, formula says ${expect}`);
}
// Chart price sanity: the in-game chart items must use these tier prices.
// (Tier mapping lives in 10-economy.md §6; this guards the tiers themselves.)
if (!(PRICES.chart_early < PRICES.chart_mid && PRICES.chart_mid < PRICES.chart_late && PRICES.chart_late < PRICES.chart_end)) {
  failures.push('chart price tiers must ascend');
}
// Move-id sanity for the shipped charts (mirror items.ts teach_move values).
for (const id of ['cinder_spit', 'mist_spray', 'gust_up', 'focus_mind', 'wave_crash', 'hearth_pulse',
  'spore_puff', 'root_strike', 'lifedrain', 'thunder_kick', 'volt_arc', 'gale_slam', 'swift_step', 'tempest',
  'sunburst_nova']) {
  if (!MOVES.moves.some((m) => m.id === id)) failures.push(`chart teaches unknown move '${id}'`);
}

// ---------------------------------------------------------------------------
// The walk
// ---------------------------------------------------------------------------
const PROFILES = {
  rusher: { questShare: 0.34, spendBalms: 0.5, spendCharts: 0, catchesPerLeg: 0.2 },
  mainline: { questShare: 1.0, spendBalms: 1.0, spendCharts: 1, catchesPerLeg: 1 },
  explorer: { questShare: 1.0, spendBalms: 1.0, spendCharts: 1, extraWilds: 0.5, catchesPerLeg: 2 },
};

function priceOf(key) {
  if (key in PRICES) return PRICES[key];
  throw new Error(`unknown spend key ${key}`);
}

function simulate(profileName) {
  const p = PROFILES[profileName];
  let exp = expForLevel(5); // the starter, level 5
  let wicks = STARTING_WICKS;
  let minWicks = wicks;
  const rows = [];
  const ledger = [];

  for (const leg of JOURNEY) {
    let earned = 0, spent = 0, gained = 0;

    // Wild battles fought on this leg.
    let fights = leg.wild.fights[profileName] ?? leg.wild.fights.mainline;
    if (p.extraWilds) fights = Math.round(fights * (1 + p.extraWilds));
    const bst = wildBst(leg.wild.areas, leg.wild.band);
    const avgLevel = (leg.wild.band[0] + leg.wild.band[1]) / 2;
    gained += fights * expYield(bst, avgLevel);
    // Catches pay the same XP as a knock-out (the collecting pillar stays on-curve).
    gained += Math.round(p.catchesPerLeg) * expYield(bst, avgLevel);

    // Trainer battles (everyone fights them — they're posted on the lanes).
    for (const t of leg.trainers) {
      const ace = Math.max(...t.kin.map((k) => k.level));
      earned += PAYOUT_RATE[t.class] * ace;
      for (const k of t.kin) {
        const kinBst = k.species ? speciesBst(k.species) : trainerBst(k.level, t.class);
        gained += Math.floor(expYield(kinBst, k.level) * TRAINER_XP_MULT);
      }
    }

    // Quest / cache / valuable income, by how much optional content the profile does.
    earned += Math.round((leg.income.quests + leg.income.finds) * p.questShare);
    earned += profileName === 'rusher' ? 0 : leg.income.valuables; // valuables exist to be sold

    // The planned kit purchases at this stop.
    for (const [key, qty] of Object.entries(leg.spend ?? {})) {
      const isChart = key.startsWith('chart');
      const isBalm = key.includes('balm');
      let n = qty;
      if (isChart) n = Math.round(qty * p.spendCharts);
      else if (isBalm) n = Math.round(qty * p.spendBalms);
      spent += n * priceOf(key);
    }

    exp += Math.round(gained * shareFor(leg, profileName));
    wicks += earned - spent;
    minWicks = Math.min(minWicks, wicks);
    ledger.push({ leg: leg.name, gained, earned, spent, wicks, level: levelForExp(exp) });

    if (leg.checkpoint) {
      rows.push({
        checkpoint: leg.checkpoint.name,
        rec: leg.checkpoint.rec,
        ace: leg.checkpoint.ace,
        level: levelForExp(exp),
        wicks,
      });
    }
  }
  return { rows, ledger, minWicks };
}

// ---------------------------------------------------------------------------
// Report
// ---------------------------------------------------------------------------
const pad = (s, n) => String(s).padEnd(n);
const num = (s, n) => String(s).padStart(n);

console.log('PixelKin progression & economy model');
console.log(`(exp = L^3; yield = bst*level/20, trainer x1.5, catch XP on; wild BST from the dex where placed)`);

const results = {};
for (const name of Object.keys(PROFILES)) results[name] = simulate(name);

console.log(`\n${pad('CHECKPOINT', 28)}${num('rec', 5)}${num('ace', 5)}` +
  Object.keys(PROFILES).map((n) => num(n, 10) + num('wicks', 8)).join(''));
results.mainline.rows.forEach((_, i) => {
  const row = results.mainline.rows[i];
  let line = `${pad(row.checkpoint, 28)}${num(row.rec ?? '—', 5)}${num(row.ace ?? '—', 5)}`;
  for (const n of Object.keys(PROFILES)) {
    const r = results[n].rows[i];
    line += num(`L${r.level}`, 10) + num(r.wicks, 8);
  }
  console.log(line);
});

if (VERBOSE) {
  for (const n of Object.keys(PROFILES)) {
    console.log(`\n--- ${n} ledger ---`);
    for (const l of results[n].ledger) {
      console.log(`${pad(l.leg, 38)} +${num(l.gained, 6)}xp  +${num(l.earned, 5)}w  -${num(l.spent, 5)}w  = ${num(l.wicks, 6)}w  L${l.level}`);
    }
  }
}

// ---------------------------------------------------------------------------
// Checks (the acceptance bar — see 10-economy.md §8)
// ---------------------------------------------------------------------------
for (const [i, row] of results.mainline.rows.entries()) {
  if (row.rec === undefined) continue;
  const d = row.level - row.rec;
  if (d < -1) failures.push(`mainline UNDER curve at "${row.checkpoint}": L${row.level} vs rec ${row.rec}`);
  if (d > 4) failures.push(`mainline OVER curve at "${row.checkpoint}": L${row.level} vs rec ${row.rec} (too easy)`);
  const rush = results.rusher.rows[i];
  if (rush.level - row.rec < -3) failures.push(`rusher too far under at "${row.checkpoint}": L${rush.level} vs rec ${row.rec}`);
  const exp = results.explorer.rows[i];
  if (row.ace !== undefined && exp.level - row.ace > 4) {
    failures.push(`explorer trivialises "${row.checkpoint}": L${exp.level} vs ace ${row.ace}`);
  }
}
for (const n of Object.keys(PROFILES)) {
  if (results[n].minWicks < 0) failures.push(`${n} wallet goes NEGATIVE (min ${results[n].minWicks}w) — cut prices or raise payouts`);
}
// The mainline player should be able to afford each region's chart purchase as
// planned (already enforced by the non-negative wallet since spends are applied).

console.log('');
if (failures.length > 0) {
  console.log(`FAIL — ${failures.length} issue(s):`);
  for (const f of failures) console.log(`  ✗ ${f}`);
  process.exit(1);
}
console.log('PASS — curve continuous, wallet solvent, payouts on formula.');
