#!/usr/bin/env node
// Remove .map files from the distributable. Sourcemaps are a debug aid (the JS
// map alone is ~10 MB) and are never needed by a deployed static site, so the
// `build:dist` flow drops them from dist/ to keep the upload small. The vite
// `build` still emits them for local debugging.

import { readdirSync, statSync, rmSync } from 'node:fs';
import { join, extname } from 'node:path';

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else if (extname(p).toLowerCase() === '.map') out.push(p);
  }
  return out;
}

let removed = 0;
let bytes = 0;
try {
  for (const f of walk('dist')) {
    bytes += statSync(f).size;
    rmSync(f);
    removed++;
  }
} catch {
  console.error('strip_sourcemaps: dist/ not found — run "vite build" first.');
  process.exit(1);
}

console.log(`strip_sourcemaps: removed ${removed} .map file(s), ${(bytes / 1048576).toFixed(2)} MB`);
