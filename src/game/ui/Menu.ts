/**
 * Menu — a themed vertical list of choices (title menu, battle Fight/Catch/Run,
 * item lists, settings). Promise-based: `await menu.run()` resolves with the chosen
 * value, or null if cancelled. It owns its own input polling so it works from any
 * scene or cutscene without the host running an input loop.
 */
import Phaser from 'phaser';
import { theme } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import type { Sfx } from '@game/systems/audio/Sfx';

export interface MenuOption {
  label: string;
  value: string;
  enabled?: boolean;
  /** Optional dim right-aligned note on the row (the battle move list's uses left). */
  right?: string;
}

export interface MenuConfig {
  x: number;
  y: number;
  /** Fixed width; defaults to fit the widest label. */
  width?: number;
  /** Allow cancel (B) to close with null. Default true. */
  cancellable?: boolean;
  sfx?: Sfx;
  /** Pin to camera (HUD/modal). Default true. */
  fixed?: boolean;
  /**
   * Window the list: show at most this many rows at once and scroll as the
   * cursor moves, with ▲/▼ hints when rows hide above/below. Omit for the
   * classic all-rows-visible menu (every existing caller). For lists that
   * outgrow the 160px screen (the settings list, the rest-point list).
   */
  maxVisible?: number;
  /** Row the cursor starts on (clamped; skips disabled rows). Default 0. */
  initialIndex?: number;
  /** Called with the highlighted row's index whenever the cursor lands on a row
   *  (on open, then on every move): drive a detail pane (the battle move info). */
  onHighlight?: (index: number) => void;
  /** Called on Left (-1) / Right (+1): the list itself only moves up/down, so a
   *  caller can use the side keys for its own toggle (the battle move info). */
  onSide?: (dir: -1 | 1) => void;
}

const ROW_H = 12;
const PAD = theme.space.lg;
const CURSOR_GAP = 8;

export class Menu {
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly rows: Phaser.GameObjects.Text[] = [];
  /** Right-aligned notes, one per row (null where a row has none). */
  private readonly notes: (Phaser.GameObjects.Text | null)[] = [];
  private index = 0;
  /** First visible row when windowed (`maxVisible`). */
  private top = 0;
  private readonly visibleRows: number;
  private moreUp?: Phaser.GameObjects.Text;
  private moreDown?: Phaser.GameObjects.Text;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly options: MenuOption[],
    private readonly config: MenuConfig,
  ) {
    const charW = 8;
    const longest = Math.max(...options.map((o) => o.label.length));
    this.visibleRows = Math.max(1, Math.min(options.length, config.maxVisible ?? options.length));
    // A windowed list keeps a column at the right for its ▲/▼ hints, so a long
    // row never runs under them (the Settings "Soundtrack: Remastered" row did).
    const hintW = this.visibleRows < options.length ? charW : 0;
    const width = config.width ?? PAD * 2 + CURSOR_GAP + longest * charW + hintW;
    const height = PAD * 2 + this.visibleRows * ROW_H;
    this.panel = new Panel(scene, config.x, config.y, width, height);

    options.forEach((opt, i) => {
      const t = makeText(
        scene,
        PAD + CURSOR_GAP,
        PAD + i * ROW_H,
        opt.label,
        opt.enabled === false ? theme.text.dim : theme.text.base,
      );
      this.panel.add(t);
      this.rows.push(t);
      const note = opt.right
        ? makeText(scene, width - PAD - hintW, PAD + i * ROW_H, opt.right, theme.text.dim).setOrigin(1, 0)
        : null;
      if (note) this.panel.add(note);
      this.notes.push(note);
    });

    if (this.visibleRows < options.length) {
      // Scroll hints at the panel's right edge (the caret glyph, flipped for up).
      // Centred origin so the up hint is a clean 180° turn of the same glyph.
      this.moreUp = makeText(scene, width - PAD - 2, PAD, '▼', theme.text.accent)
        .setOrigin(0.5)
        .setAngle(180);
      this.moreDown = makeText(scene, width - PAD - 2, height - PAD, '▼', theme.text.accent).setOrigin(0.5);
      this.panel.add(this.moreUp);
      this.panel.add(this.moreDown);
    }

    this.cursor = new Cursor(scene);
    this.panel.add(this.cursor.sprite);
    // re-add so cursor renders above rows within the container
    this.panel.container.bringToTop(this.cursor.sprite);

    if (config.fixed !== false) {
      this.panel.fixedToCamera();
      this.cursor.setScrollFactor0();
    }
    const start = Phaser.Math.Clamp(config.initialIndex ?? 0, 0, Math.max(0, options.length - 1));
    this.index = this.firstEnabled(start, 1);
    this.placeCursor();
  }

  private firstEnabled(from: number, dir: number): number {
    let i = from;
    for (let n = 0; n < this.options.length; n++) {
      if (this.options[i]?.enabled !== false) return i;
      i = (i + dir + this.options.length) % this.options.length;
    }
    return from;
  }

  private placeCursor(): void {
    // Keep the cursor's row inside the visible window (a no-op when unwindowed).
    if (this.index < this.top) this.top = this.index;
    else if (this.index >= this.top + this.visibleRows) this.top = this.index - this.visibleRows + 1;
    this.rows.forEach((row, i) => {
      const slot = i - this.top;
      const shown = slot >= 0 && slot < this.visibleRows;
      row.setVisible(shown);
      row.setY(PAD + slot * ROW_H);
      this.notes[i]?.setVisible(shown).setY(PAD + slot * ROW_H);
    });
    this.moreUp?.setVisible(this.top > 0);
    this.moreDown?.setVisible(this.top + this.visibleRows < this.options.length);
    // Cursor is a child of the panel container → use local coords.
    this.cursor.moveTo(PAD, PAD + (this.index - this.top) * ROW_H + 4);
    this.config.onHighlight?.(this.index);
  }

  private move(dir: number): void {
    let i = this.index;
    do {
      i = (i + dir + this.options.length) % this.options.length;
    } while (this.options[i]?.enabled === false && i !== this.index);
    if (i !== this.index) {
      this.index = i;
      this.placeCursor();
      void this.config.sfx?.play(theme.cursor.moveSfx);
    }
  }

  /** Show the menu and resolve with the chosen value (or null if cancelled). */
  run(): Promise<string | null> {
    const input = new InputController(this.scene);
    let armed = false; // ignore the keypress that opened this menu until released
    return new Promise((resolve) => {
      const tick = (): void => {
        input.update();
        if (!armed) {
          if (!input.isDown(InputAction.Confirm) && !input.isDown(InputAction.Cancel)) armed = true;
          return;
        }
        if (input.justPressed(InputAction.Up)) this.move(-1);
        else if (input.justPressed(InputAction.Down)) this.move(1);
        else if (this.config.onSide && input.justPressed(InputAction.Left)) this.config.onSide(-1);
        else if (this.config.onSide && input.justPressed(InputAction.Right)) this.config.onSide(1);
        else if (input.justPressed(InputAction.Confirm)) {
          const opt = this.options[this.index];
          if (opt && opt.enabled !== false) {
            void this.config.sfx?.play(theme.cursor.confirmSfx);
            finish(opt.value);
          }
        } else if (input.justPressed(InputAction.Cancel) && this.config.cancellable !== false) {
          void this.config.sfx?.play(theme.cursor.cancelSfx);
          finish(null);
        }
      };
      const finish = (value: string | null): void => {
        this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
        input.destroy();
        this.destroy();
        resolve(value);
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  destroy(): void {
    this.cursor.destroy();
    this.panel.destroy();
  }
}
