# Parte terza — Note tecniche

## I cinque strati

```
┌─────────────────────────────────────────────────────────────┐
│  1. INGRESSO MULTICANALE                                    │
│  telefono · email · WhatsApp · Facebook · Instagram          │
│  TikTok · YouTube · LinkedIn · Sara e chatbot                │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  2. MOTORE DI RILEVAMENTO INTENTO                           │
│  acquirente · investitore · affittuario · venditore          │
│  → demo/js/rilevamento-intento.js                            │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  3. GENERATORE DI LANDING                                   │
│  legge SOLO immobile.pubblico · vendita o affitto           │
│  → demo/js/genera-landing.js + calcoli.js                    │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  4. MOTORE DI REGOLE — SEMAFORO FINANZIARIO                 │
│  verde · giallo · rosso   (regole nel JSON, non nel codice) │
│  → config/regole-semaforo.json + motore-semaforo.js          │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  5. ORCHESTRATORE DELLE COMUNICAZIONI                       │
│  follow-up · recupero · promemoria · mancato arrivo         │
│  → config/comunicazioni.json + orchestratore.js              │
└─────────────────────────────────────────────────────────────┘
```

Ogni strato è sostituibile senza toccare gli altri. Il motore di regole non sa niente di
WhatsApp; l'orchestratore non sa come si calcola un'imposta di registro.

## Dove stanno i dati

| Cosa | Dove sta | Perché |
|---|---|---|
| Anagrafica immobili | **gestionale** | resta la fonte unica di verità, nessuna copia da tenere allineata |
| Foto, video, planimetrie | **Google Drive** | già in uso, già organizzato |
| Regole, testi, sequenze | file di configurazione | modificabili senza sviluppo |
| Comportamento utenti | Innova Experience | è lì che va guardato e comandato |

Nel prototipo l'anagrafica è in `data/immobili/*.json` perché serviva qualcosa su cui girare.
In produzione quei file diventano la risposta di un'API che legge dal gestionale e restituisce
**solo il nodo pubblico**.

## Integrazioni necessarie

| Servizio | A cosa serve | Cosa serve per attivarlo |
|---|---|---|
| **Google Calendar** | slot reali (FreeBusy) e creazione appuntamento (Events.insert) | account di servizio con delega sul calendario dell'agenzia |
| **Provider WhatsApp Business** | primo canale di follow-up e promemoria | numero verificato + modelli di messaggio approvati (servono giorni, va avviato per primo) |
| **Email transazionale** | conferme, fallback, notifiche interne | dominio verificato con SPF, DKIM e DMARC |
| **Vrexx** | tour virtuale | un URL per immobile in `data/immobili/*.json` |
| **Analytics comportamentale** | cruscotto in Innova Experience | endpoint che riceve la coda di eventi in POST |

### Nota sui modelli WhatsApp

I messaggi che partono per primi, senza che il cliente abbia scritto, devono essere modelli
approvati da Meta. I testi in `config/comunicazioni.json` sono già scritti nella forma
giusta, con i segnaposto `{{contatto.nome}}`: vanno sottoposti così come sono. L'approvazione
richiede tempo ed è il collo di bottiglia di tutta la fase 3.

## La regola più importante per la produzione

**Il semaforo deve girare lato server.**

Nel prototipo gira nel browser perché la demo è statica e deve poter essere aperta senza
infrastruttura. Ma un motore di regole che gira nel browser è un motore di regole che
l'utente può modificare: chiunque apra gli strumenti per sviluppatori può cambiare la
risposta e sbloccarsi la prenotazione da solo.

In produzione:

- il modulo invia le risposte al server;
- il server valuta le regole (`motore-semaforo.js` gira uguale in Node);
- il server risponde con esito, messaggio e — solo se verde — il permesso di prenotare;
- gli slot vengono generati dal server, non dal browser.

Il codice del motore non cambia: è già scritto per girare in entrambi i posti, e i test
lo eseguono in Node.

## Sicurezza e trattamento

- **Consenso prima del tracciamento identificato.** Nessun identificativo persistente prima
  della spunta privacy; solo eventi anonimi di pagina.
- **Consenso marketing separato** da quello di ricontatto: è quello che alimenta il club.
- **Dati minimi.** Reddito e budget servono al semaforo e al consulente; non vanno né esposti
  in pagina né spediti agli strumenti di analytics pubblicitari.
- **Conservazione.** Va fissato un tempo di conservazione per i contatti che non concludono
  (proposta: 24 mesi) e una procedura di cancellazione su richiesta.
- **Registro dei trattamenti.** Il semaforo è una profilazione: va inserito nel registro, con
  la logica descritta in modo comprensibile. Il file `config/regole-semaforo.json` è già
  leggibile da una persona non tecnica ed è la descrizione migliore da allegare.

Il dettaglio sull'articolo 22 sta in `06-gdpr.md`.

## Struttura del prototipo

```
progetto-landing-ai/
├── config/                    regole e testi, modificabili senza sviluppo
│   ├── regole-semaforo.json   ← il semaforo, l'ordine delle regole è la logica
│   ├── provvigioni.json       ← tariffario in chiaro
│   ├── costi-passaggi.json    ← i tre passaggi + percorso affitto
│   ├── comunicazioni.json     ← tutte le sequenze automatiche
│   ├── servizi.json           ← ventaglio servizi, incluso sovraindebitamento
│   └── modulo-campi.json      ← schema campi (punto aperto: vedi 05)
├── data/
│   ├── agenzia.json           ← club, prenotazione, video istituzionali
│   └── immobili/*.json        ← pubblico / riservato
├── demo/
│   ├── index.html             ← indice degli scenari da provare
│   ├── landing.html           ← guscio vuoto: tutto il contenuto è generato
│   └── js/                    ← i cinque motori
├── test/                      ← 51 test, node --test
└── docs/                      ← questa documentazione
```
