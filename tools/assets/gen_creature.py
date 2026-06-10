#!/usr/bin/env python3
"""
gen_creature.py — generate ALL FIVE sprite views for one kin from its species data.

The single per-creature command for filling out the dex. Reads
`src/game/data/species/NNN_slug.json`, builds an original brief from that kin's
`art` block + `types` + `dex.category`, and drives the generate-sprite-sheet skill
to produce the standard five views into `assets/creatures/NNN_slug/`:

    battle_front -> battle_back -> icon -> overworld -> portrait

battle_front is generated first; the remaining four pass it as a `--reference`
so the kin stays visually consistent across views (same palette, same silhouette).
metadata.json is written/updated by generate_sprite.py for each view.

Run from the repo root, e.g.:

    ./venv/bin/python tools/assets/gen_creature.py 65
    ./venv/bin/python tools/assets/gen_creature.py 65 70 71      # several
    ./venv/bin/python tools/assets/gen_creature.py --range 65 80 # inclusive range

Packing into public/ is a SEPARATE, central step (pack_creatures.py) so parallel
runs never race on the shared manifest. This script only writes masters under
assets/creatures/.
"""
from __future__ import annotations

import argparse
import glob
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPECIES_DIR = REPO / "src" / "game" / "data" / "species"
GEN = REPO / ".claude" / "skills" / "generate-sprite-sheet" / "scripts" / "generate_sprite.py"
PY = REPO / "venv" / "bin" / "python"

# view-type -> filename the skill writes (per sprite-specs.json "file")
VIEWS = [
    ("creature-front", "battle_front.png"),
    ("creature-back", "battle_back.png"),
    ("creature-icon", "icon.png"),
    ("creature-overworld", "overworld.png"),
    ("creature-portrait", "portrait.png"),
]


def load_species(cid: int) -> dict:
    matches = glob.glob(str(SPECIES_DIR / f"{cid:03d}_*.json"))
    if not matches:
        raise SystemExit(f"no species file for id {cid}")
    return json.loads(Path(matches[0]).read_text())


def build_subject(sp: dict) -> str:
    art = sp.get("art", {})
    sil = (art.get("silhouette") or "").strip()
    direction = (art.get("direction") or "").strip()
    palette = (art.get("palette") or "").strip()
    types = "/".join(sp.get("types", [])) or "elemental"
    category = (sp.get("dex", {}).get("category") or "").strip()
    name = sp.get("name", sp.get("slug", "kin"))

    parts = [f"{name}, an original {types}-type creature"]
    if category:
        parts.append(f"({category})")
    parts.append("— " + sil)
    # palette is often identical to silhouette in the data; only add if it differs.
    if palette and palette != sil:
        parts.append("Palette: " + palette)
    if direction:
        parts.append("Design intent: " + direction)
    subject = " ".join(parts)
    # Keep prompts tight; the per-type template supplies the rest.
    return subject


def gen_view(cid: int, slug: str, vtype: str, subject: str, reference: Path | None,
             provider: str | None = None) -> bool:
    cmd = [str(PY), str(GEN), "--type", vtype, "--subject", subject,
           "--creature-id", str(cid), "--creature-slug", slug]
    if reference is not None and reference.is_file():
        cmd += ["--reference", str(reference)]
    if provider:
        cmd += ["--provider", provider]
    print(f"  [{cid:03d} {slug}] {vtype} ...", flush=True)
    res = subprocess.run(cmd, cwd=str(REPO))
    return res.returncode == 0


def gen_creature(cid: int, provider: str | None = None) -> bool:
    sp = load_species(cid)
    slug = sp["slug"]
    subject = build_subject(sp)
    cdir = REPO / "assets" / "creatures" / f"{cid:03d}_{slug}"
    front = cdir / "battle_front.png"

    ok = True
    for vtype, fname in VIEWS:
        ref = front if vtype != "creature-front" else None
        if not gen_view(cid, slug, vtype, subject, ref, provider):
            print(f"  !! FAILED {vtype} for {cid:03d}_{slug}", file=sys.stderr)
            ok = False
    # report which files landed
    have = [f for _, f in VIEWS if (cdir / f).is_file()]
    print(f"  [{cid:03d} {slug}] wrote {len(have)}/5 views: {', '.join(have)}", flush=True)
    return ok and len(have) == 5


def main() -> int:
    p = argparse.ArgumentParser(description="Generate all 5 sprite views for one or more kin.")
    p.add_argument("ids", nargs="*", type=int, help="Dex ids to generate.")
    p.add_argument("--range", nargs=2, type=int, metavar=("LO", "HI"),
                   help="Inclusive id range to generate.")
    p.add_argument("--provider", choices=["google", "openai"], default=None,
                   help="Image provider passed through to generate_sprite.py. Default: the "
                        "skill's default (google). Use 'openai' as a fallback when Google is "
                        "rate-limited / spend-capped.")
    args = p.parse_args()

    ids: list[int] = list(args.ids)
    if args.range:
        ids += list(range(args.range[0], args.range[1] + 1))
    if not ids:
        p.error("give ids or --range LO HI")

    failures = []
    for cid in ids:
        print(f"=== creature {cid} ===", flush=True)
        if not gen_creature(cid, provider=args.provider):
            failures.append(cid)
    if failures:
        print(f"\nFAILURES: {failures}", file=sys.stderr)
        return 1
    print(f"\nAll {len(ids)} creature(s) generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
