/**
 * Rest points — every inn / home / camp fire the player has ever rested at,
 * remembered so SETTINGS → "Return to a rest point" can carry them back to one.
 * It doubles as the anti-softlock escape hatch: a player stranded by a rebuilt
 * map (or a mis-step behind a one-way ledge) can always walk out of a warm door.
 *
 * Pure helpers over `WorldSnapshot.rest_points` (an additive optional save field):
 * one entry per map (the latest coords win), kept oldest-first so the list UI can
 * show the most recent rest at the top.
 */
import type { Facing, RestPoint } from '@game/data/world/types';
import { MAP_REGISTRY } from '@game/data/world/maps';
import { worldMapNodeForMap } from '@game/data/world/worldmap';

/** `galehigh_home` -> `Galehigh Home` (the last-ditch label). */
export function prettifyMapId(id: string): string {
  return id
    .split('_')
    .filter(Boolean)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

/** A friendly name for a map without loading it: its world-map place (interiors
 *  resolve to their town), else the prettified id. */
export function placeNameForMap(mapId: string): string {
  return worldMapNodeForMap(mapId)?.name ?? prettifyMapId(mapId);
}

/** Insert/refresh a rest point: drop any older entry for that map, append the new one. */
export function bankRestPoint(list: readonly RestPoint[], point: RestPoint): RestPoint[] {
  return [...list.filter((p) => p.map !== point.map), point];
}

/**
 * Load-time normalisation: tolerate a missing/garbled list, de-duplicate by map,
 * and seed an old save (pre-list) from its single `respawn`.
 */
export function normaliseRestPoints(
  stored: readonly RestPoint[] | undefined,
  respawn: { map: string; tx: number; ty: number; facing: Facing } | undefined,
): RestPoint[] {
  let out: RestPoint[] = [];
  for (const p of Array.isArray(stored) ? stored : []) {
    if (!p || typeof p.map !== 'string' || !Number.isFinite(p.tx) || !Number.isFinite(p.ty)) continue;
    out = bankRestPoint(out, {
      map: p.map,
      tx: p.tx,
      ty: p.ty,
      facing: p.facing ?? 'down',
      label: p.label || placeNameForMap(p.map),
    });
  }
  if (respawn && !out.some((p) => p.map === respawn.map)) {
    // The last rest is the most recent one by definition — append (newest last).
    out = bankRestPoint(out, { ...respawn, label: placeNameForMap(respawn.map) });
  }
  return out;
}

/** The travel list: registered maps only (a removed map can't be entered), newest first. */
export function travellableRestPoints(list: readonly RestPoint[]): RestPoint[] {
  return list.filter((p) => MAP_REGISTRY[p.map]).reverse();
}

/** "The Steady Gust Inn, Galehigh Terraces" — the place plus its town when they differ. */
export function restPointLongName(p: RestPoint): string {
  const town = worldMapNodeForMap(p.map)?.name;
  return town && town !== p.label ? `${p.label}, ${town}` : p.label;
}
