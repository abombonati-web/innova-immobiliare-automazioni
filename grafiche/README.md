# Grafiche Innova Immobiliare

## Chiusura estiva 2026 (8 – 23 agosto)

Due versioni della stessa comunicazione, stessa gabbia e stessa palette:

1. **Versione foto** (`ferie-agosto-2026-foto.html`) — quella da pubblicare:
   post e story costruiti sulle foto di Innova.
2. **Versione illustrata** (`ferie-agosto-2026.html`) — alternativa con la
   baia di Mondello disegnata in SVG, anche in formato quadrato.

### Versione foto

| File | Formato | Foto |
|---|---|---|
| `innova-ferie-agosto-2026-foto-post.png` | 2160 × 2700 (4:5) | luna piena sul mare |
| `innova-ferie-agosto-2026-foto-story.png` | 2160 × 3840 (9:16) | la costa vista dall'aereo |

Le foto originali stanno in `foto/`, già raddrizzate secondo l'EXIF e
ridimensionate. Sopra ciascuna: un riscaldamento ambra in `soft-light`, una
velatura charcoal che scurisce progressivamente verso il basso per la
leggibilità del testo, e gli stessi stilemi della landing.

L'inquadratura si regola nella mappa `PHOTOS` in fondo al file: `pos`
(`object-position`) e `tr` (zoom/spostamento fine).

### Versione illustrata

Sfondo illustrato della baia di **Mondello** (Monte Pellegrino a destra,
Monte Gallo a sinistra) al tramonto, realizzato interamente in SVG.

### Palette (comune alle due versioni)

| Colore | HEX | Uso |
|---|---|---|
| Ambra | `#E8982A` | accenti, date, riscaldamento delle foto, payoff |
| Ambra scuro | `#C97E15` | ombre degli ombrelloni |
| Charcoal | `#2B2A28` | velature e pannello testo |
| Crema | `#FBF6EE` | testi |

Font: **Poppins** (300–800), lo stesso della landing, incorporato in
`poppins-embed.css` come woff2 base64 così l'esportazione è identica ovunque
e non serve connessione.

### File illustrati

| File | Formato | Uso |
|---|---|---|
| `innova-ferie-agosto-2026-post.png` | 2160 × 2700 (4:5) | post Instagram / Facebook |
| `innova-ferie-agosto-2026-story.png` | 2160 × 3840 (9:16) | storie e reel cover |
| `innova-ferie-agosto-2026-quadrato.png` | 2160 × 2160 (1:1) | post quadrato, Google Business, firma email |

I PNG sono esportati a 2× (1080 px di lato base) per restare nitidi anche
su schermi retina e in stampa piccola.

### Modificare testi o date

Il testo sta in un unico blocco in fondo a ciascun HTML (`CONTENT` nella
versione foto, `POSTER` in quella illustrata). Le proporzioni dei formati si
regolano con le variabili CSS `--s` (scala tipografica), `--scene` (altezza
dell'illustrazione) e `--scrim-start` (dove inizia la velatura sulle foto).

### Rigenerare i PNG

```bash
npm i playwright        # una tantum
node grafiche/render.mjs
```

Senza Node basta aprire `ferie-agosto-2026.html` nel browser e fare uno
screenshot dei tre riquadri.
