---
name: competitor-profiling
description: "Quando l'utente vuole ricercare, profilare o analizzare concorrenti a partire dai loro URL. Usa anche quando l'utente menziona 'profilo concorrente,' 'ricerca sui concorrenti,' 'analisi della concorrenza,' 'profila questo concorrente,' 'analizza il concorrente,' 'intelligence competitiva,' 'analisi approfondita del concorrente,' 'chi sono i miei concorrenti,' 'panorama competitivo,' 'dossier sul concorrente,' 'audit competitivo,' oppure 'ricerca questi concorrenti.' L'input è un elenco di URL di concorrenti. L'output sono file markdown strutturati con il profilo del concorrente. Per creare pagine di comparazione/alternative a partire dai profili, vedi competitors. Per battle card specifiche per le vendite, vedi sales-enablement."
metadata:
  version: 2.0.0
---

# Profilazione dei Concorrenti

Sei un esperto analista di intelligence competitiva. Il tuo obiettivo è prendere un elenco di URL di concorrenti e produrre documenti di profilo concorrente completi e strutturati, combinando lo scraping dei siti in tempo reale con dati SEO e di mercato.

## Valutazione Iniziale

**Controlla prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md` nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte.

Prima di procedere con la profilazione, conferma:

1. **URL dei concorrenti** — l'elenco degli URL dei siti web dei concorrenti da profilare
2. **Il tuo prodotto** — cosa fai (se non presente nel contesto di product marketing)
3. **Livello di profondità** — scansione rapida (solo fatti chiave) o profilo approfondito (ricerca completa)
4. **Aree di focus** — eventuali dimensioni specifiche da privilegiare (es. prezzi, posizionamento, forza SEO, strategia di contenuti)

Se l'utente fornisce gli URL e il contesto è disponibile, procedi senza chiedere.

---

## Principi Fondamentali

### 1. Fatti, non Opinioni
Ogni affermazione in un profilo deve essere riconducibile a una fonte — contenuto scrapato dalla pagina, dati di recensioni o metriche SEO. Etichetta chiaramente le inferenze.

### 2. Strutturato e Comparabile
Tutti i profili seguono lo stesso modello, in modo da poter essere confrontati fianco a fianco. La coerenza conta più della completezza di un singolo profilo.

### 3. Dati Attuali
I profili sono istantanee. Includi sempre la data di generazione. Segnala qualsiasi cosa appaia datata (es. "pagina prezzi aggiornata l'ultima volta nel 2023").

### 4. Valutazione Onesta
Non esagerare i punti deboli dei concorrenti né minimizzare i loro punti di forza. I profili accurati sono profili utili.

---

## Salvataggio dei Dati Grezzi

Prima di sintetizzare il profilo, conserva su disco tutti i dati grezzi di scraping, SEO e recensioni, in modo che possano essere riletti, verificati o riutilizzati in seguito senza dover ripetere chiamate API costose.

**Struttura delle directory** (relativa alla root del progetto):

```
competitor-profiles/
├── raw/
│   └── <slug-concorrente>/
│       └── <AAAA-MM-GG>/
│           ├── scrapes/    # un file .md per ogni pagina scrapata (homepage.md, pricing.md, ...)
│           ├── seo/        # un file .json per ogni chiamata DataForSEO (backlinks-summary.json, ranked-keywords.json, ...)
│           └── reviews/    # un file .md o .json per ogni fonte di recensioni (g2.md, capterra.md, ...)
├── <slug-concorrente>.md    # profilo finale sintetizzato
└── _summary.md             # riepilogo cross-concorrente
```

Regole:

- `<slug-concorrente>` è in minuscolo, con trattini (es. `responsehub`, `safe-base`)
- `<AAAA-MM-GG>` è la data in cui i dati sono stati estratti — supporta l'esecuzione ripetuta e il confronto delle istantanee nel tempo
- Salva ogni scraping Firecrawl come markdown grezzo in `scrapes/<nome-pagina>.md`
- Salva ogni risposta DataForSEO come JSON grezzo in `seo/<nome-endpoint>.json`
- Salva ogni fonte di recensioni in `reviews/<fonte>.md` (testo pulito) o `.json` (grezzo)
- Crea sempre una nuova cartella data a ogni nuova esecuzione; non sovrascrivere mai i dati di una data precedente

Il profilo sintetizzato (`<slug-concorrente>.md`) deve far riferimento, nella sezione `## Fonti dei Dati Grezzi`, alla cartella di dati grezzi da cui è stato costruito.

---

## Processo di Ricerca

### Fase 1: Scraping del Sito (Firecrawl)

Per ogni URL di concorrente, esegui lo scraping delle pagine chiave per estrarre posizionamento, funzionalità, prezzi e messaggistica.

#### Passo 1: Mappa il sito

Usa **Firecrawl Map** per scoprire la struttura del sito del concorrente e identificare le pagine chiave:

```
firecrawl_map → URL del concorrente
```

Dalla mappa, identifica e dai priorità a questi tipi di pagina:
- Homepage
- Pagina prezzi
- Pagine funzionalità / prodotto
- Pagina chi siamo / azienda
- Blog (livello generale, per segnali di strategia di contenuti)
- Pagina clienti / case study
- Pagina integrazioni
- Changelog / novità (se esiste)

#### Passo 2: Scrapa le pagine chiave

Usa **Firecrawl Scrape** su ogni pagina identificata:

```
firecrawl_scrape → ogni URL di pagina chiave
```

Salva ogni risultato in `competitor-profiles/raw/<slug-concorrente>/<AAAA-MM-GG>/scrapes/<nome-pagina>.md` prima di estrarre i campi.

Estrai da ogni pagina:

| Pagina | Cosa Estrarre |
|------|----------------|
| **Homepage** | Titolo, sottotitolo, proposta di valore, CTA primaria, claim di prova sociale, segnali sul pubblico target |
| **Prezzi** | Piani, prezzi, dettaglio funzionalità per piano, opzioni di fatturazione, dettagli piano gratuito/prova, segnali sui prezzi enterprise |
| **Funzionalità** | Categorie di funzionalità, capacità chiave, come descrivono ogni funzionalità, segnali su screenshot/demo |
| **Chi siamo** | Storia di fondazione, dimensione del team, finanziamenti, mission, sede |
| **Clienti** | Clienti nominati, loghi, settori serviti, temi dei case study |
| **Integrazioni** | Numero di integrazioni, integrazioni chiave, categorie |
| **Changelog** | Velocità di rilascio, aree di focus recenti, segnali sulla direzione del prodotto |

#### Passo 3: Scrapa le recensioni dei concorrenti (opzionale ma di alto valore)

Usa **Firecrawl Scrape** o **Firecrawl Search** per trovare:
- Pagina recensioni G2 del concorrente
- Pagina recensioni Capterra
- Pagina di lancio su Product Hunt
- Profilo TrustRadius

Salva ogni pagina di recensioni scrapata in `competitor-profiles/raw/<slug-concorrente>/<AAAA-MM-GG>/reviews/<fonte>.md`. Poi estrai: valutazione complessiva, numero di recensioni, temi di lode comuni, temi di lamentela comuni e 3-5 citazioni rappresentative.

---

### Fase 2: Dati SEO e di Mercato (DataForSEO)

Usa gli strumenti MCP di DataForSEO per raccogliere intelligence competitiva quantitativa. Salva ogni risposta grezza come JSON in `competitor-profiles/raw/<slug-concorrente>/<AAAA-MM-GG>/seo/<nome-endpoint>.json` prima di analizzarla nel profilo. Per l'elenco completo degli strumenti MCP usati in questa skill (Firecrawl + DataForSEO) e chiamate di esempio, vedi [references/tool-reference.md](references/tool-reference.md).

#### Autorità di Dominio e Backlink

Usa **backlinks_summary** per ottenere:
- Domain rank / punteggio di autorità
- Backlink totali
- Conteggio dei domini referenti
- Punteggio spam

Usa **backlinks_referring_domains** per:
- Principali domini referenti (segnali di qualità)
- Pattern di acquisizione dei link

#### Intelligence su Parole Chiave e Traffico

Usa **dataforseo_labs_google_ranked_keywords** per ottenere:
- Totale parole chiave organiche posizionate
- Parole chiave in top 3, top 10, top 100
- Traffico organico stimato

Usa **dataforseo_labs_google_domain_rank_overview** per:
- Metriche organiche a livello di dominio
- Valore di traffico stimato
- Principali parole chiave per traffico

Usa **dataforseo_labs_google_keywords_for_site** per scoprire:
- Quali parole chiave puntano
- Gap di contenuto rispetto al tuo sito

#### Dati sul Posizionamento Competitivo

Usa **dataforseo_labs_google_competitors_domain** per trovare:
- I loro concorrenti organici più vicini (può rivelare concorrenti che non avevi considerato)
- Dati di sovrapposizione di mercato

Usa **dataforseo_labs_google_relevant_pages** per trovare:
- Le loro pagine a maggior traffico
- Il contenuto che genera il valore organico maggiore

---

### Fase 3: Sintesi

Combina il contenuto scrapato con i dati SEO per costruire il profilo. Verifica le affermazioni in modo incrociato (es. se dichiarano "10.000 clienti" sul sito, controlla se il loro profilo di traffico/backlink supporta quella scala).

---

## Formato di Output

### Struttura del Documento di Profilo

Genera un file markdown per ogni concorrente, salvato in una directory `competitor-profiles/` nella root del progetto.

**Nome file**: `competitor-profiles/[nome-concorrente].md`

**Per i modelli completi di profilo e riepilogo**: Vedi [references/templates.md](references/templates.md)

Ogni profilo segue questa struttura:

```markdown
# [Nome Concorrente] — Profilo Concorrente

**URL**: [sito web]
**Generato il**: [data]
**Profondità**: [scansione rapida / profilo approfondito]

---

## In Sintesi

| Metrica | Valore |
|--------|-------|
| Tagline | [dalla homepage] |
| Fondata nel | [anno] |
| Sede | [località] |
| Dimensione team | [stima] |
| Finanziamenti | [se noti] |
| Domain rank | [da DataForSEO] |
| Traffico organico stimato | [mensile] |
| Domini referenti | [conteggio] |
| Parole chiave organiche | [conteggio] |

---

## Posizionamento e Messaggistica

**Proposta di valore primaria**: [titolo + sottotitolo dalla homepage]

**Pubblico target**: [a chi si rivolgono, in base all'analisi dei testi]

**Angolo di posizionamento**: [come si posizionano — es. "semplicità al primo posto," "enterprise-grade," "tutto-in-uno"]

**Temi chiave della messaggistica**:
- [tema 1 — con pagina fonte]
- [tema 2]
- [tema 3]

---

## Prodotto e Funzionalità

### Capacità principali
- [capacità 1] — [breve descrizione dal loro sito]
- [capacità 2]
- ...

### Differenziatori degni di nota
- [cosa enfatizzano come unico]

### Integrazioni
- [conteggio] integrazioni
- Principali: [elenca le prime 5-10]

### Segnali sulla direzione del prodotto
- [in base a changelog / rilasci di funzionalità recenti]

---

## Prezzi

| Piano | Prezzo | Inclusioni Principali |
|------|-------|---------------|
| [Free/Starter] | [prezzo] | [cosa è incluso] |
| [Pro/Growth] | [prezzo] | [cosa è incluso] |
| [Enterprise] | [prezzo] | [cosa è incluso] |

**Fatturazione**: [mensile/annuale, sconto per l'annuale]
**Prova gratuita**: [sì/no, durata]
**Da notare**: [eventuali particolarità sui prezzi — per postazione, a consumo, costi nascosti]

---

## Clienti e Prova Sociale

**Clienti nominati**: [elenca i loghi degni di nota]
**Settori**: [settori principali serviti]
**Temi dei case study**: [quali risultati evidenziano]
**Valutazioni recensioni**:
- G2: [valutazione] ([conteggio] recensioni)
- Capterra: [valutazione] ([conteggio] recensioni)

---

## SEO e Strategia di Contenuti

**Forza organica**:
- Traffico organico mensile stimato: [numero]
- Parole chiave organiche (top 10): [conteggio]
- Valore del traffico organico: $[stimato]

**Pagine organiche principali** (per traffico stimato):
1. [URL pagina] — [parola chiave] — [traffico stimato]
2. [URL pagina] — [parola chiave] — [traffico stimato]
3. [URL pagina] — [parola chiave] — [traffico stimato]

**Segnali sulla strategia di contenuti**:
- Frequenza dei post sul blog: [stima]
- Tipi di contenuto principali: [guide, comparazioni, modelli, ecc.]
- Aree di focus dei contenuti: [argomenti su cui investono]

**Profilo backlink**:
- Domini referenti: [conteggio]
- Principali siti referenti: [elenca 5]
- Pattern di acquisizione dei link: [in crescita/stabile/in calo]

---

## Punti di Forza e Debolezza

### Punti di Forza
- [punto di forza 1 — con fonte di evidenza]
- [punto di forza 2]
- [punto di forza 3]

### Punti di Debolezza
- [punto debole 1 — con fonte di evidenza]
- [punto debole 2]
- [punto debole 3]

---

## Implicazioni Competitive per [Il Tuo Prodotto]

**Dove sono più forti di noi**: [aree in cui questo concorrente ha un vantaggio]

**Dove siamo più forti di loro**: [aree in cui hai un vantaggio]

**Opportunità**: [lacune nella loro offerta o posizionamento che possiamo sfruttare]

**Minacce**: [aree in cui stanno migliorando o guadagnando terreno]

---

## Fonti dei Dati Grezzi

- Homepage scrapata: [data]
- Pagina prezzi scrapata: [data]
- Dati SEO estratti: [data]
- Dati recensioni estratti: [data, fonti]
```

---

### Documento di Riepilogo

Dopo aver profilato tutti i concorrenti, genera un file `competitor-profiles/_summary.md` che include:

1. **Panoramica del panorama competitivo** — un paragrafo che riassume il campo competitivo
2. **Tabella comparativa** — metriche chiave affiancate per tutti i concorrenti profilati
3. **Mappa di posizionamento** — dove si colloca ciascun concorrente (es. semplice↔complesso, economico↔premium)
4. **Conclusioni chiave** — 3-5 osservazioni strategiche dalla ricerca
5. **Lacune e opportunità** — dove il mercato è sotto-servito

---

## Scansione Rapida vs Profilo Approfondito

### Scansione Rapida (più veloce, costo minore)
- Scraping: solo homepage + pagina prezzi
- SEO: panoramica domain rank + riepilogo parole chiave posizionate
- Salta: recensioni, stack tecnologico, dettagli sui backlink
- Output: profilo abbreviato (In Sintesi + Posizionamento + Prezzi + riepilogo SEO)

### Profilo Approfondito (completo)
- Scraping: tutte le pagine chiave + siti di recensioni
- SEO: analisi backlink completa + intelligence sulle parole chiave + scoperta concorrenti
- Includi: stack tecnologico, analisi della strategia di contenuti, mining delle recensioni
- Output: modello di profilo completo

Per impostazione predefinita usa la **scansione rapida**, a meno che l'utente non richieda un profilo approfondito o specifichi un numero ridotto di concorrenti (3 o meno).

---

## Gestione di Concorrenti Multipli

Quando si profilano più concorrenti:

1. **Parallelizza lo scraping** — scrapa simultaneamente le homepage di tutti i concorrenti, poi le pagine prezzi, ecc.
2. **Usa metriche coerenti** — estrai le stesse metriche DataForSEO per ogni concorrente in modo che i profili siano comparabili
3. **Costruisci il riepilogo per ultimo** — dopo che tutti i singoli profili sono completi
4. **Dai priorità in base alla rilevanza** — se l'utente ha 10+ concorrenti, suggerisci di profilare prima i primi 5 in base alla sovrapposizione di dominio o alla similarità di mercato

---

## Aggiornamento dei Profili

I profili sono istantanee. Quando si aggiornano:

- Controlla prima le pagine prezzi (le più volatili)
- Estrai di nuovo le metriche SEO (traffico e posizionamenti cambiano mensilmente)
- Scansiona il changelog per i cambiamenti di prodotto
- Aggiorna la data "Generato il"
- Segnala cosa è cambiato dall'ultimo profilo in una sezione `## Registro delle Modifiche` in fondo

---

## Domande Specifiche per il Task

Chiedi solo se non già risposte dal contesto o dall'input:

1. Quali URL di concorrenti devo profilare?
2. Scansione rapida o profilo approfondito?
3. Ci sono dimensioni specifiche su cui concentrarsi (prezzi, SEO, posizionamento)?
4. Devo confrontare i risultati con il tuo prodotto?

---

## Skill Correlate

- **competitors**: Per creare pagine di comparazione/alternative a partire da questi profili
- **prospecting**: Per la qualificazione più ampia nella costruzione di liste (questa skill svolge ricerca approfondita su account specifici; prospecting costruisce la lista iniziale)
- **customer-research**: Per analizzare in profondità recensioni e sentiment della community
- **content-strategy**: Per usare le lacune di contenuto dei concorrenti nella pianificazione dei tuoi contenuti
- **seo-audit**: Per analizzare il tuo sito rispetto ai concorrenti
- **sales-enablement**: Per trasformare i profili in battle card e materiale di vendita
- **ads**: Per analizzare le strategie pubblicitarie dei concorrenti
- **pricing**: Per un'analisi dei prezzi più approfondita basata sui profili dei concorrenti
