# World data

The typed PixelKin **map & world schema** — our own JSON format (not Tiled), parsed
directly into these interfaces.

- `types.ts` — `MapDefinition` and its parts (layers, warps, triggers, encounter zones,
  NPCs, ability gates) plus `WorldSnapshot` for saves.
- `graph.ts` — `WorldGraph` + the `VESPERHOLM_GRAPH` instance (map connectivity, ability-/
  flag-gated edges, the four-way central-hub unlock).
- `maps.ts` — `MAP_REGISTRY`: area id → runtime asset paths (map JSON, tilesets, music).
- `examples.ts` — a typed example map that doubles as a compile-time schema check.

The design rationale, layer/tile-property conventions, map-size caps, and the end-to-end
area-authoring flow are documented in **[`../../../../docs/world/README.md`](../../../../docs/world/README.md)**.
The world and story this models are in `docs/world/story-bible.md` and `docs/world/atlas.md`.
