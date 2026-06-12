/**
 * WorldMapMenu — the vesperlamp's chart of Vesperholm (pause menu -> MAP).
 *
 * The classic handheld "town map": the whole region drawn schematically — the
 * ring of valleys around the Umbral Spire, towns/routes/dungeon mouths as
 * swatches, walked roads solid, gated passages and cave passes dashed, the
 * Lanternway spokes as warm dashed lanes — with a blinking you-are-here marker
 * on the player's current area. D-pad hops the cursor between places (a detail
 * strip below names the selection); B or A backs out. Read-only and
 * promise-based, built from the shared kit + theme tokens. The layout itself is
 * data: `data/world/worldmap.json`, generated and geometry-checked by
 * `tools/maps/world_layout.py`.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { WORLD_MAP, WORLD_MAP_BOX, worldMapNodeForMap } from '@game/data/world/worldmap';
import type { WorldMapNode } from '@game/data/world/worldmap';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
const HEADER_H = 10;
const STRIP_H = 12;

/** Node swatch size (screen px) by kind — towns read bigger than landmarks. */
const NODE_SIZE: Record<string, [number, number]> = {
  town: [14, 9],
  hub: [13, 10],
  route: [11, 7],
  dungeon: [11, 8],
  landmark: [5, 5],
};

const REGION_LABEL: Record<string, string> = {
  south: 'SOUTH VALE',
  east: 'EASTERN FENS',
  north: 'HIGH NORTH',
  west: 'WESTERN REACH',
  central: 'THE CENTRE',
  outer: 'THE OUTER WAYS',
};

export class WorldMapMenu {
  private readonly panel: Panel;
  private readonly strip: Phaser.GameObjects.Text;
  private readonly select: Phaser.GameObjects.Rectangle;
  private readonly nodes: WorldMapNode[];
  private readonly playerNode?: WorldMapNode;
  private index: number;
  private blink?: Phaser.Tweens.Tween;

  constructor(
    private readonly scene: Phaser.Scene,
    currentMapId: string,
    private readonly sfx?: Sfx,
  ) {
    this.nodes = WORLD_MAP.nodes;
    this.playerNode = worldMapNodeForMap(currentMapId);
    this.index = Math.max(0, this.nodes.findIndex((n) => n.id === this.playerNode?.id));

    const width = GAME_WIDTH - 8;
    const height = GAME_HEIGHT - 8;
    this.panel = new Panel(scene, 4, 4, width, height).fixedToCamera().setDepth(theme.depth.panel);
    this.panel.add(makeText(scene, PAD, PAD - 2, 'VESPERHOLM', theme.text.accent));
    this.panel.add(makeText(scene, width - PAD, PAD - 2, 'B BACK', theme.text.dim).setOrigin(1, 0));

    // Map viewport: fit the layout's virtual box, centred.
    const viewX = PAD;
    const viewY = PAD + HEADER_H;
    const viewW = width - PAD * 2;
    const viewH = height - viewY - STRIP_H - PAD;
    const scale = Math.min(viewW / WORLD_MAP_BOX.width, viewH / WORLD_MAP_BOX.height);
    const offX = viewX + (viewW - WORLD_MAP_BOX.width * scale) / 2;
    const offY = viewY + (viewH - WORLD_MAP_BOX.height * scale) / 2;
    const px = (n: WorldMapNode): [number, number] => [offX + n.x * scale, offY + n.y * scale];

    // Roads first (under the nodes). Dashes are drawn as short segments.
    const g = scene.add.graphics();
    const byId = new Map(this.nodes.map((n) => [n.id, n]));
    for (const road of WORLD_MAP.roads) {
      const a = byId.get(road.a);
      const b = byId.get(road.b);
      if (!a || !b) continue;
      const [ax, ay] = px(a);
      const [bx, by] = px(b);
      if (road.kind === 'road') {
        g.lineStyle(1, hex(theme.worldmap.road), 0.9);
        g.lineBetween(ax, ay, bx, by);
      } else {
        const color =
          road.kind === 'lane' ? theme.worldmap.lane : road.kind === 'pass' ? theme.worldmap.pass : theme.worldmap.gate;
        g.lineStyle(1, hex(color), road.kind === 'lane' ? 0.9 : 0.7);
        const len = Phaser.Math.Distance.Between(ax, ay, bx, by);
        const steps = Math.max(1, Math.floor(len / 4));
        for (let i = 0; i < steps; i += 2) {
          g.lineBetween(
            ax + ((bx - ax) * i) / steps,
            ay + ((by - ay) * i) / steps,
            ax + ((bx - ax) * (i + 1)) / steps,
            ay + ((by - ay) * (i + 1)) / steps,
          );
        }
      }
    }
    // Node swatches on top.
    for (const node of this.nodes) {
      const [w, h] = NODE_SIZE[node.kind] ?? NODE_SIZE.landmark;
      const [cx, cy] = px(node);
      g.fillStyle(hex(theme.worldmap.node[node.kind] ?? theme.worldmap.node.landmark), 1);
      g.fillRect(Math.round(cx - w / 2), Math.round(cy - h / 2), w, h);
    }
    this.panel.add(g);

    // The blinking you-are-here marker.
    if (this.playerNode) {
      const [w, h] = NODE_SIZE[this.playerNode.kind] ?? NODE_SIZE.landmark;
      const [cx, cy] = px(this.playerNode);
      const marker = scene.add
        .rectangle(Math.round(cx), Math.round(cy), w + 4, h + 4)
        .setStrokeStyle(1, hex(theme.worldmap.marker));
      this.panel.add(marker);
      this.blink = scene.tweens.add({ targets: marker, alpha: 0.15, duration: 420, yoyo: true, repeat: -1 });
    }

    // The selection outline + the name strip.
    this.select = scene.add.rectangle(0, 0, 10, 10).setStrokeStyle(1, hex(theme.color.panelEdge));
    this.panel.add(this.select);
    this.strip = makeText(scene, PAD, height - STRIP_H - 1, '', theme.text.base);
    this.panel.add(this.strip);
    this.toScreen = px;
    this.refresh();
  }

  private toScreen: (n: WorldMapNode) => [number, number];

  private refresh(): void {
    const node = this.nodes[this.index];
    const [w, h] = NODE_SIZE[node.kind] ?? NODE_SIZE.landmark;
    const [cx, cy] = this.toScreen(node);
    this.select.setPosition(Math.round(cx), Math.round(cy)).setSize(w + 2, h + 2);
    const here = node.id === this.playerNode?.id ? '  *HERE*' : '';
    const region = REGION_LABEL[node.region] ?? node.region.toUpperCase();
    this.strip.setText(`${node.name.toUpperCase()} — ${region}${here}`);
  }

  /** Hop the cursor to the nearest node in the pressed direction. */
  private move(dx: number, dy: number): void {
    const from = this.nodes[this.index];
    let best = -1;
    let bestScore = Infinity;
    this.nodes.forEach((n, i) => {
      if (i === this.index) return;
      const vx = n.x - from.x;
      const vy = n.y - from.y;
      const along = vx * dx + vy * dy; // progress in the pressed direction
      if (along <= 0) return;
      const perp = Math.abs(vx * dy) + Math.abs(vy * dx); // lateral drift
      const score = along + perp * 2;
      if (score < bestScore) {
        bestScore = score;
        best = i;
      }
    });
    if (best >= 0) {
      this.index = best;
      this.refresh();
      void this.sfx?.play(theme.cursor.moveSfx);
    }
  }

  /** Show the chart; resolve when the player backs out. */
  run(): Promise<void> {
    const input = new InputController(this.scene);
    let armed = false; // ignore the press that opened this screen until released
    return new Promise((resolve) => {
      const tick = (): void => {
        input.update();
        if (!armed) {
          if (!input.isDown(InputAction.Confirm) && !input.isDown(InputAction.Cancel)) armed = true;
          return;
        }
        if (input.justPressed(InputAction.Up)) this.move(0, -1);
        else if (input.justPressed(InputAction.Down)) this.move(0, 1);
        else if (input.justPressed(InputAction.Left)) this.move(-1, 0);
        else if (input.justPressed(InputAction.Right)) this.move(1, 0);
        else if (input.justPressed(InputAction.Cancel) || input.justPressed(InputAction.Confirm)) {
          void this.sfx?.play(theme.cursor.cancelSfx);
          this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
          input.destroy();
          this.destroy();
          resolve();
        }
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  destroy(): void {
    this.blink?.remove();
    this.panel.destroy();
  }
}
