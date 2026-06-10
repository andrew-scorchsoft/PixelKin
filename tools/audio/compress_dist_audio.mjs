#!/usr/bin/env node
// Shrink the audio that actually ships, without touching the masters.
//
// The hi-fi .mp3 loops/SFX in public/assets/audio/ (renders of the .mid
// masters) are 160 kbps mono and dominate the build (~63 MB of a ~70 MB
// upload). They stay full-fidelity in the repo; this step re-encodes ONLY the
// copies Vite has placed in dist/ down to a low bitrate that is transparent for
// chiptune. Filenames are unchanged, so the tolerant audio loaders need no edit.
//
// Run after `vite build` (see the `build:dist` npm script). ffmpeg required.

import { execFileSync } from 'node:child_process';
import { readdirSync, statSync, renameSync, rmSync } from 'node:fs';
import { join, extname } from 'node:path';

const DIST_AUDIO = 'dist/assets/audio';
const BITRATE = '64k'; // mono; chiptune is a few square waves — 64k is plenty.

function haveFfmpeg() {
  try {
    execFileSync('ffmpeg', ['-version'], { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else if (extname(p).toLowerCase() === '.mp3') out.push(p);
  }
  return out;
}

function mb(bytes) {
  return (bytes / 1048576).toFixed(2);
}

if (!haveFfmpeg()) {
  console.error('compress_dist_audio: ffmpeg not found on PATH — skipping audio compression.');
  process.exit(1);
}

let files;
try {
  files = walk(DIST_AUDIO);
} catch {
  console.error(`compress_dist_audio: ${DIST_AUDIO} not found — run "vite build" first.`);
  process.exit(1);
}

let before = 0;
let after = 0;
for (const f of files) {
  before += statSync(f).size;
  const tmp = `${f}.tmp.mp3`;
  execFileSync('ffmpeg', ['-y', '-i', f, '-ac', '1', '-b:a', BITRATE, '-loglevel', 'error', tmp]);
  rmSync(f);
  renameSync(tmp, f);
  after += statSync(f).size;
}

console.log(
  `compress_dist_audio: ${files.length} mp3 @ ${BITRATE} mono — ` +
    `${mb(before)} MB -> ${mb(after)} MB (saved ${mb(before - after)} MB)`,
);
