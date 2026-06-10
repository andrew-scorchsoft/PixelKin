/**
 * ItemsMenu — the overworld "what's in my pack" screen (opened from the pause menu).
 *
 * Lists everything the player is carrying — name + count — with a detail pane below
 * that shows only the *selected* item's description and updates as the cursor moves
 * (the same list + detail pattern StarterSelect uses, so a long blurb never overlaps
 * the list on the 240×160 screen). Pressing A on a usable item (a medicine) opens a
 * kin picker and applies it; lamps/keys can't be used from the field. B backs out.
 *
 * Phase-based and self-contained like the rest of the kit (PartyMenu / Menu): each
 * interaction spins up its own short-lived InputController and tears it down before
 * the next, so sub-menus never double-read the same press. `run()` resolves with the
 * (possibly healed) party and (possibly decremented) inventory, ready for the save.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { Menu, type MenuOption } from './Menu';
import { DialogueBox } from './DialogueBox';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { KinInstance } from '@game/systems/party/KinInstance';
import { MOVE_BY_ID } from '@game/data/dex';
import { getItem } from '@game/content/items';
import { formatWicks } from '@game/content/economy';
import type { ItemCategory } from '@game/content/types';
import type { KinInstanceData, InventoryData } from '@game/systems/save/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
/** Top of the scrollable row list inside the panel. */
const LIST_TOP = PAD + 14;
/** One compact list row: name on the left, count on the right. */
const ROW_H = 14;
/** Detail pane geometry, anchored near the panel's bottom edge. */
const DETAIL_LINES = 3;
const DETAIL_LINE_H = 9;

/** The result handed back to the caller for persistence. */
export interface ItemsMenuResult {
  party: KinInstanceData[];
  inventory: InventoryData;
}

/** One carried item, resolved to its definition for display + use. */
interface PackEntry {
  id: string;
  name: string;
  desc: string;
  category: ItemCategory;
  heal?: number;
  teach_move?: string;
  count: number;
}

export class ItemsMenu {
  private readonly dim: Phaser.GameObjects.Rectangle;
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly detail: Phaser.GameObjects.Text;
  private readonly width: number;
  private readonly detailTop: number;
  /** Live party as instances, so a heal mutates real hp; serialised back on close. */
  private readonly members: KinInstance[];
  private entries: PackEntry[] = [];
  /** Per-build row objects, destroyed and rebuilt when counts change. */
  private rowObjects: Phaser.GameObjects.GameObject[] = [];
  private names: Phaser.GameObjects.Text[] = [];
  private index = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly inventory: InventoryData,
    party: KinInstanceData[],
    private readonly sfx?: Sfx,
    /** When provided, the wallet shows beside the title (read-only here). */
    private readonly money?: number,
  ) {
    this.members = party.map((d) => KinInstance.fromData(d));

    this.dim = scene.add
      .rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, hex(theme.color.panelShadow), 0.62)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(theme.depth.overlayDim);

    this.width = GAME_WIDTH - 8;
    const height = GAME_HEIGHT - 8;
    this.detailTop = height - PAD - DETAIL_LINES * DETAIL_LINE_H;
    this.panel = new Panel(scene, 4, 4, this.width, height).fixedToCamera();

    const title = this.money !== undefined ? `ITEMS — ${formatWicks(this.money)}` : 'ITEMS';
    this.panel.add(makeText(scene, PAD, PAD - 2, title, theme.text.accent));
    this.panel.add(
      makeText(scene, this.width - PAD, PAD - 2, 'A USE  B BACK', theme.text.dim).setOrigin(1, 0),
    );

    // Detail pane: a thin separator + the selected item's description.
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

    this.rebuild();
  }

  // --- List rendering ------------------------------------------------------

  /** Resolve inventory counts to displayable entries (drops empties/unknowns). */
  private collect(): PackEntry[] {
    const out: PackEntry[] = [];
    for (const [id, count] of Object.entries(this.inventory.items)) {
      if (count <= 0) continue;
      const def = getItem(id);
      if (!def) continue;
      out.push({
        id,
        name: def.name,
        desc: def.desc,
        category: def.category,
        heal: def.heal,
        teach_move: def.teach_move,
        count,
      });
    }
    const order: Record<ItemCategory, number> = { lamp: 0, medicine: 1, chart: 2, valuable: 3, key: 4, misc: 5 };
    out.sort((a, b) => order[a.category] - order[b.category] || a.name.localeCompare(b.name));
    return out;
  }

  /** Recompute entries from inventory and redraw the rows (after a use empties one). */
  private rebuild(): void {
    for (const o of this.rowObjects) o.destroy();
    this.rowObjects = [];
    this.names = [];
    this.entries = this.collect();
    this.index = Math.max(0, Math.min(this.index, this.entries.length - 1));

    if (this.entries.length === 0) {
      this.track(makeText(this.scene, PAD, LIST_TOP + 4, 'Your pack is empty.', theme.text.dim));
    } else {
      this.entries.forEach((entry, i) => {
        const rowY = LIST_TOP + i * ROW_H;
        const name = makeText(this.scene, PAD + 10, rowY + 3, entry.name, theme.text.base);
        this.track(name);
        this.names.push(name);
        this.track(
          makeText(this.scene, this.width - PAD, rowY + 3, `x${entry.count}`, theme.text.base).setOrigin(1, 0),
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

  /** Reflect the current selection: cursor, highlighted name, description. */
  private refresh(): void {
    if (this.entries.length === 0) {
      this.cursor.sprite.setVisible(false);
      this.detail.setText('');
      return;
    }
    this.cursor.sprite.setVisible(true);
    this.cursor.moveTo(PAD, LIST_TOP + this.index * ROW_H + ROW_H / 2);
    this.names.forEach((name, i) =>
      name.setColor(i === this.index ? theme.text.accent.color : theme.text.base.color),
    );
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

  // --- Phases --------------------------------------------------------------

  /** Show the screen; resolve when the player backs out (B). */
  async run(): Promise<ItemsMenuResult> {
    let open = true;
    while (open) {
      const idx = await this.pickItem();
      if (idx === null) {
        open = false;
        break;
      }
      await this.useEntry(this.entries[idx]);
    }
    this.destroy();
    return { party: this.members.map((k) => k.toData()), inventory: this.inventory };
  }

  /** Cursor navigation over the item list. Resolves with an index, or null (cancel). */
  private pickItem(): Promise<number | null> {
    const input = new InputController(this.scene);
    let armed = false;
    return new Promise((resolve) => {
      const finish = (value: number | null): void => {
        this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
        input.destroy();
        resolve(value);
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
          if (this.entries.length === 0) return;
          void this.sfx?.play(theme.cursor.confirmSfx);
          finish(this.index);
        } else if (input.justPressed(InputAction.Cancel)) {
          void this.sfx?.play(theme.cursor.cancelSfx);
          finish(null);
        }
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  /** Use one item: medicines heal a kin; Star-charts teach one; the rest stay packed. */
  private async useEntry(entry: PackEntry): Promise<void> {
    if (entry.category === 'chart' && entry.teach_move) {
      await this.studyChart(entry);
      return;
    }
    if (entry.category !== 'medicine' || !entry.heal) {
      await new DialogueBox(this.scene, this.sfx).run([{ text: `You can't use the ${entry.name} out here.` }]);
      return;
    }
    if (this.members.length === 0) {
      await new DialogueBox(this.scene, this.sfx).run([{ text: 'No kin walk with you to tend.' }]);
      return;
    }

    const target = await this.pickKin();
    if (target === null) return;
    const kin = this.members[target];
    const restored = kin.heal(entry.heal);
    if (restored <= 0) {
      await new DialogueBox(this.scene, this.sfx).run([
        { text: `${kin.displayName} is already at full health.` },
      ]);
      return;
    }

    // Spend one and refresh the list (the entry may now be gone).
    this.inventory.items[entry.id] = (this.inventory.items[entry.id] ?? 1) - 1;
    if (this.inventory.items[entry.id] <= 0) delete this.inventory.items[entry.id];
    void this.sfx?.playVariant('world-heal', ['a', 'b']);
    await new DialogueBox(this.scene, this.sfx).run([
      { text: `${kin.displayName} recovered ${restored} HP.` },
    ]);
    this.rebuild();
  }

  /**
   * Study a Star-chart: pick a kin, check it can read the figure (type match,
   * Plain, or already in its learnset — KinInstance.canStudy), then learn into a
   * free slot or choose a move to set aside. One study consumes the chart.
   */
  private async studyChart(entry: PackEntry): Promise<void> {
    const move = MOVE_BY_ID.get(entry.teach_move ?? '');
    if (!move) {
      await new DialogueBox(this.scene, this.sfx).run([{ text: 'The chart\'s figure has faded beyond reading.' }]);
      return;
    }
    if (this.members.length === 0) {
      await new DialogueBox(this.scene, this.sfx).run([{ text: 'No kin walk with you to study it.' }]);
      return;
    }

    const target = await this.pickKin(() => true);
    if (target === null) return;
    const kin = this.members[target];

    const why = kin.canStudy(move);
    if (why === 'knows') {
      await new DialogueBox(this.scene, this.sfx).run([
        { text: `${kin.displayName} already knows ${move.name}.` },
      ]);
      return;
    }
    if (why === 'type') {
      await new DialogueBox(this.scene, this.sfx).run([
        { text: `${kin.displayName} peers at the figure, but its light isn't theirs to draw.` },
      ]);
      return;
    }

    if (!kin.learnMove(move)) {
      // All four slots taken — the classic choice: set one aside, or give up.
      const opts: MenuOption[] = kin.moves.map((k, i) => ({
        label: `${k.move.name}`,
        value: String(i),
      }));
      opts.push({ label: `GIVE UP ON ${move.name.toUpperCase()}`, value: 'giveup' });
      await new DialogueBox(this.scene, this.sfx).run([
        { text: `${kin.displayName} wants to learn ${move.name}, but already knows four moves. Set one aside?` },
      ]);
      const choice = await new Menu(this.scene, opts, { x: 8, y: 8, sfx: this.sfx, cancellable: true }).run();
      if (choice === null || choice === 'giveup') return;
      kin.replaceMove(Number(choice), move);
    }

    // Spend the chart and celebrate the study.
    this.inventory.items[entry.id] = (this.inventory.items[entry.id] ?? 1) - 1;
    if (this.inventory.items[entry.id] <= 0) delete this.inventory.items[entry.id];
    void this.sfx?.playVariant('progress-learn', ['a', 'b']);
    await new DialogueBox(this.scene, this.sfx).run([
      { text: `${kin.displayName} traces the chart by lamplight... and learns ${move.name}!` },
      { text: 'The chart\'s glow fades — its figure now lives in your kin.' },
    ]);
    this.rebuild();
  }

  /** A kin picker (re-using Menu), showing each member's HP. Resolves index or null. */
  private pickKin(enabled: (k: KinInstance) => boolean = (k) => k.hp < k.maxHp): Promise<number | null> {
    const opts: MenuOption[] = this.members.map((k, i) => ({
      label: `${k.displayName} ${Math.max(0, k.hp)}/${k.maxHp}`,
      value: String(i),
      enabled: enabled(k),
    }));
    return new Menu(this.scene, opts, { x: 8, y: 8, sfx: this.sfx, cancellable: true })
      .run()
      .then((v) => (v === null ? null : Number(v)));
  }

  destroy(): void {
    this.cursor.destroy();
    this.panel.destroy();
    this.dim.destroy();
  }
}
