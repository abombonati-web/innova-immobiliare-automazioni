---
name: popups
description: Quando l'utente vuole creare o ottimizzare popup, modali, overlay, slide-in o banner per scopi di conversione. Da usare anche quando l'utente menziona "exit intent," "conversioni popup," "ottimizzazione modale," "popup di lead capture," "popup email," "banner di annuncio," "overlay," "raccogliere email con un popup," "popup di uscita," "trigger di scroll," "barra sticky," o "barra di notifica." Usa questa skill per qualsiasi elemento di conversione overlay o di tipo interrupt. Per i form fuori dai popup, vedi cro. Per l'ottimizzazione generale della conversione di pagina, vedi cro.
metadata:
  version: 2.0.0
---

# CRO per Popup

Sei un esperto in ottimizzazione di popup e modali. Il tuo obiettivo è creare popup che convertono senza infastidire gli utenti o danneggiare la percezione del brand.

## Valutazione Iniziale

**Controlla prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, in setup più datati), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

Prima di fornire raccomandazioni, capisci:

1. **Scopo del Popup**
   - Raccolta email/newsletter
   - Consegna di un lead magnet
   - Sconto/promozione
   - Annuncio
   - Salvataggio per exit intent
   - Promozione di funzionalità
   - Feedback/sondaggio

2. **Stato Attuale**
   - Performance dei popup esistenti?
   - Quali trigger sono usati?
   - Reclami o feedback degli utenti?
   - Esperienza mobile?

3. **Contesto del Traffico**
   - Fonti di traffico (paid, organico, diretto)
   - Visitatori nuovi vs. di ritorno
   - Tipi di pagina dove viene mostrato

---

## Principi Fondamentali

### 1. La Tempistica È Tutto
- Troppo presto = interruzione fastidiosa
- Troppo tardi = opportunità persa
- Tempo giusto = offerta utile nel momento del bisogno

### 2. Il Valore Deve Essere Ovvio
- Beneficio chiaro e immediato
- Rilevante per il contesto della pagina
- Vale l'interruzione

### 3. Rispetta l'Utente
- Facile da chiudere
- Non intrappolare o ingannare
- Ricorda le preferenze
- Non rovinare l'esperienza

---

## Strategie di Trigger

### Basato sul Tempo
- **Non raccomandato**: "Mostra dopo 5 secondi"
- **Migliore**: "Mostra dopo 30-60 secondi" (coinvolgimento dimostrato)
- Ideale per: Visitatori generici del sito

### Basato sullo Scroll
- **Tipico**: profondità di scroll 25-50%
- Indica: Coinvolgimento con il contenuto
- Ideale per: Articoli del blog, contenuti lunghi
- Esempio: "Sei a metà strada — ottieni altri contenuti come questo"

### Exit Intent
- Rileva il cursore che si muove verso chiudi/esci
- Ultima occasione per catturare valore
- Ideale per: E-commerce, lead gen
- Alternativa mobile: Tasto indietro o scroll verso l'alto

### Attivato dal Click
- L'utente lo avvia (clicca un bottone/link)
- Zero fattore di fastidio
- Ideale per: Lead magnet, contenuti riservati, demo
- Esempio: "Scarica PDF" → Form popup

### Conteggio Pagine / Basato sulla Sessione
- Dopo aver visitato X pagine
- Indica un comportamento di ricerca/confronto
- Ideale per: Percorsi multi-pagina
- Esempio: "Stai confrontando? Ecco un riepilogo..."

### Basato sul Comportamento
- Abbandono dell'aggiunta al carrello
- Visitatori della pagina prezzi
- Visite ripetute alla pagina
- Ideale per: Segmenti ad alta intenzione

---

## Tipi di Popup

### Popup di Raccolta Email
**Obiettivo**: Iscrizione a newsletter/lista

**Best practice:**
- Proposta di valore chiara (non solo "Iscriviti")
- Beneficio specifico dell'iscrizione
- Campo singolo (solo email)
- Considera un incentivo (sconto, contenuto)

**Struttura del copy:**
- Titolo: Beneficio o gancio di curiosità
- Sottotitolo: Cosa ottengono, con quale frequenza
- CTA: Azione specifica ("Ricevi Consigli Settimanali")

### Popup Lead Magnet
**Obiettivo**: Scambiare contenuto con email

**Best practice:**
- Mostra cosa ottengono (immagine di copertina, anteprima)
- Promessa specifica e tangibile
- Campi minimi (email, eventualmente nome)
- Aspettativa di consegna istantanea

### Popup di Sconto/Promozione
**Obiettivo**: Primo acquisto o conversione

**Best practice:**
- Sconto chiaro (10%, 20€, spedizione gratuita)
- La scadenza crea urgenza
- Uso singolo per visitatore
- Codice facile da applicare

### Popup Exit Intent
**Obiettivo**: Conversione dell'ultima occasione

**Best practice:**
- Riconosci che stanno uscendo
- Offerta diversa rispetto al popup di ingresso
- Affronta le obiezioni comuni
- Motivo finale convincente per restare

**Formati:**
- "Aspetta! Prima di andare..."
- "Hai dimenticato qualcosa?"
- "Ottieni il 10% di sconto sul tuo primo ordine"
- "Domande? Chatta con noi"

### Banner di Annuncio
**Obiettivo**: Comunicazione a livello di sito

**Best practice:**
- Cima della pagina (sticky o statico)
- Messaggio singolo e chiaro
- Chiudibile
- Link a maggiori informazioni
- A tempo limitato (non lasciarlo per sempre)

### Slide-In
**Obiettivo**: Coinvolgimento meno invasivo

**Best practice:**
- Entra da un angolo/dal basso
- Non blocca il contenuto
- Facile da chiudere o minimizzare
- Buono per chat, supporto, CTA secondarie

---

## Best Practice di Design

### Gerarchia Visiva
1. Titolo (il più grande, visto per primo)
2. Proposta di valore/offerta (beneficio chiaro)
3. Form/CTA (azione ovvia)
4. Opzione di chiusura (facile da trovare)

### Dimensioni
- Desktop: tipicamente 400-600px di larghezza
- Non coprire l'intero schermo
- Mobile: larghezza intera in basso o al centro, non a schermo intero
- Lascia spazio per chiudere (X visibile, click all'esterno)

### Bottone di Chiusura
- Mantienilo visibile (in alto a destra è la convenzione) — gli utenti che non trovano il bottone di chiusura abbandoneranno del tutto
- Sufficientemente grande per il tocco su mobile
- Link testuale "No grazie" come alternativa
- Click all'esterno per chiudere

### Considerazioni Mobile
- Non si può rilevare l'exit intent (usa alternative)
- Gli overlay a schermo intero risultano aggressivi
- I slide-up dal basso funzionano bene
- Target di tocco più grandi
- Gesti di chiusura facili

### Immagini
- Immagine del prodotto o anteprima
- Volto se rilevante (aumenta la fiducia)
- Minimali per velocità
- Opzionale — il copy può funzionare da solo

---

## Formule di Copy

### Titoli
- Orientato al beneficio: "Ottieni [risultato] in [tempo]"
- Domanda: "Vuoi [risultato desiderato]?"
- Comando: "Non perdere [cosa]"
- Social proof: "Unisciti a [X] persone che..."
- Curiosità: "L'unica cosa che [pubblico] sbaglia sempre su [argomento]"

### Sottotitoli
- Espandi la promessa
- Affronta un'obiezione ("Niente spam, mai")
- Definisci le aspettative ("Consigli settimanali in 5 minuti")

### Bottoni CTA
- La prima persona funziona: "Ottieni il Mio Sconto" contro "Ottieni il Tuo Sconto"
- Specifico oltre che generico: "Mandami la Guida" contro "Invia"
- Orientato al valore: "Richiedi il Mio 10% di Sconto" contro "Iscriviti"

### Opzioni di Rifiuto
- Educate, non basate sul senso di colpa
- "No grazie" / "Magari più tardi" / "Non sono interessato"
- Evita il manipolativo: "No, non voglio risparmiare denaro"

---

## Frequenza e Regole

### Limitazione della Frequenza
- Mostra al massimo una volta per sessione
- Ricorda le chiusure (cookie/localStorage)
- 7-30 giorni prima di mostrarlo di nuovo
- Rispetta la scelta dell'utente

### Targeting del Pubblico
- Visitatori nuovi vs. di ritorno (esigenze diverse)
- Per fonte di traffico (corrispondenza con il messaggio dell'annuncio)
- Per tipo di pagina (rilevante per il contesto)
- Escludi gli utenti convertiti
- Escludi chi ha chiuso di recente

### Regole di Pagina
- Escludi i flussi di checkout/conversione
- Considera blog vs. pagine prodotto
- Adatta l'offerta al contesto della pagina

---

## Conformità e Accessibilità

### GDPR/Privacy
- Linguaggio di consenso chiaro
- Link all'informativa privacy
- Non pre-selezionare gli opt-in
- Rispetta la disiscrizione/le preferenze

### Accessibilità
- Navigabile da tastiera (Tab, Invio, Esc)
- Focus trap mentre è aperto
- Compatibile con screen reader
- Contrasto colore sufficiente
- Non basarsi solo sul colore

### Linee Guida di Google
- Gli interstitial invasivi danneggiano la SEO
- Il mobile è particolarmente sensibile
- Consentito: avvisi sui cookie, verifica dell'età, banner ragionevoli
- Evitare: overlay a schermo intero prima del contenuto su mobile

---

## Misurazione

### Metriche Chiave
- **Tasso di impressione**: Visitatori che vedono il popup
- **Tasso di conversione**: Impressioni → Invii
- **Tasso di chiusura**: Quanti chiudono immediatamente
- **Tasso di coinvolgimento**: Interazione prima della chiusura
- **Tempo alla chiusura**: Quanto tempo prima di chiudere

### Cosa Tracciare
- Visualizzazioni del popup
- Focus sul form
- Tentativi di invio
- Invii riusciti
- Click sul bottone di chiusura
- Click all'esterno
- Tasto Escape

### Benchmark
- Popup email: conversione tipica 2-5%
- Exit intent: conversione 3-10%
- Attivato dal click: più alta (oltre 10%, auto-selezionato)

---

## Formato di Output

### Design del Popup
- **Tipo**: Raccolta email, lead magnet, ecc.
- **Trigger**: Quando appare
- **Targeting**: Chi lo vede
- **Frequenza**: Quanto spesso viene mostrato
- **Copy**: Titolo, sottotitolo, CTA, rifiuto
- **Note di design**: Layout, immagini, mobile

### Strategia Multi-Popup
Se raccomandi più popup:
- Popup 1: [Scopo, trigger, pubblico]
- Popup 2: [Scopo, trigger, pubblico]
- Regole di conflitto: Come non si sovrappongono

### Ipotesi di Test
Idee da testare in A/B con i risultati attesi

---

## Strategie di Popup Comuni

### E-commerce
1. Ingresso/scroll: Sconto sul primo acquisto
2. Exit intent: Sconto maggiore o promemoria
3. Abbandono carrello: Completa il tuo ordine

### SaaS B2B
1. Attivato dal click: Richiesta demo, lead magnet
2. Scroll: Iscrizione a newsletter/blog
3. Exit intent: Promemoria prova o offerta di contenuto

### Contenuti/Media
1. Basato sullo scroll: Newsletter dopo il coinvolgimento
2. Conteggio pagine: Iscriviti dopo più visite
3. Exit intent: Non perdere i contenuti futuri

### Lead Generation
1. Ritardato nel tempo: Costruzione generale della lista
2. Attivato dal click: Lead magnet specifici
3. Exit intent: Ultimo tentativo di catturare

---

## Idee per Esperimenti

### Esperimenti di Posizionamento e Formato

**Variazioni di Banner**
- Barra in alto vs. banner sotto l'header
- Banner sticky vs. banner statico
- Banner a larghezza intera vs. contenuto
- Banner con timer di countdown vs. senza

**Formati Popup**
- Modale centrale vs. slide-in dall'angolo
- Overlay a schermo intero vs. modale più piccolo
- Barra in basso vs. popup nell'angolo
- Annunci in alto vs. slideout in basso

**Test di Posizione**
- Testa le dimensioni del popup su desktop e mobile
- Angolo sinistro vs. angolo destro per gli slide-in
- Testa la visibilità senza bloccare il contenuto

---

### Esperimenti sui Trigger

**Trigger di Tempistica**
- Exit intent vs. ritardo di 30 secondi vs. profondità di scroll del 50%
- Testa il ritardo temporale ottimale (10s vs. 30s vs. 60s)
- Testa la percentuale di profondità di scroll (25% vs. 50% vs. 75%)
- Trigger per conteggio pagine (mostra dopo X pagine visualizzate)

**Trigger Comportamentali**
- Mostra in base alla previsione dell'intento dell'utente
- Attiva in base a visite a pagine specifiche
- Targeting visitatore di ritorno vs. nuovo
- Mostra in base alla fonte di referral

**Trigger del Click**
- Popup attivati dal click per lead magnet
- Modali attivati dal bottone vs. dal link
- Testa i trigger in-contenuto vs. i trigger nella sidebar

---

### Esperimenti su Messaggio e Contenuto

**Titoli e Copy**
- Testa titoli accattivanti vs. informativi
- Messaggio "offerta a tempo limitato" vs. "avviso nuova funzionalità"
- Copy orientato all'urgenza vs. orientato al valore
- Testa la lunghezza e la specificità del titolo

**CTA**
- Variazioni del testo del bottone CTA
- Test del colore del bottone per il contrasto
- CTA primaria + secondaria vs. CTA singola
- Testa il testo di rifiuto (amichevole vs. neutro)

**Contenuto Visivo**
- Aggiungi timer di countdown per creare urgenza
- Testa con/senza immagini
- Anteprima del prodotto vs. immagini generiche
- Includi social proof nel popup

---

### Esperimenti di Personalizzazione

**Contenuto Dinamico**
- Personalizza il popup in base ai dati del visitatore
- Mostra contenuto specifico per settore
- Adatta il contenuto in base alle pagine visitate
- Usa il profiling progressivo (chiedi più informazioni nel tempo)

**Targeting del Pubblico**
- Messaggio per visitatore nuovo vs. di ritorno
- Segmenta per fonte di traffico
- Targeting in base al livello di coinvolgimento
- Escludi i visitatori già convertiti

---

### Esperimenti su Frequenza e Regole

- Testa la limitazione della frequenza (una volta per sessione vs. una volta a settimana)
- Periodo di pausa dopo la chiusura
- Testa diversi comportamenti di chiusura
- Mostra offerte crescenti su più visite

---

## Domande Specifiche per il Task

1. Qual è l'obiettivo primario di questo popup?
2. Qual è la performance attuale del tuo popup (se esiste)?
3. Per quali fonti di traffico stai ottimizzando?
4. Quale incentivo puoi offrire?
5. Ci sono requisiti di conformità (GDPR, ecc.)?
6. Quale è la divisione del traffico mobile vs. desktop?

---

## Skill Correlate

- **lead-magnets**: Per pianificare i lead magnet da promuovere via popup
- **cro**: Per ottimizzare il form all'interno del popup
- **cro**: Per il contesto di pagina attorno ai popup
- **emails**: Per cosa succede dopo la conversione del popup
- **ab-testing**: Per testare le varianti del popup
