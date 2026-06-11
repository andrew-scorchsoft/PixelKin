/**
 * The Wayfarer's Charts — the in-vesperlamp gallery of Vesperholm's mood pieces
 * (pause menu -> CHARTS).
 *
 * Every area, route and landmark has a wide concept-art "chart" (the establishing
 * shots in `assets/concept-art/`, served from `public/assets/concept-art/`). This
 * registry surfaces them in-game: the FIRST time the player walks into any of a
 * chart's `maps`, it's discovered — a full-screen reveal plays and the chart joins
 * the gallery. Until then it reads as a "? ? ?" tease, so the player can see the
 * SHAPE of the world (and feel the corners they've yet to find) without spoiling it.
 *
 * Discovery is tracked on a flag per chart (`chartFlag`), banked in `world.flags`
 * like every other progression flag — no new save field, no schema bump.
 *
 * Authoring: cosy, a little melancholy, canon vocabulary only (never
 * monster/gym/badge or another franchise's terms). Keep each `subtitle` to one
 * short evocative line so it fits the reveal caption and the gallery detail pane.
 * Charts are GROUPED + ORDERED by region (see REGION_ORDER); add later regions'
 * places here as their art lands. A chart with an empty `maps` list is a deliberate
 * forward tease (content not built yet, e.g. the Lanternway) — give it a map id when
 * the map is authored and it becomes discoverable for free.
 */
import type { ChartEntry } from './types';
import type { Region } from '@game/data/world/graph';

const AREA = (slug: string): string => `assets/concept-art/areas/${slug}.webp`;
const LAND = (slug: string): string => `assets/concept-art/landmarks/${slug}.webp`;

export const CHARTS: readonly ChartEntry[] = [
  // ---- The South: the apprentice's home shore ---------------------------------
  {
    id: 'tinderwick',
    name: 'Tinderwick',
    subtitle: "A wick-maker's town, keeping the last warm lanterns at the dusk's edge.",
    region: 'south',
    kind: 'area',
    art: AREA('tinderwick'),
    maps: ['tinderwick'],
  },
  {
    id: 'dimglass-coast',
    name: 'Dimglass Coast',
    subtitle: 'Grey surf under a starless sky — the long shore road south.',
    region: 'south',
    kind: 'route',
    art: AREA('dimglass-coast'),
    maps: ['dimglass_coast', 'dimglass_coast_ii'],
  },
  {
    id: 'pearlmoor-quay',
    name: 'Pearlmoor Quay',
    subtitle: 'A pearl-diving port that keeps the tide for a clock.',
    region: 'south',
    kind: 'area',
    art: AREA('pearlmoor-quay'),
    maps: ['pearlmoor_quay'],
  },
  {
    id: 'tideglass-cavern',
    name: 'Tideglass Cavern',
    subtitle: 'A sea-cave of mirrored water, glass-smooth and cold.',
    region: 'south',
    kind: 'landmark',
    art: LAND('tideglass-cavern'),
    maps: ['tideglass_cavern'],
  },
  {
    id: 'dawnstead',
    name: 'Dawnstead',
    subtitle: 'The hamlet that has waited longest for a morning overdue.',
    region: 'south',
    kind: 'area',
    art: AREA('dawnstead'),
    maps: ['dawnstead'],
  },

  // ---- The East: fen, forest and the warm stone hills -------------------------
  {
    id: 'saltreach-fen',
    name: 'Saltreach Fen',
    subtitle: 'Brackish channels and reed-light — easy to lose your bearings.',
    region: 'east',
    kind: 'route',
    art: AREA('saltreach-fen'),
    maps: ['saltreach_fen_i', 'saltreach_fen_ii'],
  },
  {
    id: 'lowleaf-hollow',
    name: 'Lowleaf Hollow',
    subtitle: 'A forest town beneath a canopy that never sees noon.',
    region: 'east',
    kind: 'area',
    art: AREA('lowleaf-hollow'),
    maps: ['lowleaf_hollow'],
  },
  {
    id: 'glowmoss-deep',
    name: 'Glowmoss Deep',
    subtitle: 'A cave lit only by moss — and the things that glow within it.',
    region: 'east',
    kind: 'landmark',
    art: LAND('glowmoss-deep'),
    maps: ['glowmoss_deep', 'glowmoss_deep_b1f'],
  },
  {
    id: 'cinderhead-mine',
    name: 'Cinderhead Mine',
    subtitle: 'A mining town set into a hill of warm, breathing stone.',
    region: 'east',
    kind: 'area',
    art: AREA('cinderhead-mine'),
    maps: ['cinderhead_mine', 'cinderhead_deep'],
  },

  // ---- The North: wind-carved heights and blue ice ----------------------------
  {
    id: 'galehigh-terraces',
    name: 'Galehigh Terraces',
    subtitle: 'Wind-carved steps where the storms have made their home.',
    region: 'north',
    kind: 'area',
    art: AREA('galehigh-terraces'),
    maps: ['galehigh_terraces'],
  },
  {
    id: 'windward-stair',
    name: 'Windward Stair',
    subtitle: 'A switchback climb into thinning, singing air.',
    region: 'north',
    kind: 'route',
    art: AREA('windward-stair'),
    maps: ['windward_stair_i', 'windward_stair_ii'],
  },
  {
    id: 'wind-eye',
    name: 'Wind-Eye',
    subtitle: 'A sky-grotto where the gales fall still and seem to listen.',
    region: 'north',
    kind: 'landmark',
    art: LAND('wind-eye'),
    maps: ['wind_eye'],
  },
  {
    id: 'pale-vault-glacier',
    name: 'Pale Vault Glacier',
    subtitle: 'A town of blue ice beneath a vault of frozen stars.',
    region: 'north',
    kind: 'area',
    art: AREA('pale-vault-glacier'),
    maps: ['pale_vault_glacier'],
  },

  // ---- The West: sun-ruins and the star-watchers ------------------------------
  {
    id: 'hushfrost-pass',
    name: 'Hushfrost Pass',
    subtitle: 'A snow canyon so quiet the cold seems to hold its breath.',
    region: 'west',
    kind: 'route',
    art: AREA('hushfrost-pass'),
    maps: ['hushfrost_pass_i', 'hushfrost_pass_ii'],
  },
  {
    id: 'sunken-solarium',
    name: 'Sunken Solarium',
    subtitle: 'A sun-temple half-drowned, still warm with stored daylight.',
    region: 'west',
    kind: 'area',
    art: AREA('sunken-solarium'),
    maps: ['sunken_solarium'],
  },
  {
    id: 'sunvault-climb',
    name: 'Sunvault Climb',
    subtitle: 'Terraces of sun-vine, bridging a ruin up toward the light.',
    region: 'west',
    kind: 'route',
    art: AREA('sunvault-climb'),
    maps: ['sunvault_climb_i', 'sunvault_climb_ii'],
  },
  {
    id: 'nightreach-observatory',
    name: 'Nightreach Observatory',
    subtitle: "A star-watchers' town under the clearest dark in Vesperholm.",
    region: 'west',
    kind: 'area',
    art: AREA('nightreach-observatory'),
    maps: ['nightreach_observatory'],
  },

  // ---- The Outer Ring: the Lanternway and the blighted marches ----------------
  {
    id: 'vesper-crossroads',
    name: 'Vesper Crossroads',
    subtitle: 'Where every lantern-road meets, and travellers trade the news.',
    region: 'outer',
    kind: 'area',
    art: AREA('vesper-crossroads'),
    maps: ['vesper_crossroads'],
  },
  {
    id: 'lanternway',
    name: 'The Lanternway',
    subtitle: 'The lit road that rings the rim, spoke to far-off spoke.',
    region: 'outer',
    kind: 'route',
    art: AREA('lanternway'),
    maps: [], // forward tease: no single map yet — add ids when authored
  },
  {
    id: 'coldfog-marches',
    name: 'Coldfog Marches',
    subtitle: 'A blighted marsh where the dark pools thick and cold.',
    region: 'outer',
    kind: 'route',
    art: AREA('coldfog-marches'),
    maps: ['coldfog_marches_i', 'coldfog_marches_ii'],
  },
  {
    id: 'drownlight-beacon',
    name: 'Drownlight Beacon',
    subtitle: 'A snuffed lighthouse, its great lamp gone cold and dark.',
    region: 'outer',
    kind: 'landmark',
    art: LAND('drownlight-beacon'),
    maps: ['drownlight_beacon'],
  },
  {
    id: 'hollowfen-stillworks',
    name: 'Hollowfen Stillworks',
    subtitle: 'A derelict works where the Hollowing once drained the light.',
    region: 'outer',
    kind: 'landmark',
    art: LAND('hollowfen-stillworks'),
    maps: ['hollowfen_stillworks'],
  },

  // ---- The Crown: the darkened heart of the world -----------------------------
  {
    id: 'penumbra-ring',
    name: 'Penumbra Ring',
    subtitle: 'The ring of half-light that guards the darkened mountain.',
    region: 'central',
    kind: 'area',
    art: AREA('penumbra-ring'),
    maps: ['penumbra_ring'],
  },
  {
    id: 'umbral-spire',
    name: 'Umbral Spire',
    subtitle: "The black peak at the world's heart, where the dusk first fell.",
    region: 'central',
    kind: 'area',
    art: AREA('umbral-spire'),
    maps: ['umbral_spire'],
  },
  {
    id: 'starwell',
    name: 'Starwell',
    subtitle: 'A shrine of fallen starlight, found only once the Crown is whole.',
    region: 'central',
    kind: 'landmark',
    art: LAND('starwell'),
    maps: ['starwell'],
  },
];

/** Display order + label for each region group in the gallery. */
export const REGION_ORDER: readonly Region[] = ['south', 'east', 'north', 'west', 'outer', 'central'];

export const REGION_LABELS: Record<Region, string> = {
  south: 'THE SOUTH',
  east: 'THE EAST',
  north: 'THE NORTH',
  west: 'THE WEST',
  outer: 'THE OUTER RING',
  central: 'THE CROWN',
};

/** The progression flag that marks a chart discovered (banked in world.flags). */
export function chartFlag(chart: ChartEntry): string {
  return `chart:${chart.id}`;
}

/** The chart (if any) whose first visit a given map id discovers. */
export function chartForMap(mapId: string): ChartEntry | undefined {
  return CHARTS.find((c) => c.maps.includes(mapId));
}
