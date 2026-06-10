/**
 * GlossaryMenu — the in-vesperlamp codex (pause menu -> LORE).
 *
 * Lists Vesperholm's vocabulary as a scrolling column of compact rows, with a detail
 * pane below that shows only the *selected* term's definition and refreshes as the
 * cursor moves — the same list + detail pattern as StarterSelect, so long blurbs
 * never overlap the list and the screen stays readable at 240x160. Terms the player
 * hasn't met yet read as "? ? ?" teases (revealed by `unlock_flag` in the registry),
 * so the codex visibly fills in as the world is learned. Up/Down scroll, B backs out.
 * Read-only and promise-based: resolves when the player closes it. Built entirely from
 * the shared kit + theme tokens.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { GLOSSARY } from '@game/content/glossary';
import type { GlossaryEntry } from '@game/content/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
const HEADER_H = 12;
const ROW_H = 12;
const DETAIL_LINE_H = 9;
// Sized one line clear of the longest authored blurb (worst case ~6 lines), so a
// definition never clips even if the browser's font metrics wrap a touch wider than
// authoring assumed. At 240x160 this still leaves room for 5 list rows + scroll.
const DETAIL_LINES = 7;
const LOCKED_LABEL = '? ? ?';
const LOCKED_DESC = "You've not learned this yet — keep walking the Wayfaring, and the lamp will hold it for you.";

interface Row {
  entry: GlossaryEntry;
  unlocked: boolean;
}

export class GlossaryMenu {
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly rows: Row[];
  private readonly rowTexts: Phaser.GameObjects.Text[] = [];
  private readonly detail: Phaser.GameObjects.Text;
  private readonly moreUp: Phaser.GameObjects.Text;
  private readonly moreDown: Phaser.GameObjects.Text;
  private readonly listTop: number;
  private readonly visibleRows: number;
  private index = 0;
  private scroll = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    isUnlocked: (flag: string) => boolean,
    private readonly sfx?: Sfx,
  ) {
    this.rows = GLOSSARY.map((entry) => ({
      entry,
      unlocked: !entry.unlock_flag || isUnlocked(entry.unlock_flag),
    }));

    const width = GAME_WIDTH - 8;
    const height = GAME_HEIGHT - 8;
    const x = 4;
    const y = 4;
    this.listTop = PAD + HEADER_H;
    const detailTop = height - PAD - DETAIL_LINES * DETAIL_LINE_H;
    const sepY = detailTop - 4;
    const listSpace = sepY - this.listTop;
    this.visibleRows = Math.max(1, Math.floor(listSpace / ROW_H));

    this.panel = new Panel(scene, x, y, width, height).fixedToCamera().setDepth(theme.depth.panel);

    // Header: in-world title + the back hint.
    this.panel.add(makeText(scene, PAD, PAD - 2, "THE LAMP'S KEEPING", theme.text.accent));
    this.panel.add(makeText(scene, width - PAD, PAD - 2, 'B BACK', theme.text.dim).setOrigin(1, 0));

    // Pre-create the visible row slots; refresh() fills their text/colour from the
    // current scroll window (never one Text per entry — the list scrolls).
    for (let i = 0; i < this.visibleRows; i++) {
      const t = makeText(scene, PAD + 10, this.listTop + i * ROW_H + 3, '', theme.text.base);
      this.panel.add(t);
      this.rowTexts.push(t);
    }

    // Scroll affordances (shown only when there's content off-window).
    this.moreUp = makeText(scene, width - PAD, this.listTop - 1, '^', theme.text.dim).setOrigin(1, 0);
    this.moreDown = makeText(scene, width - PAD, sepY - DETAIL_LINE_H, 'v', theme.text.dim).setOrigin(1, 0);
    this.panel.add(this.moreUp);
    this.panel.add(this.moreDown);

    // Detail pane: a thin separator + the selected term's definition, wrapped.
    const sep = scene.add
      .rectangle(PAD, sepY, width - PAD * 2, 1, hex(theme.color.panelEdge))
      .setOrigin(0, 0)
      .setAlpha(0.5);
    this.panel.add(sep);
    this.detail = makeText(scene, PAD, detailTop, '', theme.text.dim);
    this.detail.setWordWrapWidth(width - PAD * 2);
    this.panel.add(this.detail);

    this.cursor = new Cursor(scene).setScrollFactor0();
    this.panel.add(this.cursor.sprite);
    this.refresh();
  }

  /** Reflect the current selection + scroll window: rows, cursor, blurb, arrows. */
  private refresh(): void {
    // Keep the selected entry inside the visible window.
    if (this.index < this.scroll) this.scroll = this.index;
    else if (this.index >= this.scroll + this.visibleRows) this.scroll = this.index - this.visibleRows + 1;

    this.rowTexts.forEach((t, i) => {
      const row = this.rows[this.scroll + i];
      if (!row) {
        t.setText('');
        return;
      }
      const selected = this.scroll + i === this.index;
      t.setText(row.unlocked ? row.entry.term : LOCKED_LABEL);
      t.setColor(
        selected ? theme.text.accent.color : row.unlocked ? theme.text.base.color : theme.text.dim.color,
      );
    });

    this.cursor.moveTo(PAD, this.listTop + (this.index - this.scroll) * ROW_H + ROW_H / 2);

    const row = this.rows[this.index];
    this.detail.setText(row ? (row.unlocked ? row.entry.desc : LOCKED_DESC) : '');

    this.moreUp.setVisible(this.scroll > 0);
    this.moreDown.setVisible(this.scroll + this.visibleRows < this.rows.length);
  }

  private move(dir: number): void {
    const next = Math.min(this.rows.length - 1, Math.max(0, this.index + dir));
    if (next !== this.index) {
      this.index = next;
      this.refresh();
      void this.sfx?.play(theme.cursor.moveSfx);
    }
  }

  /** Show the codex; resolve when the player backs out. */
  run(): Promise<void> {
    const input = new InputController(this.scene);
    let armed = false; // ignore the press that opened this screen until released
    return new Promise((resolve) => {
      const tick = (): void => {
        input.update();
        if (!armed) {
          if (!input.isDown(InputAction.Confirm) && !input.isDown(InputAction.Cancel)) armed = true;
          return;
        }
        if (input.justPressed(InputAction.Up)) this.move(-1);
        else if (input.justPressed(InputAction.Down)) this.move(1);
        else if (input.justPressed(InputAction.Cancel) || input.justPressed(InputAction.Confirm)) {
          void this.sfx?.play(theme.cursor.cancelSfx);
          this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
          input.destroy();
          this.destroy();
          resolve();
        }
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  destroy(): void {
    this.cursor.destroy();
    this.panel.destroy();
  }
}
