/**
 * Blob autotile classifier — the deterministic "which tile goes here" rule.
 *
 * Given, for one terrain cell, which of its 8 neighbours are the SAME terrain,
 * return the role of the tile to place. This is the clever tile-set design from
 * the cartridge era (docs/art-style.md §11): a terrain region gets clean borders
 * automatically — straight edges, rounded outer corners, and concave inner
 * corners — from a compact "blob13" set:
 *
 *   fill                                  interior
 *   edge_n  edge_e  edge_s  edge_w        straight sides
 *   corner_nw corner_ne corner_se corner_sw   outer (convex) corners
 *   inner_nw  inner_ne  inner_se  inner_sw    inner (concave) corners
 *
 * This is a 13-tile approximation of the full 47-blob: it covers every situation
 * that occurs in normal map shapes while needing only 13 painted tiles. The
 * expand tool degrades gracefully when a set has fewer (e.g. a 9-slice with no
 * inner corners falls back to fill).
 *
 * Convention: a role names the side(s) of the region that are OPEN (not the same
 * terrain). edge_n = the north side is open (this is the top row of the region).
 * corner_nw = north AND west are open (top-left outer corner). inner_nw = north
 * and west are filled but the NW diagonal is open (a concave notch).
 */

/** Neighbour booleans (true = same terrain). d* are diagonals. */
export function classify({ n, e, s, w, ne, se, sw, nw }) {
  const orth = (n ? 1 : 0) + (e ? 1 : 0) + (s ? 1 : 0) + (w ? 1 : 0);

  // All four sides filled: interior — but a missing diagonal is a concave notch.
  if (orth === 4) {
    if (!nw) return 'inner_nw';
    if (!ne) return 'inner_ne';
    if (!se) return 'inner_se';
    if (!sw) return 'inner_sw';
    return 'fill';
  }

  // Three sides filled: a straight edge facing the one open side.
  if (orth === 3) {
    if (!n) return 'edge_n';
    if (!e) return 'edge_e';
    if (!s) return 'edge_s';
    if (!w) return 'edge_w';
  }

  // Two sides filled.
  if (orth === 2) {
    // Adjacent pair open -> outer corner at the meeting of the two open sides.
    if (!n && !w) return 'corner_nw';
    if (!n && !e) return 'corner_ne';
    if (!s && !e) return 'corner_se';
    if (!s && !w) return 'corner_sw';
    // Opposite pair open (a 1-wide strip): approximate with the matching edge.
    if (!n && !s) return e && w ? 'fill' : 'edge_n';
    if (!e && !w) return n && s ? 'fill' : 'edge_w';
  }

  // One side filled: a peninsula tip — approximate with the corner on its open side.
  if (orth === 1) {
    if (s) return 'corner_nw'; // only south filled -> top is open all around
    if (n) return 'corner_sw';
    if (e) return 'corner_nw';
    if (w) return 'corner_ne';
  }

  // Isolated cell (no same-terrain neighbour): a lone dot — use fill.
  return 'fill';
}

/** Read an 8-neighbour window out of a presence grid (1 = terrain present). */
export function neighbours(grid, width, height, x, y) {
  const at = (xx, yy) =>
    xx >= 0 && yy >= 0 && xx < width && yy < height ? grid[yy * width + xx] === 1 : false;
  return {
    n: at(x, y - 1), e: at(x + 1, y), s: at(x, y + 1), w: at(x - 1, y),
    ne: at(x + 1, y - 1), se: at(x + 1, y + 1), sw: at(x - 1, y + 1), nw: at(x - 1, y - 1),
  };
}

/** Fallback chain: if a set lacks `role`, try simpler roles down to fill. */
export function roleFallbacks(role) {
  if (role.startsWith('inner_')) return [role, 'fill'];
  if (role.startsWith('corner_')) {
    const [, dir] = role.split('_'); // nw/ne/se/sw
    const a = `edge_${dir[0]}`; // edge_n / edge_s
    const b = `edge_${dir[1]}`; // edge_w / edge_e
    return [role, a, b, 'fill'];
  }
  if (role.startsWith('edge_')) return [role, 'fill'];
  return [role];
}

// --- tiny self-test: `node tools/autotile/blob.mjs --test` --------------------
if (process.argv[1] && process.argv[1].endsWith('blob.mjs') && process.argv.includes('--test')) {
  // A 4x4 solid block of terrain (1) surrounded by empty (0).
  const W = 6, H = 6;
  const g = new Array(W * H).fill(0);
  for (let y = 1; y <= 4; y++) for (let x = 1; x <= 4; x++) g[y * W + x] = 1;
  const sym = { fill: '.', edge_n: '^', edge_s: 'v', edge_w: '<', edge_e: '>',
    corner_nw: 'F', corner_ne: '7', corner_se: 'J', corner_sw: 'L',
    inner_nw: 'a', inner_ne: 'b', inner_se: 'c', inner_sw: 'd' };
  let out = '';
  let ok = true;
  const expectCorners = [];
  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      if (g[y * W + x] !== 1) { out += ' '; continue; }
      const role = classify(neighbours(g, W, H, x, y));
      out += sym[role] ?? '?';
    }
    out += '\n';
  }
  // The 4 corners of the block must be the 4 outer corners.
  const corner = (x, y) => classify(neighbours(g, W, H, x, y));
  expectCorners.push(corner(1, 1) === 'corner_nw', corner(4, 1) === 'corner_ne',
    corner(1, 4) === 'corner_sw', corner(4, 4) === 'corner_se');
  ok = expectCorners.every(Boolean) && corner(2, 2) === 'fill' && corner(2, 1) === 'edge_n';
  process.stdout.write(out);
  console.log(ok ? 'blob self-test: PASS' : 'blob self-test: FAIL');
  process.exit(ok ? 0 : 1);
}
