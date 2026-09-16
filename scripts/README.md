# Caricamento contatti su onOffice

Automatizza l'inserimento su onOffice dei contatti che arrivano dal Modulo Innova
Experience (`innovaexperience.it/modulo`), oggi ricopiati a mano nel CRM.

## Cosa serve prima

Credenziali API onOffice — `token` e `secret` — da richiedere al supporto onOffice
(supporto@onoffice.com). Vedi `docs/richiesta-credenziali-api-onoffice.md` per la
bozza della richiesta.

## Come si usa

Lo script legge un CSV con una riga per contatto (separatore `;`, UTF-8), lo stesso
formato prodotto dall'estrazione dei moduli.

**1. Anteprima — non scrive nulla su onOffice:**

```bash
python3 scripts/onoffice_upload.py contatti.csv
```

Stampa per ogni contatto la richiesta JSON esatta che verrebbe inviata. Serve a
controllare la mappatura dei campi prima di toccare il CRM.

**2. Invio reale:**

```bash
ONOFFICE_TOKEN=xxx ONOFFICE_SECRET=yyy \
  python3 scripts/onoffice_upload.py contatti.csv --execute
```

Stampa una riga di esito per contatto e un totale finale.

## Da verificare al primo utilizzo

Il formato della richiesta e i nomi dei campi onOffice (che sono in tedesco:
`Vorname`, `Name`, `Telefon1`, `Email`, …) sono stati scritti **senza poter
consultare la documentazione ufficiale**, irraggiungibile dall'ambiente in cui lo
script è stato generato. Prima del primo `--execute` su dati veri:

1. lancia l'anteprima e prendi il JSON di un contatto;
2. confrontalo con `apidoc.onoffice.de` alle voci *API request* e *create address*;
3. correggi gli eventuali nomi sbagliati in `scripts/onoffice_fields.json`.

La mappatura vive tutta in quel file JSON proprio per non dover toccare il codice:
i campi senza corrispondenza certa in onOffice (zona, budget, tempistiche, fonte…)
non vengono persi, finiscono nella nota della scheda contatto.

Consiglio: al primo giro esegui `--execute` su un CSV con **una riga sola** di
prova, controlla la scheda creata su onOffice, poi lancia il gruppo completo.

## Dati personali

I CSV dei contatti **non vanno committati**: sono dati di lead reali, riservati
secondo l'informativa GDPR Innova. Tienili fuori dal repository — lo script accetta
un percorso qualsiasi, anche fuori dalla cartella di lavoro.

Per lo stesso motivo qui non c'è una GitHub Action: farla girare richiederebbe il
CSV dentro il repository. Lo script si esegue in locale.
