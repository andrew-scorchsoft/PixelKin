/**
 * The player character. Drives an Actor from abstract input each frame: a held
 * direction turns then steps the player one tile, and arrival fires a callback so
 * WorldScene can run encounter / trigger / warp checks for the tile just entered.
 */
import Phaser from 'phaser';
import { Actor, actionTextureKey, ensurePlaceholderCharacter, HUMAN_WALK_FRAMES } from './Actor';
import { InputController, InputAction } from '@game/systems/input/InputController';
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
    // Turning to face a new way isn't a bump; walking into a wall you already
    // face is — that's when we give feedback.
    const wasFacing = this.facing;
    const moved = this.step(facing, canEnter, onArrive);
    if (!moved) {
      this.stopWalking(); // turned or bumped, but didn't step: don't keep cycling
      if (wasFacing === facing) onBump?.();
    }
  }
}
