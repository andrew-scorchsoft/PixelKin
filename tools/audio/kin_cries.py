#!/usr/bin/env python3
"""Render every kin's CRY — a short, original chip-voice call (0.4–0.9 s).

Deterministic and data-driven: each cry is derived from the kin's species file
(src/game/data/species/NNN_slug.json), so the whole roster is covered and a
re-run reproduces the same sound (modulo the mp3 encoder):

  * TYPE -> timbre. The primary type picks the oscillator voice (pulse duty,
    triangle, square pair…) and its "trick" (Ember crackle, Tide bubble-blips,
    Stone grit, Storm zap, Frost shimmer, Solar octave brass, Lunar echo, Light
    bell sparkle, Dark growl). A second type adds a quieter harmony voice and
    its own noise colour.
  * SIZE / WEIGHT -> register and length. Small kin squeak high and short; big
    kin call low and long.
  * KINDLING STAGE -> richer + longer + a little lower. Each stage of a line
    keeps the SAME contour family and motif (seeded from the line's root slug),
    so a kindled kin is recognisably its younger self, grown up.
  * A hash of the slug -> per-kin variation (syllable count, interval, vibrato),
    so no two cries are the same.

Era-authentic on purpose: naive (aliased) pulse/triangle oscillators, a 15-bit
LFSR noise channel, 15-step volume envelopes (the handheld volume register),
then a gentle low-pass. Mastered to a common loudness (RMS of the voiced part)
with a soft peak ceiling, so a tiny chirp and a great bellow sit at the same
level in game.

    python3 tools/audio/kin_cries.py                 # render all 164
    python3 tools/audio/kin_cries.py 26 27 149       # just these ids
    python3 tools/audio/kin_cries.py --wav-dir /tmp  # also keep .wav previews

Writes public/assets/audio/sfx/cry-NNN.mp3 (3-digit id — a 1-char suffix would
read as an a/b/c variant in Sfx.ts) and refreshes sfx.manifest.json. Played via
`playCry()` in src/game/systems/audio/cries.ts. Needs numpy + ffmpeg (PATH, else
imageio-ffmpeg). Original material only — every sound here is synthesised.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
import zlib
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambient_beds import ffmpeg_bin, refresh_manifest, write_wav  # noqa: E402

import subprocess  # noqa: E402

SR = 22050
ROOT = Path(__file__).resolve().parents[2]
SPECIES_DIR = ROOT / "src" / "game" / "data" / "species"
SFX_DIR = ROOT / "public" / "assets" / "audio" / "sfx"

TARGET_RMS_DB = -15.0   # voiced-part RMS — in line with the ui/battle one-shots
PEAK_CEIL_DB = -1.0


def crc(s: str) -> int:
    return zlib.crc32(s.encode("utf-8")) & 0xFFFFFFFF


# ------------------------------------------------------------- oscillators --

def pulse(phase: np.ndarray, duty: float) -> np.ndarray:
    return np.where((phase % 1.0) < duty, 1.0, -1.0)


def tri(phase: np.ndarray) -> np.ndarray:
    p = phase % 1.0
    # 4-bit stepped triangle, like the handheld wave channel
    t = 4 * np.abs(p - 0.5) - 1
    return np.round(t * 7.5) / 7.5


def saw(phase: np.ndarray) -> np.ndarray:
    return 2 * (phase % 1.0) - 1


def lfsr_noise(n: int, rate_hz: float, seed: int, short: bool = False) -> np.ndarray:
    """The chip noise channel: a 15-bit (or 7-bit 'short', metallic) LFSR clocked at rate_hz."""
    reg = (seed & 0x7FFF) or 1
    hold = max(1, int(SR / max(50.0, rate_hz)))
    steps = n // hold + 2
    bits = np.empty(steps)
    for i in range(steps):
        b = (reg ^ (reg >> 1)) & 1
        reg = (reg >> 1) | (b << 14)
        if short:
            reg = (reg & ~(1 << 6)) | (b << 6)
        bits[i] = 1.0 if reg & 1 else -1.0
    return np.repeat(bits, hold)[:n]


def phase_from_freq(f: np.ndarray) -> np.ndarray:
    return np.cumsum(f) / SR


def quant_env(env: np.ndarray) -> np.ndarray:
    """15-step volume register."""
    return np.round(np.clip(env, 0, 1) * 15) / 15


def lowpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    a = math.exp(-2 * math.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def highpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    return x - lowpass(x, cutoff)


# --------------------------------------------------------------- contours --
# A contour = list of syllables; each syllable is (start, end) in [0,1] of the
# cry plus a pitch path (semitone offsets at evenly spaced points through it).
# `k` = per-kin interval scale, `rng` = per-kin variation, `motif` = line rng.

def c_yip(motif, rng, k):
    n = int(motif.integers(2, 4))
    syl, t = [], 0.0
    w = 0.86 / n
    for i in range(n):
        up = 5 + motif.integers(0, 4)
        syl.append((t, t + w * 0.78, [0, up * k, (up - 2) * k]))
        t += w
    return syl


def c_howl(motif, rng, k):
    peak = 4 + motif.integers(0, 4)
    return [(0.0, 1.0, [-2 * k, peak * k, peak * k, (peak - 3) * k, -8 * k])]


def c_trill(motif, rng, k):
    n = int(motif.integers(3, 6))
    step = -(1 + motif.integers(1, 3))
    syl, w = [], 0.95 / n
    for i in range(n):
        base = i * step * k + (2 if i == 0 else 0)
        syl.append((i * w, i * w + w * 0.62, [base + 3 * k, base]))
    return syl


def c_warble(motif, rng, k):
    end = -5 - motif.integers(0, 5)
    return [(0.0, 0.92, [0, 2 * k, 0, 2 * k, 0, end * k])]


def c_bark(motif, rng, k):
    n = int(motif.integers(1, 3))
    syl, w = [], 0.9 / n
    for i in range(n):
        syl.append((i * w + 0.02, i * w + w * 0.85, [3 * k, 0, -9 * k]))
    return syl


def c_coo(motif, rng, k):
    rise = 3 + motif.integers(0, 3)
    return [(0.0, 0.48, [0, rise * k, rise * k - 1]), (0.52, 1.0, [rise * k - 2, -3 * k])]


def c_screech(motif, rng, k):
    top = 9 + motif.integers(0, 5)
    return [(0.0, 1.0, [-5 * k, top * k, top * k, top * k - 1, (top - 12) * k])]


def c_burble(motif, rng, k):
    n = int(motif.integers(4, 7))
    syl, w = [], 0.96 / n
    for i in range(n):
        a = float(motif.integers(-3, 8)) * k
        syl.append((i * w, i * w + w * 0.7, [a, a + 2 * k]))
    return syl


def c_swoop(motif, rng, k):
    low = -6 - motif.integers(0, 4)
    return [(0.0, 1.0, [4 * k, low * k, low * k, 3 * k, 6 * k])]


CONTOURS = [c_yip, c_howl, c_trill, c_warble, c_bark, c_coo, c_screech, c_burble, c_swoop]


# ------------------------------------------------------------------ voices --

TYPE_VOICE = {
    # wave, duty, vibrato (rate Hz, depth semis), noise (rate, level, short)
    "Ember":   ("pulse", 0.25, (9.0, 0.30), (3800, 0.10, False)),
    "Tide":    ("tri",   0.5,  (6.0, 0.45), (900,  0.05, False)),
    "Verdant": ("pulse", 0.5,  (5.0, 0.20), (1500, 0.06, False)),
    "Stone":   ("pulse", 0.5,  (0.0, 0.0),  (700,  0.20, False)),
    "Storm":   ("saw",   0.125, (14.0, 0.35), (9000, 0.16, False)),
    "Frost":   ("pulse", 0.125, (11.0, 0.15), (11000, 0.07, True)),
    "Solar":   ("pulse", 0.5,  (5.5, 0.18), (2500, 0.04, False)),
    "Lunar":   ("tri",   0.5,  (3.5, 0.40), (1200, 0.04, False)),
    "Light":   ("pulse", 0.25, (7.0, 0.15), (7000, 0.04, True)),
    "Dark":    ("pulse", 0.375, (4.0, 0.25), (500,  0.14, False)),
}


def osc(wave: str, phase: np.ndarray, duty: float) -> np.ndarray:
    if wave == "tri":
        return tri(phase)
    if wave == "saw":
        return saw(phase)
    return pulse(phase, duty)


def load_species() -> dict[int, dict]:
    out = {}
    for f in sorted(SPECIES_DIR.glob("*.json")):
        s = json.loads(f.read_text())
        out[s["id"]] = s
    return out


def line_root(s: dict, roster: dict[int, dict]) -> dict:
    seen = set()
    while s.get("from") and s["from"] in roster and s["id"] not in seen:
        seen.add(s["id"])
        s = roster[s["from"]]
    return s


def render_cry(s: dict, roster: dict[int, dict]) -> np.ndarray:
    root = line_root(s, roster)
    motif = np.random.default_rng(crc("line:" + root["slug"]))
    rng = np.random.default_rng(crc("kin:" + s["slug"]))
    types = s["types"]
    stage = int(s.get("stage") or 1)
    legendary = s.get("tier") == "F" or (s.get("tier") == "E" and stage == 1 and not s.get("kindling"))
    size = max(5.0, float(s["dex"].get("size_cm") or 40))
    weight = max(0.01, float(s["dex"].get("weight_kg") or 10))

    sz = min(1.0, max(0.0, math.log(size / 10) / math.log(400 / 10)))
    wt = min(1.0, max(0.0, (math.log10(weight) + 1) / 4.5))
    reg = 0.6 * sz + 0.4 * wt
    base = 1150 * 2 ** (-reg * 2.6) * 0.94 ** (stage - 1)
    base *= 2 ** (float(rng.uniform(-1.5, 1.5)) / 12)
    if types[0] == "Frost":
        base *= 1.12
    if types[0] in ("Stone", "Dark"):
        base *= 0.9
    dur = 0.40 + 0.26 * reg + 0.07 * (stage - 1) + (0.12 if legendary else 0.0)
    dur = min(0.85 if ("Lunar" in types or legendary) else 0.9, max(0.4, dur))
    n = int(SR * dur)
    t = np.arange(n) / SR

    contour = CONTOURS[crc("contour:" + root["slug"]) % len(CONTOURS)]
    k = float(rng.uniform(0.8, 1.2)) * (0.85 if stage > 1 else 1.0)
    syllables = contour(motif, rng, k)

    wave, duty, (vr, vd), (nrate, nlev, nshort) = TYPE_VOICE[types[0]]
    duty = duty if wave != "pulse" else [0.125, 0.25, 0.5, 0.375][int(rng.integers(0, 4))] if types[0] in ("Verdant", "Solar") else duty
    vd *= float(rng.uniform(0.7, 1.3))
    vr *= float(rng.uniform(0.85, 1.15))

    semis = np.full(n, np.nan)
    gate = np.zeros(n)
    for (a, b, path) in syllables:
        i0, i1 = int(a * n), max(int(a * n) + 8, int(b * n))
        i1 = min(n, i1)
        m = i1 - i0
        if m <= 0:
            continue
        xs = np.linspace(0, 1, len(path))
        semis[i0:i1] = np.interp(np.linspace(0, 1, m), xs, np.asarray(path, dtype=float))
        att = max(1, int(0.006 * SR))
        rel = max(1, int(min(0.06, 0.35 * m / SR) * SR))
        env = np.ones(m)
        env[:att] = np.linspace(0, 1, att)
        env[-rel:] = np.minimum(env[-rel:], np.linspace(1, 0, rel))
        # a little decay inside each syllable (the "punch")
        env *= 1 - 0.35 * np.linspace(0, 1, m) ** 1.5
        gate[i0:i1] = np.maximum(gate[i0:i1], env)
    # hold pitch through gaps so the phase stays smooth
    idx = np.where(~np.isnan(semis), np.arange(n), 0)
    np.maximum.accumulate(idx, out=idx)
    semis = np.nan_to_num(semis[idx], nan=0.0)

    if types[0] == "Stone":
        semis = np.round(semis)  # gritty, stepped
    vib = vd * np.sin(2 * np.pi * vr * t) * np.clip(t / 0.08, 0, 1)
    freq = base * 2 ** ((semis + vib) / 12)

    env_q = quant_env(gate)
    voice = osc(wave, phase_from_freq(freq), duty)

    # --- the primary type's trick
    if types[0] == "Solar":
        voice = 0.75 * voice + 0.35 * pulse(phase_from_freq(freq * 2), 0.5)
    if types[0] == "Dark":
        voice = 0.6 * voice + 0.5 * pulse(phase_from_freq(freq * 1.012), duty)
        voice *= 0.75 + 0.25 * np.sign(np.sin(2 * np.pi * 28 * t))  # growl
    if types[0] == "Light":
        bell = np.sin(2 * np.pi * phase_from_freq(freq * 2.0)) * np.exp(-t * 6)
        voice = 0.8 * voice + 0.5 * bell
        # end sparkle: octave flips
        tail = t > dur * 0.7
        flip = (np.floor(t / 0.035) % 2 == 0) & tail
        voice = np.where(flip, osc(wave, phase_from_freq(freq * 2), duty), voice)
    if types[0] == "Tide":
        # bubble blips: a quick upward chirp at each syllable onset
        on = np.diff(np.concatenate([[0], (gate > 0).astype(int)])) > 0
        blip = np.zeros(n)
        for i0 in np.where(on)[0]:
            m = min(n - i0, int(0.03 * SR))
            blip[i0:i0 + m] = np.linspace(7, 0, m)
        voice = osc(wave, phase_from_freq(base * 2 ** ((semis + vib + blip) / 12)), duty)
        voice = 0.75 * voice + 0.3 * pulse(phase_from_freq(freq * 0.5), 0.5)

    out = env_q * voice

    # --- second type: a quieter harmony voice
    if len(types) > 1:
        w2, d2, _, (nr2, nl2, ns2) = TYPE_VOICE[types[1]]
        interval = [7, 12, 5, -12, 4][crc("iv:" + s["slug"]) % 5]
        v2 = osc(w2, phase_from_freq(freq * 2 ** (interval / 12)), d2)
        out = out + 0.32 * quant_env(gate * 0.9) * v2
        nrate = (nrate + nr2) / 2
        nlev = nlev + 0.5 * nl2
        nshort = nshort or ns2

    # --- kindled richness: a detuned unison / sub voice
    if stage >= 2:
        rich = 0.22 + 0.08 * (stage - 2)
        sub = pulse(phase_from_freq(freq * (0.5 if stage >= 3 else 1.006)), 0.5)
        out = out + rich * quant_env(gate) * sub
    if legendary:
        out = out + 0.25 * quant_env(gate) * tri(phase_from_freq(freq * 0.5))

    # --- noise channel
    noise = lfsr_noise(n, nrate * float(rng.uniform(0.8, 1.25)), crc("nz:" + s["slug"]), nshort)
    nenv = gate.copy()
    if types[0] in ("Stone", "Storm", "Dark") or "Stone" in types:
        # a burst at the head of each syllable
        on = np.diff(np.concatenate([[0], (gate > 0).astype(int)])) > 0
        burst = np.zeros(n)
        for i0 in np.where(on)[0]:
            m = min(n - i0, int(0.05 * SR))
            burst[i0:i0 + m] = np.linspace(1, 0, m) ** 2
        nenv = 0.4 * nenv + 2.2 * burst
    if types[0] == "Ember":
        crackle = (rng.random(n) < 0.004).astype(float)
        crackle = np.convolve(crackle, np.ones(60) / 6, mode="same")
        nenv = 0.3 * nenv + crackle * (gate > 0)
    out = out + nlev * quant_env(np.clip(nenv, 0, 1)) * noise

    # --- Lunar echo; legendary room
    if "Lunar" in types or legendary:
        d = int(0.085 * SR)
        echo = np.zeros(n + 3 * d)
        echo[:n] = out
        for j in range(1, 4):
            echo[j * d:j * d + n] += out * (0.38 ** j)
        out = echo[:n + int(0.05 * SR)]
        out[n:] *= np.linspace(1, 0, out.size - n)

    # soften the very top (the speaker), lift out DC
    out = lowpass(out, 7000 if types[0] not in ("Frost", "Storm") else 9000)
    out = highpass(out, 70)
    # declick both ends
    fade = int(0.004 * SR)
    out[:fade] *= np.linspace(0, 1, fade)
    out[-fade:] *= np.linspace(1, 0, fade)
    return out


def master(x: np.ndarray) -> np.ndarray:
    voiced = np.abs(x) > 1e-3
    ref = x[voiced] if voiced.any() else x
    rms = math.sqrt(float(np.mean(ref ** 2))) or 1e-9
    x = x * (10 ** (TARGET_RMS_DB / 20) / rms)
    ceil = 10 ** (PEAK_CEIL_DB / 20)
    if np.max(np.abs(x)) > ceil * 0.7:
        knee = ceil * 0.7
        over = np.abs(x) > knee
        x = np.where(over, np.sign(x) * (knee + (ceil - knee) * np.tanh((np.abs(x) - knee) / (ceil - knee))), x)
    return x


def write_mp3(path: Path, x: np.ndarray) -> None:
    with tempfile.TemporaryDirectory() as d:
        wav = Path(d) / "cry.wav"
        write_wav(wav, x)
        subprocess.run([ffmpeg_bin(), "-y", "-v", "error", "-i", str(wav), "-codec:a", "libmp3lame",
                        "-b:a", "64k", "-ac", "1", str(path)], check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*", type=int, help="species ids (default: all)")
    ap.add_argument("--wav-dir", type=Path, help="also write .wav previews here")
    args = ap.parse_args()
    roster = load_species()
    ids = args.ids or sorted(roster)
    for sid in ids:
        s = roster[sid]
        x = master(render_cry(s, roster))
        stem = f"cry-{sid:03d}"
        write_mp3(SFX_DIR / f"{stem}.mp3", x)
        if args.wav_dir:
            args.wav_dir.mkdir(parents=True, exist_ok=True)
            write_wav(args.wav_dir / f"{stem}_{s['slug']}.wav", x)
        peak = 20 * math.log10(float(np.max(np.abs(x))) or 1e-9)
        print(f"{stem} {s['name']:<12} {'/'.join(s['types']):<14} st{s.get('stage')} "
              f"{x.size / SR:.2f}s peak {peak:.1f} dBFS")
    refresh_manifest()


if __name__ == "__main__":
    main()
