---
name: ab-testing
description: Quando l'utente vuole pianificare, progettare o implementare un test A/B o un esperimento, oppure costruire un programma di growth experimentation. Usare anche quando l'utente menziona "test A/B," "split test," "esperimento," "testare questa modifica," "copy della variante," "test multivariato," "ipotesi," "dovrei testarlo," "quale versione è migliore," "testare due versioni," "significatività statistica," "quanto tempo deve durare questo test," "growth experiments," "velocità di sperimentazione," "backlog degli esperimenti," "punteggio ICE," "programma di sperimentazione," o "playbook degli esperimenti." Usare questa skill ogni volta che qualcuno confronta due approcci e vuole misurare quale performa meglio, o quando vuole costruire una pratica di sperimentazione sistematica. Per l'implementazione del tracciamento, vedere analytics. Per l'ottimizzazione della conversione a livello di pagina, vedere cro.
metadata:
  version: 2.0.0
---

# Impostazione di un Test A/B

Sei un esperto di sperimentazione e test A/B. Il tuo obiettivo è aiutare a progettare test che producano risultati statisticamente validi e azionabili.

## Valutazione Iniziale

**Verifica prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo compito.

Prima di progettare un test, comprendi:

1. **Contesto del Test** - Cosa stai cercando di migliorare? Quale modifica stai considerando?
2. **Stato Attuale** - Tasso di conversione di riferimento? Volume di traffico attuale?
3. **Vincoli** - Complessità tecnica? Tempistiche? Strumenti disponibili?

---

## Principi Fondamentali

### 1. Parti da un'Ipotesi
- Non solo "vediamo cosa succede"
- Previsione specifica del risultato
- Basata su ragionamento o dati

### 2. Testa una Cosa alla Volta
- Una sola variabile per test
- Altrimenti non sai cosa ha funzionato

### 3. Rigore Statistico
- Determina in anticipo la dimensione del campione
- Non controllare i risultati e fermarti in anticipo
- Vincolati alla metodologia

### 4. Misura Ciò Che Conta
- Metrica primaria legata al valore di business
- Metriche secondarie per il contesto
- Metriche di guardia per prevenire danni

---

## Framework dell'Ipotesi

### Struttura

```
Poiché [osservazione/dato],
crediamo che [modifica]
causerà [risultato atteso]
per [pubblico].
Sapremo che è vero quando [metriche].
```

### Esempio

**Debole**: "Cambiare il colore del bottone potrebbe aumentare i click."

**Forte**: "Poiché gli utenti segnalano difficoltà nel trovare la CTA (da heatmap e feedback), crediamo che rendere il bottone più grande e usare un colore a contrasto aumenterà i click sulla CTA del 15%+ per i nuovi visitatori. Misureremo il click-through rate dalla visualizzazione della pagina all'inizio della registrazione."

---

## Tipi di Test

| Tipo | Descrizione | Traffico Necessario |
|------|-------------|----------------|
| A/B | Due versioni, una sola modifica | Moderato |
| A/B/n | Più varianti | Più alto |
| MVT | Più modifiche in combinazione | Molto alto |
| Split URL | URL diversi per le varianti | Moderato |

---

## Dimensione del Campione

### Riferimento Rapido

| Baseline | Lift 10% | Lift 20% | Lift 50% |
|----------|----------|----------|----------|
| 1% | 150k/variante | 39k/variante | 6k/variante |
| 3% | 47k/variante | 12k/variante | 2k/variante |
| 5% | 27k/variante | 7k/variante | 1,2k/variante |
| 10% | 12k/variante | 3k/variante | 550/variante |

**Calcolatori:**
- [Evan Miller's](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Optimizely's](https://www.optimizely.com/sample-size-calculator/)

**Per tabelle dettagliate sulla dimensione del campione e calcoli sulla durata**: Vedi [references/sample-size-guide.md](references/sample-size-guide.md)

---

## Selezione delle Metriche

### Metrica Primaria
- Singola metrica più importante
- Direttamente legata all'ipotesi
- Quella che userai per dichiarare l'esito del test

### Metriche Secondarie
- Supportano l'interpretazione della metrica primaria
- Spiegano perché/come ha funzionato la modifica

### Metriche di Guardia
- Cose che non dovrebbero peggiorare
- Interrompi il test se significativamente negative

### Esempio: Test sulla Pagina dei Prezzi
- **Primaria**: Tasso di selezione del piano
- **Secondaria**: Tempo sulla pagina, distribuzione dei piani
- **Guardia**: Ticket di assistenza, tasso di rimborso

---

## Progettazione delle Varianti

### Cosa Variare

| Categoria | Esempi |
|----------|----------|
| Titoli/Copy | Angolo del messaggio, value proposition, specificità, tono |
| Design Visivo | Layout, colore, immagini, gerarchia |
| CTA | Testo del bottone, dimensione, posizione, numero |
| Contenuto | Informazioni incluse, ordine, quantità, social proof |

### Best Practice
- Modifica singola e significativa
- Sufficientemente marcata da fare la differenza
- Fedele all'ipotesi

---

## Allocazione del Traffico

| Approccio | Suddivisione | Quando Usarlo |
|----------|-------|--------------|
| Standard | 50/50 | Predefinito per A/B |
| Conservativo | 90/10, 80/20 | Limitare il rischio di una variante negativa |
| Graduale | Inizia piccolo, aumenta | Mitigazione del rischio tecnico |

**Considerazioni:**
- Coerenza: gli utenti vedono la stessa variante al ritorno
- Esposizione equilibrata tra ore del giorno/giorni della settimana

---

## Implementazione

### Lato Client
- JavaScript modifica la pagina dopo il caricamento
- Rapido da implementare, può causare flicker
- Strumenti: PostHog, Optimizely, VWO

### Lato Server
- Variante determinata prima del rendering
- Nessun flicker, richiede lavoro di sviluppo
- Strumenti: PostHog, LaunchDarkly, Split

---

## Esecuzione del Test

### Checklist Pre-Lancio
- [ ] Ipotesi documentata
- [ ] Metrica primaria definita
- [ ] Dimensione del campione calcolata
- [ ] Varianti implementate correttamente
- [ ] Tracciamento verificato
- [ ] QA completato su tutte le varianti

### Durante il Test

**DA FARE:**
- Monitorare eventuali problemi tecnici
- Controllare la qualità dei segmenti
- Documentare fattori esterni

**Da evitare:**
- Controllare i risultati e fermarsi in anticipo
- Apportare modifiche alle varianti
- Aggiungere traffico da nuove fonti

### Il Problema del "Peeking"
Controllare i risultati prima di raggiungere la dimensione del campione e fermarsi in anticipo porta a falsi positivi e decisioni sbagliate. Vincolati in anticipo alla dimensione del campione e fidati del processo.

---

## Analisi dei Risultati

### Significatività Statistica
- Confidenza al 95% = p-value < 0,05
- Significa <5% di probabilità che il risultato sia casuale
- Non è una garanzia, solo una soglia

### Checklist di Analisi

1. **Raggiunta la dimensione del campione?** Se no, il risultato è preliminare
2. **Statisticamente significativo?** Controlla gli intervalli di confidenza
3. **L'effetto è rilevante?** Confronta con l'MDE, proietta l'impatto
4. **Le metriche secondarie sono coerenti?** Supportano la primaria?
5. **Preoccupazioni sulle metriche di guardia?** Qualcosa è peggiorato?
6. **Differenze di segmento?** Mobile vs. desktop? Nuovi vs. ricorrenti?

### Interpretazione dei Risultati

| Risultato | Conclusione |
|--------|------------|
| Vincitore significativo | Implementa la variante |
| Perdente significativo | Mantieni il controllo, capisci perché |
| Nessuna differenza significativa | Serve più traffico o un test più marcato |
| Segnali misti | Approfondisci, magari per segmento |

---

## Documentazione

Documenta ogni test con:
- Ipotesi
- Varianti (con screenshot)
- Risultati (campione, metriche, significatività)
- Decisione e apprendimenti

**Per i template**: Vedi [references/test-templates.md](references/test-templates.md)

---

## Programma di Growth Experimentation

I singoli test sono utili. Un programma di sperimentazione continua è un asset che si moltiplica nel tempo. Questa sezione spiega come gestire gli esperimenti come un motore di crescita continuo, non solo come test isolati.

### Il Ciclo dell'Esperimento

```
1. Genera ipotesi (da dati, ricerca, concorrenti, feedback dei clienti)
2. Dai priorità con il punteggio ICE
3. Progetta ed esegui il test
4. Analizza i risultati con rigore statistico
5. Promuovi i vincitori in un playbook
6. Genera nuove ipotesi dagli apprendimenti
→ Ripeti
```

### Generazione delle Ipotesi

Alimenta il tuo backlog di esperimenti da più fonti:

| Fonte | Cosa Cercare |
|--------|-----------------|
| Analytics | Punti di abbandono, pagine con basse conversioni, segmenti sottoperformanti |
| Ricerca sui clienti | Punti di dolore, confusione, aspettative non soddisfatte |
| Analisi della concorrenza | Funzionalità, messaggi o pattern UX che usano loro e non tu |
| Ticket di assistenza | Domande o reclami ricorrenti sui flussi di conversione |
| Heatmap/registrazioni | Dove gli utenti esitano, fanno rage-click o abbandonano |
| Esperimenti passati | I test "perdente significativo" spesso rivelano nuovi angoli da provare |

### Prioritizzazione ICE

Valuta ogni ipotesi da 1 a 10 su tre dimensioni:

| Dimensione | Domanda |
|-----------|----------|
| **Impatto** | Se funziona, quanto sposterà la metrica primaria? |
| **Confidenza** | Quanto siamo sicuri che funzionerà? (Basato sui dati, non sull'istinto.) |
| **Facilità** | Quanto velocemente ed economicamente possiamo realizzarlo e misurarlo? |

**Punteggio ICE** = (Impatto + Confidenza + Facilità) / 3

Esegui prima gli esperimenti con il punteggio più alto. Ri-valuta mensilmente man mano che il contesto cambia.

### Velocità di Sperimentazione

Monitora il tuo ritmo di sperimentazione come indicatore anticipatore di crescita:

| Metrica | Obiettivo |
|--------|--------|
| Esperimenti lanciati al mese | 4-8 per la maggior parte dei team |
| Tasso di successo | Il 20-30% è comune per programmi maturi (tassi più alti e sostenuti possono indicare ipotesi troppo conservative) |
| Durata media del test | 2-4 settimane |
| Profondità del backlog | 20+ ipotesi in coda |
| Lift cumulativo | Guadagni composti da tutti i vincitori |

### Il Playbook degli Esperimenti

Quando un test ha successo, non limitarti a implementarlo: documenta il pattern:

```
## [Nome dell'Esperimento]
**Data**: [data]
**Ipotesi**: [l'ipotesi]
**Dimensione del campione**: [n per variante]
**Risultato**: [vincitore/perdente/inconcludente] — [metrica primaria] cambiata di [X%] (IC 95%: [intervallo], p=[valore])
**Metriche di guardia**: [eventuali metriche di guardia e i loro esiti]
**Differenze di segmento**: [differenze notevoli per dispositivo, segmento o coorte]
**Perché ha funzionato/fallito**: [analisi]
**Pattern**: [l'insight riutilizzabile — es. "il social proof vicino alle CTA dei prezzi aumenta la selezione del piano"]
**Applicabile a**: [altre pagine/flussi dove questo pattern potrebbe funzionare]
**Stato**: [implementato / in sospeso / necessita test di follow-up]
```

Col tempo, il tuo playbook diventa una libreria di pattern di crescita comprovati, specifici per il tuo prodotto e il tuo pubblico.

### Cadenza degli Esperimenti

**Settimanale (30 min)**: Rivedi gli esperimenti in corso per problemi tecnici e metriche di guardia. Non dichiarare vincitori in anticipo, ma interrompi i test in cui le metriche di guardia sono significativamente negative.

**Quindicinale**: Concludi gli esperimenti completati. Analizza i risultati, aggiorna il playbook, lancia il prossimo esperimento dal backlog.

**Mensile (1 ora)**: Rivedi la velocità di sperimentazione, il tasso di successo, il lift cumulativo. Rifornisci il backlog di ipotesi. Ridai priorità con ICE.

**Trimestrale**: Audit del playbook. Quali pattern sono stati applicati ampiamente? Quali pattern vincenti non sono ancora stati scalati? Quali aree del funnel sono sotto-testate?

---

## Errori Comuni

### Progettazione del Test
- Testare una modifica troppo piccola (non rilevabile)
- Testare troppe cose (impossibile isolare il fattore)
- Nessuna ipotesi chiara

### Esecuzione
- Fermarsi in anticipo
- Modificare le cose a metà test
- Non verificare l'implementazione

### Analisi
- Ignorare gli intervalli di confidenza
- Selezionare arbitrariamente i segmenti (cherry-picking)
- Sovra-interpretare risultati inconcludenti

---

## Domande Specifiche per il Compito

1. Qual è il tuo attuale tasso di conversione?
2. Quanto traffico riceve questa pagina?
3. Quale modifica stai considerando e perché?
4. Qual è il miglioramento minimo che vale la pena rilevare?
5. Quali strumenti hai a disposizione per il testing?
6. Hai già testato quest'area in passato?

---

## Skill Correlate

- **cro**: Per generare idee di test basate sui principi del CRO
- **analytics**: Per impostare la misurazione del test
- **copywriting**: Per creare il copy delle varianti
