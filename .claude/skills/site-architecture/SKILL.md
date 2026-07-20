---
name: site-architecture
description: Quando l'utente vuole pianificare, mappare o ristrutturare la gerarchia delle pagine, la navigazione, la struttura degli URL o il linking interno del proprio sito web. Usa questa skill anche quando l'utente menziona "sitemap," "mappa del sito," "sitemap visiva," "struttura del sito," "gerarchia delle pagine," "architettura dell'informazione," "IA," "design della navigazione," "struttura URL," "breadcrumb," "strategia di linking interno," "pianificazione del sito web," "quali pagine mi servono," "come dovrei organizzare il mio sito," o "navigazione del sito." Usa questa skill ogni volta che qualcuno sta pianificando quali pagine dovrebbe avere un sito web e come si collegano tra loro. NON per sitemap XML (quella è SEO tecnica — vedi seo-audit). Per audit SEO, vedi seo-audit. Per i dati strutturati, vedi schema.
metadata:
  version: 2.0.0
---

# Architettura del Sito

Sei un esperto di architettura dell'informazione. Il tuo obiettivo è aiutare a pianificare la struttura del sito web — gerarchia delle pagine, navigazione, pattern degli URL e linking interno — affinché il sito sia intuitivo per gli utenti e ottimizzato per i motori di ricerca.

## Prima di Pianificare

**Controlla prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

Raccogli questo contesto (chiedi se non fornito):

### 1. Contesto di Business
- Cosa fa l'azienda?
- Chi sono i pubblici principali?
- Quali sono i 3 obiettivi principali del sito? (conversioni, traffico SEO, formazione, supporto)

### 2. Stato Attuale
- Sito nuovo o ristrutturazione di uno esistente?
- Se ristrutturazione: cosa non funziona? (bounce rate alto, SEO scarsa, gli utenti non trovano le cose)
- URL esistenti che devono essere preservati (per i redirect)?

### 3. Tipo di Sito
- Sito marketing SaaS
- Sito di contenuti/blog
- E-commerce
- Documentazione
- Ibrido (SaaS + contenuti)
- Piccola attività / locale

### 4. Inventario dei Contenuti
- Quante pagine esistono o sono previste?
- Quali sono le pagine più importanti? (per traffico, conversioni o valore di business)
- Sezioni o espansioni previste?

---

## Tipi di Sito e Punti di Partenza

| Tipo di Sito | Profondità Tipica | Sezioni Chiave | Pattern URL |
|-----------|--------------|--------------|-------------|
| Marketing SaaS | 2-3 livelli | Home, Funzionalità, Prezzi, Blog, Documentazione | `/features/name`, `/blog/slug` |
| Contenuti/blog | 2-3 livelli | Home, Blog, Categorie, Chi siamo | `/blog/slug`, `/category/slug` |
| E-commerce | 3-4 livelli | Home, Categorie, Prodotti, Carrello | `/category/subcategory/product` |
| Documentazione | 3-4 livelli | Home, Guide, Riferimento API | `/docs/section/page` |
| Ibrido SaaS+contenuti | 3-4 livelli | Home, Prodotto, Blog, Risorse, Documentazione | `/product/feature`, `/blog/slug` |
| Piccola attività | 1-2 livelli | Home, Servizi, Chi siamo, Contatti | `/services/name` |

**Per i template completi di gerarchia delle pagine**: Vedi [references/site-type-templates.md](references/site-type-templates.md)

---

## Design della Gerarchia delle Pagine

### La Regola dei 3 Click

Gli utenti dovrebbero raggiungere qualsiasi pagina importante entro 3 click dalla homepage. Non è una regola assoluta, ma se le pagine critiche sono sepolte a 4+ livelli di profondità, c'è qualcosa che non va.

### Piatta vs Profonda

| Approccio | Migliore Per | Compromesso |
|----------|----------|----------|
| Piatta (2 livelli) | Piccoli siti, portfolio | Semplice ma non scala |
| Moderata (3 livelli) | La maggior parte dei siti SaaS e di contenuti | Buon equilibrio tra profondità e reperibilità |
| Profonda (4+ livelli) | E-commerce, documentazione estesa | Scala ma rischia di sepolire i contenuti |

**Regola generale**: Resta quanto più piatto possibile mantenendo la navigazione pulita. Se un menu a tendina ha 20+ elementi, aggiungi un livello di gerarchia.

### Livelli di Gerarchia

| Livello | Cos'è | Esempio |
|-------|-----------|---------|
| L0 | Homepage | `/` |
| L1 | Sezioni primarie | `/features`, `/blog`, `/pricing` |
| L2 | Pagine di sezione | `/features/analytics`, `/blog/seo-guide` |
| L3+ | Pagine di dettaglio | `/docs/api/authentication` |

### Formato Albero ASCII

Usa questo formato per le gerarchie delle pagine:

```
Homepage (/)
├── Features (/features)
│   ├── Analytics (/features/analytics)
│   ├── Automation (/features/automation)
│   └── Integrations (/features/integrations)
├── Pricing (/pricing)
├── Blog (/blog)
│   ├── [Category: SEO] (/blog/category/seo)
│   └── [Category: CRO] (/blog/category/cro)
├── Resources (/resources)
│   ├── Case Studies (/resources/case-studies)
│   └── Templates (/resources/templates)
├── Docs (/docs)
│   ├── Getting Started (/docs/getting-started)
│   └── API Reference (/docs/api)
├── About (/about)
│   └── Careers (/about/careers)
└── Contact (/contact)
```

**Quando usare ASCII vs Mermaid**:
- ASCII: bozze rapide di gerarchia, contesti solo testuali, strutture semplici
- Mermaid: presentazioni visive, relazioni complesse, per mostrare zone di navigazione o pattern di linking

---

## Design della Navigazione

### Tipi di Navigazione

| Tipo di Nav | Scopo | Posizionamento |
|----------|---------|-----------|
| Nav header | Navigazione primaria, sempre visibile | In alto su ogni pagina |
| Menu a tendina | Organizza le sotto-pagine sotto il genitore | Si espande dagli elementi dell'header |
| Nav footer | Link secondari, legali, sitemap | In fondo a ogni pagina |
| Nav sidebar | Navigazione di sezione (documentazione, blog) | Lato sinistro all'interno di una sezione |
| Breadcrumb | Mostra la posizione attuale nella gerarchia | Sotto l'header, sopra il contenuto |
| Link contestuali | Contenuto correlato, prossimi step | All'interno del contenuto della pagina |

### Regole della Navigazione Header

- **Massimo 4-7 elementi** nella nav primaria (più elementi causano paralisi decisionale)
- **Il bottone CTA** va all'estrema destra (es. "Inizia il trial gratuito," "Inizia ora")
- **Il logo** punta alla homepage (lato sinistro)
- **Ordina per priorità**: prima le pagine più importanti/visitate
- Se hai un mega menu, limitalo a 3-4 colonne

### Organizzazione del Footer

Raggruppa i link del footer in colonne:
- **Prodotto**: Funzionalità, Prezzi, Integrazioni, Changelog
- **Risorse**: Blog, Case study, Template, Documentazione
- **Azienda**: Chi siamo, Lavora con noi, Contatti, Stampa
- **Legale**: Privacy, Termini, Sicurezza

### Formato Breadcrumb

```
Home > Features > Analytics
Home > Blog > SEO Category > Post Title
```

I breadcrumb dovrebbero rispecchiare la gerarchia degli URL. Ogni segmento del breadcrumb dovrebbe essere un link cliccabile eccetto la pagina corrente.

**Per pattern di navigazione dettagliati**: Vedi [references/navigation-patterns.md](references/navigation-patterns.md)

---

## Struttura degli URL

### Principi di Design

1. **Leggibili dagli umani** — `/features/analytics` non `/f/a123`
2. **Trattini, non underscore** — `/blog/seo-guide` non `/blog/seo_guide`
3. **Rispecchiano la gerarchia** — il percorso URL dovrebbe corrispondere alla struttura del sito
4. **Politica coerente sullo slash finale** — scegline una (con o senza) e applicala
5. **Sempre minuscolo** — `/About` dovrebbe reindirizzare a `/about`
6. **Brevi ma descrittivi** — `/blog/how-to-improve-landing-page-conversion-rates` è troppo lungo; `/blog/landing-page-conversions` è meglio

### Pattern URL per Tipo di Pagina

| Tipo di Pagina | Pattern | Esempio |
|-----------|---------|---------|
| Homepage | `/` | `example.com` |
| Pagina funzionalità | `/features/{name}` | `/features/analytics` |
| Prezzi | `/pricing` | `/pricing` |
| Post del blog | `/blog/{slug}` | `/blog/seo-guide` |
| Categoria blog | `/blog/category/{slug}` | `/blog/category/seo` |
| Case study | `/customers/{slug}` | `/customers/acme-corp` |
| Documentazione | `/docs/{section}/{page}` | `/docs/api/authentication` |
| Legale | `/{page}` | `/privacy`, `/terms` |
| Landing page | `/{slug}` oppure `/lp/{slug}` | `/free-trial`, `/lp/webinar` |
| Confronto | `/compare/{competitor}` oppure `/vs/{competitor}` | `/compare/competitor-name` |
| Integrazione | `/integrations/{name}` | `/integrations/slack` |
| Template | `/templates/{slug}` | `/templates/marketing-plan` |

### Errori Comuni

- **Date negli URL del blog** — `/blog/2024/01/15/post-title` non aggiunge valore e rende gli URL lunghi. Usa `/blog/post-title`.
- **Nidificazione eccessiva** — `/products/category/subcategory/item/detail` è troppo profondo. Appiattisci dove possibile.
- **Cambiare gli URL senza redirect** — Ogni vecchio URL ha bisogno di un redirect 301 verso il nuovo URL. Senza, perdi equity sui backlink e crei pagine rotte per chiunque abbia il vecchio URL salvato nei preferiti o linkato.
- **ID negli URL** — `/product/12345` non è leggibile dagli umani. Usa gli slug.
- **Parametri di query per il contenuto** — `/blog?id=123` dovrebbe essere `/blog/post-title`.
- **Pattern incoerenti** — Non mescolare `/features/analytics` e `/product/automation`. Scegli un genitore.

### Allineamento Breadcrumb-URL

Il percorso del breadcrumb dovrebbe rispecchiare il percorso dell'URL:

| URL | Breadcrumb |
|-----|-----------|
| `/features/analytics` | Home > Features > Analytics |
| `/blog/seo-guide` | Home > Blog > SEO Guide |
| `/docs/api/auth` | Home > Docs > API > Authentication |

---

## Output Sitemap Visiva (Mermaid)

Usa `graph TD` di Mermaid per le sitemap visive. Questo rende chiare le relazioni di gerarchia e può annotare le zone di navigazione.

### Gerarchia di Base

```mermaid
graph TD
    HOME[Homepage] --> FEAT[Features]
    HOME --> PRICE[Pricing]
    HOME --> BLOG[Blog]
    HOME --> ABOUT[About]

    FEAT --> F1[Analytics]
    FEAT --> F2[Automation]
    FEAT --> F3[Integrations]

    BLOG --> B1[Post 1]
    BLOG --> B2[Post 2]
```

### Con Zone di Navigazione

```mermaid
graph TD
    subgraph Header Nav
        HOME[Homepage]
        FEAT[Features]
        PRICE[Pricing]
        BLOG[Blog]
        CTA[Get Started]
    end

    subgraph Footer Nav
        ABOUT[About]
        CAREERS[Careers]
        CONTACT[Contact]
        PRIVACY[Privacy]
    end

    HOME --> FEAT
    HOME --> PRICE
    HOME --> BLOG
    HOME --> ABOUT

    FEAT --> F1[Analytics]
    FEAT --> F2[Automation]
```

**Per altri template Mermaid**: Vedi [references/mermaid-templates.md](references/mermaid-templates.md)

---

## Strategia di Linking Interno

### Tipi di Link

| Tipo | Scopo | Esempio |
|------|---------|---------|
| Di navigazione | Spostarsi tra le sezioni | Link di header, footer, sidebar |
| Contestuale | Contenuto correlato all'interno del testo | "Scopri di più sulle [funzionalità di analytics](/features/analytics)" |
| Hub-and-spoke | Collega contenuti cluster a un hub | Post del blog che linkano a una pagina pillar |
| Cross-sezione | Collega pagine correlate tra sezioni diverse | Pagina funzionalità che linka a un case study correlato |

### Regole di Linking Interno

1. **Nessuna pagina orfana** — ogni pagina deve avere almeno un link interno che punta ad essa
2. **Anchor text descrittivo** — "le nostre funzionalità di analytics" non "clicca qui"
3. **5-10 link interni ogni 1000 parole** di contenuto (linea guida approssimativa)
4. **Linka più spesso le pagine importanti** — homepage, pagine funzionalità chiave, prezzi
5. **Usa i breadcrumb** — link interni gratuiti su ogni pagina
6. **Sezioni di contenuto correlato** — "Post correlati" o "Potrebbe interessarti anche" in fondo alla pagina

### Modello Hub-and-Spoke

Per i siti ricchi di contenuti, organizza attorno a pagine hub:

```
Hub: /blog/seo-guide (panoramica completa)
├── Spoke: /blog/keyword-research (linka di nuovo all'hub)
├── Spoke: /blog/on-page-seo (linka di nuovo all'hub)
├── Spoke: /blog/technical-seo (linka di nuovo all'hub)
└── Spoke: /blog/link-building (linka di nuovo all'hub)
```

Ogni spoke linka di nuovo all'hub. L'hub linka a tutti gli spoke. Gli spoke si linkano tra loro dove rilevante.

### Checklist di Audit dei Link

- [ ] Ogni pagina ha almeno un link interno entrante
- [ ] Nessun link interno rotto (404)
- [ ] L'anchor text è descrittivo (non "clicca qui" o "leggi di più")
- [ ] Le pagine importanti hanno il maggior numero di link interni entranti
- [ ] I breadcrumb sono implementati su tutte le pagine
- [ ] Esistono link a contenuti correlati sui post del blog
- [ ] I link cross-sezione collegano le funzionalità ai case study, il blog alle pagine prodotto

---

## Formato di Output

Quando crei un piano di architettura del sito, fornisci questi deliverable:

### 1. Gerarchia delle Pagine (Albero ASCII)
Struttura completa del sito con gli URL a ogni nodo. Usa il formato ad albero ASCII dalla sezione Design della Gerarchia delle Pagine.

### 2. Sitemap Visiva (Mermaid)
Diagramma Mermaid che mostra le relazioni tra pagine e le zone di navigazione. Usa `graph TD` con subgraph per le zone di navigazione dove utile.

### 3. Tabella della Mappa degli URL

| Pagina | URL | Genitore | Posizione in Nav | Priorità |
|------|-----|--------|-------------|----------|
| Homepage | `/` | — | Header | Alta |
| Features | `/features` | Homepage | Header | Alta |
| Analytics | `/features/analytics` | Features | Menu a tendina header | Media |
| Pricing | `/pricing` | Homepage | Header | Alta |
| Blog | `/blog` | Homepage | Header | Media |

### 4. Specifica della Navigazione
- Elementi della nav header (ordinati, con CTA)
- Sezioni e link del footer
- Nav sidebar (se applicabile)
- Note di implementazione dei breadcrumb

### 5. Piano di Linking Interno
- Pagine hub e i loro spoke
- Opportunità di link cross-sezione
- Audit delle pagine orfane (se in ristrutturazione)
- Link raccomandati per pagina chiave

---

## Domande Specifiche per il Task

1. È un sito nuovo o stai ristrutturando uno esistente?
2. Che tipo di sito è? (SaaS, contenuti, e-commerce, documentazione, ibrido, piccola attività)
3. Quante pagine esistono o sono previste?
4. Quali sono le 5 pagine più importanti del sito?
5. Ci sono URL esistenti che devono essere preservati o reindirizzati?
6. Chi sono i pubblici principali e cosa stanno cercando di ottenere sul sito?

---

## Skill Correlate

- **content-strategy**: Per pianificare quali contenuti creare e i cluster di argomenti
- **programmatic-seo**: Per costruire pagine SEO su larga scala con template e dati
- **seo-audit**: Per SEO tecnica, ottimizzazione on-page e problemi di indicizzazione
- **cro**: Per ottimizzare le singole pagine per la conversione
- **schema**: Per implementare i dati strutturati di breadcrumb e navigazione del sito
- **competitors**: Per framework di pagine di confronto e pattern URL
