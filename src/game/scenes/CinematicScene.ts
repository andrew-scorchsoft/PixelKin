/**
 * CinematicScene — plays a CinematicScript (content/cinematics.ts): full-screen
 * illustrated key-art panels with narration, cross-dissolves, and music as drama.
 * It is the cold-open prologue today and any later "chapter card" tomorrow — the
 * sequence is data, this scene is the player.
 *
 * It sits AFTER the Title (New Game routes here), so the Splash audio-unlock gesture
 * has already happened and the foreboding cue is audible from frame one. Missing
 * panel art falls back to a night-fill + starfield, so it always plays. Press Cancel
 * (B / X) to skip straight to the destination scene.
 *
 * Narration is rendered through the shared DialogueBox (typewriter, advance on
 * Confirm) so it reads identically to the rest of the game; skip is watched on a
 * separate InputController (Cancel), so the two never double-read a press.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, COLORS } from '@game/config';
import { theme, hex } from '@game/ui/theme';
import { DialogueBox } from '@game/ui/DialogueBox';
import { flash, shake } from '@game/ui/Transitions';
import { MusicDirector } from '@game/systems/audio/MusicDirector';
import { Sfx } from '@game/systems/audio/Sfx';
import { loadImage } from '@game/systems/sprites/loadImage';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { getCinematic, type CinematicBeat, type CinematicScript } from '@game/content/cinematics';

interface CinematicSceneData {
  scriptId: string;
  /** Override where the sequence goes when done (e.g. World with the spawn data). */
  next?: { scene: string; data?: unknown };
}

const MUSIC_URL = (key: string): string => `assets/audio/music/${key}.mp3`;

export class CinematicScene extends Phaser.Scene {
  private music!: MusicDirector;
  private sfx!: Sfx;
  private skipInput?: InputController;
  private skipped = false;
  private finished = false;
  private activeBox?: DialogueBox;
  private currentPanel?: Phaser.GameObjects.Image;
  private next: { scene: string; data?: unknown } = { scene: 'World' };

  constructor() {
    super('Cinematic');
  }

  create(data: CinematicSceneData): void {
    this.skipped = false;
    this.finished = false;
    this.currentPanel = undefined;

    this.cameras.main.setBackgroundColor(COLORS.night);
    this.cameras.main.fadeIn(theme.transition.fadeMs, 0, 0, 0);
    this.drawStarfield();

    this.music = new MusicDirector(this, 0.4);
    this.sfx = new Sfx(this);

    const script = getCinematic(data.scriptId);
    this.next = data.next ?? script?.next ?? { scene: 'World' };
    if (!script) {
      this.finish();
      return;
    }

    // Skip-watch on its own controller so it never competes with the DialogueBox's Confirm.
    this.skipInput = new InputController(this);
    void this.playScript(script);
  }

  update(): void {
    if (this.finished) return;
    this.skipInput?.update();
    if (!this.skipped && this.skipInput?.justPressed(InputAction.Cancel)) {
      this.skipped = true;
      this.finish();
    }
  }

  private async playScript(script: CinematicScript): Promise<void> {
    for (const beat of script.beats) {
      if (this.skipped) return;
      await this.enterBeat(beat);
      if (this.skipped) return;
      if (beat.lines?.length) {
        const box = new DialogueBox(this, this.sfx);
        this.activeBox = box;
        await box.run(beat.lines.map((text) => ({ text, style: 'narrate' as const })));
        this.activeBox = undefined;
      } else if (beat.dwellMs) {
        await this.wait(beat.dwellMs);
      }
    }
    if (!this.skipped) this.finish();
  }

  /** Cross-dissolve to the beat's panel, swap the music bed, fire any punctuation. */
  private async enterBeat(beat: CinematicBeat): Promise<void> {
    // Music change runs concurrently so the panel never stalls behind a fade.
    if (beat.music !== undefined) {
      if (beat.music === null) void this.music.fadeToSilence(600);
      else if (this.music.playingKey) void this.music.crossfade(beat.music, MUSIC_URL(beat.music), theme.cinematic.crossfadeMs);
      else void this.music.play(beat.music, MUSIC_URL(beat.music));
    }
    if (beat.panel) await this.showPanel(beat.panel);
    if (this.skipped) return;
    // Punctuation lands on the freshly revealed panel.
    if (beat.sfx) void this.sfx.play(beat.sfx);
    if (beat.fx === 'flash') void flash(this, 260);
    else if (beat.fx === 'shake') void shake(this, 260, 0.006);
  }

  /** Reveal a panel with a cross-dissolve; gracefully no-ops to the starfield if missing. */
  private async showPanel(path: string): Promise<void> {
    const ok = this.textures.exists(path) || (await loadImage(this, path, path));
    const old = this.currentPanel;
    if (!ok) {
      if (old) this.dissolveOut(old);
      this.currentPanel = undefined;
      return;
    }
    const img = this.add.image(GAME_WIDTH / 2, GAME_HEIGHT / 2, path).setOrigin(0.5).setAlpha(0).setDepth(1);
    img.setDisplaySize(GAME_WIDTH, GAME_HEIGHT);
    this.currentPanel = img;
    await new Promise<void>((resolve) => {
      this.tweens.add({ targets: img, alpha: 1, duration: theme.cinematic.dissolveMs, ease: 'Sine.inOut', onComplete: () => resolve() });
      if (old) this.dissolveOut(old);
    });
  }

  private dissolveOut(img: Phaser.GameObjects.Image): void {
    this.tweens.add({ targets: img, alpha: 0, duration: theme.cinematic.dissolveMs, ease: 'Sine.inOut', onComplete: () => img.destroy() });
  }

  /** A loose constellation behind the panels — the always-present fallback ambiance. */
  private drawStarfield(): void {
    for (let i = 0; i < 28; i++) {
      const x = Phaser.Math.Between(6, GAME_WIDTH - 6);
      const y = Phaser.Math.Between(6, GAME_HEIGHT - 6);
      const big = Math.random() < 0.25;
      const star = this.add.circle(x, y, big ? 1.6 : 1, hex(COLORS.diamond), big ? 0.9 : 0.5).setDepth(0);
      this.tweens.add({
        targets: star,
        alpha: big ? 0.4 : 0.2,
        duration: Phaser.Math.Between(1400, 2800),
        delay: Phaser.Math.Between(0, 1200),
        yoyo: true,
        repeat: -1,
        ease: 'Sine.inOut',
      });
    }
  }

  private wait(ms: number): Promise<void> {
    return new Promise((resolve) => this.time.delayedCall(ms, () => resolve()));
  }

  private finish(): void {
    if (this.finished) return;
    this.finished = true;
    this.skipInput?.destroy();
    this.skipInput = undefined;
    this.activeBox?.destroy(); // tear down a mid-page narration box on skip
    this.activeBox = undefined;
    void this.music.fadeToSilence(theme.transition.fadeMs);
    this.cameras.main.fadeOut(theme.transition.fadeMs, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.music.stop();
      this.scene.start(this.next.scene, this.next.data as object | undefined);
    });
  }
}
