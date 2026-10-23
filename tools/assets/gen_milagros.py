#!/usr/bin/env python3
"""
gen_milagros — the Booji-Wooji Man MILAGRO CARDS (Paul's painted cards) as game art.

Each card is re-created from a photo crop of the real card (assets/milagros/refs/
<slug>.jpg, rotated portrait) through the generate-image skill (OpenAI, input-image
edit), as a clean flat scan with the photo's warm cast corrected and the border
lettering kept. A brief may override the SUBJECT where the photographed one can't
ship as-is (see briefs.json). Masters land in assets/milagros/<slug>.webp (q94) and are
NEVER overwritten (a gen is a gacha: delete a master to re-roll it).

    python3 tools/assets/gen_milagros.py [--only a,b] [--jobs 6]   # generate missing masters
    python3 tools/assets/gen_milagros.py --pack                    # masters -> public/assets/milagros/*.webp
"""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "assets" / "milagros"
OUT = REPO / "public" / "assets" / "milagros"
GEN = REPO / ".claude" / "skills" / "generate-image" / "scripts" / "generate.py"
SERVED = (400, 600)   # 2:3, crisp at the in-game card size x RENDER_SCALE

CARD_PROMPT = (
    "Recreate this hand-painted folk-art card as a clean, flat, front-on scan of the physical card. "
    "Portrait orientation, the whole card filling the frame with a thin white card edge. Keep the artist's "
    "style faithfully: thick black ink outlines, felt-tip and coloured-pencil texture, the bright yellow "
    "border with its decorative pattern, the painted background panel{same}. Correct the photo's warm "
    "yellow lighting cast: neutral white balance, true bright colours, no table, no glare, no shadows, no "
    "perspective or curl.{subject} The hand-lettered text in the border, in the artist's plain capital "
    "handwriting running round the border from the top, must read exactly: \"{text}\""
)


def jobs() -> list[tuple[str, str, Path]]:
    data = json.loads((SRC / "briefs.json").read_text())
    out = []
    for c in data["cards"]:
        subject = f" Subject: {c['subject']}." if c.get("subject") else ""
        same = "" if c.get("subject") else ", the same subject and pose"
        prompt = CARD_PROMPT.format(same=same, subject=subject, text=c["text"])
        out.append((c["slug"], prompt, SRC / "refs" / f"{c.get('ref', c['slug'])}.jpg"))
    for e in data["extras"]:
        out.append((e["slug"], e["prompt"], SRC / "refs" / f"{e['slug']}.jpg"))
    return out


def generate(slug: str, prompt: str, ref: Path) -> str:
    dest = SRC / f"{slug}.webp"
    if dest.exists():
        return f"  keep {slug}"
    r = subprocess.run(
        [sys.executable, str(GEN), "--provider", "openai", "--aspect", "2:3", "--input-image", str(ref),
         "--prompt", prompt, "--output", str(dest), "--max-dim", "1024"],
        capture_output=True, text=True)
    return f"  {'drew' if dest.exists() else 'FAILED'} {slug}" + ("" if dest.exists() else f"\n{r.stderr[-400:]}")


def pack() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for p in sorted(SRC.glob("*.webp")):
        im = Image.open(p).convert("RGB").resize(SERVED, Image.LANCZOS)
        im.save(OUT / f"{p.stem}.webp", quality=88)
        print(f"  packed {p.stem}")


def main() -> None:
    if "--pack" in sys.argv:
        pack()
        return
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    n = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 6
    todo = [j for j in jobs() if only is None or j[0] in only]
    with ThreadPoolExecutor(n) as ex:
        for line in ex.map(lambda j: generate(*j), todo):
            print(line, flush=True)


if __name__ == "__main__":
    main()
