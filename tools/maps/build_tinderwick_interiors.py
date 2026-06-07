#!/usr/bin/env python3
"""
DEPRECATED shim. Tinderwick's interiors (house / shop / Ember Lumenary) are now built by the
shared, faced-wall interior builder tools/maps/build_interiors.py (docs/world/interiors.md).
This wrapper just rebuilds the Tinderwick ones so old muscle memory / scripts keep working.

Run:  python3 tools/maps/build_tinderwick_interiors.py
"""
from __future__ import annotations
import build_interiors as bi  # type: ignore

if __name__ == "__main__":
    for m in bi.all_maps():
        if m["id"].startswith("tinderwick"):
            bi.write_and_render(m)
    print("DONE (via build_interiors.py)")
