/**
 * The title screen — logo, a soft float, and the New Game / Continue / Settings
 * menu built from the shared UI kit. Continue is enabled only when a valid save
 * exists; Settings opens the in-canvas settings (shell view, audio, export/import).
 * The world plugs in from here.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { GAME_VERSION_LABEL } from '@game/version';
import { theme } from '@game/ui/theme';
import { makeText } from '@game/ui/Text';
import { Menu } from '@game/ui/Menu';
import { DialogueBox } from '@game/ui/DialogueBox';
import { SettingsMenu } from '@game/ui/SettingsMenu';
import { Sfx } from '@game/systems/audio/Sfx';
import { MusicDirector } from '@game/systems/audio/MusicDirector';
import { SaveManager } from '@game/systems/save/SaveManager';
import { SlotMenu } from '@game/ui/SlotMenu';
import { SHELL_INPUT_EVENT } from '@/shell/ShellManager';
import { VESPERHOLM_GRAPH } from '@game/data/world/graph';
import type { WorldSceneData } from './WorldScene';
import type { SaveGame } from '@game/systems/save/types';

/** The dedicated title riff (Vesper-motif theme), with a graceful silent fallback. */
const TITLE_MUSIC = { key: 'title', url: 'assets/audio/music/title.mp3' };
const IDLE_TO_ATTRACT_MS = 15000;

/**
 * Screen layout (240×160). The logo is 4:3, so capping it by width alone left it
 * ~144px tall and clipping/overlapping the menu — cap it by HEIGHT too and give it
 * the top band, then anchor the menu in the lower band so they never collide.
 */
const LOGO_CENTER_Y = 48;
const LOGO_MAX_WIDTH = GAME_WIDTH - 64; // 176
const LOGO_MAX_HEIGHT = 84;
const MENU_Y = 104;

export class TitleScene extends Phaser.Scene {
  private sfx!: Sfx;
  private music!: MusicDirector;
  private idle?: Phaser.Time.TimerEvent;
  /**
   * The active slot's decoded save, surfaced to SETTINGS for export (and updated
   * on import). Defaults to slot 1's save so a player who opens Settings straight
   * from the title can still export their existing journey.
   */
  private activeSave: SaveGame | null = null;

  constructor() {
    super('Title');
  }

  create(): void {
    this.sfx = new Sfx(this);
    this.music = new MusicDirector(this, 0.4);
    void this.music.play(TITLE_MUSIC.key, TITLE_MUSIC.url);

    // Left idle, fall back to the attract demo (reset on any input).
    this.armIdle();
    const resetIdle = (): void => this.armIdle();
    this.input.keyboard?.on('keydown', resetIdle);
    this.input.on('pointerdown', resetIdle);
    // On-screen touch controls are DOM elements OUTSIDE the canvas: they dispatch
    // through a window event, bypassing the keyboard/pointer handlers above. Without
    // this, touch navigation of the title menus never resets the idle timer, so the
    // attract demo could fire mid-decision (e.g. while reading the overwrite warning
    // on a full slot) and bounce the player back to the start menu.
    window.addEventListener(SHELL_INPUT_EVENT, resetIdle);
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, () =>
      window.removeEventListener(SHELL_INPUT_EVENT, resetIdle),
    );

    const cx = GAME_WIDTH / 2;

    const logo = this.add.image(cx, LOGO_CENTER_Y, 'logo').setOrigin(0.5);
    // Fit within both the width and height budget (the logo is 4:3, so height binds).
    const scale = Math.min(LOGO_MAX_WIDTH / logo.width, LOGO_MAX_HEIGHT / logo.height, 1);
    logo.setScale(scale);
    this.tweens.add({
      targets: logo,
      y: logo.y - 4,
      duration: 1600,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.inOut',
    });

    this.cameras.main.fadeIn(theme.transition.fadeMs, 0, 0, 0);

    // Version stamp, tucked in the bottom-right corner so it's visible at a
    // glance without crowding the logo or menu. Source: version.ts.
    makeText(this, GAME_WIDTH - 3, GAME_HEIGHT - 2, GAME_VERSION_LABEL, theme.text.dim)
      .setOrigin(1, 1)
      .setDepth(theme.depth.text);
    // Reset to the default slot on (re)entering the title, and seed the active
    // save so SETTINGS export works straight from a cold title.
    SaveManager.setActiveSlot(0);
    void SaveManager.loadSlot(0).then((s) => {
      // Only seed if the player hasn't already picked a slot (which sets it).
      if (SaveManager.activeSlot === 0 && this.activeSave === null) this.activeSave = s;
    });
    void this.showMenu();
  }

  private async showMenu(): Promise<void> {
    // The attract demo only kicks in from the idle title menu — re-arm it here on
    // every return, and cancel it the moment the player commits to a sub-flow
    // (below), so the slot picker / overwrite confirm can't time out mid-decision.
    this.armIdle();
    // Decode every slot once so CONTINUE knows how many journeys exist and the
    // pickers can show per-slot summaries without re-reading storage per row.
    const slots = await SaveManager.loadAllSlots();
    const occupied = slots.filter((s) => s !== null).length;

    const menu = new Menu(
      this,
      [
        { label: 'NEW GAME', value: 'new' },
        { label: 'CONTINUE', value: 'continue', enabled: occupied > 0 },
        { label: 'SETTINGS', value: 'settings' },
      ],
      { x: GAME_WIDTH / 2 - 44, y: MENU_Y, width: 88, cancellable: false, sfx: this.sfx },
    );

    const choice = await menu.run();
    // Committed to a sub-flow — suspend the attract fallback until we're back on
    // the bare title menu (which re-arms it at the top of showMenu).
    this.idle?.remove();
    if (choice === 'new') {
      await this.handleNewGame(slots);
    } else if (choice === 'continue' && occupied > 0) {
      await this.handleContinue(slots);
    } else if (choice === 'settings') {
      await new SettingsMenu(this, {
        // Export/import operate on the ACTIVE slot via SaveManager (unchanged
        // SettingsMenu — out of this lane). Active slot is whatever was last
        // picked, defaulting to slot 1 (slot index 0).
        getSave: () => this.activeSave,
        onImport: async (imported) => {
          await SaveManager.save(imported);
          this.activeSave = imported;
        },
        sfx: this.sfx,
      }).run();
      void this.showMenu(); // re-show the title menu after settings
    } else {
      void this.showMenu();
    }
  }

  /**
   * NEW GAME: choose a slot (any slot is fair game), confirm before clobbering an
   * occupied one, then point SaveManager at it and roll the cold open.
   */
  private async handleNewGame(slots: (SaveGame | null)[]): Promise<void> {
    const slot = await new SlotMenu(this, { slots, mode: 'new', sfx: this.sfx }).run();
    if (slot === null) {
      void this.showMenu();
      return;
    }
    if (slots[slot] && !(await this.confirmOverwrite())) {
      void this.showMenu();
      return;
    }
    SaveManager.setActiveSlot(slot);
    this.activeSave = null; // a fresh journey: nothing to export until it saves
    // A new game opens on the cold-open prologue (the Long Dusk), which then
    // hands off to the world at the canon spawn. Continue skips straight in.
    this.startCinematic('coldopen_south', { mapId: VESPERHOLM_GRAPH.start_map });
  }

  /**
   * CONTINUE: with one journey, drop straight in (no friction for the common
   * case); with several, show the slot picker.
   */
  private async handleContinue(slots: (SaveGame | null)[]): Promise<void> {
    const occupiedIdx = slots
      .map((s, i) => (s !== null ? i : -1))
      .filter((i) => i >= 0);

    let slot: number;
    if (occupiedIdx.length === 1) {
      slot = occupiedIdx[0]!;
    } else {
      const picked = await new SlotMenu(this, { slots, mode: 'continue', sfx: this.sfx }).run();
      if (picked === null) {
        void this.showMenu();
        return;
      }
      slot = picked;
    }
    SaveManager.setActiveSlot(slot);
    const save = slots[slot];
    if (!save) {
      void this.showMenu();
      return;
    }
    this.activeSave = save;
    this.start(this.continueData(save));
  }

  /** Guard a destructive New Game when the chosen slot is occupied. */
  private async confirmOverwrite(): Promise<boolean> {
    const box = new DialogueBox(this, this.sfx);
    await box.run([{ text: 'Starting anew will overwrite the journey in this slot.' }]);
    const choice = await new Menu(
      this,
      [
        { label: 'KEEP SAVE', value: 'no' },
        { label: 'OVERWRITE', value: 'yes' },
      ],
      { x: GAME_WIDTH / 2 - 44, y: MENU_Y, width: 88, sfx: this.sfx },
    ).run();
    return choice === 'yes';
  }

  private continueData(save: SaveGame): WorldSceneData {
    return {
      mapId: save.world.current_map,
      spawn: { tx: save.world.player.tx, ty: save.world.player.ty, facing: save.world.player.facing },
      flags: save.world.flags,
      abilities: save.world.abilities,
      party: save.party,
      box: save.box,
      inventory: save.inventory,
      money: save.money,
      dex: save.dex,
      battles_won: save.battles_won,
      cooldowns: save.cooldowns,
      respawn: save.world.respawn,
    };
  }

  private armIdle(): void {
    this.idle?.remove();
    this.idle = this.time.delayedCall(IDLE_TO_ATTRACT_MS, () => {
      this.music.stop();
      this.cameras.main.fadeOut(theme.transition.fadeMs, 0, 0, 0);
      this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start('Attract'));
    });
  }

  private start(data: WorldSceneData): void {
    this.idle?.remove();
    this.music.stop();
    this.cameras.main.fadeOut(theme.transition.fadeMs, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.scene.start('World', data);
    });
  }

  /** Open a cold-open / chapter cinematic, handing it the world data to spawn into. */
  private startCinematic(scriptId: string, data: WorldSceneData): void {
    this.idle?.remove();
    this.music.stop();
    this.cameras.main.fadeOut(theme.transition.fadeMs, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.scene.start('Cinematic', { scriptId, next: { scene: 'World', data } });
    });
  }
}

