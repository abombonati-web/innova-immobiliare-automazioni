"""CLI: parsing degli argomenti e precedenza degli override sul brief."""

import pytest

from innova_property_kit.cli import build_parser, load_brief
from innova_property_kit.model import MissingDataError

BRIEF = "briefs/via-petrarca-36.json"


def parse(*argv):
    return build_parser().parse_args(list(argv))


def test_defaults_match_the_documented_workflow():
    args = parse("--brief", BRIEF)
    assert args.photos == 6
    assert args.video_tone == "euforico"
    assert args.video_music == "jazz"
    assert args.landing_tone == "professionale"
    assert args.max_duration == 30.0
    assert args.bpm == 92


def test_reference_invocation_is_accepted():
    args = parse(
        "--property", "Via F. Petrarca 36", "--city", "Palermo",
        "--drive-folder-id", "1E7CcGEd8MUOeovb2F3SNf1D0PE-OMexI",
        "--old-price", "168000", "--new-price", "155000",
        "--event-date", "2026-08-05", "--event-slots", "12:00,15:30",
        "--phone", "+39 339 418 5631",
        "--video-tone", "euforico", "--video-music", "jazz",
        "--output-dir", "/tmp/out",
    )
    brief = load_brief(args)
    assert brief.title == "Via F. Petrarca 36"
    assert (brief.old_price, brief.new_price) == (168000, 155000)
    assert brief.event.slots == ["12:00", "15:30"]


def test_city_can_travel_inside_property():
    brief = load_brief(
        parse("--property", "Via F. Petrarca 36, Palermo", "--old-price", "168000",
              "--new-price", "155000")
    )
    assert brief.address == "Via F. Petrarca 36"
    assert brief.city == "Palermo"


def test_cli_values_win_over_the_brief_file():
    brief = load_brief(parse("--brief", BRIEF, "--new-price", "149000"))
    assert brief.new_price == 149000
    assert brief.old_price == 168000, "gli altri campi restano quelli del brief"
    assert brief.saving == 19000


def test_without_brief_or_property_it_stops():
    with pytest.raises(MissingDataError):
        load_brief(parse())


def test_property_alone_is_not_enough_to_invent_a_price():
    with pytest.raises(MissingDataError) as excinfo:
        load_brief(parse("--property", "Via Ignota 1"))
    assert any("price" in m for m in excinfo.value.missing)


def test_invalid_tone_is_rejected():
    with pytest.raises(SystemExit):
        parse("--brief", BRIEF, "--video-tone", "sussurrato")
