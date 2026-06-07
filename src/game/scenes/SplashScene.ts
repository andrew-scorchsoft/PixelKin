/**
 * SplashScene — the studio sting that opens the game, before the attract demo.
 *
 * Beyond branding it does one essential job: capture the user gesture that
 * browsers require before any audio can play. The Web Audio context starts
 * suspended, so without a gesture the attract trailer's battle music stays
 * silent. This splash is that gate — it animates in (lanterns kindling in the
 * dark, then "ANDREW WARD studios"), holds on a soft "PRESS START", and the
 * first key / tap / shell-press unlocks the audio context and fades into the
 * battle, which then plays with music from frame one.
 *
 * It sits only on the Preload -> Attract edge, so it shows once. The Title's
 * idle loop-back goes straight to Attract (audio already unlocked).
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, COLORS } from '@game/config';
import { theme, hex } from '@game/ui/theme';
import { makeText } from '@game/ui/Text';
import { SHELL_INPUT_EVENT } from '@/shell/ShellManager';

/** Where the kindling "stars" settle — a loose constellation above the name. */
const STARS: ReadonlyArray<{ x: number; y: number; big?: boolean }> = [
  { x: 78, y: 30 },
  { x: 104, y: 22, big: true },
  { x: 132, y: 34 },
  { x: 158, y: 24 },
  { x: 92, y: 46 },
  { x: 146, y: 48 },
  { x: 120, y: 40, big: true },
  { x: 64, y: 44 },
  { x: 176, y: 40 },
];

export class SplashScene extends Phaser.Scene {
  private shellHandler?: (e: Event) => void;
  private started = false;

  constructor() {
    super('Splash');
  }

  create(): void {
    this.cameras.main.setBackgroundColor(COLORS.night);
    this.cameras.main.fadeIn(theme.transition.fadeMs, 0, 0, 0);

    const cx = GAME_WIDTH / 2;

    // 1) Lanterns kindle in the dark — stars twinkle on in a staggered ripple.
    STARS.forEach((s, i) => {
      const r = s.big ? 2 : 1.2;
      const star = this.add.circle(s.x, s.y, r, hex(COLORS.diamond)).setAlpha(0).setScale(0.4);
      this.tweens.add({
        targets: star,
        alpha: s.big ? 1 : 0.75,
        scale: 1,
        delay: 200 + i * 90,
        duration: 360,
        ease: 'Back.out',
      });
      // a slow shimmer once lit
      this.tweens.add({
        targets: star,
        alpha: s.big ? 0.55 : 0.35,
        delay: 200 + i * 90 + 360,
        duration: 1200 + i * 80,
        yoyo: true,
        repeat: -1,
        ease: 'Sine.inOut',
      });
    });

    // 2) Studio name rises and brightens once the constellation is lit.
    const titleY = GAME_HEIGHT / 2 + 6;
    const glow = makeText(this, cx, titleY, 'ANDREW WARD', theme.text.title)
      .setOrigin(0.5)
      .setTint(hex(COLORS.water))
      .setAlpha(0)
      .setScale(1.06);
    glow.setBlendMode(Phaser.BlendModes.ADD);
    const name = makeText(this, cx, titleY, 'ANDREW WARD', theme.text.title)
      .setOrigin(0.5)
      .setAlpha(0)
      .setScale(1.12);

    [name, glow].forEach((t, i) => {
      this.tweens.add({
        targets: t,
        alpha: i === 0 ? 1 : 0.6,
        scale: i === 0 ? 1 : 1.04,
        y: titleY - 4,
        delay: 1000,
        duration: 560,
        ease: 'Cubic.out',
      });
    });
    // soft breathing glow behind the name
    this.tweens.add({
      targets: glow,
      alpha: 0.25,
      delay: 1560,
      duration: 1400,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.inOut',
    });

    const studios = makeText(this, cx, titleY + 16, 'S T U D I O S', theme.text.dim)
      .setOrigin(0.5)
      .setAlpha(0);
    this.tweens.add({ targets: studios, alpha: 1, delay: 1500, duration: 600, ease: 'Linear' });

    // 3) A single light sweep across the name, like a lantern passing.
    const sweep = this.add
      .rectangle(0, titleY - 4, 10, 26, hex(COLORS.bone), 0.5)
      .setOrigin(0.5)
      .setBlendMode(Phaser.BlendModes.ADD)
      .setAlpha(0);
    this.tweens.add({
      targets: sweep,
      x: { from: cx - 70, to: cx + 70 },
      alpha: { from: 0, to: 0.5 },
      delay: 1600,
      duration: 700,
      ease: 'Sine.inOut',
      yoyo: true,
      hold: 0,
      onComplete: () => sweep.destroy(),
    });

    // 4) The gate prompt — appears after the sting, blinks softly, holds for input.
    const prompt = makeText(this, cx, GAME_HEIGHT - 18, 'PRESS START', theme.text.dim)
      .setOrigin(0.5)
      .setAlpha(0);
    this.tweens.add({
      targets: prompt,
      alpha: 1,
      delay: 2400,
      duration: 400,
      onComplete: () => {
        this.tweens.add({ targets: prompt, alpha: 0.2, duration: 700, yoyo: true, repeat: -1 });
      },
    });

    // Any input — keyboard, pointer, or the DOM shell's on-screen buttons —
    // unlocks audio and advances. Accepted at any point, even mid-animation.
    const go = (): void => this.begin();
    this.input.keyboard?.once('keydown', go);
    this.input.once('pointerdown', go);
    this.shellHandler = () => go();
    window.addEventListener(SHELL_INPUT_EVENT, this.shellHandler);
  }

  private begin(): void {
    if (this.started) return;
    this.started = true;
    if (this.shellHandler) window.removeEventListener(SHELL_INPUT_EVENT, this.shellHandler);
    this.shellHandler = undefined;

    // Resume the (now gesture-unlocked) Web Audio context so the attract music
    // is audible the instant it starts. Phaser also auto-unlocks on this gesture;
    // resuming explicitly avoids any first-frame silence.
    void this.unlockAudio();

    this.cameras.main.fadeOut(theme.transition.fadeMs, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => this.scene.start('Attract'));
  }

  private async unlockAudio(): Promise<void> {
    const sound = this.sound as Phaser.Sound.WebAudioSoundManager;
    if (sound.context?.state === 'suspended') {
      try {
        await sound.context.resume();
      } catch {
        /* ignore — Phaser's own unlock listener will catch the gesture */
      }
    }
  }
}
