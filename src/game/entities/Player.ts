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
import { OPPOSITE, type MovePlan, type TraverseContext, type Traversal } from '@game/systems/world/Traversal';
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
/** A runner (the Wick-Run's rented bike) covers a tile in ~40% of a step. */
const RIDE_MS = Math.round(STEP_MS * 0.4);
/** Carried by glare ice or a rail: brisk and even, whatever you press. */
const SLIDE_MS = Math.round(STEP_MS * 0.5);
/** The player's runner-riding walk-sheet (same 4×4 layout). Optional — a drawn
 *  wheel under the walking sprite stands in when it isn't packed. */
const PLAYER_RIDE_SHEET = 'player_indi_runner';

/** The traversal kit, handed in by WorldScene when the map uses it. */
export interface TraverseHooks {
  rules: Traversal;
  ctx: TraverseContext;
  /** A ramp leap began (sfx). */
  onLeap?: () => void;
  /** Pressed uphill into a chute/rail (explain once). */
  onSteep?: () => void;
}

export class Player extends Actor {
  /** True while standing on water (set each frame by WorldScene). */
  private swimming = false;
  /** The bobbing wake drawn under the player when no swim sheet is packed. */
  private wake?: Phaser.GameObjects.Ellipse;
  /** The direction of the last completed move (glare ice keeps it). */
  private lastDir: Facing = 'down';
  /** Standing on a bridge deck: drawn above the deck's overhead layer. */
  private elevated = false;
  /** Riding a runner (set by WorldScene on ride maps). */
  private riding = false;
  /** The drawn wheel under the walking sprite when no runner sheet is packed. */
  private wheel?: Phaser.GameObjects.Graphics;
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
    // On a bridge deck the player is drawn over the deck's overhead layer (~20).
    super.syncDepth(playerDepthBand + (this.elevated ? 11 : 0));
    if (this.wheel) {
      this.wheel.setPosition(this.sprite.x, this.sprite.y);
      this.wheel.setDepth(this.sprite.depth - 0.0005);
    }
    if (!this.wake) return;
    this.wake.setPosition(this.sprite.x, this.sprite.y - this.sprite.height * 0.32);
    this.wake.setDepth(this.sprite.depth - 1);
  }

  /**
   * Mount or dismount the runner. The packed riding sheet if there is one; else a
   * small drawn wheel-and-frame under the walking sprite (the swim fallback's
   * "real art preferred, placeholder always works" contract).
   */
  setRiding(riding: boolean): void {
    if (riding === this.riding) return;
    this.riding = riding;
    const real = this.currentTextureKey !== 'player_placeholder';
    if (real && this.scene.textures.exists(PLAYER_RIDE_SHEET)) {
      this.setWalkSheet(riding ? PLAYER_RIDE_SHEET : PLAYER_SHEET, HUMAN_WALK_FRAMES);
      return;
    }
    this.wheel?.destroy();
    this.wheel = undefined;
    if (!riding) return;
    const g = this.scene.add.graphics();
    // Two dark wheels with a pale rim and a brass frame between them, sitting at
    // the feet — reads as a bike at 16px from any facing.
    g.fillStyle(0x1b1a24, 1).fillCircle(-5, -2, 3).fillCircle(5, -2, 3);
    g.lineStyle(1, 0xc9b27a, 1).strokeCircle(-5, -2, 3).strokeCircle(5, -2, 3);
    g.lineBetween(-5, -2, 0, -5).lineBetween(0, -5, 5, -2).lineBetween(-2, -5, 3, -5);
    this.wheel = g;
  }

  get isRiding(): boolean {
    return this.riding;
  }

  /** Re-derive deck elevation for the tile we stand on (after a warp/cutscene). */
  settleOn(rules: Traversal | undefined): void {
    this.elevated = !!rules?.spanAt(this.tx, this.ty);
  }

  override destroy(): void {
    this.wheel?.destroy();
    this.wheel = undefined;
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
    /** The traversal kit (flows/spans/jumps), when the map uses it. */
    traverse?: TraverseHooks,
  ): void {
    if (this.isMoving) return;
    if (traverse?.rules.active) {
      this.updateTraverse(input, onArrive, onBump, ledgeAt, onHop, traverse);
      return;
    }
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

  /**
   * Movement on a map that uses the traversal kit. First the ground gets its say
   * (a chute/rail/ice tile carries you on — a chute lets left/right steer), then a
   * held direction is planned through the kit's rules (decks, underpasses, ramps,
   * no climbing back up a chute). Ledges still hop exactly as on any map.
   */
  private updateTraverse(
    input: InputController,
    onArrive: (tx: number, ty: number) => void,
    onBump: (() => void) | undefined,
    ledgeAt: ((tx: number, ty: number) => Facing | undefined) | undefined,
    onHop: (() => void) | undefined,
    t: TraverseHooks,
  ): void {
    const action = input.heldDirection();
    const held = action === null ? null : (ACTION_TO_FACING[action] ?? null);
    const running = getAlwaysRun() || input.isDown(InputAction.Cancel);
    const here = { tx: this.tx, ty: this.ty };
    const stepMs = this.riding ? RIDE_MS : running ? RUN_MS : STEP_MS;
    this.sprite.anims.timeScale = STEP_MS / stepMs;

    const carry = t.rules.forced(here, this.lastDir);
    if (carry) {
      if (carry.steer && held && held !== carry.dir && held !== OPPOSITE[carry.dir]) {
        const side = t.rules.plan(here, held, t.ctx);
        if (side.kind !== 'blocked' && this.execute(side, held, stepMs, onArrive, t)) return;
      }
      const ms = carry.steer ? Math.min(stepMs, RUN_MS) : SLIDE_MS;
      const p = t.rules.plan(here, carry.dir, t.ctx);
      if (p.kind !== 'blocked' && this.execute(p, carry.dir, ms, onArrive, t)) return;
      // Stopped against something: free to choose again (uphill stays refused).
    }

    if (held === null) {
      this.stopWalking();
      return;
    }
    const p = t.rules.plan(here, held, t.ctx);
    if (p.kind !== 'blocked' && this.execute(p, held, stepMs, onArrive, t)) return;

    const wasFacing = this.facing;
    if (!t.rules.spanAt(here.tx, here.ty) || wasFacing === held) this.setFacing(held);
    const d = DELTA[held];
    const ahead = { tx: this.tx + d.dx, ty: this.ty + d.dy };
    const landing = { tx: this.tx + d.dx * 2, ty: this.ty + d.dy * 2 };
    if (ledgeAt?.(ahead.tx, ahead.ty) === held && t.ctx.canEnter(landing.tx, landing.ty)) {
      onHop?.();
      this.hop(held, (x, y) => this.arrived(x, y, held, t, onArrive));
      return;
    }
    this.stopWalking();
    if (wasFacing === held) {
      if (p.kind === 'blocked' && p.steep) t.onSteep?.();
      else onBump?.();
    }
  }

  /** Carry out a planned move; true if it began. */
  private execute(
    p: MovePlan,
    dir: Facing,
    ms: number,
    onArrive: (tx: number, ty: number) => void,
    t: TraverseHooks,
  ): boolean {
    const done = (x: number, y: number) => this.arrived(x, y, dir, t, onArrive);
    if (p.kind === 'step') {
      if (!this.step(dir, () => true, done, ms)) return false;
      if (p.deck) this.elevated = true;
      if (p.deck?.kind === 'ladder') this.playWalkAs('up');
      return true;
    }
    if (p.kind === 'pass') {
      this.elevated = false;
      return this.passThrough(dir, p.tiles, done, ms);
    }
    if (p.kind === 'leap') {
      const dist = Math.abs(p.to.tx - this.tx) + Math.abs(p.to.ty - this.ty);
      t.onLeap?.();
      return this.hop(dir, done, ms * dist + 60, dist, 12);
    }
    return false;
  }

  private arrived(
    x: number,
    y: number,
    dir: Facing,
    t: TraverseHooks,
    onArrive: (tx: number, ty: number) => void,
  ): void {
    this.lastDir = dir;
    const span = t.rules.spanAt(x, y);
    this.elevated = !!span;
    if (span?.kind === 'ladder') this.setFacing('up');
    onArrive(x, y);
  }
}
