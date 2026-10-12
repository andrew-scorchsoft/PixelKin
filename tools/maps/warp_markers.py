"""
warp_markers — place the drawn "this is a way through" props
(`draw_warp_markers.py` -> `markers_<stem>`) on a map, the one shared helper the
builders call so every marker object has the same shape.

A marker is set dressing: never solid (the warp tile must stay walkable, and a
wall tile under an arch is solid on its own), drawn BELOW the player, and never
bobbing (a jetty/skiff hanging over water stays put with the planks it joins).
Gate it with `requires_flag` = the warp's own flag so a sealed way stays plain
until it opens. `audit_warp_markers.py` is the gate that proves coverage.

    import warp_markers as wm
    wm.add(m, wm.marker("mouth_mine", "cave_mouth_wide", 13, 0, 2, 2))
"""
from __future__ import annotations

# stem -> footprint (w, h) — keep in step with draw_warp_markers.MARKERS
SIZES = {
    "cave_mouth": (1, 2), "cave_mouth_wide": (2, 2),
    "side_mouth_e": (2, 3), "side_mouth_w": (2, 3),
    "wood_arch": (1, 2), "steps_s": (1, 1), "steps_n": (1, 2),
    "ladder_up": (1, 1), "mine_hatch": (1, 1), "rope_ladder": (1, 2),
    "lift_basket": (1, 1), "jetty": (1, 2), "pier_end": (2, 2),
    "sea_buoy": (1, 1), "vigil_seam": (1, 1), "trapdoor": (1, 1),
    "chute_mouth": (1, 1), "updraft_vent": (1, 1),
}


def marker(oid: str, stem: str, tx: int, ty: int, *,
           requires_flag: str | None = None, bob: bool | None = False) -> dict:
    w, h = SIZES[stem]
    o: dict = {"id": oid, "sprite": f"markers_{stem}", "at": {"tx": tx, "ty": ty},
               "w": w, "h": h, "solid": False}
    if bob is not None:
        o["bob"] = bob
    if requires_flag:
        o["requires_flag"] = requires_flag
    return o


def add(m: dict, *objs: dict) -> None:
    """Upsert marker objects by id (idempotent across re-runs)."""
    lst = m.setdefault("objects", [])
    for o in objs:
        for i, cur in enumerate(lst):
            if cur.get("id") == o["id"]:
                lst[i] = o
                break
        else:
            lst.append(o)
