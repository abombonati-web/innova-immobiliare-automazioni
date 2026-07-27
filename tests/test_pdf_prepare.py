"""Adattamenti di stampa: senza rete, senza JS, senza iframe, senza audio."""

import pytest

from innova_property_kit import landing, pdf


@pytest.fixture(autouse=True)
def offline_fonts(monkeypatch):
    """Evita di scaricare i TTF: qui interessa la struttura, non i byte del font."""
    monkeypatch.setattr(pdf, "font_base64", lambda weight=400: f"FAKE{weight}")


@pytest.fixture
def print_html(petrarca, tmp_path):
    from PIL import Image

    photo = tmp_path / "foto.jpg"
    Image.new("RGB", (900, 700), (190, 180, 170)).save(photo)
    mp3 = tmp_path / "voce.mp3"
    mp3.write_bytes(b"\xff\xfb\x90\x00" + b"\x00" * 256)

    out = tmp_path / "landing.html"
    landing.build_landing_html(petrarca, [photo, photo], out, audio_path=mp3)
    return pdf.prepare_for_print(
        out.read_text(encoding="utf-8"), maps_url=petrarca.maps_url, address=petrarca.full_address
    )


def test_map_iframe_becomes_a_text_link(print_html):
    assert "<iframe" not in print_html
    assert "output=embed" not in print_html
    assert "Apri su Google Maps" in print_html
    assert "Via F. Petrarca 36, Palermo" in print_html


def test_google_fonts_links_are_replaced_by_embedded_faces(print_html):
    assert "fonts.googleapis.com" not in print_html
    assert "fonts.gstatic.com" not in print_html
    assert "@font-face" in print_html
    assert "base64,FAKE700" in print_html


def test_reveal_animations_are_forced_visible(print_html):
    assert ".reveal{opacity:1 !important" in print_html
    assert "transition:none !important" in print_html


def test_audio_is_replaced_by_a_note(print_html):
    assert "<audio" not in print_html
    assert "data:audio/mpeg" not in print_html
    assert "presentazione vocale" in print_html


def test_no_javascript_survives(print_html):
    assert "<script" not in print_html
    assert "IntersectionObserver" not in print_html


def test_grid_layouts_get_a_webkit_fallback(print_html):
    # il WebKit di wkhtmltopdf non conosce CSS Grid
    assert ".facts-grid{display:block" in print_html
    assert ".card{display:inline-block" in print_html
    assert ".gallery figure{display:inline-block" in print_html


def test_photos_stay_embedded(print_html):
    assert "data:image/jpeg;base64," in print_html
