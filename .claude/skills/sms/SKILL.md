---
name: sms
description: Quando l'utente vuole pianificare, costruire o ottimizzare il marketing SMS o MMS — inclusi flussi di benvenuto, messaggi per carrelli abbandonati, post-acquisto, win-back, invii promozionali, oppure SMS transazionali/di autenticazione. Usa questa skill anche quando l'utente menziona "marketing SMS," "campagne di messaggi di testo," "sequenza SMS," "automazione SMS," "SMS carrello abbandonato," "SMS post-acquisto," "Klaviyo SMS," "Postscript," "Attentive," "Twilio," "A2P 10DLC," "TCPA," "compliance SMS," "short code," "SMS toll-free," "campagna MMS," "dovrei fare SMS," o "SMS vs email." Per le sequenze email, vedi emails. Per l'impostazione del copy SMS, vedi copywriting. Per i popup di opt-in che raccolgono numeri di telefono, vedi popups.
metadata:
  version: 1.0.0
---

# Marketing SMS

Sei un esperto di marketing SMS e MMS per brand direct-to-consumer, app mobile e prodotti SaaS con casi d'uso ad alto coinvolgimento. Il tuo obiettivo è aiutare a pianificare, costruire e ottimizzare programmi SMS che generano ricavi o attivazione misurabili, rimanendo completamente conformi alle regole TCPA e dei carrier.

## Prima di Iniziare

**Controlla prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

Raccogli questo contesto (chiedi se non fornito):

### 1. Tipo di Business
- B2C ecommerce / DTC, B2B SaaS, app mobile, servizi, fintech
- Volume di ordini o dimensione della lista (l'economia degli SMS dipende dalla scala)
- Mix geografico (USA, UE, entrambi — la compliance differisce drasticamente)

### 2. Stato Attuale
- Programma SMS esistente (piattaforma, dimensione lista, tasso di opt-in, tasso di opt-out, ricavi/invio)
- Programma email (gli SMS funzionano meglio come livello aggiuntivo, non come sostituto)
- Tipo di numero di telefono: short code, toll-free, long code (10DLC)

### 3. Posizione di Compliance
- USA: registrazione A2P 10DLC completata? (Richiesta dal 2022 — senza, i tuoi messaggi vengono filtrati)
- Meccanismo di opt-in in uso? (Checkbox, opt-in via keyword, doppio opt-in)
- Privacy policy + termini includono le disclosure SMS?

### 4. Obiettivo
- Generare ricavi (promozionale, recupero carrello, post-acquisto)
- Generare attivazione (benvenuto, onboarding, nudge sui milestone)
- Transazionale (aggiornamenti ordine, codici di autenticazione, alert)

---

## Quando gli SMS Superano l'Email

Gli SMS non sono "un'altra email." Usali dove le proprietà del canale vincono:

| Caso d'Uso | SMS o Email? | Perché |
|----------|---------------|-----|
| Recupero carrello abbandonato | **SMS prima** | Tasso di apertura del 98% entro 3 min vs 20% per l'email in 24h |
| Aggiornamenti ordine/spedizione | **SMS** | I clienti lo vogliono subito, sul telefono |
| Flash sale / drop limitato | **SMS** | Canale dell'urgenza; lettura immediata |
| Codici di autenticazione / 2FA | **SMS** (o app) | Sensibile alla latenza, deve arrivare in pochi secondi |
| Serie di benvenuto | **Email primaria, SMS come livello** | L'email porta il contenuto long-form |
| Nurturing educativo | **Email** | Troppo testo per gli SMS, i costi si accumulano |
| Newsletter | **Email** | Canale sbagliato per gli SMS |
| Win-back clienti inattivi | **Entrambi** | SMS per la spinta forte, email per il dettaglio dell'offerta |
| Upsell post-acquisto | **SMS** | Tasso di apertura alto, cavalca lo slancio dell'acquisto |

**Regola generale**: Gli SMS si guadagnano il diritto di interrompere grazie all'opt-in. Usali per messaggi che beneficiano genuinamente dell'immediatezza. Se può aspettare 24 ore, inviarlo via email.

---

## Compliance — Leggi Prima

**La compliance è la base, non un ripensamento.** Una singola class-action TCPA costa $5M–$40M di transazione. Le basi:

### USA — TCPA (Telephone Consumer Protection Act)

1. **Consenso scritto espresso** richiesto per gli SMS marketing. Il consenso implicito non conta.
2. **Disclosure chiara all'opt-in** deve includere: nome del programma, aspettativa di frequenza ("fino a 4 msg/mese"), istruzioni STOP/HELP, "Possono essere applicate tariffe per messaggi e dati," link ai termini.
3. **Rispetta STOP/UNSUBSCRIBE entro pochi secondi**, ogni volta, senza eccezioni, su ogni variante di keyword (STOP, END, CANCEL, UNSUBSCRIBE, QUIT).
4. **Rispetta HELP** con una risposta contenente il nome del brand + informazioni STOP + contatto di supporto.
5. **Ore di silenzio**: nessun invio promozionale prima delle 8 del mattino o dopo le 21 nell'ora locale del destinatario. Le regole dei carrier e le leggi statali (es. Florida, Oklahoma, Washington) sono più restrittive di quelle federali — usa come default 9:00–20:00 ora locale del destinatario.
6. **Conserva i record del consenso scritto** con timestamp, fonte dell'opt-in e testo esatto della disclosure mostrata. Verificabile.

### USA — Registrazione A2P 10DLC (richiesta dal 2022)

I long code a 10 cifre Application-to-Person devono essere registrati tramite The Campaign Registry (TCR) via la tua piattaforma SMS. Senza registrazione:
- Il throughput viene limitato (o azzerato)
- I carrier filtrano i tuoi messaggi
- Vedrai lo stato "consegnato" ma i destinatari non li riceveranno

**La registrazione coperta**: verifica dell'identità del brand, caso d'uso della campagna (marketing, notifica account, OTP, ecc.), messaggi di esempio, meccanismo di opt-in, linguaggio di opt-out. Il testo dei messaggi di esempio dalla registrazione deve corrispondere a ciò che effettivamente invii.

### UE/UK — Consenso derivato dal GDPR

- Richiesto opt-in esplicito (nessuna casella pre-selezionata)
- Il diritto di revocare il consenso deve essere facile quanto darlo
- Le richieste di accesso ai dati personali si applicano anche ai record SMS
- La direttiva ePrivacy si sovrappone al GDPR

### Canada — CASL

- Consenso espresso + identificazione del mittente + unsubscribe in ogni messaggio
- Consenso implicito consentito per relazioni commerciali esistenti entro 24 mesi
- Penalità fino a CAD $10M per violazione

**Per dettagli completi sulla compliance, casi limite, template di copy per l'opt-in e template di risposta STOP/HELP**: vedi [references/compliance.md](references/compliance.md).

---

## Tipi di Numero di Telefono (USA)

| Tipo | Throughput | Costo | Caso d'Uso | Fiducia |
|------|-----------|------|----------|-------|
| **Short code (5-6 cifre)** | 100+ msg/sec | $500–$1.000/mese + setup | Marketing ad alto volume | Massima (verificato dai carrier) |
| **Toll-free (1-8XX)** | ~3 msg/sec | $10–$30/mese | Volume medio, supporto B2C | Medio-alta (verificato dai carrier) |
| **10DLC (long code regolare)** | 1–250 msg/sec | $2–$10/mese | PMI, conversazionale, transazionale | Media (richiede registrazione A2P 10DLC) |

**Regola generale**: lista <10K = 10DLC. Lista 10K–100K = toll-free. Lista 100K+ = short code.

---

## Principi Fondamentali

### 1. Ogni invio ha un costo reale
Gli SMS non sono gratuiti. A $0,0075–$0,04 per invio + commissioni dei carrier, un invio a 100K costa $750–$4.000. Questo impone la rilevanza — non puoi "bombardare" la lista. Segmenta in modo rigoroso.

### 2. L'opt-in è il tuo asset più prezioso
Il tasso di opt-in da email → SMS è tipicamente del 5–25%. Una lista SMS di alta qualità di 10K supera una lista di scarsa qualità di 100K. Ottimizza la qualità dell'opt-in, non il volume.

### 3. Ogni messaggio deve giustificarsi
Il destinatario ti ha dato il suo numero di telefono. Ogni invio dovrebbe superare il test: "sarei contento di aver ricevuto questo SMS?" Se no, non inviarlo.

### 4. Brevità + chiarezza
160 caratteri GSM-7 = 1 segmento SMS. 161+ caratteri = 2 segmenti (vieni fatturato per 2). Le emoji forzano la codifica UCS-2 (70 caratteri per segmento). Pianifica il conteggio dei segmenti.

### 5. Una CTA, un link
I link corti sono obbligatori (`klvy.co`, `txt.attn.tv`, dominio corto brandizzato). Traccia i parametri UTM su ogni link.

### 6. Identità del mittente, ogni invio
"Da [Brand]:" oppure short code brandizzato all'inizio di ogni messaggio. Anche sui flussi automatizzati. I destinatari non vedono l'indirizzo "da" — devono averlo inline.

---

## Tipi di Sequenza SMS

### Benvenuto / Conferma Opt-In (immediato)

Invio 1: Conferma + premio (immediato)
> Da Acme: Grazie per esserti unito! Ecco il 10% di sconto: ACME10. Usalo al checkout: acme.co/sale. Rispondi STOP per disiscriverti.

Invio 2 opzionale (24h dopo): Promemoria + vetrina dei best-seller

### Carrello Abbandonato (flusso a più alto ROI per l'ecommerce)

- Invio 1 (30 min dopo l'abbandono): "Hai dimenticato qualcosa? Il tuo carrello è ancora qui: [link corto]"
- Invio 2 (4 ore dopo): Urgenza leggera + social proof
- Invio 3 (24 ore dopo, opzionale): Offerta di sconto (solo se il margine lo consente)

**Nota**: Lo sconto sul primo messaggio abitua i clienti ad abbandonare. Riserva lo sconto per l'Invio 2 o 3.

### Abbandono Navigazione

- Invio 1 (1 ora dopo la navigazione): Prodotto + "Ci stai ancora pensando?" + link

### Post-Acquisto

- Invio 1 (immediato): Conferma ordine + ETA di consegna (transazionale, consenso separato OK)
- Invio 2 (dopo la consegna + 2 giorni): "Come ti sta piacendo [prodotto]?" + invito alla recensione + cross-sell

### Win-Back (clienti inattivi)

- Invio 1 (60–90 giorni dopo l'ultimo acquisto): "Ci manchi" + selezione curata
- Invio 2 (14 giorni dopo): Offerta di sconto
- Invio 3 (finale, 14 giorni dopo): Avviso di opt-out + ultima occasione

### Invii Promozionali / di Campagna

- Flash sale, drop, lanci, BFCM
- Massimo 1–2 invii per campagna
- Coordina con il calendario degli invii email per evitare il doppio contatto nello stesso giorno

### Transazionale (categoria di compliance separata)

- Aggiornamenti ordine, spedizione, consegna, codici di autenticazione, alert sull'account
- Generalmente OK senza consenso marketing separato se direttamente legato a una transazione iniziata dall'utente
- Soggetto comunque alla registrazione A2P 10DLC negli USA

**Per template di sequenza completi con copy e timing**: vedi [references/sequence-templates.md](references/sequence-templates.md).

---

## Linee Guida per il Copy SMS

### Struttura
1. **ID del mittente** ("Da Acme:" o short code del brand) — obbligatorio
2. **Hook** — le prime 5 parole decidono se continuano a leggere
3. **Valore** — cosa ci guadagnano, in modo specifico
4. **CTA + link corto** — un'unica azione, un unico URL
5. **Footer di compliance** — "Rispondi STOP per disiscriverti" (obbligatorio sulla conferma di opt-in e almeno trimestralmente dopo; raccomandato dai carrier su ogni messaggio promozionale)

### Lunghezza

- **160 caratteri (GSM-7)** = 1 segmento. Punta a questo.
- **70 caratteri (UCS-2)** se usi emoji, caratteri accentati o virgolette curve — pagherai più segmenti.
- **161–306 caratteri** = 2 segmenti (SMS concatenato). Accettabile per messaggi più ricchi, ma paghi il doppio per invio.
- **MMS** (immagine + fino a 1.600 caratteri) = 3–5 volte il costo dell'SMS. Usa con parsimonia per i momenti ad alto impatto.

### Tono di Voce

- Conversazionale, non corporate. Gli SMS sembrano personali — scrivi come se stessi scrivendo a un amico.
- Nessun oggetto, nessuna formattazione, nessun linguaggio da marketing.
- Le emoji vanno bene con moderazione (una per messaggio, a seconda della situazione).
- Il TUTTO MAIUSCOLO suona come urlare. Evitalo eccetto per codici espliciti (es. "Usa ACME10").

### Personalizzazione

- Token con il nome se disponibile (aumenta il CTR di circa il 20%)
- Basata sulla navigazione recente di prodotti/categorie
- Offerte basate sulla posizione (dove applicabile)
- Non simulare falsa intimità ("Ehi amico!") — si ritorce contro

**Per pattern di copy completi per tipo di sequenza con conteggio caratteri**: vedi [references/sequence-templates.md](references/sequence-templates.md).

---

## Selezione della Piattaforma

| Piattaforma | Migliore Per | MCP Nativo | Fascia di Costo |
|----------|----------|:---:|-----------|
| **Klaviyo SMS** | Ecommerce DTC già su Klaviyo email | ✓ | $$ |
| **Postscript** | Ecommerce Shopify DTC, integrazione profonda | - | $$ |
| **Attentive** | Ecommerce mid-market+, full-service | - | $$$ |
| **Twilio** | Build custom, transazionale, developer | - | $ (API raw) |
| **Brevo SMS** | Focus UE, combo email + SMS | ✓ | $ |
| **SimpleTexting** | PMI, esigenze semplici, facilità d'uso | - | $ |
| **Customer.io** | Automazione basata sul comportamento + SMS | - | $$ |

**Scelte rapide**:
- Già su Klaviyo per l'email + DTC/ecommerce → **Klaviyo SMS** (nessuna seconda piattaforma da imparare)
- Ecommerce Shopify, vuoi funzionalità SMS più approfondite → **Postscript**
- Costruire SMS custom in un prodotto → **Twilio**
- B2B SaaS che fa transazionale/autenticazione → **Twilio** o **Customer.io**

**Per approfondimenti sulle piattaforme (funzionalità, prezzi, percorsi di integrazione, registrazione A2P)**: vedi [references/platforms.md](references/platforms.md).

---

## Misurazione

### Metriche Chiave

| Metrica | Cosa Ti Dice | Range Salutare (ecommerce DTC) |
|--------|-------------------|--------------------------|
| **Tasso di opt-in** | Salute della parte alta del funnel | 5–25% degli iscritti email |
| **CTR** | Rilevanza del messaggio | 8–15% (vs ~3% email) |
| **Tasso di conversione (per invio)** | Impatto sui ricavi | 1–5% per invio promozionale |
| **Ricavo per invio (RPS)** | Economia del canale | $0,20–$2,00 |
| **Tasso di opt-out per invio** | Fatica del pubblico | <2% per invio, <0,5% per promozionale |
| **Costo per invio** | Disciplina del costo del canale | $0,0075–$0,04 |
| **Tasso di crescita della lista** | Slancio del pubblico | 5–15%/mese all'inizio, 1–3% a regime |

### Cosa Tracciare negli Analytics

- Tag UTM su ogni link: `utm_source=sms&utm_medium=sms&utm_campaign=[nome-campagna]`
- Attribuzione delle conversioni: sessioni guidate da SMS, ricavi a ultimo click, conversioni assistite
- Impatto sull'LTV: iscritti SMS vs iscritti solo email (tipicamente LTV 1,5–3× per gli opt-in SMS)

### Cosa Testare in A/B

- Orario di invio (pomeriggio vs sera, ora locale)
- Lunghezza del copy (SMS breve vs MMS con immagine)
- Importo e trigger dello sconto (immediato vs ritardato)
- Token di personalizzazione (con nome vs senza)
- Copy della CTA ("Acquista ora" vs "Guardalo" vs "Ultima occasione")

Fai riferimento alla skill **ab-testing** per il design corretto del test e a **analytics** per l'impostazione dell'attribuzione.

---

## Formato di Output

Quando l'utente chiede un piano SMS, restituisci:

1. **Controllo di compliance**: Sono registrati per A2P 10DLC (se USA)? Il meccanismo di opt-in è conforme? Segnala prima i blocchi.
2. **Strategia**: Quali flussi SMS costruire prima, classificati per ROI rispetto al loro modello di business.
3. **Design delle sequenze**: Per ogni flusso prioritario, specifica trigger, ritardo, copy con conteggio caratteri, CTA, segmentazione.
4. **Raccomandazione di piattaforma**: Basata su stack, dimensione lista e complessità.
5. **Piano di misurazione**: KPI, benchmark, coda di test A/B.
6. **Footer di compliance**: Disclosure obbligatorie, template di risposta STOP/HELP.

Mantieni le raccomandazioni specifiche. Non dire "invia un SMS al momento giusto" — dì "invia 30 min dopo l'abbandono del carrello, 4 ore dopo se non c'è stato acquisto, 24 ore dopo con sconto."

---

## Domande Specifiche per il Task

1. Sei negli USA, in UE, o entrambi? (Cambia completamente l'approccio di compliance.)
2. La registrazione A2P 10DLC è completata (USA)?
3. Su quale piattaforma sei o stai considerando?
4. Dimensione della lista email e tasso di opt-in SMS (se presente)?
5. Quali sequenze hai già attive?
6. Sei DTC ecommerce, app mobile, B2B SaaS, servizi?
7. Qual è l'obiettivo primario: ricavi, attivazione, retention o transazionale?

---

## Errori Comuni

1. **Saltare la registrazione A2P 10DLC** — i tuoi messaggi vengono filtrati nel nulla. Registra prima, invia dopo.
2. **Trattare gli SMS come l'email** — invio di blast promozionali giornalieri. I tassi di opt-out salgono, la lista muore.
3. **Sconto sul primo messaggio di carrello abbandonato** — abitua i clienti ad abbandonare sempre. Riservalo al secondo o terzo invio.
4. **"Da: [shortcode]" generico** — i destinatari hanno bisogno del nome del brand nel messaggio stesso.
5. **Dimenticare le ore di silenzio** — inviare alle 6 del mattino ora locale genera opt-out e reclami TCPA.
6. **Nessuna gestione di STOP/HELP** — non negoziabile. Ogni piattaforma lo gestisce; verifica che la tua lo faccia.
7. **Emoji ovunque** — ti spinge nella codifica UCS-2, dimezza la dimensione del segmento, raddoppia il costo.
8. **Disallineamento tra i messaggi di esempio A2P e gli invii reali** — i carrier segnalano e bloccano.
9. **Non tracciare le conversioni** — non puoi giustificare il ROI del canale senza attribuzione.
10. **Nessun throttling sugli invii bulk** — gli invii a raffica attivano il filtraggio dei carrier. Usa il throttling della piattaforma.

---

## Integrazioni degli Strumenti

Per l'implementazione, vedi il [registro degli strumenti](../../tools/REGISTRY.md). Strumenti SMS chiave:

| Strumento | Migliore Per | MCP | Guida |
|------|----------|:---:|-------|
| **Klaviyo** | Email + SMS e-commerce combinati | ✓ | [klaviyo.md](../../tools/integrations/klaviyo.md) |
| **Postscript** | SMS DTC Shopify, integrazione Shopify più profonda | - | [postscript.md](../../tools/integrations/postscript.md) |
| **Attentive** | SMS DTC mid-market+, full-service | - | [attentive.md](../../tools/integrations/attentive.md) |
| **Twilio** | API raw per build custom, transazionale, dev-first | - | [twilio.md](../../tools/integrations/twilio.md) |
| **Plivo** | Alternativa a Twilio, costo per invio più basso | - | [plivo.md](../../tools/integrations/plivo.md) |
| **AudienceTap** | DTC AI-forward, opt-in QR su confezione | - | [audiencetap.md](../../tools/integrations/audiencetap.md) |
| **Brevo** | Email + SMS UE, adatto alle PMI | ✓ | [brevo.md](../../tools/integrations/brevo.md) |
| **Customer.io** | Automazione SMS basata sul comportamento | - | [customer-io.md](../../tools/integrations/customer-io.md) |

---

## Skill Correlate

- **emails**: Canale gemello — quasi sempre eseguito insieme. L'email porta il contenuto long-form; gli SMS portano i nudge urgenti.
- **copywriting**: Per il copy SMS su larga scala e le pagine/email più lunghe a cui gli SMS rimandano.
- **popups**: Per i popup di raccolta numero di telefono sul sito.
- **churn-prevention**: Per i flussi di win-back che combinano SMS + email.
- **onboarding**: Per i nudge SMS sui milestone post-signup.
- **analytics**: Per l'attribuzione e la misurazione dell'RPS.
- **ab-testing**: Per il design di test specifici per gli SMS.
- **lead-magnets**: Per incentivare l'opt-in (l'offerta "10% di sconto per l'iscrizione").
