/**
 * EncounterSystem — rolls wild encounters as the player steps through terrain.
 *
 * On each tile entered, any encounter zone covering that tile (and not gated behind
 * a Lantern Gift the player lacks, or a story flag not yet held) gets a per-step
 * chance to fire; on a hit we pick a kin from the zone's weighted table and a level
 * in its range, and emit a typed intent the scene turns into a battle. Zone rects
 * are authored to match the painted terrain (see docs/world/level-design.md).
 */
import type { AbilityId, EncounterTerrain, WorldFlag } from '@game/data/world/types';
import type { RuntimeMap } from './MapLoader';

export interface EncounterIntent {
  species_id: number;
  level: number;
  terrain: EncounterTerrain;
}

/** Terrains whose encounters fire only ON a matching painted tile (grass tufts,
 *  surf). 'cave'/'sand' zones roll anywhere in their rect — a cave's whole floor
 *  is encounter ground, like the classics. */
const TILE_BOUND = new Set<EncounterTerrain>(['tall_grass', 'water']);

/** World flag set while the Hooded Lamp is shaded (ITEMS → toggle): the lamp's
 *  dimmed hood lets wild kin pass — the backtracker's friend. While held, every
 *  zone's effective encounter rate is halved (see `HOODED_RATE_FACTOR`). */
export const HOODED_LAMP_FLAG = 'flag:lamp_hooded' as WorldFlag;
/** How much the Hooded Lamp dampens the per-step encounter chance (×0.5). */
const HOODED_RATE_FACTOR = 0.5;

/** Guaranteed encounter-free steps after a wild encounter fires. The per-step
 *  roll is memoryless, so without this the very next tile has the full ~11%
 *  chance to fire again — back-to-back battles that read as "too frequent".
 *  A short grace breaks that adjacency without changing the overall density
 *  (the genre's quiet-steps-after-a-battle convention). Counted in
 *  encounterable steps; a fresh map resets it (a new EncounterSystem). */
const POST_ENCOUNTER_GRACE = 3;

export class EncounterSystem {
  /** Encounterable steps still owed as a post-battle grace (see the constant). */
  private graceRemaining = 0;

  constructor(private readonly map: RuntimeMap) {}

  /** True if any tile stacked at (tx,ty) is tagged as this encounter terrain. */
  private tileHasTerrain(tx: number, ty: number, terrain: EncounterTerrain): boolean {
    for (const gid of this.map.gidsAt(tx, ty)) {
      if (this.map.lookupGid(gid)?.meta.encounter_terrain === terrain) return true;
    }
    return false;
  }

  roll(
    tx: number,
    ty: number,
    abilities: ReadonlySet<AbilityId>,
    hasFlag: (flag: WorldFlag) => boolean = () => false,
  ): EncounterIntent | null {
    // Hold a short quiet spell after a wild battle so two encounters can't land
    // on adjacent tiles (the per-step roll below is otherwise memoryless).
    if (this.graceRemaining > 0) {
      this.graceRemaining -= 1;
      return null;
    }
    // The Hooded Lamp halves every zone's effective rate while shaded.
    const rateFactor = hasFlag(HOODED_LAMP_FLAG) ? HOODED_RATE_FACTOR : 1;
    for (const zone of this.map.def.encounters) {
      if (zone.requires_ability && !abilities.has(zone.requires_ability)) continue;
      // Flag-staggered zones: a restored site's encounters bloom in (requires_flag)
      // while its drained predecessor's stop rolling (hidden_when_flag).
      if (zone.requires_flag && !hasFlag(zone.requires_flag)) continue;
      if (zone.hidden_when_flag && hasFlag(zone.hidden_when_flag)) continue;
      const { rect } = zone;
      if (tx < rect.tx || ty < rect.ty || tx >= rect.tx + rect.w || ty >= rect.ty + rect.h) continue;
      // Tile-bound terrains only fire on a matching painted tile, so a zone's
      // rect can be a loose bounding box around an ORGANIC patch (the paint is
      // the truth — see tools/maps/patterns.py zones_from_grid).
      if (TILE_BOUND.has(zone.terrain) && !this.tileHasTerrain(tx, ty, zone.terrain)) continue;
      if (Math.random() >= zone.encounter_rate * rateFactor) continue;
      if (zone.table.length === 0) continue;

      const total = zone.table.reduce((sum, e) => sum + e.weight, 0);
      let pick = Math.random() * total;
      for (const entry of zone.table) {
        pick -= entry.weight;
        if (pick <= 0) {
          const level =
            entry.min_level + Math.floor(Math.random() * (entry.max_level - entry.min_level + 1));
          this.graceRemaining = POST_ENCOUNTER_GRACE; // quiet steps before the next roll
          return { species_id: entry.kin_id, level, terrain: zone.terrain };
        }
      }
    }
    return null;
  }
}
