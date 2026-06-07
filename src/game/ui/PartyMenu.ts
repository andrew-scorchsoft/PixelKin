/**
 * PartyMenu — the overworld "look at your kin" screen (opened from the pause menu).
 *
 * Lists the up-to-six kin travelling with you: a type-tinted icon, name, types,
 * level and an HP bar. From the list you can:
 *   • SUMMARY — a full detail card (stats, ability, known moves + charges), so you
 *     can actually see a freshly-caught kin and inspect what it can do.
 *   • MOVE    — reorder the party; slot 0 is the battle lead, so this picks who
 *     leads / comes out first.
 *
 * Promise-based and self-contained like the rest of the kit (StarterSelect / Menu):
 * `await new PartyMenu(scene, party, sfx).run()` resolves with the party data in
 * its (possibly reordered) final order, ready to drop back into the save.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { Menu, type MenuOption } from './Menu';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { KinInstance } from '@game/systems/party/KinInstance';
import { ABILITY_BY_ID } from '@game/data/dex';
import { hasCreatureSprite, loadCreatureSprite } from '@game/systems/sprites/CreatureSprites';
import type { KinInstanceData } from '@game/systems/save/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
/** Row geometry inside the list panel. */
const ROWS_TOP = 16;
const ROW_H = 22;

export class PartyMenu {
  private readonly dim: Phaser.GameObjects.Rectangle;
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly title: Phaser.GameObjects.Text;
  private readonly members: KinInstance[];
  /** Everything drawn per build of the rows, so a reorder can rebuild cleanly. */
  private rowObjects: Phaser.GameObjects.GameObject[] = [];
  private nameTexts: Phaser.GameObjects.Text[] = [];
  /** Bumped on every rows rebuild so stale async icon loads can no-op. */
  private gen = 0;
  private index = 0;
  /** While reordering, the slot picked up (highlighted); else null. */
  private moveFrom: number | null = null;

  constructor(
    private readonly scene: Phaser.Scene,
    party: KinInstanceData[],
    private readonly sfx?: Sfx,
  ) {
    this.members = party.map((d) => KinInstance.fromData(d));

    this.dim = scene.add
      .rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, hex(theme.color.panelShadow), 0.62)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(theme.depth.overlayDim);

    const width = GAME_WIDTH - 8;
    const height = GAME_HEIGHT - 8;
    this.panel = new Panel(scene, 4, 4, width, height).fixedToCamera();

    this.title = makeText(scene, PAD, PAD - 2, 'PARTY', theme.text.accent);
    this.panel.add(this.title);
    this.panel.add(
      makeText(scene, width - PAD, PAD - 2, 'A PICK   B BACK', theme.text.dim).setOrigin(1, 0),
    );

    this.cursor = new Cursor(scene).setScrollFactor0();
    this.panel.add(this.cursor.sprite);

    this.buildRows();
    this.placeCursor();
  }

  // --- List rendering ------------------------------------------------------

  private track<T extends Phaser.GameObjects.GameObject>(obj: T): T {
    this.panel.add(obj);
    this.rowObjects.push(obj);
    return obj;
  }

  private buildRows(): void {
    this.gen++;
    for (const o of this.rowObjects) o.destroy();
    this.rowObjects = [];
    this.nameTexts = [];
    this.members.forEach((kin, i) => this.buildRow(kin, i));
    this.panel.container.bringToTop(this.cursor.sprite);
    this.refreshHighlight();
  }

  private buildRow(kin: KinInstance, i: number): void {
    const g = this.gen;
    const rowY = ROWS_TOP + i * ROW_H;
    const scene = this.scene;

    // Type-tinted swatch as a placeholder until the real icon loads.
    const tint = theme.typeColor[kin.species.types[0]] ?? theme.color.panelEdge;
    const swatch = this.track(
      scene.add
        .rectangle(10, rowY + 3, 16, 16, hex(tint))
        .setOrigin(0, 0)
        .setStrokeStyle(1, hex(theme.color.panelShadow)),
    );
    if (hasCreatureSprite(kin.species.id, 'icon')) {
      void loadCreatureSprite(scene, kin.species.id, 'icon').then((key) => {
        if (!key || g !== this.gen || !swatch.active) return;
        const icon = scene.add.image(10, rowY + 3, key).setOrigin(0, 0).setDisplaySize(16, 16);
        this.track(icon);
        this.panel.container.bringToTop(this.cursor.sprite);
        swatch.setVisible(false);
      });
    }

    const name = this.track(makeText(scene, 30, rowY + 1, kin.displayName, theme.text.base));
    this.nameTexts.push(name);
    this.track(makeText(scene, 30, rowY + 11, kin.species.types.join('/'), theme.text.dim));
    this.track(makeText(scene, 124, rowY + 1, `Lv${kin.level}`, theme.text.base));

    const fainted = kin.isFainted;
    this.track(
      makeText(
        scene,
        164,
        rowY + 1,
        fainted ? 'FNT' : `${kin.hp}/${kin.maxHp}`,
        fainted ? theme.text.dim : theme.text.base,
      ),
    );

    // HP bar: dark track with a ratio-coloured fill.
    const barX = 124;
    const barY = rowY + 13;
    const barW = 96;
    this.track(scene.add.rectangle(barX, barY, barW, 4, hex(theme.color.panelShadow)).setOrigin(0, 0));
    const ratio = kin.hpRatio;
    if (ratio > 0) {
      const col = ratio > 0.5 ? theme.color.hpHigh : ratio > 0.2 ? theme.color.hpMid : theme.color.hpLow;
      this.track(
        scene.add
          .rectangle(barX, barY, Math.max(1, Math.round(barW * ratio)), 4, hex(col))
          .setOrigin(0, 0),
      );
    }
  }

  /** Tint the picked-up row (during a MOVE) so the swap target is obvious. */
  private refreshHighlight(): void {
    this.nameTexts.forEach((t, i) => {
      t.setColor(i === this.moveFrom ? theme.color.selected : theme.color.text);
    });
  }

  private placeCursor(): void {
    this.cursor.moveTo(2, ROWS_TOP + this.index * ROW_H + 8);
  }

  private move(dir: number): void {
    const n = this.members.length;
    const next = (this.index + dir + n) % n;
    if (next !== this.index) {
      this.index = next;
      this.placeCursor();
      void this.sfx?.play(theme.cursor.moveSfx);
    }
  }

  // --- Flow ----------------------------------------------------------------

  /** Show the screen; resolve with the party data in its final order. */
  async run(): Promise<KinInstanceData[]> {
    let open = true;
    while (open) {
      const idx = await this.pickSlot();
      if (idx === null) {
        open = false;
        break;
      }
      const action = await this.actionMenu();
      if (action === 'summary') await this.showSummary(idx);
      else if (action === 'move') await this.doMove(idx);
    }
    this.destroy();
    return this.members.map((k) => k.toData());
  }

  /** Cursor navigation over the list. Resolves with a slot index, or null (cancel). */
  private pickSlot(): Promise<number | null> {
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

  /** The per-kin action picker. MOVE is disabled with a lone party member. */
  private actionMenu(): Promise<string | null> {
    const opts: MenuOption[] = [
      { label: 'SUMMARY', value: 'summary' },
      { label: 'MOVE', value: 'move', enabled: this.members.length > 1 },
      { label: 'BACK', value: 'back' },
    ];
    return new Menu(this.scene, opts, { x: 150, y: 24, sfx: this.sfx, cancellable: true }).run();
  }

  /** Reorder: pick a second slot to swap with `from`. */
  private async doMove(from: number): Promise<void> {
    this.moveFrom = from;
    this.refreshHighlight();
    this.title.setText('MOVE WHERE?');

    const to = await this.pickSlot();
    if (to !== null && to !== from) {
      const tmp = this.members[from];
      this.members[from] = this.members[to];
      this.members[to] = tmp;
      this.index = to;
      this.buildRows();
      this.placeCursor();
      void this.sfx?.play(theme.cursor.confirmSfx);
    }

    this.moveFrom = null;
    this.title.setText('PARTY');
    this.refreshHighlight();
    this.placeCursor();
  }

  // --- Summary card --------------------------------------------------------

  private showSummary(idx: number): Promise<void> {
    const kin = this.members[idx];
    const scene = this.scene;
    this.panel.setVisible(false); // hide the list behind the card

    const innerW = GAME_WIDTH - 16;
    const innerH = GAME_HEIGHT - 16;
    const card = new Panel(scene, 8, 8, innerW, innerH).fixedToCamera().setDepth(theme.depth.panel + 1);

    card.add(makeText(scene, PAD, PAD - 2, kin.displayName, theme.text.accent));
    card.add(makeText(scene, innerW - PAD, PAD - 2, `Lv${kin.level}`, theme.text.base).setOrigin(1, 0));

    // Icon (type swatch, upgraded to the real icon if packed).
    const tint = theme.typeColor[kin.species.types[0]] ?? theme.color.panelEdge;
    const swatch = scene.add
      .rectangle(10, 16, 32, 32, hex(tint))
      .setOrigin(0, 0)
      .setStrokeStyle(1, hex(theme.color.panelShadow));
    card.add(swatch);
    if (hasCreatureSprite(kin.species.id, 'icon')) {
      void loadCreatureSprite(scene, kin.species.id, 'icon').then((key) => {
        if (key && swatch.active) {
          card.add(scene.add.image(10, 16, key).setOrigin(0, 0).setDisplaySize(32, 32));
          swatch.setVisible(false);
        }
      });
    }
    card.add(makeText(scene, 10, 52, kin.species.types.join('/'), theme.text.dim));
    const abilityName = ABILITY_BY_ID.get(kin.species.ability)?.name ?? kin.species.ability;
    const ability = makeText(scene, 10, 64, `Ability: ${abilityName}`, theme.text.dim);
    ability.setWordWrapWidth(100);
    card.add(ability);

    // Stats column (monospace pixel font → padEnd lines up the values).
    const stats: Array<[string, number | string]> = [
      ['HP', `${Math.max(0, kin.hp)}/${kin.maxHp}`],
      ['ATK', kin.atk],
      ['DEF', kin.def],
      ['SpA', kin.spa],
      ['SpD', kin.spd],
      ['Spe', kin.spe],
    ];
    stats.forEach(([label, val], i) => {
      card.add(makeText(scene, 120, 16 + i * 11, `${label.padEnd(4)}${val}`, theme.text.base));
    });

    // Known moves with remaining charges.
    card.add(makeText(scene, 10, 92, 'MOVES', theme.text.accent));
    kin.moves.forEach((m, i) => {
      const y = 104 + i * 11;
      card.add(makeText(scene, 10, y, m.move.name, theme.text.base));
      card.add(makeText(scene, 150, y, `${m.charges}/${m.move.charges}`, theme.text.dim));
    });

    card.add(makeText(scene, innerW - PAD, innerH - PAD, 'B BACK', theme.text.dim).setOrigin(1, 1));

    return new Promise((resolve) => {
      const input = new InputController(scene);
      let armed = false;
      const tick = (): void => {
        input.update();
        if (!armed) {
          if (!input.isDown(InputAction.Confirm) && !input.isDown(InputAction.Cancel)) armed = true;
          return;
        }
        if (input.justPressed(InputAction.Cancel) || input.justPressed(InputAction.Confirm)) {
          void this.sfx?.play(theme.cursor.cancelSfx);
          scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
          input.destroy();
          card.destroy();
          this.panel.setVisible(true);
          resolve();
        }
      };
      scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  destroy(): void {
    this.cursor.destroy();
    this.panel.destroy();
    this.dim.destroy();
  }
}
