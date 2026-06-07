#!/usr/bin/env python3
"""
Build the gold-standard Tinderwick tileset + map (the autotile/object template).

Two classes of art (docs/art-style.md §14b):
  - GROUND = recessive borderless autotile surfaces (grass variants + path/sand/
    water/forest/tall-grass edge sets), meshed from a `terrain` layer.
  - STRUCTURES = whole multi-tile OBJECTS (cottage/shop/Lumenary/trees/lamps)
    placed via the engine object layer, not tiled.

Idempotent: reads the original layout from tinderwick.source.json, derives terrain
regions + object placements (preserving all gameplay wiring), writes the live map.

Run:  ./venv/bin/python tools/maps/build_tinderwick.py
Then: pack_tileset.py --tiles-dir assets/tilesets/tinderwick ; pack_objects.py ;
      node tools/autotile/expand.mjs <map> ; render_map.py ; validate_map.py
"""
from __future__ import annotations
import json, random, subprocess, sys
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
TD = REPO / "assets" / "tilesets" / "tinderwick"
GV = TD / "grass_variants"
MAP = REPO / "public" / "assets" / "maps" / "tinderwick.json"
SOURCE = REPO / "tools" / "maps" / "tinderwick.source.json"
MT = REPO / ".claude/skills/generate-sprite-sheet/scripts/make_tileable.py"
EDGES = ["corner_nw","edge_n","corner_ne","edge_w","fill","edge_e","corner_sw","edge_s","corner_se"]

def nine(terrain, srcdir, **flags):
    role = flags.pop("role", terrain)
    out = []
    for r in EDGES:
        f = next(Path(srcdir).glob(f"*_{r}.png"))
        out.append(dict(name=f"{terrain}_{r}", src=str(f), role=role, terrain=terrain,
                        autotile=r, tileable=(r == "fill"), **flags))
    return out

# --- ground-only tile list (gid = index+1); structures are objects, not tiles ---
T = [
    dict(name="grass0", src=str(GV/"grass_00.png"), role="ground", tileable=True),
    dict(name="grass1", src=str(GV/"grass_01.png"), role="ground", tileable=True),
    dict(name="grass2", src=str(GV/"grass_02.png"), role="ground", tileable=True),
    dict(name="grass3", src=str(GV/"grass_03.png"), role="ground", tileable=True),
    dict(name="tallgrass_a", src="/tmp/tallgrass_t/00_tile.png", role="ground",
         terrain="tallgrass", autotile="fill", encounter="tall_grass", tileable=True),
    dict(name="tallgrass_b", src="/tmp/tallgrass_t/01_tile.png", role="ground",
         terrain="tallgrass", autotile="fill", encounter="tall_grass", tileable=True),
]
T += nine("path", "/tmp/path9_t", role="path")
T.append(dict(name="path_strip_h", src="/tmp/pathstrip_t/00_tile.png", role="path",
              terrain="path", autotile="strip_h"))
T.append(dict(name="path_strip_v", src="/tmp/pathstrip_t/01_tile.png", role="path",
              terrain="path", autotile="strip_v"))
T += nine("sand", "/tmp/sand9_t", role="sand")
T += nine("tree", "/tmp/tree9_t", role="tree", collides=True)       # forest border (collides)
T += nine("water", "/tmp/water9_tiles", role="water", collides=True,
          encounter="water", ability="tidecall")
T.append(dict(name="water_a2", src="/tmp/water_raw/01_frame1.png", role="water", collides=True, tileable=True))
T.append(dict(name="water_a3", src="/tmp/water_raw/02_frame2.png", role="water", collides=True, tileable=True))
T.append(dict(name="flowers", src=str(TD/"04_flowers.png"), role="decor"))
T.append(dict(name="sign", src=str(TD/"05_sign.png"), role="sign", collides=True))

idx = {t["name"]: i for i, t in enumerate(T)}
def gid(n): return idx[n] + 1

# --- write tile files + manifest ---------------------------------------------
manifest = []
for i, t in enumerate(T):
    dst = TD / f"t{i:02d}_{t['name']}.png"
    Image.open(t["src"]).convert("RGBA").resize((16, 16), Image.LANCZOS).save(dst)
    if t.get("tileable"):
        subprocess.run([sys.executable, str(MT), str(dst)], capture_output=True)
    e = {"file": dst.name, "role": t["role"]}
    for k, kk in [("terrain","terrain"),("autotile","autotile"),("collides","collides"),
                  ("encounter","encounter_terrain"),("ability","requires_ability")]:
        if t.get(k): e[kk] = t[k]
    manifest.append(e)
manifest[idx["water_fill"]]["animation"] = {
    "frames": [idx["water_fill"], idx["water_a2"], idx["water_a3"]], "duration_ms": 800}
(TD/"tileset.manifest.json").write_text(json.dumps(
    {"name": "tinderwick_set", "columns": 8, "tiles": manifest}, indent=2) + "\n")

# --- re-author the map -------------------------------------------------------
m = json.loads((SOURCE if SOURCE.is_file() else MAP).read_text())
W, H = m["width"], m["height"]
old = {ly["name"]: ly["data"] for ly in m["layers"]}
ob, od = old["base"], old.get("deco", [0]*W*H)
def where(layer, *gids):
    s = set(gids); return [1 if layer[i] in s else 0 for i in range(W*H)]

# base: scatter the 4 recessive grass variants; expand stamps terrain over it
rng = random.Random(7)
grass_gids = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(grass_gids) if rng.random() < 0.5 else grass_gids[0] for _ in range(W*H)]

terrain_layers = [
    {"name":"t_tallgrass","role":"terrain","terrain":"tallgrass","set":"tinderwick_set","depth":0,"data": where(ob, 8)},
    {"name":"t_tree","role":"terrain","terrain":"tree","set":"tinderwick_set","depth":0,"data": where(od, 7)},
    {"name":"t_path","role":"terrain","terrain":"path","set":"tinderwick_set","depth":0,"data": where(ob, 3)},
    {"name":"t_sand","role":"terrain","terrain":"sand","set":"tinderwick_set","depth":0,"data": where(ob, 13)},
    {"name":"t_water","role":"terrain","terrain":"water","set":"tinderwick_set","depth":0,"data": where(ob, 2)},
]
# deco: keep flowers + signs only (walls/roofs/lamps/doors are objects now)
deco = [gid("flowers") if od[i]==5 else gid("sign") if od[i]==6 else 0 for i in range(W*H)]

# whole-structure objects, aligned so each door sits on its existing warp tile
objects = [
    {"id":"house","sprite":"tinderwick_cottage","at":{"tx":6,"ty":11},"w":5,"h":5,"overhang":3},
    {"id":"shop","sprite":"tinderwick_shop","at":{"tx":6,"ty":5},"w":5,"h":4,"overhang":2},
    {"id":"lumenary","sprite":"tinderwick_lumenary","at":{"tx":15,"ty":3},"w":6,"h":6,"overhang":3},
    {"id":"tree_a","sprite":"tinderwick_tree","at":{"tx":2,"ty":17},"w":3,"h":4,"overhang":3,"walk_under":True},
    {"id":"tree_b","sprite":"tinderwick_tree","at":{"tx":23,"ty":16},"w":3,"h":4,"overhang":3,"walk_under":True},
    {"id":"lamp_a","sprite":"tinderwick_lamp_post","at":{"tx":11,"ty":9},"w":1,"h":3,"overhang":2,"walk_under":True},
    {"id":"lamp_b","sprite":"tinderwick_lamp_post","at":{"tx":21,"ty":11},"w":1,"h":3,"overhang":2,"walk_under":True},
    {"id":"lamp_c","sprite":"tinderwick_lamp_post","at":{"tx":4,"ty":18},"w":1,"h":3,"overhang":2,"walk_under":True},
]

m["tilesets"][0]["tile_count"] = len(T)
m["layers"] = ([{"name":"base","role":"base","depth":0,"data":base}] + terrain_layers +
               [{"name":"deco","role":"deco","depth":5,"data":deco},
                {"name":"above","role":"above","depth":20,"data":[0]*W*H}])
m["objects"] = objects
MAP.write_text(json.dumps(m, indent=2) + "\n")
print(f"built {len(T)} ground tiles + {len(objects)} objects; terrain layers ready to expand")
