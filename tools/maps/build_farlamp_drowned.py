#!/usr/bin/env python3
"""
The Drowned Lamp (10-the-farlamp-isles.md Part I, I6 + I7; kind cave, portal,
the set-piece). The Farlamp's lantern-room, gone under: the sea rose a fathom the
night the deep came up, the lighthouse's rock went down, and the great lamp fell
to the floor of its own tower — still burning, for a while. The tower's last
air is trapped here, a bubble of dry stone under the sea, and the lamp sits in
the middle of it, cold.

  * The ladder down from the Drowned Stair lands on the north step.
  * THE LAMP (centre, 4x5): `script.farlamp_lamp`. Before `flag:isles_dawn` it
    runs the RELIGHT (I6: the minor->major cadence, the isles' own dawn — no
    Gleam) and then FARLUME rises (I7: `legendaryBattle`, lv 68, cooldown 12).
    After, it just burns.
  * FARLUME (#177) waits by the lamp (`flag:isles_dawn`, until caught) for a
    retry once the cooldown's run.
  * THE STORE (south), behind the keeper's SLUICE: a junction race that only
    runs inward once you've read the keeper's fourth page (`flag:isles_log_4` —
    it tells you where she left the store's key). Inside: the signature
    Star-chart. A return race brings you out.

HANDSHAKE: `ladder_up` (10,1) <-> undertide_iv `ladder_down` (16,28).

Run:  python3 tools/maps/build_farlamp_drowned.py
"""
from __future__ import annotations

from undertidekit import Floor

PLAN = [
    "####################",
    "##########.#########",
    "#########...########",
    "######ooo...ooo#####",
    "#####ooo.....ooo####",
    "####oo.........oo###",
    "###oo...........oo##",
    "##oo...=======...oo#",
    "##o...=========...o#",
    "#oo...=========...o#",
    "#oo...=========...o#",
    "#oo...=========...o#",
    "#oo...=========...o#",
    "##o...=========...o#",
    "##oo...=======...oo#",
    "###oo...........oo##",
    "####oo.........oo###",
    "#####ooo.....ooo####",
    "#####~~~~J~~^~~#####",
    "#####~,,,,,,,,~#####",
    "#####~,,,,,,,,~#####",
    "####################",
]

LOG4 = "flag:isles_log_4"
DAWN = "flag:isles_dawn"

f = Floor("farlamp_drowned", "The Drowned Lamp", PLAN, seed=17705,
          backdrops=["assets/backgrounds/battle/farlamp-drowned-a.webp"])
f.junction((9, 18), "up", "down", LOG4)
f.home = (10, 2)

f.ladder("up", (10, 1), "undertide_iv", (16, 28))

# ---- the lamp --------------------------------------------------------------------
f.obj("farlamp_dark", "undertide_lamp_dark", (8, 6), 4, 5, overhang=2, walk_under=True,
      hidden_when_flag=DAWN)
f.obj("farlamp_lit", "undertide_lamp_lit", (8, 6), 4, 5, overhang=2, walk_under=True,
      requires_flag=DAWN)
for x in range(8, 12):
    f.m["triggers"].append({"id": f"farlamp_{x}", "kind": "script", "at": {"tx": x, "ty": 10},
                            "activation": "interact", "ref": "script.farlamp_lamp"})
f.m["npcs"].append({"id": "farlume", "at": {"tx": 10, "ty": 13}, "facing": "down",
                    "sprite": "kin_177_overworld", "movement": "static",
                    "dialogue_ref": "script.farlume_wake",
                    "requires_flag": DAWN, "hidden_when_flag": "flag:farlume_caught"})
f.solid_extra.add((10, 13))
f.owed += ["script.farlamp_lamp", "script.farlume_wake"]

# ---- the room's dressing: what the sea left -------------------------------------------
f.obj("pillar_w", "undertide_pillar", (3, 8), 2, 3, overhang=1)
f.obj("pillar_e", "undertide_pillar", (15, 11), 2, 3, overhang=1)
f.obj("glass_w", "undertide_glassheap", (4, 14), 2, 1)
f.obj("glass_e", "undertide_glassheap", (13, 5), 2, 1)
f.obj("kelp_w", "undertide_kelp", (6, 4), 1, 2, overhang=1, walk_under=True, solid=False)
f.obj("kelp_e", "undertide_kelp", (16, 7), 1, 2, overhang=1, walk_under=True, solid=False)
f.obj("logbook_desk", "undertide_logbook", (13, 15), 1, 1)
f.m["triggers"].append({"id": "keeper_desk", "kind": "script", "at": {"tx": 13, "ty": 15},
                        "activation": "interact", "ref": "script.farlamp_keeper_desk"})
f.owed.append("script.farlamp_keeper_desk")

# ---- the store, behind the sluice ---------------------------------------------------
f.post(1, (8, 18), LOG4)
f.m["triggers"].append({"id": "sluice", "kind": "script", "at": {"tx": 9, "ty": 18},
                        "activation": "interact", "ref": "script.farlamp_sluice"})
f.owed.append("script.farlamp_sluice")
f.cache("farlamp_store_chart", (7, 20))
f.obj("store_camp", "undertide_camp", (10, 19), 2, 2, solid=False)

f.scatter(["glass_a", "glass_b", "barnacle_a", "shell_a", "wrack_a"], 14, chars="=")

f.m["ambience"] = {
    "particles": [{"kind": "glowmotes", "density": 0.3}],
    "tint": {"color": "#04101e", "alpha": 0.4}, "sound_bed": "amb-surf",
    "when": [{"flag": DAWN, "ambience": {
        "particles": [{"kind": "glowmotes", "density": 0.8}, {"kind": "dust", "density": 0.4}],
        "tint": {"color": "#ffd890", "alpha": 0.08},
        "light_sources_extra": [{"at": {"tx": 10, "ty": 8}, "radius": 72, "color": "#ffd890"}],
        "sound_bed": "amb-surf"}}],
}

# ---- the proof --------------------------------------------------------------------
f.prove()
store = f.pocket_of((8, 20))
assert store not in f.reach((10, 2), {LOG4: False})
assert store in f.reach((10, 2), {LOG4: True})

f.finish(floor_mix=0.3)

if __name__ == "__main__":
    raise SystemExit(f.build())
