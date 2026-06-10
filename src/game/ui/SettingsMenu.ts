/**
 * SettingsMenu — the in-canvas options screen, built from the UI kit (Panel +
 * Menu). It's a thin controller: the actual state lives in ShellManager (shell
 * chrome + control visibility) and SaveManager/SaveCodec (mute pref + save
 * export/import). Each row reads/writes one of those and the menu re-opens so the
 * label reflects the new state, until the player backs out.
 *
 * Promise-based: `await new SettingsMenu(scene, deps).run()` resolves (void) when
 * the player chooses Back or cancels. Mounts above any open scene UI.
 *
 * Deps (constructor):
 *   - scene: the host Phaser.Scene it draws into.
 *   - deps.getSave(): current SaveGame for export, or null if there's nothing to
 *     export yet (e.g. opened from Title). Import replaces it via deps.onImport.
 *   - deps.onImport(save): called with a freshly imported SaveGame so the
 *     orchestrator can persist + apply it (SettingsMenu doesn't own world state).
 *   - deps.sfx?: optional Sfx for menu blips + the save chime ('ui-save').
 */
import Phaser from 'phaser';
import { theme } from './theme';
import { makeText } from './Text';
import { Menu } from './Menu';
import type { MenuOption } from './Menu';
import type { Sfx } from '@game/systems/audio/Sfx';
import type { SaveGame } from '@game/systems/save/types';
import { SaveManager } from '@game/systems/save/SaveManager';
import type { Settings } from '@game/systems/save/SaveManager';
import { SaveCodec } from '@game/systems/save/SaveCodec';
import { ShellManager } from '../../shell/ShellManager';
import type { ShellMode } from '@game/systems/save/SaveManager';
import { setAlwaysRun, setTextSpeed, type TextSpeed } from './preferences';
import { GAME_WIDTH } from '@game/config';

export interface SettingsMenuDeps {
  /** Current save to export (null if none exists yet). */
  getSave: () => SaveGame | null;
  /** Called with an imported save so the host can persist + apply it. */
  onImport: (save: SaveGame) => void | Promise<void>;
  sfx?: Sfx;
}

const SHELL_LABEL: Record<ShellMode, string> = {
  device: 'Device',
  overlay: 'Overlay',
  plain: 'Plain',
};

const TEXT_SPEED_LABEL: Record<TextSpeed, string> = {
  cosy: 'Cosy',
  brisk: 'Brisk',
  instant: 'Instant',
};

/** Cycle the shell mode in a stable order. */
const SHELL_ORDER: ShellMode[] = ['device', 'overlay', 'plain'];
function nextShell(mode: ShellMode): ShellMode {
  const i = SHELL_ORDER.indexOf(mode);
  return SHELL_ORDER[(i + 1) % SHELL_ORDER.length] ?? 'device';
}

export class SettingsMenu {
  private settings: Settings = { shell: 'device', controlsVisible: true };

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly deps: SettingsMenuDeps,
  ) {}

  /** Open the menu and resolve when the player backs out. */
  async run(): Promise<void> {
    this.settings = await SaveManager.loadSettings();
    let open = true;
    while (open) {
      const choice = await this.openOnce();
      open = await this.handle(choice);
    }
  }

  private buildOptions(): MenuOption[] {
    const hasSave = this.deps.getSave() !== null;
    return [
      { label: `Shell: ${SHELL_LABEL[this.settings.shell]}`, value: 'shell' },
      {
        label: `Controls: ${this.settings.controlsVisible ? 'Shown' : 'Hidden'}`,
        value: 'controls',
        enabled: this.settings.shell !== 'plain',
      },
      { label: `Sound: ${this.settings.muted ? 'Muted' : 'On'}`, value: 'mute' },
      { label: `Pace: ${this.settings.alwaysRun ? 'Always run' : 'Walk'}`, value: 'run' },
      { label: `Text: ${TEXT_SPEED_LABEL[this.settings.textSpeed ?? 'cosy']}`, value: 'text' },
      { label: 'Export save', value: 'export', enabled: hasSave },
      { label: 'Import save', value: 'import' },
      { label: 'Back', value: 'back' },
    ];
  }

  /** Show the menu once; returns the chosen value (or null on cancel). */
  private openOnce(): Promise<string | null> {
    const title = makeText(this.scene, GAME_WIDTH / 2, 8, 'SETTINGS', theme.text.accent)
      .setOrigin(0.5, 0)
      .setScrollFactor(0)
      .setDepth(theme.depth.text);

    const menu = new Menu(this.scene, this.buildOptions(), {
      x: 24,
      y: 24,
      width: GAME_WIDTH - 48,
      sfx: this.deps.sfx,
      cancellable: true,
      fixed: true,
    });

    return menu.run().then((value) => {
      title.destroy();
      return value;
    });
  }

  /** Apply a chosen action. Returns whether the menu should stay open. */
  private async handle(choice: string | null): Promise<boolean> {
    switch (choice) {
      case 'shell': {
        const mode = nextShell(this.settings.shell);
        await ShellManager.setShell(mode);
        this.settings = { ...this.settings, shell: mode };
        // Plain hides controls implicitly; keep our flag honest for the label.
        return true;
      }
      case 'controls': {
        const visible = !this.settings.controlsVisible;
        await ShellManager.setControlsVisible(visible);
        this.settings = { ...this.settings, controlsVisible: visible };
        void this.deps.sfx?.play('ui-toggle');
        return true;
      }
      case 'mute': {
        const muted = !this.settings.muted;
        this.settings = { ...this.settings, muted };
        this.scene.sound.mute = muted;
        await SaveManager.saveSettings(this.settings);
        void this.deps.sfx?.play('ui-toggle');
        return true;
      }
      case 'run': {
        const alwaysRun = !this.settings.alwaysRun;
        this.settings = { ...this.settings, alwaysRun };
        setAlwaysRun(alwaysRun);
        await SaveManager.saveSettings(this.settings);
        void this.deps.sfx?.play('ui-toggle');
        return true;
      }
      case 'text': {
        const order: TextSpeed[] = ['cosy', 'brisk', 'instant'];
        const current = this.settings.textSpeed ?? 'cosy';
        const next = order[(order.indexOf(current) + 1) % order.length];
        this.settings = { ...this.settings, textSpeed: next };
        setTextSpeed(next);
        await SaveManager.saveSettings(this.settings);
        void this.deps.sfx?.play('ui-toggle');
        return true;
      }
      case 'export': {
        const save = this.deps.getSave();
        if (save) {
          SaveCodec.exportToFile(save);
          void this.deps.sfx?.play('ui-save');
        }
        return true;
      }
      case 'import': {
        const imported = await SaveCodec.importFromFile();
        if (imported) {
          await this.deps.onImport(imported);
          void this.deps.sfx?.play('ui-save');
        }
        return true;
      }
      case 'back':
      case null:
      default:
        return false;
    }
  }
}
