# innova-immobiliare-automazioni

Automazioni Make, script CRM e workflow per Innova Immobiliare

## Routine: Report lead mattutino (ore 8:45)

Ogni mattina alle **8:45 (ora italiana)** il workflow [`report-lead-mattutino`](.github/workflows/report-lead-mattutino.yml):

1. Legge le nuove risposte dal foglio Google **"Modulo Innova Experiences (Risposte)"**.
2. Per ogni nuovo lead, Claude cerca sul web (immobiliare.it, idealista.it, casa.it, subito.it) **tutti gli immobili attualmente sul mercato allineati ai criteri del lead** (affitto/acquisto, zone, tipologia, superficie, budget) e genera un report.
3. Invia i report su **WhatsApp**.

I lead già analizzati sono tracciati in `data/leads_processati.json`: ogni mattina vengono analizzati solo i nuovi. Dal tab *Actions* si può lanciare il workflow manualmente, anche con l'opzione "rianalizza tutti i lead".

### Configurazione (da fare una sola volta)

Aggiungere questi **secrets** al repository (*Settings → Secrets and variables → Actions → New repository secret*):

| Secret | Descrizione |
|---|---|
| `ANTHROPIC_API_KEY` | Chiave API Anthropic (da [console.anthropic.com](https://console.anthropic.com)) per l'analisi dei lead e la ricerca immobili. |
| `WHATSAPP_PHONE` | Numero WhatsApp destinatario con prefisso, es. `+39333xxxxxxx`. |
| `CALLMEBOT_APIKEY` | Chiave CallMeBot (invio WhatsApp gratuito, vedi sotto). |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | JSON di un service account Google con accesso in lettura al foglio (vedi sotto). |

**CallMeBot (invio WhatsApp gratuito):**
1. Salva in rubrica il numero CallMeBot: **+34 621 331 709**.
2. Inviagli su WhatsApp il messaggio: `I allow callmebot to send me messages`.
3. Riceverai la tua API key: inseriscila nel secret `CALLMEBOT_APIKEY`.

In alternativa a CallMeBot si può usare **Twilio** (più affidabile, a pagamento) configurando `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` e `TWILIO_WHATSAPP_FROM` al posto di `CALLMEBOT_APIKEY`.

**Accesso al foglio Google (service account):**
1. Su [console.cloud.google.com](https://console.cloud.google.com) crea un progetto, abilita le API *Google Sheets* e *Google Drive*, poi crea un *service account* e scarica la chiave JSON.
2. Condividi il foglio "Modulo Innova Experiences (Risposte)" (come *Visualizzatore*) con l'email del service account (tipo `nome@progetto.iam.gserviceaccount.com`).
3. Incolla l'intero contenuto del file JSON nel secret `GOOGLE_SERVICE_ACCOUNT_JSON`.

In alternativa più rapida ma meno sicura: imposta il foglio su "Chiunque abbia il link può visualizzare" e crea il secret `GOOGLE_SHEET_CSV_URL` con `https://docs.google.com/spreadsheets/d/1qB9nTJmDseVhhxfTptxkeUAAfeLSA6hgLo0OltmZH9Q/export?format=csv`.

> **Nota:** GitHub esegue i workflow pianificati solo dal branch principale (`main`): la routine si attiva dopo il merge su `main`. L'orario può slittare di qualche minuto (code di GitHub Actions).
