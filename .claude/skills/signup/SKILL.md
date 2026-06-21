---
name: signup
description: Quando l'utente vuole ottimizzare flussi di signup, registrazione, creazione account o attivazione di trial. Usa questa skill anche quando l'utente menziona "conversioni signup," "frizione nella registrazione," "ottimizzazione form di signup," "signup per trial gratuito," "ridurre l'abbandono nel signup," "flusso di creazione account," "le persone non si registrano," "abbandono del signup," "tasso di conversione del trial," "nessuno completa la registrazione," "troppi passaggi per registrarsi," o "semplificare il nostro signup." Usa questa skill ogni volta che l'utente ha un flusso di signup o registrazione che non sta performando. Per l'onboarding post-signup, vedi onboarding. Per i form di lead capture (non creazione account), vedi cro.
metadata:
  version: 2.0.0
---

# CRO del Flusso di Signup

Sei un esperto nell'ottimizzazione dei flussi di signup e registrazione. Il tuo obiettivo è ridurre la frizione, aumentare i tassi di completamento e impostare gli utenti per un'attivazione di successo.

## Valutazione Iniziale

**Controlla prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

Prima di fornire raccomandazioni, capisci:

1. **Tipo di Flusso**
   - Signup per trial gratuito
   - Creazione account freemium
   - Creazione account a pagamento
   - Signup per waitlist/accesso anticipato
   - B2B vs B2C

2. **Stato Attuale**
   - Quanti step/schermate?
   - Quali campi sono obbligatori?
   - Qual è il tasso di completamento attuale?
   - Dove abbandonano gli utenti?

3. **Vincoli di Business**
   - Quali dati sono genuinamente necessari al signup?
   - Ci sono requisiti di compliance?
   - Cosa succede immediatamente dopo il signup?

---

## Principi Fondamentali

### 1. Minimizza i Campi Obbligatori
Ogni campo riduce la conversione. Per ogni campo, chiediti:
- Ci serve assolutamente questo dato prima che possano usare il prodotto?
- Possiamo raccoglierlo dopo tramite progressive profiling?
- Possiamo dedurlo da altri dati?

**Priorità tipica dei campi:**
- Essenziale: Email (o telefono), Password
- Spesso necessario: Nome
- Solitamente differibile: Azienda, Ruolo, Dimensione del team, Telefono, Indirizzo

### 2. Mostra il Valore Prima di Chiedere l'Impegno
- Cosa puoi mostrare/dare prima di richiedere il signup?
- Possono provare il prodotto prima di creare un account?
- Inverti l'ordine: prima il valore, poi il signup

### 3. Riduci lo Sforzo Percepito
- Mostra l'avanzamento se multi-step
- Raggruppa i campi correlati
- Usa default intelligenti
- Pre-compila quando possibile

### 4. Rimuovi l'Incertezza
- Aspettative chiare ("Richiede 30 secondi")
- Mostra cosa succede dopo il signup
- Nessuna sorpresa (requisiti nascosti, passaggi inattesi)

---

## Ottimizzazione Campo per Campo

### Campo Email
- Campo singolo (nessun campo di conferma email)
- Validazione inline del formato
- Controllo dei typo comuni (gmial.com → gmail.com)
- Messaggi di errore chiari

### Campo Password
- Mostra il toggle per visualizzare la password (icona occhio)
- Mostra i requisiti in anticipo, non dopo un fallimento
- Considera suggerimenti per passphrase per la robustezza
- Aggiorna gli indicatori dei requisiti in tempo reale

**UX migliore per la password:**
- Permetti il paste (non disabilitarlo)
- Mostra un indicatore di robustezza invece di regole rigide
- Considera opzioni passwordless

### Campo Nome
- Campo unico "Nome completo" vs. divisione Nome/Cognome (testalo)
- Richiedilo solo se usato immediatamente (personalizzazione)
- Considera di renderlo opzionale

### Opzioni di Social Auth
- Posizionale in modo prominente (spesso conversione più alta dell'email)
- Mostra le opzioni più rilevanti per il tuo pubblico
  - B2C: Google, Apple, Facebook
  - B2B: Google, Microsoft, SSO
- Separazione visiva chiara dal signup via email
- Considera "Registrati con Google" come opzione primaria

### Numero di Telefono
- Differiscilo a meno che non sia essenziale (verifica SMS, lead da chiamare)
- Se obbligatorio, spiega il perché
- Usa il tipo di input corretto con gestione del prefisso internazionale
- Formattalo mentre l'utente digita

### Azienda/Organizzazione
- Differiscilo se possibile
- Auto-suggerimento durante la digitazione
- Deduci dal dominio email quando possibile

### Domande su Uso/Ruolo
- Differiscile all'onboarding se possibile
- Se necessarie al signup, mantieni una sola domanda
- Usa la disclosure progressiva (non mostrare tutte le opzioni insieme)

---

## Singolo Step vs. Multi-Step

### Il Singolo Step Funziona Quando:
- 3 campi o meno
- Prodotti B2C semplici
- Visitatori ad alta intenzione (da ads, waitlist)

### Il Multi-Step Funziona Quando:
- Servono più di 3-4 campi
- Prodotti B2B complessi che necessitano segmentazione
- Devi raccogliere diversi tipi di informazioni

### Best Practice per il Multi-Step
- Mostra un indicatore di avanzamento
- Inizia con domande facili (nome, email)
- Metti le domande più difficili più avanti (dopo l'impegno psicologico)
- Ogni step dovrebbe sembrare completabile in pochi secondi
- Permetti la navigazione all'indietro
- Salva l'avanzamento (non perdere i dati al refresh)

**Pattern di impegno progressivo:**
1. Solo email (barriera più bassa)
2. Password + nome
3. Domande di personalizzazione (opzionali)

---

## Fiducia e Riduzione della Frizione

### A Livello di Form
- "Nessuna carta di credito richiesta" (se vero)
- "Gratis per sempre" oppure "Trial gratuito di 14 giorni"
- Nota sulla privacy: "Non condivideremo mai la tua email"
- Badge di sicurezza se rilevanti
- Testimonianza vicino al form di signup

### Gestione degli Errori
- Validazione inline (non solo all'invio)
- Messaggi di errore specifici ("Email già registrata" + percorso di recupero)
- Non svuotare il form in caso di errore
- Focus sul campo problematico

### Microcopy
- Testo placeholder: Usalo per esempi, non per le etichette
- Etichette: Mantienile visibili (non solo come placeholder) — i placeholder scompaiono mentre si digita, lasciando gli utenti incerti su cosa stanno compilando
- Testo di aiuto: Solo quando necessario, posizionato vicino al campo

---

## Ottimizzazione del Signup Mobile

- Aree di tocco più ampie (altezza 44px+)
- Tipi di tastiera appropriati (email, tel, ecc.)
- Supporto autofill
- Riduci la digitazione (social auth, pre-compilazione)
- Layout a colonna singola
- Bottone CTA sticky
- Testa su dispositivi reali

---

## Esperienza Post-Invio

### Stato di Successo
- Conferma chiara
- Prossimo step immediato
- Se è richiesta la verifica email:
  - Spiega cosa fare
  - Opzione di rinvio facile
  - Promemoria di controllare lo spam
  - Opzione per correggere l'email se errata

### Flussi di Verifica
- Considera di ritardare la verifica fino a quando necessario
- Magic link come alternativa alla password
- Permetti agli utenti di esplorare mentre attendono la verifica
- Re-engagement chiaro se la verifica si blocca

---

## Misurazione

### Metriche Chiave
- Tasso di avvio del form (arrivo → inizio compilazione)
- Tasso di completamento del form (avvio → invio)
- Abbandono a livello di campo (quali campi fanno perdere persone)
- Tempo di completamento
- Tasso di errore per campo
- Completamento mobile vs. desktop

### Cosa Tracciare
- Ogni interazione con il campo (focus, blur, errore)
- Avanzamento degli step nel multi-step
- Rapporto social auth vs. signup via email
- Tempo tra gli step

---

## Formato di Output

### Risultati dell'Audit
Per ogni problema trovato:
- **Problema**: Cosa non va
- **Impatto**: Perché è importante (con impatto stimato se possibile)
- **Soluzione**: Raccomandazione specifica
- **Priorità**: Alta/Media/Bassa

### Modifiche Raccomandate
Organizzate per:
1. Quick win (correzioni nello stesso giorno)
2. Modifiche ad alto impatto (sforzo a livello settimanale)
3. Ipotesi da testare (cose da testare in A/B)

### Redesign del Form (se richiesto)
- Set di campi raccomandato con motivazione
- Ordine dei campi
- Copy per etichette, placeholder, bottoni, errori
- Suggerimenti di layout visivo

---

## Pattern Comuni di Flussi di Signup

### Trial B2B SaaS
1. Email + Password (o auth Google)
2. Nome + Azienda (opzionale: ruolo)
3. → Flusso di onboarding

### App B2C
1. Auth Google/Apple OPPURE Email
2. → Esperienza del prodotto
3. Completamento profilo successivamente

### Waitlist/Accesso Anticipato
1. Solo email
2. Opzionale: domanda su ruolo/uso
3. → Conferma waitlist

### Account E-commerce
1. Checkout come ospite come default
2. Creazione account opzionale post-acquisto
3. OPPURE Social auth con un solo click

---

## Idee per Esperimenti

### Esperimenti sul Design del Form

**Layout e Struttura**
- Flusso di signup a singolo step vs. multi-step
- Multi-step con barra di avanzamento vs. senza
- Layout dei campi a 1 colonna vs. 2 colonne
- Form integrato nella pagina vs. pagina di signup separata
- Allineamento orizzontale vs. verticale dei campi

**Ottimizzazione dei Campi**
- Riduci ai campi minimi (solo email + password)
- Aggiungi o rimuovi il campo numero di telefono
- Campo unico "Nome" vs. divisione "Nome/Cognome"
- Aggiungi o rimuovi il campo azienda/organizzazione
- Testa l'equilibrio tra campi obbligatori vs. opzionali

**Opzioni di Autenticazione**
- Aggiungi opzioni SSO (Google, Microsoft, GitHub, LinkedIn)
- SSO prominente vs. form email prominente
- Testa quali opzioni SSO risuonano (varia per pubblico)
- Solo SSO vs. SSO + opzione email

**Design Visivo**
- Testa colori e dimensioni dei bottoni per la prominenza della CTA
- Sfondo semplice vs. visual legati al prodotto
- Testa lo stile del contenitore del form (card vs. minimale)
- Test di layout ottimizzato per mobile

---

### Esperimenti su Copy e Messaggi

**Titoli e CTA**
- Testa variazioni di titolo sopra il form di signup
- Testo del bottone CTA: "Crea account" vs. "Inizia il trial gratuito" vs. "Inizia ora"
- Aggiungi chiarezza sulla durata del trial nella CTA
- Testa l'enfasi della proposta di valore nell'intestazione del form

**Microcopy**
- Etichette dei campi: minimali vs. descrittive
- Ottimizzazione del testo placeholder
- Chiarezza e tono dei messaggi di errore
- Visualizzazione dei requisiti password (in anticipo vs. dopo l'errore)

**Elementi di Fiducia**
- Aggiungi social proof vicino al form di signup
- Testa badge di fiducia vicino al form (sicurezza, compliance)
- Aggiungi messaggi "Nessuna carta di credito richiesta"
- Includi copy di rassicurazione sulla privacy

---

### Esperimenti su Trial e Impegno

**Variazioni del Trial Gratuito**
- Carta di credito richiesta vs. non richiesta per il trial
- Testa l'impatto della durata del trial (7 vs. 14 vs. 30 giorni)
- Modello freemium vs. trial gratuito
- Trial con funzionalità limitate vs. accesso completo

**Punti di Frizione**
- Verifica email richiesta vs. ritardata vs. rimossa
- Testa l'impatto del CAPTCHA sul completamento
- Checkbox di accettazione termini vs. accettazione implicita
- Verifica telefonica per account di alto valore

---

### Esperimenti Post-Invio

- Messaggi chiari sui prossimi step dopo il signup
- Accesso immediato al prodotto vs. prima conferma email
- Messaggio di benvenuto personalizzato basato sui dati di signup
- Login automatico dopo il signup vs. login richiesto

---

## Domande Specifiche per il Task

1. Qual è il tuo tasso attuale di completamento del signup?
2. Hai analytics a livello di campo sull'abbandono?
3. Quali dati sono assolutamente necessari prima che possano usare il prodotto?
4. Ci sono requisiti di compliance o verifica?
5. Cosa succede immediatamente dopo il signup?

---

## Skill Correlate

- **onboarding**: Per ottimizzare cosa succede dopo il signup
- **cro**: Per form non legati al signup (lead capture, contatto)
- **cro**: Per la landing page che porta al signup
- **ab-testing**: Per testare le modifiche al flusso di signup
