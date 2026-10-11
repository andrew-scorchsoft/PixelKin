#!/usr/bin/env python3
"""
edm_check.py — score how "modern EDM / dance" a music cue sounds, so the retro
soundtrack doesn't drift (owner: the old Windward Stair and the rival battle read as
EDM / drum-and-bass, "not enough like retro music").

Fingerprints measured on the cue body (after the intro):
  kick    — regularity of the low-band (40-150 Hz) pulse at its dominant period
            (four-on-the-floor ≈ a kick on every beat → high autocorrelation peak)
  pump    — depth of beat-locked loudness modulation (sidechain "pumping")
  hats    — high-band (6-16 kHz) transient rate per second
  sub     — share of energy under 60 Hz
Each is z-scored against the whole score; `edm` = their mean. Calibrated on the two
owner-flagged EDM-ish takes vs clearly retro cues.

  python3 tools/audio/edm_check.py [files or ids...]
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SERVED = ROOT / "public/assets/audio/music/remaster"
SR = 22050
H = 512
N = 2048


def decode(p: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def peak_autocorr(env: np.ndarray, lo_bpm=70, hi_bpm=180) -> tuple[float, int]:
    e = env - env.mean()
    if not e.any():
        return 0.0, 0
    ac = np.correlate(e, e, "full")[len(e) - 1:]
    ac = ac / (ac[0] + 1e-9)
    fps = SR / H
    lo, hi = int(60 * fps / hi_bpm), int(60 * fps / lo_bpm)
    k = lo + int(np.argmax(ac[lo:hi]))
    return float(ac[k]), k


def features(p: Path, start_s: float = 0.0) -> dict:
    x = decode(p)[int(start_s * SR):]
    n = (len(x) - N) // H
    fr = np.lib.stride_tricks.as_strided(x, (n, N), (4 * H, 4)) * np.hanning(N).astype(np.float32)
    S = np.abs(np.fft.rfft(fr, axis=1))
    f = np.fft.rfftfreq(N, 1 / SR)
    low = np.log1p(S[:, (f > 40) & (f < 150)].sum(1))
    kick_on = np.maximum(0, np.diff(low))
    kick, lag = peak_autocorr(kick_on)
    rms = np.sqrt((fr ** 2).mean(1))
    db = 20 * np.log10(rms + 1e-6)
    trend = np.convolve(db, np.ones(43) / 43, mode="same")  # ~1 s
    mod = db - trend
    pump_ac = peak_autocorr(mod)[0]
    pump = float(pump_ac * np.std(mod))
    hb = np.log1p(S[:, (f > 6000) & (f < 10500)].sum(1))
    fl = np.maximum(0, np.diff(hb))
    thr = fl.mean() + fl.std()
    hats = float(((fl[1:-1] > thr) & (fl[1:-1] >= fl[:-2]) & (fl[1:-1] >= fl[2:])).sum() / (len(x) / SR))
    P = (S ** 2).mean(0)
    sub = float(P[(f > 20) & (f < 60)].sum() / P.sum())
    return {"kick": kick, "pump": pump, "hats": hats, "sub": sub}


def main() -> int:
    args = sys.argv[1:]
    paths = []
    for a in args or sorted(p.stem for p in SERVED.glob("*.mp3")):
        p = Path(a) if a.endswith(".mp3") else SERVED / f"{a}.mp3"
        paths.append(p)
    rows = []
    for p in paths:
        meta = ROOT / "assets/audio/elevenlabs" / p.stem / "meta.json"
        ls = (json.loads(meta.read_text()).get("loop_start") or 0.0) if meta.exists() and p.parent == SERVED else 0.0
        rows.append((p, features(p, ls)))
    keys = ["kick", "pump", "hats", "sub"]
    M = np.array([[r[1][k] for k in keys] for r in rows])
    Z = (M - M.mean(0)) / (M.std(0) + 1e-9) if len(rows) > 2 else M * 0
    for (p, ft), z in sorted(zip(rows, Z), key=lambda t: -t[1].mean()):
        print(f"{p.stem:30s} edm {z.mean():+.2f} | kick {ft['kick']:.2f} pump {ft['pump']:.2f} "
              f"hats {ft['hats']:4.1f}/s sub {ft['sub'] * 100:4.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
