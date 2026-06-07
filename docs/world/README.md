# PixelKin — World Design Docs

The conceptual framework every PixelKin area, kin, and asset hangs off. Start here,
then read in order:

1. **[`story-bible.md`](./story-bible.md)** — the region (*Vesperholm*), the story, the
   Lumenary/Gleam ("arena/badge") concept, the eight Lampwardens, the Lantern Gifts
   ("field moves"), the antagonist (the Hollowing), the celestial-calendar spine, and the
   originality/copyright audit.
2. **[`atlas.md`](./atlas.md)** — the world map: the connectivity graph, the central-hub
   lock/unlock, which Lantern Gift gates each path, and per-area **graphics direction**,
   **`generate-midi` music brief**, **kin**, and **encounter terrain**.
3. **[`music-direction.md`](./music-direction.md)** — the soundtrack plan: **2–3
   auditionable music options for every area and route**, each a ready `generate-midi`
   brief. The cohesion rules behind them (the *Vesper motif*, per-element sonic
   signatures, the voice/era policy, the dusk→dawn key arc, and how we study the
   cartridge era without copying it) live in the skill's
   [`pixelkin-soundtrack.md`](../../.claude/skills/generate-midi/references/pixelkin-soundtrack.md).
4. **[`level-design.md`](./level-design.md)** — the **binding map & level-design guide**:
   the 15×10-window rules, per-`MapKind` sizes, the readability/guidance toolkit, the
   starter-town & tutorial-route patterns, encounter-design rules, layer discipline, the
   required tile vocabulary, annotated layout sketches (Tinderwick / house / Dimglass
   Coast), and the pre-/post-flight authoring checklist. Read before authoring any map.
5. This file — the **data + authoring conventions** the engine and the asset pipeline use.

> Everything here is original to PixelKin per [`../../VISION.md`](../../VISION.md):
> inspired by the monster-collecting genre, a copy of nothing.

---

## The map data model (custom PixelKin schema)

Maps are **our own typed JSON** (not Tiled), parsed directly into the interfaces in
[`../../src/game/data/world/types.ts`](../../src/game/data/world/types.ts) and
[`graph.ts`](../../src/game/data/world/graph.ts). JSON keys are **snake_case**, mirrored by
a typed TS interface — matching the existing creature `metadata.json` convention. A worked
example lives at [`../../public/assets/maps/tinderwick.json`](../../public/assets/maps/tinderwick.json).

### Layers (classic GBC/GBA stacking)

A map renders layers in this order, with the player sprite slotted between `deco` and
`above`:

| Layer | Role | Renders | Purpose |
|-------|------|---------|---------|
| `base` | ground | below player | grass, paths, water, floors |
| `deco` (repeatable: `deco_2`…) | objects on ground | below player | flowers, signs, fences, lower halves of trees/buildings |
| **player** | — | between | the player & NPCs |
| `above` | overlay | **above** player | tree-tops, roofs, bridges, archways the player walks **under** |

Each layer is row-major `data: number[]` of tile **gids** referencing the map's
`tilesets[]`.

### Collision, ability gates & encounters are *tile properties*, not painted layers

Collision and gating live on the **tileset metadata** (emitted by the packer, see below),
so they're authored once per tileset and reused across every map:

- `collides: true` — the tile is solid (walls, deep water by default, cliffs).
- `requires_ability: <AbilityId>` — solid **until** the player has that Lantern Gift
  (e.g. deep-water tiles need `tidecall`; dark-cave tiles need `glimmerstep`). The engine
  toggles these passable when the ability is earned.
- `encounter_terrain: tall_grass | water | cave | sand` — marks a tile as wild terrain;
  `EncounterZone` rectangles in the map then attach a weighted table to a region.

Two complementary gating mechanisms (the surf/cut/flash equivalents):

- **Tile-level** — `requires_ability` tiles + `AbilityGate` (in the map JSON) for
  per-tile effects like `remove_tile` (a cleared path that stays cleared via a flag).
- **Edge-level** — `WorldEdge.requires_ability` / `requires_flag` in the world graph
  controls **map-to-map connectivity**; this is how the four-way central hub opens (the
  `crown_*` / `hub_unlocked` flags from [`atlas.md`](./atlas.md)) and how new regions
  appear as Gifts are earned.

### Map-size convention

The viewport is **15×10 tiles** (240×160 at `TILE_SIZE` 16).

- Overworld towns/routes: **soft cap 64×64 tiles** (~4×6 screens — generous for a GBC/GBA
  route).
- Interiors (houses, boats, small caves): **~32×32 tiles**, often single-screen-ish.
- **Absolute cap 128×128 tiles.** Larger regions are composed from multiple connected maps
  via the world graph — never one giant map (keeps camera bounds, encounter tables, and
  warp reasoning local).

### Route structure

Towns are joined by **routes**, and routes carry the wild encounters and traversal gating
(full network in [`atlas.md`](./atlas.md) §3). Four conventions, all expressed in the world
graph (`src/game/data/world/graph.ts`):

- **Segmented chains** — a main route is two named maps (e.g. `dimglass_coast_i` /
  `_ii`), the gift-gate sitting on the segment boundary.
- **Spurs** — optional dead-end maps flagged `optional: true` on their `AreaNode`, usually
  gated by a *later* Gift so the player backtracks for the reward.
- **Landmarks** — bigger optional micro-dungeons (also `optional: true`) with a unique kin.
- **Shortcuts** — edges gated by a `flag:shortcut_*` that open from the far side and
  permanently re-link a route to the hub.

Rewards stay in-schema: a rare kin is a low-weight `EncounterZone` entry (or a static
`EventTrigger`), a hidden item is an `EventTrigger` (`kind: 'script'`) that sets a flag.

### World state & saves

All world progress (current map, player tile/facing, earned abilities, set flags) is a
`WorldSnapshot` persisted **only** through the platform seam
([`../../src/platform/storage.ts`](../../src/platform/storage.ts), key `world`). Nothing
else touches `localStorage` — that's what lets the Capacitor mobile port swap the backend
without touching game logic.

---

## Authoring a new area (end-to-end)

1. **Design** the area in [`atlas.md`](./atlas.md): kind, region, gate, graphics, music
   brief, kin, terrain.
2. **Tileset** — generate a cohesive 16×16 tile set with the `generate-sprite-sheet` skill
   (`--area <name> --palette <…>`, anchor-tile-first then reference-seeded siblings), then
   run `pack_tileset.py` to emit the atlas PNG + tileset metadata JSON into
   `public/assets/tilesets/`. Derive `--palette` from
   [`../../assets/tilesets/world-palette.json`](../../assets/tilesets/world-palette.json)
   so areas stay cohesive across the world.
3. **Music** — feed the area's music brief to the `generate-midi` skill; write the mp3 loop
   to `public/assets/audio/music/` and key it to the map's `music` field.
4. **Map JSON** — author `public/assets/maps/<area>.json` to the `MapDefinition` schema
   (layers, warps, triggers, encounters, npcs, gates).
5. **Register** the map in [`../../src/game/data/world/maps.ts`](../../src/game/data/world/maps.ts)
   and wire its connections into the world graph in
   [`graph.ts`](../../src/game/data/world/graph.ts).
6. Add new kin/dialogue to their data registries as needed.

A new area is therefore **content (data + assets), not new engine code** — the data-driven
principle from [`../../src/game/data/README.md`](../../src/game/data/README.md).

---

## Status & what's next

- **Done (this pass):** the conceptual framework (story bible + atlas), the custom map/tile
  **schema** in `src/game/data/world/`, an example map, and the tileset-generation skill
  extension.
- **Designed, not yet built (follow-up):** the runtime `WorldScene` (layer rendering, grid
  16px movement, camera-follow, `MapLoader`, `WorldState`, encounter/warp/trigger systems)
  and the original **type chart** (Ember/Tide/Verdant/Stone/Storm/Frost/Solar/Lunar/Light/
  Dark) implied by the eight Lampwardens.
