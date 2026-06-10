/**
 * KindlePrompt — the witnessed kindling ceremony (the genre's evolution moment,
 * in PixelKin's idiom: a kin's inner light catching).
 *
 * Flow: announce ("...is kindling!") → the player may let it bloom or cup the
 * flame for now (the classic cancel — the kin will offer again after its next
 * level) → on KINDLE: a slow white-gold bloom, the species swaps
 * (KinInstance.applyKindle), the new name lands, and any kindling moves are
 * learned through the shared MoveLearnPrompt (free slot auto-learns; a full kit
 * lets the player set one aside).
 *
 * Scene-agnostic like the rest of the kit: BattleScene passes `onTransform` to
 * swap the battler sprite at the bloom's peak; the overworld (Kindlestone use)
 * passes nothing and the flash carries the moment. Resolves true if the kin
 * kindled.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme } from './theme';
import { Menu } from './Menu';
import { DialogueBox } from './DialogueBox';
import { MoveLearnPrompt } from './MoveLearnPrompt';
import type { KinInstance } from '@game/systems/party/KinInstance';
import type { Kindling, Move } from '@game/data/dex';
import type { Sfx } from '@game/systems/audio/Sfx';

export class KindlePrompt {
  constructor(
    private readonly scene: Phaser.Scene,
    private readonly kin: KinInstance,
    private readonly kindling: Kindling,
    private readonly sfx?: Sfx,
    /** Called at the bloom's peak, after the species swap — swap sprites here. */
    private readonly onTransform?: () => void,
  ) {}

  async run(): Promise<boolean> {
    const oldName = this.kin.displayName;

    await new DialogueBox(this.scene, this.sfx).run([
      { text: `What's this...? ${oldName}'s light is rising — ${oldName} is kindling!` },
    ]);

    const choice = await new Menu(
      this.scene,
      [
        { label: 'LET IT KINDLE', value: 'kindle' },
        { label: 'CUP THE FLAME', value: 'wait' },
      ],
      { x: 8, y: 8, sfx: this.sfx, cancellable: true },
    ).run();

    if (choice !== 'kindle') {
      await new DialogueBox(this.scene, this.sfx).run([
        { text: `You cup the flame, and ${oldName}'s light settles — for now.` },
      ]);
      return false;
    }

    // The bloom: a slow white-gold wash, the swap at its peak, then the reveal.
    void this.sfx?.playVariant('progress-levelup', ['a', 'b']);
    await this.bloom(() => {
      const { learned, pending } = this.kin.applyKindle(this.kindling);
      this.learnedNow = learned.map((m) => m.name);
      this.pendingMoves = pending;
      this.onTransform?.();
    });

    await new DialogueBox(this.scene, this.sfx).run([
      { text: `${oldName} kindled into ${this.kin.species.name}!` },
    ]);
    for (const name of this.learnedNow) {
      await new DialogueBox(this.scene, this.sfx).run([
        { text: `${this.kin.displayName} learned ${name}!` },
      ]);
    }
    for (const move of this.pendingMoves) {
      await new MoveLearnPrompt(this.scene, this.kin, move, this.sfx).run();
    }
    return true;
  }

  private learnedNow: string[] = [];
  private pendingMoves: Move[] = [];

  /** A two-beat white-gold flash; `atPeak` runs while the screen is washed out. */
  private bloom(atPeak: () => void): Promise<void> {
    return new Promise((resolve) => {
      const wash = this.scene.add
        .rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, 0xfff3d0, 0)
        .setOrigin(0, 0)
        .setScrollFactor(0)
        .setDepth(theme.depth.overlayDim + 1);
      this.scene.tweens.add({
        targets: wash,
        fillAlpha: 1,
        duration: 650,
        ease: 'Sine.easeIn',
        onComplete: () => {
          atPeak();
          this.scene.tweens.add({
            targets: wash,
            fillAlpha: 0,
            duration: 800,
            ease: 'Sine.easeOut',
            delay: 250,
            onComplete: () => {
              wash.destroy();
              resolve();
            },
          });
        },
      });
    });
  }
}
