#!/usr/bin/env python3
"""
DEPRECATED shim. Pearlmoor's interiors (Tide Lumenary / Chandlery / Quayside Inn) are now built
by the shared, faced-wall interior builder tools/maps/build_interiors.py (docs/world/interiors.md).
This wrapper just rebuilds the Pearlmoor ones so old scripts keep working.

Run:  python3 tools/maps/build_pearlmoor_interiors.py
"""
from __future__ import annotations
import build_interiors as bi  # type: ignore

if __name__ == "__main__":
    for m in bi.all_maps():
        if m["id"].startswith("pearlmoor"):
            bi.write_and_render(m)
    print("DONE (via build_interiors.py)")
