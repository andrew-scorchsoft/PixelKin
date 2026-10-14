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
    # the Old Light's own kin (#167-171, R10): their default row names a curated
    # tower floor, so it is dropped — only the mirrored tower tables place them
    "jesthouse": ("pearlmoor_oldlight_1", (9, 14)),
    # Lane B (Farlamp Isles, #172-177): the isles' kin live ONLY in the isles'
    # own map tables (mirrored into EXTRA_ENCOUNTERS by the map work), so
    # MAP_TABLE_ONLY_REGIONS below suppresses the generated default row.
    "isles": ("farlamp_sound", (58, 66)),
    # Lane N4 (the Hollowing's Country, #178-180): the Hollowing family lives
    # ONLY in Stillwater / the Mourning Fields / Drownlight tables (mirrored
    # into EXTRA_ENCOUNTERS by the map lanes) — table-only like the isles.
    "north_hollow": ("stillwater", (46, 56)),
}
MAP_TABLE_ONLY_REGIONS = {"isles", "north_hollow"}
TERRAIN = {"north_hollow":"tall_grass","isles":"water","jesthouse":"cave","south":"tall_grass","east":"cave","north":"tall_grass","west":"water","outer":"tall_grass","central":"cave","post":"tall_grass"}

def encounters(region, rarity, tier, stage, scripted):
    area, (blo, bhi) = REGION_AREA.get(region, ("dimglass_coast", (3, 12)))
    # higher tier / later stage -> higher level within the band
    bump = {"A":0,"B":3,"C":7,"D":12,"E":16,"F":20}[tier]
    lo = min(bhi-2, blo + bump + (stage-1)*3)
    hi = min(bhi, lo + 3)
    if scripted or region in MAP_TABLE_ONLY_REGIONS:
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
                  {"area": "dimglass_coast_ii", "terrain": "tall_grass", "rarity": "common", "min": 8, "max": 10}],
    "brineroll": [{"area": "pearlmoor_quay", "terrain": "water", "rarity": "uncommon", "min": 10, "max": 12},
                  {"area": "saltreach_fen_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 16, "max": 18},
                  # fen II reeds: thinned (D1 dex-spread, 2026-06) — Pebbit takes
                  # the slot; Brineroll keeps the fen channels via fen_i + water rows
                  {"area": "sunkbell_shallows", "terrain": "water", "rarity": "common", "min": 17, "max": 19},
                  {"area": "tideglass_cavern", "terrain": "cave", "rarity": "uncommon", "min": 21, "max": 24},
                  {"area": "tideglass_cavern", "terrain": "water", "rarity": "common", "min": 21, "max": 24},
                  {"area": "dimglass_coast_ii", "terrain": "tall_grass", "rarity": "common", "min": 9, "max": 10}],
    "lumpin":    [{"area": "pearlmoor_quay", "terrain": "tall_grass", "rarity": "common", "min": 9, "max": 11},
                  # saltreach reeds + tideglass cave: thinned (D1 dex-spread,
                  # 2026-06) — Pebbit/Fossik take the slots; Lumpin keeps the
                  # fen channels (water) and its South home maps
                  {"area": "saltreach_fen_ii", "terrain": "water", "rarity": "uncommon", "min": 17, "max": 19},
                  {"area": "dimglass_coast", "terrain": "tall_grass", "rarity": "common", "min": 3, "max": 6},
                  {"area": "dimglass_coast_ii", "terrain": "tall_grass", "rarity": "common", "min": 8, "max": 10}],
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
                    # hushfrost I: thinned (D1 dex-spread, 2026-06) — Crevasser
                    # takes the West-leg rock slot; Glacewing stays a North kin
                    {"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "rare", "min": 37, "max": 40}],
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
    # D1 dex-spread (2026-06): sunsprout promoted to the West night COMMON
    # (the tables had no >=20-share rung) — weights w28/w24 in the maps
    "sunsprout":   [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "common", "min": 42, "max": 45},
                    {"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "common", "min": 46, "max": 47}],
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
                    # sunvault II night common (D1 dex-spread, w26)
                    {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "common", "min": 47, "max": 48},
                    {"area": "helia_vault", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 49},
                    {"area": "helia_vault", "terrain": "cave", "rarity": "common", "min": 48, "max": 49}],
    "helicore":    [{"area": "sunken_solarium", "terrain": "tall_grass", "rarity": "rare", "min": 44, "max": 46},
                    {"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 48},
                    # sunvault II night common (D1 dex-spread, w24)
                    {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "common", "min": 47, "max": 48},
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
    # Coldfog I/II: mirrored by COLDFOG_TABLES (dex-id keyed, below the Stillwater mirror)
    "nullmoth":    [{"area": "hollowfen_stillworks", "terrain": "tall_grass", "rarity": "common", "min": 48, "max": 50}],
    "cindersob":   [# hushfrost II's "numbed" pockets only (w30 there) — rare cap
                    {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "rare", "min": 40, "max": 42}],
    "wispwanenull": [{"area": "hollowfen_stillworks", "terrain": "tall_grass", "rarity": "common", "min": 48, "max": 50}],
    "embergone":   [{"area": "hollowfen_stillworks", "terrain": "tall_grass", "rarity": "common", "min": 49, "max": 50}],
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

# ---------------------------------------------------------------------------
# The day-form pass (06-postgame · R4, 2026-06) — mirrors of the BUILT
# `flag:dawn`-gated day EncounterZones on the relit outdoor maps (the maps'
# `*_day` zone twins are the truth; the dex side is flag-blind, so each map
# now carries TWO rows per species/terrain where bands differ: the journey
# band + the 55-65 post-dawn band). Same weight->rarity rule as W6; per-map
# same-terrain zones merged per species. Coldfog I/II are the Light RE-BLOOM
# (atlas §4 inverted): Wisprestored + the wane-line's Light halves bloom,
# Mothdim/Nullmoth thin, Voidmantle withdraws from the day tables entirely.
# Includes the NIGHT gap-fill rows for the maps first curated here
# (tinderwick, gullcry_rock, the fen_ii channels, the sunkbell shallows).
R4_DAYFORM_ENCOUNTERS = {
    # ---- night gap-fills (newly curated areas' pre-dawn tables) ----
    "wickmoth":   [{"area": "tinderwick", "terrain": "tall_grass", "rarity": "common", "min": 2, "max": 4},
                   {"area": "tinderwick", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 60}],
    "tallowpup":  [{"area": "tinderwick", "terrain": "tall_grass", "rarity": "common", "min": 2, "max": 3},
                   {"area": "tinderwick", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 58}],
    "glostern":   [{"area": "gullcry_rock", "terrain": "water", "rarity": "common", "min": 11, "max": 13},
                   {"area": "gullcry_rock", "terrain": "water", "rarity": "common", "min": 58, "max": 65}],
    # ---- South day rows ----
    "wicklit":    [{"area": "tinderwick", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 60}],
    "glimflit":   [{"area": "tinderwick", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62},
                   {"area": "dimglass_coast", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62}],
    "brinelet":   [{"area": "dimglass_coast", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 60},
                   {"area": "dimglass_coast_ii", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 61},
                   {"area": "pearlmoor_quay", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62}],
    "lumpin":     [{"area": "gullcry_rock", "terrain": "water", "rarity": "common", "min": 10, "max": 12},
                   {"area": "sunkbell_shallows", "terrain": "water", "rarity": "common", "min": 17, "max": 19},
                   {"area": "dimglass_coast", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 62},
                   {"area": "dimglass_coast_ii", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 63},
                   {"area": "pearlmoor_quay", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 63},
                   {"area": "gullcry_rock", "terrain": "water", "rarity": "common", "min": 57, "max": 64},
                   {"area": "saltreach_fen_ii", "terrain": "water", "rarity": "common", "min": 56, "max": 63},
                   {"area": "sunkbell_shallows", "terrain": "water", "rarity": "common", "min": 56, "max": 63}],
    "brineroll":  [{"area": "gullcry_rock", "terrain": "water", "rarity": "common", "min": 11, "max": 13},
                   {"area": "saltreach_fen_ii", "terrain": "water", "rarity": "common", "min": 17, "max": 19},
                   {"area": "dimglass_coast_ii", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 63},
                   {"area": "pearlmoor_quay", "terrain": "water", "rarity": "common", "min": 57, "max": 64},
                   {"area": "gullcry_rock", "terrain": "water", "rarity": "common", "min": 58, "max": 64},
                   {"area": "saltreach_fen_i", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 61},
                   {"area": "sunkbell_shallows", "terrain": "water", "rarity": "common", "min": 56, "max": 62}],
    "brinix":     [{"area": "dimglass_coast", "terrain": "water", "rarity": "common", "min": 55, "max": 62},
                   {"area": "dimglass_coast_ii", "terrain": "water", "rarity": "common", "min": 56, "max": 63},
                   {"area": "pearlmoor_quay", "terrain": "water", "rarity": "common", "min": 57, "max": 64}],
    "shimmral":   [{"area": "dimglass_coast", "terrain": "water", "rarity": "common", "min": 56, "max": 63},
                   {"area": "dimglass_coast_ii", "terrain": "water", "rarity": "common", "min": 57, "max": 64},
                   {"area": "pearlmoor_quay", "terrain": "water", "rarity": "common", "min": 58, "max": 64},
                   {"area": "sunkbell_shallows", "terrain": "water", "rarity": "common", "min": 57, "max": 64}],
    # ---- East day rows ----
    "dewling":    [{"area": "saltreach_fen_i", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 61},
                   {"area": "saltreach_fen_ii", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62}],
    "poolfrond":  [{"area": "saltreach_fen_ii", "terrain": "water", "rarity": "common", "min": 18, "max": 19},
                   {"area": "saltreach_fen_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62},
                   {"area": "saltreach_fen_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63},
                   {"area": "saltreach_fen_ii", "terrain": "water", "rarity": "common", "min": 57, "max": 64}],
    "fennlight":  [{"area": "saltreach_fen_i", "terrain": "tall_grass", "rarity": "rare", "min": 57, "max": 63},
                   {"area": "saltreach_fen_ii", "terrain": "tall_grass", "rarity": "rare", "min": 57, "max": 64},
                   {"area": "lowleaf_hollow", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 63}],
    "sporeling":  [{"area": "lowleaf_hollow", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62}],
    "mossglow":   [{"area": "lowleaf_hollow", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 63}],
    "barkhelm":   [{"area": "lowleaf_hollow", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62}],
    "lumournis":  [{"area": "lowleaf_hollow", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 65}],
    "tidalarch":  [{"area": "sunkbell_shallows", "terrain": "water", "rarity": "uncommon", "min": 58, "max": 65}],
    # ---- North day rows ----
    "sparrowcaw": [{"area": "galehigh_terraces", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 60}],
    "thrumvane":  [{"area": "galehigh_terraces", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 61}],
    "cirruff":    [{"area": "galehigh_terraces", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62},
                   {"area": "windward_stair_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63},
                   {"area": "windward_stair_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 64}],
    "squallox":   [{"area": "galehigh_terraces", "terrain": "tall_grass", "rarity": "uncommon", "min": 55, "max": 61}],
    "flintbeak":  [{"area": "windward_stair_i", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62},
                   {"area": "windward_stair_ii", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62},
                   {"area": "thunderroost", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 63}],
    "sparkrat":   [{"area": "windward_stair_i", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62},
                   {"area": "windward_stair_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62}],
    "thrumble":   [{"area": "windward_stair_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 61},
                   {"area": "windward_stair_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 62}],
    "glacewing":  [{"area": "windward_stair_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63},
                   {"area": "windward_stair_ii", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 63},
                   {"area": "wind_eye", "terrain": "tall_grass", "rarity": "common", "min": 58, "max": 64},
                   {"area": "thunderroost", "terrain": "tall_grass", "rarity": "common", "min": 58, "max": 64}],
    "chillpip":   [{"area": "windward_stair_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 61}],
    "geolace":    [{"area": "windward_stair_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62}],
    "hailwhirr":  [{"area": "wind_eye", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 63}],
    "cumulance":  [{"area": "wind_eye", "terrain": "tall_grass", "rarity": "common", "min": 60, "max": 65},
                   {"area": "thunderroost", "terrain": "tall_grass", "rarity": "uncommon", "min": 60, "max": 65}],
    "strikeaven": [{"area": "thunderroost", "terrain": "tall_grass", "rarity": "common", "min": 60, "max": 65}],
    "glaceling":  [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63},
                   {"area": "pale_vault_glacier", "terrain": "cave", "rarity": "common", "min": 58, "max": 64}],
    "blizzrhare": [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63},
                   {"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62},
                   {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63}],
    "iceling":    [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62}],
    "snowcune":   [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62}],
    "prismcub":   [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 63},
                   {"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 63},
                   {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 64},
                   {"area": "aurora_hollow", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 63}],
    "prismantus": [{"area": "pale_vault_glacier", "terrain": "tall_grass", "rarity": "uncommon", "min": 59, "max": 65},
                   {"area": "pale_vault_glacier", "terrain": "cave", "rarity": "common", "min": 59, "max": 65},
                   {"area": "aurora_hollow", "terrain": "tall_grass", "rarity": "common", "min": 58, "max": 65}],
    "stillwarden":[{"area": "pale_vault_glacier", "terrain": "cave", "rarity": "common", "min": 58, "max": 64},
                   {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 64}],
    # ---- West day rows ----
    "hushbore":   [{"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62},
                   {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 63},
                   {"area": "aurora_hollow", "terrain": "tall_grass", "rarity": "rare", "min": 57, "max": 62}],
    "crystarn":   [{"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 63},
                   {"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63},
                   {"area": "aurora_hollow", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 63}],
    "geodrake":   [{"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62}],
    "vortexlope": [{"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64}],
    "frigalance": [{"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64}],
    "glacitern":  [{"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64}],
    # day numbed-pocket cap: pocket-only species stay rare (the W6 rule)
    "cindersob":  [{"area": "hushfrost_pass_ii", "terrain": "tall_grass", "rarity": "rare", "min": 57, "max": 63}],
    "frostholm":  [{"area": "aurora_hollow", "terrain": "tall_grass", "rarity": "very_rare", "min": 62, "max": 65}],
    "sunsprout":  [{"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62}],
    "helibud":    [{"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62},
                   {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63}],
    "dawnfawn":   [{"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 63},
                   {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 64}],
    "solvyne":    [{"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 63},
                   {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63}],
    "helicore":   [{"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 63},
                   {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63}],
    "gilpaw":     [{"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62}],
    "goldmane":   [{"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64},
                   {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 64}],
    "auravane":   [{"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64},
                   {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64}],
    "sunstag":    [{"area": "sunvault_climb_i", "terrain": "tall_grass", "rarity": "very_rare", "min": 59, "max": 65},
                   {"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "rare", "min": 59, "max": 65}],
    "lunveil":    [{"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 64}],
    "lunvane":    [{"area": "sunvault_climb_ii", "terrain": "tall_grass", "rarity": "rare", "min": 60, "max": 65}],
    # (the Coldfog day RE-BLOOM rows: COLDFOG_TABLES, below the Stillwater mirror)
}
for _slug, _rows in R4_DAYFORM_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows)

# ---------------------------------------------------------------------------
# The dex-obtainability + encounter-spread pass (D1, 2026-06) — mirrors of the
# BUILT in-map zone edits that placed the 22 unobtainable straggler lines into
# wild tables (every base now has a home; mids/finals ride kindling) and gave
# the South its rare tier. Same W6 weight->rarity rule; day-twin rows only
# where the kin is element-fitting (Light/Ember/Verdant by day).
# Also the FIRST mirrors of the cinderhead_mine/deep(+B1F/B2F) and spore_grotto
# tables (built maps that predated the mirror convention — now CURATED, so the
# full tables live here) and the Skyweavelet bed on umbral_spire_f2 (the one
# new zone rect; band 52-55 to match the Spire floors).
D1_OBTAINABILITY_ENCOUNTERS = {
    # ---- Ember A-line bases ----
    "ashlette":   [{"area": "tinderwick", "terrain": "tall_grass", "rarity": "uncommon", "min": 2, "max": 4},
                   {"area": "tinderwick", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62}],
    "scorchite":  [{"area": "cinderhead_mine", "terrain": "cave", "rarity": "common", "min": 22, "max": 24},
                   {"area": "cinderhead_deep", "terrain": "cave", "rarity": "uncommon", "min": 24, "max": 26}],
    # the b2f coal-seam rare — the mid-stage's genre-correct deep-band slot
    "coalump":    [{"area": "cinderhead_deep_b2f", "terrain": "cave", "rarity": "rare", "min": 26, "max": 27}],
    # ---- Tide/Light bases ----
    "tidmote":    [{"area": "dimglass_coast", "terrain": "water", "rarity": "common", "min": 4, "max": 6},
                   {"area": "dimglass_coast", "terrain": "water", "rarity": "uncommon", "min": 55, "max": 62},
                   {"area": "pearlmoor_quay", "terrain": "water", "rarity": "uncommon", "min": 10, "max": 12},
                   {"area": "pearlmoor_quay", "terrain": "water", "rarity": "uncommon", "min": 57, "max": 64}],
    "tidmaren":   [{"area": "sunkbell_shallows", "terrain": "water", "rarity": "rare", "min": 18, "max": 20}],
    "glintfin":   [{"area": "dimglass_coast_ii", "terrain": "water", "rarity": "common", "min": 9, "max": 11},
                   {"area": "dimglass_coast_ii", "terrain": "water", "rarity": "uncommon", "min": 56, "max": 63},
                   {"area": "gullcry_rock", "terrain": "water", "rarity": "uncommon", "min": 11, "max": 13},
                   {"area": "gullcry_rock", "terrain": "water", "rarity": "uncommon", "min": 58, "max": 64}],
    # ---- Stone bases (the early game's first Stone basics) ----
    "pebbit":     [{"area": "dimglass_coast", "terrain": "tall_grass", "rarity": "rare", "min": 3, "max": 6},
                   {"area": "dimglass_coast_ii", "terrain": "tall_grass", "rarity": "common", "min": 8, "max": 10},
                   {"area": "saltreach_fen_i", "terrain": "tall_grass", "rarity": "uncommon", "min": 16, "max": 18},
                   {"area": "saltreach_fen_ii", "terrain": "tall_grass", "rarity": "uncommon", "min": 17, "max": 19}],
    "flickore":   [{"area": "cinderhead_mine", "terrain": "cave", "rarity": "uncommon", "min": 22, "max": 24},
                   {"area": "cinderhead_deep_b1f", "terrain": "cave", "rarity": "uncommon", "min": 25, "max": 27}],
    "fossik":     [{"area": "tideglass_cavern", "terrain": "cave", "rarity": "common", "min": 20, "max": 23}],
    "oreling":    [{"area": "cinderhead_deep", "terrain": "cave", "rarity": "uncommon", "min": 24, "max": 26},
                   {"area": "cinderhead_deep_b2f", "terrain": "cave", "rarity": "uncommon", "min": 26, "max": 27}],
    # the Fossik mid's West-leg rock rare (takes Glacewing's thinned slot)
    "crevasser":  [{"area": "hushfrost_pass_i", "terrain": "tall_grass", "rarity": "rare", "min": 40, "max": 41}],
    # ---- the standalone Stone riddler + the Light strays ----
    "riddlestone": [{"area": "cinderhead_deep_b1f", "terrain": "cave", "rarity": "rare", "min": 25, "max": 27},
                    {"area": "cinderhead_deep_b2f", "terrain": "cave", "rarity": "rare", "min": 26, "max": 27}],
    "glowsip":    [{"area": "lowleaf_hollow", "terrain": "tall_grass", "rarity": "uncommon", "min": 18, "max": 20},
                   {"area": "lowleaf_hollow", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 63},
                   {"area": "spore_grotto", "terrain": "tall_grass", "rarity": "uncommon", "min": 21, "max": 23}],
    "skyweavelet": [{"area": "umbral_spire_f2", "terrain": "cave", "rarity": "common", "min": 52, "max": 55}],
    # ---- the South rare tier (D1 spread fix) ----
    "wicklit":    [{"area": "tinderwick", "terrain": "tall_grass", "rarity": "rare", "min": 3, "max": 4},
                   {"area": "pearlmoor_quay", "terrain": "tall_grass", "rarity": "rare", "min": 9, "max": 11}],
    # ---- first mirrors of the pre-existing cinderhead/spore in-map tables ----
    "gravelo":    [{"area": "cinderhead_mine", "terrain": "cave", "rarity": "common", "min": 22, "max": 24},
                   {"area": "cinderhead_deep", "terrain": "cave", "rarity": "common", "min": 24, "max": 26},
                   {"area": "cinderhead_deep_b1f", "terrain": "cave", "rarity": "common", "min": 25, "max": 27},
                   {"area": "cinderhead_deep_b2f", "terrain": "cave", "rarity": "common", "min": 26, "max": 27}],
    "sparkrat":   [{"area": "cinderhead_mine", "terrain": "cave", "rarity": "common", "min": 22, "max": 24},
                   {"area": "cinderhead_deep", "terrain": "cave", "rarity": "common", "min": 24, "max": 26},
                   {"area": "cinderhead_deep_b1f", "terrain": "cave", "rarity": "common", "min": 25, "max": 27},
                   {"area": "cinderhead_deep_b2f", "terrain": "cave", "rarity": "common", "min": 26, "max": 27}],
    "crystink":   [{"area": "cinderhead_mine", "terrain": "cave", "rarity": "uncommon", "min": 22, "max": 24},
                   {"area": "cinderhead_deep", "terrain": "cave", "rarity": "uncommon", "min": 24, "max": 26},
                   {"area": "cinderhead_deep_b1f", "terrain": "cave", "rarity": "uncommon", "min": 25, "max": 27},
                   {"area": "cinderhead_deep_b2f", "terrain": "cave", "rarity": "uncommon", "min": 26, "max": 27}],
    "sporemid":   [{"area": "spore_grotto", "terrain": "tall_grass", "rarity": "common", "min": 21, "max": 23}],
    "sporeling":  [{"area": "spore_grotto", "terrain": "tall_grass", "rarity": "common", "min": 21, "max": 23}],
    "fennlight":  [{"area": "spore_grotto", "terrain": "tall_grass", "rarity": "uncommon", "min": 22, "max": 23}],
    "mycelarch":  [{"area": "spore_grotto", "terrain": "tall_grass", "rarity": "rare", "min": 22, "max": 23}],
}
for _slug, _rows in D1_OBTAINABILITY_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows)

# S5 "Not All Who Wander" (2026-10): the Wanderwood above Pearlmoor — mirrors
# of the BUILT in-map tall-grass table (public/assets/maps/pearlmoor_wanderwood
# .json; tools/maps/build_pearlmoor_wanderwood.py is the source): the night band
# + its flag:dawn day twin. Spirlet (Omenire's line's first stage) is the rare find.
WANDERWOOD_ENCOUNTERS = {
    "sporeling": [{"area": "pearlmoor_wanderwood", "terrain": "tall_grass", "rarity": "common", "min": 14, "max": 16},
                  {"area": "pearlmoor_wanderwood", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 58}],
    "barkhelm":  [{"area": "pearlmoor_wanderwood", "terrain": "tall_grass", "rarity": "common", "min": 14, "max": 16},
                  {"area": "pearlmoor_wanderwood", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 59}],
    "mossglow":  [{"area": "pearlmoor_wanderwood", "terrain": "tall_grass", "rarity": "common", "min": 15, "max": 17},
                  {"area": "pearlmoor_wanderwood", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 60}],
    "snoozlet":  [{"area": "pearlmoor_wanderwood", "terrain": "tall_grass", "rarity": "uncommon", "min": 15, "max": 17},
                  {"area": "pearlmoor_wanderwood", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 60}],
    "spirlet":   [{"area": "pearlmoor_wanderwood", "terrain": "tall_grass", "rarity": "rare", "min": 15, "max": 17},
                  {"area": "pearlmoor_wanderwood", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 61}],
}
# The Far Side (pearlmoor_wanderwood_far, the wood's optional loop) carries the
# SAME table in its own grass (tools/maps/build_pearlmoor_wanderwood_far.py).
for _slug, _rows in list(WANDERWOOD_ENCOUNTERS.items()):
    WANDERWOOD_ENCOUNTERS[_slug] = _rows + [{**r, "area": "pearlmoor_wanderwood_far"} for r in _rows]
for _slug, _rows in WANDERWOOD_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows)

# R8 (2026-10): Duskapple Orchard, the old orchard west of Tinderwick's square —
# mirrors of the BUILT meadow table (public/assets/maps/duskapple_orchard.json;
# tools/maps/build_duskapple_orchard.py is the source): the lv 2-4 training band
# (the verge's own kin + a Glimflit) and its flag:dawn day twin. Weights ->
# rarity by the W6 share rule (>=20 common, 10-19 uncommon, 5-9 rare).
ORCHARD_ENCOUNTERS = {
    "wickmoth":  [{"area": "duskapple_orchard", "terrain": "tall_grass", "rarity": "common", "min": 2, "max": 4},
                  {"area": "duskapple_orchard", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 60}],
    "tallowpup": [{"area": "duskapple_orchard", "terrain": "tall_grass", "rarity": "common", "min": 2, "max": 4},
                  {"area": "duskapple_orchard", "terrain": "tall_grass", "rarity": "common", "min": 55, "max": 58}],
    "glimflit":  [{"area": "duskapple_orchard", "terrain": "tall_grass", "rarity": "uncommon", "min": 3, "max": 4},
                  {"area": "duskapple_orchard", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62}],
    "wicklit":   [{"area": "duskapple_orchard", "terrain": "tall_grass", "rarity": "rare", "min": 3, "max": 4},
                  {"area": "duskapple_orchard", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 60}],
}
for _slug, _rows in ORCHARD_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows)

# The 2026-10 geometry fix's two new routes — mirrors of their BUILT in-map
# tables (tools/maps/build_cinderwind_scarp.py, build_umbral_approach.py).
# Weights -> rarity by the W6 share rule (>=20 common, 10-19 uncommon, <10 rare).
def _rows(area, lo_hi_rarity):
    return [{"area": area, "terrain": "tall_grass", "rarity": r, "min": lo, "max": hi}
            for (lo, hi, r) in lo_hi_rarity]
GEOMETRY_ENCOUNTERS = {
    # Cinderwind Scarp (lv 28-31): the climb from Cinderhead Deep to Galehigh
    "rubbol":   _rows("cinderwind_scarp", [(28, 30, "common")]),
    # (Lane A, 2026-10: retuned to 28-30 — the Ashfall Shelf above carries 30-33)
    "galefox":  _rows("cinderwind_scarp", [(28, 30, "common")]),
    "thrumble": _rows("cinderwind_scarp", [(29, 30, "common")]),
    "lumecite": _rows("cinderwind_scarp", [(29, 30, "uncommon")]),
    "nimbruff": _rows("cinderwind_scarp", [(30, 30, "rare")]),
    "voltcrag": _rows("cinderwind_scarp", [(30, 30, "very_rare")]),
    # The Umbral Approach (lv 50-53): the mountain road to the Penumbra
    "voidmantle":  _rows("umbral_approach", [(50, 53, "common")]),
    "omenire":     _rows("umbral_approach", [(50, 53, "common")]),
    "nightwraith": _rows("umbral_approach", [(50, 53, "uncommon")]),
    "whorlix":     _rows("umbral_approach", [(50, 53, "uncommon")]),
    "pyriven":     _rows("umbral_approach", [(51, 53, "uncommon")]),
    "liminalux":   _rows("umbral_approach", [(51, 53, "uncommon")]),
}
for _slug, _rows_ in GEOMETRY_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows_)

# Lane A (walkthrough/10 Part II, 2026-10): the Ashfall Shelf (lv 30-33, the main
# path between the Scarp and Galehigh) + Kiln Gully (lv 33-35, optional, the cold
# lamp-glass kiln behind the Updraft vent) — mirrors of the BUILT in-map tables
# (tools/maps/build_cinderwind_ashfall.py, build_cinderwind_kiln.py). Stonebark is
# the shelf's own rare: never wild before, it grows in the grey ash-grass.
def _cave(area, lo_hi_rarity):
    return [{"area": area, "terrain": "cave", "rarity": r, "min": lo, "max": hi}
            for (lo, hi, r) in lo_hi_rarity]
ASHFALL_ENCOUNTERS = {
    # (third pass) the ash beds and the green beds run DIFFERENT mixes — the ash is
    # slag country (Stone/Ember + Stonebark), the green is the wind's (Storm +
    # Voltcrag); the dex merges same-terrain rows per area (W6 rule)
    "gravelo":     _rows("cinderwind_ashfall", [(31, 33, "common")]),
    "sparkrat":    _rows("cinderwind_ashfall", [(30, 31, "common")]),
    "flintbeak":   _rows("cinderwind_ashfall", [(30, 32, "common")]),
    "galefox":     _rows("cinderwind_ashfall", [(30, 32, "common")]),
    "thrumble":    _rows("cinderwind_ashfall", [(30, 31, "common")]),
    "pyrolith":    _rows("cinderwind_ashfall", [(32, 33, "uncommon")])
                   + _cave("cinderwind_kiln", [(34, 35, "uncommon")]),
    "stonebark":   _rows("cinderwind_ashfall", [(30, 31, "uncommon")]),
    "voltcrag":    _rows("cinderwind_ashfall", [(32, 33, "rare")]),
    "lumecite":    _cave("cinderwind_kiln", [(33, 35, "common")]),
    "riddlestone": _cave("cinderwind_kiln", [(33, 35, "common")]),
    "orebound":    _cave("cinderwind_kiln", [(33, 33, "uncommon")]),
    "pyriven":     _cave("cinderwind_kiln", [(34, 35, "uncommon")]),
    # the kiln's signature: the only pre-dawn wild Scorchwing (its other placement is
    # the post-dawn Hearthfall vigil) — a moth-hawk drawn to the old furnace's coals
    "scorchwing":  _cave("cinderwind_kiln", [(34, 35, "rare")]),
    "prismara":    _cave("cinderwind_kiln", [(35, 35, "very_rare")]),
}
for _slug, _rows_ in ASHFALL_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows_)
# ...and their post-dawn DAY-FORM twins (tools/maps/hand_placed_data.py, the R4 pattern)
ASHFALL_DAY_ENCOUNTERS = {
    "voltcrag":    _rows("cinderwind_ashfall", [(56, 61, "common")]),
    "gravelo":     _rows("cinderwind_ashfall", [(56, 61, "common")]),
    "strikeaven":  _rows("cinderwind_ashfall", [(57, 62, "common")]),
    "tempestail":  _rows("cinderwind_ashfall", [(57, 62, "uncommon")]),
    "rootwarden":  _rows("cinderwind_ashfall", [(58, 62, "uncommon")]),
    "prismara":    _cave("cinderwind_kiln", [(57, 63, "common")]),
    "riddlestone": _cave("cinderwind_kiln", [(56, 62, "common")]),
    "ferrolith":   _cave("cinderwind_kiln", [(57, 63, "common")]),
    "pyrolith":    _cave("cinderwind_kiln", [(56, 62, "common")]),
    "lithonyx":    _cave("cinderwind_kiln", [(58, 63, "uncommon")]),
}
for _slug, _rows_ in ASHFALL_DAY_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows_)

# The Wild Ways — Sunvault Climb rebuild (S, 09-the-wild-ways §2 S, 2026-10): the
# Gilt Face + the Sun Ledges' BUILT in-map tables (tools/maps/build_sunvault_climb_iii/_iv.py),
# night (48-49) + day twins. Same W6 weight->rarity rule.
SUNVAULT_FACE_ENCOUNTERS: dict = {}
SUNVAULT_FACE_ENCOUNTERS.setdefault("solvyne", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "common", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("helicore", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("solray", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("lunveil", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("helibud", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("dawnfawn", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("goldmane", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("auravane", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("sunstag", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 49, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("lunvane", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 49, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("solreach", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 49, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("solvyne", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
SUNVAULT_FACE_ENCOUNTERS.setdefault("helicore", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
SUNVAULT_FACE_ENCOUNTERS.setdefault("solray", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 64})
SUNVAULT_FACE_ENCOUNTERS.setdefault("lunveil", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 64})
SUNVAULT_FACE_ENCOUNTERS.setdefault("helibud", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
SUNVAULT_FACE_ENCOUNTERS.setdefault("dawnfawn", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 57, "max": 63})
SUNVAULT_FACE_ENCOUNTERS.setdefault("goldmane", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64})
SUNVAULT_FACE_ENCOUNTERS.setdefault("auravane", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64})
SUNVAULT_FACE_ENCOUNTERS.setdefault("sunstag", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 59, "max": 65})
SUNVAULT_FACE_ENCOUNTERS.setdefault("lunvane", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 60, "max": 65})
SUNVAULT_FACE_ENCOUNTERS.setdefault("solreach", []).append({"area": "sunvault_climb_iii", "terrain": "tall_grass", "rarity": "rare", "min": 60, "max": 65})
SUNVAULT_FACE_ENCOUNTERS.setdefault("lunveil", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("solray", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("petalune", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("helicore", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("spirlet", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("drowshorn", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "rare", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("lunvane", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "rare", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("goldmane", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "rare", "min": 48, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("solreach", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "rare", "min": 49, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("crystalune", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "rare", "min": 49, "max": 49})
SUNVAULT_FACE_ENCOUNTERS.setdefault("lunveil", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 64})
SUNVAULT_FACE_ENCOUNTERS.setdefault("solray", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 64})
SUNVAULT_FACE_ENCOUNTERS.setdefault("petalune", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 64})
SUNVAULT_FACE_ENCOUNTERS.setdefault("helicore", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
SUNVAULT_FACE_ENCOUNTERS.setdefault("spirlet", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
SUNVAULT_FACE_ENCOUNTERS.setdefault("drowshorn", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64})
SUNVAULT_FACE_ENCOUNTERS.setdefault("lunvane", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "rare", "min": 60, "max": 65})
SUNVAULT_FACE_ENCOUNTERS.setdefault("goldmane", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64})
SUNVAULT_FACE_ENCOUNTERS.setdefault("solreach", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "rare", "min": 60, "max": 65})
SUNVAULT_FACE_ENCOUNTERS.setdefault("crystalune", []).append({"area": "sunvault_climb_iv", "terrain": "tall_grass", "rarity": "rare", "min": 60, "max": 65})
for _slug, _rows_ in SUNVAULT_FACE_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows_)

# The Wild Ways — the Rimeway (C, 09-the-wild-ways §2 C, 2026-10): the Ascent/Fold/Descent
# BUILT in-map tables (tools/maps/build_rimeway_*.py), night + day twins; Vaultclaw #76
# lives only up here. Same W6 weight->rarity rule.
RIMEWAY_ENCOUNTERS: dict = {}
RIMEWAY_ENCOUNTERS.setdefault("blizzrhare", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "common", "min": 39, "max": 41})
RIMEWAY_ENCOUNTERS.setdefault("crystarn", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "uncommon", "min": 39, "max": 41})
RIMEWAY_ENCOUNTERS.setdefault("geodrake", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "uncommon", "min": 39, "max": 41})
RIMEWAY_ENCOUNTERS.setdefault("hushbore", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "uncommon", "min": 39, "max": 41})
RIMEWAY_ENCOUNTERS.setdefault("prismcub", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "uncommon", "min": 39, "max": 40})
RIMEWAY_ENCOUNTERS.setdefault("geolace", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "uncommon", "min": 39, "max": 40})
RIMEWAY_ENCOUNTERS.setdefault("glacitern", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "rare", "min": 40, "max": 41})
RIMEWAY_ENCOUNTERS.setdefault("vaultclaw", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "rare", "min": 41, "max": 41})
RIMEWAY_ENCOUNTERS.setdefault("blizzrhare", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62})
RIMEWAY_ENCOUNTERS.setdefault("crystarn", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 63})
RIMEWAY_ENCOUNTERS.setdefault("geodrake", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
RIMEWAY_ENCOUNTERS.setdefault("hushbore", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62})
RIMEWAY_ENCOUNTERS.setdefault("prismcub", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62})
RIMEWAY_ENCOUNTERS.setdefault("geolace", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62})
RIMEWAY_ENCOUNTERS.setdefault("glacitern", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64})
RIMEWAY_ENCOUNTERS.setdefault("vaultclaw", []).append({"area": "rimeway_ascent", "terrain": "tall_grass", "rarity": "rare", "min": 60, "max": 65})
RIMEWAY_ENCOUNTERS.setdefault("crystarn", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "common", "min": 40, "max": 42})
RIMEWAY_ENCOUNTERS.setdefault("geodrake", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 40, "max": 42})
RIMEWAY_ENCOUNTERS.setdefault("blizzrhare", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 40, "max": 41})
RIMEWAY_ENCOUNTERS.setdefault("snowcune", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 40, "max": 41})
RIMEWAY_ENCOUNTERS.setdefault("geolace", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 40, "max": 41})
RIMEWAY_ENCOUNTERS.setdefault("chillpip", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 40, "max": 41})
RIMEWAY_ENCOUNTERS.setdefault("vaultclaw", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "rare", "min": 41, "max": 42})
RIMEWAY_ENCOUNTERS.setdefault("crystarn", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
RIMEWAY_ENCOUNTERS.setdefault("geodrake", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
RIMEWAY_ENCOUNTERS.setdefault("blizzrhare", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62})
RIMEWAY_ENCOUNTERS.setdefault("snowcune", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62})
RIMEWAY_ENCOUNTERS.setdefault("geolace", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62})
RIMEWAY_ENCOUNTERS.setdefault("chillpip", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 61})
RIMEWAY_ENCOUNTERS.setdefault("vaultclaw", []).append({"area": "rimeway_fold", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 64})
RIMEWAY_ENCOUNTERS.setdefault("wispwane", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "common", "min": 46, "max": 47})
RIMEWAY_ENCOUNTERS.setdefault("nullmoth", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "common", "min": 46, "max": 48})
RIMEWAY_ENCOUNTERS.setdefault("wispwanenull", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 48})
RIMEWAY_ENCOUNTERS.setdefault("mothdim", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 47})
RIMEWAY_ENCOUNTERS.setdefault("crystarn", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 47})
RIMEWAY_ENCOUNTERS.setdefault("cindersob", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "rare", "min": 47, "max": 48})
RIMEWAY_ENCOUNTERS.setdefault("glacitern", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "rare", "min": 47, "max": 48})
RIMEWAY_ENCOUNTERS.setdefault("embergone", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "rare", "min": 48, "max": 48})
RIMEWAY_ENCOUNTERS.setdefault("wispwane", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62})
RIMEWAY_ENCOUNTERS.setdefault("nullmoth", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
RIMEWAY_ENCOUNTERS.setdefault("wispwanenull", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
RIMEWAY_ENCOUNTERS.setdefault("mothdim", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62})
RIMEWAY_ENCOUNTERS.setdefault("crystarn", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
RIMEWAY_ENCOUNTERS.setdefault("cindersob", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63})
RIMEWAY_ENCOUNTERS.setdefault("glacitern", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 64})
RIMEWAY_ENCOUNTERS.setdefault("embergone", []).append({"area": "rimeway_descent", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 64})
for _slug, _rows_ in RIMEWAY_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows_)

# THE WILD WAYS (09-the-wild-ways.md, 2026-10) — the Wick-Run (A): mirrors of the
# BUILT in-map tall-grass tables (tools/maps/build_wickrun_{chute,trestles,
# traverse,lower}.py are the source): the night band (46-50, rising down the run)
# + its flag:dawn day twin. Tallowcrest, Wickmere, Warmantis (and the rare
# Chandrek's night rows) live nowhere else in the wild — the run's own kin.
# Weights -> rarity by the W6 share rule (>=20 common, 10-19 uncommon, 5-9 rare,
# <5 very rare). The crest and the foot are encounter-free.
WICKRUN_ENCOUNTERS = {
    "tallowcrest": [{"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "common", "min": 46, "max": 48},
                   {"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62},
                   {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "common", "min": 47, "max": 48},
                   {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 63},
                   {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "common", "min": 47, "max": 49},
                   {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 63},
                   {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "common", "min": 48, "max": 50},
                   {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 64}],
    "wickmere": [{"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "common", "min": 46, "max": 48},
                {"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 62},
                {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "common", "min": 47, "max": 48},
                {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "common", "min": 56, "max": 63},
                {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "common", "min": 47, "max": 49},
                {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 63},
                {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "common", "min": 48, "max": 50},
                {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "common", "min": 57, "max": 64}],
    "solvyne": [{"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 48},
               {"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62},
               {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 48},
               {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 63},
               {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 49},
               {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63},
               {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 50},
               {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 64}],
    "dawnfawn": [{"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 48},
                {"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 62},
                {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 48},
                {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "uncommon", "min": 56, "max": 63},
                {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 49},
                {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63},
                {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 50},
                {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 64}],
    "helibud": [{"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "uncommon", "min": 46, "max": 48},
               {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 48},
               {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "uncommon", "min": 47, "max": 49},
               {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "uncommon", "min": 48, "max": 50}],
    "warmantis": [{"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "rare", "min": 47, "max": 48},
                 {"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 62},
                 {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "rare", "min": 48, "max": 48},
                 {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "uncommon", "min": 57, "max": 63},
                 {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "rare", "min": 48, "max": 49},
                 {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 63},
                 {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "rare", "min": 49, "max": 50},
                 {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "uncommon", "min": 58, "max": 64}],
    "chandrek": [{"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "very_rare", "min": 48, "max": 48},
                {"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 62},
                {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "very_rare", "min": 48, "max": 48},
                {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "rare", "min": 58, "max": 63},
                {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "very_rare", "min": 49, "max": 49},
                {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "rare", "min": 59, "max": 63},
                {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "very_rare", "min": 50, "max": 50},
                {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "rare", "min": 59, "max": 64}],
    "wicklord": [{"area": "wickrun_chute", "terrain": "tall_grass", "rarity": "rare", "min": 59, "max": 62},
                {"area": "wickrun_trestles", "terrain": "tall_grass", "rarity": "rare", "min": 59, "max": 63},
                {"area": "wickrun_traverse", "terrain": "tall_grass", "rarity": "rare", "min": 60, "max": 63},
                {"area": "wickrun_lower", "terrain": "tall_grass", "rarity": "rare", "min": 60, "max": 64}],
}
for _slug, _rows_ in WICKRUN_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows_)
# THE WILD WAYS — the Old Seams (D, 2026-10): mirrors of the BUILT in-map cave
# tables (tools/maps/build_old_seams_i/ii/iii.py are the source), night band +
# its flag:dawn day twin. Weights -> rarity by the W6 share rule (>=20 common,
# 10-19 uncommon, 5-9 rare, <5 very_rare). Orebound/Ferrolith/Pyrolith/Lithonyx/
# Prismara are the Seams' own; the rest are the Cinderhead regulars, deeper.
def _seam_rows(area, rows):
    def rar(wt):
        return "common" if wt >= 20 else "uncommon" if wt >= 10 else "rare" if wt >= 5 else "very_rare"
    out = {}
    for slug, wt, lo, hi in rows:
        out.setdefault(slug, []).append({"area": area, "terrain": "cave", "rarity": rar(wt),
                                         "min": lo, "max": hi})
    return out
OLD_SEAMS_TABLES = {
    "old_seams_i": [
        ("oreling", 30, 27, 29), ("coalump", 25, 27, 28), ("riddlestone", 20, 28, 29),
        ("gravelo", 15, 27, 29), ("orebound", 10, 28, 29),
        ("oreling", 26, 55, 60), ("coalump", 22, 56, 61), ("riddlestone", 20, 57, 62),
        ("gravelo", 16, 55, 60), ("orebound", 16, 58, 63)],
    "old_seams_ii": [
        ("orebound", 30, 29, 31), ("riddlestone", 20, 29, 30), ("sparkrat", 20, 29, 30),
        ("pyrolith", 15, 29, 31), ("lithonyx", 10, 30, 31), ("ferrolith", 5, 31, 31),
        ("orebound", 26, 56, 61), ("riddlestone", 20, 56, 60), ("sparkrat", 18, 56, 60),
        ("pyrolith", 16, 57, 62), ("lithonyx", 12, 58, 63), ("ferrolith", 8, 60, 65)],
    "old_seams_iii": [
        ("orebound", 26, 31, 33), ("coalump", 22, 31, 32), ("pyrolith", 20, 31, 33),
        ("lithonyx", 14, 31, 33), ("ferrolith", 8, 32, 33), ("prismara", 4, 33, 33),
        ("orebound", 24, 57, 62), ("coalump", 20, 56, 61), ("pyrolith", 20, 58, 63),
        ("lithonyx", 14, 58, 63), ("ferrolith", 12, 60, 65), ("prismara", 6, 62, 65)],
}
for _area, _tbl in OLD_SEAMS_TABLES.items():
    for _slug, _rows_ in _seam_rows(_area, _tbl).items():
        EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows_)
# ---- THE WILD WAYS: the Mirelights (09-the-wild-ways §2 B) — mirrors of the
# built in-map tables (tools/maps/mirelight_common.py — the truth; weights ->
# rarity: >=20 common, 10-19 uncommon, 5-9 rare, <5 very_rare). Night 38-43,
# day-forms 55-64. Tidwraith/Lumplass are the Mirelights' own; Lampling (the
# C1 trail's scripted catch) also drifts here, rarely, as a lost light.
_MIRE_SLUG = {31: "lumpin", 67: "fennlight", 27: "brineroll", 60: "poolfrond", 22: "tidwraith",
              21: "tidmaren", 29: "glostern", 32: "lumplass", 148: "lampling"}
# (area, [(kin, weight, night_min, night_max)], day shift) — the SAME species by
# day (the R4 day-form convention: the woken forms of the same water), +shift
# levels and four wider. The night beds sit at the lv-40 beds' BST (~400), the
# grown D-tier forms being the trainers'.
_MIRE_TABLES = [
    ("mirelight_landing", [(31, 30, 38, 40), (67, 24, 38, 41), (27, 22, 38, 40),
                           (60, 16, 39, 40), (22, 8, 39, 41)], 17),
    ("mirelight_glassmere", [(31, 30, 40, 42), (21, 24, 40, 42), (29, 22, 40, 41),
                             (22, 9, 40, 42), (32, 9, 41, 42), (148, 6, 42, 42)], 17),
    ("mirelight_chapel", [(31, 28, 41, 43), (67, 22, 41, 42), (21, 20, 41, 43),
                          (32, 12, 41, 43), (22, 9, 41, 43), (148, 9, 43, 43)], 17),
]


def _mire_rarity(w):
    return "common" if w >= 20 else "uncommon" if w >= 10 else "rare" if w >= 5 else "very_rare"


MIRELIGHT_ENCOUNTERS: dict = {}
for _area, _tab, _shift in _MIRE_TABLES:
    for (_k, _w, _lo, _hi) in _tab:
        MIRELIGHT_ENCOUNTERS.setdefault(_MIRE_SLUG[_k], []).extend(
            _rows(_area, [(_lo, _hi, _mire_rarity(_w)),
                          (_lo + _shift, _hi + _shift + 4, _mire_rarity(_w))]))
for _slug, _rows_ in MIRELIGHT_ENCOUNTERS.items():
    EXTRA_ENCOUNTERS.setdefault(_slug, []).extend(_rows_)

# ---- Lane C2 (10-the-farlamp-isles.md Part I): the Undertide — MIRRORS of the
# built in-map tables (tools/maps/build_undertide_i/ii/iii/iv.py are the truth;
# keep both in step). Post-game only (no night/day pair: the isles keep their own
# dusk). Cave = rect-wide on the galleries; water = the shallows (tide-race lanes
# never roll). Weights -> rarity: >=20 common, 10-19 uncommon, 5-9 rare, <5 very_rare.
_UT_SLUG = {172: "fathomote", 173: "fathomere", 174: "hermiwick", 175: "beaconclaw",
            176: "fogwisp", 25: "prismare", 28: "brinewrath", 29: "glostern",
            30: "glostrael", 34: "tideveil", 52: "lithonyx", 55: "ferrolith",
            61: "tidalarch", 85: "stillwarden", 138: "voidmantle", 157: "pharolux"}
UNDERTIDE_TABLES = {
    "undertide_i": {
        "cave": [(174, 30, 61, 63), (176, 26, 61, 63), (52, 20, 62, 63), (85, 14, 62, 63),
                 (55, 10, 62, 63)],
        "water": [(172, 34, 61, 63), (29, 24, 61, 62), (28, 20, 62, 63), (61, 14, 62, 63),
                  (30, 8, 63, 63)]},
    "undertide_ii": {
        "cave": [(174, 24, 61, 64), (176, 24, 62, 64), (175, 12, 63, 64), (52, 14, 62, 63),
                 (85, 12, 62, 64), (138, 10, 62, 64)],
        "water": [(172, 26, 61, 63), (173, 14, 63, 64), (61, 20, 62, 64), (28, 18, 62, 64),
                  (29, 14, 61, 63), (30, 6, 64, 64)]},
    "undertide_iii": {
        "cave": [(175, 22, 63, 65), (176, 24, 62, 65), (174, 14, 62, 64), (85, 14, 63, 64),
                 (138, 14, 63, 65), (55, 10, 63, 65)],
        "water": [(173, 24, 63, 65), (172, 14, 62, 64), (28, 20, 63, 65), (61, 16, 63, 64),
                  (30, 14, 64, 65), (25, 10, 64, 65)]},
    # deepest: kindled forms common, base forms rare; PHAROLUX (#157) the signature very-rare
    "undertide_iv": {
        "cave": [(175, 28, 64, 66), (176, 26, 63, 66), (138, 14, 64, 66), (85, 12, 63, 65),
                 (55, 12, 64, 66), (174, 6, 63, 64)],
        "water": [(173, 30, 64, 66), (28, 18, 64, 66), (30, 16, 64, 66), (25, 14, 64, 66),
                  (172, 6, 63, 64), (157, 3, 66, 66)]},
}


def _ut_rarity(w):
    return "common" if w >= 20 else "uncommon" if w >= 10 else "rare" if w >= 5 else "very_rare"


# The isles' DAWN (pass 2): each table's day-form twin rises at `flag:isles_dawn` —
# the kindled forms of the same water, +1 level (MIRROR of undertidekit.DAY_SWAP /
# day_table; keep both in step).
UNDERTIDE_DAY_SWAP = {174: 175, 172: 173, 29: 30}


def _ut_day(rows):
    out = {}
    for (k, w, lo, hi) in rows:
        d = UNDERTIDE_DAY_SWAP.get(k, k)
        lo, hi = min(lo + 1, 67), min(hi + 1, 67)
        if d in out:
            pw, plo, phi = out[d]
            out[d] = (pw + w, min(plo, lo), max(phi, hi))
        else:
            out[d] = (w, lo, hi)
    return [(k, w, lo, hi) for k, (w, lo, hi) in out.items()]


for _area, _by_terrain in UNDERTIDE_TABLES.items():
    for _terrain, _tab in _by_terrain.items():
        for (_k, _w, _lo, _hi) in _tab + _ut_day(_tab):
            EXTRA_ENCOUNTERS.setdefault(_UT_SLUG[_k], []).append(
                {"area": _area, "terrain": _terrain, "rarity": _ut_rarity(_w), "min": _lo, "max": _hi})

# ---- Lane N2 (walkthrough/11 Part B): THE DROWNLIGHT — MIRROR of
# tools/maps/build_drownlight_tower.py TABLES (the map is the truth; keep both in
# step). Cave = rect-wide in the tower's rooms. Ids, not slugs: #178-#180 are lane
# N4's Hollowing family, resolved by position in selected.json (dex id = index + 1)
# so this block never hard-codes another lane's names; an id not yet in the
# roster is skipped. Weights -> rarity as the Undertide's (_ut_rarity).
DROWNLIGHT_TABLES = {
    "drownlight_f1": [(179, 28, 50, 52), (138, 24, 50, 51), (180, 18, 51, 52),
                      (85, 16, 51, 52), (135, 14, 50, 52)],
    "drownlight_f2": [(138, 20, 51, 53), (135, 8, 52, 53), (87, 14, 51, 53),
                      (85, 12, 51, 53), (179, 28, 51, 53), (180, 18, 51, 53)],
}
with open(SEL) as _fh:
    _DL_SLUG = {i + 1: re.sub(r"[^a-z0-9]+", "_", c["name"].lower()).strip("_")
                for i, c in enumerate(json.load(_fh))}
for _area, _tab in DROWNLIGHT_TABLES.items():
    for (_k, _w, _lo, _hi) in _tab:
        if _k in _DL_SLUG:
            EXTRA_ENCOUNTERS.setdefault(_DL_SLUG[_k], []).append(
                {"area": _area, "terrain": "cave", "rarity": _ut_rarity(_w), "min": _lo, "max": _hi})
# The tower's FOOT (drownlight_beacon's blight-tuft beds) — MIRROR of
# tools/maps/build_drownlight_beacon.py TABLE_BEACON. Final forms only at band.
DROWNLIGHT_BEACON_TABLE = [(138, 34, 49, 50), (179, 28, 48, 50), (180, 24, 48, 49), (135, 9, 49, 50)]
for (_k, _w, _lo, _hi) in DROWNLIGHT_BEACON_TABLE:
    if _k in _DL_SLUG:
        EXTRA_ENCOUNTERS.setdefault(_DL_SLUG[_k], []).append(
            {"area": "drownlight_beacon", "terrain": "tall_grass", "rarity": _ut_rarity(_w), "min": _lo, "max": _hi})

# Areas whose encounter tables are BUILT into the map JSONs (the in-map zones
# are the truth, mirrored above). Generated region defaults — and stale rows
# carried in the previous per-species files — must not claim these areas:
# only EXTRA_ENCOUNTERS rows may. (North is the first fully-built region; its
# default "galehigh_terraces" band rows predated the maps.)
CURATED_AREAS = {
    # the Old Light's seven floors (R10, 2026-10): the halls' tower tables are the
    # truth (build_pearlmoor_oldlight.py), mirrored via OLDLIGHT_TABLES below
    "pearlmoor_oldlight_1", "pearlmoor_oldlight_2", "pearlmoor_oldlight_3",
    "pearlmoor_oldlight_4", "pearlmoor_oldlight_5", "pearlmoor_oldlight_6",
    "pearlmoor_oldlight_top",
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
    # the day-form pass (R4, 2026-06): the remaining relit outdoor maps with
    # built in-map tables, first fully mirrored above (night + day rows).
    "tinderwick", "gullcry_rock", "pearlmoor_quay",
    "saltreach_fen_i", "saltreach_fen_ii", "sunkbell_shallows",
    # the dex-obtainability pass (D1, 2026-06): the cinderhead chain + the
    # grotto carried built tables that predated the mirror convention (now
    # mirrored above), and the Spire's F2 gained the Skyweavelet bed.
    "spore_grotto", "cinderhead_mine", "cinderhead_deep",
    "cinderhead_deep_b1f", "cinderhead_deep_b2f", "umbral_spire_f2",
    # S5 (2026-10): Paul's wood above Pearlmoor (mirrored above, WANDERWOOD).
    "pearlmoor_wanderwood", "pearlmoor_wanderwood_far",
    # R8 (2026-10): Tinderwick's west orchard (mirrored above, ORCHARD_ENCOUNTERS).
    "duskapple_orchard",
    # the 2026-10 geometry fix's new routes (mirrored above, GEOMETRY_ENCOUNTERS)
    "cinderwind_scarp", "umbral_approach",
    # Lane A (walkthrough/10 Part II): the Ashfall Shelf + Kiln Gully (mirrored above)
    "cinderwind_ashfall", "cinderwind_kiln",
    # The Wild Ways — Sunvault Climb rebuild (S): the two new face maps
    "sunvault_climb_iii", "sunvault_climb_iv",
    # The Wild Ways — the Rimeway (C)
    "rimeway_ascent", "rimeway_fold", "rimeway_descent",
    # THE WILD WAYS — the Wick-Run (mirrored above, WICKRUN_ENCOUNTERS); the
    # crest and the foot are encounter-free and listed so nothing claims them.
    "wickrun_crest", "wickrun_chute", "wickrun_trestles", "wickrun_traverse",
    "wickrun_lower", "wickrun_foot",
    # THE WILD WAYS — the Old Seams (D): three cave floors (mirrored above,
    # OLD_SEAMS_TABLES); the heart is encounter-free by design (Emberroot's room).
    "old_seams_i", "old_seams_ii", "old_seams_iii", "emberroot_heart",
    # THE WILD WAYS — the Mirelights (mirrored above, MIRELIGHT_ENCOUNTERS);
    # the hollow is the legendary's room, listed so nothing generated claims it
    "mirelight_landing", "mirelight_glassmere", "mirelight_chapel", "lanthorne_hollow",
    # THE FARLAMP ISLES — the surface (Lane C1; mirrored above, FARLAMP_TABLES);
    # Driftholm is a town (no encounters), listed so nothing generated claims it
    "farlamp_sound", "farlamp_shelfwater", "farlamp_fogwall", "farlamp_gullwrack",
    "farlamp_kelpcrown", "driftholm",
    # Lane C2 — the Farlamp Isles' Undertide (mirrored above, UNDERTIDE_TABLES); the
    # Drowned Lamp is Farlume's room, encounter-free, listed so nothing claims it.
    "undertide_i", "undertide_ii", "undertide_iii", "undertide_iv", "farlamp_drowned",
    # Lane N2 — the Drownlight (mirrored above, DROWNLIGHT_TABLES); the lantern room
    # is the Shutterkeeper's, encounter-free, listed so nothing generated claims it.
    "drownlight_f1", "drownlight_f2", "drownlight_lantern",
}

# The Old Light's hall tables (R10) — MIRROR of build_pearlmoor_oldlight.py's
# `encounters(...)` rows (the map is the truth): floor -> (slug, weight, lo, hi).
# Weight -> rarity as everywhere: >=30 common, >=15 uncommon, else rare.
OLDLIGHT_TABLES = {
    1: [("glimflit", 30, 9, 11), ("the_smiler", 35, 9, 11), ("wickmoth", 20, 9, 11), ("riddlestone", 15, 10, 11)],
    2: [("the_smiler", 25, 10, 12), ("jesterhalf", 30, 10, 12), ("glimflit", 20, 10, 12), ("spirlet", 15, 10, 12), ("lumpin", 10, 11, 12)],
    3: [("snoozlet", 40, 10, 12), ("jesterhalf", 30, 10, 12), ("spirlet", 30, 11, 12)],
    4: [("jesterhalf", 30, 11, 13), ("riddlestone", 25, 11, 13), ("spirlet", 25, 11, 13), ("mcclownface", 20, 12, 13)],
    5: [("mcclownface", 25, 12, 14), ("jesterhalf", 25, 12, 14), ("riddlestone", 25, 12, 14), ("the_smiler", 25, 13, 14)],
    6: [("spirlet", 50, 13, 14), ("snoozlet", 30, 13, 14), ("mcclownface", 20, 13, 14)],
}
for _floor, _rows_ in OLDLIGHT_TABLES.items():
    for _slug, _w, _lo, _hi in _rows_:
        EXTRA_ENCOUNTERS.setdefault(_slug, []).append({
            "area": f"pearlmoor_oldlight_{_floor}", "terrain": "cave",
            "rarity": "common" if _w >= 30 else "uncommon" if _w >= 15 else "rare",
            "min": _lo, "max": _hi})

# THE FARLAMP ISLES (walkthrough/10 Part I, Lane C1) — MIRROR of the surface maps'
# zone tables (tools/maps/build_farlamp_isles.py TABLES — the map is the truth):
# area -> [(slug, weight, lo, hi, terrain)]. The deep (rowed) and the shallows
# both read as "water" in the dex; the isles' tall sea-grass is "tall_grass".
FARLAMP_TABLES = {
    # pass 2: +4 levels (the player crosses at L69+); the isles' family is met
    # KINDLED (fathomere/beaconclaw common), the base forms are the rare finds
    "farlamp_sound": [
        ("fathomere", 35, 62, 65, "water"), ("beaconclaw", 15, 62, 64, "water"),
        ("brinewrath", 15, 63, 65, "water"), ("tidwraith", 12, 62, 65, "water"),
        ("glostrael", 8, 63, 65, "water"), ("fathomote", 5, 62, 63, "water"),
        ("hermiwick", 5, 62, 63, "water"),
        ("lumplass", 30, 62, 64, "water"), ("tidalarch", 30, 62, 64, "water"),
        ("beaconclaw", 40, 62, 64, "tall_grass"), ("frigalance", 25, 62, 65, "tall_grass"),
        ("voltcrag", 25, 62, 64, "tall_grass"), ("glacewing", 5, 62, 63, "tall_grass"),
        ("hermiwick", 5, 62, 63, "tall_grass")],
    "farlamp_shelfwater": [
        ("fathomere", 35, 63, 66, "water"), ("beaconclaw", 15, 63, 65, "water"),
        ("tidalarch", 15, 64, 66, "water"), ("lumplass", 15, 63, 66, "water"),
        ("brinewrath", 10, 64, 66, "water"), ("fathomote", 5, 63, 64, "water"),
        ("hermiwick", 5, 63, 64, "water")],
    "farlamp_fogwall": [
        ("fogwisp", 35, 64, 67, "water"), ("fathomere", 25, 64, 66, "water"),
        ("stillwarden", 15, 65, 67, "water"), ("glacitern", 10, 64, 67, "water"),
        ("tidwraith", 10, 64, 66, "water"), ("fathomote", 5, 64, 65, "water")],
    "farlamp_gullwrack": [
        ("beaconclaw", 30, 64, 66, "tall_grass"), ("frigalance", 20, 64, 66, "tall_grass"),
        ("vaultclaw", 15, 64, 66, "tall_grass"), ("lithonyx", 15, 64, 66, "tall_grass"),
        ("voltcrag", 15, 65, 66, "tall_grass"), ("hermiwick", 5, 64, 65, "tall_grass"),
        ("fathomere", 40, 64, 66, "water"), ("brinewrath", 30, 64, 66, "water"),
        ("tidalarch", 22, 64, 66, "water"), ("glostrael", 8, 65, 66, "water"),
        ("fathomote", 5, 64, 65, "water")],
    "farlamp_kelpcrown": [
        ("beaconclaw", 25, 64, 67, "tall_grass"), ("tidalarch", 20, 64, 66, "tall_grass"),
        ("rootwarden", 15, 65, 67, "tall_grass"), ("ferrolith", 15, 64, 66, "tall_grass"),
        ("prismara", 15, 64, 66, "tall_grass"), ("hermiwick", 10, 64, 65, "tall_grass"),
        ("fathomere", 35, 64, 66, "water"), ("lumplass", 35, 64, 66, "water"),
        ("tidalarch", 25, 64, 66, "water"), ("fathomote", 5, 64, 65, "water")],
}


for _area, _rows_ in FARLAMP_TABLES.items():
    _seen = set()
    for _slug, _w, _lo, _hi, _terr in _rows_:
        if (_slug, _terr) in _seen:      # one dex row per kin per terrain
            continue
        _seen.add((_slug, _terr))
        EXTRA_ENCOUNTERS.setdefault(_slug, []).append({
            "area": _area, "terrain": _terr,
            "rarity": "common" if _w >= 30 else "uncommon" if _w >= 15 else "rare",
            "min": _lo, "max": _hi})

# ---- Lane E (walkthrough/10 Part III): Lowtinder & Tinderwick Bay -----------------
# MIRROR of the built in-map zone tables (build_tinderwick_bay.py, build_lowtinder.py,
# build_lowtinder_cellar.py, build_lowtinder_interiors.py — the maps are the truth):
# (area, terrain, [(slug, weight, lo, hi)]). Embrift (#14) and Mossmantle (#39) are
# wild here and nowhere else; the reef is the post-game deep (rowed, `deep`).
# Every row sits at or under its kin's kindle level (review 2026-10: the base
# forms that kindle at 13-15 were swapped for their kindled forms).
LOWTINDER_TABLES = [
    ("tinderwick_bay", "water", [("brineroll", 35, 17, 19), ("shimmral", 30, 17, 19), ("lumpin", 25, 18, 20), ("tidmaren", 6, 19, 20)]),
    ("tinderwick_bay", "tall_grass", [("lumpin", 40, 17, 19), ("brineroll", 30, 17, 18), ("shimmral", 20, 18, 19), ("tallowcrest", 10, 18, 19)]),
    ("tinderwick_bay", "deep", [("brinewrath", 28, 58, 61), ("prismare", 20, 58, 61), ("tidwraith", 20, 58, 61), ("fathomere", 15, 58, 60), ("beaconclaw", 12, 58, 60), ("tideveil", 5, 60, 62)]),
    ("lowtinder", "tall_grass", [("tallowcrest", 30, 18, 20), ("coalump", 25, 18, 20), ("tidmaren", 20, 18, 20), ("wickmoth", 15, 17, 18), ("embrift", 7, 20, 21)]),
    ("lowtinder", "water", [("brineroll", 35, 18, 20), ("tidmaren", 30, 18, 20), ("shimmral", 25, 18, 20), ("embrift", 5, 20, 21)]),
    ("lowtinder_cellar", "cave", [("tidmaren", 30, 19, 21), ("coalump", 25, 19, 22), ("tallowcrest", 20, 20, 22), ("lumpin", 18, 20, 22), ("embrift", 5, 21, 22)]),
    ("lowtinder_cellar_b2", "cave", [("coalump", 25, 20, 23), ("tallowcrest", 25, 20, 23), ("lumpin", 20, 21, 22), ("brineroll", 20, 21, 23), ("embrift", 8, 22, 23)]),
    ("lowtinder_school_garden", "tall_grass", [("mossmantle", 40, 24, 27), ("wickmere", 35, 24, 26), ("tidmaren", 25, 24, 26)]),
]
for _area, _terrain, _rows_ in LOWTINDER_TABLES:
    for _slug, _w, _lo, _hi in _rows_:
        EXTRA_ENCOUNTERS.setdefault(_slug, []).append({
            "area": _area, "terrain": _terrain,
            "rarity": _mire_rarity(_w), "min": _lo, "max": _hi})
CURATED_AREAS |= {"tinderwick_bay", "lowtinder", "lowtinder_cellar", "lowtinder_cellar_b2",
                  "lowtinder_school_garden", "lowtinder_lamphouse", "lowtinder_school"}

# ---- Lane N3 (walkthrough/11 Parts C + D): the Mourning Fields + the Penumbra Underways
# MIRROR of the built in-map tables (build_mourning_fields.py NIGHT/DAY,
# build_penumbra_underways.py F1_/B1_ tables — the maps are the truth):
# (area, terrain, [(kin_id, weight, lo, hi)]). The Fields' day rows are the post-dawn
# twins. The Hollowing family (#178-#180, Lane N4) joins the Fields' night table only
# once its species exist (the builder applies the same rule).
MOURNING_TABLES = [
    ("mourning_fields", "tall_grass", [(138, 22, 49, 51), (113, 18, 48, 50), (85, 16, 49, 51),
                                       (125, 14, 48, 50), (58, 12, 49, 51), (142, 10, 50, 52),
                                       (135, 6, 51, 52), (180, 14, 48, 51), (179, 8, 50, 52)]),
    # the north mouth's verge: the deliberately LOW Dousecap bed (it kindles at 44)
    ("mourning_fields", "tall_grass", [(178, 60, 42, 44), (180, 25, 46, 48), (179, 15, 47, 49)]),
    ("mourning_fields", "tall_grass", [(127, 22, 56, 61), (58, 18, 56, 61), (125, 16, 57, 62),
                                       (107, 14, 57, 62), (140, 14, 56, 61), (9, 10, 57, 62),
                                       (129, 6, 60, 62)]),
    # the Underways (build_penumbra_underways.py): night tables, then the post-dawn
    # `_day` twins; B1's warm-stones pocket is the only pre-dawn Embralux (#33) ground,
    # and (FD2, 2026-10-14) the ONLY wild JesterFull (#168, Light/Dark) anywhere
    ("penumbra_underways", "cave", [(138, 24, 52, 54), (113, 18, 52, 54), (143, 16, 52, 54),
                                    (15, 14, 53, 55), (85, 14, 53, 55), (135, 14, 53, 55)]),
    ("penumbra_underways", "tall_grass", [(127, 30, 52, 54), (135, 25, 53, 55), (107, 20, 53, 55),
                                          (40, 15, 53, 55), (140, 10, 54, 55)]),
    ("penumbra_underways", "cave", [(135, 26, 56, 59), (107, 22, 56, 59), (140, 20, 56, 59),
                                    (85, 18, 56, 59), (37, 14, 57, 59)]),
    ("penumbra_underways", "tall_grass", [(40, 32, 56, 59), (127, 28, 56, 59), (37, 24, 57, 59),
                                          (129, 16, 58, 59)]),
    ("penumbra_underways_b1", "cave", [(135, 24, 54, 56), (138, 22, 54, 56), (113, 16, 54, 56),
                                       (142, 14, 54, 56), (143, 14, 54, 56), (144, 6, 55, 56)]),
    ("penumbra_underways_b1", "tall_grass", [(40, 26, 54, 56), (107, 22, 54, 56), (127, 20, 54, 56),
                                             (37, 14, 55, 56), (135, 12, 54, 56), (129, 6, 56, 56)]),
    ("penumbra_underways_b1", "tall_grass", [(179, 34, 54, 56), (180, 24, 54, 56), (40, 20, 54, 56),
                                             (135, 14, 54, 56), (33, 8, 55, 56), (168, 6, 55, 56)]),
    ("penumbra_underways_b1", "cave", [(135, 28, 57, 60), (140, 24, 57, 60), (37, 22, 57, 60),
                                       (107, 20, 57, 60), (33, 6, 59, 60)]),
    ("penumbra_underways_b1", "tall_grass", [(40, 34, 57, 60), (37, 26, 57, 60), (127, 24, 57, 60),
                                             (129, 16, 58, 60)]),
    ("penumbra_underways_b1", "tall_grass", [(33, 30, 57, 60), (179, 30, 57, 60), (37, 22, 57, 60),
                                             (40, 18, 57, 60), (168, 6, 58, 60)]),
]


def _slug_of(kid):
    import glob as _glob
    hits = sorted(_glob.glob(os.path.join(ROOT, "src/game/data/species", f"{kid:03d}_*.json")))
    return os.path.basename(hits[0])[4:-5] if hits else None


for _area, _terrain, _rows_ in MOURNING_TABLES:
    for _kid, _w, _lo, _hi in _rows_:
        _slug = _slug_of(_kid)
        if _slug is None:          # a Lane N4 kin not merged yet
            continue
        EXTRA_ENCOUNTERS.setdefault(_slug, []).append({
            "area": _area, "terrain": _terrain,
            "rarity": _mire_rarity(_w), "min": _lo, "max": _hi})
CURATED_AREAS |= {"mourning_fields", "penumbra_underways", "penumbra_underways_b1"}
# ---- Lane N1 (walkthrough/11 Part A): Stillwater, the Hollowing's village -----------
# MIRROR of build_stillwater.py's in-map tables (the map is the truth): the grey-meadow
# beds (night 48-52 -> their day twins at flag:dawn) and the lampmaker's yard (the
# young snuffer-caps, #178 kept at/below its lv-44 kindling). Keyed by DEX ID because
# #178-#180 are Lane N4's: the slug resolves from selected.json, and an id not yet in
# the roster is skipped (no row lost once it lands — re-run this builder then).
STILLWATER_TABLES = [
    ("stillwater", [(180, 28, 48, 51), (179, 20, 49, 52), (138, 20, 48, 50), (113, 18, 50, 52),
                    (135, 14, 50, 52)]),
    ("stillwater", [(179, 24, 56, 60), (180, 22, 55, 59), (140, 22, 58, 62), (135, 18, 55, 60),
                    (142, 14, 56, 61)]),                                   # day (flag:dawn)
    ("stillwater", [(178, 70, 42, 44), (180, 30, 46, 48)]),                # the yard, night
    ("stillwater", [(178, 50, 42, 44), (179, 30, 55, 58), (140, 20, 55, 58)]),  # the yard, day
    # Coldfog I/II (2026-10 Part A review: kindled forms at 46+; r2: the base-form
    # gold pocket is gone — Mothdim/Flutterwane moved to Glowmoss Deep, below). MIRROR
    # of the builders' TABLE_I/TABLE_GOLD/TABLE_II + hand_placed_data's day tables.
    ("coldfog_marches_i", [(138, 30, 46, 48), (135, 26, 46, 48), (113, 16, 47, 48),
                           (142, 14, 46, 48), (180, 14, 46, 48)]),
    ("coldfog_marches_i", [(135, 56, 46, 48), (138, 28, 46, 48), (140, 8, 47, 48),
                           (116, 8, 46, 48)]),                             # gold (+ Auravane)
    ("coldfog_marches_i", [(140, 26, 58, 65), (135, 26, 55, 62), (138, 16, 56, 62),
                           (142, 12, 56, 62), (180, 12, 55, 60), (113, 8, 56, 62)]),     # day
    ("coldfog_marches_i", [(140, 48, 59, 65), (135, 30, 56, 62), (138, 14, 56, 62),
                           (116, 8, 58, 63)]),                             # gold, day
    ("coldfog_marches_ii", [(138, 26, 48, 50), (135, 22, 48, 50), (142, 22, 48, 50),
                            (113, 14, 49, 50), (180, 16, 48, 50)]),
    ("coldfog_marches_ii", [(140, 24, 60, 65), (135, 24, 57, 64), (138, 18, 57, 63),
                            (142, 16, 58, 64), (113, 10, 57, 63), (180, 8, 57, 62)]),    # day
]
_SW_SLUG = {c["dex_id"]: re.sub(r"[^a-z0-9]+", "_", c["name"].lower()).strip("_")
            for c in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                                 "docs", "mechanics", "concepts", "selected.json")))
            if c.get("dex_id")}
for _area, _tab in STILLWATER_TABLES:
    for (_k, _w, _lo, _hi) in _tab:
        if _k not in _SW_SLUG:
            continue
        _row = {"area": _area, "terrain": "tall_grass", "rarity": _mire_rarity(_w),
                "min": _lo, "max": _hi}
        _have = EXTRA_ENCOUNTERS.setdefault(_SW_SLUG[_k], [])
        if _row not in _have:          # a bed that keeps its night table by day
            _have.append(_row)
# Glowmoss Deep's DRAINED chamber (build_glowmoss_deep.py `drained_woken`, cave,
# flag:met_hollowing): the young Hollowing-touched moths drift in to the relit
# null-lantern, under their kindling levels (Mothdim 20, Flutterwane 22). Their
# only wild bed. MIRROR of the builder's table (the map is the truth).
for _slug_, _rar_, _lo_, _hi_ in [("mothdim", "uncommon", 18, 19), ("flutterwane", "uncommon", 20, 21)]:
    EXTRA_ENCOUNTERS.setdefault(_slug_, []).append({
        "area": "glowmoss_deep", "terrain": "cave", "rarity": _rar_, "min": _lo_, "max": _hi_})
CURATED_AREAS |= {"stillwater", "stillwater_quiet_hall", "stillwater_shutter",
                  "stillwater_lampmaker", "stillwater_home_a", "stillwater_home_b"}

# Kin that are FIXED quest catches (a legendaryBattle set-piece), even though
# tier/rarity alone wouldn't mark them scripted. #148 Lampling is C1
# "Lampling's Trail" at the Vesper Crossroads — its old umbral_spire row was a
# stale open-table teaser from before the trail was built, dropped here.
SCRIPTED_KIN = {"lampling", "chickenpig", "gloampurr"}

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
    # #163 Chickenpig — the S4 "Booji-Wooji Man" epilogue catch (scripted at the
    # breakwater's dark lamp; SCRIPTED_KIN, no open-table rows). Stats are NOT
    # pinned (make_stats C-tier bruiser); creative fields + art are.
    "chickenpig": {
        "entry": "A barrel-round piglet with a rooster's comb, one proud red wing and a spray of green tail-sickles. Every waking it climbs somewhere high and crows at the dark, on the principle that something ought to. It has never once doubted the morning.",
        "category": "Dawn-Herald Kin",
        "size_cm": 70, "weight_kg": 28,
        "art": {
            "silhouette": "A stout, cheerful piglet standing four-square: big upright pig ears, round cream body, short trotters. A bright red rooster's comb crests its head; a single red-feathered wing folds over its shoulder; brown flight feathers tuck beneath a great backswept spray of teal-and-green sickle tail-feathers. Smiling snout, kind olive eyes. At 64px the silhouette is pig-with-rooster-tail, unmistakable.",
            "palette": "Warm cream hide; bright comb-red crest and rust-red wing patch; the tail a layered fan of deep teal, sea-green and one brown under-feather; pale bone snout; soft ink (#1a1430) outlines.",
            "direction": "Half farm-pig, half dawn-rooster, wholly convinced. Sturdy and funny but DIGNIFIED — it is not a joke to itself. The comb and tail-fan read proud, the smile patient: a creature that has decided morning is coming and is simply early.",
        },
    },
    # #164 Gloampurr — the Lunar/Solar dragon-cat of the optional East side quest
    # "The Sunniest House in the Dark" (Georgina's ace + the kitten she gifts).
    # SCRIPTED_KIN (no open-table rows). Stats PINNED (a fragile mirror-axis glass
    # cannon — high spa/spe, low bulk); ability/dex/art/learnset pinned too.
    # #169 The Smiler (R11, the Old Light's clowns): the generated "Utility /
    # Speedster" spread (47s + spe 79) sat at ~9% in the sim, the roster's floor.
    # Same 312 BST re-cut as a physical clapper (it claps its foes silly) with a
    # physical Light ladder from lv 1; best of the spreads probed (~12%, level
    # with the other mono-Light A-tier babies such as Glimflit).
    "the_smiler": {
        "stats": {"hp": 55, "atk": 62, "def": 50, "spa": 30, "spd": 45, "spe": 70},
        "levelup": [(1, "quick_jab"), (1, "glimmer"), (7, "dazzle_flash"),
                    (11, "lumen_cut"), (20, "radiant_strike")],
    },
    "gloampurr": {
        # (2026-10) spa 110->98, spe 88->84 (BST 418->402, inside the C band): it sat on the C-tier outlier line
        # (~61-65% vs the ~64.5% gate across seeds) before the R10 kin; this clears it at every seed tried.
        "stats": {"hp": 60, "atk": 50, "def": 55, "spa": 98, "spd": 55, "spe": 84},
        "ability": "daybringer", "hidden_ability": "nightsight",
        "entry": "A small winged cat the colour of a violet dusk, with a coal of warm gold burning low in its chest. It does not fear the dark — it curls up in the deepest of it and purrs until the gloom glows back, carrying its own little sunrise wherever the night is thickest.",
        "category": "Dusklight Cat Kin",
        "size_cm": 42, "weight_kg": 9,
        "levelup": [(1, "quick_jab"), (1, "dream_wisp"), (5, "glint_ray"),
                    (9, "swift_step"), (13, "moonbeam"), (18, "daybeam"),
                    (24, "bask"), (30, "eclipse_wave"), (36, "sunburst_nova")],
        "art": {
            "silhouette": "A small, lithe winged cat sitting upright on its haunches, dragon-touched: pointed feline ears, a slim cat's muzzle, large round eyes, four neat paws and a long tail that ends in a soft tuft. From its shoulders rise a pair of small membranous dragon wings, half-folded like a cloak; faint ridge-scales run the spine and tail. At 64px the silhouette reads cat-first, dragon-second — a kitten that grew wings.",
            "palette": "Deep violet-and-plum fur shading to near-black at the wingtips and tail; a warm gold star-glow on the chest, the inner wings and the eyes, like a held-back sunrise; pale lilac muzzle and paw-tips; soft ink (#1a1430) outlines. Purple is the body, gold is the light it carries.",
            "direction": "Sunshine in goth clothing. The pose is content and unbothered — a happy little creature wholly at home in the dark, head up, eyes warm, a small proud arch to the wings. Gothic-cosy, never spooky: it LIKES the night, and it brought a light.",
        },
    },
    # The Wild Ways legendaries (#165-166) — docs/world/walkthrough/09-the-wild-ways.md
    # §2B/§2D. The Three Hours' treatment: tier E, very_rare -> scripted (no
    # open-table rows; legendaryBattle set-pieces), stats NOT pinned
    # (make_stats(role, 558, name)), abilities/dex/kits/art pinned. Kits come
    # from the existing pool, no signature moves.
    "lanthorne": {
        # the Tide-E default is phoenix: wrong for a lamp that leads you home.
        # tidecaller = it mends in its own mere; mistveil = the false lights.
        "ability": "tidecaller", "hidden_ability": "mistveil",
        "entry": "The Mirelight — the fen's own lamp, which once walked the drowned causeway ahead of lost boats and brought them home. A null-lantern put it to sleep long ago; the blue lights that still wander the Glassmere are only its dreams, and dreams do not know the way.",
        "category": "Mirelight Kin",
        # as met at lv 45: tide_pulse / dazzle_flash / light_pulse / mend
        "levelup": [(1, "mist_spray"), (9, "spark_mote"), (16, "drench_song"),
                    (24, "tide_pulse"), (30, "dazzle_flash"), (37, "light_pulse"),
                    (42, "mend"), (50, "lightspire"), (56, "maelstrom")],
        "art": {
            "silhouette": "A long, gentle eel-like kin rising upright out of still water like a lantern on a pole: a slender sea-glass body coiling down into the mere, a soft fin-veil at the neck, and a head shaped like an old hooded lamp — a glass-paned hood around a calm face, one steady blue-white flame held inside it. Faint wisps of blue light drift off the tail like echoes. At 64px it reads as a lamp that is also a creature, rising out of dark water.",
            "palette": "Deep fen-teal and night-blue (#13205a) body shading to translucent sea-glass at the fins; the lantern-hood in tarnished brass and pale glass; the inner flame a cool blue-white (#9fe7ff), the brightest pixel; the echo-wisps a fainter, colder blue; soft ink (#1a1430) outlines.",
            "direction": "Eerie but tender — a guide, not a ghost. Calm, half-lidded eyes, head bowed as if looking for someone on the water. It should look like something that would wait all night at the edge of a marsh to walk you home, and has been made to forget how.",
        },
    },
    "emberroot": {
        # the Stone-E default is phoenix: wrong for the oldest, most patient
        # thing in the world. stonehide = the mountain grown round it;
        # cinderveil = the coal is its own breath.
        "ability": "stonehide", "hidden_ability": "cinderveil",
        "entry": "The first star that ever fell into Vesperholm, so long ago the mountain grew up around it. It has slept at the root of Cinderhead ever since, and the warm black cinder-coal the miners dig is only its breath, cooling very slowly in the stone.",
        "category": "First-Star Kin",
        # as met at lv 46: rock_hurl / stone_wall / pyre_slam / boulder_smash
        "levelup": [(1, "pebble_toss"), (9, "cinderclaw"), (16, "gritfist"),
                    (24, "flame_lash"), (30, "rock_hurl"), (36, "stone_wall"),
                    (41, "pyre_slam"), (46, "boulder_smash"), (54, "throes")],
        "art": {
            "silhouette": "A vast, ancient, low-slung beast half-made of the mountain: a broad tortoise-like body under a humped shell of dark basalt strata, heavy legs ending in root-like claws that spread into the rock. Deep cracks run across the shell and shoulders, each glowing a slow molten amber from within; at the crown of the shell a star-shaped core shows through the stone like a banked coal. A small heavy head with eyes like embers in a kiln-mouth. At 64px it reads as a glowing, cracked boulder that is breathing.",
            "palette": "Basalt charcoal and ink (#1a1430) stone with cool grey strata bands; glowing seams of ember amber (#ff8a3d) deepening to red at their edges; the star-core a pale gold-white, the brightest pixel; ash-grey dust on the root-claws.",
            "direction": "Ancient, patient, rooted — the oldest thing in the world, asleep, not angry. Its weight should be felt: grounded, enormous, slow. The glowing cracks are breath, not wounds; the star inside is still warm.",
        },
    },
    # #135 Liminalux (2026-10, with the Farlamp kin): its generated spread sat on
    # the D-tier outlier line (~82-84% vs the ~84.7% gate across seeds) and the
    # six appended kin reshuffled the sim's pairings enough to tip it over at the
    # CI seed. spa 112->100 (BST 498->486, inside the D band) clears it with margin.
    "liminalux": {
        "stats": {"hp": 99, "atk": 42, "def": 70, "spa": 100, "spd": 90, "spe": 85},
    },
    # ---- Lane B: the Farlamp Isles kin (#172-177) — docs/world/walkthrough/
    # 10-the-farlamp-isles.md §4. Post-game, met at lv 58+, so every kit is
    # pinned to climb past the generator's B-tier stop at lv 24 (a wild
    # Fathomote at 60 must not carry a lv-13 kit). Stats are NOT pinned
    # (make_stats on role/tier) unless the sim says otherwise. No signature
    # moves: the Wild Ways legendary pattern (#165-166) uses the shared pool.
    "fathomote": {
        "entry": "A lantern-fish fry no longer than a hand, with a little glowing lure on a stalk over its nose. Shoals of them drift under the Farlamp Isles at night like spilled stars, and the old keepers set small lamps by the water so the fry have something to swim towards.",
        "category": "Lantern-Fry Kin",
        # pinned (sim): the generated 350 spread ran ~41% vs a ~31% B mean and
        # pushed the B tier's floor kin over the gate; trimmed to 330
        "stats": {"hp": 48, "atk": 30, "def": 42, "spa": 80, "spd": 50, "spe": 80},
        # kindles at lv 40; met at 58+ knowing tide_pulse/focus_mind/light_pulse/swift_step
        "levelup": [(1, "quick_jab"), (1, "mist_spray"), (6, "spark_mote"), (10, "drench_song"),
                    (16, "tide_pulse"), (22, "focus_mind"), (28, "light_pulse"), (34, "swift_step")],
        "art": {
            "silhouette": "A tiny round-bodied lantern-fish fry seen side-on, swimming upright: a big head with huge round dark eyes, a small smiling underbite, stubby frilled pectoral fins and a short fanned tail. A thin curved stalk rises from its brow and ends in a round glowing lure-bulb held out in front of its face. At 64px it reads as a chubby baby fish carrying its own little lamp.",
            "palette": "Deep sea-blue body (#13205a) with a paler water-blue (#4fb4ff) belly and fin-frills; tiny diamond-cyan (#9fe7ff) freckle-spots along the flank; the lure-bulb a warm bone-gold (#f5f0e1) glow, the brightest pixel; soft ink (#1a1430) outlines.",
            "direction": "Wide-eyed, curious and brave in a small way: a baby that swims out into the dark because its own light says it can. Cute and round, never toothy. Must read as the same line as Fathomere: same lure-stalk, same blue, same spot row.",
        },
    },
    "fathomere": {
        "entry": "A grown lantern-fish whose lure lights a whole fathom of sea. Fishers lost in the Fogwall used to follow a Fathomere's glow down the buoy lanes, and Driftholm says it still swims the old route home every night, in case anyone is out there.",
        "category": "Lantern-Fish Kin",
        # met at 58+ knowing deepsurge/lightspire/mist_screen/maelstrom
        "levelup": [(1, "quick_jab"), (1, "mist_spray"), (6, "spark_mote"), (10, "drench_song"),
                    (16, "tide_pulse"), (22, "focus_mind"), (28, "light_pulse"), (34, "swift_step"),
                    (40, "deepsurge"), (46, "lightspire"), (52, "mist_screen"), (58, "maelstrom")],
        "art": {
            "silhouette": "A long, graceful deep-sea lantern-fish seen side-on: a sleek tapering body with a row of small glowing spots along each flank, broad ribbon-like fins that trail like a veil, large calm eyes and a gentle closed mouth. A tall arching lure-stalk curves forward over its head and ends in a bright glass-like lamp-bulb. At 64px it reads as an elegant fish carrying a lantern before it.",
            "palette": "Midnight body (#13205a deepening to #0b1026 along the back) with a water-blue (#4fb4ff) belly and translucent sea-blue fin-veils; the flank spot-row in diamond-cyan (#9fe7ff); the lure-bulb a warm bone-gold (#f5f0e1) lamp with a soft amber core, the brightest pixel; ink (#1a1430) outlines.",
            "direction": "Calm, steady, a guide: the fry grown up into the light it once swam towards. Elegant and deep, never menacing, no teeth showing. Same lure-stalk, same spot row and same blues as Fathomote, now long and graceful.",
        },
    },
    "hermiwick": {
        "entry": "A small hermit crab that has made its home in the broken glass of a drowned lamp. It polishes the cracked panes every morning and backs into them at the first sign of trouble. Driftholm children say every Hermiwick is looking for the lamp its glass came from.",
        "category": "Lamp-Glass Crab Kin",
        # pinned (sim): the generated 350 wall ran ~36% vs a ~31% B mean; 336
        "stats": {"hp": 64, "atk": 47, "def": 88, "spa": 25, "spd": 56, "spe": 56},
        # kindles at lv 42; met at 58+ knowing guard_up/rock_hurl/wave_crash/bulwark
        "levelup": [(1, "quick_jab"), (1, "pebble_toss"), (6, "brine_flick"), (10, "stone_wall"),
                    (14, "gritfist"), (19, "tidewhip"), (24, "guard_up"), (29, "rock_hurl"),
                    (35, "wave_crash"), (40, "bulwark")],
        "art": {
            "silhouette": "A small sturdy hermit crab, three-quarter view: a pebble-grey plated body, two mismatched claws (one big, one small), stalked eyes and short jointed legs. On its back, instead of a shell, it wears a little brass lantern housing with cracked, chipped glass panes and a dark unlit wick inside. At 64px it reads as a crab carrying a broken lantern as its home.",
            "palette": "Pebble-grey and slate shell-plates with sandy-cream undersides; coral-orange claw tips; the lantern housing in tarnished brass with pale sea-glass panes (#9fe7ff tint) showing white crack-lines; the wick dark and unlit; ink (#1a1430) outlines.",
            "direction": "Shy, stubborn and house-proud: a tiny keeper of a lamp that doesn't work yet. Plucky, never pitiful. The broken lantern-home is the whole design; Beaconclaw is the same crab with the same brass lantern made whole and lit.",
        },
    },
    "beaconclaw": {
        "entry": "When a Hermiwick finally finds a whole glass, it kindles into a Beaconclaw and the lamp on its back lights for the first time. It stands on the reef at the tide's edge and turns slowly all night, sweeping its beam across the water like a lighthouse with legs.",
        "category": "Lighthouse Crab Kin",
        # pinned (sim): the generated wall spread (atk 70) ran ~55% vs a ~66%
        # D mean; same 498, re-cut so the claw actually hits
        "stats": {"hp": 95, "atk": 95, "def": 120, "spa": 40, "spd": 80, "spe": 68},
        # Stone/Tide -> Stone/Light (the Exciter precedent). Met at 58+ knowing
        # radiant_strike/boulder_smash/dazzle_flash/prism_beam
        "ability": "lumenward", "hidden_ability": "stonehide",
        "levelup": [(1, "quick_jab"), (1, "pebble_toss"), (6, "brine_flick"), (10, "stone_wall"),
                    (14, "gritfist"), (19, "tidewhip"), (24, "guard_up"), (29, "rock_hurl"),
                    (35, "wave_crash"), (40, "bulwark"), (42, "radiant_strike"),
                    (47, "boulder_smash"), (53, "dazzle_flash"), (59, "prism_beam")],
        "art": {
            "silhouette": "A big armoured crab built like a small lighthouse, three-quarter view: a broad stone-plated body on thick jointed legs, one huge rounded claw raised like a shield, stalked eyes. On its back stands a tall, whole lantern tower: a brass lantern room with clean glass panes and a bright lamp shining inside, under a little conical roof, with soft beams of light fanning out. At 64px it reads as a crab wearing a lit lighthouse.",
            "palette": "Pebble-grey and slate shell-plates with sandy-cream undersides and coral-orange claw tips (Hermiwick's colours, bigger and bolder); the lantern room in polished brass with clear glass; the lamp a warm bone-gold (#f5f0e1) with a fire-amber (#ff8a3d) core, the brightest pixel; a white-and-red banded stripe on the tower base; ink (#1a1430) outlines.",
            "direction": "Proud, protective and patient: the little crab grown into a lighthouse. Solid and kind, a guardian of the reef. Same crab, same brass lantern as Hermiwick, now whole and lit.",
        },
    },
    "fogwisp": {
        "entry": "A moth made of sea-fog, drawn to lamps it can never reach. Where Fogwisps settle the air turns cold and grey, and lights seem farther away than they are. Driftholm keepers don't chase them off: a Fogwisp is only lonely, they say, and lonely things go where the light is.",
        "category": "Sea-Fog Moth Kin",
        # a disruptor: chill + fog + a dark/frost special ladder; met at 60+
        # knowing chill_mist/whiteout/mist_screen/gloomswell
        "levelup": [(1, "quick_jab"), (1, "snow_veil"), (7, "gloom_spit"), (12, "blight_touch"),
                    (18, "glacier_beam"), (24, "hollow_pulse"), (30, "focus_mind"),
                    (36, "chill_mist"), (42, "whiteout"), (48, "mist_screen"), (54, "gloomswell")],
        "art": {
            "silhouette": "A soft, round-bodied moth that seems made of fog, front view with wings spread: a fluffy pale body, big feathery antennae, two pairs of wide frayed wings whose edges dissolve into curling wisps of mist, and two large dark gentle eyes. Little curls of fog trail off the wingtips. At 64px it reads as a fluffy misty moth drifting in the dark.",
            "palette": "Fog-white and pale grey body and wings shading to a cool grey-violet; a faint frost-blue sheen (#9fe7ff) along the wing veins; dusky violet-grey eye-spots on the hind wings; the eyes deep night (#0b1026) with one bone (#f5f0e1) highlight each; ink (#1a1430) outlines kept soft.",
            "direction": "Eerie-cosy: quiet, wistful, soft as breath on a window. A little sad, never sinister, no fangs, no skulls.",
        },
    },
    "farlume": {
        # Tide-F default is phoenix: wrong for the keeper of a drowned light.
        # lumenward = the lamp it kept; tidecaller = the sea it waited in.
        "ability": "lumenward", "hidden_ability": "tidecaller",
        "entry": "The Farlamp's own keeper-kin, the light that lived inside Vesperholm's outermost sea-lamp. The night the deep came up it went down with the lamp and kept it burning on the sea floor as long as it could, then waited in the drowned tower for someone to bring the flame back.",
        "category": "Drowned Lamp Kin",
        # as met at lv 68 (set-piece): lightspire / mend / maelstrom / mist_screen
        "levelup": [(1, "mist_spray"), (9, "spark_mote"), (16, "drench_song"),
                    (24, "tide_pulse"), (32, "light_pulse"), (40, "deepsurge"),
                    (48, "focus_mind"), (56, "lightspire"), (60, "mend"),
                    (64, "maelstrom"), (68, "mist_screen"), (74, "dawnburst")],
        "art": {
            "silhouette": "A great, serene sea-serpent coiled upright around itself like the spiral stair of a lighthouse: a long body of deep sea-blue scales banded with pale stone-white rings, broad translucent fin-sails along its back, and a noble head crowned with a lantern room of brass and glass in which a steady flame burns. Light spills from the lantern down its coils. At 64px it reads as a living lighthouse coiled out of the sea.",
            "palette": "Deep sea-blue (#13205a) scales with water-blue (#4fb4ff) highlights and bone-white (#f5f0e1) stone bands; translucent diamond-cyan (#9fe7ff) fin-sails; the lantern crown in warm brass; the flame a white-gold, the brightest pixel; ink (#1a1430) outlines.",
            "direction": "Ancient, faithful and grieving, then hopeful: a keeper that never stopped tending its lamp. Majestic and gentle, calm eyes, the drowned light's guardian, never a monster.",
        },
    },
    # #147 Skyweavelet / #148 Lampling (2026-10, with the Hollowing kin): both
    # are pre-existing Light edge cases (~-16/-17pp from their tier means) and
    # three new Dark kin — Dark hits Light x2 — tipped them over the 18pp gate
    # at seeds 4/6/7. Minimal in-band trims, the Liminalux precedent:
    # Skyweavelet 350->368 (B band 320-375, same speedster shape), Lampling
    # same 418 with 8 spd moved into spa so its spark actually lands.
    "skyweavelet": {
        "stats": {"hp": 58, "atk": 50, "def": 55, "spa": 58, "spd": 55, "spe": 92},
    },
    "lampling": {
        "stats": {"hp": 84, "atk": 30, "def": 71, "spa": 67, "spd": 95, "spe": 71},
    },
    # ---- Lane N4: the Hollowing family (#178-180) — docs/world/walkthrough/
    # 11-the-hollowing-country.md §F. Late and optional: met wild at lv 46-56
    # in Stillwater, the Mourning Fields and Drownlight, so every kit is
    # pinned to climb past the generator's early stop (a wild lv-50 kin must
    # not carry a lv-20 kit). Stats trust make_stats unless the sim objects.
    # No signature moves (the shared pool, the Wild Ways pattern).
    "dousecap": {
        # a snuffer eats flame: Ember moves heal it; nullheart = nothing wakes it
        "ability": "cinderveil", "hidden_ability": "nullheart",
        "entry": "A little brass snuffer-cap of a kin that hops from wick to wick at bedtime and sits on each flame until it goes out. In Stillwater a Dousecap on the windowsill means the house has gone to sleep, and nobody minds the dark there.",
        "category": "Snuffer-Cap Kin",
        # kindles at lv 44; met at 46+ knowing hone/null_claw/flame_lash/blight_touch
        "levelup": [(1, "quick_jab"), (1, "shade_nip"), (6, "ember_jab"), (10, "scorch_veil"),
                    (15, "duskmaw"), (20, "cinderclaw"), (26, "hone"), (32, "null_claw"),
                    (38, "flame_lash"), (43, "blight_touch")],
        "art": {
            "silhouette": "A small round kin shaped like a candle-snuffer's bell cap, front three-quarter view: a tarnished-brass cone that is body and hat in one, its tip curling up into a tiny wisp of grey smoke, a soft charcoal-grey face peeping out from under the wide brim with two big sleepy half-closed eyes and a small content smile, and two stubby charcoal feet. A faint warm ember-glow shows under the rim where it last sat on a flame. At 64px it reads as a tiny sleepy brass cap on little legs.",
            "palette": "Tarnished brass cone (warm ochre-gold with darker umber shading and one pale highlight streak); charcoal-grey face and feet (#2a2633); the eyes deep night (#0b1026) with one bone (#f5f0e1) highlight each; a soft fire-amber (#ff8a3d) ember glow under the rim, the brightest pixel; the smoke-curl pale grey; ink (#1a1430) outlines.",
            "direction": "Drowsy, dutiful and sweet: a tidy little kin that puts the lights to bed. Cosy-melancholy, round and huggable, never spooky. Must read as the same line as Shutterwick: same brass snuffer-cap, same charcoal, same sleepy eyes.",
        },
    },
    "shutterwick": {
        "ability": "mirrorlight", "hidden_ability": "cinderveil",
        "entry": "When a Dousecap has put out a thousand flames it kindles into a Shutterwick, whose own lamp burns behind closed shutters in its chest. It keeps that light hidden and warm for the Hollowing, and opens a single slat only for someone lost in the dark.",
        "category": "Shuttered Lantern Kin",
        # kindled at 44; met at 50-56 knowing blight_touch/radiant_strike/
        # shadow_rend/bulwark (the shutters), later prism_beam
        "levelup": [(1, "quick_jab"), (1, "shade_nip"), (6, "ember_jab"), (10, "scorch_veil"),
                    (15, "duskmaw"), (20, "cinderclaw"), (26, "hone"), (32, "null_claw"),
                    (38, "flame_lash"), (43, "blight_touch"), (44, "radiant_strike"),
                    (49, "shadow_rend"), (54, "bulwark"), (60, "prism_beam")],
        "art": {
            "silhouette": "A tall, gentle lantern-keeper kin, front three-quarter view, with a broad bell-shaped silhouette that widens to the ground: a body of soft charcoal-grey cloth like a long quilted cloak, and set into its chest a BIG square brass lantern whose four little wooden shutters are closed, with bright lines of warm gold light leaking out between the slats and spilling down the cloak. On its head sits a wide brass snuffer-cap with a little ring-handle on top. Under the brim its round charcoal face is clearly visible, the same face as Dousecap: large calm half-lidded eyes with a bone-white highlight and a small, kind, sad smile. Two long sleeves fold in front, cupping the lantern. At 64px it reads as a gentle keeper carrying a shuttered lamp inside itself.",
            "palette": "Charcoal-grey cloak (#2a2633 with slate-violet folds); tarnished brass snuffer-cap and lantern frame (warm ochre-gold, umber shading); dark wood shutters; the light leaking through the slats a warm bone-gold (#f5f0e1) with a fire-amber (#ff8a3d) core, the brightest pixels; the eyes pale moon-white; ink (#1a1430) outlines.",
            "direction": "Quiet, protective and sad-eyed: it believes the light is safest hidden. Tall and dignified but kind and round-faced, a keeper not a phantom: a visible soft face with real eyes, NOT a dark void with glowing dot eyes, never menacing, no teeth. Same brass snuffer-cap and charcoal as Dousecap, grown up; the leaking lantern-light is its signature.",
        },
    },
    "lullwing": {
        # dream-dust dims the foe's aim; nightsight = a night-flyer
        "ability": "mistveil", "hidden_ability": "nightsight",
        "entry": "A grey moth that drifts over sleeping kin and fans their dreams with dusty wings, so they sleep on and on. The Hollowing call it a mercy. In Stillwater the Lullwings settle on every hearth-warm heap of dozing kin and hum to them until a morning that never comes.",
        "category": "Dream-Moth Kin",
        # met at 46-51 knowing moonbeam/mend/lull/gloomswell; 52+ trades
        # moonbeam for moonflood
        "levelup": [(1, "quick_jab"), (1, "gloom_spit"), (6, "dream_wisp"), (12, "veil_up"),
                    (18, "hollow_pulse"), (24, "moonbeam"), (36, "mend"), (41, "lull"),
                    (46, "gloomswell"), (52, "moonflood")],
        "art": {
            "silhouette": "A soft, plump moth seen from the front with its wings spread: a round furry body, feathery drooping antennae, big heavy-lidded sleepy eyes, tiny tucked legs, and broad rounded wings patterned with pale crescent-moon eye-spots. A gentle haze of silver dream-dust sifts down from the wing edges in little sparkles. At 64px it reads as a sleepy grey moth scattering moon-dust.",
            "palette": "Dove-grey furry body and wings shading to dusk-lilac (#6b5a8e) at the wing edges; pale moon-silver (#d8d4ec) crescent eye-spots; the dream-dust silver-white specks; the eyes deep night (#0b1026), half-lidded, one bone (#f5f0e1) highlight each; ink (#1a1430) outlines kept soft.",
            "direction": "Hushing, tender and a little lonely: it only wants everyone to rest. Soft, round and drowsy, a lullaby with wings, never sinister, no skulls, no fangs. Distinct from the sea-fog moth (Fogwisp): warmer grey-lilac, rounder, moon-marked, sleepy.",
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
