"""Legge il foglio Google "Modulo Innova Experiences (Risposte)" e prepara
i lead da analizzare.

Accesso al foglio, in ordine di preferenza:
1. GOOGLE_SERVICE_ACCOUNT_JSON: JSON completo di un service account Google
   con cui il foglio è stato condiviso (sola lettura).
2. GOOGLE_SHEET_CSV_URL: URL di esportazione CSV del foglio (richiede che il
   foglio sia leggibile da "Chiunque abbia il link").

I lead già processati sono tracciati in data/leads_processati.json (impronta
sha256 della riga). Solo i lead nuovi vengono scritti in
output/leads_da_analizzare.json, salvo PROCESSA_TUTTI=true.
"""

import csv
import hashlib
import io
import json
import os
import sys
from pathlib import Path

STATO_PATH = Path("data/leads_processati.json")
OUTPUT_PATH = Path("output/leads_da_analizzare.json")

# Colonne lunghe di consenso/privacy: inutili per il report, le scartiamo.
INTESTAZIONI_DA_SCARTARE = ("gdpr", "informativa", "dichiaro di aver letto")


def leggi_righe():
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    csv_url = os.environ.get("GOOGLE_SHEET_CSV_URL", "").strip()
    sheet_id = os.environ["SHEET_ID"]

    if sa_json:
        import gspread

        client = gspread.service_account_from_dict(json.loads(sa_json))
        foglio = client.open_by_key(sheet_id).get_worksheet(0)
        return foglio.get_all_values()

    if csv_url:
        import requests

        risposta = requests.get(csv_url, timeout=60)
        risposta.raise_for_status()
        risposta.encoding = "utf-8"
        return list(csv.reader(io.StringIO(risposta.text)))

    print(
        "ERRORE: configurare il secret GOOGLE_SERVICE_ACCOUNT_JSON "
        "(consigliato) oppure GOOGLE_SHEET_CSV_URL.",
        file=sys.stderr,
    )
    sys.exit(1)


def righe_a_lead(righe):
    """Converte le righe in dizionari, gestendo intestazioni duplicate."""
    if not righe:
        return []
    intestazioni = []
    viste = {}
    for nome in righe[0]:
        nome = nome.strip() or "Colonna"
        viste[nome] = viste.get(nome, 0) + 1
        intestazioni.append(nome if viste[nome] == 1 else f"{nome} ({viste[nome]})")

    leads = []
    for riga in righe[1:]:
        if not any(cella.strip() for cella in riga):
            continue
        lead = {}
        for nome, valore in zip(intestazioni, riga):
            valore = valore.strip()
            if not valore:
                continue
            nome_minuscolo = nome.lower()
            if any(chiave in nome_minuscolo for chiave in INTESTAZIONI_DA_SCARTARE):
                continue
            lead[nome] = valore
        if lead:
            impronta = hashlib.sha256(
                "|".join(cella.strip() for cella in riga).encode("utf-8")
            ).hexdigest()
            lead["_id"] = impronta
            leads.append(lead)
    return leads


def main():
    leads = righe_a_lead(leggi_righe())
    print(f"Lead totali nel foglio: {len(leads)}")

    processati = set()
    if STATO_PATH.exists():
        processati = set(json.loads(STATO_PATH.read_text("utf-8")))

    processa_tutti = os.environ.get("PROCESSA_TUTTI", "").lower() == "true"
    nuovi = leads if processa_tutti else [l for l in leads if l["_id"] not in processati]
    print(f"Lead da analizzare: {len(nuovi)}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(nuovi, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    STATO_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATO_PATH.write_text(
        json.dumps(sorted(processati | {l["_id"] for l in leads}), indent=2),
        encoding="utf-8",
    )

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"nuovi_lead={len(nuovi)}\n")


if __name__ == "__main__":
    main()
