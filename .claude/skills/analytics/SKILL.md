---
name: analytics
description: Quando l'utente vuole impostare, migliorare o controllare il tracciamento e la misurazione analitica. Usare anche quando l'utente menziona "impostare il tracciamento," "GA4," "Google Analytics," "tracciamento delle conversioni," "tracciamento degli eventi," "parametri UTM," "tag manager," "GTM," "implementazione analytics," "piano di tracciamento," "come faccio a sapere se funziona," "tracciare le conversioni," "attribuzione," "Mixpanel," "Segment," "i miei eventi si attivano correttamente," o "l'analytics non funziona." Usare questa skill ogni volta che qualcuno chiede come sapere se qualcosa funziona o vuole misurare i risultati di marketing. Per la misurazione dei test A/B, vedere ab-testing.
metadata:
  version: 2.0.0
---

# Tracciamento Analytics

Sei un esperto di implementazione e misurazione analytics. Il tuo obiettivo è aiutare a impostare un tracciamento che fornisca insight azionabili per le decisioni di marketing e prodotto.

## Valutazione Iniziale

**Verifica prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo compito.

Prima di implementare il tracciamento, comprendi:

1. **Contesto di Business** - Quali decisioni informeranno questi dati? Quali sono le conversioni chiave?
2. **Stato Attuale** - Quale tracciamento esiste già? Quali strumenti sono in uso?
3. **Contesto Tecnico** - Qual è lo stack tecnologico? Ci sono requisiti di privacy/conformità?

---

## Principi Fondamentali

### 1. Traccia per le Decisioni, Non per i Dati
- Ogni evento dovrebbe informare una decisione
- Evita le metriche vanità
- Qualità > quantità degli eventi

### 2. Parti dalle Domande
- Cosa hai bisogno di sapere?
- Quali azioni intraprenderai sulla base di questi dati?
- Lavora a ritroso per capire cosa devi tracciare

### 3. Denomina le Cose in Modo Coerente
- Le convenzioni di denominazione contano
- Stabilisci dei pattern prima di implementare
- Documenta tutto

### 4. Mantieni la Qualità dei Dati
- Valida l'implementazione
- Monitora eventuali problemi
- Dati puliti > più dati

---

## Framework del Piano di Tracciamento

### Struttura

```
Nome Evento | Categoria | Proprietà | Trigger | Note
---------- | -------- | ---------- | ------- | -----
```

### Tipi di Evento

| Tipo | Esempi |
|------|----------|
| Pageview | Automatico, arricchito con metadati |
| Azioni Utente | Click sui bottoni, invii di form, utilizzo delle funzionalità |
| Eventi di Sistema | Registrazione completata, acquisto, abbonamento modificato |
| Conversioni Personalizzate | Completamento obiettivi, fasi del funnel |

**Per elenchi completi degli eventi**: Vedi [references/event-library.md](references/event-library.md)

---

## Convenzioni di Denominazione degli Eventi

### Formato Consigliato: Oggetto-Azione

```
signup_completed
button_clicked
form_submitted
article_read
checkout_payment_completed
```

### Best Practice
- Minuscolo con underscore
- Sii specifico: `cta_hero_clicked` invece di `button_clicked`
- Includi il contesto nelle proprietà, non nel nome dell'evento
- Evita spazi e caratteri speciali
- Documenta le decisioni

---

## Eventi Essenziali

### Sito Marketing

| Evento | Proprietà |
|-------|------------|
| cta_clicked | button_text, location |
| form_submitted | form_type |
| signup_completed | method, source |
| demo_requested | - |

### Prodotto/App

| Evento | Proprietà |
|-------|------------|
| onboarding_step_completed | step_number, step_name |
| feature_used | feature_name |
| purchase_completed | plan, value |
| subscription_cancelled | reason |

**Per la libreria completa di eventi per tipo di business**: Vedi [references/event-library.md](references/event-library.md)

---

## Proprietà degli Eventi

### Proprietà Standard

| Categoria | Proprietà |
|----------|------------|
| Pagina | page_title, page_location, page_referrer |
| Utente | user_id, user_type, account_id, plan_type |
| Campagna | source, medium, campaign, content, term |
| Prodotto | product_id, product_name, category, price |

### Best Practice
- Usa nomi di proprietà coerenti
- Includi il contesto rilevante
- Non duplicare le proprietà automatiche
- Evita PII (dati personali identificabili) nelle proprietà

---

## Implementazione GA4

### Configurazione Rapida

1. Crea la proprietà GA4 e il data stream
2. Installa gtag.js o GTM
3. Attiva la misurazione avanzata
4. Configura eventi personalizzati
5. Contrassegna le conversioni in Admin

### Esempio di Evento Personalizzato

```javascript
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});
```

**Per l'implementazione dettagliata di GA4**: Vedi [references/ga4-implementation.md](references/ga4-implementation.md)

---

## Google Tag Manager

### Struttura del Container

| Componente | Scopo |
|-----------|---------|
| Tag | Codice che viene eseguito (GA4, pixel) |
| Trigger | Quando i tag si attivano (visualizzazione pagina, click) |
| Variabili | Valori dinamici (testo del click, data layer) |

### Pattern del Data Layer

```javascript
dataLayer.push({
  'event': 'form_submitted',
  'form_name': 'contact',
  'form_location': 'footer'
});
```

**Per l'implementazione dettagliata di GTM**: Vedi [references/gtm-implementation.md](references/gtm-implementation.md)

---

## Strategia dei Parametri UTM

### Parametri Standard

| Parametro | Scopo | Esempio |
|-----------|---------|---------|
| utm_source | Fonte del traffico | google, newsletter |
| utm_medium | Canale di marketing | cpc, email, social |
| utm_campaign | Nome della campagna | spring_sale |
| utm_content | Differenzia le versioni | hero_cta |
| utm_term | Keyword di ricerca a pagamento | running+shoes |

### Convenzioni di Denominazione
- Tutto minuscolo
- Usa underscore o trattini in modo coerente
- Sii specifico ma conciso: `blog_footer_cta`, non `cta1`
- Documenta tutti gli UTM in un foglio di calcolo

---

## Debug e Validazione

### Strumenti di Test

| Strumento | Usare Per |
|------|---------|
| GA4 DebugView | Monitoraggio degli eventi in tempo reale |
| GTM Preview Mode | Testare i trigger prima della pubblicazione |
| Estensioni del Browser | Tag Assistant, dataLayer Inspector |

### Checklist di Validazione

- [ ] Gli eventi si attivano sui trigger corretti
- [ ] I valori delle proprietà si popolano correttamente
- [ ] Nessun evento duplicato
- [ ] Funziona su browser e mobile
- [ ] Le conversioni vengono registrate correttamente
- [ ] Nessuna perdita di PII

### Problemi Comuni

| Problema | Da Controllare |
|-------|-------|
| Gli eventi non si attivano | Configurazione del trigger, GTM caricato |
| Valori errati | Percorso della variabile, struttura del data layer |
| Eventi duplicati | Più container, trigger che si attiva due volte |

---

## Privacy e Conformità

### Considerazioni
- Consenso cookie richiesto in UE/UK/CA
- Nessun PII nelle proprietà analytics
- Impostazioni di conservazione dei dati
- Capacità di eliminazione dell'utente

### Implementazione
- Usa la modalità consenso (attendi il consenso)
- Anonimizzazione IP
- Raccogli solo ciò di cui hai bisogno
- Integra con una piattaforma di gestione del consenso

---

## Formato di Output

### Documento del Piano di Tracciamento

```markdown
# Piano di Tracciamento [Sito/Prodotto]

## Panoramica
- Strumenti: GA4, GTM
- Ultimo aggiornamento: [Data]

## Eventi

| Nome Evento | Descrizione | Proprietà | Trigger |
|------------|-------------|------------|---------|
| signup_completed | L'utente completa la registrazione | method, plan | Pagina di successo |

## Dimensioni Personalizzate

| Nome | Ambito | Parametro |
|------|-------|-----------|
| user_type | Utente | user_type |

## Conversioni

| Conversione | Evento | Conteggio |
|------------|-------|----------|
| Registrazione | signup_completed | Una volta per sessione |
```

---

## Domande Specifiche per il Compito

1. Quali strumenti stai utilizzando (GA4, Mixpanel, ecc.)?
2. Quali azioni chiave vuoi tracciare?
3. Quali decisioni informeranno questi dati?
4. Chi implementa - il team di sviluppo o il marketing?
5. Ci sono requisiti di privacy/consenso?
6. Cosa viene già tracciato?

---

## Integrazioni con gli Strumenti

Per l'implementazione, vedi il [registro degli strumenti](../../tools/REGISTRY.md). Strumenti analytics principali:

| Strumento | Ideale Per | MCP | Guida |
|------|----------|:---:|-------|
| **GA4** | Web analytics, ecosistema Google | ✓ | [ga4.md](../../tools/integrations/ga4.md) |
| **Mixpanel** | Product analytics, tracciamento eventi | - | [mixpanel.md](../../tools/integrations/mixpanel.md) |
| **Amplitude** | Product analytics, analisi delle coorti | - | [amplitude.md](../../tools/integrations/amplitude.md) |
| **PostHog** | Analytics open-source, session replay | - | [posthog.md](../../tools/integrations/posthog.md) |
| **Segment** | Customer data platform, instradamento | - | [segment.md](../../tools/integrations/segment.md) |

---

## Skill Correlate

- **ab-testing**: Per il tracciamento degli esperimenti
- **seo-audit**: Per l'analisi del traffico organico
- **cro**: Per l'ottimizzazione delle conversioni (usa questi dati)
- **revops**: Per le metriche di pipeline, il tracciamento CRM e l'attribuzione dei ricavi
