/**
 * SlotMenu — the save-slot picker for the title screen (QoL package F).
 *
 * Three rows, one per save slot, each showing occupied state + a short summary
 * (area — N GLEAMS, with the wick purse beneath). Empty slots read "— EMPTY —"
 * and are greyed; in CONTINUE mode they can't be chosen, in NEW GAME mode they
 * can (that's where the new journey lands). Promise-based like the rest of the UI
 * kit: `await new SlotMenu(scene, cfg).run()` resolves with the chosen slot index
 * (0-based), or null if the player backs out.
 *
 * It builds entirely from theme tokens + the shared Panel/Cursor/Text kit and
 * owns its own transient InputController (destroyed on close), so it works from
 * the title scene without the host running an input loop — the same contract the
 * Menu/DialogueBox modals follow. Keyboard + touch both feed abstract
 * InputActions, so it's mobile-ready out of the box.
 */
import Phaser from 'phaser';
import { theme } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import type { Sfx } from '@game/systems/audio/Sfx';
import type { SaveGame } from '@game/systems/save/types';
import { GAME_WIDTH } from '@game/config';

export interface SlotMenuConfig {
  /** The decoded save for each slot (null = empty), index 0..N-1. */
  slots: (SaveGame | null)[];
  /**
   * 'continue' = only occupied slots are selectable (load a journey);
   * 'new' = empty slots are selectable, occupied ones are too (overwrite is
   * confirmed by the caller before committing).
   */
  mode: 'continue' | 'new';
  sfx?: Sfx;
}

const ROW_H = 24;
const PAD = theme.space.xl;
const CURSOR_GAP = 8;
const PANEL_W = GAME_WIDTH - 32; // 208
const PANEL_X = 16;
const PANEL_Y = 28;

/** Title-case a snake_case map id into a readable place name. */
function areaName(mapId: string): string {
  return mapId
    .split(/[_-]/)
    .filter(Boolean)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

/** How many Gleams (relit constellations) a save holds. */
function gleamCount(save: SaveGame): number {
  const flags = save.world?.flags ?? {};
  let n = 0;
  for (const key of Object.keys(flags)) {
    if (key.startsWith('gleam:') && flags[key]) n += 1;
  }
  return n;
}

/** The headline + sub line shown for an occupied slot. */
function summaryLines(save: SaveGame): { head: string; sub: string } {
  const gleams = gleamCount(save);
  const where = save.world?.current_map ? areaName(save.world.current_map) : 'Wayfaring';
  const head = `${where}`;
  const sub = `${gleams} GLEAM${gleams === 1 ? '' : 'S'}  ${save.money ?? 0}w`;
  return { head, sub };
}

export class SlotMenu {
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly rows: { head: Phaser.GameObjects.Text; sub: Phaser.GameObjects.Text }[] = [];
  private index = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly config: SlotMenuConfig,
  ) {
    const count = config.slots.length;
    const titleH = 12;
    const height = PAD * 2 + titleH + count * ROW_H;
    this.panel = new Panel(scene, PANEL_X, PANEL_Y, PANEL_W, height);

    const heading = config.mode === 'new' ? 'NEW GAME — CHOOSE A SLOT' : 'CONTINUE — CHOOSE A SLOT';
    const title = makeText(scene, PANEL_W / 2, PAD, heading, theme.text.accent).setOrigin(0.5, 0);
    this.panel.add(title);

    config.slots.forEach((save, i) => {
      const y = PAD + titleH + i * ROW_H;
      const enabled = this.slotEnabled(i);
      const baseStyle = enabled ? theme.text.base : theme.text.dim;

      // Slot label + (occupied) the place, then the gleam/wick line beneath.
      const summary = save ? summaryLines(save) : null;
      const headText = summary ? `SLOT ${i + 1}  ${summary.head}` : `SLOT ${i + 1}`;
      const subText = summary ? summary.sub : '— EMPTY —';
      const head = makeText(scene, PAD + CURSOR_GAP, y, headText, baseStyle);
      const sub = makeText(scene, PAD + CURSOR_GAP, y + 10, subText, theme.text.dim);

      this.panel.add(head);
      this.panel.add(sub);
      this.rows.push({ head, sub });
    });

    this.cursor = new Cursor(scene);
    this.panel.add(this.cursor.sprite);
    this.panel.container.bringToTop(this.cursor.sprite);
    this.panel.fixedToCamera();
    this.cursor.setScrollFactor0();

    this.index = this.firstEnabled(0, 1);
    this.placeCursor();
  }

  /** Whether slot i is choosable in the current mode. */
  private slotEnabled(i: number): boolean {
    const occupied = this.config.slots[i] !== null && this.config.slots[i] !== undefined;
    // Continue can only pick occupied slots; New can pick any slot.
    return this.config.mode === 'continue' ? occupied : true;
  }

  private firstEnabled(from: number, dir: number): number {
    let i = from;
    for (let n = 0; n < this.config.slots.length; n++) {
      if (this.slotEnabled(i)) return i;
      i = (i + dir + this.config.slots.length) % this.config.slots.length;
    }
    return from;
  }

  private placeCursor(): void {
    const titleH = 12;
    this.cursor.moveTo(PAD, PAD + titleH + this.index * ROW_H + 4);
  }

  private move(dir: number): void {
    let i = this.index;
    do {
      i = (i + dir + this.config.slots.length) % this.config.slots.length;
    } while (!this.slotEnabled(i) && i !== this.index);
    if (i !== this.index) {
      this.index = i;
      this.placeCursor();
      void this.config.sfx?.play(theme.cursor.moveSfx);
    }
  }

  /** Show the picker; resolve with the chosen slot index, or null if cancelled. */
  run(): Promise<number | null> {
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
        else if (input.justPressed(InputAction.Confirm)) {
          if (this.slotEnabled(this.index)) {
            void this.config.sfx?.play(theme.cursor.confirmSfx);
            finish(this.index);
          }
        } else if (input.justPressed(InputAction.Cancel)) {
          void this.config.sfx?.play(theme.cursor.cancelSfx);
          finish(null);
        }
      };
      const finish = (value: number | null): void => {
        this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
        input.destroy();
        this.destroy();
        resolve(value);
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  destroy(): void {
    this.cursor.destroy();
    this.panel.destroy();
  }
}
