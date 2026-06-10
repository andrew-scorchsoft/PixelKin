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

export class EncounterSystem {
  constructor(private readonly map: RuntimeMap) {}

  roll(
    tx: number,
    ty: number,
    abilities: ReadonlySet<AbilityId>,
    hasFlag: (flag: WorldFlag) => boolean = () => false,
  ): EncounterIntent | null {
    for (const zone of this.map.def.encounters) {
      if (zone.requires_ability && !abilities.has(zone.requires_ability)) continue;
      // Flag-staggered zones: a restored site's encounters bloom in (requires_flag)
      // while its drained predecessor's stop rolling (hidden_when_flag).
      if (zone.requires_flag && !hasFlag(zone.requires_flag)) continue;
      if (zone.hidden_when_flag && hasFlag(zone.hidden_when_flag)) continue;
      const { rect } = zone;
      if (tx < rect.tx || ty < rect.ty || tx >= rect.tx + rect.w || ty >= rect.ty + rect.h) continue;
      if (Math.random() >= zone.encounter_rate) continue;
      if (zone.table.length === 0) continue;

      const total = zone.table.reduce((sum, e) => sum + e.weight, 0);
      let pick = Math.random() * total;
      for (const entry of zone.table) {
        pick -= entry.weight;
        if (pick <= 0) {
          const level =
            entry.min_level + Math.floor(Math.random() * (entry.max_level - entry.min_level + 1));
          return { species_id: entry.kin_id, level, terrain: zone.terrain };
        }
      }
    }
    return null;
  }
}
