"""Testi parlati: copione video (social) e presentazione landing (istituzionale).

I due testi **non** coincidono per scelta:

* il video e un hook social — tono caldo, entusiasta, frasi brevi;
* la landing e un riepilogo istituzionale — l'utente sta gia leggendo con calma,
  quindi la voce riassume in modo netto e conciso, senza tono da spot.

Il copione viene composto solo con i dati presenti nel brief. Se serve un testo
diverso lo si scrive a mano in `narration.video` / `narration.landing` e questo
modulo viene bypassato.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import fmt
from .brand import AGENCY, PAYOFF
from .model import PropertyBrief


@dataclass
class Segment:
    """Un blocco di parlato agganciato a una scena del video."""

    key: str  # intro | price | event | cta
    text: str


_SINGULAR = {"i": "o", "e": "a"}


def _singular(label: str) -> str:
    """`Vani` -> `vano`, `Camere` -> `camera` (per i conteggi pari a 1)."""
    label = label.lower()
    return label[:-1] + _SINGULAR[label[-1]] if label[-1] in _SINGULAR else label


def _fact_phrase(fact) -> str:
    """Trasforma una coppia label/valore in una frase leggibile ad alta voce."""
    if fact.spoken:
        return fact.spoken
    value = fact.value.strip()
    label = fact.label.strip()
    if value.lower() in {"no", "assente", "non presente"}:
        return ""
    if value.lower() in {"si", "sì", "presente"}:
        return f"con {label.lower()}"
    if value.replace(".", "").isdigit():
        count = float(value.replace(".", ""))
        return f"{value} {_singular(label) if count == 1 else label.lower()}"
    return fmt.speakable(f"{label.lower()} {value.lower()}")


def _facts_sentence(brief: PropertyBrief, limit: int = 4) -> str:
    phrases = [p for p in (_fact_phrase(f) for f in brief.facts[:limit] if f.value) if p]
    if not phrases:
        return ""
    sentence = ", ".join(phrases)
    return sentence[0].upper() + sentence[1:] + "."


def video_script(brief: PropertyBrief) -> list[Segment]:
    """Copione del reel, in quattro segmenti allineati alle scene."""
    if brief.narration_video:
        keys = ["intro", "price", "event", "cta"]
        return [
            Segment(key=keys[i] if i < len(keys) else f"extra{i}", text=text)
            for i, text in enumerate(brief.narration_video)
        ]

    # Il reel sta in ~30 secondi: ogni segmento dice una cosa sola e lascia il
    # resto alle slide (prezzo al mq, numero di telefono, indirizzo sono a video).

    # --- intro sulle foto --------------------------------------------------
    intro = [f"{brief.city}, {brief.address}."]
    facts = _facts_sentence(brief, limit=3)
    intro.append(facts or "Una casa pronta da vivere.")

    # --- reveal prezzo -----------------------------------------------------
    price = [
        f"Il prezzo scende da {fmt.euro_spoken(brief.old_price)} "
        f"a {fmt.euro_spoken(brief.new_price)}.",
        f"Sono {fmt.euro_spoken(brief.saving)} in meno.",
    ]

    segments = [
        Segment("intro", " ".join(intro)),
        Segment("price", " ".join(price)),
    ]

    # --- evento ------------------------------------------------------------
    if brief.event:
        segments.append(
            Segment(
                "event",
                f"Ti aspettiamo {brief.event.date_long} per l'{brief.event.label}, "
                f"{fmt.slots_spoken(brief.event.slots)}.",
            )
        )

    # --- chiamata all'azione ----------------------------------------------
    action = "prenota la tua visita" if brief.event else "prenota un appuntamento"
    segments.append(Segment("cta", f"Chiama ora e {action}. {AGENCY.name}. {PAYOFF}."))
    return segments


def landing_script(brief: PropertyBrief) -> list[str]:
    """Presentazione vocale della landing: paragrafi brevi, tono professionale."""
    if brief.narration_landing:
        return list(brief.narration_landing)

    paragraphs = [
        f"{brief.address}, {brief.city}."
        + (f" {_facts_sentence(brief)}" if _facts_sentence(brief) else "")
    ]
    if brief.description:
        paragraphs.append(brief.description[0])

    price = (
        f"Il prezzo passa da {fmt.euro_spoken(brief.old_price)} "
        f"a {fmt.euro_spoken(brief.new_price)}, con un risparmio di "
        f"{fmt.euro_spoken(brief.saving)}."
    )
    if brief.price_per_sqm:
        price += f" Circa {fmt.euro_spoken(brief.price_per_sqm)} al metro quadro."
    paragraphs.append(price)

    if brief.event:
        paragraphs.append(
            f"L'{brief.event.label} dedicata a questo immobile e in programma "
            f"{brief.event.date_long}, {fmt.slots_spoken(brief.event.slots)}. "
            "Le visite sono su prenotazione."
        )

    paragraphs.append(
        f"Per informazioni e appuntamenti: {fmt.phone_spoken(brief.phone)}. "
        f"{AGENCY.name}. {PAYOFF}."
    )
    return paragraphs


def photo_captions(brief: PropertyBrief, count: int) -> list[str]:
    """Didascalie delle foto: quelle del brief, altrimenti i quick facts."""
    captions = list(brief.photo_captions)
    if not captions:
        captions = [f"{f.label}: {f.value}" for f in brief.facts]
    if not captions:
        captions = [brief.full_address]
    # la prima inquadratura porta sempre l'indirizzo
    captions = [brief.full_address] + captions
    return (captions * (count // max(len(captions), 1) + 1))[:count]
