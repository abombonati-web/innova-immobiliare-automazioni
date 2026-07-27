"""La scaletta rientra nel limite accorciando le foto, mai il parlato."""

import pytest

from innova_property_kit.reel import MIN_PHOTO, _fit_to_budget
from innova_property_kit.video import Clip, Timeline


def _timeline(tmp_path, photo_durations, slide_durations):
    photo = tmp_path / "foto.jpg"
    overlay = tmp_path / "overlay.png"
    slide = tmp_path / "slide.png"
    for path in (photo, overlay, slide):
        path.touch()
    clips = [Clip(source=photo, duration=d, overlay=overlay) for d in photo_durations]
    clips += [Clip(source=slide, duration=d, key="price") for d in slide_durations]
    return Timeline(clips=clips, transition=0.3)


def test_timeline_within_budget_is_untouched(tmp_path):
    timeline = _timeline(tmp_path, [2.0] * 4, [6.0, 5.0])
    before = [c.duration for c in timeline.clips]
    assert _fit_to_budget(timeline, 30.0).clips == timeline.clips
    assert [c.duration for c in timeline.clips] == before


def test_photos_are_shortened_first(tmp_path):
    timeline = _timeline(tmp_path, [3.0] * 6, [8.0, 7.0, 6.0])
    assert timeline.total > 30.0
    fitted = _fit_to_budget(timeline, 30.0)

    slides = [c for c in fitted.clips if c.overlay is None]
    assert [c.duration for c in slides] == [8.0, 7.0, 6.0], "il parlato non si tocca"
    photos = [c for c in fitted.clips if c.overlay is not None]
    assert all(c.duration >= MIN_PHOTO for c in photos)
    assert fitted.total == pytest.approx(30.0, abs=0.05)


def test_warns_instead_of_cutting_speech(tmp_path, caplog):
    # solo slide parlate: non c'e nulla da accorciare senza tagliare la voce
    timeline = _timeline(tmp_path, [], [20.0, 20.0])
    with caplog.at_level("WARNING"):
        fitted = _fit_to_budget(timeline, 30.0)
    assert fitted.total > 30.0
    assert "narration.video" in caplog.text
