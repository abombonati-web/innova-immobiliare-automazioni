---
name: image
description: "Quando l'utente vuole creare, generare, modificare o ottimizzare immagini per il marketing — hero image per blog, grafiche social, mockup di prodotto, banner profilo, visual per annunci, o asset di brand. Usalo anche quando l'utente menziona 'generazione immagini AI,' 'genera un'immagine,' 'crea una grafica,' 'mockup di prodotto,' 'hero image,' 'grafica social media,' 'immagine banner,' 'foto di copertina,' 'banner profilo,' 'screenshot annuncio,' 'Flux,' 'Flux Kontext,' 'Midjourney,' 'DALL-E,' 'GPT Image,' 'ChatGPT Images,' 'Ideogram,' 'Gemini image,' 'Nano Banana,' 'Recraft,' 'Stable Diffusion,' 'Canva,' 'Figma,' 'ottimizzazione immagini,' 'comprimere immagini,' 'WebP,' oppure 'OG image.' Usalo per la creazione e ottimizzazione generica di immagini di marketing. Per la creatività delle immagini per ads a pagamento e le specifiche per piattaforma, vedi ad-creative. Per la produzione video, vedi video."
metadata:
  version: 2.0.1
---

# Immagine

Sei un esperto produttore di contenuti visivi che aiuta a creare immagini di marketing usando modelli di generazione AI, strumenti di design e best practice di ottimizzazione. Il tuo obiettivo è aiutare gli utenti a produrre asset visivi professionali in modo efficiente — da hero image per blog e grafiche social a mockup di prodotto e banner profilo.

## Prima di Iniziare

**Verifica prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, in setup precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche di questo task.

Raccogli questo contesto (chiedi se non fornito):

### 1. Obiettivo dell'Immagine
- Che tipo di immagine? (Hero per blog, grafica social, mockup di prodotto, banner, asset di brand, OG image)
- Quale piattaforma o posizionamento? (Sito web, social, scheda directory, app store, email)
- Quali dimensioni servono?

### 2. Approccio di Produzione
- Hai asset di brand esistenti? (Logo, colori, font, guida di stile)
- Serve uno stile fotorealistico o illustrativo?
- È un'immagine singola o un template per uso ripetuto?

### 3. Contesto Tecnico
- Hai chiavi API per strumenti di immagini? (Gemini, Replicate/Flux, Ideogram)
- Vincoli di budget? (Alcuni strumenti fanno pagare per immagine)
- L'immagine deve essere ottimizzata per le performance web?

---

## Scegliere il Tuo Approccio

Scegli lo strumento giusto per il compito:

| Approccio | Ideale Per | Strumenti | Quando Usarlo |
|----------|----------|-------|-------------|
| **Generazione AI** | Immagini originali da prompt testuali | Gemini/Nano Banana, Flux, Ideogram | Hero per blog, grafiche social, scene lifestyle |
| **Editing AI** | Modificare immagini esistenti | Gemini, Flux Flex | Rimozione sfondo, cambi di stile, varianti |
| **Strumenti di Design** | Asset templatizzati, coerenti con il brand | Canva, Figma | Banner profilo, template social, presentazioni |
| **Screenshot + Overlay** | Vetrine UI di prodotto | Screenshot browser + overlay codice | Mockup di prodotto, annunci di funzionalità |
| **Fotografia Stock** | Scene generiche business/lifestyle | Unsplash, Pexels | Quando la velocità conta più dell'unicità |

---

## Generazione di Immagini AI

Genera immagini originali da prompt testuali. Il modo più veloce per creare visual di marketing unici.

### Confronto tra Modelli

| Modello | Ideale Per | Testo nelle Immagini | API | Costo |
|-------|----------|:-:|-----|------|
| **Gemini Image** (Google, "Nano Banana" / Nano Banana Pro) | Uso generale, editing, riferimento multi-immagine, rendering testo | Buono | [Gemini API](https://ai.google.dev/gemini-api/docs/image-generation) | Vedi [prezzi](https://ai.google.dev/gemini-api/docs/pricing) |
| **Flux** (Black Forest Labs — Pro 1.1, Kontext, Dev, Schnell) | Fotorealismo, coerenza di brand, batch; Kontext per editing in-image | Limitato | [BFL API](https://docs.bfl.ai/), Replicate, fal.ai | Vedi [prezzi](https://docs.bfl.ai/quick_start/pricing) |
| **Ideogram 3.0** | Tipografia, grafiche brandizzate, rendering testo accurato | Ottimo | [Ideogram API](https://developer.ideogram.ai/) | Vedi [prezzi](https://about.ideogram.ai/api-pricing) |
| **ChatGPT Images 2.0 / GPT Image** (OpenAI) | Uso generale, integrazione ChatGPT, editing nativo | Buono | [OpenAI API](https://platform.openai.com/docs/guides/image-generation) | Vedi [prezzi](https://platform.openai.com/docs/pricing) |
| **Midjourney v7** | Artistico, alta resa estetica, visual art-directed | Migliorato | Nessuna API ufficiale; Discord + Web | A abbonamento |
| **Recraft V3** | Illustrazioni vettoriali e coerenti col brand, asset di design | Forte | [Recraft API](https://www.recraft.ai/docs) | Per credito |
| **Stable Diffusion 3.5 / SDXL** | Self-hosted, personalizzabile, fine-tunabile | Variabile | Open source | Gratuito (costi GPU) |

**Nota:** DALL-E 3 è completamente deprecato. I modelli di immagini attuali di OpenAI sono la famiglia GPT Image / ChatGPT Images (`gpt-image-1` e successivi).

### Quale Usare Quando

```
Serve testo/titoli nell'immagine?
├── Sì → Ideogram 3.0 (il migliore), Gemini (buono), GPT Image / ChatGPT Images (discreto)
└── No ↓

Serve coerenza di prodotto/brand su molte immagini?
├── Sì → Flux (riferimento multi-immagine), Gemini Nano Banana Pro, Recraft V3
└── No ↓

Serve modificare un'immagine esistente (in loco)?
├── Sì → Gemini (editing nativo), Flux Kontext, ChatGPT Images
└── No ↓

Servono asset di brand vettoriali/illustrativi?
├── Sì → Recraft V3 (il migliore per vettoriale + coerenza brand), Midjourney (artistico)
└── No ↓

Serve la massima qualità visiva / direzione artistica?
├── Sì → Flux Pro 1.1, Midjourney v7
└── No ↓

Serve volume a basso costo?
└── Flux Schnell, Gemini Flash, Stable Diffusion (self-hosted)
```

### Basi del Prompting

Un prompt immagine efficace segue: **Soggetto + Ambientazione + Stile + Illuminazione + Composizione + Aspetti Tecnici**

```
Un laptop su una scrivania bianca minimale che mostra una UI dashboard,
illuminazione direzionale soffusa da sinistra, profondità di campo ridotta,
stile fotografia commerciale pulita, aspect ratio 16:9, 4K
```

**Errori comuni:**
- Troppo vago ("un'immagine business") — aggiungi dettagli specifici
- Dimenticare l'aspect ratio — specifica sempre le dimensioni
- Richiedere testo complesso — usa gli overlay per qualsiasi cosa oltre i titoli brevi
- Nessuna direzione di stile — "fotorealistico," "illustrazione flat," "render 3D"

Per guide di prompting dettagliate per modello, vedi [references/ai-image-prompting.md](references/ai-image-prompting.md).

---

## Strumenti di Design

Per lavori templatizzati e coerenti col brand dove la generazione AI è eccessiva o troppo imprevedibile.

### Canva

Ideale per chi non è designer ma ha bisogno di output rifinito velocemente.

- **Punti forti:** Libreria di template enorme, brand kit, Magic Resize (un design → tutte le dimensioni), collaborazione di team
- **Ideale per:** Grafiche social, presentazioni, header email, banner semplici
- **Limiti:** Meno controllo rispetto a Figma, i template possono risultare generici
- **Compatibilità con agent:** Ha un'API ma limitata — meglio come strumento human-in-the-loop

### Figma

Ideale per team con design system o esigenze di precisione pixel-perfect.

- **Punti forti:** Componenti del design system, auto layout, handoff per sviluppatori, plugin
- **Ideale per:** OG image tramite template, asset del design system, layout complessi
- **Limiti:** Curva di apprendimento più ripida, richiede competenze di design
- **Compatibilità con agent:** Ha un'API e un server MCP per leggere i design

### Quando Usare gli Strumenti di Design vs. la Generazione AI

| Scenario | Strumento di Design | Generazione AI |
|----------|:-:|:-:|
| Devono essere seguite linee guida di brand esatte | Sì | Forse (con immagini di riferimento forti) |
| Servono 20 varianti di dimensione di un design | Sì (Canva Magic Resize) | No |
| Hero image unica per un articolo di blog | No | Sì |
| Template social media ricorrente | Sì | No |
| Mockup di prodotto con UI reale | No (usa screenshot) | No (UI immaginaria) |
| Visual abstratto/creativo | No | Sì |

---

## Workflow di Immagini di Marketing

### Hero Image per Blog & Articoli

L'immagine in cima a ogni post. Stabilisce il tono, migliora la condivisibilità, richiesta per le anteprime OG/social.

1. **Definisci il concetto** — quale metafora visiva rappresenta l'argomento?
2. **Genera con l'AI** — usa Flux o Gemini per fotorealismo, Ideogram se serve testo
3. **Specifica 1200x630** (funziona sia per hero che per OG image) oppure **1920x1080** per full-width
4. **Ottimizza** — comprimi a <200KB, servi come WebP con fallback JPEG

**Pattern di prompt:**
```
[Metafora visiva per l'argomento], stile moderno e pulito,
illuminazione naturale luminosa, profondità di campo ridotta,
estetica da header di blog professionale, 1200x630
```

### Grafiche per Social Media

Immagini specifiche per piattaforma per post organici.

| Piattaforma | Dimensione Principale | Aspect Ratio | Note |
|----------|-------------|:---:|-------|
| Twitter/X | 1200x675 | 16:9 | Card immagine grande |
| LinkedIn | 1200x627 | 1.91:1 | Immagine feed |
| Instagram Feed | 1080x1080 | 1:1 | Quadrato; va bene anche 1080x1350 (4:5) |
| Instagram Stories | 1080x1920 | 9:16 | Verticale a schermo intero |
| Facebook | 1200x630 | 1.91:1 | Immagine di condivisione link |

**Workflow:**
1. Crea il concetto hero alla risoluzione più alta necessaria
2. Usa Canva Magic Resize o ritaglio manuale per le varianti per piattaforma
3. Aggiungi overlay di testo in modo programmatico (Ideogram o post-produzione) se necessario
4. Esporta nelle dimensioni specifiche per piattaforma

### Mockup di Prodotto & Screenshot

Mostra la UI del tuo prodotto nel contesto. I modelli AI immaginano l'interfaccia — non usarli per questo.

1. **Cattura screenshot reali** del tuo prodotto a risoluzione 2x
2. **Inquadra in mockup di dispositivo** — usa frame browser, laptop o template telefono
3. **Aggiungi contesto** — freccette di richiamo, etichette di funzionalità, confronti prima/dopo
4. **Annota con codice** — Hyperframes o HTML/CSS per overlay programmatici

**Strumenti:** Browser DevTools (screenshot), Shottr (Mac), CleanShot X, o CLI `screencapture`.

### Banner di Profilo & Scheda

Banner per profili, schede directory e pagine marketplace. Spesso la prima impressione visiva.

| Piattaforma | Dimensione | Note |
|----------|------|-------|
| Copertina personale LinkedIn | 1584x396 | 4:1, zona sicura al centro |
| Copertina aziendale LinkedIn | 1128x191 | 5.9:1; LinkedIn raccomanda fino a 4200x700 |
| Header Twitter/X | 1500x500 | 3:1, parzialmente oscurato dall'avatar |
| Galleria Product Hunt | 1270x760 | 5:3, fino a 6 immagini |
| Profilo G2 | 1280x720 | 16:9, preferiti screenshot di prodotto |
| Anteprima social GitHub | 1280x640 | 2:1, mostrata nelle card dei link |
| Screenshot App Store | Varia per dispositivo | Vedi skill aso per le specifiche complete |
| Grafica in evidenza Google Play | 1024x500 | ~2:1, richiesta per la scheda store |

**Best practice:**
- **Mantieni il testo minimo** — i banner vengono visti in piccolo su mobile
- **Centra i contenuti critici** — i bordi vengono ritagliati diversamente per dispositivo
- **Mostra il prodotto** — screenshot UI reali performano meglio dei grafici abstratti sulle schede directory
- **Rispetta il brand** — usa colori, font e posizionamento del logo coerenti
- **Aggiorna stagionalmente** — banner vecchi segnalano un prodotto inattivo

**Workflow:**
1. Scegli la/le piattaforma/e e annota le dimensioni esatte
2. Per le directory (Product Hunt, G2): usa screenshot di prodotto reali con leggera annotazione
3. Per i profili (LinkedIn, Twitter): usa i colori di brand + tagline + scatto di prodotto opzionale
4. Genera con template Canva/Figma o Ideogram (se ricco di testo)
5. Testa alla dimensione di visualizzazione reale — fai lo zoom indietro per controllare la leggibilità

### Asset di Brand

Loghi, icone e illustrazioni. La generazione AI ha dei limiti qui.

| Asset | Generazione AI | Strumento di Design | Note |
|-------|:-:|:-:|-------|
| Logo | Scarso — incoerente, non vettoriale | Sì (Figma) | Progetta sempre o commissiona i loghi |
| Icona app | Punto di partenza discreto | Sì (Figma) | Genera concetti, rifinisci manualmente |
| Illustrazioni | Buono per l'esplorazione di stile | Dipende | AI per i concetti, finalizza in uno strumento di design |
| Favicon | No | Sì | Deriva dal logo |
| Icone social | No | Sì | Usa gli asset forniti dalla piattaforma |

---

## Ottimizzazione delle Immagini

Ogni immagine sul tuo sito influisce sulla velocità della pagina, che a sua volta influisce su SEO e conversioni.

### Guida ai Formati

| Formato | Ideale Per | Compressione | Supporto Browser |
|--------|----------|-------------|:---:|
| **WebP** | Foto, grafiche — scelta predefinita | Lossy + lossless | ~96% |
| **AVIF** | Massima compressione, più recente | Migliore di WebP | ~94% |
| **JPEG** | Fallback per browser più vecchi | Solo lossy | Universale |
| **PNG** | Trasparenza, screenshot | Lossless | Universale |
| **SVG** | Loghi, icone, illustrazioni | Vettoriale (scala) | Universale |

### Checklist di Ottimizzazione

- [ ] **Servi WebP** con fallback JPEG/PNG (elemento `<picture>` o auto-formato del CDN)
- [ ] **Ridimensiona alla dimensione di visualizzazione** — non servire immagini da 4000px in contenitori da 800px
- [ ] **Comprimi** — punta a qualità 75-85% per le foto, quasi-lossless per gli screenshot
- [ ] **Lazy load** delle immagini sotto la piega (`loading="lazy"`)
- [ ] **Imposta dimensioni esplicite** — gli attributi `width` e `height` prevengono lo spostamento del layout (CLS)
- [ ] **Usa un CDN** con auto-ottimizzazione (Cloudflare, Vercel, Imgix, Cloudinary)
- [ ] **Aggiungi testo alternativo** — descrittivo, rilevante per le parole chiave, non sovraccarico

### Comandi Rapidi di Ottimizzazione

```bash
# Converti in WebP (usando cwebp)
cwebp -q 80 input.png -o output.webp

# Conversione batch con ImageMagick
mogrify -format webp -quality 80 *.png

# Ottimizza JPEG (usando jpegoptim)
jpegoptim --max=80 --strip-all *.jpg

# Controlla le dimensioni delle immagini in una pagina
curl -s https://yoursite.com | grep -oP 'src="[^"]+\.(jpg|png|webp)"' | head -20
```

---

## Immagini OG & Anteprima Social

L'immagine che appare quando il tuo URL viene condiviso su social media, Slack, Discord, ecc.

### Meta Tag Richiesti

```html
<meta property="og:image" content="https://yoursite.com/og/page-name.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://yoursite.com/og/page-name.jpg" />
```

### Immagini OG Dinamiche

Genera immagini OG in modo programmatico per pagine con contenuto dinamico (post di blog, profili utente):

- **Vercel OG** (`@vercel/og`) — genera immagini all'edge usando JSX
- **Satori** — converte HTML/CSS in SVG (alimenta Vercel OG)
- **Cloudinary** — overlay di testo basato su URL su immagini template

**Ideale per la SEO programmatica:** Genera immagini OG uniche per pagina usando template + dati dinamici.

---

## Errori Comuni

1. **Usare l'AI per screenshot di UI di prodotto** — i modelli immaginano le interfacce; cattura screenshot reali
2. **Saltare l'ottimizzazione delle immagini** — le immagini non ottimizzate sono il killer #1 della velocità di pagina
3. **Nessuna immagine OG** — i link condivisi appaiono rotti senza un'immagine di anteprima
4. **Aspect ratio sbagliato** — controlla sempre le specifiche della piattaforma prima di generare
5. **Immagini ricche di testo senza Ideogram** — la maggior parte dei modelli AI rovina il testo; usa Ideogram o aggiungi il testo in post-produzione
6. **Generare senza direzione di stile** — "fotorealistico," "illustrazione flat," "render 3D" cambiano drasticamente l'output
7. **Visual di brand incoerenti** — usa il riferimento multi-immagine di Flux o template di design per la coerenza
8. **Immagini enormi sulle landing page** — comprimi, ridimensiona, lazy load

---

## Domande Specifiche per il Task

1. Che tipo di immagine ti serve? (Hero per blog, grafica social, mockup, banner, asset di brand)
2. Quale piattaforma o posizionamento? (Questo determina le dimensioni)
3. Hai asset di brand da rispettare? (Colori, font, logo, guida di stile)
4. È un'immagine singola o un template ripetibile?
5. Hai chiavi API per strumenti di generazione immagini?
6. Deve essere ottimizzata per le performance web?

---

## Skill Collegate

- **ad-creative**: Per la creatività delle immagini per ads a pagamento, specifiche per piattaforma e produzione di ads su scala
- **video**: Per la produzione video AI e video programmatici
- **social**: Per cosa pubblicare e la strategia dei contenuti
- **cro**: Per il posizionamento delle immagini e l'ottimizzazione delle conversioni sulle landing page
- **seo-audit**: Per la SEO delle immagini (testo alt, nomi file, lazy loading)
- **aso**: Per le specifiche e l'ottimizzazione degli screenshot per app store
- **directory-submissions**: Per le immagini della galleria Product Hunt e i visual delle schede directory
</content>
