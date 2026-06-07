/**
 * WorldScene — the overworld. Owns the loaded map, the player, NPCs, the camera,
 * collision, and map music. Movement is grid-based and the camera follows the
 * player, clamped to the map. Warps / triggers / encounters plug into the
 * `onPlayerArrive` seam in later phases; this phase delivers "walk around a town".
 */
import Phaser from 'phaser';
import { COLORS } from '@game/config';
import { theme } from '@game/ui/theme';
import { DebugOverlay } from '@game/ui/DebugOverlay';
import { InputController } from '@game/systems/input/InputController';
import { loadMap, RuntimeMap } from '@game/systems/world/MapLoader';
import { renderMap } from '@game/systems/world/MapRenderer';
import type { MapRenderResult } from '@game/systems/world/MapRenderer';
import { CollisionGrid } from '@game/systems/world/CollisionGrid';
import { MusicDirector } from '@game/systems/audio/MusicDirector';
import { Sfx } from '@game/systems/audio/Sfx';
import { FlagStore } from '@game/systems/flags/FlagStore';
import { Player } from '@game/entities/Player';
import { Npc } from '@game/entities/Npc';
import { VESPERHOLM_GRAPH } from '@game/data/world/graph';
import type { AbilityId, Facing } from '@game/data/world/types';

export interface WorldSceneData {
  mapId: string;
  spawn?: { tx: number; ty: number; facing?: Facing };
  flags?: Record<string, boolean>;
  abilities?: AbilityId[];
}

/** Depth band for actors: above deco (5), below the 'above' layer (20). */
const ACTOR_DEPTH = 10;

export class WorldScene extends Phaser.Scene {
  private ready = false;
  private controller!: InputController;
  private flags!: FlagStore;
  private abilities!: Set<AbilityId>;
  private music!: MusicDirector;
  private sfx!: Sfx;
  private debug!: DebugOverlay;

  private map!: RuntimeMap;
  private collision!: CollisionGrid;
  private render?: MapRenderResult;
  private player!: Player;
  private npcs: Npc[] = [];

  constructor() {
    super('World');
  }

  create(data: WorldSceneData): void {
    this.ready = false;
    this.npcs = [];
    this.cameras.main.setBackgroundColor(COLORS.night);
    this.controller = new InputController(this);
    this.flags = new FlagStore(data.flags);
    this.abilities = new Set(data.abilities ?? []);
    this.music = new MusicDirector(this);
    this.sfx = new Sfx(this);
    this.debug = new DebugOverlay(this);

    void this.build(data);
  }

  private async build(data: WorldSceneData): Promise<void> {
    const map = await loadMap(data.mapId);
    this.map = map;
    this.collision = new CollisionGrid(map);
    this.render = await renderMap(this, map);

    this.cameras.main.setBounds(0, 0, this.render.pixelWidth, this.render.pixelHeight);

    const spawn = this.resolveSpawn(data);
    this.player = new Player(this, spawn.tx, spawn.ty, spawn.facing ?? 'down');
    this.cameras.main.startFollow(this.player.sprite, true, 1, 1);

    this.spawnNpcs();

    if (map.def.music) {
      const key = map.def.music.split('/').pop()?.replace(/\.[a-z0-9]+$/i, '') ?? 'map-music';
      void this.music.play(key, map.def.music);
    }

    this.cameras.main.fadeIn(theme.transition.fadeMs, 0, 0, 0);
    this.ready = true;
  }

  /** New-game spawn: explicit > graph start (if this is the start map) > map centre. */
  private resolveSpawn(data: WorldSceneData): { tx: number; ty: number; facing?: Facing } {
    let tx: number;
    let ty: number;
    let facing: Facing | undefined;
    if (data.spawn) {
      tx = data.spawn.tx;
      ty = data.spawn.ty;
      facing = data.spawn.facing;
    } else if (data.mapId === VESPERHOLM_GRAPH.start_map) {
      tx = VESPERHOLM_GRAPH.start_at.tx;
      ty = VESPERHOLM_GRAPH.start_at.ty;
    } else {
      tx = Math.floor(this.map.width / 2);
      ty = Math.floor(this.map.height / 2);
    }
    const safe = this.findSafeTile(tx, ty);
    return { ...safe, facing };
  }

  /** Clamp into bounds, then spiral out to the nearest passable, unoccupied tile. */
  private findSafeTile(tx: number, ty: number): { tx: number; ty: number } {
    const cx = Phaser.Math.Clamp(tx, 0, this.map.width - 1);
    const cy = Phaser.Math.Clamp(ty, 0, this.map.height - 1);
    if (!this.collision.isBlocked(cx, cy, this.abilities)) return { tx: cx, ty: cy };
    for (let r = 1; r < Math.max(this.map.width, this.map.height); r++) {
      for (let dy = -r; dy <= r; dy++) {
        for (let dx = -r; dx <= r; dx++) {
          const nx = cx + dx;
          const ny = cy + dy;
          if (this.map.inBounds(nx, ny) && !this.collision.isBlocked(nx, ny, this.abilities)) {
            return { tx: nx, ty: ny };
          }
        }
      }
    }
    return { tx: cx, ty: cy };
  }

  private spawnNpcs(): void {
    for (const placement of this.map.def.npcs) {
      if (placement.requires_flag && !this.flags.get(placement.requires_flag)) continue;
      if (placement.hidden_when_flag && this.flags.get(placement.hidden_when_flag)) continue;
      this.npcs.push(new Npc(this, placement));
    }
  }

  private occupiedByNpc(tx: number, ty: number): boolean {
    return this.npcs.some((n) => n.tx === tx && n.ty === ty);
  }

  /** Can the player enter this tile? Collision + NPC bodies. */
  private playerCanEnter = (tx: number, ty: number): boolean => {
    if (this.collision.isBlocked(tx, ty, this.abilities)) return false;
    if (this.occupiedByNpc(tx, ty)) return false;
    return true;
  };

  /** Can an NPC enter this tile? Collision + the player + other NPCs. */
  private npcCanEnter = (tx: number, ty: number): boolean => {
    if (this.collision.isBlocked(tx, ty, this.abilities)) return false;
    if (this.player && this.player.tx === tx && this.player.ty === ty) return false;
    if (this.occupiedByNpc(tx, ty)) return false;
    return true;
  };

  private onPlayerArrive = (_tx: number, _ty: number): void => {
    void this.sfx.playVariant('world-footstep', ['a', 'b']);
    // Warp / trigger / encounter checks land here in later phases.
  };

  update(_time: number, delta: number): void {
    if (!this.ready) return;
    this.controller.update();

    this.player.update(this.controller, this.playerCanEnter, this.onPlayerArrive);
    for (const npc of this.npcs) npc.update(delta, this.npcCanEnter);

    this.player.syncDepth(ACTOR_DEPTH);
    for (const npc of this.npcs) npc.syncDepth(ACTOR_DEPTH);

    this.debug.set([
      `map: ${this.map.def.id}`,
      `tile: ${this.player.tx},${this.player.ty}`,
      `facing: ${this.player.facing}`,
      `npcs: ${this.npcs.length}`,
    ]);
  }
}
