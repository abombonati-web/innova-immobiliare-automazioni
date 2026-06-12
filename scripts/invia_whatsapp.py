"""Invia su WhatsApp i report generati in output/report_*.txt.

Provider supportati (in ordine di preferenza, in base ai secret configurati):
1. Twilio  - TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM
2. CallMeBot (gratuito) - CALLMEBOT_APIKEY

In entrambi i casi serve WHATSAPP_PHONE (numero destinatario con prefisso
internazionale, es. +39333...). I messaggi lunghi vengono divisi in blocchi.
"""

import os
import sys
import time
from pathlib import Path

import requests

MAX_CARATTERI = 1500
PAUSA_SECONDI = 12  # CallMeBot accetta pochi messaggi al minuto


def spezza(testo):
    """Divide il testo in blocchi <= MAX_CARATTERI, spezzando sulle righe."""
    blocchi, corrente = [], ""
    for riga in testo.splitlines():
        if len(corrente) + len(riga) + 1 > MAX_CARATTERI and corrente:
            blocchi.append(corrente)
            corrente = ""
        corrente = f"{corrente}\n{riga}" if corrente else riga
    if corrente:
        blocchi.append(corrente)
    return blocchi


def invia_callmebot(telefono, apikey, testo):
    r = requests.get(
        "https://api.callmebot.com/whatsapp.php",
        params={"phone": telefono, "apikey": apikey, "text": testo},
        timeout=60,
    )
    r.raise_for_status()


def invia_twilio(sid, token, mittente, telefono, testo):
    r = requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
        auth=(sid, token),
        data={
            "From": f"whatsapp:{mittente}",
            "To": f"whatsapp:{telefono}",
            "Body": testo,
        },
        timeout=60,
    )
    r.raise_for_status()


def main():
    telefono = os.environ.get("WHATSAPP_PHONE", "").strip()
    if not telefono:
        print("ERRORE: secret WHATSAPP_PHONE non configurato.", file=sys.stderr)
        sys.exit(1)

    twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
    callmebot_key = os.environ.get("CALLMEBOT_APIKEY", "").strip()

    if twilio_sid:
        token = os.environ["TWILIO_AUTH_TOKEN"]
        mittente = os.environ["TWILIO_WHATSAPP_FROM"]
        invia = lambda testo: invia_twilio(twilio_sid, token, mittente, telefono, testo)
    elif callmebot_key:
        invia = lambda testo: invia_callmebot(telefono, callmebot_key, testo)
    else:
        print(
            "ERRORE: configurare CALLMEBOT_APIKEY oppure i secret Twilio.",
            file=sys.stderr,
        )
        sys.exit(1)

    nuovi_lead = os.environ.get("NUOVI_LEAD", "0")
    report = sorted(Path("output").glob("report_*.txt")) if Path("output").exists() else []

    if nuovi_lead == "0" or not report:
        messaggi = [
            "*Innova Experiences - report mattutino*\n"
            "Nessun nuovo lead da analizzare oggi."
        ]
    else:
        messaggi = []
        for percorso in report:
            testo = percorso.read_text("utf-8").strip()
            if testo:
                messaggi.extend(spezza(testo))

    errori = 0
    for i, messaggio in enumerate(messaggi):
        try:
            invia(messaggio)
            print(f"Inviato messaggio {i + 1}/{len(messaggi)}")
        except Exception as e:  # noqa: BLE001 - logghiamo e proseguiamo
            errori += 1
            print(f"ERRORE invio messaggio {i + 1}: {e}", file=sys.stderr)
        if i < len(messaggi) - 1:
            time.sleep(PAUSA_SECONDI)

    if errori:
        sys.exit(1)


if __name__ == "__main__":
    main()
