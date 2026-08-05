# Parte prima — Il flusso

I quindici punti del progetto, tradotti in comportamenti verificabili. Per ciascuno:
cosa fa il sistema, dove sta scritto, e a che punto è nel prototipo.

Legenda dello stato:
**Prototipato** = funziona nella demo · **Configurato** = la logica c'è, manca il collegamento al servizio esterno · **Da fare** = previsto, non ancora costruito.

---

## 1. Canali di ingresso

Telefono, email, WhatsApp, Facebook, Instagram, TikTok, YouTube, LinkedIn: qualunque sia la porta,
il contatto entra nello stesso schema. Sara e il chatbot non sono un canale a parte, sono
il primo strato di raccolta che alimenta il campo `canale_ingresso` e passa al motore
di rilevamento intento quello che il cliente ha detto.

Il canale non cambia il flusso, cambia solo due cose: quale link viene inviato
(con i parametri `utm_source` e `intento` già impostati) e su quale canale il
follow-up risponderà per primo — si risponde dove il cliente ha scritto.

- Dove: `config/modulo-campi.json` → `campi_derivati.canale_ingresso`
- Stato: **Configurato** (la landing legge già `utm_source`; le integrazioni dei canali sono in `docs/03-architettura.md`)

## 2. Rilevamento dell'intento

Acquirente, investitore, affittuario o venditore. Tre sorgenti con affidabilità decrescente:
la risposta del modulo (certezza), il contesto di arrivo — campagna, parametri del link, tipo
di immobile — (indizio forte), le parole usate in chat con Sara (indizio).

Quando le sorgenti sono in disaccordo vince quella più affidabile. Sotto una confidenza
di 0,5 il sistema non indovina: mostra la versione neutra e chiede.

- Dove: `demo/js/rilevamento-intento.js`
- Stato: **Prototipato** — provalo con `?chat=...` o `?utm_campaign=vendere-casa-palermo`

## 3. Landing dinamica

Per acquirenti, investitori e affittuari la pagina si genera dal file dell'immobile.
La carta d'identità riporta tutto quello che già usate — zona, indirizzo, anno, metratura,
composizione, classe energetica, riscaldamento, abitabilità, categoria e rendita catastale,
prezzo, planimetria, descrizione narrativa — riprodotto in chiave digitale.

Sotto, il percorso cambia da solo secondo il tipo di operazione:

- **Vendita:** i tre passaggi dell'acquisto (proposta, preliminare, rogito) con i costi
  calcolati su questo immobile, non generici. L'imposta di registro viene calcolata sul
  valore catastale reale a partire dalla rendita.
- **Affitto:** documenti richiesti, importi alla proposta e alla firma, e come velocizzare tutto.

- Dove: `demo/js/genera-landing.js`, `demo/js/calcoli.js`, `config/costi-passaggi.json`
- Stato: **Prototipato**

## 4. I due percorsi di esperienza

Tour virtuale online con Vrexx, aperto a chi entra nel club. Oppure prova con il visore in
ufficio, riservata ai soli clienti prequalificati: la sala è una risorsa scarsa e si tiene
per chi è pronto a decidere. Chi chiede il visore senza aver superato il gate viene
riaccompagnato al modulo, non respinto.

- Dove: sezione "Due modi per visitarla" + `demo/js/prenotazione.js` → `luoghiDisponibili()`
- Stato: **Prototipato** (manca l'URL Vrexx per immobile, in `data/immobili/*.json`)

## 5. Il gate del modulo

Non "compila per informazioni", ma accesso al Club Innova: la scheda completa, la planimetria,
il tour, e soprattutto l'anteprima sugli immobili prima che finiscano sui portali pubblici.
Il vantaggio è dichiarato prima di chiedere i dati.

- Dove: `data/agenzia.json` → `club`, sezione "Club Innova" della landing
- Stato: **Prototipato**

## 6. Il semaforo finanziario

- **Contanti** o **mutuo deliberato** → verde, prenotazione aperta subito.
- **Mutuo da richiedere** o **situazione poco chiara** → giallo: notifica automatica al
  consulente finanziario, prenotazione bloccata. Solo l'esito positivo registrato dal
  consulente la sblocca.
- **Budget molto distante dal prezzo** → rosso: nessuna porta chiusa, si passa a una
  persona e ad alternative.

L'ordine delle regole *è* la logica: vince la prima che corrisponde. Chi vende non passa
dal semaforo; i casi affitto si valutano sul reddito, non sulla modalità d'acquisto.
Ogni esito diverso dal verde espone sempre "Parla con una persona" (vedi `06-gdpr.md`).

- Dove: `config/regole-semaforo.json`, `demo/js/motore-semaforo.js`
- Stato: **Prototipato**, con 14 test automatici

## 7. Prenotazione automatica

Slot reali generati dalla disponibilità dell'agenzia e incrociati con gli impegni già a
calendario: quello che il cliente vede è libero adesso. Nessuna conferma manuale — lo slot
scelto è già l'appuntamento, con evento su Google Calendar e file .ics per il cliente.

- Dove: `demo/js/prenotazione.js`, `data/agenzia.json` → `prenotazione`
- Stato: **Configurato** — la generazione slot e l'evento funzionano; manca la chiave
  Google Calendar (FreeBusy in lettura, Events.insert in scrittura)

## 8. Pipeline venditore

Modulo più snello — zona, tipologia, metratura, motivo — nessun semaforo finanziario,
e l'invito è alla valutazione immediata dell'immobile, non alla visita.

Un dettaglio delicato: fra i motivi di vendita c'è "difficoltà economica". Chi lo seleziona
riceve l'etichetta sovraindebitamento, una notifica diretta al responsabile e **nessuna**
sequenza commerciale automatica.

- Dove: `config/modulo-campi.json` → `campi_pipeline_venditore`, sequenza `venditore` in `config/comunicazioni.json`
- Stato: **Configurato** (la landing venditore dedicata è la fase 4 della roadmap)

## 9. Follow-up automatico a tre messaggi

24 ore, 3 giorni, 7 giorni. Il primo richiama il tour, il secondo racconta due dettagli che
nelle foto non si vedono, il terzo chiede il permesso di fermarsi — ed è quello che salva
la relazione con chi non è interessato.

Qualunque risposta del cliente, su qualunque canale, interrompe la sequenza e passa la
conversazione all'agente. Una prenotazione confermata la interrompe e apre la sequenza
appuntamento. Massimo un messaggio automatico al giorno, su tutti i canali sommati.

- Dove: `config/comunicazioni.json` → `sequenze.follow_up_lead`, `demo/js/orchestratore.js`
- Stato: **Configurato** — il piano viene calcolato e stampato in console; l'invio si attiva
  collegando il provider WhatsApp e il servizio email

## 10. Recupero del modulo abbandonato

Un solo messaggio, dopo 15 minuti, e solo se c'è già un contatto valido e il consenso
spuntato. Riprende dal punto esatto in cui il cliente si era fermato.

- Dove: `config/comunicazioni.json` → `sequenze.recupero_modulo_abbandonato`, `demo/js/tracciamento.js` → `osservaAbbandonoModulo()`
- Stato: **Prototipato** (chiudi la scheda a metà modulo e guarda la console)

## 11. Promemoria e mancato arrivo

Conferma immediata con .ics, promemoria il giorno prima con possibilità di spostare in un
tocco, un messaggio tre ore prima con la mappa. Se il cliente non si presenta: nessun
rimprovero, un messaggio dopo due ore per riprogrammare e uno dopo tre giorni che finisce
con una chiamata dell'agente.

- Dove: `config/comunicazioni.json` → `sequenze.appuntamento` e `sequenze.mancato_arrivo`
- Stato: **Configurato**

## 12. Versione inglese

Da valutare. La struttura è già pronta: tutti i testi rivolti al cliente stanno nei file
di configurazione e nei dati dell'immobile, nessuno è scritto nel codice. Aggiungere
l'inglese significa affiancare un secondo file di testi, non riscrivere la landing.

- Stato: **Da fare** (decisione tua, nessun lavoro sprecato se la risposta è sì)

## 13. Monitoraggio comportamentale

Quali sezioni vengono guardate e per quanti secondi, quali foto si aprono, se parte il tour,
quali video e fino a che punto, dove ci si ferma nel modulo, profondità di scorrimento,
tempo totale. Gli eventi vengono accodati e spediti in blocco a Innova Experience, dove
saranno visibili e comandabili.

Nessun evento identificato prima del consenso: fino ad allora si contano solo eventi
anonimi di pagina.

- Dove: `demo/js/tracciamento.js`
- Stato: **Prototipato** — coda locale ispezionabile con `innova.riepilogo()` in console;
  manca l'endpoint di Innova Experience

## 14. Galleria video

Video dell'immobile — i contenuti social già prodotti — e video istituzionali su chi siete
e come lavorate. Tutto in embed dai canali originali (nessun file duplicato) e tracciato
nel comportamento dell'utente.

- Dove: `data/immobili/*.json` → `media.video_immobile`, `data/agenzia.json` → `video_istituzionali`
- Stato: **Prototipato** (i due video istituzionali sono da collegare)

## 15. Assistenza nelle crisi da sovraindebitamento

Presente nel ventaglio dei servizi, senza pipeline dedicata separata, esattamente come chiesto.
Chi rischia di perdere casa per debiti, aste giudiziarie o pressione dei creditori trova
scritto che una via d'uscita ordinata quasi sempre esiste, e che il primo confronto è
riservato e senza impegno.

Due accorgimenti: il contatto entra nel flusso ordinario con un'etichetta e una notifica al
responsabile, e viene **escluso** dalle sequenze automatiche di marketing. Chi sta perdendo
la casa non deve ricevere un messaggio automatico che gli chiede se ha visto il tour virtuale.

- Dove: `config/servizi.json` → servizio `sovraindebitamento` con `esclusione_automazioni`
- Stato: **Prototipato**, con test automatico che verifica l'esclusione
