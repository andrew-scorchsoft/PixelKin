#!/usr/bin/env python3
"""Aggregate + validate the concept pool produced by the generation sub-agents.

Reads docs/mechanics/concepts/pool/batch-*.json, validates each concept against
the schema in docs/mechanics/08-data-schema.md (tolerantly, normalising where
safe), flags problems, detects duplicate names, checks kindling-line integrity,
and writes a combined docs/mechanics/concepts/pool/_all_concepts.json plus a
distribution report to stdout.
"""
import json, glob, os, sys, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POOL = os.path.join(ROOT, "docs", "mechanics", "concepts", "pool")

TYPES = {"Ember","Tide","Verdant","Stone","Storm","Frost","Solar","Lunar","Light","Dark"}
TIERS = set("ABCDEF")
RARITY = {"common","uncommon","rare","very_rare","legendary"}
REGION = {"south","east","north","west","outer","central","post"}
SHAPES = {"single","two-stage","three-stage"}

def main():
    files = sorted(glob.glob(os.path.join(POOL, "batch-*.json")))
    if not files:
        print("No batch files found in", POOL); sys.exit(1)

    concepts = []
    problems = []
    ids_by_batch = defaultdict(set)

    for fp in files:
        bname = os.path.basename(fp)
        try:
            with open(fp) as f:
                arr = json.load(f)
        except Exception as e:
            problems.append(f"{bname}: JSON parse error: {e}"); continue
        if not isinstance(arr, list):
            problems.append(f"{bname}: top-level is not a JSON array"); continue
        for i, c in enumerate(arr):
            tag = f"{bname}[{i}]"
            cid = c.get("concept_id")
            if not cid:
                problems.append(f"{tag}: missing concept_id"); cid = f"{bname}-{i}"
            ids_by_batch[bname].add(cid)
            # type checks
            ts = c.get("types") or []
            if isinstance(ts, str): ts = [ts]; c["types"] = ts
            if not ts or any(t not in TYPES for t in ts):
                problems.append(f"{tag} {c.get('name')}: bad types {ts}")
            if len(ts) > 2:
                problems.append(f"{tag} {c.get('name')}: >2 types {ts}")
            # tier
            tier = (c.get("tier") or "").strip().upper()[:1]
            if tier not in TIERS:
                problems.append(f"{tag} {c.get('name')}: bad tier {c.get('tier')}")
            else:
                c["tier"] = tier
            # rarity / region
            if c.get("rarity") not in RARITY:
                problems.append(f"{tag} {c.get('name')}: bad rarity {c.get('rarity')}")
            if c.get("region") not in REGION:
                problems.append(f"{tag} {c.get('name')}: bad region {c.get('region')}")
            # line
            line = c.get("line") or {}
            if line.get("shape") not in SHAPES:
                problems.append(f"{tag} {c.get('name')}: bad line.shape {line.get('shape')}")
            for fld in ("name","concept","visual","role"):
                if not c.get(fld):
                    problems.append(f"{tag}: missing {fld}")
            c["_batch"] = bname
            concepts.append(c)

    # duplicate names (case-insensitive)
    name_counts = Counter(c.get("name","").strip().lower() for c in concepts)
    dups = {n: ct for n, ct in name_counts.items() if n and ct > 1}

    # line integrity: kindles_into must resolve within same batch
    id_set = set(c.get("concept_id") for c in concepts)
    broken_links = []
    for c in concepts:
        nxt = (c.get("line") or {}).get("kindles_into")
        if nxt and nxt not in id_set:
            broken_links.append(f"{c.get('concept_id')} {c.get('name')} -> {nxt} (missing)")

    # write combined
    out = os.path.join(POOL, "_all_concepts.json")
    with open(out, "w") as f:
        json.dump(concepts, f, indent=1)

    # report
    print(f"=== CONCEPT POOL: {len(concepts)} concepts from {len(files)} batches ===\n")
    def dist(key, order=None):
        cc = Counter()
        for c in concepts:
            v = c.get(key)
            if key == "types":
                cc[c["types"][0]] += 1  # primary type
            else:
                cc[v] += 1
        keys = order or sorted(cc, key=lambda k: (-cc[k], str(k)))
        return "  ".join(f"{k}:{cc.get(k,0)}" for k in keys)

    print("Primary type:", dist("types", sorted(TYPES)))
    print("Tier:        ", dist("tier", list("ABCDEF")))
    print("Rarity:      ", dist("rarity", ["common","uncommon","rare","very_rare","legendary"]))
    print("Region:      ", dist("region", ["south","east","north","west","outer","central","post"]))
    print("Role:        ", dist("role"))
    # dual-type share
    dual = sum(1 for c in concepts if len(c.get("types",[]))==2)
    print(f"\nDual-typed:   {dual}/{len(concepts)} ({100*dual//max(1,len(concepts))}%)")

    print(f"\nDuplicate names: {len(dups)}")
    for n, ct in sorted(dups.items()):
        print(f"  '{n}' x{ct}")
    print(f"\nBroken kindling links: {len(broken_links)}")
    for b in broken_links[:30]:
        print("  ", b)
    print(f"\nValidation problems: {len(problems)}")
    for p in problems[:50]:
        print("  ", p)
    if len(problems) > 50:
        print(f"  ... and {len(problems)-50} more")

    print(f"\nWrote {out}")

if __name__ == "__main__":
    main()
