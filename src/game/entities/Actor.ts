/**
 * Actor — a grid-walking character (the player or an NPC).
 *
 * Movement is tile-based: an actor occupies a tile, faces a direction, and steps
 * to an adjacent tile with a short tween (no free movement — classic handheld feel).
 * Sprites are anchored bottom-centre on their tile so taller walk-sheets sit right.
 * Until real walk-sheets exist, a placeholder 4-facing character texture is drawn at
 * runtime so movement and NPC facing are fully testable.
 */
import Phaser from 'phaser';
import { TILE_SIZE } from '@game/config';
import { hex } from '@game/ui/theme';
import type { Facing } from '@game/data/world/types';

/** Facing → frame index in the (placeholder and real) walk sheet: down/left/right/up. */
export const FACING_FRAME: Record<Facing, number> = { down: 0, left: 1, right: 2, up: 3 };

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

  constructor(
    protected scene: Phaser.Scene,
    tx: number,
    ty: number,
    facing: Facing,
    textureKey: string,
  ) {
    this.tx = tx;
    this.ty = ty;
    this.facing = facing;
    const { x, y } = Actor.tileToWorld(tx, ty);
    this.sprite = scene.add.sprite(x, y, textureKey, FACING_FRAME[facing]).setOrigin(0.5, 1);
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
    this.sprite.setFrame(FACING_FRAME[facing]);
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
    if (this.moving) return false;
    this.setFacing(facing);
    const d = FACING_DELTA[facing];
    const nx = this.tx + d.dx;
    const ny = this.ty + d.dy;
    if (!canEnter(nx, ny)) return false;

    this.moving = true;
    this.tx = nx;
    this.ty = ny;
    const { x, y } = Actor.tileToWorld(nx, ny);
    this.scene.tweens.add({
      targets: this.sprite,
      x,
      y,
      duration: durationMs,
      ease: 'Linear',
      onComplete: () => {
        this.moving = false;
        onArrive?.(nx, ny);
      },
    });
    return true;
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
}
