# PixelKin — Interior Design Rules (binding)

How every building interior (home, shop, inn, Lumenary chamber, boat cabin) is
drawn and laid out. The bar is **top-down SNES-era interiors** — the cosy,
enclosed, lamp-lit rooms of a 16-bit handheld RPG: a room that reads *instantly*
as its purpose, with walls that have **height**, a patterned floor, **rooms
within the room**, furniture that stands **against** the walls, and one warm
focal point. This doc is the acceptance bar; the visual tileset spec lives in
`docs/art-style.md` (Per-type spec **I**), the layout/size rules in
`docs/world/level-design.md` (§2, §7.2). Read those too.

> **Originality:** inspired by the genre's interiors, a copy of nothing. Original
> furniture, motifs, palette (see `VISION.md`). Never reference another brand.

## 0. The two rules that fix everything

**A. Walls have a visible FACE.** An interior is a rectangular room framed by
walls on all four sides: the TOP wall is **two tiles tall** — a `wall_cap` row
(the dark wall-top band) *above* a `wall_face` row (the visible vertical
surface: plaster/wainscot or coursed stone) — then the patterned floor begins.
Side/bottom walls are the band with a lit inner lip; corners turn the lip
unbroken; one **doormat** breaks the bottom wall at centre. If a render looks
like furniture on an open field, the face is missing — hard fail.

**B. An interior is a COMPOSITION, not a furniture square.** One open box with
props around the rim is the rejected first-generation look. Every interior
bigger than a boat cabin carries **at least one internal partition** (the same
cap/face wall system, with a door gap or an open south end) shaping rooms
within the room: the cottage's bed nook, the shop's storeroom, the inn's bunk
room, the Lumenary's side niches. The partition is what makes two homes feel
like two *different* homes.

## 1. The kits

**Walls/floors** — two 13-tile register variants drawn by
`tools/maps/build_interior_walls.py`: **warm** `interior_set` (wood/plaster —
homes, shops, inns) and **cool** `interior_stone_set` (stone/dark panel —
Lumenaries). Tile roles: cap band (4 dirs + 4 corners), north face, window
(warm) / banner (cool) insets, patterned floor + variant, doormat/runner.

**Furniture** — the DRAWN kit in `tools/maps/interiorforge.py` (the gbaforge of
furniture; AI generation is retired for interiors — it produced small,
half-isometric props that floated off the walls). Two mount classes, packed by
`pack_objects.py` to `interior_<stem>` keys:

| Class | Pieces | Projection & placement |
|-------|--------|------------------------|
| **WALL-MOUNTED** | `hearth` 3×3 · `bookcase` 2×3 · `shelf` (wares) 2×3 · `dresser` 2×2 · `stove` 2×2 · `lamp_rack` 2×2 | Pure FRONT elevation, drawn edge-to-edge with a cornice shadow at the top and a floor contact line at the bottom. Placed via `roomkit.wall_mount` with the **top row over the wall FACE row** — the piece stands against the wall; on its own in mid-floor it reads as a crate (never do that). |
| **FREE-STANDING** | `bed`/`bed_inn` 2×3 · `table` 2×2 · `table_long` 3×2 · `stool` 1×1 · `counter` 4×2 · `rug` 3×2 · `rug_runner` 1×3 · `crates` 2×2 · `barrels`/`sacks`/`oil_jars` 2×1 · `plant` 1×1 · `altar` 3×3 · `brazier` 1×2 · `pew` 3×1 | Top-down-frontal split: a TOP surface, a short front face strip, 1px ink outline, contact shadow. Placed via `roomkit.place` (manifest footprints — no hand-typed w/h). |

Need a new piece? **Draw it in interiorforge** (match a neighbour's helper
structure and the shared palettes), re-run it + `pack_objects.py`. Multi-tile
first: a focal piece smaller than 2×2 will read as clutter.

## 2. Room types — partition + focal point + dressing

Every interior has **one focal point at top-centre** and **one partition**:

- **Home** — warm. Focal: the 3×3 **hearth** flush on the north wall. Partition:
  the **bed nook** (bed + window + a personal touch). Dress: stove + bookcase
  flush; table + stools on the rug; sacks/barrels in the working corner.
- **Shop** — warm. Focal: the 4×2 **counter** with the keeper behind it.
  Partition: the **storeroom bay** (crates + stock the player sees but can't
  shop from). Dress: wares `shelf` flush, a `lamp_rack` hanging, rug, plant.
- **Inn** — warm. Focal: the **hearth**. Partition: the **bunk room** (made
  `bed_inn` pair). Dress: `table_long` + stools, the round corner table, lamps.
- **Lumenary** — cool register; a shrine, never a cabin. Focal: the 3×3
  **altar** on the dais, runner aisle to the door. Partitions: **two side-niche
  stubs** (the star-ledger `bookcase` west, offerings east). Dress: braziers
  flanking the dais, `pew` rows flanking the aisle, banners on the face.
- **Boat cabin / tiny room** — the one exception to rule B: a single faced
  room, a bunk, a crate, one lantern.
- **Future rooms** (lab/observatory, bakery, hearth-home, lighthouse floors):
  same recipe — pick the register, pick the focal wall piece (draw it if it's
  new: an orrery, an oven), pick what the partition encloses.

## 3. Layout rules (binding)

1. **Single entrance**: one `doormat` at centre-bottom; the player spawns there
   facing up. (Tower floors may add stair warps.)
2. **Clear lanes**: a walkable path from the doormat to **every** NPC, trigger
   and partition opening. `audit_flow` (run by `roomkit.finish`) proves it.
3. **Furniture against walls is MOUNTED** (`wall_mount`) — never floated one
   tile south of the face with floor showing behind it.
4. **One focal point** at top-centre of the main room; the partition's room
   gets its own minor anchor (the bed, the stock, the ledger).
5. **Warm lighting**: ≥2 light sources (hearth/stove/brazier/lamp-rack count);
   windows on the face for the sense of outside.
6. **Symmetry** for civic rooms (Lumenary, shop); **cosy asymmetry** for homes.
7. **Size** (per `level-design.md` §2): small interior **12×9 → 14×11**; shop
   **14×10**; inn / Lumenary **16×12**; never below 12 wide once a partition is
   involved (the rooms need room). Door on the **bottom edge**.
8. **Collision**: walls + partitions + furniture collide; floor/rug/runner/
   doormat walk on; `lamp_rack` may be `solid:false` (lamps hang overhead).

## 4. Build & QA pattern

- Compose in a builder on **`tools/maps/roomkit.py`**: `faced_room` →
  `partition_v`/`partition_h` → `wall_mount`/`place` → `runner`/`windows` →
  `rk.finish(m)` (write → render → `audit_flow` reach gate).
  `tools/maps/build_interiors.py` is the worked example for all five room
  types; `build_beacon.py` for tower floors.
- **QA every interior** with the rendered PNG against this doc: visible
  wall-face, an internal partition shaping a second space, flush wall
  furniture (no floor showing behind the bookcase), one top-centre focal
  point, ≥2 lights, patterned floor, single doormat, clear lanes. Same-y
  square + floating props = redo it.
- If the exterior door's landing coords change (room resized), update the
  town builder's warp and re-run `audit_warps` — it enforces the pairing.
