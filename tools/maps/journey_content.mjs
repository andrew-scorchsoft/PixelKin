#!/usr/bin/env node
/**
 * journey_content — dump the content registries audit_journey.py needs as JSON.
 *
 * The journey audit is Python (like the other map audits) but the grant logic
 * lives in TypeScript content: cutscene SCRIPTS (setFlag / battle / giveStarter /
 * legendaryBattle / pay / askName matches / run / choice), TRAINERS (reward_flags
 * + reward_abilities) and the crown INTERLUDES (engine-set seen flags). Rather
 * than regex-parse TS, bundle the modules with the repo's esbuild (same recipe as
 * tools/content/check_content.mjs) and print one JSON document on stdout.
 *
 *   node tools/maps/journey_content.mjs > /tmp/content.json
 *   node tools/maps/journey_content.mjs --root <repo>
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const args = process.argv.slice(2);
const ri = args.indexOf('--root');
const ROOT = path.resolve(ri >= 0 ? args[ri + 1]
  : path.join(path.dirname(new URL(import.meta.url).pathname), '..', '..'));
const require = createRequire(path.join(ROOT, 'package.json'));
const esbuild = require('esbuild');

const C = path.join(ROOT, 'src/game/content');
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'pk-journey-'));
const entry = path.join(scratch, 'entry.ts');
const out = path.join(scratch, 'bundle.mjs');
fs.writeFileSync(entry, [
  `export { SCRIPTS } from '${C}/scripts.ts';`,
  `export { TRAINERS } from '${C}/trainers.ts';`,
  `export { ITEMS } from '${C}/items.ts';`,
  `export { CROWN_INTERLUDES } from '${C}/interludes.ts';`,
  `export { WAYSTONES } from '${C}/waystones.ts';`,
  `export { CHARTS } from '${C}/charts.ts';`,
  `export { MAP_REGISTRY } from '${path.join(ROOT, 'src/game/data/world/maps.ts')}';`,
].join('\n'));
await esbuild.build({
  entryPoints: [entry], bundle: true, format: 'esm', platform: 'node', outfile: out,
  logLevel: 'error', external: ['phaser'],
  alias: { '@game': path.join(ROOT, 'src/game'), '@platform': path.join(ROOT, 'src/platform'),
    '@': path.join(ROOT, 'src') },
});
const K = await import(pathToFileURL(out).href);
const trainers = {};
for (const [id, t] of Object.entries(K.TRAINERS)) {
  trainers[id] = { reward_flags: t.reward_flags ?? [], reward_abilities: t.reward_abilities ?? [] };
}
const items = {};
for (const [id, it] of Object.entries(K.ITEMS)) {
  items[id] = { category: it.category ?? null, toggle_flag: it.toggle_flag ?? null };
}
process.stdout.write(JSON.stringify({
  scripts: K.SCRIPTS,
  trainers,
  items,
  registered: Object.keys(K.MAP_REGISTRY),
  waystones: K.WAYSTONES.map((w) => ({ id: w.id, map: w.map, tx: w.tx, ty: w.ty, visited_flag: w.visited_flag })),
  charts: K.CHARTS.map((c) => ({ id: c.id, maps: c.maps ?? [] })),
  interludes: K.CROWN_INTERLUDES.map((i) => ({ requires: i.requires, seen_flag: i.seen_flag })),
}));
fs.rmSync(scratch, { recursive: true, force: true });
