#!/usr/bin/env node
/**
 * Assemble a deployable `release/` folder for FTP upload to the WHM/cPanel host
 * (pixelk.in). The marketing site sits at the root; the playable game goes in a
 * subfolder so it serves at pixelk.in/play/.
 *
 *   release/
 *     index.php, story.php, creatures.php, includes/, assets/   ← the web/ site
 *     play/                                                     ← the game's dist/
 *
 * You then FTP the *contents* of release/ into public_html/.
 *
 * Usage (via npm scripts — see package.json):
 *   node tools/build/assemble_release.mjs            # both site + game
 *   node tools/build/assemble_release.mjs --site     # site only (leaves play/ untouched)
 *   node tools/build/assemble_release.mjs --game     # game only (drops dist/ into play/)
 *
 * Notes:
 *  - The game must be built first for --game / default (run `npm run build:dist`).
 *    The npm `release` / `release:game` scripts do this for you.
 *  - `--site` does NOT wipe an existing release/play/, so you can refresh the
 *    site without rebuilding the game.
 */

import { existsSync, mkdirSync, rmSync, cpSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(fileURLToPath(new URL('../../', import.meta.url)));
const WEB = join(ROOT, 'web');
const DIST = join(ROOT, 'dist');
const RELEASE = join(ROOT, 'release');
const PLAY = join(RELEASE, 'play');
const GAME_SUBDIR = 'play';

const args = process.argv.slice(2);
const onlySite = args.includes('--site');
const onlyGame = args.includes('--game');
const doSite = !onlyGame; // default + --site
const doGame = !onlySite; // default + --game

function copySite() {
    if (!existsSync(WEB)) {
        console.error('assemble_release: web/ not found.');
        process.exit(1);
    }
    // Refresh every site file/folder EXCEPT the game subdir, so `--site` can run
    // without disturbing an already-staged game build.
    if (existsSync(RELEASE)) {
        for (const name of readdirSync(RELEASE)) {
            if (name === GAME_SUBDIR) continue;
            rmSync(join(RELEASE, name), { recursive: true, force: true });
        }
    }
    mkdirSync(RELEASE, { recursive: true });
    cpSync(WEB, RELEASE, { recursive: true });
    console.log('  · site   → release/  (web/ copied)');
}

function copyGame() {
    if (!existsSync(DIST)) {
        console.error('assemble_release: dist/ not found — run "npm run build:dist" first.');
        process.exit(1);
    }
    rmSync(PLAY, { recursive: true, force: true });
    mkdirSync(PLAY, { recursive: true });
    cpSync(DIST, PLAY, { recursive: true });
    console.log(`  · game   → release/${GAME_SUBDIR}/  (dist/ copied)`);
}

console.log('assemble_release:');
if (doSite) copySite();
if (doGame) copyGame();
console.log(`\nDone. FTP the *contents* of ${RELEASE} into public_html/`);
console.log('  site → pixelk.in/        game → pixelk.in/play/');
