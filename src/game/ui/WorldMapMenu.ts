/**
 * WorldMapMenu — the vesperlamp's chart of Vesperholm (pause menu -> MAP).
 *
 * The classic handheld "town map", drawn HONESTLY north-up (2026-10): every
 * place sits where it really is as walked — leave a map north and the next one
 * is north on the chart. Towns/routes/dungeon mouths as swatches, walked roads
 * solid, gated passages and cave passes dashed, the Lanternway lanes warm
 * dashed, the Lantern-car lines sky-blue dotted. The world is tall, so the
 * chart fits the width and scrolls with the cursor — with a blinking you-are-here marker
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
  outer: 'OUTER WAYS',
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

    // Map viewport. The honest north-up world is TALL (the long climb north),
    // so the chart fits the WIDTH and scrolls vertically with the cursor — the
    // classic scrolling region map. Everything is redrawn, clipped to the view,
    // whenever it scrolls (no masks needed).
    this.viewX = PAD;
    this.viewY = PAD + HEADER_H;
    this.viewW = width - PAD * 2;
    this.viewH = height - this.viewY - STRIP_H - PAD;
    this.scale = this.viewW / WORLD_MAP_BOX.width;
    this.offX = this.viewX + (this.viewW - WORLD_MAP_BOX.width * this.scale) / 2;
    this.maxScroll = Math.max(0, Math.round(WORLD_MAP_BOX.height * this.scale - this.viewH));

    this.g = scene.add.graphics();
    this.panel.add(this.g);
    // The blinking you-are-here marker.
    if (this.playerNode) {
      const [w, h] = NODE_SIZE[this.playerNode.kind] ?? NODE_SIZE.landmark;
      this.marker = scene.add.rectangle(0, 0, w + 4, h + 4).setStrokeStyle(1, hex(theme.worldmap.marker));
      this.panel.add(this.marker);
      this.blink = scene.tweens.add({ targets: this.marker, alpha: 0.15, duration: 420, yoyo: true, repeat: -1 });
    }
    // The selection outline, the scroll hints + the name strip.
    this.select = scene.add.rectangle(0, 0, 10, 10).setStrokeStyle(1, hex(theme.color.panelEdge));
    this.panel.add(this.select);
    // scroll hints ride the header row (never over a place on the chart)
    this.upHint = makeText(scene, width / 2 - 2, PAD - 2, '\u25b2', theme.text.dim).setOrigin(1, 0);
    this.downHint = makeText(scene, width / 2 + 2, PAD - 2, '\u25bc', theme.text.dim).setOrigin(0, 0);
    this.panel.add(this.upHint);
    this.panel.add(this.downHint);
    this.strip = makeText(scene, PAD, height - STRIP_H - 1, '', theme.text.base);
    this.panel.add(this.strip);
    this.refresh();
  }

  private readonly viewX: number;
  private readonly viewY: number;
  private readonly viewW: number;
  private readonly viewH: number;
  private readonly scale: number;
  private readonly offX: number;
  private readonly maxScroll: number;
  private scrollY = -1;
  private readonly g: Phaser.GameObjects.Graphics;
  private marker?: Phaser.GameObjects.Rectangle;
  private readonly upHint: Phaser.GameObjects.Text;
  private readonly downHint: Phaser.GameObjects.Text;

  private toScreen(n: WorldMapNode): [number, number] {
    return [this.offX + n.x * this.scale, this.viewY + n.y * this.scale - this.scrollY];
  }

  /** Redraw roads + nodes for the current scroll, clipped to the view. */
  private draw(): void {
    const g = this.g;
    g.clear();
    const top = this.viewY;
    const bottom = this.viewY + this.viewH;
    const byId = new Map(this.nodes.map((n) => [n.id, n]));
    // a segment clipped to the view's rows (x always fits: the chart fits the width)
    const seg = (ax: number, ay: number, bx: number, by: number): void => {
      let t0 = 0;
      let t1 = 1;
      const dy = by - ay;
      if (dy === 0) {
        if (ay < top || ay > bottom) return;
      } else {
        const ta = (top - ay) / dy;
        const tb = (bottom - ay) / dy;
        t0 = Math.max(t0, Math.min(ta, tb));
        t1 = Math.min(t1, Math.max(ta, tb));
        if (t0 > t1) return;
      }
      g.lineBetween(ax + (bx - ax) * t0, ay + dy * t0, ax + (bx - ax) * t1, ay + dy * t1);
    };
    for (const road of WORLD_MAP.roads) {
      const a = byId.get(road.a);
      const b = byId.get(road.b);
      if (!a || !b) continue;
      const [ax, ay] = this.toScreen(a);
      const [bx, by] = this.toScreen(b);
      if (road.kind === 'road') {
        g.lineStyle(1, hex(theme.worldmap.road), 0.9);
        seg(ax, ay, bx, by);
      } else {
        const color =
          road.kind === 'lane' ? theme.worldmap.lane
            : road.kind === 'pass' ? theme.worldmap.pass
              : road.kind === 'car' ? theme.worldmap.car : theme.worldmap.gate;
        g.lineStyle(1, hex(color), road.kind === 'lane' || road.kind === 'car' ? 0.9 : 0.7);
        const len = Phaser.Math.Distance.Between(ax, ay, bx, by);
        const steps = Math.max(1, Math.floor(len / (road.kind === 'car' ? 3 : 4)));
        for (let i = 0; i < steps; i += 2) {
          seg(
            ax + ((bx - ax) * i) / steps,
            ay + ((by - ay) * i) / steps,
            ax + ((bx - ax) * (i + 1)) / steps,
            ay + ((by - ay) * (i + 1)) / steps,
          );
        }
      }
    }
    for (const node of this.nodes) {
      const [w, h] = NODE_SIZE[node.kind] ?? NODE_SIZE.landmark;
      const [cx, cy] = this.toScreen(node);
      if (cy - h / 2 < top || cy + h / 2 > bottom) continue;
      g.fillStyle(hex(theme.worldmap.node[node.kind] ?? theme.worldmap.node.landmark), 1);
      g.fillRect(Math.round(cx - w / 2), Math.round(cy - h / 2), w, h);
    }
    if (this.marker && this.playerNode) {
      const [cx, cy] = this.toScreen(this.playerNode);
      this.marker.setPosition(Math.round(cx), Math.round(cy));
      const [, mh] = NODE_SIZE[this.playerNode.kind] ?? NODE_SIZE.landmark;
      // the same fit test as the swatches (the marker is 2px proud of it)
      this.marker.setVisible(cy - mh / 2 - 2 >= top && cy + mh / 2 + 2 <= bottom);
    }
    this.upHint.setVisible(this.scrollY > 0);
    this.downHint.setVisible(this.scrollY < this.maxScroll);
  }

  private refresh(): void {
    const node = this.nodes[this.index];
    // keep the cursor's node comfortably inside the view (scroll in steps)
    const ny = node.y * this.scale;
    const margin = Math.min(24, this.viewH / 3);
    let want = this.scrollY < 0 ? ny - this.viewH / 2 : this.scrollY;
    if (ny - want < margin) want = ny - margin;
    if (ny - want > this.viewH - margin) want = ny - (this.viewH - margin);
    want = Math.round(Phaser.Math.Clamp(want, 0, this.maxScroll));
    if (want !== this.scrollY) {
      this.scrollY = want;
      this.draw();
    }
    const [w, h] = NODE_SIZE[node.kind] ?? NODE_SIZE.landmark;
    const [cx, cy] = this.toScreen(node);
    this.select.setPosition(Math.round(cx), Math.round(cy)).setSize(w + 2, h + 2);
    const here = node.id === this.playerNode?.id ? '  *HERE*' : '';
    const region = REGION_LABEL[node.region] ?? node.region.toUpperCase();
    // Fit the strip inside the panel: drop the region first, then ellipsize
    // the name (long names like "Lanternway · Tinderwick Spoke" overran it).
    const maxW = GAME_WIDTH - 8 - PAD * 2;
    let name = node.name.toUpperCase();
    this.strip.setText(`${name} · ${region}${here}`);
    if (this.strip.width > maxW) this.strip.setText(`${name}${here}`);
    while (this.strip.width > maxW && name.length > 4) {
      name = name.slice(0, -1);
      this.strip.setText(`${name.trimEnd()}..${here}`);
    }
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
