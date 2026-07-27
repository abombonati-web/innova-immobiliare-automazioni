"""Identita di brand Innova Immobiliare.

Questi valori sono vincolanti: palette, font, payoff e dati agenzia non vanno
sovrascritti dai singoli brief immobile.
"""

from __future__ import annotations

from dataclasses import dataclass

# ---------------------------------------------------------------- palette ---
AMBER = "#E8982A"
AMBER_DEEP = "#C97E15"
CHARCOAL = "#4A4A4A"
CHARCOAL_DEEP = "#2B2A28"
CREAM = "#FBF6EE"
WHITE = "#FFFFFF"

# tinte di servizio derivate, usate nei template (testi secondari su fondo scuro)
SAND = "#D8D0C2"
SAND_DIM = "#BFB7AA"
FOOTER_BG = "#1F1E1C"

PALETTE = {
    "amber": AMBER,
    "amber_deep": AMBER_DEEP,
    "charcoal": CHARCOAL,
    "charcoal_deep": CHARCOAL_DEEP,
    "cream": CREAM,
    "white": WHITE,
    "sand": SAND,
    "sand_dim": SAND_DIM,
    "footer_bg": FOOTER_BG,
}

PAYOFF = "Progetta il tuo futuro"

# ------------------------------------------------------------------ font ---
FONT_FAMILY = "Poppins"
# pesi usati dal kit -> nome file nel repo google/fonts (ofl/poppins)
FONT_WEIGHTS = {
    300: "Poppins-Light",
    400: "Poppins-Regular",
    500: "Poppins-Medium",
    600: "Poppins-SemiBold",
    700: "Poppins-Bold",
    800: "Poppins-ExtraBold",
}
FONT_BASE_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins"


# --------------------------------------------------------------- agenzia ---
@dataclass(frozen=True)
class Agency:
    name: str = "Innova Immobiliare"
    legal_name: str = "Innova Immobiliare S.r.l."
    address: str = "Via Enzo ed Elvira Sellerio 44/46, Palermo"
    phone: str = "+39 339 418 5631"
    email: str = "info@innovaimmobiliare.it"
    website: str = "innovaimmobiliare.it"

    @property
    def phone_tel(self) -> str:
        """Numero in formato `tel:` (senza spazi)."""
        return "+" + "".join(c for c in self.phone if c.isdigit())


AGENCY = Agency()


# ------------------------------------------------------------ tono di voce ---
# Parametri Piper/sherpa-onnx per i due registri usati dal kit.
#
#   noise_scale    piu basso = dizione netta/professionale, piu alto = piu umano
#   noise_scale_w  variabilita ritmica: piu alto = cadenza meno robotica
#   speed          <1 rallenta, >1 velocizza
VOICE_TONES = {
    # video social: hook emotivo, caldo, entusiasta
    "euforico": {"speed": 0.90, "noise_scale": 0.80, "noise_scale_w": 0.95},
    # landing page: riepilogo istituzionale, netto e conciso
    "professionale": {"speed": 1.00, "noise_scale": 0.55, "noise_scale_w": 0.70},
}

# Voce femminile italiana Piper, mirror GitHub dei modelli sherpa-onnx
# (HuggingFace non e raggiungibile dai sandbox con whitelist ristretta).
VOICE_MODEL_NAME = "vits-piper-it_IT-paola-medium"
VOICE_MODEL_URL = (
    "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/"
    f"{VOICE_MODEL_NAME}.tar.bz2"
)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    """`#E8982A` -> `(232, 152, 42)`."""
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
