"""Audio sintetizzato: effetti, letto jazz, ducking sotto la voce."""

import numpy as np
import pytest

from innova_property_kit import audio as au


def test_silence_and_duration_are_consistent():
    assert au.duration(au.silence(2.5)) == pytest.approx(2.5)


def test_place_extends_the_track_when_needed():
    track = au.silence(1.0)
    clip = np.ones(au.SAMPLE_RATE, dtype=np.float32)
    extended = au.place(track, clip, 0.8)
    assert au.duration(extended) == pytest.approx(1.8)
    assert extended[: int(0.8 * au.SAMPLE_RATE)].max() == 0.0


def test_sfx_are_bounded_and_decaying():
    for clip in (au.ding(), au.bell(), au.thump()):
        assert clip.size > 0
        assert np.abs(clip).max() <= 1.0
        head = np.abs(clip[: clip.size // 4]).mean()
        tail = np.abs(clip[-clip.size // 4 :]).mean()
        assert tail < head, "un accento sonoro deve spegnersi"


def test_jazz_bed_has_the_requested_length_and_fades():
    bed = au.synthesize_jazz_bed(6.0, bpm=92)
    assert au.duration(bed) == pytest.approx(6.0, abs=0.01)
    assert np.abs(bed[:200]).max() < 0.02, "attacco in dissolvenza"
    assert np.abs(bed[-200:]).max() < 0.02, "coda in dissolvenza"


def test_note_hz_reference_pitch():
    assert au.note_hz("A", 4) == pytest.approx(440.0)
    assert au.note_hz("C", 4) == pytest.approx(261.63, abs=0.01)


def test_ducking_lowers_the_bed_only_under_the_voice():
    bed = np.ones(au.SAMPLE_RATE * 4, dtype=np.float32) * 0.5
    voice = np.zeros_like(bed)
    voice[au.SAMPLE_RATE : au.SAMPLE_RATE * 2] = 0.8  # voce nel secondo 1-2

    ducked = au.duck(bed, voice, amount=0.55)
    under_voice = np.abs(ducked[int(au.SAMPLE_RATE * 1.4) : int(au.SAMPLE_RATE * 1.6)]).mean()
    in_silence = np.abs(ducked[int(au.SAMPLE_RATE * 3.4) : int(au.SAMPLE_RATE * 3.6)]).mean()
    assert under_voice < in_silence * 0.6


def test_mixdown_keeps_the_voice_on_top():
    voice = np.sin(np.linspace(0, 400, au.SAMPLE_RATE * 2)).astype(np.float32) * 0.6
    bed = np.ones(au.SAMPLE_RATE * 2, dtype=np.float32) * 0.5
    mix = au.mixdown(voice, bed=bed, bed_gain=0.30)
    assert np.abs(mix).max() <= 1.0
    assert mix.size == voice.size


def test_write_wav_roundtrip(tmp_path):
    from scipy.io import wavfile

    samples = np.sin(np.linspace(0, 50, 4410)).astype(np.float32) * 0.5
    path = au.write_wav(tmp_path / "a.wav", samples)
    rate, data = wavfile.read(path)
    assert rate == au.SAMPLE_RATE
    assert data.dtype == np.int16 and data.size == samples.size
