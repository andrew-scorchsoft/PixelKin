# PixelKin — Interior Design Rules (binding)

How every building interior (home, shop, inn, Lumenary chamber, boat cabin) is
drawn and laid out. The bar is **top-down SNES-era interiors** — the cosy,
enclosed, lamp-lit rooms of a 16-bit handheld RPG: a room that reads *instantly*
as its purpose, with a sense of walls that have **height**, a patterned floor, a
bordered rug staging the action, furniture lining the walls, and one warm focal
point. This doc is the acceptance bar; the visual tileset spec lives in
`docs/art-style.md` (Per-type spec **I**), the layout/size rules in
`docs/world/level-design.md` (§2, §7.2). Read those too.

> **Originality:** inspired by the genre's interiors, a copy of nothing. Original
> furniture, motifs, palette (see `VISION.md`). Never reference another brand.

## 0. The one rule that fixes everything: walls have a visible FACE

The current failure mode is a "flat plan" — a single top-down outline of wall
tiles around a flat floor, which reads as a picnic blanket, not a room. Fix it
with the genre's enclosure convention:

- An interior is a **rectangular room framed by walls on all four sides**, drawn
  in the same gentle top-down-with-a-hint-of-front projection as the overworld.
- **The TOP wall is two tiles tall:** a `wall_cap` row (the cornice / top edge)
  *above* a `wall_face` row (the visible vertical surface — panelling, plaster,
  or stone) — *then* the floor begins. You should see the wall, not just its top.
- **Side walls** show one tile of `wall_face`. **Corners** carry the face into
  the join.
- **The floor fills the room** below/inside the walls — walkable, and **patterned**
  (subtle tiled brick / boards / stone), never one flat colour.
- The **bottom wall** is one tile, broken by a single **doormat** (the exit) at
  centre-bottom. **Corner posts/pillars** anchor the four corners.

If a render looks like furniture sitting on an open field, the wall-face is
missing — that is a hard fail.

## 1. The interior tileset (`interior_set`)

One shared 16px interior tileset, packed like any other (`pack_tileset.py` →
`*.tileset.json` sidecar with per-tile `role`/`collides`). Minimum vocabulary:

| Tile | role | collides | notes |
|------|------|----------|-------|
| `wall_cap_n` | wall | yes | top cornice row |
| `wall_face_n` | wall | yes | top vertical face (panel/stone) |
| `wall_face_w`, `wall_face_e` | wall | yes | side faces |
| `wall_corner_nw/ne/sw/se` | wall | yes | faced corners / posts |
| `wall_s` | wall | yes | bottom wall |
| `floor_fill` (+1–2 variants) | floor | no | patterned, walk-on |
| `doormat` | door | no | the exit tile, walk-on |
| `window` | wall | yes | sits on `wall_face_n`; warm or night glass |
| `rug_c/edge/corner` (optional) | floor | no | bordered rug as tiles **or** an object |

Theme accents come from **two register variants** of floor + wall-face:
**warm wood/plaster** (homes, shops, inns) and **cool stone/dark-panel**
(Lumenaries). Same kit, different accent tiles.

Big props are **objects** (`assets/tilesets/interior/objects/<stem>.png` →
`pack_objects.py` → key `interior_<stem>`), not tiles: `interior_altar`,
`interior_counter`, `interior_bed`, `interior_table`, `interior_shelf`,
`interior_bookcase`, `interior_barrels`, `interior_brazier`, `interior_hearth`,
`interior_rug` (if not done as tiles). Objects get clean transparency (composite
over a checkerboard — no white/halo) and a dark-ink outline, top-left light.

## 2. Room types — floor/wall accent + the focal point

Every interior has **one focal point at top-centre** that the eye lands on when
the player walks in from the bottom door:

- **Home** — warm wood floor, plaster walls. Focal: a **hearth**. Dress with a
  bed, table+stools, bookcase; a small rug. Cosy, a little asymmetric.
- **Shop** — wood/tile floor. Focal: a **counter** spanning near the top with the
  shopkeeper behind it. Wares on **shelves**/`barrels` along the walls, a bordered
  rug staging the goods. Symmetric, tidy.
- **Inn** — tile floor. **Tables**+stools in the room, a row of **beds** along one
  wall, a hearth/brazier. Warm, busy-but-clear.
- **Lumenary (temple)** — **stone floor + dark panelled walls** (the cool
  register). Focal: a raised **altar / lamp-shrine** at top-centre on a **runner
  rug** aisle; **braziers** flank the aisle; **banners** on the top wall-face; the
  **Lampwarden** stands at the altar. Must read as a small shrine — *never* a cabin.
- **Boat cabin / small** — tight wood room, a bunk, a crate, one lantern.

## 3. Layout rules (binding)

1. **Single entrance**: one `doormat` at centre-bottom. Its inside tile *and* the
   tile above it are walkable; the player returns/spawns there facing up.
2. **Clear central lane**: a walkable path from the doormat to **every** NPC and
   trigger. Never box the player in or strand an NPC behind solids.
3. **Furniture lines the perimeter**; keep the centre open and let a **rug**
   define it. Don't scatter props mid-floor with no anchor.
4. **One focal point** (hearth / counter / altar) at **top-centre**.
5. **Warm lighting**: ≥2 wall sconces/braziers; put **windows** on the top
   wall-face for depth and a sense of outside.
6. **Symmetry** for civic rooms (Lumenary, shop); **cosy asymmetry** for homes.
7. **Size** (per `level-design.md` §2): small interior **10×8 → 16×12**;
   Lumenary / large shop **16×12 → 20×16**. Door on the **bottom edge**.
8. **Collision**: walls + furniture collide; floor/rug/doormat walk-on. After
   placing everything, **verify** every warp-landing tile, every NPC `at` tile,
   and the lane between the door and each of them is walkable.

## 4. Build & QA pattern

- Tileset: paint masters → `pack_tileset.py` → `interior_set` (+ sidecar).
  Furniture objects → `pack_objects.py`.
- Author each interior in a build script (e.g. `tools/maps/build_interiors.py`)
  the way the overworld builders work; interiors paint the wall-frame + floor
  directly (no terrain-autotile pass needed) and place furniture objects.
- **QA every interior** with `render_map.py <id> --output … --scale 5` and read
  the PNG against this doc: visible wall-face (height), patterned floor, a
  bordered rug, perimeter furniture, one top-centre focal point, a single bottom
  doormat, ≥2 lights, and clear walkable lanes. If it looks like a flat field, the
  wall-face is missing — redo it.
