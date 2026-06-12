/**
 * The PixelKin design language — "Tailwind for the game".
 *
 * This file is the SINGLE SOURCE OF TRUTH for how every in-game screen looks and
 * behaves: panels, menus, dialogue boxes, popups, cursors, transitions. Build UI
 * from the components in this folder (Panel, Text, Menu, DialogueBox, Cursor) and
 * they all read these tokens, so the whole game stays visually consistent as it
 * grows. Never hard-code a colour, font, or spacing value in a screen — add or
 * reuse a token here instead.
 *
 * Everything is sized for the fixed 240x160 internal resolution (see
 * `@game/config`). Spacing values are in *source* pixels.
 */
import Phaser from 'phaser';
import { COLORS } from '@game/config';
import type { KinType } from '@game/data/dex';

/** The bundled pixel font's CSS family name (see global.css @font-face). */
export const FONT_FAMILY = 'PixelKin';

export const theme = {
  /** Semantic colour tokens layered over the raw brand palette in config.ts. */
  color: {
    panelFill: COLORS.deepBlue,
    panelEdge: COLORS.diamond,
    panelShadow: COLORS.night,
    text: COLORS.bone,
    textDim: '#b9b3c9',
    textAccent: COLORS.diamond,
    selected: COLORS.fire,
    danger: COLORS.fire,
    overlay: 'rgba(11, 16, 38, 0.62)', // dim the world behind modal UI
    /** HP bar fill by remaining ratio (high > 50% > mid > 20% > low). */
    hpHigh: COLORS.grass,
    hpMid: COLORS.fire,
    hpLow: '#ff5a5a',
  },

  /** Per-type accent colours for swatches/tags (the 8 elements + Light/Dark). */
  typeColor: {
    Ember: '#ff8a3d',
    Tide: '#4fb4ff',
    Verdant: '#7bdc6b',
    Stone: '#c9a86a',
    Storm: '#b9a6ff',
    Frost: '#a9e8ff',
    Solar: '#ffd76b',
    Lunar: '#8aa0ff',
    Light: '#fff3c0',
    Dark: '#6b6480',
  } as Record<KinType, string>,

  /** Spacing scale in source pixels — keep layouts on this grid. */
  space: { xs: 1, sm: 2, md: 4, lg: 6, xl: 8, xxl: 12 },

  /** 9-slice corner inset for the framed panel texture. */
  radius: { panel: 4 },

  /** Text styles. Press Start 2P is an 8px-grid font: use 8 / 16 for crispness. */
  text: {
    base: { fontFamily: FONT_FAMILY, fontSize: '8px', color: COLORS.bone },
    dim: { fontFamily: FONT_FAMILY, fontSize: '8px', color: '#b9b3c9' },
    accent: { fontFamily: FONT_FAMILY, fontSize: '8px', color: COLORS.diamond },
    title: { fontFamily: FONT_FAMILY, fontSize: '16px', color: COLORS.diamond },
    small: { fontFamily: FONT_FAMILY, fontSize: '8px', color: COLORS.bone },
    /** Un-attributed narration / cold-open prose — soft, no speaker, set apart. */
    narrate: { fontFamily: FONT_FAMILY, fontSize: '8px', color: '#d8d2e8' },
  },

  /** Dialogue typewriter speeds, characters per second. Hold confirm = fast.
   *  `narrateCps` is deliberately slower so narration reads with weight. */
  typewriter: { cps: 32, fastCps: 120, narrateCps: 22 },

  /** Character-portrait bust in the dialogue box (a 32×32 frame, top-left). */
  portrait: { size: 32, inset: 2, gap: 4 },

  /** Cinematic / cutscene presentation timings (ms). */
  cinematic: { dissolveMs: 900, letterboxMs: 320, holdMs: 700, crossfadeMs: 700 },

  /** The pointing cursor's look + the sfx keys it plays. */
  cursor: {
    blinkMs: 420,
    moveSfx: 'ui-cursor',
    confirmSfx: 'ui-confirm',
    cancelSfx: 'ui-cancel',
  },

  /** The framed-panel texture (generated at runtime — see Panel.ts) + slice. */
  panel: {
    /** Texture key created once by ensurePanelTexture(). */
    texture: 'ui_frame',
    slice: { left: 4, right: 4, top: 4, bottom: 4 },
    borderPx: 1,
  },

  /** Standard transition timings (ms). */
  transition: { fadeMs: 300, doorMs: 350, swooshMs: 420 },

  /** Depth bands so on-canvas UI always sits above the world. The cinematic
   *  tint wash sits in the dim band; letterbox bars frame just under the panel
   *  so the dialogue box still reads over the lower bar. */
  depth: {
    world: 0,
    /** The Lamplight reveal mask on dark maps — above the world and actors,
     *  below every UI/cinematic band (it's diegetic darkness, not chrome). */
    lamplight: 800,
    tint: 905,
    overlayDim: 900,
    letterbox: 950,
    panel: 1000,
    text: 1010,
    cursor: 1020,
    toast: 1100,
  },
} as const;

/** Convert a '#rrggbb' string to the 0xRRGGBB number Phaser graphics want. */
export function hex(color: string): number {
  return Phaser.Display.Color.HexStringToColor(color).color;
}
