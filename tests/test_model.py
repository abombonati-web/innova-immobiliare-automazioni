"""Brief immobile: derivati, override CLI e regola 'zero dati inventati'."""

import pytest

from innova_property_kit.model import MissingDataError, PropertyBrief


def test_petrarca_matches_official_scheda(petrarca):
    assert petrarca.title == "Via F. Petrarca 36"
    assert petrarca.city == "Palermo"
    assert (petrarca.old_price, petrarca.new_price) == (168000, 155000)
    assert petrarca.saving == 13000
    assert petrarca.surface_sqm == 90
    assert petrarca.price_per_sqm == 1722  # 155.000 / 90 mq
    assert petrarca.event.date_long == "mercoledì 5 agosto"
    assert petrarca.event.slots == ["12:00", "15:30"]
    assert petrarca.slug == "via-petrarca-36"
    assert petrarca.short_name == "Petrarca36"


def test_price_per_sqm_is_none_without_surface():
    brief = PropertyBrief(address="Via X 1", city="Palermo", old_price=100000, new_price=90000)
    assert brief.price_per_sqm is None, "senza metratura il €/mq non si inventa"


def test_missing_required_data_is_reported_not_guessed():
    with pytest.raises(MissingDataError) as excinfo:
        PropertyBrief.from_dict({"property": {"name": "Via Ignota 1"}}).validate()
    missing = " ".join(excinfo.value.missing)
    assert "price.old" in missing and "price.new" in missing and "property.city" in missing


def test_event_without_slots_is_rejected():
    data = {
        "property": {"address": "Via X 1", "city": "Palermo"},
        "price": {"old": 100000, "new": 90000},
        "event": {"date": "2026-08-05", "slots": []},
    }
    with pytest.raises(MissingDataError) as excinfo:
        PropertyBrief.from_dict(data).validate()
    assert any("event.slots" in m for m in excinfo.value.missing)


def test_new_price_must_be_lower():
    brief = PropertyBrief(address="Via X 1", city="Palermo", old_price=90000, new_price=100000)
    with pytest.raises(ValueError, match="inferiore"):
        brief.validate()


def test_cli_overrides_replace_brief_values(petrarca):
    petrarca.apply_overrides(
        old_price=170000, new_price=160000, event_date="2026-09-10",
        event_slots="10:00,17:45", phone=None,
    )
    assert petrarca.saving == 10000
    assert petrarca.event.date_iso == "2026-09-10"
    assert petrarca.event.slots == ["10:00", "17:45"]
    assert petrarca.phone == "+39 339 418 5631", "None non deve sovrascrivere"


def test_facts_have_speakable_values(petrarca):
    surface = next(f for f in petrarca.facts if f.label == "Superficie")
    assert surface.value == "90 mq"
    assert surface.spoken_text == "novanta metri quadri"


def test_maps_urls(petrarca):
    assert "output=embed" in petrarca.maps_embed_url
    assert "Petrarca" in petrarca.maps_url and "output=embed" not in petrarca.maps_url
    assert petrarca.phone_tel == "+393394185631"
