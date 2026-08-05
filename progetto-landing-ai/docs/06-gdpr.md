# Conformità — L'articolo 22 e il semaforo

## Il problema, detto semplice

Il semaforo finanziario decide, senza che intervenga una persona, se un cliente può
prenotare una visita. È una decisione automatizzata che produce un effetto su di lui.
L'articolo 22 del GDPR dice che una decisione del genere non può essere l'ultima parola:
l'interessato ha diritto a ottenere l'intervento umano, a esprimere la propria opinione
e a contestare la decisione.

Tradotto in pratica: **il sistema può filtrare, non può respingere.**

## Come è risolto

### 1. Nessun esito è definitivo

Ogni valutazione, qualunque sia l'esito, esce dal motore con un blocco `revisione_umana`
sempre presente e sempre attivo:

```js
revisione_umana: {
  disponibile: true,
  canali: ["telefono", "whatsapp", "email", "richiamata_programmata"],
  testo: "Non ti ritrovi in questo esito? Parla con una persona del team…"
}
```

Non è un dettaglio di configurazione che si può disattivare: è scritto nel motore, e un
test automatico verifica che ci sia su tutti e tre gli esiti. Se qualcuno lo togliesse,
la suite fallirebbe.

In pagina questo diventa un pulsante **"Parla con una persona"** accanto a ogni esito,
verde compreso.

### 2. Il rosso non è un rifiuto

L'esito peggiore che il sistema può produrre non chiude la porta: propone immobili
alternativi, offre la consulenza finanziaria e passa il contatto a un agente con un SLA
di 24 ore. Il messaggio al cliente non dice "non puoi", dice che la situazione merita un
approfondimento con una persona.

Nella configurazione è scritto esplicitamente: *"Contatto sempre umano. Mai una chiusura automatica."*

### 3. Solo una persona sblocca un giallo

Un esito giallo può diventare verde in un solo modo: `applicaEsitoConsulente()`, che
richiede l'identificativo dell'operatore e registra data e note. Non esiste un percorso
automatico che trasformi un giallo in un verde. La decisione che conta resta di una persona.

### 4. La logica è leggibile

L'articolo 22 chiede anche di poter spiegare la logica applicata. `config/regole-semaforo.json`
è scritto per essere letto da una persona non tecnica: ogni regola ha una descrizione in
italiano e una motivazione che finisce nella scheda del contatto. Alla domanda "perché il
sistema mi ha messo in verifica?" si risponde con una frase, non con un'analisi del codice.

## Le altre cose da sistemare prima di andare in produzione

### Informativa privacy

Va aggiornata dicendo, senza giri di parole:

- che le risposte del modulo vengono usate per una valutazione automatica di prequalifica;
- quali dati la alimentano (modalità di pagamento, budget, reddito per gli affitti);
- che l'esito può ritardare la prenotazione in attesa di una verifica;
- che esiste sempre il diritto di chiedere l'intervento di una persona, e come esercitarlo;
- per quanto tempo i dati vengono conservati.

### Consensi separati

- **Ricontatto** (obbligatorio): serve per rispondere alla richiesta.
- **Marketing** (facoltativo): è quello che alimenta le sequenze del club e le anteprime.

Il secondo non può essere spuntato di default né essere condizione per accedere alla scheda.
Nel prototipo sono già due caselle distinte e solo la prima è obbligatoria.

### Dati minimi, e non ovunque

Reddito e budget servono al semaforo e al consulente finanziario. Non vanno esposti in
pagina, non vanno inclusi negli eventi spediti agli strumenti di analytics pubblicitari,
non vanno messi nell'oggetto delle email. Nel prototipo il tracciamento invia l'esito del
semaforo, non i numeri che l'hanno prodotto.

### Tracciamento solo dopo il consenso

Il monitoraggio comportamentale identificato parte con `attivaConsenso()`, dopo la spunta.
Prima si contano solo eventi anonimi di pagina, senza identificativi persistenti.

### Conservazione e cancellazione

Va fissato un termine per i contatti che non concludono — la proposta è 24 mesi — e una
procedura per la cancellazione su richiesta che copra anche le code di invio e il cruscotto,
non solo il gestionale.

### Registro dei trattamenti

Il semaforo è profilazione: va iscritto nel registro. La descrizione della logica può essere
il file delle regole stesso, che è già in italiano leggibile.

## Una nota che non è giuridica

Tutto questo, oltre a essere dovuto, conviene. Un cliente messo in giallo che riceve
"ti richiamiamo entro poche ore per una verifica gratuita" resta un cliente. Un cliente
che riceve un no automatico da una pagina web non torna, e lo racconta in giro.
Il semaforo serve a proteggere il tempo degli agenti, non a selezionare le persone.
