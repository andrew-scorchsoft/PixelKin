#!/usr/bin/env python3
"""Constrained 500 -> 151 selection (docs/mechanics/07-selection-process.md).

Reads the aggregated concept pool + any panel score files, groups concepts into
whole kindling LINES, then selects 151 dex slots subject to hard constraints:
primary-type quotas, whole lines only, and required fixed slots (the two
existing starters' finals, a Verdant starter, the 8 Constellation Wardens, the
legendaries, the mascot). Within constraints it maximises panel score.

Outputs:
  docs/mechanics/concepts/selected.json        (the 151 chosen, with dex_id)
  docs/mechanics/concepts/archive/cut-concepts.json
  docs/mechanics/selection-report.md
"""
import json, os, glob, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CDIR = os.path.join(ROOT, "docs", "mechanics", "concepts")
POOL = os.path.join(CDIR, "pool")
ARCH = os.path.join(CDIR, "archive")
os.makedirs(ARCH, exist_ok=True)

TYPES = ["Ember","Tide","Verdant","Stone","Storm","Frost","Solar","Lunar","Light","Dark"]
QUOTA = {"Verdant":17,"Storm":17,"Ember":16,"Tide":16,"Stone":16,"Frost":15,"Light":15,"Solar":13,"Lunar":13,"Dark":13}
assert sum(QUOTA.values()) == 151
# region ordering for eventual dex numbering
REGION_ORDER = {"south":0,"east":1,"north":2,"west":3,"outer":4,"central":5,"post":6}
TYPE_SCORE = {"Ember":5,"Tide":5,"Verdant":-5,"Stone":15,"Storm":5,"Frost":5,"Solar":25,"Lunar":10,"Light":-10,"Dark":10}

def load_concepts():
    p = os.path.join(POOL, "_all_concepts.json")
    if not os.path.exists(p):
        raise SystemExit("Run aggregate_pool.py first (missing _all_concepts.json)")
    return json.load(open(p))

def load_panel():
    scores = defaultdict(list)
    for fp in glob.glob(os.path.join(POOL, "_scores_*.json")):
        try:
            arr = json.load(open(fp))
        except Exception:
            continue
        for e in arr:
            cid = e.get("concept_id") or e.get("id")
            sc = e.get("score")
            if cid is not None and isinstance(sc, (int, float)):
                scores[cid].append(float(sc))
    return {cid: sum(v)/len(v) for cid, v in scores.items()}, len(glob.glob(os.path.join(POOL, "_scores_*.json")))

def heuristic(c):
    s = 55.0
    name = (c.get("name") or "")
    if re.fullmatch(r"[A-Za-z'\-]{4,13}", name): s += 4
    if " " not in name: s += 2
    if len(c.get("types", [])) == 2: s += 3            # dual-typing enriches matchups
    if c.get("signature_idea"): s += 3
    if len(c.get("hook", "")) > 40: s += 3
    if len(c.get("visual", "")) > 40: s += 3
    if c.get("region") in REGION_ORDER: s += 2
    return min(100.0, s)

def build_lines(concepts):
    by_id = {c["concept_id"]: c for c in concepts}
    child = set()
    for c in concepts:
        nxt = (c.get("line") or {}).get("kindles_into")
        for t in ([nxt] if isinstance(nxt, str) else (nxt or [])):
            if t in by_id: child.add(t)
    lines = []
    seen = set()
    def chain(root):
        out, stack = [], [root["concept_id"]]
        local = set()
        while stack:
            cid = stack.pop(0)
            if cid in local or cid not in by_id: continue
            local.add(cid); out.append(by_id[cid])
            nxt = (by_id[cid].get("line") or {}).get("kindles_into")
            for t in ([nxt] if isinstance(nxt, str) else (nxt or [])):
                if t in by_id and t not in local: stack.append(t)
        return out
    for c in concepts:
        cid = c["concept_id"]
        if cid in child or cid in seen:  # not a root
            continue
        members = chain(c)
        for m in members: seen.add(m["concept_id"])
        lines.append(members)
    # any leftover (cycles / orphans) become singletons
    for c in concepts:
        if c["concept_id"] not in seen:
            lines.append([c]); seen.add(c["concept_id"])
    return lines

def tag_line(members, txt):
    blob = " ".join((m.get("concept","")+" "+m.get("hook","")+" "+m.get("name","")) for m in members).lower()
    tiers = [m.get("tier") for m in members]
    return {
        "warden": "constellation warden" in blob,
        "starter": "starter" in blob,
        "mascot": any(m.get("name","").lower()=="lampling" for m in members),
        "legendary": any(t=="F" for t in tiers) or any(m.get("rarity")=="legendary" for m in members),
        "apexE": "E" in tiers,
        "fromVulpyre": "vulpyre" in blob,
        "fromBrinix": "brinix" in blob,
    }

def main():
    concepts = load_concepts()
    panel, npanels = load_panel()
    for c in concepts:
        h = heuristic(c)
        p = panel.get(c["concept_id"])
        c["_score"] = round(0.7*p + 0.3*h, 1) if p is not None else round(h, 1)
        c["_panel"] = p

    lines = build_lines(concepts)
    L = []
    for members in lines:
        members = sorted(members, key=lambda m: (m.get("line") or {}).get("stage", 1))
        root = members[0]
        ptype = root["types"][0]
        sc = sum(m["_score"] for m in members)/len(members)
        # completeness bonus: coherent multi-stage with climbing tiers
        bonus = 0
        if len(members) >= 2: bonus += 3
        tg = tag_line(members, "")
        L.append({"members": members, "ptype": ptype, "size": len(members),
                  "score": round(sc + bonus, 2), "tags": tg, "root": root,
                  "region": root.get("region","south")})

    chosen, used = [], Counter()
    chosen_ids = set()
    def take(line, why):
        if id(line) in chosen_ids: return
        chosen.append((line, why)); chosen_ids.add(id(line)); used[line["ptype"]] += line["size"]

    # 1) forced: existing starter finals (inject Vulpyre/Brinix as stage-1 members)
    VULPYRE = {"concept_id":"X-VULPYRE","name":"Vulpyre","types":["Ember"],"role":"Special Sweeper","tier":"B","region":"south","rarity":"common","line":{"shape":"two-stage","stage":1},"concept":"(existing starter)","visual":"(existing art)","_score":99,"existing":True}
    BRINIX  = {"concept_id":"X-BRINIX","name":"Brinix","types":["Tide"],"role":"Special Wall","tier":"B","region":"south","rarity":"common","line":{"shape":"two-stage","stage":1},"concept":"(existing starter)","visual":"(existing art)","_score":99,"existing":True}
    for line in L:
        if line["tags"]["fromVulpyre"] and not any(m.get("name","").lower()=="vulpyre" for m in line["members"]):
            line["members"] = [VULPYRE] + line["members"]; line["size"] = len(line["members"]); take(line, "Vulpyre line (existing starter #1)")
        if line["tags"]["fromBrinix"] and not any(m.get("name","").lower()=="brinix" for m in line["members"]):
            line["members"] = [BRINIX] + line["members"]; line["size"] = len(line["members"]); take(line, "Brinix line (existing starter #2)")

    # 2) mascot
    for line in sorted([l for l in L if l["tags"]["mascot"]], key=lambda l:-l["score"])[:1]:
        take(line, "Lampling mascot")
    # 3) one Verdant starter line (best 'starter' tagged Verdant)
    vs = sorted([l for l in L if l["tags"]["starter"] and l["ptype"]=="Verdant" and id(l) not in chosen_ids], key=lambda l:-l["score"])
    if vs: take(vs[0], "Verdant starter (dex #3)")
    # 4) 8 Constellation Wardens — best warden line per element
    for t in TYPES:
        if t in ("Light","Dark"): continue  # the 8 are the elemental constellations
        cand = sorted([l for l in L if l["tags"]["warden"] and l["ptype"]==t and id(l) not in chosen_ids], key=lambda l:-l["score"])
        if not cand:  # fallback: best apex-E of that type
            cand = sorted([l for l in L if l["tags"]["apexE"] and l["ptype"]==t and id(l) not in chosen_ids], key=lambda l:-l["score"])
        if cand: take(cand[0], f"{t} Constellation Warden")
    # 5) legendaries: best Light F (Keystar), best Dark F (Null), best post/F (Dawn)
    legL = sorted([l for l in L if l["tags"]["legendary"] and l["ptype"]=="Light" and id(l) not in chosen_ids], key=lambda l:-l["score"])
    if legL: take(legL[0], "Keylumen (Light legendary)")
    legD = sorted([l for l in L if l["tags"]["legendary"] and l["ptype"]=="Dark" and id(l) not in chosen_ids], key=lambda l:-l["score"])
    if legD: take(legD[0], "Null apex (Dark legendary)")
    legP = sorted([l for l in L if l["tags"]["legendary"] and l["region"]=="post" and id(l) not in chosen_ids], key=lambda l:-l["score"])
    if legP: take(legP[0], "Dawn legendary (post-game)")

    # 6) greedy fill per type quota by line score
    remaining = sorted([l for l in L if id(l) not in chosen_ids], key=lambda l:-l["score"])
    for t in sorted(TYPES, key=lambda t: QUOTA[t]):  # fill scarce types first
        for line in remaining:
            if id(line) in chosen_ids: continue
            if line["ptype"] != t: continue
            if used[t] + line["size"] <= QUOTA[t]:
                take(line, f"fill {t}")

    total = sum(used.values())

    # 7) balance to exactly 151
    def add_best():
        # add to the most-under-quota type
        deficits = sorted(TYPES, key=lambda t: (used[t]-QUOTA[t]))
        for t in deficits:
            for line in sorted([l for l in L if id(l) not in chosen_ids and l["ptype"]==t], key=lambda l:-l["score"]):
                if used[t] + line["size"] <= QUOTA[t] + 1:
                    take(line, f"balance-add {t}"); return True
        # last resort: any line that fits
        for line in sorted([l for l in L if id(l) not in chosen_ids], key=lambda l:-l["score"]):
            take(line, "balance-add any"); return True
        return False
    def remove_worst():
        # remove lowest-score non-forced line from most-over-quota type
        forced = {"Lampling mascot","Verdant starter (dex #3)"}
        surplus = sorted(TYPES, key=lambda t: -(used[t]-QUOTA[t]))
        for t in surplus:
            cand = [ (line,why) for (line,why) in chosen if line["ptype"]==t and not why.startswith(("Vulpyre","Brinix","Keylumen","Null","Dawn")) and "Warden" not in why and why not in forced]
            cand.sort(key=lambda x: x[0]["score"])
            if cand:
                line,why = cand[0]
                chosen.remove((line,why)); chosen_ids.discard(id(line)); used[line["ptype"]]-=line["size"]; return True
        return False

    guard = 0
    while sum(used.values()) != 151 and guard < 500:
        guard += 1
        if sum(used.values()) < 151:
            if not add_best(): break
        else:
            if not remove_worst(): break

    total = sum(used.values())

    # assemble selected concepts with provisional dex ordering (region, then tier, then line)
    sel_lines = sorted([line for (line,_) in chosen], key=lambda l: (REGION_ORDER.get(l["region"],9), l["root"].get("tier","D")))
    selected = []
    dex = 3  # 1=Vulpyre, 2=Brinix assigned within their lines below; counter advances
    # Place Vulpyre(#1)/Brinix(#2) lines first
    def line_has(line, nm): return any(m.get("name","").lower()==nm for m in line["members"])
    ordered = [l for l in sel_lines if line_has(l,"vulpyre")] + [l for l in sel_lines if line_has(l,"brinix")] + \
              [l for l in sel_lines if not (line_has(l,"vulpyre") or line_has(l,"brinix"))]
    dex_id = 1
    out_lines = []
    for line in ordered:
        ids_here = []
        for m in line["members"]:
            entry = dict(m)
            entry["dex_id"] = dex_id
            entry["line_primary_type"] = line["ptype"]
            ids_here.append(dex_id); dex_id += 1
            selected.append(entry)
        out_lines.append({"primary_type": line["ptype"], "region": line["region"],
                          "score": line["score"], "dex_ids": ids_here,
                          "names": [m["name"] for m in line["members"]]})

    chosen_concept_ids = set(e["concept_id"] for e in selected if not e.get("existing"))
    cut = [c for c in concepts if c["concept_id"] not in chosen_concept_ids]

    json.dump(selected, open(os.path.join(CDIR, "selected.json"), "w"), indent=1)
    json.dump(sorted(cut, key=lambda c:-c["_score"]), open(os.path.join(ARCH, "cut-concepts.json"), "w"), indent=1)

    # report
    rep = []
    rep.append("# PixelKin — Selection Report (500 → 151)\n")
    rep.append(f"- Concepts in pool: **{len(concepts)}**")
    rep.append(f"- Panel score files used: **{npanels}** (blended 70% panel / 30% heuristic; heuristic-only where a panel didn't score a concept)")
    rep.append(f"- Lines formed: **{len(L)}**  |  Lines selected: **{len(chosen)}**  |  Dex slots: **{len(selected)}**")
    rep.append(f"- Concepts archived (cut): **{len(cut)}** (see concepts/archive/cut-concepts.json)\n")
    rep.append("## Primary-type quota vs selected\n")
    rep.append("| Type | Quota | Selected | Δ |")
    rep.append("|------|------:|---------:|--:|")
    for t in TYPES:
        rep.append(f"| {t} | {QUOTA[t]} | {used[t]} | {used[t]-QUOTA[t]:+d} |")
    rep.append(f"| **Total** | **151** | **{sum(used.values())}** | {sum(used.values())-151:+d} |\n")
    # tier dist
    tc = Counter(e.get("tier") for e in selected)
    rep.append("## Tier distribution (selected)\n")
    rep.append("  ".join(f"{t}:{tc.get(t,0)}" for t in "ABCDEF"))
    rep.append("\n## Fixed slots\n")
    for (line,why) in chosen:
        if why.startswith(("Vulpyre","Brinix","Keylumen","Null","Dawn","Lampling","Verdant starter")) or "Warden" in why:
            rep.append(f"- **{why}** → {' → '.join(m['name'] for m in line['members'])}")
    rep.append("\n## All selected lines (by region, then tier)\n")
    cur = None
    for ol in sorted(out_lines, key=lambda o:(REGION_ORDER.get(o['region'],9), o['primary_type'])):
        if ol["region"] != cur:
            cur = ol["region"]; rep.append(f"\n### Region: {cur}\n")
        rep.append(f"- [{ol['primary_type']}] {' → '.join(ol['names'])}  (score {ol['score']}, dex {ol['dex_ids']})")
    open(os.path.join(ROOT, "docs", "mechanics", "selection-report.md"), "w").write("\n".join(rep))

    print(f"Selected {len(selected)} dex slots across {len(chosen)} lines.")
    print("Per-type:", {t: used[t] for t in TYPES}, "total", sum(used.values()))
    print("Tiers:", dict(tc))
    print(f"Cut/archived: {len(cut)} concepts")
    print("Wrote selected.json, archive/cut-concepts.json, selection-report.md")

if __name__ == "__main__":
    main()
