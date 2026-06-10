#!/usr/bin/env python3
"""
Build the SHARED Vesperholm overworld tileset — `vesper_overworld_set`.

One packed atlas + sidecar that *every* overworld map references by name + `first_gid`
(the engine resolves gids across multiple tilesets, MapLoader.ts), so areas stop each
baking a bespoke full atlas and instead share one cohesive vocabulary. A map only needs
to list the set in its `tilesets[]` and paint terrain layers — no per-area tile copies.

What it does (REUSE + targeted derivation — no API needed):
  * Promotes the PROVEN Tinderwick autotile families (grass, path, sand, tree, tall-grass,
    water 9/13-slice + water animation + flowers/sign/fence) — the gold-standard kit.
  * Adds DETERMINISTIC VARIANTS per high-visibility role (water shorelines, tree-wall tops,
    sand/path fills) so the autotiler (tools/autotile, variant-aware) scatters them and the
    tell-tale "one tile stamped across the whole edge" repetition disappears.
  * Synthesises sparse SCATTER DECOR (pebble, grass tuft, daisy, dark patch) that breaks the
    flat-field grid the way Pokémon ground decor does.
  * Reuses the Dimglass coast masters (cliff face/top, lantern-buoy, dock board, lamp) so the
    coast's genuine extras live in the shared set too.

Variants are just additional tiles sharing a (terrain, autotile) tag; tools/autotile picks
among them by a stable per-cell hash (blob.mjs pickVariant). One tile per role still works.

Run:  python3 tools/maps/build_shared_overworld.py
Then it packs to public/assets/tilesets/vesper_overworld_set.{webp,tileset.json} and writes
assets/tilesets/_shared/vesper_overworld.index.json (name -> local index) for map builders.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
import gbaforge
from tileforge import (load, deborder, jitter, roll, flip_h, whole_downscale,  # seam helpers
                       KEEP, H_TILE, V_TILE,
                       grade, deglow, texture_grass, tallgrass_tuft, cliff_strata,
                       cliff_wall_edge, inner_corner, flatten_vignette, flatten_axis, match_green_to,
                       flip_v, key_alpha,
                       draw_fence_h, draw_fence_post, draw_boulder, draw_flowerbed)

REPO = Path(__file__).resolve().parents[2]
TW = REPO / "assets" / "tilesets" / "tinderwick"          # proven master kit (by manifest)
DG = REPO / "assets" / "tilesets" / "dimglass_coast"      # coast extras (cliff/buoy/dock)
OUT = REPO / "assets" / "tilesets" / "_shared" / "vesper_overworld"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"
MT = SCRIPTS / "make_tileable.py"
OUT.mkdir(parents=True, exist_ok=True)


def arr(im: Image.Image) -> np.ndarray:
    return np.asarray(im).astype(np.int16)


def img(a: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


# ---- ordered tile list -------------------------------------------------------
# Each entry: (name, PIL image, manifest-extra dict). LOCAL index = position.
TILES: list[tuple[str, Image.Image, dict]] = []
_tileable: list[str] = []   # names whose saved PNG should be make_tileable'd (fills)
_seam: dict[str, str] = {}  # name -> axis for edge seam-matching


def add(name, im, role=None, terrain=None, autotile=None, collides=False,
        encounter=None, ability=None, tileable_fill=False, seam_axis=None, **extra):
    e: dict = {}
    if role: e["role"] = role
    if terrain: e["terrain"] = terrain
    if autotile: e["autotile"] = autotile
    if collides: e["collides"] = True
    if encounter: e["encounter_terrain"] = encounter
    if ability: e["requires_ability"] = ability
    e.update(extra)
    TILES.append((name, im, e))
    if tileable_fill: _tileable.append(name)
    if seam_axis: _seam[name] = seam_axis


# 9/13-slice roles in the order the families ship them.
NINE = ["corner_nw", "edge_n", "corner_ne", "edge_w", "fill", "edge_e",
        "corner_sw", "edge_s", "corner_se"]
STRIPS = ["strip_h", "strip_v"]
SEAM_OF = {"edge_n": "h", "edge_s": "h", "edge_w": "v", "edge_e": "v",
           "strip_h": "h", "strip_v": "v"}


# The TW master dir holds leftovers from several build passes; the MANIFEST is the
# authoritative (terrain, autotile) -> file mapping. Source from it, never a glob.
_TW_MANIFEST = json.loads((TW / "tileset.manifest.json").read_text())["tiles"]
_TW_BY_ROLE = {(t.get("terrain"), t.get("autotile")): t["file"]
               for t in _TW_MANIFEST if t.get("terrain") and t.get("autotile")}


def tw_family(prefix: str, terrain: str, role: str, *, collides=False,
              encounter=None, ability=None, strips=False, variants=None, post=None):
    """Promote a Tinderwick autotile family by its manifest file names, with optional
    per-role variants (derived from the role's base tile) to break repetition.
    `post(role, im) -> im` runs a per-tile grade/texture pass after deborder."""
    variants = variants or {}
    roles = list(NINE) + (STRIPS if strips else [])
    for r in roles:
        fname = _TW_BY_ROLE.get((terrain, r))
        if not fname or not (TW / fname).is_file():
            continue
        # Deborder the base UP FRONT so the rim is gone before any variant transform —
        # rolling a clean (toroidal) tile keeps it seamless; rolling a rimmed one drags
        # the dark border into the interior (a stripe deborder can't reach afterwards).
        base = deborder(load(TW / fname), r)
        if post:
            base = deborder(post(r, base), r)
        nm = f"{prefix}_{r}"
        is_fill = (r == "fill")
        add(nm, base, role=role, terrain=terrain, autotile=r, collides=collides,
            encounter=(encounter if is_fill else None), ability=ability)
        # variants: derive N extra tiles sharing the same (terrain, role) tag.
        for i in range(variants.get(r, 0)):
            seed = abs(hash((terrain, r, i))) % 100000
            if is_fill:
                v = jitter(base, seed, 9)
            elif SEAM_OF.get(r) == "h":
                v = jitter(flip_h(base), seed, 5) if i == 0 else jitter(base, seed, 6)
            elif SEAM_OF.get(r) == "v":
                v = jitter(flip_v(base), seed, 5) if i == 0 else jitter(base, seed, 6)
            else:
                v = jitter(base, seed, 7)
            v = deborder(v, r)   # re-seam after the transform
            vnm = f"{prefix}_{r}_v{i+1}"
            add(vnm, v, role=role, terrain=terrain, autotile=r, collides=collides,
                ability=ability)


# --- 1) ground grass fills (base scatter) + scatter decor --------------------
# grass0 stays the plain anchor; 1-3 carry sparse blade texture at rising density
# so a field reads as grass, not an untextured void (level-design §11).
_g0 = flatten_vignette(load(TW / "t00_grass0.png"))
_G0_MEAN = np.asarray(_g0.convert("RGBA")).astype(np.float64)[..., :3].mean()
GRASS_RGB = tuple(int(v) for v in np.asarray(_g0.convert("RGBA"))
                  .astype(np.float64)[..., :3].reshape(-1, 3).mean(0))


def _norm_mean(im):
    """Pin a ground fill's mean to grass0's so the base scatter never checkers."""
    a = np.asarray(im.convert("RGBA")).astype(np.float64)
    m = a[..., :3].mean()
    if m > 1:
        a[..., :3] = np.clip(a[..., :3] * (_G0_MEAN / m), 0, 255)
    return Image.fromarray(a.astype(np.uint8), "RGBA")


for i in range(4):
    g = _g0 if i == 0 else flatten_vignette(load(TW / f"t0{i}_grass{i}.png"))
    if i > 0:
        g = _norm_mean(texture_grass(g, seed=50 + i, density=5 + i * 2))
    add(f"grass{i}", g, role="ground", tileable_fill=True)

GRASS = arr(load(TW / "t00_grass0.png"))
gmean = GRASS[..., :3].reshape(-1, 3).mean(0)


def decor(name, paint):
    """A mostly-transparent 16x16 scatter prop that sits on grass (deco layer)."""
    a = np.zeros((16, 16, 4), dtype=np.int16)
    paint(a)
    add(name, img(a), role="decor")


def _pebble(a):
    for (x, y, c) in [(6, 9, 150), (7, 9, 170), (8, 10, 130), (7, 10, 110)]:
        a[y, x] = [c, c, c + 8, 255]


def _tuft(a):
    g = [int(gmean[0]) - 30, int(gmean[1]) - 20, int(gmean[2]) - 10, 255]
    for (x, y) in [(7, 11), (8, 9), (9, 11), (8, 10), (8, 12), (6, 12), (10, 12)]:
        a[y, x] = g


def _daisy(a):
    for (x, y) in [(7, 8), (9, 8), (8, 7), (8, 9)]:
        a[y, x] = [235, 238, 245, 255]
    a[8, 8] = [245, 210, 90, 255]
    a[11, 10] = [235, 238, 245, 255]; a[11, 9] = [245, 210, 90, 255]


def _patch(a):
    d = [int(gmean[0]) - 22, int(gmean[1]) - 18, int(gmean[2]) - 6, 110]
    for y in range(5, 12):
        for x in range(4, 13):
            if (x - 8) ** 2 + (y - 8) ** 2 <= 12:
                a[y, x] = d


decor("g_pebble", _pebble)
decor("g_tuft", _tuft)
decor("g_daisy", _daisy)
decor("g_patch", _patch)

# --- 2) autotile families (with de-repetition variants) ----------------------
tw_family("path", "path", "path", strips=True,
          variants={"fill": 2, "edge_n": 1, "edge_s": 1, "edge_w": 1, "edge_e": 1},
          post=lambda r, im: flatten_vignette(im) if r == "fill" else im)
# Sand: de-glow the baked highlight rim, flatten the fill, then VALUE-MATCH each
# edge tile's sand body to the fill's mean — otherwise the pocket/beach is ringed
# by a visibly darker edge band with a hard line where it meets the fill.
_sand_fill_master = flatten_vignette(deglow(deborder(
    load(TW / _TW_BY_ROLE[("sand", "fill")]), "fill"), 185, 0.6))
_SAND_MEAN = np.asarray(_sand_fill_master.convert("RGBA")).astype(np.float64)[..., :3].mean()


def _sand_post(r, im):
    im = deglow(im, 185, 0.6)
    if r == "fill":
        return flatten_vignette(im)
    a = np.asarray(im.convert("RGBA")).astype(np.float64)
    keep = KEEP.get(r, set())
    y0, y1, x0, x1 = 0, 16, 0, 16
    if "N" in keep: y0 = 6
    if "S" in keep: y1 = 10
    if "W" in keep: x0 = 6
    if "E" in keep: x1 = 10
    body = a[y0:y1, x0:x1, :3].mean()
    if body > 1:
        k = max(0.92, min(1.18, _SAND_MEAN / body))
        a = a.copy()
        a[..., :3] = np.clip(a[..., :3] * k, 0, 255)
        im = Image.fromarray(a.astype(np.uint8), "RGBA")
    return match_green_to(im, GRASS_RGB)


tw_family("sand", "sand", "sand",
          variants={"fill": 2, "edge_n": 2, "edge_s": 2, "edge_w": 1, "edge_e": 1},
          post=_sand_post)
tw_family("tree", "tree", "tree", collides=True,
          variants={"fill": 2, "edge_n": 2, "edge_s": 1, "edge_w": 1, "edge_e": 1},
          post=lambda r, im: im if r == "fill" else match_green_to(im, GRASS_RGB, 22))
# Water: value-match the deep fill toward the edge tiles' water tone — the raw
# fill is far darker than the foam-edge water, so concave bays and pond centres
# read as abrupt dark blocks instead of one body of water.
_w_edge = deborder(load(TW / _TW_BY_ROLE[("water", "edge_n")]), "edge_n")
_W_EDGE_MEAN = np.asarray(_w_edge.convert("RGBA")).astype(np.float64)[10:16, :, :3].mean()


def _water_post(r, im):
    if r != "fill":
        return im
    a = np.asarray(im.convert("RGBA")).astype(np.float64)
    body = a[..., :3].mean()
    if body > 1:
        k = max(1.0, min(1.45, 0.4 + 0.6 * _W_EDGE_MEAN / body))
        a[..., :3] = np.clip(a[..., :3] * k, 0, 255)
    return Image.fromarray(a.astype(np.uint8), "RGBA")


tw_family("water", "water", "water", collides=True, encounter="water", ability="tidecall",
          variants={"edge_n": 2, "edge_s": 2, "edge_w": 2, "edge_e": 2},
          post=_water_post)

# Tall grass is REDRAWN, not promoted: readable staggered blade-fan clumps over a
# darkened bed (tileforge.tallgrass_tuft). Hard-edged single tiles by design — the
# classic handheld encounter tile has no transition ring, which is exactly what makes
# a patch read as "grass you fight in" vs decorative ground. Fill + 2 phase variants.
_tg_base = flatten_vignette(load(TW / "t00_grass0.png"))
add("tallgrass_fill", tallgrass_tuft(_tg_base, 0), role="ground",
    terrain="tallgrass", autotile="fill", encounter="tall_grass")
for _i, _ph in enumerate((5, 11, 23)):
    # variants carry the encounter tag too — the autotiler scatters them per cell,
    # and a tall-grass cell must trigger encounters whichever variant landed on it.
    add(f"tallgrass_fill_v{_i+1}", tallgrass_tuft(_tg_base, _ph), role="ground",
        terrain="tallgrass", autotile="fill", encounter="tall_grass")

# water animation frames (referenced by the water fill tile, local indices resolved later)
add("water_a2", _water_post("fill", load(TW / "t53_water_a2.png")), role="water", collides=True, tileable_fill=True)
add("water_a3", _water_post("fill", load(TW / "t54_water_a3.png")), role="water", collides=True, tileable_fill=True)

# Cleaner sand→water shoreline (production art, Nano) added as water edge_n/edge_s variants:
# a horizontal wet-sand→foam→water band. edge_n = land(sand) above/water below (as drawn);
# edge_s = the same band flipped vertically. Gives a crisp foam shore beside a beach.
SRC = OUT.parent / "_src"
sw_n = whole_downscale(SRC / "swater.png", "edge_n")
sw_s = deborder(Image.fromarray(np.flipud(np.asarray(sw_n.convert("RGBA")))), "edge_s")
add("water_edge_n_sw", sw_n, role="water", terrain="water", autotile="edge_n", collides=True)
add("water_edge_s_sw", sw_s, role="water", terrain="water", autotile="edge_s", collides=True)

# tree canopy (above-layer walk-under top) — kept for object trees too
add("canopy", load(TW / "t39_tree_fill.png"), role="canopy")

# --- 3) cliff family from PRODUCTION ART (rugged slate cliff, grass-lip top) --
# A grass-topped coastal rock cliff that meshes like the tree-wall. Rock face on the
# fill + side/bottom edges; the grassy LIP on the top edge & top corners. Whole-image
# downscale of the flat-lit field renders, then role-aware deborder + variants so a
# tall wall doesn't stamp one face. (Replaces the old brick-looking legacy kit.)
cliff_face = whole_downscale(SRC / "cliff_face.png", "fill")          # rugged rock
cliff_lip = whole_downscale(SRC / "cliff_top.png", "edge_n")         # grass-on-top lip
GRASS_MEAN = tuple(int(v) for v in GRASS[..., :3].reshape(-1, 3).mean(0))
# The raw face renders near-black on a map (the old "void cliff" read). Lift it
# ~1.4x + strata seams so it reads as stratified rock. Edge semantics for a
# TOP-DOWN cliff mass: the open-NORTH side keeps the grassy plateau lip, but the
# open-SOUTH/W/E sides are drawn as complete WALL tiles (lit rim -> face -> dark
# contact seam -> ground, tileforge.cliff_wall_edge) — that vertical light ladder
# is the height cue (art-style §14); raw face texture ending abruptly is the old
# "texture slab" look.
_face = cliff_strata(grade(flatten_vignette(cliff_face), 1.38, 6), seed=11)
_lip = match_green_to(grade(cliff_lip, 1.28, 6), GRASS_RGB)
CLIFF_TILES = {
    "fill": _face,
    "edge_n": _lip,
    "corner_nw": cliff_wall_edge(_lip, GRASS_MEAN, "w"),
    "corner_ne": cliff_wall_edge(_lip, GRASS_MEAN, "e"),
    "edge_s": cliff_wall_edge(_face, GRASS_MEAN, "s"),
    "edge_w": cliff_wall_edge(_face, GRASS_MEAN, "w"),
    "edge_e": cliff_wall_edge(_face, GRASS_MEAN, "e"),
    "corner_sw": cliff_wall_edge(cliff_wall_edge(_face, GRASS_MEAN, "s"), GRASS_MEAN, "w"),
    "corner_se": cliff_wall_edge(cliff_wall_edge(_face, GRASS_MEAN, "s"), GRASS_MEAN, "e"),
}
CLIFF_VARIANTS = {"fill": 2, "edge_n": 1, "edge_s": 1, "edge_w": 1, "edge_e": 1}
for r in NINE:
    im = deborder(CLIFF_TILES[r], r)
    add(f"cliff_{r}", im, role="cliff", terrain="cliff", autotile=r, collides=True,
        tileable_fill=(r == "fill"))
    # variants so a tall cliff wall / long ledge doesn't stamp one rock face
    for i in range(CLIFF_VARIANTS.get(r, 0)):
        seed = abs(hash(("cliff", r, i))) % 100000
        if r == "fill":
            v = jitter(im, seed, 8)
        elif SEAM_OF.get(r) == "h":
            v = jitter(flip_h(im), seed, 5)
        elif SEAM_OF.get(r) == "v":
            v = jitter(flip_v(im), seed, 5)
        else:
            v = jitter(im, seed, 6)
        add(f"cliff_{r}_v{i+1}", deborder(v, r), role="cliff", terrain="cliff",
            autotile=r, collides=True, tileable_fill=(r == "fill"))

# --- 3b) inner (concave) corners — the 13-piece completion --------------------
# Synthesised from each family's fill + matching outer corner (tileforge.inner_corner)
# so concave joins (a bay in a shoreline, an alcove in a tree-line or cliff) curve
# instead of butting fill against edge at a hard right angle.
_BY_NAME = {nm: im for (nm, im, _e) in TILES}
# (water is deliberately absent: a synthetic concave foam corner reads as a stray
# sand wedge at 1x — water's fill fallback at inner corners looks better.)
_INNER_FAMS = [
    ("path", "path", False, None, 4), ("sand", "sand", False, None, 4),
    ("tree", "tree", True, None, 5), ("cliff", "cliff", True, None, 5),
]
for fam, terr, coll, abil, bite in _INNER_FAMS:
    fill_im = _BY_NAME.get(f"{fam}_fill")
    for q in ("nw", "ne", "sw", "se"):
        outer = _BY_NAME.get(f"{fam}_corner_{q}")
        if fill_im is None or outer is None:
            continue
        add(f"{fam}_inner_{q}", inner_corner(fill_im, outer, q, r=bite), role=fam,
            terrain=terr, autotile=f"inner_{q}", collides=coll, ability=abil)

# --- 4) accents / decor (reuse + drawn props) ---------------------------------
add("flowers", load(TW / "t55_flowers.png"), role="decor")
add("sign", load(TW / "t56_sign.png"), role="sign", collides=True)
add("fence", load(TW / "14_fence.png"), role="fence", collides=True)
add("lamp", key_alpha(load(DG / "10_lamp.png")), role="decor")  # legacy 1-tile lamp (keyed); prefer the lamp-post OBJECT
add("buoy", load(DG / "14_lantern_buoy.png"), role="decor")  # lantern-buoy (Tidecall tease)
add("dock", load(DG / "15_dock_board.png"), role="floor")    # dock plank

# Drawn vocabulary props (tileforge) — the funnelling/garden kit the reference-era
# maps lean on: fence runs + end posts, boulders, and flowerbed clusters.
add("fence_h", draw_fence_h(), role="fence", collides=True)
add("fence_post", draw_fence_post(), role="fence", collides=True)
add("boulder", draw_boulder(), role="decor", collides=True)
add("flowerbed_a", draw_flowerbed(1), role="decor")
add("flowerbed_b", draw_flowerbed(7), role="decor")

# --- 5) trail family — path over SAND (dune/beach routes) ---------------------
# The path family transitions to GRASS; painted across a dune it ringed the lane
# with grass-coloured borders. Trail is the same drawn lane composed over sand.
# APPENDED after every existing tile so all prior indices stay valid.
for _r in list(gbaforge.ROLES_OUTER.keys()) + list(gbaforge.INNER_Q.keys()):
    if _r == "fill":
        _tim = gbaforge.path_fill(0)
    else:
        _tim = gbaforge.overlay_tile(_r, gbaforge.path_fill(0), gbaforge.sand_fill(0),
                                     gbaforge.sh(gbaforge.PATH, 0.55),
                                     shade_rgb=gbaforge.sh(gbaforge.PATH, 0.9))
    add(f"trail_{_r}", _tim, role="path", terrain="trail", autotile=_r)
for _i in (1, 2):
    add(f"trail_fill_v{_i}", gbaforge.path_fill(_i), role="path",
        terrain="trail", autotile="fill")

# --- 5b) pond family — water over GRASS (inland ponds; appended, index-safe) --
# The water family's shoreline is drawn against SAND (the coast); an inland pond
# painted with it gets ringed by a beach. Pond is the same foam edge over grass.
for _r in [r for r in NINE if r != "fill"]:
    _pim = gbaforge.water_edge(_r, outer_im=gbaforge.grass_fill(0))
    add(f"pond_{_r}", _pim, role="water", terrain="pond", autotile=_r,
        collides=True, ability="tidecall")
add("pond_fill", gbaforge.water_fill(0), role="water", terrain="pond",
    autotile="fill", collides=True, encounter="water", ability="tidecall")

# --- 5c) dune grass — the encounter tuft over a SAND bed (tidal-flat crossings).
# Hard-edged fill-only like tallgrass; every variant carries the encounter tag.
for _i in range(3):
    add(f"dunegrass_fill{'' if _i == 0 else f'_v{_i}'}", gbaforge.dunegrass_fill(_i),
        role="ground", terrain="dunegrass", autotile="fill", encounter="tall_grass")

# ---- GBA-register structured redraw (gbaforge) -------------------------------
# The terrain families above established the *vocabulary* (names, roles, order —
# maps reference these by stable index). Their imagery, though, was AI-noise
# cured with seam passes. gbaforge replaces the imagery per NAME with drawn,
# structured tiles (flat base + deliberate motifs, crisp rounded transitions) —
# the cartridge-era look. Order never changes, so existing maps update for free.
import re as _re

_GBA_ROLE = r"(corner_[ns][we]|edge_[nswe]|fill|strip_[hv]|inner_[ns][we])"


def _gba_override(nm: str, cur: Image.Image) -> Image.Image | None:
    g = gbaforge
    m = _re.fullmatch(r"tree_(edge_[nswe]|corner_[ns][we])(?:_v\d+)?", nm)
    if m:
        # painterly bubble-crown masters stay; their inner half eases into the
        # drawn fill so the mass interior doesn't band.
        return g.tree_edge_blend(cur, m.group(1))
    if _re.fullmatch(r"grass[0-3]", nm):
        return g.grass_fill(int(nm[-1]))
    m = _re.fullmatch(r"tallgrass_fill(?:_v(\d+))?", nm)
    if m:
        return g.tallgrass_fill(int(m.group(1) or 0))
    m = _re.fullmatch(r"dunegrass_fill(?:_v(\d+))?", nm)
    if m:
        return g.dunegrass_fill(int(m.group(1) or 0))
    m = _re.fullmatch(r"tree_fill(?:_v(\d+))?", nm)
    if m:
        return g.tree_fill(int(m.group(1) or 0))
    if _re.fullmatch(r"tree_inner_[ns][we]", nm):
        # concave canopy joins read best as plain canopy (same call water makes)
        return g.tree_fill(0)
    if nm == "water_a2":
        return g.water_fill(1)
    if nm == "water_a3":
        return g.water_fill(2)
    if nm == "water_edge_n_sw":
        return g.water_edge("edge_n", phase=1)
    if nm == "water_edge_s_sw":
        return g.water_edge("edge_s", phase=1)
    m = _re.fullmatch(rf"(path|sand|water|cliff|trail|pond)_{_GBA_ROLE}(?:_v(\d+))?", nm)
    if not m:
        return None
    fam, role, v = m.group(1), m.group(2), int(m.group(3) or 0)
    if fam == "pond":
        if role == "fill":
            return g.water_fill(0)
        return g.water_edge(role, outer_im=g.grass_fill(0), phase=v)
    if fam == "trail":
        if role == "fill":
            return g.path_fill(v)
        return g.overlay_tile(role, g.path_fill(v), g.sand_fill(v),
                              g.sh(g.PATH, 0.55), shade_rgb=g.sh(g.PATH, 0.9))
    if fam == "path":
        if role == "fill":
            return g.path_fill(v)
        return g.overlay_tile(role, g.path_fill(v), g.grass_fill(v),
                              g.sh(g.PATH, 0.55), shade_rgb=g.sh(g.PATH, 0.9))
    if fam == "sand":
        if role == "fill":
            return g.sand_fill(v)
        return g.overlay_tile(role, g.sand_fill(v), g.grass_fill(v),
                              g.sh(g.SAND, 0.62), shade_rgb=g.sh(g.SAND, 0.88))
    if fam == "water":
        if role == "fill":
            return g.water_fill(0)
        return g.water_edge(role, phase=v)
    if fam == "cliff":
        return g.cliff_tile(role, v)
    return None


# ---- write masters, manifest, index, then pack ------------------------------
name_index = {nm: i for i, (nm, _, _) in enumerate(TILES)}
# resolve the water animation now that indices are known
water_anim = {"frames": [name_index["water_fill"], name_index["water_a2"],
                         name_index["water_a3"]], "duration_ms": 800}

manifest_tiles = []
for i, (nm, im, extra) in enumerate(TILES):
    fn = f"{i:03d}_{nm}.png"
    ov = _gba_override(nm, im)
    if ov is not None:
        # drawn tiles are seamless by construction — no seam pass (it would
        # smear the designed 1px borders).
        im = ov
    else:
        # seamless pass: autotile tiles by their role; plain ground/anim fills as 'fill'.
        role = extra.get("autotile")
        if role:
            ax = SEAM_OF.get(role)
            if ax:
                im = flatten_axis(im, ax)
            im = deborder(im, role)
        elif nm in _tileable:
            im = deborder(im, "fill")
    im.save(OUT / fn)
    entry = {"file": fn, **extra}
    if nm == "water_fill":
        entry["animation"] = water_anim
    if nm == "pond_fill":
        entry["animation"] = {"frames": [name_index["pond_fill"], name_index["water_a2"],
                                         name_index["water_a3"]], "duration_ms": 800}
    manifest_tiles.append(entry)

manifest = {"name": "vesper_overworld_set", "columns": 12, "tiles": manifest_tiles}
(OUT / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
(REPO / "assets/tilesets/_shared/vesper_overworld.index.json").write_text(
    json.dumps(name_index, indent=2) + "\n")

print(f"shared set: {len(TILES)} tiles -> {OUT}")
res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                      "--tiles-dir", str(OUT)], capture_output=True, text=True)
print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
sys.exit(res.returncode)
