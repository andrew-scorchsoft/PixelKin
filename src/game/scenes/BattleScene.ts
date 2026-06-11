/**
 * BattleScene — the turn-based battle screen (scene key 'Battle').
 *
 * ── How the orchestrator starts a battle ───────────────────────────────────
 *   const onComplete = (result: BattleResult) => {
 *     // apply result.party / result.inventory / result.set_flags to the save,
 *     // add result.caught to the party, then:
 *     this.scene.resume('World');
 *   };
 *   this.scene.pause('World');
 *   this.scene.launch('Battle', { ...request, onComplete });
 *
 * `request` is a `BattleRequest` (wild or trainer). BattleScene runs the whole
 * fight, then calls `onComplete(result)` and stops itself (Phaser scenes can't
 * return a value, so the result is handed back through this callback). The world
 * stays paused underneath and resumes when onComplete runs.
 *
 * The scene is otherwise self-contained: it owns the BattleEngine, the battlers,
 * the HP plates, the action menus and the message strip, all built from the
 * shared UI kit so the look matches the rest of the game.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, COLORS } from '@game/config';
import { theme } from '@game/ui/theme';
import { Menu } from '@game/ui/Menu';
import type { MenuOption } from '@game/ui/Menu';
import { DialogueBox } from '@game/ui/DialogueBox';
import { fadeIn } from '@game/ui/Transitions';
import { Sfx } from '@game/systems/audio/Sfx';
import { MusicDirector } from '@game/systems/audio/MusicDirector';
import { Party } from '@game/systems/party/Party';
import { KinInstance } from '@game/systems/party/KinInstance';
import { BattleEngine } from '@game/systems/battle/BattleEngine';
import type { BattleEvent } from '@game/systems/battle/types';
import { effectivenessLabel } from '@game/systems/battle/types';
import { Battler } from '@game/ui/battle/Battler';
import { HpPanel } from '@game/ui/battle/HpPanel';
import { BattleMessage } from '@game/ui/battle/BattleMessage';
import { MoveLearnPrompt } from '@game/ui/MoveLearnPrompt';
import { KindlePrompt } from '@game/ui/KindlePrompt';
import { getTrainer, getTrainerLines } from '@game/content/trainers';
import { getItem } from '@game/content/items';
import { trainerPayout } from '@game/content/economy';
import { resolveBattleBackdrop } from '@game/data/world/maps';
import type { KinInstanceData, InventoryData } from '@game/systems/save/types';
import type { WorldFlag, AbilityId } from '@game/data/world/types';

const MUSIC_DIR = 'assets/audio/music/';

/** What the caller hands in to start a fight. */
export type BattleRequest =
  | { kind: 'wild'; species_id: number; level: number; party: KinInstanceData[]; box: KinInstanceData[]; inventory: InventoryData }
  | { kind: 'trainer'; trainer: string; party: KinInstanceData[]; box: KinInstanceData[]; inventory: InventoryData };

/** What the scene hands back via onComplete. */
export interface BattleResult {
  outcome: 'win' | 'lose' | 'caught' | 'fled';
  /** Player party with mutated hp/exp/levels (and any newly caught kin appended). */
  party: KinInstanceData[];
  /** Kin at the Hearth, with any full-lamp catch overflow appended. */
  box: KinInstanceData[];
  inventory: InventoryData;
  /** The kin caught this battle (appended to `party`, or to `box` if the lamp was full). */
  caught?: KinInstanceData;
  /** Flags to set on win (e.g. a trainer's reward_flags). */
  set_flags?: string[];
  /** Species ids met this battle — merged into the save's register (seen). */
  dex_seen?: number[];
  /** Lantern Gifts (abilities) granted on win (e.g. a Lampwarden's reward_abilities). */
  grant_abilities?: AbilityId[];
  /** Wicks won (a beaten trainer's payout; wild battles pay nothing). */
  money_earned?: number;
}

/** Full scene data = the request plus the result callback. */
export type BattleSceneData = BattleRequest & {
  onComplete: (result: BattleResult) => void;
  /** Map the fight started on; selects the battle backdrop (see data/world/maps.ts). */
  mapId?: string;
};

const FOE_POS = { x: GAME_WIDTH - 56, y: 50 };
const PLAYER_POS = { x: 56, y: 104 };

export class BattleScene extends Phaser.Scene {
  private request!: BattleSceneData;
  private engine!: BattleEngine;
  private playerParty!: Party;
  /** Kin at the Hearth; a catch made with a full lamp overflows into this list. */
  private box: KinInstanceData[] = [];
  private inventory!: InventoryData;
  private sfx!: Sfx;
  private music!: MusicDirector;

  private playerBattler!: Battler;
  private foeBattler!: Battler;
  private playerHp!: HpPanel;
  private foeHp!: HpPanel;
  private msg!: BattleMessage;

  private setFlags: string[] = [];
  private grantAbilities: AbilityId[] = [];
  private moneyEarned = 0;
  private dexSeen = new Set<number>();
  private finished = false;

  constructor() {
    super('Battle');
  }

  create(data: BattleSceneData): void {
    this.request = data;
    this.finished = false;
    this.setFlags = [];
    this.grantAbilities = [];
    this.moneyEarned = 0;
    this.dexSeen = new Set();
    this.cameras.main.setBackgroundColor(COLORS.night);
    this.sfx = new Sfx(this);
    this.music = new MusicDirector(this);

    this.playerParty = Party.fromData(data.party);
    this.box = [...(data.box ?? [])];
    this.inventory = { items: { ...data.inventory.items } };

    const foeParty = this.buildFoeParty();
    this.engine = new BattleEngine({
      kind: data.kind,
      playerParty: this.playerParty,
      foeParty,
      ai: data.kind === 'trainer' ? getTrainer(data.trainer)?.ai ?? 'basic' : 'basic',
    });
    this.dexSeen.add(this.engine.foe.species.id); // you've met what you're facing

    this.buildScene();
    void this.run();
  }

  // --- Setup ---------------------------------------------------------------

  private buildFoeParty(): Party {
    if (this.request.kind === 'wild') {
      return new Party([KinInstance.create(this.request.species_id, this.request.level)]);
    }
    const trainer = getTrainer(this.request.trainer);
    if (!trainer || trainer.party.length === 0) {
      // Fallback so a missing trainer id doesn't hard-crash the slice.
      return new Party([KinInstance.create(1, 5)]);
    }
    return new Party(trainer.party.map((k) => KinInstance.create(k.species_id, k.level)));
  }

  private buildScene(): void {
    this.addBackdrop();
    this.foeBattler = new Battler(this, FOE_POS.x, FOE_POS.y, this.engine.foe.species, 'foe');
    this.playerBattler = new Battler(this, PLAYER_POS.x, PLAYER_POS.y, this.engine.player.species, 'player');
    this.foeHp = new HpPanel(this, 6, 8, this.engine.foe, false, 'left');
    this.playerHp = new HpPanel(this, GAME_WIDTH - 6, GAME_HEIGHT - 78, this.engine.player, true, 'right');
    this.msg = new BattleMessage(this);
    this.cameras.main.fadeIn(theme.transition.fadeMs, 0, 0, 0);
  }

  /**
   * Drop the map's battle backdrop behind the battlers, over the night fill. The
   * variant was chosen (and the texture preloaded) for this map; if there is none,
   * or it somehow isn't loaded, we just keep the plain night camera fill.
   */
  private addBackdrop(): void {
    const path = resolveBattleBackdrop(this.request.mapId);
    if (!path || !this.textures.exists(path)) return;
    this.add
      .image(GAME_WIDTH / 2, GAME_HEIGHT / 2, path)
      .setDepth(theme.depth.world - 1)
      .setScrollFactor(0);
  }

  private startMusic(): void {
    const key = this.request.kind === 'trainer'
      ? getTrainer(this.request.trainer)?.music ?? 'battle-main-dusk-duel'
      : 'battle-main-dusk-duel';
    void this.music.play(key, `${MUSIC_DIR}${key}.mp3`);
  }

  // --- Top-level flow ------------------------------------------------------

  private async run(): Promise<void> {
    await fadeIn(this);
    void this.sfx.play('battle-encounter');
    this.startMusic();

    if (this.request.kind === 'trainer') {
      const trainer = getTrainer(this.request.trainer);
      const intro = getTrainerLines(trainer?.intro_ref);
      if (intro.length > 0) {
        this.msg.setVisible(false);
        await new DialogueBox(this, this.sfx).run(intro);
        this.msg.setVisible(true);
      }
      await this.msg.show(`${trainer?.name ?? 'Foe'} sent out ${this.engine.foe.displayName}!`);
    } else {
      await this.msg.show(`A wild ${this.engine.foe.displayName} appeared!`);
    }
    await this.msg.show(`Go, ${this.engine.player.displayName}!`, { wait: false });

    await this.loop();
  }

  /** The main decision → resolution loop. */
  private async loop(): Promise<void> {
    while (!this.engine.ended) {
      const events = await this.chooseAndResolve();
      await this.playEvents(events);

      // If our active kin fainted but we have more, prompt a replacement.
      if (!this.engine.ended && this.engine.player.isFainted) {
        await this.forceSwitch();
      }
    }
    await this.finish();
  }

  /** Present the root menu and resolve the chosen action into engine events. */
  private async chooseAndResolve(): Promise<BattleEvent[]> {
    this.msg.set('What will you do?');
    const root = await this.rootMenu();

    switch (root) {
      case 'fight': {
        const events = await this.fightMenu();
        return events ?? this.chooseAndResolve();
      }
      case 'catch': {
        const events = await this.lampMenu();
        return events ?? this.chooseAndResolve();
      }
      case 'switch': {
        const idx = await this.switchMenu(true);
        if (idx === null) return this.chooseAndResolve();
        return this.engine.takeTurn({ kind: 'switch', partyIndex: idx });
      }
      case 'bag': {
        const ev = await this.bagMenu();
        return ev ?? this.chooseAndResolve();
      }
      case 'run':
        return this.engine.takeTurn({ kind: 'run' });
      default:
        return this.chooseAndResolve();
    }
  }

  /**
   * The LAMP throw menu: a plain throw is always free (your vesperlamp is the
   * device, not a consumable); any owned charges are offered as one-throw
   * boosters and spent on use.
   */
  private async lampMenu(): Promise<BattleEvent[] | null> {
    const charges = Object.entries(this.inventory.items)
      .filter(([id, n]) => n > 0 && getItem(id)?.category === 'charge')
      .map(([id, n]) => ({ def: getItem(id)!, count: n }));

    // Nothing to choose between — just raise the lamp.
    if (charges.length === 0) {
      return this.engine.catchWithBonus('vesperlamp', 1.0);
    }

    const opts: MenuOption[] = [
      { label: 'PLAIN THROW', value: 'plain' },
      ...charges.map((c) => ({ label: `${c.def.name.toUpperCase()} x${c.count}`, value: c.def.id })),
    ];
    const choice = await new Menu(this, opts, { x: 6, y: this.menuY(opts.length), sfx: this.sfx }).run();
    if (choice === null) return null;
    if (choice === 'plain') return this.engine.catchWithBonus('vesperlamp', 1.0);

    const def = getItem(choice);
    this.consumeItem(choice);
    return this.engine.catchWithBonus(choice, def?.catch_bonus ?? 1.0);
  }

  // --- Menus ---------------------------------------------------------------

  /**
   * Bottom-align a menu of `rows` options so it sits just above the message strip
   * and its last row (e.g. RUN) is never clipped off the 160px-tall screen.
   */
  private menuY(rows: number): number {
    const ROW_H = 12;
    const height = theme.space.lg * 2 + rows * ROW_H;
    const messageTop = GAME_HEIGHT - 34 - 4; // mirrors BattleMessage's HEIGHT + MARGIN
    return messageTop - 2 - height;
  }

  private rootMenu(): Promise<string | null> {
    const opts: MenuOption[] = [
      { label: 'FIGHT', value: 'fight' },
      { label: 'BAG', value: 'bag' },
      { label: 'KIN', value: 'switch' },
    ];
    if (this.request.kind === 'wild') {
      opts.splice(1, 0, { label: 'LAMP', value: 'catch' });
      opts.push({ label: 'RUN', value: 'run' });
    } else {
      opts.push({ label: 'RUN', value: 'run' });
    }
    return new Menu(this, opts, { x: 6, y: this.menuY(opts.length), sfx: this.sfx, cancellable: false }).run();
  }

  /** Returns engine events for the chosen move, or null if the player backed out. */
  private async fightMenu(): Promise<BattleEvent[] | null> {
    const moves = this.engine.player.moves;
    const opts: MenuOption[] = moves.map((k, i) => ({
      label: `${k.move.name}  ${k.charges}/${k.move.charges}`,
      value: String(i),
      enabled: k.charges > 0,
    }));
    if (opts.length === 0 || opts.every((o) => o.enabled === false)) {
      await this.msg.show(`${this.engine.player.displayName} has no charges left!`);
      return null;
    }
    const choice = await new Menu(this, opts, { x: 6, y: this.menuY(opts.length), sfx: this.sfx }).run();
    if (choice === null) return null;
    return this.engine.takeTurn({ kind: 'move', moveIndex: Number(choice) });
  }

  /**
   * Party menu. When `cancellable` is false (a forced switch after a faint) the
   * player must pick a healthy kin. Returns the chosen index or null.
   */
  private async switchMenu(cancellable: boolean): Promise<number | null> {
    const opts: MenuOption[] = this.playerParty.all.map((k, i) => ({
      label: `${k.displayName} Lv${k.level} ${k.isFainted ? 'FNT' : `${k.hp}/${k.maxHp}`}`,
      value: String(i),
      enabled: !k.isFainted && i !== this.playerParty.activeSlot,
    }));
    const choice = await new Menu(this, opts, {
      x: 6,
      y: this.menuY(opts.length),
      sfx: this.sfx,
      cancellable,
    }).run();
    return choice === null ? null : Number(choice);
  }

  /** Bag (medicine + lamps). Returns engine events if an action was taken. */
  private async bagMenu(): Promise<BattleEvent[] | null> {
    const owned = Object.entries(this.inventory.items).filter(([, n]) => n > 0);
    const opts: MenuOption[] = owned.map(([id, n]) => {
      const def = getItem(id);
      return { label: `${def?.name ?? id} x${n}`, value: id, enabled: this.itemUsable(id) };
    });
    if (opts.length === 0) {
      await this.msg.show('Your bag is empty.');
      return null;
    }
    const choice = await new Menu(this, opts, { x: 6, y: this.menuY(opts.length), sfx: this.sfx }).run();
    if (choice === null) return null;

    const def = getItem(choice);
    if (!def) return null;

    if (def.category === 'charge') {
      if (this.request.kind !== 'wild') {
        await this.msg.show("You can't catch another warden's kin!");
        return null;
      }
      this.consumeItem(choice);
      return this.engine.catchWithBonus(choice, def.catch_bonus ?? 1.0);
    }

    if (def.category === 'medicine' && def.heal) {
      const target = this.engine.player;
      if (target.hpRatio >= 1) {
        await this.msg.show(`${target.displayName} is already at full health.`);
        return null;
      }
      const healed = target.heal(def.heal);
      this.consumeItem(choice);
      await this.msg.show(`Used ${def.name}. ${target.displayName} recovered ${healed} HP.`);
      await this.playerHp.animateTo();
      // Using an item costs the turn; the foe attacks back.
      return this.engine.takeTurn({ kind: 'item', itemId: choice });
    }

    await this.msg.show("That can't be used right now.");
    return null;
  }

  private itemUsable(id: string): boolean {
    const def = getItem(id);
    if (!def) return false;
    if (def.category === 'charge') return this.request.kind === 'wild';
    if (def.category === 'medicine') return true;
    return false;
  }

  private consumeItem(id: string): void {
    if (this.inventory.items[id] > 0) this.inventory.items[id]--;
  }

  /** After our active kin faints (battle not over), make the player send another. */
  private async forceSwitch(): Promise<void> {
    await this.msg.show(`${this.engine.player.displayName} fainted!`);
    const idx = await this.switchMenu(false);
    const events = this.engine.sendOut(idx ?? this.playerParty.firstHealthyIndex());
    await this.playEvents(events);
  }

  // --- Event playback ------------------------------------------------------

  private async playEvents(events: BattleEvent[]): Promise<void> {
    for (const ev of events) {
      await this.playEvent(ev);
    }
  }

  private async playEvent(ev: BattleEvent): Promise<void> {
    switch (ev.type) {
      case 'message':
        await this.msg.show(ev.text);
        return;
      case 'move-used': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        (ev.side === 'player' ? this.playerBattler : this.foeBattler).nudge(this, ev.side === 'player' ? 6 : -6);
        await this.msg.show(`${who.displayName} used ${ev.move.name}!`, { wait: false });
        return;
      }
      case 'miss':
        void this.sfx.play('battle-miss');
        await this.msg.show('But it missed!');
        return;
      case 'no-charges':
        await this.msg.show('No charges left for that move!');
        return;
      case 'damage': {
        await this.playDamage(ev);
        return;
      }
      case 'stat-change': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        const up = ev.delta > 0;
        await this.msg.show(`${who.displayName}'s ${ev.stat.toUpperCase()} ${up ? 'rose' : 'fell'}!`);
        return;
      }
      case 'status': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        await this.msg.show(`${who.displayName} ${statusLanded(ev.status)}`);
        return;
      }
      case 'status-block': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        await this.msg.show(`${who.displayName} ${statusBlocked(ev.status)}`);
        return;
      }
      case 'status-wake': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        await this.msg.show(`${who.displayName} woke up!`);
        return;
      }
      case 'status-thaw': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        await this.msg.show(`${who.displayName} thawed out!`);
        return;
      }
      case 'confusion-hit': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        void this.sfx.playVariant('battle-hit-physical', ['a', 'b', 'c']);
        await this.msg.show(`${who.displayName} is dazzled — it hurt itself!`);
        await (ev.side === 'player' ? this.playerHp : this.foeHp).animateTo();
        return;
      }
      case 'status-tick': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        await this.msg.show(
          ev.status === 'scorch'
            ? `${who.displayName} is seared by its scorch!`
            : `The blight deepens in ${who.displayName}!`,
        );
        await (ev.side === 'player' ? this.playerHp : this.foeHp).animateTo();
        return;
      }
      case 'status-cure': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        await this.msg.show(`${who.displayName}'s affliction lifted!`);
        return;
      }
      case 'recoil': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        await this.msg.show(`${who.displayName} is hit by the kickback!`);
        await (ev.side === 'player' ? this.playerHp : this.foeHp).animateTo();
        return;
      }
      case 'drain': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        await this.msg.show(`${who.displayName} drew strength from the hit!`);
        await (ev.side === 'player' ? this.playerHp : this.foeHp).animateTo();
        return;
      }
      case 'heal': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        void this.sfx.playVariant('world-heal', ['a', 'b']);
        await this.msg.show(`${who.displayName} recovered ${ev.amount} HP!`);
        await (ev.side === 'player' ? this.playerHp : this.foeHp).animateTo();
        return;
      }
      case 'flinch': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        await this.msg.show(`${who.displayName} flinched!`);
        return;
      }
      case 'screen-up': {
        const mine = ev.side === 'player';
        await this.msg.show(
          ev.screen === 'physical'
            ? `A bulwark settles over ${mine ? 'your' : "the foe's"} side!`
            : `A soft mist veils ${mine ? 'your' : "the foe's"} side!`,
        );
        return;
      }
      case 'screen-fade': {
        const mine = ev.side === 'player';
        await this.msg.show(`The ${ev.screen === 'physical' ? 'bulwark' : 'mist'} over ${mine ? 'your' : "the foe's"} side faded.`);
        return;
      }
      case 'hazard-set': {
        const mine = ev.side === 'player';
        await this.msg.show(`Caltrops scatter across ${mine ? 'your' : "the foe's"} side of the field!`);
        return;
      }
      case 'hazard-hurt': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        await this.msg.show(`${who.displayName} is hurt by the caltrops!`);
        await (ev.side === 'player' ? this.playerHp : this.foeHp).animateTo();
        return;
      }
      case 'pivot': {
        const who = ev.side === 'player' ? this.engine.player : this.engine.foe;
        await this.msg.show(`${who.displayName} slips back toward the lamplight!`);
        if (ev.side === 'player') {
          // The player picks who swaps in (cancel keeps the current kin out).
          const idx = await this.switchMenu(true);
          if (idx !== null) await this.playEvents(this.engine.pivotSwitch(idx));
        }
        return;
      }
      case 'faint':
        await this.playFaint(ev.side);
        return;
      case 'switch':
        await this.playSwitch(ev.side, ev.incoming);
        return;
      case 'catch-throw':
        void this.sfx.playVariant('capture-throw', ['a', 'b']);
        await this.msg.show(`You raised your lamp toward ${this.engine.foe.displayName}...`);
        return;
      case 'catch-wobble':
        for (let i = 0; i < ev.count; i++) {
          void this.sfx.play('capture-wobble');
          await this.msg.show('...', { wait: true });
        }
        return;
      case 'catch-success':
        void this.sfx.playVariant('capture-success', ['a', 'b', 'c']);
        // isFull is still true here — the add happens in complete() — so it
        // correctly predicts whether this catch will overflow to the Hearth.
        if (this.playerParty.isFull) {
          await this.msg.show(`Your lamp is full! ${this.engine.foe.displayName} will rest at the Hearth.`);
        } else {
          await this.msg.show(`${this.engine.foe.displayName} walks with you now!`);
        }
        return;
      case 'catch-break':
        void this.sfx.play('capture-break');
        await this.msg.show(`${this.engine.foe.displayName} slipped free!`);
        return;
      case 'run-success':
        void this.sfx.play('battle-flee');
        await this.msg.show('You slipped away into the dusk.');
        return;
      case 'run-fail':
        await this.msg.show("Couldn't get away!");
        return;
      case 'item-used':
        return;
      default:
        return;
    }
  }

  private async playDamage(ev: Extract<BattleEvent, { type: 'damage' }>): Promise<void> {
    const hitPlayer = ev.side === 'player';
    const battler = hitPlayer ? this.playerBattler : this.foeBattler;
    const panel = hitPlayer ? this.playerHp : this.foeHp;

    battler.flashHit(this);
    if (ev.crit) void this.sfx.play('battle-critical');
    else void this.sfx.playVariant('battle-hit-physical', ['a', 'b', 'c']);

    await panel.animateTo();

    const label = effectivenessLabel(ev.effectiveness);
    if (label === 'super') {
      void this.sfx.play('battle-super-effective');
      await this.msg.show("It's super effective!");
    } else if (label === 'not') {
      void this.sfx.play('battle-not-effective');
      await this.msg.show("It's not very effective...");
    } else if (label === 'none') {
      await this.msg.show('It had no effect...');
    } else if (ev.crit) {
      await this.msg.show('A critical hit!');
    }
  }

  private async playFaint(side: 'player' | 'foe'): Promise<void> {
    void this.sfx.playVariant('battle-faint', ['a', 'b', 'c']);
    const who = side === 'player' ? this.engine.player : this.engine.foe;
    const battler = side === 'player' ? this.playerBattler : this.foeBattler;
    await battler.fall(this);
    await this.msg.show(`${who.displayName} fainted!`);
  }

  private async playSwitch(side: 'player' | 'foe', incoming: KinInstance): Promise<void> {
    if (side === 'player') {
      this.playerBattler.setSpecies(this, incoming.species, 'player');
      this.playerBattler.container.setAlpha(1).setY(PLAYER_POS.y);
      this.playerHp.setKin(incoming);
      await this.msg.show(`Go, ${incoming.displayName}!`, { wait: false });
    } else {
      this.dexSeen.add(incoming.species.id);
      this.foeBattler.setSpecies(this, incoming.species, 'foe');
      this.foeBattler.container.setAlpha(1).setY(FOE_POS.y);
      this.foeHp.setKin(incoming);
      const trainer = this.request.kind === 'trainer' ? getTrainer(this.request.trainer) : undefined;
      await this.msg.show(`${trainer?.name ?? 'Foe'} sent out ${incoming.displayName}!`);
    }
  }

  // --- Win / lose / exit ---------------------------------------------------

  private async finish(): Promise<void> {
    const outcome = this.engine.outcome ?? 'fled';

    if (outcome === 'win' || outcome === 'caught') {
      // A catch pays the same XP as a knock-out — collecting (the game's heart)
      // must keep the player on the level curve, not punish them off it.
      await this.awardExp();
      if (outcome === 'win' && this.request.kind === 'trainer') {
        const trainer = getTrainer(this.request.trainer);
        const lines = getTrainerLines(trainer?.defeat_ref);
        if (lines.length > 0) {
          this.msg.setVisible(false);
          await new DialogueBox(this, this.sfx).run(lines);
          this.msg.setVisible(true);
        }
        for (const f of trainer?.reward_flags ?? []) this.setFlags.push(f as WorldFlag);
        for (const a of trainer?.reward_abilities ?? []) this.grantAbilities.push(a);
        const payout = trainerPayout(trainer);
        if (payout > 0) {
          this.moneyEarned = payout;
          void this.sfx.playVariant('world-pickup', ['a', 'b', 'c']);
          await this.msg.show(`You earned ${payout} wicks for the bout!`);
        }
      }
    } else if (outcome === 'lose') {
      await this.msg.show('Your lamp guttered out... You hurry home to the hearth.');
    }

    this.complete(outcome);
  }

  /** Grant exp to the active (and a share to other participants is out of scope). */
  private async awardExp(): Promise<void> {
    // Simple yield: summed over the foe party, weighted by level & BST tier.
    const winner = this.playerParty.firstHealthy() ?? this.engine.player;
    let totalGain = 0;
    for (const defeated of this.engine.foeParty.all) {
      totalGain += this.expYield(defeated);
    }
    // The genre's trainer-battle bonus — raised kin teach more than wild ones.
    if (this.request.kind === 'trainer') totalGain = Math.floor(totalGain * 1.5);
    if (totalGain <= 0) return;

    void this.sfx.play('battle-xp');
    const before = winner.level;
    const { learned, pending, kindleReady } = winner.gainExp(totalGain);
    await this.msg.show(`${winner.displayName} gained ${totalGain} EXP!`);
    await this.playerHp.animateTo();

    if (winner.level > before) {
      void this.sfx.playVariant('progress-levelup', ['a', 'b']);
      this.playerHp.refresh();
      await this.msg.show(`${winner.displayName} grew to Lv${winner.level}!`);
      for (const m of learned) {
        await this.msg.show(`${winner.displayName} learned ${m.name}!`);
      }
      // A full kit met a new move: the player chooses what to set aside.
      for (const m of pending) {
        this.msg.setVisible(false);
        await new MoveLearnPrompt(this, winner, m, this.sfx).run();
        this.msg.setVisible(true);
      }
    }

    // The level crossed a kindling threshold — the witnessed ceremony, here at
    // the battle's end like the classics. Declining is honoured (the kin offers
    // again after its next level-up).
    if (kindleReady) {
      this.msg.setVisible(false);
      const kindled = await new KindlePrompt(this, winner, kindleReady, this.sfx, () => {
        if (winner === this.engine.player) {
          this.playerBattler.setSpecies(this, winner.species, 'player');
        }
      }).run();
      if (kindled) {
        this.dexSeen.add(winner.species.id);
        this.playerHp.refresh();
      }
      this.msg.setVisible(true);
    }
  }

  /**
   * EXP a defeated (or caught) kin yields: level-scaled, weighted by its BST.
   * The /20 divisor is set by the journey model (tools/balance/progression.mjs)
   * so the locked level curve is reachable on the designed battle budget —
   * change it there first, then mirror it here.
   */
  private expYield(defeated: KinInstance): number {
    return Math.max(1, Math.floor((defeated.species.bst * defeated.level) / 20));
  }

  private complete(outcome: BattleResult['outcome']): void {
    if (this.finished) return;
    this.finished = true;

    let caught: KinInstanceData | undefined;
    if (outcome === 'caught' && this.engine.caught) {
      // Append the caught kin to the party if there's room; otherwise the lamp is
      // full and it overflows to the Hearth (never silently lost). The catch-success
      // message already told the player which happened.
      const c = this.engine.caught;
      caught = c.toData();
      if (!this.playerParty.add(c)) this.box.push(caught);
    }

    // The first wild catch is a progression beat (Brisa's bond-test waits for
    // it) — every catch sets the flag; setting it twice is harmless.
    if (outcome === 'caught') this.setFlags.push('flag:caught_first_kin');

    const result: BattleResult = {
      outcome,
      party: this.playerParty.toData(),
      box: this.box,
      inventory: this.inventory,
      caught,
      set_flags: this.setFlags.length > 0 ? this.setFlags : undefined,
      grant_abilities: this.grantAbilities.length > 0 ? this.grantAbilities : undefined,
      money_earned: this.moneyEarned > 0 ? this.moneyEarned : undefined,
      dex_seen: this.dexSeen.size > 0 ? [...this.dexSeen] : undefined,
    };

    this.music.stop();
    const done = this.request.onComplete;
    this.cameras.main.fadeOut(theme.transition.fadeMs, 0, 0, 0);
    this.cameras.main.once(Phaser.Cameras.Scene2D.Events.FADE_OUT_COMPLETE, () => {
      this.teardown();
      done(result);
      this.scene.stop();
    });
  }

  private teardown(): void {
    this.playerBattler?.destroy();
    this.foeBattler?.destroy();
    this.playerHp?.destroy();
    this.foeHp?.destroy();
    this.msg?.destroy();
  }
}

// --- Status narration (canon names, warm voice) ------------------------------

function statusLanded(status: string): string {
  switch (status) {
    case 'scorch': return 'was scorched!';
    case 'drench': return 'was drenched and slowed!';
    case 'numb': return 'was numbed!';
    case 'doze': return 'drifted into a doze...';
    case 'blight': return 'was blighted!';
    case 'dazzle': return 'was dazzled!';
    case 'chill': return 'was chilled through!';
    default: return `was afflicted with ${status}!`;
  }
}

function statusBlocked(status: string): string {
  switch (status) {
    case 'doze': return 'is fast asleep.';
    case 'chill': return 'is chilled solid!';
    case 'numb': return 'is numb and cannot move!';
    case 'drench': return 'is waterlogged and cannot move!';
    default: return 'cannot move!';
  }
}
