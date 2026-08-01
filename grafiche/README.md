# Grafiche Innova Immobiliare

## Chiusura estiva 2026 (8 – 23 agosto)

Grafica di avviso ferie con sfondo illustrato della baia di **Mondello**
(Monte Pellegrino a destra, Monte Gallo a sinistra) al tramonto, realizzata
interamente in SVG con la palette del brand usata sul sito:

| Colore | HEX | Uso |
|---|---|---|
| Ambra | `#E8982A` | accenti, date, ombrelloni, payoff |
| Ambra scuro | `#C97E15` | ombre degli ombrelloni |
| Charcoal | `#2B2A28` | pannello testo, silhouette |
| Crema | `#FBF6EE` | testi e sabbia |

Font: **Poppins** (300–800), lo stesso della landing, incorporato in
`poppins-embed.css` come woff2 base64 così l'esportazione è identica ovunque
e non serve connessione.

### File

| File | Formato | Uso |
|---|---|---|
| `innova-ferie-agosto-2026-post.png` | 2160 × 2700 (4:5) | post Instagram / Facebook |
| `innova-ferie-agosto-2026-story.png` | 2160 × 3840 (9:16) | storie e reel cover |
| `innova-ferie-agosto-2026-quadrato.png` | 2160 × 2160 (1:1) | post quadrato, Google Business, firma email |
| `ferie-agosto-2026.html` | sorgente | da cui si rigenerano i PNG |

I PNG sono esportati a 2× (1080 px di lato base) per restare nitidi anche
su schermi retina e in stampa piccola.

### Modificare testi o date

Tutto il testo sta nella costante `POSTER` in fondo a `ferie-agosto-2026.html`.
Le proporzioni dei tre formati si regolano con le variabili CSS
`--s` (scala tipografica) e `--scene` (altezza dell'illustrazione).

### Rigenerare i PNG

```bash
npm i playwright        # una tantum
node grafiche/render.mjs
```

Senza Node basta aprire `ferie-agosto-2026.html` nel browser e fare uno
screenshot dei tre riquadri.
