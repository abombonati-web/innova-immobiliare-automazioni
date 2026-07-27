"""Conversione della landing page in PDF stampabile (wkhtmltopdf).

Prima della conversione la pagina va adattata, perche wkhtmltopdf non ha rete e
non esegue nulla di interattivo:

1. l'`<iframe>` della mappa non renderizza -> diventa un link testuale;
2. le animazioni `.reveal` restano invisibili senza JS -> forzate a `opacity:1`;
3. `fonts.googleapis.com` non e raggiungibile -> Poppins incorporato in base64;
4. il player audio non e riproducibile -> sostituito da una nota.
"""

from __future__ import annotations

import logging
import re
import shutil
import subprocess
from pathlib import Path

from .assets import font_base64
from .brand import FONT_WEIGHTS

log = logging.getLogger(__name__)

PRINT_WEIGHTS = (300, 400, 500, 600, 700, 800)

PRINT_CSS = """
/* --- adattamenti per la stampa/PDF ------------------------------------ */
.reveal{opacity:1 !important;transform:none !important;transition:none !important}
*{transition:none !important;animation:none !important}
html{scroll-behavior:auto}
body{background:var(--cream)}
section{padding:52px 0;page-break-inside:avoid}
.hero .container{padding-top:56px;padding-bottom:56px}
.card,.details-table,.gallery figure{page-break-inside:avoid}
.audio-note{margin-top:30px;display:inline-block;border:1px dashed rgba(232,152,42,.6);
  border-radius:14px;padding:14px 22px;font-size:.86rem;color:#EDE6DA;font-weight:300}
.audio-note strong{color:#E8982A;font-weight:600}
a{text-decoration:none}

/* Il WebKit di wkhtmltopdf non conosce CSS Grid ne aspect-ratio/object-fit:
   ogni griglia viene ricostruita con inline-block e larghezze percentuali. */
.facts-grid{display:block;text-align:center;font-size:0}
.fact{display:inline-block;width:15.6%;vertical-align:top;margin:0 .5%;font-size:1rem}
.cards{display:block;font-size:0}
.card{display:inline-block;width:47.5%;vertical-align:top;margin:0 1% 20px;font-size:1rem}
.gallery{display:block;font-size:0}
.gallery figure{display:inline-block;width:48%;margin:0 1% 14px;font-size:1rem;
  height:auto;aspect-ratio:auto}
.gallery img{height:auto}
.details-grid{display:block;font-size:0}
.details-table{display:inline-table;width:58%;vertical-align:top;font-size:1rem}
.details-photo{display:inline-block;width:38%;margin-left:2%;vertical-align:top;font-size:1rem}
.details-photo img{height:auto;aspect-ratio:auto}
.zone-grid{display:block;font-size:0}
.zone-grid > *{display:inline-block;width:48%;vertical-align:top;margin:0 1%;font-size:1rem}
.zone-map{min-height:0}
"""


def font_face_css(weights: tuple[int, ...] = PRINT_WEIGHTS) -> str:
    """`@font-face` con i TTF Poppins incorporati: nessuna richiesta di rete."""
    blocks = []
    for weight in weights:
        if weight not in FONT_WEIGHTS:
            continue
        blocks.append(
            "@font-face{font-family:'Poppins';font-style:normal;"
            f"font-weight:{weight};"
            f"src:url(data:font/truetype;charset=utf-8;base64,{font_base64(weight)}) format('truetype');"
            "}"
        )
    return "\n".join(blocks)


def prepare_for_print(html_text: str, *, maps_url: str = "", address: str = "") -> str:
    """Applica alla pagina i quattro adattamenti necessari al PDF."""
    # 1. mappa: l'iframe sparisce, resta il link
    link = maps_url or "https://www.google.com/maps"
    replacement = (
        "<div class='zone-map' style='min-height:0;box-shadow:none'>"
        f"<p class='section-lead'><strong>{address}</strong><br>"
        f"<a class='map-link' href='{link}'>Apri su Google Maps &rarr;</a></p></div>"
    )
    html_text = re.sub(
        r"<div class='zone-map[^>]*>.*?</div>", replacement, html_text, flags=re.DOTALL
    )
    html_text = re.sub(r"<iframe\b.*?</iframe>", "", html_text, flags=re.DOTALL)

    # 2. player audio: non riproducibile su carta
    html_text = re.sub(
        r"<div class='audio-player'>.*?</div>\s*</div>\s*<span class='time'.*?</audio>\s*</div>",
        "<div class='audio-note'>&#9834; La <strong>presentazione vocale</strong> "
        "dell'immobile e disponibile nella versione online di questa pagina.</div>",
        html_text,
        flags=re.DOTALL,
    )
    # eventuali residui del tag audio con l'MP3 in base64 (inutile e pesantissimo su carta)
    html_text = re.sub(r"<audio\b.*?</audio>", "", html_text, flags=re.DOTALL)

    # 3. font: via i link a Google Fonts, dentro gli @font-face base64
    html_text = re.sub(
        r"<link[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>\s*", "", html_text
    )
    html_text = html_text.replace("</style>", f"{PRINT_CSS}\n</style>", 1)
    html_text = html_text.replace("<style>", f"<style>\n{font_face_css()}\n", 1)

    # 4. niente JS in un documento statico
    html_text = re.sub(r"<script\b.*?</script>", "", html_text, flags=re.DOTALL)
    return html_text


def ensure_wkhtmltopdf() -> str:
    path = shutil.which("wkhtmltopdf")
    if path is None:
        raise RuntimeError(
            "wkhtmltopdf non trovato nel PATH: serve per la versione stampabile "
            "(`apt-get install wkhtmltopdf`)."
        )
    return path


def html_to_pdf(
    html_path: str | Path,
    pdf_path: str | Path | None = None,
    *,
    maps_url: str = "",
    address: str = "",
    keep_print_html: bool = False,
) -> Path:
    """Converte una landing page in PDF A4 senza margini, applicando i fix di stampa."""
    ensure_wkhtmltopdf()
    html_path = Path(html_path)
    pdf_path = Path(pdf_path) if pdf_path else html_path.with_suffix(".pdf")

    print_html = html_path.with_name(html_path.stem + "-print.html")
    print_html.write_text(
        prepare_for_print(html_path.read_text(encoding="utf-8"), maps_url=maps_url, address=address),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            "wkhtmltopdf",
            "--enable-local-file-access",
            "--page-size", "A4",
            "--margin-top", "0", "--margin-bottom", "0",
            "--margin-left", "0", "--margin-right", "0",
            "--disable-smart-shrinking",
            "--quiet",
            str(print_html),
            str(pdf_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(f"wkhtmltopdf fallito:\n{result.stderr[-3000:]}")

    if not keep_print_html:
        print_html.unlink(missing_ok=True)
    log.info("PDF: %s (%.1f MB)", pdf_path.name, pdf_path.stat().st_size / 1e6)
    return pdf_path
