"""Costruzione della scaletta del reel a partire dal brief e dalle durate reali del parlato.

Le durate delle scene non sono fisse: si ricavano dalla voce gia sintetizzata
(piu un margine di respiro), cosi il montaggio resta sincronizzato anche quando
il testo cambia. Le durate indicative del workflow manuale restano come minimi.
"""

from __future__ import annotations

import logging
from pathlib import Path

from . import script as copy
from .model import PropertyBrief
from .slides import SlideSet, build_caption_overlay
from .video import Clip, Timeline
from .voice import VoiceTrack

log = logging.getLogger(__name__)

MIN_PHOTO = 1.25
PAD = {"price": 1.5, "event": 1.3, "cta": 1.2}
OLD_PRICE_DURATION = 1.8


def build_timeline(
    brief: PropertyBrief,
    photos: list[Path],
    slides: SlideSet,
    voice: VoiceTrack,
    work_dir: Path,
    *,
    max_duration: float = 30.0,
    transition: float = 0.30,
) -> Timeline:
    durations = voice.durations
    captions = copy.photo_captions(brief, len(photos))

    # --- foto: la sequenza copre tutto il parlato di apertura --------------
    # ogni transizione mangia `transition` secondi di visibilita, quindi va
    # riaggiunta a ciascuna clip: altrimenti la voce sfora sulla slide dopo.
    count = max(len(photos), 1)
    intro_total = max(durations.get("intro", 0.0) + 0.9, MIN_PHOTO * count)
    per_photo = intro_total / count + transition

    clips: list[Clip] = []
    for index, (photo, caption) in enumerate(zip(photos, captions)):
        overlay = build_caption_overlay(
            caption,
            work_dir / f"overlay-{index:02d}.png",
            eyebrow=brief.full_address.upper() if index == 0 else "",
        )
        clips.append(
            Clip(
                source=photo,
                duration=round(per_photo, 3),
                key="intro" if index == 0 else "",
                overlay=overlay,
                zoom="in" if index % 2 == 0 else "out",
                label=caption,
            )
        )

    # --- slide -------------------------------------------------------------
    clips.append(
        Clip(source=slides.price_old, duration=OLD_PRICE_DURATION, zoom="still", label="prezzo precedente")
    )
    clips.append(
        Clip(
            source=slides.price_new,
            duration=round(durations.get("price", 4.0) + PAD["price"], 3),
            key="price",
            zoom="still",
            label="nuovo prezzo",
        )
    )
    if slides.event is not None:
        clips.append(
            Clip(
                source=slides.event,
                duration=round(durations.get("event", 4.0) + PAD["event"], 3),
                key="event",
                zoom="still",
                label="evento",
            )
        )
    clips.append(
        Clip(
            source=slides.cta,
            duration=round(durations.get("cta", 4.0) + PAD["cta"], 3),
            key="cta",
            zoom="still",
            label="CTA",
        )
    )

    timeline = Timeline(clips=clips, transition=transition)
    return _fit_to_budget(timeline, max_duration)


def _fit_to_budget(timeline: Timeline, max_duration: float) -> Timeline:
    """Rientra nel limite concordato accorciando prima le foto, mai il parlato."""
    if timeline.total <= max_duration:
        return timeline

    photos = [c for c in timeline.clips if c.overlay is not None]
    excess = timeline.total - max_duration
    trimmable = sum(c.duration - MIN_PHOTO for c in photos)
    if trimmable > 0:
        factor = min(excess / trimmable, 1.0)
        for clip in photos:
            clip.duration = round(clip.duration - (clip.duration - MIN_PHOTO) * factor, 3)
        timeline = Timeline(clips=timeline.clips, transition=timeline.transition)
        log.info("scene foto accorciate per rientrare in %.0fs", max_duration)

    if timeline.total > max_duration:
        log.warning(
            "Il video dura %.1fs, oltre il limite di %.0fs: il parlato non viene tagliato "
            "automaticamente. Accorcia i testi in narration.video oppure alza --max-duration.",
            timeline.total,
            max_duration,
        )
    return timeline
