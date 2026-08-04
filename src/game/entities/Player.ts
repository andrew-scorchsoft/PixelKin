/**
 * The player character. Drives an Actor from abstract input each frame: a held
 * direction turns then steps the player one tile, and arrival fires a callback so
 * WorldScene can run encounter / trigger / warp checks for the tile just entered.
 */
import Phaser from 'phaser';
import {
  Actor,
  type ActorFrames,
  actionTextureKey,
  ensurePlaceholderCharacter,
  HUMAN_WALK_FRAMES,
  STEP_MS,
} from './Actor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { getAlwaysRun } from '@game/ui/preferences';
import type { Facing } from '@game/data/world/types';
import { COLORS } from '@game/config';

/** Served walk-sheet texture for the player (packed from assets/trainers/). */
const PLAYER_SHEET = 'player_indi';
/**
 * The player's SWIMMING walk-sheet (same 4×4 layout, drawn submerged to
 * mid-chest inside a ripple ring). Swapped in while standing on water the
 * vesperlamp's Tidecall carries you over. Optional: if it isn't packed, the
 * procedural fallback below still reads as swimming.
 */
const PLAYER_SWIM_SHEET = 'player_indi_swim';

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
  /** True while standing on water (set each frame by WorldScene). */
  private swimming = false;
  /** The bobbing wake drawn under the player when no swim sheet is packed. */
  private wake?: Phaser.GameObjects.Ellipse;
  constructor(scene: Phaser.Scene, tx: number, ty: number, facing: Facing) {
    super(scene, tx, ty, facing, ...Player.resolveSheet(scene));
  }

  /**
   * Pick the player's texture: the real walk-sheet (plus its layer-3 action
   * sheet) if the art loaded, else the runtime placeholder so the world stays
   * playable either way. Returned as super() args — the Npc.resolveSheet pattern
   * — so the super call stays a root-level statement.
   */
  private static resolveSheet(
    scene: Phaser.Scene,
  ): [string, ActorFrames?, string?] {
    if (scene.textures.exists(PLAYER_SHEET)) {
      return [PLAYER_SHEET, HUMAN_WALK_FRAMES, actionTextureKey(PLAYER_SHEET)];
    }
    ensurePlaceholderCharacter(scene, 'player_placeholder', COLORS.diamond);
    return ['player_placeholder'];
  }

  /**
   * Tell the player whether the tile under them is water. Called every frame by
   * WorldScene, so it must be cheap and idempotent — it returns immediately
   * unless the state actually changed.
   *
   * Preferred look is the packed SWIM SHEET (submerged to mid-chest in a ripple
   * ring). When that art isn't present we fall back to a procedural treatment —
   * the walking sprite cropped at the waterline plus a bobbing wake — so the
   * mechanic still reads on any build, the same "real art preferred, placeholder
   * always works" contract the rest of the actor code follows.
   */
  setSwimming(swimming: boolean): void {
    if (swimming === this.swimming) return;
    this.swimming = swimming;
    // Only the real sheet has a swimming twin; the placeholder falls through to
    // the procedural look.
    if (this.currentTextureKey !== 'player_placeholder' && this.scene.textures.exists(PLAYER_SWIM_SHEET)) {
      this.setWalkSheet(swimming ? PLAYER_SWIM_SHEET : PLAYER_SHEET, HUMAN_WALK_FRAMES);
      return;
    }
    this.setProceduralSwim(swimming);
  }

  /** Whether the player is currently in the water (WorldScene gates on this). */
  get isSwimming(): boolean {
    return this.swimming;
  }

  /**
   * The art-free swimming look: crop the sprite at the waterline so the legs
   * disappear under the surface, and float a pale wake ellipse that breathes.
   */
  private setProceduralSwim(swimming: boolean): void {
    const h = this.sprite.height;
    const w = this.sprite.width;
    if (swimming) {
      // Hide the bottom ~40% of the frame: the body below the surface.
      this.sprite.setCrop(0, 0, w, Math.round(h * 0.6));
      const wake = this.scene.add
        .ellipse(this.sprite.x, this.sprite.y - h * 0.32, w * 0.66, 5, 0xbcd9ea, 0.5)
        .setDepth(this.sprite.depth - 1);
      this.scene.tweens.add({
        targets: wake,
        scaleX: 1.18,
        alpha: 0.28,
        duration: 620,
        yoyo: true,
        repeat: -1,
        ease: 'Sine.inOut',
      });
      this.wake = wake;
    } else {
      this.sprite.setCrop();
      this.wake?.destroy();
      this.wake = undefined;
    }
  }

  /** Keep the procedural wake pinned under the player. WorldScene calls this
   *  every frame (modal included), so the wake tracks cutscene walks too. */
  override syncDepth(playerDepthBand: number): void {
    super.syncDepth(playerDepthBand);
    if (!this.wake) return;
    this.wake.setPosition(this.sprite.x, this.sprite.y - this.sprite.height * 0.32);
    this.wake.setDepth(this.sprite.depth - 1);
  }

  override destroy(): void {
    this.wake?.destroy();
    this.wake = undefined;
    super.destroy();
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
