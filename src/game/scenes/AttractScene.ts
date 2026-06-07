/**
 * AttractScene — the opening demo. Two kin trade blows under the battle theme, the
 * way the genre's title sequences hook you before the menu. Any input, or a short
 * timeout, advances to the Title. The Title returns here when left idle, so the game
 * loops its own trailer on the menu. Uses placeholder battlers until creature art is
 * packed (the real sprites swap in at one call site later).
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, COLORS } from '@game/config';
import { theme, hex } from '@game/ui/theme';
import { makeText } from '@game/ui/Text';
import { MusicDirector } from '@game/systems/audio/MusicDirector';
import { Sfx } from '@game/systems/audio/Sfx';
import { SHELL_INPUT_EVENT } from '@/shell/ShellManager';

const DEMO_MS = 9000;

export class AttractScene extends Phaser.Scene {
  private music!: MusicDirector;
  private shellHandler?: (e: Event) => void;

  constructor() {
    super('Attract');
  }

  create(): void {
    this.cameras.main.setBackgroundColor(COLORS.night);
    this.cameras.main.fadeIn(theme.transition.fadeMs, 0, 0, 0);
    this.music = new MusicDirector(this, 0.4);
    void this.music.play('battle-main-dusk-duel', 'assets/audio/music/battle-main-dusk-duel.mp3');
    const sfx = new Sfx(this);

    const groundY = GAME_HEIGHT - 44;
    // two placeholder battlers facing off
    const left = this.makeBattler(64, groundY, COLORS.fire);
    const right = this.makeBattler(GAME_WIDTH - 64, groundY, COLORS.water);

    // alternating lunges + hit flash, on a loop
    const lunge = (attacker: Phaser.GameObjects.Container, target: Phaser.GameObjects.Container, dir: number): void => {
      this.tweens.add({
        targets: attacker,
        x: attacker.x + dir * 14,
        duration: 160,
        yoyo: true,
        ease: 'Quad.out',
        onYoyo: () => {
          target.setScale(1.12);
          this.tweens.add({ targets: target, scale: 1, duration: 180 });
          void sfx.playVariant('battle-hit-physical', ['a', 'b', 'c']);
        },
      });
    };
    this.time.addEvent({
      delay: 1100,
      loop: true,
      callback: () => {
        const goLeft = Math.random() < 0.5;
        if (goLeft) lunge(left, right, 1);
        else lunge(right, left, -1);
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

  private makeBattler(x: number, y: number, color: string): Phaser.GameObjects.Container {
    const body = this.add.rectangle(0, 0, 26, 26, hex(color)).setStrokeStyle(1, hex(COLORS.ink));
    const shadow = this.add.ellipse(0, 16, 26, 7, hex(COLORS.night), 0.5);
    const c = this.add.container(x, y, [shadow, body]);
    this.tweens.add({ targets: body, y: -3, duration: 900, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    return c;
  }

  private toTitle(): void {
    if (this.shellHandler) window.removeEventListener(SHELL_INPUT_EVENT, this.shellHandler);
    this.shellHandler = undefined;
    this.music.stop();
    this.cameras.main.fadeOut(theme.transition.fadeMs, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start('Title'));
  }
}
