#!/usr/bin/env python3
"""
generate-midi — toolkit for the PixelKin MIDI-music skill.

Two jobs, two subcommands (plus helpers):

  build    A declarative JSON *song spec* (Claude is the composer) -> a real
           .mid file. Maps note names + durations to MIDI events, writes General
           MIDI program changes for portable playback, embeds loop markers, and
           validates the arrangement against the chosen era's hardware limits
           (voice count, "no chords" eras, tempo range) — warnings, not errors,
           so you can bend a rule on purpose.

  render   A .mid -> .wav / .mp3 using a built-in, dependency-light *chiptune
           synthesizer* (numpy): pulse waves with duty cycles, triangle bass,
           4-bit "wave", saw/strings/pad, bells, and a noise drum kit. This is
           deliberately NOT a generic General-MIDI soundfont — the chip timbres
           are what make the era sound iconic. Optional --engine soundfont uses
           fluidsynth + an .sf2 if you have one (lusher SNES/orchestral colour).
           MP3 encoding uses the ffmpeg bundled by imageio-ffmpeg (no apt).

  presets  List form presets (title/overworld/battle/...), eras, and voices.
  schema   Print the song-spec format + a worked example.

The script does NOT judge musicality. The calling agent composes the spec,
builds, renders, *listens*, and iterates. See SKILL.md and references/.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import wave
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROFILES_PATH = SCRIPT_DIR / "profiles.json"

SAMPLE_RATE = 44100


def _repo_root() -> Path:
    """Walk up from this script to the repo root (a dir with .git / requirements.txt)."""
    for d in SCRIPT_DIR.parents:
        if (d / ".git").exists() or (d / "requirements.txt").is_file():
            return d
    return SCRIPT_DIR.parents[-1]


# Soundfonts live with the MIDI sources, not in the served bundle, and are
# gitignored (too big to commit). fetch_soundfont.py populates this folder.
SOUNDFONT_DIR = _repo_root() / "assets" / "audio" / "midi" / "soundfonts"
# Preferred default soundfont filename, if several are present.
DEFAULT_SOUNDFONT = "GeneralUser-GS.sf2"


def resolve_default_soundfont() -> str | None:
    if not SOUNDFONT_DIR.is_dir():
        return None
    preferred = SOUNDFONT_DIR / DEFAULT_SOUNDFONT
    if preferred.is_file():
        return str(preferred)
    found = sorted(SOUNDFONT_DIR.glob("*.sf2"))
    return str(found[0]) if found else None
DRUM_CHANNEL = 9  # GM channel 10 (0-indexed)
# Pitch-bend range (± semitones) our writer/synth agree on for glide "sweeps".
# Wide enough for octave-plus SFX slides; written into the .mid as a text meta.
BEND_RANGE = 24
BEND_STEPS = 24  # bend control points emitted across a glide note
NOISE_DENSITY = 8.0  # pitched-noise grain: new random per (freq * this) per second

# Quarter-note-relative durations for the compact note DSL.
DUR_BEATS = {"w": 4.0, "h": 2.0, "q": 1.0, "e": 0.5, "s": 0.25}
NOTE_SEMITONE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


# --------------------------------------------------------------------------- #
# Data
# --------------------------------------------------------------------------- #
def load_profiles() -> dict:
    with PROFILES_PATH.open() as f:
        return json.load(f)


def _meta_text(s: str) -> str:
    """MIDI meta strings are latin-1; titles/track-names often carry em-dashes or
    curly quotes. Normalise the common offenders, then drop anything still
    un-encodable so a stray glyph never crashes `build`."""
    s = (s.replace("—", "-").replace("–", "-")
          .replace("‘", "'").replace("’", "'")
          .replace("“", '"').replace("”", '"'))
    return s.encode("latin-1", "replace").decode("latin-1")


# --------------------------------------------------------------------------- #
# Note / duration parsing
# --------------------------------------------------------------------------- #
def pitch_to_midi(token: str, default_octave: int) -> int:
    """'C4' / 'F#3' / 'Bb5' / 'A' (uses default_octave) -> MIDI number (C4=60)."""
    m = re.fullmatch(r"([A-G])([#b]?)(-?\d+)?", token)
    if not m:
        raise ValueError(f"bad pitch '{token}' (want like C4, F#3, Bb5)")
    letter, acc, octs = m.group(1), m.group(2), m.group(3)
    semi = NOTE_SEMITONE[letter] + (1 if acc == "#" else -1 if acc == "b" else 0)
    octave = int(octs) if octs is not None else default_octave
    midi = 12 * (octave + 1) + semi
    if not 0 <= midi <= 127:
        raise ValueError(f"pitch '{token}' out of MIDI range 0..127")
    return midi


def _split_dur(token: str) -> tuple[str, float, int | None]:
    """Strip a trailing @velocity and a duration suffix off a token.

    Returns (body, beats_or_-1, velocity_or_None). beats == -1 means "inherit
    the previous token's duration" (tracker convention). Duration suffix grammar:
    one of w/h/q/e/s, optional '.' (dotted) / '..' (double-dotted), optional 't'
    (triplet). Note letters are UPPER-case so the lower-case duration letters are
    never ambiguous.
    """
    vel: int | None = None
    mvel = re.search(r"@(\d+)$", token)
    if mvel:
        vel = max(1, min(127, int(mvel.group(1))))
        token = token[: mvel.start()]

    mdur = re.search(r"([whqes])(\.{0,2})(t?)$", token)
    if not mdur:
        return token, -1.0, vel
    base = DUR_BEATS[mdur.group(1)]
    dots = len(mdur.group(2))
    if dots == 1:
        base *= 1.5
    elif dots == 2:
        base *= 1.75
    if mdur.group(3) == "t":
        base *= 2.0 / 3.0
    return token[: mdur.start()], base, vel


def parse_notes(notes, *, default_octave: int, drums: bool, drum_map: dict) -> list[dict]:
    """Parse a track's notes (compact string DSL or list form) into events:
    [{midi: [ints] | drum-names, beats: float, vel: int}], rests -> midi [].
    """
    if isinstance(notes, list):
        return _parse_list(notes, default_octave, drums, drum_map)
    return _parse_dsl(str(notes), default_octave, drums, drum_map)


def _drum_gm(name: str, drum_map: dict) -> int:
    if name not in drum_map or name.startswith("_"):
        known = ", ".join(k for k in drum_map if not k.startswith("_"))
        raise ValueError(f"unknown drum '{name}'. Known: {known}")
    return int(drum_map[name]["gm"])


def _parse_dsl(text: str, default_octave: int, drums: bool, drum_map: dict) -> list[dict]:
    valid_drums = {k for k in drum_map if not k.startswith("_")}
    out: list[dict] = []
    last_beats = 1.0
    for raw in text.replace("|", " ").split():
        tok = raw.strip()
        if not tok:
            continue
        body, beats, vel = _split_dur(tok)

        # A standalone duration token ("e", "q.", "h"...) sets the running note
        # duration for everything after it (tracker-style), so "e kick hat snare"
        # is three eighth-note hits. Rests must be written explicitly (r / -).
        if body == "" and beats >= 0 and tok not in ("r", "-"):
            last_beats = beats
            continue

        if drums and body not in ("r", "-", ""):
            # Drum names are whole words; some end in a duration letter (e.g.
            # "crash" ends in 'h'). If stripping a duration left an invalid drum,
            # the token had no explicit duration — keep the whole word, inherit.
            if not all(p in valid_drums for p in body.split("+")):
                stripped = re.sub(r"@\d+$", "", tok)
                if all(p in valid_drums for p in stripped.split("+")):
                    body, beats = stripped, -1.0

        if beats < 0:
            beats = last_beats
        last_beats = beats
        if body in ("r", "-", ""):
            out.append({"midi": [], "beats": beats, "vel": 0})
            continue
        # Pitch GLIDE (the chip "sweep"): "C6~C4" bends from the first pitch to
        # the second over the note's duration. Monophonic; not for drums.
        glide_to = None
        if not drums and "~" in body:
            head, _, tail = body.partition("~")
            body = head
            glide_to = pitch_to_midi(tail, default_octave)
        parts = body.split("+")
        if drums:
            midis = [_drum_gm(p, drum_map) for p in parts]
        else:
            midis = [pitch_to_midi(p, default_octave) for p in parts]
        out.append({"midi": midis, "beats": beats,
                    "vel": vel if vel is not None else 96, "glide": glide_to})
    return out


def _parse_list(items: list, default_octave: int, drums: bool, drum_map: dict) -> list[dict]:
    out: list[dict] = []
    for it in items:
        beats = float(it.get("beats", 1.0))
        vel = int(it.get("vel", 96))
        pitch = it.get("pitch", "rest")
        if pitch in ("rest", "r", None, ""):
            out.append({"midi": [], "beats": beats, "vel": 0})
            continue
        plist = pitch if isinstance(pitch, list) else [pitch]
        glide = it.get("glide_to", it.get("glide"))
        glide_to = pitch_to_midi(glide, default_octave) if glide and not drums else None
        if drums:
            midis = [_drum_gm(p, drum_map) for p in plist]
        else:
            midis = [pitch_to_midi(p, default_octave) for p in plist]
        out.append({"midi": midis, "beats": beats, "vel": vel, "glide": glide_to})
    return out


# --------------------------------------------------------------------------- #
# build: spec -> .mid
# --------------------------------------------------------------------------- #
def build_midi(spec: dict, profiles: dict) -> tuple[object, dict]:
    import mido

    eras = profiles["eras"]
    voices = profiles["voices"]
    drum_map = profiles["drum_map"]

    era_key = spec.get("era", "gbc")
    era = eras.get(era_key)
    if era is None:
        raise SystemExit(f"unknown era '{era_key}'. Choose from: {', '.join(eras)}")

    tempo = int(spec.get("tempo", era.get("tempo_range", [120, 120])[0]))
    ppq = int(spec.get("ppq", 480))
    ts = spec.get("time_signature", [4, 4])
    loop = bool(spec.get("loop", True))
    title = spec.get("title", "untitled")

    mid = mido.MidiFile(ticks_per_beat=ppq)

    # Meta track: name, tempo, time signature, era tag, loop markers.
    meta = mido.MidiTrack()
    meta.append(mido.MetaMessage("track_name", name=_meta_text(title), time=0))
    meta.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo), time=0))
    meta.append(
        mido.MetaMessage("time_signature", numerator=ts[0], denominator=ts[1], time=0)
    )
    meta.append(mido.MetaMessage("text", text=f"era={era_key}", time=0))
    meta.append(mido.MetaMessage("text", text=f"bendrange={BEND_RANGE}", time=0))
    if loop:
        meta.append(mido.MetaMessage("marker", text="loopStart", time=0))
    mid.tracks.append(meta)

    warnings: list[str] = []
    if not (era["tempo_range"][0] <= tempo <= era["tempo_range"][1]):
        warnings.append(
            f"tempo {tempo} is outside the typical {era['label']} range "
            f"{era['tempo_range'][0]}–{era['tempo_range'][1]} BPM."
        )

    # Channel assignment: drums -> 9, everyone else fills 0..15 skipping 9.
    next_chan = iter([c for c in range(16) if c != DRUM_CHANNEL])
    # For voice-count validation we collect (start_tick, end_tick) of every
    # sounding note across non-drum tracks.
    spans: list[tuple[int, int]] = []
    total_ticks = 0
    chord_eras_ok = era["chords"]
    used_chord = False

    for tdef in spec.get("tracks", []):
        voice_name = tdef.get("voice", "pulse25")
        vinfo = voices.get(voice_name)
        if vinfo is None:
            raise SystemExit(f"unknown voice '{voice_name}'. See `presets` for the catalog.")
        is_drums = vinfo["timbre"] == "drums"
        chan = DRUM_CHANNEL if is_drums else next(next_chan)

        events = parse_notes(
            tdef.get("notes", ""),
            default_octave=int(tdef.get("octave", 4)),
            drums=is_drums,
            drum_map=drum_map,
        )
        transpose = int(tdef.get("transpose", 0))
        gain = float(tdef.get("gain", 1.0))

        trk = mido.MidiTrack()
        # Encode the chip voice in the track name as "name::voice" so render can
        # recover the exact timbre the composer chose.
        trk.append(
            mido.MetaMessage("track_name", name=_meta_text(f"{tdef.get('name', voice_name)}::{voice_name}"), time=0)
        )
        if not is_drums:
            trk.append(mido.Message("program_change", channel=chan, program=vinfo["gm"], time=0))

        # Absolute-tick event list, then emit as deltas.
        # kind: 0=note_off, 1=note_on, 2=pitchwheel (the `note` slot carries the
        # bend value -8192..8191 instead of a pitch).
        ev: list[tuple[int, int, int, int]] = []
        cur = 0
        for e in events:
            dur = max(1, int(round(e["beats"] * ppq)))
            if e["midi"]:
                if len(e["midi"]) > 1 and not is_drums:
                    used_chord = True
                vel = max(1, min(127, int(round(e["vel"] * gain))))
                glide = e.get("glide")
                if glide is not None and not is_drums:
                    # Monophonic glide: hold the start pitch and bend it to the
                    # target across the note (the hardware "sweep").
                    start_n = max(0, min(127, e["midi"][0] + transpose))
                    semis = max(0, min(127, glide + transpose)) - start_n
                    ev.append((cur, 1, start_n, vel))
                    # Ramp the wheel across the note, landing the final point one
                    # tick INSIDE the note so the post-note reset (below) doesn't
                    # bleed into this note's own release tail.
                    for k in range(BEND_STEPS + 1):
                        frac = k / BEND_STEPS
                        bend = int(round(semis * frac / BEND_RANGE * 8192))
                        ev.append((cur + int(round(frac * (dur - 1))), 2,
                                   max(-8192, min(8191, bend)), 0))
                    ev.append((cur + dur, 0, start_n, 0))
                    ev.append((cur + dur, 2, 0, 0))  # reset wheel for later notes
                    spans.append((cur, cur + dur))
                else:
                    for n in e["midi"]:
                        note = n if is_drums else max(0, min(127, n + transpose))
                        ev.append((cur, 1, note, vel))
                        ev.append((cur + dur, 0, note, 0))
                        if not is_drums:
                            spans.append((cur, cur + dur))
            cur += dur
        total_ticks = max(total_ticks, cur)

        ev.sort(key=lambda x: (x[0], x[1]))  # off(0) before on(1) before bend(2)
        last = 0
        for tick, kind, note, vel in ev:
            delta = tick - last
            last = tick
            if kind == 2:
                trk.append(mido.Message("pitchwheel", channel=chan, pitch=note, time=delta))
            else:
                msg = "note_on" if kind == 1 else "note_off"
                trk.append(mido.Message(msg, channel=chan, note=note, velocity=vel, time=delta))
        mid.tracks.append(trk)

    if loop:
        meta.append(mido.MetaMessage("marker", text="loopEnd", time=total_ticks))

    # Validation: peak simultaneous voices (sweep-line over spans).
    peak = _peak_overlap(spans)
    if peak > era["max_voices"]:
        warnings.append(
            f"up to {peak} notes sound at once but {era['label']} has only "
            f"{era['max_voices']} voices — thin the arrangement or it won't be era-true."
        )
    if used_chord and not chord_eras_ok:
        warnings.append(
            f"{era['label']} can't play real chords — imply harmony with fast "
            f"arpeggios on one channel instead of stacking notes."
        )

    beats_total = total_ticks / ppq
    info = {
        "era": era_key,
        "tempo": tempo,
        "ppq": ppq,
        "time_signature": ts,
        "loop": loop,
        "tracks": len(spec.get("tracks", [])),
        "bars": round(beats_total / (ts[0] * 4 / ts[1]), 2),
        "beats": round(beats_total, 2),
        "loop_seconds": round(beats_total * 60.0 / tempo, 2),
        "peak_voices": peak,
        "max_voices": era["max_voices"],
        "warnings": warnings,
    }
    return mid, info


def _peak_overlap(spans: list[tuple[int, int]]) -> int:
    if not spans:
        return 0
    pts: list[tuple[int, int]] = []
    for a, b in spans:
        pts.append((a, 1))
        pts.append((b, -1))
    pts.sort(key=lambda x: (x[0], x[1]))
    cur = peak = 0
    for _, d in pts:
        cur += d
        peak = max(peak, cur)
    return peak


# --------------------------------------------------------------------------- #
# render: .mid -> audio (built-in chiptune synth)
# --------------------------------------------------------------------------- #
def _midi_to_freq(n: float) -> float:
    return 440.0 * (2.0 ** ((n - 69) / 12.0))


def _gm_to_voice(program: int, channel: int) -> str:
    if channel == DRUM_CHANNEL:
        return "drums"
    table = [
        (7, "bell"), (15, "bell"), (23, "organ"), (31, "pluck"),
        (39, "bass"), (47, "strings"), (55, "strings"), (63, "brass"),
        (71, "flute"), (79, "flute"), (87, "pulse25"), (95, "pad"),
    ]
    for hi, v in table:
        if program <= hi:
            return v
    return "pulse25"


def _adsr(n_total: int, a: int, d: int, s_level: float, r: int, sustain_n: int):
    import numpy as np

    env = np.zeros(n_total, dtype=np.float32)
    i = 0
    if a > 0:
        a = min(a, n_total)
        env[:a] = np.linspace(0, 1, a, endpoint=False)
        i = a
    if d > 0 and i < n_total:
        d = min(d, n_total - i)
        env[i : i + d] = np.linspace(1, s_level, d, endpoint=False)
        i += d
    if sustain_n > 0 and i < n_total:
        sn = min(sustain_n, n_total - i)
        env[i : i + sn] = s_level
        i += sn
    if i < n_total:
        rn = n_total - i
        start = env[i - 1] if i > 0 else s_level
        env[i:] = np.linspace(start, 0, rn)
    return env


def _osc(timbre: str, phase, duty: float):
    import numpy as np

    frac = np.mod(phase, 1.0)
    if timbre == "pulse":
        return np.where(frac < duty, 1.0, -1.0).astype(np.float32)
    if timbre == "triangle":
        return (4.0 * np.abs(frac - 0.5) - 1.0).astype(np.float32)
    if timbre == "saw":
        return (2.0 * frac - 1.0).astype(np.float32)
    if timbre == "sine":
        return np.sin(2 * np.pi * frac).astype(np.float32)
    if timbre == "wave":  # Game-Boy-ish 4-bit quantised sine: hollow, mellow.
        return (np.round(np.sin(2 * np.pi * frac) * 7.0) / 7.0).astype(np.float32)
    return np.sin(2 * np.pi * frac).astype(np.float32)


def _bend_freq(base_freq, bend, t):
    """Per-sample frequency for a glide: interpolate the bend curve (rel_sec ->
    semitones) over t and apply it to the base frequency. np.interp holds the
    endpoint values outside the curve's range, so the pitch settles on target."""
    import numpy as np

    xs = np.array([p[0] for p in bend], dtype=np.float32)
    ys = np.array([p[1] for p in bend], dtype=np.float32)
    semis = np.interp(t, xs, ys).astype(np.float32)
    return (base_freq * (2.0 ** (semis / 12.0))).astype(np.float32)


def _synth_note(freq, dur_s, vel, voice, voices, envelopes, bend=None):
    import numpy as np

    vinfo = voices[voice]
    env_def = envelopes[vinfo["env"]]
    r_s = env_def["r"]
    n_main = max(1, int(dur_s * SAMPLE_RATE))
    n_rel = int(r_s * SAMPLE_RATE)
    n_total = n_main + n_rel
    t = np.arange(n_total, dtype=np.float32) / SAMPLE_RATE

    # Instantaneous frequency: a glide curve (pitch bend) wins, else vibrato,
    # else a flat tone. Phase integrates frequency so glides slide smoothly.
    vd, vr = env_def["vib_depth"], env_def["vib_rate"]
    if bend:
        phase = np.cumsum(_bend_freq(freq, bend, t)) / SAMPLE_RATE
    elif vd > 0 and vr > 0:
        f_t = freq * (2.0 ** (vd / 12.0 * np.sin(2 * np.pi * vr * t)))
        phase = np.cumsum(f_t) / SAMPLE_RATE
    else:
        phase = freq * t

    if vinfo["timbre"] == "noise":
        # Pitched noise via sample-and-hold driven by the (possibly gliding)
        # phase: higher pitch = finer grain = brighter hiss, so a glide makes the
        # noise sweep — the iconic chip whoosh / zap / wind.
        idx = np.floor(phase * NOISE_DENSITY).astype(np.int64)
        idx -= int(idx.min())
        randoms = np.random.uniform(-1.0, 1.0, int(idx.max()) + 2).astype(np.float32)
        wave_buf = randoms[idx]
    else:
        wave_buf = _osc(vinfo["timbre"], phase, vinfo["duty"])

    a = int(env_def["a"] * SAMPLE_RATE)
    d = int(env_def["d"] * SAMPLE_RATE)
    sustain_n = max(0, n_main - a - d)
    env = _adsr(n_total, a, d, env_def["s"], n_rel if n_rel > 0 else 1, sustain_n)

    amp = (vel / 127.0) * 0.85
    out = wave_buf * env * amp

    # Gentle one-pole low-pass to tame the buzziest timbres (keeps pulse crisp).
    if vinfo["timbre"] in ("saw",) or vinfo["env"] in ("string", "pad"):
        out = _lowpass(out, 0.35)
    return out.astype(np.float32)


def _lowpass(x, alpha: float):
    import numpy as np

    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += alpha * (x[i] - acc)
        y[i] = acc
    return y


def _synth_drum(gm_note: int, dur_s, vel, drum_map):
    import numpy as np

    dtype = "snare"
    for k, v in drum_map.items():
        if k.startswith("_"):
            continue
        if int(v["gm"]) == gm_note:
            dtype = v["type"]
            break
    amp = (vel / 127.0) * 0.9

    def env(n, decay):
        return np.exp(-np.arange(n, dtype=np.float32) / (decay * SAMPLE_RATE))

    if dtype == "kick":
        n = int(0.18 * SAMPLE_RATE)
        t = np.arange(n) / SAMPLE_RATE
        f = np.linspace(130, 45, n)
        sig = np.sin(2 * np.pi * np.cumsum(f) / SAMPLE_RATE) * env(n, 0.06)
    elif dtype == "tom":
        n = int(0.25 * SAMPLE_RATE)
        t = np.arange(n) / SAMPLE_RATE
        f = np.linspace(180, 90, n)
        sig = np.sin(2 * np.pi * np.cumsum(f) / SAMPLE_RATE) * env(n, 0.12)
    elif dtype in ("hat", "ohat"):
        decay = 0.02 if dtype == "hat" else 0.18
        n = int((decay * 3) * SAMPLE_RATE)
        noise = np.random.uniform(-1, 1, n).astype(np.float32)
        sig = _highpass(noise, 0.7) * env(n, decay)
    elif dtype == "crash":
        n = int(0.6 * SAMPLE_RATE)
        noise = np.random.uniform(-1, 1, n).astype(np.float32)
        sig = _highpass(noise, 0.5) * env(n, 0.35)
    else:  # snare / clap
        n = int(0.2 * SAMPLE_RATE)
        t = np.arange(n) / SAMPLE_RATE
        tone = np.sin(2 * np.pi * 185 * t) * 0.5
        noise = np.random.uniform(-1, 1, n).astype(np.float32)
        sig = (tone + noise) * env(n, 0.1)
    return (sig * amp).astype(np.float32)


def _highpass(x, alpha: float):
    import numpy as np

    return (x - _lowpass(x, 1.0 - alpha)).astype(np.float32)


def _reverb(x, amount: float):
    import numpy as np

    if amount <= 0:
        return x
    out = x.copy()
    for delay_ms, fb in ((37, 0.5), (53, 0.42), (71, 0.34)):
        d = int(delay_ms / 1000.0 * SAMPLE_RATE)
        if d >= len(x):
            continue
        echo = np.zeros_like(x)
        echo[d:] = x[:-d] * fb
        out += echo * amount
    peak = float(np.max(np.abs(out))) or 1.0
    return (out / peak * float(np.max(np.abs(x)) or 1.0)).astype(np.float32)


def parse_midi_notes(mid) -> tuple[list[dict], float, str | None, bool, float]:
    """Read a .mid into [{start, dur, freq?, gm_note, vel, voice}], plus the last
    note-off time, an embedded era tag (if any), whether it is a seamless loop,
    and the loop-body length in seconds (from the loopEnd marker — this includes
    any trailing rest, so loops tile without drifting)."""
    ppq = mid.ticks_per_beat
    # tempo map (abs_tick -> tempo)
    tempo_changes: list[tuple[int, int]] = []
    era_tag: str | None = None
    is_loop = False
    loop_end_tick = 0
    bend_range = float(BEND_RANGE)
    bends: dict[int, list[tuple[int, int]]] = {}  # channel -> [(tick, raw_pitch)]
    for trk in mid.tracks:
        at = 0
        for msg in trk:
            at += msg.time
            if msg.type == "set_tempo":
                tempo_changes.append((at, msg.tempo))
            elif msg.type == "text" and msg.text.startswith("era="):
                era_tag = msg.text.split("=", 1)[1]
            elif msg.type == "text" and msg.text.startswith("bendrange="):
                try:
                    bend_range = float(msg.text.split("=", 1)[1])
                except ValueError:
                    pass
            elif msg.type == "pitchwheel":
                bends.setdefault(msg.channel, []).append((at, msg.pitch))
            elif msg.type == "marker" and msg.text == "loopStart":
                is_loop = True
            elif msg.type == "marker" and msg.text == "loopEnd":
                loop_end_tick = max(loop_end_tick, at)
    tempo_changes.sort()
    for ch in bends:
        bends[ch].sort()
    if not tempo_changes:
        tempo_changes = [(0, 500000)]

    def tick_to_sec(tick: int) -> float:
        sec = 0.0
        prev_tick, prev_tempo = 0, tempo_changes[0][1]
        for ct, tp in tempo_changes:
            if ct >= tick:
                break
            sec += (ct - prev_tick) / ppq * (prev_tempo / 1_000_000.0)
            prev_tick, prev_tempo = ct, tp
        sec += (tick - prev_tick) / ppq * (prev_tempo / 1_000_000.0)
        return sec

    def note_bend(channel: int, start_tick: int, end_tick: int):
        """Bend automation overlapping a note -> [(rel_sec, semitones)] or None
        (None = no glide on this note's channel)."""
        ch = bends.get(channel)
        if not ch:
            return None
        start_sec = tick_to_sec(start_tick)
        val0 = 0
        for tk, raw in ch:
            if tk <= start_tick:
                val0 = raw
            else:
                break
        pts = [(0.0, val0 / 8192.0 * bend_range)]
        pts += [(tick_to_sec(tk) - start_sec, raw / 8192.0 * bend_range)
                for tk, raw in ch if start_tick < tk < end_tick]
        if len(pts) == 1 and abs(pts[0][1]) < 1e-6:
            return None
        return pts

    notes: list[dict] = []
    end_tick = 0
    for trk in mid.tracks:
        at = 0
        voice_override: str | None = None
        prog_by_chan: dict[int, int] = {}
        active: dict[tuple[int, int], tuple[int, int]] = {}  # (chan,note)->(tick,vel)
        for msg in trk:
            at += msg.time
            if msg.type == "track_name" and "::" in msg.name:
                voice_override = msg.name.split("::", 1)[1]
            elif msg.type == "program_change":
                prog_by_chan[msg.channel] = msg.program
            elif msg.type == "note_on" and msg.velocity > 0:
                active[(msg.channel, msg.note)] = (at, msg.velocity)
            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                key = (msg.channel, msg.note)
                if key in active:
                    start_tick, vel = active.pop(key)
                    end_tick = max(end_tick, at)
                    voice = voice_override or _gm_to_voice(
                        prog_by_chan.get(msg.channel, 80), msg.channel
                    )
                    notes.append(
                        {
                            "start": tick_to_sec(start_tick),
                            "dur": max(0.01, tick_to_sec(at) - tick_to_sec(start_tick)),
                            "gm_note": msg.note,
                            "vel": vel,
                            "voice": voice,
                            "channel": msg.channel,
                            "bend": note_bend(msg.channel, start_tick, at),
                        }
                    )
    loop_end_sec = tick_to_sec(loop_end_tick) if loop_end_tick else 0.0
    return notes, tick_to_sec(end_tick), era_tag, is_loop, loop_end_sec


def _body_and_tail(last_sec: float, is_loop: bool, loop_end_sec: float,
                   tail: float = 0.6) -> tuple[float, float]:
    """One self-contained pass = body_sec; tail_sec rings past it. A loop body is
    its loopEnd (incl. trailing rests) with NO tail so it tiles seamlessly; a
    one-shot is up to its last note with a `tail`-second ring-out (shorter for
    tight SFX blips, longer for sparkle/chime cues)."""
    if is_loop:
        return (loop_end_sec if loop_end_sec > 0 else last_sec), 0.0
    return last_sec, tail


def _finalize(buf, body_sec: float, tail_sec: float, loops: int, fade_out: float):
    """Shared post-processing for both engines: normalise, trim to one pass
    (body + tail), tile extra loop copies for previews, apply an optional fade."""
    import numpy as np

    peak = float(np.max(np.abs(buf))) or 1.0
    buf = buf / peak * 0.89
    buf = np.tanh(buf * 1.1).astype(np.float32)

    body_n = max(1, int(body_sec * SAMPLE_RATE))
    pass_n = min(len(buf), int((body_sec + tail_sec) * SAMPLE_RATE))
    out = buf[:pass_n]
    if loops > 1:
        body = buf[:body_n]
        out = np.concatenate([np.tile(body, loops - 1), out])
    if fade_out > 0:
        fn = min(len(out), int(fade_out * SAMPLE_RATE))
        out[-fn:] *= np.linspace(1.0, 0.0, fn)
    return out


def render_audio(mid_path: Path, profiles: dict, *, reverb: float | None,
                 loops: int, fade_out: float, tail: float | None = None) -> "object":
    import mido
    import numpy as np

    voices = profiles["voices"]
    envelopes = profiles["envelopes"]
    drum_map = profiles["drum_map"]

    mid = mido.MidiFile(mid_path)
    notes, last_sec, era_tag, is_loop, loop_end_sec = parse_midi_notes(mid)
    if not notes:
        raise SystemExit(f"no notes found in {mid_path}")

    era = profiles["eras"].get(era_tag, {}) if era_tag else {}
    if reverb is None:
        reverb = era.get("reverb", 0.0)
    use_tail = tail if tail is not None else era.get("tail", 0.6)

    body_sec, tail = _body_and_tail(last_sec, is_loop, loop_end_sec, use_tail)
    # Scratch buffer with headroom for note releases and the reverb tail.
    work_len = int((max(body_sec, last_sec) + tail + 1.0) * SAMPLE_RATE)
    buf = np.zeros(work_len, dtype=np.float32)

    for nt in notes:
        if nt["voice"] == "drums" or nt["channel"] == DRUM_CHANNEL:
            seg = _synth_drum(nt["gm_note"], nt["dur"], nt["vel"], drum_map)
        else:
            voice = nt["voice"] if nt["voice"] in voices else "pulse25"
            seg = _synth_note(_midi_to_freq(nt["gm_note"]), nt["dur"], nt["vel"],
                              voice, voices, envelopes, bend=nt.get("bend"))
        start = int(nt["start"] * SAMPLE_RATE)
        endp = min(work_len, start + len(seg))
        buf[start:endp] += seg[: endp - start]

    if reverb and reverb > 0:
        buf = _reverb(buf, float(reverb))

    out = _finalize(buf, body_sec, tail, loops, fade_out)
    return out, float(reverb), is_loop


def render_soundfont_tsf(mid_path: Path, soundfont: str, profiles: dict, *,
                         loops: int, fade_out: float, gain: float,
                         tail: float | None = None) -> "object":
    """Lush render path: synthesize the .mid through a real SoundFont using the
    pure-pip tinysoundfont engine (no system libs). Same loop/tail discipline as
    the chip engine, so SNES/hifi showpieces drop straight into the game."""
    import mido
    import numpy as np
    import tinysoundfont

    if not Path(soundfont).is_file():
        raise SystemExit(
            f"soundfont not found: {soundfont}\n"
            f"Fetch one first:  ./venv/bin/python "
            f".claude/skills/generate-midi/scripts/fetch_soundfont.py"
        )

    mid = mido.MidiFile(mid_path)
    _, last_sec, era_tag, is_loop, loop_end_sec = parse_midi_notes(mid)
    era = profiles["eras"].get(era_tag, {}) if era_tag else {}
    use_tail = tail if tail is not None else era.get("tail", 0.6)
    body_sec, tail = _body_and_tail(last_sec, is_loop, loop_end_sec, use_tail)

    synth = tinysoundfont.Synth(gain=gain, samplerate=SAMPLE_RATE)
    synth.sfload(str(soundfont))
    seq = tinysoundfont.Sequencer(synth)
    seq.midi_load(str(mid_path))

    chunk = 0.05
    n = int(chunk * SAMPLE_RATE)
    render_for = max(body_sec, last_sec) + tail + 1.0  # +1s for releases
    chunks: list = []
    elapsed = 0.0
    while elapsed < render_for:
        seq.process(chunk)
        chunks.append(np.frombuffer(synth.generate(n), dtype=np.float32).copy())
        elapsed += chunk
    stereo = np.concatenate(chunks).reshape(-1, 2)
    mono = stereo.mean(axis=1).astype(np.float32)

    out = _finalize(mono, body_sec, tail, loops, fade_out)
    return out, is_loop


def write_wav(path: Path, buf) -> None:
    import numpy as np

    pcm = np.clip(buf, -1.0, 1.0)
    pcm16 = (pcm * 32767.0).astype("<i2")
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm16.tobytes())


def write_mp3(path: Path, buf, bitrate: str) -> None:
    import subprocess
    import tempfile

    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        raise SystemExit(
            "MP3 encoding needs ffmpeg. Install the bundled binary with "
            "`./venv/bin/pip install imageio-ffmpeg`, or write a .wav instead."
        )
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        write_wav(tmp_path, buf)
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [ffmpeg, "-y", "-i", str(tmp_path), "-codec:a", "libmp3lame",
             "-b:a", bitrate, str(path)],
            check=True, capture_output=True,
        )
    finally:
        tmp_path.unlink(missing_ok=True)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
SCHEMA_DOC = """\
Song spec (JSON) — Claude composes this; `build` renders it to .mid.

{
  "title": "Sunhaven Route",
  "era": "gbc",                 // nes | gb | gbc | snes | gba | hifi | sfx
  "tempo": 132,                 // BPM
  "time_signature": [4, 4],
  "ppq": 480,                   // MIDI ticks per quarter (480 is plenty)
  "loop": true,                 // writes loopStart/loopEnd markers
  "key": "C major",             // documentation only
  "tracks": [
    {
      "name": "lead",
      "voice": "pulse25",       // see `presets` for the voice catalog
      "octave": 4,              // default octave for bare note letters
      "transpose": 0,           // semitone shift applied to the whole track
      "gain": 1.0,              // mix level 0..1.2
      "notes": "E4q G4q B4q A4q | G4h E4h"
    },
    {
      "name": "bass", "voice": "tri_bass", "octave": 2,
      "notes": "C2q C3q G2q G3q | A2q A3q F2q F3q"
    },
    {
      "name": "drums", "voice": "drums",
      "notes": "e kick+hat hat snare+hat hat kick+hat kick snare+hat hat"
    }
  ]
}

NOTE DSL (the `notes` string):
  pitch    C D E F G A B (UPPER-case), accidental # or b, optional octave: C4 F#3 Bb5
           bare letter (A) uses the track's "octave".
  duration suffix w=whole h=half q=quarter e=eighth s=sixteenth;
           dotted '.' (×1.5), double '..' (×1.75), triplet 't' (×2/3).
           OMIT the suffix to reuse the previous note's duration.
  set dur  a duration on its own ("e", "q.") sets the running duration for the
           notes after it:  "e kick hat snare"  -> three eighth-note hits.
  chord    join with '+'  ->  C4+E4+G4q   (only on chord-capable eras: snes/gba/hifi)
  glide    join with '~'  ->  C6~C4s   pitch SLIDES from C6 down to C4 over the
           note (the chip "sweep"); monophonic. On the 'noise' voice it sweeps the
           hiss (whoosh/zap). Up=jump/positive, down=fall/zap. Great for SFX.
  rest     r or -          ->  rq (quarter rest), re (eighth rest), r (inherit)
  velocity '@1..127'       ->  C4q@110
  bars     '|' is optional and ignored (use it to keep yourself honest)
  drums    on a "drums" voice, tokens are kit names: kick snare hat ohat tom crash clap
           e.g. "e kick+hat hat snare+hat hat kick+hat kick snare+hat hat"

You can also pass "notes" as a list:
  [{"pitch": "C4", "beats": 1, "vel": 100}, {"pitch": ["C4","E4","G4"], "beats": 2},
   {"pitch": "C6", "glide_to": "C4", "beats": 0.5}]   // glide in list form

SOUND EFFECTS: use era "sfx" + loop:false for short one-shot cues (blips, coins,
zaps, whooshes, hits, sparkles). Lean on glides ('~') and the 'noise' voice
(real pitched noise). Render with --tail (e.g. 0.03 tight, 0.4 ring-out). See
references/sfx-cookbook.md for the PixelKin SFX catalog and recipes.
"""


def cmd_presets(profiles: dict) -> int:
    print("ERAS (hardware profiles):")
    for k, e in profiles["eras"].items():
        print(f"  {k:6} {e['label']} — {e['max_voices']} voices, "
              f"chords={'yes' if e['chords'] else 'no'}, "
              f"tempo {e['tempo_range'][0]}–{e['tempo_range'][1]}")
    print("\nVOICES (instrument catalog):")
    for k, v in profiles["voices"].items():
        print(f"  {k:9} {v['desc']}")
    print("\nDRUMS (on a 'drums' voice):")
    print("  " + ", ".join(k for k in profiles["drum_map"] if not k.startswith("_")))
    print("\nFORM PRESETS (composition briefs):")
    for k, p in profiles["presets"].items():
        print(f"  {k:11} {p['label']} — era={p['era']}, ~{p['tempo']}bpm, "
              f"{p['length_seconds']}s, loop={'yes' if p['loop'] else 'no'}")
        print(f"              {p['form']}")
    return 0


def cmd_build(args, profiles: dict) -> int:
    spec_path = Path(args.spec)
    if not spec_path.is_file():
        raise SystemExit(f"spec not found: {spec_path}")
    spec = json.loads(spec_path.read_text())
    mid, info = build_midi(spec, profiles)
    out = Path(args.output).expanduser().resolve()
    if out.suffix.lower() not in (".mid", ".midi"):
        print(f"warning: output '{out.name}' isn't a .mid file.", file=sys.stderr)
    out.parent.mkdir(parents=True, exist_ok=True)
    mid.save(str(out))
    info["path"] = str(out)
    info["bytes"] = out.stat().st_size
    print(json.dumps(info, indent=2))
    for w in info["warnings"]:
        print(f"  ⚠  {w}", file=sys.stderr)
    return 0


def cmd_render(args, profiles: dict) -> int:
    mid_path = Path(args.input)
    if not mid_path.is_file():
        raise SystemExit(f"midi not found: {mid_path}")
    out = Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    if args.engine == "soundfont":
        sf = args.soundfont or resolve_default_soundfont()
        if not sf:
            raise SystemExit(
                "No soundfont found. Pass --soundfont path/to.sf2, or fetch one:\n"
                "  ./venv/bin/python .claude/skills/generate-midi/scripts/fetch_soundfont.py"
            )
        buf, is_loop = render_soundfont_tsf(
            mid_path, sf, profiles, loops=args.loops,
            fade_out=args.fade_out, gain=args.gain, tail=args.tail)
        if out.suffix.lower() == ".wav":
            write_wav(out, buf)
        else:
            write_mp3(out, buf, args.bitrate)
        info = {
            "path": str(out), "engine": "soundfont",
            "soundfont": str(Path(sf).name), "loop": is_loop, "loops": args.loops,
            "seconds": round(len(buf) / SAMPLE_RATE, 2),
        }
    else:
        buf, used_reverb, is_loop = render_audio(
            mid_path, profiles, reverb=args.reverb,
            loops=args.loops, fade_out=args.fade_out, tail=args.tail)
        if out.suffix.lower() == ".wav":
            write_wav(out, buf)
        else:
            write_mp3(out, buf, args.bitrate)
        info = {
            "path": str(out), "engine": "chip",
            "loop": is_loop, "loops": args.loops, "reverb": round(used_reverb, 3),
            "seconds": round(len(buf) / SAMPLE_RATE, 2),
        }
    info["bytes"] = out.stat().st_size
    print(json.dumps(info, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="PixelKin MIDI music toolkit.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("presets", help="List eras, voices, drums, and form presets.")
    sub.add_parser("schema", help="Print the song-spec format and an example.")

    pb = sub.add_parser("build", help="Song-spec JSON -> .mid")
    pb.add_argument("--spec", required=True, help="Path to the song-spec JSON.")
    pb.add_argument("--output", required=True, help="Output .mid path.")

    pr = sub.add_parser("render", help=".mid -> .mp3 / .wav")
    pr.add_argument("--input", required=True, help="Input .mid path.")
    pr.add_argument("--output", required=True, help="Output .mp3 or .wav path.")
    pr.add_argument("--engine", choices=["chip", "soundfont"], default="chip",
                    help="chip = built-in chiptune synth (default, authentic & lo-fi); "
                         "soundfont = render through a real .sf2 (lush; SNES/orchestral).")
    pr.add_argument("--soundfont", default=None,
                    help=".sf2 path. Default: GeneralUser-GS.sf2 in assets/audio/midi/"
                         "soundfonts/ (run fetch_soundfont.py to get one).")
    pr.add_argument("--gain", type=float, default=0.0,
                    help="Soundfont engine output gain in dB (default 0).")
    pr.add_argument("--reverb", type=float, default=None,
                    help="0..0.5 reverb mix. Default: from the era tag in the .mid.")
    pr.add_argument("--loops", type=int, default=1,
                    help="Repeat the loop body N times for a longer preview (default 1).")
    pr.add_argument("--fade-out", type=float, default=0.0,
                    help="Seconds of fade at the very end (for previews, not loops).")
    pr.add_argument("--tail", type=float, default=None,
                    help="One-shot ring-out seconds past the last note. Default: the "
                         "era's tail (sfx=0.08) or 0.6. Use ~0.03 for tight blips, "
                         "~0.4 for sparkle/chime cues. Ignored for loops.")
    pr.add_argument("--bitrate", default="160k", help="MP3 bitrate (default 160k).")

    args = p.parse_args()
    profiles = load_profiles()

    if args.cmd == "presets":
        return cmd_presets(profiles)
    if args.cmd == "schema":
        print(SCHEMA_DOC)
        return 0
    if args.cmd == "build":
        return cmd_build(args, profiles)
    if args.cmd == "render":
        return cmd_render(args, profiles)
    return 1


if __name__ == "__main__":
    sys.exit(main())
