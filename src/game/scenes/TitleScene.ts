/**
 * The title screen — logo, a soft float, and the New Game / Continue / Settings
 * menu built from the shared UI kit. Continue is enabled only when a valid save
 * exists; Settings opens the in-canvas settings (shell view, audio, export/import).
 * The world plugs in from here.
 */
import Phaser from 'phaser';
import { GAME_WIDTH } from '@game/config';
import { theme } from '@game/ui/theme';
import { Menu } from '@game/ui/Menu';
import { DialogueBox } from '@game/ui/DialogueBox';
import { SettingsMenu } from '@game/ui/SettingsMenu';
import { Sfx } from '@game/systems/audio/Sfx';
import { MusicDirector } from '@game/systems/audio/MusicDirector';
import { SaveManager } from '@game/systems/save/SaveManager';
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

  constructor() {
    super('Title');
  }

  create(): void {
    this.sfx = new Sfx(this);
    this.music = new MusicDirector(this, 0.4);
    void this.music.play(TITLE_MUSIC.key, TITLE_MUSIC.url);

    // Left idle, fall back to the attract demo (reset on any input).
    this.armIdle();
    this.input.keyboard?.on('keydown', () => this.armIdle());
    this.input.on('pointerdown', () => this.armIdle());

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
    void this.showMenu();
  }

  private async showMenu(): Promise<void> {
    const save = await SaveManager.load();
    const menu = new Menu(
      this,
      [
        { label: 'NEW GAME', value: 'new' },
        { label: 'CONTINUE', value: 'continue', enabled: save !== null },
        { label: 'SETTINGS', value: 'settings' },
      ],
      { x: GAME_WIDTH / 2 - 44, y: MENU_Y, width: 88, cancellable: false, sfx: this.sfx },
    );

    const choice = await menu.run();
    if (choice === 'new') {
      if (save && !(await this.confirmOverwrite())) {
        void this.showMenu();
        return;
      }
      // A new game opens on the cold-open prologue (the Long Dusk), which then
      // hands off to the world at the canon spawn. Continue skips straight in.
      this.startCinematic('coldopen_south', { mapId: VESPERHOLM_GRAPH.start_map });
    } else if (choice === 'continue' && save) this.start(this.continueData(save));
    else if (choice === 'settings') {
      await new SettingsMenu(this, {
        getSave: () => save,
        onImport: async (imported) => {
          await SaveManager.save(imported);
        },
        sfx: this.sfx,
      }).run();
      void this.showMenu(); // re-show the title menu after settings
    }
  }

  /** Guard a destructive New Game when a save exists. */
  private async confirmOverwrite(): Promise<boolean> {
    const box = new DialogueBox(this, this.sfx);
    await box.run([{ text: 'Starting anew will overwrite your saved journey.' }]);
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

