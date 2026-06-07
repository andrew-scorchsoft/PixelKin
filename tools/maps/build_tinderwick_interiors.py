#!/usr/bin/env python3
"""
Build Tinderwick's two new enterable interiors — the general SHOP and the Ember LUMENARY —
reusing the existing `tinderwick_house_set` interior tileset (floor / wall / door / furniture),
exactly as tinderwick_house.json does.

Interiors are single-screen cosy rooms (level-design §2/§7.2): a solid wall ring, a wood
floor, an exit DOOR on the bottom edge (step-on warp back to town landing on the tile just
outside the building's town-side door), and a couple of furniture props + an NPC.

NOTE on validation: validate_map.py is the OVERWORLD quality gate (it requires terrain /
autotile vocabulary, which an interior tileset deliberately has none of — the stock
tinderwick_house.json fails it too). Interiors are therefore checked by EYE via render_map.py
(written to /tmp/<id>.png) rather than by that gate. This builder renders both and prints
the paths.

Interior tileset gids (first_gid=1):  1 floor · 2 wall(collides) · 3 floor-alt(rug) ·
                                       4 barrel(collides) · 5 chest(collides) · 6 door
Run:  python3 tools/maps/build_tinderwick_interiors.py
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS = REPO / "public/assets/maps"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

FLOOR, WALL, RUG, BARREL, CHEST, DOOR = 1, 2, 3, 4, 5, 6

HOUSE_SET = {
    "name": "tinderwick_house_set",
    "image": "assets/tilesets/tinderwick_house_set.webp",
    "tile_width": 16, "tile_height": 16,
    "first_gid": 1, "columns": 8, "tile_count": 6,
}


def grid(w, h, fill=0):
    return [fill] * (w * h)


def rect(g, w, x0, y0, x1, y1, val):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            g[y * w + x] = val


def wall_ring(base, w, h):
    """Floor everywhere, wall on the full border, an exit door gap centred on the bottom."""
    rect(base, w, 0, 0, w - 1, h - 1, FLOOR)
    rect(base, w, 0, 0, w - 1, 0, WALL)          # top
    rect(base, w, 0, 0, h - 1, 0, WALL)          # left
    rect(base, w, w - 1, 0, w - 1, h - 1, WALL)  # right
    rect(base, w, 0, h - 1, w - 1, h - 1, WALL)  # bottom


def build_shop():
    W, H = 12, 9
    door_x = W // 2  # exit door centred on the bottom edge (tx 6)
    base = grid(W, H)
    wall_ring(base, W, H)
    base[(H - 1) * W + door_x] = DOOR            # exit door tile (bottom edge)

    deco = grid(W, H)
    # shop counter: a row of chests/barrels reading as a sales counter across the back
    for x in range(2, 7):
        deco[2 * W + x] = CHEST
    deco[2 * W + 7] = BARREL
    # a couple of stock barrels in the corner
    deco[5 * W + 9] = BARREL
    deco[6 * W + 9] = BARREL

    m = {
        "id": "tinderwick_shop", "display_name": "Tinderwick General Store",
        "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "interior",
        "tilesets": [HOUSE_SET],
        "layers": [
            {"name": "base", "role": "base", "depth": 0, "data": base},
            {"name": "deco", "role": "deco", "depth": 5, "data": deco},
        ],
        "warps": [
            # Step out the door, back to the town tile just outside the shop's town door (5,8).
            {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
             "to_map": "tinderwick", "to": {"tx": 5, "ty": 8}, "facing": "down", "transition": "door"},
        ],
        "triggers": [
            {"id": "sign_wares", "kind": "sign", "at": {"tx": 8, "ty": 2}, "activation": "interact",
             "ref": "sign.tinderwick_shop_wares"},
        ],
        "encounters": [],
        "npcs": [
            {"id": "shopkeeper", "at": {"tx": door_x - 1, "ty": 3}, "facing": "down",
             "sprite": "npc_shopkeeper", "movement": "static",
             "dialogue_ref": "npc.tinderwick_shopkeeper"},
        ],
        "gates": [], "music": "assets/audio/music/tinderwick-b.mp3",
    }
    return m


def build_lumenary():
    W, H = 14, 11
    door_x = W // 2  # exit door centred on the bottom edge (tx 7)
    base = grid(W, H)
    wall_ring(base, W, H)
    base[(H - 1) * W + door_x] = DOOR
    # a single-tile aisle rug runs up the centre toward the warden's dais
    for y in range(3, H - 1):
        base[y * W + door_x] = RUG

    deco = grid(W, H)
    # the warden's dais furniture flanking the constellation altar at the back
    deco[2 * W + (door_x - 2)] = CHEST
    deco[2 * W + (door_x + 1)] = CHEST
    # braziers/barrels lining the aisle
    for y in (4, 6, 8):
        deco[y * W + 2] = BARREL
        deco[y * W + (W - 3)] = BARREL

    m = {
        "id": "tinderwick_lumenary", "display_name": "Tinderwick Lumenary",
        "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "interior",
        "tilesets": [HOUSE_SET],
        "layers": [
            {"name": "base", "role": "base", "depth": 0, "data": base},
            {"name": "deco", "role": "deco", "depth": 5, "data": deco},
        ],
        "warps": [
            # Exit back to the town tile just outside the Lumenary's town door (19,8).
            {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
             "to_map": "tinderwick", "to": {"tx": 19, "ty": 8}, "facing": "down", "transition": "door"},
        ],
        "triggers": [
            # The Ember bond-test: Brisa Tallow's battle, gated on holding a starter.
            {"id": "lumenary_battle", "kind": "cutscene", "at": {"tx": door_x, "ty": 3},
             "activation": "step_on", "ref": "script.lumenary_tinderwick", "once": True,
             "requires_flag": "flag:has_starter"},
            {"id": "sign_lumenary", "kind": "sign", "at": {"tx": 2, "ty": 2}, "activation": "interact",
             "ref": "sign.tinderwick_lumenary_inside"},
        ],
        "encounters": [],
        "npcs": [
            # Brisa Tallow, the Ember Lampwarden, at the constellation altar.
            {"id": "brisa", "at": {"tx": door_x - 1, "ty": 2}, "facing": "down",
             "sprite": "npc_lampwarden", "movement": "static",
             "dialogue_ref": "npc.brisa_tallow"},
        ],
        "gates": [], "music": "assets/audio/music/tinderwick-a.mp3",
    }
    return m


def write_and_render(m):
    path = MAPS / f"{m['id']}.json"
    path.write_text(json.dumps(m, indent=2) + "\n")
    out = Path("/tmp") / f"{m['id']}.png"
    subprocess.run([sys.executable, str(SCRIPTS / "render_map.py"), str(path),
                    "--output", str(out), "--scale", "6"], capture_output=True)
    print(f"  wrote {path.relative_to(REPO)}  ->  rendered {out}")


if __name__ == "__main__":
    for m in (build_shop(), build_lumenary()):
        write_and_render(m)
    print("DONE")
