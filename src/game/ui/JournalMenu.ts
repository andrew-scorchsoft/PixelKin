/**
 * JournalMenu — the Wayfarer's journal (pause menu -> JOURNAL).
 *
 * A scrolling list of the named quests the player has actually begun: UNDERWAY ones
 * first (with their "n/m" progress), then the KEPT (finished) ones in a warm grey so a
 * completed slate still reads as a quiet record of the road walked. Quests are grouped
 * by region within each section. A quest whose `start_flag` isn't held doesn't appear
 * at all — the journal is a record of what you've done, never a checklist of what's
 * left (no spoilers). Same list + detail-pane pattern as GlossaryMenu/ChartsMenu, so a
 * long blurb never overlaps the list and the screen stays readable at 240x160.
 * Up/Down move (skipping section/region headers), B backs out. Read-only and
 * promise-based; resolves when the player closes it. Built from the shared kit + theme.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { QUESTS } from '@game/content/quests';
import { REGION_ORDER, REGION_LABELS } from '@game/content/charts';
import type { QuestDef } from '@game/content/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
const HEADER_H = 12;
const ROW_H = 12;
const DETAIL_LINE_H = 9;
const DETAIL_LINES = 4;
/** KEPT quests read in a warm gold rather than the live accent — done, not gone. */
const KEPT_COLOR = theme.typeColor.Solar;
const EMPTY_LINE = 'No quests underway. The road is quiet — wander a while, and the lamp will fill these pages.';

interface QuestRow {
  quest: QuestDef;
  kept: boolean;
  /** progress n / m, or undefined for a flat (no-stage) quest. */
  have?: number;
  total?: number;
}

type Item =
  | { kind: 'section'; label: string }
  | { kind: 'region'; label: string }
  | { kind: 'entry'; row: QuestRow };

export class JournalMenu {
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly items: Item[] = [];
  private readonly rowTexts: Phaser.GameObjects.Text[] = [];
  private readonly detail: Phaser.GameObjects.Text;
  private readonly moreUp: Phaser.GameObjects.Text;
  private readonly moreDown: Phaser.GameObjects.Text;
  private readonly listTop: number;
  private readonly visibleRows: number;
  private readonly empty: boolean;
  private sel = 0; // index into items; always points at an 'entry' (when any exist)
  private scroll = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    countHeld: (prefix: string) => number,
    isHeld: (flag: string) => boolean,
    private readonly sfx?: Sfx,
  ) {
    // Build the visible rows: only STARTED quests, split underway/kept, region-grouped.
    const started: QuestRow[] = QUESTS.filter((q) => isHeld(q.start_flag)).map((quest) => {
      const kept = isHeld(quest.done_flag);
      let have: number | undefined;
      let total: number | undefined;
      if (quest.count_prefix && quest.count_total) {
        have = Math.min(quest.count_total, countHeld(quest.count_prefix));
        total = quest.count_total;
      } else if (quest.stage_flags && quest.stage_flags.length > 0) {
        have = quest.stage_flags.filter((f) => isHeld(f)).length;
        total = quest.stage_flags.length;
      }
      // A KEPT quest reads as fully done regardless of which optional stages it took.
      if (kept && total !== undefined) have = total;
      return { quest, kept, have, total };
    });

    const sections: Array<{ label: string; kept: boolean }> = [
      { label: 'UNDERWAY', kept: false },
      { label: 'KEPT', kept: true },
    ];
    for (const section of sections) {
      const rows = started.filter((r) => r.kept === section.kept);
      if (rows.length === 0) continue;
      this.items.push({ kind: 'section', label: section.label });
      for (const region of REGION_ORDER) {
        const inRegion = rows.filter((r) => r.quest.region === region);
        if (inRegion.length === 0) continue;
        this.items.push({ kind: 'region', label: REGION_LABELS[region] });
        for (const row of inRegion) this.items.push({ kind: 'entry', row });
      }
    }

    this.empty = !this.items.some((it) => it.kind === 'entry');
    this.sel = this.items.findIndex((it) => it.kind === 'entry');
    if (this.sel < 0) this.sel = 0;

    const width = GAME_WIDTH - 8;
    const height = GAME_HEIGHT - 8;
    this.listTop = PAD + HEADER_H;
    const detailTop = height - PAD - DETAIL_LINES * DETAIL_LINE_H;
    const sepY = detailTop - 4;
    const listSpace = sepY - this.listTop;
    this.visibleRows = Math.max(1, Math.floor(listSpace / ROW_H));

    this.panel = new Panel(scene, 4, 4, width, height).fixedToCamera().setDepth(theme.depth.panel);
    this.panel.add(makeText(scene, PAD, PAD - 2, "THE WAYFARER'S JOURNAL", theme.text.accent));
    this.panel.add(makeText(scene, width - PAD, PAD - 2, 'B BACK', theme.text.dim).setOrigin(1, 0));

    for (let i = 0; i < this.visibleRows; i++) {
      const t = makeText(scene, PAD + 10, this.listTop + i * ROW_H + 3, '', theme.text.base);
      this.panel.add(t);
      this.rowTexts.push(t);
    }

    this.moreUp = makeText(scene, width - PAD, this.listTop - 1, '^', theme.text.dim).setOrigin(1, 0);
    this.moreDown = makeText(scene, width - PAD, sepY - DETAIL_LINE_H, 'v', theme.text.dim).setOrigin(1, 0);
    this.panel.add(this.moreUp);
    this.panel.add(this.moreDown);

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
    if (this.empty) this.cursor.sprite.setVisible(false);
    this.refresh();
  }

  /** One row's label: name + progress, e.g. 'First-Dawn Letters  3/10'. */
  private rowLabel(row: QuestRow): string {
    if (row.have !== undefined && row.total !== undefined && !row.kept) {
      return `${row.quest.name}  ${row.have}/${row.total}`;
    }
    return row.quest.name;
  }

  private refresh(): void {
    if (this.empty) {
      this.rowTexts.forEach((t) => t.setText(''));
      this.detail.setText(EMPTY_LINE);
      this.moreUp.setVisible(false);
      this.moreDown.setVisible(false);
      return;
    }

    if (this.sel < this.scroll) this.scroll = this.sel;
    else if (this.sel >= this.scroll + this.visibleRows) this.scroll = this.sel - this.visibleRows + 1;

    this.rowTexts.forEach((t, i) => {
      const item = this.items[this.scroll + i];
      if (!item) {
        t.setText('');
        return;
      }
      if (item.kind === 'section') {
        t.setText(item.label);
        t.setColor(theme.text.accent.color);
        t.setX(PAD); // section headers hug the edge
      } else if (item.kind === 'region') {
        t.setText(` ${item.label}`);
        t.setColor(theme.text.dim.color);
        t.setX(PAD);
      } else {
        const selected = this.scroll + i === this.sel;
        t.setText(this.rowLabel(item.row));
        t.setColor(
          selected ? theme.text.accent.color : item.row.kept ? KEPT_COLOR : theme.text.base.color,
        );
        t.setX(PAD + 10); // entries indent under the cursor
      }
    });

    this.cursor.moveTo(PAD, this.listTop + (this.sel - this.scroll) * ROW_H + ROW_H / 2);

    const item = this.items[this.sel];
    if (item && item.kind === 'entry') {
      const q = item.row.quest;
      const progress =
        item.row.have !== undefined && item.row.total !== undefined && !item.row.kept
          ? `  (${item.row.have}/${item.row.total})`
          : item.row.kept
            ? '  (kept)'
            : '';
      this.detail.setText(`${q.blurb}\nGiven by ${q.giver}.${progress}`);
    } else {
      this.detail.setText('');
    }

    this.moreUp.setVisible(this.scroll > 0);
    this.moreDown.setVisible(this.scroll + this.visibleRows < this.items.length);
  }

  /** Step the cursor to the next/prev ENTRY row, skipping headers. */
  private move(dir: number): void {
    if (this.empty) return;
    let next = this.sel;
    for (let i = this.sel + dir; i >= 0 && i < this.items.length; i += dir) {
      if (this.items[i].kind === 'entry') {
        next = i;
        break;
      }
    }
    if (next !== this.sel) {
      this.sel = next;
      this.refresh();
      void this.sfx?.play(theme.cursor.moveSfx);
    }
  }

  /** Show the journal; resolve when the player backs out. */
  run(): Promise<void> {
    const input = new InputController(this.scene);
    let armed = false;
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
