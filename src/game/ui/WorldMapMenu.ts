/**
 * WorldMapMenu — the vesperlamp's chart of Vesperholm (pause menu -> MAP).
 *
 * The classic handheld town map (2026-10 redraw): every place is ONE square on
 * a coarse grid — towns gold, the Crossroads orange, dungeons violet, routes a
 * small path stone, landmarks a dot — joined by roads drawn as straight runs of
 * path with right-angle bends, on land tinted by region and ringed by sea. Map
 * SIZE never shows (a long route is still one stop on the chart). The grid is
 * still honest north-up: it is snapped from the walked layout, so leave a map
 * north and the next stop is north here too. Gated passages are dashed, cave
 * passes violet-dashed, the Lanternway lanes warm-dashed; a Lantern-car line
 * appears only while the cursor is on one of its stations. The chart is bigger
 * than the screen, so it scrolls smoothly after the cursor; a blinking pin
 * marks where you are. D-pad hops between places (the strip names the pick);
 * B or A backs out. Read-only and promise-based, built from the shared kit +
 * theme tokens. The layout is data: `data/world/worldmap.json`, generated and
 * geometry-checked by `tools/maps/world_layout.py`.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { WORLD_MAP, worldMapNodeForMap } from '@game/data/world/worldmap';
import type { WorldMapNode, WorldMapRoad } from '@game/data/world/worldmap';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
const HEADER_H = 10;
const STRIP_H = 12;
/** Screen px per grid cell. */
const CELL = 8;

/** Square size (screen px) by kind — all places read alike; the hub a touch bigger. */
const NODE_SIZE: Record<string, number> = {
  town: 6,
  hub: 7,
  dungeon: 6,
  route: 4,
  landmark: 4,
};

const REGION_LABEL: Record<string, string> = {
  south: 'SOUTH VALE',
  east: 'EASTERN FENS',
  north: 'HIGH NORTH',
  west: 'WESTERN REACH',
  central: 'THE CENTRE',
  outer: 'OUTER WAYS',
};

type Cell = [number, number];

export class WorldMapMenu {
  private readonly panel: Panel;
  private readonly strip: Phaser.GameObjects.Text;
  private readonly cursor: Phaser.GameObjects.Rectangle;
  private readonly pin?: Phaser.GameObjects.Graphics;
  private readonly g: Phaser.GameObjects.Graphics;
  private readonly upHint: Phaser.GameObjects.Text;
  private readonly downHint: Phaser.GameObjects.Text;
  private readonly nodes: WorldMapNode[];
  private readonly playerNode?: WorldMapNode;
  /** Land cells ("x,y") -> their region's tint. */
  private readonly land = new Map<string, string>();
  private readonly viewX: number;
  private readonly viewY: number;
  private readonly viewW: number;
  private readonly viewH: number;
  private readonly maxX: number;
  private readonly maxY: number;
  /** Map-px offset so a chart narrower than the view sits centred. */
  private readonly padX: number;
  private readonly padY: number;
  private index: number;
  private scrollX = 0;
  private scrollY = 0;
  private targetX = 0;
  private targetY = 0;
  private drawnX = NaN;
  private drawnY = NaN;
  private drawnIndex = -1;
  private readonly tweens: Phaser.Tweens.Tween[] = [];

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

    this.viewX = PAD;
    this.viewY = PAD + HEADER_H;
    this.viewW = width - PAD * 2;
    this.viewH = height - this.viewY - STRIP_H - PAD;
    const mapW = WORLD_MAP.grid.cols * CELL;
    const mapH = WORLD_MAP.grid.rows * CELL;
    this.padX = Math.max(0, Math.floor((this.viewW - mapW) / 2));
    this.padY = Math.max(0, Math.floor((this.viewH - mapH) / 2));
    this.maxX = Math.max(0, mapW - this.viewW);
    this.maxY = Math.max(0, mapH - this.viewH);
    this.buildLand();

    this.g = scene.add.graphics();
    this.panel.add(this.g);
    // the selection box + the blinking you-are-here pin ride above the chart
    this.cursor = scene.add.rectangle(0, 0, CELL + 3, CELL + 3).setStrokeStyle(1, hex(theme.worldmap.cursor));
    this.panel.add(this.cursor);
    if (this.playerNode) {
      const pin = scene.add.graphics();
      pin.fillStyle(hex(theme.worldmap.nodeEdge), 1);
      pin.fillRect(-3, -8, 7, 6);
      pin.fillRect(-1, -2, 3, 2);
      pin.fillStyle(hex(theme.worldmap.marker), 1);
      pin.fillRect(-2, -7, 5, 4);
      pin.fillRect(0, -3, 1, 2);
      this.panel.add(pin);
      this.pin = pin;
      this.tweens.push(scene.tweens.add({ targets: pin, alpha: 0.2, duration: theme.cursor.blinkMs, yoyo: true, repeat: -1 }));
    }
    this.upHint = makeText(scene, width / 2 - 2, PAD - 2, '▲', theme.text.dim).setOrigin(1, 0);
    this.downHint = makeText(scene, width / 2 + 2, PAD - 2, '▼', theme.text.dim).setOrigin(0, 0);
    this.panel.add(this.upHint);
    this.panel.add(this.downHint);
    this.strip = makeText(scene, PAD, height - STRIP_H - 1, '', theme.text.base);
    this.panel.add(this.strip);

    // open centred on the cursor, no slide
    this.aim(true);
    this.refresh();
  }

  /** Land = every place + road cell and a one-cell coast round them, tinted by
   *  the nearest place's region (so each valley reads as its own country). */
  private buildLand(): void {
    const owners: { x: number; y: number; region: string }[] = this.nodes.map((n) => ({ x: n.gx, y: n.gy, region: n.region }));
    const byId = new Map(this.nodes.map((n) => [n.id, n]));
    for (const road of WORLD_MAP.roads) {
      if (road.kind === 'car') continue;
      const region = byId.get(road.a)?.region ?? 'outer';
      for (const [x, y] of this.roadCells(road)) owners.push({ x, y, region });
    }
    const core = new Map<string, string>();
    for (const o of owners) core.set(`${o.x},${o.y}`, o.region);
    for (const o of owners) {
      for (let dy = -1; dy <= 1; dy++) {
        for (let dx = -1; dx <= 1; dx++) {
          const k = `${o.x + dx},${o.y + dy}`;
          if (this.land.has(k)) continue;
          // the nearest core cell's region (core cells own themselves)
          let best = o.region;
          let bestD = Infinity;
          for (const [ck, region] of core) {
            const [cx, cy] = ck.split(',').map(Number);
            const d = Math.abs(cx - o.x - dx) + Math.abs(cy - o.y - dy);
            if (d < bestD) {
              bestD = d;
              best = region;
              if (d === 0) break;
            }
          }
          this.land.set(k, theme.worldmap.land[best] ?? theme.worldmap.land.outer);
        }
      }
    }
  }

  /** Every cell a road's path passes through, ends included. */
  private roadCells(road: WorldMapRoad): Cell[] {
    const out: Cell[] = [];
    const path = road.path;
    if (!path.length) return out;
    out.push([path[0][0], path[0][1]]);
    for (let i = 1; i < path.length; i++) {
      let [x, y] = path[i - 1];
      const [bx, by] = path[i];
      const sx = Math.sign(bx - x);
      const sy = Math.sign(by - y);
      while (x !== bx || y !== by) {
        x += sx;
        y += sy;
        out.push([x, y]);
      }
    }
    return out;
  }

  /** Map-px (cell grid) -> panel-local screen px at the current scroll. */
  private sx(px: number): number {
    return this.viewX + this.padX + px - Math.round(this.scrollX);
  }

  private sy(py: number): number {
    return this.viewY + this.padY + py - Math.round(this.scrollY);
  }

  /** A filled rect in map px, clipped to the view (everything on the chart is a rect). */
  private rect(x: number, y: number, w: number, h: number, color: string, alpha = 1): void {
    let x0 = this.sx(x);
    let y0 = this.sy(y);
    let x1 = x0 + w;
    let y1 = y0 + h;
    x0 = Math.max(x0, this.viewX);
    y0 = Math.max(y0, this.viewY);
    x1 = Math.min(x1, this.viewX + this.viewW);
    y1 = Math.min(y1, this.viewY + this.viewH);
    if (x1 <= x0 || y1 <= y0) return;
    this.g.fillStyle(hex(color), alpha);
    this.g.fillRect(x0, y0, x1 - x0, y1 - y0);
  }

  /** A road run between two cell centres, `w` px thick; dashed runs skip every other 3px. */
  private leg(a: number[], b: number[], w: number, color: string, dashed: boolean, inset = 0): void {
    const ax = a[0] * CELL + CELL / 2;
    const ay = a[1] * CELL + CELL / 2;
    const bx = b[0] * CELL + CELL / 2;
    const by = b[1] * CELL + CELL / 2;
    const h = Math.floor(w / 2);
    if (ay === by) {
      const x0 = Math.min(ax, bx) + inset;
      const x1 = Math.max(ax, bx) - inset;
      if (!dashed) this.rect(x0 - h, ay - h, x1 - x0 + w, w, color);
      else for (let x = x0; x < x1; x += 6) this.rect(x, ay - h, Math.min(3, x1 - x), w, color);
    } else {
      const y0 = Math.min(ay, by) + inset;
      const y1 = Math.max(ay, by) - inset;
      if (!dashed) this.rect(ax - h, y0 - h, w, y1 - y0 + w, color);
      else for (let y = y0; y < y1; y += 6) this.rect(ax - h, y, w, Math.min(3, y1 - y), color);
    }
  }

  private draw(): void {
    const g = this.g;
    g.clear();
    const wm = theme.worldmap;
    // the sea
    g.fillStyle(hex(wm.sea), 1);
    g.fillRect(this.viewX, this.viewY, this.viewW, this.viewH);
    // the land, with a pale shoreline where it meets the sea
    for (const [k, color] of this.land) {
      const [cx, cy] = k.split(',').map(Number);
      this.rect(cx * CELL, cy * CELL, CELL, CELL, color);
    }
    for (const k of this.land.keys()) {
      const [cx, cy] = k.split(',').map(Number);
      const x = cx * CELL;
      const y = cy * CELL;
      if (!this.land.has(`${cx},${cy - 1}`)) this.rect(x, y - 1, CELL, 1, wm.shore);
      if (!this.land.has(`${cx},${cy + 1}`)) this.rect(x, y + CELL, CELL, 1, wm.shore);
      if (!this.land.has(`${cx - 1},${cy}`)) this.rect(x - 1, y, 1, CELL, wm.shore);
      if (!this.land.has(`${cx + 1},${cy}`)) this.rect(x + CELL, y, 1, CELL, wm.shore);
    }
    // roads: an outlined path for walked roads, dashes for the rest
    const legs = (road: WorldMapRoad, fn: (a: number[], b: number[]) => void): void => {
      for (let i = 1; i < road.path.length; i++) fn(road.path[i - 1], road.path[i]);
    };
    const roads = WORLD_MAP.roads.filter((r) => r.kind !== 'car');
    for (const r of roads) if (r.kind === 'road') legs(r, (a, b) => this.leg(a, b, 4, wm.roadEdge, false));
    for (const r of roads) {
      const color = r.kind === 'road' ? wm.road : r.kind === 'lane' ? wm.lane : r.kind === 'pass' ? wm.pass : wm.gate;
      legs(r, (a, b) => this.leg(a, b, 2, color, r.kind !== 'road', r.kind === 'road' ? 0 : 2));
    }
    // a Lantern-car line shows while the cursor sits on one of its stations
    const sel = this.nodes[this.index];
    const byId = new Map(this.nodes.map((n) => [n.id, n]));
    for (const r of WORLD_MAP.roads) {
      if (r.kind !== 'car' || (r.a !== sel.id && r.b !== sel.id)) continue;
      const a = byId.get(r.a);
      const b = byId.get(r.b);
      if (!a || !b) continue;
      const ax = a.gx * CELL + CELL / 2;
      const ay = a.gy * CELL + CELL / 2;
      const bx = b.gx * CELL + CELL / 2;
      const by = b.gy * CELL + CELL / 2;
      const steps = Math.max(1, Math.floor(Math.hypot(bx - ax, by - ay) / 4));
      for (let i = 1; i < steps; i++) {
        this.rect(Math.round(ax + ((bx - ax) * i) / steps) - 1, Math.round(ay + ((by - ay) * i) / steps) - 1, 2, 2, wm.car);
      }
    }
    // the places: one square each, outlined so they pop off land and road alike
    for (const n of this.nodes) {
      const s = NODE_SIZE[n.kind] ?? NODE_SIZE.landmark;
      const x = n.gx * CELL + Math.floor((CELL - s) / 2);
      const y = n.gy * CELL + Math.floor((CELL - s) / 2);
      this.rect(x - 1, y - 1, s + 2, s + 2, wm.nodeEdge);
      this.rect(x, y, s, s, wm.node[n.kind] ?? wm.node.landmark);
      if (n.kind === 'town' || n.kind === 'hub') this.rect(x, y, s, 1, '#ffffff', 0.45);
    }
    this.drawnX = this.scrollX;
    this.drawnY = this.scrollY;
    this.drawnIndex = this.index;
    this.place();
  }

  /** Position the cursor + pin over the chart (hidden when scrolled out of view). */
  private place(): void {
    const inView = (n: WorldMapNode): [number, number, boolean] => {
      const x = this.sx(n.gx * CELL + CELL / 2);
      const y = this.sy(n.gy * CELL + CELL / 2);
      const ok = x - 5 >= this.viewX && x + 5 <= this.viewX + this.viewW && y - 5 >= this.viewY && y + 5 <= this.viewY + this.viewH;
      return [x, y, ok];
    };
    const [cx, cy, cok] = inView(this.nodes[this.index]);
    this.cursor.setPosition(cx, cy).setVisible(cok);
    if (this.pin && this.playerNode) {
      const [px, py, pok] = inView(this.playerNode);
      this.pin.setPosition(px, py - 2).setVisible(pok && py - 10 >= this.viewY);
    }
    this.upHint.setVisible(this.scrollY > 0.5);
    this.downHint.setVisible(this.scrollY < this.maxY - 0.5);
  }

  /** Choose the scroll that keeps the cursor comfortably inside the view. */
  private aim(snap = false): void {
    const n = this.nodes[this.index];
    const nx = n.gx * CELL + CELL / 2 + this.padX;
    const ny = n.gy * CELL + CELL / 2 + this.padY;
    const mx = Math.min(32, this.viewW / 3);
    const my = Math.min(28, this.viewH / 3);
    let tx = snap ? nx - this.viewW / 2 : this.targetX;
    let ty = snap ? ny - this.viewH / 2 : this.targetY;
    if (nx - tx < mx) tx = nx - mx;
    if (nx - tx > this.viewW - mx) tx = nx - (this.viewW - mx);
    if (ny - ty < my) ty = ny - my;
    if (ny - ty > this.viewH - my) ty = ny - (this.viewH - my);
    this.targetX = Phaser.Math.Clamp(Math.round(tx), 0, this.maxX);
    this.targetY = Phaser.Math.Clamp(Math.round(ty), 0, this.maxY);
    if (snap) {
      this.scrollX = this.targetX;
      this.scrollY = this.targetY;
    }
  }

  /** Glide the scroll toward its target; redraw only when something moved. */
  private step(): void {
    const ease = (cur: number, to: number): number => {
      const d = to - cur;
      if (Math.abs(d) < 1) return to;
      return cur + Math.sign(d) * Math.max(1, Math.abs(d) * 0.25);
    };
    this.scrollX = ease(this.scrollX, this.targetX);
    this.scrollY = ease(this.scrollY, this.targetY);
    if (
      Math.round(this.scrollX) !== Math.round(this.drawnX) ||
      Math.round(this.scrollY) !== Math.round(this.drawnY) ||
      this.index !== this.drawnIndex
    ) {
      this.draw();
    }
  }

  private refresh(): void {
    this.aim();
    this.step();
    const node = this.nodes[this.index];
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

  /** Hop the cursor to the nearest place in the pressed direction. */
  private move(dx: number, dy: number): void {
    const from = this.nodes[this.index];
    let best = -1;
    let bestScore = Infinity;
    this.nodes.forEach((n, i) => {
      if (i === this.index) return;
      const vx = n.gx - from.gx;
      const vy = n.gy - from.gy;
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
        this.step();
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
    for (const t of this.tweens) t.remove();
    this.panel.destroy();
  }
}
