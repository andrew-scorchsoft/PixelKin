/**
 * NPC — a placement-driven actor. Reads an `NpcPlacement` from the map and behaves
 * per its movement pattern (static / wander / patrol / look_around). NPCs can be
 * told to face the player when talked to, and can be conditionally present based on
 * flags (handled by WorldScene when it instantiates them).
 */
import Phaser from 'phaser';
import { Actor, type ActorFrames, ensurePlaceholderCharacter, HUMAN_WALK_FRAMES } from './Actor';
import type { NpcPlacement, Facing } from '@game/data/world/types';
import { COLORS } from '@game/config';

const FACINGS: Facing[] = ['down', 'left', 'right', 'up'];

/** Map NPC sprite keys → a served walk-sheet texture where real art exists. */
const SPRITE_SHEETS: Record<string, string> = {
  npc_mentor: 'professor_fenn',
  wren: 'wren',
  npc_shopkeeper: 'npc_shopkeeper',
  npc_lampwarden: 'npc_lampwarden',
};

/** Placeholder body colours so distinct NPCs read apart before real walk-sheets. */
const SPRITE_COLORS: Record<string, string> = {
  npc_mentor: COLORS.bone,
  npc_child: COLORS.grass,
  wren: COLORS.diamond,
  npc_shopkeeper: COLORS.fire,
  npc_lampwarden: COLORS.deepBlue,
};

/**
 * Draw (once) the ground item-cache sprite — a small wayfarer's supply bundle
 * with a lamp-glint, used by `sprite: 'item_cache'` NPC placements. Item caches
 * are NPCs so they can run a pickup script and vanish via hidden_when_flag.
 */
export function ensureItemCacheSprite(scene: Phaser.Scene, key: string): void {
  if (scene.textures.exists(key)) return;
  const size = 16;
  const canvas = scene.textures.createCanvas(key, size * 4, size);
  const ctx = canvas?.getContext();
  if (!ctx || !canvas) return;
  for (let i = 0; i < 4; i++) {
    const ox = i * size;
    // rolled bundle
    ctx.fillStyle = '#6b4a2e';
    ctx.fillRect(ox + 4, 8, 8, 6);
    ctx.fillStyle = '#8a6238';
    ctx.fillRect(ox + 4, 8, 8, 2);
    // strap
    ctx.fillStyle = '#3c2a18';
    ctx.fillRect(ox + 7, 8, 2, 6);
    // contact shadow
    ctx.fillStyle = 'rgba(0,0,0,0.35)';
    ctx.fillRect(ox + 3, 14, 10, 1);
    // lamp-glint
    ctx.fillStyle = '#f5d98a';
    ctx.fillRect(ox + 10, 6, 2, 2);
  }
  canvas.refresh();
  for (let i = 0; i < 4; i++) canvas.add(i, 0, i * size, 0, size, size);
}

export class Npc extends Actor {
  private timer = 0;
  private patrolIndex = 0;

  constructor(
    scene: Phaser.Scene,
    readonly placement: NpcPlacement,
  ) {
    super(scene, placement.at.tx, placement.at.ty, placement.facing, ...Npc.resolveSheet(scene, placement));
  }

  /**
   * Pick this NPC's texture: the real walk-sheet if it loaded, else a runtime
   * placeholder swatch. Returned as super() args so it can run before `super`.
   */
  private static resolveSheet(
    scene: Phaser.Scene,
    placement: NpcPlacement,
  ): [string, ActorFrames?] {
    if (placement.sprite === 'item_cache') {
      ensureItemCacheSprite(scene, 'npc_item_cache');
      return ['npc_item_cache'];
    }
    const sheet = SPRITE_SHEETS[placement.sprite];
    if (sheet && scene.textures.exists(sheet)) return [sheet, HUMAN_WALK_FRAMES];
    const color = SPRITE_COLORS[placement.sprite] ?? COLORS.fire;
    const key = `npc_placeholder_${placement.sprite}`;
    ensurePlaceholderCharacter(scene, key, color);
    return [key];
  }

  get id(): string {
    return this.placement.id;
  }

  get dialogueRef(): string | undefined {
    return this.placement.dialogue_ref;
  }

  /** Turn to look at a tile (used when the player talks to this NPC). */
  facePoint(tx: number, ty: number): void {
    const dx = tx - this.tx;
    const dy = ty - this.ty;
    if (Math.abs(dx) > Math.abs(dy)) this.setFacing(dx > 0 ? 'right' : 'left');
    else this.setFacing(dy > 0 ? 'down' : 'up');
  }

  /** Ambient movement. `canEnter` prevents walking into walls or onto the player. */
  update(deltaMs: number, canEnter: (tx: number, ty: number) => boolean): void {
    if (this.isMoving) return;
    // Standing this frame: settle the walk cycle onto the idle pose. step()
    // below replays the cycle if this NPC actually moves.
    this.stopWalking();
    const move = this.placement.movement;
    if (move === 'static') return;

    this.timer -= deltaMs;
    if (this.timer > 0) return;
    this.timer = 900 + Math.random() * 1600;

    if (move === 'look_around') {
      this.setFacing(FACINGS[Math.floor(Math.random() * FACINGS.length)]);
      return;
    }
    if (move === 'wander') {
      const dir = FACINGS[Math.floor(Math.random() * FACINGS.length)];
      this.step(dir, canEnter);
      return;
    }
    if (move === 'patrol' && this.placement.patrol && this.placement.patrol.length > 0) {
      const target = this.placement.patrol[this.patrolIndex % this.placement.patrol.length];
      const dx = target.tx - this.tx;
      const dy = target.ty - this.ty;
      let dir: Facing | null = null;
      if (Math.abs(dx) > Math.abs(dy)) dir = dx > 0 ? 'right' : dx < 0 ? 'left' : null;
      else dir = dy > 0 ? 'down' : dy < 0 ? 'up' : null;
      if (dir) this.step(dir, canEnter);
      else this.patrolIndex++;
    }
  }
}
