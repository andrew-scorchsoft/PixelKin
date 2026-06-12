#!/usr/bin/env python3
"""Expand docs/mechanics/concepts/selected.json (151 chosen concepts) into full,
schema-valid species records (docs/mechanics/08-data-schema.md).

Mechanical fields (stats, BST, catch rate, kindling wiring, learnsets, abilities,
encounters) are generated DETERMINISTICALLY from each concept's role/tier/type/
region/line so the roster is guaranteed valid and balanced; the creative content
(name, concept, visual, size/weight, hook) comes from the design panel's chosen
concepts. Writes one file per species to src/game/data/species/NNN_slug.json and
a combined src/game/data/species.json.
"""
import json, os, re, hashlib
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEL = os.path.join(ROOT, "docs", "mechanics", "concepts", "selected.json")
OUTDIR = os.path.join(ROOT, "src", "game", "data", "species")
os.makedirs(OUTDIR, exist_ok=True)
MOVES = json.load(open(os.path.join(ROOT, "src", "game", "data", "moves.json")))
MOVE_IDS = {m["id"] for m in MOVES["moves"]}
ABIL_IDS = {a["id"] for a in MOVES["abilities"]}

# damaging moves grouped by type+category, sorted by power
DMG = defaultdict(lambda: {"physical": [], "special": []})
STATUS = defaultdict(list)
for m in MOVES["moves"]:
    if m["category"] == "status" or m["power"] == 0:
        STATUS[m["type"]].append(m)
    else:
        DMG[m["type"]][m["category"]].append(m)
for t in DMG:
    DMG[t]["physical"].sort(key=lambda m: m["power"])
    DMG[t]["special"].sort(key=lambda m: m["power"])

ROLE_TPL = {
    "physical sweeper": dict(hp=70, atk=115, def_=65, spa=50, spd=65, spe=135),
    "special sweeper":  dict(hp=70, atk=50, def_=60, spa=125, spd=70, spe=125),
    "glass cannon":     dict(hp=55, atk=130, def_=50, spa=60, spd=55, spe=150),
    "physical wall":    dict(hp=95, atk=70, def_=120, spa=45, spd=85, spe=85),
    "special wall":     dict(hp=100, atk=40, def_=85, spa=70, spd=120, spe=85),
    "physical bruiser": dict(hp=100, atk=110, def_=90, spa=50, spd=75, spe=75),
    "special tank":     dict(hp=100, atk=45, def_=70, spa=110, spd=90, spe=85),
    "balanced / pivot": dict(hp=85, atk=85, def_=85, spa=85, spd=85, spe=75),
    "utility / speedster": dict(hp=75, atk=75, def_=75, spa=75, spd=75, spe=125),
    "disruptor / status": dict(hp=80, atk=70, def_=90, spa=70, spd=90, spe=100),
}
def norm_role(r):
    r = re.sub(r"\s*/\s*", " / ", (r or "").strip().lower())
    if r in ROLE_TPL: return r
    if "sweeper" in r and "special" in r: return "special sweeper"
    if "sweeper" in r: return "physical sweeper"
    if "glass" in r: return "glass cannon"
    if "special wall" in r: return "special wall"
    if "wall" in r: return "physical wall"
    if "special tank" in r or "special tank" in r: return "special tank"
    if "bruiser" in r or "tank" in r: return "physical bruiser"
    if "speed" in r or "utility" in r: return "utility / speedster"
    if "disrupt" in r or "status" in r: return "disruptor / status"
    return "balanced / pivot"

TIER_BST = {"A": 312, "B": 350, "C": 418, "D": 498, "E": 558, "F": 642}
TIER_BAND = {"A": (280,340), "B": (320,375), "C": (390,445), "D": (470,525), "E": (535,580), "F": (590,680)}
TIER_CATCH = {"A": 210, "B": 175, "C": 120, "D": 65, "E": 32, "F": 6}
PHYS_ROLES = {"physical sweeper","glass cannon","physical wall","physical bruiser"}

def seed(name): return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)

def make_stats(role, target_bst, name):
    tpl = ROLE_TPL[role]
    raw = {"hp":tpl["hp"],"atk":tpl["atk"],"def":tpl["def_"],"spa":tpl["spa"],"spd":tpl["spd"],"spe":tpl["spe"]}
    f = target_bst / 500.0
    st = {k: max(1, round(v*f)) for k, v in raw.items()}
    # fix rounding so sum == target
    diff = target_bst - sum(st.values())
    order = sorted(st, key=lambda k: -st[k])
    i = 0
    while diff != 0:
        k = order[i % len(order)]
        step = 1 if diff > 0 else -1
        if st[k] + step >= 1:
            st[k] += step; diff -= step
        i += 1
    # gentle deterministic jitter that preserves the sum (swap a few points hi<->lo)
    rnd = seed(name)
    hi = max(st, key=lambda k: st[k]); lo = min(st, key=lambda k: st[k])
    j = rnd % 7  # 0..6
    if st[lo] - j >= 1:
        st[hi] += j; st[lo] -= j
    return st

def pick_ability(types, role, tier):
    t0 = types[0]
    base = {
        "Ember": "emberheart", "Tide": "tidecaller", "Verdant": "verdant_vigor",
        "Stone": "stonehide", "Storm": "static_skin", "Frost": "coldblood",
        "Solar": "sunsoak", "Lunar": "nightsight", "Light": "mirrorlight", "Dark": "nullheart",
    }
    strong = {
        "Ember": "daybringer", "Solar": "daybringer", "Lunar": "nightfall",
        "Frost": "aurora_guard", "Storm": "stormcall", "Light": "lumenward", "Dark": "nullheart",
    }
    if tier in ("E", "F"):
        return strong.get(t0, "phoenix"), base.get(t0, "keen")
    if role in PHYS_ROLES and t0 == "Stone":
        return "grounded", "stonehide"
    if "wall" in role or "tank" in role:
        return base.get(t0, "cozy"), "thickcoat"
    return base.get(t0, "keen"), ("brisk" if "spe" in role or "sweep" in role else "forager")

def band(t, chan, power):
    """The type's damaging move nearest (<=) the requested power band, non-signature."""
    pool = [m for m in DMG[t][chan] if not m.get("signature")]
    best = None
    for m in pool:
        if m["power"] <= power:
            best = m
    return best or (pool[0] if pool else None)

def learnset(types, role, tier):
    # Band-aware (wave 2, 2026-06): both channels now run a full ladder
    # (phys 40/58/78/92, spec 58/78/92/115), so learnsets climb it explicitly
    # instead of indexing the pool — richer mid-game kits, no nuke-at-31.
    phys = role in PHYS_ROLES or (role == "balanced / pivot")
    chan = "physical" if phys else "special"
    t0 = types[0]; t1 = types[1] if len(types) > 1 else None
    lv = []
    # L1: a plain quick + the primary opener (quick 40 phys / light 58 spec)
    lv.append((1, "quick_jab"))
    opener = band(t0, chan, 40 if phys else 58)
    if opener: lv.append((1, opener["id"]))
    # status flavour move of the type
    if STATUS.get(t0):
        lv.append((9, STATUS[t0][0]["id"]))
    # the mid step (light 58 phys / standard 78 spec)
    mid = band(t0, chan, 58 if phys else 78)
    if mid: lv.append((13, mid["id"]))
    # coverage from secondary type (its light step)
    if t1:
        cov = band(t1, chan, 58)
        if cov: lv.append((19, cov["id"]))
    # the workhorse standard (phys catches up to 78 here)
    std = band(t0, chan, 78)
    if std: lv.append((22, std["id"]))
    # a self-buff utility
    lv.append((24, "hone" if phys else "focus_mind"))
    # heavy primary (mid/final tiers)
    if tier in ("C","D","E","F"):
        heavy = band(t0, chan, 92)
        if heavy: lv.append((31, heavy["id"]))
    # nuke primary (final/apex/legend; the special channel carries the nukes)
    if tier in ("D","E","F"):
        nuke = band(t0, "special", 115)
        if nuke: lv.append((40, nuke["id"]))
    # apex breadth: strongest off-channel STAB
    if tier in ("E","F"):
        alt = band(t0, "physical" if not phys else "special", 999)
        if alt: lv.append((48, alt["id"]))
    # dedupe + validate, keep order by level
    seen = set(); out = []
    for level, mid_ in sorted(lv, key=lambda x: x[0]):
        if mid_ in MOVE_IDS and mid_ not in seen:
            seen.add(mid_); out.append({"level": level, "move": mid_})
    return out

REGION_AREA = {
    "south": ("dimglass_coast", (3, 12)),
    "east": ("lowleaf_hollow", (12, 24)),
    "north": ("galehigh_terraces", (26, 40)),
    "west": ("sunken_solarium", (38, 50)),
    "outer": ("coldfog_marches", (46, 54)),
    "central": ("umbral_spire", (55, 62)),
    "post": ("dawnstead", (50, 70)),
}
TERRAIN = {"south":"tall_grass","east":"cave","north":"tall_grass","west":"water","outer":"tall_grass","central":"cave","post":"tall_grass"}

def encounters(region, rarity, tier, stage, scripted):
    area, (blo, bhi) = REGION_AREA.get(region, ("dimglass_coast", (3, 12)))
    # higher tier / later stage -> higher level within the band
    bump = {"A":0,"B":3,"C":7,"D":12,"E":16,"F":20}[tier]
    lo = min(bhi-2, blo + bump + (stage-1)*3)
    hi = min(bhi, lo + 3)
    if scripted:
        return []  # legendaries/very-rare apexes are scripted/landmark, not in open tables
    return [{"area": area, "terrain": TERRAIN.get(region, "tall_grass"), "rarity": rarity, "min": lo, "max": hi}]

# Hand-curated encounter placements layered on top of the generated defaults —
# map work (e.g. Pearlmoor's harbour tables) adds entries HERE so a rebuild
# never erases them. slug -> extra EncounterZone-source rows.
EXTRA_ENCOUNTERS = {
    "brinix":    [{"area": "pearlmoor_quay", "terrain": "water", "rarity": "uncommon", "min": 10, "max": 12},
                  # South coast surf (R5 S/E encounters-sync, 2026-06): mirrors of
                  # the BUILT dimglass_coast/_ii in-map tables (the truth; weights
                  # -> rarity). These two maps were the south REGION_AREA default,
                  # so they carried ~37 stale generated rows — now curated.
                  {"area": "dimglass_coast", "terrain": "water", "rarity": "common", "min": 4, "max": 6},
                  {"area": "dimglass_coast_ii", "terrain": "water", "rarity": "common", "min": 9, "max": 11}],
    # Tideglass Cavern rows below (the Hours wiring, 2026-06): mirrors of the
    # BUILT in-map zone tables (tideglass_cavern.json — the truth; weights ->
    # rarity). The cave bed is the South's lv 20-24 backtrack; the Tidecall
    # side-pool carries the atlas-promised signature rare (#30 Glostrael w5).
    # tideglass_gallery has NO encounter zones by design (the Hour's room).
    "shimmral":  [{"area": "pearlmoor_quay", "terrain": "water", "rarity": "rare", "min": 11, "max": 12},
                  # the drowned shrine's rare circler (the Saltreach spur)
                  {"area": "sunkbell_shallows", "terrain": "water", "rarity": "rare", "min": 18, "max": 20},
                  {"area": "tideglass_cavern", "terrain": "cave", "rarity": "uncommon", "min": 21, "max": 24},
                  {"area": "tideglass_cavern", "terrain": "water", "rarity": "common", "min": 21, "max": 24}],
    "brinelet":  [{"area": "pearlmoor_quay", "terrain": "tall_grass", "rarity": "common", "min": 8, "max": 11},
                  {"area": "tideglass_cavern", "terrain": "cave", "rarity": "common", "min": 20, "max": 22},
                  {"area": "dimglass_coast", "terrain": "tall_grass", "rarity": "common", "min": 3, "max": 6},
                  {"area": "dimglass_coast_ii", "terrain": "tall_grass", "rarity": "common", "min": 8, "max": 11}],
    "brineroll": [{"area": "pearlmoor_quay", "terrain": "water", "rarity": "uncommon", "min": 10, "max": 12},
                  {"area": "saltreach_fen_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 16, "max": 18},
                  {"area": "saltreach_fen_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 17, "max": 19},
                  {"area": "sunkbell_shallows", "terrain": "water", "rarity": "common", "min": 17, "max": 19},
                  {"area": "tideglass_cavern", "terrain": "cave", "rarity": "uncommon", "min": 21, "max": 24},
                  {"area": "tideglass_cavern", "terrain": "water", "rarity": "common", "min": 21, "max": 24},
                  {"area": "dimglass_coast_ii", "terrain": "tall_grass", "rarity": "common", "min": 9, "max": 11}],
    "lumpin":    [{"area": "pearlmoor_quay", "terrain": "tall_grass", "rarity": "common", "min": 9, "max": 11},
                  {"area": "saltreach_fen_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 16, "max": 18},
                  {"area": "saltreach_fen_ii", "terrain": "water", "rarity": "uncommon", "min": 17, "max": 19},
                  {"area": "tideglass_cavern", "terrain": "cave", "rarity": "uncommon", "min": 20, "max": 23},
                  {"area": "dimglass_coast", "terrain": "tall_grass", "rarity": "common", "min": 3, "max": 6},
                  {"area": "dimglass_coast_ii", "terrain": "tall_grass", "rarity": "common", "min": 8, "max": 11}],
    # the Glostern line's middle form is the cavern pool's signature rare —
    # it seeds Pharolux's living-lighthouse legend two doors from where the
    # players caught Glostern (07-the-three §4).
    "glostern":  [{"area": "tideglass_cavern", "terrain": "water", "rarity": "uncommon", "min": 22, "max": 24}],
    "glostrael": [{"area": "tideglass_cavern", "terrain": "water", "rarity": "very_rare", "min": 22, "max": 24}],
    # the Saltreach marsh chain (fen I/II + the Sunkbell spur) — the maps'
    # authored tables, mirrored here as the dex's flavour rows
    "dewling":   [{"area": "saltreach_fen_i", "terrain": "tall_grass", "rarity": "common", "min": 16, "max": 18},
                  {"area": "saltreach_fen_ii", "terrain": "tall_grass", "rarity": "common", "min": 17, "max": 19}],
    "poolfrond": [{"area": "saltreach_fen_i", "terrain": "tall_grass", "rarity": "rare", "min": 17, "max": 18},
                  {"area": "saltreach_fen_ii", "terrain": "tall_grass", "rarity": "rare", "min": 18, "max": 19}],
    "tidalarch": [{"area": "sunkbell_shallows", "terrain": "water", "rarity": "very_rare", "min": 19, "max": 20}],
    # the dimglass coast verge's uncommon flit (R5 S/E sync) — its one South row
    "glimflit":  [{"area": "dimglass_coast", "terrain": "tall_grass", "rarity": "uncommon", "min": 3, "max": 6}],
    # ---- the East fringe (R5 S/E encounters-sync, 2026-06): mirror of the BUILT
    # lowleaf_hollow in-map table (the truth). lowleaf_hollow was the east
    # REGION_AREA default, so it carried ~34 stale generated rows — now curated.
    "mossglow":  [{"area": "lowleaf_hollow", "terrain": "tall_grass", "rarity": "common", "min": 18, "max": 20}],
    "sporeling": [{"area": "lowleaf_hollow", "terrain": "tall_grass", "rarity": "common", "min": 18, "max": 20}],
    "barkhelm":  [{"area": "lowleaf_hollow", "terrain": "tall_grass", "rarity": "uncommon", "min": 18, "max": 20}],
    "fennlight": [{"area": "lowleaf_hollow", "terrain": "tall_grass", "rarity": "common", "min": 18, "max": 20}],
    # ---- the North (N5 encounters-sync, 2026-06): mirrors of the BUILT in-map
    # zone tables (public/assets/maps/*.json — the truth; weights -> rarity).
    # The deep-ice fold + undercroft rows are the Emberward/Lamp-Line ground.
    "sparrowcaw":  [{"area": "galehigh_terraces", "terrain": "tall_grass", "rarity": "common", "min": 28, "max": 30}],
    "thrumvane":   [{"area": "galehigh_terraces", "terrain": "tall_grass", "rarity": "common", "min": 28, "max": 30}],
    "cirruff":     [{"area": "galehigh_terraces", "terrain": "tall_grass", "rarity": "uncommon", "min": 28, "max": 30}],
    "squallox":    [{"area": "galehigh_terraces", "terrain": "tall_grass", "rarity": "uncommon", "min": 28, "max": 30}],
    # Windward I min 32: the SE foot verge rolls its own gentler 32-34 band
    # (N6 MIN-3 — the three common Storm lines only); upper ledges stay 34-36.
    "flintbeak":   [{"area": "windward_stair_i", "terrain": "tall_grass", "rarity": "common", "min": 32, "max": 36},
                    {"area": "windward_stair_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 34, "max": 36},
                    {"area": "thunderroost", "terrain": "tall_grass", "rarity": "common", "min": 34, "max": 36}],
    "sparkrat":    [{"area": "windward_stair_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 32, "max": 36},
                    {"area": "windward_stair_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 34, "max": 36}],
    "thrumble":    [{"area": "windward_stair_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 32, "max": 35},
                    {"area": "windward_stair_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 35, "max": 36}],
    "chillpip":    [{"area": "windward_stair_i", "terrain": "tall_grass", "rarity": "rare", "min": 34, "max": 35}],
    "geolace":     [{"area": "windward_stair_ii", "terrain": "tall_grass", "rarity": "rare", "min": 34, "max": 36}],
    "glacewing":   [{"area": "windward_stair_i", "terrain": "tall_grass", "rarity": "rare", "min": 35, "max": 36},
                    {"area": "windward_stair_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 35, "max": 36},
                    {"area": "wind_eye", "terrain": "tall_grass", "rarity": "common", "min": 35, "max": 36},
                    {"area": "thunderroost", "terrain": "tall_grass", "rarity": "common", "min": 35, "max": 36},
                    {"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "rare", "min": 37, "max": 40},
                    {"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "rare", "min": 40, "max": 41}],
    "hailwhirr":   [{"area": "wind_eye", "terrain": "tall_grass", "rarity": "common", "min": 34, "max": 36}],
    "cumulance":   [{"area": "wind_eye", "terrain": "tall_grass", "rarity": "rare", "min": 36, "max": 36}],
    "strikeaven":  [{"area": "thunderroost", "terrain": "tall_grass", "rarity": "rare", "min": 36, "max": 37}],
    "glaceling":   [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "uncommon", "min": 36, "max": 39},
                    {"area": "pale_vault_glacier", "terrain": "cave", "rarity": "rare", "min": 38, "max": 40},
                    {"area": "pale_vault_undercroft", "terrain": "cave", "rarity": "uncommon", "min": 37, "max": 40},
                    # the Hourfold (Hours wiring 2026-06): mirror of the BUILT
                    # in-map bed (pale_vault_hourfold.json — sparse cave 44-48,
                    # a band above the North curve by design)
                    {"area": "pale_vault_hourfold", "terrain": "cave", "rarity": "uncommon", "min": 44, "max": 46}],
    "iceling":     [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "uncommon", "min": 36, "max": 38}],
    "snowcune":    [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "uncommon", "min": 36, "max": 38}],
    "prismcub":    [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "uncommon", "min": 36, "max": 38},
                    {"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 40, "max": 41},
                    {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 40, "max": 42},
                    {"area": "aurora_hollow", "terrain": "tall_grass", "rarity": "common", "min": 40, "max": 42}],
    "prismantus":  [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "very_rare", "min": 38, "max": 40},
                    {"area": "pale_vault_glacier", "terrain": "cave", "rarity": "rare", "min": 38, "max": 40},
                    {"area": "aurora_hollow", "terrain": "tall_grass", "rarity": "uncommon", "min": 41, "max": 42},
                    {"area": "pale_vault_hourfold", "terrain": "cave", "rarity": "uncommon", "min": 44, "max": 47}],
    "stillwarden": [{"area": "pale_vault_glacier", "terrain": "cave", "rarity": "rare", "min": 38, "max": 40},
                    {"area": "pale_vault_undercroft", "terrain": "cave", "rarity": "rare", "min": 38, "max": 40},
                    # hushfrost II: main bed w12 + the "numbed" pockets where it runs w45
                    {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 41, "max": 42},
                    {"area": "pale_vault_hourfold", "terrain": "cave", "rarity": "common", "min": 44, "max": 48}],
    "hushbore":    [{"area": "pale_vault_undercroft", "terrain": "cave", "rarity": "common", "min": 37, "max": 40},
                    {"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "common", "min": 40, "max": 42},
                    {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "common", "min": 40, "max": 42},
                    {"area": "aurora_hollow", "terrain": "tall_grass", "rarity": "uncommon", "min": 40, "max": 42}],
    "hushvole":    [{"area": "pale_vault_undercroft", "terrain": "cave", "rarity": "uncommon", "min": 37, "max": 39}],
    "blizzrhare":  [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "uncommon", "min": 36, "max": 39},
                    {"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 40, "max": 41},
                    {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 40, "max": 42}],
    # ---- the West (W6 encounters-sync, 2026-06): mirrors of the BUILT in-map
    # zone tables (public/assets/maps/*.json — the truth). Rarity from weight
    # share (tables total ~100): >=20 common, 10-19 uncommon, 5-9 rare, <=4
    # very_rare; apex teasers cap at very_rare, pocket-only species at rare;
    # per-species levels/weights merged across a map's same-terrain zones.
    # Frost-line rows for the hushfrost/aurora leg ride the North keys above.
    "crystarn":    [{"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "common", "min": 40, "max": 42},
                    {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "common", "min": 41, "max": 42},
                    {"area": "aurora_hollow", "terrain": "tall_grass", "rarity": "common", "min": 40, "max": 42}],
    "geodrake":    [{"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 40, "max": 41}],
    "vortexlope":  [{"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "rare", "min": 41, "max": 42}],
    "frigalance":  [{"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "rare", "min": 41, "max": 42}],
    "glacitern":   [{"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "rare", "min": 41, "max": 42}],
    # the aurora bed's w6 lv42 Frost-Light apex teaser (scripted kin; this is
    # its one wild window)
    "frostholm":   [{"area": "aurora_hollow", "terrain": "tall_grass", "rarity": "very_rare", "min": 42, "max": 42}],
    # Sunken Solarium — the BUILT split wins: dry-outer 42-44 (crossings) +
    # dry-inner 43-46 (garden beds) merge per species; water halls 43-46 are
    # Tidecall-gated zones (gate lives in the map, not mirrored here).
    "snoozlet":    [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "uncommon", "min": 42, "max": 44},
                    {"area": "nightreach_observatory", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 50}],
    "spirlet":     [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "uncommon", "min": 42, "max": 44},
                    {"area": "nightreach_observatory", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 50}],
    "sunsprout":   [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "uncommon", "min": 42, "max": 45},
                    {"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 47}],
    "gilpaw":      [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "uncommon", "min": 42, "max": 44},
                    {"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 47}],
    "helibud":     [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "uncommon", "min": 42, "max": 46},
                    {"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 47},
                    {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 48},
                    {"area": "helia_vault", "terrain": "tall_grass", "rarity": "common", "min": 47, "max": 48}],
    "dawnfawn":    [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "uncommon", "min": 43, "max": 46},
                    {"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 47},
                    {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 48}],
    "petalune":    [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "uncommon", "min": 43, "max": 46},
                    {"area": "nightreach_observatory", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 50}],
    "lunveil":     [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "uncommon", "min": 43, "max": 46},
                    {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 48},
                    {"area": "nightreach_observatory", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 51}],
    "solvyne":     [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "rare", "min": 44, "max": 46},
                    {"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 48},
                    {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 48},
                    {"area": "helia_vault", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 49},
                    {"area": "helia_vault", "terrain": "cave", "rarity": "common", "min": 48, "max": 49}],
    "helicore":    [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "rare", "min": 44, "max": 46},
                    {"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 48},
                    {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 48},
                    {"area": "helia_vault", "terrain": "tall_grass", "rarity": "common", "min": 47, "max": 49},
                    {"area": "helia_vault", "terrain": "cave", "rarity": "common", "min": 48, "max": 50}],
    "goldmane":    [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "rare", "min": 45, "max": 46},
                    {"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "rare", "min": 47, "max": 48},
                    {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 48},
                    {"area": "helia_vault", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49},
                    {"area": "helia_vault", "terrain": "cave", "rarity": "common", "min": 48, "max": 50}],
    "crystalune":  [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "rare", "min": 44, "max": 46}],
    "drowshorn":   [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "very_rare", "min": 44, "max": 46},
                    {"area": "nightreach_observatory", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 51}],
    "auravane":    [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "very_rare", "min": 45, "max": 46},
                    {"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "rare", "min": 47, "max": 48},
                    {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "rare", "min": 47, "max": 48},
                    {"area": "helia_vault", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49}],
    "sunstag":     [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "very_rare", "min": 44, "max": 46},
                    {"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "very_rare", "min": 47, "max": 48},
                    {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "rare", "min": 47, "max": 48},
                    {"area": "helia_vault", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49}],
    "lunvane":     [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "very_rare", "min": 45, "max": 46},
                    {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "very_rare", "min": 48, "max": 48},
                    {"area": "nightreach_observatory", "terrain": "tall_grass", "rarity": "rare", "min": 50, "max": 52}],
    "solunet":     [{"area": "sunken_solarium", "terrain": "water", "rarity": "common", "min": 43, "max": 45}],
    "solray":      [{"area": "sunken_solarium", "terrain": "water", "rarity": "common", "min": 43, "max": 46}],
    "tidalune":    [{"area": "sunken_solarium", "terrain": "water", "rarity": "uncommon", "min": 44, "max": 46}],
    "nightwraith": [{"area": "sunken_solarium", "terrain": "water", "rarity": "uncommon", "min": 44, "max": 46},
                    {"area": "nightreach_observatory", "terrain": "tall_grass", "rarity": "uncommon", "min": 49, "max": 51}],
    "lunaquell":   [{"area": "sunken_solarium", "terrain": "water", "rarity": "rare", "min": 45, "max": 46}],
    "omenire":     [{"area": "sunken_solarium", "terrain": "water", "rarity": "rare", "min": 45, "max": 46}],
    "lunarbel":    [{"area": "sunken_solarium", "terrain": "water", "rarity": "rare", "min": 45, "max": 46}],
    "solreach":    [{"area": "sunken_solarium", "terrain": "water", "rarity": "rare", "min": 45, "max": 46}],
    # the reliquary bed (helia_vault cave zone) is gated flag:helia_far_bloomed
    # in the map JSON — the Solar apex's one wild window (scripted kin); apex
    # caps at rare despite the w12 share
    "heliovast":   [{"area": "helia_vault", "terrain": "cave", "rarity": "rare", "min": 49, "max": 50}],
    # nightreach verge w3 Lunar-Light apex teaser (scripted kin)
    "dawnwatcher": [{"area": "nightreach_observatory", "terrain": "tall_grass", "rarity": "very_rare", "min": 51, "max": 52}],
    # Coldfog — the maps split the designed coldfog_marches rows into I/II
    "mothdim":     [{"area": "coldfog_marches_i", "terrain": "tall_grass", "rarity": "common", "min": 46, "max": 48}],
    "flutterwane": [{"area": "coldfog_marches_i", "terrain": "tall_grass", "rarity": "common", "min": 46, "max": 48}],
    "nullmoth":    [{"area": "coldfog_marches_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 48},
                    {"area": "coldfog_marches_ii", "terrain": "tall_grass", "rarity": "common", "min": 48, "max": 50},
                    {"area": "drownlight_beacon", "terrain": "tall_grass", "rarity": "common", "min": 48, "max": 49},
                    {"area": "hollowfen_stillworks", "terrain": "tall_grass", "rarity": "common", "min": 48, "max": 50}],
    "wispwane":    [{"area": "coldfog_marches_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 48},
                    {"area": "coldfog_marches_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 49, "max": 50},
                    {"area": "drownlight_beacon", "terrain": "tall_grass", "rarity": "common", "min": 48, "max": 50}],
    "cindersob":   [# hushfrost II's "numbed" pockets only (w30 there) — rare cap
                    {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "rare", "min": 40, "max": 42},
                    {"area": "coldfog_marches_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 48},
                    {"area": "coldfog_marches_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 50}],
    # the gold bed (coldfog I's 1-tile gold_a pocket, w5) — the lone Light
    # exception in the Dark marches
    "wisprestored": [{"area": "coldfog_marches_i", "terrain": "tall_grass", "rarity": "rare", "min": 47, "max": 48}],
    "wispwanenull": [{"area": "coldfog_marches_ii", "terrain": "tall_grass", "rarity": "common", "min": 48, "max": 50},
                     {"area": "hollowfen_stillworks", "terrain": "tall_grass", "rarity": "common", "min": 48, "max": 50}],
    "embergone":   [{"area": "coldfog_marches_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 49, "max": 50},
                    {"area": "hollowfen_stillworks", "terrain": "tall_grass", "rarity": "common", "min": 49, "max": 50}],
    "voidmantle":  [{"area": "coldfog_marches_ii", "terrain": "tall_grass", "rarity": "rare", "min": 49, "max": 50},
                    {"area": "drownlight_beacon", "terrain": "tall_grass", "rarity": "common", "min": 49, "max": 50}],
    "liminalux":   [{"area": "drownlight_beacon", "terrain": "tall_grass", "rarity": "rare", "min": 49, "max": 50}],
    # the husk-cradle (w55 pocket) + the works bed (w12)
    "whorlix":     [{"area": "hollowfen_stillworks", "terrain": "tall_grass", "rarity": "uncommon", "min": 50, "max": 51}],
}

# ---------------------------------------------------------------------------
# The Starfall Vigils (06-postgame · R3, 2026-06) — the five annex beds + the
# Dawnstead post-dawn DAY-FORM table + Helixia's post-crown verge entry. Kept in
# a separate dict and MERGED into EXTRA_ENCOUNTERS below (many of these species
# already carry rows there, and a duplicate literal key would silently clobber
# them). Tables are VERBATIM from each site's Hooks block (the map-build lane
# bakes the same spec tables — the spec is the shared truth). Each annex's apex
# Vigilant doubles as the bed's very-rare catch (the register ledger).
VIGIL_ENCOUNTERS = {
    # Vigil I — Hearthfall (`vigil_hearthfall`, off tinderwick) — Ember & Tide, 58–60.
    "scorchwing":  [{"area": "vigil_hearthfall", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 60}],
    "chandrek":    [{"area": "vigil_hearthfall", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 60},
                    {"area": "dawnstead", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 62}],
    "wicklord":    [{"area": "vigil_hearthfall", "terrain": "tall_grass", "rarity": "rare", "min": 59, "max": 60},
                    {"area": "dawnstead", "terrain": "tall_grass", "rarity": "rare", "min": 60, "max": 65}],
    "embralux":    [{"area": "vigil_hearthfall", "terrain": "tall_grass", "rarity": "very_rare", "min": 60, "max": 60}],
    "prismare":    [{"area": "vigil_hearthfall", "terrain": "water", "rarity": "uncommon", "min": 58, "max": 60}],
    "tideveil":    [{"area": "vigil_hearthfall", "terrain": "water", "rarity": "very_rare", "min": 60, "max": 60}],
    # Vigil II — Grovefall (`vigil_grovefall`, off spore_grotto, kind cave/glowmoss) — Verdant & Stone, 60–62.
    "fernlance":   [{"area": "vigil_grovefall", "terrain": "tall_grass", "rarity": "uncommon", "min": 60, "max": 62}],
    "rootwarden":  [{"area": "vigil_grovefall", "terrain": "tall_grass", "rarity": "uncommon", "min": 60, "max": 62}],
    "gravelo":     [{"area": "vigil_grovefall", "terrain": "tall_grass", "rarity": "uncommon", "min": 60, "max": 62}],
    "mycelarch":   [{"area": "vigil_grovefall", "terrain": "tall_grass", "rarity": "rare", "min": 61, "max": 62}],
    "mycovast":    [{"area": "vigil_grovefall", "terrain": "tall_grass", "rarity": "very_rare", "min": 62, "max": 62}],
    # Vigil III — Stormfall (`vigil_stormfall`, off thunderroost) — Storm & Frost, 62–64.
    "tempestail":  [{"area": "vigil_stormfall", "terrain": "tall_grass", "rarity": "uncommon", "min": 62, "max": 64}],
    "vortavane":   [{"area": "vigil_stormfall", "terrain": "tall_grass", "rarity": "uncommon", "min": 62, "max": 64}],
    "glacitern":   [{"area": "vigil_stormfall", "terrain": "tall_grass", "rarity": "uncommon", "min": 62, "max": 64}],
    "strikeaven":  [{"area": "vigil_stormfall", "terrain": "tall_grass", "rarity": "rare", "min": 63, "max": 64}],
    "nullhusk":    [{"area": "vigil_stormfall", "terrain": "tall_grass", "rarity": "very_rare", "min": 64, "max": 64}],
    # Vigil IV — Sunfall (`vigil_sunfall`, off sunvault_climb_ii) — Solar & Lunar, 64–66.
    "sunstag":     [{"area": "vigil_sunfall", "terrain": "tall_grass", "rarity": "uncommon", "min": 64, "max": 66}],
    "solreach":    [{"area": "vigil_sunfall", "terrain": "tall_grass", "rarity": "uncommon", "min": 64, "max": 66}],
    "crystalune":  [{"area": "vigil_sunfall", "terrain": "tall_grass", "rarity": "uncommon", "min": 64, "max": 66}],
    "lunaquell":   [{"area": "vigil_sunfall", "terrain": "tall_grass", "rarity": "rare", "min": 64, "max": 66}],
    "dawnwatcher": [{"area": "vigil_sunfall", "terrain": "tall_grass", "rarity": "very_rare", "min": 65, "max": 65}],
    "helithorn":   [{"area": "vigil_sunfall", "terrain": "tall_grass", "rarity": "very_rare", "min": 66, "max": 66}],
    # Vigil V — Murkfall (`vigil_murkfall`, off coldfog_marches_ii) — Light & Dark, 66–68.
    "embergone":   [{"area": "vigil_murkfall", "terrain": "tall_grass", "rarity": "uncommon", "min": 66, "max": 68}],
    "voidmantle":  [{"area": "vigil_murkfall", "terrain": "tall_grass", "rarity": "uncommon", "min": 66, "max": 68}],
    "wisprestored":[{"area": "vigil_murkfall", "terrain": "tall_grass", "rarity": "uncommon", "min": 66, "max": 68}],
    "solarmourn":  [{"area": "vigil_murkfall", "terrain": "tall_grass", "rarity": "very_rare", "min": 67, "max": 67}],
    "cindervast":  [{"area": "vigil_murkfall", "terrain": "tall_grass", "rarity": "very_rare", "min": 67, "max": 67}],
    "bogvast":     [{"area": "vigil_murkfall", "terrain": "tall_grass", "rarity": "very_rare", "min": 68, "max": 68}],
    # Dawnstead — the post-dawn DAY-FORM table (built in dawnstead.json; weights
    # -> rarity: w30 common, w20 common, w15 uncommon, w12 uncommon, w8 rare).
    "wickmoth":    [{"area": "dawnstead", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 60}],
    "tallowpup":   [{"area": "dawnstead", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 58}],
    "hearthkit":   [{"area": "dawnstead", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 60}],
    "glimscout":   [{"area": "dawnstead", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 60}],
    # Helixia — the day-form table's CAPSTONE: a very-rare verge entry that only
    # rolls post-crown (`requires flag:starfall_crown` in the live zone; the dex
    # row is flat — the register ledger's final placement).
    "helixia":     [{"area": "dawnstead", "terrain": "tall_grass", "rarity": "very_rare", "min": 60, "max": 62}],
}
# Merge VIGIL rows into EXTRA_ENCOUNTERS (append where a slug already has rows).
for _slug, _rows in VIGIL_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows)

# Areas whose encounter tables are BUILT into the map JSONs (the in-map zones
# are the truth, mirrored above). Generated region defaults — and stale rows
# carried in the previous per-species files — must not claim these areas:
# only EXTRA_ENCOUNTERS rows may. (North is the first fully-built region; its
# default "galehigh_terraces" band rows predated the maps.)
CURATED_AREAS = {
    "galehigh_terraces", "windward_stair_i", "windward_stair_ii", "wind_eye",
    "thunderroost", "pale_vault_glacier", "pale_vault_undercroft",
    # the West (W6): the 12 built encounter-bearing maps. "coldfog_marches"
    # (no suffix) is the pre-build design area — the maps split it into I/II,
    # so the unsuffixed design rows are dropped, never resurrected.
    "hushfrost_pass_i", "hushfrost_pass_ii", "aurora_hollow",
    "sunken_solarium", "sunvault_climb_i", "sunvault_climb_ii", "helia_vault",
    "coldfog_marches", "coldfog_marches_i", "coldfog_marches_ii",
    "drownlight_beacon", "hollowfen_stillworks", "nightreach_observatory",
    # the Three Hours sites (Hours wiring 2026-06): the cavern + the fold carry
    # built in-map tables (mirrored above); the gallery is encounter-free by
    # design and listed so no generated row can ever claim the Hour's room.
    "tideglass_cavern", "tideglass_gallery", "pale_vault_hourfold",
    # the South/East REGION_AREA defaults (R5 S/E encounters-sync, 2026-06): these
    # two maps' built in-map tables are the truth (mirrored above), so the ~71
    # stale generated rows that named them (dimglass_coast ~37 + lowleaf_hollow
    # ~34) are dropped on rebuild; the _ii coast map joins them.
    "dimglass_coast", "dimglass_coast_ii", "lowleaf_hollow",
    # the Starfall Vigils (06-postgame · R3, 2026-06): the five annex sites carry
    # built in-map tables (mirrored below); Dawnstead carries the post-dawn
    # DAY-FORM table (built in dawnstead.json) + the Helixia post-crown verge
    # entry, both mirrored below. The map-build lane bakes the same spec tables.
    "vigil_hearthfall", "vigil_grovefall", "vigil_stormfall",
    "vigil_sunfall", "vigil_murkfall", "dawnstead",
}

# Kin that are FIXED quest catches (a legendaryBattle set-piece), even though
# tier/rarity alone wouldn't mark them scripted. #148 Lampling is C1
# "Lampling's Trail" at the Vesper Crossroads — its old umbral_spire row was a
# stale open-table teaser from before the trail was built, dropped here.
SCRIPTED_KIN = {"lampling"}

# Wave-2 signature moves (gen_moves.py): one per elemental apex line. Inserted
# into the owner's learnset late (the awe-curve payoff); excluded from the
# generic pools by autobuild.mjs/chart_check.mjs so they shape ONLY their owner.
SIGNATURE_MOVES = {
    "embralux":    ("last_ember", 48),
    "tideveil":    ("veiltide", 44),
    "mycovast":    ("spore_cathedral", 44),
    "prismara":    ("prism_lance", 48),
    "nullhusk":    ("static_hollow", 44),
    "frostholm":   ("hoarfrost_crown", 44),
    "solarmourn":  ("mourninglight", 46),
    "lunaveil":    ("dreamlace", 46),
    "keylumen":    ("keystar_beam", 52),
    "nullmajor":   ("hollowing_hymn", 52),
    "dawnbrael":   ("daybreak_lance", 52),
}

def parse_trigger(text, stage, tier):
    text = (text or "").lower()
    m = re.search(r"(\d{1,2})", text)
    lvl = int(m.group(1)) if m else (16 if stage == 1 else 34)
    if tier in ("D","E"): lvl = max(lvl, 30 if stage==1 else 46)
    if "stone" in text or "kindlestone" in text:
        kt = next((k for k in ["ember","tide","verdant","stone","storm","frost","solar","lunar"] if k in text), "ember")
        return {"kind": "stone", "item": f"{kt}_kindlestone"}
    if "bond" in text or "friend" in text:
        return {"kind": "bond", "min": 160}
    if "night" in text: return {"kind": "time", "level": lvl, "when": "night"}
    if "day" in text or "sun" in text: return {"kind": "time", "level": lvl, "when": "day"}
    if "location" in text or "vault" in text or "well" in text or "cavern" in text:
        return {"kind": "location", "area": REGION_AREA.get("east")[0]}
    return {"kind": "level", "level": lvl}

# Canonical data for the two pre-existing starters (docs/sample-kin.md + assets/).
CANON = {
    "vulpyre": {
        "stats": {"hp": 56, "atk": 61, "def": 50, "spa": 65, "spd": 52, "spe": 72},
        "ability": "emberheart", "hidden_ability": "brisk", "signature": "tuft_spark",
        "size_cm": 60, "weight_kg": 9.4,
        "entry": "It dozes on sun-warmed stones and bolts at the first drop of rain. When a Vulpyre trusts you, its mane burns a steadier gold.",
        "category": "Hearth-Fox Kin",
    },
    "brinix": {
        "stats": {"hp": 62, "atk": 53, "def": 58, "spa": 60, "spd": 64, "spe": 55},
        "ability": "tidecaller", "hidden_ability": "mistveil", "signature": "bubble_hum",
        "size_cm": 52, "weight_kg": 11.5,
        "entry": "Its side-fins glow softly in deep water. Brinix hums a bubbling tune that settles nervous kin, and rides fast currents purely for the fun of it.",
        "category": "Tide-Hum Kin",
    },
    # Third starter (Verdant) — completes the founding trio with Vulpyre/Brinix.
    # Logo creature; full art in assets/creatures/152_cloverkit/.
    "cloverkit": {
        "stats": {"hp": 72, "atk": 78, "def": 64, "spa": 36, "spd": 53, "spe": 53},
        "ability": "verdant_vigor", "hidden_ability": "bramble", "signature": "vine_tap",
        "size_cm": 45, "weight_kg": 6.5,
        "entry": "A sprout-cub that wears a four-leaf clover like a tiny lantern-leaf; in the Long Dusk the clover gathers what light remains and glows a gentle green. A Cloverkit that trusts you is said to share its luck.",
        "category": "Clover-Cub Kin",
    },
    "cloverhart": {
        "stats": {"hp": 100, "atk": 112, "def": 95, "spa": 48, "spd": 78, "spe": 65},
        "ability": "verdant_vigor", "hidden_ability": "bramble", "signature": "root_strike",
        "size_cm": 165, "weight_kg": 98,
        "entry": "Cloverkit's kindled form: a great clover-crowned stag whose antlers bloom with year-round green even beneath the dark sky. It plants its hooves and shields the grove, taking blows that would fell lesser kin. The cub you raised became the forest's gentle guardian.",
        "category": "Grove-Guardian Kin",
    },
    # The Three Hours (#160-162) — docs/world/walkthrough/07-the-three.md §2.
    # Stats are NOT pinned: make_stats(role, 558, name) reproduces the dossier
    # lines deterministically (verified). 'levelup' pins the as-met kits from
    # the existing 125-move pool; 'art' carries the dossier's distinct
    # silhouette/palette/direction so gen_creature.py gets a real palette line.
    "gloamber": {
        # the generator's Ember-E default is daybringer, wrong for a dusk kin
        "ability": "nightfall", "hidden_ability": "emberheart",
        "entry": "The First Hour — the keeper of dusk, grown heavy with an evening it has never been allowed to put down. Lamp-tenders say every wick in Vesperholm is lit from the one coal it carries, at one remove or another.",
        "category": "Dusk Hour Kin",
        "levelup": [(1, "cinder_spit"), (9, "scorch_veil"), (13, "hearth_pulse"),
                    (24, "mend"), (31, "gloomswell"), (44, "sunflare_burst"), (52, "voidburst")],
        "art": {
            "silhouette": "A long, low lynx-like beast, heavy-lidded and patient, built close to the ground like something settling in for the night. A banked mane of small, steady flame-tongues runs low along the neck and shoulders — embers, not fire. At its chest, a locket of teal sea-glass holds one bright coal. The tail ends in a slow curl of pale smoke. Reads at 64px as a dark animal carrying one precious light.",
            "palette": "Charcoal-violet fur deepening to ink (#1a1430) along the spine like a sky losing its light; ember amber (#ff8a3d) and rose for the banked mane; diamond-teal sea-glass locket; a faint dusk-rose gradient on the brow and flanks.",
            "direction": "The moment of lamp-lighting as an animal. Heavy, warm at the core, unhurried — the dusk as a keeper, not a threat. The single chest-coal must read as the brightest pixel on the sprite.",
        },
    },
    "noctilune": {
        # the Lunar-E default nightfall is already Gloamber's curtain —
        # Midnight doesn't bring the night, it IS the night
        "ability": "mirrorlight", "hidden_ability": "nightsight",
        "entry": "The Still Hour — the keeper of midnight, standing the same unrelieved watch since the night stopped turning. The Hollowing call it proof that the dark can be gentle; Noctilune, for its part, has never once answered them.",
        "category": "Midnight Hour Kin",
        "levelup": [(1, "moon_nip"), (13, "moonshard"), (24, "lull"), (30, "bulwark"),
                    (38, "nightfall_veil"), (46, "shadow_rend"), (54, "eclipse_wave")],
        "art": {
            "silhouette": "A huge pangolin-like sentinel, its overlapping scales panes of midnight-blue glass, each pane holding exactly one star-speck. Standing, it reads as a hooded watchman; curled, as a dark moonless disc. A small unstruck bell of dark ice hangs at its throat. Eyes are two thin silver crescents. At 64px it should read like a piece of the midnight sky knelt down to wait.",
            "palette": "Night (#0b1026) and deepBlue (#13205a) scale-panes; diamond (#9fe7ff) star-specks, one per scale; pale moon-grey underbelly and claws; the throat-bell a darker, colder blue than everything around it.",
            "direction": "The deep of night as armour. Utterly still until it isn't. No menace — endurance. The unstruck bell is the motif: midnight is the hour no bell marks.",
        },
    },
    "erstmorn": {
        # abilities match the Solar-E generator defaults (daybringer/sunsoak)
        "entry": "The Lost Hour — the keeper of a dawn that has not come, waiting half-finished where the morning was meant to land. Those who meet it say the worst part is its patience: it does not doubt the sunrise, and it will not be told the years.",
        "category": "Dawn Hour Kin",
        "levelup": [(1, "sun_jab"), (13, "glint_ray"), (22, "daybeam"), (28, "dazzle_flash"),
                    (36, "sun_nap"), (44, "light_pulse"), (52, "sunburst_nova")],
        "art": {
            "silhouette": "A tall, slender hare of pale gold light, mid-stride even when standing. Long ears trail behind it like horizon ribbons. Parts of its outline are UNFINISHED — one hindquarter and the tip of one ear fade into faint sketch-lines of light, as if the painter stopped at the moment the dawn did. The missing parts must read as waiting, not wounded.",
            "palette": "Bone (#f5f0e1) and pale gold body; a sunrise gradient of rose and amber along the spine and ear-ribbons; the unfinished edges in faint diamond-cyan (#9fe7ff) sketch-lines over transparency.",
            "direction": "An unfinished sunrise as a creature — fast, gentle, heartbreaking. The emotional apex of the triad: in the Long Dusk it is incomplete by definition, and the sprite should make the player want to fix that.",
        },
    },
}

def slugify(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")

def dex_entry(c):
    base = c.get("concept", "").strip()
    hook = c.get("hook", "").strip()
    entry = base if base.endswith(".") else base + "."
    if hook:
        # take the first sentence of the hook for an original flavour line
        first = re.split(r"(?<=[.!?])\s", hook)[0]
        entry += " " + (first if first.endswith((".", "!", "?")) else first + ".")
    return entry[:300]

def category(c):
    t = c["types"][0]
    role = norm_role(c.get("role"))
    word = {"physical sweeper":"Striker","special sweeper":"Caster","glass cannon":"Fragile","physical wall":"Bulwark",
            "special wall":"Warden","physical bruiser":"Brute","special tank":"Channeler","balanced / pivot":"Wanderer",
            "utility / speedster":"Courier","disruptor / status":"Trickster"}[role]
    return f"{t} {word} Kin"

def main():
    selected = json.load(open(SEL))
    by_dex = {e["dex_id"]: e for e in selected}
    # group lines by following dex_id contiguity via line membership recorded in concept ids/order:
    # selected.json lists members consecutively per line; reconstruct lines by 'from/into' using line.kindles_into mapping of concept_ids -> dex_ids
    cid_to_dex = {e["concept_id"]: e["dex_id"] for e in selected}

    out_all = []
    for e in selected:
        name = e["name"]
        if e.get("_needs_rename"):
            name = name + " " + {"Ember":"Cinder","Tide":"Brine","Verdant":"Fen","Stone":"Crag","Storm":"Gale",
                                 "Frost":"Rime","Solar":"Sol","Lunar":"Luna","Light":"Glim","Dark":"Null"}[e["types"][0]]
            name = name.replace(" ", "")  # keep one-word style; flesh polish later
        tier = e["tier"]
        role = norm_role(e.get("role"))
        target = TIER_BST[tier]
        stats = make_stats(role, target, name)
        bst = sum(stats.values())
        stage = (e.get("line") or {}).get("stage", 1)
        nxt_cid = (e.get("line") or {}).get("kindles_into")
        into = cid_to_dex.get(nxt_cid) if isinstance(nxt_cid, str) else None
        # 'from': find a concept whose kindles_into == this concept_id
        frm = None
        for o in selected:
            ok = (o.get("line") or {}).get("kindles_into")
            if ok == e["concept_id"]:
                frm = o["dex_id"]; break
        scripted = (e.get("rarity") in ("legendary",)
                    or (tier in ("E", "F") and e.get("rarity") == "very_rare")
                    or slugify(name) in SCRIPTED_KIN)
        ab, hab = pick_ability(e["types"], role, tier)
        kindling = None
        if into:
            kindling = {"into": into, "trigger": parse_trigger((e.get("line") or {}).get("kindle_trigger"), stage, tier)}
        rec = {
            "id": e["dex_id"],
            "slug": slugify(name),
            "name": name,
            "types": e["types"],
            "role": role.title().replace(" / ", " / "),
            "tier": tier,
            "stats": stats,
            "bst": bst,
            "ability": ab,
            "hidden_ability": hab,
            "catchRate": TIER_CATCH[tier] + (-8 if e.get("rarity") in ("rare","very_rare") else 0) if tier not in ("F",) else TIER_CATCH["F"],
            "kindling": kindling,
            "from": frm,
            "stage": stage,
            "learnset": {"levelup": learnset(e["types"], role, tier), "kindling": [], "tutor": []},
            "dex": {
                "entry": dex_entry(e),
                "category": category(e),
                "size_cm": e.get("size_cm") or (320 if tier in ("E", "F") else 70),
                "weight_kg": e.get("weight_kg") or (240 if tier in ("E", "F") else 12),
                "habitat": e.get("region", "south"),
            },
            "encounters": encounters(e.get("region","south"), e.get("rarity","common"), tier, stage, scripted),
            "scripted": bool(scripted),
            "art": {
                "silhouette": e.get("visual", ""),
                "palette": e.get("visual", ""),
                "direction": e.get("hook", ""),
            },
            "provenance_concept_id": e["concept_id"],
        }
        # clamp catchRate into band
        lo, hi = {"A":(190,235),"B":(150,200),"C":(90,150),"D":(45,90),"E":(20,45),"F":(3,10)}[tier]
        rec["catchRate"] = max(lo, min(hi, rec["catchRate"]))
        # Built-map areas are hand-curated: drop any generated default row that
        # claims one (the EXTRA_ENCOUNTERS mirror is the only allowed source),
        # then merge the hand-curated placements so they survive a rebuild.
        rec["encounters"] = [x for x in rec["encounters"] if x["area"] not in CURATED_AREAS]
        rec["encounters"].extend(EXTRA_ENCOUNTERS.get(rec["slug"], []))
        # Preserve hand-added encounter rows from the existing per-species file.
        # Map-content work appends area tables the generator doesn't know about
        # (e.g. pearlmoor_quay); regenerating must not clobber them. Keys are
        # taken AFTER the EXTRA_ENCOUNTERS merge and preserved rows are deduped,
        # so a rebuild never re-appends the extras (the old duplicate-row bug),
        # and stale rows naming a CURATED area are dropped, not resurrected.
        if not scripted:
            prev_path = os.path.join(OUTDIR, f"{e['dex_id']:03d}_{rec['slug']}.json")
            if os.path.exists(prev_path):
                try:
                    prev = json.load(open(prev_path))
                    seen_keys = {json.dumps(x, sort_keys=True) for x in rec["encounters"]}
                    for enc in prev.get("encounters", []):
                        key = json.dumps(enc, sort_keys=True)
                        if key in seen_keys or enc.get("area") in CURATED_AREAS:
                            continue
                        seen_keys.add(key)
                        rec["encounters"].append(enc)
                except Exception:
                    pass
        # apply canonical overrides (starters + appended canon kin). Every key
        # is optional: pin only what the dossier locks (e.g. the Three Hours
        # pin abilities/dex/kits/art but trust make_stats for their lines).
        canon = CANON.get(rec["slug"])
        if canon:
            if "stats" in canon:
                rec["stats"] = canon["stats"]; rec["bst"] = sum(canon["stats"].values())
            if "ability" in canon: rec["ability"] = canon["ability"]
            if "hidden_ability" in canon: rec["hidden_ability"] = canon["hidden_ability"]
            if "entry" in canon: rec["dex"]["entry"] = canon["entry"]
            if "category" in canon: rec["dex"]["category"] = canon["category"]
            if "size_cm" in canon: rec["dex"]["size_cm"] = canon["size_cm"]
            if "weight_kg" in canon: rec["dex"]["weight_kg"] = canon["weight_kg"]
            if "art" in canon: rec["art"].update(canon["art"])
            if "levelup" in canon:  # pinned full ladder (validated, level-sorted)
                rec["learnset"]["levelup"] = [
                    {"level": lvl, "move": mv}
                    for lvl, mv in sorted(canon["levelup"], key=lambda r: r[0])
                    if mv in MOVE_IDS
                ]
            sig = canon.get("signature")
            if sig and sig in MOVE_IDS and not any(e["move"] == sig for e in rec["learnset"]["levelup"]):
                rec["learnset"]["levelup"].insert(0, {"level": 1, "move": sig})
        # apex signature moves (late learnset payoff)
        sigrow = SIGNATURE_MOVES.get(rec["slug"])
        if sigrow:
            sid, slvl = sigrow
            if sid in MOVE_IDS and not any(e["move"] == sid for e in rec["learnset"]["levelup"]):
                rec["learnset"]["levelup"].append({"level": slvl, "move": sid})
                rec["learnset"]["levelup"].sort(key=lambda e: e["level"])
        out_all.append(rec)
        with open(os.path.join(OUTDIR, f"{e['dex_id']:03d}_{rec['slug']}.json"), "w") as f:
            json.dump(rec, f, indent=2)
            f.write("\n")

    combined = {"_notes": "Generated by tools/balance/build_species.py from the panel-selected concepts. Mechanical fields are deterministic from role/tier/type; creative fields come from the selected concepts. Per-species files in src/game/data/species/.",
                "version": 1, "count": len(out_all), "species": out_all}
    with open(os.path.join(ROOT, "src", "game", "data", "species.json"), "w") as f:
        json.dump(combined, f, indent=1)
        f.write("\n")
    print(f"Built {len(out_all)} species -> src/game/data/species.json (+ per-species files)")
    # quick tier/type tally
    from collections import Counter
    print("Tiers:", dict(Counter(r["tier"] for r in out_all)))
    print("Types:", dict(Counter(r["types"][0] for r in out_all)))

if __name__ == "__main__":
    main()
