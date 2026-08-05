/**
 * NameEntry — the in-canvas "what are you called?" screen.
 *
 * Every device can finish it, because three input sources feed the same buffer
 * and none of them can fight each other:
 *
 *  - **A physical keyboard TYPES straight into it** (the natural thing to do):
 *    printable characters append, Backspace deletes, Enter confirms. This is a
 *    raw `keydown` listener rather than an InputController, deliberately — the
 *    controller binds W/A/S/D, Z, X and Space to movement/confirm/cancel, so
 *    running it here would make typing "DAWN" walk the cursor around.
 *  - **The pointer** (mouse or a bare touchscreen): tap a letter, DEL or OK.
 *  - **The device shell's on-screen pad**: the d-pad moves the grid cursor, A
 *    picks the highlighted cell, B deletes, START confirms. Read straight off
 *    the shell's window event (the touch source) so it never sees the keyboard.
 *
 * Promise-based like the rest of the kit: `await new NameEntry(scene, cfg).run()`
 * resolves with the trimmed name, or with the fallback if the player confirms an
 * empty box — the screen can never dead-end a story beat.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { SHELL_INPUT_EVENT, type ShellInputDetail } from '@/shell/ShellManager';
import type { Sfx } from '@game/systems/audio/Sfx';

export interface NameEntryConfig {
  /** Heading above the box, e.g. 'YOUR NAME'. */
  title?: string;
  /** Pre-filled text (an existing name being changed). */
  initial?: string;
  /** Returned when the player confirms an empty box. */
  fallback?: string;
  /** Hard cap on length — the box is sized for this. */
  maxLength?: number;
  sfx?: Sfx;
}

/** The on-screen grid, 10 columns wide. Uppercase only: the game compares names
 *  case-insensitively, so a second case doubles the grid for nothing. */
const ROWS = ['ABCDEFGHIJ', 'KLMNOPQRST', 'UVWXYZ0123', "456789 -'."];
const COLS = 10;
/** Grid geometry (source pixels on the 240×160 screen). */
const CELL_W = 20;
const CELL_H = 13;
const GRID_X = 16;
const GRID_Y = 62;
/** The two control cells sit on their own row under the grid. */
const CTRL_Y = GRID_Y + ROWS.length * CELL_H + 3;

const DEFAULT_MAX = 10;

export class NameEntry {
  private readonly dim: Phaser.GameObjects.Rectangle;
  private readonly panel: Panel;
  private readonly box: Phaser.GameObjects.Text;
  private readonly caret: Phaser.GameObjects.Rectangle;
  private readonly cells: Phaser.GameObjects.Text[] = [];
  private readonly delLabel: Phaser.GameObjects.Text;
  private readonly okLabel: Phaser.GameObjects.Text;
  private readonly highlight: Phaser.GameObjects.Rectangle;

  private value: string;
  private readonly maxLength: number;
  /** Grid cursor. `row === ROWS.length` is the control row (0 = DEL, 1 = OK). */
  private row = 0;
  private col = 0;

  private keyHandler?: (e: KeyboardEvent) => void;
  private shellHandler?: (e: Event) => void;
  private resolve?: (name: string) => void;
  private settled = false;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly cfg: NameEntryConfig = {},
  ) {
    this.maxLength = cfg.maxLength ?? DEFAULT_MAX;
    this.value = (cfg.initial ?? '').slice(0, this.maxLength);

    this.dim = scene.add
      .rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, hex(theme.color.panelShadow), 0.72)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(theme.depth.overlayDim);

    this.panel = new Panel(scene, 4, 4, GAME_WIDTH - 8, GAME_HEIGHT - 8).fixedToCamera();
    this.panel.add(
      makeText(scene, GAME_WIDTH / 2 - 4, theme.space.lg, cfg.title ?? 'YOUR NAME', theme.text.accent).setOrigin(0.5, 0),
    );
    this.panel.add(
      makeText(
        scene,
        GAME_WIDTH / 2 - 4,
        theme.space.lg + 12,
        'Type it and press ENTER',
        theme.text.dim,
      ).setOrigin(0.5, 0),
    );

    // The entry box: a framed strip with the name typed into it.
    const boxW = 140;
    const boxX = (GAME_WIDTH - 8 - boxW) / 2;
    const boxY = 34;
    this.panel.add(
      scene.add
        .rectangle(boxX, boxY, boxW, 14, hex(theme.color.panelShadow), 0.55)
        .setOrigin(0, 0)
        .setStrokeStyle(1, hex(theme.color.panelEdge), 0.8),
    );
    this.box = makeText(scene, boxX + 5, boxY + 4, '', theme.text.base);
    this.panel.add(this.box);
    this.caret = scene.add.rectangle(0, boxY + 3, 1, 9, hex(theme.color.selected), 1).setOrigin(0, 0);
    this.panel.add(this.caret);
    scene.tweens.add({ targets: this.caret, alpha: 0.15, duration: 480, yoyo: true, repeat: -1 });

    // The highlight sits UNDER the letters so it never hides them.
    this.highlight = scene.add
      .rectangle(0, 0, CELL_W - 2, CELL_H - 2, hex(theme.color.selected), 0.32)
      .setOrigin(0, 0);
    this.panel.add(this.highlight);

    // Letter grid — every cell is tappable, so a bare touchscreen works too.
    ROWS.forEach((rowChars, r) => {
      [...rowChars].forEach((ch, c) => {
        const t = makeText(
          scene,
          GRID_X + c * CELL_W + CELL_W / 2,
          GRID_Y + r * CELL_H + 2,
          ch === ' ' ? '_' : ch,
          theme.text.base,
        ).setOrigin(0.5, 0);
        t.setInteractive(
          new Phaser.Geom.Rectangle(-CELL_W / 2, -2, CELL_W, CELL_H),
          Phaser.Geom.Rectangle.Contains,
        );
        t.on('pointerdown', () => {
          this.row = r;
          this.col = c;
          this.refresh();
          this.append(ch);
        });
        this.panel.add(t);
        this.cells.push(t);
      });
    });

    this.delLabel = this.makeControl('DEL', GRID_X + CELL_W, () => this.backspace());
    this.okLabel = this.makeControl('OK', GRID_X + CELL_W * 6, () => this.commit());

    this.refresh();
  }

  /** One tappable control cell on the row beneath the grid. */
  private makeControl(label: string, x: number, onTap: () => void): Phaser.GameObjects.Text {
    const t = makeText(this.scene, x + CELL_W, CTRL_Y + 2, label, theme.text.base).setOrigin(0.5, 0);
    t.setInteractive(
      new Phaser.Geom.Rectangle(-CELL_W, -2, CELL_W * 2, CELL_H),
      Phaser.Geom.Rectangle.Contains,
    );
    t.on('pointerdown', onTap);
    this.panel.add(t);
    return t;
  }

  // --- State ---------------------------------------------------------------

  private append(ch: string): void {
    if (this.value.length >= this.maxLength) {
      void this.cfg.sfx?.play(theme.cursor.cancelSfx);
      return;
    }
    this.value += ch;
    void this.cfg.sfx?.play(theme.cursor.moveSfx);
    this.refresh();
  }

  private backspace(): void {
    if (this.value.length === 0) return;
    this.value = this.value.slice(0, -1);
    void this.cfg.sfx?.play(theme.cursor.cancelSfx);
    this.refresh();
  }

  private commit(): void {
    if (this.settled) return;
    // An EMPTY box never commits. Players mash Confirm through dialogue, and the
    // line right before this one ends in a question — without this guard that
    // carried-over press closes the screen before they've typed a character, and
    // the game quietly names them the fallback. A box with only spaces in it is
    // a deliberate act, and does fall back.
    if (this.value.length === 0) {
      void this.cfg.sfx?.play(theme.cursor.cancelSfx);
      this.nudge();
      return;
    }
    this.settled = true;
    void this.cfg.sfx?.play(theme.cursor.confirmSfx);
    const name = this.value.trim() || (this.cfg.fallback ?? '').trim();
    this.destroy();
    this.resolve?.(name);
  }

  /** Shake the empty box, so "nothing happened" reads as "type something". */
  private nudge(): void {
    const x = this.box.x;
    this.scene.tweens.add({
      targets: this.box,
      x: x + 3,
      duration: 55,
      yoyo: true,
      repeat: 2,
      onComplete: () => this.box.setX(x),
    });
  }

  /** Redraw the typed name, the caret, and the grid highlight. */
  private refresh(): void {
    this.box.setText(this.value);
    this.caret.x = this.box.x + this.box.width + 1;

    const onControls = this.row >= ROWS.length;
    this.highlight.setVisible(true);
    if (onControls) {
      // Straddle whichever control cell is selected (DEL is 0, OK is 1).
      const target = this.col === 0 ? this.delLabel : this.okLabel;
      this.highlight.setSize(CELL_W * 2 - 2, CELL_H - 2);
      this.highlight.setPosition(target.x - CELL_W + 1, CTRL_Y);
    } else {
      this.highlight.setSize(CELL_W - 2, CELL_H - 2);
      this.highlight.setPosition(GRID_X + this.col * CELL_W + 1, GRID_Y + this.row * CELL_H);
    }
    this.delLabel.setColor(
      onControls && this.col === 0 ? theme.text.accent.color : theme.text.base.color,
    );
    this.okLabel.setColor(
      onControls && this.col === 1 ? theme.text.accent.color : theme.text.base.color,
    );
  }

  /** Move the grid cursor, wrapping, with the control row as a fifth row. */
  private moveCursor(dx: number, dy: number): void {
    const rows = ROWS.length + 1; // + the control row
    if (dy !== 0) {
      this.row = (this.row + dy + rows) % rows;
      // Dropping onto the control row from anywhere lands on the nearer control.
      if (this.row >= ROWS.length) this.col = this.col < COLS / 2 ? 0 : 1;
      else this.col = Math.min(this.col, COLS - 1);
    }
    if (dx !== 0) {
      const width = this.row >= ROWS.length ? 2 : COLS;
      this.col = (this.col + dx + width) % width;
    }
    void this.cfg.sfx?.play(theme.cursor.moveSfx);
    this.refresh();
  }

  /** Act on the highlighted cell (the shell's A button). */
  private pickHighlighted(): void {
    if (this.row >= ROWS.length) {
      if (this.col === 0) this.backspace();
      else this.commit();
      return;
    }
    this.append(ROWS[this.row][this.col]);
  }

  // --- Run -----------------------------------------------------------------

  /** Show the screen; resolves with the entered (or fallback) name. */
  run(): Promise<string> {
    return new Promise<string>((resolve) => {
      this.resolve = resolve;

      // 1. Physical keyboard — the primary path. Raw keydown, so no InputController
      //    binding can swallow a letter.
      this.keyHandler = (e: KeyboardEvent): void => {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.commit();
          return;
        }
        if (e.key === 'Backspace') {
          e.preventDefault();
          this.backspace();
          return;
        }
        // One printable character, normalised to the grid's uppercase alphabet.
        if (e.key.length !== 1 || e.ctrlKey || e.metaKey || e.altKey) return;
        const ch = e.key.toUpperCase();
        if (!ROWS.some((r) => r.includes(ch))) return;
        e.preventDefault();
        this.append(ch);
      };
      window.addEventListener('keydown', this.keyHandler);

      // 2. The device shell's on-screen pad (touch). Read from the shell event
      //    directly so this path is blind to the keyboard entirely.
      this.shellHandler = (e: Event): void => {
        const detail = (e as CustomEvent<ShellInputDetail>).detail;
        if (!detail?.isDown) return;
        switch (detail.action) {
          case 'up':
            this.moveCursor(0, -1);
            break;
          case 'down':
            this.moveCursor(0, 1);
            break;
          case 'left':
            this.moveCursor(-1, 0);
            break;
          case 'right':
            this.moveCursor(1, 0);
            break;
          case 'confirm':
            this.pickHighlighted();
            break;
          case 'cancel':
            this.backspace();
            break;
          case 'menu':
            this.commit();
            break;
        }
      };
      window.addEventListener(SHELL_INPUT_EVENT, this.shellHandler);
    });
  }

  destroy(): void {
    if (this.keyHandler) window.removeEventListener('keydown', this.keyHandler);
    if (this.shellHandler) window.removeEventListener(SHELL_INPUT_EVENT, this.shellHandler);
    this.keyHandler = undefined;
    this.shellHandler = undefined;
    this.panel.destroy();
    this.dim.destroy();
  }
}
