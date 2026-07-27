"""Landing page: file autonomo, sezioni condizionate ai dati del brief."""

import re

import pytest
from PIL import Image

from innova_property_kit import landing
from innova_property_kit.model import PropertyBrief


@pytest.fixture
def photos(tmp_path):
    paths = []
    for index in range(3):
        path = tmp_path / f"foto-{index}.jpg"
        Image.new("RGB", (1200, 900), (200 - index * 20, 180, 160)).save(path)
        paths.append(path)
    return paths


@pytest.fixture
def page(petrarca, photos, tmp_path):
    out = tmp_path / "landing.html"
    landing.build_landing_html(petrarca, photos, out)
    return out.read_text(encoding="utf-8")


def test_no_placeholder_is_left_unresolved(page):
    assert re.search(r"\{\{[A-Z0-9_]+\}\}", page) is None


def test_photos_are_embedded_not_linked(page):
    assert page.count("data:image/jpeg;base64,") >= 4  # hero + galleria + dettagli
    external = re.findall(r'src="(?!data:)([^"]+)"', page)
    assert external == [], f"riferimenti esterni non ammessi: {external}"


def test_only_fonts_and_map_reach_the_network(page):
    hosts = set(re.findall(r"https://([a-z.]+)/", page))
    assert hosts <= {"fonts.googleapis.com", "fonts.gstatic.com", "www.google.com", "formsubmit.co"}


def test_prices_and_event_are_rendered(page):
    assert "€ 168.000" in page and "€ 155.000" in page
    assert "Risparmi € 13.000" in page
    assert "circa € 1.722/mq" in page
    assert "Mercoledì 5 agosto" in page and "ore 12:00 e 15:30" in page


def test_sections_from_the_brief_are_present(page):
    assert "Perché è un'occasione" in page
    assert "Per chi è perfetta" in page
    assert "I dettagli tecnici" in page
    assert "output=embed" in page  # mappa
    assert "Pompa di calore" in page


def test_form_has_utm_honeypot_and_privacy(page):
    for field in ("utm_source", "utm_medium", "utm_campaign", "utm_content"):
        assert f'name="{field}"' in page
    assert 'name="_honey"' in page
    assert 'id="privacy" required' in page
    assert "formsubmit.co/ajax/info@innovaimmobiliare.it" in page


def test_form_messages_are_hidden_until_javascript_shows_them(page):
    assert ".form-msg{display:none" in page
    assert ".form-msg.show{display:block}" in page
    assert 'class="form-msg ok" id="msgOk"' in page
    assert "style.display" not in page, "la visibilita passa dalla classe .show"


def test_audio_player_only_when_audio_is_provided(petrarca, photos, tmp_path):
    without = tmp_path / "senza.html"
    landing.build_landing_html(petrarca, photos, without)
    assert "narrationAudio" not in without.read_text(encoding="utf-8")

    mp3 = tmp_path / "voce.mp3"
    mp3.write_bytes(b"\xff\xfb\x90\x00" + b"\x00" * 512)
    with_audio = tmp_path / "con.html"
    landing.build_landing_html(petrarca, photos, with_audio, audio_path=mp3)
    text = with_audio.read_text(encoding="utf-8")
    assert 'id="narrationAudio"' in text or "id='narrationAudio'" in text
    assert "data:audio/mpeg;base64," in text
    assert "Ascolta la presentazione dell'immobile" in text


def test_missing_optional_sections_are_omitted_not_invented(photos, tmp_path):
    minimal = PropertyBrief(
        address="Via Ignota 1", city="Palermo", old_price=200000, new_price=180000
    ).validate()
    out = tmp_path / "minima.html"
    landing.build_landing_html(minimal, photos, out)
    text = out.read_text(encoding="utf-8")
    assert "Perché è un'occasione" not in text
    assert "Per chi è perfetta" not in text
    assert "I dettagli tecnici" not in text
    assert "La zona" not in text
    assert "Innova Experience" not in text
    assert "€ 180.000" in text  # il prezzo resta
    assert "/mq" not in text  # senza metratura niente €/mq


def test_reduced_motion_and_lazy_loading(page):
    assert "prefers-reduced-motion" in page
    assert "IntersectionObserver" in page
    assert 'loading="lazy"' in page
