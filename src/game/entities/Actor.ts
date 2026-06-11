/**
 * Actor — a grid-walking character (the player or an NPC).
 *
 * Movement is tile-based: an actor occupies a tile, faces a direction, and steps
 * to an adjacent tile with a short tween (no free movement — classic handheld feel).
 * Sprites are anchored bottom-centre on their tile so taller walk-sheets sit right.
 * An actor draws from real 3×4 walk-sheets (`HUMAN_WALK_FRAMES`, with a step cycle)
 * where the art is packed; callers fall back to a runtime placeholder texture
 * (`PLACEHOLDER_FRAMES`) so movement and facing stay testable when art is missing.
 */
import Phaser from 'phaser';
import { TILE_SIZE } from '@game/config';
import { hex } from '@game/ui/theme';
import type { Facing } from '@game/data/world/types';

/**
 * How an actor's texture maps facing → frame(s). The placeholder is a single-row
 * 4-frame sheet (one idle pose per direction); a real human walk-sheet is the
 * 3×4 / 32×32 standard (docs/art-style.md §A) with a step cycle per direction.
 */
export interface ActorFrames {
  /** Standing/idle frame index per facing. */
  idle: Record<Facing, number>;
  /** Optional step-cycle frames per facing, played while moving. */
  walk?: Record<Facing, number[]>;
}

/** Placeholder sheet: 4 frames, one idle pose per facing (no walk cycle). */
export const PLACEHOLDER_FRAMES: ActorFrames = {
  idle: { down: 0, left: 1, right: 2, up: 3 },
};

/**
 * The 4×4 human walk-sheet layout (docs/art-style.md §5A): rows =
 * down/left/right/up, columns = idle / contact-L / passing / contact-R. The walk
 * cycle is a real stride — `contactL → passing → contactR → passing` — so the
 * legs cross over and the body bobs (the passing frame is drawn 1px higher),
 * instead of the old two-frame shuffle. The engine plays this continuously
 * across consecutive tiles (it never resets to idle between steps); it settles
 * to the idle frame only when movement actually stops (`stopWalking`).
 */
export const HUMAN_WALK_FRAMES: ActorFrames = (() => {
  const row: Record<Facing, number> = { down: 0, left: 1, right: 2, up: 3 };
  const idle = {} as Record<Facing, number>;
  const walk = {} as Record<Facing, number[]>;
  (['down', 'left', 'right', 'up'] as Facing[]).forEach((f) => {
    const base = row[f] * 4; // col0 idle, col1 contact-L, col2 passing, col3 contact-R
    idle[f] = base;
    walk[f] = [base + 1, base + 2, base + 3, base + 2];
  });
  return { idle, walk };
})();

/**
 * Suffix for a character's optional layer-3 action texture: a walk-sheet texture
 * `player_indi` has its action sheet loaded as `player_indi_actions` (see
 * PreloadScene + pack_trainers.py). `actionTextureKey()` builds it.
 */
export const ACTIONS_KEY_SUFFIX = '_actions';
/** Texture key of the one shared layer-2 emote/bubble sheet (docs/art-style.md §A3). */
export const EMOTE_TEXTURE = 'emotes';

/** Build the action-texture key for a walk-sheet key (e.g. `player_indi` → `player_indi_actions`). */
export const actionTextureKey = (walkKey: string): string => `${walkKey}${ACTIONS_KEY_SUFFIX}`;

/**
 * Event poses on a layer-3 action sheet (4×2, docs/art-style.md §A2), as frame
 * lists played as one-shots. Two-frame poses animate (start → hold); single-frame
 * poses are a held pose. Must match the sheet's cell order.
 */
export const HUMAN_ACTION_FRAMES = {
  raiseLamp: [0, 1],
  toss: [2, 3],
  gift: [4, 5],
  sit: [6],
  hurt: [7],
} as const;
export type ActionName = keyof typeof HUMAN_ACTION_FRAMES;

/**
 * Emote bubbles on the shared layer-2 emote sheet (4×2, docs/art-style.md §A3),
 * by cell index. Popped above an actor via `showEmote`.
 */
export const EMOTE_FRAMES = {
  alert: 0,
  question: 1,
  heart: 2,
  ellipsis: 3,
  sweat: 4,
  sleep: 5,
  music: 6,
  anger: 7,
} as const;
export type EmoteName = keyof typeof EMOTE_FRAMES;

const FACING_DELTA: Record<Facing, { dx: number; dy: number }> = {
  down: { dx: 0, dy: 1 },
  up: { dx: 0, dy: -1 },
  left: { dx: -1, dy: 0 },
  right: { dx: 1, dy: 0 },
};

/** Default step duration in ms (one tile). */
export const STEP_MS = 160;

export class Actor {
  readonly sprite: Phaser.GameObjects.Sprite;
  tx: number;
  ty: number;
  facing: Facing;
  private moving = false;

  /** True while a one-shot action pose is playing; movement is suspended. */
  private acting = false;

  constructor(
    protected scene: Phaser.Scene,
    tx: number,
    ty: number,
    facing: Facing,
    private readonly textureKey: string,
    private readonly frames: ActorFrames = PLACEHOLDER_FRAMES,
    /** Optional layer-3 action texture key (e.g. `player_indi_actions`); enables `playAction`. */
    private readonly actionsKey?: string,
  ) {
    this.tx = tx;
    this.ty = ty;
    this.facing = facing;
    if (frames.walk) Actor.ensureWalkAnims(scene, textureKey, frames.walk);
    const { x, y } = Actor.tileToWorld(tx, ty);
    this.sprite = scene.add.sprite(x, y, textureKey, frames.idle[facing]).setOrigin(0.5, 1);
  }

  /** Register one looping walk animation per facing for a texture (idempotent). */
  private static ensureWalkAnims(
    scene: Phaser.Scene,
    textureKey: string,
    walk: Record<Facing, number[]>,
  ): void {
    (['down', 'left', 'right', 'up'] as Facing[]).forEach((f) => {
      const key = `${textureKey}__walk_${f}`;
      if (scene.anims.exists(key)) return;
      scene.anims.create({
        key,
        frames: walk[f].map((frame) => ({ key: textureKey, frame })),
        // One full cycle spans a single tile step.
        frameRate: (walk[f].length * 1000) / STEP_MS,
        repeat: -1,
      });
    });
  }

  /** Bottom-centre world position of a tile (origin 0.5,1 sits the feet on the tile). */
  static tileToWorld(tx: number, ty: number): { x: number; y: number } {
    return { x: tx * TILE_SIZE + TILE_SIZE / 2, y: ty * TILE_SIZE + TILE_SIZE };
  }

  get isMoving(): boolean {
    return this.moving;
  }

  setFacing(facing: Facing): void {
    this.facing = facing;
    // The walk animation owns the displayed frame whenever it's running — both
    // while a tile tween is in flight (`moving`) AND in the brief gap between
    // consecutive held-direction steps, where `moving` has flipped false but the
    // looping cycle is still playing. Stamping the idle frame in that gap (every
    // `step()` begins with setFacing) flashed a "standing" frame at each tile
    // boundary — the twitch. Only settle to idle when nothing is animating.
    if (!this.moving && !this.sprite.anims.isPlaying) {
      this.sprite.setFrame(this.frames.idle[facing]);
    }
  }

  /** The tile directly in front of the actor. */
  tileAhead(): { tx: number; ty: number } {
    const d = FACING_DELTA[this.facing];
    return { tx: this.tx + d.dx, ty: this.ty + d.dy };
  }

  /**
   * Try to step one tile toward `facing`. Faces that way first (turn-in-place),
   * then moves only if `canEnter` allows the target. Returns true if a step began.
   */
  step(
    facing: Facing,
    canEnter: (tx: number, ty: number) => boolean,
    onArrive?: (tx: number, ty: number) => void,
    durationMs = STEP_MS,
  ): boolean {
    if (this.moving || this.acting) return false;
    this.setFacing(facing);
    const d = FACING_DELTA[facing];
    const nx = this.tx + d.dx;
    const ny = this.ty + d.dy;
    if (!canEnter(nx, ny)) return false;

    this.moving = true;
    this.tx = nx;
    this.ty = ny;
    // `true` = ignoreIfPlaying: when the player holds a direction over several
    // tiles this keeps ONE walk cycle flowing instead of restarting it (and
    // flashing the idle frame) at every tile boundary — the old "shuffle".
    if (this.frames.walk) this.sprite.play(`${this.textureKey}__walk_${facing}`, true);
    const { x, y } = Actor.tileToWorld(nx, ny);
    this.scene.tweens.add({
      targets: this.sprite,
      x,
      y,
      duration: durationMs,
      ease: 'Linear',
      onComplete: () => {
        // Don't stop here — if another step follows, the cycle carries on
        // seamlessly. `stopWalking()` settles us to idle once movement ends.
        this.moving = false;
        onArrive?.(nx, ny);
      },
    });
    return true;
  }

  /**
   * Hop a one-way LEDGE: a two-tile leap over the ledge tile, with a small arc.
   * The caller has already verified the ledge direction and that the landing
   * tile is enterable. Fires `onArrive` at the landing (encounters roll there,
   * like the classics).
   */
  hop(
    facing: Facing,
    onArrive?: (tx: number, ty: number) => void,
    durationMs = STEP_MS * 2,
  ): boolean {
    if (this.moving || this.acting) return false;
    this.setFacing(facing);
    const d = FACING_DELTA[facing];
    const nx = this.tx + d.dx * 2;
    const ny = this.ty + d.dy * 2;

    this.moving = true;
    this.tx = nx;
    this.ty = ny;
    if (this.frames.walk) this.sprite.play(`${this.textureKey}__walk_${facing}`, true);
    const { x, y } = Actor.tileToWorld(nx, ny);
    // Linear travel + a little parabolic lift so the leap reads as a jump.
    const fromX = this.sprite.x;
    const fromY = this.sprite.y;
    const lift = 6;
    this.scene.tweens.addCounter({
      from: 0,
      to: 1,
      duration: durationMs,
      ease: 'Linear',
      onUpdate: (tw) => {
        const t = tw.getValue() ?? 0;
        this.sprite.x = fromX + (x - fromX) * t;
        this.sprite.y = fromY + (y - fromY) * t - lift * 4 * t * (1 - t);
      },
      onComplete: () => {
        this.sprite.setPosition(x, y);
        this.moving = false;
        this.stopWalking();
        onArrive?.(nx, ny);
      },
    });
    return true;
  }

  /**
   * Settle to the idle pose when movement has stopped. Call this each frame the
   * actor is NOT taking a step (no held direction, a blocked bump, etc.) so the
   * continuously-playing walk cycle stops cleanly on the standing frame.
   */
  stopWalking(): void {
    if (this.moving || !this.frames.walk) return;
    if (this.sprite.anims.isPlaying) this.sprite.stop();
    this.sprite.setFrame(this.frames.idle[this.facing]);
  }

  /** Whether this actor has a layer-3 action sheet (so `playAction` will do something). */
  get hasActions(): boolean {
    return !!this.actionsKey && this.scene.textures.exists(this.actionsKey);
  }

  /** Register (once) a one-shot animation for an action pose on the action texture. */
  private ensureActionAnim(key: string, name: ActionName): void {
    const animKey = `${key}__act_${name}`;
    if (this.scene.anims.exists(animKey)) return;
    const frames = HUMAN_ACTION_FRAMES[name];
    this.scene.anims.create({
      key: animKey,
      frames: frames.map((frame) => ({ key, frame })),
      frameRate: 1000 / 150, // ~150ms per pose frame
      repeat: 0,
    });
  }

  /**
   * Play a one-shot event pose (raise-lamp, toss, gift, sit, hurt) from the
   * layer-3 action sheet, then settle back to idle. No-op (resolves immediately)
   * for actors without an action sheet, so cutscene code can call it
   * unconditionally. Movement is suspended for the duration. `holdMs` is how long
   * the final pose holds before returning to idle.
   */
  playAction(name: ActionName, holdMs = 600): Promise<void> {
    const key = this.actionsKey;
    if (!key || !this.scene.textures.exists(key) || this.acting) return Promise.resolve();
    this.acting = true;
    this.stopWalking();
    this.ensureActionAnim(key, name);
    return new Promise<void>((resolve) => {
      const finish = () => {
        this.acting = false;
        this.sprite.setTexture(this.textureKey, this.frames.idle[this.facing]);
        resolve();
      };
      this.sprite.play(`${key}__act_${name}`);
      this.sprite.once(Phaser.Animations.Events.ANIMATION_COMPLETE, () => {
        this.scene.time.delayedCall(holdMs, finish);
      });
    });
  }

  /**
   * Pop a shared emote bubble (alert, question, heart, …) above the actor's head:
   * a transient overlay sprite that scales in, bobs, holds, then fades and
   * destroys itself. No-op (resolves immediately) if the emote sheet isn't loaded.
   */
  showEmote(name: EmoteName, holdMs = 900): Promise<void> {
    if (!this.scene.textures.exists(EMOTE_TEXTURE)) return Promise.resolve();
    const restY = this.sprite.y - TILE_SIZE - 6; // just above the head
    const bubble = this.scene.add
      .sprite(this.sprite.x, restY + 4, EMOTE_TEXTURE, EMOTE_FRAMES[name])
      .setOrigin(0.5, 1)
      .setDepth(this.sprite.depth + 1000)
      .setAlpha(0)
      .setScale(0.5);
    return new Promise<void>((resolve) => {
      this.scene.tweens.add({
        targets: bubble,
        alpha: 1,
        scale: 1,
        y: restY,
        duration: 140,
        ease: 'Back.easeOut',
        onComplete: () => {
          this.scene.tweens.add({ targets: bubble, y: restY - 2, duration: 260, yoyo: true, repeat: 1 });
          this.scene.time.delayedCall(holdMs, () => {
            this.scene.tweens.add({
              targets: bubble,
              alpha: 0,
              duration: 140,
              onComplete: () => {
                bubble.destroy();
                resolve();
              },
            });
          });
        },
      });
    });
  }

  /** Keep depth in sync with row so actors sort correctly among deco tiles. */
  syncDepth(playerDepthBand: number): void {
    this.sprite.setDepth(playerDepthBand + this.sprite.y * 0.001);
  }

  destroy(): void {
    this.sprite.destroy();
  }
}

/**
 * Build (once) a placeholder 4-facing character spritesheet so actors are visible
 * and their facing is readable before real walk-sheets are generated. Frames are
 * 16x16: a coloured body with a small "face" marker that moves per direction.
 */
export function ensurePlaceholderCharacter(scene: Phaser.Scene, key: string, color: string): void {
  if (scene.textures.exists(key)) return;
  const size = TILE_SIZE;
  const canvas = scene.textures.createCanvas(key, size * 4, size);
  const ctx = canvas?.getContext();
  if (!ctx || !canvas) return;

  const body = `#${hex(color).toString(16).padStart(6, '0')}`;
  const facings: Facing[] = ['down', 'left', 'right', 'up'];
  facings.forEach((facing, i) => {
    const ox = i * size;
    // body
    ctx.fillStyle = body;
    ctx.fillRect(ox + 3, 3, size - 6, size - 4);
    ctx.strokeStyle = 'rgba(0,0,0,0.45)';
    ctx.lineWidth = 1;
    ctx.strokeRect(ox + 3.5, 3.5, size - 7, size - 5);
    // face marker indicating facing
    ctx.fillStyle = '#0b1026';
    const cx = ox + size / 2;
    const cy = 7;
    const m: Record<Facing, [number, number]> = {
      down: [cx, cy + 1],
      up: [cx, cy - 2],
      left: [cx - 3, cy],
      right: [cx + 3, cy],
    };
    const [mx, my] = m[facing];
    ctx.fillRect(mx - 1, my - 1, 2, 2);
  });
  canvas.refresh();
  // Register one 16x16 frame per facing (0=down,1=left,2=right,3=up) so actors can
  // setFrame(idle[facing]) — a CanvasTexture otherwise has only the whole-image
  // `__BASE` frame, and requesting frame "1"/"2"/"3" would warn and show nothing.
  facings.forEach((_facing, i) => canvas.add(i, 0, i * size, 0, size, size));
}
