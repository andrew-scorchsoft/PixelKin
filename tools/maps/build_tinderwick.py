#!/usr/bin/env python3
"""
Build the gold-standard Tinderwick tileset + map (the autotile/object template).

Two classes of art (docs/art-style.md §14b):
  - GROUND = recessive borderless autotile surfaces (grass variants + path/sand/
    water/forest/tall-grass edge sets), meshed from a `terrain` layer.
  - STRUCTURES = whole multi-tile OBJECTS (cottage/shop/Lumenary/trees/lamps).

The map is authored PROCEDURALLY here (34x26): a 2-deep TREE-WALL border (runs off
the map edges via the autotiler's continuation rule), a central path spine to the
north exit, buildings along a street, a tall-grass verge by the exit, sand + sea
at the south. Re-run any time; tools/autotile then meshes the terrain layers.

Run:  ./venv/bin/python tools/maps/build_tinderwick.py
Then: pack_tileset.py ; pack_objects.py ; expand.mjs ; render_map.py ; validate_map.py
"""
from __future__ import annotations
import json, random, subprocess, sys
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
TD = REPO / "assets" / "tilesets" / "tinderwick"
GV = TD / "grass_variants"
MAP = REPO / "public" / "assets" / "maps" / "tinderwick.json"
MT = REPO / ".claude/skills/generate-sprite-sheet/scripts/make_tileable.py"
EDGES = ["corner_nw","edge_n","corner_ne","edge_w","fill","edge_e","corner_sw","edge_s","corner_se"]

def nine(terrain, srcdir, **flags):
    """9-slice (+ optional strip_h/strip_v if strips=True) for an autotile terrain."""
    role = flags.pop("role", terrain); strips = flags.pop("strips", False); out = []
    roles = list(EDGES) + (["strip_h", "strip_v"] if strips else [])
    for r in roles:
        f = next(Path(srcdir).glob(f"*_{r}.png"))
        out.append(dict(name=f"{terrain}_{r}", src=str(f), role=role, terrain=terrain,
                        autotile=r, tileable=(r == "fill"), **flags))
    return out

# --- ground-only tileset (gid = index+1); structures are objects -------------
T = [
    dict(name="grass0", src=str(GV/"grass_00.png"), role="ground", tileable=True),
    dict(name="grass1", src=str(GV/"grass_01.png"), role="ground", tileable=True),
    dict(name="grass2", src=str(GV/"grass_02.png"), role="ground", tileable=True),
    dict(name="grass3", src=str(GV/"grass_03.png"), role="ground", tileable=True),
]
# path + tall-grass are FLAT transitions -> composited autotile bodies (uniform
# fill + dithered grass edge), not AI-per-cell. tall grass meshes into one field.
T += nine("path", "/tmp/path_auto", role="path", strips=True)
T += nine("tallgrass", "/tmp/tg_auto", role="ground", encounter="tall_grass", strips=True)
T += nine("sand", "/tmp/sand9_t", role="sand")
T += nine("tree", "/tmp/tree9_t", role="tree", collides=True)
T += nine("water", "/tmp/water9_tiles", role="water", collides=True, encounter="water", ability="tidecall")
T.append(dict(name="water_a2", src="/tmp/water_raw/01_frame1.png", role="water", collides=True, tileable=True))
T.append(dict(name="water_a3", src="/tmp/water_raw/02_frame2.png", role="water", collides=True, tileable=True))
T.append(dict(name="flowers", src=str(TD/"04_flowers.png"), role="decor"))
T.append(dict(name="sign", src=str(TD/"05_sign.png"), role="sign", collides=True))
idx = {t["name"]: i for i, t in enumerate(T)}
def gid(n): return idx[n] + 1

manifest = []
for i, t in enumerate(T):
    dst = TD / f"t{i:02d}_{t['name']}.png"
    Image.open(t["src"]).convert("RGBA").resize((16, 16), Image.LANCZOS).save(dst)
    if t.get("tileable"):
        subprocess.run([sys.executable, str(MT), str(dst)], capture_output=True)
    # edge tiles: seam-match along the axis they repeat on (shoreline/path/wall)
    ax = {"edge_n": "h", "edge_s": "h", "edge_w": "v", "edge_e": "v"}.get(t.get("autotile"))
    if ax:
        subprocess.run([sys.executable, str(MT), str(dst), "--axis", ax], capture_output=True)
    e = {"file": dst.name, "role": t["role"]}
    for k, kk in [("terrain","terrain"),("autotile","autotile"),("collides","collides"),
                  ("encounter","encounter_terrain"),("ability","requires_ability")]:
        if t.get(k): e[kk] = t[k]
    manifest.append(e)
manifest[idx["water_fill"]]["animation"] = {"frames":[idx["water_fill"],idx["water_a2"],idx["water_a3"]],"duration_ms":800}
(TD/"tileset.manifest.json").write_text(json.dumps({"name":"tinderwick_set","columns":8,"tiles":manifest}, indent=2)+"\n")

# --- procedural layout (34x30) -----------------------------------------------
W, H = 34, 30
def grid(): return [0]*(W*H)
def rect(g, x0, y0, x1, y1):
    for y in range(max(0,y0), min(H,y1+1)):
        for x in range(max(0,x0), min(W,x1+1)): g[y*W+x] = 1
def hline(g, y, x0, x1): rect(g, x0, y, x1, y)
def vline(g, x, y0, y1): rect(g, x, y0, x, y1)

EXIT = (16, 18)        # north exit gap columns
STREET_Y = 10
SPINE_X = 17
SEA_Y0 = 24            # big sea rows 24-29; wide beach rows 22-23

# tree wall: 2-deep N/E/W (down to the sand), gap at the north exit
tree = grid()
rect(tree, 0, 0, W-1, 1)                       # north band (2 deep)
for x in range(EXIT[0], EXIT[1]+1):            # punch the exit gap
    tree[0*W+x] = 0; tree[1*W+x] = 0
rect(tree, 0, 0, 1, SEA_Y0-4)                  # west band (stops above the beach)
rect(tree, W-2, 0, W-1, SEA_Y0-4)             # east band

water = grid(); rect(water, 0, SEA_Y0, W-1, H-1)        # full-width sea, continues off bottom
sand = grid(); rect(sand, 0, SEA_Y0-3, W-1, SEA_Y0-1)   # full-width 3-row beach (edge/fill/edge)
tallgrass = grid(); rect(tallgrass, 9, 3, 13, 4)   # verge near the exit approach

# paths: spine (exit -> street -> shore) + the street + door stubs
path = grid()
vline(path, SPINE_X, 2, SEA_Y0-3)              # spine
hline(path, STREET_Y, 4, 30)                   # street along the building fronts
# door-front stubs (cols of each building's door, from door-front down to street/up)
for sx in (6, 28):                             # shop + cottage door columns to street
    vline(path, sx, STREET_Y, STREET_Y)        # (fronts already on street row)
vline(path, 28, STREET_Y, 19)                  # cottage sits lower; run a lane down to it
hline(path, 19, 24, 28)                         # cottage front lane

# base = scattered recessive grass; terrain layers expand over it
rng = random.Random(11)
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.45 else gg[0] for _ in range(W*H)]

terrain_layers = [
    {"name":"t_tallgrass","role":"terrain","terrain":"tallgrass","set":"tinderwick_set","depth":0,"data":tallgrass},
    {"name":"t_tree","role":"terrain","terrain":"tree","set":"tinderwick_set","depth":0,"data":tree},
    {"name":"t_path","role":"terrain","terrain":"path","set":"tinderwick_set","depth":0,"data":path},
    {"name":"t_sand","role":"terrain","terrain":"sand","set":"tinderwick_set","depth":0,"data":sand},
    {"name":"t_water","role":"terrain","terrain":"water","set":"tinderwick_set","depth":0,"data":water},
]

# decoration: a few flower clumps + signs on grass
deco = grid_dec = [0]*(W*H)
for (x,y) in [(11,7),(25,7),(8,13),(30,14),(13,20),(22,20)]:
    grid_dec[y*W+x] = gid("flowers")
for (x,y) in [(6,11),(20,11),(SPINE_X,5)]:
    grid_dec[y*W+x] = gid("sign")

# objects: buildings (doors on row 9 -> fronts on the street row 10), trees, lamps
objects = [
    {"id":"shop","sprite":"tinderwick_shop","at":{"tx":4,"ty":6},"w":5,"h":4,"overhang":2},
    {"id":"lumenary","sprite":"tinderwick_lumenary","at":{"tx":18,"ty":4},"w":6,"h":6,"overhang":3},
    {"id":"house","sprite":"tinderwick_cottage","at":{"tx":26,"ty":14},"w":5,"h":5,"overhang":3},
    {"id":"tree_a","sprite":"tinderwick_tree","at":{"tx":4,"ty":15},"w":3,"h":4,"overhang":3,"walk_under":True},
    {"id":"tree_b","sprite":"tinderwick_tree","at":{"tx":13,"ty":13},"w":3,"h":4,"overhang":3,"walk_under":True},
    {"id":"lamp_a","sprite":"tinderwick_lamp_post","at":{"tx":SPINE_X-1,"ty":7},"w":1,"h":3,"overhang":2,"walk_under":True},
    {"id":"lamp_b","sprite":"tinderwick_lamp_post","at":{"tx":SPINE_X+1,"ty":13},"w":1,"h":3,"overhang":2,"walk_under":True},
    {"id":"lamp_c","sprite":"tinderwick_lamp_post","at":{"tx":10,"ty":11},"w":1,"h":3,"overhang":2,"walk_under":True},
]

doors = {"shop":(6,9), "lumenary":(20,9), "house":(28,18)}
m = {
    "id":"tinderwick","display_name":"Tinderwick","width":W,"height":H,
    "tile_width":16,"tile_height":16,"kind":"town",
    "tilesets":[{"name":"tinderwick_set","image":"assets/tilesets/tinderwick_set.webp",
                 "tile_width":16,"tile_height":16,"first_gid":1,"columns":8,"tile_count":len(T)}],
    "layers":[{"name":"base","role":"base","depth":0,"data":base}] + terrain_layers +
             [{"name":"deco","role":"deco","depth":5,"data":deco},
              {"name":"above","role":"above","depth":20,"data":[0]*(W*H)}],
    "objects":objects,
    "warps":[
        {"id":"to_coast","at":{"tx":17,"ty":0},"trigger":"step_on","to_map":"dimglass_coast","to":{"tx":6,"ty":32},"facing":"up","transition":"fade"},
        {"id":"to_coast_w","at":{"tx":16,"ty":0},"trigger":"step_on","to_map":"dimglass_coast","to":{"tx":6,"ty":32},"facing":"up","transition":"fade"},
        {"id":"to_coast_e","at":{"tx":18,"ty":0},"trigger":"step_on","to_map":"dimglass_coast","to":{"tx":6,"ty":32},"facing":"up","transition":"fade"},
        {"id":"to_house","at":{"tx":28,"ty":18},"trigger":"interact","to_map":"tinderwick_house","to":{"tx":5,"ty":7},"facing":"up","transition":"door"},
    ],
    "triggers":[
        {"id":"intro_mentor","kind":"cutscene","at":{"tx":SPINE_X,"ty":7},"activation":"step_on","ref":"script.intro_mentor","once":True,"sets_flags":["flag:has_vesperlamp","flag:has_starter"]},
        {"id":"lumenary_battle","kind":"cutscene","at":{"tx":20,"ty":9},"activation":"interact","ref":"script.lumenary_tinderwick","once":True,"requires_flag":"flag:has_starter"},
        {"id":"sign_shop","kind":"sign","at":{"tx":6,"ty":11},"activation":"interact","ref":"sign.tinderwick_square"},
        {"id":"sign_lumenary","kind":"sign","at":{"tx":20,"ty":11},"activation":"interact","ref":"sign.tinderwick_lumenary"},
        {"id":"sign_mentor","kind":"sign","at":{"tx":SPINE_X,"ty":5},"activation":"interact","ref":"sign.tinderwick_mentor"},
    ],
    "encounters":[{"id":"verge_grass","terrain":"tall_grass","rect":{"tx":9,"ty":3,"w":5,"h":2},"encounter_rate":0.07,
                   "table":[{"kin_id":16,"weight":60,"min_level":2,"max_level":4},{"kin_id":10,"weight":40,"min_level":2,"max_level":3}]}],
    "npcs":[
        {"id":"mentor","at":{"tx":SPINE_X,"ty":8},"facing":"down","sprite":"npc_mentor","movement":"static","dialogue_ref":"npc.mentor_intro"},
        {"id":"child_runner","at":{"tx":12,"ty":12},"facing":"left","sprite":"npc_child","movement":"wander","dialogue_ref":"npc.child_lanterns"},
    ],
    "gates":[], "music":"assets/audio/music/tinderwick-a.mp3",
    "_doors": doors,
}
MAP.write_text(json.dumps(m, indent=2) + "\n")
print(f"built {len(T)} tiles + {len(objects)} objects; {W}x{H} map with tree-wall border; spawn ~ (28,19)")
