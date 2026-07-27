# Innova Property Kit — reel + landing page da un brief immobile

Automatizza il workflow costruito a mano per **Via F. Petrarca 36 (Palermo)**: da una
cartella Drive e da quattro dati di prezzo/evento produce, in un colpo solo, tre
deliverable pronti alla pubblicazione.

| Deliverable | File | Cos'e |
|---|---|---|
| Reel / Story | `Innova_<Immobile>_VoceJazz.mp4` | verticale 1080×1920, 30 fps, ~25-30s, voce narrante italiana + jazz sintetizzato |
| Landing page | `landing-<immobile>.html` | file singolo autonomo, foto e audio in base64, player vocale brandizzato |
| Versione stampabile | `landing-<immobile>.pdf` | stesso contenuto in A4, senza mappa interattiva ne audio |

Tutto e generato **in locale con software open source**: nessuna API TTS a pagamento,
nessuna libreria musicale con royalty, nessun servizio cloud.

---

## 1. Requisiti

```bash
# binari di sistema
apt-get install -y ffmpeg wkhtmltopdf

# librerie Python
pip install -r requirements.txt
```

Al primo avvio il kit scarica e mette in cache (`~/.cache/innova-property-kit`, oppure
`$INNOVA_KIT_CACHE`):

* i TTF **Poppins** (300–800) da `raw.githubusercontent.com/google/fonts`;
* la voce **Piper `it_IT-paola-medium`** (~67 MB) dalle release GitHub di sherpa-onnx.

Entrambe le sorgenti sono su domini raggiungibili anche dai sandbox con whitelist
ristretta. **HuggingFace non e raggiungibile**: per aggiungere una voce nuova serve un
mirror su GitHub Releases.

Variabili d'ambiente utili in ambienti offline:

| Variabile | A cosa serve |
|---|---|
| `INNOVA_KIT_CACHE` | cartella di cache degli asset |
| `INNOVA_KIT_FONT_DIR` | cartella con i TTF Poppins gia presenti |
| `INNOVA_KIT_VOICE_DIR` | cartella del modello Piper gia estratto |
| `INNOVA_GDRIVE_TOKEN` | access token OAuth per leggere le foto da Drive |
| `GOOGLE_APPLICATION_CREDENTIALS` | in alternativa, un service account con accesso alla cartella |

---

## 2. Uso rapido

```bash
python innova_property_kit.py \
  --brief briefs/via-petrarca-36.json \
  --drive-folder-id 1E7CcGEd8MUOeovb2F3SNf1D0PE-OMexI \
  --old-price 168000 --new-price 155000 \
  --event-date 2026-08-05 --event-slots "12:00,15:30" \
  --phone "+39 339 418 5631" \
  --video-tone euforico --video-music jazz \
  --output-dir ./output
```

Con le foto gia su disco (per esempio scaricate dall'assistente tramite il connettore
MCP Google Drive) basta:

```bash
python innova_property_kit.py --brief briefs/via-petrarca-36.json --photos-dir ./foto
```

Opzioni principali:

| Opzione | Default | Note |
|---|---|---|
| `--brief` | — | JSON con i dati dell'immobile (vedi `briefs/`) |
| `--property` / `--city` | — | alternativa al brief per una prova rapida; `--property "Via X 1, Palermo"` va bene |
| `--photos-dir` / `--photos-manifest` / `--drive-folder-id` / `--drive-search` | — | sorgente foto (la prima indicata vince) |
| `--photos` | `6` | quante foto usare |
| `--video-tone` | `euforico` | `euforico` \| `professionale` |
| `--video-music` | `jazz` | `jazz` \| `nessuna` |
| `--max-duration` | `30` | limite concordato col cliente |
| `--landing-tone` | `professionale` | registro della voce nella landing |
| `--skip-video` / `--skip-landing` / `--skip-pdf` | — | rigenerare un solo deliverable |
| `--work-dir` / `--keep-work-dir` | temporanea | per ispezionare slide, clip e WAV intermedi |

---

## 3. Il brief immobile

Un JSON per immobile, in `briefs/`. **Nessun campo viene dedotto**: prezzo, metratura,
vani e date evento arrivano dalla scheda ufficiale (`.docx` su Drive) o dalla CLI. Se un
dato obbligatorio manca, il tool si ferma e lo elenca invece di inventarlo; i campi
facoltativi mancanti fanno semplicemente sparire la sezione dalla landing.

```jsonc
{
  "property": {
    "name": "Via F. Petrarca 36",
    "address": "Via F. Petrarca 36",
    "city": "Palermo",
    "map_query": "Via Francesco Petrarca 36, Palermo",
    "surface_sqm": 90,                 // serve per il €/mq: senza, non viene stampato
    "eyebrow": "Nuovo prezzo · Palermo centro",
    "headline": "90 mq ... <em>Via Libertà</em>.",   // HTML minimo ammesso
    "description": ["paragrafo 1", "paragrafo 2"]
  },
  "price":  { "old": 168000, "new": 155000 },
  "facts":  [{ "label": "Superficie", "value": "90 mq", "icon": "▦",
               "spoken": "novanta metri quadri" }],   // `spoken` = come lo legge il TTS
  "details":[{ "label": "Riscaldamento", "value": "Pompa di calore" }],
  "highlights": [{ "icon": "↓", "title": "...", "text": "..." }],
  "targets":    [{ "title": "Investitori", "text": "..." }],
  "zone":   { "intro": "...", "advantages": ["..."] },
  "photo_captions": ["4 vani ben distribuiti", "..."],
  "event":  { "label": "Innova Experience", "date": "2026-08-05",
              "slots": ["12:00", "15:30"], "note": "Visite su prenotazione." },
  "contact":{ "phone": "+39 339 418 5631" },
  "narration": { "video": ["..."], "landing": ["..."] }  // opzionale: testi scritti a mano
}
```

Campi calcolati (mai scritti a mano): risparmio (`old − new`) e prezzo al metro quadro
(`new / surface_sqm`).

### Testi parlati

Senza `narration`, il kit compone i copioni dai dati del brief:

* **video** — quattro segmenti (`intro`, `price`, `event`, `cta`), frasi corte, tono da
  hook social; sta dentro i 30 secondi;
* **landing** — paragrafi piu distesi, tono istituzionale: chi legge la pagina e gia
  attento, la voce fa da riepilogo, non da spot.

Per un testo su misura basta riempire `narration.video` / `narration.landing`: il
generatore viene bypassato.

---

## 4. Struttura Drive attesa

```
/<Nome Via>/
  ├── <scheda immobile>.docx      → dati tecnici e prezzo (fonte di verita)
  ├── documenti <indirizzo>.pdf
  ├── planimetria con logo.png
  ├── Video <indirizzo>.mp4
  └── FOTO/
        ├── CON LOGO/
        ├── SENZA LOGO/            ← usata SEMPRE per i materiali pubblici
        └── __MACOSX/              ← ignorata
```

`--drive-folder-id` scende automaticamente fino a `SENZA LOGO`, ignora `CON LOGO` e
`__MACOSX`, ordina i file in modo naturale (`INNOVA-2` prima di `INNOVA-10`) e scarica le
prime `--photos` immagini.

---

## 5. Come e fatto

```
tools/innova_property_kit/
  brand.py     palette, font, payoff, dati agenzia, preset di voce (vincolanti)
  model.py     PropertyBrief + validazione "zero dati inventati"
  fmt.py       euro, date italiane, numeri a parole per il TTS, slug
  assets.py    download/cache di Poppins e della voce Piper
  photos.py    fetch_property_photos: Drive REST / cartella locale / manifest
  slides.py    slide 1080×1920 e didascalie (Pillow)
  script.py    copioni video e landing
  voice.py     Piper via sherpa-onnx, con durate esatte per la sincronizzazione
  audio.py     ding/bell/thump, letto jazz, ducking, mixdown, export MP3
  reel.py      scaletta: durate scena ricavate dal parlato + rientro nel budget
  video.py     Ken Burns, catena xfade con offset calcolati, mux finale
  landing.py   HTML autonomo (foto e audio in base64) + player brandizzato
  pdf.py       adattamenti di stampa + wkhtmltopdf
  cli.py       interfaccia a riga di comando
```

### Il punto delicato: gli offset di `xfade`

Ogni transizione sovrappone `T` secondi, quindi la clip *i* diventa visibile a
`somma(durate precedenti) − i·T`, **non** alla somma semplice. `video.scene_offsets()`
calcola questi valori una volta sola: li usa il filtro `xfade` e li usa il montaggio
audio per posizionare i segmenti vocali. Ad ogni build la timeline viene stampata:

```
timeline (10 scene, transizione 0.30s):
    0.00s  +1.55s  intro          Via F. Petrarca 36, Palermo
    ...
    9.00s  +7.59s  price          nuovo prezzo
   16.29s  +6.25s  event          evento
   22.24s  +6.36s  cta            CTA
  durata totale: 28.60s
```

Le durate delle scene non sono fisse: si ricavano dalla voce gia sintetizzata piu un
margine. Se il totale supera `--max-duration`, il kit accorcia **solo le foto** (fino a
1,25s l'una) e avvisa se non basta — il parlato non viene mai tagliato di nascosto.

### Voce

| Uso | speed | noise_scale | noise_scale_w |
|---|---|---|---|
| `euforico` (video) | 0.90 | 0.80 | 0.95 |
| `professionale` (landing) | 1.00 | 0.55 | 0.70 |

### Musica

Jazz in sintesi additiva a ~92 BPM: walking bass, accordi rhodes in levare con feel
swing, spazzole sugli ottavi. Sotto la voce il letto scende del 55% (maschera di attivita
vocale smussata con `uniform_filter1d`).

### PDF

`wkhtmltopdf` monta un WebKit datato e non ha rete, quindi prima della conversione la
pagina viene adattata: iframe della mappa → link testuale, `.reveal` forzate visibili,
Poppins incorporato come `@font-face` base64, JS rimosso, player audio sostituito da una
nota, e le griglie CSS ricostruite con `inline-block` (CSS Grid non e supportato).

---

## 6. Test

```bash
python -m pytest tests -q
```

Gli 83 test non richiedono rete, ffmpeg o wkhtmltopdf: coprono la matematica degli
offset, la formattazione italiana, la validazione del brief, la generazione dei copioni,
l'HTML prodotto e gli adattamenti di stampa.

---

## 7. Limiti noti

* La voce Piper e sintetica e si riconosce: ottima per contenuti social rapidi, non
  sostituisce uno speaker reale su materiali istituzionali di alto profilo.
* Il jazz e sintesi additiva, non campioni di strumenti veri: rende l'atmosfera, non la
  qualita di una libreria professionale.
* La whitelist di rete del sandbox e ristretta: nuovi modelli/voci vanno cercati su
  mirror raggiungibili (`github.com`, `raw.githubusercontent.com`, `pypi.org`).
* Il render del video e la parte lenta (~100s per un reel da 6 foto su CPU).
