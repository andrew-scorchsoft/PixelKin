/**
 * KindlePrompt — the witnessed kindling ceremony (the genre's evolution moment,
 * in PixelKin's idiom: a kin's inner light catching).
 *
 * Flow, the classic shape: "...is kindling!" → its own night-sky stage takes the
 * screen and the `kindle-ceremony` cue starts its heartbeat → the kin glows white
 * and flickers between its old shape and the new silhouette, faster and faster →
 * the bloom (a white-out on the cue's last bar), the species swaps
 * (KinInstance.applyKindle), the new kin is revealed to the `kindle-fanfare`, and
 * any kindling moves are learned through the shared MoveLearnPrompt.
 *
 * The player may press B at ANY point during the flicker to cup the flame (the
 * classic cancel): the light settles back, nothing changes, and the kin offers
 * again after its next level (or next bond gain, for a bond kindling).
 *
 * Scene-agnostic like the rest of the kit: BattleScene passes `onTransform` to
 * swap the battler sprite behind the stage; the overworld (ITEMS) passes nothing.
 * `music` hands the ceremony the scene's bed so it can take the soundtrack and
 * give it back (`restore`) afterwards; without it the ceremony plays silent music
 * but still runs. Resolves true if the kin kindled.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { DialogueBox } from './DialogueBox';
import { MoveLearnPrompt } from './MoveLearnPrompt';
import { battlerTexture } from './battle/Battler';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { hasCreatureSprite, loadCreatureSprite } from '@game/systems/sprites/CreatureSprites';
import { SPECIES_BY_ID } from '@game/data/dex';
import type { KinInstance } from '@game/systems/party/KinInstance';
import type { Kindling, Move, Species } from '@game/data/dex';
import type { Sfx } from '@game/systems/audio/Sfx';
import type { MusicDirector } from '@game/systems/audio/MusicDirector';

/** The scene's music, lent to the ceremony. */
export interface KindleMusic {
  director: MusicDirector;
  /** Put the scene's own bed back once the ceremony is over. */
  restore(): void;
}

const MUSIC_DIR = 'assets/audio/music/';
const CEREMONY_CUE = 'kindle-ceremony';
const FANFARE_CUE = 'kindle-fanfare';

/**
 * The ceremony cue is 8 bars at 168 BPM (assets/audio/midi/specs/kindle-ceremony.json):
 * the flicker runs bars 1–7 and the bloom lands on the bar-8 climb, so the white-out
 * hits as the music peaks. Change the cue's tempo/length and change these with it.
 */
const BAR_MS = (60_000 / 168) * 4;
const GLOW_MS = BAR_MS; // bar 1: the kin warms to white before it starts to change
const FLICKER_MS = BAR_MS * 6; // bars 2–7: old shape ⇄ new shape, accelerating
const BLOOM_IN_MS = 520; // the white-out, into the bar-8 climb

/** Flicker period (ms one shape is held) from slow to frantic over FLICKER_MS. */
const FLICKER_SLOW_MS = 520;
const FLICKER_FAST_MS = 45;

const SKY = hex(theme.kindle.sky);
const GLOW = hex(theme.kindle.glow);
const SILHOUETTE = hex(theme.kindle.silhouette);
const BLOOM = hex(theme.kindle.bloom);
const MOTE = hex(theme.kindle.mote);

export class KindlePrompt {
  constructor(
    private readonly scene: Phaser.Scene,
    private readonly kin: KinInstance,
    private readonly kindling: Kindling,
    private readonly sfx?: Sfx,
    /** Called right after the species swap (under the bloom) — swap sprites here. */
    private readonly onTransform?: () => void,
    private readonly music?: KindleMusic,
  ) {}

  private learnedNow: string[] = [];
  private pendingMoves: Move[] = [];
  private readonly parts: Phaser.GameObjects.GameObject[] = [];

  async run(): Promise<boolean> {
    const oldName = this.kin.displayName;
    const oldSpecies = this.kin.species;
    const newSpecies = SPECIES_BY_ID.get(this.kindling.into);
    if (!newSpecies) return false;

    // Warm both shapes before the stage opens so the flicker never pops in late.
    const [oldKey, newKey] = await Promise.all([
      this.textureFor(oldSpecies),
      this.textureFor(newSpecies),
    ]);

    const stage = this.buildStage(oldKey);
    await this.fade(stage.cover, 1, 260);

    await new DialogueBox(this.scene, this.sfx).run([
      { text: `What's this...? ${oldName}'s light is rising — ${oldName} is kindling!` },
    ]);

    void this.music?.director.play(CEREMONY_CUE, `${MUSIC_DIR}${CEREMONY_CUE}.mp3`, { classic: true });
    void this.sfx?.playVariant('kindle-start', ['a', 'b']);

    const kindled = await this.ceremony(stage, oldKey, newKey);

    if (!kindled) {
      void this.music?.director.fadeToSilence(500);
      void this.sfx?.play('kindle-cancel-a');
      await new DialogueBox(this.scene, this.sfx).run([
        { text: `You cup the flame, and ${oldName}'s light settles — it didn't kindle.` },
        { text: `It may try again when it grows a little more.` },
      ]);
      await this.close(stage.cover);
      return false;
    }

    // The new kin, revealed to the fanfare.
    this.music?.director.stop();
    this.music?.director.playSting(FANFARE_CUE, `${MUSIC_DIR}${FANFARE_CUE}.mp3`, 0.7);
    void this.sfx?.playVariant('kindle-complete', ['a', 'b', 'c']);
    await new DialogueBox(this.scene, this.sfx).run([
      { text: `${oldName} kindled into ${newSpecies.name}!` },
    ]);
    for (const name of this.learnedNow) {
      await new DialogueBox(this.scene, this.sfx).run([
        { text: `${this.kin.displayName} learned ${name}!` },
      ]);
    }
    for (const move of this.pendingMoves) {
      await new MoveLearnPrompt(this.scene, this.kin, move, this.sfx).run();
    }
    await this.close(stage.cover);
    return true;
  }

  /** Packed battle-front sprite if there is one, else the type-tinted placeholder. */
  private async textureFor(species: Species): Promise<string> {
    if (hasCreatureSprite(species.id, 'front')) {
      const key = await loadCreatureSprite(this.scene, species.id, 'front');
      if (key) return key;
    }
    return battlerTexture(this.scene, species, 'foe');
  }

  /**
   * The ceremony's own screen: a night-sky panel (it hides the battle/world, like
   * the classics' dedicated evolution screen), a soft glow behind the kin, rising
   * motes and the kin itself. Sits at the panel depth but is created after the
   * battle HUD, so it covers the HP boxes while every DialogueBox opened later
   * still draws on top of it.
   */
  private buildStage(oldKey: string): {
    cover: Phaser.GameObjects.Container;
    kin: Phaser.GameObjects.Image;
    sil: Phaser.GameObjects.Image;
    glow: Phaser.GameObjects.Arc[];
    motes: Phaser.GameObjects.Rectangle[];
    hint: Phaser.GameObjects.Text;
  } {
    const cx = GAME_WIDTH / 2;
    const cy = 64;
    const sky = this.scene.add.rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, SKY, 1).setOrigin(0, 0);
    // A soft halo: three stacked faint discs read as light, one solid disc reads as a plate.
    const glow = [1, 0.72, 0.46].map((k) => this.scene.add.circle(cx, cy, 30 * k, GLOW, 0));
    const motes: Phaser.GameObjects.Rectangle[] = [];
    for (let i = 0; i < 14; i++) {
      const m = this.scene.add.rectangle(0, 0, 1, 1, MOTE, 0);
      motes.push(m);
    }
    const kin = this.scene.add.image(cx, cy, oldKey);
    // The white silhouette rides on top of the kin and fades in as its light rises.
    const sil = this.scene.add.image(cx, cy, oldKey).setTintFill(SILHOUETTE).setAlpha(0);
    const hint = makeText(this.scene, GAME_WIDTH - 6, 6, 'B: cup the flame', theme.text.dim)
      .setOrigin(1, 0)
      .setAlpha(0);
    const cover = this.scene.add
      .container(0, 0, [sky, ...glow, ...motes, kin, sil, hint])
      .setScrollFactor(0)
      .setDepth(theme.depth.panel)
      .setAlpha(0);
    this.parts.push(cover);
    return { cover, kin, sil, glow, motes, hint };
  }

  /**
   * The flicker. Resolves true when the bloom completes (the kin has kindled),
   * false if the player pressed B first.
   */
  private ceremony(
    stage: ReturnType<KindlePrompt['buildStage']>,
    oldKey: string,
    newKey: string,
  ): Promise<boolean> {
    const { kin, sil, glow, motes, hint } = stage;
    const cx = GAME_WIDTH / 2;
    const cy = 64;
    const input = new InputController(this.scene);
    const startAt = this.scene.time.now;
    let showingNew = false;
    let nextSwapAt = startAt + GLOW_MS;
    let phase: 'flicker' | 'bloom' | 'done' = 'flicker';

    // Motes: each rises from below the kin on its own lane and loops.
    const moteSeed = motes.map((_, i) => ({
      x: cx - 34 + ((i * 37) % 68),
      speed: 0.012 + ((i * 13) % 7) * 0.003,
      offset: (i * 53) % 90,
    }));

    hint.setAlpha(1);

    return new Promise((resolve) => {
      const finish = (kindled: boolean): void => {
        phase = 'done';
        this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
        input.destroy();
        hint.setAlpha(0);
        for (const m of motes) m.setAlpha(0);
        resolve(kindled);
      };

      const tick = (): void => {
        if (phase !== 'flicker') return;
        input.update();
        const now = this.scene.time.now;
        const t = now - startAt;

        // B, any time before the bloom: cup the flame.
        if (input.justPressed(InputAction.Cancel)) {
          kin.setTexture(oldKey).setScale(1).setVisible(true);
          sil.setTexture(oldKey).setScale(1);
          this.scene.tweens.add({ targets: sil, alpha: 0, duration: 500 });
          this.scene.tweens.add({ targets: glow, alpha: 0, duration: 500 });
          finish(false);
          return;
        }

        // Warm-up: the kin pales toward white over the first bar.
        const warm = Math.min(1, t / GLOW_MS);
        const f0 = Math.max(0, Math.min(1, (t - GLOW_MS) / FLICKER_MS));
        const r = 26 + 10 * warm + 8 * f0 + Math.sin(t / 140) * 2;
        glow.forEach((g, i) => {
          g.setFillStyle(GLOW, (0.06 + 0.06 * i) * (0.4 + 0.6 * warm + 0.6 * f0));
          g.setRadius(r * [1, 0.72, 0.46][i]);
        });
        sil.setAlpha(warm);

        // The flicker: old ⇄ new, the hold shrinking from slow to frantic.
        const f = Math.max(0, Math.min(1, (t - GLOW_MS) / FLICKER_MS));
        if (t >= GLOW_MS && now >= nextSwapAt) {
          showingNew = !showingNew;
          const key = showingNew ? newKey : oldKey;
          kin.setTexture(key).setVisible(false);
          sil.setTexture(key);
          const hold = FLICKER_SLOW_MS + (FLICKER_FAST_MS - FLICKER_SLOW_MS) * Math.pow(f, 0.7);
          // The new shape is glimpsed briefly at first, held longer as it wins out.
          nextSwapAt = now + (showingNew ? hold * (0.5 + 0.5 * f) : hold);
        }
        sil.setScale(1 + 0.05 * f * Math.sin(t / 60));

        // Motes rise faster as the light builds.
        for (let i = 0; i < motes.length; i++) {
          const s = moteSeed[i];
          const y = cy + 40 - ((t * s.speed * (1 + 2 * f) + s.offset) % 90);
          motes[i].setPosition(s.x, y).setAlpha(warm * 0.8);
        }

        if (t >= GLOW_MS + FLICKER_MS) {
          phase = 'bloom';
          hint.setAlpha(0);
          void this.bloom(kin, sil, glow, newKey).then(() => finish(true));
        }
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  /** The white-out; the species swaps while the screen is washed, then the reveal. */
  private bloom(
    kin: Phaser.GameObjects.Image,
    sil: Phaser.GameObjects.Image,
    glow: Phaser.GameObjects.Arc[],
    newKey: string,
  ): Promise<void> {
    return new Promise((resolve) => {
      const wash = this.scene.add
        .rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, BLOOM, 0)
        .setOrigin(0, 0)
        .setScrollFactor(0)
        .setDepth(theme.depth.panel);
      this.parts.push(wash);
      this.scene.tweens.add({
        targets: wash,
        fillAlpha: 1,
        duration: BLOOM_IN_MS,
        ease: 'Sine.easeIn',
        onComplete: () => {
          const { learned, pending } = this.kin.applyKindle(this.kindling);
          this.learnedNow = learned.map((m) => m.name);
          this.pendingMoves = pending;
          this.onTransform?.();
          kin.setTexture(newKey).setScale(1).setVisible(true);
          sil.setVisible(false);
          for (const g of glow) g.setAlpha(0.6);
          this.ringBurst(kin.x, kin.y);
          this.scene.tweens.add({
            targets: wash,
            fillAlpha: 0,
            duration: 700,
            delay: 200,
            ease: 'Sine.easeOut',
            onComplete: () => {
              wash.destroy();
              // A proud little hop as it stands in its new shape.
              this.scene.tweens.add({
                targets: kin,
                y: kin.y - 6,
                duration: 140,
                yoyo: true,
                ease: 'Quad.easeOut',
                onComplete: () => resolve(),
              });
            },
          });
        },
      });
    });
  }

  /** Two light rings spreading out from the new kin as the bloom clears. */
  private ringBurst(x: number, y: number): void {
    for (let i = 0; i < 2; i++) {
      const ring = this.scene.add
        .circle(x, y, 8)
        .setStrokeStyle(1, GLOW, 0.9)
        .setScrollFactor(0)
        .setDepth(theme.depth.panel);
      this.parts.push(ring);
      this.scene.tweens.add({
        targets: ring,
        radius: 70,
        alpha: 0,
        delay: 200 + i * 220,
        duration: 900,
        ease: 'Cubic.easeOut',
        onComplete: () => ring.destroy(),
      });
    }
  }

  /** Fade the stage out, tear it down and hand the scene its music back. */
  private async close(cover: Phaser.GameObjects.Container): Promise<void> {
    await this.fade(cover, 0, 300);
    for (const p of this.parts) p.destroy();
    this.parts.length = 0;
    this.music?.restore();
  }

  private fade(target: Phaser.GameObjects.Container, alpha: number, duration: number): Promise<void> {
    return new Promise((resolve) => {
      this.scene.tweens.add({ targets: target, alpha, duration, onComplete: () => resolve() });
    });
  }
}
