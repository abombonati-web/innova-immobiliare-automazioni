"""Slide verticali brandizzate 1080x1920 generate con Pillow.

Tutte le slide condividono lo stesso impianto: fondo antracite profonda con
alone ambra, wordmark in alto, contenuto al centro, payoff e recapito in basso.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import fmt
from .assets import font_path
from .brand import (
    AGENCY,
    AMBER,
    CHARCOAL_DEEP,
    CREAM,
    PAYOFF,
    SAND,
    SAND_DIM,
    WHITE,
    hex_to_rgb,
)
from .model import PropertyBrief

log = logging.getLogger(__name__)

WIDTH, HEIGHT = 1080, 1920
MARGIN = 96

_FONT_CACHE: dict[tuple[int, int], ImageFont.FreeTypeFont] = {}


def font(weight: int, size: int) -> ImageFont.FreeTypeFont:
    key = (weight, size)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(str(font_path(weight)), size)
    return _FONT_CACHE[key]


# ------------------------------------------------------------------ canvas ---
def new_canvas(*, glow: bool = True) -> Image.Image:
    """Fondo antracite profonda con alone ambra in alto a destra."""
    image = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(CHARCOAL_DEEP))
    if glow:
        _add_glow(image, center=(WIDTH + 60, -60), radius=760, color=AMBER, alpha=0.30)
        _add_glow(image, center=(-120, HEIGHT + 120), radius=620, color=AMBER, alpha=0.16)
    return image


def _add_glow(
    image: Image.Image,
    *,
    center: tuple[int, int],
    radius: int,
    color: str,
    alpha: float,
) -> None:
    layer = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(layer)
    cx, cy = center
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=int(255 * alpha),
    )
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.42))
    image.paste(Image.new("RGB", image.size, hex_to_rgb(color)), (0, 0), layer)


def fit_font(
    text: str,
    weight: int,
    *,
    max_size: int,
    min_size: int = 40,
    max_width: int = WIDTH - 2 * MARGIN,
) -> ImageFont.FreeTypeFont:
    """Il peso piu grande che fa stare `text` su una sola riga."""
    size = max_size
    while size > min_size and font(weight, size).getlength(text) > max_width:
        size -= 4
    return font(weight, size)


def wrap(text: str, font_obj: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if font_obj.getlength(candidate) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def text_block(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    font_obj: ImageFont.FreeTypeFont,
    fill: str,
    top: int,
    max_width: int = WIDTH - 2 * MARGIN,
    line_height: float = 1.22,
    center: bool = True,
    letter_spacing: int = 0,
) -> int:
    """Disegna un blocco di testo e restituisce la `y` subito sotto."""
    step = int(font_obj.size * line_height)
    y = top
    for line in wrap(text, font_obj, max_width):
        if letter_spacing:
            _draw_spaced(draw, line, font_obj, fill, y, letter_spacing, center)
        else:
            x = (WIDTH - font_obj.getlength(line)) / 2 if center else MARGIN
            draw.text((x, y), line, font=font_obj, fill=fill)
        y += step
    return y


def _draw_spaced(
    draw: ImageDraw.ImageDraw,
    line: str,
    font_obj: ImageFont.FreeTypeFont,
    fill: str,
    y: int,
    spacing: int,
    center: bool,
) -> None:
    width = sum(font_obj.getlength(c) + spacing for c in line) - spacing
    x = (WIDTH - width) / 2 if center else MARGIN
    for char in line:
        draw.text((x, y), char, font=font_obj, fill=fill)
        x += font_obj.getlength(char) + spacing


def pill(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    top: int,
    font_obj: ImageFont.FreeTypeFont,
    fg: str,
    border: str | None = None,
    bg: str | None = None,
    padding: tuple[int, int] = (34, 18),
    letter_spacing: int = 4,
) -> int:
    px, py = padding
    width = sum(font_obj.getlength(c) + letter_spacing for c in text) - letter_spacing
    box_w = width + px * 2
    box_h = font_obj.size + py * 2
    x0 = (WIDTH - box_w) / 2
    draw.rounded_rectangle(
        [x0, top, x0 + box_w, top + box_h],
        radius=box_h / 2,
        fill=hex_to_rgb(bg) if bg else None,
        outline=hex_to_rgb(border) if border else None,
        width=3,
    )
    x = x0 + px
    for char in text:
        draw.text((x, top + py - font_obj.size * 0.10), char, font=font_obj, fill=fg)
        x += font_obj.getlength(char) + letter_spacing
    return int(top + box_h)


def wordmark(draw: ImageDraw.ImageDraw, top: int = 108) -> int:
    """`INNOVA IMMOBILIARE` — wordmark testuale, coerente col footer web."""
    innova = font(800, 46)
    immobiliare = font(500, 46)
    gap = 16
    w1 = innova.getlength("Innova")
    w2 = sum(immobiliare.getlength(c) + 3 for c in "Immobiliare") - 3
    x = (WIDTH - (w1 + gap + w2)) / 2
    draw.text((x, top), "Innova", font=innova, fill=CREAM)
    x += w1 + gap
    for char in "Immobiliare":
        draw.text((x, top), char, font=immobiliare, fill=AMBER)
        x += immobiliare.getlength(char) + 3
    return top + 46


def footer(draw: ImageDraw.ImageDraw, *, phone: str | None = None) -> None:
    payoff = font(500, 36)
    line = f"{PAYOFF}."
    draw.text(((WIDTH - payoff.getlength(line)) / 2, HEIGHT - 214), line, font=payoff, fill=AMBER)
    small = font(300, 32)
    contact = phone or AGENCY.phone
    draw.text(
        ((WIDTH - small.getlength(contact)) / 2, HEIGHT - 156),
        contact,
        font=small,
        fill=SAND_DIM,
    )


def strike(draw: ImageDraw.ImageDraw, *, y: int, width: float, color: str, thickness: int = 8) -> None:
    x0 = (WIDTH - width) / 2
    draw.line([x0, y, x0 + width, y], fill=hex_to_rgb(color), width=thickness)


# ------------------------------------------------------------------ slides ---
@dataclass
class SlideSet:
    price_old: Path
    price_new: Path
    event: Path | None
    cta: Path


def build_price_slides(brief: PropertyBrief, out_dir: Path) -> tuple[Path, Path]:
    """Slide 'prezzo precedente' (barrato) e 'nuovo prezzo' (reveal)."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- prezzo precedente -------------------------------------------------
    old = new_canvas()
    draw = ImageDraw.Draw(old)
    wordmark(draw)
    y = pill(
        draw,
        brief.full_address.upper(),
        top=250,
        font_obj=font(600, 30),
        fg=AMBER,
        border=AMBER,
    )
    y = text_block(
        draw,
        "Fino a ieri",
        font_obj=font(300, 62),
        fill=SAND,
        top=int(HEIGHT * 0.36),
    )
    value = fmt.euro(brief.old_price)
    value_font = fit_font(value, 800, max_size=150, min_size=90)
    y = text_block(draw, value, font_obj=value_font, fill=WHITE, top=y + 40)
    strike(draw, y=int(y - value_font.size * 0.62), width=value_font.getlength(value) + 40, color=AMBER)
    footer(draw, phone=brief.phone)
    old_path = out_dir / "slide-01-prezzo-precedente.png"
    old.save(old_path)

    # --- nuovo prezzo ------------------------------------------------------
    new = new_canvas()
    draw = ImageDraw.Draw(new)
    wordmark(draw)
    pill(
        draw,
        "NUOVO PREZZO",
        top=250,
        font_obj=font(700, 30),
        fg=CHARCOAL_DEEP,
        bg=AMBER,
    )
    y = text_block(
        draw,
        "Da oggi",
        font_obj=font(300, 62),
        fill=SAND,
        top=int(HEIGHT * 0.33),
    )
    y = text_block(draw, fmt.euro(brief.new_price), font_obj=font(800, 172), fill=AMBER, top=y + 34)
    y = pill(
        draw,
        f"RISPARMI {fmt.euro(brief.saving)}".upper(),
        top=y + 46,
        font_obj=font(700, 34),
        fg=CREAM,
        border=CREAM,
        letter_spacing=3,
    )
    if brief.price_per_sqm:
        text_block(
            draw,
            f"circa {fmt.euro(brief.price_per_sqm)} al metro quadro",
            font_obj=font(300, 40),
            fill=SAND_DIM,
            top=y + 46,
        )
    footer(draw, phone=brief.phone)
    new_path = out_dir / "slide-02-nuovo-prezzo.png"
    new.save(new_path)

    log.info("slide prezzo generate: %s, %s", old_path.name, new_path.name)
    return old_path, new_path


def build_event_slide(brief: PropertyBrief, out_dir: Path) -> Path | None:
    """Slide dell'Innova Experience (data + fasce orarie)."""
    if brief.event is None:
        return None
    out_dir.mkdir(parents=True, exist_ok=True)

    image = new_canvas()
    draw = ImageDraw.Draw(image)
    wordmark(draw)
    pill(
        draw,
        brief.event.label.upper(),
        top=250,
        font_obj=font(700, 30),
        fg=CHARCOAL_DEEP,
        bg=AMBER,
    )
    y = text_block(
        draw,
        "Vieni a visitarla",
        font_obj=font(300, 62),
        fill=SAND,
        top=int(HEIGHT * 0.30),
    )
    date_label = brief.event.date_long.capitalize()
    y = text_block(
        draw,
        date_label,
        font_obj=fit_font(date_label, 700, max_size=96, min_size=58),
        fill=CREAM,
        top=y + 30,
    )

    # fasce orarie affiancate
    slot_font = font(800, 86)
    label_font = font(500, 30)
    slots = brief.event.slots[:3]
    if slots:
        box_w, box_h, gap = 380, 210, 40
        total = len(slots) * box_w + (len(slots) - 1) * gap
        x = (WIDTH - total) / 2
        top = y + 70
        for slot in slots:
            draw.rounded_rectangle(
                [x, top, x + box_w, top + box_h], radius=28, outline=hex_to_rgb(AMBER), width=4
            )
            draw.text(
                (x + (box_w - label_font.getlength("ORE")) / 2, top + 30),
                "ORE",
                font=label_font,
                fill=AMBER,
            )
            draw.text(
                (x + (box_w - slot_font.getlength(slot)) / 2, top + 78),
                slot,
                font=slot_font,
                fill=CREAM,
            )
            x += box_w + gap
        y = top + box_h

    text_block(
        draw,
        brief.event.note or brief.full_address,
        font_obj=font(300, 40),
        fill=SAND_DIM,
        top=int(y + 70),
    )
    footer(draw, phone=brief.phone)

    path = out_dir / "slide-03-evento.png"
    image.save(path)
    log.info("slide evento generata: %s", path.name)
    return path


def build_cta_slide(brief: PropertyBrief, out_dir: Path) -> Path:
    """Slide finale: invito a chiamare / prenotare."""
    out_dir.mkdir(parents=True, exist_ok=True)
    image = new_canvas()
    draw = ImageDraw.Draw(image)
    wordmark(draw)

    headline = "Prenota la tua visita" if brief.event else "Prenota un appuntamento"
    y = text_block(
        draw,
        headline,
        font_obj=fit_font(headline, 700, max_size=92, min_size=62),
        fill=CREAM,
        top=int(HEIGHT * 0.30),
    )

    if brief.event:
        y = text_block(
            draw,
            f"Posti limitati — {brief.event.date_long}",
            font_obj=font(300, 44),
            fill=SAND,
            top=y + 26,
        )

    # bottone ambra col numero di telefono
    label = brief.phone
    button_font = fit_font(label, 800, max_size=76, min_size=48, max_width=WIDTH - 2 * MARGIN - 120)
    box_w = button_font.getlength(label) + 120
    box_h = 156
    x0 = (WIDTH - box_w) / 2
    top = y + 70
    draw.rounded_rectangle([x0, top, x0 + box_w, top + box_h], radius=box_h / 2, fill=hex_to_rgb(AMBER))
    draw.text(
        (x0 + 60, top + (box_h - button_font.size) / 2 - 8),
        label,
        font=button_font,
        fill=CHARCOAL_DEEP,
    )

    text_block(
        draw,
        AGENCY.address,
        font_obj=font(300, 38),
        fill=SAND_DIM,
        top=int(top + box_h + 60),
    )
    footer(draw, phone=AGENCY.email)

    path = out_dir / "slide-04-cta.png"
    image.save(path)
    log.info("slide CTA generata: %s", path.name)
    return path


def build_caption_overlay(text: str, out_path: Path, *, eyebrow: str = "") -> Path:
    """Didascalia trasparente da sovrapporre alle foto (banda sfumata in basso)."""
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    band_h = 520
    band = Image.new("RGBA", (WIDTH, band_h), (0, 0, 0, 0))
    band_draw = ImageDraw.Draw(band)
    r, g, b = hex_to_rgb(CHARCOAL_DEEP)
    for row in range(band_h):
        alpha = int(232 * (row / band_h) ** 1.35)
        band_draw.line([0, row, WIDTH, row], fill=(r, g, b, alpha))
    overlay.alpha_composite(band, (0, HEIGHT - band_h))

    draw = ImageDraw.Draw(overlay)
    y = HEIGHT - 300
    if eyebrow:
        eyebrow_font = font(600, 30)
        width = sum(eyebrow_font.getlength(c) + 5 for c in eyebrow) - 5
        x = (WIDTH - width) / 2
        for char in eyebrow:
            draw.text((x, y), char, font=eyebrow_font, fill=AMBER)
            x += eyebrow_font.getlength(char) + 5
        y += 58
    text_block(draw, text, font_obj=font(600, 56), fill=CREAM, top=y, max_width=WIDTH - 160)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    overlay.save(out_path)
    return out_path


def build_all_slides(brief: PropertyBrief, out_dir: Path) -> SlideSet:
    old, new = build_price_slides(brief, out_dir)
    return SlideSet(
        price_old=old,
        price_new=new,
        event=build_event_slide(brief, out_dir),
        cta=build_cta_slide(brief, out_dir),
    )
