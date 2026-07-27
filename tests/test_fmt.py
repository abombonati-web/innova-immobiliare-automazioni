"""Formattazione italiana: prezzi, date, numeri a parole, slug."""

import pytest

from innova_property_kit import fmt


@pytest.mark.parametrize(
    "value,expected",
    [(155000, "€ 155.000"), (168000, "€ 168.000"), (1722, "€ 1.722"), (900, "€ 900")],
)
def test_euro(value, expected):
    assert fmt.euro(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (155000, "centocinquantacinquemila euro"),
        (168000, "centosessantottomila euro"),
        (13000, "tredicimila euro"),
        (1722, "millesettecentoventidue euro"),
        (1000, "mille euro"),
        (1_000_000, "un milione euro"),
        (21, "ventuno euro"),
        (180, "centottanta euro"),
    ],
)
def test_euro_spoken(value, expected):
    assert fmt.euro_spoken(value) == expected


def test_date_long_italian():
    assert fmt.date_long("2026-08-05") == "mercoledì 5 agosto"
    assert fmt.date_short("2026-08-05") == "5 agosto 2026"


def test_slots():
    assert fmt.slots_text(["12:00", "15:30"]) == "ore 12:00 e 15:30"
    assert fmt.slots_spoken(["12:00", "15:30"]) == "alle 12 e alle 15 e 30"
    assert fmt.slots_text([]) == ""


def test_phone_spoken_drops_prefix_and_groups_digits():
    assert fmt.phone_spoken("+39 339 418 5631") == "3 3 9, 4 1 8, 5 6 3 1"


def test_speakable_expands_abbreviations():
    assert fmt.speakable("90 mq al piano") == "90 metri quadri al piano"


def test_slugs_match_project_filenames():
    assert fmt.slug("Via F. Petrarca 36") == "via-f-petrarca-36"
    # i nomi dei deliverable perdono le iniziali puntate
    assert fmt.file_slug("Via F. Petrarca 36") == "via-petrarca-36"
    assert fmt.camel("Via F. Petrarca 36") == "Petrarca36"
