/**
 * Panel — the framed box every PixelKin screen is built from (dialogue, menus,
 * popups). One look, defined once: a 9-slice frame whose texture is generated at
 * runtime from theme tokens, so there's no art dependency and the frame stays
 * consistent everywhere. Build a screen by making a Panel and adding themed Text /
 * Menu / Cursor into it.
 */
import Phaser from 'phaser';
import { theme, hex } from './theme';

/** Create the shared frame texture once (deepBlue fill, 1px diamond edge). */
export function ensurePanelTexture(scene: Phaser.Scene): void {
  const key = theme.panel.texture;
  if (scene.textures.exists(key)) return;

  const s = theme.panel.slice;
  const w = s.left + s.right + 2; // small middle so the 9-slice has stretch room
  const h = s.top + s.bottom + 2;

  const g = scene.add.graphics();
  g.fillStyle(hex(theme.color.panelFill), 1);
  g.fillRect(0, 0, w, h);
  // 1px bright edge
  g.lineStyle(theme.panel.borderPx, hex(theme.color.panelEdge), 1);
  g.strokeRect(0.5, 0.5, w - 1, h - 1);
  // subtle inner shadow line for depth
  g.lineStyle(theme.panel.borderPx, hex(theme.color.panelShadow), 0.5);
  g.strokeRect(1.5, 1.5, w - 3, h - 3);
  g.generateTexture(key, w, h);
  g.destroy();
}

export class Panel {
  readonly container: Phaser.GameObjects.Container;
  readonly bg: Phaser.GameObjects.NineSlice;

  constructor(scene: Phaser.Scene, x: number, y: number, width: number, height: number) {
    ensurePanelTexture(scene);
    const s = theme.panel.slice;
    this.bg = scene.add
      .nineslice(0, 0, theme.panel.texture, undefined, width, height, s.left, s.right, s.top, s.bottom)
      .setOrigin(0, 0);
    this.container = scene.add.container(x, y, [this.bg]).setDepth(theme.depth.panel);
  }

  get width(): number {
    return this.bg.width;
  }
  get height(): number {
    return this.bg.height;
  }

  /** Add a child (positioned relative to the panel's top-left). */
  add(obj: Phaser.GameObjects.GameObject): void {
    this.container.add(obj);
  }

  /** Pin to the camera (for HUD / modal use). */
  fixedToCamera(): this {
    this.container.setScrollFactor(0);
    return this;
  }

  setDepth(depth: number): this {
    this.container.setDepth(depth);
    return this;
  }

  setVisible(v: boolean): this {
    this.container.setVisible(v);
    return this;
  }

  destroy(): void {
    this.container.destroy();
  }
}
