// Full-roster Monte Carlo for PixelKin. Loads the final species set, auto-builds
// movesets (or uses authored ones), and runs tens of thousands of seeded fair
// fights to report per-type win-rates, per-species outliers, the BST/tier
// histogram, speed clustering, and offensive coverage gaps. This is the
// referee for roster balance (docs/mechanics/02 & 09).
//
//   node tools/balance/simulate.mjs [speciesPath] [battles] [seed]
// default speciesPath: src/game/data/species.json

import { readFileSync } from "node:fs";
import { join } from "node:path";
import { ROOT, TYPES, MOVES, TYPE_CHART, battle1v1, rng, pct } from "./lib.mjs";
import { attachMovesets } from "./autobuild.mjs";

const speciesPath = process.argv[2] || "src/game/data/species.json";
const BATTLES = parseInt(process.argv[3] || "80000", 10);
const SEED = parseInt(process.argv[4] || "777", 10);
const LEVEL = 50;

const species = JSON.parse(readFileSync(join(ROOT, speciesPath), "utf8"));
const roster = (Array.isArray(species) ? species : species.species).filter((s) => s.stats);
attachMovesets(roster);

// --- BST / tier histogram -------------------------------------------------
const tierCount = {}, tierBst = {};
for (const s of roster) {
  s.bst = s.bst || Object.values(s.stats).reduce((a, b) => a + b, 0);
  tierCount[s.tier] = (tierCount[s.tier] || 0) + 1;
  (tierBst[s.tier] ||= []).push(s.bst);
}
console.log(`\n=== ROSTER: ${roster.length} species ===`);
console.log("Tier  count  bst(min/avg/max)");
for (const t of "ABCDEF") {
  const arr = (tierBst[t] || []).sort((a, b) => a - b);
  if (!arr.length) continue;
  const avg = Math.round(arr.reduce((a, b) => a + b, 0) / arr.length);
  console.log(`  ${t}  ${String(tierCount[t]).padStart(4)}   ${arr[0]}/${avg}/${arr.at(-1)}`);
}

// --- Primary-type distribution -------------------------------------------
const typeCount = {};
for (const s of roster) typeCount[s.types[0]] = (typeCount[s.types[0]] || 0) + 1;
console.log("\nPrimary type:", TYPES.map((t) => `${t}:${typeCount[t] || 0}`).join("  "));

// --- Offensive coverage check: is every type hit x2 by some STAB attacker? -
const hitSE = new Set();
for (const s of roster) {
  for (const mid of s._moveset) {
    const mv = MOVES[mid];
    if (!mv || mv.power === 0) continue;
    if (!s.types.includes(mv.type)) continue; // STAB only
    const row = TYPE_CHART.chart[mv.type] || {};
    for (const def of TYPES) {
      if (row[def] === 2) hitSE.add(def);
    }
  }
}
const noAnswer = TYPES.filter((t) => !hitSE.has(t));
console.log(`\nCoverage: types with a super-effective STAB answer in the roster: ${hitSE.size}/10`);
if (noAnswer.length) console.log(`  !! NO SE answer for: ${noAnswer.join(", ")}`);

// --- Monte Carlo: fair 1v1 at L50, all base-stat ------------------------
const rand = rng(SEED);
const wins = Object.fromEntries(TYPES.map((t) => [t, 0]));
const games = Object.fromEntries(TYPES.map((t) => [t, 0]));
const winsST = Object.fromEntries(TYPES.map((t) => [t, 0]));   // same-tier only
const gamesST = Object.fromEntries(TYPES.map((t) => [t, 0]));
const spWins = new Map(), spGames = new Map();
for (const s of roster) { spWins.set(s.id, 0); spGames.set(s.id, 0); }
let draws = 0;

for (let i = 0; i < BATTLES; i++) {
  const a = roster[(rand() * roster.length) | 0];
  let b = roster[(rand() * roster.length) | 0];
  while (b === a) b = roster[(rand() * roster.length) | 0];
  const res = battle1v1(a, b, LEVEL, rand);
  games[a.types[0]]++; games[b.types[0]]++;
  spGames.set(a.id, spGames.get(a.id) + 1); spGames.set(b.id, spGames.get(b.id) + 1);
  if (res === 1) { wins[a.types[0]]++; spWins.set(a.id, spWins.get(a.id) + 1); }
  else if (res === -1) { wins[b.types[0]]++; spWins.set(b.id, spWins.get(b.id) + 1); }
  else draws++;
  if (a.tier === b.tier) {                 // same-tier: isolates TYPE from tier composition
    gamesST[a.types[0]]++; gamesST[b.types[0]]++;
    if (res === 1) winsST[a.types[0]]++;
    else if (res === -1) winsST[b.types[0]]++;
  }
}

console.log(`\n=== MONTE CARLO (${BATTLES} fair 1v1, seed ${SEED}, L${LEVEL}, base stats) ===`);
const ranked = TYPES.map((t) => ({ t, wr: wins[t] / Math.max(1, games[t]) })).sort((a, b) => b.wr - a.wr);
let lo = 1, hi = 0;
for (const { t, wr } of ranked) {
  lo = Math.min(lo, wr); hi = Math.max(hi, wr);
  console.log(`${t.padEnd(9)} ${pct(wr).padStart(6)}  ${"#".repeat(Math.round(wr * 50))}`);
}
console.log(`type win-rate spread: ${pct(lo)} .. ${pct(hi)}  (raw, mixes tiers; skew = tier composition + abilities excluded)`);

console.log(`\n=== SAME-TIER type win-rates (isolates TYPE from tier composition) ===`);
const rankedST = TYPES.map((t) => ({ t, wr: winsST[t] / Math.max(1, gamesST[t]) })).sort((a, b) => b.wr - a.wr);
let loST = 1, hiST = 0;
for (const { t, wr } of rankedST) {
  loST = Math.min(loST, wr); hiST = Math.max(hiST, wr);
  console.log(`${t.padEnd(9)} ${pct(wr).padStart(6)}  ${"#".repeat(Math.round(wr * 50))}`);
}
console.log(`same-tier spread: ${pct(loST)} .. ${pct(hiST)}  (this is the true type-balance signal; abilities/status still excluded)`);

// --- Per-species outliers (note: cross-tier, so big tiers naturally skew) -
const spStats = roster.map((s) => ({
  id: s.id, name: s.name, tier: s.tier, type: s.types.join("/"),
  wr: spWins.get(s.id) / Math.max(1, spGames.get(s.id)), n: spGames.get(s.id),
})).filter((x) => x.n >= 30);
spStats.sort((a, b) => b.wr - a.wr);
console.log(`\nTop 8 (overall, all tiers — apex/legendary expected on top):`);
for (const x of spStats.slice(0, 8)) console.log(`  ${x.name.padEnd(14)} ${x.tier} ${x.type.padEnd(14)} ${pct(x.wr)}`);
console.log(`Bottom 8:`);
for (const x of spStats.slice(-8)) console.log(`  ${x.name.padEnd(14)} ${x.tier} ${x.type.padEnd(14)} ${pct(x.wr)}`);

// Within-tier outliers: a species winning very differently from its tier peers
const byTier = {};
for (const x of spStats) (byTier[x.tier] ||= []).push(x);
console.log(`\nWithin-tier outliers (>18pp from tier mean):`);
let flagged = 0;
for (const t of "ABCDEF") {
  const arr = byTier[t] || [];
  if (arr.length < 3) continue;
  const mean = arr.reduce((a, b) => a + b.wr, 0) / arr.length;
  for (const x of arr) {
    if (Math.abs(x.wr - mean) > 0.18) {
      console.log(`  [${t}] ${x.name.padEnd(14)} ${x.type.padEnd(14)} ${pct(x.wr)} (tier mean ${pct(mean)})`);
      flagged++;
    }
  }
}
if (!flagged) console.log("  none — every species within 18pp of its tier mean.");

// --- Speed clustering -----------------------------------------------------
const spes = roster.map((s) => s.stats.spe).sort((a, b) => a - b);
const q = (p) => spes[Math.floor(p * (spes.length - 1))];
console.log(`\nBase Speed spread: min ${spes[0]} | p25 ${q(0.25)} | median ${q(0.5)} | p75 ${q(0.75)} | max ${spes.at(-1)}`);

console.log(`\ndraws: ${draws} (${pct(draws / BATTLES)})`);
