/**
 * MilagroView — the Booji-Wooji Man's milagro cards (content/milagros.ts).
 *
 * One full-screen view, two uses:
 *  - REVEAL (the `milagroCard` cutscene op) — a small ceremony, because a card is a
 *    prize to keep: the world dims, the card rises face-down in a warm glow, turns
 *    over with a flash, a burst of sparkles and the music-box chime
 *    (`world-milagro`, the score ducked under it), and is held up to be admired
 *    ("No. 12 of 54") before it settles to the left and its phrase and story
 *    appear, paged with A. Closes after the last page.
 *  - THE PACK (pause menu -> MILAGROS): page 0 is the box and its lore card (a
 *    tease until Paul gives you the box), then every card in deck order;
 *    LEFT/RIGHT flip one, UP/DOWN jump to the next card you hold, A turns the
 *    story's page, B closes. Cards not yet found show their painted back.
 *
 * Portrait art (2:3) on the left, words on the right; theme tokens throughout and
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
import type { MusicDirector } from '@game/systems/audio/MusicDirector';

const DEPTH = theme.depth.toast;
const CARD = { w: 96, h: 144 };
/** The card's resting centre (left column) and its ceremony centre (mid-screen). */
const REST = { x: 6 + CARD.w / 2, y: 8 + CARD.h / 2 };
const STAGE = { x: GAME_WIDTH / 2, y: GAME_HEIGHT / 2 + 1 };
/** Held up mid-screen a little smaller, so its caption and number sit clear of it. */
const STAGE_SCALE = 0.76;
const COL_X = 6 + CARD.w + 8;
const COL_W = GAME_WIDTH - COL_X - 6;
const LINE_H = 9;
const TEXT_BOTTOM = GAME_HEIGHT - 16;
const BOX_ART = 'assets/milagros/box.webp';
const BACK_ART = 'assets/milagros/back.webp';
/** Warm candle-gold for the glow and sparkles (world-feel colour, like Ambience's). */
const GLOW = 0xffa63a;
const SPARK = [0xfff6d0, 0xffd27a, 0xffffff, 0xffb35c];
const UNFOUND =
  'Still out there somewhere: left on a seat, tucked in a book, under somebody\'s teacup. Whoever finds it will hand it on.';
const NO_BOX =
  'Little painted cards with a phrase lettered round the border, and no name on any of them. Somebody, somewhere, must know where they come from.';
const ALTERED = ' (This card has been altered from the original.)';
const FIRST_TIP = ' Keep it safe: your cards are under START > MILAGROS.';

interface Page {
  art: string;
  heading: string;
  sub?: string;
  title: string;
  story: string;
}

export interface RevealOptions {
  /** This card's place in the deck and the deck's size, for "No. n of N". */
  number: number;
  total: number;
  /** The first card the player has ever been given. */
  first: boolean;
  /** Ducked under the chime, if given. */
  music?: MusicDirector;
}

export class MilagroView {
  private readonly objs: Phaser.GameObjects.GameObject[] = [];
  private readonly dim: Phaser.GameObjects.Rectangle;
  private readonly glow: Phaser.GameObjects.Container;
  private readonly slot: Phaser.GameObjects.Rectangle;
  private readonly img: Phaser.GameObjects.Image;
  private readonly heading: Phaser.GameObjects.Text;
  private readonly sub: Phaser.GameObjects.Text;
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
    this.dim = this.add(
      scene.add.rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, hex(theme.color.panelShadow), 1).setOrigin(0, 0),
    );
    // a soft radial glow: stacked rings, faint at the rim and warmer at the heart
    const rings = [1, 0.78, 0.58, 0.4].map((k) =>
      scene.add.circle(0, 0, 76 * k, GLOW, 0.09 + (1 - k) * 0.12).setBlendMode(Phaser.BlendModes.ADD),
    );
    this.glow = this.add(scene.add.container(REST.x, REST.y, rings).setAlpha(0), 1);
    this.slot = this.add(
      scene.add
        .rectangle(REST.x, REST.y, CARD.w, CARD.h, hex(theme.color.panelFill), 1)
        .setStrokeStyle(1, hex(theme.color.panelEdge)),
      1,
    );
    this.img = this.add(scene.add.image(REST.x, REST.y, '__DEFAULT').setVisible(false), 2);
    this.heading = this.add(makeText(scene, COL_X, 6, '', theme.text.accent), 3);
    this.sub = this.add(makeText(scene, COL_X, 15, '', theme.text.dim), 3);
    this.title = this.add(makeText(scene, COL_X, 18, '', theme.text.accent), 3);
    this.title.setWordWrapWidth(COL_W);
    this.story = this.add(makeText(scene, COL_X, 0, '', theme.text.narrate), 3);
    this.story.setWordWrapWidth(COL_W).setLineSpacing(LINE_H - 8);
    this.hint = this.add(makeText(scene, GAME_WIDTH - 6, GAME_HEIGHT - 11, '', theme.text.dim).setOrigin(1, 0), 3);
  }

  private add<T extends Phaser.GameObjects.GameObject>(o: T, d = 0): T {
    (o as unknown as { setScrollFactor: (n: number) => void }).setScrollFactor(0);
    (o as unknown as { setDepth: (n: number) => void }).setDepth(DEPTH + d);
    this.objs.push(o);
    return o;
  }

  // ---------------------------------------------------------------------------
  // The reveal ceremony
  // ---------------------------------------------------------------------------

  /** One card, given: the ceremony, then its phrase and story; resolves when read. */
  async reveal(card: MilagroCard, opts: RevealOptions): Promise<void> {
    const front = milagroArt(card.id);
    const [hasBack, hasFront] = await Promise.all([this.ensure(BACK_ART), this.ensure(front)]);
    const words = [this.heading, this.sub, this.title, this.story, this.hint];
    for (const w of words) w.setAlpha(0);
    this.slot.setVisible(false);
    this.dim.setAlpha(0);
    await this.tween({ targets: this.dim, alpha: 0.94, duration: 450 });

    // 1. it rises, face down, into a warm glow
    this.glow.setPosition(STAGE.x, STAGE.y).setScale(1);
    this.setCard(hasBack ? BACK_ART : hasFront ? front : null);
    const s = this.img.scaleX * STAGE_SCALE;
    this.img.setPosition(STAGE.x, STAGE.y + 22).setScale(s * 0.55).setAlpha(0);
    void this.tween({ targets: this.glow, alpha: 0.8, duration: 700 });
    await this.tween({ targets: this.img, y: STAGE.y, scaleX: s, scaleY: s, alpha: 1, duration: 700, ease: 'Cubic.out' });
    await this.wait(250);

    // 2. it turns over: a flash, a sparkle burst, the music-box chime
    await this.tween({ targets: this.img, scaleX: 0, duration: 200, ease: 'Sine.in' });
    this.setCard(hasFront ? front : null);
    const full = this.img.scaleX;
    const sFront = full * STAGE_SCALE;
    this.img.setScale(0, sFront);
    this.flash();
    this.burst(STAGE.x, STAGE.y);
    void opts.music?.duck(300, 4200);
    void this.sfx?.play('world-milagro');
    await this.tween({ targets: this.img, scaleX: sFront, duration: 220, ease: 'Back.out' });

    // 3. held up to be admired: the glow breathes, "No. n of N" underneath
    const pulse = this.scene.tweens.add({
      targets: this.glow, alpha: { from: 1, to: 0.6 }, scale: { from: 1.06, to: 0.96 },
      duration: 900, yoyo: true, repeat: -1, ease: 'Sine.inOut',
    });
    const caption = this.add(
      makeText(this.scene, STAGE.x, 4, opts.first ? 'YOUR FIRST MILAGRO CARD' : 'A MILAGRO CARD', theme.text.accent)
        .setOrigin(0.5, 0).setAlpha(0),
      3,
    );
    const number = this.add(
      makeText(this.scene, STAGE.x, GAME_HEIGHT - 11, `No. ${opts.number} of ${opts.total}`, theme.text.dim)
        .setOrigin(0.5, 0).setAlpha(0),
      3,
    );
    void this.tween({ targets: [caption, number], alpha: 1, duration: 400 });
    await this.wait(1500);

    // 4. it settles to the left; its words arrive
    void this.tween({ targets: [caption, number], alpha: 0, duration: 300 });
    pulse.stop();
    void this.tween({ targets: this.glow, x: REST.x, y: REST.y, alpha: 0.45, scale: 0.9, duration: 500, ease: 'Cubic.inOut' });
    await this.tween({ targets: this.img, x: REST.x, y: REST.y, scaleX: full, scaleY: full, duration: 500, ease: 'Cubic.inOut' });
    this.show({
      art: front,
      heading: opts.first ? 'YOUR FIRST CARD' : 'A MILAGRO CARD',
      sub: `No. ${opts.number} of ${opts.total}`,
      title: card.title,
      story: card.story + (card.altered ? ALTERED : '') + (opts.first ? FIRST_TIP : ''),
    }, false);
    await this.tween({ targets: words, alpha: 1, duration: 350 });
    this.scene.tweens.add({ targets: this.glow, alpha: { from: 0.45, to: 0.25 }, duration: 1400, yoyo: true, repeat: -1 });

    await this.loop({ flip: false });
    await this.tween({ targets: this.objs, alpha: 0, duration: 300 });
    this.destroy();
  }

  /** A soft white flash over the card as it turns. */
  private flash(): void {
    const f = this.add(this.scene.add.rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, 0xffffff, 0.55).setOrigin(0, 0), 4);
    this.scene.tweens.add({ targets: f, alpha: 0, duration: 380, onComplete: () => f.destroy() });
  }

  /** Little gold sparkles flung out from the card, falling and fading. */
  private burst(x: number, y: number): void {
    for (let i = 0; i < 22; i++) {
      const a = (i / 22) * Math.PI * 2 + Math.random() * 0.3;
      const d = 34 + Math.random() * 46;
      const size = Math.random() < 0.3 ? 2 : 1;
      const p = this.add(
        this.scene.add.rectangle(x, y, size, size, SPARK[i % SPARK.length]).setBlendMode(Phaser.BlendModes.ADD),
        4,
      );
      this.scene.tweens.add({
        targets: p,
        x: x + Math.cos(a) * d,
        y: y + Math.sin(a) * d * 0.8 + 10,
        alpha: { from: 1, to: 0 },
        duration: 700 + Math.random() * 600,
        ease: 'Cubic.out',
        onComplete: () => p.destroy(),
      });
    }
  }

  // ---------------------------------------------------------------------------
  // The pack
  // ---------------------------------------------------------------------------

  /** The pack: the box, then every card; resolves on B. */
  async gallery(has: (id: string) => boolean, hasBox: boolean): Promise<void> {
    const total = MILAGROS.length;
    const held = MILAGROS.filter((c) => has(c.id)).length;
    this.glow.setAlpha(0.3).setScale(0.9);
    const deck: Page[] = [
      hasBox
        ? { art: BOX_ART, heading: `MILAGROS  ${held}/${total}`, title: 'BOOJI-WOOJI MAN MILAGRO CARDS', story: MILAGRO_LORE }
        : { art: BACK_ART, heading: `MILAGROS  ${held}/${total}`, title: 'PAINTED CARDS', story: NO_BOX },
      ...MILAGROS.map((c, i) => this.cardPage(c, has(c.id), `CARD ${i + 1}/${total}`)),
    ];
    // the box and every card you hold: where UP/DOWN jump to
    const heldAt = deck.map((_, i) => (i === 0 || has(MILAGROS[i - 1].id) ? i : -1)).filter((i) => i >= 0);
    let at = 0;
    this.show(deck[at]);
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
        this.show(deck[at]);
      },
    });
    this.destroy();
  }

  private cardPage(card: MilagroCard, found: boolean, heading: string): Page {
    return found
      ? { art: milagroArt(card.id), heading, title: card.title, story: card.story + (card.altered ? ALTERED : '') }
      : { art: BACK_ART, heading, title: '? ? ?', story: UNFOUND };
  }

  // ---------------------------------------------------------------------------
  // Shared
  // ---------------------------------------------------------------------------

  /** Lay out a page's words, then (unless the ceremony owns the card) its art. */
  private show(p: Page, art = true): void {
    const mine = ++this.token;
    this.heading.setText(p.heading);
    this.sub.setText(p.sub ?? '');
    this.title.setY(p.sub ? 27 : 18).setText(p.title);
    this.story.setY(this.title.y + this.title.height + 5);
    const budget = Math.max(1, Math.floor((TEXT_BOTTOM - this.story.y) / LINE_H));
    const lines = this.story.getWrappedText(p.story);
    this.pages = [];
    for (let i = 0; i < lines.length; i += budget) this.pages.push(lines.slice(i, i + budget).join('\n'));
    if (this.pages.length === 0) this.pages.push('');
    this.page = 0;
    this.renderPage();
    if (!art) return;
    void this.ensure(p.art).then((ok) => {
      if (mine !== this.token || !this.img.active) return;
      this.setCard(ok ? p.art : null);
      this.img.setPosition(REST.x, REST.y);
    });
  }

  /** Put `key` on the card (scaled to the card's size), or show the empty slot. */
  private setCard(key: string | null): void {
    if (!key) {
      this.img.setVisible(false);
      this.slot.setVisible(true);
      return;
    }
    // painted cards, not pixel art: smooth the downscale so the lettering stays legible
    this.scene.textures.get(key).setFilter(Phaser.Textures.FilterMode.LINEAR);
    this.img.setTexture(key).setDisplaySize(CARD.w, CARD.h).setVisible(true);
    this.slot.setVisible(false);
  }

  private async ensure(key: string): Promise<boolean> {
    return this.scene.textures.exists(key) || (await loadImage(this.scene, key, key));
  }

  private tween(cfg: Phaser.Types.Tweens.TweenBuilderConfig): Promise<void> {
    return new Promise((resolve) => {
      this.scene.tweens.add({ ...cfg, onComplete: () => resolve() });
    });
  }

  private wait(ms: number): Promise<void> {
    return new Promise((resolve) => this.scene.time.delayedCall(ms, () => resolve()));
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
