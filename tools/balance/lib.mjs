// Shared balance-engine library for PixelKin.
// Pure ESM, zero dependencies. Loads the canonical JSON data and implements the
// damage/stat/battle rules from docs/mechanics/02 & 03. Used by simulate.mjs,
// validate.mjs and select.mjs.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
export const ROOT = join(__dirname, "..", "..");

export function loadJSON(rel) {
  return JSON.parse(readFileSync(join(ROOT, rel), "utf8"));
}

export const TYPE_CHART = loadJSON("src/game/data/type-chart.json");
export const MOVES_DATA = loadJSON("src/game/data/moves.json");
export const TYPES = TYPE_CHART.types;
export const MOVES = Object.fromEntries(MOVES_DATA.moves.map((m) => [m.id, m]));
export const ABILITIES = Object.fromEntries(MOVES_DATA.abilities.map((a) => [a.id, a]));

// --- Seeded RNG (mulberry32) so runs are reproducible ---------------------
export function rng(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// --- Type effectiveness ---------------------------------------------------
export function typeMult(attackType, defenderTypes) {
  if (attackType === "Plain") return 1;
  const row = TYPE_CHART.chart[attackType] || {};
  let m = 1;
  for (const dt of defenderTypes) {
    m *= row[dt] === undefined ? 1 : row[dt];
  }
  return m;
}

// --- Stat at level (IV/EV-free baseline; docs/mechanics/02) ---------------
export function statAtLevel(base, level, isHP) {
  const core = Math.floor((2 * base * level) / 100);
  return isHP ? core + level + 10 : core + 5;
}

export function liveStats(species, level) {
  const s = species.stats;
  return {
    hp: statAtLevel(s.hp, level, true),
    atk: statAtLevel(s.atk, level, false),
    def: statAtLevel(s.def, level, false),
    spa: statAtLevel(s.spa, level, false),
    spd: statAtLevel(s.spd, level, false),
    spe: statAtLevel(s.spe, level, false),
  };
}

// --- Damage (docs/mechanics/02) -------------------------------------------
export function damage(attacker, defender, move, level, rand) {
  if (move.category === "status" || move.power === 0) return 0;
  const aStats = attacker._live, dStats = defender._live;
  const A = move.category === "physical" ? aStats.atk : aStats.spa;
  const D = move.category === "physical" ? dStats.def : dStats.spd;
  const base = Math.floor((Math.floor((2 * level) / 5 + 2) * move.power * A) / D / 50) + 2;
  const stab = attacker.types.includes(move.type) ? 1.5 : 1.0;
  const eff = typeMult(move.type, defender.types);
  if (eff === 0) return 0;
  const roll = 0.85 + rand() * 0.15;
  return Math.max(0, Math.floor(base * stab * eff * roll));
}

// Expected (no-roll) damage, used by the AI to choose a move.
export function expectedDamage(attacker, defender, move, level) {
  if (move.category === "status" || move.power === 0) return 0;
  const aStats = attacker._live, dStats = defender._live;
  const A = move.category === "physical" ? aStats.atk : aStats.spa;
  const D = move.category === "physical" ? dStats.def : dStats.spd;
  const base = Math.floor((Math.floor((2 * level) / 5 + 2) * move.power * A) / D / 50) + 2;
  const stab = attacker.types.includes(move.type) ? 1.5 : 1.0;
  const eff = typeMult(move.type, defender.types);
  const acc = (move.accuracy === 0 ? 100 : move.accuracy) / 100;
  return base * stab * eff * 0.925 * acc;
}

// --- A combatant wraps a species + its chosen moveset at a level ----------
export function makeCombatant(species, level) {
  return {
    species,
    name: species.name,
    types: species.types,
    moves: (species._moveset || []).map((id) => MOVES[id]).filter(Boolean),
    level,
    _live: liveStats(species, level),
    hp: liveStats(species, level).hp,
    maxhp: liveStats(species, level).hp,
  };
}

// --- A single 1v1 battle. Returns +1 if A wins, -1 if B wins, 0 if draw ---
// Deliberately compact: damage moves only, smart-ish AI (best expected
// damage), accuracy, the [0.85,1] roll, and a turn cap. Status/abilities are
// intentionally excluded here so the TYPE CHART + STATS are tested in
// isolation; the full roster sim can layer them in later.
export function battle1v1(a, b, level, rand, turnCap = 200) {
  const A = makeCombatant(a, level);
  const B = makeCombatant(b, level);

  const bestMove = (att, def) => {
    let best = null, bestDmg = -1;
    for (const mv of att.moves) {
      if (mv.category === "status") continue;
      const d = expectedDamage(att, def, mv, level);
      if (d > bestDmg) { bestDmg = d; best = mv; }
    }
    return best || att.moves[0];
  };

  const act = (att, def) => {
    const mv = bestMove(att, def);
    if (!mv) return;
    const acc = (mv.accuracy === 0 ? 100 : mv.accuracy) / 100;
    if (rand() > acc) return; // miss
    def.hp -= damage(att, def, mv, level, rand);
  };

  for (let t = 0; t < turnCap; t++) {
    const aFirst = A._live.spe === B._live.spe ? rand() < 0.5 : A._live.spe > B._live.spe;
    const [first, second] = aFirst ? [A, B] : [B, A];
    act(first, second);
    if (second.hp <= 0) return first === A ? 1 : -1;
    act(second, first);
    if (first.hp <= 0) return second === A ? 1 : -1;
  }
  return A.hp === B.hp ? 0 : A.hp > B.hp ? 1 : -1; // timeout: more HP% wins
}

export function pct(x) { return (100 * x).toFixed(1) + "%"; }
