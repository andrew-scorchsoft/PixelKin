/**
 * WorldScene — the overworld. Owns the loaded map, the player, NPCs, the camera,
 * collision, and map music, and handles the moment-to-moment loop: grid movement,
 * talking to NPCs / reading signs (Confirm), step-on and interact warps between maps
 * (with transitions), and step-on triggers. Encounters → battle plug into
 * `onPlayerArrive` once the battle scene exists. A modal flag pauses movement while
 * dialogue or a menu is open.
 */
import Phaser from 'phaser';
import { COLORS, TILE_SIZE } from '@game/config';
import { theme } from '@game/ui/theme';
import { makeText } from '@game/ui/Text';
import { DebugOverlay } from '@game/ui/DebugOverlay';
import { DialogueBox } from '@game/ui/DialogueBox';
import { Menu } from '@game/ui/Menu';
import { PartyMenu } from '@game/ui/PartyMenu';
import { ItemsMenu } from '@game/ui/ItemsMenu';
import { HearthMenu } from '@game/ui/HearthMenu';
import { SettingsMenu } from '@game/ui/SettingsMenu';
import { GlossaryMenu } from '@game/ui/GlossaryMenu';
import { RegisterMenu } from '@game/ui/RegisterMenu';
import { ChartsMenu } from '@game/ui/ChartsMenu';
import { ChartView } from '@game/ui/ChartView';
import { fadeIn, fadeOut } from '@game/ui/Transitions';
import { KinInstance } from '@game/systems/party/KinInstance';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { loadMap, RuntimeMap } from '@game/systems/world/MapLoader';
import { renderMap, tickAnimatedTiles } from '@game/systems/world/MapRenderer';
import type { MapRenderResult } from '@game/systems/world/MapRenderer';
import { CollisionGrid } from '@game/systems/world/CollisionGrid';
import { EncounterSystem } from '@game/systems/world/EncounterSystem';
import { loadCreatureSprite } from '@game/systems/sprites/CreatureSprites';
import type { BattleRequest, BattleResult } from '@game/scenes/BattleScene';
import { MusicDirector } from '@game/systems/audio/MusicDirector';
import { Sfx } from '@game/systems/audio/Sfx';
import { FlagStore } from '@game/systems/flags/FlagStore';
import { Player } from '@game/entities/Player';
import { Npc } from '@game/entities/Npc';
import type { Actor } from '@game/entities/Actor';
import { getDialogue } from '@game/content/dialogue';
import { getScript } from '@game/content/scripts';
import { getShop } from '@game/content/shops';
import { chartForMap, chartFlag } from '@game/content/charts';
import type { ChartEntry } from '@game/content/types';
import { STARTING_WICKS, faintTithe } from '@game/content/economy';
import { ShopMenu } from '@game/ui/ShopMenu';
import { makeStarterKin } from '@game/content/starters';
import { runCutscene } from '@game/systems/cutscene/CutsceneRunner';
import type { CutsceneContext } from '@game/systems/cutscene/CutsceneRunner';
import type { ActorRef, CutsceneStep } from '@game/content/types';
import type { KinInstanceData, InventoryData, SaveGame, DexProgress } from '@game/systems/save/types';
import { SAVE_SCHEMA_VERSION } from '@game/systems/save/types';
import { SaveManager } from '@game/systems/save/SaveManager';
import type { WorldSnapshot } from '@game/data/world/types';
import { MAP_REGISTRY } from '@game/data/world/maps';
import { VESPERHOLM_GRAPH } from '@game/data/world/graph';
import type { AbilityId, Facing, Warp, EventTrigger, NpcPlacement } from '@game/data/world/types';

export interface WorldSceneData {
  mapId: string;
  spawn?: { tx: number; ty: number; facing?: Facing };
  flags?: Record<string, boolean>;
  abilities?: AbilityId[];
  party?: KinInstanceData[];
  /** Kin resting at the Hearth (storage beyond the active party). */
  box?: KinInstanceData[];
  inventory?: InventoryData;
  /** The player's wicks; a fresh game starts on STARTING_WICKS. */
  money?: number;
  /** Collection progress (the vesperlamp's register). */
  dex?: DexProgress;
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
  private encounters!: EncounterSystem;
  private render?: MapRenderResult;
  private player!: Player;
  private npcs: Npc[] = [];

  private party: KinInstanceData[] = [];
  /** Kin kept at the Hearth (storage); overflow from a full lamp lands here. */
  private box: KinInstanceData[] = [];
  private inventory: InventoryData = { items: {} };
  /** The player's wicks (currency — content/economy.ts). */
  private money = 0;
  /** The vesperlamp's register: species seen/caught (REGISTER screen). */
  private dexSeen = new Set<number>();
  private dexCaught = new Set<number>();
  /** A newly-discovered chart awaiting its full-screen reveal (fires when idle). */
  private pendingReveal?: ChartEntry;

  constructor() {
    super('World');
  }

  create(data: WorldSceneData): void {
    this.ready = false;
    this.modal = false;
    this.pendingReveal = undefined;
    this.controller = new InputController(this);
    this.flags = new FlagStore(data.flags);
    this.abilities = new Set(data.abilities ?? []);
    this.party = data.party ?? [];
    this.box = data.box ?? [];
    this.inventory = data.inventory ?? { items: {} };
    this.money = data.money ?? STARTING_WICKS;
    this.dexSeen = new Set(data.dex?.seen ?? []);
    this.dexCaught = new Set(data.dex?.caught ?? []);
    // Whatever walks with you is certainly on the register.
    for (const k of [...this.party, ...this.box]) {
      this.dexSeen.add(k.species_id);
      this.dexCaught.add(k.species_id);
    }
    this.music = new MusicDirector(this);
    this.sfx = new Sfx(this);
    this.debug = new DebugOverlay(this);
    this.cameras.main.setBackgroundColor(COLORS.night);

    // Release music + the global shell-input listener when the scene ends, so a
    // later World restart doesn't stack a second music track or input listener.
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => {
      this.music.stop();
      this.controller.destroy();
    });

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

    try {
      const map = await loadMap(mapId);
      this.map = map;
      this.collision = new CollisionGrid(map);
      this.encounters = new EncounterSystem(map);
      this.render = await renderMap(this, map);
      this.cameras.main.setBounds(0, 0, this.render.pixelWidth, this.render.pixelHeight);

      const safe = this.findSafeTile(spawn.tx, spawn.ty);
      this.player = new Player(this, safe.tx, safe.ty, facing ?? 'down');
      this.cameras.main.startFollow(this.player.sprite, true, 1, 1);

      this.spawnNpcs();
      this.playMapMusic();
      this.warmEncounterSprites();

      if (initial) this.cameras.main.fadeIn(theme.transition.fadeMs, 0, 0, 0);
      this.ready = true;
      this.noteChartDiscovery(mapId);
      void this.persist(); // autosave on entering any map (so Continue always works)
    } catch (err) {
      // A missing/malformed map must not freeze the game on a black screen.
      console.error(`Failed to enter map "${mapId}":`, err);
      this.cameras.main.fadeIn(theme.transition.fadeMs, 0, 0, 0);
      this.modal = false;
    }
  }

  /**
   * Pre-warm the battle sprites for every kin this map's encounter tables can
   * roll, so the FIRST wild battle on a new map never hitches on a lazy load.
   * Fire-and-forget; the tolerant loader no-ops anything already cached.
   */
  private warmEncounterSprites(): void {
    const ids = new Set<number>();
    for (const zone of this.map.def.encounters) {
      for (const entry of zone.table) ids.add(entry.kin_id);
    }
    for (const id of ids) void loadCreatureSprite(this, id, 'front');
  }

  /** Play (or resume) the current map's music loop. */
  private playMapMusic(): void {
    const music = this.map?.def.music;
    if (!music) return;
    const key = music.split('/').pop()?.replace(/\.[a-z0-9]+$/i, '') ?? 'map-music';
    void this.music.play(key, music);
  }

  /** Snapshot the live world state into the canonical save shape. */
  private buildSnapshot(): WorldSnapshot {
    return {
      current_map: this.map.def.id,
      player: { tx: this.player.tx, ty: this.player.ty, facing: this.player.facing },
      abilities: [...this.abilities],
      flags: this.flags.snapshot(),
      schema_version: SAVE_SCHEMA_VERSION,
    };
  }

  /** Build the full save blob from live state. */
  private buildSaveGame(): SaveGame {
    return {
      schema_version: SAVE_SCHEMA_VERSION,
      saved_at: Date.now(),
      play_seconds: 0,
      world: this.buildSnapshot(),
      party: this.party,
      box: this.box,
      inventory: this.inventory,
      money: this.money,
      dex: { seen: [...this.dexSeen], caught: [...this.dexCaught] },
    };
  }

  /** Autosave through the storage seam (with a quiet corner glyph so the player
   *  knows the lamp is keeping their place). */
  async persist(): Promise<void> {
    await SaveManager.save(this.buildSaveGame());
    this.flashSaveGlyph();
  }

  private saveGlyph?: Phaser.GameObjects.Text;
  private flashSaveGlyph(): void {
    if (this.saveGlyph) return; // one at a time is plenty
    const { width, height } = this.cameras.main;
    this.saveGlyph = makeText(this, width - 4, height - 4, 'SAVED', theme.text.dim)
      .setOrigin(1, 1)
      .setScrollFactor(0)
      .setDepth(theme.depth.overlayDim + 1)
      .setAlpha(0);
    this.tweens.add({
      targets: this.saveGlyph,
      alpha: 0.85,
      duration: 250,
      yoyo: true,
      hold: 700,
      onComplete: () => {
        this.saveGlyph?.destroy();
        this.saveGlyph = undefined;
      },
    });
  }

  private teardownMap(): void {
    this.cameras.main.stopFollow();
    this.player?.destroy();
    for (const npc of this.npcs) npc.destroy();
    this.npcs = [];
    for (const o of this.render?.objects ?? []) o.destroy();
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

  private npcVisible(placement: NpcPlacement): boolean {
    if (placement.requires_flag && !this.flags.get(placement.requires_flag)) return false;
    if (placement.hidden_when_flag && this.flags.get(placement.hidden_when_flag)) return false;
    return true;
  }

  /** A hidden trigger is GONE (it must not swallow the step's warp/encounter roll),
   *  unlike a requires_flag one, which stays present to deliver its blocked_ref. */
  private triggerActive(trigger: EventTrigger): boolean {
    return !(trigger.hidden_when_flag && this.flags.get(trigger.hidden_when_flag));
  }

  private spawnNpcs(): void {
    for (const placement of this.map.def.npcs) {
      if (this.npcVisible(placement)) this.npcs.push(new Npc(this, placement));
    }
  }

  /** Re-evaluate flag-conditional NPCs after flags change (a picked-up item
   *  cache vanishes immediately; a festival crowd appears without a re-entry). */
  private refreshNpcs(): void {
    this.npcs = this.npcs.filter((npc) => {
      if (this.npcVisible(npc.placement)) return true;
      npc.destroy();
      return false;
    });
    for (const placement of this.map.def.npcs) {
      if (!this.npcVisible(placement)) continue;
      if (this.npcs.some((n) => n.placement === placement)) continue;
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
      // An NPC whose dialogue_ref is a script runs it as a cutscene (inn rest,
      // item caches, festival beats) — NPCs stay pure data either way.
      if (npc.dialogueRef?.startsWith('script.')) {
        const steps = getScript(npc.dialogueRef);
        if (steps) {
          this.modal = true;
          const completed = await runCutscene(this.cutsceneContext(), steps);
          if (completed) void this.persist();
          this.modal = false;
          this.refreshNpcs();
        }
        return;
      }
      await this.runDialogue(npc.dialogueRef);
      return;
    }

    const trigger = this.map.def.triggers.find(
      (t) =>
        t.activation === 'interact' &&
        t.at.tx === ahead.tx &&
        t.at.ty === ahead.ty &&
        this.triggerActive(t),
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
    if (trigger.requires_flag && !this.flags.get(trigger.requires_flag)) {
      // If the player actively tried this, tell them it's not ready yet —
      // with the trigger's own "not yet" dialogue when it has one.
      if (trigger.blocked_ref) await this.runDialogue(trigger.blocked_ref);
      else if (trigger.activation === 'interact') await this.showHint();
      return;
    }
    if (trigger.once && this.flags.triggerFired(trigger.id)) return;

    if (trigger.kind === 'script' || trigger.kind === 'cutscene') {
      const steps = getScript(trigger.ref);
      if (!steps) return;
      this.modal = true;
      const completed = await runCutscene(this.cutsceneContext(), steps);
      // Only bank progress if the scene actually finished (a lost battle aborts it).
      if (completed) {
        this.flags.setMany(trigger.sets_flags);
        if (trigger.once) this.flags.markTriggerFired(trigger.id);
        void this.persist();
      }
      this.modal = false;
      this.refreshNpcs();
      return;
    }

    await this.runDialogue(trigger.ref);
    this.flags.setMany(trigger.sets_flags);
    if (trigger.once) this.flags.markTriggerFired(trigger.id);
  }

  /** A short "the way is shut" message when a gated thing isn't ready. */
  private async showHint(): Promise<void> {
    this.modal = true;
    await new DialogueBox(this, this.sfx).run([
      { text: 'It is not time yet — something is still needed here.' },
    ]);
    this.modal = false;
  }

  private cutsceneContext(): CutsceneContext {
    return {
      scene: this,
      sfx: this.sfx,
      music: this.music,
      flags: this.flags,
      getActor: (ref: ActorRef): Actor | undefined =>
        ref === 'player' ? this.player : this.npcs.find((n) => n.id === ref),
      canEnter: (tx, ty) => this.playerCanEnter(tx, ty),
      onGiveStarter: (speciesId) => {
        this.party.push(makeStarterKin(speciesId));
        this.dexSeen.add(speciesId);
        this.dexCaught.add(speciesId);
      },
      onGiveItem: (item, count) => {
        this.inventory.items[item] = (this.inventory.items[item] ?? 0) + count;
      },
      onGiveMoney: (amount) => {
        this.money = Math.max(0, this.money + Math.floor(amount));
      },
      openShop: async (shopId) => {
        const shop = getShop(shopId);
        if (!shop) {
          await ShopMenu.missing(this, this.sfx);
          return;
        }
        const result = await new ShopMenu(this, shop, this.inventory, this.money, this.sfx, (flag) =>
          this.flags.get(flag),
        ).run();
        this.inventory = result.inventory;
        this.money = result.money;
        void this.persist();
      },
      onHealParty: () => {
        this.healParty();
      },
      startTrainerBattle: async (trainer: string): Promise<boolean> => {
        const result = await this.startBattle({
          kind: 'trainer',
          trainer,
          party: this.party,
          box: this.box,
          inventory: this.inventory,
        });
        if (result.outcome !== 'win') {
          await this.blackout();
          return false;
        }
        return true;
      },
      cameraFocusTile: (tx, ty, ms, zoom) => this.cameraFocusTile(tx, ty, ms, zoom),
      cameraReset: (ms) => this.cameraResetToPlayer(ms),
    };
  }

  /** Pan (and optionally zoom) the camera onto a world tile's centre for a beat. */
  private cameraFocusTile(tx: number, ty: number, ms: number, zoom?: number): Promise<void> {
    const cam = this.cameras.main;
    cam.stopFollow();
    const x = tx * TILE_SIZE + TILE_SIZE / 2;
    const y = ty * TILE_SIZE + TILE_SIZE / 2;
    if (zoom && zoom !== cam.zoom) cam.zoomTo(zoom, ms, 'Sine.easeInOut');
    return new Promise((resolve) => {
      cam.pan(x, y, ms, 'Sine.easeInOut', false, (_c, progress) => {
        if (progress >= 1) resolve();
      });
    });
  }

  /** Restore the standard follow-the-player framing and zoom after a focus. */
  private cameraResetToPlayer(ms: number): Promise<void> {
    const cam = this.cameras.main;
    if (cam.zoom !== 1) cam.zoomTo(1, ms, 'Sine.easeInOut');
    return new Promise((resolve) => {
      cam.pan(this.player.sprite.x, this.player.sprite.y, ms, 'Sine.easeInOut', false, (_c, progress) => {
        if (progress >= 1) {
          cam.startFollow(this.player.sprite, true, 1, 1);
          resolve();
        }
      });
    });
  }

  // --- Route-trainer line of sight ------------------------------------------

  /** True if this NPC is an undefeated sight-trainer with the player in its
   *  unobstructed straight-ahead line. */
  private npcSeesPlayer(npc: Npc): boolean {
    const p = npc.placement;
    const range = p.sight_range ?? 0;
    if (!range || !p.dialogue_ref?.startsWith('script.')) return false;
    if (p.defeated_flag && this.flags.get(p.defeated_flag)) return false;
    const delta: Record<Facing, { dx: number; dy: number }> = {
      down: { dx: 0, dy: 1 },
      up: { dx: 0, dy: -1 },
      left: { dx: -1, dy: 0 },
      right: { dx: 1, dy: 0 },
    };
    const { dx, dy } = delta[npc.facing];
    for (let i = 1; i <= range; i++) {
      const cx = npc.tx + dx * i;
      const cy = npc.ty + dy * i;
      if (this.player.tx === cx && this.player.ty === cy) return true;
      if (this.collision.isBlocked(cx, cy, this.abilities)) return false;
      if (this.npcAt(cx, cy)) return false;
    }
    return false;
  }

  /** The classic challenge: alert (!), march up to the player, face off, run
   *  the trainer's script (battle inside), bank the defeated flag on a win. */
  private async engageTrainer(npc: Npc): Promise<void> {
    const steps = getScript(npc.dialogueRef ?? '');
    if (!steps) return;
    this.modal = true;
    void this.sfx.playVariant('ui-confirm', ['a', 'b']);
    await npc.showEmote('alert');
    // march to the tile adjacent to the player along the (axis-aligned) line,
    // then face off before the script's first line
    const sx = Math.sign(this.player.tx - npc.tx);
    const sy = Math.sign(this.player.ty - npc.ty);
    const npcFacing: Facing = sx > 0 ? 'right' : sx < 0 ? 'left' : sy > 0 ? 'down' : 'up';
    const playerFacing: Facing = sx > 0 ? 'left' : sx < 0 ? 'right' : sy > 0 ? 'up' : 'down';
    const approach: CutsceneStep[] = [
      { op: 'move', actor: npc.id, to: { tx: this.player.tx - sx, ty: this.player.ty - sy } },
      { op: 'face', actor: npc.id, facing: npcFacing },
      { op: 'face', actor: 'player', facing: playerFacing },
    ];
    const completed = await runCutscene(this.cutsceneContext(), [...approach, ...steps]);
    if (completed) {
      if (npc.placement.defeated_flag) this.flags.set(npc.placement.defeated_flag, true);
      void this.persist();
    }
    this.modal = false;
    this.refreshNpcs();
  }

  // --- Step-on (on arrival) -----------------------------------------------

  private onPlayerArrive = (tx: number, ty: number): void => {
    if (this.modal) return; // a warp/cutscene/battle is already in progress
    void this.sfx.playVariant('world-footstep', ['a', 'b']);

    // First time a Lantern Gift carries you onto its gated ground, mark the
    // moment — the lamp raised, a wash of its light. Once per Gift.
    const gift = this.collision.gateAt(tx, ty);
    if (gift && this.abilities.has(gift) && !this.flags.get(`flag:gift_first_${gift}`)) {
      this.flags.set(`flag:gift_first_${gift}`, true);
      void this.playGiftFlourish(gift);
      return;
    }

    const warp = this.map.def.warps.find(
      (w) => w.trigger === 'step_on' && w.at.tx === tx && w.at.ty === ty,
    );
    if (warp) {
      void this.executeWarp(warp);
      return;
    }

    const trigger = this.map.def.triggers.find(
      (t) => t.activation === 'step_on' && t.at.tx === tx && t.at.ty === ty && this.triggerActive(t),
    );
    if (trigger) {
      void this.handleTrigger(trigger);
      return;
    }

    // Route trainers: stepping into a trainer's line of sight starts the
    // challenge (and pre-empts a same-step wild encounter, like the classics).
    const spotter = this.npcs.find((n) => this.npcSeesPlayer(n));
    if (spotter) {
      void this.engageTrainer(spotter);
      return;
    }

    // Wild encounter — only if we have a kin able to fight.
    if (this.hasHealthyKin()) {
      const intent = this.encounters.roll(tx, ty, this.abilities, (flag) => this.flags.get(flag));
      if (intent) {
        void this.startBattle({
          kind: 'wild',
          species_id: intent.species_id,
          level: intent.level,
          terrain: intent.terrain,
          party: this.party,
          box: this.box,
          inventory: this.inventory,
        }).then((result) => {
          if (result.outcome === 'lose') void this.blackout();
        });
      }
    }
  };

  private hasHealthyKin(): boolean {
    return this.party.some((k) => k.hp > 0);
  }

  // --- Battle bridge -------------------------------------------------------

  /** Launch a battle over the (paused) overworld; resolve when it returns. */
  private startBattle(request: BattleRequest): Promise<BattleResult> {
    return new Promise((resolve) => {
      this.modal = true;
      this.music.stop(); // hand the soundtrack over to the battle scene
      const onComplete = (result: BattleResult): void => {
        this.applyBattleResult(result);
        this.scene.resume('World');
        this.playMapMusic(); // restore the overworld loop
        this.modal = false;
        resolve(result);
      };
      this.scene.launch('Battle', { ...request, onComplete, mapId: this.map.def.id });
      this.scene.pause();
    });
  }

  private applyBattleResult(result: BattleResult): void {
    this.party = result.party;
    this.box = result.box;
    this.inventory = result.inventory;
    if (result.money_earned) this.money += result.money_earned;
    if (result.set_flags) this.flags.setMany(result.set_flags);
    for (const id of result.dex_seen ?? []) this.dexSeen.add(id);
    if (result.caught) {
      this.dexSeen.add(result.caught.species_id);
      this.dexCaught.add(result.caught.species_id);
    }
    // A kindle mid-battle puts the new form on the register too.
    for (const k of [...this.party, ...this.box]) {
      this.dexSeen.add(k.species_id);
      this.dexCaught.add(k.species_id);
    }
    // Lantern Gifts granted by a Lampwarden win — add to the live ability set so
    // gated tiles/warps unlock immediately, and persist() (below) saves them.
    if (result.grant_abilities) {
      for (const a of result.grant_abilities) this.abilities.add(a);
    }
    void this.persist();
  }

  /** Defeat recovery: revive the party and wake back at the start town. */
  private async blackout(): Promise<void> {
    this.modal = true;
    this.healParty();
    // The kind light keeps a small tithe of wicks (10%) — losing costs, gently.
    const tithe = faintTithe(this.money);
    this.money -= tithe;
    void this.sfx.playVariant('world-heal', ['a', 'b']);
    await new DialogueBox(this, this.sfx).run([
      { text: 'Your lamp guttered low... but a kind light carried you home.' },
      ...(tithe > 0 ? [{ text: `You left ${tithe} wicks in thanks, as the custom asks.` }] : []),
    ]);
    await fadeOut(this);
    await this.enterMap(VESPERHOLM_GRAPH.start_map, VESPERHOLM_GRAPH.start_at, 'down', false);
    await fadeIn(this);
    this.modal = false;
  }

  /** Fully restore every kin in the party (used by blackout recovery). */
  private healParty(): void {
    this.party = this.party.map((d) => {
      const kin = KinInstance.fromData(d);
      kin.fullHeal();
      return kin.toData();
    });
  }

  private warpAllowed(warp: Warp): boolean {
    if (warp.requires_ability && !this.abilities.has(warp.requires_ability)) return false;
    if (warp.requires_flag && !this.flags.get(warp.requires_flag)) return false;
    return true;
  }

  private async executeWarp(warp: Warp): Promise<void> {
    if (!this.warpAllowed(warp)) {
      // A gated warp with its own "not yet" line delivers it in-voice (step_on
      // included — the player walked into a chained gate); otherwise only an
      // active interact gets the generic hint.
      if (warp.blocked_ref) await this.runDialogue(warp.blocked_ref);
      else if (warp.trigger === 'interact') await this.showHint();
      return;
    }
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

  update(time: number, delta: number): void {
    if (!this.ready) return;
    // Cycle water/lamp/etc. frames — keeps the world breathing even while a
    // dialogue or menu is open (movement is what a modal pauses, not the scenery).
    if (this.render) tickAnimatedTiles(this.render.animatedTiles, time);
    this.controller.update();

    if (!this.modal) {
      if (this.pendingReveal) {
        const chart = this.pendingReveal;
        this.pendingReveal = undefined;
        void this.revealChart(chart);
        return;
      }
      if (this.controller.justPressed(InputAction.Menu)) {
        void this.openPauseMenu();
      } else if (!this.player.isMoving && this.controller.justPressed(InputAction.Confirm)) {
        void this.interact();
      } else {
        this.player.update(
          this.controller,
          this.playerCanEnter,
          this.onPlayerArrive,
          this.onBump,
          (tx, ty) => this.collision.ledgeAt(tx, ty),
          () => void this.sfx.playVariant('world-ledge-hop', ['a', 'b']),
        );
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

  /**
   * The first time each Lantern Gift carries the player onto its gated ground:
   * raise the lamp, wash the screen in the Gift's light, say its name. Two
   * seconds of ceremony, once per Gift — earning a Gift deserves a moment of
   * using it.
   */
  private async playGiftFlourish(gift: AbilityId): Promise<void> {
    const LOOK: Partial<Record<AbilityId, { color: number; line: string }>> = {
      tidecall: { color: 0x66b8d8, line: 'You raise the lamp, and the night-water stills to let you pass. Tidecall.' },
      glimmerstep: { color: 0xb8d96e, line: 'You raise the lamp, and the dark steps back a stride. Glimmerstep.' },
      updraft_kite: { color: 0xb9c7e8, line: 'You raise the lamp, and the wind takes its warmth — and you with it. Updraft Kite.' },
      emberward: { color: 0xe89a5d, line: 'You raise the lamp, and the coldfog curls away from its ember. Emberward.' },
      sunsketch: { color: 0xf0d77a, line: 'You raise the lamp, and stored daylight blooms ahead of you. Sunsketch.' },
      starreach: { color: 0xcdb9ea, line: 'You raise the lamp, and the void itself holds your weight. Starreach.' },
    };
    const look = LOOK[gift];
    this.modal = true;
    void this.sfx.playVariant('world-gleam', ['a', 'b', 'c']);
    const done = this.player.playAction('raiseLamp', 900);
    if (look) {
      const wash = this.add
        .rectangle(0, 0, this.cameras.main.width, this.cameras.main.height, look.color, 0)
        .setOrigin(0, 0)
        .setScrollFactor(0)
        .setDepth(theme.depth.overlayDim);
      this.tweens.add({ targets: wash, fillAlpha: 0.4, duration: 450, yoyo: true, onComplete: () => wash.destroy() });
    }
    await done;
    if (look) await new DialogueBox(this, this.sfx).run([{ text: look.line }]);
    void this.persist();
    this.modal = false;
  }

  /**
   * First time the player sets foot in a map that belongs to a chart, bank the
   * discovery flag (so it joins the Wayfarer's Charts gallery and survives a save)
   * and queue its full-screen reveal — `update()` fires it on the next idle frame,
   * after any warp fade has settled.
   */
  private noteChartDiscovery(mapId: string): void {
    const chart = chartForMap(mapId);
    if (!chart || this.flags.get(chartFlag(chart))) return;
    this.flags.set(chartFlag(chart));
    this.pendingReveal = chart;
  }

  /**
   * Surface a newly-discovered place: bloom in its concept-art mood piece with a
   * "A NEW CHART" banner + the place's name and mood line, and hold it until the
   * player presses on. Degrades gracefully — missing art shows a framed name card.
   */
  private async revealChart(chart: ChartEntry): Promise<void> {
    this.modal = true;
    void this.sfx.playVariant('world-gleam', ['a', 'b', 'c']);
    const view = new ChartView(this, { mode: 'reveal' });
    // Start the bloom immediately (alpha 0 this same tick, no black pop) while the
    // art loads in behind it, then hold once it's fully bloomed.
    const bloom = view.fadeIn();
    await view.setChart(chart);
    await bloom;
    await this.waitForPress();
    view.destroy();
    this.modal = false;
  }

  /** Resolve on the next Confirm/Cancel press (ignoring one held from before). */
  private waitForPress(): Promise<void> {
    const input = new InputController(this);
    let armed = false;
    return new Promise((resolve) => {
      const tick = (): void => {
        input.update();
        if (!armed) {
          if (!input.isDown(InputAction.Confirm) && !input.isDown(InputAction.Cancel)) armed = true;
          return;
        }
        if (input.justPressed(InputAction.Confirm) || input.justPressed(InputAction.Cancel)) {
          this.events.off(Phaser.Scenes.Events.UPDATE, tick);
          input.destroy();
          resolve();
        }
      };
      this.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  /** Feedback when walking into a wall: a throttled bump sfx + a tiny squash. */
  private lastBumpAt = 0;
  private onBump = (): void => {
    const now = this.time.now;
    if (now - this.lastBumpAt < 280) return;
    this.lastBumpAt = now;
    void this.sfx.playVariant('world-bump', ['a', 'b']);
    this.tweens.add({
      targets: this.player.sprite,
      scaleX: 0.9,
      scaleY: 1.06,
      duration: 70,
      yoyo: true,
    });
  };

  /**
   * Party viewer (pause menu → KIN): see your kin, inspect their stats/moves, and
   * reorder them (slot 0 leads the next battle). Persists the new order on close.
   */
  private async openPartyMenu(): Promise<void> {
    if (this.party.length === 0) {
      await new DialogueBox(this, this.sfx).run([
        { text: 'No kin walk with you yet — your lamp is still your only companion.' },
      ]);
      return;
    }
    this.party = await new PartyMenu(this, this.party, this.sfx).run();
    void this.persist();
  }

  /**
   * Pack viewer (pause menu → ITEMS): see what you're carrying, read each item's
   * description, and use a medicine on a kin. Returns the (possibly healed) party
   * and the (possibly decremented) inventory, which are persisted on close.
   */
  private async openItemsMenu(): Promise<void> {
    if (Object.keys(this.inventory.items).length === 0) {
      await new DialogueBox(this, this.sfx).run([
        { text: 'Your pack is empty — nothing to carry but your lamp, for now.' },
      ]);
      return;
    }
    const result = await new ItemsMenu(this, this.inventory, this.party, this.sfx, this.money).run();
    this.party = result.party;
    this.inventory = result.inventory;
    void this.persist();
  }

  /**
   * The Hearth (pause menu → HEARTH): the warm keep where kin rest when they're not
   * travelling in your lamp. Move kin between the party (max 6) and storage; a full
   * lamp also overflows here on a catch. Returns the new party + box order to persist.
   */
  private async openHearthMenu(): Promise<void> {
    const result = await new HearthMenu(this, this.party, this.box, this.sfx).run();
    this.party = result.party;
    this.box = result.box;
    void this.persist();
  }

  /** In-game pause menu (Start/Esc): Resume / Kin / Hearth / Items / Save / Settings. */
  private async openPauseMenu(): Promise<void> {
    this.modal = true;
    // A holder so the closure write in onImport survives TS flow analysis.
    const pending: { load: SaveGame | null } = { load: null };
    let open = true;
    while (open) {
      const choice = await new Menu(
        this,
        [
          { label: 'RESUME', value: 'resume' },
          { label: 'KIN', value: 'kin' },
          { label: 'REGISTER', value: 'register' },
          { label: 'HEARTH', value: 'hearth' },
          { label: 'ITEMS', value: 'items' },
          { label: 'LORE', value: 'lore' },
          { label: 'CHARTS', value: 'charts' },
          { label: 'SAVE', value: 'save' },
          { label: 'SETTINGS', value: 'settings' },
        ],
        { x: 8, y: 8, sfx: this.sfx },
      ).run();

      if (choice === 'kin') {
        await this.openPartyMenu();
      } else if (choice === 'register') {
        await new RegisterMenu(this, { seen: [...this.dexSeen], caught: [...this.dexCaught] }, this.sfx).run();
      } else if (choice === 'hearth') {
        await this.openHearthMenu();
      } else if (choice === 'items') {
        await this.openItemsMenu();
      } else if (choice === 'lore') {
        await new GlossaryMenu(this, (flag) => this.flags.get(flag), this.sfx).run();
      } else if (choice === 'charts') {
        await new ChartsMenu(this, (flag) => this.flags.get(flag), this.sfx).run();
      } else if (choice === 'save') {
        await this.persist();
        void this.sfx.playVariant('ui-save', ['a', 'b']);
      } else if (choice === 'settings') {
        await new SettingsMenu(this, {
          getSave: () => this.buildSaveGame(),
          onImport: async (imported) => {
            await SaveManager.save(imported);
            pending.load = imported;
          },
          sfx: this.sfx,
        }).run();
        if (pending.load) open = false;
      } else {
        open = false; // Resume or cancel
      }
    }

    this.modal = false;
    const loaded = pending.load;
    if (loaded) {
      // Apply an imported save by reloading the world from it.
      this.scene.start('World', {
        mapId: loaded.world.current_map,
        spawn: loaded.world.player,
        flags: loaded.world.flags,
        abilities: loaded.world.abilities,
        party: loaded.party,
        box: loaded.box,
        inventory: loaded.inventory,
        money: loaded.money,
        dex: loaded.dex,
      });
    }
  }
}
