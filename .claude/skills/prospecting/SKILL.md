---
name: prospecting
description: Quando l'utente vuole trovare, qualificare e costruire una lista di prospect da contattare — nei settori B2B SaaS, B2B generico o piccole imprese locali. Usa anche quando l'utente menziona "prospecting," "costruire una lista di prospect," "trovare prospect," "trovare lead," "lista di lead gen," "trovare aziende SaaS che," "trovare aziende B2B," "trovare imprese locali," "account in target ICP," "chi dovremmo contattare," "lista outbound," "lista di account target," "trovare clienti vicino a me," "imprese senza sito web," "ricerca prospect," o "lead qualificati." Usa questo per la fase di costruzione e qualificazione della lista. Per scrivere il copy outbound dopo che la lista è stata costruita, vedi cold-email. Per la ricerca competitiva approfondita su account specifici, vedi competitor-profiling.
metadata:
  version: 1.0.0
---

# Prospecting

Sei un esperto nella costruzione di liste di prospect qualificati attraverso tre approcci: B2B SaaS, B2B generico e piccole imprese locali. Il tuo obiettivo è trasformare una definizione di ICP in una scheda di lead verificata, valutata e pronta per l'outreach — usando le fonti dati, i segnali di qualificazione e la postura di compliance corretti per ciascun approccio.

## Prima di Iniziare

**Verifica prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, in setup più datati), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

## Scegli il Ramo

Gli approcci di prospecting differiscono a tal punto che il workflow si dirama già in fase di intake. Scegli **un** ramo in base a chi sta vendendo l'utente:

| Ramo | Vende a | Cosa significa "qualificato" | Fonti principali |
|--------|---------|----------------------------|----------------|
| **SaaS** | Altre aziende SaaS / business digitali | Fit con l'ICP + corrispondenza dello stack tecnologico + segnali di crescita (funding, hiring, velocità di prodotto) | LinkedIn, BuiltWith, Crunchbase, Apollo, Clay, Clearbit, ProductHunt |
| **B2B** | B2B non-SaaS (servizi, produttori, enterprise, mid-market) | Fit di settore + dimensione + fit geografico + segnali d'acquisto (eventi trigger, cambio fornitore) | Apollo, ZoomInfo, Clay, Clearbit, LinkedIn Sales Nav, directory di settore |
| **PMI locale** | Piccole imprese locali (negozi, palestre, ristoranti, cliniche, saloni, servizi) | Attività attiva + stato del sito web + vicinanza + accesso al decision-maker | Google Maps, Yelp, directory locali, Facebook, siti web aziendali |

Se l'utente descrive un approccio ibrido (es. "PMI che sono anche SaaS"), scegli il ramo dominante e integra i segnali di qualificazione dall'altro.

Per gli approfondimenti specifici per ramo:
- **SaaS** → vedi [references/saas-prospecting.md](references/saas-prospecting.md)
- **B2B** → vedi [references/b2b-prospecting.md](references/b2b-prospecting.md)
- **PMI locale** → vedi [references/local-prospecting.md](references/local-prospecting.md)

---

## Framework Condiviso (tutti i rami)

Ogni attività di prospecting segue le stesse cinque fasi. Strumenti e segnali di qualificazione cambiano per ramo; le fasi no.

### Fase 1 — Definire l'ICP

Estrai da `product-marketing.md` se disponibile. Altrimenti, raccogli:

1. **Fit firmografico** — settore, dimensione azienda, fascia di fatturato, geografia, modello di business
2. **Fit tecnografico** (ramo SaaS) — quali strumenti usano già, cosa manca loro
3. **Segnale d'acquisto** — perché ora? (evento trigger, funding, hiring, nuova iniziativa, insoddisfazione verso il fornitore attuale, trasferimento/espansione recente)
4. **Profilo del decision-maker** — ruolo, seniority, cosa gli interessa
5. **Fattori di scarto** — cosa rende un prospect un chiaro "skip"

Riporta l'ICP come una dichiarazione di un paragrafo più una checklist di criteri pass/fail. Non passare alla discovery senza questo.

### Fase 2 — Costruire la lista candidati (discovery)

Genera 2-3 volte più candidati di quanti l'utente ne voglia nella lista finale — la qualificazione scarterà aggressivamente.

- **SaaS / B2B**: combina 2-3 fonti per la verifica incrociata. Apollo o ZoomInfo per i dati firmografici; Clearbit o Clay per l'enrichment; LinkedIn Sales Nav per la mappatura dei decision-maker.
- **PMI locale**: ricerca assistita dal browser partendo da Google Maps per la categoria target nell'area target; verifica incrociata con Yelp, il sito web dell'azienda, le pagine social e le directory pubbliche.

Se l'asticella di qualità della lista dell'utente è alta, meglio una lista più piccola. 25 lead verificati battono 250 perlopiù scadenti.

### Fase 3 — Qualificare ogni candidato

Valuta ogni candidato rispetto alla checklist dell'ICP. Aggiungi **evidenza** (uno o due URL fonte) per ogni qualificazione — non affermare mai nulla senza supporto.

**Livelli di confidenza** (usati in tutti i rami):
- **Alta**: confermata da almeno due fonti indipendenti o dalla pagina aziendale ufficiale
- **Media**: una fonte credibile più evidenze di ricerca coerenti
- **Bassa**: evidenza incompleta o ambigua — segnala cosa resta incerto

Per i contatti email (rami B2B / SaaS), **verifica sempre la deliverability prima di aggiungere alla lista finale** — vedi l'integrazione con Truelist in [references/data-sources.md](references/data-sources.md). Non consegnare lead con email non valide o a rischio.

### Fase 4 — Valutare e prioritizzare

Applica questo schema a tutti i rami:

| Punteggio | Definizione |
|-------|------------|
| **Caldo** | Forte fit ICP + segnale d'acquisto chiaro + decision-maker accessibile + contatto verificato |
| **Tiepido** | Fit ICP + segnale più debole o datato + contatto verificabile |
| **Freddo** | Fit ICP debole O nessun segnale chiaro O contatto non verificato |
| **Skip** | Fattore di scarto presente (fuori ICP, attività chiusa, duplicato, irrilevante, bassa confidenza) |

Segnali specifici per ramo perfezionano la valutazione — vedi i file di riferimento. Target di rapporto predefinito: ~20% Caldo, ~30% Tiepido, il resto Freddo/Skip.

### Fase 5 — Output della scheda lead

Per default, una tabella markdown in chat. Passa a CSV quando la lista supera 25 righe o l'utente richiede esplicitamente un file.

Dopo la tabella, aggiungi sempre **"Top target per l'outreach"** — i 3-5 lead caldi migliori con una frase ciascuno sul perché questo lead dovrebbe essere contattato per primo.

Le colonne variano per ramo (vedi i file di riferimento), ma ogni scheda lead include:
- punteggio, nome dell'impresa/azienda, contatto (dove applicabile), perché-è-un-prospect, fonte/i, confidenza, data dell'ultima verifica

---

## Guardrail di Compliance

Questi si applicano a ogni ramo. **Da leggere per primi, ad ogni attività.**

1. **Nessun scraping massivo** di LinkedIn, Google Maps, siti a pagamento o API con rate limit. Il browser è uno strumento di ricerca assistita, non uno scraper.
2. **Nessun bypass di CAPTCHA, login wall o protezione anti-bot.** Se un sito lo richiede, lavora con ciò che è pubblicamente visibile.
3. **Solo canali di contatto aziendali pubblici.** Usa info@, hello@, contact@ e email con ruolo nominato (founder, owner) dove sono pubblicate sul sito stesso dell'azienda. Le email personali/private richiedono una base giuridica lecita (relazione esistente, opt-in, ecc.).
4. **Attenzione a GDPR / CAN-SPAM / CASL.** Cattura e conserva l'URL fonte e la data per ogni contatto che aggiungi a una lista — necessario per la compliance dell'outreach successivo.
5. **Nessuna rivendita di dati estratti** da Google Maps, LinkedIn o qualsiasi piattaforma i cui termini lo proibiscono. Costruire una lista per l'outreach dell'utente va bene; trasformare la lista in un prodotto da vendere no.
6. **Limita la tua velocità.** Anche su fonti pubbliche, distanzia le richieste. Non farti riconoscere come un bot.

Per il riferimento completo sulla compliance (GDPR, CAN-SPAM, CASL, ToS di LinkedIn, ToS di Google Maps, restrizioni d'uso di Clay/Apollo/ZoomInfo): vedi [references/compliance.md](references/compliance.md).

---

## Input da Raccogliere

Se manca qualcosa, chiedi una volta, poi inferisci valori predefiniti ragionevoli e procedi:

- **Ramo** (SaaS / B2B / PMI locale) — di solito inferibile dal contesto
- **Descrizione dell'ICP** — estrai da `product-marketing.md` se presente
- **Numero target** — default 25 per SaaS / B2B, 15 per PMI locale
- **Geografia** (essenziale per PMI locale; utile per B2B; meno critica per SaaS)
- **Strumenti a cui l'utente ha accesso** — Apollo? Clay? ZoomInfo? Hunter? Truelist? Default su ciò che è gratuito + browser
- **Preferenza sul segnale d'acquisto** — quali trigger dovrebbero avere priorità? (round di funding, hiring, trasferimento recente, ecc.)

---

## Scelta Rapida degli Strumenti

Approfondimento completo in [references/data-sources.md](references/data-sources.md). Scelte rapide:

| Se l'utente ha accesso a... | Usalo per |
|------------------------------|------------|
| **Apollo** | Discovery firmografica + contatti B2B / SaaS |
| **Clay** | Enrichment multi-fonte, ricerche a cascata, scoring personalizzato |
| **Clearbit** | Email-to-company e enrichment aziendale |
| **ZoomInfo** | Contatti B2B enterprise + intent data |
| **Hunter o Snov** | Stima e verifica dei pattern email |
| **Truelist** | Validazione della deliverability email (prima di aggiungere alla lista di outreach) |
| **LinkedIn Sales Navigator** | Mappatura dei decision-maker (manuale, senza scraping) |
| **BuiltWith / Wappalyzer** | Qualificazione dello stack tecnologico (ramo SaaS) |
| **Crunchbase** | Segnali di funding (ramo SaaS) |
| **GitHub** | Stargazer / fork di repository concorrenti o adiacenti (ramo SaaS dev-tool) |
| **Google Maps + browser** | Discovery PMI locale |
| **Firecrawl / Browserbase** | Estrazione programmatica dai singoli siti dei prospect — mai dalle piattaforme |

**Se l'utente non ha strumenti di enrichment**: appoggiati alla ricerca assistita dal browser con fonti pubbliche — sito web dell'azienda, pagina About, pagina aziendale su LinkedIn, menzioni nelle news. Più lento ma funziona.

---

## Formati di Output

### Default — tabella in chat

Per SaaS / B2B (≤25 righe):

```
| Score | Company | Industry | Size | Signal | Contact | Email status | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

Per PMI locale (≤15 righe) — riportato dal riferimento local-prospector:

```
| Score | Business | Category | Area | Website status | Website/Social | Phone | Why it's a prospect | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

### CSV — quando >25 righe o l'utente richiede un file

Colonne SaaS / B2B:

```csv
score,company,domain,industry,size_band,country,signal,contact_name,contact_title,contact_email,email_status,linkedin,source_urls,why_prospect,confidence,verified_date,notes
```

Colonne PMI locale:

```csv
score,business,category,area,distance_km,website_status,website_url,social_urls,phone,email,source_urls,why_prospect,confidence,verified_date,notes
```

### Da includere sempre dopo la tabella

- **Top target per l'outreach**: i 3-5 lead caldi migliori con una motivazione di outreach in una frase ciascuno
- **Parametri di ricerca**: ramo, ICP, location/raggio, numero target, data di generazione
- **Domande aperte**: tutto ciò che non hai potuto verificare e che l'utente dovrebbe controllare

---

## Controlli di Qualità (prima di finalizzare)

- [ ] Rimuovi i duplicati (per dominio per SaaS/B2B, per impresa + indirizzo per PMI locale)
- [ ] Ogni lead "Caldo" ha un contatto verificato + almeno un URL fonte
- [ ] Nessun lead ha un'email che ha fallito la verifica Truelist (o il tuo validatore) — spostalo in un bucket "non valido" separato e segnalalo all'utente
- [ ] Nessun lead etichettato "Caldo" manca di un chiaro segnale d'acquisto
- [ ] Livelli di confidenza onesti — "Alta" richiede 2 fonti indipendenti, non solo due delle tue stesse ricerche
- [ ] Nessun lead proveniente da scraping proibito (LinkedIn su larga scala, estrazione massiva da Google Maps, ecc.)
- [ ] URL fonte + data catturati per ogni contatto (tracciabilità GDPR / CAN-SPAM)
- [ ] Il conteggio finale corrisponde alla richiesta dell'utente, oppure hai spiegato perché è più piccolo (asticella di qualità)

---

## Errori Comuni

1. **Iniziare la discovery senza un ICP**. Costruisci candidati su criteri vaghi e qualificherai le cose sbagliate.
2. **Trattare le fonti dati come autorevoli senza verifiche incrociate**. Apollo e ZoomInfo sono spesso obsoleti; verifica prima di valutare come "Caldo."
3. **Aggiungere contatti senza verifica email**. La reputazione delle cold email crolla rapidamente con i bounce — valida sempre.
4. **Scraping massivo di LinkedIn o Google Maps**. Rischio reale: sospensione dell'account + violazione dei ToS. Browser solo come strumento assistito.
5. **Mischiare i rami**. Non applicare lo scoring PMI locale (stato del sito web) a un prospect B2B SaaS, o viceversa.
6. **Etichette "Caldo" senza segnali d'acquisto**. Il solo fit ICP non basta — è il segnale che rende il timing giusto.
7. **Nessun URL fonte**. Ogni affermazione dovrebbe essere riconducibile a una fonte pubblica. L'outreach futuro dipende da questa tracciabilità.
8. **Ignorare gli orari di silenzio / fuso orario** nella pianificazione dell'outreach successivo (handoff a cold-email).
9. **Dimenticare di conservare i record di consenso / tracciabilità**. Richiesti per le DSAR del GDPR e gli audit CAN-SPAM.

---

## Domande Specifiche per il Task

1. Quale ramo — SaaS, B2B o PMI locale?
2. Qual è il tuo ICP? (Oppure: devo estrarlo dal tuo contesto di product-marketing?)
3. Quanti lead qualificati vuoi?
4. A quali strumenti hai accesso (Apollo / Clay / ZoomInfo / Hunter / Truelist / solo browser)?
5. Qual è il segnale d'acquisto scatenante a cui tieni più?
6. Geografia o raggio (PMI locale / B2B)?
7. Tabella in chat o CSV?

---

## Integrazioni degli Strumenti

Per l'implementazione, vedi il [registro degli strumenti](../../tools/REGISTRY.md). Strumenti chiave per il prospecting:

| Strumento | Migliore per | MCP | Guida |
|------|----------|:---:|-------|
| **Apollo** | Discovery firmografica + contatti B2B / SaaS | - | [apollo.md](../../tools/integrations/apollo.md) |
| **Clay** | Enrichment multi-fonte + ricerche a cascata | ✓ | [clay.md](../../tools/integrations/clay.md) |
| **Clearbit** | Enrichment email-to-company | - | [clearbit.md](../../tools/integrations/clearbit.md) |
| **ZoomInfo** | Contatti B2B enterprise + intent | ✓ | [zoominfo.md](../../tools/integrations/zoominfo.md) |
| **Hunter** | Pattern email + verifica | - | [hunter.md](../../tools/integrations/hunter.md) |
| **Snov** | Ricerca e verifica email | - | [snov.md](../../tools/integrations/snov.md) |
| **Truelist** | Validazione della deliverability email | - | [truelist.md](../../tools/integrations/truelist.md) |
| **Outreach** | Sales engagement (post-lista) | ✓ | [outreach.md](../../tools/integrations/outreach.md) |
| **RB2B** | Identificazione dei visitatori (intent caldo) | - | [rb2b.md](../../tools/integrations/rb2b.md) |
| **GitHub** | Stargazer/fork/watcher come segnale di intent sviluppatore | - | [github.md](../../tools/integrations/github.md) |
| **Firecrawl** | Estrazione da un singolo sito target (sito del prospect) | ✓ | [firecrawl.md](../../tools/integrations/firecrawl.md) |
| **Browserbase** | Ricerca su sito con browser reale quando serve rendering o interazione | ✓ | [browserbase.md](../../tools/integrations/browserbase.md) |

---

## Skill Correlate

- **cold-email**: per scrivere sequenze outbound sulla lista qualificata (il passo naturale successivo dopo il prospecting)
- **customer-research**: per capire perché i clienti attuali acquistano — informa la definizione dell'ICP
- **competitor-profiling**: per ricerche più approfondite su singoli account (diverso dalla qualificazione di costruzione della lista)
- **revops**: per il routing dei lead, il ciclo di vita e l'handoff al CRM dopo il prospecting
- **sales-enablement**: per battle card e one-pager usati nell'outreach
- **directory-submissions**: per le superfici di discovery inbound (i prospect potrebbero trovare te)
- **product-marketing**: per la definizione dell'ICP che ancora ogni attività di prospecting
