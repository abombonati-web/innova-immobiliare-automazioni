# Grafiche Innova Immobiliare

## Chiusura estiva 2026 (8 – 23 agosto)

Avviso di chiusura per ferie con il logo Innova, foto reali e il numero da
chiamare per parlare con Sara, l'assistente digitale.

### Da pubblicare

| File | Formato | Immagine |
|---|---|---|
| `innova-ferie-agosto-2026-post.png` | 1080 × 1350 (4:5) | baia di Mondello |
| `innova-ferie-agosto-2026-story.png` | 1080 × 1920 (9:16) | baia di Mondello |

### Alternative con le foto di Innova (doppia risoluzione)

| File | Formato | Immagine |
|---|---|---|
| `innova-ferie-agosto-2026-luna-post.png` | 2160 × 2700 | luna piena sul mare |
| `innova-ferie-agosto-2026-volo-story.png` | 2160 × 3840 | la costa vista dall'aereo |
| `innova-ferie-agosto-2026-illustrata-post.png` | 2160 × 2700 | Mondello illustrata in SVG |
| `innova-ferie-agosto-2026-illustrata-story.png` | 2160 × 3840 | idem |
| `innova-ferie-agosto-2026-illustrata-quadrato.png` | 2160 × 2160 | idem, 1:1 |

> **Risoluzione.** La foto della baia di Mondello è arrivata a 275 × 183 px:
> è già portata a 1080 px di larghezza (il formato nativo di Instagram) ma
> oltre non si può andare senza inventare dettaglio, perciò quei due file
> sono esportati a 1×. Con un originale più grande basta sostituire
> `foto/mondello-baia.jpg` e rilanciare l'export a 2×.

### Sorgenti

| File | Cosa contiene |
|---|---|
| `ferie-agosto-2026-foto.html` | le quattro grafiche fotografiche |
| `ferie-agosto-2026.html` | la versione illustrata in SVG |
| `foto/` | foto e logo |
| `poppins-embed.css` | Poppins 300–800 in base64 |
| `render.mjs` | export dei PNG con Playwright |

Il logo (`foto/logo-innova.png`) è quello ufficiale, solo scontornato dal
fondo bianco: i colori non vengono mai alterati. Per questo il pannello di
post e story è crema come il fondo del sito, e sulle due grafiche a foto
piena il marchio sta su una targhetta crema.

### Palette e font

| Colore | HEX | Uso |
|---|---|---|
| Ambra | `#E8982A` | pulsante telefono, accenti sui fondi scuri |
| Ambra scuro | `#C97E15` | date e accenti sul pannello crema |
| Ambra logo | `#F4AF37` | tetto e lettere "nn" del marchio |
| Grigio caldo | `#86776F` | lettere "i…ova" del marchio |
| Charcoal | `#2B2A28` | titoli e velature |
| Crema | `#FBF6EE` | pannello di post e story, targhetta del logo |

Font: **Poppins** (300–800), lo stesso della landing, incorporato in
`poppins-embed.css` come woff2 base64 così l'esportazione è identica ovunque
e non serve connessione.

### Modificare testi, date o inquadratura

Testo e numero di telefono stanno nelle costanti `LOCKUP` e `BLOCK` in fondo
a `ferie-agosto-2026-foto.html`. Nella mappa `POSTERS` si regolano per ogni
formato: `layout` (`band` = fascia foto in alto, `full` = foto a tutto
campo), `band` (altezza della fascia), `s` (scala tipografica), `pos` e `tr`
(inquadratura e zoom sulla foto).

### Rigenerare i PNG

```bash
npm i playwright        # una tantum
node grafiche/render.mjs
```

Senza Node basta aprire il file HTML nel browser e fare uno screenshot dei
riquadri.
