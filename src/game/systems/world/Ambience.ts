/**
 * Ambience — "every screen moves" (docs/reviews/world-craft-panel.md §3, WP0).
 *
 * One per entered map, owned by WorldScene (built in `enterMap`, destroyed in
 * `teardownMap`). Everything here is VISUAL/aural colour layered over the world —
 * it never touches collision, encounters, triggers, warps or flags — and every
 * piece degrades silently: it is all code-drawn (no art required), a missing sfx
 * stem is silence, a kin sprite that won't load simply isn't shown.
 *
 * What it draws:
 *  - Map-level (from `MapDefinition.ambience`, docs/art-style.md §12b): capped
 *    particles (snow, ash, embers, glowmotes, spores, sea spray, cold motes,
 *    leaves, starglints, dust — ONE shared cap of 40), a drifting mist strip, a
 *    persistent tint, gull flocks + fly-overs, a looped sound bed, and THE
 *    STARFALL STREAK (the game's motif: a falling star crosses the sky every
 *    40–90 s outdoors — cinder blue-grey under the Long Dusk, warm gold after
 *    `flag:dawn`; the `starfall` cutscene op calls one on cue).
 *  - Sprite-keyed tables (the HEAL_ENTRANCE_MAPS pattern, no map edit needed):
 *    LIGHT_SOURCES (lamp/brazier → a soft flickering pool on the ground, below
 *    actors and above the ground, plus a halo at the flame) and CHIMNEYS
 *    (building → rising smoke puffs).
 *  - Per-actor FOLLOWERS, attached from outside so the entity classes stay
 *    untouched: a drop shadow (shrinks through a hop), the tall-grass LEGS
 *    overlay (the real grass tile re-drawn over the bottom of the actor), the
 *    grass rustle + leaf fleck, an item-cache glint, an NPC breathing bob and the
 *    player's idle glance.
 *  - AMBIENT KIN (`NpcPlacement.ambient`): overworld kin that graze near their
 *    post, never collide, never interact, and hop away when you come within 2.
 *  - One-shot beats WorldScene calls: footprints, the encounter tell, the
 *    door-open beat, a pickup puff, ledge-hop dust.
 *
 * Settings → "Ambient motion: Off" (preferences.getAmbientMotion, read live)
 * stills particles, mist drift, streaks, birds, smoke, flicker, flecks and bob.
 */
import Phaser from 'phaser';
import { GAME_HEIGHT, GAME_WIDTH, TILE_SIZE } from '@game/config';
import { getAmbientMotion, sfxMasterGain } from '@game/ui/preferences';
import type { RuntimeMap } from './MapLoader';
import { ensureTileFrame } from './MapRenderer';
import { loadAudio } from '@game/systems/audio/loadAudio';
import { creatureTextureKey, loadCreatureSprite } from '@game/systems/sprites/CreatureSprites';
import type { Actor } from '@game/entities/Actor';
import type {
  AmbienceParticleKind,
  AmbienceParticles,
  Facing,
  MapAmbience,
  MapObject,
  NpcPlacement,
  TileCoord,
} from '@game/data/world/types';

// ---------------------------------------------------------------- tables --

/**
 * Light sources keyed by object sprite: the flame's px offset inside the sprite
 * (`hx`,`hy`), the pool radius on the ground and its colour. Add a row and every
 * map with that object glows — no per-map art or JSON edit.
 */
export const LIGHT_SOURCES: Record<string, { hx: number; hy: number; radius: number; color: number }> = {
  tinderwick_lamp_post: { hx: 8, hy: 8, radius: 16, color: 0xffc46b },
  penumbra_way_lamp: { hx: 8, hy: 8, radius: 15, color: 0xffd089 },
  interior_brazier: { hx: 8, hy: 8, radius: 13, color: 0xff9a4a },
  hourfold_brazier_lit: { hx: 16, hy: 12, radius: 18, color: 0xff9a4a },
  solarium_brazier_lit: { hx: 16, hy: 12, radius: 18, color: 0xffd76b },
  pale_vault_brazier: { hx: 16, hy: 10, radius: 18, color: 0x9fe7ff },
  saltreach_reed_lantern_lit: { hx: 8, hy: 6, radius: 12, color: 0xffd089 },
  nightreach_watch_lamp_lit: { hx: 16, hy: 8, radius: 17, color: 0xdfe6ff },
  nightreach_vigil_lamp: { hx: 8, hy: 6, radius: 12, color: 0xdfe6ff },
  tideglass_wrecklamp_lit: { hx: 8, hy: 8, radius: 12, color: 0x9fe7ff },
  // north
  pale_vault_ice_lantern: { hx: 8, hy: 9, radius: 12, color: 0x9fe7ff },
  windward_wind_shrine: { hx: 16, hy: 18, radius: 9, color: 0xffc46b },
};

/** Chimney tops keyed by building sprite (px offset of the stack's mouth). */
export const CHIMNEYS: Record<string, { x: number; y: number }> = {
  tinderwick_cottage: { x: 56, y: 2 },
  tinderwick_shop: { x: 61, y: 2 },
  pearlmoor_inn: { x: 60, y: 2 },
  vesper_crossroads_inn: { x: 58, y: 6 },
  // north
  pale_vault_home: { x: 20, y: 14 },
  galehigh_cottage: { x: 22, y: 34 },
};

/** Map kinds that are "under the sky" (the starfall default + bird fly-overs). */
const OUTDOOR_KINDS = new Set(['town', 'route', 'hub', 'water']);

/** Surfaces that keep a footprint under `footprints: 'auto'`. */
const PRINT_SURFACES = new Set(['sand', 'trail', 'dunegrass', 'snowpatch', 'snowtrail']);

/** Hard cap across every emitter on the map. */
const PARTICLE_CAP = 40;
const PRINT_CAP = 12;
const PRINT_FADE_MS = 3600;

const DEPTH = {
  print: 6, // above deco (5), below objects (9) and actors (10)
  pool: 8,
  doorway: 9.5,
  halo: 21.5, // over the object overhang band (21)
  smoke: 22,
  particles: 23,
  streak: 23.6,
  mist: 23.4,
  tint: 24,
  birds: 23.2,
} as const;

// A world-feel palette (not UI chrome — theme.ts tokens are for screens).
const STREAK = {
  dusk: { trail: 0x9aa8cc, head: 0xf4f8ff }, // cold cinder, the Long Dusk
  dawn: { trail: 0xffb347, head: 0xfff3c0 }, // the Starfall mirror after flag:dawn
};
const LEAF_FLECK = [0x7bdc6b, 0x4a9a55, 0x9fd36b];

interface KindSpec {
  base: number;
  colors: number[];
  fall?: boolean; // spawn at the top edge (weather)
  vx: [number, number];
  vy: [number, number];
  sway?: number;
  gravity?: number;
  life: [number, number];
  size?: [number, number]; // w,h px
  alpha?: number;
  flicker?: boolean;
  glint?: boolean;
}

const KINDS: Record<AmbienceParticleKind, KindSpec> = {
  snow: { base: 30, colors: [0xf4f6ff, 0xdfe8f5, 0xffffff], fall: true, vx: [-4, 2], vy: [9, 17], sway: 6, life: [10, 14] },
  ash: { base: 22, colors: [0x9a96a3, 0x7d7886, 0xb9b3c9], fall: true, vx: [-5, 5], vy: [4, 9], sway: 4, life: [10, 14], alpha: 0.8 },
  embers: { base: 14, colors: [0xff8a3d, 0xffc06b, 0xff5a3a], vx: [-3, 3], vy: [-14, -6], sway: 3, life: [1.5, 3.5], flicker: true },
  glowmotes: { base: 16, colors: [0xc8f27b, 0xf4e27a, 0x9fe7ff], vx: [-3, 3], vy: [-3, 2], sway: 2, life: [3, 6], flicker: true },
  spores: { base: 16, colors: [0xe8b8e0, 0xf2dcf0, 0xc9a6e6], vx: [-2, 2], vy: [-4, -1], sway: 3, life: [4, 7], alpha: 0.85 },
  spray: { base: 14, colors: [0xffffff, 0xd8f0ff, 0xa9d8f0], vx: [-6, 6], vy: [-24, -12], gravity: 44, life: [0.5, 0.9] },
  motes: { base: 18, colors: [0xb8c8e8, 0xd0dcf0], vx: [2, 6], vy: [-1, 1], sway: 2, life: [5, 8], alpha: 0.7 },
  leaves: { base: 8, colors: [0xd98a3a, 0xb8642e, 0x7bbf5a], fall: true, vx: [-4, 4], vy: [8, 14], sway: 10, life: [10, 14], size: [2, 1] },
  starglint: { base: 10, colors: [0xfff3c0, 0xcfe0ff], vx: [0, 0], vy: [0, 0], life: [0.8, 1.4], glint: true },
  dust: { base: 12, colors: [0xe8dcc0, 0xcdbf9e], vx: [-1.5, 1.5], vy: [-1, 1], sway: 1, life: [4, 8], alpha: 0.5 },
};

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  age: number;
  life: number;
  color: number;
  w: number;
  h: number;
  phase: number;
  spec: KindSpec;
  emitter: number;
}

interface Emitter {
  cfg: AmbienceParticles;
  spec: KindSpec;
  target: number;
  alive: number;
}

/** What the host scene lends the ambience (kept narrow, so Ambience never reaches into WorldScene). */
export interface AmbienceHost {
  /** Is this world flag held? (starfall colour, flag-gated objects) */
  flag(flag: string): boolean;
  /** Walkable on foot, no Gifts (ambient kin keep to real ground). */
  walkable(tx: number, ty: number): boolean;
  /** Is an object currently shown (flag-gated set dressing)? */
  objectVisible(obj: MapObject): boolean;
  /** Is this sfx stem rendered? (a sound bed that isn't yet is silence, not a 404) */
  hasSfx(stem: string): boolean;
}

/** Per-actor follower state. */
interface Follow {
  actor: Actor;
  kind: 'player' | 'npc' | 'kin' | 'cache';
  shadow?: Phaser.GameObjects.Ellipse;
  legs?: Phaser.GameObjects.Image;
  legsGid: number;
  rustleUntil: number;
  hop?: { start: number; ms: number; fromY: number; toY: number };
  nextGlint: number;
  nextBob: number;
  bobUntil: number;
  // player idle glance
  idleSince: number;
  lastKey: string;
  glance?: { original: Facing; steps: Facing[]; nextAt: number };
}

const SHADOW_W = 13;
const LEGS_H = 6;

const rand = (a: number, b: number): number => a + Math.random() * (b - a);
const pick = <T>(xs: readonly T[]): T => xs[Math.floor(Math.random() * xs.length)];

function groundYOf(_tx: number, ty: number): number {
  return ty * TILE_SIZE + TILE_SIZE;
}

// ------------------------------------------------------------- ambient kin --

/** Ambient (wild, grazing) kin draw at this fraction of their 32px overworld view. */
const AMBIENT_KIN_SCALE = 0.7;

/** The kin id behind an ambient sprite key (`kin_<id>_overworld`), or null. */
function ambientKinId(sprite: string): number | null {
  const m = /^kin_(\d+)_overworld$/.exec(sprite);
  return m ? Number(m[1]) : null;
}

class AmbientKin {
  readonly sprite: Phaser.GameObjects.Image;
  readonly shadow: Phaser.GameObjects.Ellipse;
  tx: number;
  ty: number;
  private busy = false;
  private nextAt: number;
  private calmAt = 0;
  private readonly radius: number;

  constructor(
    private readonly scene: Phaser.Scene,
    readonly placement: NpcPlacement,
    private readonly ok: (tx: number, ty: number) => boolean,
  ) {
    this.tx = placement.at.tx;
    this.ty = placement.at.ty;
    this.radius = Math.max(0, placement.wander_radius ?? 2);
    const x = this.tx * TILE_SIZE + TILE_SIZE / 2;
    const y = groundYOf(this.tx, this.ty);
    this.shadow = scene.add.ellipse(x, y - 0.5, 13, 4, 0x000000, 0.3).setVisible(false);
    // Hidden until the kin's packed view lands — a missing sprite is simply absent.
    // Drawn at AMBIENT_KIN_SCALE: the 32px overworld view is sized for a kin
    // standing in for a person; a grazing wild kin should read smaller than the
    // ~28px player (the pilot's full-size Brinelet towered over them).
    this.sprite = scene.add.image(x, y, '__MISSING').setOrigin(0.5, 1).setVisible(false)
      .setScale(AMBIENT_KIN_SCALE);
    this.nextAt = scene.time.now + rand(1200, 3500);
    const id = ambientKinId(placement.sprite);
    if (id === null) return;
    const key = creatureTextureKey(id, 'overworld');
    const show = (k: string | null): void => {
      if (!k || !this.sprite.active) return;
      this.sprite.setTexture(k).setVisible(true);
      this.shadow.setVisible(true);
    };
    if (scene.textures.exists(key)) show(key);
    else void loadCreatureSprite(scene, id, 'overworld').then(show);
  }

  private inLeash(tx: number, ty: number): boolean {
    const { at } = this.placement;
    return Math.max(Math.abs(tx - at.tx), Math.abs(ty - at.ty)) <= this.radius;
  }

  /** Hop to (tx,ty) — a little arc. Pure tween; nothing collides with an ambient kin. */
  private hopTo(tx: number, ty: number, ms: number, lift: number): void {
    this.busy = true;
    const fx = this.sprite.x;
    const fy = this.sprite.y;
    const toX = tx * TILE_SIZE + TILE_SIZE / 2;
    const toY = groundYOf(tx, ty);
    if (toX !== fx) this.sprite.setFlipX(toX > fx);
    this.tx = tx;
    this.ty = ty;
    this.scene.tweens.addCounter({
      from: 0,
      to: 1,
      duration: ms,
      onUpdate: (tw) => {
        const t = tw.getValue() ?? 0;
        const gx = fx + (toX - fx) * t;
        const gy = fy + (toY - fy) * t;
        this.sprite.setPosition(gx, gy - lift * 4 * t * (1 - t));
        this.shadow.setPosition(gx, gy - 0.5).setScale(1 - 0.35 * 4 * t * (1 - t));
      },
      onComplete: () => {
        this.sprite.setPosition(toX, toY);
        this.shadow.setPosition(toX, toY - 0.5).setScale(1);
        this.busy = false;
      },
    });
  }

  update(time: number, player: { tx: number; ty: number } | undefined, motion: boolean): void {
    this.sprite.setDepth(10 + this.sprite.y * 0.001);
    this.shadow.setDepth(this.sprite.depth - 0.0002);
    if (this.busy || !this.sprite.visible) return;
    // Spooked: the player came within 2 tiles — hop to the farthest leashed tile.
    if (player && time >= this.calmAt) {
      const d = Math.abs(player.tx - this.tx) + Math.abs(player.ty - this.ty);
      if (d <= 2) {
        let best: TileCoord | undefined;
        let bestD = d;
        for (let dy = -2; dy <= 2; dy++) {
          for (let dx = -2; dx <= 2; dx++) {
            const nx = this.tx + dx;
            const ny = this.ty + dy;
            if (!this.inLeash(nx, ny) || !this.ok(nx, ny)) continue;
            if (nx === player.tx && ny === player.ty) continue;
            const nd = Math.abs(player.tx - nx) + Math.abs(player.ty - ny);
            if (nd > bestD) {
              bestD = nd;
              best = { tx: nx, ty: ny };
            }
          }
        }
        this.calmAt = time + 1100;
        this.nextAt = time + rand(2500, 4500);
        if (best) this.hopTo(best.tx, best.ty, 280, motion ? 6 : 0);
        else this.hopTo(this.tx, this.ty, 240, motion ? 5 : 0); // cornered: a startled hop in place
        return;
      }
    }
    if (time < this.nextAt) return;
    this.nextAt = time + rand(2200, 5200);
    if (!motion) return;
    // Graze: a small step-hop to a neighbouring leashed tile, or just a little bounce.
    const dirs: [number, number][] = [
      [1, 0],
      [-1, 0],
      [0, 1],
      [0, -1],
    ];
    const [dx, dy] = pick(dirs);
    const nx = this.tx + dx;
    const ny = this.ty + dy;
    const blockedByPlayer = player && player.tx === nx && player.ty === ny;
    if (this.inLeash(nx, ny) && this.ok(nx, ny) && !blockedByPlayer) this.hopTo(nx, ny, 360, 2);
    else this.hopTo(this.tx, this.ty, 220, 2);
  }

  destroy(): void {
    this.sprite.destroy();
    this.shadow.destroy();
  }
}

// ------------------------------------------------------------------ class --

export class Ambience {
  private readonly cfg: MapAmbience;
  private readonly outdoor: boolean;
  private readonly follows: Follow[] = [];
  private readonly kin: AmbientKin[] = [];
  private readonly lights: {
    obj?: MapObject;
    pool: Phaser.GameObjects.Graphics;
    halo?: Phaser.GameObjects.Arc;
    base: number;
    seed: number;
  }[] = [];
  private readonly chimneys: { x: number; y: number; obj: MapObject; nextAt: number }[] = [];
  private readonly prints: Phaser.GameObjects.Graphics[] = [];
  private readonly transients = new Set<Phaser.GameObjects.GameObject>();

  private readonly particles: Particle[] = [];
  private readonly emitters: Emitter[] = [];
  private particleGfx?: Phaser.GameObjects.Graphics;
  private shoreTiles: TileCoord[] = [];

  private mist?: Phaser.GameObjects.TileSprite;
  private mistSpeed = 4;
  private tintRect?: Phaser.GameObjects.Rectangle;

  private streakGfx?: Phaser.GameObjects.Graphics;
  private streakBusy = false;
  private nextStreakAt = Number.POSITIVE_INFINITY;
  private streakMin = 40;
  private streakMax = 90;

  private flocks: { tx: number; ty: number; birds: Phaser.GameObjects.Image[]; gone: boolean; backAt: number }[] = [];
  private nextFlyoverAt = Number.POSITIVE_INFINITY;
  private bed?: Phaser.Sound.BaseSound;
  private destroyed = false;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly map: RuntimeMap,
    private readonly host: AmbienceHost,
  ) {
    this.cfg = map.def.ambience ?? {};
    this.outdoor = OUTDOOR_KINDS.has(map.def.kind);
    const now = scene.time.now;

    this.buildLights();
    this.buildChimneys(now);

    // Particles
    for (const p of this.cfg.particles ?? []) {
      const spec = KINDS[p.kind];
      if (!spec) continue;
      const density = Phaser.Math.Clamp(p.density ?? 1, 0, 1);
      this.emitters.push({ cfg: p, spec, target: Math.round(spec.base * density), alive: 0 });
    }
    if (this.emitters.some((e) => (e.cfg.area ?? (e.cfg.kind === 'spray' ? 'water_edge' : 'screen')) === 'water_edge')) {
      this.shoreTiles = this.findShore();
    }
    if (this.emitters.length) this.particleGfx = scene.add.graphics().setDepth(DEPTH.particles);

    if (this.cfg.mist) this.buildMist(this.cfg.mist);
    if (this.cfg.tint) {
      const c = Phaser.Display.Color.HexStringToColor(this.cfg.tint.color).color;
      this.tintRect = scene.add
        .rectangle(-40, -40, GAME_WIDTH + 80, GAME_HEIGHT + 80, c, Phaser.Math.Clamp(this.cfg.tint.alpha, 0, 0.6))
        .setOrigin(0, 0)
        .setScrollFactor(0)
        .setDepth(DEPTH.tint);
    }

    // Starfall: outdoors by default; opt out with `starfall: false`.
    const sf = this.cfg.starfall;
    const on = sf === undefined ? this.outdoor : sf !== false;
    if (on) {
      if (typeof sf === 'object') {
        this.streakMin = Math.max(20, sf.min_s ?? this.streakMin);
        this.streakMax = Math.max(this.streakMin, sf.max_s ?? this.streakMax);
      }
      this.nextStreakAt = now + rand(this.streakMin, this.streakMax) * 1000;
    }
    // Dev-only screenshot hook: `?starfall_dev=<ms>` fires a streak every <ms>
    // (bypasses the 20 s floor) so the harness can catch one mid-flight.
    if (import.meta.env.DEV && typeof window !== 'undefined') {
      const dev = Number(new URLSearchParams(window.location.search).get('starfall_dev'));
      if (dev > 0) {
        this.streakMin = this.streakMax = dev / 1000;
        this.nextStreakAt = now + dev;
      }
    }

    if (this.cfg.birds) {
      ensureBirdTexture(scene);
      for (const at of this.cfg.birds.flocks ?? []) this.flocks.push(this.buildFlock(at));
      if (this.cfg.birds.flyover !== false && this.outdoor) this.nextFlyoverAt = now + rand(12000, 30000);
    }

    if (this.cfg.sound_bed) void this.startBed(this.cfg.sound_bed);
  }

  // ---------------------------------------------------------------- lights --

  private buildLights(): void {
    for (const obj of this.map.def.objects ?? []) {
      const ls = LIGHT_SOURCES[obj.sprite];
      if (!ls) continue;
      const fx = obj.at.tx * TILE_SIZE + ls.hx;
      const fy = obj.at.ty * TILE_SIZE + ls.hy;
      const groundY = (obj.at.ty + obj.h) * TILE_SIZE - 4;
      this.addLight(fx, groundY, ls.radius, ls.color, obj, { x: fx, y: fy });
    }
    for (const extra of this.cfg.light_sources_extra ?? []) {
      const c = extra.color ? Phaser.Display.Color.HexStringToColor(extra.color).color : 0xffc46b;
      this.addLight(
        extra.at.tx * TILE_SIZE + TILE_SIZE / 2,
        extra.at.ty * TILE_SIZE + TILE_SIZE / 2,
        extra.radius ?? 14,
        c,
      );
    }
    this.refreshLights();
  }

  /** A stepped, additive pool of light on the ground (3 rings → a pixel glow). */
  private addLight(x: number, y: number, radius: number, color: number, obj?: MapObject, head?: { x: number; y: number }): void {
    const pool = this.scene.add.graphics().setDepth(DEPTH.pool).setBlendMode(Phaser.BlendModes.ADD);
    const rings = [1, 0.72, 0.44];
    for (const k of rings) {
      pool.fillStyle(color, 0.075);
      pool.fillEllipse(x, y, radius * 2 * k, radius * k);
    }
    const halo = head
      ? this.scene.add.circle(head.x, head.y, 5, color, 0.22).setDepth(DEPTH.halo).setBlendMode(Phaser.BlendModes.ADD)
      : undefined;
    this.lights.push({ obj, pool, halo, base: 1, seed: Math.random() * 1000 });
  }

  /** Follow flag-gated objects (a lit/dark lantern swap pair): only shown objects glow. */
  refreshLights(): void {
    for (const l of this.lights) {
      const vis = !l.obj || this.host.objectVisible(l.obj);
      l.pool.setVisible(vis);
      l.halo?.setVisible(vis);
    }
  }

  // -------------------------------------------------------------- chimneys --

  private buildChimneys(now: number): void {
    for (const obj of this.map.def.objects ?? []) {
      const c = CHIMNEYS[obj.sprite];
      if (!c) continue;
      this.chimneys.push({
        x: obj.at.tx * TILE_SIZE + c.x,
        y: obj.at.ty * TILE_SIZE + c.y,
        obj,
        nextAt: now + rand(0, 900),
      });
    }
  }

  private puffSmoke(x: number, y: number): void {
    const p = this.scene.add.circle(x, y, 1.5, 0xb9b3c9, 0.42).setDepth(DEPTH.smoke);
    this.track(p);
    this.scene.tweens.add({
      targets: p,
      y: y - rand(12, 16),
      x: x + rand(2, 6),
      scale: 2.1,
      alpha: 0,
      duration: rand(1900, 2500),
      ease: 'Sine.out',
      onComplete: () => this.untrack(p),
    });
  }

  // ------------------------------------------------------------- particles --

  private findShore(): TileCoord[] {
    const out: TileCoord[] = [];
    const { width, height } = this.map;
    for (let ty = 0; ty < height; ty++) {
      for (let tx = 0; tx < width; tx++) {
        if (!this.map.hasTerrainAt(tx, ty, 'water') && this.map.surfaceAt(tx, ty) !== 'water') continue;
        const dry = [
          [1, 0],
          [-1, 0],
          [0, 1],
          [0, -1],
        ].some(([dx, dy]) => {
          const nx = tx + dx;
          const ny = ty + dy;
          return this.map.inBounds(nx, ny) && this.map.surfaceAt(nx, ny) !== 'water' && !this.map.hasTerrainAt(nx, ny, 'water');
        });
        if (dry) out.push({ tx, ty });
      }
    }
    return out;
  }

  private spawn(e: Emitter, idx: number, view: Phaser.Geom.Rectangle, initial: boolean): boolean {
    const s = e.spec;
    let x: number;
    let y: number;
    const area = e.cfg.area ?? (e.cfg.kind === 'spray' ? 'water_edge' : 'screen');
    if (area === 'water_edge') {
      const inView = this.shoreTiles.filter(
        (t) =>
          t.tx * TILE_SIZE >= view.x - TILE_SIZE &&
          t.tx * TILE_SIZE <= view.right &&
          t.ty * TILE_SIZE >= view.y - TILE_SIZE &&
          t.ty * TILE_SIZE <= view.bottom,
      );
      if (!inView.length) return false;
      const t = pick(inView);
      x = t.tx * TILE_SIZE + rand(2, 14);
      y = t.ty * TILE_SIZE + rand(4, 12);
    } else if (area === 'screen') {
      x = rand(view.x - 8, view.right + 8);
      y = s.fall && !initial ? view.y - rand(2, 10) : rand(view.y, view.bottom);
    } else {
      const r = area;
      const rx = r.tx * TILE_SIZE;
      const ry = r.ty * TILE_SIZE;
      const rw = r.w * TILE_SIZE;
      const rh = r.h * TILE_SIZE;
      if (rx > view.right || rx + rw < view.x || ry > view.bottom || ry + rh < view.y) return false;
      x = rand(rx, rx + rw);
      y = s.fall && !initial ? ry : rand(ry, ry + rh);
    }
    const [w, h] = s.size ?? (Math.random() < 0.2 ? [2, 2] : [1, 1]);
    this.particles.push({
      x,
      y,
      vx: rand(s.vx[0], s.vx[1]),
      vy: rand(s.vy[0], s.vy[1]),
      age: initial && s.fall ? rand(0, s.life[0] * 0.5) : 0,
      life: rand(s.life[0], s.life[1]),
      color: pick(s.colors),
      w,
      h,
      phase: Math.random() * Math.PI * 2,
      spec: s,
      emitter: idx,
    });
    e.alive++;
    return true;
  }

  private tickParticles(dt: number, view: Phaser.Geom.Rectangle, motion: boolean): void {
    const g = this.particleGfx;
    if (!g) return;
    g.clear();
    if (!motion) {
      if (this.particles.length) {
        this.particles.length = 0;
        for (const e of this.emitters) e.alive = 0;
      }
      return;
    }
    // Top up each emitter (2 per frame at most), honouring the global cap.
    for (let i = 0; i < this.emitters.length; i++) {
      const e = this.emitters[i];
      for (let n = 0; n < 2 && e.alive < e.target && this.particles.length < PARTICLE_CAP; n++) {
        if (!this.spawn(e, i, view, this.particles.length === 0 && n === 0 && e.alive === 0)) break;
      }
    }
    const margin = 24;
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      const s = p.spec;
      p.age += dt;
      if (s.gravity) p.vy += s.gravity * dt;
      p.x += (p.vx + (s.sway ? Math.sin(p.age * 1.7 + p.phase) * s.sway * 0.5 : 0)) * dt;
      p.y += p.vy * dt;
      const out =
        p.x < view.x - margin || p.x > view.right + margin || p.y < view.y - margin || p.y > view.bottom + margin;
      if (p.age >= p.life || out) {
        this.particles.splice(i, 1);
        this.emitters[p.emitter].alive--;
        continue;
      }
      let a = Math.min(1, p.age / 0.4, (p.life - p.age) / 0.5) * (s.alpha ?? 1);
      if (s.flicker) a *= 0.65 + 0.35 * Math.sin(p.age * 9 + p.phase);
      if (a <= 0.02) continue;
      const x = Math.round(p.x);
      const y = Math.round(p.y);
      g.fillStyle(p.color, a);
      if (s.glint) {
        // a twinkle: a dot that blooms into a tiny + at its peak
        const peak = Math.sin((p.age / p.life) * Math.PI);
        g.fillRect(x, y, 1, 1);
        if (peak > 0.6) {
          g.fillStyle(p.color, a * 0.7);
          g.fillRect(x - 1, y, 3, 1);
          g.fillRect(x, y - 1, 1, 3);
        }
      } else {
        g.fillRect(x, y, p.w, p.h);
      }
    }
  }

  // ------------------------------------------------------------------ mist --

  private buildMist(m: NonNullable<MapAmbience['mist']>): void {
    const key = 'amb_mist';
    if (!this.scene.textures.exists(key)) {
      const w = 96;
      const h = 64;
      const canvas = this.scene.textures.createCanvas(key, w, h);
      const ctx = canvas?.getContext();
      if (!canvas || !ctx) return;
      // Soft blobs, wrapped on both axes so the tile scroll never shows a seam.
      for (let i = 0; i < 26; i++) {
        const cx = Math.random() * w;
        const cy = Math.random() * h;
        const r = 6 + Math.random() * 14;
        for (const ox of [-w, 0, w]) {
          for (const oy of [-h, 0, h]) {
            const grad = ctx.createRadialGradient(cx + ox, cy + oy, 0, cx + ox, cy + oy, r);
            grad.addColorStop(0, 'rgba(255,255,255,0.55)');
            grad.addColorStop(1, 'rgba(255,255,255,0)');
            ctx.fillStyle = grad;
            ctx.fillRect(cx + ox - r, cy + oy - r, r * 2, r * 2);
          }
        }
      }
      canvas.refresh();
    }
    const color = m.color ? Phaser.Display.Color.HexStringToColor(m.color).color : 0xdfe6f5;
    this.mistSpeed = m.speed ?? 4;
    this.mist = this.scene.add
      .tileSprite(0, 0, GAME_WIDTH, GAME_HEIGHT, key)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setTileScale(2.5, 2.5)
      .setTint(color)
      .setAlpha(Phaser.Math.Clamp(m.alpha ?? 0.22, 0, 0.6))
      .setDepth(DEPTH.mist);
  }

  // -------------------------------------------------------------- starfall --

  /**
   * A falling star crosses the sky: a 1px line with a glowing head — cold cinder
   * blue-grey under the Long Dusk, warm gold once `flag:dawn` is held (the
   * Starfall mirror). Resolves when it has burned out. No-op (resolves at once)
   * with ambient motion off, or while another streak is still falling.
   */
  starfall(opts: { from?: 'left' | 'right' } = {}): Promise<void> {
    if (this.destroyed || this.streakBusy || !getAmbientMotion()) return Promise.resolve();
    this.streakBusy = true;
    const g = (this.streakGfx ??= this.scene.add.graphics().setScrollFactor(0).setDepth(DEPTH.streak));
    const dawn = this.host.flag('flag:dawn');
    const pal = dawn ? STREAK.dawn : STREAK.dusk;
    const fromLeft = opts.from ? opts.from === 'left' : Math.random() < 0.5;
    const sx = fromLeft ? rand(24, 120) : rand(120, 216);
    const sy = rand(6, 34);
    const dir = fromLeft ? 1 : -1;
    const len = rand(110, 160);
    const ang = rand(0.32, 0.5); // radians below horizontal (stays in the upper sky)
    const dx = Math.cos(ang) * len * dir;
    const dy = Math.sin(ang) * len;
    const travel = rand(900, 1250);
    const fade = 260;
    return new Promise((resolve) => {
      this.scene.tweens.addCounter({
        from: 0,
        to: 1,
        duration: travel + fade,
        onUpdate: (tw) => {
          if (this.destroyed) return;
          const ms = (tw.getValue() ?? 0) * (travel + fade);
          const t = Math.min(1, ms / travel);
          const e = 1 - (1 - t) * (1 - t); // ease-out: it slows as it burns
          const fadeA = ms > travel ? 1 - (ms - travel) / fade : 1;
          const hx = sx + dx * e;
          const hy = sy + dy * e;
          g.clear();
          // The game's signature motif: it must be unmistakable at a glance, so a
          // long tapering tail, a bright 3px head with a soft halo, and a few
          // sparks shed behind it (deterministic per segment — no flicker noise).
          const segs = 14;
          const tail = Math.min(e, 0.6);
          for (let i = 0; i < segs; i++) {
            const a0 = e - (tail * i) / segs;
            const a1 = e - (tail * (i + 1)) / segs;
            if (a1 < 0) break;
            const w = i < 2 ? 2.5 : i < 5 ? 2 : i < 9 ? 1.5 : 1;
            g.lineStyle(w, i < 3 ? pal.head : pal.trail, (1 - i / segs) * fadeA);
            g.lineBetween(sx + dx * a0, sy + dy * a0, sx + dx * a1, sy + dy * a1);
          }
          for (let k = 1; k <= 4; k++) {
            const a = e - tail * (k / 5);
            if (a < 0) break;
            const off = ((k * 37) % 5) - 2;
            g.fillStyle(pal.head, (0.7 - k * 0.12) * fadeA);
            g.fillRect(Math.round(sx + dx * a) + off, Math.round(sy + dy * a) + 2, 1, 1);
          }
          g.fillStyle(pal.trail, 0.28 * fadeA);
          g.fillCircle(hx, hy, 4.5);
          g.fillStyle(pal.head, 0.55 * fadeA);
          g.fillCircle(hx, hy, 2.5);
          g.fillStyle(pal.head, fadeA);
          g.fillRect(Math.round(hx) - 1, Math.round(hy) - 1, 3, 3);
        },
        onComplete: () => {
          g.clear();
          this.streakBusy = false;
          resolve();
        },
      });
    });
  }

  // ----------------------------------------------------------------- birds --

  private buildFlock(at: TileCoord): { tx: number; ty: number; birds: Phaser.GameObjects.Image[]; gone: boolean; backAt: number } {
    const birds: Phaser.GameObjects.Image[] = [];
    const n = 3 + Math.floor(Math.random() * 3);
    const frame = this.cfg.birds?.kind === 'bird' ? 'bird_0' : 'gull_0';
    for (let i = 0; i < n; i++) {
      const b = this.scene.add
        .image(at.tx * TILE_SIZE + rand(0, 22), at.ty * TILE_SIZE + rand(4, 14), 'amb_birds', frame)
        .setDepth(DEPTH.print + 0.5)
        .setFlipX(Math.random() < 0.5);
      birds.push(b);
    }
    return { tx: at.tx, ty: at.ty, birds, gone: false, backAt: 0 };
  }

  private liftFlock(f: { birds: Phaser.GameObjects.Image[]; gone: boolean; backAt: number }, awayX: number): void {
    f.gone = true;
    f.backAt = this.scene.time.now + 20000;
    const kind = this.cfg.birds?.kind === 'bird' ? 'bird' : 'gull';
    for (const b of f.birds) {
      b.setDepth(DEPTH.birds);
      const flap = this.scene.time.addEvent({
        delay: 110,
        loop: true,
        callback: () => b.setFrame(b.frame.name === `${kind}_0` ? `${kind}_1` : `${kind}_0`),
      });
      const dir = awayX >= 0 ? 1 : -1;
      b.setFlipX(dir > 0);
      this.scene.tweens.add({
        targets: b,
        x: b.x + dir * rand(90, 140),
        y: b.y - rand(70, 110),
        alpha: 0,
        delay: rand(0, 220),
        duration: rand(1300, 1800),
        ease: 'Sine.in',
        onComplete: () => {
          flap.remove();
          b.setVisible(false);
        },
      });
    }
  }

  private flyover(view: Phaser.Geom.Rectangle): void {
    const kind = this.cfg.birds?.kind === 'bird' ? 'bird' : 'gull';
    const ltr = Math.random() < 0.5;
    const y = rand(view.y + 10, view.y + view.height * 0.55);
    const b = this.scene.add
      .image(ltr ? view.x - 8 : view.right + 8, y, 'amb_birds', `${kind}_0`)
      .setDepth(DEPTH.birds)
      .setFlipX(ltr);
    this.track(b);
    const flap = this.scene.time.addEvent({
      delay: 140,
      loop: true,
      callback: () => b.active && b.setFrame(b.frame.name === `${kind}_0` ? `${kind}_1` : `${kind}_0`),
    });
    this.scene.tweens.add({
      targets: b,
      x: ltr ? view.right + 12 : view.x - 12,
      y: y + rand(-20, 12),
      duration: rand(4200, 6000),
      onComplete: () => {
        flap.remove();
        this.untrack(b);
      },
    });
  }

  // ------------------------------------------------------------- sound bed --

  private async startBed(stem: string): Promise<void> {
    const gain = sfxMasterGain();
    if (gain <= 0 || !this.host.hasSfx(stem)) return;
    const ok = await loadAudio(this.scene, stem, `assets/audio/sfx/${stem}.mp3`);
    if (!ok || this.destroyed) return;
    try {
      this.bed = this.scene.sound.add(stem, { loop: true, volume: 0.22 * gain });
      this.bed.play();
    } catch {
      this.bed = undefined; // a missing/undecodable bed is silence
    }
  }

  // ----------------------------------------------------------- ambient kin --

  /** Spawn the map's `ambient: true` placements (non-colliding grazing kin). */
  spawnAmbientKin(placements: NpcPlacement[]): void {
    for (const p of placements) {
      this.kin.push(new AmbientKin(this.scene, p, (tx, ty) => this.host.walkable(tx, ty)));
    }
  }

  // ------------------------------------------------------------- followers --

  /**
   * Attach shadow / legs / glint / bob followers to an actor (the player, an NPC,
   * an item cache). Followers are synced from `update()` — the actor classes are
   * never touched, so this costs them nothing.
   */
  attach(actor: Actor, kind: Follow['kind']): void {
    if (this.follows.some((f) => f.actor === actor)) return;
    const now = this.scene.time.now;
    const f: Follow = {
      actor,
      kind,
      legsGid: 0,
      rustleUntil: 0,
      nextGlint: now + rand(600, 2600),
      nextBob: now + rand(2500, 6000),
      bobUntil: 0,
      idleSince: now,
      lastKey: '',
    };
    if (kind !== 'cache') {
      f.shadow = this.scene.add.ellipse(0, 0, kind === 'kin' ? 16 : SHADOW_W, 4, 0x000000, 0.3);
    }
    this.follows.push(f);
  }

  detach(actor: Actor): void {
    const i = this.follows.findIndex((f) => f.actor === actor);
    if (i < 0) return;
    const [f] = this.follows.splice(i, 1);
    if (f.kind === 'cache' && actor.sprite.active) this.puff(actor.sprite.x, actor.sprite.y - 5);
    f.shadow?.destroy();
    f.legs?.destroy();
  }

  /** A ledge hop just began: the shadow stays on the ground and shrinks through the arc. */
  noteHop(actor: Actor, facing: Facing, ms: number): void {
    const f = this.follows.find((x) => x.actor === actor);
    if (!f) return;
    const dy = facing === 'down' ? 2 : facing === 'up' ? -2 : 0;
    f.hop = {
      start: this.scene.time.now,
      ms,
      fromY: groundYOf(actor.tx, actor.ty),
      toY: groundYOf(actor.tx, actor.ty + dy),
    };
    this.scene.time.delayedCall(ms, () => {
      if (this.destroyed) return;
      this.dust(actor.sprite.x, actor.sprite.y);
    });
  }

  /** The player pressed something: cancel an idle glance and face where they meant. */
  wake(actor: Actor): void {
    const f = this.follows.find((x) => x.actor === actor);
    if (!f) return;
    f.idleSince = this.scene.time.now;
    if (f.glance) {
      actor.setFacing(f.glance.original);
      f.glance = undefined;
    }
  }

  // ----------------------------------------------------------- one-shots --

  /** Grass rustle: the tuft shudders and kicks a leaf fleck or two. */
  rustle(actor: Actor): void {
    const f = this.follows.find((x) => x.actor === actor);
    if (f) f.rustleUntil = this.scene.time.now + 200;
    if (getAmbientMotion()) this.flecks(actor.sprite.x, groundYOf(actor.tx, actor.ty) - 3, 1 + (Math.random() < 0.5 ? 1 : 0));
  }

  /** The encounter tell: the grass you stand in shivers for a beat before the swoosh. */
  encounterTell(actor: Actor): Promise<void> {
    const f = this.follows.find((x) => x.actor === actor);
    if (f) f.rustleUntil = this.scene.time.now + 300;
    if (getAmbientMotion()) this.flecks(actor.sprite.x, groundYOf(actor.tx, actor.ty) - 3, 3);
    return new Promise((r) => this.scene.time.delayedCall(300, r));
  }

  private flecks(x: number, y: number, n: number): void {
    for (let i = 0; i < n; i++) {
      const leaf = this.scene.add.rectangle(x + rand(-5, 5), y, 2, 1, pick(LEAF_FLECK), 1).setDepth(DEPTH.particles);
      this.track(leaf);
      const dx = rand(-8, 8);
      this.scene.tweens.add({
        targets: leaf,
        x: leaf.x + dx,
        y: y - rand(6, 11),
        angle: rand(-90, 90),
        duration: 240,
        ease: 'Quad.out',
        onComplete: () =>
          this.scene.tweens.add({
            targets: leaf,
            y: y + rand(1, 3),
            x: leaf.x + dx * 0.4,
            alpha: 0,
            duration: 380,
            ease: 'Quad.in',
            onComplete: () => this.untrack(leaf),
          }),
      });
    }
  }

  /**
   * A footprint on the tile just left, if its surface keeps one (sand, dune
   * trails, snow — the sidecar's terrain tags; or anywhere on a `footprints: 'all'`
   * map). Fades within ~4 s; never more than 12 alive.
   */
  footprint(tx: number, ty: number, facing: Facing): void {
    const mode = this.cfg.footprints ?? 'auto';
    if (mode === 'none') return;
    const surf = this.map.surfaceAt(tx, ty);
    if (!surf) return;
    const keeps =
      PRINT_SURFACES.has(surf) ||
      (mode === 'all' && (surf === 'ground' || surf === 'path' || PRINT_SURFACES.has(surf)));
    if (!keeps || this.map.hasTerrainAt(tx, ty, 'water') || this.map.hasTerrainAt(tx, ty, 'tall_grass')) return;
    while (this.prints.length >= PRINT_CAP) this.prints.shift()?.destroy();
    const snow = surf.startsWith('snow');
    const g = this.scene.add.graphics().setDepth(DEPTH.print);
    g.fillStyle(snow ? 0x7f90b0 : 0x7a5a30, snow ? 0.55 : 0.5);
    const cx = tx * TILE_SIZE + TILE_SIZE / 2;
    const cy = ty * TILE_SIZE + TILE_SIZE / 2 + 2;
    if (facing === 'up' || facing === 'down') {
      g.fillRect(cx - 3, cy - 3, 2, 3);
      g.fillRect(cx + 1, cy + 1, 2, 3);
    } else {
      g.fillRect(cx - 4, cy - 2, 3, 2);
      g.fillRect(cx + 1, cy + 1, 3, 2);
    }
    this.prints.push(g);
    this.scene.tweens.add({
      targets: g,
      alpha: 0,
      delay: 600,
      duration: PRINT_FADE_MS - 600,
      onComplete: () => {
        const i = this.prints.indexOf(g);
        if (i >= 0) this.prints.splice(i, 1);
        g.destroy();
      },
    });
  }

  /** The door-open beat: the doorway darkens for ~120 ms before the fade. */
  doorBeat(tx: number, ty: number): Promise<void> {
    const r = this.scene.add
      .rectangle(tx * TILE_SIZE + 2, ty * TILE_SIZE + 1, TILE_SIZE - 4, TILE_SIZE - 1, 0x140c08, 0)
      .setOrigin(0, 0)
      .setDepth(DEPTH.doorway);
    this.track(r);
    return new Promise((resolve) => {
      this.scene.tweens.add({
        targets: r,
        fillAlpha: 0.85,
        duration: 120,
        onComplete: () => resolve(),
      });
    });
  }

  /** A little puff of dust (a cache picked up, a ledge landing). */
  puff(x: number, y: number): void {
    if (!getAmbientMotion()) return;
    for (let i = 0; i < 4; i++) {
      const p = this.scene.add.circle(x + rand(-3, 3), y + rand(-2, 1), 1.5, 0xe8dcc0, 0.7).setDepth(DEPTH.particles);
      this.track(p);
      this.scene.tweens.add({
        targets: p,
        x: p.x + rand(-7, 7),
        y: p.y - rand(3, 7),
        scale: 2,
        alpha: 0,
        duration: rand(320, 480),
        ease: 'Quad.out',
        onComplete: () => this.untrack(p),
      });
    }
  }

  private dust(x: number, y: number): void {
    if (!getAmbientMotion()) return;
    for (const side of [-1, 1]) {
      const p = this.scene.add.circle(x + side * 3, y - 1, 1.5, 0xcdbf9e, 0.65).setDepth(DEPTH.print + 0.6);
      this.track(p);
      this.scene.tweens.add({
        targets: p,
        x: p.x + side * 6,
        y: p.y - 2,
        scale: 1.8,
        alpha: 0,
        duration: 300,
        onComplete: () => this.untrack(p),
      });
    }
  }

  private glint(x: number, y: number, depth: number): void {
    const s = this.scene.add.star(x, y, 4, 0.6, 2.6, 0xfff3c0).setDepth(depth).setScale(0);
    this.track(s);
    this.scene.tweens.add({
      targets: s,
      scale: 1,
      angle: 45,
      yoyo: true,
      duration: 260,
      onComplete: () => this.untrack(s),
    });
  }

  private track(o: Phaser.GameObjects.GameObject): void {
    this.transients.add(o);
  }

  private untrack(o: Phaser.GameObjects.GameObject): void {
    this.transients.delete(o);
    o.destroy();
  }

  // ---------------------------------------------------------------- update --

  /**
   * Per-frame: followers, ambient kin, particles, mist, lights, smoke, birds and
   * the starfall clock. Call AFTER actors' `syncDepth` so overlays sort on top.
   */
  update(time: number, delta: number, player: Actor | undefined, modal: boolean): void {
    if (this.destroyed) return;
    const motion = getAmbientMotion();
    const dt = Math.min(0.05, delta / 1000);
    const cam = this.scene.cameras.main;
    const view = cam.worldView;

    for (const f of this.follows) this.syncFollow(f, time, motion, modal, player);
    const pos = player ? { tx: player.tx, ty: player.ty } : undefined;
    for (const k of this.kin) k.update(time, pos, motion);

    this.tickParticles(dt, view, motion);

    if (this.mist && motion) {
      const scale = this.mist.tileScaleX;
      this.mist.tilePositionX = (cam.scrollX * 0.6 + (time / 1000) * this.mistSpeed) / scale;
      this.mist.tilePositionY = (cam.scrollY * 0.6) / scale;
    }

    for (const l of this.lights) {
      const a = motion
        ? 0.86 + 0.08 * Math.sin(time / 230 + l.seed) + 0.06 * Math.sin(time / 97 + l.seed * 3)
        : 1;
      l.pool.setAlpha(a);
      l.halo?.setAlpha(0.22 * a);
    }

    if (motion) {
      for (const c of this.chimneys) {
        if (time < c.nextAt) continue;
        c.nextAt = time + rand(700, 1150);
        if (!this.host.objectVisible(c.obj)) continue;
        if (c.x < view.x - 16 || c.x > view.right + 16 || c.y < view.y - 32 || c.y > view.bottom + 16) continue;
        this.puffSmoke(c.x, c.y);
      }
    }

    if (time >= this.nextStreakAt) {
      this.nextStreakAt = time + rand(this.streakMin, this.streakMax) * 1000;
      void this.starfall();
    }

    if (this.flocks.length && player) {
      for (const fl of this.flocks) {
        const d = Math.abs(player.tx - fl.tx) + Math.abs(player.ty - fl.ty);
        if (!fl.gone && d <= 3 && motion) this.liftFlock(fl, fl.tx - player.tx || 1);
        else if (fl.gone && time >= fl.backAt && d >= 8) {
          for (const b of fl.birds) b.destroy();
          Object.assign(fl, this.buildFlock({ tx: fl.tx, ty: fl.ty }));
        }
      }
    }
    if (motion && time >= this.nextFlyoverAt) {
      this.nextFlyoverAt = time + rand(25000, 60000);
      this.flyover(view);
    }
  }

  private syncFollow(f: Follow, time: number, motion: boolean, modal: boolean, player: Actor | undefined): void {
    const a = f.actor;
    const s = a.sprite;
    if (!s.active) return;
    const onWater = this.map.hasTerrainAt(a.tx, a.ty, 'water');
    const shown = s.visible && s.alpha > 0.05;

    // --- drop shadow: on the ground, shrinking through a hop
    let groundY: number;
    if (f.hop) {
      const t = (time - f.hop.start) / f.hop.ms;
      if (t >= 1) f.hop = undefined;
      groundY = f.hop ? f.hop.fromY + (f.hop.toY - f.hop.fromY) * Math.max(0, t) : groundYOf(a.tx, a.ty);
    } else {
      groundY = a.isMoving ? s.y : groundYOf(a.tx, a.ty);
    }
    if (f.shadow) {
      const lift = Math.max(0, groundY - s.y);
      f.shadow
        // Centred on the sole line so it peeks out below and beside the feet.
        .setPosition(s.x, groundY - 0.5)
        .setScale(Phaser.Math.Clamp(1 - lift / 18, 0.45, 1))
        .setVisible(shown && !onWater)
        .setDepth(s.depth - 0.0002);
    }

    // --- legs hidden in tall grass: the real grass tile re-drawn over the feet
    if (f.kind !== 'cache') {
      const gid = shown ? this.map.terrainGidAt(a.tx, a.ty, 'tall_grass') : 0;
      if (gid) {
        if (!f.legs || f.legsGid !== gid) {
          const tf = ensureTileFrame(this.scene, this.map, gid);
          if (tf) {
            f.legs ??= this.scene.add.image(0, 0, tf.key, tf.frame).setOrigin(0, 0);
            f.legs.setTexture(tf.key, tf.frame);
            f.legs.setCrop(0, TILE_SIZE - LEGS_H, TILE_SIZE, LEGS_H);
            f.legsGid = gid;
          }
        }
        if (f.legs) {
          const jitter = motion && time < f.rustleUntil ? (Math.floor(time / 45) % 2 ? 1 : -1) : 0;
          f.legs
            .setPosition(a.tx * TILE_SIZE + jitter, a.ty * TILE_SIZE)
            .setDepth(s.depth + 0.0001)
            .setVisible(true);
        }
      } else if (f.legs?.visible) {
        f.legs.setVisible(false);
      }
    }

    // --- item-cache glint
    if (f.kind === 'cache' && motion && shown && time >= f.nextGlint) {
      f.nextGlint = time + rand(2400, 4200);
      this.glint(s.x + rand(-4, 4), s.y - rand(7, 11), s.depth + 0.001);
    }

    // --- NPC breathing bob: a 1px lift via the origin (never the tweened y)
    if (f.kind === 'npc' && s.height > 0) {
      if (f.bobUntil && time >= f.bobUntil) {
        s.setOrigin(0.5, 1);
        f.bobUntil = 0;
      } else if (!f.bobUntil && motion && !a.isMoving && time >= f.nextBob) {
        f.nextBob = time + rand(3000, 6500);
        f.bobUntil = time + 260;
        s.setOrigin(0.5, 1 + 1 / s.height);
      }
    }

    // --- the player glances about after 8 s idle (restored on any input: wake())
    if (f.kind === 'player' && player === a) {
      const key = `${a.tx},${a.ty},${a.isMoving}`;
      if (key !== f.lastKey || modal) {
        f.lastKey = key;
        f.idleSince = time;
        if (f.glance) {
          a.setFacing(f.glance.original);
          f.glance = undefined;
        }
      } else if (f.glance) {
        if (time >= f.glance.nextAt) {
          const next = f.glance.steps.shift();
          if (next) {
            a.setFacing(next);
            f.glance.nextAt = time + 650;
          } else {
            f.glance = undefined;
            f.idleSince = time;
          }
        }
      } else if (motion && time - f.idleSince > 8000) {
        const o = a.facing;
        const sides: Facing[] = o === 'left' || o === 'right' ? ['down', 'up'] : ['left', 'right'];
        if (Math.random() < 0.5) sides.reverse();
        f.glance = { original: o, steps: [...sides, o], nextAt: time };
      }
    }
  }

  // --------------------------------------------------------------- teardown --

  destroy(): void {
    this.destroyed = true;
    for (const f of this.follows) {
      f.shadow?.destroy();
      f.legs?.destroy();
    }
    this.follows.length = 0;
    for (const k of this.kin) k.destroy();
    this.kin.length = 0;
    for (const l of this.lights) {
      l.pool.destroy();
      l.halo?.destroy();
    }
    for (const p of this.prints) p.destroy();
    for (const o of this.transients) o.destroy();
    this.transients.clear();
    for (const fl of this.flocks) for (const b of fl.birds) b.destroy();
    this.particleGfx?.destroy();
    this.streakGfx?.destroy();
    this.mist?.destroy();
    this.tintRect?.destroy();
    if (this.bed) {
      this.bed.stop();
      this.bed.destroy();
    }
  }
}

/** Draw (once) the 2-frame gull + bird glyph sheet (6×4 cells, wings up/down). */
function ensureBirdTexture(scene: Phaser.Scene): void {
  const key = 'amb_birds';
  if (scene.textures.exists(key)) return;
  const canvas = scene.textures.createCanvas(key, 24, 4);
  const ctx = canvas?.getContext();
  if (!canvas || !ctx) return;
  const draw = (ox: number, body: string, up: boolean): void => {
    ctx.fillStyle = body;
    ctx.fillRect(ox + 2, 2, 2, 1); // body
    if (up) {
      ctx.fillRect(ox, 0, 1, 1);
      ctx.fillRect(ox + 1, 1, 1, 1);
      ctx.fillRect(ox + 4, 1, 1, 1);
      ctx.fillRect(ox + 5, 0, 1, 1);
    } else {
      ctx.fillRect(ox, 2, 2, 1);
      ctx.fillRect(ox + 4, 2, 2, 1);
      ctx.fillRect(ox + 1, 3, 1, 1);
      ctx.fillRect(ox + 4, 3, 1, 1);
    }
  };
  draw(0, '#f4f6ff', true);
  draw(6, '#f4f6ff', false);
  draw(12, '#2a2438', true);
  draw(18, '#2a2438', false);
  canvas.refresh();
  canvas.add('gull_0', 0, 0, 0, 6, 4);
  canvas.add('gull_1', 0, 6, 0, 6, 4);
  canvas.add('bird_0', 0, 12, 0, 6, 4);
  canvas.add('bird_1', 0, 18, 0, 6, 4);
}
