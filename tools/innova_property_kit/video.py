"""Montaggio del reel verticale 1080x1920 con ffmpeg.

Punto delicato della pipeline: `xfade` sposta indietro l'inizio "visibile" di
ogni clip (ogni transizione mangia `T` secondi), quindi i tempi di partenza
delle scene **non** sono la somma semplice delle durate. Qui vengono calcolati
una volta sola da `scene_offsets()`, loggati ad ogni build e riusati sia per il
filtro video sia per posizionare i segmenti audio.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import audio as au

log = logging.getLogger(__name__)

WIDTH, HEIGHT, FPS = 1080, 1920, 30
TRANSITION = 0.30


@dataclass
class Clip:
    """Una scena del reel."""

    source: Path
    duration: float
    key: str = ""  # chiave del segmento vocale agganciato alla scena
    overlay: Path | None = None
    zoom: str = "in"  # in | out | still
    label: str = ""

    @property
    def frames(self) -> int:
        return max(int(round(self.duration * FPS)), 2)


@dataclass
class Timeline:
    """Scene + offset calcolati, pronti per video e audio."""

    clips: list[Clip]
    transition: float = TRANSITION
    starts: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.starts = scene_offsets([c.duration for c in self.clips], self.transition)

    @property
    def total(self) -> float:
        return total_duration([c.duration for c in self.clips], self.transition)

    def start_of(self, key: str) -> float | None:
        for clip, start in zip(self.clips, self.starts):
            if clip.key == key:
                return start
        return None

    def log(self) -> None:
        log.info("timeline (%d scene, transizione %.2fs):", len(self.clips), self.transition)
        for clip, start in zip(self.clips, self.starts):
            log.info(
                "  %6.2fs  +%.2fs  %-14s %s",
                start,
                clip.duration,
                clip.key or "-",
                clip.label or clip.source.name,
            )
        log.info("  durata totale: %.2fs", self.total)


def scene_offsets(durations: list[float], transition: float = TRANSITION) -> list[float]:
    """Istante in cui ogni clip diventa visibile in una catena di `xfade`.

    Ogni transizione sovrappone `transition` secondi, quindi la clip `i` parte a
    `sum(durate precedenti) - i * transition`, non alla somma semplice.
    """
    starts: list[float] = []
    cumulative = 0.0
    for index, value in enumerate(durations):
        starts.append(round(cumulative - index * transition, 3))
        cumulative += value
    return starts


def total_duration(durations: list[float], transition: float = TRANSITION) -> float:
    if not durations:
        return 0.0
    return round(sum(durations) - (len(durations) - 1) * transition, 3)


def ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "ffmpeg non trovato nel PATH: e necessario per generare il video "
            "(`apt-get install ffmpeg`)."
        )


def _run(args: list[str]) -> None:
    log.debug("ffmpeg %s", " ".join(args[1:]))
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg fallito:\n{result.stderr[-4000:]}")


def render_clip(clip: Clip, out_path: Path) -> Path:
    """Renderizza una singola scena (Ken Burns + eventuale didascalia)."""
    zoom_expr = {
        "in": f"min(1+{0.10 / max(clip.frames, 1):.6f}*on,1.10)",
        "out": f"max(1.10-{0.10 / max(clip.frames, 1):.6f}*on,1.0)",
        "still": f"min(1+{0.035 / max(clip.frames, 1):.6f}*on,1.035)",
    }[clip.zoom]

    chain = (
        f"scale={WIDTH * 2}:{HEIGHT * 2}:force_original_aspect_ratio=increase,"
        f"crop={WIDTH * 2}:{HEIGHT * 2},"
        f"zoompan=z='{zoom_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d={clip.frames}:s={WIDTH}x{HEIGHT}:fps={FPS},"
        f"setsar=1,format=yuv420p"
    )

    args = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", f"{clip.duration:.3f}",
            "-i", str(clip.source)]
    if clip.overlay:
        args += ["-loop", "1", "-t", f"{clip.duration:.3f}", "-i", str(clip.overlay)]
        filter_complex = f"[0:v]{chain}[base];[1:v]scale={WIDTH}:{HEIGHT}[ov];[base][ov]overlay=0:0[v]"
    else:
        filter_complex = f"[0:v]{chain}[v]"

    args += [
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-r", str(FPS),
        "-t", f"{clip.duration:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        str(out_path),
    ]
    _run(args)
    return out_path


def concat_with_xfade(clips: list[Path], durations: list[float], out_path: Path,
                      transition: float = TRANSITION) -> Path:
    """Concatena i clip renderizzati con crossfade, usando gli offset calcolati."""
    if len(clips) == 1:
        shutil.copyfile(clips[0], out_path)
        return out_path

    starts = scene_offsets(durations, transition)
    args: list[str] = ["ffmpeg", "-y", "-loglevel", "error"]
    for clip in clips:
        args += ["-i", str(clip)]

    steps: list[str] = []
    current = "[0:v]"
    for index in range(1, len(clips)):
        label = f"[x{index}]" if index < len(clips) - 1 else "[v]"
        steps.append(
            f"{current}[{index}:v]xfade=transition=fade:duration={transition}"
            f":offset={starts[index]:.3f}{label}"
        )
        current = label

    args += [
        "-filter_complex", ";".join(steps),
        "-map", "[v]",
        "-r", str(FPS),
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        str(out_path),
    ]
    _run(args)
    return out_path


def mux(video_path: Path, audio_path: Path, out_path: Path) -> Path:
    """Unisce video e audio finale (H.264 + AAC), tagliando sulla traccia piu corta."""
    _run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-shortest", "-movflags", "+faststart",
        str(out_path),
    ])
    return out_path


def assemble_video(
    timeline: Timeline,
    audio_path: Path,
    out_path: Path,
    work_dir: Path,
) -> Path:
    """Renderizza le scene, le concatena con xfade e monta l'audio."""
    ensure_ffmpeg()
    timeline.log()
    work_dir.mkdir(parents=True, exist_ok=True)

    rendered: list[Path] = []
    for index, clip in enumerate(timeline.clips):
        dest = work_dir / f"clip-{index:02d}.mp4"
        log.info("render scena %d/%d (%.2fs)", index + 1, len(timeline.clips), clip.duration)
        rendered.append(render_clip(clip, dest))

    silent = concat_with_xfade(
        rendered, [c.duration for c in timeline.clips], work_dir / "montaggio.mp4", timeline.transition
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    return mux(silent, audio_path, out_path)


def build_soundtrack(
    timeline: Timeline,
    voice_clips: dict[str, np.ndarray],
    *,
    music: str = "jazz",
    bpm: int = 92,
    lead_in: float = 0.20,
) -> np.ndarray:
    """Traccia audio del reel: voce posizionata sugli offset reali + sfx + letto musicale."""
    total = timeline.total
    voice = au.silence(total)
    sfx = au.silence(total)

    for clip, start in zip(timeline.clips, timeline.starts):
        if clip.key and clip.key in voice_clips:
            voice = au.place(voice, voice_clips[clip.key], max(start + lead_in, 0.0))
            log.info("  voce '%s' posizionata a %.2fs", clip.key, start + lead_in)
        if clip.key == "price":
            sfx = au.place(sfx, au.ding(), max(start - 0.10, 0.0), gain=0.9)
        elif clip.key in {"event", "cta"}:
            sfx = au.place(sfx, au.thump(), max(start - 0.05, 0.0), gain=0.8)

    voice = voice[: int(round(total * au.SAMPLE_RATE))]
    sfx = sfx[: int(round(total * au.SAMPLE_RATE))]

    bed = au.synthesize_jazz_bed(total, bpm=bpm) if music == "jazz" else None
    return au.mixdown(voice, bed=bed, sfx=sfx)
