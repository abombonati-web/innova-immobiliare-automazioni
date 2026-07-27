"""Sintesi e montaggio audio: effetti, letto musicale jazz, mixaggio con ducking.

Tutto e generato da zero con numpy/scipy: nessun campione, nessuna libreria
musicale con royalty. Il jazz e sintesi additiva semplice — rende l'atmosfera,
non sostituisce una libreria professionale.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.ndimage import uniform_filter1d
from scipy.signal import resample_poly

log = logging.getLogger(__name__)

SAMPLE_RATE = 44_100


# ------------------------------------------------------------------ helper ---
def silence(seconds: float, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    return np.zeros(int(round(seconds * sample_rate)), dtype=np.float32)


def resample(samples: np.ndarray, src_rate: int, dst_rate: int = SAMPLE_RATE) -> np.ndarray:
    if src_rate == dst_rate:
        return samples.astype(np.float32)
    from math import gcd

    divisor = gcd(src_rate, dst_rate)
    return resample_poly(samples, dst_rate // divisor, src_rate // divisor).astype(np.float32)


def normalize(samples: np.ndarray, peak: float = 0.95) -> np.ndarray:
    top = float(np.max(np.abs(samples))) if samples.size else 0.0
    if top < 1e-9:
        return samples
    return (samples * (peak / top)).astype(np.float32)


def fade(samples: np.ndarray, *, fade_in: float = 0.0, fade_out: float = 0.0) -> np.ndarray:
    out = samples.copy()
    n_in = int(fade_in * SAMPLE_RATE)
    n_out = int(fade_out * SAMPLE_RATE)
    if n_in > 0:
        out[:n_in] *= np.linspace(0.0, 1.0, min(n_in, out.size), dtype=np.float32)
    if n_out > 0 and out.size:
        n_out = min(n_out, out.size)
        out[-n_out:] *= np.linspace(1.0, 0.0, n_out, dtype=np.float32)
    return out


def place(track: np.ndarray, clip: np.ndarray, at_seconds: float, gain: float = 1.0) -> np.ndarray:
    """Somma `clip` dentro `track` a partire da `at_seconds` (estende se serve)."""
    start = int(round(at_seconds * SAMPLE_RATE))
    end = start + clip.size
    if end > track.size:
        track = np.concatenate([track, np.zeros(end - track.size, dtype=np.float32)])
    track[start:end] += clip * gain
    return track


def write_wav(path: str | Path, samples: np.ndarray, sample_rate: int = SAMPLE_RATE) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    clipped = np.clip(samples, -1.0, 1.0)
    wavfile.write(path, sample_rate, (clipped * 32767).astype(np.int16))
    return path


def wav_to_mp3(wav_path: str | Path, mp3_path: str | Path, bitrate: str = "96k") -> Path:
    """MP3 mono: compromesso qualita/peso per l'audio incorporato nella landing."""
    mp3_path = Path(mp3_path)
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(wav_path),
            "-ac", "1", "-b:a", bitrate, "-codec:a", "libmp3lame",
            str(mp3_path),
        ],
        check=True,
    )
    return mp3_path


def duration(samples: np.ndarray) -> float:
    return samples.size / SAMPLE_RATE


# ------------------------------------------------------------------- sfx ---
def _envelope(n: int, attack: float, decay: float) -> np.ndarray:
    attack_n = max(int(attack * SAMPLE_RATE), 1)
    env = np.ones(n, dtype=np.float32)
    env[:attack_n] = np.linspace(0.0, 1.0, attack_n, dtype=np.float32)
    tail = np.exp(-np.arange(n - attack_n, dtype=np.float32) / (decay * SAMPLE_RATE))
    env[attack_n:] = tail
    return env


def ding(freq: float = 1568.0, seconds: float = 1.6, gain: float = 0.55) -> np.ndarray:
    """Campanella cristallina del reveal prezzo (fondamentale + parziali inarmoniche)."""
    t = np.arange(int(seconds * SAMPLE_RATE), dtype=np.float32) / SAMPLE_RATE
    partials = [(1.0, 1.0, 0.90), (2.01, 0.42, 0.55), (2.99, 0.22, 0.35), (4.17, 0.12, 0.22)]
    out = np.zeros_like(t)
    for ratio, amp, decay in partials:
        out += amp * np.sin(2 * np.pi * freq * ratio * t) * np.exp(-t / decay)
    return normalize(out, gain)


def bell(freq: float = 987.0, seconds: float = 1.1, gain: float = 0.35) -> np.ndarray:
    """Accento leggero per i cambi scena."""
    return ding(freq=freq, seconds=seconds, gain=gain)


def thump(freq: float = 62.0, seconds: float = 0.55, gain: float = 0.45) -> np.ndarray:
    """Colpo grave e morbido, per l'ingresso delle slide."""
    t = np.arange(int(seconds * SAMPLE_RATE), dtype=np.float32) / SAMPLE_RATE
    sweep = freq * np.exp(-t * 6.0) + 38.0
    wave = np.sin(2 * np.pi * np.cumsum(sweep) / SAMPLE_RATE)
    return normalize(wave * _envelope(t.size, 0.004, 0.10), gain)


# -------------------------------------------------------------------- jazz ---
_NOTE_BASE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def note_hz(name: str, octave: int) -> float:
    """`('A', 4)` -> 440.0 Hz."""
    semitone = _NOTE_BASE[name[0]] + (1 if name.endswith("#") else -1 if name.endswith("b") else 0)
    midi = 12 * (octave + 1) + semitone
    return 440.0 * 2 ** ((midi - 69) / 12)


# I - vi - ii - V in Do maggiore: giro standard, morbido, non invadente
PROGRESSION = [
    {"root": ("C", 2), "chord": [("E", 3), ("G", 3), ("B", 3)], "walk": ["C", "E", "G", "A"]},
    {"root": ("A", 1), "chord": [("C", 3), ("E", 3), ("G", 3)], "walk": ["A", "C", "E", "G"]},
    {"root": ("D", 2), "chord": [("F", 3), ("A", 3), ("C", 4)], "walk": ["D", "F", "A", "C"]},
    {"root": ("G", 1), "chord": [("B", 2), ("D", 3), ("F", 3)], "walk": ["G", "B", "D", "F"]},
]


def _bass_note(freq: float, seconds: float) -> np.ndarray:
    t = np.arange(int(seconds * SAMPLE_RATE), dtype=np.float32) / SAMPLE_RATE
    wave = (
        np.sin(2 * np.pi * freq * t)
        + 0.35 * np.sin(2 * np.pi * 2 * freq * t)
        + 0.12 * np.sin(2 * np.pi * 3 * freq * t)
    )
    return (wave * _envelope(t.size, 0.008, 0.42) * 0.5).astype(np.float32)


def _rhodes_chord(freqs: list[float], seconds: float) -> np.ndarray:
    t = np.arange(int(seconds * SAMPLE_RATE), dtype=np.float32) / SAMPLE_RATE
    out = np.zeros_like(t)
    for freq in freqs:
        out += np.sin(2 * np.pi * freq * t) + 0.30 * np.sin(2 * np.pi * freq * 2.002 * t)
    out /= max(len(freqs), 1)
    return (out * _envelope(t.size, 0.012, 0.28) * 0.32).astype(np.float32)


def _brush(seconds: float, rng: np.random.Generator) -> np.ndarray:
    n = int(seconds * SAMPLE_RATE)
    noise = rng.standard_normal(n).astype(np.float32)
    # passa-alto rudimentale: la differenza prima toglie il grave
    filtered = np.diff(noise, prepend=noise[:1])
    return (filtered * _envelope(n, 0.003, 0.05) * 0.10).astype(np.float32)


def synthesize_jazz_bed(seconds: float, bpm: int = 92, seed: int = 7) -> np.ndarray:
    """Letto jazz sintetizzato: walking bass, comping in levare, spazzole.

    Swing 2:1 sugli ottavi. Volume tenuto basso: la voce resta il contenuto
    primario, questo e solo atmosfera.
    """
    rng = np.random.default_rng(seed)
    beat = 60.0 / bpm
    bar = beat * 4
    track = np.zeros(int(round(seconds * SAMPLE_RATE)) + SAMPLE_RATE, dtype=np.float32)

    bars = int(np.ceil(seconds / bar)) + 1
    for index in range(bars):
        step = PROGRESSION[index % len(PROGRESSION)]
        bar_start = index * bar
        root_name, root_octave = step["root"]

        # walking bass: una nota per quarto
        for quarter, degree in enumerate(step["walk"]):
            octave = root_octave + (1 if _NOTE_BASE[degree] < _NOTE_BASE[root_name] else 0)
            clip = _bass_note(note_hz(degree, octave), beat * 0.95)
            track = place(track, clip, bar_start + quarter * beat, gain=0.9)

        # comping in levare: sul "and" di 2 e di 4, con feel swing
        chord_freqs = [note_hz(n, o) for n, o in step["chord"]]
        for quarter in (1, 3):
            offset = bar_start + quarter * beat + beat * (2 / 3)
            track = place(track, _rhodes_chord(chord_freqs, beat * 0.9), offset, gain=0.85)

        # spazzole sugli ottavi swingati
        for quarter in range(4):
            track = place(track, _brush(0.09, rng), bar_start + quarter * beat, gain=0.8)
            track = place(track, _brush(0.07, rng), bar_start + quarter * beat + beat * (2 / 3), gain=0.6)

    track = track[: int(round(seconds * SAMPLE_RATE))]
    return fade(normalize(track, 0.5), fade_in=1.2, fade_out=2.0)


# ------------------------------------------------------------------- mixdown ---
def voice_activity(voice: np.ndarray, smooth_seconds: float = 0.35) -> np.ndarray:
    """Maschera 0..1 dell'attivita vocale, smussata: serve al ducking."""
    envelope = uniform_filter1d(np.abs(voice), size=max(int(0.02 * SAMPLE_RATE), 1))
    envelope = uniform_filter1d(envelope, size=max(int(smooth_seconds * SAMPLE_RATE), 1))
    top = float(np.max(envelope)) if envelope.size else 0.0
    if top < 1e-9:
        return np.zeros_like(envelope)
    return np.clip(envelope / (top * 0.35), 0.0, 1.0).astype(np.float32)


def duck(bed: np.ndarray, voice: np.ndarray, amount: float = 0.55) -> np.ndarray:
    """Abbassa il letto musicale del `amount` quando la voce e attiva."""
    length = max(bed.size, voice.size)
    bed = np.pad(bed, (0, length - bed.size))
    padded_voice = np.pad(voice, (0, length - voice.size))
    return (bed * (1.0 - amount * voice_activity(padded_voice))).astype(np.float32)


def mixdown(
    voice: np.ndarray,
    *,
    bed: np.ndarray | None = None,
    sfx: np.ndarray | None = None,
    bed_gain: float = 0.30,
    duck_amount: float = 0.55,
) -> np.ndarray:
    """Mix finale: la voce e sempre nettamente sopra al letto musicale."""
    length = voice.size
    for extra in (bed, sfx):
        if extra is not None:
            length = max(length, extra.size)
    mix = np.pad(voice, (0, length - voice.size)).astype(np.float32)
    if sfx is not None:
        mix += np.pad(sfx, (0, length - sfx.size))
    if bed is not None:
        ducked = duck(np.pad(bed, (0, max(0, length - bed.size)))[:length], mix, duck_amount)
        mix += ducked * bed_gain
    return normalize(mix, 0.92)
