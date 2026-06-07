/**
 * WorldScene — the overworld. Owns the loaded map, the player, NPCs, the camera,
 * collision, and map music, and handles the moment-to-moment loop: grid movement,
 * talking to NPCs / reading signs (Confirm), step-on and interact warps between maps
 * (with transitions), and step-on triggers. Encounters → battle plug into
 * `onPlayerArrive` once the battle scene exists. A modal flag pauses movement while
 * dialogue or a menu is open.
 */
import Phaser from 'phaser';
import { COLORS } from '@game/config';
import { theme } from '@game/ui/theme';
import { DebugOverlay } from '@game/ui/DebugOverlay';
import { DialogueBox } from '@game/ui/DialogueBox';
import { fadeIn, fadeOut } from '@game/ui/Transitions';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { loadMap, RuntimeMap } from '@game/systems/world/MapLoader';
import { renderMap } from '@game/systems/world/MapRenderer';
import type { MapRenderResult } from '@game/systems/world/MapRenderer';
import { CollisionGrid } from '@game/systems/world/CollisionGrid';
import { MusicDirector } from '@game/systems/audio/MusicDirector';
import { Sfx } from '@game/systems/audio/Sfx';
import { FlagStore } from '@game/systems/flags/FlagStore';
import { Player } from '@game/entities/Player';
import { Npc } from '@game/entities/Npc';
import { getDialogue } from '@game/content/dialogue';
import { MAP_REGISTRY } from '@game/data/world/maps';
import { VESPERHOLM_GRAPH } from '@game/data/world/graph';
import type { AbilityId, Facing, Warp, EventTrigger } from '@game/data/world/types';

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
  private modal = false;
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
    this.modal = false;
    this.controller = new InputController(this);
    this.flags = new FlagStore(data.flags);
    this.abilities = new Set(data.abilities ?? []);
    this.music = new MusicDirector(this);
    this.sfx = new Sfx(this);
    this.debug = new DebugOverlay(this);
    this.cameras.main.setBackgroundColor(COLORS.night);

    const spawn = data.spawn ?? this.defaultSpawn(data.mapId);
    void this.enterMap(data.mapId, spawn, spawn.facing, true);
  }

  private defaultSpawn(mapId: string): { tx: number; ty: number; facing?: Facing } {
    if (mapId === VESPERHOLM_GRAPH.start_map) {
      return { tx: VESPERHOLM_GRAPH.start_at.tx, ty: VESPERHOLM_GRAPH.start_at.ty };
    }
    return { tx: 0, ty: 0 };
  }

  /** Tear down any current map and build the requested one, placing the player. */
  private async enterMap(
    mapId: string,
    spawn: { tx: number; ty: number },
    facing: Facing | undefined,
    initial: boolean,
  ): Promise<void> {
    this.ready = false;
    this.teardownMap();

    const map = await loadMap(mapId);
    this.map = map;
    this.collision = new CollisionGrid(map);
    this.render = await renderMap(this, map);
    this.cameras.main.setBounds(0, 0, this.render.pixelWidth, this.render.pixelHeight);

    const safe = this.findSafeTile(spawn.tx, spawn.ty);
    this.player = new Player(this, safe.tx, safe.ty, facing ?? 'down');
    this.cameras.main.startFollow(this.player.sprite, true, 1, 1);

    this.spawnNpcs();

    if (map.def.music) {
      const key = map.def.music.split('/').pop()?.replace(/\.[a-z0-9]+$/i, '') ?? 'map-music';
      void this.music.play(key, map.def.music);
    }

    if (initial) this.cameras.main.fadeIn(theme.transition.fadeMs, 0, 0, 0);
    this.ready = true;
  }

  private teardownMap(): void {
    this.cameras.main.stopFollow();
    this.player?.destroy();
    for (const npc of this.npcs) npc.destroy();
    this.npcs = [];
    this.render?.tilemap.destroy();
    this.render = undefined;
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

  private npcAt(tx: number, ty: number): Npc | undefined {
    return this.npcs.find((n) => n.tx === tx && n.ty === ty);
  }

  private playerCanEnter = (tx: number, ty: number): boolean => {
    if (this.collision.isBlocked(tx, ty, this.abilities)) return false;
    if (this.npcAt(tx, ty)) return false;
    return true;
  };

  private npcCanEnter = (tx: number, ty: number): boolean => {
    if (this.collision.isBlocked(tx, ty, this.abilities)) return false;
    if (this.player && this.player.tx === tx && this.player.ty === ty) return false;
    if (this.npcAt(tx, ty)) return false;
    return true;
  };

  // --- Interaction (Confirm) ----------------------------------------------

  private async interact(): Promise<void> {
    const ahead = this.player.tileAhead();

    const npc = this.npcAt(ahead.tx, ahead.ty);
    if (npc) {
      npc.facePoint(this.player.tx, this.player.ty);
      await this.runDialogue(npc.dialogueRef);
      return;
    }

    const trigger = this.map.def.triggers.find(
      (t) => t.activation === 'interact' && t.at.tx === ahead.tx && t.at.ty === ahead.ty,
    );
    if (trigger) {
      await this.handleTrigger(trigger);
      return;
    }

    const warp = this.map.def.warps.find(
      (w) => w.trigger === 'interact' && w.at.tx === ahead.tx && w.at.ty === ahead.ty,
    );
    if (warp) await this.executeWarp(warp);
  }

  private async runDialogue(ref: string | undefined): Promise<void> {
    this.modal = true;
    await new DialogueBox(this, this.sfx).run(getDialogue(ref));
    this.modal = false;
  }

  private async handleTrigger(trigger: EventTrigger): Promise<void> {
    if (trigger.requires_flag && !this.flags.get(trigger.requires_flag)) return;
    if (trigger.once && this.flags.triggerFired(trigger.id)) return;

    // Script / cutscene triggers wait for the cutscene system (next phase).
    if (trigger.kind === 'script' || trigger.kind === 'cutscene') return;

    await this.runDialogue(trigger.ref);
    this.flags.setMany(trigger.sets_flags);
    if (trigger.once) this.flags.markTriggerFired(trigger.id);
  }

  // --- Step-on (on arrival) -----------------------------------------------

  private onPlayerArrive = (tx: number, ty: number): void => {
    void this.sfx.playVariant('world-footstep', ['a', 'b']);

    const warp = this.map.def.warps.find(
      (w) => w.trigger === 'step_on' && w.at.tx === tx && w.at.ty === ty,
    );
    if (warp) {
      void this.executeWarp(warp);
      return;
    }

    const trigger = this.map.def.triggers.find(
      (t) => t.activation === 'step_on' && t.at.tx === tx && t.at.ty === ty,
    );
    if (trigger) void this.handleTrigger(trigger);
    // Encounter checks plug in here once the battle scene exists.
  };

  private warpAllowed(warp: Warp): boolean {
    if (warp.requires_ability && !this.abilities.has(warp.requires_ability)) return false;
    if (warp.requires_flag && !this.flags.get(warp.requires_flag)) return false;
    return true;
  }

  private async executeWarp(warp: Warp): Promise<void> {
    if (!this.warpAllowed(warp)) return;
    // Tolerant: ignore warps whose target map isn't authored/registered yet.
    if (!MAP_REGISTRY[warp.to_map]) return;
    this.modal = true;
    void this.sfx.play(warp.transition === 'door' ? 'world-door-open' : 'world-warp');
    await fadeOut(this, warp.transition === 'door' ? theme.transition.doorMs : theme.transition.fadeMs);
    await this.enterMap(warp.to_map, warp.to, warp.facing, false);
    await fadeIn(this, theme.transition.fadeMs);
    this.modal = false;
  }

  // --- Loop ----------------------------------------------------------------

  update(_time: number, delta: number): void {
    if (!this.ready) return;
    this.controller.update();

    if (!this.modal) {
      if (!this.player.isMoving && this.controller.justPressed(InputAction.Confirm)) {
        void this.interact();
      } else {
        this.player.update(this.controller, this.playerCanEnter, this.onPlayerArrive);
      }
      for (const npc of this.npcs) npc.update(delta, this.npcCanEnter);
    }

    this.player.syncDepth(ACTOR_DEPTH);
    for (const npc of this.npcs) npc.syncDepth(ACTOR_DEPTH);

    this.debug.set([
      `map: ${this.map.def.id}`,
      `tile: ${this.player.tx},${this.player.ty} (${this.player.facing})`,
      `npcs: ${this.npcs.length}  flags: ${Object.keys(this.flags.snapshot()).length}`,
      `modal: ${this.modal}`,
    ]);
  }
}
