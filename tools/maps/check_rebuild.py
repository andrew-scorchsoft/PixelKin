#!/usr/bin/env python3
"""
check_rebuild — prove the map pipeline REPRODUCES every shipped map.

Shipped map JSONs are written by the builders AND by id-keyed post-build runners.
This runs the whole pipeline from scratch in a throw-away `git worktree` (your
working tree is never touched) and diffs the result against what is shipped:

    every tools/maps/build_*.py (map builders; the tileset builders are skipped)
      -> add_hand_placed.py -> add_peril_thread.py
      -> add_world_craft.py (all regions) -> vary_trees.py

then compares each public/assets/maps/*.json as PARSED JSON (key order ignored).
Any map that differs is reported per list-entry id / layer / key, and the script
exits 1. A map that only exists after the rebuild (or only before) is a mismatch
too.

The worktree is a snapshot of your CURRENT working state (`git stash create`, so
uncommitted edits to tracked files are included, plus untracked non-ignored
files), so you can check a builder edit before committing it.

Run (from the repo root; ~1-2 min — every builder runs its own render + audits):
    python3 tools/maps/check_rebuild.py                 # full experiment
    python3 tools/maps/check_rebuild.py --keep          # leave the worktree for poking at
    python3 tools/maps/check_rebuild.py --only build_tinderwick,build_crossroads
    python3 tools/maps/check_rebuild.py -v              # also print each builder's log tail
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS_REL = Path("public/assets/maps")
# builders that write TILESETS (art), not maps — not part of the map pipeline
NOT_MAP_BUILDERS = {"build_shared_overworld", "build_coldfog_set", "build_interior_walls"}
# the post-build runners, in pipeline order (each is an id-keyed idempotent upsert)
RUNNERS = [
    ["tools/maps/add_hand_placed.py"],
    ["tools/maps/add_peril_thread.py"],
    ["tools/maps/add_world_craft.py"],
    ["tools/maps/vary_trees.py"],
]


def git(*args: str, cwd: Path = REPO, check: bool = True) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                          check=check).stdout.strip()


def make_worktree(dest: Path) -> None:
    snap = git("stash", "create") or "HEAD"
    git("worktree", "add", "--detach", str(dest), snap)
    # untracked (non-ignored) files: a brand-new builder or runner not yet added
    for rel in git("ls-files", "--others", "--exclude-standard", "-z").split("\0"):
        if rel and (REPO / rel).is_file():
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / rel, dest / rel)
    nm = REPO / "node_modules"
    if nm.is_dir():
        (dest / "node_modules").symlink_to(nm)


def load_maps(root: Path) -> dict[str, object]:
    return {p.stem: json.loads(p.read_text()) for p in sorted((root / MAPS_REL).glob("*.json"))}


def _short(v: object, n: int = 110) -> str:
    s = json.dumps(v, sort_keys=True)
    return s if len(s) <= n else s[: n - 3] + "..."


def diff(a: object, b: object, path: str = "", W: int = 0) -> list[str]:
    """Human diff of shipped `a` vs rebuilt `b` (parsed JSON)."""
    if a == b:
        return []
    if isinstance(a, dict) and isinstance(b, dict):
        out: list[str] = []
        for k in sorted(set(a) | set(b)):
            p = f"{path}.{k}" if path else k
            if k not in b:
                out.append(f"  - {p}: lost {_short(a[k])}")
            elif k not in a:
                out.append(f"  + {p}: gained {_short(b[k])}")
            else:
                out += diff(a[k], b[k], p, W)
        return out
    if isinstance(a, list) and isinstance(b, list):
        keyed = lambda L: all(isinstance(x, dict) and "id" in x for x in L)  # noqa: E731
        if (a or b) and keyed(a) and keyed(b):
            ia = {x["id"]: x for x in a}
            ib = {x["id"]: x for x in b}
            out = []
            for k in ia:
                if k not in ib:
                    out.append(f"  - {path}[{k}] lost on rebuild")
            for k in ib:
                if k not in ia:
                    out.append(f"  + {path}[{k}] only in rebuild")
            for k in ia:
                if k in ib:
                    out += diff(ia[k], ib[k], f"{path}[{k}]", W)
            if not out and [x["id"] for x in a] != [x["id"] for x in b]:
                out.append(f"  ~ {path}: same entries, different order")
            return out
        if all(isinstance(x, dict) and ("role" in x or "name" in x) for x in a + b) and len(a) == len(b):
            out = []
            for i, (x, y) in enumerate(zip(a, b)):
                out += diff(x, y, f"{path}[{x.get('role') or x.get('name') or i}]", W)
            return out
        if len(a) == len(b) and all(isinstance(x, int) for x in a + b):
            cells = [(i % W, i // W, x, y) if W else (i, 0, x, y)
                     for i, (x, y) in enumerate(zip(a, b)) if x != y]
            where = ""
            if len(cells) <= 12:
                where = "  " + " ".join(f"({cx},{cy}):{x}->{y}" for cx, cy, x, y in cells)
            return [f"  ~ {path}: {len(cells)} cell(s) differ (gids){where}"]
        return [f"  ~ {path}: {_short(a, 70)} -> {_short(b, 70)}"]
    return [f"  ~ {path}: {_short(a, 70)} -> {_short(b, 70)}"]


def run(cmd: list[str], cwd: Path, log: Path) -> tuple[int, float]:
    t = time.time()
    with log.open("w") as fh:
        rc = subprocess.run([sys.executable, *cmd], cwd=cwd, stdout=fh, stderr=subprocess.STDOUT).returncode
    return rc, time.time() - t


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keep", action="store_true", help="leave the worktree + logs behind")
    ap.add_argument("--only", help="comma-separated builder stems to run (default: all)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    t0 = time.time()
    tmp = Path(tempfile.mkdtemp(prefix="pixelkin-rebuild-"))
    wt = tmp / "wt"
    logs = tmp / "logs"
    logs.mkdir()
    print(f"worktree: {wt}")
    make_worktree(wt)
    try:
        shipped = load_maps(wt)
        builders = sorted(p.stem for p in (wt / "tools/maps").glob("build_*.py")
                          if p.stem not in NOT_MAP_BUILDERS)
        if args.only:
            want = {s.strip().removesuffix(".py") for s in args.only.split(",")}
            builders = [b for b in builders if b in want]
        crashed: list[str] = []
        for b in builders:
            rc, dt = run([f"tools/maps/{b}.py"], wt, logs / f"{b}.log")
            log = (logs / f"{b}.log").read_text()
            # exit 1 alone is the builder's own audit verdict (expected before the
            # runners re-add their warps); a TRACEBACK means the map wasn't written
            if "Traceback (most recent call last)" in log:
                crashed.append(b)
                print("    " + "\n    ".join(log.splitlines()[-8:]))
            flag = "" if rc == 0 else f"  (exit {rc}: {'CRASHED' if b in crashed else 'its own audits; see log'})"
            print(f"  built {b:<34} {dt:5.1f}s{flag}")
            if args.verbose:
                print("    " + "\n    ".join((logs / f"{b}.log").read_text().splitlines()[-6:]))
        for r in RUNNERS:
            if not (wt / r[0]).is_file():
                print(f"  (runner {r[0]} missing — skipped)")
                continue
            rc, dt = run(r, wt, logs / f"{Path(r[0]).stem}.log")
            tail = (logs / f"{Path(r[0]).stem}.log").read_text().strip().splitlines()
            print(f"  ran   {Path(r[0]).name:<34} {dt:5.1f}s  {tail[-1] if tail else ''}"[:160])
            if rc != 0:
                crashed.append(Path(r[0]).name)
                print("    " + "\n    ".join(tail[-12:]))
        rebuilt = load_maps(wt)

        bad = 0
        for mid in sorted(set(shipped) | set(rebuilt)):
            if mid not in rebuilt:
                print(f"\n✗ {mid}: shipped but GONE after rebuild"); bad += 1; continue
            if mid not in shipped:
                print(f"\n✗ {mid}: written by the rebuild but not shipped"); bad += 1; continue
            d = diff(shipped[mid], rebuilt[mid], W=shipped[mid].get("width", 0))
            if d:
                bad += 1
                print(f"\n✗ {mid}: {len(d)} difference(s) (- shipped only, + rebuild only)")
                for line in d[:60]:
                    print(line)
                if len(d) > 60:
                    print(f"  ... {len(d) - 60} more")
        n = len(set(shipped) | set(rebuilt))
        if crashed:
            print(f"\n✗ these steps failed (their maps can't be trusted): {', '.join(crashed)}")
            bad += 1
        print(f"\n{'PASS' if not bad else 'FAIL'} — {n - bad}/{n} maps reproduce exactly "
              f"({time.time() - t0:.0f}s)")
        return 1 if bad else 0
    finally:
        if args.keep:
            print(f"kept: {wt}  (logs: {logs}); remove with `git worktree remove --force {wt}`")
        else:
            git("worktree", "remove", "--force", str(wt), check=False)
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
