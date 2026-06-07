#!/usr/bin/env python3
"""
Build Pearlmoor Quay's three enterable interiors — the Tide LUMENARY (Reyl Wash's
sea-shrine chamber + battle), the port CHANDLERY (shop), and the quayside INN —
reusing the existing `tinderwick_house_set` interior tileset (floor / wall / door /
furniture), exactly as build_tinderwick_interiors.py does.

Interiors are single-screen cosy rooms (level-design §2/§7.2): a solid wall ring, a wood
floor, an exit DOOR on the bottom edge whose step-on warp lands on the walkable tile just
OUTSIDE the building's town-side door (the approach tile, never the colliding door-art tile).
Furniture is kept simple and clean (a follow-up pass polishes interior decor) — no column
of identical rug discs.

NOTE on validation: validate_map.py is the OVERWORLD quality gate (it needs terrain/autotile
vocabulary, which an interior tileset deliberately lacks — the stock tinderwick interiors fail
it too). Interiors are checked by EYE via render_map.py (/tmp/<id>.png).

Interior tileset gids (first_gid=1):  1 floor · 2 wall(collides) · 3 floor-alt(rug) ·
                                       4 barrel(collides) · 5 chest(collides) · 6 door
Run:  python3 tools/maps/build_pearlmoor_interiors.py
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


def build_lumenary():
    """Reyl Wash's Tide Lumenary chamber. Return-door lands outside the town Lumenary
    door (col 3 = the walkable arch twin tile, since col 2 is the interact-warp tile)."""
    W, H = 14, 11
    door_x = W // 2  # exit door centred on the bottom edge (tx 7)
    base = grid(W, H)
    wall_ring(base, W, H)
    base[(H - 1) * W + door_x] = DOOR
    # a single-tile aisle rug runs up the centre toward the warden's sea-altar
    for y in range(3, H - 1):
        base[y * W + door_x] = RUG

    deco = grid(W, H)
    # the warden's sea-altar furniture flanking the Tide constellation altar at the back
    deco[2 * W + (door_x - 2)] = CHEST
    deco[2 * W + (door_x + 1)] = CHEST
    # net-barrels / lantern stands lining the aisle
    for y in (4, 6, 8):
        deco[y * W + 2] = BARREL
        deco[y * W + (W - 3)] = BARREL

    return {
        "id": "pearlmoor_lumenary", "display_name": "Pearlmoor Tide Lumenary",
        "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "interior",
        "tilesets": [HOUSE_SET],
        "layers": [
            {"name": "base", "role": "base", "depth": 0, "data": base},
            {"name": "deco", "role": "deco", "depth": 5, "data": deco},
        ],
        "warps": [
            # Exit to the town tile just outside the Lumenary's walkable arch twin (14,7).
            {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
             "to_map": "pearlmoor_quay", "to": {"tx": 14, "ty": 7}, "facing": "down", "transition": "door"},
        ],
        "triggers": [
            # The Tide bond-test: Reyl Wash's battle, gated on holding a starter. On a win the
            # trainer's reward_flags (gleam:tide, crown_south) + reward_abilities (tidecall) apply.
            {"id": "lumenary_battle", "kind": "cutscene", "at": {"tx": door_x, "ty": 3},
             "activation": "step_on", "ref": "script.lumenary_pearlmoor", "once": True,
             "requires_flag": "flag:has_starter"},
            {"id": "sign_lumenary", "kind": "sign", "at": {"tx": 2, "ty": 2}, "activation": "interact",
             "ref": "sign.pearlmoor_lumenary"},
        ],
        "encounters": [],
        "npcs": [
            # Reyl Wash, the Tide Lampwarden, an old ferryman, at the sea-altar.
            {"id": "reyl", "at": {"tx": door_x - 1, "ty": 2}, "facing": "down",
             "sprite": "npc_lampwarden", "movement": "static",
             "dialogue_ref": "npc.reyl_wash"},
        ],
        "gates": [], "music": "assets/audio/music/dimglass-coast-a.mp3",
    }


def build_shop():
    W, H = 12, 9
    door_x = W // 2  # exit door centred on the bottom edge (tx 6)
    base = grid(W, H)
    wall_ring(base, W, H)
    base[(H - 1) * W + door_x] = DOOR

    deco = grid(W, H)
    # chandlery counter: a row of chests/barrels reading as a sales counter across the back
    for x in range(2, 7):
        deco[2 * W + x] = CHEST
    deco[2 * W + 7] = BARREL
    # a couple of stock barrels in the corner
    deco[5 * W + 9] = BARREL
    deco[6 * W + 9] = BARREL

    return {
        "id": "pearlmoor_shop", "display_name": "Pearlmoor Chandlery",
        "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "interior",
        "tilesets": [HOUSE_SET],
        "layers": [
            {"name": "base", "role": "base", "depth": 0, "data": base},
            {"name": "deco", "role": "deco", "depth": 5, "data": deco},
        ],
        "warps": [
            # Step out to the town tile just outside the chandlery door (the approach, 5,12).
            {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
             "to_map": "pearlmoor_quay", "to": {"tx": 5, "ty": 12}, "facing": "down", "transition": "door"},
        ],
        "triggers": [
            {"id": "sign_wares", "kind": "sign", "at": {"tx": 8, "ty": 2}, "activation": "interact",
             "ref": "sign.pearlmoor_shop"},
        ],
        "encounters": [],
        "npcs": [
            {"id": "chandler", "at": {"tx": door_x - 1, "ty": 3}, "facing": "down",
             "sprite": "npc_shopkeeper", "movement": "static",
             "dialogue_ref": "npc.pearlmoor_shopkeeper"},
        ],
        "gates": [], "music": "assets/audio/music/dimglass-coast-a.mp3",
    }


def build_inn():
    W, H = 12, 9
    door_x = W // 2  # exit door centred on the bottom edge (tx 6)
    base = grid(W, H)
    wall_ring(base, W, H)
    base[(H - 1) * W + door_x] = DOOR

    deco = grid(W, H)
    # a simple, clean inn common-room: a counter at the back-left, a couple of seats.
    deco[2 * W + 2] = CHEST
    deco[2 * W + 3] = CHEST
    deco[5 * W + 8] = BARREL
    deco[5 * W + 2] = BARREL

    return {
        "id": "pearlmoor_inn", "display_name": "Pearlmoor Quayside Inn",
        "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "interior",
        "tilesets": [HOUSE_SET],
        "layers": [
            {"name": "base", "role": "base", "depth": 0, "data": base},
            {"name": "deco", "role": "deco", "depth": 5, "data": deco},
        ],
        "warps": [
            # Step out to the town tile just outside the inn door (the approach, 22,12).
            {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
             "to_map": "pearlmoor_quay", "to": {"tx": 22, "ty": 12}, "facing": "down", "transition": "door"},
        ],
        "triggers": [
            {"id": "sign_welcome", "kind": "sign", "at": {"tx": 9, "ty": 2}, "activation": "interact",
             "ref": "sign.pearlmoor_welcome"},
        ],
        "encounters": [],
        "npcs": [
            {"id": "innkeep", "at": {"tx": door_x - 2, "ty": 3}, "facing": "down",
             "sprite": "npc_shopkeeper", "movement": "static",
             "dialogue_ref": "npc.pearlmoor_innkeep"},
            {"id": "fisher", "at": {"tx": door_x + 2, "ty": 4}, "facing": "left",
             "sprite": "wren", "movement": "static",
             "dialogue_ref": "npc.pearlmoor_fisher"},
        ],
        "gates": [], "music": "assets/audio/music/dimglass-coast-a.mp3",
    }


def write_and_render(m):
    path = MAPS / f"{m['id']}.json"
    path.write_text(json.dumps(m, indent=2) + "\n")
    out = Path("/tmp") / f"{m['id']}.png"
    subprocess.run([sys.executable, str(SCRIPTS / "render_map.py"), str(path),
                    "--output", str(out), "--scale", "6"], capture_output=True)
    print(f"  wrote {path.relative_to(REPO)}  ->  rendered {out}")


if __name__ == "__main__":
    for m in (build_lumenary(), build_shop(), build_inn()):
        write_and_render(m)
    print("DONE")
