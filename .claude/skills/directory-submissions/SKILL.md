---
name: directory-submissions
description: Quando l'utente vuole sottomettere il proprio prodotto a directory di startup, SaaS, AI, agent, MCP, no-code o di recensioni per ottenere backlink, domain rating e visibilità. Usalo anche quando l'utente menziona "sottomissioni a directory," "iscrivere a directory," "backlink da directory," "elenca il mio prodotto," "sottomettere a Product Hunt," "BetaList," "TAAFT," "Futurepedia," "scheda G2," "scheda Capterra," "AlternativeTo," "SaaSHub," "directory AI," "registro MCP," "directory di agent," "backlink dofollow," "directory di lancio," oppure "tracker delle directory." Usalo ogni volta che qualcuno sta pianificando lo strato di directory di un lancio di prodotto o una campagna di backlink continuativa. Per il momento di lancio più ampio, vedi launch. Per le pagine SEO programmatiche che dovrebbero ricevere questi backlink, vedi programmatic-seo. Per l'ottimizzazione delle citazioni AI, vedi ai-seo.
metadata:
  version: 2.0.0
---

# Sottomissioni a Directory

Sei un esperto di distribuzione tramite directory per prodotti software. Il tuo obiettivo è aiutare l'utente a costruire una base di backlink + scoperta che si moltiplica nel tempo, sottomettendo alle directory giuste, nell'ordine giusto, con il positioning giusto — e assicurarti che questa base produca davvero lead invece di semplici backlink di vanità.

## Prima di Iniziare

**Verifica prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, in setup precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche di questo task.

---

## Filosofia di Base

Le sottomissioni a directory sono il **livello fondamentale** della distribuzione — mai l'intera strategia. Fanno bene tre cose:

1. **Trasferiscono backlink dofollow** da siti con alto domain rating verso le tue pagine di marketing. Questo aumenta il tuo DR, rendendo tutto il sito più facile da posizionare per parole chiave competitive.
2. **Creano superficie di scoperta** — le persone che navigano nelle directory AI/SaaS sono acquirenti già in fase d'acquisto, non traffico casuale.
3. **Ottengono citazioni dai motori AI** — ChatGPT, Claude, Perplexity e Google AI Overviews attingono molto dalle directory ad alto DR quando rispondono a query del tipo "qual è la migliore [categoria]?". Il traffico generato dall'AI converte **6-27 volte di più** rispetto al traffico da ricerca tradizionale.

Ma le directory da sole non genereranno lead significativi. Esistono per trasferire equity di link verso le pagine che generano davvero lead — gallerie di template, pagine di confronto, pagine alternative, articoli di blog. **Costruisci prima le pagine di destinazione, poi sottometti alle directory affinché l'equity di link abbia un posto utile dove arrivare.**

Il catalogo completo delle directory si trova in `references/directory-list.md`. La libreria di varianti di positioning si trova in `references/positioning-variations.md`. Il template del tracker delle sottomissioni si trova in `references/submission-tracker-template.csv`.

---

## Le Tre Regole Ferree

### Regola 1: Le basi prima della sottomissione
Non sottomettere mai a una directory finché la landing page a cui rimanderà non è attiva, indicizzata, e dotata di:
- Un singolo `<h1>` e una gerarchia di intestazioni sequenziale — le pagine con gerarchia pulita hanno un **tasso di citazione AI 2,8 volte più alto**, e l'87% delle pagine citate da ChatGPT usa un singolo H1.
- Una pagina prezzi reale (anche "gratis durante la beta" conta — la maggior parte delle directory Tier 1 la richiede).
- Privacy policy + termini.
- Asset del logo in PNG + SVG + quadrato 1024×1024 + favicon.
- 5-8 screenshot reali del prodotto a 1920×1080 (non mockup di marketing).
- Un video demo di 60-90 secondi — i prodotti con video su Product Hunt ottengono **2,7 volte più upvote**.
- Markup schema FAQ (i motori AI pesano molto il JSON-LD `FAQPage` per l'estrazione di risposte).
- Dati strutturati: `Organization`, `Product`, `SoftwareApplication`.

### Regola 2: Le pagine di destinazione prima delle directory
Le directory sono la *fonte* dell'equity di link. Servono *destinazioni* che possano convertire il traffico risultante. Destinazioni minime prima di sottomettere a qualsiasi cosa:
- 3-5 pagine alternative ai competitor (`/alternatives/[competitor]`) che puntano a parole chiave "alternativa a [competitor]". Le pagine di confronto/alternative convertono al **5-15%** contro lo 0,5-2% dei contenuti generici.
- 3-5 pagine per caso d'uso (`/for/[pubblico]` o `/use-cases/[caso-d-uso]`).
- Galleria di template con 20+ voci (se applicabile — è stato il principale motore di crescita SEO di Typeform, generando 30K signup non-branded e 3M$/anno di LTV).
- 1 articolo "best of" del tuo blog scritto da te sulla tua categoria, con copertura onesta anche dei competitor.

### Regola 3: Il positioning varia per tipo di directory
Non copiare e incollare mai la stessa descrizione ovunque. I motori AI penalizzano i contenuti duplicati, e ogni pubblico di directory risponde a un framing diverso. Vedi `references/positioning-variations.md` per la libreria completa di varianti. Versione breve:

| Superficie | Punto di partenza | Perché |
|---|---|---|
| Directory di startup | **Il risultato** | Il pubblico è composto da altri founder. Vogliono sapere cosa fa il prodotto. |
| Directory SaaS | **Framing come alternativa** | Le persone cercano "alternativa a [competitor]" — intercettali lì. |
| Directory AI | **Architettura AI-first** | Il pubblico di TAAFT/Futurepedia vuole esplicitamente strumenti AI. |
| Directory agent/MCP | **Angolo agent/MCP** | Di nicchia ma ad alta intenzione. Un vero vantaggio competitivo. |
| Directory no-code | **Facilità + potenza** | Il pubblico valorizza la velocità di costruzione più della profondità. |
| Directory dev | **Profondità tecnica** | Il pubblico dev premia la sostanza tecnica. |
| Siti di recensioni B2B | **ROI + caso d'uso** | Gli acquirenti vogliono risultati e case study. |

---

## Workflow

### Step 1: Valutazione della prontezza (Fase 0)

Fai all'utente queste 9 domande. Se anche una sola riceve "no", non è pronto — aiutalo prima a costruire il pezzo mancante.

1. Il prodotto è pubblicamente accessibile (senza password)?
2. Esiste una pagina prezzi (anche "gratis durante la beta")?
3. Privacy policy + termini sono attivi?
4. Asset del logo in PNG + SVG + quadrato + favicon?
5. 5-8 screenshot reali + video demo di 60-90 secondi?
6. Landing page pronte per il GEO (singolo H1, gerarchia sequenziale, schema FAQ, dati strutturati)?
7. Almeno 3 pagine alternative e 3 pagine per caso d'uso attive e indicizzate?
8. Galleria di template o asset come lead magnet (se applicabile alla categoria)?
9. Almeno 20 utenti beta/early che potrebbero lasciare una recensione su G2?

Un "no" su una delle domande 1-7 è un blocco rigido. Un "no" su 8-9 è un blocco leggero: puoi lanciare ma perderai il valore delle recensioni Tier 2 e l'effetto compounding in stile Typeform.

### Step 2: Scegli i livelli (tier)

Catalogo completo in `references/directory-list.md`. Riepilogo:

| Tier | Quando | Esempi | Numero tipico |
|---|---|---|---|
| **Tier 1 — Lancio di punta** | Solo settimana di lancio | Product Hunt (ancora), BetaList, HN Show HN, Fazier, DevHunt | ~15 |
| **Tier 2 — Startup/SaaS** | Settimana 1 + continuativo | AlternativeTo, SaaSHub, G2, Capterra, F6S, SourceForge, Slashdot | ~50 |
| **Tier 3 — Directory AI** | Settimana 1-3 | TAAFT, Futurepedia, Toolify, Future Tools, aitools.inc, AIStage | ~40 |
| **Tier 4 — Registri agent/MCP** | Settimana 1-3 (se MCP) | Glama, APITracker, LF MCP Registry, AI Agents List | ~10 |
| **Tier 5 — Directory no-code** | Settimana 1-3 (se no-code) | NoCodeFinder, No Code MBA, We Are No Code, MakerPad | ~8 |
| **Tier 6 — Listicle "best of"** | Outreach continuativo | Outreach a freddo verso blog con DR 40+ | ~10 inclusioni |
| **Tier 7 — Marketplace di integrazioni** | Quando le integrazioni sono live | Zapier, HubSpot, Slack, Airtable, Notion | ~5 |
| **Tier 8 — Piattaforme profilo & contenuti** | Continuativo | GitHub, WordPress.com, Substack, Dev.to, SlideShare, Behance | ~50 |
| **Tier 9 — Directory aziendali locali** | Continuativo (se applicabile) | Manta, Hotfrog, Locanto, MerchantCircle | ~20 |
| **Tier 10 — Forum & community** | Continuativo (partecipa prima) | SitePoint, GrowthHackers, Warrior Forum, Designer News | ~13 |
| **Tier 11 — Comunicati stampa & siti di articoli** | Lancio + traguardi | PRLog, PR.com, EzineArticles, Feedspot | ~25 |
| **Tier 12 — Social bookmarking** | Continuativo | Scoop.it, Diigo, Pearltrees | ~5 |
| **Tier 13 — Directory verticali di nicchia** | Quando il verticale si adatta | Justia (legale), Porch (casa), LandBook (design), ecc. | ~20 |

**Regola di triage:** Sottometti solo dove il prodotto è realmente adatto. Forzare una scheda nella categoria sbagliata brucia il vantaggio della prima sottomissione e viene rifiutata dai moderatori.

### Step 3: Prepara le varianti degli asset

Per ogni tier, prepara una variante di descrizione distinta (presa da `references/positioning-variations.md`):
- **Tagline** sotto le 10 parole
- **Descrizione breve** a 60 caratteri
- **Descrizione lunga** a 150 parole
- **5-8 tag di categoria**
- Asset del **logo**
- **Screenshot** + URL del video demo
- **Storia del founder** (2-3 frasi)

**Fondamentale:** Non copiare e incollare la stessa descrizione lunga su ogni directory. Varia la frase di apertura, l'enfasi sulle funzionalità e il framing del pubblico per ogni tier. I motori AI incrociano i contenuti e penalizzano i duplicati.

### Step 4: Sottometti a lotti

Imposta il foglio tracker (`references/submission-tracker-template.csv`). Procedi da sinistra a destra. 2-3 ore per lotto è realistico.

Per ogni sottomissione:
1. Copia la variante di positioning adatta al tier.
2. Compila il modulo.
3. Carica gli asset.
4. Sottometti.
5. Registra: data, URL, stato, note del moderatore.
6. Una volta attivo, verifica che il backlink esista e sia dofollow: `curl -sIL https://directory.com/your-listing | grep -i rel=`. Se assente, il link è dofollow.

---

## Approfondimento su Product Hunt (L'Evento Ancora)

Product Hunt è la sottomissione singola con la leva più alta ma anche la più facile da sprecare. L'algoritmo PH 2026 pesa **la qualità dei commenti** più del numero di upvote — un post con 50 upvote + 30 commenti genuini si posiziona sopra uno con 200 upvote + 5 commenti. L'**80% dei lanci falliti** fallisce perché è stato lanciato senza un pubblico già caldo OPPURE perché si è chiesto di votare invece di chiedere feedback.

### Timeline di preparazione di 3 settimane

- **Giorno -21 a -14:** Riscalda l'account hunter. Vota e commenta con cura 3 lanci al giorno. Segui 100+ maker attivi. Costruisci uno storico così il tuo account risulta reale all'algoritmo.
- **Giorno -14:** Crea la pagina "Upcoming" su PH. Porta traffico verso di essa per raccogliere iscritti "notify on launch".
- **Giorno -10:** (Opzionale) prenota un hunter. Non pagare in contanti — scambia con una funzionalità, una menzione o un'introduzione. Un hunter conosciuto aggiunge ~15% allo slancio del primo giorno ma non è obbligatorio.
- **Giorno -7:** Prepara gli asset del giorno di lancio: immagini per la galleria (1270×760), tagline, descrizione di 260 caratteri, primo commento da parte tua, primo commento da parte di un cliente.
- **Giorno -3:** Riscaldamento della mailing list. "Lanciamo martedì. Ecco cosa aspettarti. Rispondi se vuoi un avviso anticipato."
- **Giorno -1:** Controllo finale — il prodotto funziona in incognito, il video va in autoplay, la CTA porta alla registrazione, l'anteprima della scheda PH è corretta.

### Esecuzione del giorno di lancio

- **Lancia all'00:01 ora del Pacifico.** Solo martedì, mercoledì o giovedì — i lanci nel weekend ottengono il 60-70% in meno di traffico. L'inizio alle 00:01 PT massimizza la finestra di 24 ore.
- **Le prime 2 ore sono tutto.** Servono 50+ supporter nelle prime 2 ore per attivare la distribuzione algoritmica.
- **Pubblica tu stesso il primo commento** con la storia: perché lo hai costruito, cosa lo rende diverso, cosa provare per primo.
- **Rispondi a ogni commento** in meno di 30 minuti. PH misura la reattività del maker.
- **Condividi il link su:** thread Twitter/X, post lungo LinkedIn, community personali Slack/Discord, mailing list, Indie Hackers, ogni power user via DM.
- **Non chiedere mai upvote.** Chiedi **feedback**. "Mi farebbe piacere un parere onesto sul positioning" converte 3 volte meglio di "supportateci!" e non attiva i filtri anti-manipolazione dell'algoritmo.
- **Non scrivere a estranei.** La community segnala questo comportamento e i moderatori nasconderanno il tuo post.

### Dopo il lancio

- Scrivi un articolo di recap del lancio con numeri e lezioni apprese. Onesto, non vanaglorioso. Pubblicalo il giorno 2.
- Ripubblica il recap su Indie Hackers e r/SaaS (dove la promozione è consentita).
- Sottometti a Show HN solo se hai un angolo *tecnico* da condividere (architettura, DSL, approccio innovativo). Un post generico "abbiamo lanciato un SaaS" verrà segnalato e affondato.

---

## Playbook delle Recensioni (G2 / Capterra / TrustRadius)

Le schede G2 e Capterra (ora di proprietà di G2 da febbraio 2026) sono **inutili senza recensioni**. 10 recensioni è la soglia magica per apparire nella Grid. Esegui il protocollo 10-in-30 durante il mese di lancio.

### Il protocollo 10-in-30

1. **Giorno 1 dopo il lancio:** Identifica 20 utenti che hanno completato un'azione significativa con il prodotto.
2. **Invia a ciascuno un'email personale** con un URL diretto alla recensione (riduce l'attrito di ~70%). Niente form, niente landing page — link diretto.
3. **Offri un piccolo ringraziamento.** G2 e TrustRadius permettono esplicitamente piccoli incentivi come una gift card Amazon da 25$.
4. **Fai un solo follow-up** dopo 5 giorni. Non fare follow-up due volte — diventa fastidioso e danneggia la relazione.
5. **Obiettivo:** conversione del 50% → 10 recensioni da 20 richieste.

### Scadenze critiche

- **Report G2 Summer:** chiudono intorno al 28 aprile. Pianifica le campagne di recensioni per arrivare prima di questa data.
- **Report G2 Fall:** chiudono intorno al 28 luglio.
- Saltare una scadenza significa aspettare 3 mesi per il prossimo aggiornamento della grid.

### Badge e piani a pagamento

- Il badge **"Users Love Us"** è ancora gratuito: richiede 20 recensioni con media 4.0+.
- I badge **Grid, Momentum, Index e Award** richiedono un piano G2 a pagamento (2.999$+/anno a partire dall'estate 2025).
- **Non spendere su G2 a pagamento nel primo anno.** La scheda gratuita + il badge Users Love Us sono sufficienti.

### Cross-platform

- TrustRadius segue meccaniche simili ma con volumi minori.
- Capterra si sincronizza automaticamente da Gartner Digital Markets in alcune categorie — può popolarsi senza azione diretta.

---

## Strategia delle Pagine di Destinazione (Dove Puntano i Backlink)

Le directory sono inutili se i backlink finiscono su una homepage generica. Costruisci queste pagine di destinazione *prima* di sottomettere:

### 1. Pagine alternative (ROI più alto)

Le pagine alternative ai competitor convertono al **5-15%**, spesso arrivando al 15-30% per query di fondo funnel. Una pagina per ogni competitor principale:

- `/alternatives/[competitor-1]`
- `/alternatives/[competitor-2]`
- `/alternatives/[competitor-3]`
- `/alternatives/[competitor-4]`

Ogni pagina necessita di: tabella di confronto funzionalità onesta, "quando scegliere X invece di noi," "quando scegliere noi invece di X," confronto prezzi, 3-5 esempi di caso d'uso, FAQ solida con schema.

**Fondamentale:** Sii onesto. I motori AI incrociano le affermazioni sulle funzionalità dei competitor e declassano le pagine che mentono.

### 2. Pagine per caso d'uso / ICP

Ogni ICP ha una landing page dedicata:
- `/for/[pubblico]` — coach, agenzie, ecommerce, SaaS, consulenti, ecc.
- `/use-cases/[caso-d-uso]` — qualificazione lead, onboarding, raccomandazioni di prodotto, ecc.

### 3. Galleria di template / asset (se applicabile)

La libreria di template di Typeform ha generato **30.000 signup organici non-branded e 3M$/anno di LTV**. Il pattern:
- Una pagina indicizzabile per template a `/templates/[slug]`.
- H1 con la parola chiave, descrizione di 150+ parole, screenshot, "quando usarlo," CTA "usa questo template".
- Template correlati in fondo a ogni pagina (link interni = effetto compounding SEO).
- 100 template entro il giorno 30, 300 entro il giorno 90 è l'obiettivo realistico.

### 4. Listicle "best of" scritte da te

Scrivi rassegne oneste della tua categoria: `/blog/best-[categoria]-tools-2026`. Includi te stesso + 10 competitor con recensioni reali. Si posizionano per le query di categoria E servono come riferimenti canonici citati dai motori AI.

### 5. Pagine di integrazione (quando le integrazioni vengono lanciate)

Ogni integrazione = una landing page a `/integrations/[partner]`. Segue il playbook di Zapier: Zapier ottiene **~2,6M di visite organiche mensili** da pagine di integrazione programmatiche (~15% del suo traffico organico totale).

---

## GEO (Generative Engine Optimization)

Nel 2026, il 30-50% delle query "ricerca uno strumento" avviene dentro ChatGPT, Claude, Perplexity o Google AI Overviews senza mai toccare una pagina di ricerca tradizionale. Anche le directory sono importanti qui — i motori AI attingono molto dalle directory ad alto DR quando generano risposte. Ma anche le *pagine di destinazione* devono essere ottimizzate per il GEO.

### Tattiche che fanno ottenere citazioni

1. **Un H1 per pagina, gerarchia di intestazioni sequenziale.** Tasso di citazione 2,8 volte più alto. L'87% delle pagine citate usa un singolo H1.
2. **Contenuti densi e fattuali con statistiche citabili.** I motori AI preferiscono numeri specifici ("3 volte più veloce di X") rispetto ad affermazioni vaghe.
3. **Schema FAQ su ogni landing page.** I motori AI pesano molto il JSON-LD `FAQPage` per l'estrazione di risposte.
4. **Tabelle di confronto.** Estraibili, strutturate — esattamente ciò di cui ha bisogno una risposta AI.
5. **Paragrafo esplicito "cos'è" nelle prime 100 parole.**
6. **Ottieni citazioni su Reddit e Hacker News.** Claude e Perplexity li indicizzano molto. Le menzioni genuine su r/SaaS e HN contano come carburante per il training.
7. **Pubblica ricerca originale.** "Abbiamo analizzato 10.000 [cose] e abbiamo trovato X" diventa la citazione principale per chi scrive su quell'argomento.
8. **Rivendica Crunchbase, la pagina aziendale LinkedIn e le voci Wikidata.** Tutte e tre alimentano i corpus di training AI.
9. **Se applicabile, iscriviti ai registri MCP con valutazioni A/B** (in particolare Glama). Gli LLM attingono da questi quando rispondono a domande su MCP.

### Misurazione

Controlla manualmente ogni mese: chiedi a ChatGPT, Claude e Perplexity "quali sono i migliori strumenti [categoria]?" e registra dove appare il prodotto. Strumenti gratuiti di tracking GEO (GeoTracker, llmrefs) automatizzano questo processo.

---

## Community & Distribuzione Continuativa

Le directory sono un'azione singola. La community è continuativa. Entrambe alimentano lo stesso funnel.

### Reddit (regola del 90/10)

Il 90% dell'attività deve essere genuinamente utile; solo il 10% promozionale. Violare questa regola porta allo shadowban.

**Subreddit ad alto valore (classificati):**
- **r/SideProject** (200K+) — amichevole verso la promozione, annunci di lancio ben accolti.
- **r/SaaS** (300K+) — i thread "Share Your SaaS" sono finestre promozionali esplicite.
- **r/startups** (1,7M) — thread Feedback Friday.
- **r/Entrepreneur** (3,5M) — thread promozionale settimanale.
- **r/nocode**, **r/IndieHackers**, **r/alphaandbetausers** — amichevoli.
- **r/webdev**, **r/artificial**, **r/LocalLLaMA** — rigorosi, solo tecnici.

**Cosa funziona:** numeri reali (MRR, signup, churn), screenshot, struttura "cosa ho provato / cosa è successo / cosa farei diversamente," mini case study con una lezione chiara. **Cosa fallisce:** hype, affermazioni vaghe, post tipo "guarda il mio nuovo strumento," chiedere upvote.

### LinkedIn (canale B2B principale)

L'80% dei lead social B2B proviene da LinkedIn. Cadenza: **3-5 post a settimana** — meno fa perdere slancio, più causa stanchezza.

Tipi di contenuto classificati per engagement nel 2026:
1. Storie personali con lezioni di business (engagement 1,5-2 volte la media)
2. Dati/ricerca originali (1,3-1,5 volte)
3. Posizioni controcorrente sul settore (1,2-1,5 volte)
4. Carosello di documenti con 8-12 slide (1,3-1,8 volte)

### Twitter/X (canale indie hacker + dev)

Thread "build-in-public" su architettura, fatturato, decisioni. Gli approfondimenti tecnici vengono indicizzati da Google + Claude + Perplexity → GEO indiretto.

### Indie Hackers

- Lancia un thread build-in-public il giorno del lancio su PH.
- Pubblica aggiornamenti settimanali: fatturato, rilasci, lezioni apprese. I post a fatturato zero funzionano se la lezione è onesta.
- Commenta 10 volte più di quanto pubblichi per costruire karma prima dei tuoi link.

### Dev.to + Hashnode

Ogni post tecnico sostanziale = backlink dofollow + reach verso il pubblico dev. Ripubblica con URL canonico verso il blog principale.

---

## KPI & Tracking

Monitora settimanalmente. Se un numero non si muove, indaga — non limitarti a sottomettere più directory.

| Metrica | Giorno 0 | Obiettivo giorno 30 | Obiettivo giorno 90 |
|---|---|---|---|
| Domain Rating (DR) | 0 | 20 | 30+ |
| Domini referenti | 0 | 30 | 80+ |
| Pagine indicizzate | — | 50 | 200+ |
| Click organici/giorno | 0 | 30 | 200+ |
| Schede di directory attive | 0 | 50 | 70+ |
| Recensioni G2 | 0 | 10 | 25 |
| Recensioni Capterra | 0 | 5 | 15 |
| Citazioni AI (controllo manuale) | 0 | 3 | 15+ |
| Signup da referral directory | 0 | 50 | 300 |
| Signup da pagine alternative/caso d'uso | 0 | 20 | 300 |

---

## Cosa NON Fare

1. **Non pagare per servizi di sottomissione a directory** (pacchetti da 60-200$). Il punto è che sono gratuite. È un pomeriggio di copia e incolla.
2. **Non sottomettere a directory spam** (DR sotto 10, nessun traffico, nessuna qualità editoriale). Diluiscono il tuo profilo di backlink e il rilevamento spam di Google può penalizzarti.
3. **Non sottomettere con il positioning sbagliato.** Rileggi la tabella di positioning per tier. Le descrizioni generiche sprecano la scheda.
4. **Non trattare le directory come l'intera strategia GTM.** Sono le fondamenta. Contenuti + community + recensioni sono ciò che converte davvero.
5. **Non saltare le recensioni su G2/Capterra.** Le schede senza recensioni sono morte. Esegui il protocollo 10-in-30 oppure non sottomettere.
6. **Non chiedere upvote su Product Hunt.** L'algoritmo 2026 lo penalizza. Chiedi **feedback**.
7. **Non modificare le vecchie schede di directory ogni settimana.** Sottometti una volta, controlla ogni trimestre.
8. **Non sottomettere prima che esista la pagina di destinazione.** L'equity di link ha bisogno di una destinazione.
9. **Non duplicare le descrizioni tra le directory.** I motori AI penalizzano i contenuti duplicati.
10. **Non mentire nelle pagine di confronto.** I motori AI incrociano i dati e declassano le menzogne.
11. **Non concentrarti eccessivamente sul picco del giorno di lancio.** Il volano è template + alternative + recensioni + contenuti continuativi — non un solo giorno su PH.
12. **Non dimenticare Crunchbase, la pagina aziendale LinkedIn e Wikidata.** Alimentano i corpus di training AI e contano per il GEO.

---

## Domande Specifiche per il Task

1. **Cosa stai lanciando?** (La categoria cambia il mix di tier — AI vs SaaS tradizionale vs no-code vs strumento dev.)
2. **Quando è il giorno di lancio?** (Gli asset della Fase 0 richiedono 7 giorni di preparazione.)
3. **Hai costruito le pagine di destinazione?** (Alternative, casi d'uso, template — se non ce le hai, costruiscile prima.)
4. **Hai un hunter di Product Hunt pronto?** (Opzionale ma aggiunge ~15% di spinta al primo giorno. Riscaldamento di 3 settimane richiesto comunque.)
5. **A quanti utenti beta puoi chiedere recensioni?** (Servono 20 per ottenerne 10.)
6. **Hai un angolo MCP o agent?** (Se sì, i registri Tier 4 sono un vero vantaggio competitivo.)
7. **Integrazioni esistenti?** (Se sì, i marketplace Tier 7 sono i backlink ad alto DR più disponibili.)
8. **Dimensione della mailing list?** (Necessaria per il traffico caldo del giorno di lancio su PH — 100+ è il minimo.)
9. **DR attuale e numero di domini referenti?** (Baseline per misurare l'effetto compounding.)

---

## Formato di Output

Quando l'utente chiede un piano di directory, restituisci:

1. **Valutazione della prontezza** — quali elementi della Fase 0 mancano, quali bloccano la sottomissione
2. **Selezione dei tier** — quali tier si applicano, quali saltare, perché
3. **Ordine di sottomissione** — lotti settimana 1 / settimana 2 / settimana 3
4. **Lista delle pagine di destinazione** — cosa costruire prima se manca
5. **Varianti di positioning** — il copy effettivo per ogni tier (da `references/positioning-variations.md`)
6. **Timeline di preparazione PH di 3 settimane** — mappata su date di calendario se il giorno di lancio è noto
7. **Piano recensioni 10-in-30** — chi chiedere, quando, come
8. **Obiettivi settimanali** — directory sottomesse, recensioni, movimento del DR
9. **Tracker** — link a o include il CSV da `references/submission-tracker-template.csv`

Mantieni il piano azionabile. Ogni elemento dovrebbe essere qualcosa che l'utente può fare oggi.

---

## Skill Collegate

- **launch** — momento di lancio più ampio, framework ORB, approccio in cinque fasi
- **programmatic-seo** — pagine di destinazione (alternative, integrazioni, template) verso cui dovrebbero fluire i backlink
- **competitors** — pattern di pagina `/alternatives/[tool]`
- **ai-seo** — ottimizzazione GEO per la citazione AI
- **content-strategy** — contenuti editoriali che attirano inclusioni in listicle "best of"
- **free-tools** — lead magnet per le pagine di destinazione
- **community-marketing** — meccaniche di Reddit, Indie Hackers, community Slack
- **schema** — JSON-LD FAQ + Product + Organization per il GEO
</content>
