/**
 * Expand a map's `terrain` layers into a plain gid `base` layer.
 *
 * Authoring side of blob autotiling (docs/art-style.md §11). Instead of
 * hand-placing 13 different corner/edge gids, you paint a `terrain` layer — a
 * presence grid (1 = this terrain here, 0 = not) tagged with which terrain group
 * and which packed tileset it uses. This tool reads those layers, classifies
 * every cell with the blob rule (blob.mjs), looks up the matching tile in the
 * set's sidecar by (terrain, autotile-role), and stamps the right gid into the
 * base layer. Later terrain layers paint over earlier ones.
 *
 * Runtime stays plain gids — the cleverness is offline, like tools/balance.
 *
 * Usage:
 *   node tools/autotile/expand.mjs public/assets/maps/foo.json            # writes foo.json (base layer)
 *   node tools/autotile/expand.mjs foo --output /tmp/foo.expanded.json    # bare id; don't overwrite
 *   node tools/autotile/expand.mjs foo --dry-run                          # report only
 *
 * A `terrain` layer looks like:
 *   { "name": "ground", "role": "terrain", "terrain": "grass",
 *     "set": "tinderwick_set", "into": "base", "data": [0,1,1,...] }
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';
import { classify, neighbours, roleFallbacks } from './blob.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..', '..');

function resolveMap(arg) {
  if (existsSync(arg)) return arg;
  const cand = join(REPO, 'public', 'assets', 'maps', `${arg}.json`);
  if (existsSync(cand)) return cand;
  throw new Error(`Map not found: ${arg}`);
}

function loadSidecar(setName) {
  const path = join(REPO, 'public', 'assets', 'tilesets', `${setName}.tileset.json`);
  if (!existsSync(path)) throw new Error(`Sidecar not found for set '${setName}': ${path}`);
  return JSON.parse(readFileSync(path, 'utf8'));
}

/** Build role -> local index map for one terrain group within a sidecar. */
function roleIndex(sidecar, terrain) {
  const map = new Map();
  for (const t of sidecar.tiles ?? []) {
    if (t.terrain === terrain && t.autotile) map.set(t.autotile, t.index);
  }
  return map;
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('usage: node tools/autotile/expand.mjs <map.json|id> [--output PATH] [--dry-run]');
    process.exit(2);
  }
  const mapArg = args[0];
  const outIdx = args.indexOf('--output');
  const dryRun = args.includes('--dry-run');
  const mapPath = resolveMap(mapArg);
  const outPath = outIdx >= 0 ? args[outIdx + 1] : mapPath;

  const map = JSON.parse(readFileSync(mapPath, 'utf8'));
  const { width, height } = map;
  const terrainLayers = (map.layers ?? []).filter((l) => l.role === 'terrain');
  if (terrainLayers.length === 0) {
    console.error(`No 'terrain' layers in ${mapPath}; nothing to expand.`);
    process.exit(1);
  }

  // first_gid per set, from the map's tilesets.
  const firstGid = new Map();
  for (const ts of map.tilesets ?? []) firstGid.set(ts.name, ts.first_gid);

  // Target base layer.
  const baseLayer = (map.layers ?? []).find((l) => (l.name === 'base' || l.role === 'base'));
  if (!baseLayer) throw new Error("Map has no 'base' layer to write into.");
  const base = baseLayer.data.slice();

  const stats = [];
  for (const layer of terrainLayers) {
    const sidecar = loadSidecar(layer.set);
    const roles = roleIndex(sidecar, layer.terrain);
    if (roles.size === 0) {
      throw new Error(`Set '${layer.set}' has no tiles tagged terrain='${layer.terrain}'. ` +
        `Tag them in the tileset manifest (terrain + autotile) and re-pack.`);
    }
    const fg = firstGid.get(layer.set);
    if (fg == null) throw new Error(`Set '${layer.set}' is not in the map's tilesets.`);

    const grid = layer.data;
    let placed = 0;
    const missing = new Set();
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        if (grid[y * width + x] !== 1) continue;
        const role = classify(neighbours(grid, width, height, x, y));
        let local;
        for (const cand of roleFallbacks(role)) {
          if (roles.has(cand)) { local = roles.get(cand); break; }
        }
        if (local == null) { missing.add(role); local = roles.get('fill'); }
        if (local == null) continue;
        base[y * width + x] = fg + local;
        placed += 1;
      }
    }
    stats.push({ layer: layer.name, terrain: layer.terrain, set: layer.set, placed,
      missing_roles: [...missing] });
  }

  baseLayer.data = base;
  if (!dryRun) writeFileSync(outPath, JSON.stringify(map, null, 2) + '\n');
  console.log(JSON.stringify({ map: mapPath, output: dryRun ? '(dry-run)' : outPath, layers: stats }, null, 2));
}

main();
