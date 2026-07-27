"""Reperimento delle foto dell'immobile.

Tre sorgenti, nell'ordine in cui la CLI le prova:

1. ``--photos-dir``      cartella locale (anche esportata a mano da Drive);
2. ``--photos-manifest`` JSON con i file gia scaricati (base64 o path): e il
   formato che esce dal connettore MCP Google Drive quando le foto vengono
   prelevate dall'assistente invece che dallo script;
3. ``--drive-folder-id`` cartella Drive dell'immobile, letta via API REST v3.

In tutti i casi vale la regola del workflow manuale: per i materiali pubblici si
usano **sempre** le foto in ``FOTO/SENZA LOGO``, e ``__MACOSX`` si ignora.
"""

from __future__ import annotations

import base64
import json
import logging
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

log = logging.getLogger(__name__)

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
PREFERRED_FOLDER = "senza logo"
IGNORED_FOLDERS = {"__macosx", "con logo"}

DRIVE_API = "https://www.googleapis.com/drive/v3"
FOLDER_MIME = "application/vnd.google-apps.folder"


def natural_key(name: str) -> list:
    """Ordinamento naturale: `INNOVA-2` prima di `INNOVA-10`, non dopo."""
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", name)]


# ------------------------------------------------------------------ locale ---
def photos_from_dir(directory: str | Path, n: int = 6) -> list[Path]:
    """Prime `n` immagini della cartella, preferendo la sottocartella SENZA LOGO."""
    root = Path(directory)
    if not root.is_dir():
        raise FileNotFoundError(f"Cartella foto inesistente: {root}")

    search_root = _preferred_subfolder(root) or root
    files = sorted(
        (
            p
            for p in search_root.rglob("*")
            if p.is_file()
            and p.suffix.lower() in IMAGE_SUFFIXES
            and not _is_ignored(p.relative_to(search_root))
        ),
        key=lambda p: natural_key(p.name),
    )
    if not files:
        raise FileNotFoundError(f"Nessuna immagine utilizzabile in {search_root}")
    log.info("foto locali: %d trovate in %s, ne uso %d", len(files), search_root, min(n, len(files)))
    return files[:n]


def _preferred_subfolder(root: Path) -> Path | None:
    for candidate in sorted(root.rglob("*")):
        if candidate.is_dir() and candidate.name.strip().lower() == PREFERRED_FOLDER:
            return candidate
    return None


def _is_ignored(relative: Path) -> bool:
    parts = {part.strip().lower() for part in relative.parts[:-1]}
    return bool(parts & IGNORED_FOLDERS) or relative.name.startswith("._")


# ---------------------------------------------------------------- manifest ---
def photos_from_manifest(manifest_path: str | Path, out_dir: str | Path, n: int = 6) -> list[Path]:
    """Materializza le foto descritte in un manifest JSON.

    Formato accettato (lista, oppure ``{"photos": [...]}``)::

        [{"name": "01.jpg", "base64": "..."},
         {"name": "02.jpg", "path": "/percorso/locale/02.jpg"}]
    """
    manifest_path = Path(manifest_path)
    raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = raw.get("photos", raw) if isinstance(raw, dict) else raw

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    for index, entry in enumerate(entries):
        if len(saved) >= n:
            break
        if isinstance(entry, str):
            entry = {"path": entry}
        name = entry.get("name") or f"foto-{index + 1:02d}.jpg"
        dest = out_dir / name
        if entry.get("base64"):
            dest.write_bytes(base64.b64decode(_strip_data_url(entry["base64"])))
        elif entry.get("path"):
            dest.write_bytes(Path(entry["path"]).read_bytes())
        else:
            raise ValueError(f"Voce del manifest senza 'base64' ne 'path': {entry!r}")
        saved.append(dest)
    if not saved:
        raise ValueError(f"Manifest foto vuoto: {manifest_path}")
    return saved


def _strip_data_url(value: str) -> str:
    return value.split(",", 1)[1] if value.startswith("data:") else value


# ------------------------------------------------------------------- drive ---
class DriveClient:
    """Client minimale per Google Drive v3 (sola lettura, via REST)."""

    def __init__(self, token: str | None = None) -> None:
        self.token = token or _drive_token()

    def _get(self, path: str, **params: str) -> dict:
        url = f"{DRIVE_API}/{path}?{urllib.parse.urlencode(params)}"
        request = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.token}"})
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))

    def list_children(self, folder_id: str) -> list[dict]:
        items: list[dict] = []
        page_token = ""
        while True:
            params = {
                "q": f"'{folder_id}' in parents and trashed = false",
                "fields": "nextPageToken, files(id, name, mimeType, size)",
                "pageSize": "200",
                "supportsAllDrives": "true",
                "includeItemsFromAllDrives": "true",
            }
            if page_token:
                params["pageToken"] = page_token
            payload = self._get("files", **params)
            items.extend(payload.get("files", []))
            page_token = payload.get("nextPageToken", "")
            if not page_token:
                return items

    def find_folder(self, name_contains: str) -> str:
        """Cerca la cartella dell'immobile per nome (equivalente di `title contains`)."""
        escaped = name_contains.replace("'", "\\'")
        payload = self._get(
            "files",
            q=f"mimeType = '{FOLDER_MIME}' and name contains '{escaped}' and trashed = false",
            fields="files(id, name)",
            pageSize="20",
            supportsAllDrives="true",
            includeItemsFromAllDrives="true",
        )
        files = payload.get("files", [])
        if not files:
            raise FileNotFoundError(f"Nessuna cartella Drive trovata per '{name_contains}'")
        if len(files) > 1:
            log.warning(
                "piu cartelle Drive corrispondono a '%s': uso '%s'. Le altre: %s",
                name_contains,
                files[0]["name"],
                ", ".join(f["name"] for f in files[1:]),
            )
        return files[0]["id"]

    def find_photos_folder(self, folder_id: str, depth: int = 3) -> str:
        """Scende nell'albero fino alla cartella SENZA LOGO."""
        frontier = [(folder_id, 0)]
        while frontier:
            current, level = frontier.pop(0)
            for child in self.list_children(current):
                if child["mimeType"] != FOLDER_MIME:
                    continue
                name = child["name"].strip().lower()
                if name == PREFERRED_FOLDER:
                    return child["id"]
                if name in IGNORED_FOLDERS or level >= depth:
                    continue
                frontier.append((child["id"], level + 1))
        log.warning("cartella SENZA LOGO non trovata: uso le immagini della cartella indicata")
        return folder_id

    def download_images(self, folder_id: str, out_dir: Path, n: int) -> list[Path]:
        images = sorted(
            (
                f
                for f in self.list_children(folder_id)
                if Path(f["name"]).suffix.lower() in IMAGE_SUFFIXES
                and not f["name"].startswith("._")
            ),
            key=lambda f: natural_key(f["name"]),
        )[:n]
        if not images:
            raise FileNotFoundError(f"Nessuna immagine nella cartella Drive {folder_id}")

        out_dir.mkdir(parents=True, exist_ok=True)
        saved: list[Path] = []
        for image in images:
            dest = out_dir / image["name"]
            url = f"{DRIVE_API}/files/{image['id']}?alt=media&supportsAllDrives=true"
            request = urllib.request.Request(
                url, headers={"Authorization": f"Bearer {self.token}"}
            )
            with urllib.request.urlopen(request, timeout=180) as response:
                dest.write_bytes(response.read())
            log.info("scaricata %s", dest.name)
            saved.append(dest)
        return saved


def _drive_token() -> str:
    token = os.environ.get("INNOVA_GDRIVE_TOKEN") or os.environ.get("GDRIVE_ACCESS_TOKEN")
    if token:
        return token

    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        try:
            from google.auth.transport.requests import Request  # type: ignore
            from google.oauth2 import service_account  # type: ignore
        except ImportError as exc:  # pragma: no cover - dipendenza opzionale
            raise RuntimeError(
                "GOOGLE_APPLICATION_CREDENTIALS e impostato ma google-auth non e installato: "
                "`pip install google-auth`."
            ) from exc
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=["https://www.googleapis.com/auth/drive.readonly"]
        )
        credentials.refresh(Request())
        return credentials.token

    raise RuntimeError(
        "Nessuna credenziale Google Drive disponibile.\n"
        "Opzioni:\n"
        "  - esporta INNOVA_GDRIVE_TOKEN con un access token OAuth (scope drive.readonly);\n"
        "  - imposta GOOGLE_APPLICATION_CREDENTIALS su un service account con accesso alla cartella;\n"
        "  - scarica le foto a mano (o con il connettore MCP Drive) e usa --photos-dir/--photos-manifest."
    )


def fetch_property_photos(
    n: int = 6,
    *,
    photos_dir: str | Path | None = None,
    manifest: str | Path | None = None,
    drive_folder_id: str | None = None,
    drive_search: str | None = None,
    work_dir: str | Path = "photos",
) -> list[Path]:
    """Restituisce fino a `n` path locali di foto pronte per video e landing."""
    if photos_dir:
        return photos_from_dir(photos_dir, n)
    if manifest:
        return photos_from_manifest(manifest, work_dir, n)
    if drive_folder_id or drive_search:
        client = DriveClient()
        folder_id = drive_folder_id or client.find_folder(drive_search or "")
        photos_folder = client.find_photos_folder(folder_id)
        return client.download_images(photos_folder, Path(work_dir), n)
    raise ValueError(
        "Nessuna sorgente foto indicata: usa --photos-dir, --photos-manifest o --drive-folder-id."
    )
