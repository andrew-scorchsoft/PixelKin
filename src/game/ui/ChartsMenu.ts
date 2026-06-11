/**
 * ChartsMenu — the Wayfarer's Charts gallery (pause menu -> CHARTS).
 *
 * A scrolling, region-grouped roster of every area, route and landmark in Vesperholm.
 * Places the player has set foot in show their name and open to the full concept-art
 * piece (flip left/right through the ones collected so far); places not yet visited
 * read as "? ? ?" teases under their region header, with a "found / total" tally — so
 * the shape of the world, and the corners still to walk, are visible without spoiling
 * them. Same list + detail-pane pattern as GlossaryMenu, so long mood-lines never
 * overlap the list. Up/Down move, A opens a discovered chart, B backs out.
 *
 * Multi-phase (per the house style): the LIST phase and the full-screen VIEWER phase
 * each own their InputController + update tick and tear both down before handing over,
 * so a press is never double-read. Read-only and promise-based; resolves on back-out.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { ChartView } from './ChartView';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { CHARTS, REGION_ORDER, REGION_LABELS, chartFlag } from '@game/content/charts';
import type { ChartEntry } from '@game/content/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
const HEADER_H = 12;
const ROW_H = 12;
const DETAIL_LINE_H = 9;
const DETAIL_LINES = 4;
const LOCKED_LABEL = '? ? ?';
const LOCKED_DESC = 'An unwalked corner of the dusk — somewhere out there, a chart waiting to be drawn.';

type Item =
  | { kind: 'header'; region: (typeof REGION_ORDER)[number]; found: number; total: number }
  | { kind: 'entry'; chart: ChartEntry; discovered: boolean };

export class ChartsMenu {
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly items: Item[] = [];
  /** Discovered charts in registry order — what the viewer flips through. */
  private readonly discovered: ChartEntry[] = [];
  private readonly rowTexts: Phaser.GameObjects.Text[] = [];
  private readonly detail: Phaser.GameObjects.Text;
  private readonly moreUp: Phaser.GameObjects.Text;
  private readonly moreDown: Phaser.GameObjects.Text;
  private readonly listTop: number;
  private readonly visibleRows: number;
  private sel = 0; // index into items; always points at an 'entry'
  private scroll = 0;
  private finishRun?: () => void;

  constructor(
    private readonly scene: Phaser.Scene,
    isUnlocked: (flag: string) => boolean,
    private readonly sfx?: Sfx,
  ) {
    // Group charts by region, in display order, with a header carrying the tally.
    for (const region of REGION_ORDER) {
      const charts = CHARTS.filter((c) => c.region === region);
      if (charts.length === 0) continue;
      const unlocked = charts.map((c) => isUnlocked(chartFlag(c)));
      const found = unlocked.filter(Boolean).length;
      this.items.push({ kind: 'header', region, found, total: charts.length });
      charts.forEach((chart, i) => {
        const discovered = unlocked[i];
        this.items.push({ kind: 'entry', chart, discovered });
        if (discovered) this.discovered.push(chart);
      });
    }
    // Start on the first discoverable/entry row (skip the leading header).
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
    this.panel.add(makeText(scene, PAD, PAD - 2, "THE WAYFARER'S CHARTS", theme.text.accent));
    this.panel.add(
      makeText(scene, width - PAD, PAD - 2, `${this.discovered.length}/${CHARTS.length}`, theme.text.dim).setOrigin(
        1,
        0,
      ),
    );

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
    this.refresh();
  }

  /** Reflect the current selection + scroll window: rows, cursor, mood line, arrows. */
  private refresh(): void {
    if (this.sel < this.scroll) this.scroll = this.sel;
    else if (this.sel >= this.scroll + this.visibleRows) this.scroll = this.sel - this.visibleRows + 1;

    this.rowTexts.forEach((t, i) => {
      const item = this.items[this.scroll + i];
      if (!item) {
        t.setText('');
        return;
      }
      if (item.kind === 'header') {
        t.setText(`${REGION_LABELS[item.region]}   ${item.found}/${item.total}`);
        t.setColor(theme.text.accent.color);
        t.setX(PAD); // headers hug the panel edge (no cursor gutter)
      } else {
        const selected = this.scroll + i === this.sel;
        t.setText(item.discovered ? item.chart.name : LOCKED_LABEL);
        t.setColor(
          selected ? theme.text.accent.color : item.discovered ? theme.text.base.color : theme.text.dim.color,
        );
        t.setX(PAD + 10); // entries indent under the cursor
      }
    });

    this.cursor.moveTo(PAD, this.listTop + (this.sel - this.scroll) * ROW_H + ROW_H / 2);

    const item = this.items[this.sel];
    if (item && item.kind === 'entry') {
      this.detail.setText(item.discovered ? item.chart.subtitle : LOCKED_DESC);
    } else {
      this.detail.setText('');
    }

    this.moreUp.setVisible(this.scroll > 0);
    this.moreDown.setVisible(this.scroll + this.visibleRows < this.items.length);
  }

  /** Step the cursor to the next/prev ENTRY row, skipping region headers. */
  private move(dir: number): void {
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

  /** Show the gallery; resolve when the player backs out of the list. */
  run(): Promise<void> {
    return new Promise((resolve) => {
      this.finishRun = resolve;
      this.startListPhase();
    });
  }

  // --- LIST phase -----------------------------------------------------------

  private startListPhase(): void {
    const input = new InputController(this.scene);
    let armed = false;
    const tick = (): void => {
      input.update();
      if (!armed) {
        if (!input.isDown(InputAction.Confirm) && !input.isDown(InputAction.Cancel)) armed = true;
        return;
      }
      if (input.justPressed(InputAction.Up)) this.move(-1);
      else if (input.justPressed(InputAction.Down)) this.move(1);
      else if (input.justPressed(InputAction.Confirm)) {
        const item = this.items[this.sel];
        if (item?.kind === 'entry' && item.discovered) {
          this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
          input.destroy();
          void this.openViewer(item.chart);
        } else {
          void this.sfx?.play(theme.cursor.cancelSfx); // a tease can't be opened yet
        }
      } else if (input.justPressed(InputAction.Cancel)) {
        void this.sfx?.play(theme.cursor.cancelSfx);
        this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
        input.destroy();
        this.destroy();
        this.finishRun?.();
      }
    };
    this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
  }

  // --- VIEWER phase (full-screen, flip left/right) --------------------------

  private async openViewer(chart: ChartEntry): Promise<void> {
    const view = new ChartView(this.scene, { mode: 'gallery' });
    let pos = Math.max(0, this.discovered.indexOf(chart));
    const arrows = (): { left: boolean; right: boolean } => ({
      left: pos > 0,
      right: pos < this.discovered.length - 1,
    });
    void this.sfx?.play(theme.cursor.confirmSfx);
    await view.setChart(this.discovered[pos], arrows());

    const input = new InputController(this.scene);
    let armed = false;
    const tick = (): void => {
      input.update();
      if (!armed) {
        if (!input.isDown(InputAction.Confirm) && !input.isDown(InputAction.Cancel)) armed = true;
        return;
      }
      if (input.justPressed(InputAction.Left) && pos > 0) {
        pos -= 1;
        void this.sfx?.play(theme.cursor.moveSfx);
        void view.setChart(this.discovered[pos], arrows());
      } else if (input.justPressed(InputAction.Right) && pos < this.discovered.length - 1) {
        pos += 1;
        void this.sfx?.play(theme.cursor.moveSfx);
        void view.setChart(this.discovered[pos], arrows());
      } else if (input.justPressed(InputAction.Cancel) || input.justPressed(InputAction.Confirm)) {
        void this.sfx?.play(theme.cursor.cancelSfx);
        this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
        input.destroy();
        view.destroy();
        // Return to the list, parked on whatever chart we left on.
        this.selectChart(this.discovered[pos]);
        this.startListPhase();
      }
    };
    this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
  }

  /** Park the list cursor on a given chart's row (after closing the viewer). */
  private selectChart(chart: ChartEntry): void {
    const idx = this.items.findIndex((it) => it.kind === 'entry' && it.chart === chart);
    if (idx >= 0) this.sel = idx;
    this.refresh();
  }

  destroy(): void {
    this.cursor.destroy();
    this.panel.destroy();
  }
}
