#!/usr/bin/env node
/**
 * PixelKin static content checker (story/content integrity across ALL content + ALL maps).
 *
 *   node content_check.mjs [--root <repo>] [--old <root of a baseline checkout>] [--json out.json]
 *
 * Bundles src/game/content/* with esbuild (from the repo's node_modules), loads every
 * map JSON in public/assets/maps, and reports:
 *   E-REF     unresolved dialogue_ref / trigger ref / blocked_ref / run / dialogue / cooldownRef /
 *             missingRef / battle trainer / trainer intro/defeat / shop / item / cinematic
 *   E-KIND    a non-script trigger (sign/dialogue) whose ref is a script.* (shows "...")
 *   E-ACTOR   a cutscene actor id not placed on any map that can play the script
 *   E-PORT    portrait / expr not in portraits.ts
 *   E-SPRITE  NPC sprite with no sheet (renders a coloured-box placeholder) / object sprite missing
 *   E-FLAG    flag READ but never SET anywhere (content, maps, derived, engine literals)
 *   W-STAGE   staged if_flag/unless_flag (and NPC requires/hidden) chains: gap or overlap
 *   W-OBJSWAP flag-gated SOLID object without a same-footprint partner (invisible wall / missing swap)
 *   W-PROG    progression step (setFlag of a gating flag, battle, giveItem, giveKin, ...) guarded
 *   W-DUP     a regional/oldlight registry key that collides with (silently overrides) another
 *   W-TEXT    an unbreakable word too wide for the dialogue box; banned-vocabulary hits
 *   I-UNREAD  flags set but never read (informational)
 *   PRE       (with --old) per-script count of player-paced steps old→new for the pre-Chickenpig path
 * Exit code 1 when any E-* finding exists.
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
// Default root: the repo this script lives in (tools/content/ -> ../..).
const ROOT = path.resolve(opt('--root', path.join(path.dirname(new URL(import.meta.url).pathname), '..', '..')));
const OLD = opt('--old', null);
const JSON_OUT = opt('--json', null);
const SCRATCH = fs.mkdtempSync(path.join(os.tmpdir(), 'pk-content-'));
const require = createRequire(path.join(ROOT, 'package.json'));
const esbuild = require('esbuild');

async function loadContent(root, tag) {
  const C = path.join(root, 'src/game/content');
  const has = (f) => fs.existsSync(path.join(C, f));
  const lines = [
    `export { SCRIPTS } from '${C}/scripts.ts';`,
    `export { DIALOGUE } from '${C}/dialogue.ts';`,
    `export { PORTRAITS } from '${C}/portraits.ts';`,
    `export { ITEMS } from '${C}/items.ts';`,
    `export { TRAINERS, TRAINER_DIALOGUE } from '${C}/trainers.ts';`,
    `export { SHOPS } from '${C}/shops.ts';`,
    `export { QUESTS } from '${C}/quests.ts';`,
    `export { GLOSSARY } from '${C}/glossary.ts';`,
    `export { CHARTS } from '${C}/charts.ts';`,
    `export { WAYSTONES } from '${C}/waystones.ts';`,
    `export { GLEAMS } from '${C}/gleams.ts';`,
    `export { CINEMATICS } from '${C}/cinematics.ts';`,
    `export { OLDLIGHT_SCRIPTS, OLDLIGHT_DIALOGUE } from '${C}/oldlight.ts';`,
  ];
  if (has('regions/index.ts')) {
    for (const r of ['south', 'east', 'north', 'west', 'central'])
      lines.push(`export { ${r.toUpperCase()}_SCRIPTS, ${r.toUpperCase()}_DIALOGUE } from '${C}/regions/${r}.ts';`);
  }
  const entry = path.join(SCRATCH, `.cc_entry_${tag}.ts`);
  const out = path.join(SCRATCH, `.cc_bundle_${tag}.mjs`);
  fs.writeFileSync(entry, lines.join('\n'));
  await esbuild.build({
    entryPoints: [entry],
    bundle: true,
    format: 'esm',
    platform: 'node',
    outfile: out,
    logLevel: 'error',
    alias: { '@game': path.join(root, 'src/game'), '@platform': path.join(root, 'src/platform'), '@': path.join(root, 'src') },
    external: ['phaser'],
  });
  return import(pathToFileURL(out).href + `?t=${Date.now()}`);
}

function loadMaps(root) {
  const dir = path.join(root, 'public/assets/maps');
  const maps = {};
  for (const f of fs.readdirSync(dir)) if (f.endsWith('.json')) maps[f.slice(0, -5)] = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
  return maps;
}

// ---- walk helpers -----------------------------------------------------------
/** Flatten a step list including choice branches; yields {step, guards:[...]} */
function* walkSteps(steps, guards = []) {
  for (const s of steps ?? []) {
    const g = [...guards];
    if (s.if_flag) g.push({ if: s.if_flag });
    if (s.unless_flag) g.push({ unless: s.unless_flag });
    yield { step: s, guards: g };
    if (s.op === 'choice')
      for (const o of s.options ?? []) {
        const og = [...g];
        if (o.if_flag) og.push({ if: o.if_flag });
        if (o.unless_flag) og.push({ unless: o.unless_flag });
        yield* walkSteps(o.ops, og);
      }
  }
}
const SPEECH = new Set(['say', 'narrate', 'dialogue', 'choice', 'askName']);

async function analyse(root, tag) {
  const K = await loadContent(root, tag);
  const maps = loadMaps(root);
  const findings = [];
  const add = (code, msg, extra = {}) => findings.push({ code, msg, ...extra });
  const SCRIPTS = K.SCRIPTS, DIALOGUE = K.DIALOGUE;

  // --- registry collisions (regional spreads land LAST and silently override) ---
  if (K.SOUTH_SCRIPTS) {
    const src = fs.readFileSync(path.join(root, 'src/game/content/scripts.ts'), 'utf8');
    const dsrc = fs.readFileSync(path.join(root, 'src/game/content/dialogue.ts'), 'utf8');
    const baseS = new Set([...src.matchAll(/^\s{2}'([^']+)':\s*\[/gm)].map((m) => m[1]));
    const baseD = new Set([...dsrc.matchAll(/^\s{2}'([^']+)':\s*\[/gm)].map((m) => m[1]));
    const seen = new Map();
    for (const [reg, objS, objD] of [
      ['oldlight', K.OLDLIGHT_SCRIPTS, K.OLDLIGHT_DIALOGUE],
      ...['south', 'east', 'north', 'west', 'central'].map((r) => [r, K[`${r.toUpperCase()}_SCRIPTS`], K[`${r.toUpperCase()}_DIALOGUE`]]),
    ]) {
      for (const k of Object.keys(objS)) {
        if (baseS.has(k)) add('W-DUP', `${reg} script '${k}' overrides scripts.ts`);
        if (seen.has('s' + k)) add('W-DUP', `${reg} script '${k}' collides with ${seen.get('s' + k)}`);
        seen.set('s' + k, reg);
      }
      for (const k of Object.keys(objD)) {
        if (baseD.has(k)) add('W-DUP', `${reg} dialogue '${k}' overrides dialogue.ts`);
        if (seen.has('d' + k)) add('W-DUP', `${reg} dialogue '${k}' collides with ${seen.get('d' + k)}`);
        seen.set('d' + k, reg);
      }
    }
  }

  // --- who can play which script (maps → scripts, transitive via run) ---
  const scriptMaps = {}; // script ref -> Set(map ids)
  const mark = (ref, m) => ((scriptMaps[ref] ??= new Set()).add(m));
  const refUsers = []; // {ref, where}
  for (const [mid, m] of Object.entries(maps)) {
    for (const n of m.npcs ?? []) {
      if (n.dialogue_ref) {
        refUsers.push({ ref: n.dialogue_ref, where: `${mid} npc ${n.id}`, script: n.dialogue_ref.startsWith('script.') });
        if (!n.dialogue_ref.startsWith('script.') && SCRIPTS[n.dialogue_ref] && !DIALOGUE[n.dialogue_ref]) add('E-KIND', `${mid} npc ${n.id}: dialogue_ref '${n.dialogue_ref}' is a SCRIPT key without the script. prefix — NPCs only run script.* refs, so this renders "..."`);
        if (n.dialogue_ref.startsWith('script.')) mark(n.dialogue_ref, mid);
      }
    }
    for (const t of m.triggers ?? []) {
      const isScript = t.kind === 'script' || t.kind === 'cutscene';
      refUsers.push({ ref: t.ref, where: `${mid} trigger ${t.id} (${t.kind})`, script: isScript });
      if (!isScript && t.ref?.startsWith('script.')) add('E-KIND', `${mid} trigger ${t.id}: kind '${t.kind}' but ref ${t.ref} (renders "...")`);
      if (isScript) mark(t.ref, mid);
      if (t.blocked_ref) refUsers.push({ ref: t.blocked_ref, where: `${mid} trigger ${t.id} blocked_ref`, script: false });
    }
    for (const w of m.warps ?? []) {
      if (!w.blocked_ref) continue;
      // a warp's blocked_ref may be a script.* (WorldScene.runBlockedScript)
      const isScript = w.blocked_ref.startsWith('script.');
      refUsers.push({ ref: w.blocked_ref, where: `${mid} warp ${w.id} blocked_ref`, script: isScript });
      if (isScript) mark(w.blocked_ref, mid);
    }
    for (const g of m.gates ?? []) if (g.blocked_ref) refUsers.push({ ref: g.blocked_ref, where: `${mid} gate blocked_ref`, script: false });
  }
  for (const u of refUsers) {
    if (u.script) {
      if (!SCRIPTS[u.ref]) add('E-REF', `${u.where}: script '${u.ref}' not found`);
    } else if (!DIALOGUE[u.ref]) add('E-REF', `${u.where}: dialogue '${u.ref}' not found (renders "...")`);
  }
  // propagate maps through `run`
  let changed = true;
  while (changed) {
    changed = false;
    for (const [ref, steps] of Object.entries(SCRIPTS)) {
      const ms = scriptMaps[ref];
      if (!ms) continue;
      for (const { step } of walkSteps(steps))
        if (step.op === 'run')
          for (const m of ms) if (!scriptMaps[step.ref]?.has(m)) (mark(step.ref, m), (changed = true));
    }
  }

  const sfxStems = new Set(JSON.parse(fs.readFileSync(path.join(root, 'public/assets/audio/sfx/sfx.manifest.json'), 'utf8')).stems ?? []);
  const musicDir = path.join(root, 'public/assets/audio/music');
  const music = new Set(fs.readdirSync(musicDir).filter((f) => f.endsWith('.mp3')).map((f) => f.slice(0, -4)));
  const portraitFrames = {};
  for (const [k, d] of Object.entries(K.PORTRAITS)) {
    const f = path.join(root, 'public', d.path);
    if (!fs.existsSync(f)) { add('E-PORT', `portrait sheet ${d.path} missing`); continue; }
    const b = fs.readFileSync(f);
    portraitFrames[k] = b.readUInt32BE(16) / 32;
    for (const [e, i] of Object.entries(d.expressions)) if (i >= portraitFrames[k]) add('E-PORT', `portrait '${k}' expr '${e}' frame ${i} beyond sheet (${portraitFrames[k]} frames)`);
  }
  const portraitOk = (p, e) => {
    const def = K.PORTRAITS[p];
    if (!def) return `portrait '${p}' missing`;
    if (e && def.expressions && !(e in def.expressions)) return `portrait '${p}' has no expr '${e}'`;
    return null;
  };
  const textIssues = (txt, where, portrait) => {
    const max = portrait ? 23 : 27;
    for (const w of txt.replace(/\{name\}/g, 'Wayfarer').split(/\s+/)) if (w.length > max) add('W-TEXT', `${where}: unbreakable word (${w.length} ch > ${max}): "${w}"`);
  };

  // --- per-script checks ---
  const reads = new Map(); // flag -> [where]
  const sets = new Map();
  const R = (f, w) => f && (reads.get(f) ?? reads.set(f, []).get(f)).push(w);
  const S = (f, w) => f && (sets.get(f) ?? sets.set(f, []).get(f)).push(w);
  const progGuarded = [];
  let actorChecks = 0;
  for (const [ref, steps] of Object.entries(SCRIPTS)) {
    const playMaps = scriptMaps[ref];
    for (const { step: s, guards } of walkSteps(steps)) {
      const where = `${ref} [${s.op}]`;
      if (s.if_flag) R(s.if_flag, ref);
      if (s.unless_flag) R(s.unless_flag, ref);
      if (s.op === 'choice') for (const o of s.options ?? []) (R(o.if_flag, ref), R(o.unless_flag, ref));
      switch (s.op) {
        case 'run':
          if (!SCRIPTS[s.ref]) add('E-REF', `${ref}: run '${s.ref}' not found`);
          break;
        case 'dialogue':
          if (!DIALOGUE[s.ref]) add('E-REF', `${ref}: dialogue '${s.ref}' not found`);
          break;
        case 'battle': {
          const t = K.TRAINERS[s.trainer];
          if (!t) add('E-REF', `${ref}: trainer '${s.trainer}' not found`);
          break;
        }
        case 'spar': {
          if (!K.TRAINERS[s.trainer]) add('E-REF', `${ref}: spar trainer '${s.trainer}' not found`);
          if (!DIALOGUE[s.restingRef]) add('E-REF', `${ref}: spar restingRef '${s.restingRef}' not found`);
          break;
        }
        case 'legendaryBattle':
          if (!DIALOGUE[s.cooldownRef]) add('E-REF', `${ref}: cooldownRef '${s.cooldownRef}' not found`);
          S(s.caughtFlag, ref);
          break;
        case 'setLead':
          if (s.missingRef && !DIALOGUE[s.missingRef]) add('E-REF', `${ref}: missingRef '${s.missingRef}' not found`);
          break;
        case 'giveItem':
        case 'ensureItem':
          if (!K.ITEMS[s.item]) add('E-REF', `${ref}: item '${s.item}' not found`);
          break;
        case 'shop':
          if (!K.SHOPS[s.shop]) add('E-REF', `${ref}: shop '${s.shop}' not found`);
          break;
        case 'cinematic':
          if (!K.CINEMATICS[s.id]) add('E-REF', `${ref}: cinematic '${s.id}' not found`);
          break;
        case 'setFlag':
          if (s.value === false) R(s.flag, ref + '(clear)');
          else S(s.flag, ref);
          break;
        case 'pay':
          S(s.flag, ref);
          break;
        case 'milagroCard': // banks milagro:<card> (content/milagros.ts)
          S(s.card === 'lore' ? 'flag:milagro_lore' : `milagro:${s.card}`, ref);
          break;
        case 'timer': // a run clock's `stop` sets each beaten tier's flag (the Wick-Run)
          for (const t of s.tiers ?? []) (S(t.flag, ref), S(t.flag + '_now', ref));
          break;
        case 'askName':
          for (const m of s.matches ?? []) S(m.flag, ref);
          break;
        case 'sfx':
          if (!sfxStems.has(s.key) && !sfxStems.has(s.key + '-a')) add('W-REF', `${ref}: sfx '${s.key}' not in sfx.manifest`);
          break;
        case 'music':
        case 'musicCrossfade':
        case 'musicSting':
          if (s.key && !music.has(s.key)) add('W-REF', `${ref}: music '${s.key}' has no mp3`);
          break;
        case 'say':
          if (s.portrait) {
            const e = portraitOk(s.portrait, s.expr);
            if (e) add('E-PORT', `${ref}: ${e}`);
          }
          textIssues(s.text, ref, !!s.portrait);
          break;
        case 'narrate':
          textIssues(s.text, ref, false);
          break;
      }
      if (s.actor && s.actor !== 'player') actorChecks++;
      if (s.actor && s.actor !== 'player') {
        if (!playMaps || playMaps.size === 0) add('I-ACTOR', `${ref}: actor '${s.actor}' — script not placed on any map (cannot verify)`);
        else {
          const missing = [...playMaps].filter((m) => !(maps[m].npcs ?? []).some((n) => n.id === s.actor));
          if (missing.length) add('E-ACTOR', `${ref}: actor '${s.actor}' absent on ${missing.join(', ')} (op ${s.op} silently no-ops)`);
        }
      }
      const progOps = ['battle', 'spar', 'giveItem', 'giveKin', 'giveStarter', 'legendaryBattle', 'bossBattle', 'cinematic', 'giveMoney', 'giveAbility', 'heal', 'ensureItem'];
      if (guards.length && (progOps.includes(s.op) || s.op === 'setFlag'))
        progGuarded.push({ ref, op: s.op, flag: s.flag ?? s.trainer ?? s.item ?? s.kin ?? '', guards: guards.map((g) => (g.if ? 'if ' + g.if : 'unless ' + g.unless)).join(' & '), onStep: !!(s.if_flag || s.unless_flag) });
    }
  }
  for (const [k, lines] of Object.entries(DIALOGUE))
    for (const l of lines) {
      if (l.portrait) {
        const e = portraitOk(l.portrait, l.expr);
        if (e) add('E-PORT', `dialogue ${k}: ${e}`);
      }
      textIssues(l.text, `dialogue ${k}`, !!l.portrait);
    }
  for (const [id, t] of Object.entries(K.TRAINERS)) {
    for (const r of [t.intro_ref, t.defeat_ref]) if (r && !K.TRAINER_DIALOGUE[r] && !DIALOGUE[r]) add('E-REF', `trainer ${id}: line '${r}' not found`);
    for (const f of t.reward_flags ?? []) S(f, `trainer ${id}`);
  }
  for (const [id, it] of Object.entries(K.ITEMS)) if (it.toggle_flag) (S(it.toggle_flag, `item ${id}`), R(it.toggle_flag, `item ${id}`));
  for (const sh of Object.values(K.SHOPS)) for (const e of sh.stock) if (typeof e !== 'string') R(e.requires_flag, `shop ${sh.id}`);
  for (const q of K.QUESTS) {
    R(q.start_flag, `quest ${q.id}`);
    R(q.done_flag, `quest ${q.id}`);
    for (const f of q.stage_flags ?? []) R(f, `quest ${q.id}`);
  }
  for (const g of K.GLOSSARY) if (g.unlock_flag) R(g.unlock_flag, `glossary ${g.id}`);
  for (const c of K.CHARTS) S(`chart:${c.id}`, 'charts (engine)');
  for (const w of K.WAYSTONES) for (const k of ['flag', 'requires_flag', 'unlock_flag', 'discover_flag']) if (w[k]) R(w[k], `waystone ${w.id}`);

  add('I-STAT', `actor references checked: ${actorChecks}`);
  // --- withheld-name audit: every 'Senna' must play only after flag:dawn ---
  const runnersOf = (ref) => Object.entries(maps).flatMap(([mid, m]) => [
    ...(m.npcs ?? []).filter((n) => n.dialogue_ref === ref).map((n) => `${mid}:${n.id} req=${n.requires_flag ?? '-'}`),
    ...(m.triggers ?? []).filter((t) => t.ref === ref).map((t) => `${mid}:${t.id} req=${t.requires_flag ?? '-'}`),
  ]);
  for (const [ref, steps] of Object.entries(SCRIPTS))
    for (const { step: s, guards } of walkSteps(steps))
      if (/Senna/.test(s.text ?? '')) add('I-SENNA', `${ref} guards=[${guards.map((g) => g.if ?? '!' + g.unless).join(',')}] runners=${runnersOf(ref).join(' | ') || '(run-only)'}`);
  for (const [ref, lines] of Object.entries(DIALOGUE)) if (lines.some((l) => /Senna/.test(l.text))) add('I-SENNA', `dialogue ${ref} runners=${runnersOf(ref).join(' | ')}`);

  // --- maps: flags, sprites, objects ---
  const trainerManifest = JSON.parse(fs.readFileSync(path.join(root, 'public/assets/sprites/trainers/trainers.manifest.json'), 'utf8'));
  const packed = new Set(Object.keys(trainerManifest.sheets ?? trainerManifest.trainers ?? trainerManifest));
  const npcSrc = fs.readFileSync(path.join(root, 'src/game/entities/Npc.ts'), 'utf8');
  const tableKeys = (name) => {
    const m = npcSrc.match(new RegExp(`const ${name}[^=]*=\\s*\\{([\\s\\S]*?)\\n\\};`));
    const out = {};
    if (m) for (const mm of m[1].matchAll(/^\s*'?([a-z0-9_]+)'?\s*:\s*'?([^',\n]+)'?,/gm)) out[mm[1]] = mm[2];
    return out;
  };
  const SHEETS = tableKeys('SPRITE_SHEETS'), FALLBACK = tableKeys('REGIONAL_FALLBACK'), ALIASES = tableKeys('CREATURE_SPRITE_ALIASES');
  const objManifest = JSON.parse(fs.readFileSync(path.join(root, 'public/assets/sprites/objects/objects.manifest.json'), 'utf8')).objects;
  const creatureManifest = JSON.parse(fs.readFileSync(path.join(root, 'public/assets/sprites/creatures/creatures.manifest.json'), 'utf8'));
  const creatureIds = new Set(Object.keys(creatureManifest.creatures ?? {}).map(Number));
  for (const [mid, m] of Object.entries(maps)) {
    for (const n of m.npcs ?? []) {
      R(n.requires_flag, `${mid}:${n.id}`);
      R(n.hidden_when_flag, `${mid}:${n.id}`);
      if (n.defeated_flag) (S(n.defeated_flag, `${mid}:${n.id} (engine on win)`), R(n.defeated_flag, `${mid}:${n.id}`));
      const sp = n.sprite;
      const km = /^kin_(\d+)_overworld$/.exec(sp);
      if (sp === 'item_cache' || sp === 'milagro_card' || sp in ALIASES) continue;
      if (km) {
        if (creatureIds.size && !creatureIds.has(Number(km[1]))) add('E-SPRITE', `${mid}:${n.id} creature sprite ${sp} not packed`);
        continue;
      }
      const sheet = SHEETS[sp];
      const fb = FALLBACK[sp];
      const isPacked = (k) => packed.has(k) || fs.existsSync(path.join(root, `public/assets/sprites/trainers/${k}.webp`));
      if (!sheet && !fb) add('E-SPRITE', `${mid}:${n.id} sprite '${sp}' not in SPRITE_SHEETS → coloured-box placeholder`);
      else if (!(sheet && isPacked(sheet)) && !(fb && isPacked(fb))) add('E-SPRITE', `${mid}:${n.id} sprite '${sp}' → sheet '${sheet ?? fb}' not packed → placeholder`);
    }
    for (const t of m.triggers ?? []) {
      R(t.requires_flag, `${mid}:${t.id}`);
      R(t.hidden_when_flag, `${mid}:${t.id}`);
      for (const f of t.sets_flags ?? []) S(f, `${mid}:${t.id}`);
    }
    for (const w of m.warps ?? []) R(w.requires_flag, `${mid}:warp ${w.id}`);
    for (const g of m.gates ?? []) (S(g.sets_flag, `${mid}:gate`), R(g.requires_flag, `${mid}:gate`));
    for (const z of m.encounters?.zones ?? m.encounters ?? []) if (z && typeof z === 'object') (R(z.requires_flag, `${mid}:zone`), R(z.hidden_when_flag, `${mid}:zone`));
    for (const o of m.objects ?? []) {
      if (!objManifest[o.sprite]) add('E-SPRITE', `${mid}: object ${o.id} sprite '${o.sprite}' not in objects.manifest`);
      R(o.requires_flag, `${mid}:obj ${o.id}`);
      R(o.hidden_when_flag, `${mid}:obj ${o.id}`);
    }
    // object swap pairs
    const gated = (m.objects ?? []).filter((o) => o.requires_flag || o.hidden_when_flag);
    for (const o of gated) {
      const solid = o.solid !== false;
      const f = o.requires_flag ?? o.hidden_when_flag;
      const partner = gated.find((p) => p !== o && (o.requires_flag ? p.hidden_when_flag === f : p.requires_flag === f) && p.at.tx === o.at.tx && p.at.ty === o.at.ty);
      if (partner) {
        if (partner.w !== o.w || partner.h !== o.h || (partner.solid !== false) !== solid || !!partner.walk_under !== !!o.walk_under || (partner.overhang ?? 0) !== (o.overhang ?? 0))
          add('W-OBJSWAP', `${mid}: swap pair ${o.id}/${partner.id} differ in footprint/solidity`);
      } else if (solid) add('W-OBJSWAP', `${mid}: solid flag-gated object ${o.id} (${o.requires_flag ? 'requires ' : 'hidden_when '}${f}) has no partner — collision stays while it is invisible`);
    }
  }

  // derived + engine-literal sets
  const fsrc = fs.readFileSync(path.join(root, 'src/game/systems/flags/FlagStore.ts'), 'utf8');
  for (const mm of fsrc.matchAll(/'((?:flag|gleam):[a-z0-9_]+)'/g)) S(mm[1], 'FlagStore (derived/literal)');
  const engineFiles = [];
  const walk = (d) => {
    for (const f of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, f.name);
      if (f.isDirectory()) {
        if (!p.includes('/content')) walk(p);
      } else if (p.endsWith('.ts')) engineFiles.push(p);
    }
  };
  walk(path.join(root, 'src'));
  const prefixes = [];
  for (const p of engineFiles) {
    const t = fs.readFileSync(p, 'utf8');
    for (const mm of t.matchAll(/['"]((?:flag|gleam|chart):[a-z0-9_]+)['"]/g)) S(mm[1], `engine ${path.basename(p)}`);
    for (const mm of t.matchAll(/`((?:flag|gleam|chart):[a-z0-9_]*)\$\{/g)) prefixes.push(mm[1]);
  }
  // gleam:* from the gleams registry are set by warden reward_flags; CHARTS discovered by engine.
  const isSet = (f) => sets.has(f) || prefixes.some((p) => p && f.startsWith(p));
  const readNeverSet = [...reads.keys()].filter((f) => !isSet(f)).sort();
  for (const f of readNeverSet) add('E-FLAG', `read-never-set ${f} ← ${[...new Set(reads.get(f))].slice(0, 4).join('; ')}`);
  const setNeverRead = [...sets.keys()].filter((f) => !reads.has(f) && !f.startsWith('chart:')).sort();
  for (const f of setNeverRead) add('I-UNREAD', `set-never-read ${f} ← ${[...new Set(sets.get(f))].slice(0, 3).join('; ')}`);

  // --- staged chains in scripts: (if A, unless B) stage groups ---
  const stageReport = (label, stages) => {
    // stages: [{if, unless, id}] ; build order A->B, enumerate prefix states along the longest chain
    const ifs = new Set(stages.map((s) => s.if).filter(Boolean));
    const nexts = new Map();
    for (const s of stages) if (s.if && s.unless) nexts.set(s.if, s.unless);
    // chain heads: an `if` that is no one's `unless`
    const unlessSet = new Set(stages.map((s) => s.unless).filter(Boolean));
    const heads = [...ifs].filter((f) => !unlessSet.has(f));
    for (const h of heads.length ? heads : [...ifs].slice(0, 1)) {
      const chain = [h];
      const seen = new Set([h]);
      while (nexts.has(chain.at(-1)) && !seen.has(nexts.get(chain.at(-1)))) (chain.push(nexts.get(chain.at(-1))), seen.add(chain.at(-1)));
      for (let i = 1; i <= chain.length; i++) {
        const held = new Set(chain.slice(0, i));
        const playing = stages.filter((s) => (!s.if || held.has(s.if)) && (!s.unless || !held.has(s.unless)) && (s.if || s.unless));
        const ids = [...new Set(playing.map((s) => s.id))];
        if (ids.length === 0) add('W-STAGE', `${label}: GAP — holding [${[...held].join(', ')}] nothing plays`);
        else if (ids.length > 1) add('W-STAGE', `${label}: OVERLAP — holding [${[...held].join(', ')}] ${ids.length} stages play: ${ids.join(' | ')}`);
      }
    }
  };
  for (const [ref, steps] of Object.entries(SCRIPTS)) {
    const top = (steps ?? []).filter((s) => SPEECH.has(s.op) || s.op === 'run');
    const paired = top.filter((s) => s.if_flag && s.unless_flag);
    if (paired.length < 2) continue;
    const stages = new Map();
    for (const s of top) if (s.if_flag || s.unless_flag) stages.set(`${s.if_flag ?? '-'}~${s.unless_flag ?? '-'}`, { if: s.if_flag, unless: s.unless_flag, id: `${s.if_flag ?? '-'}~${s.unless_flag ?? '-'}` });
    stageReport(`script ${ref}`, [...stages.values()]);
  }
  // NPC tile/id-family stacks: two placements visible on the same tile in one state
  for (const [mid, m] of Object.entries(maps)) {
    const byTile = new Map();
    for (const n of m.npcs ?? []) {
      const k = `${n.at.tx},${n.at.ty}`;
      (byTile.get(k) ?? byTile.set(k, []).get(k)).push(n);
    }
    for (const [k, ns] of byTile) {
      if (ns.length < 2) continue;
      // brute force over the flags involved (≤ 8)
      const fl = [...new Set(ns.flatMap((n) => [n.requires_flag, n.hidden_when_flag]).filter(Boolean))];
      if (fl.length > 8) continue;
      const bad = [];
      for (let mask = 0; mask < 1 << fl.length; mask++) {
        const held = new Set(fl.filter((_, i) => mask & (1 << i)));
        const vis = ns.filter((n) => (!n.requires_flag || held.has(n.requires_flag)) && !(n.hidden_when_flag && held.has(n.hidden_when_flag)));
        if (vis.length > 1) bad.push(`[${[...held].join(',') || '∅'}]→${vis.map((v) => v.id).join('+')}`);
      }
      if (bad.length) add('W-NPCSTACK', `${mid} (${k}) ids ${ns.map((n) => n.id).sort().join(',')}`, { key: `${mid}|${k}|${ns.map((n) => JSON.stringify([n.id, n.requires_flag, n.hidden_when_flag])).sort().join()}`, detail:  `${mid} (${k}): ${bad.length}/${1 << fl.length} flag states show >1 NPC on one tile, e.g. ${bad.slice(0, 2).join('  ')}` });
    }
  }

  // progression guarded (only on gating flags for setFlag)
  const gatingFlags = new Set();
  for (const m of Object.values(maps)) {
    for (const w of m.warps ?? []) if (w.requires_flag) gatingFlags.add(w.requires_flag);
    for (const t of m.triggers ?? []) if (t.requires_flag) gatingFlags.add(t.requires_flag);
    for (const g of m.gates ?? []) if (g.requires_flag) gatingFlags.add(g.requires_flag);
  }
  for (const t of Object.values(K.TRAINERS)) for (const f of t.reward_flags ?? []) if (f.startsWith('gleam:')) gatingFlags.add(f);
  for (const p of progGuarded) if (p.op !== 'setFlag' || gatingFlags.has(p.flag)) add('W-PROG', `${p.ref}: ${p.op} ${p.flag} guarded by ${p.guards}`, { key: `${p.ref}|${p.op}|${p.flag}|${p.guards}` });

  return { K, maps, findings, scriptMaps };
}

// ---- pre-Chickenpig comparison ---------------------------------------------
const PRE_PATH = [
  /^script\.(gate_warden|intro_mentor|dusk_begins|wren_dimglass|beacon_battle|brisa_quest|give_wick|reyl_quest|netmender_floats|netmender_rope|ring_moorbell)$/,
  /^script\.(beacon_keeper_[ab])$/,
  /^script\.oldlight_\d$|^script\.oldlight_(welcome|top)$/,
  /^script\.booji_/,
  /^script\.(catch_tutorial|tutorial_offer)$/,
];
/** Estimated DialogueBox pages for one line: greedy word-wrap at 27 ch (23 with a
 *  portrait) — Press Start 2P 8px in a 216/184px body — and LINES_PER_PAGE rows. */
const LINES_PER_PAGE = 3;
function estPages(text, portrait) {
  const w = portrait ? 23 : 27;
  let lines = 1, cur = 0;
  for (const word of String(text).replace(/\{name\}/g, 'Wayfarer').split(/\s+/).filter(Boolean)) {
    const need = cur === 0 ? word.length : cur + 1 + word.length;
    if (need > w && cur > 0) { lines++; cur = word.length; } else cur = need;
  }
  return Math.ceil(lines / LINES_PER_PAGE);
}
function paced(K, steps, seen = new Set()) {
  // count player-paced pages (say/narrate = 1, dialogue = its pages, choice/askName = 1); run expands
  let n = 0, pg = 0;
  const ops = {};
  for (const { step: s } of walkSteps(steps)) {
    ops[s.op] = (ops[s.op] ?? 0) + 1;
    if (s.op === 'say' || s.op === 'narrate') pg += estPages(s.text, s.op === 'say' && s.portrait);
    if (s.op === 'dialogue') for (const l of K.DIALOGUE[s.ref] ?? []) pg += estPages(l.text, l.portrait);
    if (s.op === 'choice' || s.op === 'askName') pg++;
    if (s.op === 'say' || s.op === 'narrate' || s.op === 'choice' || s.op === 'askName') n++;
    if (s.op === 'dialogue') n += (K.DIALOGUE[s.ref] ?? [1]).length;
    if (s.op === 'run' && !seen.has(s.ref)) {
      seen.add(s.ref);
      const r = paced(K, K.SCRIPTS[s.ref] ?? [], seen);
      n += r.n;
      pg += r.pg;
      for (const [k, v] of Object.entries(r.ops)) ops['run>' + k] = (ops['run>' + k] ?? 0) + v;
    }
  }
  return { n, pg, ops };
}

const cur = await analyse(ROOT, 'cur');
let oldA = null;
if (OLD) oldA = await analyse(path.resolve(OLD), 'old');

const out = [];
const byCode = {};
for (const f of cur.findings) byCode[f.code] = (byCode[f.code] ?? 0) + 1;
const newOnly = (code) => {
  if (!oldA) return cur.findings.filter((f) => f.code === code);
  const old = new Set(oldA.findings.filter((f) => f.code === code).map((f) => f.key ?? f.msg));
  return cur.findings.filter((f) => f.code === code && !old.has(f.key ?? f.msg));
};
out.push(`PixelKin content_check — root ${ROOT}${OLD ? `  (baseline ${OLD})` : ''}`);
out.push(`scripts ${Object.keys(cur.K.SCRIPTS).length}, dialogue ${Object.keys(cur.K.DIALOGUE).length}, maps ${Object.keys(cur.maps).length}`);
out.push('counts: ' + Object.entries(byCode).sort().map(([k, v]) => `${k}=${v}`).join('  '));
for (const code of ['E-REF', 'E-KIND', 'E-ACTOR', 'E-PORT', 'E-SPRITE', 'E-FLAG', 'W-DUP', 'W-REF', 'W-STAGE', 'W-NPCSTACK', 'W-OBJSWAP', 'W-PROG', 'W-TEXT', 'I-ACTOR', 'I-SENNA', 'I-STAT', 'I-UNREAD']) {
  const all = cur.findings.filter((f) => f.code === code);
  if (!all.length) continue;
  const fresh = newOnly(code);
  out.push(`\n== ${code}: ${all.length}${oldA ? ` (${fresh.length} new vs baseline)` : ''}`);
  for (const f of oldA ? fresh : all) out.push('  ' + f.msg + (f.detail ? ' :: ' + f.detail : ''));
}
if (oldA) {
  out.push('\n== PRE: pre-Chickenpig required scenes, player-paced pages old → new (+ new op kinds)');
  const keys = new Set([...Object.keys(cur.K.SCRIPTS), ...Object.keys(oldA.K.SCRIPTS)].filter((k) => PRE_PATH.some((re) => re.test(k))));
  for (const k of [...keys].sort()) {
    const a = paced(oldA.K, oldA.K.SCRIPTS[k] ?? []);
    const b = paced(cur.K, cur.K.SCRIPTS[k] ?? []);
    const newOps = Object.keys(b.ops).filter((o) => (b.ops[o] ?? 0) > (a.ops[o] ?? 0)).map((o) => `${o}+${b.ops[o] - (a.ops[o] ?? 0)}`);
    const flag = b.n > a.n ? '  <-- MORE STEPS' : b.pg > a.pg ? '  <-- MORE BOX PAGES (longer text)' : '';
    if (b.n !== a.n || b.pg !== a.pg || newOps.length) out.push(`  ${k}: steps ${a.n} → ${b.n}, est. pages ${a.pg} → ${b.pg}${flag}  ${newOps.join(' ')}`);
  }
  const cin = (K) => JSON.stringify(K.CINEMATICS);
  out.push(`  cinematics changed: ${cin(cur.K) !== cin(oldA.K)}`);
}
console.log(out.join('\n'));
if (JSON_OUT) fs.writeFileSync(JSON_OUT, JSON.stringify(cur.findings, null, 1));
process.exit(cur.findings.some((f) => f.code.startsWith('E-')) ? 1 : 0);
