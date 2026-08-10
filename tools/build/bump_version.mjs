#!/usr/bin/env node
/**
 * Bump the project's version in the TWO places that hold it, in one step:
 *
 *   • package.json  "version"          — full semver, e.g. 1.3.0
 *   • src/game/version.ts GAME_VERSION — the player-facing "major.minor", e.g. 1.3
 *     (surfaces on the title screen + the browser tab title)
 *
 * Used by the deploy flow (.claude/skills/deploy-ftp) so every upload carries a
 * fresh, visible version — but it's a normal script you can run by hand too.
 *
 * Usage:
 *   node tools/build/bump_version.mjs minor      # 1.3.0 -> 1.4.0   (the default)
 *   node tools/build/bump_version.mjs major      # 1.3.0 -> 2.0.0
 *   node tools/build/bump_version.mjs patch      # 1.3.0 -> 1.3.1
 *   node tools/build/bump_version.mjs none       # print the current version, change nothing
 *   node tools/build/bump_version.mjs minor --dry-run
 *   node tools/build/bump_version.mjs --print    # print the current version only
 *
 * Prints the resulting version on the last line as `version=X.Y.Z` so callers
 * (and Claude) can scrape it for a commit message or a deploy log.
 */

import { readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(fileURLToPath(new URL('../../', import.meta.url)));
const PKG = join(ROOT, 'package.json');
const VERSION_TS = join(ROOT, 'src/game/version.ts');

const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');
const printOnly = args.includes('--print');
const level = args.find((a) => !a.startsWith('--')) ?? (printOnly ? 'none' : 'minor');

const LEVELS = new Set(['major', 'minor', 'patch', 'none']);
if (!LEVELS.has(level)) {
    console.error(`bump_version: unknown level "${level}" (expected major|minor|patch|none).`);
    process.exit(1);
}

const pkgRaw = readFileSync(PKG, 'utf8');
const pkg = JSON.parse(pkgRaw);
const current = String(pkg.version ?? '0.0.0');
const m = /^(\d+)\.(\d+)\.(\d+)/.exec(current);
if (!m) {
    console.error(`bump_version: package.json version "${current}" isn't semver.`);
    process.exit(1);
}
let [major, minor, patch] = m.slice(1).map(Number);

if (level === 'major') { major += 1; minor = 0; patch = 0; }
else if (level === 'minor') { minor += 1; patch = 0; }
else if (level === 'patch') { patch += 1; }

const next = `${major}.${minor}.${patch}`;
const gameVersion = `${major}.${minor}`; // what the player sees

if (level === 'none') {
    console.log(`bump_version: no bump requested — staying on ${current}.`);
    console.log(`version=${current}`);
    process.exit(0);
}

if (dryRun) {
    console.log(`bump_version (dry run): ${current} -> ${next}  (GAME_VERSION '${gameVersion}')`);
    console.log(`version=${next}`);
    process.exit(0);
}

// package.json — surgical replace of the top-level "version" line so we keep the
// file's own formatting (JSON.stringify would reflow the whole thing).
const patched = pkgRaw.replace(
    /("version"\s*:\s*")[^"]+(")/,
    (_all, a, b) => `${a}${next}${b}`,
);
if (patched === pkgRaw) {
    console.error('bump_version: could not find a "version" field to patch in package.json.');
    process.exit(1);
}
writeFileSync(PKG, patched);

// src/game/version.ts — the displayed major.minor.
// A patch bump leaves major.minor alone, so an unchanged file is expected here —
// only a regex that doesn't MATCH means the constant has gone missing.
const vtsRaw = readFileSync(VERSION_TS, 'utf8');
const GAME_VERSION_RE = /(export const GAME_VERSION\s*=\s*')[^']+(')/;
if (!GAME_VERSION_RE.test(vtsRaw)) {
    console.error('bump_version: could not find GAME_VERSION in src/game/version.ts.');
    process.exit(1);
}
const vtsPatched = vtsRaw.replace(GAME_VERSION_RE, (_all, a, b) => `${a}${gameVersion}${b}`);
if (vtsPatched !== vtsRaw) writeFileSync(VERSION_TS, vtsPatched);

console.log(`bump_version: ${current} -> ${next}`);
console.log(`  · package.json          version      = ${next}`);
console.log(`  · src/game/version.ts   GAME_VERSION = '${gameVersion}'`);
console.log(`version=${next}`);
