/**
 * NPC — a placement-driven actor. Reads an `NpcPlacement` from the map and behaves
 * per its movement pattern (static / wander / patrol / look_around). NPCs can be
 * told to face the player when talked to, and can be conditionally present based on
 * flags (handled by WorldScene when it instantiates them).
 */
import Phaser from 'phaser';
import {
  Actor,
  type ActorFrames,
  ensurePlaceholderCharacter,
  HUMAN_WALK_FRAMES,
  STATIC_FRAMES,
} from './Actor';
import type { NpcPlacement, Facing } from '@game/data/world/types';
import { COLORS } from '@game/config';
import { creatureTextureKey, loadCreatureSprite } from '@game/systems/sprites/CreatureSprites';

const FACINGS: Facing[] = ['down', 'left', 'right', 'up'];

/**
 * Creature NPCs: a placement whose `sprite` is `kin_<id>_overworld` (the Three
 * Hours at their sites) — or a named alias below — renders the kin's packed
 * overworld sprite instead of a human walk sheet. The view is lazy-loaded:
 * the NPC spawns on the placeholder swatch and swaps when the texture lands.
 */
const CREATURE_SPRITE_ALIASES: Record<string, number> = {
  fennlight_dim: 67, // the Glowmoss Deep sleeper — a drained Fennlight
};

/** The kin id behind a creature-NPC sprite key, or null for human sprites. */
function creatureKinId(sprite: string): number | null {
  if (sprite in CREATURE_SPRITE_ALIASES) return CREATURE_SPRITE_ALIASES[sprite];
  const m = /^kin_(\d+)_overworld$/.exec(sprite);
  return m ? Number(m[1]) : null;
}

/** Map NPC sprite keys → a served walk-sheet texture where real art exists. */
const SPRITE_SHEETS: Record<string, string> = {
  npc_mentor: 'professor_fenn',
  wren: 'wren',
  npc_shopkeeper: 'npc_shopkeeper',
  npc_lampwarden: 'npc_lampwarden',
  // The remaining-cast Lampwardens + the Hollowing's leader (bespoke walk sheets).
  mira_vael: 'mira_vael',
  mira: 'mira_vael',
  ysolde_frost: 'ysolde_frost',
  ysolde: 'ysolde_frost',
  lucan_pyre: 'lucan_pyre',
  lucan: 'lucan_pyre',
  nessa_cole: 'nessa_cole',
  nessa: 'nessa_cole',
  warden_cor: 'warden_cor',
  cor: 'warden_cor',
  // The Lifting House crew + the Booji-Wooji Man (S4, Pearlmoor — bespoke sheets).
  booji_paul: 'booji_paul',
  lifter_andy: 'lifter_andy',
  lifter_andrew: 'lifter_andrew',
  lifter_abdul: 'lifter_abdul',
  lifter_sid: 'lifter_sid',
  lifter_rot: 'lifter_rot',
  // Generic, reusable townsfolk archetypes — drop these on any NpcPlacement.sprite.
  npc_man: 'npc_man',
  npc_woman: 'npc_woman',
  npc_old_man: 'npc_old_man',
  npc_old_woman: 'npc_old_woman',
  // Gran (tinderwick_house) — her own sheet, not the generic old-woman.
  npc_parent: 'npc_parent',
  npc_boy: 'npc_boy',
  npc_girl: 'npc_girl',
  // 'npc_child' is the long-standing generic-kid key; point it at the boy sheet.
  npc_child: 'npc_boy',
};

/** Placeholder body colours so distinct NPCs read apart before real walk-sheets. */
const SPRITE_COLORS: Record<string, string> = {
  npc_mentor: COLORS.bone,
  npc_child: COLORS.grass,
  npc_boy: COLORS.grass,
  npc_girl: COLORS.diamond,
  npc_man: COLORS.deepBlue,
  npc_woman: COLORS.fire,
  npc_old_man: COLORS.bone,
  npc_old_woman: COLORS.bone,
  wren: COLORS.diamond,
  npc_shopkeeper: COLORS.fire,
  npc_lampwarden: COLORS.deepBlue,
  mira_vael: COLORS.diamond,
  ysolde_frost: COLORS.bone,
  lucan_pyre: COLORS.fire,
  nessa_cole: COLORS.deepBlue,
  warden_cor: COLORS.ink,
  booji_paul: COLORS.bone,
  lifter_andy: COLORS.deepBlue,
  lifter_andrew: COLORS.diamond,
  lifter_abdul: COLORS.grass,
  lifter_sid: COLORS.fire,
  lifter_rot: COLORS.grass,
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
    // Creature NPC whose packed view hasn't loaded yet: fetch it and swap off
    // the placeholder. Safe if the NPC is destroyed first (sprite.active check).
    const kinId = creatureKinId(placement.sprite);
    if (kinId !== null && !scene.textures.exists(creatureTextureKey(kinId, 'overworld'))) {
      void loadCreatureSprite(scene, kinId, 'overworld').then((key) => {
        if (key && this.sprite.active) this.setStaticTexture(key);
      });
    }
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
    const kinId = creatureKinId(placement.sprite);
    if (kinId !== null) {
      const key = creatureTextureKey(kinId, 'overworld');
      // Already loaded (e.g. a map revisit) → use it now; else fall through to
      // the placeholder and let the constructor's lazy load swap it in.
      if (scene.textures.exists(key)) return [key, STATIC_FRAMES];
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
