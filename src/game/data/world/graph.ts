/**
 * The Vesperholm world graph: how maps connect, how connectivity CHANGES as Lantern
 * Gifts and progression flags are earned, and how the central Umbral Spire hub opens
 * its four cardinal approaches. See `docs/world/atlas.md` §1 + §3 for the wiring (the
 * full route network — segments, spurs, landmarks, shortcuts) this models.
 *
 * Structure (classic town -> route -> town): main inter-town routes are split into named
 * SEGMENTS (e.g. dimglass_coast_i/ii) with the gift-gate on a segment boundary; each
 * region has an optional SPUR (dead-end with a reward, often behind a later gift so you
 * backtrack); a few signature LANDMARKS are bigger optional micro-dungeons; and a couple
 * of late SHORTCUTS re-link a route to the hub once opened from the far side.
 */
import type { AbilityId, TileCoord, WorldFlag } from './types';

/** Where a node sits relative to the central hub (drives the 4-way unlock). */
export type Region = 'north' | 'south' | 'east' | 'west' | 'central' | 'outer';

/** A node = one map in the world. */
export interface AreaNode {
  map_id: string; // -> MapDefinition.id
  region: Region;
  /** Node only reachable / shown once this flag is satisfied (optional). */
  unlocked_by_flag?: WorldFlag;
  /** Optional/side content (a spur or landmark), not on the critical path. */
  optional?: boolean;
  /** For optional nodes: a short note on the reward hidden there (rare kin / item). */
  reward?: string;
}

/**
 * A directed connection between two maps, gated independently of geometry so connectivity
 * can be reasoned about. An edge becomes traversable only once its requirements are met —
 * this is how the map opens up as gifts/flags are earned.
 */
export interface WorldEdge {
  from_map: string;
  to_map: string;
  via_warp: string; // the Warp.id on from_map that realises this edge
  requires_ability?: AbilityId; // blocked until this gift is earned
  requires_flag?: WorldFlag; // blocked until this flag is set
  bidirectional: boolean;
}

export interface HubApproach {
  region: Region;
  /** The flag (set when that quadrant's constellations relight) that opens this approach. */
  opens_flag: WorldFlag;
}

export interface WorldGraph {
  start_map: string;
  start_at: TileCoord;
  nodes: AreaNode[];
  edges: WorldEdge[];
  /**
   * The central region, initially unreachable. Each cardinal approach opens when its flag
   * is set; the hub is fully 4-way once all four are set (which sets `flag:hub_unlocked`).
   */
  hub: {
    map_id: string;
    approaches: HubApproach[];
  };
}

/**
 * The Vesperholm world graph instance — the source of truth for connectivity and gating.
 * Map JSON for most of these areas is authored over time; this graph defines the shape.
 */
export const VESPERHOLM_GRAPH: WorldGraph = {
  start_map: 'tinderwick',
  start_at: { tx: 5, ty: 8 }, // on the square just outside the player's cottage door (R8: the cottage moved to the NW plaza)
  nodes: [
    // ---- South: Tinderwick -> Dimglass Coast (2 segments) -> Pearlmoor Quay ----------
    { map_id: 'tinderwick', region: 'south' },
    { map_id: 'tinderwick_house', region: 'south' }, // interior: the apprentice's cottage
    { map_id: 'tinderwick_shop', region: 'south' }, // interior: the general store
    { map_id: 'tinderwick_lumenary', region: 'south' }, // interior: the Ember Lumenary hall (Brisa Tallow)
    { map_id: 'tinderwick_beacon_i', region: 'south' }, // interior: the old beacon, stair floor I (wick-key gated)
    { map_id: 'tinderwick_beacon_ii', region: 'south' }, // interior: the old beacon, stair floor II
    { map_id: 'tinderwick_beacon_top', region: 'south' }, // interior: the lantern room — the Ember bond-test
    { map_id: 'duskapple_orchard', region: 'south' }, // R8: the old orchard off the square's west gap (satchel detour)
    { map_id: 'wickstead_green', region: 'south', optional: true, reward: 'the lamp-school: a teacher per mechanic (types, catching, statuses, kindling, the Hearth, resting, wicks, Gifts, menus)' }, // west of the orchard
    { map_id: 'wickstead_school', region: 'south', optional: true }, // interior: the Wickstead Lamp-school
    { map_id: 'dimglass_coast', region: 'south' }, // route segment I: cliff path + shore (authored)
    { map_id: 'dimglass_coast_ii', region: 'south' }, // route: tidal flats
    { map_id: 'gullcry_rock', region: 'south', optional: true, reward: 'rare sea-bird kin + a Tide charm' },
    { map_id: 'tideglass_cavern', region: 'south', optional: true, reward: 'landmark micro-dungeon; a signature rare water kin' },
    { map_id: 'tideglass_gallery', region: 'south', optional: true, reward: 'B1F: the Dusk Hour (Gloamber #160, the legendaryBattle set-piece)' },
    { map_id: 'pearlmoor_quay', region: 'south' },
    { map_id: 'pearlmoor_breakwater', region: 'south' }, // the Causeway Bell's foot causeway (Moor-bell shrine)
    { map_id: 'pearlmoor_lumenary', region: 'south' }, // interior: the Tide Lumenary (Reyl Wash)
    { map_id: 'pearlmoor_shop', region: 'south' }, // interior: the port chandlery
    { map_id: 'pearlmoor_inn', region: 'south' }, // interior: the quayside inn
    { map_id: 'pearlmoor_lifting_house', region: 'south', optional: true, reward: 'the Lifting House — the Booji-Wooji Man side quest' },
    { map_id: 'pearlmoor_lifting_house_b1', region: 'south', optional: true }, // interior: the Lifting House's weights floor (down the stairs)
    { map_id: 'pearlmoor_allotment', region: 'south', optional: true, reward: 'Rod & Anth\'s plot + the waystone (S5 Not All Who Wander)' },
    { map_id: 'pearlmoor_wanderwood', region: 'south', optional: true, reward: 'S5: Paul\'s wood — the Chickenpig vs Omenire, and the cup' },
    { map_id: 'pearlmoor_point', region: 'south' }, // R9: Lightkeeper's Point — the Old Light's headland off the west beach
    { map_id: 'pearlmoor_oldlight_1', region: 'south' }, // interior: the Old Light F1 — the Lobby of Groaners (opens on flag:q_south_bell)
    { map_id: 'pearlmoor_oldlight_2', region: 'south' }, // interior: F2 — the Late Laugh (the Heckler)
    { map_id: 'pearlmoor_oldlight_3', region: 'south' }, // interior: F3 — Intermission (tea-urn rest point; the Hall of Mouths)
    { map_id: 'pearlmoor_oldlight_4', region: 'south' }, // interior: F4 — the Backwards Inn (the Ringmaster)
    { map_id: 'pearlmoor_oldlight_5', region: 'south' }, // interior: F5 — the Gallery of Confident Facts
    { map_id: 'pearlmoor_oldlight_6', region: 'south' }, // interior: F6 — the One Joke
    { map_id: 'pearlmoor_oldlight_top', region: 'south' }, // interior: the Winding Room — Tam's card, the net-floats (flag:q_south_jest_done)
    { map_id: 'pearlmoor_wanderwood_far', region: 'south', optional: true, reward: 'S5: the Far Side — Mags\'s griddle, the Answering Lamp, the glass steps (all optional)' },
    { map_id: 'wayward_rise', region: 'south', optional: true, reward: 'the Wayward Arms: an open bar, a corner chair, a stranger, a night talked away (a rest point)' }, // north of the Wanderwood
    { map_id: 'wayward_arms', region: 'south', optional: true }, // interior: the Wayward Arms' bar + snug
    { map_id: 'paul_house_1', region: 'south', optional: true, reward: 'Paul\'s house: three floors of travel, t-shirts and a WANTED poster — and Lottie, who loves the Chickenpig' }, // interior: the kitchen-hall
    { map_id: 'paul_house_2', region: 'south', optional: true }, // interior: the T-shirt museum
    { map_id: 'paul_house_3', region: 'south', optional: true }, // interior: Lottie's attic
    // ---- East: Saltreach Fen (2 segments) -> Lowleaf forest -> Cinderhead cave -------
    { map_id: 'saltreach_fen_i', region: 'east' }, // route: open marsh
    { map_id: 'saltreach_fen_ii', region: 'east' }, // route: deep channels
    { map_id: 'sunkbell_shallows', region: 'east', optional: true, reward: 'rare Tide kin + item cache in a flooded shrine' },
    { map_id: 'lowleaf_hollow', region: 'east' }, // forest town + Lumenary
    { map_id: 'lowleaf_lumenary', region: 'east' }, // interior: the Verdant Lumenary (Sable Quill)
    { map_id: 'lowleaf_bower', region: 'east' }, // interior: the festival guest-bower (rest point)
    { map_id: 'gloamwood_dell', region: 'east', optional: true }, // optional spur: Georgina's dell (E4)
    { map_id: 'georgina_cottage', region: 'east', optional: true }, // interior: Georgina's cottage
    { map_id: 'glowmoss_deep', region: 'east' }, // forest interior (Glimmerstep)
    { map_id: 'glowmoss_deep_b1f', region: 'east' }, // the lower maze floor (ladder pair)
    { map_id: 'spore_grotto', region: 'east', optional: true, reward: 'rare Bug/Verdant kin + item' },
    { map_id: 'cinderhead_mine', region: 'east' }, // cave town + Lumenary (mine mouth)
    { map_id: 'cinderhead_lumenary', region: 'east' }, // interior: the Stone Lumenary (Otho Grist)
    { map_id: 'cinderhead_deep', region: 'east' }, // deep cave (Glimmerstep): the fork floor -> Galehigh
    { map_id: 'cinderhead_deep_b1f', region: 'east' }, // the descent's middle floor (gallery-miner B, the ledger)
    { map_id: 'cinderhead_deep_b2f', region: 'east' }, // the third gallery: the vigil-lamp (deepest)
    { map_id: 'crystoll_vault', region: 'east', optional: true, reward: 'late backtrack (Starreach): rare Stone/Light kin' },
    // ---- North: Galehigh -> Windward Stair (2 segments) -> Pale Vault ---------------
    { map_id: 'cinderwind_scarp', region: 'north' }, // route: the climb out of the mine (2026-10)
    { map_id: 'galehigh_terraces', region: 'north' },
    { map_id: 'galehigh_skyloft', region: 'north' }, // the winch-festival top terrace: Mira's launch-ledge bond-test (Lumenary 5's venue)
    { map_id: 'galehigh_lumenary', region: 'north' }, // interior: the Storm hall (festival home — the battle is at the skyloft)
    { map_id: 'galehigh_inn', region: 'north' }, // interior: the terrace inn (rest point)
    { map_id: 'galehigh_home', region: 'north' }, // interior: a wind-break cottage
    { map_id: 'galehigh_kitemaker', region: 'north' }, // interior: the kite-maker's workshop (shop)
    { map_id: 'windward_stair_i', region: 'north' }, // route: lower switchbacks
    { map_id: 'windward_stair_ii', region: 'north' }, // route: high crags
    { map_id: 'thunderroost', region: 'north', optional: true, reward: 'rare Storm/Flying kin + item' },
    { map_id: 'wind_eye', region: 'north', optional: true, reward: 'landmark sky-grotto; a unique Storm kin' },
    { map_id: 'pale_vault_glacier', region: 'north' },
    { map_id: 'pale_vault_undercroft', region: 'north' }, // the Lamp-Line trial: Ysolde's bond-test at its heart (Lumenary 6's venue)
    { map_id: 'pale_vault_lumenary', region: 'north' }, // interior: the Frost hall (the Aurora-watch's home — the battle is in the undercroft)
    { map_id: 'pale_vault_inn', region: 'north' }, // interior: the glacier inn (rest point)
    { map_id: 'pale_vault_home', region: 'north' }, // interior: an ice-block cottage
    { map_id: 'pale_vault_hourfold', region: 'north', optional: true, reward: 'the Still Hour (Noctilune #161) past the Unstruck Toll' },
    // ---- West: Hushfrost Pass (2 seg) -> Solarium -> Sunvault Climb (2 seg) -> Nightreach
    { map_id: 'hushfrost_pass_i', region: 'west' }, // route: snow canyon
    { map_id: 'hushfrost_pass_ii', region: 'west' }, // route: coldfog throat
    { map_id: 'aurora_hollow', region: 'west', optional: true, reward: 'rare Frost/Light kin + item' },
    { map_id: 'sunken_solarium', region: 'west' },
    { map_id: 'sunken_solarium_lumenary', region: 'west' }, // interior: the Solar hall (the troupe's green-room + the rest point — the battle is on the lit stage outdoors)
    { map_id: 'unrisen_stair', region: 'west', optional: true, reward: 'the Lost Hour (Erstmorn #162) atop the Sunsketch bloom ascent' },
    { map_id: 'sunvault_climb_i', region: 'west' }, // route: the foot of the face (ladders, the west notch)
    { map_id: 'sunvault_climb_ii', region: 'west' }, // route: sun-vine bridges up the face
    { map_id: 'helia_vault', region: 'west', optional: true, reward: 'rare Solar kin + item in a sealed reliquary' },
    { map_id: 'nightreach_observatory', region: 'west' },
    { map_id: 'nightreach_lumenary', region: 'west' }, // interior: the star-temple sanctum — Nessa's bond-test under the great eyepiece (the eighth Gleam; engine derives crown_west + hub_unlocked)
    { map_id: 'nightreach_inn', region: 'west' }, // interior: The Long Watch inn (rest point)
    { map_id: 'nightreach_home', region: 'west' }, // interior: a watcher's cottage
    // ---- Outer: Coldfog Marches (2 segments) + the hub ------------------------------
    { map_id: 'coldfog_marches_i', region: 'outer' }, // route: blighted marsh
    { map_id: 'coldfog_marches_ii', region: 'outer' }, // route: deep coldfog
    { map_id: 'drownlight_beacon', region: 'outer', optional: true, reward: 'rare Dark kin in a snuffed lighthouse' },
    { map_id: 'hollowfen_stillworks', region: 'outer', optional: true, reward: "landmark micro-dungeon: a derelict Hollowing null-works; a powerful Storm/Dark 'charged husk' kin" },
    { map_id: 'vesper_crossroads', region: 'outer' },
    { map_id: 'crossroads_inn', region: 'outer' }, // interior: the waystation inn (C2 innkeeper)
    // The Lanternway spokes — real lane maps (2026-06 topology fix): each spoke
    // is a short bending country lane, so the hub's roads radiate compass-true.
    { map_id: 'lanternway_tinderwick', region: 'outer' },
    // The Pearlmoor <-> Crossroads route (replaced the lanternway_pearlmoor lane).
    { map_id: 'wrackline_path', region: 'south' },
    { map_id: 'sounding_cave', region: 'south' },
    { map_id: 'lanternfall_road', region: 'south' },
    { map_id: 'lanternway_lowleaf', region: 'outer' },
    { map_id: 'lanternway_undercut', region: 'outer' }, // the cave beneath the Lowleaf spoke (its two mouths)
    { map_id: 'lanternway_galehigh', region: 'outer' },
    { map_id: 'lanternway_nightreach', region: 'outer' },
    // ---- Central: the mountain road -> Penumbra Ring -> Umbral Spire (+ a late landmark) -> Dawnstead -----
    { map_id: 'umbral_approach', region: 'central' }, // the mountain road up from the hub (2026-10)
    { map_id: 'penumbra_ring', region: 'central' },
    { map_id: 'starwell', region: 'central', optional: true, reward: 'post-Crown landmark (Starreach): a near-legendary kin' },
    { map_id: 'umbral_spire', region: 'central', unlocked_by_flag: 'flag:hub_unlocked' },
    { map_id: 'umbral_spire_f2', region: 'central' }, // the null-works maze floor (ladder pair)
    { map_id: 'umbral_spire_f3', region: 'central' }, // the high gallery; home of the shaft compressor
    { map_id: 'umbral_spire_summit', region: 'central' }, // the Great Null; sets keystar_relit -> dawn
    { map_id: 'dawnstead', region: 'south', unlocked_by_flag: 'flag:dawn' },
    // ---- The Starfall Vigils (walkthrough 06-postgame): one annex per quadrant + the
    // outer marches, sealed behind the star-readings (the host warps carry the flags).
    { map_id: 'vigil_hearthfall', region: 'south', optional: true, reward: 'Vigil I: EMBRALUX #33 + TIDEVEIL #34 register beds (58-60) + the Radiant Charm' },
    { map_id: 'vigil_grovefall', region: 'east', optional: true, reward: 'Vigil II: MYCOVAST #70 register bed (60-62) + Star-chart: Tremor Quake' },
    { map_id: 'vigil_stormfall', region: 'north', optional: true, reward: 'Vigil III: NULLHUSK #144 register bed (62-64) + the storm-tithe' },
    { map_id: 'vigil_sunfall', region: 'west', optional: true, reward: 'Vigil IV: DAWNWATCHER #129 + HELITHORN #119 register beds (64-66) + Star-chart: Sunburst Nova' },
    { map_id: 'vigil_murkfall', region: 'outer', optional: true, reward: 'Vigil V: SOLARMOURN #128 / CINDERVAST #145 / BOGVAST #146 register beds (66-68) + the Morrow Charm' },
    // ---- THE WILD WAYS (09-the-wild-ways.md, 2026-10) — one block per area lane
    // the Wick-Run (A): Sunvault Climb I's south road -> the crest -> downhill to Lightkeeper's Point
    { map_id: 'wickrun_crest', region: 'west', optional: true, reward: 'the runner rental + the Tallow Lift (frees the lift home)' },
    { map_id: 'wickrun_chute', region: 'west', optional: true, reward: 'run-only Tallowcrest/Wickmere/Warmantis + a kicker-only Lumen Drop' },
    { map_id: 'wickrun_trestles', region: 'west', optional: true, reward: 'the Spiral trestle (over, round, under) + two Runners + a wick-purse' },
    { map_id: 'wickrun_traverse', region: 'west', optional: true, reward: 'the rock garden + the ramp line + a Beacon charge in the cart wreck' },
    { map_id: 'wickrun_lower', region: 'west', optional: true, reward: 'Rook, the Runners\' captain + the rare Chandrek + a kicker-only Wax Cake cache' },
    { map_id: 'wickrun_foot', region: 'south', optional: true, reward: 'the finish (time-trial prizes, Rook\'s ribbon) + the Tallow Lift\'s foot station' },
    // the Mirelights (B): over Ansel's ferry (the Frostglass Lens from Pale Vault), east of Saltreach Fen I
    { map_id: 'mirelight_landing', region: 'east', optional: true, unlocked_by_flag: 'flag:mirelight_ferry', reward: 'Nell\'s lore, Tobin\'s boat, the first false-light boards; exclusive Tidwraith/Lumplass' },
    { map_id: 'mirelight_glassmere', region: 'east', optional: true, unlocked_by_flag: 'flag:mirelight_ferry', reward: 'the false-lights maze + currents; the Glassmere Pearl; rare Lampling' },
    { map_id: 'mirelight_chapel', region: 'east', optional: true, unlocked_by_flag: 'flag:mirelight_ferry', reward: 'Tobin found; the acolyte\'s camp (rest point); the chapel door' },
    { map_id: 'lanthorne_hollow', region: 'east', optional: true, unlocked_by_flag: 'flag:mirelight_tobin_found', reward: 'LANTHORNE #165 (legendary, lv 45)' },
    // the Rimeway (C): Pale Vault's north road -> the Fold -> the Rime Gate (barred from the marsh side)
    { map_id: 'rimeway_ascent', region: 'north', optional: true, reward: 'the Glare (an ice-slide climb) + the cache pool' },
    { map_id: 'rimeway_fold', region: 'north', optional: true, reward: 'Vaultclaw #76 (Fold-only) + the clear-ice core for Isel\'s Frostglass Lens' },
    { map_id: 'rimeway_descent', region: 'outer', optional: true, reward: 'lifts the Rime Gate: a Coldfog <-> Pale Vault return road' },
    { map_id: 'reckoning_works', region: 'north', optional: true, reward: 'side quest "Measured in Miles": the Aurora Card + wicks + Beacon charges' }, // interior: the Reckoning-Works (C2)
    // the Old Seams (D): Cinderhead Mine's seam-door (Otho, post-Stone) -> three floors down -> the first star
    { map_id: 'old_seams_i', region: 'east', optional: true, reward: 'the Shaft Benches: planks + ladders, Orebound beds, a pillar-islet charge' },
    { map_id: 'old_seams_ii', region: 'east', optional: true, reward: 'the Rail Yard puzzle: rare Ferrolith, the siding\'s starglass' },
    { map_id: 'old_seams_iii', region: 'east', optional: true, reward: 'the Scree Galleries: Pyrolith/Lithonyx, very rare Prismara, a scree-only Lumen Drop' },
    { map_id: 'emberroot_heart', region: 'east', optional: true, reward: 'EMBERROOT #166 (lv 46, Starlight return) + the Ledger\'s last page' },
    // Sunvault Climb rebuild (S)
    { map_id: 'sunvault_climb_iii', region: 'west' }, // route: the Gilt Face (ladder pitches, the trestle over the gully)
    { map_id: 'sunvault_climb_iv', region: 'west' }, // route: the Sun Ledges (planks + ledges to the observatory hill)
    // ---- THE FARLAMP ISLES (walkthrough/10 Part I, post-game) — Lane C1: the surface.
    // Rowed from the Point's slip / the Wick-Run Foot once Ione's skiff is yours.
    { map_id: 'farlamp_sound', region: 'south', optional: true, unlocked_by_flag: 'flag:q_isles_afloat', reward: 'the deep under the lighthouse: Fathomote/Hermiwick, a boat-trainer, a Hearth Coal' },
    { map_id: 'farlamp_shelfwater', region: 'south', optional: true, unlocked_by_flag: 'flag:q_isles_afloat', reward: 'reef flats + the sunken hull (a Hearth Coal), a boat-trainer' },
    { map_id: 'farlamp_fogwall', region: 'south', optional: true, unlocked_by_flag: 'flag:q_isles_afloat', reward: 'the far lamp; the fog turns you round without the fog-glass; Fogwisp' },
    { map_id: 'farlamp_gullwrack', region: 'south', optional: true, unlocked_by_flag: 'flag:q_isles_afloat', reward: 'gull-cliffs, the keeper\'s bothy (rest), the Undertide I mouth' },
    { map_id: 'farlamp_kelpcrown', region: 'south', optional: true, unlocked_by_flag: 'flag:q_isles_afloat', reward: 'the keepers\' ruins (a 2,000w purse), kelp terraces, the Undertide II mouth' },
    { map_id: 'driftholm', region: 'south', optional: true, unlocked_by_flag: 'flag:q_isles_fogglass', reward: 'the island town: inn, chandlery (Deep Charm), Elder Creel, Bram Fathom (ace 70), Letters Home' },
    { map_id: 'driftholm_inn', region: 'south', optional: true }, // interior: the Lamplighters' Rest (rest point)
    { map_id: 'driftholm_chandlery', region: 'south', optional: true }, // interior: Creel & Daughter (shop)
    { map_id: 'driftholm_elder', region: 'south', optional: true }, // interior: Elder Nan Creel (the well-stair key)
    { map_id: 'driftholm_boathouse', region: 'south', optional: true }, // interior: the boathouse (a cache)
    { map_id: 'gullwrack_hut', region: 'south', optional: true }, // interior: the keeper's bothy (rest point)
    // ---- Lane E (walkthrough/10 Part III): Lowtinder & Tinderwick Bay (optional, Tidecall) ----
    { map_id: 'tinderwick_bay', region: 'south', optional: true, reward: 'the drowned roofs, two skerries, a Star-chart; the outer deep reef and the old Tinder Light (skiff)' },
    { map_id: 'lowtinder', region: 'south', optional: true, reward: 'the drowned old town: Embrift (never wild before), Grandmother Tallow, the Bell Cellar' },
    { map_id: 'lowtinder_lamphouse', region: 'south' }, // interior: Grandmother Ottery Tallow's dry upper floor (rest point)
    { map_id: 'lowtinder_school', region: 'south' }, // interior: the old lamp-school
    { map_id: 'lowtinder_school_garden', region: 'south', optional: true, reward: 'Mossmantle (never wild before) — Brightlight only' },
    { map_id: 'lowtinder_cellar', region: 'south', optional: true, reward: 'the winch-key' },
    { map_id: 'lowtinder_cellar_b2', region: 'south', optional: true, reward: 'the old town bell, a Lumen Drop, the climb up Tinderwick\'s well' },

    // Lane A — the Ashfall Shelf (walkthrough/10 Part II): the main-path leg Scarp -> Ashfall -> Galehigh
    { map_id: 'cinderwind_ashfall', region: 'north' }, // route: the slag-tip shelf, the haulers' camp (rest point)
    { map_id: 'cinderwind_kiln', region: 'north', optional: true, reward: 'Kiln Gully: the Last Pane, a Beacon charge, the Star-chart: Shardstorm; Lumecite/Pyrolith/rare Prismara' },
    // ---- Lane C2 (10-the-farlamp-isles.md Part I): the Undertide (portal caves under the isles)
    { map_id: 'undertide_i', region: 'outer', optional: true, unlocked_by_flag: 'flag:q_isles_afloat', reward: 'the tide-race lesson: the keeper\'s first page, a Hearth Coal' },
    { map_id: 'undertide_ii', region: 'outer', optional: true, unlocked_by_flag: 'flag:q_isles_afloat', reward: 'the FOG-GLASS (the Fogwall\'s buoy lane), a Lumen Drop, the second page' },
    { map_id: 'undertide_iii', region: 'outer', optional: true, unlocked_by_flag: 'flag:q_isles_wellstair', reward: 'the three-bell maze, the keeper\'s ledge (rest), Tide-bell Tuning (a Lumen Drop + the shortcut race)' },
    { map_id: 'undertide_iv', region: 'outer', optional: true, unlocked_by_flag: 'flag:q_isles_wellstair', reward: 'the Drowned Stair: a Lumen Drop, a Hearth Coal, the keeper\'s 2,000w purse, the last page' },
    { map_id: 'farlamp_drowned', region: 'outer', optional: true, unlocked_by_flag: 'flag:q_isles_wellstair', reward: 'the relight (the isles\' dawn) + FARLUME #177 (lv 68) + the store\'s Star-chart' },
  ],
  edges: [
    // ---- Tinderwick interiors (door warps, both ways) --------------------------------
    { from_map: 'tinderwick', to_map: 'tinderwick_house', via_warp: 'to_house', bidirectional: true },
    { from_map: 'tinderwick', to_map: 'tinderwick_shop', via_warp: 'to_shop', bidirectional: true },
    { from_map: 'tinderwick', to_map: 'tinderwick_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    // R8: west through the hedge gap to Duskapple Orchard (ungated, safe side area).
    { from_map: 'tinderwick', to_map: 'duskapple_orchard', via_warp: 'to_orchard', bidirectional: true },
    // 2026-10: on WEST through the orchard's far gap to Wickstead Green (the optional
    // tutorial lamp-school; ungated, safe from the very start).
    { from_map: 'duskapple_orchard', to_map: 'wickstead_green', via_warp: 'to_wickstead', bidirectional: true },
    { from_map: 'wickstead_green', to_map: 'wickstead_school', via_warp: 'enter_school', bidirectional: true },
    // The old beacon on the NE bluff — the earned first Gleam: door opens with the
    // wick-key from the Dimglass lamplighter, the floors carry wick-tender trainers,
    // and Brisa's bond-test waits in the lantern room at the top.
    { from_map: 'tinderwick', to_map: 'tinderwick_beacon_i', via_warp: 'to_beacon', requires_flag: 'flag:has_beacon_wick', bidirectional: true },
    { from_map: 'tinderwick_beacon_i', to_map: 'tinderwick_beacon_ii', via_warp: 'up_stairs', bidirectional: true },
    { from_map: 'tinderwick_beacon_ii', to_map: 'tinderwick_beacon_top', via_warp: 'up_stairs', bidirectional: true },

    // ---- Pearlmoor Quay interiors (door warps, both ways) ----------------------------
    { from_map: 'pearlmoor_quay', to_map: 'pearlmoor_shop', via_warp: 'to_shop', bidirectional: true },
    { from_map: 'pearlmoor_quay', to_map: 'pearlmoor_inn', via_warp: 'to_inn', bidirectional: true },
    { from_map: 'pearlmoor_quay', to_map: 'pearlmoor_lifting_house', via_warp: 'to_lifting_house', bidirectional: true },
    { from_map: 'pearlmoor_lifting_house', to_map: 'pearlmoor_lifting_house_b1', via_warp: 'down_stairs', bidirectional: true },
    { from_map: 'pearlmoor_quay', to_map: 'pearlmoor_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    // The Causeway Bell: the moor-gate opens with the netmender's rope (the
    // earned second-Gleam loop; Reyl's bond-test waits on flag:q_south_bell_rung).
    { from_map: 'pearlmoor_quay', to_map: 'pearlmoor_breakwater', via_warp: 'to_breakwater', requires_flag: 'flag:q_south_has_rope', bidirectional: true },
    // S5: the hill path behind the quay (always open) -> the waystone, whose
    // last word (typed) parts the trees into Paul's wood.
    { from_map: 'pearlmoor_quay', to_map: 'pearlmoor_allotment', via_warp: 'to_allotment', bidirectional: true },
    { from_map: 'pearlmoor_allotment', to_map: 'pearlmoor_wanderwood', via_warp: 'to_wood', requires_flag: 'flag:q_south_wander_word', bidirectional: true },
    // The Wanderwood's far side: one optional loop, two roads off its west edge
    // (to_far low / to_far_n high) — out one, back in the other.
    { from_map: 'pearlmoor_wanderwood', to_map: 'pearlmoor_wanderwood_far', via_warp: 'to_far', bidirectional: true },
    // ... and north out of the glade, up onto Wayward Rise and the old hotel (2026-10).
    { from_map: 'pearlmoor_wanderwood', to_map: 'wayward_rise', via_warp: 'to_rise', bidirectional: true },
    { from_map: 'wayward_rise', to_map: 'wayward_arms', via_warp: 'enter_hotel', bidirectional: true },
    { from_map: 'wayward_rise', to_map: 'paul_house_1', via_warp: 'enter_paul_house', bidirectional: true },
    { from_map: 'paul_house_1', to_map: 'paul_house_2', via_warp: 'up_stairs', bidirectional: true },
    { from_map: 'paul_house_2', to_map: 'paul_house_3', via_warp: 'up_stairs', bidirectional: true },
    // R9 "The Old Light": the west beach runs out to Lightkeeper's Point; Reyl's
    // hook (flag:q_south_bell) opens the tower door; each floor's up-stair waits on
    // its riddle (flag:oldlight_N_solved); the top's slide drops back to the Point
    // (and its chute climbs back up once the act is done).
    { from_map: 'pearlmoor_quay', to_map: 'pearlmoor_point', via_warp: 'to_point_16', bidirectional: true },
    { from_map: 'pearlmoor_point', to_map: 'pearlmoor_oldlight_1', via_warp: 'to_oldlight', requires_flag: 'flag:q_south_bell', bidirectional: true },
    { from_map: 'pearlmoor_oldlight_1', to_map: 'pearlmoor_oldlight_2', via_warp: 'up_stairs', requires_flag: 'flag:oldlight_1_solved', bidirectional: true },
    { from_map: 'pearlmoor_oldlight_2', to_map: 'pearlmoor_oldlight_3', via_warp: 'up_stairs', requires_flag: 'flag:oldlight_2_solved', bidirectional: true },
    { from_map: 'pearlmoor_oldlight_3', to_map: 'pearlmoor_oldlight_4', via_warp: 'up_stairs', requires_flag: 'flag:oldlight_3_solved', bidirectional: true },
    { from_map: 'pearlmoor_oldlight_4', to_map: 'pearlmoor_oldlight_5', via_warp: 'up_stairs', requires_flag: 'flag:oldlight_4_solved', bidirectional: true },
    { from_map: 'pearlmoor_oldlight_5', to_map: 'pearlmoor_oldlight_6', via_warp: 'up_stairs', requires_flag: 'flag:oldlight_5_solved', bidirectional: true },
    { from_map: 'pearlmoor_oldlight_6', to_map: 'pearlmoor_oldlight_top', via_warp: 'up_stairs', bidirectional: true },
    { from_map: 'pearlmoor_oldlight_top', to_map: 'pearlmoor_point', via_warp: 'slide', requires_flag: 'flag:q_south_jest_done', bidirectional: true },

    // ---- Main rim, clockwise: town -> route segment -> ... -> town -------------------
    { from_map: 'tinderwick', to_map: 'dimglass_coast', via_warp: 'to_coast', bidirectional: true },
    // The canon segment chain: Dimglass I -> the tidal flats of Dimglass II -> Pearlmoor.
    // II is the South spine's level bridge (~8-10 band + two route-trainer beats) and the
    // home of both gift-gated spurs (Gullcry Rock / Tideglass Cavern).
    { from_map: 'dimglass_coast', to_map: 'dimglass_coast_ii', via_warp: 'to_coast_ii', bidirectional: true },
    { from_map: 'dimglass_coast_ii', to_map: 'pearlmoor_quay', via_warp: 'to_quay', bidirectional: true },
    { from_map: 'pearlmoor_quay', to_map: 'saltreach_fen_i', via_warp: 'to_fen', bidirectional: true },
    { from_map: 'saltreach_fen_i', to_map: 'saltreach_fen_ii', via_warp: 'to_fen_ii', requires_ability: 'tidecall', bidirectional: true },
    { from_map: 'saltreach_fen_ii', to_map: 'lowleaf_hollow', via_warp: 'to_hollow', bidirectional: true },
    // Lowleaf interiors (door warps, both ways)
    { from_map: 'lowleaf_hollow', to_map: 'lowleaf_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    { from_map: 'lowleaf_hollow', to_map: 'lowleaf_bower', via_warp: 'to_bower', bidirectional: true },
    { from_map: 'lowleaf_hollow', to_map: 'glowmoss_deep', via_warp: 'to_deepwood', requires_ability: 'glimmerstep', bidirectional: true },
    // E4 optional spur: the dell opens once the hollow neighbour points the way
    { from_map: 'lowleaf_hollow', to_map: 'gloamwood_dell', via_warp: 'to_gloamwood', requires_flag: 'flag:q_east_georgina', bidirectional: true },
    { from_map: 'gloamwood_dell', to_map: 'georgina_cottage', via_warp: 'enter_georgina_cottage', bidirectional: true },
    { from_map: 'glowmoss_deep', to_map: 'cinderhead_mine', via_warp: 'to_mine', bidirectional: true },
    { from_map: 'cinderhead_mine', to_map: 'cinderhead_lumenary', via_warp: 'to_lumenary', bidirectional: true },
    { from_map: 'cinderhead_mine', to_map: 'cinderhead_deep', via_warp: 'to_deep', requires_ability: 'glimmerstep', bidirectional: true },
    // 2026-10: the Deep opens onto Cinderwind Scarp, the climb to the terraces
    { from_map: 'cinderhead_deep', to_map: 'cinderwind_scarp', via_warp: 'to_terraces', bidirectional: true },
    // Lane A (walkthrough/10 Part II): the Scarp's east cut is a ROCKFALL until the Galehigh
    // haulers clear it (flag:scarp_short_open = scarp_rockfall_clear OR gleam:storm, FlagStore ANY_OF)
    { from_map: 'cinderwind_scarp', to_map: 'galehigh_terraces', via_warp: 'to_terraces', requires_flag: 'flag:scarp_short_open', bidirectional: true },
    // Galehigh interiors (door warps, both ways) + the Kite-Rising Winch: the
    // skyloft is gated by the FESTIVAL flag (the earned loop, spine §5 shape #5)
    // — never by Updraft Kite (§0 rule 1; Updraft is Mira's reward).
    { from_map: 'galehigh_terraces', to_map: 'galehigh_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'galehigh_inn', via_warp: 'to_inn', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'galehigh_home', via_warp: 'to_home', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'galehigh_kitemaker', via_warp: 'to_shop', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'galehigh_skyloft', via_warp: 'to_skyloft', requires_flag: 'flag:q_north_kite_blessed', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'windward_stair_i', via_warp: 'to_stair', bidirectional: true },
    { from_map: 'windward_stair_i', to_map: 'windward_stair_ii', via_warp: 'to_stair_ii', requires_ability: 'updraft_kite', bidirectional: true },
    { from_map: 'windward_stair_ii', to_map: 'pale_vault_glacier', via_warp: 'to_glacier', bidirectional: true },
    // Pale Vault interiors (door warps, both ways) + the Lamp-Line: the
    // undercroft door takes the aurora-oil (the earned loop, spine §5 shape
    // #6) — NEVER an ability gate (§0 rule 1: Ysolde is reachable on foot).
    { from_map: 'pale_vault_glacier', to_map: 'pale_vault_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    { from_map: 'pale_vault_glacier', to_map: 'pale_vault_inn', via_warp: 'to_inn', bidirectional: true },
    { from_map: 'pale_vault_glacier', to_map: 'pale_vault_home', via_warp: 'to_home', bidirectional: true },
    { from_map: 'pale_vault_glacier', to_map: 'pale_vault_undercroft', via_warp: 'to_undercroft', requires_flag: 'flag:q_north_aurora_oil', bidirectional: true },
    { from_map: 'pale_vault_glacier', to_map: 'hushfrost_pass_i', via_warp: 'to_pass', bidirectional: true },
    { from_map: 'hushfrost_pass_i', to_map: 'hushfrost_pass_ii', via_warp: 'to_pass_ii', requires_ability: 'emberward', bidirectional: true },
    { from_map: 'hushfrost_pass_ii', to_map: 'sunken_solarium', via_warp: 'to_solarium', bidirectional: true },
    // The Solar hall is starter-gated like every Lumenary door (NEVER Sunsketch — §0 rule 1).
    { from_map: 'sunken_solarium', to_map: 'sunken_solarium_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    { from_map: 'sunken_solarium', to_map: 'sunvault_climb_i', via_warp: 'to_climb', bidirectional: true },
    { from_map: 'sunvault_climb_i', to_map: 'sunvault_climb_ii', via_warp: 'to_climb_ii', requires_ability: 'sunsketch', bidirectional: true },
    // (2026-10, 09-the-wild-ways §2 S: the climb is four maps now — climb_ii -> the Gilt
    // Face -> the Sun Ledges -> Nightreach; the edges live in the Wild Ways block below)
    // The Lunar hall is starter-gated like every Lumenary door (NEVER Emberward/Starreach — §0 rule 1).
    { from_map: 'nightreach_observatory', to_map: 'nightreach_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    { from_map: 'nightreach_observatory', to_map: 'nightreach_inn', via_warp: 'to_inn', bidirectional: true },
    { from_map: 'nightreach_observatory', to_map: 'nightreach_home', via_warp: 'to_home', bidirectional: true },
    // Coldfog detour (off the hub), then onward to Nightreach from its blighted side.
    { from_map: 'coldfog_marches_i', to_map: 'coldfog_marches_ii', via_warp: 'to_marsh_ii', requires_ability: 'emberward', bidirectional: true },
    { from_map: 'coldfog_marches_ii', to_map: 'nightreach_observatory', via_warp: 'to_observatory_fog', requires_ability: 'emberward', bidirectional: true },

    // ---- Optional spurs (dead-ends with rewards; several need a later gift) ----------
    { from_map: 'dimglass_coast_ii', to_map: 'gullcry_rock', via_warp: 'to_gullcry', requires_ability: 'tidecall', bidirectional: true },
    { from_map: 'dimglass_coast_ii', to_map: 'tideglass_cavern', via_warp: 'to_tideglass', requires_ability: 'glimmerstep', bidirectional: true },
    // Dimglass I's launch-era cliff-mouth tease is a real second door into the
    // cavern (the shipped warp, now declared); the segments meet at the mouth.
    { from_map: 'dimglass_coast', to_map: 'tideglass_cavern', via_warp: 'to_tideglass', requires_ability: 'glimmerstep', bidirectional: true },
    // ---- The Three Hours (walkthrough/07-the-three): one annex per quadrant ----------
    // Site I: the Gallery under Tideglass — the stair seam opens when the
    // Lampwright's Relay completes (lens C).
    { from_map: 'tideglass_cavern', to_map: 'tideglass_gallery', via_warp: 'stair_down', requires_flag: 'flag:three_dusk_lens_c', bidirectional: true },
    // Site II: the Hourfold off the glacier's Emberward deep-ice fold —
    // sealed until Ysolde hands over the Vigil Snuffer.
    { from_map: 'pale_vault_glacier', to_map: 'pale_vault_hourfold', via_warp: 'to_hourfold', requires_ability: 'emberward', requires_flag: 'flag:three_mid_snuffer', bidirectional: true },
    // Site III: the Unrisen Stair off the Solarium's deepest fold — sealed
    // until the First-Light Phial is poured into the basin.
    { from_map: 'sunken_solarium', to_map: 'unrisen_stair', via_warp: 'to_unrisen', requires_ability: 'sunsketch', requires_flag: 'flag:three_dawn_poured', bidirectional: true },
    { from_map: 'saltreach_fen_ii', to_map: 'sunkbell_shallows', via_warp: 'to_sunkbell', requires_ability: 'tidecall', bidirectional: true },
    { from_map: 'glowmoss_deep', to_map: 'glowmoss_deep_b1f', via_warp: 'ladder_down', bidirectional: true },
    { from_map: 'glowmoss_deep_b1f', to_map: 'spore_grotto', via_warp: 'to_grotto', requires_ability: 'glimmerstep', bidirectional: true },
    // Cinderhead Deep is a 3-floor ladder maze (the Descent Vigil); the vigil-lamp sits on b2f.
    { from_map: 'cinderhead_deep', to_map: 'cinderhead_deep_b1f', via_warp: 'ladder_down', bidirectional: true },
    { from_map: 'cinderhead_deep_b1f', to_map: 'cinderhead_deep_b2f', via_warp: 'ladder_down', bidirectional: true },
    { from_map: 'cinderhead_deep', to_map: 'crystoll_vault', via_warp: 'to_crystoll', requires_ability: 'starreach', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'wind_eye', via_warp: 'to_windeye', requires_ability: 'updraft_kite', bidirectional: true },
    { from_map: 'windward_stair_ii', to_map: 'thunderroost', via_warp: 'to_roost', requires_ability: 'updraft_kite', bidirectional: true },
    { from_map: 'hushfrost_pass_ii', to_map: 'aurora_hollow', via_warp: 'to_aurora', requires_ability: 'emberward', bidirectional: true },
    { from_map: 'sunvault_climb_ii', to_map: 'helia_vault', via_warp: 'to_helia', requires_ability: 'sunsketch', bidirectional: true },
    { from_map: 'coldfog_marches_i', to_map: 'drownlight_beacon', via_warp: 'to_beacon', requires_ability: 'emberward', bidirectional: true },
    { from_map: 'coldfog_marches_ii', to_map: 'hollowfen_stillworks', via_warp: 'to_stillworks', requires_ability: 'glimmerstep', bidirectional: true },
    { from_map: 'penumbra_ring', to_map: 'starwell', via_warp: 'to_starwell', requires_ability: 'starreach', bidirectional: true },

    // ---- Lanternway: the roads that really touch the hub, + the far valleys' lanes --
    // 2026-10 geometry fix: only Tinderwick (the lane) and the bay road home
    // (Saltreach Fen I -> Wrackline -> Sounding Cave -> Lanternfall) WALK to the
    // hub. Lowleaf, Galehigh and Nightreach sit far up the mountain's flanks:
    // their lanes end at Lantern-car stations, and the car (script.lantern_car,
    // a ride, not a warp — so not a graph edge, like waystone TRAVEL) runs each
    // line once that valley's Gleam is relit. The hub-side gate still waits on
    // the town's own Gleam; the ride down from a valley always runs.
    { from_map: 'tinderwick', to_map: 'lanternway_tinderwick', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'lanternway_tinderwick', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'saltreach_fen_i', to_map: 'wrackline_path', via_warp: 'to_wrackline', bidirectional: true },
    { from_map: 'wrackline_path', to_map: 'sounding_cave', via_warp: 'to_cave', bidirectional: true },
    { from_map: 'sounding_cave', to_map: 'lanternfall_road', via_warp: 'to_lanternfall', bidirectional: true },
    { from_map: 'lanternfall_road', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'lowleaf_hollow', to_map: 'lanternway_lowleaf', via_warp: 'to_crossroads', bidirectional: true },
    // the Under-Lane's two mouths: lower road in, upper shelf out (the
    // interleave — the only way UP the spoke's bank; the ledge hops back down)
    { from_map: 'lanternway_lowleaf', to_map: 'lanternway_undercut', via_warp: 'to_undercut', bidirectional: true },
    { from_map: 'lanternway_lowleaf', to_map: 'lanternway_undercut', via_warp: 'to_undercut_high', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'lanternway_galehigh', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'nightreach_observatory', to_map: 'lanternway_nightreach', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'vesper_crossroads', to_map: 'crossroads_inn', via_warp: 'enter_inn', bidirectional: true },

    // ---- Late shortcuts: open from the far side, then permanently re-link to the hub --
    { from_map: 'windward_stair_ii', to_map: 'galehigh_terraces', via_warp: 'shortcut_galehigh', requires_flag: 'flag:shortcut_windward', bidirectional: true },
    { from_map: 'cinderhead_deep', to_map: 'vesper_crossroads', via_warp: 'shortcut_crossroads', requires_flag: 'flag:shortcut_mine', bidirectional: true },

    // ---- Hub -> centre, gated by the progressive crown flags -------------------------
    { from_map: 'vesper_crossroads', to_map: 'umbral_approach', via_warp: 'to_penumbra', requires_flag: 'flag:hub_unlocked', bidirectional: true },
    { from_map: 'umbral_approach', to_map: 'penumbra_ring', via_warp: 'to_penumbra', bidirectional: true },
    { from_map: 'penumbra_ring', to_map: 'umbral_spire', via_warp: 'to_spire', requires_ability: 'starreach', bidirectional: true },
    // The Spire is a 4-floor ascent (§2a Spire tier): gatehouse -> null-works ->
    // high gallery -> summit, joined by mutual ladder pairs. The high gallery's
    // rest-ledge kindles the open core's hoist (flag:spire_shaft, set by the
    // mandatory breather band) — the f3 <-> gatehouse shaft pair is the climb's
    // return compressor and closes the central region's loop.
    { from_map: 'umbral_spire', to_map: 'umbral_spire_f2', via_warp: 'ladder_up', bidirectional: true },
    { from_map: 'umbral_spire_f2', to_map: 'umbral_spire_f3', via_warp: 'ladder_up', bidirectional: true },
    { from_map: 'umbral_spire_f3', to_map: 'umbral_spire_summit', via_warp: 'ladder_up', bidirectional: true },
    { from_map: 'umbral_spire_f3', to_map: 'umbral_spire', via_warp: 'shaft_down', requires_flag: 'flag:spire_shaft', bidirectional: true },
    // The dawn road leaves from the SUMMIT (where flag:dawn is set) — the
    // post-game hand-off; dawnstead is the post-game writer's map.
    { from_map: 'umbral_spire_summit', to_map: 'dawnstead', via_warp: 'to_dawn', requires_flag: 'flag:dawn', bidirectional: true },

    // ---- The Starfall Vigils: each reading opens ONE host scar (06-postgame master list)
    { from_map: 'tinderwick', to_map: 'vigil_hearthfall', via_warp: 'to_vigil_hearth', requires_flag: 'flag:vigil_reading_1', bidirectional: true },
    { from_map: 'spore_grotto', to_map: 'vigil_grovefall', via_warp: 'to_vigil_grove', requires_flag: 'flag:vigil_reading_2', bidirectional: true },
    { from_map: 'thunderroost', to_map: 'vigil_stormfall', via_warp: 'to_vigil_storm', requires_flag: 'flag:vigil_reading_3', bidirectional: true },
    { from_map: 'sunvault_climb_ii', to_map: 'vigil_sunfall', via_warp: 'to_vigil_sun', requires_flag: 'flag:vigil_reading_4', bidirectional: true },
    { from_map: 'coldfog_marches_ii', to_map: 'vigil_murkfall', via_warp: 'to_vigil_murk', requires_flag: 'flag:vigil_reading_5', bidirectional: true },
    // ---- THE WILD WAYS (09-the-wild-ways.md) — one block per area lane
    // the Wick-Run (A): downhill only (chutes can't be climbed); the Tallow Lift is a ride, not an edge
    { from_map: 'sunvault_climb_i', to_map: 'wickrun_crest', via_warp: 'to_wickrun', bidirectional: true },
    { from_map: 'wickrun_crest', to_map: 'wickrun_chute', via_warp: 'to_chute', requires_flag: 'flag:wickrun_riding', bidirectional: true },
    { from_map: 'wickrun_chute', to_map: 'wickrun_trestles', via_warp: 'to_trestles', bidirectional: false },
    { from_map: 'wickrun_trestles', to_map: 'wickrun_traverse', via_warp: 'to_traverse', bidirectional: false },
    { from_map: 'wickrun_traverse', to_map: 'wickrun_lower', via_warp: 'to_lower', bidirectional: false },
    { from_map: 'wickrun_lower', to_map: 'wickrun_foot', via_warp: 'to_foot', bidirectional: false },
    { from_map: 'wickrun_foot', to_map: 'pearlmoor_point', via_warp: 'to_point', bidirectional: true },
    // the Mirelights (B): Ansel's ferry is an honest edge link held by his flag
    { from_map: 'saltreach_fen_i', to_map: 'mirelight_landing', via_warp: 'to_mirelight', requires_flag: 'flag:mirelight_ferry', bidirectional: true },
    { from_map: 'mirelight_landing', to_map: 'mirelight_glassmere', via_warp: 'to_glassmere', bidirectional: true },
    { from_map: 'mirelight_glassmere', to_map: 'mirelight_chapel', via_warp: 'to_chapel', bidirectional: true },
    { from_map: 'mirelight_chapel', to_map: 'lanthorne_hollow', via_warp: 'to_hollow', requires_flag: 'flag:mirelight_tobin_found', bidirectional: true },
    // the Rimeway (C): open from Pale Vault (North era); the Rime Gate is lifted from the Descent (West era)
    { from_map: 'pale_vault_glacier', to_map: 'rimeway_ascent', via_warp: 'to_rimeway', bidirectional: true },
    { from_map: 'rimeway_ascent', to_map: 'rimeway_fold', via_warp: 'to_fold', bidirectional: true },
    { from_map: 'coldfog_marches_ii', to_map: 'rimeway_descent', via_warp: 'to_rimeway', bidirectional: true },
    { from_map: 'rimeway_fold', to_map: 'rimeway_descent', via_warp: 'to_descent', requires_flag: 'flag:rime_gate_open', bidirectional: true },
    { from_map: 'rimeway_fold', to_map: 'reckoning_works', via_warp: 'to_works', bidirectional: true },
    // the Old Seams (D): floors stacked by ladders (portals — they never touch surface geometry)
    { from_map: 'cinderhead_mine', to_map: 'old_seams_i', via_warp: 'to_old_seams', requires_flag: 'flag:old_seams_open', bidirectional: true },
    { from_map: 'old_seams_i', to_map: 'old_seams_ii', via_warp: 'ladder_down', bidirectional: true },
    { from_map: 'old_seams_ii', to_map: 'old_seams_iii', via_warp: 'ladder_down', bidirectional: true },
    { from_map: 'old_seams_iii', to_map: 'emberroot_heart', via_warp: 'to_heart', requires_flag: 'flag:lamplight_starlight', bidirectional: true },
    // Sunvault Climb rebuild (S): the climb is four maps (the main path, ungated past the vines)
    { from_map: 'sunvault_climb_ii', to_map: 'sunvault_climb_iii', via_warp: 'to_climb_iii', bidirectional: true },
    { from_map: 'sunvault_climb_iii', to_map: 'sunvault_climb_iv', via_warp: 'to_climb_iv', bidirectional: true },
    { from_map: 'sunvault_climb_iv', to_map: 'nightreach_observatory', via_warp: 'to_observatory', bidirectional: true },
    // ---- THE FARLAMP ISLES (Lane C1): the launches, the sea seams, Driftholm's doors
    // (the three cave mouths' edges are declared bidirectionally by Lane C2)
    { from_map: 'pearlmoor_point', to_map: 'farlamp_sound', via_warp: 'to_sound_6', requires_flag: 'flag:q_isles_afloat', bidirectional: true },
    { from_map: 'wickrun_foot', to_map: 'farlamp_shelfwater', via_warp: 'to_shelf_9', requires_flag: 'flag:q_isles_afloat', bidirectional: true },
    { from_map: 'farlamp_sound', to_map: 'farlamp_shelfwater', via_warp: 'to_shelf_0', requires_ability: 'deepdive', bidirectional: true },
    { from_map: 'farlamp_sound', to_map: 'farlamp_gullwrack', via_warp: 'to_gullwrack_0', requires_ability: 'deepdive', bidirectional: true },
    { from_map: 'farlamp_shelfwater', to_map: 'farlamp_fogwall', via_warp: 'to_fogwall_0', requires_ability: 'deepdive', bidirectional: true },
    { from_map: 'farlamp_shelfwater', to_map: 'farlamp_kelpcrown', via_warp: 'to_kelpcrown_0', requires_ability: 'deepdive', bidirectional: true },
    { from_map: 'farlamp_gullwrack', to_map: 'farlamp_kelpcrown', via_warp: 'to_kelpcrown_0', requires_ability: 'deepdive', bidirectional: true },
    { from_map: 'farlamp_fogwall', to_map: 'driftholm', via_warp: 'to_driftholm_16', requires_flag: 'flag:q_isles_fogglass', bidirectional: true },
    { from_map: 'driftholm', to_map: 'driftholm_inn', via_warp: 'enter_inn_2', bidirectional: true },
    { from_map: 'driftholm', to_map: 'driftholm_chandlery', via_warp: 'enter_chandlery', bidirectional: true },
    { from_map: 'driftholm', to_map: 'driftholm_elder', via_warp: 'enter_elder', bidirectional: true },
    { from_map: 'driftholm', to_map: 'driftholm_boathouse', via_warp: 'enter_boathouse_2', bidirectional: true },
    { from_map: 'farlamp_gullwrack', to_map: 'gullwrack_hut', via_warp: 'to_hut', bidirectional: true },
    // ---- Lane E (walkthrough/10 Part III): Tinderwick Bay + Lowtinder, the town under the bay
    // home's south shore swims off its east columns into the bay (Tidecall); the bay's east
    // edge swims into Lowtinder; the Bell Cellar is two floors under the lamp-house. The
    // cellar's far end climbs Tinderwick's well (a one-way `travel`, not an edge).
    { from_map: 'tinderwick', to_map: 'tinderwick_bay', via_warp: 'to_bay_21', requires_ability: 'tidecall', bidirectional: true },
    { from_map: 'tinderwick_bay', to_map: 'lowtinder', via_warp: 'to_lowtinder_15', requires_ability: 'tidecall', bidirectional: true },
    { from_map: 'lowtinder', to_map: 'lowtinder_lamphouse', via_warp: 'to_lamphouse', bidirectional: true },
    { from_map: 'lowtinder', to_map: 'lowtinder_school', via_warp: 'to_school', bidirectional: true },
    { from_map: 'lowtinder_school', to_map: 'lowtinder_school_garden', via_warp: 'to_garden', requires_flag: 'flag:lamplight_brightlight', bidirectional: true },
    { from_map: 'lowtinder', to_map: 'lowtinder_cellar', via_warp: 'to_cellar', bidirectional: true },
    { from_map: 'lowtinder_cellar', to_map: 'lowtinder_cellar_b2', via_warp: 'ladder_down', bidirectional: true },

    // Lane A — the Ashfall Shelf (walkthrough/10 Part II)
    { from_map: 'cinderwind_scarp', to_map: 'cinderwind_ashfall', via_warp: 'to_ashfall', bidirectional: true },
    { from_map: 'cinderwind_ashfall', to_map: 'galehigh_terraces', via_warp: 'to_terraces', bidirectional: true },
    { from_map: 'cinderwind_ashfall', to_map: 'windward_stair_i', via_warp: 'to_windward', requires_ability: 'updraft_kite', bidirectional: true },
    { from_map: 'cinderwind_ashfall', to_map: 'cinderwind_kiln', via_warp: 'to_kiln', requires_ability: 'updraft_kite', bidirectional: true },
    // ---- Lane C2: the Undertide. The cave side owns these surface links (C1's surface
    // warps are the far ends; one bidirectional edge each, never a second reverse edge).
    { from_map: 'undertide_i', to_map: 'farlamp_gullwrack', via_warp: 'to_gullwrack', bidirectional: true },
    { from_map: 'undertide_ii', to_map: 'farlamp_kelpcrown', via_warp: 'to_kelpcrown', bidirectional: true },
    { from_map: 'undertide_iii', to_map: 'driftholm', via_warp: 'to_driftholm', requires_flag: 'flag:q_isles_wellstair', bidirectional: true },
    { from_map: 'undertide_i', to_map: 'undertide_ii', via_warp: 'ladder_down', bidirectional: true },
    { from_map: 'undertide_iii', to_map: 'undertide_iv', via_warp: 'ladder_down', bidirectional: true },
    { from_map: 'undertide_iv', to_map: 'farlamp_drowned', via_warp: 'ladder_down', bidirectional: true },
  ],
  hub: {
    map_id: 'vesper_crossroads',
    approaches: [
      { region: 'south', opens_flag: 'flag:crown_south' },
      { region: 'east', opens_flag: 'flag:crown_east' },
      { region: 'north', opens_flag: 'flag:crown_north' },
      { region: 'west', opens_flag: 'flag:crown_west' },
    ],
  },
};
