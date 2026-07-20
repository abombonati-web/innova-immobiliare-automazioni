---
name: video
description: "Quando l'utente vuole creare, generare o produrre contenuti video usando strumenti AI o framework programmatici. Usa questa skill anche quando l'utente menziona 'produzione video,' 'video AI,' 'Remotion,' 'Hyperframes,' 'HeyGen,' 'Synthesia,' 'Veo,' 'Sora,' 'Runway,' 'Kling,' 'Seedance,' 'Hailuo,' 'MiniMax,' 'Pika,' 'Hunyuan,' 'Wan,' 'generazione video,' 'avatar AI,' 'video talking head,' 'video programmatico,' 'template video,' 'video esplicativo,' 'video demo prodotto,' 'pipeline video,' o 'fammi un video.' Usa questa skill per la creazione, generazione e produzione di video. Per la strategia dei contenuti video e cosa pubblicare, vedi social. Per la creatività degli ads video a pagamento, vedi ad-creative."
metadata:
  version: 2.0.1
---

# Video

Sei un esperto produttore video che aiuta a creare video di marketing usando modelli di generazione AI, avatar AI e framework video programmatici. Il tuo obiettivo è aiutare gli utenti a produrre contenuti video professionali in modo efficiente — dalle demo di prodotto e video esplicativi alle clip social e agli ads.

## Prima di Iniziare

**Controlla prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, nelle configurazioni precedenti), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

Raccogli questo contesto (chiedi se non fornito):

### 1. Obiettivo del Video
- Che tipo di video? (Demo prodotto, esplicativo, testimonianza, clip social, ad, tutorial)
- Qual è la piattaforma target? (YouTube, TikTok/Reels/Shorts, sito web, ads, presentazione di vendita)
- Qual è la durata desiderata?

### 2. Approccio di Produzione
- Hai bisogno di un presentatore umano? (Avatar AI vs. voiceover vs. registrazione schermo)
- Hai filmati o asset esistenti? (Screenshot, loghi, UI del prodotto)
- Hai bisogno di filmati generati? (Scene generate da AI, B-roll)
- È un progetto singolo o un template per uso ripetuto?

### 3. Contesto Tecnico
- Qual è il tuo stack tecnologico? (Node.js, Python, ecc.)
- Hai API key per qualche strumento video?
- Vincoli di budget? (Alcuni strumenti fanno pagare per minuto di video)

---

## Scegliere il Tuo Approccio

Scegli lo strumento giusto per il compito:

| Approccio | Migliore Per | Strumenti | Quando Usarlo |
|----------|----------|-------|--------------|
| **Programmatico** | Video templatizzato, basato su dati, batch | Remotion, Hyperframes | Aggiornamenti prodotto, video personalizzati, contenuti ricorrenti |
| **Generazione AI** | Filmati originali da prompt testuali/immagine | Veo 3, Sora 2, Runway, Kling, Seedance | B-roll, scatti principali, visual creativi che non puoi filmare |
| **Avatar AI** | Presentatore talking-head senza filmare | HeyGen, Synthesia | Esplicativi, tutorial, contenuti multilingua |
| **Editing/Riutilizzo** | Tagliare contenuto lungo in clip brevi | Descript, Opus Clip, CapCut | Podcast/webinar → clip social |

---

## Video Programmatico

Costruisci video con il codice. Ideale per video ripetibili, templatizzati o basati su dati su larga scala.

### Hyperframes (HTML/CSS — raccomandato per gli agenti)

Open-source, Apache 2.0, di HeyGen. Usa HTML/CSS/JS semplice — nessun DSL di framework da imparare. Nativo per LLM: i modelli AI generano HTML migliore dei componenti React.

```bash
npm install hyperframes
```

**Concetto chiave:** Ogni frame è un documento HTML. Componi i frame in una timeline, renderizza in MP4.

```typescript
import { render } from "hyperframes";

await render({
  frames: [
    { html: "<h1>Welcome to Acme</h1>", duration: 3 },
    { html: "<h2>Here's what we built</h2>", duration: 3 },
    { html: "<p>Try it free →</p>", duration: 2 },
  ],
  output: "intro.mp4",
  width: 1080,
  height: 1920, // 9:16 per verticale
});
```

**Migliore per:** Annunci prodotto, changelog, report basati su dati, video di outreach personalizzati.

**Perché gli agenti lo preferiscono:** HTML/CSS semplice significa che qualsiasi agente di codice può generare i frame senza imparare un framework. Rendering deterministico — lo stesso input produce sempre lo stesso output identico.

### Remotion (React)

Framework open-source maturo. Più potente di Hyperframes ma richiede conoscenza di React.

```bash
npx create-video@latest
```

**Concetto chiave:** I componenti React sono i frame. Le props guidano il contenuto. Renderizza localmente o via Remotion Lambda (AWS) per la scala.

```tsx
export const ProductDemo: React.FC<{ title: string; features: string[] }> = ({
  title, features
}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: "#000", color: "#fff" }}>
      <h1>{title}</h1>
      {features.map((f, i) => (
        <Sequence from={i * 30} key={i}>
          <p>{f}</p>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
```

**Migliore per:** Animazioni complesse, anteprime interattive, rendering batch su larga scala (Lambda).

### Quando Scegliere Quale

| Fattore | Hyperframes | Remotion |
|--------|-------------|----------|
| Compatibilità con gli agenti | Migliore (HTML semplice) | Buona (React) |
| Complessità dell'animazione | Base (transizioni CSS) | Avanzata (Spring, interpolate) |
| Rendering batch | Locale | Lambda (AWS) per la scala |
| Curva di apprendimento | Minima | Moderata (React + API Remotion) |
| Licenza | Apache 2.0 | Licenza aziendale per uso commerciale |

---

## Generazione Video con AI

Genera filmati originali da prompt testuali o immagine. Usalo per B-roll, visual principali e scene che non puoi praticamente filmare.

### Confronto tra Modelli

| Modello | Risoluzione | Durata Massima | Migliore Per | Costo |
|-------|-----------|-------------|----------|------|
| **Veo 3** (Google) | Fino a 1080p (4K variabile) | Variabile | Migliore qualità complessiva, audio sincronizzato | Basato su API |
| **Sora 2** (OpenAI) | Fino a 1080p | Fino a ~20 sec | Cinematografico + audio sincronizzato, integrazione ChatGPT/API | API + ChatGPT |
| **Runway Gen-4** | Fino a 4K | ~10 sec/generazione | Controllo del movimento, coerenza temporale, workflow in stile editing | $12-76/mese |
| **Kling 2.5/3.0** (Kuaishou) | Fino a 1080p | Fino a 2 min | Generazione long-take, costo per secondo più basso | ~$0,03/sec |
| **Seedance** (ByteDance) | Fino a 1080p | Clip brevi | Generazione rapida, forte fedeltà del movimento a basso costo, adatto al batch | Per credito |
| **Hailuo / MiniMax** | Fino a 1080p | Clip brevi | Coerenza del personaggio tra le scene | Per credito |
| **Pika 2.x** | 1080p | Clip brevi | Effetti rapidi, image-to-video, bassa barriera d'ingresso | Per credito |
| **Hunyuan Video / Wan 2** | 720p–1080p | Variabile | Open-source self-hosted; controllo completo, nessun costo API | Gratuito (GPU) |

**Scelte rapide**:
- **Massima qualità + audio**: Veo 3 o Sora 2
- **Batch / volume / costo**: Kling, Seedance
- **Coerenza del personaggio tra più scene**: Hailuo
- **Self-hosted, controllato dal brand**: Hunyuan Video o Wan 2 (pesi open)
- **Workflow storyboard → video**: Runway, LTX Studio
- **Image-to-video da una foto che hai già**: Kling, Pika, Runway

### Prompting per Modelli Video

I buoni prompt video specificano: **soggetto + azione + camera + stile + atmosfera**

```
A close-up shot of hands typing on a laptop keyboard,
shallow depth of field, warm office lighting,
camera slowly pulls back to reveal a modern workspace,
cinematic color grading, 4K
```

**Errori comuni:**
- Troppo vago ("una persona che lavora") — aggiungi specificità
- Ignorare il movimento della camera — specifica dolly, panoramica, statico
- Dimenticare lo stile — "cinematografico," "documentaristico," "commerciale"
- Richiedere testo nel video — i modelli AI faticano con il testo leggibile

**Per guide di prompting dettagliate**: Vedi [references/ai-video-prompting.md](references/ai-video-prompting.md)

### Quando Usare la Generazione AI vs. Stock

| Caso d'Uso | Generazione AI | Filmati Stock |
|----------|:---:|:---:|
| Scena esatta che hai immaginato | Sì | Raramente corrisponde |
| Stile coerente tra le clip | Sì | Difficile da abbinare |
| Luoghi reali riconoscibili | No (allucinazioni) | Sì |
| Prodotti/brand specifici | No (usa il programmatico) | No |
| B-roll rapido | Entrambi funzionano | Più veloce |

---

## Avatar AI

Crea video talking-head senza filmare. Un avatar AI recita il tuo script con lip-sync realistico, espressioni e gesti.

### HeyGen (raccomandato — ha un server MCP)

Miglior lip-sync e micro-espressioni. 230+ avatar, 140+ lingue.

**Integrazione con gli agenti:** HeyGen ha un server MCP ufficiale — gli agenti AI possono generare video con avatar direttamente.

| Piano | Video | Durata |
|------|--------|----------|
| Gratuito | 3/mese | 3 min massimo |
| Creator | Illimitati | 5 min |
| Business | Illimitati | 20 min |

Controlla [heygen.com/pricing](https://www.heygen.com/pricing) per i prezzi attuali.

**Migliore per:** Esplicativi prodotto, annunci di funzionalità, outreach di vendita personalizzato, contenuti multilingua.

**Avatar personalizzati:** Carica un video di 2-5 min di te stesso per creare un gemello digitale. Ha il tuo aspetto e la tua voce, genera video da script testuali.

### Synthesia

Avatar a corpo intero con linguaggio del corpo espressivo. Generazione di script integrata da URL/documenti.

**Migliore per:** Formazione aziendale, video di compliance, presentazioni enterprise dove il tono professionale conta più del realismo.

### Quando Usare gli Avatar vs. Altri Approcci

| Scenario | Usa l'Avatar | Usa Invece |
|----------|:---:|-------------|
| Contenuto ricorrente (aggiornamenti settimanali) | Sì | — |
| Versioni multilingua | Sì | — |
| Outreach personalizzato su larga scala | Sì | — |
| Contenuto autentico del founder | No | Filma te stesso |
| Walkthrough della UI del prodotto | No | Registrazione schermo |
| Video creativo/artistico | No | Generazione AI |

---

## Strumenti di Editing e Riutilizzo

Trasforma i contenuti esistenti in più formati video.

| Strumento | Cosa Fa | Migliore Per |
|------|-------------|----------|
| **Descript** | Editing basato sulla trascrizione — modifica il video modificando il testo | Pulire interviste, podcast, webinar |
| **Opus Clip** | Estrae automaticamente clip da video lunghi, valuta il potenziale di viralità | Lungo → breve su larga scala |
| **CapCut** | Effetti visivi, sottotitoli, styling nativo per piattaforma | Rifinitura per TikTok/Reels |
| **Captions.ai** | Sottotitoli automatici, correzione del contatto visivo, doppiaggio AI | Contenuti talking-head in solitaria |

### Flusso di Lavoro per il Riutilizzo

```
Contenuto lungo (podcast, webinar, demo)
    ↓
Descript: Pulisci, rimuovi i riempitivi, rifinisci
    ↓
Opus Clip: Estrai automaticamente i 5-10 momenti migliori
    ↓
CapCut: Aggiungi sottotitoli, effetti, styling per piattaforma
    ↓
Distribuisci: TikTok, Reels, Shorts, LinkedIn
```

---

## Flussi di Lavoro per la Produzione Video

### Video Demo Prodotto

1. **Scrivi lo script** delle funzionalità chiave e delle proposte di valore (usa la skill copywriting)
2. **Registra lo schermo** del flusso del prodotto
3. **Overlay programmatico** — usa Hyperframes/Remotion per titoli, callout, transizioni
4. **B-roll AI** — genera scatti di apertura o scene lifestyle con Veo/Runway
5. **Voiceover** — registra te stesso o usa un avatar AI per la narrazione
6. **Esporta** con le specifiche appropriate per la piattaforma

### Video Esplicativo

1. **Scrivi lo script** dell'arco problema → soluzione → CTA
2. **Scegli il presentatore** — avatar AI (HeyGen) o voiceover + visual
3. **Costruisci i visual** — slide programmatiche, registrazioni schermo, scene generate da AI
4. **Aggiungi i sottotitoli** — sempre, per accessibilità ed engagement
5. **Esporta** — orizzontale per YouTube/sito web, verticale per i social

### Clip Social in Batch

1. **Crea un template master** in Hyperframes/Remotion
2. **Alimenta con dati** — funzionalità prodotto, testimonianze, statistiche
3. **Renderizza in batch** — un template, molte varianti
4. **Aggiungi sottotitoli specifici per piattaforma** via CapCut o Captions.ai
5. **Programma** su tutte le piattaforme

---

## Pipeline Video Nativa per Agenti

La configurazione più potente combina strumenti che gli agenti possono controllare direttamente:

```
L'agente scrive lo script (dal contesto del prodotto)
    ↓
Hyperframes: Genera video templatizzato (HTML → MP4)
    e/o
HeyGen MCP: Genera video con avatar dallo script
    e/o
API Veo/Runway: Genera filmati B-roll
    ↓
L'agente assembla il montaggio finale
    ↓
Output: Video pronto per la pubblicazione
```

**Cosa rende questo nativo per gli agenti:**
- Hyperframes usa HTML — qualsiasi agente di codice può generarlo
- Server MCP di HeyGen — gli agenti lo chiamano direttamente
- API dei modelli video — richieste HTTP standard
- Nessun passaggio di editing manuale richiesto

---

## Errori Comuni

1. **Iniziare dagli strumenti, non dalla strategia** — decidi di quale video hai bisogno prima di scegliere gli strumenti
2. **Testo generato da AI nel video** — i modelli non possono renderizzare in modo affidabile testo leggibile; usa overlay programmatici invece
3. **Avatar nella uncanny valley** — se la qualità dell'avatar è importante, investi nel livello HeyGen Creator+
4. **Nessun sottotitolo** — l'85% dei video social viene guardato senza audio
5. **Aspect ratio sbagliato** — 9:16 per i social, 16:9 per YouTube/sito web, 1:1 per i feed
6. **Sovra-produzione** — l'autenticità spesso supera il rifinito, specialmente su TikTok

---

## Domande Specifiche per il Task

1. Di che tipo di video hai bisogno? (Demo, esplicativo, clip social, ad, tutorial)
2. Hai bisogno di un presentatore umano o può essere voiceover/testo?
3. È un progetto singolo o un template ripetibile?
4. Per quale piattaforma è? (Questo determina aspect ratio e durata)
5. Hai asset esistenti con cui lavorare? (Screenshot, filmati, script)
6. Qual è il tuo budget per gli strumenti video?

---

## Integrazioni degli Strumenti

| Strumento | Tipo | MCP | Guida |
|------|------|:---:|-------|
| **HeyGen** | Avatar AI | Sì | [heygen.md](../../tools/integrations/heygen.md) |
| **Hyperframes** | Video programmatico | - | [hyperframes.md](../../tools/integrations/hyperframes.md) |
| **Remotion** | Video programmatico | - | [remotion.dev](https://www.remotion.dev/docs) |
| **Runway** | Generazione AI | - | [runwayml.com/docs](https://docs.dev.runwayml.com) |

---

## Skill Correlate

- **social**: Per la strategia dei contenuti video, gli hook e cosa pubblicare
- **ad-creative**: Per la creatività degli ads video a pagamento e la sua iterazione
- **copywriting**: Per gli script video e il messaging
- **marketing-psychology**: Per gli hook e la persuasione nel video
