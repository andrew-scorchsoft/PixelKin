/**
 * ItemsMenu — the overworld "what's in my pack" screen (opened from the pause menu).
 *
 * Lists everything the player is carrying: each item's name and the count held,
 * with a detail pane below that shows only the *selected* item's description and
 * updates as the cursor moves — the same list + detail pattern StarterSelect uses,
 * so a long blurb never overlaps the list on the 240×160 screen. up/down to browse,
 * B to back out. Read-only for now (items aren't usable from the field yet); it
 * exists so a player can actually see the kit they've been given.
 *
 * Promise-based and self-contained like the rest of the kit (StarterSelect / Menu /
 * PartyMenu): `await new ItemsMenu(scene, inventory, sfx).run()` resolves when the
 * player backs out. The inventory is only read, never mutated.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { getItem } from '@game/content/items';
import type { ItemCategory } from '@game/content/types';
import type { InventoryData } from '@game/systems/save/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
/** Vertical room reserved for the header line. */
const HEADER_H = 14;
/** One compact list row: name on the left, count on the right. */
const ROW_H = 14;
/** Detail pane: lines × line-height, sized for the longest blurb so nothing clips. */
const DETAIL_LINE_H = 9;
const DETAIL_LINES = 3;

/** One carried item, resolved to its definition for display. */
interface PackEntry {
  name: string;
  desc: string;
  category: ItemCategory;
  count: number;
}

export class ItemsMenu {
  private readonly dim: Phaser.GameObjects.Rectangle;
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly entries: PackEntry[];
  private readonly names: Phaser.GameObjects.Text[] = [];
  private readonly detail: Phaser.GameObjects.Text;
  private readonly listTop: number;
  private index = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    inventory: InventoryData,
    private readonly sfx?: Sfx,
  ) {
    this.entries = ItemsMenu.collect(inventory);

    this.dim = scene.add
      .rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, hex(theme.color.panelShadow), 0.62)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(theme.depth.overlayDim);

    const width = GAME_WIDTH - 8;
    this.listTop = PAD + HEADER_H;
    const rows = Math.max(this.entries.length, 1);
    const detailTop = this.listTop + rows * ROW_H + PAD;
    const height = detailTop + DETAIL_LINES * DETAIL_LINE_H + PAD;
    this.panel = new Panel(scene, 4, 4, width, height).fixedToCamera();

    this.panel.add(makeText(scene, PAD, PAD - 2, 'ITEMS', theme.text.accent));
    this.panel.add(
      makeText(scene, width - PAD, PAD - 2, 'B BACK', theme.text.dim).setOrigin(1, 0),
    );

    if (this.entries.length === 0) {
      // Empty pack: a single dim line, no list/detail (WorldScene gates this too,
      // but keep the screen sensible if opened with nothing carried).
      this.panel.add(
        makeText(scene, PAD, this.listTop + 4, 'Your pack is empty.', theme.text.dim),
      );
    } else {
      this.entries.forEach((entry, i) => {
        const rowY = this.listTop + i * ROW_H;
        const name = makeText(scene, PAD + 10, rowY + 3, entry.name, theme.text.base);
        this.panel.add(name);
        this.names.push(name);
        this.panel.add(
          makeText(scene, width - PAD, rowY + 3, `x${entry.count}`, theme.text.base).setOrigin(1, 0),
        );
      });
    }

    // Detail pane: a thin separator + the selected item's description, wrapped to the
    // panel width and refreshed on every cursor move (never stacked per-row).
    const sep = scene.add
      .rectangle(PAD, detailTop - Math.floor(PAD / 2), width - PAD * 2, 1, hex(theme.color.panelEdge))
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

  /** Resolve the inventory counts to displayable entries, dropping empties/unknowns. */
  private static collect(inventory: InventoryData): PackEntry[] {
    const out: PackEntry[] = [];
    for (const [id, count] of Object.entries(inventory.items)) {
      if (count <= 0) continue;
      const def = getItem(id);
      if (!def) continue; // an id with no definition can't be shown
      out.push({ name: def.name, desc: def.desc, category: def.category, count });
    }
    // Group by category so lamps/medicine/keys read together, then by name.
    const order: Record<ItemCategory, number> = { lamp: 0, medicine: 1, key: 2, misc: 3 };
    out.sort((a, b) => order[a.category] - order[b.category] || a.name.localeCompare(b.name));
    return out;
  }

  /** Reflect the current selection: cursor position, highlighted name, description. */
  private refresh(): void {
    if (this.entries.length === 0) return;
    this.cursor.moveTo(PAD, this.listTop + this.index * ROW_H + ROW_H / 2);
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

  /** Show the screen; resolve when the player backs out (B). */
  run(): Promise<void> {
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
    this.dim.destroy();
  }
}
