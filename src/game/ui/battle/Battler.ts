/**
 * Battler — the on-screen representation of one combatant.
 *
 * No real creature sprites are packed yet (the battle_front/back masters under
 * assets/creatures/ are NOT served), so we draw a PLACEHOLDER: a rounded panel
 * tinted by the kin's primary type, with its name. The texture key is chosen by
 * `battlerTexture(species, side)`, which currently always returns a generated
 * placeholder key — swapping in a real loaded sprite later is a one-line change
 * (return the packed texture key once it exists).
 */
import Phaser from 'phaser';
import { theme, hex } from '@game/ui/theme';
import { makeText } from '@game/ui/Text';
import type { Species, KinType } from '@game/data/dex';

/** A type → colour map for the placeholder battlers (themed, original palette). */
const TYPE_COLOR: Record<KinType, number> = {
  Ember: 0xff8a3d,
  Tide: 0x4fb4ff,
  Verdant: 0x7bdc6b,
  Stone: 0xc8a06a,
  Storm: 0xc9b8ff,
  Frost: 0x9fe7ff,
  Solar: 0xffd86b,
  Lunar: 0x8f7bd8,
  Light: 0xfff4c2,
  Dark: 0x6a5a8a,
};

/**
 * Texture key for a combatant. Today: a generated placeholder rectangle keyed by
 * type + side. Later: detect a packed sprite (e.g. `creature_${species.id}_front`)
 * and return that instead — the rest of the battle UI is unaffected.
 */
export function battlerTexture(scene: Phaser.Scene, species: Species, side: 'player' | 'foe'): string {
  const color = TYPE_COLOR[species.types[0]] ?? hex(theme.color.panelEdge);
  const key = `battler_ph_${species.types[0]}_${side}`;
  if (!scene.textures.exists(key)) {
    const w = 40;
    const h = 40;
    const g = scene.add.graphics();
    g.fillStyle(color, 1);
    g.fillRoundedRect(0, 0, w, h, 6);
    g.lineStyle(1, hex(theme.color.panelShadow), 0.8);
    g.strokeRoundedRect(0.5, 0.5, w - 1, h - 1, 6);
    g.generateTexture(key, w, h);
    g.destroy();
  }
  return key;
}

export class Battler {
  readonly container: Phaser.GameObjects.Container;
  readonly sprite: Phaser.GameObjects.Image;

  constructor(
    scene: Phaser.Scene,
    x: number,
    y: number,
    species: Species,
    side: 'player' | 'foe',
  ) {
    this.sprite = scene.add.image(0, 0, battlerTexture(scene, species, side)).setOrigin(0.5);
    const label = makeText(scene, 0, side === 'foe' ? -28 : 26, species.name, theme.text.dim).setOrigin(0.5);
    this.container = scene.add
      .container(x, y, [this.sprite, label])
      .setDepth(theme.depth.world + 5)
      .setScrollFactor(0);
  }

  /** Swap to a different species' placeholder (used when the active kin changes). */
  setSpecies(scene: Phaser.Scene, species: Species, side: 'player' | 'foe'): void {
    this.sprite.setTexture(battlerTexture(scene, species, side));
    const label = this.container.list[1] as Phaser.GameObjects.Text | undefined;
    label?.setText(species.name);
  }

  /** A small hop/shake when the kin acts or is hit. */
  nudge(scene: Phaser.Scene, dx: number): void {
    scene.tweens.add({
      targets: this.container,
      x: this.container.x + dx,
      duration: 60,
      yoyo: true,
      ease: 'Sine.inOut',
    });
  }

  flashHit(scene: Phaser.Scene): void {
    scene.tweens.add({ targets: this.sprite, alpha: 0.3, duration: 60, yoyo: true, repeat: 2 });
  }

  fall(scene: Phaser.Scene): Promise<void> {
    return new Promise((resolve) => {
      scene.tweens.add({
        targets: this.container,
        y: this.container.y + 16,
        alpha: 0,
        duration: 320,
        ease: 'Quad.in',
        onComplete: () => resolve(),
      });
    });
  }

  destroy(): void {
    this.container.destroy();
  }
}
