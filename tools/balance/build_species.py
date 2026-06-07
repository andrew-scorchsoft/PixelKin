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

def learnset(types, role, tier):
    phys = role in PHYS_ROLES or (role == "balanced / pivot")
    chan = "physical" if phys else "special"
    t0 = types[0]; t1 = types[1] if len(types) > 1 else None
    lv = []
    # L1: a plain quick + the primary quick
    lv.append((1, "quick_jab"))
    prim = DMG[t0][chan]
    if prim: lv.append((1, prim[0]["id"]))            # quick/light of primary
    # status flavour move of the type
    if STATUS.get(t0):
        lv.append((9, STATUS[t0][0]["id"]))
    # standard primary
    if len(prim) > 1: lv.append((13, prim[1]["id"]))
    # coverage from secondary type
    if t1 and DMG[t1][chan]:
        lv.append((19, DMG[t1][chan][1]["id"] if len(DMG[t1][chan]) > 1 else DMG[t1][chan][0]["id"]))
    # a self-buff utility
    lv.append((24, "hone" if phys else "focus_mind"))
    # heavy primary (mid/final tiers)
    if tier in ("C","D","E","F") and len(prim) > 2:
        lv.append((31, prim[2]["id"]))
    # nuke primary (final/apex/legend)
    if tier in ("D","E","F"):
        nuke = DMG[t0]["special"][-1] if DMG[t0]["special"] else (prim[-1] if prim else None)
        if nuke: lv.append((40, nuke["id"]))
    # legendary signature-ish: strongest off-channel STAB
    if tier in ("E","F"):
        alt = DMG[t0]["physical" if not phys else "special"]
        if alt: lv.append((48, alt[-1]["id"]))
    # dedupe + validate, keep order by level
    seen = set(); out = []
    for level, mid in sorted(lv, key=lambda x: x[0]):
        if mid in MOVE_IDS and mid not in seen:
            seen.add(mid); out.append({"level": level, "move": mid})
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
        scripted = e.get("rarity") in ("legendary",) or (tier in ("E","F") and e.get("rarity") == "very_rare")
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
        # apply canonical overrides for the two existing starters
        canon = CANON.get(rec["slug"])
        if canon:
            rec["stats"] = canon["stats"]; rec["bst"] = sum(canon["stats"].values())
            rec["ability"] = canon["ability"]; rec["hidden_ability"] = canon["hidden_ability"]
            rec["dex"]["entry"] = canon["entry"]; rec["dex"]["category"] = canon["category"]
            rec["dex"]["size_cm"] = canon["size_cm"]; rec["dex"]["weight_kg"] = canon["weight_kg"]
            sig = canon["signature"]
            if sig in MOVE_IDS and not any(e["move"] == sig for e in rec["learnset"]["levelup"]):
                rec["learnset"]["levelup"].insert(0, {"level": 1, "move": sig})
        out_all.append(rec)
        with open(os.path.join(OUTDIR, f"{e['dex_id']:03d}_{rec['slug']}.json"), "w") as f:
            json.dump(rec, f, indent=2)

    combined = {"_notes": "Generated by tools/balance/build_species.py from the panel-selected concepts. Mechanical fields are deterministic from role/tier/type; creative fields come from the selected concepts. Per-species files in src/game/data/species/.",
                "version": 1, "count": len(out_all), "species": out_all}
    json.dump(combined, open(os.path.join(ROOT, "src", "game", "data", "species.json"), "w"), indent=1)
    print(f"Built {len(out_all)} species -> src/game/data/species.json (+ per-species files)")
    # quick tier/type tally
    from collections import Counter
    print("Tiers:", dict(Counter(r["tier"] for r in out_all)))
    print("Types:", dict(Counter(r["types"][0] for r in out_all)))

if __name__ == "__main__":
    main()
