# Innova Experience

La piattaforma degli eventi Innova Experience: le pagine pubbliche degli immobili e la gestione delle lead, con un archivio unico e condiviso.

## Cosa contiene

| File | A cosa serve |
|---|---|
| `index.html` | Pagina pubblica dell'evento (Villa Città Giardino) con il modulo di candidatura |
| `gestione.html` | Area riservata: contatti, attività da fare e attività svolte |
| `netlify/functions/api.mjs` | Lato server: risponde su `/api/…` e conserva l'archivio |
| `netlify/functions/rotte.mjs` | Le rotte della piattaforma |
| `netlify/functions/nucleo.mjs` | Le regole su contatti, attività, accessi ed e-mail |
| `test/` | Prove automatiche del lato server |

---

## Come funziona il giro di una lead

1. **Un visitatore compila il modulo** sulla pagina dell'evento. Oltre a nome, telefono ed email, dichiara **a cosa è interessato**, **come pensa di procedere all'acquisto** e può lasciare una nota.

2. **La candidatura entra da sola nella piattaforma.** Sul momento vengono creati il **contatto** e la sua **attività fissa** di richiamo, con la traccia della telefonata già dentro. Nessuno deve importare niente.

3. **Parte l'e-mail di riepilogo** a `info@innovaimmobiliare.it`: a cosa è interessata, come intende acquistare, fascia richiesta, cosa ha scritto, campagna di provenienza, entro quando richiamarla, la traccia per la chiamata, i link per **chiamarla** o **scriverle su WhatsApp**, e il link che apre la sua scheda nella gestione.

4. **Chi ha già la gestione aperta se la ritrova lì**, perché l'archivio è unico.

Se la stessa persona si candida una seconda volta non nasce un doppione: la scheda si aggiorna e viene messo in agenda un nuovo richiamo.

---

## La gestione

Si apre all'indirizzo della piattaforma seguito da `/gestione.html`, con la password condivisa.

### Creare un contatto

- **+ Nuovo contatto** — scheda completa: nome, recapiti, stato, fascia di visita, interesse, modalità d'acquisto, provenienza e note. Se il telefono o l'email risultano già in archivio compare un avviso con il nome del contatto esistente. L'attività fissa nasce insieme al contatto, con scadenza modificabile, e si può escludere.
- **Incolla lead** — si incolla un'e-mail, un messaggio o qualunque testo con i recapiti: la piattaforma riconosce nome, telefono, email, interesse, modalità d'acquisto, fascia, note e provenienza, e apre la scheda già compilata. Funziona sia con testo etichettato sia con testo libero.

### Da fare
Quante attività sono scadute, quante scadono oggi, quante sono in arrivo e quante lead non sono mai state contattate. Sotto, le attività aperte in ordine di scadenza, con i pulsanti per chiamare, aprire la scheda o segnare come fatta.

### Contatti
Ricerca per nome, telefono, email o interesse, filtro per stato, ordinamento. Ogni contatto ha uno stato lungo il percorso dell'evento:

`Nuovo` → `Contattato` → `Visita confermata` → `Ha visitato` → `Ha fatto offerta` → `Non interessato`

Lo stato passa da solo a *Contattato* quando si registra la prima attività.

### Attività
Tutte le attività di tutti i contatti: prima le cose da fare per scadenza, poi le svolte. Si crea un'attività su qualunque contatto — da fare o già svolta — e si modifica qualsiasi attività esistente, compreso il passaggio fra *da fare* e *svolta*.

### Scheda contatto
Dati modificabili, azioni rapide chiama / WhatsApp / e-mail, registrazione delle attività svolte con esito e note, programmazione delle prossime, storico completo.

### Impostazioni
Attività fissa (titolo, tipo, scadenza, traccia della chiamata), stato dell'archivio, sincronizzazione manuale, uscita, esportazione JSON e CSV.

---

## L'archivio

L'archivio è **unico e condiviso**: chiunque acceda, da qualunque dispositivo, vede le stesse schede e le stesse attività. Vive nei Netlify Blobs, insieme alla piattaforma.

Ogni gestione ne tiene anche una **copia locale**, per due motivi: si continua a lavorare quando la rete manca, e le modifiche fatte nel frattempo partono da sole appena il collegamento torna. L'indicatore in alto dice sempre a che punto si è:

| Indicatore | Significato |
|---|---|
| ● Collegata | Archivio allineato con la piattaforma |
| ◐ Salvataggio… | Modifiche non ancora inviate |
| ○ Solo locale | Rete assente: si lavora in locale, si invierà al ritorno |

Quando due persone toccano la stessa scheda, **vince la modifica più recente**; le schede toccate da una sola parte non vengono mai perse. Le cancellazioni lasciano un segnaposto, così spariscono anche sugli altri dispositivi.

---

## Messa in funzione

La piattaforma va servita da **Netlify**, perché è lì che girano le funzioni `/api/…` e l'archivio condiviso.

> Nel repository è rimasto anche il workflow `deploy-pages.yml`, che pubblica su GitHub Pages. Quella copia serve solo le pagine pubbliche: non avendo il lato server, la gestione non funziona e le candidature ripiegano sull'invio via e-mail. Se la piattaforma vive su Netlify, quel workflow si può disattivare.

### 1. Variabili d'ambiente

Su Netlify, in *Site configuration → Environment variables*:

| Variabile | A cosa serve |
|---|---|
| `INNOVA_PASSWORD` | La password con cui si entra nella gestione |
| `INNOVA_SEGRETO` | Una stringa lunga e casuale con cui vengono firmati gli accessi |
| `INNOVA_EMAIL` | La casella a cui arrivano i riepiloghi (se assente: `info@innovaimmobiliare.it`) |

Senza `INNOVA_PASSWORD` e `INNOVA_SEGRETO` la gestione non lascia entrare nessuno e lo dice apertamente.

### 2. Attivare l'invio delle e-mail

Al primo riepilogo, FormSubmit manda un'e-mail di conferma a `info@innovaimmobiliare.it`: bisogna cliccare **Activate**. È un'operazione da fare una volta sola. Le candidature entrano in archivio anche prima: l'e-mail è un di più, non la strada per cui passano.

### 3. Prova

Una candidatura di prova dalla pagina pubblica, poi si apre la gestione: il contatto e la sua attività di richiamo devono essere già lì.

---

## Prove automatiche

```bash
npm test
```

Coprono il lato server senza bisogno di Netlify: creazione di contatti e attività, riconoscimento dei doppioni, scadenze, accessi e token, sincronizzazione fra dispositivi, e i casi in cui qualcosa va storto (e-mail non partita, archivio irraggiungibile, corpo illeggibile).
