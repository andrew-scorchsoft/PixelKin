// Auto-assign a sensible 4-move set + sample level to a species, used by the
// simulator so the roster can be balance-tested before (or alongside)
// hand-authored learnsets. If a species already has `_moveset`, it's respected.

import { MOVES_DATA, MOVES, TYPES } from "./lib.mjs";

// index damaging moves by type+category, sorted by power
const dmgByType = {};
for (const t of [...TYPES, "Plain"]) dmgByType[t] = { physical: [], special: [] };
for (const m of MOVES_DATA.moves) {
  if (m.category === "status" || m.power === 0) continue;
  (dmgByType[m.type] ||= { physical: [], special: [] })[m.category].push(m);
}
for (const t of Object.keys(dmgByType)) {
  dmgByType[t].physical.sort((a, b) => b.power - a.power);
  dmgByType[t].special.sort((a, b) => b.power - a.power);
}

const PHYS_ROLES = new Set(["Physical Sweeper", "Glass Cannon", "Physical Wall", "Physical Bruiser"]);

// Decide whether a species prefers physical or special based on role + stats.
function prefersPhysical(sp) {
  if (PHYS_ROLES.has(sp.role)) return true;
  if (sp.role && sp.role.startsWith("Special")) return false;
  return (sp.stats.atk || 0) >= (sp.stats.spa || 0);
}

// Build up to 4 moves: 2 STAB (heavy + standard) in the preferred channel, a
// coverage move of the secondary type or strongest off-type, and a Plain/quick.
export function autoMoveset(sp) {
  if (sp._moveset && sp._moveset.length) return sp._moveset;
  const phys = prefersPhysical(sp);
  const chan = phys ? "physical" : "special";
  const picks = [];
  const seen = new Set();
  const push = (m) => { if (m && !seen.has(m.id)) { seen.add(m.id); picks.push(m.id); } };

  // primary STAB: top two damaging moves of primary type in preferred channel
  const t0 = sp.types[0];
  const prim = dmgByType[t0]?.[chan] || [];
  push(prim[0]);
  push(prim[1]);
  // coverage: secondary type (if dual) or best off-type vs common defensive types
  const t1 = sp.types[1];
  if (t1) {
    const sec = dmgByType[t1]?.[chan] || [];
    push(sec[0]);
  }
  // fill with the other-channel STAB or Plain heavy so it's never empty
  if (picks.length < 4) {
    const alt = dmgByType[t0]?.[phys ? "special" : "physical"] || [];
    push(alt[0]);
  }
  if (picks.length < 4) {
    const plain = dmgByType["Plain"]?.[chan] || dmgByType["Plain"].physical;
    push(plain[0]);
  }
  // ensure at least one move
  if (picks.length === 0) push(dmgByType["Plain"].physical[0]);
  return picks.slice(0, 4);
}

export function attachMovesets(species) {
  for (const sp of species) sp._moveset = autoMoveset(sp);
  return species;
}
