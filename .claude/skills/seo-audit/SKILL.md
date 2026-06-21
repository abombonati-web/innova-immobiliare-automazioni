---
name: seo-audit
description: Quando l'utente vuole controllare, revisionare o diagnosticare problemi SEO sul proprio sito. Usa questa skill anche quando l'utente menziona "audit SEO," "SEO tecnica," "perché non sono in classifica," "problemi SEO," "SEO on-page," "revisione meta tag," "controllo salute SEO," "il mio traffico è calato," "ho perso posizioni," "non compaio su Google," "il sito non si posiziona," "un aggiornamento Google mi ha colpito," "velocità della pagina," "core web vitals," "errori di scansione," o "problemi di indicizzazione." Usa questa skill anche se l'utente dice solo qualcosa di vago come "la mia SEO è scarsa" o "aiuto con la SEO" — inizia con un audit. Per costruire pagine su larga scala per targetizzare keyword, vedi programmatic-seo. Per aggiungere dati strutturati, vedi schema. Per l'ottimizzazione per la ricerca AI, vedi ai-seo.
metadata:
  version: 2.0.0
---

# Audit SEO

Sei un esperto di ottimizzazione per i motori di ricerca. Il tuo obiettivo è identificare i problemi SEO e fornire raccomandazioni concrete per migliorare le performance di ricerca organica.

## Valutazione Iniziale

**Controlla prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

Prima di fare l'audit, capisci:

1. **Contesto del Sito**
   - Che tipo di sito è? (SaaS, e-commerce, blog, ecc.)
   - Qual è l'obiettivo di business principale per la SEO?
   - Quali keyword/argomenti sono prioritari?

2. **Stato Attuale**
   - Ci sono problemi o preoccupazioni note?
   - Qual è il livello di traffico organico attuale?
   - Cambiamenti o migrazioni recenti?

3. **Ambito**
   - Audit completo del sito o pagine specifiche?
   - Tecnico + on-page, o un'unica area di focus?
   - Accesso a Search Console / analytics?

---

## Framework dell'Audit

### Limite nella Rilevazione dello Schema Markup

**`web_fetch` e `curl` non possono rilevare in modo affidabile i dati strutturati / lo schema markup.**

Molti plugin CMS (AIOSEO, Yoast, RankMath) iniettano JSON-LD tramite JavaScript lato client — non apparirà nell'HTML statico né nell'output di `web_fetch` (che rimuove i tag `<script>` durante la conversione).

**Per verificare correttamente la presenza di schema markup, usa uno di questi metodi:**
1. **Strumento browser** — renderizza la pagina ed esegui: `document.querySelectorAll('script[type="application/ld+json"]')`
2. **Google Rich Results Test** — https://search.google.com/test/rich-results
3. **Export di Screaming Frog** — se il cliente ne fornisce uno, usalo (SF renderizza il JavaScript)

Riportare "nessuno schema trovato" basandosi solo su `web_fetch` o `curl` porta a risultati di audit falsi — questi strumenti non possono vedere lo schema iniettato via JS.

### Ordine di Priorità
1. **Scansionabilità e Indicizzazione** (Google può trovarlo e indicizzarlo?)
2. **Fondamenta Tecniche** (il sito è veloce e funzionale?)
3. **Ottimizzazione On-Page** (il contenuto è ottimizzato?)
4. **Qualità del Contenuto** (merita di posizionarsi?)
5. **Autorevolezza e Link** (ha credibilità?)

---

## Audit SEO Tecnica

### Scansionabilità

**Robots.txt**
- Controlla blocchi non intenzionali
- Verifica che le pagine importanti siano consentite
- Controlla il riferimento alla sitemap

**Sitemap XML**
- Esiste ed è accessibile
- Inviata a Search Console
- Contiene solo URL canonici e indicizzabili
- Aggiornata regolarmente
- Formattazione corretta

**Architettura del Sito**
- Pagine importanti raggiungibili entro 3 click dalla homepage
- Gerarchia logica
- Struttura di link interni
- Nessuna pagina orfana

**Problemi di Crawl Budget** (per siti di grandi dimensioni)
- URL parametrizzati sotto controllo
- Navigazione a faccette gestita correttamente
- Scroll infinito con fallback di paginazione
- ID di sessione non presenti negli URL

### Indicizzazione

**Stato di Indicizzazione**
- Controllo con site:dominio.com
- Report di copertura su Search Console
- Confronto tra pagine indicizzate e attese

**Problemi di Indicizzazione**
- Tag noindex su pagine importanti
- Canonical che puntano nella direzione errata
- Catene/loop di redirect
- Soft 404
- Contenuto duplicato senza canonical

**Canonicalizzazione**
- Tutte le pagine hanno tag canonical
- Canonical auto-referenziali su pagine uniche
- Canonical da HTTP a HTTPS
- Coerenza www vs. non-www
- Coerenza nello slash finale

### Velocità del Sito e Core Web Vitals

**Core Web Vitals**
- LCP (Largest Contentful Paint): < 2,5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0,1

**Fattori di Velocità**
- Tempo di risposta del server (TTFB)
- Ottimizzazione delle immagini
- Esecuzione JavaScript
- Distribuzione del CSS
- Header di caching
- Utilizzo di CDN
- Caricamento dei font

**Strumenti**
- PageSpeed Insights
- WebPageTest
- Chrome DevTools
- Report Core Web Vitals di Search Console

### Mobile-Friendliness

- Design responsive (non sito m. separato)
- Dimensioni delle aree tap
- Viewport configurato
- Nessuno scroll orizzontale
- Stesso contenuto del desktop
- Pronto per l'indicizzazione mobile-first

### Sicurezza e HTTPS

- HTTPS su tutto il sito
- Certificato SSL valido
- Nessun contenuto misto
- Redirect da HTTP a HTTPS
- Header HSTS (bonus)

### Struttura degli URL

- URL leggibili e descrittivi
- Keyword negli URL dove naturale
- Struttura coerente
- Nessun parametro superfluo
- Minuscolo e separato da trattini

---

## SEO Internazionale e Localizzazione

Verifica quando il sito serve più lingue o regioni. Configurazioni errate possono bloccare l'indicizzazione di intere varianti locali o abbassare i segnali di qualità a livello di sito. Vedi [riferimento SEO internazionale](references/international-seo.md) per evidenze e URL delle fonti.

### Hreflang

Tre metodi di posizionamento equivalenti: `<link>` HTML nell'`<head>`, header HTTP `Link`, `<xhtml:link>` nella sitemap XML. Se ne usi più di uno, devono essere coerenti tra loro -- segnali in conflitto fanno scartare quella coppia da Google. Per 10+ locali, preferisci l'approccio basato su sitemap (nessun peso sulla pagina, nessun costo per richiesta).

**Verifica:**
- Voce auto-referenziale su ogni pagina (la pagina deve includere se stessa nel set hreflang)
- Link reciproci (se A punta a B, B deve puntare a sua volta ad A -- altrimenti entrambi vengono ignorati)
- Codici validi: lingua ISO 639-1 + regione opzionale ISO 3166-1 Alpha 2 (es. `en`, `en-GB` -- mai `en-UK`)
- `x-default` presente, che punta a una pagina di fallback (selettore di lingua o locale predefinito)
- Tutti gli URL target restituiscono 200, sono indicizzabili e corrispondono al loro URL canonico
- Nessun codice lingua-regione duplicato che punta a URL diversi

**Errori comuni:** voce auto-referenziale mancante (tutto l'hreflang viene ignorato). Nessun tag di ritorno / monodirezionale (la coppia viene scartata). Codici non validi come `en-UK` (usa `en-GB`). Il target hreflang non è canonico, è un 404 o è bloccato (il cluster viene scartato). Le annotazioni HTML e sitemap sono in disaccordo (la coppia in conflitto viene scartata).

**Su larga scala:** i figli di `<xhtml:link>` non contano verso il limite di 50K URL della sitemap, ma il limite di dimensione file di 50MB diventa il collo di bottiglia (pianifica 2K-5K URL per file con hreflang completo). Concentra l'hreflang sulle pagine che ricevono traffico nella lingua sbagliata -- non è richiesto su ogni pagina. Per Bing: integra con `<html lang>` e `<meta http-equiv="content-language">` (Bing tratta l'hreflang come un segnale debole).

### Canonicalizzazione per Siti Multilingua

- Ogni pagina locale deve auto-canonicalizzarsi (es. `/ar/page` ha come canonical `/ar/page`)
- Mai un canonical cross-locale (francese verso inglese) -- sopprime completamente la versione non canonica
- L'URL canonico deve apparire nel set hreflang -- altrimenti tutto l'hreflang viene ignorato
- Il canonical ha la precedenza sull'hreflang in caso di conflitto
- Protocollo/dominio devono essere coerenti tra canonical, hreflang e sitemap (`https` + stessa variante di dominio)
- Pagine locali paginate: canonical auto-referenziale per pagina (mai canonicalizzare la pagina 2+ verso la pagina 1)

**Errori comuni:** tutte le locali con canonical verso l'inglese (uccide l'indicizzazione), URL canonico non presente nel set hreflang (viene ignorato silenziosamente), discrepanza di protocollo tra canonical e hreflang, il CMS imposta il canonical di una pagina profonda verso la homepage.

### Sitemap Internazionali

**Verifica:**
- Namespace `xmlns:xhtml` su `<urlset>`, ogni `<url>` include `<xhtml:link>` per tutte le locali incluse se stessa
- `x-default` alternativo incluso; tutti gli URL assoluti (protocollo + dominio completi)
- Indice sitemap in Search Console e nel robots.txt; diviso per tipo di contenuto, non per locale

**Avvertenza Next.js:** `alternates.languages` NON include automaticamente un `<xhtml:link>` auto-referenziale per l'URL `<loc>` -- devi aggiungere esplicitamente la locale corrente.

### Struttura URL delle Locali

**Raccomandato:** Sottodirectory (`/en/`, `/ar/`). **Accettabile:** Sottodomini o ccTLD. **Non raccomandato:** Parametri URL (`?lang=en`).

**Verifica:**
- Strategia coerente di prefisso locale; tutte le locali con prefisso (nascondere la locale dagli URL impedisce a Google di distinguere le versioni)
- L'URL radice è gestito come `x-default` con redirect, oppure serve il contenuto della locale predefinita
- Nessuna negoziazione del contenuto basata su IP/Accept-Language (Googlebot: IP USA, nessun header Accept-Language)
- Coerenza di slash finale + maiuscole/minuscole tra percorsi locali, canonical, hreflang e sitemap
- Redirect 301 dal formato non canonico al canonico

**Nota:** Il report di Targeting Internazionale di Google in Search Console è deprecato. Il geotargeting si basa su hreflang, segnali di contenuto e pattern di linking.

### Qualità del Contenuto tra le Locali

**Qualità della traduzione:**
- Il contenuto tradotto con l'AI non è intrinsecamente spam (posizione di Google nel 2025), ma traduzioni di basso valore su larga scala possono attivare le politiche anti-abuso sui contenuti scalati
- Google usa il contenuto visibile per determinare la lingua -- traduci TUTTO il contenuto della pagina (titolo, descrizione, intestazioni, corpo), non solo gli elementi standard
- Tradurre solo template/nav lasciando il contenuto principale nella lingua originale crea duplicati

**Pagine locali povere (thin content):**
- Il sistema "helpful content" è a livello di sito -- molte pagine locali povere possono sopprimere il posizionamento anche di pagine forti
- Non mettere noindex sulle locali povere (spreca crawl budget) né canonical cross-locale (entra in conflitto con l'hreflang)
- Approccio migliore: non creare pagine locali che non puoi rendere genuinamente utili

**Verifica:**
- Tutte le pagine locali hanno il contenuto principale completamente tradotto (non solo l'interfaccia)
- Nessun contenuto quasi identico tra le locali ("Duplicato, Google ha scelto un canonical diverso" in GSC)
- Hreflang solo per le locali con contenuto genuino e domanda di ricerca
- Segnali localizzati: valuta, formato telefono, indirizzi dove applicabile
- Link hreflang rotti (404, redirect) sprecano crawl budget E invalidano i cluster hreflang

---

## Audit SEO On-Page

### Tag Title

**Verifica:**
- Title unici per ogni pagina
- Keyword primaria vicino all'inizio
- 50-60 caratteri (visibili nella SERP)
- Accattivanti e che invitano al click
- Posizionamento del nome del brand (di solito alla fine)

**Problemi comuni:**
- Title duplicati
- Troppo lunghi (troncati)
- Troppo corti (opportunità sprecata)
- Keyword stuffing
- Completamente assenti

### Meta Description

**Verifica:**
- Descrizioni unique per pagina
- 150-160 caratteri
- Includono la keyword primaria
- Proposta di valore chiara
- Call to action

**Problemi comuni:**
- Descrizioni duplicate
- Generate automaticamente e di scarsa qualità
- Troppo lunghe/corte
- Nessuna ragione convincente per cliccare

### Struttura delle Intestazioni

**Verifica:**
- Un H1 per pagina
- L'H1 contiene la keyword primaria
- Gerarchia logica (H1 → H2 → H3)
- Le intestazioni descrivono il contenuto
- Non usate solo per lo styling

**Problemi comuni:**
- H1 multipli
- Livelli saltati (H1 → H3)
- Intestazioni usate solo per lo styling
- Nessun H1 nella pagina

### Ottimizzazione del Contenuto

**Contenuto Principale della Pagina**
- Keyword nelle prime 100 parole
- Keyword correlate usate naturalmente
- Profondità/lunghezza sufficiente per l'argomento
- Risponde all'intento di ricerca
- Migliore dei competitor

**Problemi di Contenuto Povero**
- Pagine con poco contenuto unico
- Pagine tag/categoria senza valore
- Pagine "doorway"
- Contenuto duplicato o quasi duplicato

### Ottimizzazione delle Immagini

**Verifica:**
- Nomi file descrittivi
- Testo alt su tutte le immagini
- Il testo alt descrive l'immagine
- Dimensioni file compresse
- Formati moderni (WebP)
- Lazy loading implementato
- Immagini responsive

### Link Interni

**Verifica:**
- Pagine importanti ben collegate
- Anchor text descrittivo
- Relazioni di link logiche
- Nessun link interno rotto
- Numero ragionevole di link per pagina

**Problemi comuni:**
- Pagine orfane (nessun link interno)
- Anchor text eccessivamente ottimizzato
- Pagine importanti sepolte
- Link eccessivi in footer/sidebar

### Targeting delle Keyword

**Per Pagina**
- Target chiaro della keyword primaria
- Title, H1, URL allineati
- Il contenuto soddisfa l'intento di ricerca
- Non in competizione con altre pagine (cannibalizzazione)

**A Livello di Sito**
- Documento di keyword mapping
- Nessuna lacuna importante nella copertura
- Nessuna cannibalizzazione di keyword
- Cluster tematici logici

---

## Valutazione della Qualità del Contenuto

### Segnali E-E-A-T

**Esperienza**
- Esperienza diretta dimostrata
- Insight/dati originali
- Esempi reali e case study

**Competenza (Expertise)**
- Credenziali dell'autore visibili
- Informazioni accurate e dettagliate
- Affermazioni adeguatamente supportate da fonti

**Autorevolezza**
- Riconosciuto nel settore
- Citato da altri
- Credenziali di settore

**Affidabilità**
- Informazioni accurate
- Trasparenza sull'attività
- Informazioni di contatto disponibili
- Privacy policy, termini
- Sito sicuro (HTTPS)

### Profondità del Contenuto

- Copertura completa dell'argomento
- Risponde a domande di approfondimento
- Migliore dei competitor in top posizione
- Aggiornato e attuale

### Segnali di Coinvolgimento degli Utenti

- Tempo sulla pagina
- Bounce rate nel contesto
- Pagine per sessione
- Visite di ritorno

---

## Problemi Comuni per Tipo di Sito

### Siti SaaS/Prodotto
- Pagine prodotto con poca profondità di contenuto
- Blog non integrato con le pagine prodotto
- Mancano pagine di confronto/alternative
- Pagine funzionalità povere di contenuto
- Nessun glossario/contenuto educativo

### E-commerce
- Pagine categoria povere
- Descrizioni prodotto duplicate
- Schema prodotto mancante
- Navigazione a faccette che crea duplicati
- Pagine fuori stock gestite male

### Siti di Contenuto/Blog
- Contenuto datato non aggiornato
- Cannibalizzazione di keyword
- Nessun clustering tematico
- Linking interno scarso
- Pagine autore mancanti

### Siti Multilingua / Multi-Regionali
- Errori hreflang (tag di ritorno mancanti, codici non validi, nessuna auto-referenza)
- Canonical in conflitto con hreflang (canonical cross-locale sopprime l'indicizzazione)
- Pagine locali povere che abbassano il segnale di qualità a livello di sito
- Solo gli elementi standard tradotti, contenuto principale identico tra le locali
- Nessun fallback x-default dichiarato
- Sitemap senza alternate hreflang o senza voci reciproche
- Redirect basati su IP che nascondono contenuto a Googlebot
- Modalità locale del framework che nasconde la locale dagli URL

### Attività Locale
- NAP incoerente
- Schema locale mancante
- Nessuna ottimizzazione del Google Business Profile
- Pagine di localizzazione mancanti
- Nessun contenuto locale

---

## Formato di Output

### Struttura del Report di Audit

**Sintesi Esecutiva**
- Valutazione generale della salute del sito
- Top 3-5 problemi prioritari
- Quick win identificati

**Risultati SEO Tecnica**
Per ogni problema:
- **Problema**: Cosa non va
- **Impatto**: Impatto SEO (Alto/Medio/Basso)
- **Evidenza**: Come l'hai trovato
- **Soluzione**: Raccomandazione specifica
- **Priorità**: 1-5 oppure Alta/Media/Bassa

**Risultati SEO On-Page**
Stesso formato di cui sopra

**Risultati sul Contenuto**
Stesso formato di cui sopra

**Piano d'Azione Prioritizzato**
1. Correzioni critiche (che bloccano indicizzazione/posizionamento)
2. Miglioramenti ad alto impatto
3. Quick win (facili, beneficio immediato)
4. Raccomandazioni a lungo termine

---

## Riferimenti

- [Rilevazione Scrittura AI](references/ai-writing-detection.md): Pattern comuni di scrittura AI da evitare (lineette lunghe, frasi abusate, parole di riempimento)
- [SEO Internazionale](references/international-seo.md): Evidenze e fonti per hreflang, canonical + i18n, sitemap, struttura URL e qualità del contenuto tra le locali
- Per l'ottimizzazione per la ricerca AI (AEO, GEO, LLMO, AI Overview), vedi la skill **ai-seo**

---

## Strumenti di Riferimento

**Strumenti Gratuiti**
- Google Search Console (essenziale)
- Google PageSpeed Insights
- Bing Webmaster Tools
- Rich Results Test (**usa questo per la validazione dello schema — renderizza il JavaScript**)
- Mobile-Friendly Test
- Schema Validator

> **Nota sulla rilevazione dello schema:** `web_fetch` rimuove i tag `<script>` (incluso il JSON-LD) e non può rilevare schema iniettato via JS. Usa invece lo strumento browser, il Rich Results Test o Screaming Frog — questi renderizzano il JavaScript e catturano il markup iniettato dinamicamente. Vedi la sezione Limite nella Rilevazione dello Schema Markup sopra.

**Strumenti a Pagamento** (se disponibili)
- Screaming Frog
- Ahrefs / Semrush
- Sitebulb
- ContentKing

---

## Domande Specifiche per il Task

1. Quali pagine/keyword contano di più?
2. Hai accesso a Search Console?
3. Cambiamenti o migrazioni recenti?
4. Chi sono i tuoi principali competitor organici?
5. Qual è la tua baseline attuale di traffico organico?

---

## Skill Correlate

- **ai-seo**: Per ottimizzare il contenuto per i motori di ricerca AI (AEO, GEO, LLMO)
- **programmatic-seo**: Per costruire pagine SEO su larga scala
- **site-architecture**: Per la gerarchia delle pagine, il design della navigazione e la struttura degli URL
- **schema**: Per implementare i dati strutturati
- **cro**: Per ottimizzare le pagine per la conversione (non solo per il posizionamento)
- **analytics**: Per misurare le performance SEO
