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
import { Panel } from './Panel';
import { Menu } from './Menu';
import type { MenuOption } from './Menu';
import type { Sfx } from '@game/systems/audio/Sfx';
import type { SaveGame } from '@game/systems/save/types';
import { SaveManager } from '@game/systems/save/SaveManager';
import type { Settings } from '@game/systems/save/SaveManager';
import { SaveCodec } from '@game/systems/save/SaveCodec';
import { ShellManager } from '../../shell/ShellManager';
import type { ShellMode, ControlSize } from '@game/systems/save/SaveManager';
import {
  setAlwaysRun,
  setTextSpeed,
  setBattlePace,
  setMusicVolume,
  setSfxVolume,
  type TextSpeed,
  type BattlePace,
  type VolumeLevel,
} from './preferences';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';

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

const BATTLE_PACE_LABEL: Record<BattlePace, string> = {
  cosy: 'Cosy',
  swift: 'Swift',
};

const VOLUME_LABEL: Record<VolumeLevel, string> = {
  off: 'Off',
  low: 'Low',
  mid: 'Mid',
  full: 'Full',
};

/** Cycle order for the stepped volume prefs. */
const VOLUME_ORDER: VolumeLevel[] = ['off', 'low', 'mid', 'full'];
function nextVolume(level: VolumeLevel): VolumeLevel {
  return VOLUME_ORDER[(VOLUME_ORDER.indexOf(level) + 1) % VOLUME_ORDER.length] ?? 'full';
}

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
    return [
      { label: `Shell: ${SHELL_LABEL[this.settings.shell]}`, value: 'shell' },
      {
        // One control for the touch buttons: their size, plus Hidden as the last
        // step. Folded into a single row so the settings list stays within the
        // 160px height budget (no room for a separate size row).
        label: `Controls: ${
          this.settings.controlsVisible ? `Size ${this.settings.controlSize ?? 2}` : 'Hidden'
        }`,
        value: 'controls',
        enabled: this.settings.shell !== 'plain',
      },
      { label: `Sound: ${this.settings.muted ? 'Muted' : 'On'}`, value: 'mute' },
      { label: `Pace: ${this.settings.alwaysRun ? 'Always run' : 'Walk'}`, value: 'run' },
      { label: `Text: ${TEXT_SPEED_LABEL[this.settings.textSpeed ?? 'cosy']}`, value: 'text' },
      { label: `Battle: ${BATTLE_PACE_LABEL[this.settings.battlePace ?? 'cosy']}`, value: 'battle' },
      { label: `Music: ${VOLUME_LABEL[this.settings.musicVolume ?? 'full']}`, value: 'music' },
      { label: `Sfx: ${VOLUME_LABEL[this.settings.sfxVolume ?? 'full']}`, value: 'sfx' },
      { label: 'Backup / restore', value: 'backup' },
      { label: 'Back', value: 'back' },
    ];
  }

  /** Show the menu once; returns the chosen value (or null on cancel). */
  private openOnce(): Promise<string | null> {
    const title = makeText(this.scene, GAME_WIDTH / 2, 4, 'SETTINGS', theme.text.accent)
      .setOrigin(0.5, 0)
      .setScrollFactor(0)
      .setDepth(theme.depth.text);

    const menu = new Menu(this.scene, this.buildOptions(), {
      x: 24,
      // The list is height-budgeted (one row per setting + Backup/restore + Back);
      // starting at 16 keeps the panel's bottom inside the 160px screen.
      y: 16,
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

  /**
   * Backup / restore sub-screen. Carries the standing note that progress lives in
   * this browser (so a cleared cache / new device can lose it) and that Export
   * keeps a copy you can carry — the guidance a player must not miss. Export saves
   * a JSON file; Import loads one back.
   */
  private async openBackup(): Promise<void> {
    const w = GAME_WIDTH - 16;
    const note = new Panel(this.scene, 8, 8, w, 74).fixedToCamera().setDepth(theme.depth.panel);
    // Panel children are panel-local (origin at the panel's top-left).
    note.add(makeText(this.scene, w / 2, 4, 'BACKUP / RESTORE', theme.text.accent).setOrigin(0.5, 0));
    const body = makeText(
      this.scene,
      6,
      16,
      'Your journey is kept in this browser. Clear its data, or move to a new device, and it can be lost. EXPORT keeps a copy of your whole journey as a file you can store anywhere; IMPORT carries it back.',
      theme.text.dim,
    );
    body.setWordWrapWidth(w - 12);
    note.add(body);

    let open = true;
    while (open) {
      const hasSave = this.deps.getSave() !== null;
      const choice = await new Menu(
        this.scene,
        [
          { label: 'Export a copy', value: 'export', enabled: hasSave },
          { label: 'Import a copy', value: 'import' },
          { label: 'Back', value: 'back' },
        ],
        { x: 24, y: GAME_HEIGHT - 56, width: GAME_WIDTH - 48, sfx: this.deps.sfx, cancellable: true, fixed: true },
      ).run();

      if (choice === 'export') {
        const save = this.deps.getSave();
        if (save) {
          SaveCodec.exportToFile(save);
          void this.deps.sfx?.play('ui-save');
        }
      } else if (choice === 'import') {
        const imported = await SaveCodec.importFromFile();
        if (imported) {
          await this.deps.onImport(imported);
          void this.deps.sfx?.play('ui-save');
        }
      } else {
        open = false;
      }
    }
    note.destroy();
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
        // Cycle Size 1 → 2 → 3 → Hidden → Size 1. A size step shows the controls
        // at that scale; the fourth step hides them.
        const hidden = !this.settings.controlsVisible;
        const size = this.settings.controlSize ?? 2;
        if (hidden) {
          // Hidden → Size 1 (re-show small).
          await ShellManager.setControlsVisible(true);
          await ShellManager.setControlSize(1);
          this.settings = { ...this.settings, controlsVisible: true, controlSize: 1 };
        } else if (size < 3) {
          const next = (size + 1) as ControlSize;
          await ShellManager.setControlSize(next);
          this.settings = { ...this.settings, controlSize: next };
        } else {
          // Size 3 → Hidden.
          await ShellManager.setControlsVisible(false);
          this.settings = { ...this.settings, controlsVisible: false };
        }
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
      case 'battle': {
        const current = this.settings.battlePace ?? 'cosy';
        const next: BattlePace = current === 'cosy' ? 'swift' : 'cosy';
        this.settings = { ...this.settings, battlePace: next };
        setBattlePace(next);
        await SaveManager.saveSettings(this.settings);
        void this.deps.sfx?.play('ui-toggle');
        return true;
      }
      case 'music': {
        const next = nextVolume(this.settings.musicVolume ?? 'full');
        this.settings = { ...this.settings, musicVolume: next };
        setMusicVolume(next); // notifies the live MusicDirector to re-apply
        await SaveManager.saveSettings(this.settings);
        // Confirm chime respects the NEW sfx level (unchanged here, plays normally).
        void this.deps.sfx?.play('ui-toggle');
        return true;
      }
      case 'sfx': {
        const next = nextVolume(this.settings.sfxVolume ?? 'full');
        this.settings = { ...this.settings, sfxVolume: next };
        setSfxVolume(next);
        await SaveManager.saveSettings(this.settings);
        // Play AFTER the write so the player hears the level they just set (OFF = silent).
        void this.deps.sfx?.play('ui-toggle');
        return true;
      }
      case 'backup': {
        await this.openBackup();
        return true;
      }
      case 'back':
      case null:
      default:
        return false;
    }
  }
}
