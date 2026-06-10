// Validate the TYPE CHART + damage formulas in isolation, before any real
// creatures exist. Builds a synthetic, perfectly-fair roster (every type gets
// the same three role spreads at the same BST/level) so any win-rate skew is
// attributable to the type chart alone, then Monte-Carlo's tens of thousands of
// fair fights. Also prints static offensive/defensive reach per type.
//
//   node tools/balance/chart_check.mjs [battles] [seed]

import { TYPES, MOVES_DATA, TYPE_CHART, battle1v1, rng, pct } from "./lib.mjs";

const BATTLES = parseInt(process.argv[2] || "60000", 10);
const SEED = parseInt(process.argv[3] || "12345", 10);
const LEVEL = 50;

// --- group damaging moves by type ----------------------------------------
const byType = {};
for (const t of TYPES) byType[t] = { phys: [], spec: [] };
const plain = { phys: [], spec: [] };
for (const m of MOVES_DATA.moves) {
  if (m.category === "status" || m.power === 0) continue;
  if (m.signature) continue; // one-line moves would make the fair roster unfair
  const bucket = m.type === "Plain" ? plain : byType[m.type];
  if (!bucket) continue;
  bucket[m.category === "physical" ? "phys" : "spec"].push(m);
}
for (const t of TYPES) {
  byType[t].phys.sort((a, b) => a.power - b.power);
  byType[t].spec.sort((a, b) => a.power - b.power);
}
plain.phys.sort((a, b) => a.power - b.power);
plain.spec.sort((a, b) => a.power - b.power);

// --- three fair role spreads, all BST 480 --------------------------------
const SPREADS = {
  physSweeper: { hp: 67, atk: 110, def: 62, spa: 48, spd: 62, spe: 131 },
  specSweeper: { hp: 67, atk: 48, def: 58, spa: 120, spd: 67, spe: 120 },
  bulky:       { hp: 100, atk: 75, def: 90, spa: 75, spd: 90, spe: 50 },
};

// build the synthetic roster: each type x each spread
const roster = [];
for (const t of TYPES) {
  const physIds = byType[t].phys.map((m) => m.id);
  const specIds = byType[t].spec.map((m) => m.id);
  roster.push({
    name: `${t}-PhysSweeper`, types: [t], stats: SPREADS.physSweeper,
    _moveset: [...physIds, plain.phys.at(-1).id],
  });
  roster.push({
    name: `${t}-SpecSweeper`, types: [t], stats: SPREADS.specSweeper,
    _moveset: [...specIds, plain.spec.at(-1).id],
  });
  roster.push({
    name: `${t}-Bulky`, types: [t], stats: SPREADS.bulky,
    _moveset: [byType[t].phys[1].id, byType[t].spec[1].id, plain.phys.at(-1).id, byType[t].phys[0].id],
  });
}

// --- static reach (no battles): how many x2 / x0.5 / x0 each type deals & takes
function staticReach() {
  const rows = [];
  for (const atk of TYPES) {
    const row = TYPE_CHART.chart[atk] || {};
    let se = 0, nve = 0, imm = 0, off = 1;
    for (const def of TYPES) {
      const v = row[def] === undefined ? 1 : row[def];
      if (v === 2) se++; else if (v === 0.5) nve++; else if (v === 0) imm++;
      off += v - 1;
    }
    // defensive: how others hit this type
    let weak = 0, res = 0, immIn = 0, dfn = 0;
    for (const other of TYPES) {
      const r = TYPE_CHART.chart[other] || {};
      const v = r[atk] === undefined ? 1 : r[atk];
      if (v === 2) weak++; else if (v === 0.5) res++; else if (v === 0) immIn++;
      dfn += v - 1;
    }
    rows.push({ type: atk, se, nve, imm, offIdx: off.toFixed(1), weak, res, immIn, defIdx: dfn.toFixed(1) });
  }
  return rows;
}

console.log(`\n=== STATIC TYPE REACH ===`);
console.log("type      SEout NVEout IMMout  offIdx | WEAKin RESin IMMin  defIdx");
for (const r of staticReach()) {
  console.log(
    `${r.type.padEnd(9)} ${String(r.se).padStart(4)} ${String(r.nve).padStart(6)} ${String(r.imm).padStart(6)} ${String(r.offIdx).padStart(7)} |` +
    ` ${String(r.weak).padStart(5)} ${String(r.res).padStart(5)} ${String(r.immIn).padStart(5)} ${String(r.defIdx).padStart(7)}`
  );
}

// --- Monte Carlo: random fair fights, tally per-type win rate -------------
const rand = rng(SEED);
const wins = Object.fromEntries(TYPES.map((t) => [t, 0]));
const games = Object.fromEntries(TYPES.map((t) => [t, 0]));
let draws = 0;

for (let i = 0; i < BATTLES; i++) {
  const a = roster[(rand() * roster.length) | 0];
  let b = roster[(rand() * roster.length) | 0];
  while (b === a) b = roster[(rand() * roster.length) | 0];
  const res = battle1v1(a, b, LEVEL, rand);
  games[a.types[0]]++; games[b.types[0]]++;
  if (res === 1) wins[a.types[0]]++;
  else if (res === -1) wins[b.types[0]]++;
  else draws++;
}

console.log(`\n=== MONTE CARLO (${BATTLES} fair fights, seed ${SEED}, L${LEVEL}) ===`);
const ranked = TYPES.map((t) => ({ t, wr: wins[t] / games[t] })).sort((a, b) => b.wr - a.wr);
let spreadMin = 1, spreadMax = 0;
for (const { t, wr } of ranked) {
  spreadMin = Math.min(spreadMin, wr); spreadMax = Math.max(spreadMax, wr);
  const bar = "#".repeat(Math.round(wr * 50));
  console.log(`${t.padEnd(9)} ${pct(wr).padStart(6)}  ${bar}`);
}
console.log(`draws: ${draws} (${pct(draws / BATTLES)})`);
console.log(`win-rate spread: ${pct(spreadMin)} .. ${pct(spreadMax)}  (target: ~45-55%)`);

const outliers = ranked.filter((r) => r.wr < 0.45 || r.wr > 0.55);
if (outliers.length) {
  console.log(`\nOUTLIERS (outside 45-55%): ${outliers.map((o) => `${o.t} ${pct(o.wr)}`).join(", ")}`);
} else {
  console.log(`\nAll types within the 45-55% guardrail. Chart is balanced for fair fights.`);
}
