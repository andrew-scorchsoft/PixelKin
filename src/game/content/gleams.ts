/**
 * The eight Gleams — the relit constellations that are this game's "badges".
 *
 * A Gleam is the honour a Lampwarden grants when you relight their valley's
 * constellation: not a trophy but a homecoming, given inside the town's festival
 * (story-bible §4). Eight, two to a quadrant, close the Skyweave Crown and part
 * the Penumbra. This is the single registry behind the GLEAMS screen (the badge
 * case) and the slot-picker's gleam tally — so the screen, the count and the
 * places you earn them never drift apart. Display order is the canonical journey
 * order (South → East → North → West, two per region).
 *
 * Each Gleam's emblem art is served from public/assets/ui/gleams/<id>.webp (the
 * path drops the public/ prefix at runtime); a missing file degrades to a drawn
 * constellation roundel in GleamsMenu, so the screen always reads.
 */
import type { WorldFlag } from '@game/data/world/types';

export type Quadrant = 'South' | 'East' | 'North' | 'West';

export interface GleamEntry {
  /** Short id, also the emblem art stem (e.g. 'ember'). */
  id: string;
  /** The progression flag a Lampwarden's win raises (e.g. 'gleam:ember'). */
  flag: WorldFlag;
  /** Element name — keys theme.typeColor for the emblem's colour. */
  element: string;
  /** The relit constellation's figure-name, shown on the badge case. */
  constellation: string;
  /** The Lampwarden who vouches for you and grants it. */
  warden: string;
  /** The town whose Lumenary (and festival) the Gleam belongs to. */
  lumenary: string;
  /** Which quadrant of the Crown it closes. */
  region: Quadrant;
  /** A cosy one-liner about the relit constellation. */
  blurb: string;
  /** Served emblem art (public/assets/ui/gleams/<id>.webp at runtime). */
  art: string;
}

export const GLEAMS: readonly GleamEntry[] = [
  {
    id: 'ember',
    flag: 'gleam:ember',
    element: 'Ember',
    constellation: 'the Hearthflame',
    warden: 'Brisa Tallow',
    lumenary: 'Tinderwick',
    region: 'South',
    blurb: "Tinderwick's hearth-fire, lit in the sky again — a small flame, and the first you carry.",
    art: 'assets/ui/gleams/ember.webp',
  },
  {
    id: 'tide',
    flag: 'gleam:tide',
    element: 'Tide',
    constellation: 'the Tideglass',
    warden: 'Reyl Wash',
    lumenary: 'Pearlmoor Quay',
    region: 'South',
    blurb: "Pearlmoor's moonlit water, set turning overhead once more.",
    art: 'assets/ui/gleams/tide.webp',
  },
  {
    id: 'verdant',
    flag: 'gleam:verdant',
    element: 'Verdant',
    constellation: 'the Greenbough',
    warden: 'Sable Quill',
    lumenary: 'Lowleaf Hollow',
    region: 'East',
    blurb: "Lowleaf's glowmoss, flowered all at once across the dark in green.",
    art: 'assets/ui/gleams/verdant.webp',
  },
  {
    id: 'stone',
    flag: 'gleam:stone',
    element: 'Stone',
    constellation: 'the Deepcairn',
    warden: 'Otho Grist',
    lumenary: 'Cinderhead Mine',
    region: 'East',
    blurb: "Cinderhead's deep-earth gleam — the light that endures the longest dark.",
    art: 'assets/ui/gleams/stone.webp',
  },
  {
    id: 'storm',
    flag: 'gleam:storm',
    element: 'Storm',
    constellation: 'the Stormkite',
    warden: 'Mira Vael',
    lumenary: 'Galehigh Terraces',
    region: 'North',
    blurb: "Galehigh's lightning, strung kite-high over the terraces.",
    art: 'assets/ui/gleams/storm.webp',
  },
  {
    id: 'frost',
    flag: 'gleam:frost',
    element: 'Frost',
    constellation: 'the Auroracrown',
    warden: 'Ysolde Frost',
    lumenary: 'Pale Vault Glacier',
    region: 'North',
    blurb: "Pale Vault's aurora, hung still and shimmering over the ice.",
    art: 'assets/ui/gleams/frost.webp',
  },
  {
    id: 'solar',
    flag: 'gleam:solar',
    element: 'Solar',
    constellation: 'the Last Sun',
    warden: 'Lucan Pyre',
    lumenary: 'Sunken Solarium',
    region: 'West',
    blurb: "The Solarium's stored daylight, spent gladly back onto the night sky.",
    art: 'assets/ui/gleams/solar.webp',
  },
  {
    id: 'lunar',
    flag: 'gleam:lunar',
    element: 'Lunar',
    constellation: 'the Dreaming Moon',
    warden: 'Nessa Cole',
    lumenary: 'Nightreach Observatory',
    region: 'West',
    blurb: "Nightreach's dreamlight — the last of the eight, and the most haunted.",
    art: 'assets/ui/gleams/lunar.webp',
  },
];

/** How many of the eight Gleams the player holds. */
export function gleamCount(held: (flag: WorldFlag) => boolean): number {
  return GLEAMS.filter((g) => held(g.flag)).length;
}
