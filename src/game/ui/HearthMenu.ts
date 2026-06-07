/**
 * HearthMenu — the Hearth: the warm keep where kin rest when they aren't travelling
 * in your lamp (this game's take on the genre's storage box). Opened from the pause
 * menu. Shows one scrolling list of every kin you own — those in your party and those
 * resting at the Hearth — and lets you move them between the two:
 *   • DEPOSIT  — send a party kin to rest at the Hearth (you must keep at least one).
 *   • WITHDRAW — bring a resting kin back into your lamp (party caps at six).
 *
 * A full lamp also overflows here automatically on a catch, so nothing caught is ever
 * lost. Origin is shown by a left marker (lit = party, dim = Hearth) and the running
 * counts in the header; the bottom line summarises the highlighted kin.
 *
 * Phase-based and self-contained like the rest of the kit (PartyMenu / Menu): each
 * interaction owns a short-lived InputController. `run()` resolves with the new party
 * and box orders, ready to drop straight back into the save.
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
import { MAX_PARTY } from '@game/systems/party/Party';
import type { KinInstanceData } from '@game/systems/save/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
/** Top of the scrolling row list inside the panel. */
const LIST_TOP = 26;
const ROW_H = 14;
/** Rows shown at once; the list scrolls to keep the cursor in view. */
const VISIBLE = 8;

/** The result handed back for persistence. */
export interface HearthMenuResult {
  party: KinInstanceData[];
  box: KinInstanceData[];
}

/** A row in the combined list: a kin plus where it currently lives. */
interface Entry {
  kin: KinInstance;
  origin: 'party' | 'box';
  /** Index within its own source list (party or box). */
  srcIndex: number;
}

export class HearthMenu {
  private readonly dim: Phaser.GameObjects.Rectangle;
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly header: Phaser.GameObjects.Text;
  private readonly footer: Phaser.GameObjects.Text;
  private readonly width: number;
  private readonly party: KinInstance[];
  private readonly box: KinInstance[];
  private entries: Entry[] = [];
  private rowObjects: Phaser.GameObjects.GameObject[] = [];
  private index = 0;
  private scrollTop = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    party: KinInstanceData[],
    box: KinInstanceData[],
    private readonly sfx?: Sfx,
  ) {
    this.party = party.map((d) => KinInstance.fromData(d));
    this.box = box.map((d) => KinInstance.fromData(d));

    this.dim = scene.add
      .rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, hex(theme.color.panelShadow), 0.62)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(theme.depth.overlayDim);

    this.width = GAME_WIDTH - 8;
    const height = GAME_HEIGHT - 8;
    this.panel = new Panel(scene, 4, 4, this.width, height).fixedToCamera();

    this.panel.add(makeText(scene, PAD, PAD - 2, 'THE HEARTH', theme.text.accent));
    this.panel.add(makeText(scene, this.width - PAD, PAD - 2, 'B BACK', theme.text.dim).setOrigin(1, 0));
    this.header = makeText(scene, PAD, PAD + 8, '', theme.text.dim);
    this.panel.add(this.header);

    this.footer = makeText(scene, PAD, height - PAD - 4, '', theme.text.dim);
    this.panel.add(this.footer);

    this.cursor = new Cursor(scene).setScrollFactor0();
    this.panel.add(this.cursor.sprite);

    this.rebuild();
  }

  // --- List rendering ------------------------------------------------------

  private collect(): Entry[] {
    const out: Entry[] = [];
    this.party.forEach((kin, i) => out.push({ kin, origin: 'party', srcIndex: i }));
    this.box.forEach((kin, i) => out.push({ kin, origin: 'box', srcIndex: i }));
    return out;
  }

  /** Recompute entries and redraw the visible window after a move. */
  private rebuild(): void {
    this.entries = this.collect();
    this.index = Math.max(0, Math.min(this.index, this.entries.length - 1));
    this.clampScroll();
    this.header.setText(`LAMP ${this.party.length}/${MAX_PARTY}   HEARTH ${this.box.length}`);
    this.draw();
  }

  /** Keep the cursor inside the visible window. */
  private clampScroll(): void {
    if (this.index < this.scrollTop) this.scrollTop = this.index;
    else if (this.index >= this.scrollTop + VISIBLE) this.scrollTop = this.index - VISIBLE + 1;
    this.scrollTop = Math.max(0, Math.min(this.scrollTop, Math.max(0, this.entries.length - VISIBLE)));
  }

  /** Redraw the windowed rows + cursor + footer for the current selection. */
  private draw(): void {
    for (const o of this.rowObjects) o.destroy();
    this.rowObjects = [];

    if (this.entries.length === 0) {
      this.track(makeText(this.scene, PAD, LIST_TOP + 4, 'You have no kin yet.', theme.text.dim));
      this.cursor.sprite.setVisible(false);
      this.footer.setText('');
      this.panel.container.bringToTop(this.cursor.sprite);
      return;
    }

    const end = Math.min(this.scrollTop + VISIBLE, this.entries.length);
    for (let i = this.scrollTop; i < end; i++) {
      const e = this.entries[i];
      const rowY = LIST_TOP + (i - this.scrollTop) * ROW_H;
      const selected = i === this.index;

      // Origin marker: lit for party, dim for the Hearth.
      this.track(
        this.scene.add
          .rectangle(PAD, rowY + 2, 4, 9, hex(e.origin === 'party' ? theme.color.panelEdge : theme.color.panelShadow))
          .setOrigin(0, 0),
      );
      const nameColor = selected ? theme.text.accent.color : e.origin === 'party' ? theme.text.base.color : theme.text.dim.color;
      this.track(makeText(this.scene, PAD + 10, rowY + 3, e.kin.displayName, theme.text.base)).setColor(nameColor);
      this.track(
        makeText(this.scene, this.width - PAD, rowY + 3, `Lv${e.kin.level}`, theme.text.dim).setOrigin(1, 0),
      );
    }

    // Scroll hints when there's more above/below the window.
    if (this.scrollTop > 0) {
      this.track(makeText(this.scene, this.width / 2, LIST_TOP - 8, '▲', theme.text.dim).setOrigin(0.5, 0));
    }
    if (end < this.entries.length) {
      this.track(makeText(this.scene, this.width / 2, LIST_TOP + VISIBLE * ROW_H - 2, '▼', theme.text.dim).setOrigin(0.5, 0));
    }

    this.cursor.sprite.setVisible(true);
    this.cursor.moveTo(PAD, LIST_TOP + (this.index - this.scrollTop) * ROW_H + ROW_H / 2);

    const sel = this.entries[this.index].kin;
    const where = this.entries[this.index].origin === 'party' ? 'In your lamp' : 'Resting';
    this.footer.setText(`${sel.species.types.join('/')}  HP ${Math.max(0, sel.hp)}/${sel.maxHp}  ${where}`);
    this.panel.container.bringToTop(this.cursor.sprite);
  }

  private track<T extends Phaser.GameObjects.GameObject>(obj: T): T {
    this.panel.add(obj);
    this.rowObjects.push(obj);
    return obj;
  }

  private move(dir: number): void {
    if (this.entries.length === 0) return;
    const next = (this.index + dir + this.entries.length) % this.entries.length;
    if (next !== this.index) {
      this.index = next;
      this.clampScroll();
      this.draw();
      void this.sfx?.play(theme.cursor.moveSfx);
    }
  }

  // --- Phases --------------------------------------------------------------

  async run(): Promise<HearthMenuResult> {
    let open = true;
    while (open) {
      const idx = await this.pickEntry();
      if (idx === null) {
        open = false;
        break;
      }
      const e = this.entries[idx];
      const action = await this.actionMenu(e);
      if (action === 'deposit') this.deposit(e.srcIndex);
      else if (action === 'withdraw') this.withdraw(e.srcIndex);
    }
    this.destroy();
    return { party: this.party.map((k) => k.toData()), box: this.box.map((k) => k.toData()) };
  }

  /** Cursor navigation. Resolves with an entry index, or null (cancel). */
  private pickEntry(): Promise<number | null> {
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

  /** Move options for the highlighted kin, gated by the party-size rules. */
  private actionMenu(e: Entry): Promise<string | null> {
    const opts: MenuOption[] =
      e.origin === 'party'
        ? [
            { label: 'DEPOSIT', value: 'deposit', enabled: this.party.length > 1 },
            { label: 'BACK', value: 'back' },
          ]
        : [
            { label: 'WITHDRAW', value: 'withdraw', enabled: this.party.length < MAX_PARTY },
            { label: 'BACK', value: 'back' },
          ];
    return new Menu(this.scene, opts, { x: 140, y: 24, sfx: this.sfx, cancellable: true }).run();
  }

  /** Send a party kin to rest at the Hearth (keeps at least one in the lamp). */
  private deposit(srcIndex: number): void {
    if (this.party.length <= 1) return;
    const [kin] = this.party.splice(srcIndex, 1);
    this.box.push(kin);
    void this.sfx?.play(theme.cursor.confirmSfx);
    this.rebuild();
  }

  /** Bring a resting kin back into the lamp (party caps at MAX_PARTY). */
  private withdraw(srcIndex: number): void {
    if (this.party.length >= MAX_PARTY) return;
    const [kin] = this.box.splice(srcIndex, 1);
    this.party.push(kin);
    void this.sfx?.play(theme.cursor.confirmSfx);
    this.rebuild();
  }

  destroy(): void {
    this.cursor.destroy();
    this.panel.destroy();
    this.dim.destroy();
  }
}
