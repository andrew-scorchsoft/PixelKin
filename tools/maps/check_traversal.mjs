#!/usr/bin/env node
/**
 * check_traversal — the traversal kit's PARITY gate (CI).
 *
 * The engine walks maps with src/game/systems/world/Traversal.ts; every map audit
 * walks them with tools/maps/worldmodel.py. If the two ever disagree, the audits
 * are proving a different world from the one players walk. This gate bundles the
 * engine's Traversal.ts, re-walks every kit map (plus a synthetic fixture that
 * exercises every feature) over the SAME base grid the Python model uses — with
 * the engine's real state (the heading glare ice keeps) — and FAILs on any tile
 * one side reaches and the other doesn't.
 *
 *   node tools/maps/check_traversal.mjs
 */
import { execFileSync } from 'node:child_process';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const repo = resolve(here, '../..');
const require = createRequire(join(repo, 'package.json'));
const esbuild = require('esbuild');

// A fixture that exercises every rule: a chute with steering, glare ice with a
// stopper, a rail pair switched by a lever flag, a bridge with an underpass over
// a solid trench, a ladder up a cliff and a ramp over a gap. '#' solid, '.' open.
const FIX_ROWS = [
  '##############',
  '#....#.......#',
  '#....#.......#',
  '#..........#.#',
  '#....###.....#',
  '#............#',
  '#.##########.#',
  '#............#',
  '#..##.....##.#',
  '#............#',
  '##############',
];
function fixture() {
  const H = FIX_ROWS.length;
  const W = FIX_ROWS[0].length;
  // Raw ground as a plain grid; the Python side reads it via a synthetic tileset-free map.
  return {
    id: '__fixture__',
    width: W,
    height: H,
    tile_width: 16,
    tile_height: 16,
    kind: 'route',
    tilesets: [],
    layers: [],
    objects: FIX_ROWS.flatMap((row, y) =>
      [...row].flatMap((c, x) => (c === '#' ? [{ id: `w${x}_${y}`, sprite: 'x', at: { tx: x, ty: y }, w: 1, h: 1 }] : [])),
    ),
    warps: [],
    triggers: [],
    encounters: [],
    npcs: [],
    gates: [],
    _starts: [[1, 1]],
    ride: true,
    flows: [
      { id: 'chute', kind: 'slope', dir: 'down', rect: { tx: 1, ty: 2, w: 3, h: 3 } },
      { id: 'ice', kind: 'ice', rect: { tx: 6, ty: 1, w: 6, h: 2 } },
      { id: 'rail_a', kind: 'rail', dir: 'right', rect: { tx: 2, ty: 5, w: 4, h: 1 } },
      { id: 'rail_b', kind: 'rail', dir: 'down', rect: { tx: 6, ty: 5, w: 1, h: 1 }, requires_flag: 'flag:lever' },
    ],
    spans: [
      { id: 'trestle', kind: 'bridge', axis: 'h', under: true, rect: { tx: 5, ty: 8, w: 5, h: 1 } },
      { id: 'ladder', kind: 'ladder', axis: 'v', rect: { tx: 12, ty: 6, w: 1, h: 1 } },
      { id: 'cliff_ladder', kind: 'ladder', axis: 'v', rect: { tx: 2, ty: 6, w: 1, h: 1 } },
    ],
    jumps: [{ id: 'ramp', at: { tx: 9, ty: 9 }, dir: 'left', length: 3 }],
  };
}

const KEY = (x, y) => `${x},${y}`;
const DIRS = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] };

async function loadTraversal() {
  const out = join(mkdtempSync(join(tmpdir(), 'pk-trav-')), 'traversal.mjs');
  await esbuild.build({
    entryPoints: [join(repo, 'src/game/systems/world/Traversal.ts')],
    bundle: true,
    format: 'esm',
    platform: 'node',
    outfile: out,
    logLevel: 'silent',
    alias: { '@game': join(repo, 'src/game') },
  });
  return import(pathToFileURL(out).href);
}

/** The engine's reach: BFS over (tile, heading) with Traversal's plan/forced, under
 *  EVERY combination of the map's lever flags (a yard with several levers — the Old
 *  Seams — can set each independently; the model's per-move union of switch states
 *  reaches exactly the union over combinations). */
function engineReach(T, d) {
  const npcs = new Set(d.npcs.map(([x, y]) => KEY(x, y)));
  const inb = (x, y) => x >= 0 && y >= 0 && x < d.w && y < d.h;
  const ground = (x, y) => inb(x, y) && d.ground[y][x];
  const reached = new Set();
  const levers = [...new Set(d.flows.flatMap((f) => [f.requires_flag, f.hidden_when_flag].filter(Boolean)))];
  if (levers.length > 8) throw new Error(`${d.id}: ${levers.length} lever flags — too many combinations to walk`);
  const combos = [];
  for (let bits = 0; bits < 1 << levers.length; bits++) {
    combos.push(new Set(levers.filter((_, i) => bits & (1 << i))));
  }
  for (const held of combos) {
    const def = { flows: d.flows, spans: d.spans, jumps: d.jumps };
    const rules = new T.Traversal(def, (flag) => held.has(flag));
    const ctx = {
      canEnter: (x, y) => ground(x, y) && !npcs.has(KEY(x, y)),
      occupied: (x, y) => npcs.has(KEY(x, y)),
      groundOpen: (x, y) => ground(x, y) && !npcs.has(KEY(x, y)),
      riding: d.ride,
    };
    // Ledges aren't in the fixture/grid here (the Python side folds them in its
    // base grid as blocked), so plan()'s blocked == blocked.
    const seen = new Set();
    const q = [];
    for (const [x, y] of d.starts) {
      for (const h of Object.keys(DIRS)) {
        const k = `${x},${y},${h}`;
        if (!seen.has(k)) {
          seen.add(k);
          q.push([x, y, h]);
        }
      }
    }
    while (q.length) {
      const [x, y, last] = q.shift();
      const from = { tx: x, ty: y };
      // A tile you only slide THROUGH on glare ice isn't one you can stop on
      // (the model treats a slide as one macro move to its stop).
      const onIce = rules.flowAt(x, y)?.kind === 'ice';
      const iceCarries = onIce && rules.plan(from, last, ctx).kind !== 'blocked';
      if (!iceCarries) reached.add(KEY(x, y));
      const push = (p, dir) => {
        if (p.kind === 'blocked') return false;
        const to = p.kind === 'pass' ? p.tiles[p.tiles.length - 1] : p.to;
        const k = `${to.tx},${to.ty},${dir}`;
        if (!seen.has(k)) {
          seen.add(k);
          q.push([to.tx, to.ty, dir]);
        }
        return true;
      };
      const carry = rules.forced(from, last);
      if (carry) {
        const moved = push(rules.plan(from, carry.dir, ctx), carry.dir);
        if (moved) {
          if (carry.steer) {
            for (const s of Object.keys(DIRS)) {
              if (s !== carry.dir && s !== T.OPPOSITE[carry.dir]) push(rules.plan(from, s, ctx), s);
            }
          }
          continue;
        }
      }
      for (const dir of Object.keys(DIRS)) push(rules.plan(from, dir, ctx), dir);
    }
  }
  return reached;
}

async function main() {
  const T = await loadTraversal();
  const fx = fixture();
  const raw = execFileSync('python3', [join(here, 'traversal_reach.py')], {
    input: JSON.stringify([fx]),
    maxBuffer: 1 << 28,
  }).toString();
  const maps = JSON.parse(raw);
  let fails = 0;
  for (const d of maps) {
    const eng = engineReach(T, d);
    const py = new Set(d.reach.map(([x, y]) => KEY(x, y)));
    const onlyEng = [...eng].filter((k) => !py.has(k));
    const onlyPy = [...py].filter((k) => !eng.has(k));
    if (onlyEng.length || onlyPy.length) {
      fails++;
      console.log(`  [FAIL] ${d.id}: engine-only ${onlyEng.slice(0, 8).join(' ')} | model-only ${onlyPy.slice(0, 8).join(' ')}`);
    } else {
      console.log(`  [ok]   ${d.id}: ${eng.size} tiles reached by both`);
    }
  }
  // The fixture must actually exercise the rules (a regression that stops the
  // chute or the underpass would otherwise pass trivially on both sides).
  const fxd = maps.find((m) => m.id === '__fixture__');
  const r = new Set(fxd.reach.map(([x, y]) => KEY(x, y)));
  const must = [
    ['the underpass lands south of the trestle', '7,9'],
    ['the ramp clears the gap', '6,9'],
    ['the lever-switched rail drops south', '6,7'],
  ];
  for (const [why, k] of must) {
    if (!r.has(k)) {
      fails++;
      console.log(`  [FAIL] fixture: ${why} (${k} unreached)`);
    }
  }
  console.log(fails ? `FAIL — ${fails} traversal parity problem(s)` : `PASS — engine and audit model agree on ${maps.length} map(s)`);
  process.exit(fails ? 1 : 0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
