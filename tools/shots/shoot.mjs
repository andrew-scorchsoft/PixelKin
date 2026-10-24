#!/usr/bin/env node
/**
 * PixelKin headless screenshot harness.
 *
 * Boots the REAL game (Vite dev server + headless Chromium), injects a crafted
 * current-schema save into slot 1, drives the boot flow with the keyboard
 * (Splash -> Attract -> Title -> CONTINUE) and screenshots the canvas once the
 * WorldScene is idle. See tools/shots/README.md for usage.
 *
 * Reads game state through the dev-only `window.__pixelkin` handle (src/main.ts).
 */
import { createServer as createViteServer } from 'vite';
import { chromium } from 'playwright';
import net from 'node:net';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

const USAGE = `usage:
  node tools/shots/shoot.mjs --map <map_id> --x <tx> --y <ty> [options]
  node tools/shots/shoot.mjs --scene title [--out title.png]
  node tools/shots/shoot.mjs --batch shots.json

world options:
  --facing down|up|left|right   player facing (default down)
  --flags a,b,c                 world flags held (bare names get a "flag:" prefix;
                                "gleam:ember", "chart:x" etc. pass through)
  --abilities tidecall,...      Lantern Gifts held
  --items runner,lumen_drop:2   pack items held (id[:count])
  --party starter|none|ID[:LV[:HP[:STATUS]]],...  party (default "starter" = #1 Vulpyre lv 5);
                                HP 0 = fainted (test revives / FNT rows); STATUS e.g. numb
  --level N                     level for "starter" (default 5)
  --steps "right,right,up"      walk these steps after spawning (one tile each)
  --battle <kin_id>[:LV]        open a wild battle vs that kin on the map
  --trainer <trainer_id>        open a TRAINER battle (the trainer-intro beat); --confirms N
                                then pages on (1.4s apart) before the shot
  --greet <placement_id>        step beside that AMBIENT kin (wherever it grazed to),
                                face it and press Confirm — shoots the greeting
                                (cry + kinchatter line) mid-dialogue
  --script <script.ref>         play that cutscene script in the world (World.playScene);
                                --confirms N then pages on, 1.4s apart (battles too)
  --dump-flags <prefix>         after the shot, print every held world flag with that
                                prefix (e.g. "flag:brew") — check a scene's outcome
  --keep-hud                    don't wait for the area-name banner / SAVED glyph
                                to fade (default waits)
  --version-from <v>            write an older save last_version (e.g. 1.0, or ""
                                for pre-tracking) to shoot the "world has changed"
                                notice; default = current GAME_VERSION (no notice)
  --no-idle                     don't wait for the world to go idle after CONTINUE:
                                shoot --wait ms after the World starts (for a scene
                                that plays on load, e.g. a crown interlude)
  --confirms N                  with --no-idle (or --greet): then tap Confirm N times (1.4s
                                apart) to page through the scene's lines
  --no-defaults                 don't auto-add the quiet flags (chart reveals,
                                tutorials seen, has_starter)
common:
  --battle-keys "z,ArrowDown"   with --battle: once the wild battle is up, tap these keys
                                (~400ms apart) — open FIGHT/BAG, move the cursor
  --keys "Escape,ArrowDown,z"   after the world is idle, tap these keys in order
                                (Playwright key names, ~300ms apart) — open menus;
                                runs AFTER --confirms. Escape opens the pause menu
                                (Enter is Confirm and does not)
  --device WxH                  emulate a touch phone at WxH (e.g. 844x390 landscape) with
                                the device shell + on-screen controls; shoots the WHOLE page
  --out path.png                output (default ./shot.png)
  --scale N                     output = 240N x 160N px (default 4)
  --wait ms                     extra settle time before the shot (default 700;
                                battles default 2500)
  --url http://host:port/       use an already-running dev server
  --headed                      show the browser (debugging)
  --verbose                     log browser console`;

function parseArgs(argv) {
  const o = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) throw new Error(`unexpected argument: ${a}`);
    const key = a.slice(2);
    if (['no-defaults', 'no-idle', 'keep-hud', 'headed', 'verbose', 'help'].includes(key)) {
      o[key] = true;
      continue;
    }
    const v = argv[++i];
    if (v === undefined) throw new Error(`missing value for ${a}`);
    o[key] = v;
  }
  return o;
}

const list = (v) =>
  v === undefined || v === null
    ? []
    : Array.isArray(v)
      ? v.map(String)
      : String(v)
          .split(',')
          .map((s) => s.trim())
          .filter(Boolean);

/** Normalise a CLI/batch spec into a canonical shot object. */
function normaliseSpec(raw, index = 0) {
  const s = { ...raw };
  const shot = {
    scene: s.scene ?? (s.map ? 'world' : undefined),
    map: s.map,
    x: s.x !== undefined ? Number(s.x) : undefined,
    y: s.y !== undefined ? Number(s.y) : undefined,
    facing: s.facing ?? 'down',
    flags: list(s.flags),
    abilities: list(s.abilities),
    items: list(s.items),
    party: s.party ?? 'starter',
    level: Number(s.level ?? 5),
    steps: list(s.steps),
    battle: s.battle !== undefined ? String(s.battle) : undefined,
    trainer: s.trainer !== undefined ? String(s.trainer) : undefined,
    noDefaults: Boolean(s['no-defaults'] ?? s.noDefaults),
    keepHud: Boolean(s['keep-hud'] ?? s.keepHud),
    noIdle: Boolean(s['no-idle'] ?? s.noIdle),
    confirms: Number(s.confirms ?? 0),
    keys: s.keys ? String(s.keys).split(',').map((k) => k.trim()).filter(Boolean) : [],
    battleKeys: s['battle-keys'] ? String(s['battle-keys']).split(',').map((k) => k.trim()).filter(Boolean) : [],
    greet: s.greet,
    script: s.script !== undefined ? String(s.script) : undefined,
    dumpFlags: s['dump-flags'] ?? s.dumpFlags,
    versionFrom:
      s['version-from'] !== undefined || s.versionFrom !== undefined
        ? String(s['version-from'] ?? s.versionFrom)
        : undefined,
    out: path.resolve(s.out ?? (index ? `shot-${index}.png` : 'shot.png')),
    scale: Number(s.scale ?? 4),
    device: s.device ? String(s.device) : undefined,
    wait: s.wait !== undefined ? Number(s.wait) : undefined,
  };
  if (shot.scene === 'world') {
    if (!shot.map || !Number.isFinite(shot.x) || !Number.isFinite(shot.y))
      throw new Error('a world shot needs --map, --x and --y');
    const mapFile = path.join(ROOT, 'public/assets/maps', `${shot.map}.json`);
    if (!fs.existsSync(mapFile)) throw new Error(`no such map: ${shot.map} (${mapFile})`);
  } else if (shot.scene !== 'title') {
    throw new Error(`unknown --scene "${shot.scene}" (world needs --map; or --scene title)`);
  }
  if (!['down', 'up', 'left', 'right'].includes(shot.facing)) throw new Error(`bad --facing ${shot.facing}`);
  if (shot.wait === undefined) shot.wait = shot.battle || shot.trainer ? 2500 : 700;
  return shot;
}

// ---------------------------------------------------------------------------
// Server + browser
// ---------------------------------------------------------------------------

function freePort() {
  return new Promise((resolve, reject) => {
    const srv = net.createServer();
    srv.unref();
    srv.on('error', reject);
    srv.listen(0, '127.0.0.1', () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
  });
}

async function startServer() {
  const port = await freePort();
  const server = await createViteServer({
    root: ROOT,
    configFile: path.join(ROOT, 'vite.config.ts'),
    logLevel: 'error',
    clearScreen: false,
    server: { host: '127.0.0.1', port, strictPort: true, hmr: false, watch: null },
  });
  await server.listen();
  return { server, url: `http://127.0.0.1:${port}/` };
}

const SETTINGS = {
  // plain = full-bleed canvas (no device casing); controls hidden; silent.
  shell: 'plain',
  controlsVisible: false,
  controlSize: 2,
  muted: true,
  musicVolume: 'off',
  sfxVolume: 'off',
  textSpeed: 'instant',
  battlePace: 'swift',
};

// ---------------------------------------------------------------------------
// In-page helpers (run inside the browser)
// ---------------------------------------------------------------------------

/** Wait (polling) until `fn` returns truthy inside the page. */
async function waitFor(page, fn, arg, { timeout = 30000, what = 'condition' } = {}) {
  try {
    await page.waitForFunction(fn, arg, { timeout, polling: 50 });
  } catch (err) {
    const state = await page
      .evaluate(() => {
        const g = window.__pixelkin;
        if (!g) return 'no game';
        const out = { scenes: g.scene.getScenes(true).map((s) => s.scene.key) };
        if (g.scene.isActive('World')) {
          const w = g.scene.getScene('World');
          Object.assign(out, {
            modal: w._modal,
            reveal: !!w.pendingReveal,
            tutorial: !!w.pendingTutorial,
            moving: w.player?.isMoving,
            fading: w.cameras.main.fadeEffect?.isRunning,
            banner: !!w.locationBanner,
            saved: !!w.saveGlyph,
          });
        }
        return out;
      })
      .catch(() => '?');
    throw new Error(`timed out waiting for ${what} (state: ${JSON.stringify(state)})`);
  }
}

const sceneActive = (key) => (k) => {
  const g = window.__pixelkin;
  return !!g && g.scene.isActive(k);
};

/** Tap a key long enough for Phaser's per-frame poll to see it. */
async function tap(page, key, hold = 90) {
  await page.keyboard.down(key);
  await page.waitForTimeout(hold);
  await page.keyboard.up(key);
  await page.waitForTimeout(60);
}

/** True once the world is free-roaming: no modal, no queued reveal/tutorial, no fade. */
function worldIdle() {
  const g = window.__pixelkin;
  if (!g || !g.scene.isActive('World')) return false;
  const w = g.scene.getScene('World');
  if (!w.player || !w.map) return false;
  if (w._modal || w.pendingReveal || w.pendingTutorial) return false;
  if (w.player.isMoving) return false;
  const cam = w.cameras.main;
  if (cam.fadeEffect?.isRunning) return false;
  return true;
}

/** worldIdle + the transient HUD (area-name banner, SAVED glyph) has faded. */
function worldIdleHudClear() {
  const g = window.__pixelkin;
  if (!g || !g.scene.isActive('World')) return false;
  const w = g.scene.getScene('World');
  if (!w.player || !w.map || w._modal || w.pendingReveal || w.pendingTutorial || w.player.isMoving) return false;
  if (w.cameras.main.fadeEffect?.isRunning) return false;
  return !w.locationBanner && !w.saveGlyph;
}

/** Hide DOM shell chrome that can float over the canvas (help link, hints). */
const HIDE_CHROME_CSS = `
  .pk-controls-help, .pk-restore-controls, .pk-rotate-hint, .pk-fs-toggle,
  body > *:not(:has(canvas)):not(script):not(style) { display: none !important; }
`;

// ---------------------------------------------------------------------------
// One shot
// ---------------------------------------------------------------------------

async function seedSave(page, shot) {
  await page.evaluate(async (s) => {
    const { makeStarterKin } = await import('/src/game/content/starters.ts');
    const { CHARTS, chartFlag } = await import('/src/game/content/charts.ts');
    const { SAVE_SCHEMA_VERSION } = await import('/src/game/systems/save/types.ts');
    const { GAME_VERSION } = await import('/src/game/version.ts');

    // Party: "starter" | "none" | "ID[:LV],ID[:LV]".
    let party = [];
    if (s.party === 'starter') party = [makeStarterKin(1, s.level)];
    else if (s.party !== 'none' && s.party !== '')
      party = String(s.party)
        .split(',')
        .map((p) => p.trim())
        .filter(Boolean)
        .map((p) => {
          const [id, lv, hp, status] = p.split(':');
          const kin = makeStarterKin(Number(id), Number(lv ?? s.level));
          if (hp !== undefined && hp !== '') kin.hp = Number(hp); // 0 = fainted
          if (status) kin.status = status; // numb, doze, chill, …
          return kin;
        });

    const flags = {};
    const add = (f) => {
      flags[f.includes(':') ? f : `flag:${f}`] = true;
    };
    if (!s.noDefaults) {
      for (const c of CHARTS) flags[chartFlag(c)] = true; // no "A NEW CHART" reveal
      add('tutorial_offered');
      add('catch_tutorial_seen');
      add('tip_backup_seen');
      // No crown interlude (content/interludes.ts) hijacking a crown-holding shot —
      // unless --no-idle, which exists to shoot one.
      if (!s.noIdle) for (const id of ['south', 'east', 'north', 'west']) add(`interlude_${id}_seen`);
      if (party.length) {
        add('has_starter');
        add('caught_first_kin');
      }
    }
    for (const f of s.flags) add(f);

    const ids = [...new Set(party.map((k) => k.species_id))];
    const save = {
      schema_version: SAVE_SCHEMA_VERSION,
      saved_at: Date.now(),
      play_seconds: 0,
      world: {
        current_map: s.map,
        player: { tx: s.x, ty: s.y, facing: s.facing },
        abilities: s.abilities,
        flags,
        schema_version: SAVE_SCHEMA_VERSION,
      },
      party,
      box: [],
      inventory: {
        items: {
          vesperlamp: 1,
          ...Object.fromEntries(
            (s.items ?? []).map((t) => {
              const [k, n] = t.split(':');
              return [k, Number(n ?? 1)];
            }),
          ),
        },
      },
      money: 500,
      dex: { seen: ids, caught: ids },
      battles_won: 0,
      cooldowns: {},
      // Current version = no "the world has changed" notice; --version-from <v>
      // writes an older one to shoot that notice on purpose ('' = pre-tracking).
      last_version: s.versionFrom ?? GAME_VERSION,
    };
    if (s.versionFrom === '') delete save.last_version;
    // Only slot 1 occupied => CONTINUE drops straight in (no slot picker).
    for (const k of Object.keys(localStorage)) if (k.startsWith('pixelkin:save:')) localStorage.removeItem(k);
    localStorage.setItem('pixelkin:save:slot0', JSON.stringify(save));
  }, shot);
}

async function bootToTitle(page, url) {
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await waitFor(page, sceneActive(), 'Splash', { timeout: 60000, what: 'Splash scene' });
}

async function splashToTitle(page) {
  // Splash: any key unlocks audio and moves on (to Attract).
  await page.waitForTimeout(150);
  await tap(page, 'x');
  await waitFor(page, sceneActive(), 'Attract', { what: 'Attract scene' });
  await page.waitForTimeout(150);
  await tap(page, 'x');
  await waitFor(page, sceneActive(), 'Title', { what: 'Title scene' });
  // Let the fade-in + async slot read + menu build land.
  await waitFor(
    page,
    () => {
      const t = window.__pixelkin.scene.getScene('Title');
      return t && !t.cameras.main.fadeEffect?.isRunning;
    },
    undefined,
    { what: 'Title fade-in' },
  );
  await page.waitForTimeout(400);
}

async function walk(page, dir) {
  const key = { up: 'ArrowUp', down: 'ArrowDown', left: 'ArrowLeft', right: 'ArrowRight' }[dir];
  if (!key) throw new Error(`bad step "${dir}"`);
  const before = await page.evaluate(() => {
    const w = window.__pixelkin.scene.getScene('World');
    return { tx: w.player.tx, ty: w.player.ty, map: w.map.def.id };
  });
  await page.keyboard.down(key);
  // Release as soon as a step starts (or the tile changes), so it's one tile.
  await page
    .waitForFunction(
      (b) => {
        const w = window.__pixelkin.scene.getScene('World');
        return w.player.isMoving || w.player.tx !== b.tx || w.player.ty !== b.ty || w._modal;
      },
      before,
      { timeout: 700, polling: 'raf' },
    )
    .catch(() => {}); // blocked: just a turn
  await page.keyboard.up(key);
  // A step may fire a warp/trigger/encounter: wait for the world to settle again.
  await waitFor(page, worldIdle, undefined, { timeout: 30000, what: `world idle after step ${dir}` }).catch(
    async (e) => {
      // A cutscene/battle opened by the step: report it but keep the frame.
      console.warn(`  ! ${e.message}`);
    },
  );
}

async function shoot(page, url, shot) {
  await bootToTitle(page, url);
  if (shot.scene === 'world') await seedSave(page, shot);
  await splashToTitle(page);

  if (shot.scene === 'title') {
    await page.waitForTimeout(shot.wait);
  } else {
    // Title menu with a seeded save: CONTINUE / NEW GAME / LOAD FILE / SETTINGS —
    // CONTINUE leads and holds the cursor, so just Confirm.
    await tap(page, 'z');
    await waitFor(page, sceneActive(), 'World', { what: 'World scene (CONTINUE)' });
    if (shot.noIdle) {
      // A scene that plays on load (a crown interlude): shoot it as-is, mid-scene.
      await page.waitForTimeout(shot.wait);
      for (let i = 0; i < shot.confirms; i++) {
        await tap(page, 'z');
        await page.waitForTimeout(1400);
      }
    } else if (shot.versionFrom !== undefined) {
      // The "world has changed" narration holds the world modal: shoot it as-is.
      await page.waitForTimeout(1500);
    } else {
      await waitFor(page, worldIdle, undefined, { timeout: 30000, what: 'world idle' });
    }
    for (const key of shot.keys ?? []) {
      await tap(page, key);
      await page.waitForTimeout(300);
    }

    const at = shot.noIdle ? { map: shot.map } : await page.evaluate(() => {
      const w = window.__pixelkin.scene.getScene('World');
      return { map: w.map.def.id, tx: w.player.tx, ty: w.player.ty };
    });
    if (at.map !== shot.map) throw new Error(`landed on ${at.map}, expected ${shot.map}`);

    if (process.env.PROBE_MUSIC) {
      // Debug aid: report the music bed (intro + looping body for a remaster).
      for (const t of [0, Number(process.env.PROBE_MUSIC) || 0]) {
        if (t) await page.waitForTimeout(t);
        const state = await page.evaluate(() =>
          window.__pixelkin.sound.getAllPlaying().map((snd) => ({
            key: snd.key, marker: snd.currentMarker?.name ?? null, loop: snd.loop,
            seek: Math.round(snd.seek * 100) / 100, volume: Math.round(snd.volume * 100) / 100,
          })),
        );
        console.log(`  music @+${t}ms: ${JSON.stringify(state)}`);
      }
    }

    for (const step of shot.steps) await walk(page, step);

    if (shot.greet) {
      await waitFor(page, worldIdleHudClear, undefined, { timeout: 15000, what: 'HUD banner to fade' }).catch((e) =>
        console.warn(`  ! ${e.message}`),
      );
      // Teleport beside the ambient kin's CURRENT tile, face it, Confirm.
      const ok = await page.evaluate(async (pid) => {
        const w = window.__pixelkin.scene.getScene('World');
        const k = w.ambience?.kin?.find((a) => a.placement.id === pid);
        if (!k) return false;
        const sides = [['left', 1, 0], ['right', -1, 0], ['up', 0, 1], ['down', 0, -1]];
        for (const [facing, dx, dy] of sides) {
          const tx = k.tx + dx;
          const ty = k.ty + dy;
          if (!w.playerCanEnter(tx, ty)) continue;
          w.player.tx = tx;
          w.player.ty = ty;
          w.player.sprite.setPosition(tx * 16 + 8, ty * 16 + 16);
          w.player.setFacing(facing);
          void w.interact(); // resolves only once the box closes — don't wait on it
          return true;
        }
        return false;
      }, shot.greet);
      if (!ok) throw new Error(`no ambient kin "${shot.greet}" to greet (or boxed in)`);
      // --confirms N pages on through the greeting (REGISTER note, the event).
      for (let i = 0; i < shot.confirms; i++) {
        await page.waitForTimeout(1400);
        await tap(page, 'z');
      }
    } else if (shot.script) {
      await page.evaluate((ref) => {
        const w = window.__pixelkin.scene.getScene('World');
        w.modal = true;
        void w.playScene([{ op: 'run', ref }]).finally(() => { w.modal = false; w.refreshNpcs(); });
      }, shot.script);
      for (let i = 0; i < shot.confirms; i++) {
        await page.waitForTimeout(1400);
        await tap(page, 'z');
      }
    } else if (shot.trainer) {
      await page.evaluate((id) => {
        const w = window.__pixelkin.scene.getScene('World');
        void w.startBattle({
          kind: 'trainer', trainer: id, party: w.party, box: w.box,
          inventory: w.inventory, dex_caught: [...w.dexCaught],
        });
      }, shot.trainer);
      await waitFor(page, sceneActive(), 'Battle', { what: 'Battle scene' });
      for (let i = 0; i < shot.confirms; i++) {
        await page.waitForTimeout(1400);
        await tap(page, 'z');
      }
    } else if (shot.battle) {
      const [id, lv] = shot.battle.split(':');
      await page.evaluate(
        ({ id, lv }) => {
          const w = window.__pixelkin.scene.getScene('World');
          void w.startBattle({
            kind: 'wild',
            species_id: id,
            level: lv,
            party: w.party,
            box: w.box,
            inventory: w.inventory,
            dex_caught: [...w.dexCaught],
          });
        },
        { id: Number(id), lv: Number(lv ?? shot.level) },
      );
      await waitFor(page, sceneActive(), 'Battle', { what: 'Battle scene' });
      if (shot.battleKeys.length) await page.waitForTimeout(2500); // the send-out beat
      for (const key of shot.battleKeys) {
        await tap(page, key);
        await page.waitForTimeout(400);
      }
    } else if (!shot.keepHud && shot.versionFrom === undefined && !shot.noIdle) {
      await waitFor(page, worldIdleHudClear, undefined, { timeout: 15000, what: 'HUD banner to fade' }).catch((e) =>
        console.warn(`  ! ${e.message}`),
      );
    }
    if (!shot.noIdle) await page.waitForTimeout(shot.wait);
  }

  fs.mkdirSync(path.dirname(shot.out), { recursive: true });
  if (shot.device) {
    // --device: the whole phone page — device shell, controls and all.
    await page.screenshot({ path: shot.out });
  } else {
    await page.addStyleTag({ content: HIDE_CHROME_CSS });
    const canvas = await page.$('#game-root canvas');
    if (!canvas) throw new Error('no game canvas found');
    await canvas.screenshot({ path: shot.out });
  }
  const info =
    shot.scene === 'world'
      ? await page.evaluate(() => {
          const w = window.__pixelkin.scene.getScene('World');
          return `${w.map.def.id} (${w.player.tx},${w.player.ty}) ${w.player.facing}`;
        })
      : 'title';
  if (shot.dumpFlags && shot.scene === 'world') {
    const held = await page.evaluate((pre) => {
      const w = window.__pixelkin.scene.getScene('World');
      const f = w.flags.flags ?? {};
      return Object.keys(f).filter((k) => f[k] === true && k.startsWith(pre)).sort();
    }, String(shot.dumpFlags));
    console.log(`  flags ${shot.dumpFlags}*: ${held.join(' ') || '(none)'}`);
  }
  return info;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || Object.keys(args).length === 0) {
    console.log(USAGE);
    return;
  }

  let specs;
  if (args.batch) {
    const raw = JSON.parse(fs.readFileSync(args.batch, 'utf8'));
    if (!Array.isArray(raw)) throw new Error('--batch file must be a JSON array of shot specs');
    // CLI flags (other than --batch) act as defaults for every spec.
    const { batch, headed, verbose, url, ...defaults } = args;
    specs = raw.map((s, i) => normaliseSpec({ ...defaults, ...s }, i + 1));
  } else {
    specs = [normaliseSpec(args)];
  }

  // Group by scale: the viewport sets the render resolution (one page per scale).
  let server;
  let url = args.url;
  if (!url) {
    ({ server, url } = await startServer());
  }
  const browser = await chromium.launch({
    // PIXELKIN_CHROMIUM: a browser binary to use when the pinned Playwright build
    // isn't installed (cloud sessions ship one at /opt/pw-browsers/chromium).
    ...(process.env.PIXELKIN_CHROMIUM ? { executablePath: process.env.PIXELKIN_CHROMIUM } : {}),
    headless: !args.headed,
    args: ['--mute-audio', '--autoplay-policy=no-user-gesture-required', '--use-gl=angle', '--use-angle=swiftshader'],
  });

  let failures = 0;
  try {
    const pages = new Map();
    const pageFor = async (scale, device) => {
      const key = device ?? scale;
      if (pages.has(key)) return pages.get(key);
      const [dw, dh] = device ? device.split('x').map(Number) : [];
      const ctx = await browser.newContext(device
        ? { viewport: { width: dw, height: dh }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }
        : { viewport: { width: 240 * scale, height: 160 * scale }, deviceScaleFactor: 1 });
      const settings = device ? { ...SETTINGS, shell: 'device', controlsVisible: true } : SETTINGS;
      await ctx.addInitScript((settings) => {
        try {
          localStorage.setItem('pixelkin:settings', JSON.stringify(settings));
        } catch {
          /* ignore */
        }
      }, settings);
      const page = await ctx.newPage();
      page.on('pageerror', (e) => console.warn(`  [pageerror] ${e.message}`));
      if (args.verbose) page.on('console', (m) => console.log(`  [${m.type()}] ${m.text()}`));
      pages.set(key, page);
      return page;
    };

    for (const shot of specs) {
      const t0 = Date.now();
      try {
        const page = await pageFor(shot.scale, shot.device);
        const info = await shoot(page, url, shot);
        console.log(`ok  ${shot.out}  [${info}${shot.battle ? ` battle ${shot.battle}` : ''}] ${Date.now() - t0}ms`);
      } catch (err) {
        failures++;
        console.error(`ERR ${shot.out}: ${err.message}`);
        // Keep whatever is on screen for diagnosis.
        const page = pages.get(shot.device ?? shot.scale);
        const failOut = shot.out.replace(/\.png$/i, '') + '.fail.png';
        if (page) await page.screenshot({ path: failOut }).then(() => console.error(`    see ${failOut}`)).catch(() => {});
      }
    }
  } finally {
    await browser.close();
    if (server) await server.close();
  }
  process.exitCode = failures ? 1 : 0;
}

main().catch((err) => {
  console.error(err.message ?? err);
  process.exit(1);
});
