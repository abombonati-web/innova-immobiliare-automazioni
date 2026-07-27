"""Landing page autonoma: un unico file HTML, senza dipendenze esterne.

Foto e audio sono incorporati in base64, quindi la pagina si apre e si condivide
anche senza hosting. Le sezioni prive di dati nel brief non vengono stampate:
il kit non riempie i buchi con testo inventato.
"""

from __future__ import annotations

import base64
import html
import logging
import re
from io import BytesIO
from pathlib import Path

from PIL import Image

from . import fmt
from .brand import AGENCY, PAYOFF
from .model import PropertyBrief

log = logging.getLogger(__name__)

TEMPLATE_PATH = Path(__file__).parent / "templates" / "landing.html"
FORM_ENDPOINT = "https://formsubmit.co/ajax/{email}"

GOOGLE_FONTS_HEAD = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800'
    '&display=swap" rel="stylesheet">'
)


def render(template: str, values: dict[str, str]) -> str:
    """Sostituzione dei segnaposto `{{CHIAVE}}`; le chiavi mancanti diventano vuote."""
    def replace(match: re.Match) -> str:
        return values.get(match.group(1), "")

    return re.sub(r"\{\{([A-Z0-9_]+)\}\}", replace, template)


# ------------------------------------------------------------------ media ---
def image_data_uri(path: Path, *, max_width: int = 1600, quality: int = 78) -> str:
    """JPEG ridimensionato e incorporato in base64 (le foto originali sono enormi)."""
    with Image.open(path) as image:
        image = image.convert("RGB")
        if image.width > max_width:
            height = round(image.height * max_width / image.width)
            image = image.resize((max_width, height), Image.LANCZOS)
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=quality, optimize=True, progressive=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def audio_data_uri(path: Path) -> str:
    encoded = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    return f"data:audio/mpeg;base64,{encoded}"


def _img(path: Path, alt: str, *, max_width: int = 1600, quality: int = 78, extra: str = "") -> str:
    return (
        f'<img src="{image_data_uri(path, max_width=max_width, quality=quality)}" '
        f'alt="{html.escape(alt)}"{extra}>'
    )


# --------------------------------------------------------------- sezioni ---
def _facts_section(brief: PropertyBrief) -> str:
    if not brief.facts:
        return ""
    items = "".join(
        f'<div class="fact">'
        f'<div class="icon">{html.escape(f.icon or "•")}</div>'
        f'<div class="value">{html.escape(f.value)}</div>'
        f'<div class="label">{html.escape(f.label)}</div>'
        f"</div>"
        for f in brief.facts
    )
    return f'<div class="facts"><div class="container facts-grid">{items}</div></div>'


def _highlights_section(brief: PropertyBrief) -> str:
    if not brief.highlights:
        return ""
    cards = "".join(
        f'<div class="card reveal">'
        f'<div class="icon">{html.escape(card.icon or "—")}</div>'
        f"<h3>{html.escape(card.title)}</h3>"
        f"<p>{html.escape(card.text)}</p>"
        f"</div>"
        for card in brief.highlights
    )
    return (
        "<section><div class='container'>"
        "<h2 class='section-title reveal'>Perché è un'occasione.<br>"
        "<span class='accent'>In modo verificabile.</span></h2>"
        f"<div class='cards'>{cards}</div>"
        "</div></section>"
    )


def _gallery_section(brief: PropertyBrief, photos: list[Path]) -> str:
    if not photos:
        return ""
    captions = brief.photo_captions or []
    figures = []
    for index, photo in enumerate(photos):
        caption = captions[index] if index < len(captions) else ""
        caption_html = f"<figcaption>{html.escape(caption)}</figcaption>" if caption else ""
        image = _img(photo, caption or brief.full_address, extra=' loading="lazy"')
        figures.append(f"<figure>{image}{caption_html}</figure>")
    lead = brief.description[1] if len(brief.description) > 1 else ""
    lead_html = f"<p class='section-lead reveal'>{html.escape(lead)}</p>" if lead else ""
    return (
        "<section class='gallery-section'><div class='container'>"
        "<h2 class='section-title reveal'>Gli spazi.<br>"
        f"<span class='accent'>{html.escape(brief.full_address)}.</span></h2>"
        f"{lead_html}"
        f"<div class='gallery reveal'>{''.join(figures)}</div>"
        "</div></section>"
    )


def _details_section(brief: PropertyBrief, photos: list[Path]) -> str:
    if not brief.details:
        return ""
    rows = "".join(
        f"<tr><th>{html.escape(d.label)}</th><td>{html.escape(d.value)}</td></tr>"
        for d in brief.details
    )
    photo_html = ""
    if len(photos) > 1:
        photo_html = f"<div class='details-photo reveal'>{_img(photos[1], brief.full_address, max_width=1000)}</div>"
    return (
        "<section><div class='container'>"
        "<h2 class='section-title reveal'>I dettagli tecnici.<br>"
        "<span class='accent'>Senza sorprese.</span></h2>"
        "<div class='details-grid'>"
        f"<table class='details-table reveal'><tbody>{rows}</tbody></table>"
        f"{photo_html}"
        "</div></div></section>"
    )


def _targets_section(brief: PropertyBrief) -> str:
    if not brief.targets:
        return ""
    cards = "".join(
        f"<div class='card reveal'><h3>{html.escape(card.title)}</h3>"
        f"<p>{html.escape(card.text)}</p></div>"
        for card in brief.targets
    )
    return (
        "<section class='targets'><div class='container'>"
        "<h2 class='section-title reveal'>Per chi è perfetta.<br>"
        "<span class='accent'>Detto chiaramente.</span></h2>"
        f"<div class='cards'>{cards}</div>"
        "</div></section>"
    )


def _zone_section(brief: PropertyBrief, *, static_map: bool = False) -> str:
    if not brief.zone_intro and not brief.zone_advantages:
        return ""
    advantages = (
        "<ul class='zone-list reveal'>"
        + "".join(f"<li>{html.escape(a)}</li>" for a in brief.zone_advantages)
        + "</ul>"
        if brief.zone_advantages
        else ""
    )
    if static_map:
        # nel PDF l'iframe non renderizza: si sostituisce con un link testuale
        map_html = (
            f"<p class='section-lead'><strong>{html.escape(brief.full_address)}</strong><br>"
            f"<a class='map-link' href='{brief.maps_url}'>Apri su Google Maps →</a></p>"
        )
    else:
        map_html = (
            f"<div class='zone-map reveal'><iframe src='{brief.maps_embed_url}' loading='lazy' "
            f"title='Mappa — {html.escape(brief.full_address)}' "
            "referrerpolicy='no-referrer-when-downgrade'></iframe></div>"
        )
    intro = f"<p class='section-lead reveal'>{html.escape(brief.zone_intro)}</p>" if brief.zone_intro else ""
    return (
        "<section class='gallery-section'><div class='container'>"
        "<h2 class='section-title reveal'>La zona.<br><span class='accent'>Dove si trova.</span></h2>"
        f"{intro}"
        f"<div class='zone-grid'>{map_html}<div>{advantages}"
        f"<a class='map-link' href='{brief.maps_url}' target='_blank' rel='noopener'>"
        "Apri su Google Maps →</a></div></div>"
        "</div></section>"
    )


def _event_bar(brief: PropertyBrief) -> str:
    if brief.event is None:
        return ""
    return (
        "<div class='event-bar'><div class='container event-inner'>"
        f"<span class='label'>{html.escape(brief.event.label)}</span>"
        f"<span class='when'>{html.escape(brief.event.date_long.capitalize())}</span>"
        f"<span class='slots'>{html.escape(brief.event.slots_text)} · su prenotazione</span>"
        "</div></div>"
    )


def _audio_player(audio_uri: str | None) -> str:
    if not audio_uri:
        return ""
    return (
        "<div class='audio-player'>"
        "<button class='play-btn' id='playBtn' type='button' "
        "aria-label='Ascolta la presentazione dell\\'immobile'>▶</button>"
        "<div class='info'>"
        "<div class='title'>🔊 Ascolta la presentazione dell'immobile</div>"
        "<div class='progress-wrap' id='progressWrap'><div class='progress-bar' id='progressBar'></div></div>"
        "</div>"
        "<span class='time' id='audioTime'>0:00</span>"
        f"<audio id='narrationAudio' preload='none' src='{audio_uri}'></audio>"
        "</div>"
    )


def _slot_field(brief: PropertyBrief) -> str:
    if brief.event is None or not brief.event.slots:
        return ""
    options = "".join(
        f"<option>{html.escape(brief.event.date_long.capitalize())} · ore {html.escape(slot)}</option>"
        for slot in brief.event.slots
    )
    return (
        "<div class='field'><label for='slot'>Fascia di visita preferita</label>"
        "<select id='slot' name='slot'><option value=''>Scegli una fascia</option>"
        f"{options}<option>Nessuna preferenza</option></select></div>"
    )


def _scripts(brief: PropertyBrief, *, with_audio: bool) -> str:
    audio_js = (
        """
/* Player audio brandizzato: play/pause, barra cliccabile, timer mm:ss */
(function(){
  const audio = document.getElementById("narrationAudio");
  const btn   = document.getElementById("playBtn");
  const bar   = document.getElementById("progressBar");
  const wrap  = document.getElementById("progressWrap");
  const time  = document.getElementById("audioTime");
  if(!audio || !btn) return;

  const mmss = s => (isFinite(s) ? Math.floor(s/60) + ":" + String(Math.floor(s%60)).padStart(2,"0") : "0:00");

  btn.addEventListener("click", () => {
    if(audio.paused){ audio.play(); } else { audio.pause(); }
  });
  audio.addEventListener("play",  () => { btn.textContent = "❚❚"; });
  audio.addEventListener("pause", () => { btn.textContent = "▶"; });
  audio.addEventListener("ended", () => { btn.textContent = "▶"; bar.style.width = "0%"; });
  audio.addEventListener("loadedmetadata", () => { time.textContent = mmss(audio.duration); });
  audio.addEventListener("timeupdate", () => {
    if(audio.duration){ bar.style.width = (audio.currentTime/audio.duration*100) + "%"; }
    time.textContent = mmss(audio.duration - audio.currentTime);
  });
  wrap.addEventListener("click", e => {
    const rect = wrap.getBoundingClientRect();
    if(audio.duration){ audio.currentTime = (e.clientX - rect.left)/rect.width * audio.duration; }
  });
})();
"""
        if with_audio
        else ""
    )

    return f"""<script>
/* ============================================================
   INVIO RICHIESTE — FormSubmit verso {AGENCY.email}
   Al primo invio FormSubmit manda una email di conferma:
   cliccare "Activate" una sola volta per attivare la casella.
============================================================ */
const FORM_ENDPOINT = "{FORM_ENDPOINT.format(email=AGENCY.email)}";
{audio_js}
/* Cattura automatica dei parametri UTM dalle Ads */
const params = new URLSearchParams(location.search);
["utm_source","utm_medium","utm_campaign","utm_content"].forEach(k=>{{
  const f = document.getElementById(k);
  if(f && params.get(k)) f.value = params.get(k);
}});

/* Invio form */
document.getElementById("leadForm").addEventListener("submit", async function(e){{
  e.preventDefault();
  const ok = document.getElementById("msgOk"), err = document.getElementById("msgErr");
  ok.classList.remove("show"); err.classList.remove("show");

  const nome = document.getElementById("nome").value.trim();
  const tel  = document.getElementById("telefono").value.trim();
  const mail = document.getElementById("email").value.trim();
  const priv = document.getElementById("privacy").checked;
  if(!nome || !tel || !mail || !priv){{ err.classList.add("show"); return; }}

  const data = Object.fromEntries(new FormData(this).entries());
  if(data._honey){{ return; }} /* spam bot: scarta in silenzio */

  const btn = this.querySelector("button[type=submit]");
  const btnText = btn.textContent;
  btn.disabled = true; btn.textContent = "Invio in corso…";

  try{{
    const r = await fetch(FORM_ENDPOINT, {{
      method:"POST",
      headers:{{ "Content-Type":"application/json", "Accept":"application/json" }},
      body: JSON.stringify(data)
    }});
    if(!r.ok) throw new Error("Invio non riuscito");
    if(typeof fbq === "function") fbq("track", "Lead");
    ok.classList.add("show");
    this.reset();
  }}catch(_){{
    err.textContent = "Si è verificato un problema con l'invio. Riprova oppure chiamaci al {brief.phone}.";
    err.classList.add("show");
  }}finally{{
    btn.disabled = false; btn.textContent = btnText;
  }}
}});

/* Reveal on scroll (disattivato se l'utente preferisce ridurre le animazioni) */
if(matchMedia("(prefers-reduced-motion: no-preference)").matches){{
  const io = new IntersectionObserver(es=>{{
    es.forEach(e=>{{ if(e.isIntersecting){{ e.target.classList.add("in"); io.unobserve(e.target);}} }});
  }},{{threshold:.15}});
  document.querySelectorAll(".reveal").forEach(el=>io.observe(el));
}}else{{
  document.querySelectorAll(".reveal").forEach(el=>el.classList.add("in"));
}}
</script>"""


# ------------------------------------------------------------------ build ---
def build_landing_html(
    brief: PropertyBrief,
    photos: list[Path],
    out_path: str | Path,
    *,
    audio_path: str | Path | None = None,
    font_head: str = GOOGLE_FONTS_HEAD,
    extra_css: str = "",
    static_map: bool = False,
    with_scripts: bool = True,
) -> Path:
    """Genera la landing page standalone e la scrive su disco."""
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    audio_uri = audio_data_uri(Path(audio_path)) if audio_path else None

    headline = brief.headline or (
        f"{html.escape(brief.title)}.<br>Ora a <em>un prezzo nuovo</em>."
    )
    subtitle = brief.description[0] if brief.description else brief.full_address

    price_sqm = (
        f"<span class='price-sqm'>circa {fmt.euro(brief.price_per_sqm)}/mq</span>"
        if brief.price_per_sqm
        else ""
    )

    values = {
        "TITLE": f"{brief.title}, {brief.city} — nuovo prezzo | {AGENCY.name}",
        "META_DESCRIPTION": (
            f"{brief.title}, {brief.city}: prezzo ribassato da {fmt.euro(brief.old_price)} "
            f"a {fmt.euro(brief.new_price)}."
            + (f" {brief.event.label}: {brief.event.date_long}, {brief.event.slots_text}." if brief.event else "")
        ),
        "FONT_HEAD": font_head,
        "EXTRA_CSS": extra_css,
        "HERO_IMAGE": _img(photos[0], brief.full_address, max_width=1800, quality=72) if photos else "",
        "EYEBROW": html.escape(brief.eyebrow or f"Nuovo prezzo · {brief.city}"),
        "HEADLINE": headline,
        "SUBTITLE": html.escape(subtitle),
        "OLD_PRICE": fmt.euro(brief.old_price),
        "NEW_PRICE": fmt.euro(brief.new_price),
        "SAVING": fmt.euro(brief.saving),
        "PRICE_SQM": price_sqm,
        "AUDIO_PLAYER": _audio_player(audio_uri),
        "CTA_LABEL": "Prenota la visita" if brief.event else "Richiedi informazioni",
        "PHONE": html.escape(brief.phone),
        "PHONE_TEL": brief.phone_tel,
        "EVENT_BAR": _event_bar(brief),
        "FACTS": _facts_section(brief),
        "HIGHLIGHTS": _highlights_section(brief),
        "GALLERY": _gallery_section(brief, photos),
        "DETAILS": _details_section(brief, photos),
        "TARGETS": _targets_section(brief),
        "ZONE": _zone_section(brief, static_map=static_map),
        "FORM_TITLE": "Prenota la tua visita." if brief.event else "Richiedi informazioni.",
        "FORM_SUBTITLE": "I posti sono limitati." if brief.event else "Ti richiamiamo noi.",
        "FORM_LEAD": (
            f"Le visite dell'{brief.event.label} si prenotano in anticipo, in piccoli gruppi. "
            "Il team Innova ti contatterà per confermare il tuo posto."
            if brief.event
            else "Lasciaci i tuoi contatti: il team Innova ti risponde entro 24 ore."
        ),
        "FORM_SLOT_FIELD": _slot_field(brief),
        "FORM_SUBJECT": f"Richiesta — {brief.title}, {brief.city}",
        "PROPERTY_TITLE": html.escape(f"{brief.title}, {brief.city}"),
        "AGENCY_LEGAL": AGENCY.legal_name,
        "AGENCY_ADDRESS": AGENCY.address,
        "AGENCY_EMAIL": AGENCY.email,
        "AGENCY_WEBSITE": AGENCY.website,
        "PAYOFF": PAYOFF,
        "SCRIPTS": _scripts(brief, with_audio=bool(audio_uri)) if with_scripts else "",
    }

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render(template, values), encoding="utf-8")
    log.info("landing page: %s (%.1f MB)", out_path.name, out_path.stat().st_size / 1e6)
    return out_path
