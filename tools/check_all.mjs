#!/usr/bin/env node
/**
 * check_all.mjs — run EVERY CI gate locally, exactly as CI does.
 *
 * The single source of truth is .github/workflows/checks.yml: this script reads
 * its `run:` steps (single-line and `run: |` blocks) and runs them in order, so a
 * new CI gate is picked up here with no edit. Setup steps (`npm ci`, `pip
 * install`) are skipped; `python3` is swapped for the project venv when it
 * exists (Pillow/numpy live there locally).
 *
 *   npm run check            # all gates, keep going, summary table, exit 1 on any FAIL
 *   npm run check -- --fast  # skip the slow ones (full map rebuild, balance sim)
 *
 * Run it before every push/PR — "one validated push beats three speculative ones".
 */
import { readFileSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const FAST = process.argv.includes('--fast');
const SLOW = [/check_rebuild\.py/, /simulate\.mjs/];
const SKIP = [/^npm ci\b/, /^pip install\b/];
const venvPy = path.join(ROOT, 'venv', 'bin', 'python');
const PY = existsSync(venvPy) ? venvPy : 'python3';

// --- parse the workflow's steps: { name, cmd } -----------------------------------
const lines = readFileSync(path.join(ROOT, '.github/workflows/checks.yml'), 'utf8').split('\n');
const steps = [];
let pendingName = null;
for (let i = 0; i < lines.length; i++) {
  const l = lines[i];
  const name = l.match(/^\s*-\s*name:\s*(.+)$/);
  if (name) { pendingName = name[1].trim(); continue; }
  const run = l.match(/^(\s*)(?:-\s*)?run:\s*(.*)$/);
  if (!run) continue;
  let cmd = run[2].trim();
  if (cmd === '|') {
    const indent = run[1].length;
    const block = [];
    while (i + 1 < lines.length && (lines[i + 1].trim() === '' || lines[i + 1].search(/\S/) > indent)) {
      if (lines[i + 1].trim()) block.push(lines[i + 1].trim());
      i++;
    }
    cmd = block.join(' && ');
  }
  steps.push({ name: pendingName ?? cmd.slice(0, 60), cmd });
  pendingName = null;
}

// --- run ------------------------------------------------------------------------
const results = [];
for (const s of steps) {
  if (SKIP.some((r) => r.test(s.cmd))) continue;
  if (FAST && SLOW.some((r) => r.test(s.cmd))) { results.push({ ...s, status: 'skip', ms: 0 }); continue; }
  const cmd = s.cmd.replace(/\bpython3\b/g, PY);
  const t0 = Date.now();
  process.stdout.write(`… ${s.name}\n`);
  const r = spawnSync('bash', ['-c', cmd], { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  const ok = r.status === 0;
  results.push({ ...s, status: ok ? 'PASS' : 'FAIL', ms: Date.now() - t0, out: ok ? '' : (r.stdout + r.stderr).trim().split('\n').slice(-15).join('\n') });
}

console.log('\n' + '='.repeat(72));
for (const r of results) {
  console.log(`${r.status.padEnd(4)}  ${(r.ms / 1000).toFixed(1).padStart(6)}s  ${r.name}`);
}
const failed = results.filter((r) => r.status === 'FAIL');
for (const f of failed) console.log(`\n--- ${f.name} (last lines) ---\n${f.out}`);
console.log(`\n${results.length - failed.length}/${results.length} gates passed${FAST ? ' (--fast: slow gates skipped)' : ''}.`);
process.exit(failed.length ? 1 : 0);
