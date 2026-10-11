#!/usr/bin/env python3
"""Render PixelKin's ambient sound beds (the looping `amb-*` stems).

A map opts into a bed with `ambience.sound_bed` (see src/game/systems/world/
Ambience.ts — it loads `assets/audio/sfx/<stem>.mp3` and loops it quietly under
the area music). Chip noise can't make a convincing *gentle* bed, so these are
rendered here instead: a small, deterministic numpy synthesiser (fixed seeds —
re-running reproduces the same files byte-for-byte modulo the mp3 encoder).

Seamless by construction, not by crossfade: every layer is CIRCULAR over the loop
length N. Noise is shaped in the frequency domain over exactly N samples (so the
inverse FFT is periodic), amplitude envelopes use whole cycles of N, one-off
events (drips, croaks, chirps) wrap around the seam, and reverb is a circular
convolution. Sample N-1 flows into sample 0 exactly as any other pair does — no
click, no swell, no dip at the loop point. N is a multiple of the 1152-sample mp3
frame so the encoder pads as little as possible (and the LAME gapless tag covers
the rest).

    python3 tools/audio/ambient_beds.py                 # render all beds
    python3 tools/audio/ambient_beds.py amb-surf        # just one
    python3 tools/audio/ambient_beds.py --wav-dir /tmp  # also keep .wav previews

Writes public/assets/audio/sfx/<stem>.mp3 and refreshes sfx.manifest.json (the
list Sfx.ts / the bed loader check before loading). Needs numpy + ffmpeg (PATH,
else imageio-ffmpeg). Original material only — every sound here is synthesised.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

SR = 22050
FRAME = 1152
ROOT = Path(__file__).resolve().parents[2]
SFX_DIR = ROOT / "public" / "assets" / "audio" / "sfx"

# Loudness the bed FILE is mastered to. Ambience.ts plays beds at 0.22 x the sfx
# master (music plays at 0.45 x the music master), so a -23 dBFS RMS bed lands
# ~16 dB under a typical area loop (~-13 dBFS RMS): felt more than heard.
TARGET_RMS_DB = -23.0
PEAK_CEIL_DB = -7.0


# ----------------------------------------------------------------- helpers --

def loop_len(seconds: float) -> int:
    return int(round(seconds * SR / FRAME)) * FRAME


def shaped_noise(n: int, rng: np.random.Generator, lo: float, hi: float,
                 tilt: float = 0.0, soft: float = 0.25) -> np.ndarray:
    """Periodic noise band-limited to [lo, hi] Hz with soft (log-gaussian-ish)
    skirts; `tilt` dB/octave slope (negative = darker). Unit RMS."""
    freqs = np.fft.rfftfreq(n, 1.0 / SR)
    spec = rng.normal(size=freqs.size) + 1j * rng.normal(size=freqs.size)
    f = np.maximum(freqs, 1.0)
    lf = np.log2(f)
    w = np.ones_like(f)
    w *= 1.0 / (1.0 + np.exp(-(lf - np.log2(lo)) / soft))
    w *= 1.0 / (1.0 + np.exp((lf - np.log2(hi)) / soft))
    w *= 10 ** ((tilt * (lf - np.log2(lo))) / 20.0)
    spec *= w
    spec[0] = 0
    x = np.fft.irfft(spec, n)
    return x / (np.sqrt(np.mean(x ** 2)) or 1.0)


def slow_lfo(n: int, rng: np.random.Generator, cycles: tuple[int, ...],
             depth: float = 1.0) -> np.ndarray:
    """Sum of whole-cycle sinusoids (periodic over n) mapped to 0..1."""
    t = np.arange(n) / n
    y = np.zeros(n)
    for c in cycles:
        y += np.sin(2 * np.pi * (c * t + rng.random())) / len(cycles)
    y = (y - y.min()) / ((y.max() - y.min()) or 1.0)
    return 1.0 - depth + depth * y


def place(buf: np.ndarray, ev: np.ndarray, at: int) -> None:
    """Add `ev` into `buf` starting at sample `at`, wrapping around the seam."""
    n = buf.size
    idx = (at + np.arange(ev.size)) % n
    np.add.at(buf, idx, ev)


def circ_reverb(x: np.ndarray, rng: np.random.Generator, seconds: float,
                lp_hz: float, mix: float) -> np.ndarray:
    """Circular convolution with a decaying, darkened noise tail (seamless)."""
    n = x.size
    m = min(n, int(seconds * SR))
    t = np.arange(m) / SR
    ir = rng.normal(size=m) * np.exp(-6.9 * t / seconds)
    # darken the tail
    k = max(1, int(SR / lp_hz))
    ir = np.convolve(ir, np.ones(k) / k, mode="same")
    ir /= np.sqrt(np.sum(ir ** 2)) or 1.0
    full = np.zeros(n)
    full[:m] = ir
    wet = np.fft.irfft(np.fft.rfft(x) * np.fft.rfft(full), n)
    return (1 - mix) * x + mix * wet


def env_ad(n: int, attack: float, decay: float) -> np.ndarray:
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-np.maximum(t - attack, 0) / max(decay, 1e-4))


def bumps(n: int, rng: np.random.Generator, times: list[float], width: float,
          rise: float = 0.35) -> np.ndarray:
    """Periodic envelope of smooth swells (raised-cosine rise, longer fall)
    centred at `times` (fractions of the loop), wrapping the seam."""
    out = np.zeros(n)
    w = int(width * SR)
    r = int(w * rise)
    shape = np.concatenate([
        0.5 - 0.5 * np.cos(np.linspace(0, np.pi, r, endpoint=False)),
        0.5 + 0.5 * np.cos(np.linspace(0, np.pi, w - r)),
    ])
    for t in times:
        place(out, shape * (0.75 + 0.25 * rng.random()), int(t * n))
    return out


# ------------------------------------------------------------------- beds --

def bed_surf(rng: np.random.Generator) -> np.ndarray:
    """Coast/harbour: slow swells breaking on the shore, foam hiss trailing each."""
    n = loop_len(16)
    times = [0.03, 0.27, 0.49, 0.76]
    swell = bumps(n, rng, times, width=4.6, rise=0.45)
    foam_env = np.roll(bumps(n, rng, times, width=3.2, rise=0.25), int(1.4 * SR))
    body = shaped_noise(n, rng, 120, 900, tilt=-3) * (0.25 + 0.75 * swell)
    foam = shaped_noise(n, rng, 1500, 5200, tilt=-4) * (0.08 + 0.55 * foam_env)
    under = shaped_noise(n, rng, 40, 160) * 0.35 * slow_lfo(n, rng, (1, 3), 0.5)
    return circ_reverb(body + foam + under, rng, 1.2, 3000, 0.25)


def bed_marsh(rng: np.random.Generator) -> np.ndarray:
    """Fen: soft water lapping, reeds stirring, a distant frog now and then."""
    n = loop_len(18)
    lap_times = list(np.sort(rng.uniform(0, 1, 11)))
    lap = shaped_noise(n, rng, 180, 700, tilt=-4) * (0.15 + 0.6 * bumps(n, rng, lap_times, 0.9, 0.3))
    reeds = shaped_noise(n, rng, 2200, 6000, tilt=-3) * 0.22 * slow_lfo(n, rng, (2, 5, 7), 0.85)
    air = shaped_noise(n, rng, 60, 300) * 0.25
    frogs = np.zeros(n)
    for at, f0, pulses in ((0.21, 170.0, 3), (0.64, 150.0, 2), (0.71, 176.0, 3)):
        call = []
        for p in range(pulses):
            m = int(0.07 * SR)
            t = np.arange(m) / SR
            f = f0 * (1 + 0.08 * np.sin(2 * np.pi * 34 * t))
            tone = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + np.sin(2 * np.pi * np.cumsum(f) / SR)
            call.append(tone * env_ad(m, 0.008, 0.03) * (1 - 0.15 * p))
            call.append(np.zeros(int(0.05 * SR)))
        c = np.concatenate(call)
        k = 14  # muffle: a distant frog, not a close one
        c = np.convolve(c, np.ones(k) / k, mode="same")
        place(frogs, c * 0.55, int(at * n))
    frogs = circ_reverb(frogs, rng, 0.9, 1500, 0.55)
    return lap + reeds + air + frogs


def bed_wind(rng: np.random.Generator) -> np.ndarray:
    """High places: a low steady blow with slow gusts and a faint shifting whistle."""
    n = loop_len(20)
    gust = slow_lfo(n, rng, (1, 2, 3), 0.8)
    base = shaped_noise(n, rng, 70, 600, tilt=-5) * (0.35 + 0.65 * gust)
    hiss = shaped_noise(n, rng, 900, 3500, tilt=-6) * 0.25 * gust ** 2
    whistle = np.zeros(n)
    for centre, cyc in ((520, (2, 3)), (780, (3, 4)), (1100, (1, 5))):
        band = shaped_noise(n, rng, centre * 0.93, centre * 1.07, soft=0.05)
        whistle += band * 0.12 * slow_lfo(n, rng, cyc, 1.0) ** 3 * gust
    return base + hiss + whistle


def bed_drips(rng: np.random.Generator) -> np.ndarray:
    """Caves: a deep, still room tone with sparse echoing water drips."""
    n = loop_len(14)
    room = shaped_noise(n, rng, 35, 220, tilt=-4) * 0.5 * slow_lfo(n, rng, (1, 2), 0.3)
    drips = np.zeros(n)
    spots = [0.06, 0.19, 0.24, 0.43, 0.58, 0.71, 0.87]
    for at in spots:
        m = int(0.09 * SR)
        t = np.arange(m) / SR
        f0 = rng.uniform(900, 1700)
        f = f0 * (1 + 0.9 * (1 - np.exp(-t / 0.012)))  # the "plink" upward bend
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(m, 0.001, 0.022)
        place(drips, tone * rng.uniform(0.45, 1.0), int(at * n))
    drips = circ_reverb(drips, rng, 1.8, 2500, 0.6)
    return room + drips * 1.6


def bed_crickets(rng: np.random.Generator) -> np.ndarray:
    """Night meadows/towns: still night air and a few crickets at different rates."""
    n = loop_len(12)
    air = shaped_noise(n, rng, 80, 500, tilt=-4) * 0.35 * slow_lfo(n, rng, (1, 2), 0.4)
    crick = np.zeros(n)
    for carrier, period, pulses, level, phase in (
        (4400.0, 0.92, 3, 1.0, 0.0),
        (4950.0, 1.37, 4, 0.55, 0.31),
        (3900.0, 2.05, 2, 0.35, 0.67),
    ):
        count = max(1, int(round(n / SR / period)))  # whole calls per loop -> regular, seamless rhythm
        for i in range(count):
            at = (phase + i) / count + rng.uniform(-0.004, 0.004)
            call = []
            for p in range(pulses):
                m = int(0.016 * SR)
                t = np.arange(m) / SR
                call.append(np.sin(2 * np.pi * carrier * t) * np.sin(np.pi * t / t[-1]) ** 2)
                call.append(np.zeros(int(0.018 * SR)))
            place(crick, np.concatenate(call) * level * rng.uniform(0.7, 1.0), int(at * n) % n)
    crick = circ_reverb(crick, rng, 0.7, 4000, 0.35) * slow_lfo(n, rng, (1,), 0.35)
    return air + crick * 0.5


BEDS = {
    "amb-surf": (bed_surf, 101),
    "amb-marsh": (bed_marsh, 202),
    "amb-wind": (bed_wind, 303),
    "amb-drips": (bed_drips, 404),
    "amb-crickets": (bed_crickets, 505),
}


# ------------------------------------------------------------------ output --

def master(x: np.ndarray) -> np.ndarray:
    x = x - x.mean()
    x *= 10 ** (TARGET_RMS_DB / 20) / (np.sqrt(np.mean(x ** 2)) or 1.0)
    ceil = 10 ** (PEAK_CEIL_DB / 20)
    peak = np.max(np.abs(x))
    if peak > ceil:  # soft-limit the rare transient rather than turn the whole bed down
        x = np.tanh(x / ceil) * ceil
    return x


def ffmpeg_bin() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        sys.exit("ambient_beds: needs ffmpeg on PATH (or `pip install imageio-ffmpeg`).")


def write_wav(path: Path, x: np.ndarray) -> None:
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def write_mp3(path: Path, x: np.ndarray) -> None:
    with tempfile.TemporaryDirectory() as d:
        wav = Path(d) / "bed.wav"
        write_wav(wav, x)
        subprocess.run([ffmpeg_bin(), "-y", "-v", "error", "-i", str(wav), "-codec:a", "libmp3lame",
                        "-b:a", "64k", "-ac", "1", str(path)], check=True)


def refresh_manifest() -> None:
    stems = sorted(p.stem for p in SFX_DIR.glob("*.mp3"))
    (SFX_DIR / "sfx.manifest.json").write_text(json.dumps({"stems": stems}, indent=2) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("beds", nargs="*", help=f"subset of {', '.join(BEDS)} (default: all)")
    ap.add_argument("--wav-dir", type=Path, help="also write .wav previews here")
    args = ap.parse_args()
    for stem in args.beds or list(BEDS):
        fn, seed = BEDS[stem]
        x = master(fn(np.random.default_rng(seed)))
        write_mp3(SFX_DIR / f"{stem}.mp3", x)
        if args.wav_dir:
            args.wav_dir.mkdir(parents=True, exist_ok=True)
            write_wav(args.wav_dir / f"{stem}.wav", x)
        rms = 20 * np.log10(np.sqrt(np.mean(x ** 2)))
        print(f"{stem}: {x.size / SR:.2f} s, rms {rms:.1f} dBFS, peak {20 * np.log10(np.max(np.abs(x))):.1f} dBFS")
    refresh_manifest()


if __name__ == "__main__":
    main()
