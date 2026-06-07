#!/usr/bin/env python3
"""
Build the gold-standard Tinderwick tileset + map (the autotile template area).

Reproducible assembly of:
  1) a fully-tagged tinderwick tileset (grass base + autotile sets for path, sand,
     water-shoreline, forest, tall-grass, plus buildings & decor), and
  2) the Tinderwick map re-authored as TERRAIN LAYERS derived from the existing
     hand-authored layout (so all gameplay wiring is preserved) — which
     tools/autotile/expand.mjs then meshes into a clean base layer.

Run from repo root:  ./venv/bin/python tools/maps/build_tinderwick.py
Then: pack_tileset.py --tiles-dir assets/tilesets/tinderwick ; expand ; render ; validate.

Tile source art comes from the sliced autotile blocks in /tmp (generated via
generate_block.py) and the existing decor masters. See docs/world/level-design.md §10.
"""
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
TD = REPO / "assets" / "tilesets" / "tinderwick"
MAP = REPO / "public" / "assets" / "maps" / "tinderwick.json"
# Read the ORIGINAL hand-authored layout (idempotent): the live map gets rewritten
# with terrain layers + expanded each run, so we always re-derive from this snapshot.
SOURCE = REPO / "tools" / "maps" / "tinderwick.source.json"
EDGES = ["corner_nw","edge_n","corner_ne","edge_w","fill","edge_e","corner_sw","edge_s","corner_se"]

# --- the new tile list (order fixes local index; gid = index+1) ---------------
# Each: name, src path, role, terrain?, autotile?, collides?, encounter?, ability?, tileable?
def nine(terrain, srcdir, **flags):
    role = flags.pop("role", terrain)
    return [dict(name=f"{terrain}_{r}", src=f"{srcdir}/{_find(srcdir, r)}", role=role,
                 terrain=terrain, autotile=r, tileable=(r == "fill"), **flags) for r in EDGES]

def _find(srcdir, role):
    for p in Path(srcdir).glob(f"*_{role}.png"):
        return p.name
    raise SystemExit(f"missing {role} in {srcdir}")

T = []
T.append(dict(name="grass_fill", src=str(TD/"00_grass.png"), role="ground", tileable=True))
T.append(dict(name="grass_var",  src=str(TD/"07_grass_dark.png"), role="ground", tileable=True))
T.append(dict(name="tallgrass_a", src="/tmp/tallgrass_t/00_tile.png", role="ground",
              terrain="tallgrass", autotile="fill", encounter="tall_grass", tileable=True))
T.append(dict(name="tallgrass_b", src="/tmp/tallgrass_t/01_tile.png", role="ground",
              terrain="tallgrass", autotile="fill", encounter="tall_grass", tileable=True))
T += nine("path", "/tmp/path9_t", role="path")
# 1-wide path strips (grass on both flanks) so thin lanes don't read as solid blocks
T.append(dict(name="path_strip_h", src="/tmp/pathstrip_t/00_tile.png", role="path",
              terrain="path", autotile="strip_h", tileable=False))
T.append(dict(name="path_strip_v", src="/tmp/pathstrip_t/01_tile.png", role="path",
              terrain="path", autotile="strip_v", tileable=False))
T += nine("sand", "/tmp/sand9_t", role="sand")
T += nine("tree", "/tmp/tree9_t", role="tree", collides=True)
# water: 9-slice shoreline (collides, tidecall, water encounter); fill is animated
T += nine("water", "/tmp/water9_tiles", role="water", collides=True,
          encounter="water", ability="tidecall")
T.append(dict(name="water_a2", src="/tmp/water_raw/01_frame1.png", role="water", collides=True, tileable=True))
T.append(dict(name="water_a3", src="/tmp/water_raw/02_frame2.png", role="water", collides=True, tileable=True))
# buildings + decor (reuse existing masters)
T.append(dict(name="wall",  src=str(TD/"10_wall.png"),  role="wall",  collides=True))
T.append(dict(name="roof",  src=str(TD/"11_roof.png"),  role="roof"))
T.append(dict(name="door",  src=str(TD/"09_door.png"),  role="door"))
T.append(dict(name="flowers", src=str(TD/"04_flowers.png"), role="decor"))
T.append(dict(name="sign",  src=str(TD/"05_sign.png"),  role="sign", collides=True))
T.append(dict(name="lamp",  src=str(TD/"08_lamp.png"),  role="decor", collides=True))
T.append(dict(name="fence", src=str(TD/"14_fence.png"), role="fence", collides=True))
T.append(dict(name="canopy", src=str(TD/"06_tree_top.png"), role="tree"))

idx = {t["name"]: i for i, t in enumerate(T)}
def gid(name): return idx[name] + 1

# --- 1. write tile files + manifest ------------------------------------------
MT = REPO/".claude/skills/generate-sprite-sheet/scripts/make_tileable.py"
manifest_tiles = []
for i, t in enumerate(T):
    dst = TD / f"t{i:02d}_{t['name']}.png"
    Image.open(t["src"]).convert("RGBA").resize((16,16), Image.LANCZOS).save(dst)
    if t.get("tileable"):
        subprocess.run([sys.executable, str(MT), str(dst)], capture_output=True)
    entry = {"file": dst.name, "role": t["role"]}
    for k_src, k_dst in [("terrain","terrain"),("autotile","autotile"),("collides","collides"),
                          ("encounter","encounter_terrain"),("ability","requires_ability")]:
        if t.get(k_src): entry[k_dst] = t[k_src]
    manifest_tiles.append(entry)
# animated water: the water fill cycles through itself + the 2 extra frames
wf = manifest_tiles[idx["water_fill"]]
wf["animation"] = {"frames": [idx["water_fill"], idx["water_a2"], idx["water_a3"]], "duration_ms": 800}
(TD/"tileset.manifest.json").write_text(json.dumps(
    {"name": "tinderwick_set", "columns": 8, "tiles": manifest_tiles}, indent=2) + "\n")
print(f"wrote {len(T)} tiles + manifest")

# --- 2. re-author the map as terrain layers from the existing layout ----------
m = json.loads((SOURCE if SOURCE.is_file() else MAP).read_text())
W, H = m["width"], m["height"]
old = {ly["name"]: ly["data"] for ly in m["layers"]}
# old gid -> meaning (old set: gid = local+1; local: 1 water,2 path,3 floor,4 flowers,
#   5 sign,6 tree,7 grass_dark,8 lamp,9 door,10 wall,11 roof,12 sand,13 water_edge)
ob = old["base"]; od = old.get("deco", [0]*W*H); oa = old.get("above", [0]*W*H)
def grid_where(layer, *gids):
    s = set(gids); return [1 if layer[i] in s else 0 for i in range(W*H)]

terrain_layers = [
    {"name":"t_tallgrass","role":"terrain","terrain":"tallgrass","set":"tinderwick_set","into":"base","depth":0,
     "data": grid_where(ob, 8)},                       # old grass_dark verge
    {"name":"t_tree","role":"terrain","terrain":"tree","set":"tinderwick_set","into":"base","depth":0,
     "data": grid_where(od, 7)},                        # old deco trees -> forest mass border
    {"name":"t_path","role":"terrain","terrain":"path","set":"tinderwick_set","into":"base","depth":0,
     "data": grid_where(ob, 3)},                        # old path lanes
    {"name":"t_sand","role":"terrain","terrain":"sand","set":"tinderwick_set","into":"base","depth":0,
     "data": grid_where(ob, 13)},                       # old sand shore band
    {"name":"t_water","role":"terrain","terrain":"water","set":"tinderwick_set","into":"base","depth":0,
     "data": grid_where(ob, 2)},                        # old sea (last = shoreline over sand)
]
# base starts all grass; expand stamps the meshed terrain gids over it
base = [gid("grass_fill")] * (W*H)
# door tiles (old base gid 10) sit on base under the building front
door_cells = [i for i in range(W*H) if ob[i] == 10]

# deco: walls, signs, lamps, flowers, fences (old deco gids 11,6,8?,5,...)
remap_deco = {11: gid("wall"), 6: gid("sign"), 9: gid("lamp"), 5: gid("flowers")}
deco = [remap_deco.get(od[i], 0) for i in range(W*H)]
# above: roofs (old above gid 12) only; the forest is solid on base now
above = [gid("roof") if oa[i] == 12 else 0 for i in range(W*H)]

m["tilesets"][0]["tile_count"] = len(T)
m["layers"] = (
    [{"name":"base","role":"base","depth":0,"data":base}] +
    terrain_layers +
    [{"name":"deco","role":"deco","depth":5,"data":deco},
     {"name":"above","role":"above","depth":20,"data":above}]
)
m["_door_cells"] = door_cells  # consumed by the post-expand door pass below
MAP.write_text(json.dumps(m, indent=2) + "\n")
print(f"wrote map with {len(terrain_layers)} terrain layers; {len(door_cells)} door tiles pending")
print("next: pack_tileset.py --tiles-dir assets/tilesets/tinderwick ; then expand ; then place doors")
