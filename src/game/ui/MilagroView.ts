/**
 * MilagroView — the Booji-Wooji Man's milagro cards (content/milagros.ts).
 *
 * One full-screen view, two uses:
 *  - REVEAL (the `milagroCard` cutscene op): "A MILAGRO CARD", the card, its phrase,
 *    then its story, paged with A; closes after the last page.
 *  - THE PACK (pause menu -> MILAGROS): page 0 is the box and its lore card, then
 *    every card in deck order; LEFT/RIGHT flip one, UP/DOWN jump to the next card
 *    you hold, A turns the story's page, B closes. Cards not yet found show their
 *    painted back and "? ? ?".
 *
 * Portrait art (2:3) on the left, words on the right; built from theme tokens and
 * camera-fixed so it sits over the world. Missing art falls back to a framed slot.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { loadImage } from '@game/systems/sprites/loadImage';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { MILAGROS, MILAGRO_LORE, milagroArt, type MilagroCard } from '@game/content/milagros';
import type { Sfx } from '@game/systems/audio/Sfx';

const DEPTH = theme.depth.toast;
const CARD = { x: 6, y: 8, w: 96, h: 144 };
const COL_X = CARD.x + CARD.w + 8;
const COL_W = GAME_WIDTH - COL_X - 6;
const LINE_H = 9;
const TEXT_BOTTOM = GAME_HEIGHT - 16;
const BOX_ART = 'assets/milagros/box.webp';
const BACK_ART = 'assets/milagros/back.webp';
const UNFOUND =
  'Still out there somewhere: left on a seat, tucked in a book, under somebody\'s teacup. Whoever finds it will hand it on.';

interface Page {
  art: string;
  heading: string;
  title: string;
  story: string;
}

export class MilagroView {
  private readonly objs: Phaser.GameObjects.GameObject[] = [];
  private readonly img: Phaser.GameObjects.Image;
  private readonly heading: Phaser.GameObjects.Text;
  private readonly title: Phaser.GameObjects.Text;
  private readonly story: Phaser.GameObjects.Text;
  private readonly hint: Phaser.GameObjects.Text;
  private pages: string[] = [];
  private page = 0;
  private token = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly sfx?: Sfx,
  ) {
    const add = <T extends Phaser.GameObjects.GameObject>(o: T, d = 0): T => {
      (o as unknown as { setScrollFactor: (n: number) => void }).setScrollFactor(0);
      (o as unknown as { setDepth: (n: number) => void }).setDepth(DEPTH + d);
      this.objs.push(o);
      return o;
    };
    add(scene.add.rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, hex(theme.color.panelShadow), 1).setOrigin(0, 0));
    // the card's slot: a framed blank that shows while (or if) the art loads
    add(
      scene.add
        .rectangle(CARD.x, CARD.y, CARD.w, CARD.h, hex(theme.color.panelFill), 1)
        .setOrigin(0, 0)
        .setStrokeStyle(1, hex(theme.color.panelEdge)),
      1,
    );
    this.img = add(scene.add.image(CARD.x, CARD.y, '__DEFAULT').setOrigin(0, 0).setVisible(false), 2);
    this.heading = add(makeText(scene, COL_X, 6, '', theme.text.dim), 2);
    this.title = add(makeText(scene, COL_X, 18, '', theme.text.accent), 2);
    this.title.setWordWrapWidth(COL_W);
    this.story = add(makeText(scene, COL_X, 0, '', theme.text.narrate), 2);
    this.story.setWordWrapWidth(COL_W).setLineSpacing(LINE_H - 8);
    this.hint = add(makeText(scene, GAME_WIDTH - 6, GAME_HEIGHT - 11, '', theme.text.dim).setOrigin(1, 0), 2);
  }

  /** The reveal: one card, its phrase and its story; resolves when read. */
  async reveal(card: MilagroCard): Promise<void> {
    await this.show(this.cardPage(card, true, 'A MILAGRO CARD'));
    await this.loop({ flip: false });
    this.destroy();
  }

  /** The pack: the box, then every card; resolves on B. */
  async gallery(has: (id: string) => boolean): Promise<void> {
    const total = MILAGROS.length;
    const held = MILAGROS.filter((c) => has(c.id)).length;
    const deck: Page[] = [
      {
        art: BOX_ART,
        heading: `MILAGROS  ${held}/${total}`,
        title: 'BOOJI-WOOJI MAN MILAGRO CARDS',
        story: MILAGRO_LORE,
      },
      ...MILAGROS.map((c, i) => this.cardPage(c, has(c.id), `CARD ${i + 1}/${total}`)),
    ];
    // the box and every card you hold: where UP/DOWN jump to
    const heldAt = deck.map((_, i) => (i === 0 || has(MILAGROS[i - 1].id) ? i : -1)).filter((i) => i >= 0);
    let at = 0;
    await this.show(deck[at]);
    await this.loop({
      flip: true,
      onFlip: async (dir, jump) => {
        let next = at;
        if (jump) {
          const ahead = dir > 0 ? heldAt.find((i) => i > at) : [...heldAt].reverse().find((i) => i < at);
          next = ahead ?? at;
        } else next = Phaser.Math.Wrap(at + dir, 0, deck.length);
        if (next === at) return;
        at = next;
        void this.sfx?.play(theme.cursor.moveSfx);
        await this.show(deck[at]);
      },
    });
    this.destroy();
  }

  private cardPage(card: MilagroCard, found: boolean, heading: string): Page {
    return found
      ? { art: milagroArt(card.id), heading, title: card.title, story: card.story }
      : { art: BACK_ART, heading, title: '? ? ?', story: UNFOUND };
  }

  private async show(p: Page): Promise<void> {
    const mine = ++this.token;
    this.heading.setText(p.heading);
    this.title.setText(p.title);
    this.story.setY(this.title.y + this.title.height + 5);
    const budget = Math.max(1, Math.floor((TEXT_BOTTOM - this.story.y) / LINE_H));
    const lines = this.story.getWrappedText(p.story);
    this.pages = [];
    for (let i = 0; i < lines.length; i += budget) this.pages.push(lines.slice(i, i + budget).join('\n'));
    if (this.pages.length === 0) this.pages.push('');
    this.page = 0;
    this.renderPage();
    const ok = this.scene.textures.exists(p.art) || (await loadImage(this.scene, p.art, p.art));
    if (mine !== this.token || !this.img.active) return;
    if (ok) {
      // painted cards, not pixel art: smooth the downscale so the lettering stays legible
      this.scene.textures.get(p.art).setFilter(Phaser.Textures.FilterMode.LINEAR);
      this.img.setTexture(p.art).setDisplaySize(CARD.w, CARD.h).setVisible(true);
    }
    else this.img.setVisible(false);
  }

  private renderPage(): void {
    this.story.setText(this.pages[this.page] ?? '');
    const more = this.page < this.pages.length - 1;
    const marker = this.pages.length > 1 ? `${this.page + 1}/${this.pages.length} ` : '';
    this.hint.setText(`${marker}${more ? 'A MORE' : ''}`);
  }

  /** The input loop: A pages the story (and, without flipping, closes after the last
   *  page); with flipping, LEFT/RIGHT/UP/DOWN move through the deck and B closes. */
  private loop(opts: { flip: boolean; onFlip?: (dir: number, jump: boolean) => Promise<void> }): Promise<void> {
    return new Promise((resolve) => {
      const input = new InputController(this.scene);
      let armed = false;
      let busy = false;
      const done = (): void => {
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
        if (busy) return;
        if (input.justPressed(InputAction.Confirm)) {
          if (this.page < this.pages.length - 1) {
            this.page++;
            this.renderPage();
            void this.sfx?.play(theme.cursor.moveSfx);
          } else if (!opts.flip) {
            void this.sfx?.play(theme.cursor.confirmSfx);
            done();
          } else if (this.pages.length > 1) {
            this.page = 0;
            this.renderPage();
          }
        } else if (opts.flip && input.justPressed(InputAction.Cancel)) {
          void this.sfx?.play(theme.cursor.cancelSfx);
          done();
        } else if (opts.flip && opts.onFlip) {
          const dir = input.justPressed(InputAction.Right) ? 1 : input.justPressed(InputAction.Left) ? -1 : 0;
          const jump = input.justPressed(InputAction.Down) ? 1 : input.justPressed(InputAction.Up) ? -1 : 0;
          if (dir || jump) {
            busy = true;
            void opts.onFlip(dir || jump, !!jump).then(() => {
              busy = false;
            });
          }
        }
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  destroy(): void {
    this.token++;
    for (const o of this.objs) o.destroy();
    this.objs.length = 0;
  }
}
