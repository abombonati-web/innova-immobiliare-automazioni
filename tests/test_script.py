"""Copioni: il video e un hook social, la landing un riepilogo istituzionale."""

from innova_property_kit import script
from innova_property_kit.model import PropertyBrief


def test_video_script_has_one_segment_per_scene(petrarca):
    segments = script.video_script(petrarca)
    assert [s.key for s in segments] == ["intro", "price", "event", "cta"]


def test_video_script_only_quotes_brief_numbers(petrarca):
    text = " ".join(s.text for s in script.video_script(petrarca))
    assert "centosessantottomila euro" in text  # 168.000
    assert "centocinquantacinquemila euro" in text  # 155.000
    assert "tredicimila euro" in text  # risparmio calcolato
    assert "mercoledì 5 agosto" in text
    assert "Progetta il tuo futuro" in text


def test_video_script_is_shorter_than_landing_script(petrarca):
    video_chars = sum(len(s.text) for s in script.video_script(petrarca))
    landing_chars = sum(len(p) for p in script.landing_script(petrarca))
    assert video_chars < landing_chars, "il reel deve stare in ~30s, la landing no"


def test_landing_script_differs_from_video_script(petrarca):
    video = " ".join(s.text for s in script.video_script(petrarca))
    landing = " ".join(script.landing_script(petrarca))
    assert video != landing
    assert "Chiama ora" not in landing, "niente tono da spot nella landing"


def test_handwritten_narration_overrides_the_generator(petrarca):
    petrarca.narration_video = ["Primo blocco.", "Secondo blocco."]
    petrarca.narration_landing = ["Testo istituzionale."]
    assert [s.text for s in script.video_script(petrarca)] == ["Primo blocco.", "Secondo blocco."]
    assert script.landing_script(petrarca) == ["Testo istituzionale."]


def test_no_event_means_no_event_segment():
    brief = PropertyBrief(
        address="Via X 1", city="Palermo", old_price=100000, new_price=90000
    ).validate()
    keys = [s.key for s in script.video_script(brief)]
    assert keys == ["intro", "price", "cta"]
    assert "appuntamento" in script.video_script(brief)[-1].text


def test_fact_phrases_are_readable_aloud(petrarca):
    intro = script.video_script(petrarca)[0].text
    assert "4 vani" in intro
    assert "2 camere" in intro
    assert "novanta metri quadri" in intro.lower()


def test_singular_labels_for_counts_of_one():
    brief = PropertyBrief.from_dict(
        {
            "property": {"address": "Via X 1", "city": "Palermo"},
            "price": {"old": 100000, "new": 90000},
            "facts": [{"label": "Bagni", "value": "1"}, {"label": "Vani", "value": "1"}],
        }
    ).validate()
    intro = script.video_script(brief)[0].text
    assert "1 bagno" in intro and "1 vano" in intro


def test_photo_captions_start_with_the_address(petrarca):
    captions = script.photo_captions(petrarca, 6)
    assert len(captions) == 6
    assert captions[0] == "Via F. Petrarca 36, Palermo"
