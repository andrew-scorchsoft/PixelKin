#!/usr/bin/env python3
"""Render the one-shot under the Hartway's mist reel (the `frames` op in
content/regions/hartway.ts, fired as the herd frame lands):

  world-mist-herd   ~24 s: a herd of Sunstags going past in the mist — soft hoof-falls
                    on turf, close and then closer, breath, three far-off stag calls
                    (a rising, wavering two-note bugle) and a faint glassy shimmer for
                    the light in their antlers; then they are gone up the hill.

Synthesised (numpy, fixed seed), not chip-rendered. Shares ambient_beds.py's helpers
and mp3 writer. Original material only.

    python3 tools/audio/mist_herd.py [--wav-dir DIR]

Writes public/assets/audio/sfx/world-mist-herd.mp3 and refreshes sfx.manifest.json.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from ambient_beds import SR, SFX_DIR, shaped_noise, write_mp3, write_wav, refresh_manifest

SECONDS = 24.0
TARGET_RMS_DB = -21.0
PEAK_DB = -2.0


def env(n: int, pts: list[tuple[float, float]]) -> np.ndarray:
    t = np.arange(n) / SR
    xs, ys = zip(*pts)
    return np.interp(t, xs, ys)


def hoof(rng, weight: float) -> np.ndarray:
    """One soft hoof-fall on turf: a low thud with a short muffled scuff."""
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    f = rng.uniform(58, 92)
    thud = np.sin(2 * np.pi * f * t * (1 - 0.6 * t)) * np.exp(-t / 0.045)
    scuff = shaped_noise(n, rng, 180, 900, tilt=-6) * np.exp(-t / 0.03) * 0.25
    return (thud + scuff) * weight


def call(rng, f0: float) -> np.ndarray:
    """A far stag's call: rises, holds with a waver, falls away; softened by distance."""
    n = int(2.6 * SR)
    t = np.arange(n) / SR
    glide = np.interp(t, [0, 0.5, 1.7, 2.6], [f0 * 0.62, f0, f0 * 1.04, f0 * 0.7])
    waver = 1 + 0.012 * np.sin(2 * np.pi * 5.5 * t)
    ph = 2 * np.pi * np.cumsum(glide * waver) / SR
    x = np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph)
    x *= np.interp(t, [0, 0.35, 1.8, 2.6], [0, 1, 0.8, 0])
    k = int(SR / 1800)
    x = np.convolve(x, np.ones(k) / k, mode="same")          # far away
    out = np.zeros(n + int(0.9 * SR))
    out[:n] += x
    for d, gain in ((0.31, 0.35), (0.62, 0.16)):               # the hillside answers
        i = int(d * SR)
        out[i:i + n] += x * gain
    return out


def mist_herd(rng) -> np.ndarray:
    n = int(SECONDS * SR)
    out = np.zeros(n)
    # the mist itself: a soft breath, swelling as it closes round the bench
    out += shaped_noise(n, rng, 120, 1400, tilt=-7) * 0.16 * env(n, [(0, 0.2), (6, 0.8), (16, 0.9), (SECONDS, 0.1)])
    # hoof-falls: sparse, then all around, then thinning uphill
    density = env(n, [(0, 0.5), (3, 3.0), (9, 9.0), (15, 8.0), (20, 2.0), (SECONDS, 0.2)])
    t = 0.3
    while t < SECONDS - 0.4:
        i = int(t * SR)
        near = rng.uniform(0.25, 1.0) ** 2
        h = hoof(rng, 0.9 * near)
        out[i:i + h.size] += h[: n - i]
        t += rng.exponential(1.0 / max(0.3, density[i]))
    # three calls, the middle one close
    for at, f0, gain in ((2.2, 610, 0.25), (9.5, 520, 0.42), (17.5, 680, 0.2)):
        c = call(rng, f0) * gain
        i = int(at * SR)
        out[i:i + c.size] += c[: n - i]
    # the antler-light: a few glassy pings high in the mist
    for at in rng.uniform(5, 18, size=9):
        m = int(1.2 * SR)
        tt = np.arange(m) / SR
        f = rng.choice([1760, 2093, 2349, 2637, 3136])
        ping = np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.35) * rng.uniform(0.02, 0.05)
        i = int(at * SR)
        out[i:i + m] += ping[: n - i]
    return out * env(n, [(0, 0), (1.2, 1), (SECONDS - 4, 1), (SECONDS, 0)])


def master(x: np.ndarray) -> np.ndarray:
    x = x - x.mean()
    x *= 10 ** (TARGET_RMS_DB / 20) / (np.sqrt(np.mean(x ** 2)) or 1.0)
    ceil = 10 ** (PEAK_DB / 20)
    return np.tanh(x / ceil) * ceil


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wav-dir", type=Path)
    args = ap.parse_args()
    x = master(mist_herd(np.random.default_rng(12104)))
    write_mp3(SFX_DIR / "world-mist-herd.mp3", x)
    if args.wav_dir:
        args.wav_dir.mkdir(parents=True, exist_ok=True)
        write_wav(args.wav_dir / "world-mist-herd.wav", x)
    print(f"world-mist-herd: {x.size / SR:.2f} s, rms {20 * np.log10(np.sqrt(np.mean(x ** 2))):.1f} dBFS")
    refresh_manifest()


if __name__ == "__main__":
    main()
