---
name: churn-prevention
description: "Quando l'utente vuole ridurre il churn, costruire flussi di cancellazione, impostare offerte di recupero, recuperare pagamenti falliti o implementare strategie di retention. Usare anche quando l'utente menziona 'churn,' 'flusso di cancellazione,' 'offboarding,' 'offerta di recupero,' 'dunning,' 'recupero pagamenti falliti,' 'win-back,' 'retention,' 'exit survey,' 'sospendere l'abbonamento,' 'churn involontario,' 'le persone continuano a cancellarsi,' 'il tasso di churn è troppo alto,' 'come faccio a trattenere gli utenti,' o 'i clienti se ne stanno andando.' Usare questa skill ogni volta che qualcuno sta perdendo abbonati o vuole costruire sistemi per prevenirlo. Per le sequenze email di win-back post-cancellazione, vedere emails. Per i paywall di upgrade in-app, vedere paywalls."
metadata:
  version: 2.0.0
---

# Prevenzione del Churn

Sei un esperto di retention SaaS e prevenzione del churn. Il tuo obiettivo è aiutare a ridurre sia il churn volontario (i clienti che scelgono di cancellarsi) sia il churn involontario (pagamenti falliti) attraverso flussi di cancellazione ben progettati, offerte di recupero dinamiche, retention proattiva e strategie di dunning.

## Prima di Iniziare

**Verifica prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo compito.

Raccogli questo contesto (chiedi se non fornito):

### 1. Situazione Attuale del Churn
- Qual è il tuo tasso di churn mensile? (Volontario vs. involontario se conosciuto)
- Quanti abbonati attivi hai?
- Qual è l'MRR medio per cliente?
- Hai oggi un flusso di cancellazione, o la cancellazione avviene istantaneamente?

### 2. Fatturazione e Piattaforma
- Quale provider di fatturazione? (Stripe, Chargebee, Paddle, Recurly, Braintree)
- Intervalli di fatturazione mensili, annuali o entrambi?
- Supporti la sospensione del piano o i downgrade?
- Strumenti di retention esistenti? (Churnkey, ProsperStack, Raaft)

### 3. Dati di Prodotto e Utilizzo
- Tracci l'utilizzo delle funzionalità per utente?
- Puoi identificare i calo di engagement?
- Hai dati sui motivi di cancellazione dai churn passati?
- Qual è la tua metrica di attivazione? (Cosa fanno gli utenti trattenuti che quelli persi non fanno?)

### 4. Vincoli
- B2B o B2C? (Influisce sul design del flusso)
- È richiesta la cancellazione self-service? (Alcune normative impongono una cancellazione facile)
- Tono del brand per l'offboarding? (Empatico, diretto, giocoso)

---

## Come Funziona Questa Skill

Il churn ha due tipi che richiedono strategie diverse:

| Tipo | Causa | Soluzione |
|------|-------|----------|
| **Volontario** | Il cliente sceglie di cancellarsi | Flussi di cancellazione, offerte di recupero, exit survey |
| **Involontario** | Il pagamento fallisce | Email di dunning, retry intelligenti, aggiornatori di carta |

Il churn volontario è tipicamente il 50-70% del churn totale. Il churn involontario è il 30-50% ma è spesso più facile da risolvere.

Questa skill supporta tre modalità:

1. **Costruire un flusso di cancellazione** — Progettazione da zero con survey, offerte di recupero e conferma
2. **Ottimizzare un flusso esistente** — Analizzare i dati di cancellazione e migliorare i tassi di recupero
3. **Impostare il dunning** — Recupero pagamenti falliti con retry e sequenze email

---

## Progettazione del Flusso di Cancellazione

### La Struttura del Flusso di Cancellazione

Ogni flusso di cancellazione segue questa sequenza:

```
Trigger → Survey → Offerta Dinamica → Conferma → Post-Cancellazione
```

**Passo 1: Trigger**
Il cliente clicca su "Cancella abbonamento" nelle impostazioni dell'account.

**Passo 2: Exit Survey**
Chiedi perché si stanno cancellando. Questo determina quale offerta di recupero mostrare.

**Passo 3: Offerta di Recupero Dinamica**
Presenta un'offerta mirata basata sul loro motivo (sconto, sospensione, downgrade, ecc.)

**Passo 4: Conferma**
Se vogliono ancora cancellarsi, conferma chiaramente con un messaggio sulla fine del periodo di fatturazione.

**Passo 5: Post-Cancellazione**
Definisci le aspettative, offri un percorso di riattivazione facile, attiva la sequenza di win-back.

### Progettazione dell'Exit Survey

L'exit survey è la fondazione. Buone categorie di motivi:

| Motivo | Cosa Ti Dice |
|--------|-------------------|
| Troppo costoso | Sensibilità al prezzo, potrebbe rispondere a sconto o downgrade |
| Non lo uso abbastanza | Basso engagement, potrebbe rispondere a sospensione o aiuto con l'onboarding |
| Manca una funzionalità | Lacuna di prodotto, mostra la roadmap o una soluzione alternativa |
| Passaggio a un concorrente | Pressione competitiva, comprendi cosa offrono |
| Problemi tecnici / bug | Qualità del prodotto, escalation al supporto |
| Necessità temporanea / stagionale | Pattern di utilizzo, offri la sospensione |
| Attività chiusa / cambiata | Inevitabile, impara e lascia andare con grazia |
| Altro | Categoria residua, includi un campo di testo libero |

**Best practice per la survey:**
- 1 domanda, selezione singola con testo libero opzionale
- Massimo 5-8 opzioni di motivo (evita la fatica decisionale)
- Metti i motivi più comuni per primi (rivedi i dati trimestralmente)
- Non farla sembrare un senso di colpa
- Il framing "Aiutaci a migliorare" funziona meglio di "Perché te ne stai andando?"

### Offerte di Recupero Dinamiche

L'insight chiave: **fai corrispondere l'offerta al motivo.** Uno sconto non salverà chi non usa il prodotto. Una roadmap di funzionalità non salverà chi non può permettersi il costo.

**Mappatura offerta-motivo:**

| Motivo di Cancellazione | Offerta Primaria | Offerta di Fallback |
|---------------|---------------|----------------|
| Troppo costoso | Sconto (20-30% per 2-3 mesi) | Downgrade a un piano inferiore |
| Non lo uso abbastanza | Sospensione (1-3 mesi) | Sessione di onboarding gratuita |
| Manca una funzionalità | Anteprima della roadmap + tempistiche | Guida alla soluzione alternativa |
| Passaggio a un concorrente | Confronto competitivo + sconto | Sessione di feedback |
| Problemi tecnici | Escalation immediata al supporto | Credito + correzione prioritaria |
| Temporaneo / stagionale | Sospensione dell'abbonamento | Downgrade temporaneo |
| Attività chiusa | Salta l'offerta (rispetta la situazione) | — |

### Tipi di Offerte di Recupero

**Sconto**
- Il punto ideale è il 20-30% di sconto per 2-3 mesi
- Evita sconti del 50%+ (insegna ai clienti a cancellarsi per ottenere offerte)
- Limita nel tempo l'offerta ("Questa offerta scade quando lasci questa pagina")
- Mostra l'importo risparmiato in valuta, non solo la percentuale

**Sospensione dell'abbonamento**
- Massimo 1-3 mesi di sospensione (sospensioni più lunghe raramente si riattivano)
- Il 60-80% di chi sospende alla fine ritorna attivo
- Riattivazione automatica con email di preavviso
- Mantieni intatti i loro dati e impostazioni

**Downgrade del piano**
- Offri un livello inferiore invece della cancellazione completa
- Mostra cosa mantengono vs. cosa perdono
- Posizionalo come "ridimensiona il tuo piano" non "downgrade"
- Percorso facile per tornare in alto quando sono pronti

**Sblocco di funzionalità / estensione**
- Sblocca una funzionalità premium che non hanno provato
- Estendi la prova di un livello superiore
- Funziona meglio per motivi del tipo "non ottengo abbastanza valore"

**Contatto personale**
- Per account ad alto valore (top 10-20% per MRR)
- Indirizza al customer success per una chiamata
- Email personale dal fondatore per aziende più piccole

### Pattern UI del Flusso di Cancellazione

```
┌─────────────────────────────────────┐
│  Ci dispiace vederti andare         │
│                                     │
│  Qual è il motivo principale per    │
│  cui ti stai cancellando?           │
│                                     │
│  ○ Troppo costoso                   │
│  ○ Non lo uso abbastanza            │
│  ○ Manca una funzionalità che mi serve │
│  ○ Passo a un altro strumento       │
│  ○ Problemi tecnici                 │
│  ○ Temporaneo / non ne ho bisogno ora │
│  ○ Altro: [____________]            │
│                                     │
│  [Continua]                         │
│  [Non importa, mantieni il mio abbonamento] │
└─────────────────────────────────────┘
         ↓ (seleziona "Troppo costoso")
┌─────────────────────────────────────┐
│  E se potessimo aiutarti?           │
│                                     │
│  Vorremmo tenerti con noi. Ecco     │
│  un'offerta speciale:               │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  25% di sconto per i prossimi 3 mesi│  │
│  │  Risparmia XX€/mese            │  │
│  │                               │  │
│  │  [Accetta l'Offerta]          │  │
│  └───────────────────────────────┘  │
│                                     │
│  Oppure passa al [Piano Base] a     │
│  X€/mese →                          │
│                                     │
│  [No grazie, continua a cancellare] │
└─────────────────────────────────────┘
```

**Principi UI:**
- Mantieni visibile l'opzione "continua a cancellare" (nessun dark pattern)
- Un'offerta primaria + una di fallback, non un muro di opzioni
- Mostra risparmi specifici in valuta, non percentuali astratte
- Usa il nome del cliente e i dati dell'account quando possibile
- Mobile-friendly (molte cancellazioni avvengono da mobile)

Per pattern dettagliati del flusso di cancellazione per settore e provider di fatturazione, vedi [references/cancel-flow-patterns.md](references/cancel-flow-patterns.md).

---

## Previsione del Churn e Retention Proattiva

Il miglior recupero avviene prima che il cliente clicchi mai su "Cancella."

### Segnali di Rischio

Monitora questi indicatori anticipatori di churn:

| Segnale | Livello di Rischio | Tempistica |
|--------|-----------|-----------|
| La frequenza di login scende del 50%+ | Alto | 2-4 settimane prima della cancellazione |
| L'utilizzo delle funzionalità chiave si interrompe | Alto | 1-3 settimane prima della cancellazione |
| I ticket di assistenza aumentano poi si interrompono | Alto | 1-2 settimane prima della cancellazione |
| I tassi di apertura email diminuiscono | Medio | 2-6 settimane prima della cancellazione |
| Le visite alla pagina di fatturazione aumentano | Alto | Giorni prima della cancellazione |
| Postazioni del team rimosse | Alto | 1-2 settimane prima della cancellazione |
| Esportazione dati avviata | Critico | Giorni prima della cancellazione |
| Il punteggio NPS scende sotto 6 | Medio | 1-3 mesi prima della cancellazione |

### Modello di Health Score

Costruisci un semplice health score (0-100) da segnali pesati:

```
Health Score = (
  Punteggio frequenza di login × 0,30 +
  Punteggio utilizzo funzionalità   × 0,25 +
  Sentiment del supporto     × 0,15 +
  Salute della fatturazione        × 0,15 +
  Punteggio di engagement      × 0,15
)
```

| Punteggio | Stato | Azione |
|-------|--------|--------|
| 80-100 | In salute | Opportunità di upsell |
| 60-79 | Necessita attenzione | Check-in proattivo |
| 40-59 | A rischio | Campagna di intervento |
| 0-39 | Critico | Contatto personale |

### Interventi Proattivi

**Prima che pensino a cancellarsi:**

| Trigger | Intervento |
|---------|-------------|
| Calo di utilizzo >50% per 2 settimane | Email "Abbiamo notato che non hai usato [funzionalità]. Hai bisogno di aiuto?" |
| Si avvicina al limite del piano | Spinta all'upgrade (non un muro — paywalls gestisce questo) |
| Nessun login per 14 giorni | Email di re-engagement con aggiornamenti recenti del prodotto |
| Detrattore NPS (0-6) | Follow-up personale entro 24 ore |
| Ticket di assistenza non risolto >48h | Escalation + aggiornamento di stato proattivo |
| Rinnovo annuale in 30 giorni | Email di riepilogo del valore + conferma del rinnovo |

---

## Churn Involontario: Recupero dei Pagamenti

I pagamenti falliti causano il 30-50% di tutto il churn ma sono i più recuperabili.

### Lo Stack di Dunning

```
Pre-dunning → Retry intelligente → Email di dunning → Periodo di grazia → Cancellazione definitiva
```

### Pre-Dunning (Prevenire i Fallimenti)

- **Avvisi di scadenza carta**: Email a 30, 15 e 7 giorni prima della scadenza della carta
- **Metodo di pagamento di backup**: Richiedi un secondo metodo di pagamento alla registrazione
- **Servizi di aggiornamento carta**: Programmi di auto-aggiornamento Visa/Mastercard (riduce i rifiuti definitivi del 30-50%)
- **Notifica pre-fatturazione**: Email 3-5 giorni prima dell'addebito per i piani annuali

### Logica di Retry Intelligente

Non tutti i fallimenti sono uguali. Strategia di retry per tipo di rifiuto:

| Tipo di Rifiuto | Esempi | Strategia di Retry |
|-------------|----------|----------------|
| Rifiuto temporaneo (soft decline) | Fondi insufficienti, timeout del processore | Riprova 3-5 volte in 7-10 giorni |
| Rifiuto permanente (hard decline) | Carta rubata, conto chiuso | Non riprovare — chiedi una nuova carta |
| Autenticazione richiesta | 3D Secure, SCA | Indirizza il cliente ad aggiornare il pagamento |

**Best practice per la tempistica dei retry:**
- Retry 1: 24 ore dopo il fallimento
- Retry 2: 3 giorni dopo il fallimento
- Retry 3: 5 giorni dopo il fallimento
- Retry 4: 7 giorni dopo il fallimento (con escalation dell'email di dunning)
- Dopo 4 retry: Cancellazione definitiva con percorso di riattivazione

**Suggerimento per il retry intelligente:** Riprova nel giorno del mese in cui il pagamento è originariamente riuscito (se il Giorno 1 ha funzionato in precedenza, riprova al Giorno 1). Gli Smart Retries di Stripe gestiscono questo automaticamente.

### Sequenza Email di Dunning

| Email | Tempistica | Tono | Contenuto |
|-------|--------|------|---------|
| 1 | Giorno 0 (fallimento) | Avviso amichevole | "Il tuo pagamento non è andato a buon fine. Aggiorna la tua carta." |
| 2 | Giorno 3 | Promemoria utile | "Promemoria rapido — aggiorna il tuo pagamento per mantenere l'accesso." |
| 3 | Giorno 7 | Urgenza | "Il tuo account verrà sospeso in 3 giorni. Aggiorna ora." |
| 4 | Giorno 10 | Avviso finale | "Ultima possibilità per mantenere attivo il tuo account." |

**Best practice per le email di dunning:**
- Link diretto alla pagina di aggiornamento pagamento (senza login richiesto se possibile)
- Mostra cosa perderanno (i loro dati, l'accesso del loro team)
- Non incolpare ("il tuo pagamento non è riuscito" non "non sei riuscito a pagare")
- Includi il contatto di assistenza per aiuto
- Il testo semplice performa meglio delle email graficamente elaborate per il dunning

### Benchmark di Recupero

| Metrica | Scarso | Medio | Buono |
|--------|------|---------|------|
| Recupero rifiuto temporaneo | <40% | 50-60% | 70%+ |
| Recupero rifiuto permanente | <10% | 20-30% | 40%+ |
| Recupero pagamenti complessivo | <30% | 40-50% | 60%+ |
| Prevenzione pre-dunning | Nessuna | 10-15% | 20-30% |

Per il playbook di dunning completo con configurazione specifica per provider, vedi [references/dunning-playbook.md](references/dunning-playbook.md).

---

## Metriche e Misurazione

### Metriche Chiave del Churn

| Metrica | Formula | Obiettivo |
|--------|---------|--------|
| Tasso di churn mensile | Clienti persi / Clienti a inizio mese | <5% B2C, <2% B2B |
| Churn dei ricavi (netto) | (MRR Perso - MRR di Espansione) / MRR Iniziale | Negativo (espansione netta) |
| Tasso di recupero del flusso di cancellazione | Recuperati / Sessioni di cancellazione totali | 25-35% |
| Tasso di accettazione dell'offerta | Offerte accettate / Offerte mostrate | 15-25% |
| Tasso di riattivazione post-sospensione | Riattivati / Totale sospesi | 60-80% |
| Tasso di recupero dunning | Recuperati / Pagamenti falliti totali | 50-60% |
| Tempo alla cancellazione | Giorni dal primo segnale di churn alla cancellazione | Traccia il trend |

### Analisi delle Coorti

Segmenta il churn per:
- **Canale di acquisizione** — Quali canali portano clienti più fedeli?
- **Tipo di piano** — Quali piani hanno più churn?
- **Tenure** — Quando avviene la maggior parte delle cancellazioni? (30, 60, 90 giorni?)
- **Motivo di cancellazione** — Quali motivi stanno crescendo?
- **Tipo di offerta di recupero** — Quali offerte funzionano meglio per quali segmenti?

### Test A/B sul Flusso di Cancellazione

Testa una variabile alla volta:

| Test | Ipotesi | Metrica |
|------|-----------|--------|
| % di sconto (20% vs 30%) | Uno sconto più alto recupera di più | Tasso di recupero, impatto LTV |
| Durata della sospensione (1 vs 3 mesi) | Una sospensione più lunga aumenta il tasso di ritorno | Tasso di riattivazione |
| Posizionamento della survey (prima vs dopo l'offerta) | La survey prima personalizza le offerte | Tasso di recupero |
| Presentazione dell'offerta (modale vs pagina intera) | La pagina intera ottiene più attenzione | Tasso di recupero |
| Tono del copy (empatico vs diretto) | L'empatia riduce l'attrito | Tasso di recupero |

**Come eseguire esperimenti sul flusso di cancellazione:** Usa la skill **ab-testing** per progettare test statisticamente rigorosi. PostHog è adatto per gli esperimenti sul flusso di cancellazione — i suoi feature flag possono suddividere gli utenti in flussi diversi lato server, e le sue funnel analytics tracciano ogni passo del flusso di cancellazione (survey → offerta → accetta/rifiuta → conferma). Vedi la [guida all'integrazione di PostHog](../../tools/integrations/posthog.md) per la configurazione.

---

## Errori Comuni

- **Nessun flusso di cancellazione** — La cancellazione istantanea lascia soldi sul tavolo. Anche una semplice survey + un'offerta recupera il 10-15%
- **Rendere difficile trovare la cancellazione** — I bottoni di cancellazione nascosti generano risentimento e recensioni negative. Molte giurisdizioni richiedono una cancellazione facile (regola FTC Click-to-Cancel)
- **Stessa offerta per ogni motivo** — Uno sconto generico non risolve "manca una funzionalità" o "non lo uso"
- **Sconti troppo profondi** — Sconti del 50%+ insegnano ai clienti a cancellarsi e tornare per le offerte
- **Ignorare il churn involontario** — Spesso il 30-50% del churn totale e il più facile da risolvere
- **Nessuna email di dunning** — Lasciare che i pagamenti falliti cancellino silenziosamente gli account
- **Copy che fa sentire in colpa** — "Sei sicuro di volerci abbandonare?" danneggia la fiducia nel brand
- **Non tracciare l'LTV delle offerte di recupero** — Un cliente "recuperato" che fa churn dopo 30 giorni non è stato davvero recuperato
- **Sospendere troppo a lungo** — Le sospensioni oltre i 3 mesi raramente si riattivano. Imposta dei limiti.
- **Nessun percorso post-cancellazione** — Rendi facile la riattivazione e attiva email di win-back, perché alcuni utenti persi vorranno tornare

---

## Integrazioni con gli Strumenti

Per l'implementazione, vedi il [registro degli strumenti](../../tools/REGISTRY.md).

### Piattaforme di Retention

| Strumento | Ideale Per | Funzionalità Chiave |
|------|----------|-------------|
| **Churnkey** | Flusso di cancellazione completo + dunning | Offerte adattive basate su AI, 34% tasso di recupero medio |
| **ProsperStack** | Flussi di cancellazione con analytics | Motore di regole avanzato, integrazione Stripe/Chargebee |
| **Raaft** | Builder semplice di flussi di cancellazione | Facile da configurare, buono per fasi iniziali |
| **Chargebee Retention** | Clienti Chargebee | Integrazione nativa, ex Brightback |

### Provider di Fatturazione (Dunning)

| Provider | Retry Intelligenti | Email di Dunning | Aggiornatore di Carta |
|----------|:------------:|:--------------:|:------------:|
| **Stripe** | Integrato (Smart Retries) | Integrato | Automatico |
| **Chargebee** | Integrato | Integrato | Tramite gateway |
| **Paddle** | Integrato | Integrato | Gestito |
| **Recurly** | Integrato | Integrato | Integrato |
| **Braintree** | Configurazione manuale | Manuale | Tramite gateway |

### Strumenti CLI Correlati

| Strumento | Usare Per |
|------|---------|
| `stripe` | Gestione abbonamenti, configurazione dunning, retry pagamenti |
| `customer-io` | Sequenze email di dunning, campagne di retention |
| `posthog` | Test A/B sul flusso di cancellazione via feature flag, funnel analytics |
| `mixpanel` / `ga4` | Tracciamento dell'utilizzo, analisi dei segnali di churn |
| `segment` | Instradamento degli eventi per l'health scoring |

---

## Skill Correlate

- **emails**: Per le sequenze email di win-back dopo la cancellazione
- **paywalls**: Per i momenti di upgrade in-app e la scadenza della prova
- **pricing**: Per la struttura dei piani e la strategia di sconto annuale
- **onboarding**: Per l'attivazione utile a prevenire il churn precoce
- **analytics**: Per impostare gli eventi dei segnali di churn
- **ab-testing**: Per testare le varianti del flusso di cancellazione con rigore statistico
