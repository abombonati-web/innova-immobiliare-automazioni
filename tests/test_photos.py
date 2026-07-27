"""Reperimento foto: SENZA LOGO, ordinamento naturale, manifest."""

import base64
import json

import pytest

from innova_property_kit import photos


def _make(path, name):
    path.mkdir(parents=True, exist_ok=True)
    (path / name).write_bytes(b"\xff\xd8\xff\xdb")  # header JPEG fittizio


def test_natural_sort_beats_lexicographic():
    names = ["INNOVA-10.jpg", "INNOVA-2.jpg", "INNOVA-1.jpg", "INNOVA-21.jpg"]
    assert sorted(names, key=photos.natural_key) == [
        "INNOVA-1.jpg",
        "INNOVA-2.jpg",
        "INNOVA-10.jpg",
        "INNOVA-21.jpg",
    ]


def test_senza_logo_is_preferred_over_con_logo(tmp_path):
    _make(tmp_path / "FOTO" / "CON LOGO", "INNOVA-1.jpg")
    _make(tmp_path / "FOTO" / "SENZA LOGO", "INNOVA-1.jpg")
    _make(tmp_path / "FOTO" / "SENZA LOGO", "INNOVA-2.jpg")

    found = photos.photos_from_dir(tmp_path, 6)
    assert [p.parent.name for p in found] == ["SENZA LOGO", "SENZA LOGO"]
    assert [p.name for p in found] == ["INNOVA-1.jpg", "INNOVA-2.jpg"]


def test_macosx_and_resource_forks_are_ignored(tmp_path):
    _make(tmp_path / "__MACOSX", "INNOVA-1.jpg")
    _make(tmp_path, "._INNOVA-2.jpg")
    _make(tmp_path, "INNOVA-3.jpg")
    assert [p.name for p in photos.photos_from_dir(tmp_path, 6)] == ["INNOVA-3.jpg"]


def test_limit_is_respected(tmp_path):
    for index in range(1, 10):
        _make(tmp_path, f"INNOVA-{index}.jpg")
    assert len(photos.photos_from_dir(tmp_path, 6)) == 6


def test_empty_folder_raises(tmp_path):
    (tmp_path / "vuota").mkdir()
    with pytest.raises(FileNotFoundError):
        photos.photos_from_dir(tmp_path / "vuota", 6)


def test_manifest_accepts_base64_and_paths(tmp_path):
    source = tmp_path / "originale.jpg"
    source.write_bytes(b"\xff\xd8\xff\xdb-src")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            [
                {"name": "01.jpg", "base64": base64.b64encode(b"\xff\xd8-b64").decode()},
                {"name": "02.jpg", "path": str(source)},
            ]
        )
    )
    saved = photos.photos_from_manifest(manifest, tmp_path / "out", 6)
    assert [p.name for p in saved] == ["01.jpg", "02.jpg"]
    assert saved[0].read_bytes() == b"\xff\xd8-b64"
    assert saved[1].read_bytes() == b"\xff\xd8\xff\xdb-src"


def test_manifest_accepts_data_urls(tmp_path):
    manifest = tmp_path / "m.json"
    encoded = base64.b64encode(b"jpegbytes").decode()
    manifest.write_text(json.dumps({"photos": [{"name": "a.jpg", "base64": f"data:image/jpeg;base64,{encoded}"}]}))
    saved = photos.photos_from_manifest(manifest, tmp_path / "out", 6)
    assert saved[0].read_bytes() == b"jpegbytes"


def test_no_source_is_an_explicit_error():
    with pytest.raises(ValueError, match="Nessuna sorgente foto"):
        photos.fetch_property_photos(6)
