import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, COLORS } from '@game/config';
import { allBattleBackdrops } from '@game/data/world/maps';
import trainerManifest from '../../../public/assets/sprites/trainers/trainers.manifest.json';
import objectManifest from '../../../public/assets/sprites/objects/objects.manifest.json';
import {
  creatureSpritePath,
  creatureTextureKey,
  type CreatureView,
} from '@game/systems/sprites/CreatureSprites';
import { ACTIONS_KEY_SUFFIX, EMOTE_TEXTURE } from '@game/entities/Actor';
import { ARENA_LAYER_PATHS } from './AttractScene';

interface SheetEntry {
  path: string;
  width: number;
  height: number;
  cols?: number;
  rows?: number;
}
interface TrainerManifest {
  frame_width: number;
  frame_height: number;
  trainers: Record<string, SheetEntry & { actions?: SheetEntry }>;
  /** One shared emote/bubble sheet, popped above any character (Actor.showEmote). */
  emotes?: SheetEntry;
}

/**
 * Loads the game's assets behind a progress bar. Right now there is almost
 * nothing to load — as sprites, tilesets, maps, music and sfx land in
 * public/assets/, queue them here and the progress bar handles the rest.
 */
export class PreloadScene extends Phaser.Scene {
  constructor() {
    super('Preload');
  }

  preload(): void {
    this.drawLoadingUi();

    // --- Queue real assets here as they arrive, e.g.: ---
    // this.load.spritesheet('player', 'assets/sprites/player.png', { frameWidth: 16, frameHeight: 24 });
    // this.load.tilemapTiledJSON('town', 'assets/maps/town.json');
    // this.load.audio('overworld', 'assets/audio/music/overworld.mp3');

    // Battle music — lush SNES-era dusk themes. 'dusk-duel' is the default
    // wild-encounter theme; emberfall/nightfall/veil are interchangeable
    // siblings to rotate per encounter so random battles stay fresh. Each is a
    // seamless loop, so play with `{ loop: true }`.
    this.load.audio('battle-dusk-duel', 'assets/audio/music/battle-main-dusk-duel.mp3');
    this.load.audio('battle-emberfall', 'assets/audio/music/battle-emberfall.mp3');
    this.load.audio('battle-nightfall', 'assets/audio/music/battle-nightfall.mp3');
    this.load.audio('battle-veil', 'assets/audio/music/battle-veil.mp3');
    // Boss / hard-opponent theme — grander, with a key-lifting climax.
    this.load.audio('battle-boss-eclipse', 'assets/audio/music/battle-boss-eclipse.mp3');

    // The two starters the attract-mode trailer pits against each other (the
    // pair on the logo): Vulpyre's back view (player side) vs Brinix's front
    // (foe side). Preloaded so the demo battle shows real kin from frame one
    // instead of popping in mid-loop.
    const FEATURED: ReadonlyArray<[number, CreatureView]> = [
      [1, 'back'],
      [2, 'front'],
    ];
    for (const [id, v] of FEATURED) {
      const path = creatureSpritePath(id, v);
      if (path) this.load.image(creatureTextureKey(id, v), path);
    }

    // Parallax arena layers behind the attract-mode duel — seamless mirror
    // strips scrolled at different speeds for a slow "orbit the arena" depth.
    // Keyed by their asset path (same convention as battle backdrops).
    for (const path of ARENA_LAYER_PATHS) {
      this.load.image(path, path);
    }

    // Per-map battle backdrops (240x160 WebP). Keyed by their asset path so the
    // BattleScene can add the chosen variant with no further loading. Maps without
    // a backdrop fall back to the plain night fill. See data/world/maps.ts.
    for (const path of allBattleBackdrops()) {
      this.load.image(path, path);
    }

    // Human walk-sheets (player + named NPCs), packed by pack_trainers.py. Keyed
    // by master stem; Player/Npc load them by that key and fall back to a runtime
    // placeholder if one is missing. Adding a trainer = re-pack, no code change.
    const trainers = trainerManifest as TrainerManifest;
    const frame = { frameWidth: trainers.frame_width, frameHeight: trainers.frame_height };
    for (const [key, t] of Object.entries(trainers.trainers)) {
      this.load.spritesheet(key, t.path, frame);
      // Optional layer-3 action sheet (raise-lamp/toss/gift/sit/hurt), keyed
      // `<key>_actions` — same 32×32 frame, fewer cells. Actor swaps to it for
      // one-shot event poses (see entities/Actor.ts).
      if (t.actions) this.load.spritesheet(`${key}${ACTIONS_KEY_SUFFIX}`, t.actions.path, frame);
    }
    // Layer-2 shared emote sheet — one texture, popped above any character.
    if (trainers.emotes) this.load.spritesheet(EMOTE_TEXTURE, trainers.emotes.path, frame);

    // Whole-structure object sprites (buildings, big trees, lamps), packed by
    // pack_objects.py. Loaded as plain images keyed by name; MapRenderer places
    // them per the map's `objects`, falling back to none if a key is missing.
    const objects = objectManifest as { objects: Record<string, { path: string }> };
    for (const [key, o] of Object.entries(objects.objects)) {
      this.load.image(key, o.path);
    }
  }

  create(): void {
    // Open on the studio splash: it doubles as the audio gate — its first gesture
    // unlocks the Web Audio context (browsers block sound until then), so the
    // attract demo it hands off to plays its battle music from frame one.
    this.scene.start('Splash');
  }

  private drawLoadingUi(): void {
    const cx = GAME_WIDTH / 2;
    const cy = GAME_HEIGHT / 2;

    const logo = this.add.image(cx, cy - 18, 'logo').setOrigin(0.5);
    const maxLogoWidth = GAME_WIDTH - 48;
    if (logo.width > maxLogoWidth) {
      logo.setScale(maxLogoWidth / logo.width);
    }

    const barWidth = GAME_WIDTH - 80;
    const barHeight = 6;
    const barX = cx - barWidth / 2;
    const barY = cy + 40;

    const frame = this.add.graphics();
    frame.lineStyle(1, Phaser.Display.Color.HexStringToColor(COLORS.diamond).color, 1);
    frame.strokeRect(barX - 1, barY - 1, barWidth + 2, barHeight + 2);

    const fill = this.add.graphics();
    this.load.on('progress', (value: number) => {
      fill.clear();
      fill.fillStyle(Phaser.Display.Color.HexStringToColor(COLORS.diamond).color, 1);
      fill.fillRect(barX, barY, barWidth * value, barHeight);
    });
  }
}
