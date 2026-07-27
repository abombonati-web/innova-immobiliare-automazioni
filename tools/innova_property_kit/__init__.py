"""Innova Property Kit — reel verticale + landing page da un brief immobile.

Pipeline completa (foto Drive -> video 1080x1920 con voce e musica sintetizzate,
landing HTML autonoma con player audio, PDF stampabile) costruita solo con
strumenti locali/open source: ffmpeg, Pillow, numpy/scipy, Piper via sherpa-onnx,
wkhtmltopdf. Nessun servizio cloud a pagamento.
"""

from __future__ import annotations

__version__ = "1.0.0"

from .model import Event, Fact, MissingDataError, PropertyBrief  # noqa: F401
