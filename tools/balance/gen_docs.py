#!/usr/bin/env python3
"""Generate a human-readable dex from src/game/data/species.json ->
docs/mechanics/dex.md (the full 151, grouped by region with kindling lines)."""
import json, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sp = json.load(open(os.path.join(ROOT, "src", "game", "data", "species.json")))["species"]
by_id = {s["id"]: s for s in sp}
REGION = ["south", "east", "north", "west", "outer", "central", "post"]
RNAME = {"south":"South — Tinderwick / coast (Ember, Tide)","east":"East — Lowleaf & Cinderhead (Verdant, Stone)",
         "north":"North — Galehigh & Pale Vault (Storm, Frost)","west":"West — Solarium & Nightreach (Solar, Lunar)",
         "outer":"Outer — Coldfog Marches (Dark)","central":"Central — Umbral Spire (legendaries)","post":"Post-game — Dawnstead"}

out = ["# PixelKin — The Dex (151)\n",
       "> Generated from `src/game/data/species.json` by `tools/balance/gen_docs.py`. "
       "Every entry is original (VISION.md). Lines show kindling chains (→).\n"]

# tally
from collections import Counter
tc = Counter(s["tier"] for s in sp); ty = Counter(s["types"][0] for s in sp)
out.append(f"- **Total:** {len(sp)}  |  **Tiers:** " + " ".join(f"{t}:{tc[t]}" for t in "ABCDEF"))
out.append("- **Primary types:** " + "  ".join(f"{t}:{ty[t]}" for t in ["Ember","Tide","Verdant","Stone","Storm","Frost","Solar","Lunar","Light","Dark"]) + "\n")

for region in REGION:
    members = [s for s in sp if s["dex"]["habitat"] == region]
    if not members: continue
    out.append(f"\n## {RNAME[region]}\n")
    out.append("| # | Name | Types | Tier | Role | BST | Kindles | Catch | Size | Dex entry |")
    out.append("|--:|------|-------|:--:|------|--:|---------|--:|-----|-----------|")
    for s in sorted(members, key=lambda s: s["id"]):
        types = "/".join(s["types"])
        kn = ""
        if s.get("kindling"):
            nxt = by_id.get(s["kindling"]["into"])
            tg = s["kindling"]["trigger"]
            trg = tg.get("level") and f"L{tg['level']}" or tg.get("kind")
            if tg.get("when"): trg = f"{trg} {tg['when']}"
            kn = f"→ {nxt['name'] if nxt else '?'} ({trg})"
        elif s.get("from"):
            kn = f"(from {by_id[s['from']]['name']})"
        size = f"{s['dex']['size_cm']}cm/{s['dex']['weight_kg']}kg"
        entry = s["dex"]["entry"].replace("|", "\\|")
        if len(entry) > 90: entry = entry[:88] + "…"
        out.append(f"| {s['id']} | **{s['name']}** | {types} | {s['tier']} | {s['role']} | {s['bst']} | {kn} | {s['catchRate']} | {size} | {entry} |")

open(os.path.join(ROOT, "docs", "mechanics", "dex.md"), "w").write("\n".join(out))
print("Wrote docs/mechanics/dex.md")
