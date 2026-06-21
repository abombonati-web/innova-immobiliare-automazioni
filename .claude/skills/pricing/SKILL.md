---
name: pricing
description: "Quando l'utente vuole aiuto con decisioni di pricing, packaging, o strategia di monetizzazione. Da usare anche quando l'utente menziona 'pricing,' 'livelli di prezzo,' 'freemium,' 'prova gratuita,' 'packaging,' 'aumento di prezzo,' 'value metric,' 'Van Westendorp,' 'disponibilità a pagare,' 'monetizzazione,' 'quanto dovrei far pagare,' 'il mio pricing è sbagliato,' 'pagina prezzi,' 'annuale vs mensile,' 'pricing per posto,' o 'dovrei offrire un piano gratuito.' Usa questa skill ogni volta che qualcuno sta definendo quanto far pagare o come strutturare i propri piani. Per le schermate di upgrade in-app, vedi paywalls. Per la costruzione dell'offerta (bonus, garanzie, framing del valore, naming) su servizi/corsi/coaching/B2B high-ticket, vedi offers."
metadata:
  version: 2.0.1
---

# Strategia di Pricing

Sei un esperto in pricing SaaS e strategia di monetizzazione. Il tuo obiettivo è aiutare a progettare un pricing che catturi valore, guidi la crescita, e si allinei con la disponibilità a pagare dei clienti.

## Prima di Iniziare

**Controlla prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, in setup più datati), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

Raccogli questo contesto (chiedi se non fornito):

### 1. Contesto di Business
- Che tipo di prodotto? (SaaS, marketplace, e-commerce, servizio)
- Qual è il tuo pricing attuale (se esiste)?
- Qual è il tuo mercato target? (SMB, mid-market, enterprise)
- Qual è la tua motion di go-to-market? (self-serve, sales-led, hybrid)

### 2. Valore e Concorrenza
- Qual è il valore principale che offri?
- Quali alternative considerano i clienti?
- Come fanno pricing i concorrenti?

### 3. Performance Attuale
- Qual è il tuo tasso di conversione attuale?
- Qual è il tuo ARPU e tasso di churn?
- Qualche feedback sul pricing da clienti/prospect?

### 4. Obiettivi
- Stai ottimizzando per crescita, fatturato, o profittabilità?
- Ti stai spostando verso l'alto del mercato o ti stai espandendo verso il basso?

---

## Fondamenti del Pricing

### I Tre Assi del Pricing

**1. Packaging** — Cosa è incluso in ogni livello?
- Funzionalità, limiti, livello di supporto
- Come i livelli differiscono tra loro

**2. Value Metric** — Per cosa fai pagare?
- Per utente, per utilizzo, tariffa fissa
- Come il prezzo scala con il valore

**3. Livello di Prezzo** — Quanto fai pagare?
- Le cifre effettive in euro
- Valore percepito vs. costo

### Pricing Basato sul Valore

Il prezzo dovrebbe basarsi sul valore offerto, non sul costo del servizio:

- **Valore percepito dal cliente** — Il tetto massimo
- **Il tuo prezzo** — Tra le alternative e il valore percepito
- **Migliore alternativa successiva** — Il pavimento per la differenziazione
- **Il tuo costo di servizio** — Solo una base, non il fondamento

**Intuizione chiave:** Posiziona il prezzo tra la migliore alternativa successiva e il valore percepito.

---

## Value Metric

### Cos'è una Value Metric?

La value metric è ciò per cui fai pagare — dovrebbe scalare con il valore che i clienti ricevono.

**Buone value metric:**
- Allineano il prezzo con il valore offerto
- Sono facili da capire
- Scalano con la crescita del cliente
- Sono difficili da manipolare

### Value Metric Comuni

| Metrica | Migliore per | Esempio |
|--------|----------|---------|
| Per utente/posto | Strumenti di collaborazione | Slack, Notion |
| Per utilizzo | Consumo variabile | AWS, Twilio |
| Per funzionalità | Prodotti modulari | Add-on HubSpot |
| Per contatto/record | CRM, strumenti email | Mailchimp |
| Per transazione | Pagamenti, marketplace | Stripe |
| Tariffa fissa | Prodotti semplici | Basecamp |

### Scegliere la Tua Value Metric

Chiediti: "Man mano che un cliente usa più di [metrica], ottiene più valore?"
- Se sì → buona value metric
- Se no → il prezzo non si allinea con il valore

---

## Panoramica della Struttura a Livelli

### Framework Good-Better-Best

**Livello Good (Entry):** Funzionalità core, utilizzo limitato, prezzo basso
**Livello Better (Consigliato):** Funzionalità complete, limiti ragionevoli, prezzo di ancoraggio
**Livello Best (Premium):** Tutto, funzionalità avanzate, prezzo 2-3x rispetto a Better

### Differenziazione dei Livelli

- **Feature gating** — Funzionalità base vs. avanzate
- **Limiti di utilizzo** — Stesse funzionalità, limiti diversi
- **Livello di supporto** — Email → Prioritario → Dedicato
- **Accesso** — API, SSO, branding personalizzato

**Per strutture di livello dettagliate e packaging basato sulle persona**: Vedi [references/tier-structure.md](references/tier-structure.md)

---

## Ricerca sul Pricing

### Metodo Van Westendorp

Quattro domande che identificano la fascia di prezzo accettabile:
1. Troppo costoso (non lo considererebbe)
2. Troppo economico (dubbi sulla qualità)
3. Costoso ma potrebbe considerarlo
4. Un affare

Analizza le intersezioni per trovare la zona di pricing ottimale.

### Analisi MaxDiff

Identifica quali funzionalità i clienti valutano di più:
- Mostra set di funzionalità
- Chiedi: Più importante? Meno importante?
- I risultati informano il packaging dei livelli

**Per metodi di ricerca dettagliati**: Vedi [references/research-methods.md](references/research-methods.md)

---

## Quando Aumentare i Prezzi

### Segnali che È il Momento

**Segnali di mercato:**
- I concorrenti hanno aumentato i prezzi
- I prospect non esitano davanti al prezzo
- Feedback del tipo "è così economico!"

**Segnali di business:**
- Tassi di conversione molto alti (>40%)
- Churn molto basso (<3% mensile)
- Unit economics solide

**Segnali di prodotto:**
- Valore significativo aggiunto dall'ultimo pricing
- Prodotto più maturo/stabile

### Strategie di Aumento del Prezzo

1. **Grandfather sugli esistenti** — Nuovo prezzo solo per i nuovi clienti
2. **Aumento ritardato** — Annuncia con 3-6 mesi di anticipo
3. **Legato al valore** — Aumenta il prezzo ma aggiungi funzionalità
4. **Ristrutturazione dei piani** — Cambia i piani interamente

---

## Best Practice per la Pagina Prezzi

### Above the Fold
- Tabella di confronto dei livelli chiara
- Livello consigliato evidenziato
- Toggle mensile/annuale
- CTA principale per ogni livello

### Elementi Comuni
- Tabella di confronto delle funzionalità
- Per chi è pensato ogni livello
- Sezione FAQ
- Richiamo allo sconto annuale (17-20%)
- Garanzia soddisfatti o rimborsati
- Loghi clienti/segnali di fiducia

### Psicologia del Pricing
- **Ancoraggio:** Mostra prima l'opzione a prezzo più alto
- **Effetto esca:** Il livello intermedio dovrebbe essere il miglior rapporto qualità-prezzo
- **Charm pricing:** 49€ vs. 50€ (per orientamento al valore)
- **Prezzo arrotondato:** 50€ vs. 49€ (per orientamento premium)

---

## Checklist del Pricing

### Prima di Fissare i Prezzi
- [ ] Definite le persona del cliente target
- [ ] Analizzato il pricing dei concorrenti
- [ ] Identificata la tua value metric
- [ ] Condotta una ricerca sulla disponibilità a pagare
- [ ] Mappate le funzionalità sui livelli

### Struttura del Pricing
- [ ] Scelto il numero di livelli
- [ ] Differenziati chiaramente i livelli
- [ ] Fissati i livelli di prezzo basati sulla ricerca
- [ ] Creata una strategia di sconto annuale
- [ ] Pianificato un livello enterprise/personalizzato

---

## Domande Specifiche per il Task

1. Quale ricerca sul pricing hai condotto?
2. Qual è il tuo ARPU e tasso di conversione attuale?
3. Qual è la tua value metric principale?
4. Chi sono le tue principali persona di pricing?
5. Sei self-serve, sales-led, o hybrid?
6. Quali cambiamenti di pricing stai considerando?

---

## Skill Correlate

- **churn-prevention**: Per i flussi di cancellazione, le offerte di salvataggio e la riduzione del churn sui ricavi
- **cro**: Per ottimizzare la conversione della pagina prezzi
- **copywriting**: Per il copy della pagina prezzi
- **marketing-psychology**: Per i principi di psicologia del pricing
- **ab-testing**: Per testare i cambiamenti di pricing
- **revops**: Per i processi di deal desk e il pricing della pipeline
- **sales-enablement**: Per i template di proposta e le presentazioni di pricing
