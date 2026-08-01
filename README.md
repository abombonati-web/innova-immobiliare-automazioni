# innova-immobiliare-automazioni

Automazioni Make, script CRM e workflow per Innova Immobiliare.

## Cosa contiene

| File | A cosa serve |
|---|---|
| `index.html` | La landing page **Innova Experience** (Villa Città Giardino) con il modulo di candidatura |
| `gestione.html` | La **Gestione Lead**: contatti, attività da fare e attività svolte |

Entrambe le pagine vengono pubblicate su GitHub Pages dal workflow `.github/workflows/deploy-pages.yml` a ogni push su `main`.

---

## Come funziona il giro di una lead

1. **Un visitatore compila il modulo** sulla landing page. Oltre a nome, telefono ed email, dichiara **a cosa è interessato**, **come pensa di procedere all'acquisto** e può lasciare una nota libera.

2. **Arriva l'e-mail di riepilogo** a `info@innovaimmobiliare.it`, con tutto ciò che serve per chiamare la persona sapendo già perché ha scritto:

   - a cosa è interessata e come intende acquistare;
   - la fascia di visita richiesta e cosa ha scritto nelle note;
   - da quale campagna proviene (parametri UTM);
   - entro quando va richiamata;
   - una **traccia per la chiamata**, costruita su quello che ha dichiarato;
   - i link per **chiamarla** o **scriverle su WhatsApp** con un tocco;
   - il link **"APRI IN GESTIONE LEAD"**.

3. **Un clic su quel link** apre `gestione.html` e crea automaticamente:
   - il **contatto**, con tutti i dati della candidatura;
   - l'**attività fissa** di richiamo, con scadenza e traccia della telefonata già dentro.

   Riaprendo lo stesso link il contatto non viene duplicato: si apre la scheda già esistente.

4. **Dalla scheda del contatto** si può chiamare, scrivere su WhatsApp o via email, **modificare e aggiornare tutti i dati**, **registrare le attività svolte** (con esito e note) e **programmare le prossime**.

---

## La Gestione Lead

Si apre all'indirizzo della landing page seguito da `/gestione.html`.

### Da fare
La prima schermata: quante attività sono scadute, quante scadono oggi, quante sono in arrivo e quante lead non sono mai state contattate. Sotto, l'elenco delle attività aperte in ordine di scadenza, con i pulsanti per chiamare, aprire la scheda o segnare l'attività come fatta.

### Contatti
L'elenco completo, con ricerca per nome, telefono, email o interesse, filtro per stato e ordinamento. Ogni contatto ha uno stato lungo il percorso dell'evento:

`Nuovo` → `Contattato` → `Visita confermata` → `Ha visitato` → `Ha fatto offerta` → `Non interessato`

Lo stato passa da solo a *Contattato* quando si registra la prima attività su quel contatto.

### Scheda contatto
- **Dati del contatto** — nome, telefono, email, stato, fascia di visita, interesse, modalità di acquisto e note: tutto modificabile e salvabile.
- **Registra un'attività svolta** — tipo (chiamata, WhatsApp, email, visita, nota), quando è avvenuta, esito e cosa è emerso.
- **Programma una prossima attività** — cosa va fatto ed entro quando: finisce nell'elenco *Da fare*.
- **Storico attività** — la cronologia completa del contatto, attività automatiche comprese.

### Impostazioni
- **Attività fissa** — titolo, tipo, scadenza in ore e traccia della chiamata. Le modifiche valgono per le lead successive.
- **PIN di accesso** — blocco leggero per i dispositivi condivisi.
- **Backup** — esportazione in JSON e CSV, importazione, cancellazione dell'archivio.

---

## Da sapere prima di usarla

**Dove stanno i dati.** Contatti e attività sono salvati nel browser di chi gestisce le lead, non su un server: la landing page è un sito statico su GitHub Pages e non ha un database. Da questo discendono tre conseguenze pratiche:

- l'archivio è **legato al browser e al dispositivo** su cui si lavora: aprendo la Gestione Lead da un altro computer o telefono si parte da un archivio vuoto;
- per lavorare su più dispositivi, o in più persone, si usa **Esporta backup** e poi **Importa backup** sull'altro dispositivo (l'importazione unisce e salta i contatti già presenti);
- svuotando i dati del browser si perde l'archivio, quindi **conviene esportare un backup con regolarità**.

**Il PIN non è una misura di sicurezza**: impedisce che qualcuno apra la gestione da un dispositivo condiviso, nulla di più. La riservatezza dei dati dipende dal fatto che restino su quel browser.

Se in futuro servirà un archivio condiviso in tempo reale tra più persone, occorrerà affiancare un server o un database: la struttura dei dati è già pronta per essere spostata.

---

## Prima messa in funzione

1. **Attivare l'invio delle e-mail.** Al primo invio di prova dal modulo, FormSubmit manda un'e-mail di conferma a `info@innovaimmobiliare.it`: bisogna cliccare **Activate** in quella e-mail. Da quel momento tutte le candidature arrivano in casella. È un'operazione da fare una volta sola.

2. **Fare una candidatura di prova** e verificare che l'e-mail di riepilogo arrivi e che il link *Apri in Gestione Lead* crei contatto e attività.

3. **Impostare un PIN** dalla sezione Impostazioni, se la gestione viene usata da un dispositivo condiviso.

4. **Adattare l'attività fissa**, se la traccia della chiamata va cambiata.

### Se la Gestione Lead viene pubblicata a un altro indirizzo

Il link dentro l'e-mail punta a `gestione.html` accanto alla landing page. Se la console viene ospitata altrove, va scritto l'indirizzo completo in `index.html`:

```js
const GESTIONE_URL = new URL("gestione.html", location.href).href;
```

Nello stesso punto si trova anche `ORE_RICHIAMO`, che stabilisce entro quante ore la lead va richiamata secondo l'e-mail di riepilogo (va tenuto allineato alla scadenza dell'attività fissa impostata nella Gestione Lead).
