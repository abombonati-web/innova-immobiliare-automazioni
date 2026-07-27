"""Sincronizzazione audio/video: gli offset di `xfade` non sono la somma delle durate."""

import pytest

from innova_property_kit.video import Clip, Timeline, scene_offsets, total_duration


def test_offsets_account_for_each_transition():
    durations = [2.0, 3.0, 4.0]
    # senza transizioni sarebbero 0, 2, 5; ogni xfade sovrappone 0.3s
    assert scene_offsets(durations, 0.3) == [0.0, 1.7, 4.4]


def test_total_duration_removes_every_overlap():
    assert total_duration([2.0, 3.0, 4.0], 0.3) == pytest.approx(8.4)
    assert total_duration([5.0], 0.3) == 5.0
    assert total_duration([], 0.3) == 0.0


def test_offset_equals_previous_offset_plus_visible_span():
    durations = [1.5, 1.5, 6.0, 5.0]
    transition = 0.3
    starts = scene_offsets(durations, transition)
    for index in range(1, len(starts)):
        visible = durations[index - 1] - transition
        assert starts[index] == pytest.approx(starts[index - 1] + visible)


def test_last_scene_fits_inside_total():
    durations = [1.4, 1.4, 1.4, 1.8, 7.5, 6.2, 5.9]
    transition = 0.3
    starts = scene_offsets(durations, transition)
    assert starts[-1] + durations[-1] == pytest.approx(total_duration(durations, transition))


def test_timeline_exposes_scene_start_by_key(tmp_path):
    source = tmp_path / "x.png"
    source.touch()
    timeline = Timeline(
        clips=[
            Clip(source=source, duration=2.0, key="intro"),
            Clip(source=source, duration=3.0, key="price"),
            Clip(source=source, duration=4.0, key="cta"),
        ],
        transition=0.3,
    )
    assert timeline.start_of("intro") == 0.0
    assert timeline.start_of("price") == pytest.approx(1.7)
    assert timeline.start_of("cta") == pytest.approx(4.4)
    assert timeline.start_of("mancante") is None
    assert timeline.total == pytest.approx(8.4)


def test_clip_frames_never_below_two(tmp_path):
    source = tmp_path / "x.png"
    source.touch()
    assert Clip(source=source, duration=0.0).frames == 2
    assert Clip(source=source, duration=1.5).frames == 45  # 30 fps
