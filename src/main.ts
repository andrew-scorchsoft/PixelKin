import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, COLORS, RENDER_SCALE } from '@game/config';
import { BootScene } from '@game/scenes/BootScene';
import { PreloadScene } from '@game/scenes/PreloadScene';
import { TitleScene } from '@game/scenes/TitleScene';
import { AttractScene } from '@game/scenes/AttractScene';
import { WorldScene } from '@game/scenes/WorldScene';
import { BattleScene } from '@game/scenes/BattleScene';

/**
 * Game entry point. Boots Phaser at a fixed handheld-era internal resolution
 * and scales it up to fill whatever screen it lands on — desktop browser today,
 * a Capacitor mobile webview tomorrow. `pixelArt: true` forces nearest-neighbour
 * sampling so the world art stays crisp and chunky.
 *
 * `scale.zoom: RENDER_SCALE` renders the 240x160 game into a higher-resolution
 * framebuffer (the world art is still nearest-sampled, so it reads identically —
 * just at more device pixels). That gives the in-canvas pixel font real pixels to
 * render into, so text is crisp rather than a 240x160 bitmap stretched by the
 * upscale. Game coordinates remain 240x160 (see config.ts).
 */
const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  parent: 'game-root',
  width: GAME_WIDTH,
  height: GAME_HEIGHT,
  backgroundColor: COLORS.night,
  pixelArt: true,
  roundPixels: true,
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
    zoom: RENDER_SCALE,
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { x: 0, y: 0 }, debug: false },
  },
  input: {
    // Both matter for a web-first / mobile-future game: keyboard for desktop,
    // pointer (touch) for handheld. On-screen controls come later.
    keyboard: true,
    touch: true,
  },
  scene: [BootScene, PreloadScene, AttractScene, TitleScene, WorldScene, BattleScene],
};

new Phaser.Game(config);

// Mount the device/overlay/plain shell chrome around the canvas (DOM, outside the
// 240x160 game). Reads the saved view preference; its on-screen controls dispatch
// the same abstract input the keyboard does (see InputController).
import { ShellManager } from '@/shell/ShellManager';
void ShellManager.init();
