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
import { sellValue, formatWicks } from '@game/content/economy';
import type { ShopDef } from '@game/content/types';
import type { InventoryData } from '@game/systems/save/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
const LIST_TOP = PAD + 14;
const ROW_H = 14;
const DETAIL_LINES = 3;
const DETAIL_LINE_H = 9;

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
  private money: number;
  private entries: CounterEntry[] = [];
  private rowObjects: Phaser.GameObjects.GameObject[] = [];
  private names: Phaser.GameObjects.Text[] = [];
  private index = 0;
  private mode: 'buy' | 'sell' = 'buy';

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly shop: ShopDef,
    private readonly inventory: InventoryData,
    money: number,
    private readonly sfx?: Sfx,
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
    this.panel = new Panel(scene, 4, 4, this.width, height).fixedToCamera();

    this.title = makeText(scene, PAD, PAD - 2, shop.name, theme.text.accent);
    this.panel.add(this.title);
    this.wallet = makeText(scene, this.width - PAD, PAD - 2, '', theme.text.base).setOrigin(1, 0);
    this.panel.add(this.wallet);

    const sep = scene.add
      .rectangle(PAD, this.detailTop - 4, this.width - PAD * 2, 1, hex(theme.color.panelEdge))
      .setOrigin(0, 0)
      .setAlpha(0.5);
    this.panel.add(sep);
    this.detail = makeText(scene, PAD, this.detailTop, '', theme.text.dim);
    this.detail.setWordWrapWidth(this.width - PAD * 2);
    this.panel.add(this.detail);

    this.cursor = new Cursor(scene).setScrollFactor0();
    this.panel.add(this.cursor.sprite);
    this.panel.container.setVisible(false);
  }

  // --- Entry collection ------------------------------------------------------

  private held(id: string): number {
    return this.inventory.items[id] ?? 0;
  }

  /** The shop's stock, priced for buying. */
  private collectBuy(): CounterEntry[] {
    const out: CounterEntry[] = [];
    for (const id of this.shop.stock) {
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
    for (const o of this.rowObjects) o.destroy();
    this.rowObjects = [];
    this.names = [];
    this.entries = this.mode === 'buy' ? this.collectBuy() : this.collectSell();
    this.index = Math.max(0, Math.min(this.index, this.entries.length - 1));
    this.title.setText(`${this.shop.name} — ${this.mode === 'buy' ? 'BUY' : 'SELL'}`);

    if (this.entries.length === 0) {
      const blank = this.mode === 'buy' ? 'Nothing on the shelves today.' : 'Nothing in your pack to sell.';
      this.track(makeText(this.scene, PAD, LIST_TOP + 4, blank, theme.text.dim));
    } else {
      this.entries.forEach((entry, i) => {
        const rowY = LIST_TOP + i * ROW_H;
        const name = makeText(this.scene, PAD + 10, rowY + 3, entry.name, theme.text.base);
        this.track(name);
        this.names.push(name);
        this.track(
          makeText(
            this.scene,
            this.width - PAD,
            rowY + 3,
            `${formatWicks(entry.wicks)}  x${entry.held}`,
            theme.text.base,
          ).setOrigin(1, 0),
        );
      });
    }
    this.panel.container.bringToTop(this.cursor.sprite);
    this.refresh();
  }

  private track<T extends Phaser.GameObjects.GameObject>(obj: T): T {
    this.panel.add(obj);
    this.rowObjects.push(obj);
    return obj;
  }

  private refresh(): void {
    this.wallet.setText(formatWicks(this.money));
    if (this.entries.length === 0) {
      this.cursor.sprite.setVisible(false);
      this.detail.setText('');
      return;
    }
    this.cursor.sprite.setVisible(true);
    this.cursor.moveTo(PAD, LIST_TOP + this.index * ROW_H + ROW_H / 2);
    const affordable = (e: CounterEntry): boolean => this.mode === 'sell' || e.wicks <= this.money;
    this.names.forEach((name, i) => {
      const e = this.entries[i];
      name.setColor(
        i === this.index ? theme.text.accent.color : affordable(e) ? theme.text.base.color : theme.text.dim.color,
      );
    });
    this.detail.setText(this.entries[this.index].desc);
  }

  private move(dir: number): void {
    if (this.entries.length === 0) return;
    const next = (this.index + dir + this.entries.length) % this.entries.length;
    if (next !== this.index) {
      this.index = next;
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
