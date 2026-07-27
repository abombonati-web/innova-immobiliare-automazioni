"""Voce narrante italiana con Piper (modello `it_IT-paola-medium`) via sherpa-onnx.

Due registri, definiti in `brand.VOICE_TONES`:

* ``euforico``      video social  — speed 0.90, noise 0.80 / 0.95 (piu umano, caldo);
* ``professionale`` landing page  — speed 1.00, noise 0.55 / 0.70 (dizione netta).

Limite noto: e una voce sintetica e si sente. Va benissimo per contenuti rapidi,
non sostituisce uno speaker reale su materiali istituzionali di alto profilo.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import audio as au
from .assets import voice_model_dir
from .brand import VOICE_TONES

log = logging.getLogger(__name__)

PAUSE_BETWEEN_PARAGRAPHS = 0.42
PAUSE_BETWEEN_SENTENCES = 0.30


@dataclass
class VoiceClip:
    """Un blocco di parlato gia renderizzato, con la sua durata esatta."""

    key: str
    text: str
    samples: np.ndarray

    @property
    def duration(self) -> float:
        return au.duration(self.samples)


@dataclass
class VoiceTrack:
    """Sequenza di blocchi parlati, con le durate necessarie a sincronizzare il video."""

    clips: list[VoiceClip] = field(default_factory=list)

    @property
    def durations(self) -> dict[str, float]:
        return {c.key: c.duration for c in self.clips}

    def by_key(self, key: str) -> VoiceClip | None:
        return next((c for c in self.clips if c.key == key), None)

    def concatenated(self, gap: float = PAUSE_BETWEEN_PARAGRAPHS) -> np.ndarray:
        parts: list[np.ndarray] = []
        for index, clip in enumerate(self.clips):
            if index:
                parts.append(au.silence(gap))
            parts.append(clip.samples)
        return np.concatenate(parts) if parts else au.silence(0.1)


class Narrator:
    """Wrapper attorno al TTS offline; il modello viene caricato una volta sola."""

    def __init__(self, tone: str = "professionale", *, num_threads: int = 2) -> None:
        if tone not in VOICE_TONES:
            raise ValueError(f"Tono sconosciuto '{tone}'. Disponibili: {sorted(VOICE_TONES)}")
        self.tone = tone
        self.params = VOICE_TONES[tone]
        self._tts = None
        self._num_threads = num_threads
        self._sample_rate = 22_050

    def _engine(self):
        if self._tts is not None:
            return self._tts
        import sherpa_onnx  # import pigro: pesante e non serve ai test di layout

        model_dir = voice_model_dir()
        onnx = next(model_dir.glob("*.onnx"))
        config = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                    model=str(onnx),
                    tokens=str(model_dir / "tokens.txt"),
                    data_dir=str(model_dir / "espeak-ng-data"),
                    noise_scale=self.params["noise_scale"],
                    noise_scale_w=self.params["noise_scale_w"],
                ),
                provider="cpu",
                num_threads=self._num_threads,
            ),
            max_num_sentences=1,
        )
        log.info(
            "voce Piper '%s' — speed %.2f, noise %.2f/%.2f",
            self.tone,
            self.params["speed"],
            self.params["noise_scale"],
            self.params["noise_scale_w"],
        )
        self._tts = sherpa_onnx.OfflineTts(config)
        return self._tts

    def say(self, text: str) -> np.ndarray:
        """Sintetizza un testo, spezzandolo in frasi con pause naturali."""
        chunks: list[np.ndarray] = []
        for index, sentence in enumerate(split_sentences(text)):
            result = self._engine().generate(sentence, sid=0, speed=self.params["speed"])
            self._sample_rate = result.sample_rate
            samples = au.resample(np.asarray(result.samples, dtype=np.float32), result.sample_rate)
            if index:
                chunks.append(au.silence(PAUSE_BETWEEN_SENTENCES))
            chunks.append(samples)
        if not chunks:
            return au.silence(0.1)
        return au.fade(np.concatenate(chunks), fade_in=0.02, fade_out=0.06)


def split_sentences(text: str) -> list[str]:
    """Spezza in frasi brevi: pause piu naturali e sintesi piu stabile."""
    parts = re.split(r"(?<=[.!?:])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def synthesize_voice(
    segments: list[tuple[str, str]] | list[str],
    tone: str = "professionale",
) -> VoiceTrack:
    """Sintetizza i segmenti e restituisce la traccia con le durate esatte.

    `segments` puo essere una lista di stringhe oppure di coppie `(chiave, testo)`.
    """
    narrator = Narrator(tone)
    track = VoiceTrack()
    for index, segment in enumerate(segments):
        key, text = segment if isinstance(segment, (tuple, list)) else (f"seg{index}", segment)
        clip = VoiceClip(key=key, text=text, samples=narrator.say(text))
        log.info("  [%s] %.2fs — %s", key, clip.duration, text[:64] + ("..." if len(text) > 64 else ""))
        track.clips.append(clip)
    return track


def render_narration(
    paragraphs: list[str],
    out_wav: str | Path,
    *,
    tone: str = "professionale",
    gap: float = PAUSE_BETWEEN_PARAGRAPHS,
) -> tuple[Path, float]:
    """Voce continua per la landing page: WAV + durata totale."""
    track = synthesize_voice(paragraphs, tone=tone)
    samples = au.normalize(track.concatenated(gap), 0.92)
    path = au.write_wav(out_wav, samples)
    return path, au.duration(samples)
