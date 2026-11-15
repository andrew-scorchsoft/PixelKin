#!/usr/bin/env python3
"""Render the Rolling Thunder one-shots for the Rio Tower's Thunder Table (the
`frames` reel in content/regions/sere.ts):

  world-thunder-roll   ~16 s: the dry storm crossing the Sere — a far grumble that
                       grows, rolls overhead in long rumbles under a hiss of rain
                       on the sand, and rolls away north. Timed to the reel
                       (six stills, 1600 ms holds + 700 ms dissolves).
  world-thunder-crack  ~4 s: one strike close by — the rip, the boom, the long
                       roll-off. The reel plays it on the frames that STRIKE.

Synthesised here (numpy, fixed seeds), not chip-rendered: a chip noise channel
can't do a convincing thunderclap. Shares ambient_beds.py's helpers + mp3 writer.
Original material only.

    python3 tools/audio/thunder_roll.py [--wav-dir DIR]

Writes public/assets/audio/sfx/<stem>.mp3 and refreshes sfx.manifest.json.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from ambient_beds import SR, SFX_DIR, shaped_noise, write_mp3, write_wav, refresh_manifest, bed_wind

TARGET_RMS_DB = -17.0
PEAK_DB = -1.5


def env(n: int, pts: list[tuple[float, float]]) -> np.ndarray:
    t = np.arange(n) / SR
    xs, ys = zip(*pts)
    return np.interp(t, xs, ys)


def lowpass(x: np.ndarray, hz: float) -> np.ndarray:
    k = max(1, int(SR / hz))
    return np.convolve(x, np.ones(k) / k, mode="same")


def rumble_burst(rng, seconds: float, lo=28, hi=140) -> np.ndarray:
    """One long roll: low noise with a lumpy, rolling amplitude (many small swells)."""
    n = int(seconds * SR)
    x = shaped_noise(n, rng, lo, hi, tilt=-6)
    lumps = np.zeros(n)
    t = np.arange(n) / SR
    for c in rng.uniform(0, seconds, size=int(seconds * 3)):
        w = rng.uniform(0.15, 0.6)
        lumps += rng.uniform(0.4, 1.0) * np.exp(-((t - c) / w) ** 2)
    shape = np.minimum(1.0, t / 0.6) * np.exp(-t / (seconds * 0.55))
    return x * (0.35 + lumps) * shape


def crack(rng, seconds: float = 4.0) -> np.ndarray:
    n = int(seconds * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    # the RIP: broadband, a few stuttering sub-cracks in the first 0.35 s
    rip = shaped_noise(n, rng, 600, 7000, tilt=-2)
    stut = np.zeros(n)
    for c in [0.0, 0.05, 0.11, 0.19, 0.30]:
        stut += rng.uniform(0.5, 1.0) * np.exp(-np.maximum(t - c, 0) / 0.035) * (t >= c)
    out += rip * stut * 0.9
    # the BOOM: a low thump that rings
    boom = shaped_noise(n, rng, 30, 110, tilt=-4)
    out += boom * np.minimum(1, t / 0.02) * np.exp(-t / 0.9) * 1.8
    # the ROLL-OFF: the long grumble that follows a near strike
    roll = rumble_burst(rng, seconds - 0.2)
    out[int(0.2 * SR):] += roll[: n - int(0.2 * SR)] * 1.4
    return out


def rain(rng, n: int) -> np.ndarray:
    hiss = shaped_noise(n, rng, 1200, 9000, tilt=-3) * 0.25
    patter = np.zeros(n)
    for at in rng.integers(0, n - 200, size=int(n / SR * 90)):
        m = 60
        patter[at:at + m] += rng.uniform(0.2, 1.0) * np.exp(-np.arange(m) / 9.0) * rng.normal(size=m)
    patter = patter - lowpass(patter, 1500)
    return hiss + patter * 0.35


def thunder_roll(rng) -> np.ndarray:
    seconds = 16.5
    n = int(seconds * SR)
    out = np.zeros(n)
    # far-off grumbles while the shelf is still on the horizon
    for at, dur, g in [(0.6, 3.5, 0.35), (2.6, 3.0, 0.5)]:
        b = rumble_burst(rng, dur, 25, 90)
        i = int(at * SR)
        out[i:i + b.size] += b[: n - i] * g
    # it rolls in: long overlapping rumbles, loudest overhead (8-12 s)
    for at, dur, g in [(4.6, 4.5, 0.8), (7.0, 5.0, 1.0), (9.8, 4.5, 0.9), (12.2, 4.0, 0.55)]:
        b = rumble_burst(rng, dur)
        i = int(at * SR)
        out[i:i + b.size] += b[: n - i] * g
    # the rain on the sand: in with the shelf, gone as it rolls north
    out += rain(rng, n) * env(n, [(0, 0), (3.5, 0), (5.5, 0.55), (10.5, 0.8), (13.0, 0.35), (15.5, 0), (16.5, 0)])
    # the desert wind underneath it all (the Sere's own bed, softly)
    w = bed_wind(rng)
    out += np.resize(w, n) * 0.18 * env(n, [(0, 0.6), (8, 1.0), (16.5, 0.3)])
    return out * env(n, [(0, 0), (0.3, 1), (15.0, 1), (16.5, 0)])


def master(x: np.ndarray) -> np.ndarray:
    x = x - x.mean()
    x *= 10 ** (TARGET_RMS_DB / 20) / (np.sqrt(np.mean(x ** 2)) or 1.0)
    ceil = 10 ** (PEAK_DB / 20)
    return np.tanh(x / ceil) * ceil


SHOTS = {
    "world-thunder-roll": (thunder_roll, 7101),
    "world-thunder-crack": (crack, 7202),
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wav-dir", type=Path)
    args = ap.parse_args()
    for stem, (fn, seed) in SHOTS.items():
        x = master(fn(np.random.default_rng(seed)))
        write_mp3(SFX_DIR / f"{stem}.mp3", x)
        if args.wav_dir:
            args.wav_dir.mkdir(parents=True, exist_ok=True)
            write_wav(args.wav_dir / f"{stem}.wav", x)
        print(f"{stem}: {x.size / SR:.2f} s, rms {20 * np.log10(np.sqrt(np.mean(x ** 2))):.1f} dBFS")
    refresh_manifest()


if __name__ == "__main__":
    main()
