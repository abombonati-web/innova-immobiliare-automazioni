"""Modello dati del brief immobile.

Regola ferrea del kit: **zero dati inventati**. Prezzo, metratura, vani e date
evento arrivano solo dal brief (JSON estratto dalla scheda ufficiale) o dai
parametri espliciti della CLI. Se un dato obbligatorio manca il tool si ferma e
lo chiede, non lo presume. I dati facoltativi mancanti fanno semplicemente
sparire la sezione corrispondente dalla landing page.
"""

from __future__ import annotations

import datetime as _dt
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import fmt
from .brand import AGENCY


class MissingDataError(ValueError):
    """Un dato obbligatorio non e stato fornito: va chiesto, non presunto."""

    def __init__(self, missing: list[str]) -> None:
        self.missing = missing
        lines = "\n".join(f"  - {m}" for m in missing)
        super().__init__(
            "Dati obbligatori mancanti nel brief (non vengono mai presunti):\n"
            f"{lines}\n\n"
            "Aggiungili al file JSON del brief oppure passali via CLI "
            "(--old-price, --new-price, --event-date, --event-slots, ...)."
        )


@dataclass
class Fact:
    """Voce della barra 'quick facts' (mq, vani, camere, ...)."""

    label: str
    value: str
    icon: str = ""
    spoken: str = ""

    @property
    def spoken_text(self) -> str:
        """Versione leggibile dal TTS (`90 mq` -> `90 metri quadri`)."""
        return self.spoken or fmt.speakable(self.value)

    @classmethod
    def from_any(cls, raw: Any) -> "Fact":
        if isinstance(raw, dict):
            return cls(
                label=str(raw["label"]).strip(),
                value=str(raw["value"]).strip(),
                icon=str(raw.get("icon", "")).strip(),
                spoken=str(raw.get("spoken", "")).strip(),
            )
        # forma compatta "Superficie: 90 mq"
        label, _, value = str(raw).partition(":")
        return cls(label=label.strip(), value=value.strip())


@dataclass
class Card:
    """Card generica con titolo e testo (occasione / target / vantaggi zona)."""

    title: str
    text: str
    icon: str = ""

    @classmethod
    def from_any(cls, raw: Any) -> "Card":
        if isinstance(raw, dict):
            return cls(
                title=str(raw.get("title", "")).strip(),
                text=str(raw.get("text", "")).strip(),
                icon=str(raw.get("icon", "")).strip(),
            )
        title, _, text = str(raw).partition(":")
        return cls(title=title.strip(), text=text.strip())


@dataclass
class Event:
    """Evento Innova Experience associato all'immobile."""

    date: _dt.date
    slots: list[str]
    label: str = "Innova Experience"
    note: str = ""

    @property
    def date_iso(self) -> str:
        return self.date.isoformat()

    @property
    def date_long(self) -> str:
        return fmt.date_long(self.date)

    @property
    def slots_text(self) -> str:
        return fmt.slots_text(self.slots)


@dataclass
class PropertyBrief:
    """Tutto cio che serve per generare video + landing di un immobile."""

    address: str
    city: str
    old_price: int
    new_price: int

    name: str = ""
    map_query: str = ""
    headline: str = ""
    eyebrow: str = ""
    surface_sqm: float | None = None
    description: list[str] = field(default_factory=list)
    facts: list[Fact] = field(default_factory=list)
    details: list[Fact] = field(default_factory=list)
    highlights: list[Card] = field(default_factory=list)
    targets: list[Card] = field(default_factory=list)
    zone_intro: str = ""
    zone_advantages: list[str] = field(default_factory=list)
    photo_captions: list[str] = field(default_factory=list)
    event: Event | None = None
    phone: str = AGENCY.phone
    narration_video: list[str] = field(default_factory=list)
    narration_landing: list[str] = field(default_factory=list)
    source: Path | None = None

    # ------------------------------------------------------------ derivati ---
    @property
    def title(self) -> str:
        return self.name or self.address

    @property
    def full_address(self) -> str:
        return f"{self.address}, {self.city}"

    @property
    def saving(self) -> int:
        return self.old_price - self.new_price

    @property
    def price_per_sqm(self) -> int | None:
        """€/mq sul nuovo prezzo. `None` se la metratura non e stata fornita."""
        if not self.surface_sqm:
            return None
        return int(round(self.new_price / self.surface_sqm))

    @property
    def slug(self) -> str:
        return fmt.file_slug(self.title)

    @property
    def short_name(self) -> str:
        return fmt.camel(self.title)

    @property
    def maps_url(self) -> str:
        from urllib.parse import quote_plus

        return f"https://www.google.com/maps?q={quote_plus(self.map_query or self.full_address)}"

    @property
    def maps_embed_url(self) -> str:
        from urllib.parse import quote_plus

        query = quote_plus(self.map_query or self.full_address)
        return f"https://www.google.com/maps?q={query}&output=embed"

    @property
    def phone_tel(self) -> str:
        return "+" + "".join(c for c in self.phone if c.isdigit())

    # ------------------------------------------------------------ costruttori ---
    @classmethod
    def from_dict(cls, data: dict[str, Any], *, source: Path | None = None) -> "PropertyBrief":
        prop = data.get("property", {}) or {}
        price = data.get("price", {}) or {}
        contact = data.get("contact", {}) or {}
        zone = data.get("zone", {}) or {}
        narration = data.get("narration", {}) or {}

        event_raw = data.get("event") or {}
        event = None
        if event_raw.get("date"):
            event = Event(
                date=fmt.parse_date(event_raw["date"]),
                slots=[str(s).strip() for s in (event_raw.get("slots") or []) if str(s).strip()],
                label=str(event_raw.get("label") or "Innova Experience"),
                note=str(event_raw.get("note") or ""),
            )

        description = prop.get("description") or []
        if isinstance(description, str):
            description = [description]

        return cls(
            address=str(prop.get("address") or "").strip(),
            city=str(prop.get("city") or "").strip(),
            old_price=_as_price(price.get("old")),
            new_price=_as_price(price.get("new")),
            name=str(prop.get("name") or "").strip(),
            map_query=str(prop.get("map_query") or "").strip(),
            headline=str(prop.get("headline") or "").strip(),
            eyebrow=str(prop.get("eyebrow") or "").strip(),
            surface_sqm=_as_float(prop.get("surface_sqm")),
            description=[str(p).strip() for p in description if str(p).strip()],
            facts=[Fact.from_any(f) for f in (data.get("facts") or [])],
            details=[Fact.from_any(f) for f in (data.get("details") or [])],
            highlights=[Card.from_any(c) for c in (data.get("highlights") or [])],
            targets=[Card.from_any(c) for c in (data.get("targets") or [])],
            zone_intro=str(zone.get("intro") or "").strip(),
            zone_advantages=[str(a).strip() for a in (zone.get("advantages") or []) if str(a).strip()],
            photo_captions=[str(c).strip() for c in (data.get("photo_captions") or [])],
            event=event,
            phone=str(contact.get("phone") or AGENCY.phone).strip(),
            narration_video=[str(s).strip() for s in (narration.get("video") or []) if str(s).strip()],
            narration_landing=[str(s).strip() for s in (narration.get("landing") or []) if str(s).strip()],
            source=source,
        )

    @classmethod
    def load(cls, path: str | Path) -> "PropertyBrief":
        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_dict(data, source=path)

    # ------------------------------------------------------------ override ---
    def apply_overrides(self, **overrides: Any) -> "PropertyBrief":
        """Applica gli override espliciti passati dalla CLI (valori `None` ignorati)."""
        for key, value in overrides.items():
            if value is None:
                continue
            if key == "event_date":
                date = fmt.parse_date(value)
                if self.event is None:
                    self.event = Event(date=date, slots=[])
                else:
                    self.event.date = date
            elif key == "event_slots":
                slots = value if isinstance(value, list) else [s for s in str(value).split(",")]
                slots = [s.strip() for s in slots if s.strip()]
                if self.event is None:
                    raise MissingDataError(
                        ["event.date (--event-date): gli orari senza data non bastano)"]
                    )
                self.event.slots = slots
            elif key == "property" and value:
                # accetta sia "Via F. Petrarca 36" sia "Via F. Petrarca 36, Palermo"
                address, _, city = str(value).partition(",")
                self.name = address.strip()
                if not self.address:
                    self.address = self.name
                if city.strip():
                    self.city = city.strip()
            else:
                setattr(self, key, value)
        return self

    # ------------------------------------------------------------ validazione ---
    def validate(self, *, require_event: bool = False) -> "PropertyBrief":
        missing: list[str] = []
        if not self.address:
            missing.append("property.address — indirizzo dell'immobile")
        if not self.city:
            missing.append("property.city — comune dell'immobile")
        if not self.old_price:
            missing.append("price.old (--old-price) — prezzo precedente dalla scheda ufficiale")
        if not self.new_price:
            missing.append("price.new (--new-price) — nuovo prezzo ribassato")
        if require_event and self.event is None:
            missing.append("event.date (--event-date) — data dell'Innova Experience")
        if self.event is not None and not self.event.slots:
            missing.append("event.slots (--event-slots) — orari dell'Innova Experience")
        if missing:
            raise MissingDataError(missing)

        if self.new_price >= self.old_price:
            raise ValueError(
                f"Il nuovo prezzo ({fmt.euro(self.new_price)}) deve essere inferiore al "
                f"precedente ({fmt.euro(self.old_price)}): il kit racconta un ribasso."
            )
        return self

    def summary(self) -> str:
        lines = [
            f"Immobile      : {self.title} ({self.city})",
            f"Prezzo        : {fmt.euro(self.old_price)} -> {fmt.euro(self.new_price)}"
            f"  (risparmio {fmt.euro(self.saving)})",
        ]
        if self.price_per_sqm:
            lines.append(f"Prezzo al mq  : {fmt.euro(self.price_per_sqm)}/mq su {self.surface_sqm:g} mq")
        if self.event:
            lines.append(
                f"Evento        : {self.event.label} — {self.event.date_long}, {self.event.slots_text}"
            )
        else:
            lines.append("Evento        : nessuno (materiali senza annuncio evento)")
        return "\n".join(lines)


def _as_price(value: Any) -> int:
    if value in (None, "", 0):
        return 0
    if isinstance(value, str):
        value = value.replace(".", "").replace(",", ".").replace("€", "").strip()
    return int(round(float(value)))


def _as_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, str):
        value = value.replace(",", ".").strip()
    return float(value)
