#!/usr/bin/env python3
"""check_walk_facing.py — catch walk sheets that look fine as a grid but break
when the walk CYCLES (a stray cell in the left row facing right/forward, an up
row cell that shows a face).

Per side-row frame we ask two independent questions:
  1. Whole-row direction (WARN only): which side of the head the face sits on
     (or, with no skin showing, the head's lean). Calibrated 2026-10 against the
     shipped cast, pixel tests mis-call this both ways (hair buns, packs, hands,
     pale hair), so the whole-row direction is confirmed by EYE in the GIF.
  2. Mirror-consistency (ERROR): is the frame more like its row-mates than like
     their MIRRORS? A cell drawn facing the other way is closer to the mirrors.
     This is THE walk-cycle bug (one stray cell) and it is reliable.
  3. Symmetry: a side-row cell that's nearly its own mirror is a FRONT view
     smuggled into a profile row.
The up row gets a skin-tone WARNING only (hair colour fools pixel tests —
back-of-head vs face is the one thing you must confirm by eye in the GIF).

Also writes an animated GIF of each row cycling (--gif out.gif) — always LOOK at
it; a walk sheet is only approved once the cycle reads right in motion.

Usage: check_walk_facing.py SHEET.png [--gif out.gif] [--frame 32] [--json]
Exit 1 when any ERROR is found.
"""
import argparse, json, sys
from PIL import Image, ImageChops, ImageStat

ROWS = ["down", "left", "right", "up"]


def frames(sheet, fw, fh):
    cols, rows = sheet.width // fw, sheet.height // fh
    return [[sheet.crop((c * fw, r * fh, c * fw + fw, r * fh + fh)) for c in range(cols)] for r in range(rows)]


def alpha_mask(im):
    return im.split()[3].point(lambda v: 255 if v > 0 else 0)


def diff(a, b):
    """Mean abs RGBA difference over the union of both silhouettes (0 = identical)."""
    m = ImageChops.lighter(alpha_mask(a), alpha_mask(b))
    d = ImageChops.difference(a.convert("RGBA"), b.convert("RGBA")).convert("L")
    st = ImageStat.Stat(d, m)
    return st.mean[0] if st.count[0] else 0.0


def head_lean(im):
    """Signed x offset of the head band's opaque-pixel centroid from the whole
    body's centroid (negative = leans left). Head band = the top 40% of the bbox."""
    a = im.split()[3]
    bb = a.getbbox()
    if not bb:
        return 0.0
    px = a.load()
    x0, y0, x1, y1 = bb
    hy = y0 + max(1, int((y1 - y0) * 0.4))
    def cx(ya, yb):
        s = n = 0
        for y in range(ya, yb):
            for x in range(x0, x1):
                if px[x, y] > 0:
                    s += x; n += 1
        return s / n if n else (x0 + x1) / 2
    return cx(y0, hy) - cx(hy, y1)


def face_side(im):
    """Signed x offset of the head band's SKIN centroid from the head band's
    opaque centroid (negative = the face sits on the left = facing left), or
    None when too little skin shows (helmets, hoods, back views). A profile's
    face is on the leading side; hair buns, hoods and packs trail behind it,
    which is why this beats raw head-lean when skin is visible."""
    a = im.split()[3]; bb = a.getbbox()
    if not bb:
        return None
    x0, y0, x1, y1 = bb
    hy = y0 + max(1, int((y1 - y0) * 0.4))
    rgba = im.convert("RGBA").load()
    sx = sn = ox = on = 0
    for y in range(y0, hy):
        for x in range(x0, x1):
            r, g, b, al = rgba[x, y]
            if al == 0:
                continue
            ox += x; on += 1
            if _is_skin(r, g, b):
                sx += x; sn += 1
    if sn < 4 or not on:
        return None
    return sx / sn - ox / on


def _is_skin(r, g, b):
    return r > 150 and g > 95 and b > 65 and r > g > b and 35 < r - b < 120 and g - b > 15


def skin_ratio(im):
    """Fraction of head-band pixels that look like a lit skin tone (warm, mid-light)."""
    a = im.split()[3]; bb = a.getbbox()
    if not bb:
        return 0.0
    x0, y0, x1, y1 = bb
    hy = y0 + max(1, int((y1 - y0) * 0.4))
    rgba = im.convert("RGBA").load()
    tot = sk = 0
    for y in range(y0, hy):
        for x in range(x0, x1):
            r, g, b, al = rgba[x, y]
            if al == 0:
                continue
            tot += 1
            if _is_skin(r, g, b):
                sk += 1
    return sk / tot if tot else 0.0


def check(path, fw=32, fh=32):
    sheet = Image.open(path).convert("RGBA")
    fr = frames(sheet, fw, fh)
    errs, warns, detail = [], [], {}
    for ri, name in enumerate(ROWS[: len(fr)]):
        row = fr[ri]
        if name in ("left", "right"):
            want = -1 if name == "left" else 1
            leans = [head_lean(f) for f in row]
            detail[name] = {"head_lean": [round(v, 2) for v in leans]}
            # Row direction by majority; every cell must agree with it.
            for ci, f in enumerate(row):
                others = [o for j, o in enumerate(row) if j != ci]
                same = sum(diff(f, o) for o in others) / len(others)
                flip = sum(diff(f, o.transpose(Image.FLIP_LEFT_RIGHT)) for o in others) / len(others)
                sym = diff(f, f.transpose(Image.FLIP_LEFT_RIGHT))
                if flip + 2.0 < same:
                    errs.append(f"{name} row cell {ci}: faces the OPPOSITE way to its row-mates "
                                f"(diff same={same:.1f} vs mirrored={flip:.1f})")
                if sym < 6.0:
                    errs.append(f"{name} row cell {ci}: nearly symmetric (sym={sym:.1f}) — a FRONT/BACK "
                                f"view in a profile row")
            mean_lean = sum(leans) / len(leans)
            faces = [v for v in (face_side(f) for f in row) if v is not None]
            detail[name]["face_side"] = [round(v, 2) for v in faces]
            if len(faces) >= 2:
                # The face is visible: trust which side it's on over the head's bulk
                # (a hair bun / hood / pack trails behind and skews the lean).
                mean_face = sum(faces) / len(faces)
                if abs(mean_face) >= 0.5 and (mean_face > 0) != (want > 0):
                    warns.append(f"{name} row: the face may sit on the {'right' if mean_face > 0 else 'left'} "
                                f"of the head ({mean_face:+.2f}px) — the whole row faces the wrong way")
                elif abs(mean_face) < 0.5:
                    warns.append(f"{name} row face-side is ambiguous ({mean_face:+.2f}px) — eyeball the GIF")
            elif abs(mean_lean) >= 0.4 and (mean_lean > 0) != (want > 0):
                warns.append(f"{name} row leans {'right' if mean_lean > 0 else 'left'} "
                            f"(head centroid {mean_lean:+.2f}px) — the whole row may face the wrong way")
            elif abs(mean_lean) < 0.4:
                warns.append(f"{name} row head-lean is ambiguous ({mean_lean:+.2f}px) — eyeball the GIF")
        elif name == "up":
            sr = [round(skin_ratio(f), 3) for f in row]
            detail["up"] = {"skin_ratio": sr}
            down_sr = sum(skin_ratio(f) for f in fr[0]) / len(fr[0])
            for ci, v in enumerate(sr):
                if down_sr > 0.08 and v > down_sr * 0.6:
                    warns.append(f"up row cell {ci}: may show a face (skin {v:.2f} vs down-row {down_sr:.2f}) "
                                f"— the up row must be the BACK of the head")
    return {"sheet": str(path), "ok": not errs, "errors": errs, "warnings": warns, "detail": detail}


def write_gif(path, out, fw=32, fh=32, scale=4, bg=(46, 52, 84, 255)):
    sheet = Image.open(path).convert("RGBA")
    fr = frames(sheet, fw, fh)
    seq = []
    for step in range(len(fr[0]) * 2):
        canvas = Image.new("RGBA", (fw * len(fr), fh), bg)
        for ri, row in enumerate(fr):
            canvas.alpha_composite(row[step % len(row)], (ri * fw, 0))
        seq.append(canvas.resize((canvas.width * scale, canvas.height * scale), Image.NEAREST).convert("P"))
    seq[0].save(out, save_all=True, append_images=seq[1:], duration=160, loop=0)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("sheets", nargs="+")
    p.add_argument("--gif", help="write an animated preview (single sheet only)")
    p.add_argument("--frame", type=int, default=32)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    bad = False
    for s in a.sheets:
        r = check(s, a.frame, a.frame)
        bad |= not r["ok"]
        if a.json:
            print(json.dumps(r, indent=2))
        else:
            print(("OK   " if r["ok"] else "FAIL ") + s)
            for e in r["errors"]:
                print("   ERROR", e)
            for w in r["warnings"]:
                print("   warn ", w)
        if a.gif and len(a.sheets) == 1:
            write_gif(s, a.gif, a.frame, a.frame)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
