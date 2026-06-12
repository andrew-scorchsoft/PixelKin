/**
 * TravelMenu — the Lanternway's waystone map (pause menu -> TRAVEL).
 *
 * Once the four-way hub is lit, the apprentice can step the lit road between the
 * towns they've reached. This is the region-grouped list + detail-pane envelope
 * (the JournalMenu/ChartsMenu pattern, so a long flavour line never overlaps the
 * list): each known waystone shows its name under its region header, with its
 * canon flavour in the detail pane. The town the player is STANDING in is shown
 * too — but greyed and unselectable ("you are here"). Up/Down move (skipping
 * headers + the here-row), A travels, B backs out.
 *
 * Only waystones whose visited_flag is held are listed, so the map fills in as the
 * player explores. Read-only, promise-based: resolves with the chosen Waystone, or
 * undefined if the player backs out. Built from the shared kit + theme tokens.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { WAYSTONES, WAYSTONE_REGION_ORDER } from '@game/content/waystones';
import { REGION_LABELS } from '@game/content/charts';
import type { Waystone } from '@game/content/waystones';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
const HEADER_H = 12;
const ROW_H = 12;
const DETAIL_LINE_H = 9;
const DETAIL_LINES = 4;
const HERE_LABEL = '(you are here)';
const EMPTY_LINE = 'No waystones lit yet. Walk the road a while, and the Lanternway will open to you.';

type Item =
  | { kind: 'region'; label: string }
  | { kind: 'entry'; stone: Waystone; here: boolean };

export class TravelMenu {
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
  private sel = 0; // index into items; always points at a SELECTABLE entry (when any exist)
  private scroll = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    currentMap: string,
    isHeld: (flag: string) => boolean,
    private readonly sfx?: Sfx,
  ) {
    // Build the visible rows: only REACHED waystones, region-grouped. The current
    // map's stone is shown (as a here-row) so the player always sees where they are.
    for (const region of WAYSTONE_REGION_ORDER) {
      const stones = WAYSTONES.filter((s) => s.region === region && isHeld(s.visited_flag));
      if (stones.length === 0) continue;
      this.items.push({ kind: 'region', label: REGION_LABELS[region] });
      for (const stone of stones) this.items.push({ kind: 'entry', stone, here: stone.map === currentMap });
    }

    this.empty = !this.items.some((it) => it.kind === 'entry' && !it.here);
    this.sel = this.firstSelectable(0, 1);
    if (this.sel < 0) this.sel = this.items.findIndex((it) => it.kind === 'entry');
    if (this.sel < 0) this.sel = 0;

    const width = GAME_WIDTH - 8;
    const height = GAME_HEIGHT - 8;
    this.listTop = PAD + HEADER_H;
    const detailTop = height - PAD - DETAIL_LINES * DETAIL_LINE_H;
    const sepY = detailTop - 4;
    const listSpace = sepY - this.listTop;
    this.visibleRows = Math.max(1, Math.floor(listSpace / ROW_H));

    this.panel = new Panel(scene, 4, 4, width, height).fixedToCamera().setDepth(theme.depth.panel);
    this.panel.add(makeText(scene, PAD, PAD - 2, 'THE LANTERNWAY', theme.text.accent));
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

  /** First SELECTABLE entry (an entry that isn't the here-row) from `start`, stepping `dir`. */
  private firstSelectable(start: number, dir: number): number {
    for (let i = start; i >= 0 && i < this.items.length; i += dir) {
      const it = this.items[i];
      if (it.kind === 'entry' && !it.here) return i;
    }
    return -1;
  }

  private refresh(): void {
    if (this.empty) {
      this.rowTexts.forEach((t, i) => {
        // Still paint the region/here rows so the player sees where they are.
        const item = this.items[this.scroll + i];
        if (!item) {
          t.setText('');
          return;
        }
        if (item.kind === 'region') {
          t.setText(item.label);
          t.setColor(theme.text.accent.color);
          t.setX(PAD);
        } else {
          t.setText(`${item.stone.name}  ${HERE_LABEL}`);
          t.setColor(theme.text.dim.color);
          t.setX(PAD + 10);
        }
      });
      this.detail.setText(EMPTY_LINE);
      this.moreUp.setVisible(this.scroll > 0);
      this.moreDown.setVisible(this.scroll + this.visibleRows < this.items.length);
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
      if (item.kind === 'region') {
        t.setText(item.label);
        t.setColor(theme.text.accent.color);
        t.setX(PAD);
      } else if (item.here) {
        t.setText(`${item.stone.name}  ${HERE_LABEL}`);
        t.setColor(theme.text.dim.color);
        t.setX(PAD + 10);
      } else {
        const selected = this.scroll + i === this.sel;
        t.setText(item.stone.name);
        t.setColor(selected ? theme.text.accent.color : theme.text.base.color);
        t.setX(PAD + 10);
      }
    });

    this.cursor.moveTo(PAD, this.listTop + (this.sel - this.scroll) * ROW_H + ROW_H / 2);

    const item = this.items[this.sel];
    if (item && item.kind === 'entry') {
      this.detail.setText(item.here ? `${item.stone.flavour}\nYou are already here.` : item.stone.flavour);
    } else {
      this.detail.setText('');
    }

    this.moreUp.setVisible(this.scroll > 0);
    this.moreDown.setVisible(this.scroll + this.visibleRows < this.items.length);
  }

  /** Step the cursor to the next/prev SELECTABLE entry, skipping headers + the here-row. */
  private move(dir: number): void {
    if (this.empty) return;
    const next = this.firstSelectable(this.sel + dir, dir);
    if (next >= 0 && next !== this.sel) {
      this.sel = next;
      this.refresh();
      void this.sfx?.play(theme.cursor.moveSfx);
    }
  }

  /** Show the travel map; resolve with the chosen waystone (or undefined on back-out). */
  run(): Promise<Waystone | undefined> {
    const input = new InputController(this.scene);
    let armed = false;
    return new Promise((resolve) => {
      const close = (result: Waystone | undefined): void => {
        this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
        input.destroy();
        this.destroy();
        resolve(result);
      };
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
          if (!this.empty && item?.kind === 'entry' && !item.here) {
            void this.sfx?.play(theme.cursor.confirmSfx);
            close(item.stone);
          } else {
            void this.sfx?.play(theme.cursor.cancelSfx); // here-row / empty can't be travelled
          }
        } else if (input.justPressed(InputAction.Cancel)) {
          void this.sfx?.play(theme.cursor.cancelSfx);
          close(undefined);
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
