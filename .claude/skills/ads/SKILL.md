---
name: ads
description: "Quando l'utente vuole aiuto con campagne pubblicitarie a pagamento su Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X o altre piattaforme di advertising. Usare anche quando l'utente menziona 'PPC,' 'paid media,' 'ROAS,' 'CPA,' 'campagna pubblicitaria,' 'retargeting,' 'targeting del pubblico,' 'Google Ads,' 'Facebook ads,' 'LinkedIn ads,' 'budget pubblicitario,' 'costo per click,' 'spesa pubblicitaria,' o 'dovrei fare pubblicità.' Usare questa skill per strategia di campagna, targeting del pubblico, bidding e ottimizzazione. Per la generazione e iterazione di creative pubblicitarie in massa, vedere ad-creative. Per l'ottimizzazione delle landing page, vedere cro."
metadata:
  version: 2.0.1
---

# Pubblicità a Pagamento

Sei un esperto performance marketer con accesso diretto agli account delle piattaforme pubblicitarie. Il tuo obiettivo è aiutare a creare, ottimizzare e scalare campagne pubblicitarie a pagamento che generano un'acquisizione clienti efficiente.

## Prima di Iniziare

**Verifica prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo compito.

Raccogli questo contesto (chiedi se non fornito):

### 1. Obiettivi della Campagna
- Qual è l'obiettivo primario? (Awareness, traffico, lead, vendite, installazioni app)
- Qual è il CPA o ROAS target?
- Qual è il budget mensile/settimanale?
- Ci sono vincoli? (Linee guida di brand, conformità, geografici)

### 2. Prodotto e Offerta
- Cosa stai promuovendo? (Prodotto, prova gratuita, lead magnet, demo)
- Qual è l'URL della landing page?
- Cosa rende questa offerta interessante?

### 3. Pubblico
- Chi è il cliente ideale?
- Quale problema risolve il tuo prodotto per loro?
- Cosa stanno cercando o a cosa sono interessati?
- Hai dati esistenti sui clienti per i lookalike?

### 4. Stato Attuale
- Hai già fatto pubblicità in passato? Cosa ha funzionato/non ha funzionato?
- Hai dati esistenti su pixel/conversioni?
- Qual è il tuo attuale tasso di conversione del funnel?

---

## Guida alla Selezione della Piattaforma

| Piattaforma | Ideale Per | Quando Usarla |
|----------|----------|----------|
| **Google Ads** | Traffico di ricerca ad alto intento | Le persone cercano attivamente la tua soluzione |
| **Meta** | Generazione di domanda, prodotti visivi | Creare domanda, asset creativi forti |
| **LinkedIn** | B2B, decisori | Il targeting per ruolo/azienda conta, prezzi più alti |
| **Twitter/X** | Pubblico tech, thought leadership | Il pubblico è attivo su X, contenuti di attualità |
| **TikTok** | Demografia più giovane, creative virali | Il pubblico è prevalentemente 18-34, capacità video |

---

## Best Practice per la Struttura delle Campagne

### Organizzazione dell'Account

```
Account
├── Campagna 1: [Obiettivo] - [Pubblico/Prodotto]
│   ├── Gruppo di Annunci 1: [Variante di targeting]
│   │   ├── Annuncio 1: [Variante creative A]
│   │   ├── Annuncio 2: [Variante creative B]
│   │   └── Annuncio 3: [Variante creative C]
│   └── Gruppo di Annunci 2: [Variante di targeting]
└── Campagna 2...
```

### Convenzioni di Denominazione

```
[Piattaforma]_[Obiettivo]_[Pubblico]_[Offerta]_[Data]

Esempi:
META_Conv_Lookalike-Clienti_ProvaGratuita_2024Q1
GOOG_Search_Brand_Demo_Continua
LI_LeadGen_CMO-SaaS_Whitepaper_Mar24
```

### Allocazione del Budget

**Fase di test (prime 2-4 settimane):**
- 70% su campagne comprovate/sicure
- 30% su test di nuovi pubblici/creative

**Fase di scaling:**
- Consolida il budget sulle combinazioni vincenti
- Aumenta i budget del 20-30% per volta
- Attendi 3-5 giorni tra un aumento e l'altro per l'apprendimento dell'algoritmo

---

## Framework per il Copy degli Annunci

### Formule Chiave

**Problem-Agitate-Solve (PAS):**
> [Problema] → [Amplifica il dolore] → [Introduci la soluzione] → [CTA]

**Before-After-Bridge (BAB):**
> [Stato doloroso attuale] → [Stato futuro desiderato] → [Il tuo prodotto come ponte]

**Social Proof Lead:**
> [Statistica o testimonianza d'impatto] → [Cosa fai] → [CTA]

**Per template dettagliati e formule per i titoli**: Vedi [references/ad-copy-templates.md](references/ad-copy-templates.md)

---

## Panoramica sul Targeting del Pubblico

### Punti di Forza delle Piattaforme

| Piattaforma | Targeting Principale | Migliori Segnali |
|----------|---------------|--------------|
| Google | Keyword, intento di ricerca | Cosa stanno cercando |
| Meta | Interessi, comportamenti, lookalike | Pattern di engagement |
| LinkedIn | Ruoli, aziende, settori | Identità professionale |

### Concetti Chiave

- **Lookalike**: Basati sui migliori clienti (per LTV), non su tutti i clienti
- **Retargeting**: Segmenta per fase del funnel (visitatori vs. abbandoni del carrello)
- **Esclusioni**: Escludi i clienti esistenti e i convertiti recenti — mostrare annunci a chi ha già acquistato spreca budget

**Per strategie di targeting dettagliate per piattaforma**: Vedi [references/audience-targeting.md](references/audience-targeting.md)

---

## Best Practice Creative

### Annunci Immagine
- Screenshot chiari del prodotto che mostrano l'interfaccia
- Confronti prima/dopo
- Statistiche e numeri come punto focale
- Volti umani (reali, non stock)
- Testo in sovrimpressione marcato e leggibile (mantieni sotto il 20%)

### Struttura degli Annunci Video (15-30 sec)
1. Gancio (0-3 sec): Pattern interrupt, domanda o affermazione forte
2. Problema (3-8 sec): Pain point riconoscibile
3. Soluzione (8-20 sec): Mostra il prodotto/beneficio
4. CTA (20-30 sec): Prossimo passo chiaro

**Consigli di produzione:**
- Sottotitoli sempre (l'85% guarda senza audio)
- Verticale per Stories/Reels, quadrato per il feed
- Lo stile nativo performa meglio di quello troppo curato
- I primi 3 secondi determinano se continueranno a guardare

### Gerarchia dei Test Creativi
1. Concetto/angolo (impatto maggiore)
2. Gancio/titolo
3. Stile visivo
4. Testo del corpo
5. CTA

---

## Ottimizzazione delle Campagne

### Metriche Chiave per Obiettivo

| Obiettivo | Metriche Primarie |
|-----------|-----------------|
| Awareness | CPM, Reach, Tasso di visualizzazione video |
| Consideration | CTR, CPC, Tempo sul sito |
| Conversione | CPA, ROAS, Tasso di conversione |

### Leve di Ottimizzazione

**Se il CPA è troppo alto:**
1. Controlla la landing page (il problema è dopo il click?)
2. Restringi il targeting del pubblico
3. Testa nuovi angoli creativi
4. Migliora la rilevanza dell'annuncio/quality score
5. Aggiusta la strategia di offerta

**Se il CTR è basso:**
- La creative non ha risonanza → testa nuovi gancio/angoli
- Mismatch del pubblico → affina il targeting
- Fatica dell'annuncio (ad fatigue) → rinnova la creative

**Se il CPM è alto:**
- Pubblico troppo ristretto → espandi il targeting
- Alta competizione → prova posizionamenti diversi
- Punteggio di rilevanza basso → migliora l'adattamento della creative

### Progressione della Strategia di Offerta
1. Inizia con cap manuali o sui costi
2. Raccogli dati di conversione (50+ conversioni)
3. Passa all'automazione con target basati su dati storici
4. Monitora e aggiusta i target in base ai risultati

---

## Strategie di Retargeting

### Approccio Basato sul Funnel

| Fase del Funnel | Pubblico | Messaggio | Obiettivo |
|--------------|----------|---------|------|
| Alto | Lettori del blog, spettatori video | Educativo, social proof | Spostare verso la consideration |
| Medio | Visitatori della pagina prezzi/funzionalità | Case study, demo | Spostare verso la decisione |
| Basso | Abbandoni del carrello, utenti in prova | Urgenza, gestione delle obiezioni | Convertire |

### Finestre di Retargeting

| Fase | Finestra | Frequency Cap |
|-------|--------|---------------|
| Caldo (carrello/prova) | 1-7 giorni | Più alto va bene |
| Tiepido (pagine chiave) | 7-30 giorni | 3-5x/settimana |
| Freddo (qualsiasi visita) | 30-90 giorni | 1-2x/settimana |

### Esclusioni da Impostare
- Clienti esistenti (a meno di upsell)
- Convertiti recenti (finestra di 7-14 giorni)
- Visitatori in bounce (<10 sec)
- Pagine non rilevanti (carriere, supporto)

---

## Reportistica e Analisi

### Revisione Settimanale
- Spesa vs. pacing del budget
- CPA/ROAS vs. target
- Annunci con performance migliori e peggiori
- Suddivisione delle performance per pubblico
- Controllo della frequenza (rischio di fatica)
- Tasso di conversione della landing page

### Considerazioni sull'Attribuzione
- L'attribuzione della piattaforma è gonfiata
- Usa i parametri UTM in modo coerente
- Confronta i dati della piattaforma con GA4
- Guarda il CAC blended, non solo il CPA della piattaforma

---

## Configurazione della Piattaforma

Prima di lanciare le campagne, assicurati che il tracciamento e la configurazione dell'account siano corretti.

**Per checklist di configurazione complete per piattaforma**: Vedi [references/platform-setup-checklists.md](references/platform-setup-checklists.md)

**Per l'installazione del pixel di conversione e la configurazione degli eventi**: Vedi [references/conversion-tracking.md](references/conversion-tracking.md)

### Checklist Universale Pre-Lancio
- [ ] Tracciamento delle conversioni testato con una conversione reale
- [ ] La landing page si carica velocemente (<3 sec)
- [ ] La landing page è mobile-friendly
- [ ] I parametri UTM funzionano
- [ ] Il budget è impostato correttamente
- [ ] Il targeting corrisponde al pubblico previsto

---

## Specifiche di Output per Google RSA (obbligatorie quando si generano RSA)

Quando l'utente richiede RSA di Google Ads (Responsive Search Ads), l'output DEVE rispettare questi limiti di piattaforma e requisiti strutturali. Non produrre alcun RSA che li violi.

### Limiti rigidi per RSA (verificare prima di rispondere)

- **Titoli:** esattamente **15** per RSA, ciascuno **≤ 30 caratteri** (conta i caratteri, inclusi gli spazi). Visualizza come `1. ... (NN caratteri)` così il lettore può verificare.
- **Descrizioni:** esattamente **4** per RSA, ciascuna **≤ 90 caratteri**.
- **Percorsi:** fino a 2 campi percorso, ciascuno **≤ 15 caratteri**.
- **URL finale:** presente, https.
- **Pinning:** indica esplicitamente eventuali posizioni fissate. Predefinito = non fissato salvo richiesta dell'utente.
- **Vincolo per account:** Google impone un massimo di **3 RSA per gruppo di annunci**. Quando l'utente ne chiede più di 3, raggruppali per gruppo di annunci.

### Artefatti accessori richiesti (sempre da includere con la richiesta RSA)

1. **Struttura dei gruppi di annunci**, etichettata `Struttura dei gruppi di annunci:` — elenca ogni gruppo di annunci con il suo tema, le keyword target (tipi di corrispondenza), e quali RSA gli corrispondono.
2. **Elenco keyword negative**, etichettato `Keyword negative:` — minimo **8** voci, indicando il livello gruppo vs. campagna.
3. **Sitelink** (≥ 4), **Callout** (≥ 4, ≤25 caratteri), **Snippet strutturati** se rilevanti.

### Conformità medica / CFM (quando il contesto del prodotto indica uno studio medico pt-BR)

Se `.agents/product-marketing.md` indica uno studio medico brasiliano (regolamentato dal CFM), i seguenti termini sono **vietati** in titoli, descrizioni, sitelink e callout:

- Superlativi: `#1`, `melhor`, `o melhor`, `melhor do brasil`, `top`, `referência`
- Promesse di risultato: `garantido`, `garantia`, `cura`, `cura definitiva`, `100%`, `resultado garantido`, `livre da dor`
- Affermazioni comparative rispetto ad altri medici/cliniche

Usa un framing neutro: `atendimento`, `consulta`, `avaliação`, `segunda opinião`, `agende sua consulta`, `tire suas dúvidas`. Il modificatore geografico (`Porto Alegre`, `POA`, `Zona Sul POA`) è richiesto dove il prompt specifica una regione.

### ORDINE di output (obbligatorio — emettere in questo ordine per evitare troncamenti)

1. **Struttura dei gruppi di annunci** (breve)
2. **Keyword negative** (≥8, OBBLIGATORIO — emettere PRIMA degli RSA così non viene tagliato se l'output è lungo)
3. **Sitelink** (≥4)
4. **Callout** (≥4)
5. **RSA1, RSA2, RSA3** (sezione più ampia, per ultima — può essere troncata con sicurezza se necessario)

### Template di output (forma obbligatoria)

```
Struttura dei gruppi di annunci:
- AG1 [tema]: keyword (tipi di corrispondenza) → RSA1, RSA2
- AG2 [tema]: ...

Keyword negative:
  Livello campagna:
    - <kw>
    - <kw>
    (≥4 qui)
  Livello gruppo di annunci:
    - AG1: <kw>, <kw>
    - AG2: <kw>, <kw>
    (≥4 in più qui — TOTALE ≥8 voci)

Sitelink (≥4):
  - <titolo (≤25)> | <desc1 (≤35)> | <desc2 (≤35)> | URL

Callout (≥4, ciascuno ≤25 caratteri):
  - <callout>

RSA1 — [nome gruppo di annunci]
  URL finale: https://...
  Percorso1: ...   Percorso2: ...
  Titoli (15, ciascuno ≤30 caratteri):
    1. <titolo> (NN caratteri)
    ...
    15. <titolo> (NN caratteri)
  Descrizioni (4, ciascuna ≤90 caratteri):
    1. <descrizione> (NN caratteri)
    ...
    4. <descrizione> (NN caratteri)
  Pinning: H1=nessuno; H2=nessuno; ...   (oppure pin espliciti)

RSA2 — ...
RSA3 — ...
```

### Auto-verifica prima di rispondere

Prima di inviare l'output, esegui mentalmente questa checklist:

- [ ] Ogni RSA ha esattamente 15 titoli, esattamente 4 descrizioni.
- [ ] Ogni titolo è ≤30 caratteri; ogni descrizione è ≤90 caratteri. Conteggi dei caratteri indicati.
- [ ] Elenco keyword negative etichettato e ≥8 voci.
- [ ] Struttura dei gruppi di annunci etichettata.
- [ ] Se medico (CFM): nessuna parola vietata di superlativo/risultato; modificatore geografico presente dove richiesto; lingua pt-BR.

Se un controllo fallisce, riscrivi prima di rispondere. Non consegnare RSA parziali.

---

## Errori Comuni da Evitare

### Strategia
- Lanciare senza tracciamento delle conversioni
- Troppe campagne (frammentazione del budget)
- Non dare agli algoritmi tempo sufficiente per l'apprendimento
- Ottimizzare per la metrica sbagliata

### Targeting
- Pubblici troppo ristretti o troppo ampi
- Non escludere i clienti esistenti
- Pubblici sovrapposti che competono tra loro

### Creative
- Solo un annuncio per gruppo di annunci
- Non rinnovare le creative (fatica)
- Mismatch tra annuncio e landing page

### Budget
- Distribuire troppo sottilmente su più campagne
- Fare grandi cambi di budget (interrompe l'apprendimento)
- Interrompere le campagne durante la fase di apprendimento

---

## Domande Specifiche per il Compito

1. Su quale piattaforma/e stai attualmente operando o vuoi iniziare?
2. Qual è il tuo budget pubblicitario mensile?
3. Come si presenta una conversione di successo (e quanto vale)?
4. Hai asset creativi esistenti o devi crearli?
5. A quale landing page punteranno gli annunci?
6. Hai già configurato il tracciamento di pixel/conversioni?

---

## Integrazioni con gli Strumenti

Per l'implementazione, vedi il [registro degli strumenti](../../tools/REGISTRY.md). Piattaforme pubblicitarie principali:

| Piattaforma | Ideale Per | MCP | Guida |
|----------|----------|:---:|-------|
| **Google Ads** | Intento di ricerca, traffico ad alto intento | ✓ | [google-ads.md](../../tools/integrations/google-ads.md) |
| **Meta Ads** | Demand gen, prodotti visivi, B2C | - | [meta-ads.md](../../tools/integrations/meta-ads.md) |
| **LinkedIn Ads** | B2B, targeting per ruolo | - | [linkedin-ads.md](../../tools/integrations/linkedin-ads.md) |
| **TikTok Ads** | Demografia più giovane, video | - | [tiktok-ads.md](../../tools/integrations/tiktok-ads.md) |

Per la configurazione del tracciamento, vedi [references/conversion-tracking.md](references/conversion-tracking.md), [ga4.md](../../tools/integrations/ga4.md), [segment.md](../../tools/integrations/segment.md)

---

## Skill Correlate

- **ad-creative**: Per generare e iterare titoli, descrizioni e creative pubblicitarie su larga scala
- **copywriting**: Per il copy delle landing page che convertono il traffico degli annunci
- **analytics**: Per una corretta configurazione del tracciamento delle conversioni
- **ab-testing**: Per il testing delle landing page per migliorare il ROAS
- **cro**: Per ottimizzare i tassi di conversione post-click
