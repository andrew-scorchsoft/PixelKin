/**
 * The player character. Drives an Actor from abstract input each frame: a held
 * direction turns then steps the player one tile, and arrival fires a callback so
 * WorldScene can run encounter / trigger / warp checks for the tile just entered.
 */
import Phaser from 'phaser';
import { Actor, actionTextureKey, ensurePlaceholderCharacter, HUMAN_WALK_FRAMES, STEP_MS } from './Actor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { getAlwaysRun } from '@game/ui/preferences';
import type { Facing } from '@game/data/world/types';
import { COLORS } from '@game/config';

/** Served walk-sheet texture for the player (packed from assets/trainers/). */
const PLAYER_SHEET = 'player_indi';

const ACTION_TO_FACING: Partial<Record<InputAction, Facing>> = {
  [InputAction.Up]: 'up',
  [InputAction.Down]: 'down',
  [InputAction.Left]: 'left',
  [InputAction.Right]: 'right',
};

const DELTA: Record<Facing, { dx: number; dy: number }> = {
  down: { dx: 0, dy: 1 },
  up: { dx: 0, dy: -1 },
  left: { dx: -1, dy: 0 },
  right: { dx: 1, dy: 0 },
};

/** Running covers a tile in ~60% of a walking step (hold B, or Pace: Always run). */
const RUN_MS = Math.round(STEP_MS * 0.6);

export class Player extends Actor {
  constructor(scene: Phaser.Scene, tx: number, ty: number, facing: Facing) {
    // Prefer the real walk-sheet; fall back to the runtime placeholder if the
    // art failed to load, so the world stays playable either way.
    if (scene.textures.exists(PLAYER_SHEET)) {
      // Pass the layer-3 action sheet too (raise-lamp/toss/gift/sit/hurt), if it
      // loaded — enables `playAction` for cutscene poses.
      super(scene, tx, ty, facing, PLAYER_SHEET, HUMAN_WALK_FRAMES, actionTextureKey(PLAYER_SHEET));
    } else {
      ensurePlaceholderCharacter(scene, 'player_placeholder', COLORS.diamond);
      super(scene, tx, ty, facing, 'player_placeholder');
    }
  }

  /**
   * Advance one frame. `canEnter` queries collision; `onArrive` runs when a step
   * completes. Returns true while the player is mid-step (caller may pause world).
   */
  update(
    input: InputController,
    canEnter: (tx: number, ty: number) => boolean,
    onArrive: (tx: number, ty: number) => void,
    onBump?: () => void,
    /** One-way ledge lookup (CollisionGrid.ledgeAt); walking into a ledge facing
     *  its hop direction leaps it instead of bumping. */
    ledgeAt?: (tx: number, ty: number) => Facing | undefined,
    /** Fired when a ledge hop begins (the scene plays the hop sfx). */
    onHop?: () => void,
  ): void {
    if (this.isMoving) return;
    const dir = input.heldDirection();
    if (dir === null) {
      this.stopWalking(); // no input: settle the walk cycle onto the idle pose
      return;
    }
    const facing = ACTION_TO_FACING[dir];
    if (!facing) {
      this.stopWalking();
      return;
    }
    // Running: hold B (Cancel) like the classics, or the Always-run setting.
    // Same walk frames, faster cycle — running is free (docs/art-style.md §A).
    const running = getAlwaysRun() || input.isDown(InputAction.Cancel);
    this.sprite.anims.timeScale = running ? STEP_MS / RUN_MS : 1;

    // Turning to face a new way isn't a bump; walking into a wall you already
    // face is — that's when we give feedback.
    const wasFacing = this.facing;
    const moved = this.step(facing, canEnter, onArrive, running ? RUN_MS : STEP_MS);
    if (!moved) {
      // A blocked step might be a LEDGE in our hop direction: leap it if the
      // landing two tiles ahead is open.
      const ahead = { tx: this.tx + DELTA[facing].dx, ty: this.ty + DELTA[facing].dy };
      const landing = { tx: this.tx + DELTA[facing].dx * 2, ty: this.ty + DELTA[facing].dy * 2 };
      if (ledgeAt?.(ahead.tx, ahead.ty) === facing && canEnter(landing.tx, landing.ty)) {
        onHop?.();
        this.hop(facing, onArrive);
        return;
      }
      this.stopWalking(); // turned or bumped, but didn't step: don't keep cycling
      if (wasFacing === facing) onBump?.();
    }
  }
}
