/**
 * TrainerStage — the classic trainer-intro beat on the battle screen.
 *
 * The opponent trainer (64×64, `tb_<key>`) slides in from the right onto the foe's
 * spot and your apprentice's back slides in from the left; after the trainer has
 * spoken they slide out (trainer first, as they send out their kin, then you, as
 * yours goes in). After a win the trainer slides back in for their closing words.
 * A missing texture simply skips the picture (the lines still play).
 */
import Phaser from 'phaser';
import { GAME_WIDTH } from '@game/config';
import { theme, hex } from '@game/ui/theme';
import { battlePaceFactor } from '@game/ui/preferences';

const SLIDE_MS = 420;

export class TrainerStage {
  private readonly foe?: Phaser.GameObjects.Container;
  private readonly player?: Phaser.GameObjects.Container;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly foeHome: { x: number; y: number },
    private readonly playerHome: { x: number; y: number },
    foeTexture: string | undefined,
    playerTexture: string | undefined,
  ) {
    const depth = theme.depth.world + 5;
    // each figure stands on a soft oval of shadow, so it reads as on the ground
    const figure = (x: number, y: number, tex: string, shadowW: number) =>
      scene.add.container(x, y, [
        scene.add.ellipse(0, -1, shadowW, 7, hex(theme.color.panelShadow), 0.55),
        scene.add.image(0, 0, tex).setOrigin(0.5, 1),
      ]).setDepth(depth).setScrollFactor(0);
    if (foeTexture && scene.textures.exists(foeTexture)) {
      this.foe = figure(GAME_WIDTH + 40, foeHome.y, foeTexture, 40);
    }
    if (playerTexture && scene.textures.exists(playerTexture)) {
      this.player = figure(-40, playerHome.y, playerTexture, 0);
    }
  }

  get hasFoe(): boolean {
    return !!this.foe;
  }

  private slide(img: Phaser.GameObjects.Container | undefined, x: number, ease: string): Promise<void> {
    if (!img) return Promise.resolve();
    return new Promise((resolve) => {
      this.scene.tweens.add({
        targets: img, x, duration: SLIDE_MS * battlePaceFactor(), ease, onComplete: () => resolve(),
      });
    });
  }

  /** Both step on: the trainer from the right, you from the left. */
  async enter(): Promise<void> {
    await Promise.all([
      this.slide(this.foe, this.foeHome.x, 'Cubic.out'),
      this.slide(this.player, this.playerHome.x, 'Cubic.out'),
    ]);
  }

  /** The trainer steps aside to send out their kin. */
  exitFoe(): Promise<void> {
    return this.slide(this.foe, GAME_WIDTH + 40, 'Cubic.in');
  }

  /** You step back as your kin goes in. */
  exitPlayer(): Promise<void> {
    return this.slide(this.player, -40, 'Cubic.in');
  }

  /** After the win: the trainer comes back for their closing words. */
  reenterFoe(): Promise<void> {
    return this.slide(this.foe, this.foeHome.x, 'Cubic.out');
  }

  destroy(): void {
    this.foe?.destroy();
    this.player?.destroy();
  }
}
