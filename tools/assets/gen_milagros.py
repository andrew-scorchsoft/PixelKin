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
        if c.get("photo"):
            continue   # the master is the flattened photo (milagro_photo.py)
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


def altered_note(im: Image.Image, note: str) -> Image.Image:
    """Bake the 'this card has been altered' note onto the served card: a small
    white label over the bottom border, in plain capitals."""
    from PIL import ImageDraw, ImageFont
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
    except OSError:
        font = ImageFont.load_default()
    d = ImageDraw.Draw(im)
    words, lines, cur = note.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if d.textlength(trial, font=font) > im.width - 56:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    lines.append(cur)
    lh = 16
    h = lh * len(lines) + 8
    top = im.height - h - 14
    d.rounded_rectangle([18, top, im.width - 18, top + h], radius=6, fill=(255, 255, 255), outline=(20, 20, 30), width=2)
    for i, line in enumerate(lines):
        d.text((im.width / 2, top + 4 + i * lh), line, font=font, fill=(20, 20, 30), anchor="ma")
    return im


def pack() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = json.loads((SRC / "briefs.json").read_text())
    notes = {c["slug"]: c["altered"] for c in data["cards"] if c.get("altered")}
    for p in sorted(SRC.glob("*.webp")):
        im = Image.open(p).convert("RGB").resize(SERVED, Image.LANCZOS)
        if p.stem in notes:
            im = altered_note(im, notes[p.stem])
        im.save(OUT / f"{p.stem}.webp", quality=88)
        print(f"  packed {p.stem}" + ("  (altered note)" if p.stem in notes else ""))


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
