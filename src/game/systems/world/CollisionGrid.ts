/**
 * Per-tile passability, precomputed from the map's tile behaviour + ability gates.
 *
 * A tile is blocked if any non-`above` tile stacked there is solid. Some tiles are
 * only conditionally solid — water blocks until you hold Tidecall, etc. — modelled
 * as "requires ability". `AbilityGate`s of effect make_passable/remove_tile turn
 * listed tiles into the same conditional form. NPCs and the player both query this.
 */
import type { AbilityGate, AbilityId, Facing, TileCoord } from '@game/data/world/types';
import type { RuntimeMap } from './MapLoader';

/**
 * The tiles a gate covers, from whichever form it uses: a `rect` region
 * (preferred — matches warps/encounter zones) expanded to its tiles, or an
 * explicit `tiles` list (legacy). Empty if neither is present.
 */
function gateTiles(gate: AbilityGate): TileCoord[] {
  if (gate.rect) {
    const { tx, ty, w, h } = gate.rect;
    const out: TileCoord[] = [];
    for (let dy = 0; dy < h; dy++) {
      for (let dx = 0; dx < w; dx++) out.push({ tx: tx + dx, ty: ty + dy });
    }
    return out;
  }
  return gate.tiles ?? [];
}

export class CollisionGrid {
  private readonly w: number;
  private readonly h: number;
  /** Unconditionally solid tiles. */
  private readonly solid: boolean[];
  /** Tile index -> ability that makes it passable (otherwise solid). */
  private readonly gated = new Map<number, AbilityId>();
  /** Tile index -> the hop direction of a one-way ledge (solid otherwise). */
  private readonly ledges = new Map<number, Facing>();

  constructor(private readonly map: RuntimeMap) {
    this.w = map.width;
    this.h = map.height;
    this.solid = new Array(this.w * this.h).fill(false);
    this.precompute();
  }

  private precompute(): void {
    for (let ty = 0; ty < this.h; ty++) {
      for (let tx = 0; tx < this.w; tx++) {
        const i = ty * this.w + tx;
        for (const gid of this.map.gidsAt(tx, ty)) {
          const look = this.map.lookupGid(gid);
          if (!look) continue;
          const { meta } = look;
          if (meta.requires_ability) {
            // Conditionally passable (e.g. water + tidecall). Last one wins; fine.
            this.gated.set(i, meta.requires_ability);
          } else if (meta.ledge) {
            // A one-way ledge: solid for normal entry; Player hops it when
            // approaching in its direction (see Player.update).
            this.solid[i] = true;
            this.ledges.set(i, meta.ledge);
          } else if (meta.collides) {
            this.solid[i] = true;
          }
        }
      }
    }

    // Whole-structure objects (buildings, big trees): their footprint collides
    // except the overhanging top rows the player walks under (art-style §14b).
    for (const obj of this.map.def.objects ?? []) {
      if (obj.solid === false) continue;
      // Buildings collide on their whole footprint; only walk-under objects (trees,
      // lamps) free their overhang rows so the player can pass beneath the canopy.
      const startRow = obj.walk_under ? (obj.overhang ?? 0) : 0;
      for (let dy = startRow; dy < obj.h; dy++) {
        for (let dx = 0; dx < obj.w; dx++) {
          const tx = obj.at.tx + dx;
          const ty = obj.at.ty + dy;
          if (this.map.inBounds(tx, ty)) this.solid[ty * this.w + tx] = true;
        }
      }
    }

    // Doorways are WALK-ONTO tiles (the genre's step-into-the-door entry): a
    // `transition:'door'` warp sits in a building's otherwise-solid footprint (or a
    // cave mouth), so free its tile or the player could never reach it to walk
    // through. Runs after the object loop so it overrides the footprint. Gated
    // ("locked") doors stay freed too — stepping on fires the warp, which delivers
    // its blocked_ref "it's locked" line rather than silently barring the way.
    for (const w of this.map.def.warps) {
      if (w.transition === 'door' && this.map.inBounds(w.at.tx, w.at.ty)) {
        this.solid[w.at.ty * this.w + w.at.tx] = false;
      }
    }

    // Ability gates override: listed tiles become conditional on their gift.
    for (const gate of this.map.def.gates) {
      if (gate.effect === 'make_passable' || gate.effect === 'remove_tile') {
        for (const t of gateTiles(gate)) {
          if (!this.map.inBounds(t.tx, t.ty)) continue;
          const i = t.ty * this.w + t.tx;
          this.solid[i] = false;
          this.gated.set(i, gate.ability);
        }
      }
    }
  }

  /** True if the player/NPC cannot enter this tile given the abilities they hold. */
  isBlocked(tx: number, ty: number, abilities: ReadonlySet<AbilityId>): boolean {
    if (tx < 0 || ty < 0 || tx >= this.w || ty >= this.h) return true;
    const i = ty * this.w + tx;
    if (this.solid[i]) return true;
    const need = this.gated.get(i);
    if (need && !abilities.has(need)) return true;
    return false;
  }

  /** The Lantern Gift this tile is gated behind, if any (for the use flourish). */
  gateAt(tx: number, ty: number): AbilityId | undefined {
    if (tx < 0 || ty < 0 || tx >= this.w || ty >= this.h) return undefined;
    return this.gated.get(ty * this.w + tx);
  }

  /** The hop direction if this tile is a one-way ledge (it reads as solid to isBlocked). */
  ledgeAt(tx: number, ty: number): Facing | undefined {
    if (tx < 0 || ty < 0 || tx >= this.w || ty >= this.h) return undefined;
    return this.ledges.get(ty * this.w + tx);
  }
}
