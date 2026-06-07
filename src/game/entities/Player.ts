/**
 * The player character. Drives an Actor from abstract input each frame: a held
 * direction turns then steps the player one tile, and arrival fires a callback so
 * WorldScene can run encounter / trigger / warp checks for the tile just entered.
 */
import Phaser from 'phaser';
import { Actor, ensurePlaceholderCharacter } from './Actor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import type { Facing } from '@game/data/world/types';
import { COLORS } from '@game/config';

const ACTION_TO_FACING: Partial<Record<InputAction, Facing>> = {
  [InputAction.Up]: 'up',
  [InputAction.Down]: 'down',
  [InputAction.Left]: 'left',
  [InputAction.Right]: 'right',
};

export class Player extends Actor {
  constructor(scene: Phaser.Scene, tx: number, ty: number, facing: Facing) {
    ensurePlaceholderCharacter(scene, 'player_placeholder', COLORS.diamond);
    super(scene, tx, ty, facing, 'player_placeholder');
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
    if (dir === null) return;
    const facing = ACTION_TO_FACING[dir];
    if (!facing) return;
    // Turning to face a new way isn't a bump; walking into a wall you already
    // face is — that's when we give feedback.
    const wasFacing = this.facing;
    const moved = this.step(facing, canEnter, onArrive);
    if (!moved && wasFacing === facing) onBump?.();
  }
}
