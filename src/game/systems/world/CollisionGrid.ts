/**
 * Per-tile passability, precomputed from the map's tile behaviour + ability gates.
 *
 * A tile is blocked if any non-`above` tile stacked there is solid. Some tiles are
 * only conditionally solid — water blocks until you hold Tidecall, etc. — modelled
 * as "requires ability". `AbilityGate`s of effect make_passable/remove_tile turn
 * listed tiles into the same conditional form. NPCs and the player both query this.
 */
import type { AbilityId } from '@game/data/world/types';
import type { RuntimeMap } from './MapLoader';

export class CollisionGrid {
  private readonly w: number;
  private readonly h: number;
  /** Unconditionally solid tiles. */
  private readonly solid: boolean[];
  /** Tile index -> ability that makes it passable (otherwise solid). */
  private readonly gated = new Map<number, AbilityId>();

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
          } else if (meta.collides) {
            this.solid[i] = true;
          }
        }
      }
    }

    // Ability gates override: listed tiles become conditional on their gift.
    for (const gate of this.map.def.gates) {
      if (gate.effect === 'make_passable' || gate.effect === 'remove_tile') {
        for (const t of gate.tiles) {
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
}
