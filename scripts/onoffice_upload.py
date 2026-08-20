#!/usr/bin/env python3
"""Carica su onOffice i contatti dei moduli Innova Experience.

Legge il CSV prodotto dall'estrazione dei moduli (una riga per contatto) e crea
le schede anagrafiche su onOffice via API.

Uso:
    # anteprima: stampa le richieste senza inviare nulla (default)
    python3 scripts/onoffice_upload.py contatti.csv

    # invio reale
    ONOFFICE_TOKEN=... ONOFFICE_SECRET=... \
        python3 scripts/onoffice_upload.py contatti.csv --execute

Le credenziali si ottengono dal supporto onOffice (supporto@onoffice.com) e non
vanno mai scritte nel repository: passarle da variabile d'ambiente o dai secret
del repository GitHub.

ATTENZIONE — da verificare prima del primo invio reale:
il formato della richiesta e i nomi dei campi qui sotto sono stati scritti senza
poter consultare apidoc.onoffice.de (bloccato dalla policy di rete dell'ambiente
in cui il file e' stato generato). Prima di usare --execute su dati veri, fare un
giro con --dry-run e confrontare il JSON stampato con la documentazione ufficiale
in "API request" e "create address". I nomi dei campi si correggono in
scripts/onoffice_fields.json senza toccare questo codice.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://api.onoffice.de/api/stable/api.php"
ACTION_CREATE = "urn:onoffice-de-ns:smart:2.16:smartml:action:create"
RESOURCE_ADDRESS = "address"
HMAC_VERSION = 2

FIELDS_PATH = Path(__file__).parent / "onoffice_fields.json"


def build_hmac(timestamp: int, token: str, resourcetype: str, actionid: str,
               secret: str) -> str:
    """HMAC v2 onOffice: base64(sha256(timestamp + token + resourcetype + actionid))."""
    message = f"{timestamp}{token}{resourcetype}{actionid}".encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("ascii")


def load_mapping() -> dict:
    with open(FIELDS_PATH, encoding="utf-8") as f:
        return json.load(f)


def row_to_parameters(row: dict, mapping: dict) -> dict:
    """Traduce una riga del CSV nei parametri della createAddress."""
    params: dict[str, object] = {}

    for csv_col, oo_field in mapping["campi_base"].items():
        value = (row.get(csv_col) or "").strip()
        if value:
            params[oo_field] = value

    for csv_col, oo_field in mapping["campi_estesi"].items():
        value = (row.get(csv_col) or "").strip()
        if value:
            params[oo_field] = value

    # I campi senza corrispondenza certa non si perdono: finiscono nella nota,
    # cosi' l'operatore li ha comunque sotto gli occhi nella scheda.
    da_verificare = mapping["campi_da_verificare"]
    extra_lines = []
    for csv_col, oo_field in da_verificare.items():
        if csv_col.startswith("_"):
            continue
        value = (row.get(csv_col) or "").strip()
        if not value:
            continue
        if oo_field:
            params[oo_field] = value
        else:
            extra_lines.append(f"{csv_col}: {value}")

    nota_field = mapping["campi_estesi"].get("Note complete", "Bemerkung")
    if extra_lines:
        existing = params.get(nota_field, "")
        blocco = "\n".join(extra_lines)
        params[nota_field] = f"{blocco}\n\n{existing}".strip()

    for key, value in mapping["valori_fissi"].items():
        if not key.startswith("_"):
            params.setdefault(key, value)

    # Evita di ricreare un contatto gia' presente con la stessa email.
    params["checkDuplicate"] = True

    return params


def build_action(params: dict, token: str, secret: str) -> dict:
    timestamp = int(time.time())
    return {
        "actionid": ACTION_CREATE,
        "resourceid": "",
        "identifier": "",
        "resourcetype": RESOURCE_ADDRESS,
        "timestamp": timestamp,
        "hmac_version": HMAC_VERSION,
        "hmac": build_hmac(timestamp, token, RESOURCE_ADDRESS, ACTION_CREATE, secret),
        "parameters": params,
    }


def send(action: dict, token: str) -> dict:
    envelope = {"token": token, "request": {"actions": [action]}}
    body = json.dumps(envelope).encode("utf-8")
    req = urllib.request.Request(
        API_URL, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def describe_result(payload: dict) -> tuple[bool, str]:
    """Estrae esito e messaggio dalla risposta onOffice."""
    try:
        action = payload["response"]["results"][0]
    except (KeyError, IndexError, TypeError):
        return False, f"risposta non riconosciuta: {json.dumps(payload)[:200]}"

    status = action.get("status", {})
    code = status.get("errorcode", -1)
    message = status.get("message", "")
    if code == 0:
        records = action.get("data", {}).get("records", [])
        new_id = records[0].get("id") if records else "?"
        return True, f"creato (id {new_id})"
    return False, f"errore {code}: {message}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv_path", help="CSV dei contatti (separatore ';')")
    parser.add_argument("--execute", action="store_true",
                        help="invia davvero a onOffice (senza questo flag e' una prova a vuoto)")
    parser.add_argument("--delimiter", default=";", help="separatore del CSV (default ';')")
    args = parser.parse_args()

    mapping = load_mapping()

    with open(args.csv_path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=args.delimiter))

    if not rows:
        print("Nessuna riga nel CSV.", file=sys.stderr)
        return 1

    token = os.environ.get("ONOFFICE_TOKEN", "")
    secret = os.environ.get("ONOFFICE_SECRET", "")

    if args.execute and not (token and secret):
        print("ONOFFICE_TOKEN e ONOFFICE_SECRET non impostati: impossibile inviare.",
              file=sys.stderr)
        return 2

    print(f"{len(rows)} contatti da {args.csv_path}")
    if not args.execute:
        print("MODALITA' ANTEPRIMA — nessuna scrittura su onOffice. "
              "Confrontare il JSON con apidoc.onoffice.de, poi rilanciare con --execute.\n")

    ok = failed = 0
    for i, row in enumerate(rows, 1):
        nome = f"{row.get('Nome', '')} {row.get('Cognome', '')}".strip()
        params = row_to_parameters(row, mapping)

        if not args.execute:
            action = build_action(params, token or "<TOKEN>", secret or "<SECRET>")
            print(f"--- {i}. {nome} ---")
            print(json.dumps({"token": token or "<TOKEN>",
                              "request": {"actions": [action]}},
                             ensure_ascii=False, indent=2))
            print()
            continue

        try:
            payload = send(build_action(params, token, secret), token)
            success, message = describe_result(payload)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            success, message = False, f"chiamata fallita: {exc}"

        print(f"{i:2}. {nome:35} {'OK ' if success else 'KO '} {message}")
        ok += success
        failed += not success

    if args.execute:
        print(f"\nCreati {ok} — falliti {failed}")
        return 1 if failed else 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
