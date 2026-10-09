#!/usr/bin/env node
// Shrink the audio that actually ships, without touching the masters.
//
// The hi-fi .mp3 loops/SFX in public/assets/audio/ (renders of the .mid
// masters) are 160 kbps mono and dominate the build (~63 MB of a ~70 MB
// upload). They stay full-fidelity in the repo; this step re-encodes ONLY the
// copies Vite has placed in dist/ down to a low bitrate that is transparent for
// chiptune. Filenames are unchanged, so the tolerant audio loaders need no edit.
//
// Run after `vite build` (see the `build:dist` npm script). Uses ffmpeg from
// PATH, else the `ffmpeg-static` devDependency (so CI / Cloudflare Workers
// Builds, which ship no ffmpeg, still compress). With neither it warns and
// leaves the full-fidelity audio in place rather than failing the build.

import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { readdirSync, statSync, renameSync, rmSync } from 'node:fs';
import { join, extname } from 'node:path';

const DIST_AUDIO = 'dist/assets/audio';
const BITRATE = '64k'; // mono; chiptune is a few square waves — 64k is plenty.

function works(bin) {
  try {
    execFileSync(bin, ['-version'], { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

function findFfmpeg() {
  if (works('ffmpeg')) return 'ffmpeg';
  try {
    const bin = createRequire(import.meta.url)('ffmpeg-static');
    if (bin && works(bin)) return bin;
  } catch {
    // ffmpeg-static not installed
  }
  return null;
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

const FFMPEG = findFfmpeg();
if (!FFMPEG) {
  console.warn('compress_dist_audio: no ffmpeg (PATH or ffmpeg-static) — shipping full-fidelity audio uncompressed.');
  process.exit(0);
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
  execFileSync(FFMPEG, ['-y', '-i', f, '-ac', '1', '-b:a', BITRATE, '-loglevel', 'error', tmp]);
  rmSync(f);
  renameSync(tmp, f);
  after += statSync(f).size;
}

console.log(
  `compress_dist_audio: ${files.length} mp3 @ ${BITRATE} mono — ` +
    `${mb(before)} MB -> ${mb(after)} MB (saved ${mb(before - after)} MB)`,
);
