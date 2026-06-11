#!/usr/bin/env python3
"""
Build Pearlmoor Quay — the third area, the second Lumenary town — on the SHARED overworld set.

A moonlit Tide fishing-port (walkthrough/01-south "Pearlmoor Quay"): wet boardwalks (the
`dock` tile) running over/along the harbour water, a sand quay, a moored area with boats,
a lit path spine, the Tide Lumenary as the tallest landmark up top, a port chandlery (shop)
and a quayside inn (both enterable), lantern-buoys offshore, lamps + trees for warmth.

Per spine §0 rule 1 the TOWN and the LUMENARY are NOT gated by Tidecall — they are reachable
on foot. The Tidecall-gated content is the harbour `water` zone (an AbilityGate make_passable
over the open water, exactly like Dimglass's tide_shallows) which carries the rarer Tide kin.

DOOR ALIGNMENT (the core rule): every enterable building's interact-warp sits on its actual
door-art tile, with the tile directly BELOW it walkable and on the path.
  * lumenary (6 wide): arched door straddles cols 2-3 -> col 2 is the interact-warp tile,
    col 3 is the twin walkable approach; the boardwalk runs directly below both.
  * shop     (5 wide): door art = col 2 -> door tile (tx0+2, ty_bottom); approach below it.
  * inn      (5 wide): door art = col 2 -> door tile (tx0+2, ty_bottom); approach below it.

Run:  python3 tools/maps/build_pearlmoor.py
Prereq: python3 tools/maps/build_shared_overworld.py (the shared set must exist) and the
        packed pearlmoor objects (pack_objects.py over assets/tilesets/pearlmoor/objects/).
"""
from __future__ import annotations
import random
import mapkit as mk
from mapkit import gid

W, H = 28, 24
rng = random.Random(23)

# ---- building footprints (top-left anchor) + measured door columns -----------
# door tile = (at.tx + door_col, at.ty + h - 1); approach tile = one row below that.
LUMENARY = {"at": (11, 1), "w": 6, "h": 6, "door_col": 2}   # arch straddles cols 2-3, top-centre landmark
SHOP = {"at": (3, 8), "w": 5, "h": 4, "door_col": 2}        # chandlery, left of the spine
INN = {"at": (20, 7), "w": 5, "h": 5, "door_col": 2}        # quayside inn, right of the spine


def door_tile(b):
    return (b["at"][0] + b["door_col"], b["at"][1] + b["h"] - 1)


lum_door = door_tile(LUMENARY)        # (13, 6)
lum_door_r = (lum_door[0] + 1, lum_door[1])  # (14, 6) walkable twin (grand arch)
shop_door = door_tile(SHOP)           # (5, 11)
inn_door = door_tile(INN)             # (22, 11)

# ---- terrain presence grids -------------------------------------------------
# A tree-line frames the top/sides (north/west/east land edge); the harbour (water + sand
# quay + boardwalks) fills the south. The lit path spine runs the dry land between.
tree = mk.make_grid(W, H)
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(4, 4, 2), (24, 4, 2), (2, 14, 2), (25, 14, 2)])
for x in (5, 6, 7):                       # punch the south-entry gap from Dimglass (land-in)
    pass
mk.rect(tree, W, H, 0, 15, W - 1, H - 1, 0)   # clear the border below the quay line

# The harbour: a broad sea across the south, a sand quay strip above it, with boardwalks
# (dock tiles, placed on the deco/object pass) reaching out over the water. A central SAND
# jetty noses down into the harbour as the always-walkable arrival pier (the player lands
# here from Dimglass on foot) — dock decor laid over sand stays walkable, while dock over
# open WATER inherits the water tile's Tidecall gate, so the side-piers read as gated tease.
water = mk.make_grid(W, H)
mk.rect(water, W, H, 0, 18, W - 1, H - 1)     # full-width harbour sea (continues off-south)
mk.blob(water, W, H, 4, 18, 2.4, 1.2)         # the tide bites the quay line…
mk.blob(water, W, H, 24, 18, 2.2, 1.2)
sand = mk.make_grid(W, H)
mk.rect(sand, W, H, 0, 16, W - 1, 17)         # 2-row sand quay meeting the sea
mk.blob(sand, W, H, 9, 15, 2.0, 1.2)          # …and the quay sand laps up into the green
mk.blob(sand, W, H, 19, 15, 1.8, 1.2)
mk.rect(sand, W, H, 13, 18, 14, 21, 1)        # central arrival jetty (sand) down into the harbour
# carve the water out from under the jetty so the jetty boards stay ungated/walkable
mk.rect(water, W, H, 13, 18, 14, 21, 0)

# tall-grass fringe (grass-kin encounter patch) tucked top-left under the tree-line
tallgrass = mk.make_grid(W, H)
mk.blob(tallgrass, W, H, 3.5, 5.5, 2.4, 2.2)

# ---- the lit path spine + approach lanes to every door ----------------------
path = mk.make_grid(W, H)
# N-S spine (2 wide) from the Lumenary forecourt down to the quay/boardwalk
mk.vline(path, W, H, 13, 7, 16)
mk.vline(path, W, H, 14, 7, 16)
# the quay promenade street along the building fronts / waterline approach
mk.rect(path, W, H, 4, 12, 23, 13)
# Lumenary forecourt: door (13,6)/(14,6) -> row 7 is the spine head; carve the forecourt
mk.hline(path, W, H, 7, 12, 15)
# shop approach: door (5,11) -> below (5,12) on the promenade street row 12
path[12 * W + shop_door[0]] = 1
mk.vline(path, W, H, shop_door[0], shop_door[1] + 1, 12)
# inn approach: door (22,11) -> below (22,12) on the promenade
path[12 * W + inn_door[0]] = 1
mk.vline(path, W, H, inn_door[0], inn_door[1] + 1, 12)
# connect the promenade down across the quay to the sand jetty head (rows 12->17)
mk.vline(path, W, H, 13, 12, 17)
mk.vline(path, W, H, 14, 12, 17)
# the Lanternway WEST to Vesper Crossroads + the EAST road tease toward Saltreach
# Fen (East region; inert until authored — the engine no-ops unregistered warps).
mk.hline(path, W, H, 12, 0, 4)
mk.hline(path, W, H, 12, 23, W - 1)
for x in (0, 1, 2):
    tree[12 * W + x] = 0
for x in (25, 26, 27):
    tree[12 * W + x] = 0

# ---- base = full grass scatter; terrain layers mesh over it -----------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
]

# ---- objects: buildings, trees, lamps (walk-under) --------------------------
objects = [
    {"id": "lumenary", "sprite": "pearlmoor_lumenary",
     "at": {"tx": LUMENARY["at"][0], "ty": LUMENARY["at"][1]},
     "w": LUMENARY["w"], "h": LUMENARY["h"], "overhang": 3},
    {"id": "shop", "sprite": "pearlmoor_shop",
     "at": {"tx": SHOP["at"][0], "ty": SHOP["at"][1]},
     "w": SHOP["w"], "h": SHOP["h"], "overhang": 2},
    {"id": "inn", "sprite": "pearlmoor_inn",
     "at": {"tx": INN["at"][0], "ty": INN["at"][1]},
     "w": INN["w"], "h": INN["h"], "overhang": 3},
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 8, "ty": 9},
     "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 24, "ty": 12},
     "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    # a small moored boat decor sitting against the boardwalk over the water
    {"id": "boat_a", "sprite": "pearlmoor_boat", "at": {"tx": 9, "ty": 18},
     "w": 2, "h": 3, "overhang": 0},
    {"id": "boat_b", "sprite": "pearlmoor_boat", "at": {"tx": 18, "ty": 18},
     "w": 2, "h": 3, "overhang": 0},
    {"id": "tree_c", "sprite": "tinderwick_tree", "at": {"tx": 18, "ty": 3},
     "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_d", "sprite": "tinderwick_tree", "at": {"tx": 1, "ty": 10},
     "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_e", "sprite": "tinderwick_tree", "at": {"tx": 7, "ty": 3},
     "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_f", "sprite": "tinderwick_tree", "at": {"tx": 3, "ty": 2},
     "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_g", "sprite": "tinderwick_tree", "at": {"tx": 23, "ty": 1},
     "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 9},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 15, "ty": 13},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    # the promenade + quay lamps are OBJECTS too (no 1-tile lamps anywhere)
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 5, "ty": 12},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_d", "sprite": "tinderwick_lamp_post", "at": {"tx": 21, "ty": 12},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_e", "sprite": "tinderwick_lamp_post", "at": {"tx": 16, "ty": 14},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
building_cells = set()
for o in objects:
    for yy in range(o["at"]["ty"], o["at"]["ty"] + o["h"]):
        for xx in range(o["at"]["tx"], o["at"]["tx"] + o["w"]):
            building_cells.add((xx, yy))

covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (tree, water, sand, tallgrass, path))}
avoid = covered | building_cells

# ---- deco: boardwalks (dock), buoys, lamps, signs, scatter ------------------
deco = mk.make_grid(W, H)
# Boardwalks (dock tiles, walkable floor) reaching out over the harbour water from the quay.
# Two finger-piers under the spine and beside the boats, so the player can walk onto the water-
# edge. dock is role:floor so it overrides the colliding water beneath at the same cell.
# central arrival jetty boards (over SAND -> always walkable) and side piers (over WATER
# -> Tidecall-gated tease). dock is role:floor and draws above the surface beneath it.
dock_cells = []
for ty in (18, 19, 20, 21):                  # central arrival pier on the sand jetty
    dock_cells += [(13, ty), (14, ty)]
for ty in (18, 19):                          # short side piers by each moored boat (over water)
    dock_cells += [(8, ty), (19, ty)]
dock_cells += [(11, 18), (16, 18)]           # quay-edge boards bridging out to the side piers
for (x, y) in dock_cells:
    deco[y * W + x] = gid("dock")

# lantern-buoys offshore in the open harbour (the Tidecall tease line), clear of the jetty
for (x, y) in [(4, 21), (10, 22), (18, 22), (23, 21), (6, 20), (21, 20)]:
    deco[y * W + x] = gid("buoy")


# signs immediately beside the path the player walks (never mid-field)
sign_tiles = {
    "sign_welcome": (12, 8),     # by the Lumenary forecourt / spine head
    "sign_lumenary": (15, 7),    # right of the Lumenary door
    "sign_shop": (7, 14),        # across the promenade from the shop door — NOT
                                 # at (4,12): that tile is the west lane's only
                                 # link to the Crossroads gate (audit_flow caught
                                 # the sign sealing the whole west spoke), and
                                 # (5,14)/(6,14) hold the lamp trunk + flowerbed
    "sign_harbour": (15, 16),    # by the quay/boardwalk, facing the gated water
    "sign_lanternway": (2, 11),  # beside the west lane, pointing to the Crossroads
    "sign_fen": (25, 11),        # beside the east lane, the sleeping Saltreach road
}
for (x, y) in sign_tiles.values():
    deco[y * W + x] = gid("sign")

# a fenced flower garden for warmth, between the spine and the inn
mk.fence_run(deco, W, H, 17, 9, 19)
for (x, y) in [(17, 10), (18, 10), (19, 10)]:
    deco[y * W + x] = gid("flowerbed_a") if x % 2 else gid("flowerbed_b")
mk.fence_run(deco, W, H, 17, 11, 19)
# quay boulders + harbour-mouth rocks
for (x, y) in [(2, 16), (25, 17), (10, 16), (26, 21)]:
    deco[y * W + x] = gid("boulder")

# scatter decor only beside the lit lane so the open field stays clean
near_path = set()
for y in range(H):
    for x in range(W):
        if path[y * W + x]:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    near_path.add((x + dx, y + dy))
deco_avoid = avoid | {(x, y) for y in range(H) for x in range(W) if (x, y) not in near_path}
# keep scatter off the dock/buoy/sign/lamp/flower cells already placed
deco_avoid |= {(x, y) for (x, y) in dock_cells}
mk.scatter_decor(deco, base, W, H, rng, density=0.15, avoid=deco_avoid)

# ---- assemble ---------------------------------------------------------------
m = {
    "id": "pearlmoor_quay", "display_name": "Pearlmoor Quay", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "town",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        # South land-in from / return to Dimglass Coast: the player arrives on foot at the
        # seaward tip of the central sand jetty (always-walkable) and heads up the spine.
        {"id": "to_dimglass", "at": {"tx": 13, "ty": 21}, "trigger": "step_on",
         "to_map": "dimglass_coast_ii", "to": {"tx": 7, "ty": 0}, "facing": "down", "transition": "fade"},
        {"id": "to_dimglass_e", "at": {"tx": 14, "ty": 21}, "trigger": "step_on",
         "to_map": "dimglass_coast_ii", "to": {"tx": 8, "ty": 0}, "facing": "down", "transition": "fade"},
        # Lumenary door — interact on the arch door-art tile (col 2); col 3 is the twin
        # walkable approach. Reachable WITHOUT Tidecall (spine §0 rule 1); soft-gated on
        # holding a starter, like Tinderwick's.
        {"id": "to_lumenary", "at": {"tx": lum_door[0], "ty": lum_door[1]}, "trigger": "interact",
         "to_map": "pearlmoor_lumenary", "to": {"tx": 7, "ty": 9}, "facing": "down",
         "requires_flag": "flag:has_starter", "transition": "door"},
        # Shop door — interact on the chandlery's door-art tile (col 2).
        {"id": "to_shop", "at": {"tx": shop_door[0], "ty": shop_door[1]}, "trigger": "interact",
         "to_map": "pearlmoor_shop", "to": {"tx": 6, "ty": 7}, "facing": "down", "transition": "door"},
        # Inn door — interact on the inn's door-art tile (col 2).
        # The inn room is 14 wide -> its doormat column is 7, not the shops' 6.
        {"id": "to_inn", "at": {"tx": inn_door[0], "ty": inn_door[1]}, "trigger": "interact",
         "to_map": "pearlmoor_inn", "to": {"tx": 7, "ty": 8}, "facing": "down", "transition": "door"},
        # The Lanternway west to Vesper Crossroads (the hub; graph.ts spoke).
        {"id": "to_crossroads", "at": {"tx": 0, "ty": 12}, "trigger": "step_on",
         "to_map": "vesper_crossroads", "to": {"tx": 19, "ty": 9}, "facing": "left",
         "transition": "fade"},
        # East road to Saltreach Fen (East region) — inert tease until authored.
        {"id": "to_fen", "at": {"tx": W - 1, "ty": 12}, "trigger": "step_on",
         "to_map": "saltreach_fen_i", "to": {"tx": 1, "ty": 38}, "facing": "right",
         "transition": "fade"},
    ],
    "triggers": [
        {"id": "sign_welcome", "kind": "sign", "at": {"tx": sign_tiles["sign_welcome"][0], "ty": sign_tiles["sign_welcome"][1]},
         "activation": "interact", "ref": "sign.pearlmoor_welcome"},
        {"id": "sign_lumenary", "kind": "sign", "at": {"tx": sign_tiles["sign_lumenary"][0], "ty": sign_tiles["sign_lumenary"][1]},
         "activation": "interact", "ref": "sign.pearlmoor_lumenary"},
        {"id": "sign_shop", "kind": "sign", "at": {"tx": sign_tiles["sign_shop"][0], "ty": sign_tiles["sign_shop"][1]},
         "activation": "interact", "ref": "sign.pearlmoor_shop"},
        {"id": "sign_harbour", "kind": "sign", "at": {"tx": sign_tiles["sign_harbour"][0], "ty": sign_tiles["sign_harbour"][1]},
         "activation": "interact", "ref": "sign.pearlmoor_harbour"},
        {"id": "sign_lanternway", "kind": "sign",
         "at": {"tx": sign_tiles["sign_lanternway"][0], "ty": sign_tiles["sign_lanternway"][1]},
         "activation": "interact", "ref": "sign.pearlmoor_lanternway"},
        {"id": "sign_fen", "kind": "sign", "at": {"tx": sign_tiles["sign_fen"][0], "ty": sign_tiles["sign_fen"][1]},
         "activation": "interact", "ref": "sign.pearlmoor_to_fen"},
    ],
    # Tide port (walkthrough/01-south): grass-fringe Tide kin lv 8-11; the Tidecall-gated
    # harbour water carries the rarer Tide reads lv 10-12. Every kin_id is in the creatures
    # manifest (26 Brinelet, 31 Lumpin, 2 Brinix, 24 Shimmral, 27 Brineroll).
    "encounters": [
        {"id": "fringe_grass", "terrain": "tall_grass", "rect": {"tx": 2, "ty": 4, "w": 4, "h": 4},
         "encounter_rate": 0.08,
         "table": [{"kin_id": 26, "weight": 60, "min_level": 8, "max_level": 11},
                   {"kin_id": 31, "weight": 40, "min_level": 9, "max_level": 11}]},
        # The Tidecall-gated open harbour, split W/E of the central arrival jetty (cols 13-14).
        {"id": "harbour_water_w", "terrain": "water", "rect": {"tx": 3, "ty": 19, "w": 9, "h": 4},
         "encounter_rate": 0.07, "requires_ability": "tidecall",
         "table": [{"kin_id": 2, "weight": 45, "min_level": 10, "max_level": 12},
                   {"kin_id": 27, "weight": 35, "min_level": 10, "max_level": 12},
                   {"kin_id": 24, "weight": 20, "min_level": 11, "max_level": 12}]},
        {"id": "harbour_water_e", "terrain": "water", "rect": {"tx": 16, "ty": 19, "w": 9, "h": 4},
         "encounter_rate": 0.07, "requires_ability": "tidecall",
         "table": [{"kin_id": 2, "weight": 45, "min_level": 10, "max_level": 12},
                   {"kin_id": 27, "weight": 35, "min_level": 10, "max_level": 12},
                   {"kin_id": 24, "weight": 20, "min_level": 11, "max_level": 12}]},
    ],
    "npcs": [
        # Townsfolk for Tide-blessing flavour, beside the promenade (not mid-field).
        {"id": "fisher", "at": {"tx": 16, "ty": 13}, "facing": "left", "sprite": "wren",
         "movement": "look_around", "dialogue_ref": "npc.pearlmoor_fisher"},
        # The Tide-blessing festival (Arc E): once 'gleam:tide' stands, the quay
        # fills — the second "Gleam = belonging" payoff, pure data.
        {"id": "blessing_elder", "at": {"tx": 10, "ty": 13}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "npc.blessing_elder", "requires_flag": "gleam:tide"},
        {"id": "blessing_kid", "at": {"tx": 18, "ty": 13}, "facing": "down",
         "sprite": "npc_child", "movement": "wander",
         "dialogue_ref": "npc.blessing_kid", "requires_flag": "gleam:tide"},
    ],
    # AbilityGate (Tidecall, make_passable) over the open harbour water — split W/E of the
    # central arrival jetty (cols 13-14) so the always-walkable jetty is never gated.
    "gates": [
        {"id": "harbour_gate_w", "ability": "tidecall", "effect": "make_passable",
         "rect": {"tx": 3, "ty": 18, "w": 9, "h": 5}},
        {"id": "harbour_gate_e", "ability": "tidecall", "effect": "make_passable",
         "rect": {"tx": 16, "ty": 18, "w": 9, "h": 5}}],
    "music": "assets/audio/music/dimglass-coast-a.mp3",
    "_doors": {"lumenary": lum_door, "lumenary_twin": lum_door_r,
               "shop": shop_door, "inn": inn_door},
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
