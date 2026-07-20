---
name: aso
description: "Quando l'utente vuole controllare o ottimizzare una scheda App Store o Google Play. Usare anche quando l'utente menziona 'audit ASO,' 'app store optimization,' 'ottimizzare la mia scheda app,' 'migliorare la visibilità dell'app,' 'posizionamento app store,' 'controlla la mia scheda,' 'perché nessuno scarica la mia app,' 'migliorare la conversione della mia app,' 'ottimizzazione keyword per app,' o 'confronta la mia app con i concorrenti.' Usare quando l'utente condivide un URL di App Store o Google Play e vuole migliorarlo."
metadata:
  version: 2.0.0
---

# Audit ASO

Analizza le schede App Store e Google Play rispetto alle best practice ASO. Recupera
i dati live della scheda, valuta metadati, elementi visivi e recensioni, poi produce
un piano d'azione con priorità.

## Quando Usarla

- L'utente condivide un URL di App Store o Google Play
- L'utente chiede di controllare o ottimizzare una scheda app
- L'utente vuole confrontare la propria app con i concorrenti
- L'utente chiede informazioni sul posizionamento, la visibilità o la conversione dei download dell'app store

## Prima dell'Audit

**Verifica prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo compito.

## Fase 1 — Identifica lo Store e Recupera i Dati

### Rileva il tipo di store dall'URL

```
Apple:  apps.apple.com/{country}/app/{name}/id{digits}
Google: play.google.com/store/apps/details?id={package}
```

Se l'utente fornisce un nome app invece di un URL, cerca sul web:
`site:apps.apple.com "{nome app}"` o `site:play.google.com "{nome app}"`

### Recupera la scheda

Usa WebFetch per recuperare la pagina della scheda. Estrai ogni campo disponibile:

**Campi Apple App Store:**

- Nome app (titolo) — limite 30 caratteri
- Sottotitolo — limite 30 caratteri
- Descrizione (lunga) — non indicizzata per la ricerca, ma conta per la conversione
- Testo promozionale — 170 caratteri, aggiornabile senza nuova release
- Categoria (primaria + secondaria)
- Screenshot (numero, ordine, testo della caption)
- Video di anteprima (presenza, durata)
- Valutazione (media + numero)
- Recensioni recenti (quelle visibili)
- Prezzo / acquisti in-app
- Nome dello sviluppatore
- Data dell'ultimo aggiornamento
- Note sulla cronologia delle versioni
- Classificazione per età
- Dimensione
- Lingue / localizzazioni elencate
- Eventi in-app (se presenti e visibili)

**Campi Google Play:**

- Nome app (titolo) — limite 30 caratteri
- Descrizione breve — limite 80 caratteri
- Descrizione completa — limite 4.000 caratteri, È indicizzata per la ricerca
- Categoria + tag
- Grafica in evidenza (presenza)
- Screenshot (numero, ordine)
- Video di anteprima (presenza)
- Valutazione (media + numero)
- Recensioni recenti (quelle visibili)
- Prezzo / acquisti in-app
- Nome dello sviluppatore
- Data dell'ultimo aggiornamento
- Testo delle novità
- Intervallo dei download
- Classificazione del contenuto
- Sezione sulla sicurezza dei dati
- Lingue elencate

Se WebFetch restituisce dati incompleti (gli store renderizzano lato client), segnala le lacune e
lavora con quanto disponibile. Chiedi all'utente di incollare i campi mancanti se critici.

### Valutazione degli asset visivi

WebFetch non può estrarre le immagini degli screenshot o il testo delle caption. **Fai uno screenshot
della pagina della scheda** per ottenere i dati visivi:

1. Naviga all'URL della scheda e acquisisci uno screenshot a pagina intera
2. Valuta lo screenshot per: qualità dell'icona, numero di screenshot, testo delle caption,
   qualità del messaggio, presenza di video di anteprima, grafica in evidenza (Google Play)
3. Se gli strumenti del browser non sono disponibili, chiedi all'utente di condividere uno screenshot della
   pagina della scheda

**Testo promozionale (Apple):** Questo campo di 170 caratteri appare sopra la descrizione
ma è spesso indistinguibile da essa nell'HTML estratto. Se non puoi confermare la sua
presenza, segnalalo e raccomanda all'utente di controllare App Store Connect.

---

## Fase 1.5 — Valuta la Maturità del Brand

Prima di assegnare i punteggi, classifica l'app in uno dei tre livelli. Questo determina come
interpreti le deviazioni dall'"ASO da manuale" — una scelta di brand deliberata da parte di un
nome noto non è la stessa cosa di un'opportunità persa da un'app sconosciuta.

### Definizioni dei livelli

| Livello            | Segnali                                                                                                                              | Esempi                                    |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------- |
| **Dominante**    | Nome noto, 1M+ valutazioni, top-10 nella categoria, riconoscimento del brand quasi universale. Gli utenti cercano per nome del brand, non per keyword generiche. | Instagram, Uber, Spotify, WhatsApp, Netflix |
| **Consolidata** | Ben conosciuta nella propria categoria, 100K+ valutazioni, installazioni organiche solide, brand riconosciuto ma non universalmente conosciuto.                    | Strava, Notion, Duolingo, Cash App, Calm    |
| **Sfidante**  | In costruzione della propria notorietà, <100K valutazioni, necessita di scoperta tramite keyword e tattiche ASO. La maggior parte delle app rientra qui.            | La tua app, la maggior parte delle app indie/startup |

### Come il livello influenza il punteggio

Le **app dominanti** ottengono un punteggio adattato in queste aree:

- **Titolo:** titoli solo-brand o brand-first sono validi (punteggio 8+ se il brand è la keyword). Queste app non hanno bisogno di scoperta tramite keyword generiche.
- **Descrizione:** punteggio basato puramente sulla qualità di conversione, non sulla presenza di keyword. Se l'app è un nome noto, una descrizione di brand ben fatta vince su una piena di keyword.
- **Asset Visivi:** fotografia lifestyle/brand invece di demo dell'interfaccia è una strategia di conversione legittima. Nessun video è accettabile se il prodotto è difficile da mostrare in 30 secondi o la notorietà del brand è quasi universale.
- **Novità:** note di release generiche a cadenza settimanale+ sono accettabili (punteggio 8+). Su larga scala, changelog detagliati hanno un ROI minimo e rischiano reazioni negative.
- **Eventi in-app:** la mancanza di eventi per app utility con basi di installazione enormi (Uber, WhatsApp) non è una penalità. Queste app non hanno bisogno di aiuto per la scoperta.
- **Localizzazione:** punteggio relativo al mercato effettivo, non al conteggio assoluto. Una fintech solo-USA con 2 lingue (inglese + spagnolo) è adeguatamente localizzata.

Le **app consolidate** ottengono un adattamento parziale:

- Titoli brand-first vanno bene ma dovrebbero comunque includere 1-2 keyword
- Le scelte strategiche nella descrizione ottengono il beneficio del dubbio
- Le altre dimensioni vengono valutate normalmente

Le **app sfidanti** sono valutate strettamente rispetto alle best practice ASO da manuale — ogni carattere, screenshot e keyword conta.

**Principio chiave:** Prima di togliere punti, chiedi: "È un errore o una scelta deliberata
da parte di un team che ha dati che io non ho?" Se l'app ha 1M+ valutazioni e un
team ASO dedicato, presumi che le loro scelte siano basate sui dati a meno che non siano chiaramente sbagliate.

---

## Fase 2 — Valuta Ogni Dimensione

Valuta ogni dimensione da 0 a 10 usando i criteri in `references/scoring-criteria.md`.
Applica gli adattamenti per livello di maturità del brand della Fase 1.5.

File di riferimento per specifiche di piattaforma e benchmark:

- `references/apple-specs.md` — Limiti di caratteri ufficiali Apple, specifiche screenshot/video, regole CPP/PPO, motivi di rifiuto
- `references/google-play-specs.md` — Limiti ufficiali Google Play, specifiche screenshot, soglie Android Vitals, policy
- `references/benchmarks.md` — Dati di conversione, impatto delle valutazioni, lift dei video, comportamento degli screenshot, benchmark CPP/eventi

### Dimensioni e Pesi

| #   | Dimensione            | Peso | Cosa Copre                                                            |
| --- | -------------------- | ------ | ------------------------------------------------------------------------- |
| 1   | Titolo e Sottotitolo     | 20%    | Utilizzo dei caratteri, presenza di keyword, chiarezza, equilibrio brand + keyword       |
| 2   | Descrizione          | 15%    | Prime 3 righe, densità di keyword (Google), CTA, struttura, testo promozionale |
| 3   | Asset Visivi        | 25%    | Numero/qualità/messaggio degli screenshot, video, icona, grafica in evidenza          |
| 4   | Valutazioni e Recensioni    | 20%    | Valutazione media, volume, recenza, risposte dello sviluppatore                      |
| 5   | Metadati e Freschezza | 10%    | Scelta della categoria, recenza dell'aggiornamento, numero di localizzazioni, sicurezza dei dati            |
| 6   | Segnali di Conversione   | 10%    | Posizionamento del prezzo, trasparenza IAP, social proof, intervallo di download                      |

**Punteggio finale** = somma pesata, su 100.

### Interpretazione del punteggio

| Punteggio  | Voto | Significato                                                   |
| ------ | ----- | --------------------------------------------------------- |
| 85-100 | A     | Ben ottimizzata; concentrarsi su A/B test e iterazione        |
| 70-84  | B     | Buona base; opportunità chiare di miglioramento           |
| 50-69  | C     | Lacune significative; le correzioni prioritarie avranno alto impatto |
| 30-49  | D     | Necessaria un'ottimizzazione importante su più dimensioni      |
| 0-29   | F     | La scheda necessita di una revisione completa                         |

---

## Fase 3 — Confronto con i Concorrenti (Opzionale)

Se l'utente fornisce URL dei concorrenti o chiede un confronto:

1. Recupera 2-3 principali concorrenti nella stessa categoria
2. Esegui la stessa valutazione su ciascuno
3. Costruisci una tabella comparativa evidenziando dove l'app dell'utente è più debole/forte
4. Identifica le lacune di keyword — termini per cui i concorrenti si posizionano e l'app dell'utente non targetizza

Se non vengono specificati concorrenti, suggerisci all'utente di fornirne 2-3 o offriti di cercare
le app principali nella loro categoria.

---

## Fase 4 — Genera il Report

Usa il template in `references/report-template.md` per strutturare l'output.

Il report deve includere:

1. **Scheda dei punteggi** — tabella con tutte le 6 dimensioni, punteggi e voto
2. **Top 3 vittorie rapide** — modifiche che richiedono <1 ora e hanno il maggiore impatto
3. **Risultati dettagliati** — analisi per dimensione con problemi specifici e correzioni
4. **Suggerimenti di keyword** — basati sull'analisi titolo/descrizione e sulle lacune dei concorrenti
5. **Raccomandazioni sugli asset visivi** — miglioramenti specifici per screenshot/video
6. **Piano d'azione prioritario** — elenco ordinato di modifiche per impatto vs. impegno

### Regole del report

- Ogni raccomandazione deve essere **specifica e azionabile** ("Cambia il sottotitolo da X a Y" non "Migliora il sottotitolo")
- Includi il conteggio dei caratteri per tutte le raccomandazioni testuali
- Segnala le differenze specifiche per piattaforma (Apple vs Google) quando rilevanti
- Nota cosa NON PUÒ essere valutato senza strumenti a pagamento (volume di ricerca, posizionamenti esatti)
- Quando suggerisci modifiche alle keyword, spiega PERCHÉ ogni keyword conta

---

## Regole Specifiche per Piattaforma

### Apple App Store — Fatti Chiave

- Titolo (30 caratteri) + Sottotitolo (30 caratteri) + Campo keyword (100 **byte**, nascosto) = testo indicizzato
- Il campo keyword è in byte non caratteri — Arabo/CJK usano 2-3 byte per carattere
- La descrizione lunga NON è indicizzata per la ricerca — ottimizza solo per la conversione
- Il testo promozionale (170 caratteri) NON influisce sulla ricerca (confermato da Apple)
- Non ripetere mai parole tra titolo/sottotitolo/campo keyword (Apple indicizza ogni parola una sola volta)
- Campo keyword: virgole, senza spazi ("photo,editor,filter" non "photo, editor, filter")
- Screenshot: fino a 10 per dispositivo. I primi 3 visibili nella ricerca — il 90% non scorre oltre il 3°
- Le caption degli screenshot sono indicizzate da giugno 2025 (estrazione AI)
- Eventi in-app: max 10 pubblicati contemporaneamente, max 31 giorni ciascuno. Indicizzati e appaiono nella ricerca
- Custom Product Pages (fino a 70) nella ricerca organica da luglio 2025. +5,9% di lift medio sulla conversione
- Video di anteprima app: fino a 3, 15-30s ciascuno. Si avvia automaticamente in muto — +20-40% di lift sulla conversione
- SKStoreReviewController: max 3 prompt ogni 365 giorni
- Apple ha una curazione editoriale umana — qualità e design contano di più
- Vedi `references/apple-specs.md` per specifiche complete, dimensioni e motivi di rifiuto

### Google Play — Fatti Chiave

- Titolo (30 caratteri) + Descrizione breve (80 caratteri) + Descrizione completa (4.000 caratteri) = testo indicizzato
- La descrizione completa È indicizzata — punta a una densità di keyword del 2-3% in modo naturale
- Nessun campo keyword nascosto — tutte le keyword devono essere nel testo visibile
- Comprensione NLP/semantica di Google — il keyword stuffing viene rilevato e penalizzato
- Vietato nel titolo: emoji, TUTTO MAIUSCOLO, "best"/"#1"/"free", CTA (applicato da 2021)
- Screenshot: minimo 2, **massimo 8** per dispositivo (non 10 come Apple)
- Grafica in evidenza (1024x500, esatta) richiesta per i posizionamenti in evidenza
- Il video NON si avvia automaticamente — solo il ~6% degli utenti tocca play (basso ROI vs iOS)
- Android Vitals influisce direttamente sul posizionamento: crash >1,09% o ANR >0,47% = visibilità ridotta
- Promotional Content: invia 14 giorni prima per essere in evidenza. Le app vedono 2x acquisizioni da esplora
- Custom Store Listings: fino a 50 (possono targetizzare utenti persi, paesi specifici, campagne pubblicitarie)
- Store Listing Experiments: testa fino a 3 varianti, esegui per 7+ giorni, un esperimento alla volta
- Vedi `references/google-play-specs.md` per specifiche complete e dettagli sulle policy

### Cosa Indicizza Apple vs Cosa Indicizza Google

| Campo                 | Indicizzato da Apple?   | Indicizzato da Google?        |
| --------------------- | ---------------- | ---------------------- |
| Titolo                 | Sì              | Sì (segnale più forte) |
| Sottotitolo / descrizione breve | Sì              | Sì                      |
| Campo keyword         | Sì (nascosto)     | Non esiste            |
| Descrizione lunga      | No               | Sì (fortemente)               |
| Caption degli screenshot   | Sì (da 2025) | No                      |
| Eventi in-app         | Sì              | N/D (LiveOps invece)  |
| Nome dello sviluppatore        | No               | Parziale                |
| Nomi IAP             | Sì              | Sì                      |

---

## Checklist dei Problemi Comuni

Segnala questi se trovati. Gli elementi contrassegnati _(dipendenti dal livello)_ dovrebbero essere valutati
rispetto al livello di maturità del brand dell'app — potrebbero essere scelte deliberate per app Dominanti.

**Segnalare sempre (tutti i livelli):**

- [ ] Valutazione sotto 4.0
- [ ] Ultimo aggiornamento > 3 mesi fa
- [ ] La descrizione Google Play non ha strategia di keyword (sotto l'1% di densità)
- [ ] Google Play senza grafica in evidenza
- [ ] Il campo keyword Apple probabilmente ha parole ripetute (inferito da titolo+sottotitolo)
- [ ] Mismatch di categoria — l'app affronterebbe meno competizione in una categoria diversa
- [ ] Meno di 5 screenshot

**Segnalare solo per Sfidante/Consolidata** _(non errori per app Dominanti):_

- [ ] Il titolo spreca caratteri solo sul nome del brand (nessuna keyword) _(Dominante: il brand È la keyword)_
- [ ] Il sottotitolo/descrizione breve duplica le keyword del titolo
- [ ] Le prime 3 righe della descrizione sono generiche _(Dominante: potrebbe essere una scelta di tono di brand)_
- [ ] Nessun video di anteprima _(Dominante: potrebbe essere razionale se il prodotto è difficile da mostrare)_
- [ ] Gli screenshot sono solo dump dell'interfaccia senza messaggio/caption _(Dominante: foto lifestyle/brand potrebbero convertire meglio)_
- [ ] Solo 1-2 localizzazioni _(punteggio relativo al mercato effettivo, non al conteggio assoluto)_
- [ ] Nessun evento in-app o contenuto promozionale _(le app utility Dominanti potrebbero non aver bisogno di aiuto per la scoperta)_

**Segnalare per tutti i livelli ma notare il contesto:**

- [ ] Nessuna risposta dello sviluppatore alle recensioni negative _(nota il volume — rispondere a 10M+ recensioni è una sfida diversa rispetto a 1K)_
- [ ] Testo "Novità" generico _(accettabile a cadenza di release settimanale+ per app Consolidate/Dominanti)_

---

## Domande Specifiche per il Compito

1. Qual è l'URL di App Store o Google Play?
2. È la tua app o quella di un concorrente?
3. In quale categoria compete l'app?
4. Hai URL di concorrenti da confrontare?
5. Sei concentrato sulla visibilità di ricerca, sul tasso di conversione, o entrambi?
6. Hai accesso ai dati di App Store Connect o Google Play Console?

---

## Skill Correlate

- **cro**: Per ottimizzare la conversione delle landing page web che generano installazioni dell'app
- **ad-creative**: Per creare creative pubblicitarie per App Store e Google Play
- **analytics**: Per impostare l'attribuzione delle installazioni e il tracciamento degli eventi in-app
- **customer-research**: Per comprendere i bisogni e il linguaggio degli utenti utili al copy della scheda
