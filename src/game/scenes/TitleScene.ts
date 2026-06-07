/**
 * The title screen — logo, a soft float, and the New Game / Continue / Settings
 * menu built from the shared UI kit. Continue is enabled only when a valid save
 * exists; Settings opens the in-canvas settings (shell view, audio, export/import).
 * The world plugs in from here.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme } from '@game/ui/theme';
import { Menu } from '@game/ui/Menu';
import { SettingsMenu } from '@game/ui/SettingsMenu';
import { Sfx } from '@game/systems/audio/Sfx';
import { SaveManager } from '@game/systems/save/SaveManager';
import { VESPERHOLM_GRAPH } from '@game/data/world/graph';
import type { WorldSceneData } from './WorldScene';
import type { SaveGame } from '@game/systems/save/types';

export class TitleScene extends Phaser.Scene {
  private sfx!: Sfx;

  constructor() {
    super('Title');
  }

  create(): void {
    this.sfx = new Sfx(this);
    const cx = GAME_WIDTH / 2;
    const cy = GAME_HEIGHT / 2;

    const logo = this.add.image(cx, cy - 28, 'logo').setOrigin(0.5);
    const maxLogoWidth = GAME_WIDTH - 48;
    if (logo.width > maxLogoWidth) logo.setScale(maxLogoWidth / logo.width);
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
      { x: GAME_WIDTH / 2 - 44, y: GAME_HEIGHT / 2 + 18, width: 88, cancellable: false, sfx: this.sfx },
    );

    const choice = await menu.run();
    if (choice === 'new') this.start({ mapId: VESPERHOLM_GRAPH.start_map });
    else if (choice === 'continue' && save) this.start(this.continueData(save));
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

  private continueData(save: SaveGame): WorldSceneData {
    return {
      mapId: save.world.current_map,
      spawn: { tx: save.world.player.tx, ty: save.world.player.ty, facing: save.world.player.facing },
      flags: save.world.flags,
      abilities: save.world.abilities,
      party: save.party,
      inventory: save.inventory,
    };
  }

  private start(data: WorldSceneData): void {
    this.cameras.main.fadeOut(theme.transition.fadeMs, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.scene.start('World', data);
    });
  }
}
