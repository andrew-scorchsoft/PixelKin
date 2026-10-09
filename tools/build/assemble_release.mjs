#!/usr/bin/env node
/**
 * Assemble the deployable `release/` folder: the static marketing site at the
 * root, the playable game in a subfolder so it serves at pixelk.in/play/.
 *
 *   release/
 *     index.html, about.html, …, 404.html, _redirects, assets/   ← web/ rendered
 *     play/                                                      ← the game's dist/
 *
 * release/ is exactly what the Cloudflare Worker serves (wrangler.jsonc →
 * assets.directory) — `npx wrangler deploy` uploads it. It's also plain static
 * files, so the FTP path (tools/deploy/ftp_deploy.py) still works too.
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
 *    site without rebuilding the game. If no game is staged yet it drops in a
 *    small "not built here" placeholder so /play/ doesn't 404 during site work.
 */

import { existsSync, mkdirSync, rmSync, cpSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(fileURLToPath(new URL('../../', import.meta.url)));
const DIST = join(ROOT, 'dist');
const RELEASE = join(ROOT, 'release');
const PLAY = join(RELEASE, 'play');
const GAME_SUBDIR = 'play';

const args = process.argv.slice(2);
const onlySite = args.includes('--site');
const onlyGame = args.includes('--game');
const doSite = !onlyGame; // default + --site
const doGame = !onlySite; // default + --game

const PLACEHOLDER = `<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>Play · PixelKin (site-only build)</title>
<style>
  body{margin:0;min-height:100vh;display:grid;place-items:center;text-align:center;
    font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
    color:#f5f0e1;background:linear-gradient(180deg,#0b1026,#0a0d1f);padding:2rem;}
  .card{max-width:560px;background:rgba(19,32,90,.5);border:1px solid rgba(159,231,255,.22);
    border-radius:14px;padding:2.5rem;}
  h1{color:#9fe7ff;font-size:1.4rem;margin:0 0 1rem;}
  code{background:rgba(0,0,0,.35);padding:.15rem .45rem;border-radius:5px;color:#ffd76b;}
  p{line-height:1.6;color:#d8d2e8;} a{color:#9fe7ff;}
</style></head>
<body><div class="card">
  <h1>The game isn't built here yet</h1>
  <p>This is a site-only build. Run <code>npm run release</code> to stage the game at <code>/play/</code>.</p>
  <p><a href="/">← Back to the site</a></p>
</div></body></html>
`;

function buildSite() {
    execFileSync(process.execPath, [join(ROOT, 'tools/build/build_site.mjs'), RELEASE], { stdio: 'inherit' });
    if (!existsSync(PLAY)) {
        mkdirSync(PLAY, { recursive: true });
        writeFileSync(join(PLAY, 'index.html'), PLACEHOLDER);
        console.log(`  · game   → release/${GAME_SUBDIR}/  (placeholder — game not built)`);
    }
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
if (doGame) copyGame();
if (doSite) buildSite();
console.log(`\nDone. Deploy with \`npx wrangler deploy\` (serves ${RELEASE})`);
console.log('  site → pixelk.in/        game → pixelk.in/play/');
