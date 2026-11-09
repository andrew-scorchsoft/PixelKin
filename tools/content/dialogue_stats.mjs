#!/usr/bin/env node
/**
 * Dialogue pace report — how long the game makes the player read.
 *
 *   node tools/content/dialogue_stats.mjs [--top 30] [--json out.json] [--budget]
 *
 * Bundles every script/dialogue registry (scripts.ts, dialogue.ts and the regional /
 * Old Light / trainer / kin-chatter registries it spreads), walks each script's steps
 * (say / narrate / choice prompts, recursing into choice branches) and estimates how
 * many dialogue-box PAGES each one costs the player, using the box's real geometry:
 *
 *   - PressStart2P is monospace (8px a glyph): 27 chars a row full-width, 23 beside a
 *     portrait bust; 4 rows a page (~100 characters).
 *
 * It prints totals, the longest single lines, and the longest interactions. With
 * `--budget` it also lists every line over 300 characters, the Pace Rubric's hard
 * ceiling (docs/world/dialogue-rubric.md) — informational, never an exit code.
 *
 * Key-information marks (`[[like this]]`) are stripped before measuring.
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const args = process.argv.slice(2);
const opt = (k, d) => {
  const i = args.indexOf(k);
  return i >= 0 ? args[i + 1] : d;
};
const TOP = Number(opt('--top', 25));
const JSON_OUT = opt('--json', null);
const BUDGET = args.includes('--budget');
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const require = createRequire(path.join(ROOT, 'package.json'));
const esbuild = require('esbuild');

const COLS_FULL = 27;
const COLS_PORTRAIT = 23;
const LINES_PER_PAGE = 4;

const strip = (t) => t.replace(/\[\[|\]\]/g, '');

/** Greedy word wrap, the way Phaser's basic word wrap breaks a line. */
function wrapCount(text, cols) {
  let lines = 0;
  for (const para of strip(text).split('\n')) {
    let cur = 0;
    let any = false;
    for (const w of para.split(/\s+/).filter(Boolean)) {
      const len = w.length;
      if (!any) {
        cur = len;
        any = true;
        lines += Math.max(1, Math.ceil(len / cols));
      } else if (cur + 1 + len <= cols) cur += 1 + len;
      else {
        lines += 1;
        cur = len;
      }
    }
    if (!any) lines += 1;
  }
  return lines;
}
const pagesOf = (text, portrait) => Math.ceil(wrapCount(text, portrait ? COLS_PORTRAIT : COLS_FULL) / LINES_PER_PAGE);

async function load() {
  const C = path.join(ROOT, 'src/game/content');
  const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'pk-dlg-'));
  const entry = path.join(scratch, 'entry.ts');
  const out = path.join(scratch, 'bundle.mjs');
  fs.writeFileSync(
    entry,
    [
      `export { SCRIPTS } from '${C}/scripts.ts';`,
      `export { DIALOGUE } from '${C}/dialogue.ts';`,
      `export { TRAINER_DIALOGUE } from '${C}/trainers.ts';`,
    ].join('\n'),
  );
  await esbuild.build({
    entryPoints: [entry],
    bundle: true,
    format: 'esm',
    platform: 'node',
    outfile: out,
    logLevel: 'error',
    alias: { '@game': path.join(ROOT, 'src/game'), '@platform': path.join(ROOT, 'src/platform'), '@': path.join(ROOT, 'src') },
    external: ['phaser'],
  });
  return import(pathToFileURL(out).href);
}

/** Every text a script shows (say / narrate / choice prompt), recursing into branches. */
function scriptTexts(steps, acc = []) {
  for (const s of steps ?? []) {
    if (s.op === 'say' || s.op === 'narrate') acc.push({ text: s.text, portrait: !!s.portrait && s.style !== 'narrate' });
    else if (s.op === 'choice') {
      if (s.prompt) acc.push({ text: s.prompt, portrait: false });
      for (const o of s.options ?? []) scriptTexts(o.ops, acc);
    }
  }
  return acc;
}

const { SCRIPTS, DIALOGUE, TRAINER_DIALOGUE } = await load();
const units = []; // { ref, kind, lines: [{text, portrait, pages}] }
const add = (ref, kind, lines) =>
  units.push({ ref, kind, lines: lines.map((l) => ({ ...l, pages: pagesOf(l.text, l.portrait) })) });
for (const [ref, lines] of Object.entries(DIALOGUE)) add(ref, 'dialogue', lines.map((l) => ({ text: l.text, portrait: !!l.portrait })));
for (const [ref, lines] of Object.entries(TRAINER_DIALOGUE ?? {})) add(ref, 'trainer', lines.map((l) => ({ text: l.text, portrait: !!l.portrait })));
for (const [ref, steps] of Object.entries(SCRIPTS)) add(ref, 'script', scriptTexts(steps));

const allLines = units.flatMap((u) => u.lines.map((l) => ({ ...l, ref: u.ref })));
const totalChars = allLines.reduce((s, l) => s + strip(l.text).length, 0);
const totalPages = allLines.reduce((s, l) => s + l.pages, 0);
const marks = allLines.reduce((s, l) => s + (l.text.match(/\[\[/g)?.length ?? 0), 0);
const len = (l) => strip(l.text).length;
const over160 = allLines.filter((l) => len(l) > 160).length;
const over300 = allLines.filter((l) => len(l) > 300).length;

console.log('Dialogue pace report');
console.log(`  units: ${units.length}   lines: ${allLines.length}   chars: ${totalChars}   est. pages: ${totalPages}`);
console.log(`  avg chars/line: ${(totalChars / allLines.length).toFixed(0)}   lines >160 chars: ${over160}   lines >300 chars (ceiling): ${over300}`);
console.log(`  key-information marks: ${marks}`);

console.log(`\nLongest single lines (pages):`);
for (const l of [...allLines].sort((a, b) => b.pages - a.pages).slice(0, TOP))
  console.log(`  ${String(l.pages).padStart(2)}  ${l.ref}  "${strip(l.text).slice(0, 70)}…"`);

console.log(`\nLongest interactions (pages, whole script incl. branches):`);
const unitPages = units.map((u) => ({ ref: u.ref, pages: u.lines.reduce((s, l) => s + l.pages, 0) }));
for (const u of unitPages.sort((a, b) => b.pages - a.pages).slice(0, TOP)) console.log(`  ${String(u.pages).padStart(3)}  ${u.ref}`);

if (BUDGET) {
  console.log('\nLines over the 300-character ceiling:');
  for (const l of allLines.filter((x) => len(x) > 300)) console.log(`  ${len(l)}  ${l.ref}`);
}

if (JSON_OUT)
  fs.writeFileSync(
    JSON_OUT,
    JSON.stringify({ totalChars, totalPages, lines: allLines.length, over160, over300, marks, units: unitPages }, null, 1),
  );
