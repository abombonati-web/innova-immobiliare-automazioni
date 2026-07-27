"""Download e cache degli asset esterni (font Poppins, voce Piper).

Tutte le sorgenti sono su domini raggiungibili anche dai sandbox con whitelist
ristretta (`github.com`, `release-assets.githubusercontent.com`,
`raw.githubusercontent.com`). HuggingFace **non** e raggiungibile: se serve una
voce nuova va cercato un mirror su GitHub Releases.
"""

from __future__ import annotations

import logging
import os
import shutil
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

from .brand import FONT_BASE_URL, FONT_WEIGHTS, VOICE_MODEL_NAME, VOICE_MODEL_URL

log = logging.getLogger(__name__)

_UA = {"User-Agent": "innova-property-kit/1.0"}


def cache_dir() -> Path:
    """Directory di cache degli asset (override con `INNOVA_KIT_CACHE`)."""
    root = os.environ.get("INNOVA_KIT_CACHE")
    path = Path(root) if root else Path.home() / ".cache" / "innova-property-kit"
    path.mkdir(parents=True, exist_ok=True)
    return path


def download(url: str, dest: Path, *, retries: int = 4) -> Path:
    """Scarica `url` in `dest` con backoff esponenziale (2s, 4s, 8s, 16s)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return dest

    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            log.info("download %s", url)
            request = urllib.request.Request(url, headers=_UA)
            with urllib.request.urlopen(request, timeout=180) as response:
                tmp = dest.with_suffix(dest.suffix + ".part")
                with tmp.open("wb") as handle:
                    shutil.copyfileobj(response, handle)
                tmp.replace(dest)
            return dest
        except (urllib.error.URLError, TimeoutError, OSError) as exc:  # pragma: no cover - rete
            last = exc
            if attempt == retries:
                break
            delay = 2 ** (attempt + 1)
            log.warning("download fallito (%s), riprovo tra %ss", exc, delay)
            time.sleep(delay)
    raise RuntimeError(f"Impossibile scaricare {url}: {last}")


# ------------------------------------------------------------------- font ---
def font_path(weight: int = 400) -> Path:
    """Percorso locale del TTF Poppins per il peso richiesto (lo scarica se serve)."""
    weight = min(FONT_WEIGHTS, key=lambda w: abs(w - weight))
    name = FONT_WEIGHTS[weight]
    local = _local_font_override(name)
    if local:
        return local
    dest = cache_dir() / "fonts" / f"{name}.ttf"
    return download(f"{FONT_BASE_URL}/{name}.ttf", dest)


def _local_font_override(name: str) -> Path | None:
    """Permette di usare font gia presenti su disco (`INNOVA_KIT_FONT_DIR`)."""
    root = os.environ.get("INNOVA_KIT_FONT_DIR")
    if not root:
        return None
    candidate = Path(root) / f"{name}.ttf"
    return candidate if candidate.exists() else None


def font_base64(weight: int = 400) -> str:
    """TTF Poppins in base64, per gli `@font-face` incorporati nel PDF."""
    import base64

    return base64.b64encode(font_path(weight).read_bytes()).decode("ascii")


# ------------------------------------------------------------------- voce ---
def voice_model_dir() -> Path:
    """Directory del modello Piper italiano (scaricato ed estratto se assente).

    Override con `INNOVA_KIT_VOICE_DIR` per ambienti completamente offline.
    """
    override = os.environ.get("INNOVA_KIT_VOICE_DIR")
    if override:
        path = Path(override)
        if not (path / "tokens.txt").exists():
            raise FileNotFoundError(
                f"INNOVA_KIT_VOICE_DIR={path} non contiene un modello Piper valido "
                "(manca tokens.txt)."
            )
        return path

    target = cache_dir() / "voices" / VOICE_MODEL_NAME
    if (target / "tokens.txt").exists():
        return target

    archive = cache_dir() / "voices" / f"{VOICE_MODEL_NAME}.tar.bz2"
    download(VOICE_MODEL_URL, archive)

    with tempfile.TemporaryDirectory(dir=str(archive.parent)) as tmpdir:
        with tarfile.open(archive, "r:bz2") as tar:
            _safe_extract(tar, Path(tmpdir))
        extracted = Path(tmpdir) / VOICE_MODEL_NAME
        if not extracted.exists():  # archivio senza cartella radice attesa
            candidates = [p for p in Path(tmpdir).iterdir() if p.is_dir()]
            if len(candidates) != 1:
                raise RuntimeError(f"Struttura inattesa nell'archivio voce: {candidates}")
            extracted = candidates[0]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(extracted), str(target))
    return target


def _safe_extract(tar: tarfile.TarFile, dest: Path) -> None:
    """Estrazione con controllo path traversal (equivalente a `filter='data'`)."""
    dest = dest.resolve()
    for member in tar.getmembers():
        member_path = (dest / member.name).resolve()
        if not str(member_path).startswith(str(dest)):
            raise RuntimeError(f"Percorso non sicuro nell'archivio: {member.name}")
    tar.extractall(dest)  # noqa: S202 - path verificati sopra
