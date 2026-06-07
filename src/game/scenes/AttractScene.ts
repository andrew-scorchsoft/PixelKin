/**
 * AttractScene — the opening demo. Two kin trade blows under the battle theme, the
 * way the genre's title sequences hook you before the menu. Any input, or a short
 * timeout, advances to the Title. The Title returns here when left idle, so the game
 * loops its own trailer on the menu.
 *
 * The duel features the two starters on the logo — Vulpyre (back view, "your" side,
 * lower-left) facing off against Brinix (front view, the "foe", upper-right) — in the
 * same diagonal composition BattleScene uses, so the trailer reads as a real fight.
 * Their packed sprites are preloaded in PreloadScene; if one is missing we fall back
 * to a type-tinted placeholder and swap the real art in when it loads.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, COLORS } from '@game/config';
import { theme, hex } from '@game/ui/theme';
import { makeText } from '@game/ui/Text';
import { MusicDirector } from '@game/systems/audio/MusicDirector';
import { Sfx } from '@game/systems/audio/Sfx';
import {
  creatureTextureKey,
  loadCreatureSprite,
  type CreatureView,
} from '@game/systems/sprites/CreatureSprites';
import { SHELL_INPUT_EVENT } from '@/shell/ShellManager';

const DEMO_MS = 9000;

/** The two combatants in the trailer duel — the starters that appear on the logo. */
const PLAYER_KIN = { id: 1, view: 'back' as CreatureView, color: COLORS.fire }; // Vulpyre
const FOE_KIN = { id: 2, view: 'front' as CreatureView, color: COLORS.water }; // Brinix

/** Mirror the real battle layout: foe upper-right, your kin lower-left. */
const FOE_POS = { x: GAME_WIDTH - 58, y: 62 };
const PLAYER_POS = { x: 60, y: 108 };

/**
 * The parallax arena behind the duel. Three seamless mirror-strip layers
 * (far sky → mid stone tiers → near silhouetted braziers) scrolled in the same
 * direction at rising speeds, so the scene reads as a slow orbit around an arena
 * rather than a side-scrolling treadmill. `speed` is in px/sec; all stay behind
 * the battlers (negative depth) and dim, so the kin always read first.
 */
const ARENA_LAYERS = [
  { key: 'assets/backgrounds/attract/arena-sky.webp', alpha: 1, speed: 4, depth: -30 },
  { key: 'assets/backgrounds/attract/arena-tiers.webp', alpha: 0.8, speed: 9, depth: -20 },
  { key: 'assets/backgrounds/attract/arena-fore.webp', alpha: 0.95, speed: 16, depth: -10 },
] as const;

/** Asset paths for the parallax layers, for PreloadScene to queue. */
export const ARENA_LAYER_PATHS: readonly string[] = ARENA_LAYERS.map((l) => l.key);

export class AttractScene extends Phaser.Scene {
  private music!: MusicDirector;
  private shellHandler?: (e: Event) => void;
  private parallax: { sprite: Phaser.GameObjects.TileSprite; speed: number }[] = [];

  constructor() {
    super('Attract');
  }

  create(): void {
    this.parallax = [];
    this.cameras.main.setBackgroundColor(COLORS.night);
    this.cameras.main.fadeIn(theme.transition.fadeMs, 0, 0, 0);
    this.buildArena();
    this.music = new MusicDirector(this, 0.4);
    void this.music.play('battle-main-dusk-duel', 'assets/audio/music/battle-main-dusk-duel.mp3');
    const sfx = new Sfx(this);

    const foe = this.makeBattler(FOE_POS.x, FOE_POS.y, FOE_KIN.id, FOE_KIN.view, FOE_KIN.color);
    const player = this.makeBattler(PLAYER_POS.x, PLAYER_POS.y, PLAYER_KIN.id, PLAYER_KIN.view, PLAYER_KIN.color);

    // alternating lunges + hit flash, on a loop
    const lunge = (
      attacker: Phaser.GameObjects.Container,
      target: { container: Phaser.GameObjects.Container; body: Phaser.GameObjects.Image },
      dx: number,
      dy: number,
    ): void => {
      this.tweens.add({
        targets: attacker,
        x: attacker.x + dx,
        y: attacker.y + dy,
        duration: 160,
        yoyo: true,
        ease: 'Quad.out',
        onYoyo: () => {
          target.body.setScale(1.12);
          this.tweens.add({ targets: target.body, scale: 1, duration: 180 });
          this.tweens.add({ targets: target.body, alpha: 0.3, duration: 55, yoyo: true, repeat: 2 });
          void sfx.playVariant('battle-hit-physical', ['a', 'b', 'c']);
        },
      });
    };
    // Lunge along the diagonal toward the opponent.
    this.time.addEvent({
      delay: 1100,
      loop: true,
      callback: () => {
        if (Math.random() < 0.5) lunge(player.container, foe, 14, -10);
        else lunge(foe.container, player, -14, 10);
      },
    });

    makeText(this, GAME_WIDTH / 2, 18, 'PIXELKIN', theme.text.title).setOrigin(0.5);
    const prompt = makeText(this, GAME_WIDTH / 2, GAME_HEIGHT - 16, 'PRESS START', theme.text.dim).setOrigin(0.5);
    this.tweens.add({ targets: prompt, alpha: 0.2, duration: 700, yoyo: true, repeat: -1 });

    // advance on any input, or after the demo plays out
    const go = (): void => this.toTitle();
    this.input.keyboard?.once('keydown', go);
    this.input.once('pointerdown', go);
    this.shellHandler = () => go();
    window.addEventListener(SHELL_INPUT_EVENT, this.shellHandler);
    this.time.delayedCall(DEMO_MS, go);
  }

  /** Continuously pan each parallax layer; differing speeds give the depth. */
  update(_time: number, delta: number): void {
    for (const layer of this.parallax) {
      layer.sprite.tilePositionX += (layer.speed * delta) / 1000;
    }
  }

  /**
   * Build the parallax arena: stacked seamless tile-strips behind the battlers, a
   * gentle dim overlay so the kin pop, and a few drifting lantern motes for depth.
   * Falls back gracefully to the plain night fill if a layer texture is missing.
   */
  private buildArena(): void {
    for (const layer of ARENA_LAYERS) {
      if (!this.textures.exists(layer.key)) continue;
      const sprite = this.add
        .tileSprite(0, 0, GAME_WIDTH, GAME_HEIGHT, layer.key)
        .setOrigin(0, 0)
        .setAlpha(layer.alpha)
        .setDepth(layer.depth);
      this.parallax.push({ sprite, speed: layer.speed });
    }
    // Knock the whole backdrop back a touch so the duel stays the focus.
    this.add
      .rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, hex(COLORS.night), 0.22)
      .setOrigin(0, 0)
      .setDepth(-5);
    this.addMotes();
  }

  /** A handful of slow-rising lantern sparks — subtle atmosphere, never busy. */
  private addMotes(): void {
    for (let i = 0; i < 7; i++) {
      const x = Phaser.Math.Between(8, GAME_WIDTH - 8);
      const y = Phaser.Math.Between(20, GAME_HEIGHT - 24);
      const mote = this.add
        .circle(x, y, 1, hex(COLORS.diamond), 0.7)
        .setDepth(-4);
      this.tweens.add({
        targets: mote,
        y: y - Phaser.Math.Between(10, 20),
        alpha: 0.15,
        duration: Phaser.Math.Between(2200, 3800),
        delay: Phaser.Math.Between(0, 1500),
        yoyo: true,
        repeat: -1,
        ease: 'Sine.inOut',
      });
    }
  }

  /**
   * A bobbing battler. Uses the packed kin sprite if available (preloaded), otherwise a
   * type-tinted placeholder that the real sprite swaps into once it loads.
   */
  private makeBattler(
    x: number,
    y: number,
    id: number,
    view: CreatureView,
    color: string,
  ): { container: Phaser.GameObjects.Container; body: Phaser.GameObjects.Image } {
    const shadow = this.add.ellipse(0, 28, 36, 10, hex(COLORS.night), 0.5);
    const body = this.add.image(0, 0, this.spriteKeyOrPlaceholder(id, view, color)).setOrigin(0.5);
    const c = this.add.container(x, y, [shadow, body]);
    this.tweens.add({ targets: body, y: -3, duration: 900, yoyo: true, repeat: -1, ease: 'Sine.inOut' });

    // If the packed sprite wasn't preloaded, fetch it lazily and swap it in.
    if (!this.textures.exists(creatureTextureKey(id, view))) {
      void loadCreatureSprite(this, id, view).then((key) => {
        if (key && body.active) body.setTexture(key);
      });
    }
    return { container: c, body };
  }

  /** The packed texture key if loaded, else a generated rounded type-tinted placeholder. */
  private spriteKeyOrPlaceholder(id: number, view: CreatureView, color: string): string {
    const key = creatureTextureKey(id, view);
    if (this.textures.exists(key)) return key;

    const phKey = `attract_ph_${color}`;
    if (!this.textures.exists(phKey)) {
      const g = this.add.graphics();
      g.fillStyle(hex(color), 1);
      g.fillRoundedRect(0, 0, 30, 30, 6);
      g.lineStyle(1, hex(COLORS.ink), 0.8);
      g.strokeRoundedRect(0.5, 0.5, 29, 29, 6);
      g.generateTexture(phKey, 30, 30);
      g.destroy();
    }
    return phKey;
  }

  private toTitle(): void {
    if (this.shellHandler) window.removeEventListener(SHELL_INPUT_EVENT, this.shellHandler);
    this.shellHandler = undefined;
    this.music.stop();
    this.cameras.main.fadeOut(theme.transition.fadeMs, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start('Title'));
  }
}
