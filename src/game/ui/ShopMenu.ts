/**
 * ShopMenu — a keeper's counter (opened by the cutscene op `{ op: 'shop' }`).
 *
 * Root: BUY / SELL / LEAVE. Buying lists the shop's stock (content/shops.ts)
 * with prices; selling lists the player's sellable pack at the buy-back value
 * (content/economy.ts). Both are the list + detail-pane pattern (StarterSelect /
 * ItemsMenu), with the wallet always visible in the header — one Confirm trades
 * exactly one item, so a quick tap-tap-tap stocks up and the wallet visibly
 * counts along. Key items and quest charms never appear on the sell list.
 *
 * Phase-based and self-contained like the rest of the kit: each phase attaches
 * its own short-lived InputController and tears it down before the next, so
 * presses are never double-read. `run()` resolves with the mutated inventory +
 * wicks, ready for the caller to assign back and persist.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { Menu } from './Menu';
import { DialogueBox } from './DialogueBox';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { getItem } from '@game/content/items';
import { stockItemId } from '@game/content/shops';
import { sellValue, formatWicks } from '@game/content/economy';
import type { ShopDef } from '@game/content/types';
import type { WorldFlag } from '@game/data/world/types';
import type { InventoryData } from '@game/systems/save/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
const HEADER_Y = PAD - 2;
const LIST_TOP = PAD + 12;
const ROW_H = 13;
const DETAIL_LINES = 4;
const DETAIL_LINE_H = 9;
const NAME_X = PAD + 10; // left edge of the name column (cursor sits at PAD)
const COL_GAP = 5; // minimum gap between the name column and the price column
const MARQUEE_TAIL = '   •   '; // separator looped into a scrolling clipped name
const MARQUEE_EVERY = 6; // advance the marquee one glyph every N frames

export interface ShopMenuResult {
  inventory: InventoryData;
  money: number;
}

/** One row at the counter: an item plus what changes hands for it. */
interface CounterEntry {
  id: string;
  name: string;
  desc: string;
  /** Wicks that change hands for one (price when buying, value when selling). */
  wicks: number;
  /** How many the player holds (shown on both lists). */
  held: number;
}

export class ShopMenu {
  private readonly dim: Phaser.GameObjects.Rectangle;
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly title: Phaser.GameObjects.Text;
  private readonly wallet: Phaser.GameObjects.Text;
  private readonly detail: Phaser.GameObjects.Text;
  private readonly width: number;
  private readonly detailTop: number;
  /** How many rows fit between the header and the detail pane (the rest scroll). */
  private readonly vis: number;
  /** Approximate width of one glyph, measured from the bundled font at boot. */
  private readonly charW: number;
  private readonly scrollUp: Phaser.GameObjects.Triangle;
  private readonly scrollDown: Phaser.GameObjects.Triangle;
  private money: number;
  private entries: CounterEntry[] = [];
  private rowObjects: Phaser.GameObjects.GameObject[] = [];
  /** Per-visible-row name label, indexed by screen slot (0..vis-1). */
  private names: Phaser.GameObjects.Text[] = [];
  private index = 0;
  /** Index of the first entry drawn (the scroll window's top). */
  private scrollTop = 0;
  private mode: 'buy' | 'sell' = 'buy';
  // Marquee state for the selected row's name when it's too long to fit.
  private marqueeText = ''; // full name + tail, or '' when nothing scrolls
  private marqueeChars = 0; // visible glyph budget for the name column
  private marqueePos = 0;
  private marqueeFrame = 0;
  private marqueeLabel?: Phaser.GameObjects.Text;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly shop: ShopDef,
    private readonly inventory: InventoryData,
    money: number,
    private readonly sfx?: Sfx,
    /** Flag check for gated stock lines; absent = gated lines stay hidden. */
    private readonly hasFlag?: (flag: WorldFlag) => boolean,
  ) {
    this.money = money;

    this.dim = scene.add
      .rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, hex(theme.color.panelShadow), 0.62)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(theme.depth.overlayDim);

    this.width = GAME_WIDTH - 8;
    const height = GAME_HEIGHT - 8;
    this.detailTop = height - PAD - DETAIL_LINES * DETAIL_LINE_H;
    this.vis = Math.max(1, Math.floor((this.detailTop - 4 - LIST_TOP) / ROW_H));
    this.panel = new Panel(scene, 4, 4, this.width, height).fixedToCamera();

    // Measure one glyph of the bundled font so the marquee can size its window
    // in characters (the font is near-fixed-width, so an average is plenty).
    const probe = makeText(scene, 0, 0, 'AAAAAAAAAA', theme.text.base);
    this.charW = probe.width / 10;
    probe.destroy();

    this.title = makeText(scene, PAD, HEADER_Y, shop.name, theme.text.accent);
    this.panel.add(this.title);
    // Right header carries the mode + wallet on one line, right-aligned, so a long
    // shop name and the balance never collide (the title is clipped to fit).
    this.wallet = makeText(scene, this.width - PAD, HEADER_Y, '', theme.text.base).setOrigin(1, 0);
    this.panel.add(this.wallet);

    const sep = scene.add
      .rectangle(PAD, this.detailTop - 4, this.width - PAD * 2, 1, hex(theme.color.panelEdge))
      .setOrigin(0, 0)
      .setAlpha(0.5);
    this.panel.add(sep);
    this.detail = makeText(scene, PAD, this.detailTop, '', theme.text.dim);
    this.detail.setWordWrapWidth(this.width - PAD * 2);
    this.panel.add(this.detail);

    // Scroll affordances: a small filled triangle at the top/bottom of the list
    // when there are off-screen entries above/below.
    const triColor = hex(theme.color.panelEdge);
    const triX = this.width - PAD - 2;
    this.scrollUp = scene.add
      .triangle(triX, LIST_TOP - 3, 0, 4, 4, 4, 2, 0, triColor)
      .setOrigin(0.5, 0.5)
      .setVisible(false);
    this.scrollDown = scene.add
      .triangle(triX, this.detailTop - 6, 0, 0, 4, 0, 2, 4, triColor)
      .setOrigin(0.5, 0.5)
      .setVisible(false);
    this.panel.add(this.scrollUp);
    this.panel.add(this.scrollDown);

    this.cursor = new Cursor(scene).setScrollFactor0();
    this.panel.add(this.cursor.sprite);
    this.panel.container.setVisible(false);
  }

  /** Trim a string with an ellipsis so the rendered label fits `maxW` pixels. */
  private clip(label: Phaser.GameObjects.Text, full: string, maxW: number): boolean {
    label.setText(full);
    if (label.width <= maxW) return false;
    let s = full;
    while (s.length > 1 && label.width > maxW) {
      s = s.slice(0, -1);
      label.setText(s.trimEnd() + '…');
    }
    return true;
  }

  // --- Entry collection ------------------------------------------------------

  private held(id: string): number {
    return this.inventory.items[id] ?? 0;
  }

  /** The shop's stock, priced for buying (gated lines appear once their flag is held). */
  private collectBuy(): CounterEntry[] {
    const out: CounterEntry[] = [];
    for (const entry of this.shop.stock) {
      if (typeof entry !== 'string' && !this.hasFlag?.(entry.requires_flag)) continue;
      const id = stockItemId(entry);
      const def = getItem(id);
      if (!def || def.price === undefined) continue;
      out.push({ id, name: def.name, desc: def.desc, wicks: def.price, held: this.held(id) });
    }
    return out;
  }

  /** The player's sellable pack (anything with a buy-back value). */
  private collectSell(): CounterEntry[] {
    const out: CounterEntry[] = [];
    for (const [id, count] of Object.entries(this.inventory.items)) {
      if (count <= 0) continue;
      const def = getItem(id);
      if (!def || def.category === 'key') continue;
      const value = sellValue(def);
      if (value <= 0) continue;
      out.push({ id, name: def.name, desc: def.desc, wicks: value, held: count });
    }
    out.sort((a, b) => a.name.localeCompare(b.name));
    return out;
  }

  // --- Rendering --------------------------------------------------------------

  private rebuild(): void {
    this.entries = this.mode === 'buy' ? this.collectBuy() : this.collectSell();
    this.index = Math.max(0, Math.min(this.index, this.entries.length - 1));
    this.scrollTop = Math.min(this.scrollTop, Math.max(0, this.entries.length - this.vis));
    this.ensureVisible();
    this.renderList();
    this.refresh();
  }

  /** Draw the visible scroll window of rows (entries[scrollTop .. +vis]). */
  private renderList(): void {
    for (const o of this.rowObjects) o.destroy();
    this.rowObjects = [];
    this.names = [];
    this.marqueeLabel = undefined;
    this.marqueeText = '';

    if (this.entries.length === 0) {
      const blank = this.mode === 'buy' ? 'Nothing on the shelves today.' : 'Nothing in your pack to sell.';
      this.track(makeText(this.scene, NAME_X, LIST_TOP + 4, blank, theme.text.dim));
      this.scrollUp.setVisible(false);
      this.scrollDown.setVisible(false);
      return;
    }

    const end = Math.min(this.entries.length, this.scrollTop + this.vis);
    for (let i = this.scrollTop; i < end; i++) {
      const entry = this.entries[i];
      const rowY = LIST_TOP + (i - this.scrollTop) * ROW_H;
      // Price + held count, right-aligned. Drawn first so its left edge bounds the name.
      const price = this.track(
        makeText(
          this.scene,
          this.width - PAD,
          rowY + 3,
          `${formatWicks(entry.wicks)}  x${entry.held}`,
          theme.text.base,
        ).setOrigin(1, 0),
      );
      const maxNameW = this.width - PAD - price.width - COL_GAP - NAME_X;
      const name = this.track(makeText(this.scene, NAME_X, rowY + 3, entry.name, theme.text.base));
      const overflow = this.clip(name, entry.name, maxNameW);
      this.names[i - this.scrollTop] = name;
      // The selected row reveals a too-long name by scrolling it (a marquee).
      if (i === this.index && overflow) {
        this.marqueeLabel = name;
        this.marqueeText = entry.name + MARQUEE_TAIL;
        this.marqueeChars = Math.max(1, Math.floor(maxNameW / this.charW));
        this.marqueePos = 0;
        this.marqueeFrame = 0;
        name.setText(this.marqueeText.slice(0, this.marqueeChars)); // clean start window
      }
    }
    this.scrollUp.setVisible(this.scrollTop > 0);
    this.scrollDown.setVisible(end < this.entries.length);
    this.panel.container.bringToTop(this.cursor.sprite);
  }

  private track<T extends Phaser.GameObjects.GameObject>(obj: T): T {
    this.panel.add(obj);
    this.rowObjects.push(obj);
    return obj;
  }

  private refresh(): void {
    this.wallet.setText(`${this.mode === 'buy' ? 'BUY' : 'SELL'} ${formatWicks(this.money)}`);
    // Clip the shop name to whatever room the mode + wallet leave it.
    this.clip(this.title, this.shop.name, this.width - PAD - this.wallet.width - COL_GAP - PAD);
    if (this.entries.length === 0) {
      this.cursor.sprite.setVisible(false);
      this.detail.setText('');
      return;
    }
    this.cursor.sprite.setVisible(true);
    const slot = this.index - this.scrollTop;
    this.cursor.moveTo(PAD, LIST_TOP + slot * ROW_H + ROW_H / 2);
    const affordable = (e: CounterEntry): boolean => this.mode === 'sell' || e.wicks <= this.money;
    this.names.forEach((name, s) => {
      const e = this.entries[this.scrollTop + s];
      name.setColor(
        this.scrollTop + s === this.index
          ? theme.text.accent.color
          : affordable(e)
            ? theme.text.base.color
            : theme.text.dim.color,
      );
    });
    this.setDetail(this.entries[this.index].desc);
  }

  /** Show a description, clamped to the detail box so it never runs off-screen. */
  private setDetail(desc: string): void {
    this.detail.setText(desc);
    const lines = this.detail.getWrappedText(desc);
    if (lines.length > DETAIL_LINES) {
      const keep = lines.slice(0, DETAIL_LINES);
      const trimmed = keep[keep.length - 1].replace(/\s+\S*$/, '');
      keep[keep.length - 1] = (trimmed || keep[keep.length - 1]) + '…';
      this.detail.setText(keep.join('\n'));
    }
  }

  /** Move the scroll window so the current selection sits inside it. */
  private ensureVisible(): void {
    if (this.index < this.scrollTop) this.scrollTop = this.index;
    else if (this.index >= this.scrollTop + this.vis) this.scrollTop = this.index - this.vis + 1;
  }

  /** Advance the selected row's name marquee (called each frame while trading). */
  private tickMarquee(): void {
    if (!this.marqueeLabel || !this.marqueeText) return;
    if (++this.marqueeFrame < MARQUEE_EVERY) return;
    this.marqueeFrame = 0;
    this.marqueePos = (this.marqueePos + 1) % this.marqueeText.length;
    const doubled = this.marqueeText + this.marqueeText;
    this.marqueeLabel.setText(doubled.slice(this.marqueePos, this.marqueePos + this.marqueeChars));
  }

  private move(dir: number): void {
    if (this.entries.length === 0) return;
    const next = (this.index + dir + this.entries.length) % this.entries.length;
    if (next !== this.index) {
      this.index = next;
      this.ensureVisible();
      this.renderList();
      this.refresh();
      void this.sfx?.play(theme.cursor.moveSfx);
    }
  }

  // --- Phases -------------------------------------------------------------------

  /** Run the counter; resolve with the mutated inventory + wicks on LEAVE. */
  async run(): Promise<ShopMenuResult> {
    let open = true;
    while (open) {
      this.panel.container.setVisible(false);
      const choice = await new Menu(
        this.scene,
        [
          { label: 'BUY', value: 'buy' },
          { label: 'SELL', value: 'sell' },
          { label: 'LEAVE', value: 'leave' },
        ],
        { x: 8, y: 8, sfx: this.sfx },
      ).run();

      if (choice === 'buy' || choice === 'sell') {
        this.mode = choice;
        this.index = 0;
        this.panel.container.setVisible(true);
        this.rebuild();
        await this.tradeLoop();
      } else {
        open = false; // LEAVE or cancel
      }
    }
    this.destroy();
    return { inventory: this.inventory, money: this.money };
  }

  /** Cursor over the counter list; Confirm trades one of the selection; Cancel backs out. */
  private tradeLoop(): Promise<void> {
    const input = new InputController(this.scene);
    let armed = false;
    return new Promise((resolve) => {
      const finish = (): void => {
        this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
        input.destroy();
        resolve();
      };
      const tick = (): void => {
        input.update();
        this.tickMarquee();
        if (!armed) {
          if (!input.isDown(InputAction.Confirm) && !input.isDown(InputAction.Cancel)) armed = true;
          return;
        }
        if (input.justPressed(InputAction.Up)) this.move(-1);
        else if (input.justPressed(InputAction.Down)) this.move(1);
        else if (input.justPressed(InputAction.Confirm)) this.tradeOne();
        else if (input.justPressed(InputAction.Cancel)) {
          void this.sfx?.play(theme.cursor.cancelSfx);
          finish();
        }
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  /** Trade exactly one of the selected entry (the wallet/header narrate the result). */
  private tradeOne(): void {
    if (this.entries.length === 0) return;
    const entry = this.entries[this.index];

    if (this.mode === 'buy') {
      if (entry.wicks > this.money) {
        void this.sfx?.play(theme.cursor.cancelSfx);
        return; // can't afford — the dim row already says so
      }
      this.money -= entry.wicks;
      this.inventory.items[entry.id] = (this.inventory.items[entry.id] ?? 0) + 1;
      void this.sfx?.playVariant('world-pickup', ['a', 'b', 'c']);
    } else {
      this.money += entry.wicks;
      this.inventory.items[entry.id] = (this.inventory.items[entry.id] ?? 1) - 1;
      if (this.inventory.items[entry.id] <= 0) delete this.inventory.items[entry.id];
      void this.sfx?.play(theme.cursor.confirmSfx);
    }
    this.rebuild();
  }

  /** A keeper has nothing to say when the registry is missing the shop. */
  static async missing(scene: Phaser.Scene, sfx?: Sfx): Promise<void> {
    await new DialogueBox(scene, sfx).run([
      { text: 'The counter is bare — the trade-cart must be late again.' },
    ]);
  }

  destroy(): void {
    this.cursor.destroy();
    this.panel.destroy();
    this.dim.destroy();
  }
}
