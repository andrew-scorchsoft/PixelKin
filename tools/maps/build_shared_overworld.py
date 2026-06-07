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

REPO = Path(__file__).resolve().parents[2]
TW = REPO / "assets" / "tilesets" / "tinderwick"          # proven master kit (by manifest)
DG = REPO / "assets" / "tilesets" / "dimglass_coast"      # coast extras (cliff/buoy/dock)
OUT = REPO / "assets" / "tilesets" / "_shared" / "vesper_overworld"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"
MT = SCRIPTS / "make_tileable.py"
OUT.mkdir(parents=True, exist_ok=True)


def load(p: Path) -> Image.Image:
    im = Image.open(p).convert("RGBA")
    # Only resample if it isn't already 16x16 — a same-size LANCZOS pass softens the
    # crisp pixel edges and can reintroduce a faint rim (the grid-seam gotcha).
    return im if im.size == (16, 16) else im.resize((16, 16), Image.NEAREST)


def arr(im: Image.Image) -> np.ndarray:
    return np.asarray(im).astype(np.int16)


def img(a: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def jitter(im: Image.Image, seed: int, amt: int = 10) -> Image.Image:
    """Per-pixel value jitter on opaque pixels — a different-but-same fill variant."""
    a = arr(im)
    rng = np.random.default_rng(seed)
    noise = rng.integers(-amt, amt + 1, size=a.shape[:2])
    for c in range(3):
        a[..., c] = a[..., c] + noise
    a[..., 3] = arr(im)[..., 3]  # keep alpha
    return img(a)


def roll(im: Image.Image, dx: int, dy: int) -> Image.Image:
    """Phase-shift the texture (foam crest moves along the shore) -> a new edge variant."""
    a = np.asarray(im)
    return Image.fromarray(np.roll(np.roll(a, dx, axis=1), dy, axis=0))


def flip_h(im: Image.Image) -> Image.Image:
    return im.transpose(Image.FLIP_LEFT_RIGHT)


# Which sides of an autotile role carry the DESIGNED transition (keep them); every
# other side's 1px rim is the model's baked ink border and must be stripped or it
# tiles into a visible grid (the seam the user flagged). After stripping, the axis
# the tile repeats on is seam-matched (opposite edges averaged) so it's toroidal.
KEEP = {
    "edge_n": {"N"}, "edge_s": {"S"}, "edge_w": {"W"}, "edge_e": {"E"},
    "corner_nw": {"N", "W"}, "corner_ne": {"N", "E"},
    "corner_se": {"S", "E"}, "corner_sw": {"S", "W"},
    "strip_h": {"N", "S"}, "strip_v": {"E", "W"}, "fill": set(),
}
H_TILE = {"edge_n", "edge_s", "strip_h", "fill"}   # repeats left↔right
V_TILE = {"edge_w", "edge_e", "strip_v", "fill"}   # repeats top↔bottom


def deborder(im: Image.Image, role: str) -> Image.Image:
    """Strip the baked rim on non-transition sides and seam the tiling axis."""
    a = np.asarray(im).astype(np.int16).copy()
    keep = KEEP.get(role, set())
    if "N" not in keep: a[0, :, :] = a[1, :, :]
    if "S" not in keep: a[-1, :, :] = a[-2, :, :]
    if "W" not in keep: a[:, 0, :] = a[:, 1, :]
    if "E" not in keep: a[:, -1, :] = a[:, -2, :]
    if role in H_TILE:
        m = (a[:, 0, :] + a[:, -1, :]) // 2
        a[:, 0, :] = m; a[:, -1, :] = m
    if role in V_TILE:
        m = (a[0, :, :] + a[-1, :, :]) // 2
        a[0, :, :] = m; a[-1, :, :] = m
    return img(a)


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
              encounter=None, ability=None, strips=False, variants=None):
    """Promote a Tinderwick autotile family by its manifest file names, with optional
    per-role variants (derived from the role's base tile) to break repetition."""
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
                v = roll(base, dx=(i + 1) * 4 + 1, dy=0)
            elif SEAM_OF.get(r) == "v":
                v = roll(base, dx=0, dy=(i + 1) * 4 + 1)
            else:
                v = jitter(base, seed, 7)
            v = deborder(v, r)   # re-seam after the transform
            vnm = f"{prefix}_{r}_v{i+1}"
            add(vnm, v, role=role, terrain=terrain, autotile=r, collides=collides,
                ability=ability)


# --- 1) ground grass fills (base scatter) + scatter decor --------------------
for i in range(4):
    add(f"grass{i}", load(TW / f"t0{i}_grass{i}.png"), role="ground", tileable_fill=True)

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
          variants={"fill": 2, "edge_n": 1, "edge_s": 1, "edge_w": 1, "edge_e": 1})
tw_family("tallgrass", "tallgrass", "ground", encounter="tall_grass", strips=True)
tw_family("sand", "sand", "sand",
          variants={"fill": 2, "edge_n": 2, "edge_s": 2, "edge_w": 1, "edge_e": 1})
tw_family("tree", "tree", "tree", collides=True,
          variants={"edge_n": 2, "edge_s": 1, "edge_w": 1, "edge_e": 1})
tw_family("water", "water", "water", collides=True, encounter="water", ability="tidecall",
          variants={"edge_n": 2, "edge_s": 2, "edge_w": 2, "edge_e": 2})

# water animation frames (referenced by the water fill tile, local indices resolved later)
add("water_a2", load(TW / "t53_water_a2.png"), role="water", collides=True, tileable_fill=True)
add("water_a3", load(TW / "t54_water_a3.png"), role="water", collides=True, tileable_fill=True)

# tree canopy (above-layer walk-under top) — kept for object trees too
add("canopy", load(TW / "t39_tree_fill.png"), role="canopy")

# --- 3) cliff family from the Dimglass coast masters (collide blob) ----------
# A grass-topped coastal cliff that meshes like the tree-wall. The kit is a partial
# 9-slice; we map what exists and mirror to fill the rest so every boundary cell gets
# an edge/corner tile (meshing PASS) and the wall reads as honest rock.
ck = DG / "cliff_kit"
cliff_map = {
    "corner_nw": "cliff_00", "edge_n": "cliff_01", "corner_ne": "cliff_02",
    "edge_w": "cliff_03", "fill": "cliff_04", "edge_e": None,   # mirror of edge_w
    "corner_sw": "cliff_05", "edge_s": "cliff_07", "corner_se": "cliff_06",
}
CLIFF_VARIANTS = {"fill": 1, "edge_n": 1, "edge_s": 1, "edge_w": 1, "edge_e": 1}
for r in NINE:
    src = cliff_map.get(r)
    if src:
        im = load(ck / f"{src}.png")
    elif r == "edge_e":
        im = flip_h(load(ck / "cliff_03.png"))
    else:
        im = load(ck / "cliff_04.png")
    im = deborder(im, r)
    add(f"cliff_{r}", im, role="cliff", terrain="cliff", autotile=r, collides=True,
        tileable_fill=(r == "fill"))
    # variants so a tall cliff wall / long ledge doesn't stamp one rock face
    for i in range(CLIFF_VARIANTS.get(r, 0)):
        seed = abs(hash(("cliff", r, i))) % 100000
        if r == "fill":
            v = jitter(im, seed, 8)
        elif SEAM_OF.get(r) == "h":
            v = roll(im, dx=(i + 1) * 5 + 1, dy=0)
        elif SEAM_OF.get(r) == "v":
            v = roll(im, dx=0, dy=(i + 1) * 5 + 1)
        else:
            v = jitter(im, seed, 6)
        add(f"cliff_{r}_v{i+1}", deborder(v, r), role="cliff", terrain="cliff",
            autotile=r, collides=True, tileable_fill=(r == "fill"))

# --- 4) accents / decor (reuse) ----------------------------------------------
add("flowers", load(TW / "t55_flowers.png"), role="decor")
add("sign", load(TW / "t56_sign.png"), role="sign", collides=True)
add("fence", load(TW / "14_fence.png"), role="fence", collides=True)
add("lamp", load(DG / "10_lamp.png"), role="decor")          # lamp-post breadcrumb
add("buoy", load(DG / "14_lantern_buoy.png"), role="decor")  # lantern-buoy (Tidecall tease)
add("dock", load(DG / "15_dock_board.png"), role="floor")    # dock plank

# ---- write masters, manifest, index, then pack ------------------------------
name_index = {nm: i for i, (nm, _, _) in enumerate(TILES)}
# resolve the water animation now that indices are known
water_anim = {"frames": [name_index["water_fill"], name_index["water_a2"],
                         name_index["water_a3"]], "duration_ms": 800}

manifest_tiles = []
for i, (nm, im, extra) in enumerate(TILES):
    fn = f"{i:03d}_{nm}.png"
    # seamless pass: autotile tiles by their role; plain ground/anim fills as 'fill'.
    role = extra.get("autotile")
    if role:
        im = deborder(im, role)
    elif nm in _tileable:
        im = deborder(im, "fill")
    im.save(OUT / fn)
    entry = {"file": fn, **extra}
    if nm == "water_fill":
        entry["animation"] = water_anim
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
