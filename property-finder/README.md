# Agente Property Finder — specifiche per innovaexperience.it

> Stato: **specifiche + modello del report**. Il codice della piattaforma (SvelteKit + Supabase) non è in questo repository: queste specifiche servono per integrarlo lì.

## Cosa fa

1. Nella lista clienti (`/clienti`) e nella scheda cliente compare il pulsante **«Report Property»**, **solo** se il cliente ha compilato un questionario di acquisto o affitto.
2. Il report si prepara **solo al click**: non c'è nessuna generazione automatica.
3. L'agente legge il questionario e prepara il report:
   - **Sezione 1 – Immobili Innova:** abbinamento con la stessa logica di «immobili per cliente» già presente (budget come tetto, zona, tipologia, superficie), solo immobili con stato `disponibile`. Include foto, dati completi e **un solo link: la scheda su innovaexperience.it**.
   - **Sezione 2 – Mercato:** ricerca sul web pubblico (portali, siti di agenzie, annunci di privati) con gli strumenti web di Claude. Per ogni immobile compaiono i dati fattuali e una descrizione **riscritta** da Innova. **Nessun link, nessun nome di agenzia, nessun numero di terzi**, e il civico viene tolto.
   - **Sezione 3 – Lettura del mercato:** prezzi reali delle compravendite (Agenzia delle Entrate, atti sul Drive), **mai OMI**. Rata del mutuo e costi d'acquisto si calcolano con i calcolatori della piattaforma. Se un dato manca, il report lo dice.
   - **Sezione 4 – Incarico di ricerca:** proposta di farsi seguire da Innova (testo in `incarico-ricerca-BOZZA.md`, da validare con il legale).
4. Il report finito va nella coda **«Da approvare»**. Dopo l'approvazione parte **sia su WhatsApp sia via email**: link alla pagina del report e PDF allegato all'email.

## Limiti da conoscere

- **Gruppi Facebook e social chiusi:** non sono leggibili in automatico, perché richiedono un account e Meta lo vieta. Nella schermata del report c'è un campo **«Segnalazioni manuali»** in cui il team incolla annunci trovati a mano; l'agente li normalizza come gli altri.
- **Portali:** la ricerca web trova gli annunci indicizzati, non l'intero database dei portali. Niente scraping massivo, che violerebbe le condizioni d'uso di Immobiliare.it e Idealista, con cui Innova ha contratti.
- **Foto di terzi:** interruttore `includi_foto_terzi`, **spento di default**. Va acceso solo dopo il parere del legale, per via del diritto d'autore sulle foto.
- **Dati di terzi:** sono «come dichiarati nell'annuncio alla data del report». Vanno sempre verificati prima di qualsiasi proposta.

## Flusso tecnico

```
[Click «Report Property»]
   → POST /api/property-finder/{clienteId}
   → crea riga property_reports (stato: in_preparazione) e risponde subito
   → job in background:
       1. carica questionario + scheda cliente
       2. match immobili Innova disponibili (riuso funzione esistente)
       3. Claude: ricerca mercato (web_search + web_fetch) → JSON validato
       4. post-processing: rimuove URL, telefoni ed email non Innova; deduplica; scarta fuori budget/zona
       5. render HTML (modello report-esempio.html) + PDF (Playwright)
       6. stato: da_approvare → entra nella coda «Da approvare»
[Approvazione] → invio WhatsApp + email → stato: inviato → nota nello storico cliente
```

### Tabella Supabase `property_reports`

| campo | tipo | note |
|---|---|---|
| id | uuid | |
| cliente_id | fk | |
| questionario_id | fk | questionario usato |
| stato | text | `in_preparazione`, `da_approvare`, `inviato`, `errore` |
| immobili_innova | jsonb | slug + snapshot dei dati |
| immobili_mercato | jsonb | schede normalizzate (senza link e contatti) |
| fonti_interne | jsonb | URL di origine, **solo per lo staff**, mai nel report |
| segnalazioni_manuali | text | incollate dal team |
| includi_foto_terzi | bool | default `false` |
| html_url / pdf_url | text | storage Supabase |
| creato_da / approvato_da | fk utente | |
| created_at / sent_at | timestamptz | |

Le URL di origine degli annunci di terzi si salvano in `fonti_interne`, così il consulente sa dove trovare l'immobile quando il cliente chiama. Non escono mai dal sistema.

### Regola anti-contatti (step 4, obbligatoria)

Prima del render, su ogni campo testo delle schede di mercato:
- rimuovere ogni URL (`https?://…`, `www.…`);
- rimuovere numeri di telefono ed email **diversi** da `3394185631`, `0917934524` e `info@innovaimmobiliare.it`;
- rimuovere nomi di agenzie (lista da mantenere) e i civici dagli indirizzi;
- se dopo la pulizia la scheda non ha prezzo **o** superficie, scartarla.

### Chiamata a Claude (TypeScript, `@anthropic-ai/sdk`) — schema di riferimento

```ts
import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic(); // ANTHROPIC_API_KEY lato server

const params = {
  model: "claude-opus-5-5",
  max_tokens: 32000,
  betas: ["server-side-fallback-2026-07-01"],
  fallbacks: "default",               // se il modello rifiuta, riprova in automatico su un modello di riserva
  output_config: { effort: "high" },
  system: SYSTEM_PROPERTY_FINDER,      // vedi sotto
  tools: [
    { type: "web_search_20260209", name: "web_search", max_uses: 25,
      user_location: { type: "approximate", city: "Palermo", country: "IT" } },
    { type: "web_fetch_20260209", name: "web_fetch", max_uses: 30 },
  ],
  messages: [{ role: "user", content: JSON.stringify({ questionario, immobili_innova_gia_inclusi, segnalazioni_manuali }) }],
};
const finale = await client.beta.messages.toolRunner(params).runUntilDone();
// controllare finale.stop_reason (refusal / max_tokens) prima di leggere il testo,
// poi JSON.parse + validazione con zod dello schema SchedaMercato[]
```

### Prompt di sistema (bozza)

```
Sei l'agente Property Finder di Innova Immobiliare (Palermo).
Ricevi il questionario di un cliente. Cerca sul web pubblico gli immobili in vendita (o in affitto) oggi
coerenti con: tipologia, zone, budget (tetto massimo, tolleranza +5%), superficie e tempistiche.
Fonti: portali immobiliari, siti di agenzie, annunci di privati. Escludi gli immobili già in elenco Innova.
Per ogni immobile restituisci SOLO dati letti nell'annuncio: tipologia, zona/via senza civico, mq, locali,
bagni, piano, ascensore, classe energetica, stato, spese condominiali, prezzo, caratteristiche principali.
Mai inventare dati mancanti: lascia il campo vuoto.
Scrivi una descrizione nuova di 2-3 frasi (non copiare il testo dell'annuncio), un "perché è in linea"
e un "da verificare" (conformità, APE, spese ecc.).
Metti l'URL di origine solo nel campo fonte_interna. Nessun nome di agenzia, telefono o email nei testi.
Elimina i duplicati (stesso immobile su più portali). Massimo 15 immobili, ordinati per aderenza.
Rispondi solo con un array JSON secondo lo schema SchedaMercato.
```

## File in questa cartella

- `report-esempio.html` — modello grafico del report (colori e Poppins Innova). La sezione 1 contiene 3 immobili **reali** del catalogo; le sezioni 2 e 3 sono segnaposto. Il profilo cliente è di prova.
- `incarico-ricerca-BOZZA.md` — bozza dell'incarico di ricerca, **da validare con il legale**.
