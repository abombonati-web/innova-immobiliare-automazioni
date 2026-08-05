# Sistema landing page automatica con prequalifica AI

Prototipo del sistema descritto nel progetto per **Innova Immobiliare**: una landing generata
automaticamente dai dati dell'immobile, che riconosce chi la sta guardando, mostra tutto in
chiaro — provvigioni comprese — e lascia prenotare solo chi è davvero pronto a comprare.

> ## ⚠️ Non operativo
>
> Questo progetto è tenuto **fuori dalla piattaforma Innova Experience**, come richiesto.
> Non è pubblicato, non è collegato al sito, non invia messaggi a nessuno e non tocca la
> landing dell'evento già online (`index.html` alla radice del repository, invariata).
>
> Vive su un ramo separato e resta lì finché non arriva la tua conferma.

## Provalo in due comandi

```bash
cd progetto-landing-ai
python3 -m http.server 8080
```

Poi apri **http://localhost:8080/demo/** — c'è un indice con gli scenari e una tabella di
cosa deve succedere a ogni prova.

I test dei motori:

```bash
node --test "test/*.test.js"     # 51 test, nessuna dipendenza da installare
```

## Che cosa funziona davvero

| | |
|---|---|
| **Landing dinamica** | tutto il contenuto è generato da un file JSON: cambia il parametro `?immobile=` e la pagina si riscrive |
| **Rilevamento intento** | acquirente, investitore, affittuario o venditore, riconosciuto da campagna, link o parole della chat con Sara |
| **Carta d'identità** | zona, indirizzo, anno, metratura, composizione, classe energetica, riscaldamento, abitabilità, dati catastali, prezzo |
| **Tre passaggi dell'acquisto** | proposta, preliminare, rogito con i costi calcolati su **questo** immobile, imposta di registro compresa |
| **Percorso affitto** | documenti richiesti, importi alla proposta e alla firma, come velocizzare |
| **Provvigioni in chiaro** | criterio, imponibile, IVA e totale, prima della visita |
| **Semaforo finanziario** | verde, giallo, rosso — regole in un file di configurazione, non nel codice |
| **Prenotazione** | slot reali che escludono gli orari occupati, evento calendario, file .ics |
| **Comunicazioni** | follow-up 24h/3g/7g, recupero modulo, promemoria, mancato arrivo: calcolati e stampati in console |
| **Tracciamento** | sezioni lette e per quanto, foto aperte, video, punto di abbandono del modulo |

Quello che **non** succede: nessun messaggio parte, nessun evento viene creato su Google
Calendar, nessun dato esce dal browser. Le automazioni vengono calcolate e mostrate, non eseguite.

## Come si legge il progetto

| Documento | Contenuto |
|---|---|
| [`docs/01-flusso.md`](docs/01-flusso.md) | i quindici punti del flusso, con lo stato di ciascuno |
| [`docs/02-visibilita-dati.md`](docs/02-visibilita-dati.md) | cosa vede il cliente, cosa resta all'agenzia, e come è garantito |
| [`docs/03-architettura.md`](docs/03-architettura.md) | i cinque strati, le integrazioni, dove stanno i dati |
| [`docs/04-roadmap.md`](docs/04-roadmap.md) | le cinque fasi: cosa è fatto, cosa manca |
| [`docs/05-modulo-campi.md`](docs/05-modulo-campi.md) | **il punto ancora aperto** e come chiuderlo in cinque minuti |
| [`docs/06-gdpr.md`](docs/06-gdpr.md) | l'articolo 22 e perché il sistema può filtrare ma non respingere |

## Cosa si cambia senza toccare il codice

Tutto quello che conta sta in `config/`, in italiano leggibile:

- `regole-semaforo.json` — chi passa, chi va in verifica, chi parla con una persona
- `provvigioni.json` — il tariffario
- `costi-passaggi.json` — i tre passaggi e il percorso affitto
- `comunicazioni.json` — testi, canali e tempi di ogni messaggio automatico
- `servizi.json` — il ventaglio dei servizi, sovraindebitamento compreso
- `modulo-campi.json` — lo schema dei campi

## Il punto ancora aperto

Il contenuto esatto del modulo su `innovaexperience.it/modulo` non è recuperabile da questo
ambiente: il dominio è bloccato dalla policy di rete del container (403 sul proxy, prima di
arrivare al sito). Lo schema dei campi è quindi una proposta, costruita per essere
sovrapponibile al modulo reale tramite una mappa di corrispondenze — nessun motore va
riscritto quando arriverà quello vero.

Per chiuderlo basta incollare qui le etichette e le opzioni del modulo attuale, oppure un
paio di screenshot. Dettagli in [`docs/05-modulo-campi.md`](docs/05-modulo-campi.md).
