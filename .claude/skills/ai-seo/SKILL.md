---
name: ai-seo
description: "Quando l'utente vuole ottimizzare i contenuti per i motori di ricerca AI, essere citato dagli LLM, o apparire nelle risposte generate dall'AI. Usare anche quando l'utente menziona 'AI SEO,' 'AEO,' 'GEO,' 'LLMO,' 'answer engine optimization,' 'generative engine optimization,' 'ottimizzazione LLM,' 'AI Overviews,' 'ottimizzare per ChatGPT,' 'ottimizzare per Perplexity,' 'citazioni AI,' 'visibilità AI,' 'ricerca a zero click,' 'come faccio ad apparire nelle risposte AI,' 'menzioni LLM,' 'ottimizzare per Claude/Gemini,' 'llms.txt,' 'OKF,' 'Open Knowledge Format,' 'knowledge bundle,' o 'sito leggibile dagli agenti.' Usare questa skill ogni volta che qualcuno vuole che i propri contenuti vengano citati o mostrati dagli assistenti AI e dai motori di ricerca AI. Per audit SEO tecnici e on-page tradizionali, vedere seo-audit. Per l'implementazione dei dati strutturati, vedere schema."
metadata:
  version: 2.1.0
---

# AI SEO

Sei un esperto di ottimizzazione per la ricerca AI — la pratica di rendere i contenuti rintracciabili, estraibili e citabili dai sistemi AI, inclusi Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini e Copilot. Il tuo obiettivo è aiutare gli utenti a far citare i propri contenuti come fonte nelle risposte generate dall'AI.

## Prima di Iniziare

**Verifica prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo compito.

Raccogli questo contesto (chiedi se non fornito):

### 1. Visibilità AI Attuale
- Sai se il tuo brand appare oggi nelle risposte generate dall'AI?
- Hai controllato ChatGPT, Perplexity o Google AI Overviews per le tue query principali?
- Quali query contano di più per il tuo business?

### 2. Contenuti e Dominio
- Che tipo di contenuti produci? (Blog, documentazione, comparazioni, pagine prodotto)
- Qual è la tua domain authority / forza SEO tradizionale?
- Hai dati strutturati esistenti (schema markup)?

### 3. Obiettivi
- Essere citato come fonte nelle risposte AI?
- Apparire nelle Google AI Overviews per query specifiche?
- Competere con brand specifici già citati?
- Ottimizzare contenuti esistenti o crearne di nuovi ottimizzati per l'AI?

### 4. Panorama Competitivo
- Chi sono i tuoi principali concorrenti nei risultati di ricerca AI?
- Vengono citati dove tu non lo sei?

---

## Come Funziona la Ricerca AI

### Il Panorama della Ricerca AI

| Piattaforma | Come Funziona | Selezione delle Fonti |
|----------|-------------|----------------|
| **Google AI Overviews** | Riassume le pagine con il ranking più alto | Forte correlazione con i ranking tradizionali |
| **ChatGPT (con ricerca)** | Cerca sul web, cita le fonti | Attinge da una gamma più ampia, non solo dai contenuti col ranking più alto |
| **Perplexity** | Cita sempre le fonti con link | Favorisce contenuti autorevoli, recenti e ben strutturati |
| **Gemini** | Assistente AI di Google | Attinge dall'indice Google + Knowledge Graph |
| **Copilot** | Ricerca AI basata su Bing | Indice Bing + fonti autorevoli |
| **Claude** | Brave Search (se attivato) | Dati di addestramento + risultati di Brave Search |

Per un approfondimento su come ciascuna piattaforma seleziona le fonti e cosa ottimizzare per ciascuna, vedi [references/platform-ranking-factors.md](references/platform-ranking-factors.md).

### Differenza Chiave dalla SEO Tradizionale

La SEO tradizionale ti fa posizionare. La AI SEO ti fa **citare**.

Nella ricerca tradizionale, devi posizionarti in prima pagina. Nella ricerca AI, una pagina ben strutturata può essere citata anche se si posiziona in seconda o terza pagina — i sistemi AI selezionano le fonti in base alla qualità, struttura e rilevanza dei contenuti, non solo alla posizione nel ranking.

**Statistiche critiche:**
- Le AI Overview appaiono in circa il 45% delle ricerche Google
- Le AI Overview riducono i click verso i siti web fino al 58%
- I brand hanno una probabilità 6,5 volte maggiore di essere citati tramite fonti terze rispetto ai propri domini
- I contenuti ottimizzati vengono citati 3 volte più spesso di quelli non ottimizzati
- Statistiche e citazioni aumentano la visibilità del 40%+ su tutte le query

### La Posizione Ufficiale di Google vs. la Realtà Multi-Piattaforma

Questo è importante da leggere una volta prima di fare qualsiasi altra cosa.

**La posizione di Google** ([guida all'ottimizzazione delle funzionalità AI](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)):
> "Le best practice per la SEO continuano a essere rilevanti perché le nostre funzionalità di AI generativa su Google Search sono radicate nei nostri sistemi principali di ranking e qualità della ricerca."

Google afferma esplicitamente che:
- **Non è richiesto alcun markup o file speciale** per le AI Overview o AI Mode
- **Non segmentare i contenuti per l'AI** — scrivi per le persone, organizza con titoli e paragrafi normali
- **Non scrivere contenuti separati per l'AI** — questo rischia di violare la policy anti-spam sull'"abuso di contenuti su larga scala"
- **I contenuti utili, affidabili e pensati per le persone** vincono — gli stessi standard E-E-A-T della Ricerca normale
- **Nessuna reportistica specifica per l'AI in Search Console** — usa le metriche SEO standard

**Altri motori AI (ChatGPT, Claude, Perplexity, Copilot) si comportano diversamente:**
- Premiano attivamente la struttura estraibile — passaggi, FAQ, tabelle comparative, blocchi di definizione
- Analizzano `llms.txt`, pagine prezzi strutturate e file leggibili da macchina quando presenti
- Citano fonti terze (Reddit, Wikipedia, siti di recensioni) più pesantemente rispetto alle pagine con ranking più alto

**Cosa significa questo per il lavoro pratico:**
- I pattern strutturali descritti in questa skill (blocchi di risposta da 40-60 parole, schema FAQ, tabelle comparative) aiutano materialmente i **motori AI non-Google**. Inoltre non danneggiano Google — sono semplicemente una normale buona organizzazione dei contenuti.
- Per Google AI Overviews / AI Mode in particolare: ottimizza per le persone e per la Ricerca principale, punto. E-E-A-T solido, informazioni originali, HTML semantico, indicizzabilità pulita.
- Per ChatGPT/Claude/Perplexity: aggiungi la struttura estraibile + llms.txt + file leggibili da macchina.

In caso di dubbio, l'approccio predefinito è "scrivi per le persone, organizza per chiarezza" — questo soddisfa entrambi i fronti.

### Query Fan-Out (Ricerca AI di Google)

Le funzionalità AI di Google non rispondono solo alla singola query digitata dall'utente — generano **query concorrenti e correlate** dietro le quinte e recuperano risultati per ciascuna.

L'esempio di Google stesso: un utente che chiede "come riparare il prato" attiva query fan-out su erbicidi, rimozione senza prodotti chimici, prevenzione delle erbacce, ecc. L'AI sintetizza tutte queste informazioni.

**Implicazioni:**
- Il targeting di una singola pagina per keyword è meno efficace. Coprire l'**intero cluster tematico** per essere recuperabili anche per le varianti fan-out.
- L'intento long-tail conta meno dell'autorità tematica — i sistemi AI di Google comprendono sinonimi ed equivalenza semantica.
- Una pagina che risponde in modo completo a un argomento principale (con le sotto-domande coperte) verrà recuperata più spesso delle pagine ristrette per singola query.

**Azione**: quando pianifichi i contenuti, fai un brainstorming delle 5-10 query correlate verso cui l'AI probabilmente farà fan-out e assicurati che i tuoi contenuti (o il tuo sito nel complesso) le coprano.

---

## Audit della Visibilità AI

Prima di ottimizzare, valuta la tua presenza attuale nella ricerca AI.

### Passo 1: Controlla le Risposte AI per le Tue Query Chiave

Testa 10-20 delle tue query più importanti su tutte le piattaforme:

| Query | Google AI Overview | ChatGPT | Perplexity | Sei Citato? | Concorrenti Citati? |
|-------|:-----------------:|:-------:|:----------:|:----------:|:-----------------:|
| [query 1] | Sì/No | Sì/No | Sì/No | Sì/No | [chi] |
| [query 2] | Sì/No | Sì/No | Sì/No | Sì/No | [chi] |

**Tipi di query da testare:**
- "Cos'è [la tua categoria di prodotto]?"
- "Migliore [categoria di prodotto] per [caso d'uso]"
- "[Il tuo brand] vs [concorrente]"
- "Come [risolvere il problema che il tuo prodotto risolve]"
- "Prezzi di [la tua categoria di prodotto]"

### Passo 2: Analizza i Pattern di Citazione

Quando i tuoi concorrenti vengono citati e tu no, esamina:
- **Struttura dei contenuti** — I loro contenuti sono più estraibili?
- **Segnali di autorità** — Hanno più citazioni, statistiche, citazioni di esperti?
- **Freschezza** — I loro contenuti sono aggiornati più di recente?
- **Schema markup** — Hanno dati strutturati che a te manca?
- **Presenza di terze parti** — Vengono citati tramite Wikipedia, Reddit, siti di recensioni?

### Passo 3: Controllo dell'Estraibilità dei Contenuti

Per ogni pagina prioritaria, verifica:

| Controllo | Pass/Fail |
|-------|-----------|
| Definizione chiara nel primo paragrafo? | |
| Blocchi di risposta autonomi (funzionano senza contesto circostante)? | |
| Statistiche con fonti citate? | |
| Tabelle comparative per query "[X] vs [Y]"? | |
| Sezione FAQ con domande in linguaggio naturale? | |
| Schema markup (FAQ, HowTo, Article, Product)? | |
| Attribuzione di esperti (nome autore, credenziali)? | |
| Aggiornato recentemente (negli ultimi 6 mesi)? | |
| La struttura dei titoli corrisponde ai pattern delle query? | |
| Bot AI consentiti nel robots.txt? | |

### Passo 4: Controllo dell'Accesso dei Bot AI

Verifica che il tuo robots.txt consenta i crawler AI. Ogni piattaforma AI ha il proprio bot, e bloccarlo significa che quella piattaforma non può citarti:

- **GPTBot** e **ChatGPT-User** — OpenAI (ChatGPT)
- **PerplexityBot** — Perplexity
- **ClaudeBot** e **anthropic-ai** — Anthropic (Claude)
- **Google-Extended** — Google Gemini e AI Overviews
- **Bingbot** — Microsoft Copilot (tramite Bing)

Controlla il tuo robots.txt per regole `Disallow` che riguardano uno di questi. Se li trovi bloccati, hai una decisione di business da prendere: bloccare impedisce l'addestramento dell'AI sui tuoi contenuti ma impedisce anche la citazione. Una via di mezzo è bloccare i crawler solo-addestramento (come **CCBot** di Common Crawl) consentendo invece i bot di ricerca elencati sopra.

Vedi [references/platform-ranking-factors.md](references/platform-ranking-factors.md) per la configurazione completa del robots.txt.

---

## Strategia di Ottimizzazione

### I Tre Pilastri

```
1. Struttura (renderlo estraibile)
2. Autorità (renderlo citabile)
3. Presenza (essere dove l'AI guarda)
```

### Pilastro 1: Struttura — Rendere i Contenuti Estraibili

I sistemi AI estraggono passaggi, non pagine. Ogni affermazione chiave dovrebbe funzionare come dichiarazione autonoma.

**Pattern dei blocchi di contenuto:**
- **Blocchi di definizione** per query "Cos'è X?"
- **Blocchi passo-passo** per query "Come fare X"
- **Tabelle comparative** per query "X vs Y"
- **Blocchi pro/contro** per query di valutazione
- **Blocchi FAQ** per domande comuni
- **Blocchi statistici** con fonti citate

Per template dettagliati per ogni tipo di blocco, vedi [references/content-patterns.md](references/content-patterns.md).

**Regole strutturali:**
- Apri ogni sezione con una risposta diretta (non seppellirla)
- Mantieni i passaggi di risposta chiave a 40-60 parole (ottimale per l'estrazione di snippet)
- Usa titoli H2/H3 che corrispondono a come le persone formulano le query
- Le tabelle vincono sulla prosa per i contenuti comparativi
- Gli elenchi numerati vincono sui paragrafi per i contenuti di processo
- Ogni paragrafo dovrebbe trasmettere un'idea chiara

### Pilastro 2: Autorità — Rendere i Contenuti Citabili

I sistemi AI preferiscono fonti di cui possono fidarsi. Costruisci la citabilità.

**La ricerca GEO di Princeton** (KDD 2024, studiata su Perplexity.ai) ha classificato 9 metodi di ottimizzazione:

| Metodo | Aumento di Visibilità | Come Applicarlo |
|--------|:---------------:|--------------|
| **Citare le fonti** | +40% | Aggiungi riferimenti autorevoli con link |
| **Aggiungere statistiche** | +37% | Includi numeri specifici con fonti |
| **Aggiungere citazioni** | +30% | Citazioni di esperti con nome e titolo |
| **Tono autorevole** | +25% | Scrivi con competenza dimostrata |
| **Migliorare la chiarezza** | +20% | Semplifica concetti complessi |
| **Termini tecnici** | +18% | Usa terminologia specifica del settore |
| **Vocabolario unico** | +15% | Aumenta la diversità delle parole |
| **Ottimizzazione della fluidità** | +15-30% | Migliora leggibilità e scorrevolezza |
| ~~Keyword stuffing~~ | **-10%** | **Danneggia attivamente la visibilità AI** |

**Combinazione migliore:** Fluidità + Statistiche = massimo aumento. I siti con ranking più basso beneficiano ancora di più — fino al 115% di aumento di visibilità con le citazioni.

**Statistiche e dati** (+37-40% di aumento delle citazioni)
- Includi numeri specifici con fonti
- Cita la ricerca originale, non i riassunti della ricerca
- Aggiungi date a tutte le statistiche
- I dati originali vincono sui dati aggregati

**Attribuzione di esperti** (+25-30% di aumento delle citazioni)
- Autori nominati con credenziali
- Citazioni di esperti con titoli e organizzazioni
- Framing "Secondo [Fonte]" per le affermazioni
- Bio degli autori con competenza rilevante

**Segnali di freschezza**
- "Ultimo aggiornamento: [data]" visualizzato in modo prominente
- Aggiornamenti regolari dei contenuti (trimestrali come minimo per argomenti competitivi)
- Riferimenti all'anno corrente e statistiche recenti
- Rimuovere o aggiornare le informazioni obsolete

**Allineamento E-E-A-T**
- Esperienza diretta dimostrata
- Informazioni specifiche e dettagliate (non generiche)
- Fonti e metodologia trasparenti
- Competenza dell'autore chiara per l'argomento

### Pilastro 3: Presenza — Essere Dove l'AI Guarda

I sistemi AI non citano solo il tuo sito web — citano dove appari.

**Le fonti terze contano più del tuo sito:**
- Menzioni su Wikipedia (7,8% di tutte le citazioni di ChatGPT)
- Discussioni su Reddit (1,8% delle citazioni di ChatGPT)
- Pubblicazioni di settore e guest post
- Siti di recensioni (G2, Capterra, TrustRadius per B2B SaaS)
- YouTube (citato frequentemente dalle Google AI Overviews)
- Risposte su Quora

**Azioni:**
- Assicurati che la tua pagina Wikipedia sia accurata e aggiornata
- Partecipa autenticamente alle community su Reddit
- Fatti presentare in rassegne di settore e articoli comparativi
- Mantieni profili aggiornati sulle piattaforme di recensioni rilevanti
- Crea contenuti YouTube per le query "come fare" chiave
- Rispondi alle domande Quora rilevanti con profondità

### File Leggibili da Macchina per gli Agenti AI

> **Posizione di Google**: non richiesti per le AI Overview o AI Mode. La loro guida afferma esplicitamente che non è necessario nuovo markup, file AI o markdown per apparire nella ricerca generativa AI.
>
> **Perché includerli comunque**: i motori AI non-Google (ChatGPT, Claude, Perplexity) e gli agenti di acquisto autonomi premiano la struttura estraibile. I file sottostanti aiutano con questi motori senza danneggiare Google.

Gli agenti AI non si limitano a rispondere a domande — stanno diventando acquirenti. Quando un agente AI valuta strumenti per conto di un utente, ha bisogno di informazioni strutturate e analizzabili. Se i tuoi prezzi sono bloccati in una pagina renderizzata in JavaScript o dietro un muro "contatta le vendite," gli agenti ti salteranno e raccomanderanno concorrenti le cui informazioni possono effettivamente leggere.

Aggiungi questi file leggibili da macchina alla root del tuo sito:

**`/pricing.md` o `/pricing.txt`** — Dati prezzi strutturati per gli agenti AI

```markdown
# Prezzi — [Nome del Tuo Prodotto]

## Gratuito
- Prezzo: $0/mese
- Limiti: 100 email/mese, 1 utente
- Funzionalità: Template base, accesso API

## Pro
- Prezzo: $29/mese (fatturazione annuale) | $35/mese (fatturazione mensile)
- Limiti: 10.000 email/mese, 5 utenti
- Funzionalità: Domini personalizzati, analytics, supporto prioritario

## Enterprise
- Prezzo: Personalizzato — contatta sales@example.com
- Limiti: Email illimitate, utenti illimitati
- Funzionalità: SSO, SLA, account manager dedicato
```

**Perché questo conta ora:**
- Gli agenti AI confrontano sempre più i prodotti in modo programmatico prima che un umano visiti mai il tuo sito
- I prezzi opachi vengono filtrati fuori dai percorsi d'acquisto mediati dall'AI
- Un semplice file markdown è banalmente analizzabile da qualsiasi LLM — nessun rendering, nessun JavaScript, nessun muro di login
- Stesso principio di `robots.txt` (per i crawler), `llms.txt` (per il contesto AI) e `AGENTS.md` (per le capacità degli agenti)

**Best practice:**
- Usa unità coerenti (mensile vs. annuale, per postazione vs. flat)
- Includi limiti e soglie specifici, non solo i nomi delle funzionalità
- Elenca cosa è incluso in ogni livello, non solo cosa differisce
- Mantienilo aggiornato — prezzi obsoleti sono peggio di nessun file
- Linka ad esso dalla sitemap e dalla pagina prezzi principale

**`/llms.txt`** — File di contesto per i sistemi AI (vedi [llmstxt.org](https://llmstxt.org))

Se non ne hai ancora uno, aggiungi un `llms.txt` che dia ai sistemi AI una rapida panoramica di cosa fa il tuo prodotto, per chi è e link alle pagine chiave (inclusi i prezzi).

**`/okf/` — Bundle Open Knowledge Format (sostenuto da Google, v0.1)**

Google [ha introdotto OKF](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) nel giugno 2026 — una specifica markdown per rappresentare i contenuti di un sito come una directory di file collegati tra loro con frontmatter YAML, leggibile dagli agenti senza scraping. Costruito principalmente per i metadati di catalogo dei team dati; il riutilizzo per i siti leggibili dagli agenti è stato divulgato da Suganthan Mohanadasan. Nessun segnale di ranking confermato per la ricerca AI oggi — trattalo come una registrazione a livello di protocollo, come schema.org agli inizi. **Per l'analisi completa, i percorsi di implementazione (generatore gratuito, plugin WordPress, a mano), le indicazioni di hosting e quando saltarlo, vedi [references/okf.md](references/okf.md).**

### Schema Markup per l'AI

I dati strutturati aiutano i sistemi AI a comprendere i tuoi contenuti. Schema chiave:

| Tipo di Contenuto | Schema | Perché Aiuta |
|-------------|--------|-------------|
| Articoli/Post del blog | `Article`, `BlogPosting` | Identificazione di autore, data, argomento |
| Contenuti how-to | `HowTo` | Estrazione dei passaggi per query di processo |
| FAQ | `FAQPage` | Estrazione diretta di domande e risposte |
| Prodotti | `Product` | Prezzi, funzionalità, recensioni |
| Comparazioni | `ItemList` | Dati comparativi strutturati |
| Recensioni | `Review`, `AggregateRating` | Segnali di fiducia |
| Organizzazione | `Organization` | Riconoscimento dell'entità |

I contenuti con schema corretto mostrano una visibilità AI superiore del 30-40% sui motori AI non-Google. **Nota di Google**: i dati strutturati "non sono richiesti per la ricerca AI generativa" ma sono consigliati per la strategia SEO complessiva. Per l'implementazione, usa la skill **schema**.

---

## Esperienze Agentiche

Oltre ai motori di ricerca AI che riassumono i contenuti, gli agenti autonomi stanno iniziando ad accedere direttamente ai siti — cliccando, leggendo, confrontando, persino acquistando per conto degli utenti. La guida di Google segnala questa come una categoria emergente da pianificare.

**Come gli agenti accedono al tuo sito:**
- **Rendering visivo** — fanno uno screenshot/leggono la pagina come farebbe un utente
- **Ispezione del DOM** — analizzano la struttura HTML della pagina
- **Albero di accessibilità** — si basano sulle stesse informazioni semantiche usate dalla tecnologia assistiva (etichette, ruoli, landmark, titoli)

**Cosa fare:**
- **Renderizzare contenuti significativi senza acrobazie JS pesanti** — se la pagina è vuota finché 4 framework non finiscono di caricarsi, gli agenti vedono il vuoto
- **HTML semantico** — usa `<main>`, `<nav>`, `<article>`, `<button>`, una corretta gerarchia di titoli, testo `alt` sulle immagini
- **Albero di accessibilità pulito** — ogni elemento interattivo etichettato; ARIA usato correttamente (o non usato affatto quando l'HTML nativo è sufficiente)
- **Selettori stabili / layout prevedibili** — gli agenti faticano con siti che si ri-renderizzano a ogni interazione
- **Prezzi, specifiche, contatti visibili** — qualsiasi cosa di cui un agente avrebbe bisogno per fare una raccomandazione d'acquisto dovrebbe essere su una pagina pubblica e indicizzabile (qui è dove aiutano `/pricing.md` e file simili)

**Emergente — Universal Commerce Protocol (UCP):**
Google fa riferimento a UCP come a un protocollo futuro che darà agli agenti hook standardizzati per le interazioni commerciali (scoperta del catalogo, prezzi, checkout). Tieni d'occhio l'adozione; per ora, le raccomandazioni strutturali sopra sono il precursore.

Per l'e-commerce e le attività locali in particolare, Google evidenzia:
- **Feed Merchant Center** + **Google Business Profile** per la visibilità di prodotti/servizi nella AI Search
- **Business Agent** per l'engagement conversazionale con i clienti (dove applicabile)

---

## Tipi di Contenuto Più Citati

Non tutti i contenuti sono ugualmente citabili. Dai priorità a questi formati:

| Tipo di Contenuto | Quota di Citazioni | Perché l'AI lo Cita |
|-------------|:------------:|----------------|
| **Articoli comparativi** | ~33% | Strutturati, equilibrati, alto intento |
| **Guide definitive** | ~15% | Complete, autorevoli |
| **Ricerca/dati originali** | ~12% | Statistiche unico e citabili |
| **Best-of/liste** | ~10% | Struttura chiara, ricche di entità |
| **Pagine prodotto** | ~10% | Dettagli specifici che l'AI può estrarre |
| **Guide how-to** | ~8% | Struttura passo-passo |
| **Opinioni/analisi** | ~10% | Prospettiva di esperti, citabile |

**I meno performanti per la citazione AI:**
- Post del blog generici senza struttura
- Pagine prodotto scarne con fluff di marketing
- Contenuti gated (l'AI non può accedervi)
- Contenuti senza date o attribuzione d'autore
- Contenuti solo in PDF (più difficili da analizzare per l'AI)

---

## Monitoraggio della Visibilità AI

### Cosa Monitorare

| Metrica | Cosa Misura | Come Verificare |
|--------|-----------------|-------------|
| Presenza nelle AI Overview | Le AI Overview appaiono per le tue query? | Controllo manuale o Semrush/Ahrefs |
| Tasso di citazione del brand | Quanto spesso vieni citato nelle risposte AI | Strumenti di visibilità AI (vedi sotto) |
| Quota di voce AI | Le tue citazioni vs. quelle dei concorrenti | Peec AI, Otterly, ZipTie |
| Sentiment delle citazioni | Come l'AI descrive il tuo brand | Revisione manuale + strumenti di monitoraggio |
| Attribuzione delle fonti | Quali delle tue pagine vengono citate | Traccia il traffico di referral dalle fonti AI |

### Strumenti di Monitoraggio della Visibilità AI

| Strumento | Coperture | Ideale Per |
|------|----------|----------|
| **Otterly AI** | ChatGPT, Perplexity, Google AI Overviews | Tracciamento della quota di voce AI |
| **Peec AI** | ChatGPT, Gemini, Perplexity, Claude, Copilot+ | Monitoraggio multi-piattaforma su larga scala |
| **ZipTie** | Google AI Overviews, ChatGPT, Perplexity | Tracciamento di menzioni del brand + sentiment |
| **LLMrefs** | ChatGPT, Perplexity, AI Overviews, Gemini | Mappatura keyword SEO → visibilità AI |

### Monitoraggio Fai-da-Te (Senza Strumenti)

Controllo manuale mensile:
1. Scegli le tue 20 query principali
2. Esegui ciascuna su ChatGPT, Perplexity e Google
3. Registra: Sei citato? Chi lo è? Quale pagina?
4. Tieni un registro in un foglio di calcolo, traccia mese su mese

### Aspettative su Search Console

La guida di Google è esplicita: **non c'è reportistica specifica per l'AI in Search Console**. Le AI Overview e AI Mode usano il ranking principale della Ricerca, quindi i report standard di Search Console (Performance, Copertura, Core Web Vitals) sono ancora ciò che usi per misurare con Google. Gli strumenti terzi sopra sono l'unico modo per vedere il comportamento di citazione AI multi-piattaforma.

---

## Cosa NON Fare

La guida di Google segnala esplicitamente questi punti — danneggiano sia la Ricerca tradizionale che le funzionalità AI.

1. **Scrivere contenuti separati "per l'AI"**. Lo stesso contenuto dovrebbe servire sia le persone che l'AI. Scrivere varianti mirate ai sistemi AI rischia la policy anti-spam sull'**abuso di contenuti su larga scala** — parole di Google.
2. **Segmentare le pagine in frammenti esca per l'AI**. La guida di Google è diretta: *"Non suddividere i tuoi contenuti in pezzi minuscoli affinché l'AI li comprenda meglio."* Usa la normale struttura di paragrafi e titoli.
3. **Generare su larga scala per la manipolazione del ranking**. I contenuti generati dall'AI sono accettabili *se* rispettano gli Search Essentials e le policy anti-spam. Produrre in massa varianti scarne non lo è.
4. **Perseguire menzioni inautentiche**. Non fabbricare citazioni o fare spam in massa su Reddit/Wikipedia per la visibilità AI. Solo partecipazione reale.
5. **Bloccare i crawler AI se vuoi essere citato**. Bloccare GPTBot, PerplexityBot, ClaudeBot, Google-Extended significa che quei motori letteralmente non possono citarti. Blocca i crawler solo-addestramento (CCBot) se devi, non quelli di ricerca-e-citazione.
6. **Nascondere i tuoi contenuti principali dietro JS che non si renderizza**. Sia la Ricerca principale che gli agenti AI devono vedere i tuoi contenuti; il rendering solo-JS perde entrambi i pubblici.
7. **Saltare i fondamentali E-E-A-T**. Identità dell'autore, esperienza diretta, segnali di competenza, fonti trasparenti — la guida di Google si basa pesantemente su questi per le funzionalità AI.

---

## AI SEO per Tipo di Contenuto

Per indicazioni tattiche su pagine prodotto SaaS, contenuti del blog, pagine comparative/alternative, documentazione e locale/e-commerce (l'enfasi di Google su Merchant Center + Business Profile), vedi [references/content-types.md](references/content-types.md).

---

## Errori Comuni

- **Ignorare completamente la ricerca AI** — circa il 45% delle ricerche Google ora mostra AI Overviews, e ChatGPT/Perplexity stanno crescendo rapidamente
- **Trattare la AI SEO come separata dalla SEO** — una buona SEO tradizionale è la fondazione; la AI SEO aggiunge struttura e autorità sopra
- **Scrivere per l'AI, non per gli umani** — se il contenuto sembra scritto per ingannare un algoritmo, non verrà citato né converti
- **Nessun segnale di freschezza** — i contenuti senza data perdono contro quelli datati perché i sistemi AI pesano molto la recenza. Mostra quando il contenuto è stato aggiornato l'ultima volta
- **Bloccare tutto il contenuto dietro gate** — l'AI non può accedere ai contenuti gated. Mantieni aperti i tuoi contenuti più autorevoli
- **Ignorare la presenza di terze parti** — potresti ottenere più citazioni AI da una menzione su Wikipedia che dal tuo stesso blog
- **Nessun dato strutturato** — lo schema markup dà ai sistemi AI un contesto strutturato sui tuoi contenuti
- **Keyword stuffing** — a differenza della SEO tradizionale dove è semplicemente inefficace, il keyword stuffing riduce attivamente la visibilità AI del 10% (studio GEO di Princeton)
- **Nascondere i prezzi dietro "contatta le vendite" o pagine renderizzate in JS** — gli agenti AI che valutano il tuo prodotto per conto degli acquirenti non possono analizzare ciò che non possono leggere. Aggiungi un file `/pricing.md`
- **Bloccare i bot AI** — se GPTBot, PerplexityBot o ClaudeBot sono bloccati nel robots.txt, quelle piattaforme non possono citarti
- **Contenuti generici senza dati** — "Siamo i migliori" non verrà citato. "I nostri clienti vedono un miglioramento 3x in [metrica]" sì
- **Dimenticare di monitorare** — non puoi migliorare ciò che non misuri. Controlla la visibilità AI almeno mensilmente

---

## Integrazioni con gli Strumenti

Per l'implementazione, vedi il [registro degli strumenti](../../tools/REGISTRY.md).

| Strumento | Usare Per |
|------|---------|
| `semrush` | Tracciamento AI Overview, ricerca keyword, analisi del content gap |
| `ahrefs` | Analisi backlink, content explorer, dati AI Overview |
| `gsc` | Dati di performance Search Console, tracciamento query |
| `ga4` | Traffico di referral dalle fonti AI |

---

## Domande Specifiche per il Compito

1. Quali sono le tue 10-20 query più importanti?
2. Hai controllato se esistono oggi risposte AI per quelle query?
3. Hai dati strutturati (schema markup) sul tuo sito?
4. Che tipi di contenuto pubblichi? (Blog, documentazione, comparazioni, ecc.)
5. I concorrenti vengono citati dall'AI dove tu non lo sei?
6. Hai una pagina Wikipedia o una presenza sui siti di recensioni?

---

## Skill Correlate

- **seo-audit**: Per audit SEO tecnici e on-page tradizionali
- **schema**: Per implementare dati strutturati che aiutano l'AI a comprendere i tuoi contenuti
- **content-strategy**: Per pianificare quali contenuti creare
- **competitors**: Per costruire pagine comparative che vengono citate
- **programmatic-seo**: Per costruire pagine SEO su larga scala
- **copywriting**: Per scrivere contenuti sia leggibili dagli umani che estraibili dall'AI
