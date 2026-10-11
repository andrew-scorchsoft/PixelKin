#!/usr/bin/env python3
"""
make_loop.py — turn a generated music render (e.g. an ElevenLabs track) into a
seamless whole-file game loop.

The engine loops a music file end-to-start (`MusicDirector`, `loop: true`), so
the file itself must be seamless. A text-to-music render is a performance, not a
loop: it may have a pickup, a drift in level, or a tail. This tool:

  1. decodes the render to mono (ffmpeg) and estimates its tempo,
  2. searches for a loop start `s` (early) and loop end `e` (late) whose
     following few seconds sound the same (chroma + timbre + loudness),
     preferring loop lengths that are a whole number of bars,
  3. writes audio[s:e] with the first `--xfade` ms blended with audio[e:...]
     (fading out) so the jump end->start is continuous on every repeat.

  python3 tools/audio/make_loop.py IN.mp3 OUT.mp3 [--min-len 40] [--bars-per 4]
        [--xfade 250] [--report]

numpy + ffmpeg only. Prints the chosen points, the seam score and the level at
head/tail so you can judge before listening.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

import numpy as np

SR = 22050          # analysis rate
HOP = 512
FFT = 2048


def decode(path: str, sr: int, channels: int) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", str(channels), "-ar", str(sr), "-"],
        check=True, capture_output=True,
    ).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    return x.reshape(-1, channels) if channels > 1 else x


def features(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-frame chroma (12), coarse log-spectrum (24 bands), rms."""
    n = 1 + (len(x) - FFT) // HOP
    win = np.hanning(FFT).astype(np.float32)
    frames = np.lib.stride_tricks.as_strided(
        x, shape=(n, FFT), strides=(x.strides[0] * HOP, x.strides[0]))
    mag = np.abs(np.fft.rfft(frames * win, axis=1))
    freqs = np.fft.rfftfreq(FFT, 1 / SR)
    ok = (freqs > 55) & (freqs < 5000)
    pc = (np.round(12 * np.log2(freqs[ok] / 440.0)) % 12).astype(int)
    chroma = np.zeros((n, 12), np.float32)
    for k in range(12):
        chroma[:, k] = (mag[:, ok][:, pc == k] ** 2).sum(1)
    chroma /= chroma.sum(1, keepdims=True) + 1e-9
    edges = np.geomspace(40, SR / 2, 25)
    bands = np.stack([mag[:, (freqs >= a) & (freqs < b)].mean(1) for a, b in zip(edges[:-1], edges[1:])], 1)
    logspec = np.log1p(bands * 10)
    rms = np.sqrt((frames ** 2).mean(1))
    return chroma, logspec, rms


def tempo(logspec: np.ndarray) -> float:
    flux = np.maximum(0, np.diff(logspec, axis=0)).sum(1)
    flux = flux - flux.mean()
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    fps = SR / HOP
    lags = np.arange(len(ac))
    bpm = 60 * fps / np.maximum(lags, 1)
    m = (bpm >= 60) & (bpm <= 180)
    lag = lags[m][np.argmax(ac[m])]
    return 60 * fps / lag


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--min-len", type=float, default=40.0, help="shortest loop body, seconds")
    ap.add_argument("--max-start", type=float, default=12.0, help="latest loop start, seconds")
    ap.add_argument("--window", type=float, default=4.0, help="seconds compared after each point")
    ap.add_argument("--bars-per", type=int, default=4, help="prefer loop lengths that are a multiple of N bars")
    ap.add_argument("--bpm", type=float, default=None, help="override tempo estimate")
    ap.add_argument("--xfade", type=float, default=250.0, help="seam blend, ms")
    ap.add_argument("--bitrate", default="128k")
    ap.add_argument("--report", action="store_true", help="analyse only")
    ap.add_argument("--keep-intro", action="store_true",
                    help="keep audio[0:s] as a play-once intro: the file is audio[0:e] and the engine loops back to s (prints loop_start)")
    ap.add_argument("--preview", metavar="OUT", help="also write an intro + loop + loop listening preview")
    a = ap.parse_args()

    x = decode(a.inp, SR, 1)
    chroma, logspec, rms = features(x)
    fps = SR / HOP
    total = len(x) / SR
    bpm = a.bpm or tempo(logspec)
    bar = 4 * 60 / bpm

    def norm(f):
        return (f - f.mean(0)) / (f.std(0) + 1e-6)
    F = np.concatenate([norm(chroma) * 1.5, norm(logspec), norm(np.log(rms + 1e-5))[:, None]], 1)
    W = int(a.window * fps)
    nfr = len(F)

    best = None
    max_s = min(int(a.max_start * fps), nfr - W - 1)
    e_lo = int(a.min_len * fps)
    # For each lag (= loop length), frame-wise distance F[t] vs F[t+lag], then a
    # windowed sum gives the seam distance for every start t at once.
    for lag in range(e_lo, nfr - W):
        dd = ((F[:nfr - lag] - F[lag:]) ** 2).mean(1)
        cs = np.concatenate([[0.0], np.cumsum(dd)])
        n = min(max_s + 1, len(dd) - W + 1)
        if n <= 0:
            continue
        win = (cs[W:W + n] - cs[:n]) / W
        s = int(np.argmin(win))
        d = float(win[s])
        L = lag / fps
        bars = L / bar
        grid = abs(bars / a.bars_per - round(bars / a.bars_per)) * a.bars_per
        score = d + 0.15 * grid
        if best is None or score < best[0]:
            best = (score, s, s + lag, d, bars)
    score, s, e, d, bars = best
    ts, te = s / fps, e / fps

    def lvl(t0, t1):
        seg = x[int(t0 * SR):int(t1 * SR)]
        return round(float(20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9)), 1)
    rep = {
        "duration": round(total, 2), "bpm_est": round(float(bpm), 1), "bar_s": round(bar, 3),
        "loop_start": round(ts, 3), "loop_end": round(te, 3), "loop_len": round(te - ts, 2),
        "loop_bars": round(bars, 2), "seam_distance": round(d, 3),
        "level_db": {"first5": lvl(0, 5), "mid": lvl(total / 2 - 2.5, total / 2 + 2.5), "last5": lvl(total - 5, total)},
    }
    print(json.dumps(rep, indent=2))
    if a.report or not a.out:
        return 0

    # Render at full quality: stereo 44.1k, sample-accurate cut + seam blend.
    SR2 = 44100
    y = decode(a.inp, SR2, 2)
    i0, i1 = int(round(ts * SR2)), int(round(te * SR2))
    xf = int(a.xfade / 1000 * SR2)
    body = y[i0:i1].copy()
    tail = y[i1:i1 + xf]
    xf = len(tail)
    if xf:
        ramp = np.linspace(0, 1, xf, dtype=np.float32)[:, None]
        body[:xf] = body[:xf] * np.sqrt(ramp) + tail * np.sqrt(1 - ramp)
    intro = y[:i0] if a.keep_intro else y[:0]
    # With an intro, the blend sits at the loop start (heard on every repeat AND on
    # the first pass straight out of the intro, which is continuous anyway).
    full = np.concatenate([intro, body])

    def write(arr, path):
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR2), "-i", "-",
             "-c:a", "libmp3lame", "-b:a", a.bitrate, path],
            input=np.clip(arr, -1, 1).astype(np.float32).tobytes(), check=True,
        )
    write(full, a.out)
    if a.preview:
        write(np.concatenate([full, body, body[: SR2 * 8]]), a.preview)
    print(f"wrote {a.out}  ({(i1 - i0) / SR2:.2f}s loop"
          + (f", loop_start={len(intro) / SR2:.4f}s intro" if a.keep_intro else "") + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
