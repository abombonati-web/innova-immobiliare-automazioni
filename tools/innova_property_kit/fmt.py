"""Formattazione italiana (prezzi, date, slug) senza dipendere dai locale di sistema."""

from __future__ import annotations

import datetime as _dt
import re
import unicodedata

WEEKDAYS = [
    "lunedi",
    "martedi",
    "mercoledi",
    "giovedi",
    "venerdi",
    "sabato",
    "domenica",
]
WEEKDAYS_ACCENTED = [
    "lunedì",
    "martedì",
    "mercoledì",
    "giovedì",
    "venerdì",
    "sabato",
    "domenica",
]
MONTHS = [
    "gennaio",
    "febbraio",
    "marzo",
    "aprile",
    "maggio",
    "giugno",
    "luglio",
    "agosto",
    "settembre",
    "ottobre",
    "novembre",
    "dicembre",
]


def euro(value: int | float, *, symbol: bool = True) -> str:
    """`155000` -> `€ 155.000` (separatore migliaia italiano)."""
    n = int(round(value))
    body = f"{n:,}".replace(",", ".")
    return f"€ {body}" if symbol else body


def euro_spoken(value: int | float) -> str:
    """Prezzo pronunciabile dal TTS: `155000` -> `centocinquantacinquemila euro`."""
    return f"{_spell_number(int(round(value)))} euro"


def parse_date(value: str | _dt.date) -> _dt.date:
    if isinstance(value, _dt.date):
        return value
    return _dt.date.fromisoformat(str(value).strip())


def date_long(value: str | _dt.date, *, weekday: bool = True, accented: bool = True) -> str:
    """`2026-08-05` -> `mercoledì 5 agosto`."""
    d = parse_date(value)
    names = WEEKDAYS_ACCENTED if accented else WEEKDAYS
    month = MONTHS[d.month - 1]
    if weekday:
        return f"{names[d.weekday()]} {d.day} {month}"
    return f"{d.day} {month}"


def date_short(value: str | _dt.date) -> str:
    """`2026-08-05` -> `5 agosto 2026`."""
    d = parse_date(value)
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def slots_text(slots: list[str], *, conjunction: str = "e") -> str:
    """`['12:00', '15:30']` -> `ore 12:00 e 15:30`."""
    slots = [s.strip() for s in slots if s.strip()]
    if not slots:
        return ""
    if len(slots) == 1:
        return f"ore {slots[0]}"
    return "ore " + ", ".join(slots[:-1]) + f" {conjunction} {slots[-1]}"


def slots_spoken(slots: list[str]) -> str:
    """`['12:00', '15:30']` -> `alle 12 e alle 15 e 30` (leggibile dal TTS)."""
    out = []
    for slot in slots:
        slot = slot.strip()
        if not slot:
            continue
        hh, _, mm = slot.partition(":")
        h = int(hh)
        m = int(mm or 0)
        out.append(f"alle {h}" if m == 0 else f"alle {h} e {m:02d}")
    if not out:
        return ""
    if len(out) == 1:
        return out[0]
    return ", ".join(out[:-1]) + f" e {out[-1]}"


ABBREVIATIONS = {
    "mq": "metri quadri",
    "m²": "metri quadri",
    "mc": "metri cubi",
    "n.": "numero",
    "p.": "piano",
    "ca.": "circa",
    "ca": "circa",
    "cl.": "classe",
    "kw": "chilowatt",
}


def speakable(text: str) -> str:
    """Espande le abbreviazioni che il TTS leggerebbe male (`90 mq` -> `90 metri quadri`)."""
    out = []
    for token in re.split(r"(\s+)", text):
        key = token.strip().lower()
        out.append(ABBREVIATIONS.get(key, token))
    return "".join(out)


def phone_spoken(phone: str) -> str:
    """`+39 339 418 5631` -> gruppi di cifre separati, letti chiaramente dal TTS."""
    digits = "".join(c for c in phone if c.isdigit())
    if digits.startswith("39") and len(digits) > 10:
        digits = digits[2:]
    groups = [digits[0:3], digits[3:6], digits[6:]]
    return ", ".join(" ".join(g) for g in groups if g)


def slug(value: str) -> str:
    """`Via F. Petrarca 36` -> `via-f-petrarca-36`."""
    norm = unicodedata.normalize("NFKD", value)
    norm = "".join(c for c in norm if not unicodedata.combining(c))
    norm = re.sub(r"[^a-zA-Z0-9]+", "-", norm).strip("-").lower()
    return re.sub(r"-{2,}", "-", norm)


def file_slug(value: str) -> str:
    """Slug per i nomi dei deliverable: via le iniziali puntate.

    `Via F. Petrarca 36` -> `via-petrarca-36` (come i file del progetto di riferimento).
    """
    parts = [p for p in slug(value).split("-") if len(p) > 1]
    return "-".join(parts) or slug(value)


def camel(value: str) -> str:
    """`Via F. Petrarca 36` -> `Petrarca36` (per i nomi file dei deliverable)."""
    parts = [p for p in re.split(r"[^A-Za-z0-9]+", slug(value).replace("-", " ")) if p]
    drop = {"via", "viale", "piazza", "corso", "vicolo", "largo", "contrada", "f", "v"}
    kept = [p for p in parts if p not in drop] or parts
    return "".join(p.capitalize() for p in kept)


# --------------------------------------------------------- numeri a parole ---
_UNITS = [
    "zero",
    "uno",
    "due",
    "tre",
    "quattro",
    "cinque",
    "sei",
    "sette",
    "otto",
    "nove",
    "dieci",
    "undici",
    "dodici",
    "tredici",
    "quattordici",
    "quindici",
    "sedici",
    "diciassette",
    "diciotto",
    "diciannove",
]
_TENS = {
    2: "venti",
    3: "trenta",
    4: "quaranta",
    5: "cinquanta",
    6: "sessanta",
    7: "settanta",
    8: "ottanta",
    9: "novanta",
}


def _spell_below_100(n: int) -> str:
    if n < 20:
        return _UNITS[n]
    tens, unit = divmod(n, 10)
    word = _TENS[tens]
    if unit == 0:
        return word
    if unit in (1, 8):  # elisione: ventuno, ventotto
        word = word[:-1]
    return word + _UNITS[unit]


def _spell_below_1000(n: int) -> str:
    hundreds, rest = divmod(n, 100)
    if hundreds == 0:
        return _spell_below_100(rest)
    prefix = "cento" if hundreds == 1 else _UNITS[hundreds] + "cento"
    if rest == 0:
        return prefix
    if rest in (80, 81, 88):  # centottanta
        prefix = prefix[:-1]
    return prefix + _spell_below_100(rest)


def _spell_number(n: int) -> str:
    """Numeri interi fino a 999.999.999, in italiano, per il TTS."""
    if n < 0:
        return "meno " + _spell_number(-n)
    if n < 1000:
        return _spell_below_1000(n)
    if n < 1_000_000:
        thousands, rest = divmod(n, 1000)
        head = "mille" if thousands == 1 else _spell_below_1000(thousands) + "mila"
        return head if rest == 0 else f"{head}{_spell_below_1000(rest)}"
    millions, rest = divmod(n, 1_000_000)
    head = "un milione" if millions == 1 else _spell_number(millions) + " milioni"
    return head if rest == 0 else f"{head} e {_spell_number(rest)}"
