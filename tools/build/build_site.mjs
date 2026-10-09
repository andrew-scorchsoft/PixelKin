#!/usr/bin/env node
/**
 * Render the marketing site (web/) into static HTML.
 *
 *   web/pages/<stem>.html  (body)  ─┐
 *   web/layout.mjs  (head + footer) ├─▶  <out>/<stem>.html
 *   web/site.mjs  (data + blocks)  ─┘
 *   web/assets/, _redirects, .htaccess, .assetsignore  ──▶  copied as-is
 *
 * The output is plain static files, so it serves from a Cloudflare Worker's
 * static assets (wrangler.jsonc) or any static host. Cloudflare serves
 * /about from about.html and 404.html for anything missing.
 *
 * Usage: node tools/build/build_site.mjs [outDir]   (default: release/)
 * Does NOT touch <outDir>/play/ (the game build).
 */

import { cpSync, existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { PAGES, BLOCKS, tokens, typeColor } from '../../web/site.mjs';
import { header, footer } from '../../web/layout.mjs';

const ROOT = resolve(fileURLToPath(new URL('../../', import.meta.url)));
const WEB = join(ROOT, 'web');
const OUT = resolve(process.argv[2] ?? join(ROOT, 'release'));
const KEEP = new Set(['play']);

function render(page) {
    let body = readFileSync(join(WEB, 'pages', `${page.stem}.html`), 'utf8');
    body = body.replace(/<!-- block:([\w-]+) -->/g, (_, name) => {
        if (!BLOCKS[name]) throw new Error(`${page.stem}: unknown block "${name}"`);
        return BLOCKS[name]().replace(/^\n/, '');
    });
    const vals = tokens(page);
    body = body.replace(/\{\{(tint:)?(\w+)\}\}/g, (_, tint, key) => {
        if (tint) return typeColor(key);
        if (!(key in vals)) throw new Error(`${page.stem}: unknown token {{${key}}}`);
        return vals[key];
    });
    return header(page) + '\n' + body + '\n' + footer();
}

// Refresh everything except the staged game build.
if (existsSync(OUT)) {
    for (const name of readdirSync(OUT)) if (!KEEP.has(name)) rmSync(join(OUT, name), { recursive: true, force: true });
}
mkdirSync(OUT, { recursive: true });
cpSync(join(WEB, 'assets'), join(OUT, 'assets'), { recursive: true });
for (const f of ['_redirects', '.htaccess', '.assetsignore']) cpSync(join(WEB, f), join(OUT, f));
for (const page of PAGES) writeFileSync(join(OUT, `${page.stem}.html`), render(page));
console.log(`  · site   → ${OUT}  (${PAGES.length} pages)`);
