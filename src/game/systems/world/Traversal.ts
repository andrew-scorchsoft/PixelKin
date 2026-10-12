/**
 * The traversal kit's rules (2026-10, docs/world/walkthrough/09-the-wild-ways.md §1):
 * forced-movement FLOWS (steep chutes, glare ice, ore-cart rails), axis-bound SPANS
 * (bridges you can pass under, ladders, rope planks) and rider JUMPS (ramps).
 *
 * Pure rules, no Phaser: the Player asks `plan()` what a press in a direction does,
 * and `forced()` whether the tile it just reached carries it on. Everything is map
 * data; `tools/maps/worldmodel.py` mirrors these rules so the audits walk the same
 * world. Standing ON a span tile always means standing on its deck (an underpass is
 * a single pass-through move — you never stop beneath a bridge).
 */
import type { Facing, FlowZone, JumpPad, MapDefinition, SpanZone, TileCoord } from '@game/data/world/types';

const DELTA: Record<Facing, { dx: number; dy: number }> = {
  down: { dx: 0, dy: 1 },
  up: { dx: 0, dy: -1 },
  left: { dx: -1, dy: 0 },
  right: { dx: 1, dy: 0 },
};

export const OPPOSITE: Record<Facing, Facing> = { down: 'up', up: 'down', left: 'right', right: 'left' };

export type MovePlan =
  | { kind: 'blocked'; steep?: boolean }
  /** One ordinary step (onto a deck when `deck` is set). */
  | { kind: 'step'; to: TileCoord; deck?: SpanZone }
  /** Under a bridge: every tile walked through, the last is where you stop. */
  | { kind: 'pass'; tiles: TileCoord[] }
  /** A rider's leap off a ramp: over `via`, landing on `to`. */
  | { kind: 'leap'; via: TileCoord; to: TileCoord };

export interface TraverseContext {
  /** Ordinary enterability (collision + NPC bodies) — what the map always used. */
  canEnter(tx: number, ty: number): boolean;
  /** True if an NPC/actor body stands here (decks ignore collision, not bodies). */
  occupied(tx: number, ty: number): boolean;
  /** In bounds and not solid UNDERNEATH (the ground beneath a bridge deck). */
  groundOpen(tx: number, ty: number): boolean;
  /** Riding a runner on a ride map (ramps only launch riders). */
  riding: boolean;
}

function inRect(r: { tx: number; ty: number; w: number; h: number } | undefined, tx: number, ty: number): boolean {
  return !!r && tx >= r.tx && ty >= r.ty && tx < r.tx + r.w && ty < r.ty + r.h;
}

export const alongAxis = (span: SpanZone, dir: Facing): boolean =>
  span.axis === 'h' ? dir === 'left' || dir === 'right' : dir === 'up' || dir === 'down';

export class Traversal {
  private readonly flows: FlowZone[];
  private readonly spans: SpanZone[];
  private readonly jumps: JumpPad[];

  constructor(
    def: MapDefinition,
    /** Flag lookup for lever-switched flows; re-read live, so a lever takes effect at once. */
    private readonly isHeld: (flag: string) => boolean,
  ) {
    this.flows = def.flows ?? [];
    this.spans = def.spans ?? [];
    this.jumps = def.jumps ?? [];
  }

  /** Does this map use the kit at all? (the fast path skips it entirely) */
  get active(): boolean {
    return this.flows.length + this.spans.length + this.jumps.length > 0;
  }

  flowAt(tx: number, ty: number): FlowZone | undefined {
    // Last listed wins, so a switched junction can sit on top of its rail.
    for (let i = this.flows.length - 1; i >= 0; i--) {
      const f = this.flows[i];
      if (f.requires_flag && !this.isHeld(f.requires_flag)) continue;
      if (f.hidden_when_flag && this.isHeld(f.hidden_when_flag)) continue;
      if (inRect(f.rect, tx, ty) || f.tiles?.some((t) => t.tx === tx && t.ty === ty)) return f;
    }
    return undefined;
  }

  spanAt(tx: number, ty: number): SpanZone | undefined {
    return this.spans.find((s) => inRect(s.rect, tx, ty));
  }

  jumpAt(tx: number, ty: number): JumpPad | undefined {
    return this.jumps.find((j) => j.at.tx === tx && j.at.ty === ty);
  }

  /**
   * After arriving on (or stopping at) `from`, does the ground carry you on?
   * Ice keeps your last heading; a chute or rail carries its own way. `steer` says
   * whether a held left/right may nudge you sideways instead (chutes only).
   */
  forced(from: TileCoord, lastDir: Facing): { dir: Facing; steer: boolean } | null {
    const f = this.flowAt(from.tx, from.ty);
    if (!f) return null;
    if (f.kind === 'ice') return { dir: lastDir, steer: false };
    if (!f.dir) return null;
    return { dir: f.dir, steer: f.kind === 'slope' };
  }

  /** What a press toward `dir` from `from` does. */
  plan(from: TileCoord, dir: Facing, ctx: TraverseContext): MovePlan {
    const d = DELTA[dir];
    const to = { tx: from.tx + d.dx, ty: from.ty + d.dy };

    // On a deck you walk its axis only — never off its sides.
    const here = this.spanAt(from.tx, from.ty);
    if (here && !alongAxis(here, dir)) return { kind: 'blocked' };

    // Never back UP a chute or a rail you're standing on.
    const flowHere = this.flowAt(from.tx, from.ty);
    if (flowHere && flowHere.kind !== 'ice' && flowHere.dir === OPPOSITE[dir]) {
      return { kind: 'blocked', steep: true };
    }

    // A rider meeting a ramp head-on clears it.
    const jump = ctx.riding ? this.jumpAt(to.tx, to.ty) : undefined;
    if (jump && jump.dir === dir) {
      const len = jump.length ?? 3;
      const land = { tx: to.tx + d.dx * (len - 1), ty: to.ty + d.dy * (len - 1) };
      if (this.enterable(land, dir, ctx)) return { kind: 'leap', via: to, to: land };
    }

    const span = this.spanAt(to.tx, to.ty);
    if (span) {
      if (alongAxis(span, dir)) {
        // Onto the deck: its own collision doesn't matter (it's a bridge over a
        // gap, a ladder up a cliff), only bodies standing on it.
        return ctx.occupied(to.tx, to.ty) ? { kind: 'blocked' } : { kind: 'step', to, deck: span };
      }
      if (!span.under) return { kind: 'blocked' };
      // The underpass: walk straight through beneath the whole deck in one go.
      const tiles: TileCoord[] = [];
      let cur = to;
      while (this.spanAt(cur.tx, cur.ty)?.under && !alongAxis(this.spanAt(cur.tx, cur.ty)!, dir)) {
        if (!ctx.groundOpen(cur.tx, cur.ty) || ctx.occupied(cur.tx, cur.ty)) return { kind: 'blocked' };
        tiles.push(cur);
        cur = { tx: cur.tx + d.dx, ty: cur.ty + d.dy };
      }
      if (!this.enterable(cur, dir, ctx) || this.spanAt(cur.tx, cur.ty)) return { kind: 'blocked' };
      tiles.push(cur);
      return { kind: 'pass', tiles };
    }

    if (!this.enterable(to, dir, ctx)) {
      const f = this.flowAt(to.tx, to.ty);
      return { kind: 'blocked', steep: !!f && f.kind !== 'ice' && f.dir === OPPOSITE[dir] };
    }
    return { kind: 'step', to };
  }

  /** Ordinary ground you may step onto heading `dir` (chutes/rails refuse uphill entry). */
  private enterable(t: TileCoord, dir: Facing, ctx: TraverseContext): boolean {
    const f = this.flowAt(t.tx, t.ty);
    if (f && f.kind !== 'ice' && f.dir === OPPOSITE[dir]) return false;
    const s = this.spanAt(t.tx, t.ty);
    if (s) return alongAxis(s, dir) && !ctx.occupied(t.tx, t.ty);
    return ctx.canEnter(t.tx, t.ty);
  }
}
