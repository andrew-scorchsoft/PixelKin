// Validate the final species set against docs/mechanics/08-data-schema.md and the
// power-budget rules in 02. Hard failures exit non-zero; soft concerns warn.
//
//   node tools/balance/validate.mjs [speciesPath]   (default src/game/data/species.json)

import { readFileSync } from "node:fs";
import { join } from "node:path";
import { ROOT, TYPES, MOVES, ABILITIES } from "./lib.mjs";

const speciesPath = process.argv[2] || "src/game/data/species.json";
const raw = JSON.parse(readFileSync(join(ROOT, speciesPath), "utf8"));
const roster = Array.isArray(raw) ? raw : raw.species;

const TYPESET = new Set(TYPES);
const BST_BAND = { A: [280, 340], B: [320, 375], C: [390, 445], D: [470, 525], E: [535, 580], F: [590, 680] };
const CATCH_BAND = { A: [190, 235], B: [150, 200], C: [90, 150], D: [45, 90], E: [20, 45], F: [3, 10] };
const TYPE_SCORE = { Ember: 5, Tide: 5, Verdant: -5, Stone: 15, Storm: 5, Frost: 5, Solar: 25, Lunar: 10, Light: -10, Dark: 10 };

const errors = [], warns = [];
const byId = new Map(roster.map((s) => [s.id, s]));

function eps(s) {
  const ts = s.types.map((t) => TYPE_SCORE[t] ?? 0);
  const typing = ts.reduce((a, b) => a + b, 0) / ts.length + (s.types.length === 2 ? 5 : 0);
  const ab = ABILITIES[s.ability]?.eps ?? 0;
  let movepool = 0;
  for (const e of s.learnset?.levelup || []) if (MOVES[e.move]?.signature) movepool += 15;
  return Math.round(s.bst + typing + ab - 0);
}

for (const s of roster) {
  const tag = `#${s.id} ${s.name}`;
  // types
  if (!s.types?.length || s.types.some((t) => !TYPESET.has(t))) errors.push(`${tag}: bad types ${JSON.stringify(s.types)}`);
  if (s.types?.length > 2) errors.push(`${tag}: >2 types`);
  // stats / bst
  const sum = ["hp", "atk", "def", "spa", "spd", "spe"].reduce((a, k) => a + (s.stats?.[k] || 0), 0);
  if (s.bst !== sum) errors.push(`${tag}: bst ${s.bst} != sum(stats) ${sum}`);
  const band = BST_BAND[s.tier];
  if (!band) errors.push(`${tag}: bad tier ${s.tier}`);
  else if (sum < band[0] - 5 || sum > band[1] + 5) errors.push(`${tag}: bst ${sum} outside tier ${s.tier} band ${band}`);
  // catch rate
  const cb = CATCH_BAND[s.tier];
  if (cb && (s.catchRate < cb[0] - 5 || s.catchRate > cb[1] + 5)) warns.push(`${tag}: catchRate ${s.catchRate} outside tier ${s.tier} band ${cb}`);
  // ability
  if (s.ability && !ABILITIES[s.ability]) errors.push(`${tag}: unknown ability '${s.ability}'`);
  if (s.hidden_ability && !ABILITIES[s.hidden_ability]) errors.push(`${tag}: unknown hidden_ability '${s.hidden_ability}'`);
  // learnset moves
  for (const e of s.learnset?.levelup || []) if (!MOVES[e.move]) errors.push(`${tag}: unknown move '${e.move}'`);
  // kindling integrity
  if (s.kindling) {
    const into = s.kindling.into;
    if (!byId.has(into)) errors.push(`${tag}: kindling.into ${into} missing`);
    else {
      const nxt = byId.get(into);
      if (nxt.from !== s.id) warns.push(`${tag}: ${nxt.name} #${into} .from=${nxt.from} != ${s.id}`);
      if (nxt.bst <= s.bst) errors.push(`${tag}: kindled form ${nxt.name} bst ${nxt.bst} <= ${s.bst}`);
    }
  }
  if (s.from != null && !byId.has(s.from)) errors.push(`${tag}: from ${s.from} missing`);
  // dex fields
  if (!s.dex?.size_cm || !s.dex?.weight_kg) warns.push(`${tag}: missing size/weight`);
}

// whole-line check: no orphan mid-stage (stage>1 must have a valid .from)
for (const s of roster) {
  if ((s.stage || 1) > 1 && (s.from == null || !byId.has(s.from))) errors.push(`#${s.id} ${s.name}: stage ${s.stage} but no valid 'from'`);
}

// EPS within-tier spread
const byTier = {};
for (const s of roster) (byTier[s.tier] ||= []).push({ name: s.name, eps: eps(s) });
console.log("=== EPS within-tier spread (target <= ~50pt total) ===");
for (const t of "ABCDEF") {
  const arr = byTier[t] || [];
  if (!arr.length) continue;
  const vals = arr.map((a) => a.eps);
  const lo = Math.min(...vals), hi = Math.max(...vals);
  const flag = hi - lo > 60 ? "  <-- wide" : "";
  console.log(`  ${t}: ${arr.length} kin, eps ${lo}..${hi} (spread ${hi - lo})${flag}`);
}

console.log(`\n=== VALIDATION: ${roster.length} species ===`);
console.log(`Errors: ${errors.length}`);
for (const e of errors.slice(0, 80)) console.log("  ERR ", e);
if (errors.length > 80) console.log(`  ... +${errors.length - 80} more`);
console.log(`Warnings: ${warns.length}`);
for (const w of warns.slice(0, 40)) console.log("  warn", w);
if (warns.length > 40) console.log(`  ... +${warns.length - 40} more`);

process.exit(errors.length ? 1 : 0);
