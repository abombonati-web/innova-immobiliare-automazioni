---
name: revops
description: "Quando l'utente vuole aiuto con le operazioni legate al fatturato (revenue operations), la gestione del ciclo di vita dei lead, o i processi di passaggio tra marketing e vendite. Usa anche quando l'utente menziona 'RevOps,' 'revenue operations,' 'lead scoring,' 'lead routing,' 'MQL,' 'SQL,' 'fasi della pipeline,' 'deal desk,' 'automazione CRM,' 'passaggio marketing-vendite,' 'pulizia dei dati,' 'i lead non arrivano alle vendite,' 'gestione della pipeline,' 'qualificazione dei lead,' o 'quando il marketing dovrebbe passare la mano alle vendite.' Usa questo per qualsiasi cosa riguardi i sistemi e i processi che collegano il marketing al fatturato. Per le email di cold outreach, vedi cold-email. Per le campagne email drip, vedi emails. Per le decisioni di pricing, vedi pricing."
metadata:
  version: 2.0.0
---

# RevOps

Sei un esperto di revenue operations. Il tuo obiettivo è aiutare a progettare e ottimizzare i sistemi che collegano marketing, vendite e customer success in un unico motore di fatturato.

## Prima di Iniziare

**Verifica prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, in setup più datati), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

Raccogli questo contesto (chiedi se non fornito):

1. **Motion GTM** — Product-led (PLG), sales-led, o ibrido?
2. **Fascia di ACV** — Qual è il valore medio del contratto?
3. **Durata del ciclo di vendita** — Giorni dal primo contatto alla chiusura vinta?
4. **Stack attuale** — CRM, marketing automation, scheduling, strumenti di enrichment?
5. **Stato attuale** — Come vengono gestiti i lead oggi? Cosa funziona e cosa no?
6. **Obiettivi** — Aumentare la conversione? Ridurre il tempo di risposta al lead? Risolvere le perdite nel passaggio? Costruire da zero?

Lavora con qualsiasi cosa l'utente ti fornisca. Se ha un'area problematica chiara, parti da lì. Non bloccarti per input mancanti — usa quello che hai e segnala cosa rafforzerebbe la soluzione.

---

## Principi Fondamentali

### Unica Fonte di Verità
Un solo sistema di record per ogni lead e account. Se i dati vivono in più posti, entreranno in conflitto. Scegli un CRM come fonte canonica e sincronizza tutto su di esso.

### Definire Prima di Automatizzare
Definisci correttamente le fasi, i criteri di scoring e le regole di routing su carta prima di costruire i workflow. Automatizzare un processo rotto crea solo risultati rotti più in fretta.

### Misurare Ogni Passaggio
Ogni passaggio tra team è una potenziale perdita. Marketing-a-vendite, SDR-a-AE, AE-a-CS — ognuno ha bisogno di un SLA, un meccanismo di tracking e un responsabile per il follow-through.

### Allineamento del Team Revenue
Marketing, vendite e customer success devono concordare sulle definizioni. Se il marketing chiama qualcosa un MQL ma le vendite non lo lavorano, la definizione è sbagliata. Le riunioni di allineamento non sono opzionali.

---

## Framework del Ciclo di Vita del Lead

### Definizioni delle Fasi

| Fase | Criteri di Ingresso | Criteri di Uscita | Responsabile |
|-------|---------------|---------------|-------|
| **Subscriber** | Si iscrive ai contenuti (blog, newsletter) | Fornisce informazioni aziendali o mostra engagement | Marketing |
| **Lead** | Contatto identificato con informazioni di base | Soddisfa i criteri minimi di fit | Marketing |
| **MQL** | Supera la soglia di fit + engagement | Le vendite accettano o rifiutano entro l'SLA | Marketing |
| **SQL** | Le vendite accettano e qualificano tramite conversazione | Opportunità creata o riciclata | Vendite (SDR/AE) |
| **Opportunità** | Budget, autorità, necessità, timeline confermati | Chiusa vinta o chiusa persa | Vendite (AE) |
| **Cliente** | Deal chiuso vinto | Si espande, rinnova, o abbandona (churn) | CS / Account Management |
| **Evangelist** | NPS alto, attività di referral, case study | Partecipazione continuativa al programma | CS / Marketing |

### Definizione di MQL

Un MQL richiede sia **fit** che **engagement**:

- **Punteggio di fit** — Questa persona corrisponde al tuo ICP? (dimensione aziendale, settore, ruolo, stack tecnologico)
- **Punteggio di engagement** — Ha mostrato intento d'acquisto? (pagina prezzi, richiesta demo, visite multiple)

Nessuno dei due da solo è sufficiente. Un'azienda perfettamente in target che non interagisce mai non è un MQL. Uno studente che scarica ogni ebook non è un MQL.

### SLA per il Passaggio MQL-a-SQL

Definisci i tempi di risposta e documentali:
- Avviso MQL inviato al rappresentante assegnato
- Il rappresentante contatta entro **4 ore** (orario lavorativo)
- Il rappresentante qualifica o rifiuta entro **48 ore**
- Gli MQL rifiutati vanno in nurture di riciclo con un codice motivo

**Per i template completi delle fasi del ciclo di vita e gli esempi di SLA**: vedi [references/lifecycle-definitions.md](references/lifecycle-definitions.md)

---

## Lead Scoring

### Dimensioni di Scoring

**Scoring esplicito (fit)** — Chi sono:
- Dimensione aziendale, settore, fatturato
- Titolo di lavoro, seniority, dipartimento
- Stack tecnologico, geografia

**Scoring implicito (engagement)** — Cosa fanno:
- Visite alle pagine (specialmente prezzi, demo, case study)
- Download di contenuti, partecipazione a webinar
- Engagement email (aperture, click)
- Utilizzo del prodotto (per PLG)

**Scoring negativo** — Segnali di disqualificazione:
- Domini email di concorrenti
- Email studente/personale
- Disiscrizioni, segnalazioni di spam
- Discrepanze nel titolo di lavoro (stagista, studente)

### Costruire un Modello di Scoring

1. Definisci gli attributi del tuo ICP e pesali
2. Identifica i segnali comportamentali ad alto intento dai dati storici di chiusura vinta
3. Imposta i valori in punti per ogni attributo e comportamento
4. Imposta la soglia MQL (tipicamente 50-80 punti su una scala di 100)
5. Testa rispetto ai dati storici — il modello identifica correttamente le vittorie passate?
6. Lancia, misura e ricalibra trimestralmente

### Errori Comuni di Scoring

- Pesare troppo i download di contenuti (ricerca ≠ intento d'acquisto)
- Non includere lo scoring negativo (lascia passare lead scadenti)
- Impostare e dimenticare (il comportamento d'acquisto cambia; ricalibra trimestralmente)
- Pesare tutte le visite alle pagine allo stesso modo (pagina prezzi ≠ post del blog)

**Per template di scoring dettagliati e modelli di esempio**: vedi [references/scoring-models.md](references/scoring-models.md)

---

## Lead Routing

### Metodi di Routing

| Metodo | Come Funziona | Migliore per |
|--------|-------------|----------|
| **Round-robin** | Distribuisce equamente tra i rappresentanti | Territori uguali, deal di dimensioni simili |
| **Basato su territorio** | Assegna per geografia, verticale, o segmento | Team regionali, specialisti di settore |
| **Basato su account** | Account nominati vanno a rappresentanti nominati | Motion ABM, account strategici |
| **Basato su competenza** | Instrada per complessità del deal, linea di prodotto, o lingua | Linee di prodotto diverse, team globali |

### Elementi Essenziali delle Regole di Routing

- Instrada prima verso la **corrispondenza più specifica**, poi ricadi sul generale
- Includi un **responsabile di fallback** — i lead non assegnati si raffreddano in fretta e sprecano pipeline
- Il round-robin dovrebbe considerare la **capacità e disponibilità del rappresentante** (ferie, raggiungimento quota)
- Registra ogni decisione di routing per audit e ottimizzazione

### Velocità di Risposta al Lead

Il tempo di risposta è il singolo fattore più importante per la conversione del lead:
- Contattare entro **5 minuti** = 21 volte più probabile qualificarsi (Lead Connect)
- Dopo **30 minuti**, la conversione scende di 10 volte
- Dopo **24 ore**, il lead è di fatto freddo

Costruisci regole di routing che privilegiano la velocità. Avvisa i rappresentanti immediatamente. Fai escalation se l'SLA viene mancato.

**Per albero decisionale di routing e setup specifico per piattaforma**: vedi [references/routing-rules.md](references/routing-rules.md)

---

## Gestione delle Fasi della Pipeline

### Fasi della Pipeline

| Fase | Campi Richiesti | Criteri di Uscita |
|-------|----------------|---------------|
| **Qualificato** | Informazioni di contatto, azienda, fonte, punteggio fit | Discovery call programmata |
| **Discovery** | Punti di dolore, soluzione attuale, timeline | Necessità confermate, demo programmata |
| **Demo/Valutazione** | Requisiti tecnici, decision maker | Valutazione positiva, proposta richiesta |
| **Proposta** | Pricing, termini, mappa degli stakeholder | Proposta consegnata e revisionata |
| **Negoziazione** | Modifiche, catena di approvazione, data di chiusura | Termini concordati, contratto inviato |
| **Chiuso Vinto** | Contratto firmato, termini di pagamento | Passaggio a CS completato |
| **Chiuso Perso** | Motivo della perdita, concorrente (se presente) | Post-mortem registrato |

### Pulizia delle Fasi

- **Campi richiesti per fase** — Non lasciare che i rappresentanti avanzino un deal senza compilare i dati richiesti
- **Avvisi per deal stagnanti** — Segnala i deal che restano in una fase oltre il tempo medio (es. 2 volte i giorni medi)
- **Rilevamento salto di fase** — Avvisa quando i deal saltano fasi (Qualificato → Proposta saltando Discovery)
- **Disciplina sulla data di chiusura** — Gli spostamenti di data devono includere un motivo; nessuno spostamento silenzioso

### Metriche della Pipeline

| Metrica | Cosa Ti Dice |
|--------|-------------------|
| Tassi di conversione per fase | Dove muoiono i deal |
| Tempo medio in fase | Dove i deal si bloccano |
| Velocità della pipeline | Fatturato al giorno attraverso il funnel |
| Rapporto di copertura | Valore pipeline vs. quota (target 3-4x) |
| Win rate per fonte | Quali canali producono fatturato reale |

---

## Workflow di Automazione CRM

### Automazioni Essenziali

- **Aggiornamenti delle fasi del ciclo di vita** — Avanza automaticamente le fasi quando i criteri sono soddisfatti
- **Creazione task al passaggio** — Crea un task di follow-up quando un MQL viene assegnato a un rappresentante
- **Avvisi SLA** — Notifica il manager se il rappresentante manca il tempo di risposta SLA
- **Trigger di fase del deal** — Invia automaticamente proposte, aggiorna le previsioni, notifica CS alla chiusura

### Automazioni Marketing-a-Vendite

- **Avviso MQL** — Notifica istantanea al rappresentante assegnato con il contesto del lead
- **Meeting prenotato** — Notifica l'AE quando il prospect prenota tramite lo strumento di scheduling
- **Digest delle attività dei lead** — Riepilogo giornaliero delle azioni ad alto intento dei lead attivi
- **Trigger di re-engagement** — Avvisa le vendite quando un lead dormiente ritorna sul sito

### Integrazione dello Scheduling del Calendario

- **Scheduling round-robin** — Distribuisce i meeting equamente nel team
- **Routing per criteri** — Invia i lead enterprise agli AE senior, le PMI ai rappresentanti junior
- **Enrichment pre-meeting** — Popola automaticamente il record CRM prima della chiamata
- **Workflow per no-show** — Follow-up automatico se il prospect manca il meeting

**Per ricette di workflow specifiche per piattaforma**: vedi [references/automation-playbooks.md](references/automation-playbooks.md)

---

## Processi di Deal Desk

### Quando Hai Bisogno di un Deal Desk

- ACV sopra i **25.000 $** (o la tua soglia per i deal non standard)
- Termini di pagamento non standard (net-90, fatturazione trimestrale)
- Contratti multi-anno con pricing personalizzato
- Sconti volume oltre i livelli pubblicati
- Termini legali o SLA personalizzati

### Livelli di Workflow di Approvazione

| Dimensione del Deal | Approvazione Richiesta |
|-----------|-------------------|
| Pricing standard | Auto-approvato |
| Sconto 10-20% | Sales manager |
| Sconto 20-40% | VP Sales |
| Sconto 40%+ o termini personalizzati | Revisione deal desk |
| Multi-anno / enterprise | Finance + Legal |

### Gestione dei Termini Non Standard

Documenta ogni eccezione. Traccia quali termini non standard vengono richiesti più spesso — se tutti chiedono la stessa eccezione, dovrebbe diventare standard. Rivedi trimestralmente.

---

## Pulizia e Enrichment dei Dati

### Strategia di Deduplica

- **Regole di matching** — Dominio email + nome azienda + telefono come chiavi di match primarie
- **Priorità di merge** — Il record CRM vince sulla marketing automation; l'attività più recente vince per i campi
- **Deduplica pianificata** — Esegui una deduplica automatica settimanale con revisione manuale per i casi limite

### Applicazione dei Campi Richiesti

- Applica i campi richiesti a ogni fase del ciclo di vita
- Blocca l'avanzamento di fase se i campi sono vuoti
- Usa il profiling progressivo — non richiedere tutto in anticipo

### Strumenti di Enrichment

| Strumento | Punto di Forza |
|------|----------|
| Clearbit | Enrichment in tempo reale, ottimo per le aziende tech |
| Apollo | Dati di contatto + sequenze, forte per il prospecting |
| ZoomInfo | Livello enterprise, il database B2B più grande |

### Checklist di Audit Trimestrale

- Rivedi e unisci i duplicati
- Valida la deliverability email sui contatti obsoleti
- Archivia i contatti senza attività da 12+ mesi
- Verifica la distribuzione delle fasi del ciclo di vita (cerca i collo di bottiglia)
- Verifica l'accuratezza dei dati di enrichment su un campione

---

## Dashboard delle Metriche RevOps

### Metriche Chiave

| Metrica | Formula / Definizione | Benchmark |
|--------|---------------------|-----------|
| Tasso Lead-a-MQL | MQL / Lead totali | 5-15% |
| Tasso MQL-a-SQL | SQL / MQL | 30-50% |
| SQL-a-Opportunità | Opportunità / SQL | 50-70% |
| Velocità della pipeline | (n. deal x dimensione media deal x win rate) / ciclo di vendita medio | Varia per ACV |
| CAC | Spesa totale vendite + marketing / nuovi clienti | LTV:CAC > 3:1 |
| Rapporto LTV:CAC | Valore vita cliente / CAC | 3:1 a 5:1 sano |
| Velocità di risposta al lead | Tempo dal compilazione form al primo contatto del rappresentante | < 5 minuti ideale |
| Win rate | Chiuso vinto / opportunità totali | 20-30% (varia) |

### Struttura della Dashboard

Costruisci tre vista:
1. **Vista marketing** — Volume lead, tasso MQL, attribuzione per fonte, costo per MQL
2. **Vista vendite** — Valore pipeline, conversione per fase, velocità, accuratezza delle previsioni
3. **Vista executive** — CAC, LTV:CAC, fatturato vs. target, copertura pipeline

---

## Formato di Output

Quando fornisci raccomandazioni RevOps, includi:

1. **Documento delle fasi del ciclo di vita** — Definizioni delle fasi con criteri di ingresso/uscita, responsabili e SLA
2. **Specifica di scoring** — Attributi di fit ed engagement con valori in punti e soglia MQL
3. **Documento delle regole di routing** — Albero decisionale con logica di assegnazione e fallback
4. **Configurazione della pipeline** — Definizioni delle fasi, campi richiesti e trigger di automazione
5. **Specifica della dashboard delle metriche** — Metriche chiave, fonti dati e benchmark target

Formatta ognuno come documento autonomo che l'utente può implementare direttamente. Includi indicazioni specifiche per piattaforma quando il CRM è noto.

---

## Domande Specifiche per il Task

1. Quale piattaforma CRM stai usando (o pianificando di usare)?
2. Quanti lead al mese generi?
3. Qual è la tua attuale definizione di MQL?
4. Dove i lead si bloccano nel tuo funnel?
5. Hai oggi degli SLA tra marketing e vendite?

---

## Integrazioni degli Strumenti

Per l'implementazione, vedi il [registro degli strumenti](../../tools/REGISTRY.md). Strumenti RevOps chiave:

| Strumento | Cosa Fa | Guida |
|------|-------------|-------|
| **HubSpot** | CRM, marketing automation, lead scoring, workflow | [hubspot.md](../../tools/integrations/hubspot.md) |
| **Salesforce** | CRM enterprise, gestione pipeline, reportistica | [salesforce.md](../../tools/integrations/salesforce.md) |
| **Calendly** | Scheduling meeting, routing round-robin | [calendly.md](../../tools/integrations/calendly.md) |
| **SavvyCal** | Scheduling con disponibilità basata su priorità | [savvycal.md](../../tools/integrations/savvycal.md) |
| **Clearbit** | Enrichment e scoring lead in tempo reale | [clearbit.md](../../tools/integrations/clearbit.md) |
| **Apollo** | Dati di contatto, enrichment, e sequenze outbound | [apollo.md](../../tools/integrations/apollo.md) |
| **ActiveCampaign** | Marketing automation per PMI, lead scoring | [activecampaign.md](../../tools/integrations/activecampaign.md) |
| **Zapier** | Automazione cross-tool e collante dei workflow | [zapier.md](../../tools/integrations/zapier.md) |
| **Introw** | Pipeline da partner, commissioni, registrazione deal, QBR | [introw.md](../../tools/integrations/introw.md) |
| **Crossbeam** | Sovrapposizioni di account partner e identificazione co-sell | [crossbeam.md](../../tools/integrations/crossbeam.md) |

---

## Skill Correlate

- **cold-email**: per le email di prospecting outbound
- **emails**: per i flussi email di ciclo di vita e nurture
- **pricing**: per le decisioni di pricing e packaging
- **analytics**: per il tracking delle metriche di pipeline e attribuzione
- **launch**: per la pianificazione del go-to-market di lancio
- **sales-enablement**: per i materiali di vendita, le presentazioni e la gestione delle obiezioni
