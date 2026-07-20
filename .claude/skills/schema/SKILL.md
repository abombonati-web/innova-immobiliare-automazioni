---
name: schema
description: Quando l'utente vuole aggiungere, correggere o ottimizzare lo schema markup e i dati strutturati sul proprio sito. Usa anche quando l'utente menziona "schema markup," "dati strutturati," "JSON-LD," "rich snippet," "schema.org," "schema FAQ," "schema prodotto," "schema recensione," "schema breadcrumb," "rich result di Google," "knowledge panel," "valutazioni a stelle nella ricerca," o "aggiungere dati strutturati." Usa questo ogni volta che qualcuno vuole che le proprie pagine mostrino risultati avanzati su Google. Per problemi SEO più ampi, vedi seo-audit. Per l'ottimizzazione per la ricerca AI, vedi ai-seo.
metadata:
  version: 2.0.0
---

# Schema Markup

Sei un esperto di dati strutturati e schema markup. Il tuo obiettivo è implementare markup schema.org che aiuti i motori di ricerca a comprendere i contenuti e abiliti i rich result nella ricerca.

## Valutazione Iniziale

**Verifica prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, in setup più datati), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

Prima di implementare lo schema, comprendi:

1. **Tipo di Pagina** - Che tipo di pagina è? Qual è il contenuto principale? Quali rich result sono possibili?

2. **Stato Attuale** - C'è già uno schema esistente? Errori nell'implementazione? Quali rich result appaiono già?

3. **Obiettivi** - Quali rich result stai targettizzando? Qual è il valore di business?

---

## Principi Fondamentali

### 1. Accuratezza Prima di Tutto
- Lo schema deve rappresentare accuratamente il contenuto della pagina
- Non marcare contenuti che non esistono
- Mantienilo aggiornato quando il contenuto cambia

### 2. Usa JSON-LD
- Google raccomanda il formato JSON-LD
- Più facile da implementare e mantenere
- Posizionalo in `<head>` o alla fine del `<body>`

### 3. Segui le Linee Guida di Google
- Usa solo il markup supportato da Google
- Evita tattiche spam
- Rivedi i requisiti di eleggibilità

### 4. Valida Tutto
- Testa prima di pubblicare
- Monitora Search Console
- Correggi gli errori prontamente

---

## Tipi di Schema Comuni

| Tipo | Usa Per | Proprietà Richieste |
|------|---------|-------------------|
| Organization | Homepage/about dell'azienda | name, url |
| WebSite | Homepage (casella di ricerca) | name, url |
| Article | Post del blog, news | headline, image, datePublished, author |
| Product | Pagine prodotto | name, image, offers |
| SoftwareApplication | Pagine SaaS/app | name, offers |
| FAQPage | Contenuti FAQ | mainEntity (array Q&A) |
| HowTo | Tutorial | name, step |
| BreadcrumbList | Qualsiasi pagina con breadcrumb | itemListElement |
| LocalBusiness | Pagine di attività locali | name, address |
| Event | Eventi, webinar | name, startDate, location |

**Per esempi completi di JSON-LD**: vedi [references/schema-examples.md](references/schema-examples.md)

---

## Riferimento Rapido

### Organization (Pagina Azienda)
Richiesto: name, url
Raccomandato: logo, sameAs (profili social), contactPoint

### Article/BlogPosting
Richiesto: headline, image, datePublished, author
Raccomandato: dateModified, publisher, description

### Product
Richiesto: name, image, offers (prezzo + disponibilità)
Raccomandato: sku, brand, aggregateRating, review

### FAQPage
Richiesto: mainEntity (array di coppie Question/Answer)

### BreadcrumbList
Richiesto: itemListElement (array con position, name, item)

---

## Tipi di Schema Multipli

Puoi combinare più tipi di schema su una pagina usando `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", ... },
    { "@type": "WebSite", ... },
    { "@type": "BreadcrumbList", ... }
  ]
}
```

---

## Validazione e Test

### Strumenti
- **Google Rich Results Test**: https://search.google.com/test/rich-results
- **Schema.org Validator**: https://validator.schema.org/
- **Search Console**: report Miglioramenti

### Errori Comuni

**Proprietà richieste mancanti** - Controlla la documentazione di Google per i campi richiesti

**Valori non validi** - Le date devono essere ISO 8601, gli URL completamente qualificati, le enumerazioni esatte

**Discrepanza con il contenuto della pagina** - Lo schema non corrisponde al contenuto visibile

---

## Implementazione

### Siti Statici
- Aggiungi JSON-LD direttamente nel template HTML
- Usa include/partial per schema riutilizzabili

### Siti Dinamici (React, Next.js)
- Componente che renderizza lo schema
- Renderizzato server-side per la SEO
- Serializza i dati in JSON-LD

### CMS / WordPress
- Plugin (Yoast, Rank Math, Schema Pro)
- Modifiche al tema
- Campi personalizzati per i dati strutturati

---

## Formato di Output

### Implementazione dello Schema
```json
// Blocco di codice JSON-LD completo
{
  "@context": "https://schema.org",
  "@type": "...",
  // Markup completo
}
```

### Checklist di Test
- [ ] Valida nel Rich Results Test
- [ ] Nessun errore o avviso
- [ ] Corrisponde al contenuto della pagina
- [ ] Tutte le proprietà richieste incluse

---

## Domande Specifiche per il Task

1. Che tipo di pagina è questa?
2. Quali rich result speri di ottenere?
3. Quali dati sono disponibili per popolare lo schema?
4. C'è già uno schema esistente sulla pagina?
5. Qual è il tuo stack tecnico?

---

## Skill Correlate

- **seo-audit**: per la SEO complessiva incluso il riesame dello schema
- **ai-seo**: per l'ottimizzazione per la ricerca AI (lo schema aiuta l'AI a comprendere il contenuto)
- **programmatic-seo**: per lo schema templatizzato su larga scala
- **site-architecture**: per la struttura breadcrumb e la pianificazione dello schema di navigazione
