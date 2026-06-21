---
name: product-marketing
description: "Quando l'utente vuole creare o aggiornare il proprio documento di contesto di product marketing. Da usare anche quando l'utente menziona 'contesto del prodotto,' 'contesto di marketing,' 'impostare il contesto,' 'positioning,' 'qual è il mio pubblico target,' 'descrivi il mio prodotto,' 'ICP,' 'ideal customer profile,' o vuole evitare di ripetere informazioni fondamentali tra i vari task di marketing. Usa questa skill all'inizio di ogni nuovo progetto prima di usare altre skill di marketing — crea `.agents/product-marketing.md` che tutte le altre skill consultano per il contesto di prodotto, pubblico, e positioning."
metadata:
  version: 2.0.0
---

# Contesto di Product Marketing

Aiuti gli utenti a creare e mantenere un documento di contesto di product marketing. Questo cattura le informazioni fondamentali di positioning e messaggistica che le altre skill di marketing consultano, così gli utenti non devono ripetersi.

Il documento è salvato in `.agents/product-marketing.md`.

## Workflow

### Passo 1: Controlla il Contesto Esistente

Per prima cosa, controlla se `.agents/product-marketing.md` esiste già. Controlla anche `.claude/product-marketing.md` e il vecchio nome file `product-marketing-context.md` (in `.agents/` o `.claude/`) per setup più datati — se trovato in un posto diverso dalla posizione canonica `.agents/product-marketing.md`, offri di spostarlo lì.

**Se esiste:**
- Leggilo e riassumi cosa è stato catturato
- Chiedi quali sezioni vogliono aggiornare
- Raccogli informazioni solo per quelle sezioni

**Se non esiste, offri due opzioni:**

1. **Bozza automatica dal codebase** (consigliata): Studierai il repository — README, landing page, copy di marketing, package.json, ecc. — e redigerai una V1 del documento di contesto. L'utente poi rivede, corregge, e completa le lacune. È più rapido che iniziare da zero.

2. **Inizia da zero**: Percorri ogni sezione in modo conversazionale, raccogliendo informazioni una sezione alla volta.

La maggior parte degli utenti preferisce l'opzione 1. Dopo aver presentato la bozza, chiedi: "Cosa va corretto? Cosa manca?"

### Passo 2: Raccogli le Informazioni

**Se redigi automaticamente:**
1. Leggi il codebase: README, landing page, copy di marketing, pagine about, meta description, package.json, qualsiasi documentazione esistente
2. Redigi tutte le sezioni in base a ciò che trovi
3. Presenta la bozza e chiedi cosa va corretto o manca
4. Itera finché l'utente non è soddisfatto

**Se inizi da zero:**
Percorri ogni sezione di seguito in modo conversazionale, una alla volta. Non scaricare tutte le domande in una volta.

Per ogni sezione:
1. Spiega brevemente cosa stai catturando
2. Fai le domande rilevanti
3. Conferma l'accuratezza
4. Passa alla successiva

Spingi per ottenere il linguaggio verbatim del cliente — le frasi esatte sono più valoroso delle descrizioni levigate perché rispecchiano come i clienti pensano e parlano davvero, il che rende il copy più risonante.

---

## Sezioni da Catturare

### 1. Panoramica del Prodotto
- Descrizione in una riga
- Cosa fa (2-3 frasi)
- Categoria di prodotto (su quale "scaffale" ti posizioni — come i clienti ti cercano)
- Tipo di prodotto (SaaS, marketplace, e-commerce, servizio, ecc.)
- Modello di business e pricing

### 2. Pubblico Target
- Tipo di azienda target (settore, dimensione, fase)
- Decision-maker target (ruoli, dipartimenti)
- Caso d'uso primario (il problema principale che risolvi)
- Jobs to be done (2-3 cose per cui i clienti ti "assumono")
- Casi d'uso o scenari specifici

### 3. Persona (solo B2B)
Se più stakeholder sono coinvolti nell'acquisto, cattura per ciascuno:
- Utente, Champion, Decision Maker, Buyer Finanziario, Influencer Tecnico
- Cosa interessa a ciascuno, la loro sfida, e il valore che prometti loro

### 4. Problemi e Punti di Dolore
- Sfida principale che i clienti affrontano prima di trovarti
- Perché le soluzioni attuali non bastano
- Cosa costa loro (tempo, denaro, opportunità)
- Tensione emotiva (stress, paura, dubbio)

### 5. Panorama Competitivo
- **Concorrenti diretti**: Stessa soluzione, stesso problema (es. Calendly vs SavvyCal)
- **Concorrenti secondari**: Soluzione diversa, stesso problema (es. Calendly vs la pianificazione di Superhuman)
- **Concorrenti indiretti**: Approccio in conflitto (es. Calendly vs assistente personale)
- Come ciascuno non basta per i clienti

### 6. Differenziazione
- Differenziatori chiave (capacità che le alternative non hanno)
- Come lo risolvi in modo diverso
- Perché è meglio (benefici)
- Perché i clienti ti scelgono rispetto alle alternative

### 7. Obiezioni e Anti-Persona
- Le 3 obiezioni principali sentite in fase di vendita e come affrontarle
- Chi NON è un buon fit (anti-persona)

### 8. Dinamiche di Switching
Le Quattro Forze del JTBD:
- **Push**: Quali frustrazioni li spingono via dalla soluzione attuale
- **Pull**: Cosa li attira verso di te
- **Habit**: Cosa li tiene bloccati con l'approccio attuale
- **Anxiety**: Cosa li preoccupa nel cambiare

### 9. Linguaggio del Cliente
- Come i clienti descrivono il problema (verbatim)
- Come descrivono la tua soluzione (verbatim)
- Parole/frasi da usare
- Parole/frasi da evitare
- Glossario dei termini specifici del prodotto

### 10. Voce del Brand
- Tono (professionale, casual, giocoso, ecc.)
- Stile di comunicazione (diretto, conversazionale, tecnico)
- Personalità del brand (3-5 aggettivi)

### 11. Elementi di Prova
- Metriche o risultati chiave da citare
- Clienti/loghi rilevanti
- Estratti di testimonianze
- Temi di valore principali e prove a supporto

### 12. Obiettivi
- Obiettivo di business primario
- Azione di conversione chiave (cosa vuoi che le persone facciano)
- Metriche attuali (se note)

---

## Passo 3: Crea il Documento

Dopo aver raccolto le informazioni, crea `.agents/product-marketing.md` con questa struttura:

```markdown
# Contesto di Product Marketing

*Ultimo aggiornamento: [data]*

## Panoramica del Prodotto
**Descrizione in una riga:**
**Cosa fa:**
**Categoria di prodotto:**
**Tipo di prodotto:**
**Modello di business:**

## Pubblico Target
**Aziende target:**
**Decision-maker:**
**Caso d'uso primario:**
**Jobs to be done:**
-
**Casi d'uso:**
-

## Persona
| Persona | Cosa gli interessa | Sfida | Valore che promettiamo |
|---------|-------------|-----------|------------------|
| | | | |

## Problemi e Punti di Dolore
**Problema principale:**
**Perché le alternative non bastano:**
-
**Cosa costa loro:**
**Tensione emotiva:**

## Panorama Competitivo
**Diretto:** [Concorrente] — non basta perché...
**Secondario:** [Approccio] — non basta perché...
**Indiretto:** [Alternativa] — non basta perché...

## Differenziazione
**Differenziatori chiave:**
-
**Come lo facciamo in modo diverso:**
**Perché è meglio:**
**Perché i clienti ci scelgono:**

## Obiezioni
| Obiezione | Risposta |
|-----------|----------|
| | |

**Anti-persona:**

## Dinamiche di Switching
**Push:**
**Pull:**
**Habit:**
**Anxiety:**

## Linguaggio del Cliente
**Come descrivono il problema:**
- "[verbatim]"
**Come ci descrivono:**
- "[verbatim]"
**Parole da usare:**
**Parole da evitare:**
**Glossario:**
| Termine | Significato |
|------|---------|
| | |

## Voce del Brand
**Tono:**
**Stile:**
**Personalità:**

## Elementi di Prova
**Metriche:**
**Clienti:**
**Testimonianze:**
> "[citazione]" — [chi]
**Temi di valore:**
| Tema | Prova |
|-------|-------|
| | |

## Obiettivi
**Obiettivo di business:**
**Azione di conversione:**
**Metriche attuali:**
```

---

## Passo 4: Conferma e Salva

- Mostra il documento completato
- Chiedi se qualcosa necessita di aggiustamenti
- Salva in `.agents/product-marketing.md`
- Comunica: "Le altre skill di marketing useranno ora questo contesto automaticamente. Esegui `/product-marketing` in qualsiasi momento per aggiornarlo."

---

## Consigli

- **Sii specifico**: Chiedi "Qual è la frustrazione numero 1 che li porta da te?" non "Quale problema risolvono?"
- **Cattura le parole esatte**: Il linguaggio del cliente batte le descrizioni levigate
- **Chiedi esempi**: "Puoi darmi un esempio?" sblocca risposte migliori
- **Valida man mano che procedi**: Riassumi ogni sezione e conferma prima di passare alla successiva
- **Salta ciò che non si applica**: Non ogni prodotto ha bisogno di tutte le sezioni (es. Persona per il B2C)
