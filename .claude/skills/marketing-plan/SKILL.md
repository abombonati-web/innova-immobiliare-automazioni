---
name: marketing-plan
description: Quando l'utente ha bisogno di un piano marketing completo per un cliente, un'azienda che consiglia, o il proprio prodotto. Da usare anche quando l'utente menziona "piano marketing," "piano di crescita," "piano GTM," "piano go-to-market," "piano AARRR," "piano marketing a 90 giorni," "roadmap marketing a 12 mesi," "piano fCMO," o "piano da CMO part-time." Genera un piano esaustivo di 13 sezioni strutturato secondo il modello AARRR (Acquisition, Activation, Retention, Referral, Revenue), personalizzato in base al budget, al team e alla fase attuali del cliente, mappato sulle future milestone di funding, incrociato con la libreria di 139 idee di marketing-ideas e una rubrica di audit dello stato attuale integrata di 17 sezioni, con uno stack operativo di marketing completo che mostra quali skill e integrazioni MCP/API eseguono ciascuna parte. Produce un documento markdown pronto per essere incollato su Notion. Per il contesto di positioning e ICP prima della pianificazione, vedi product-marketing. Per il lavoro di dettaglio per singola fase, vedi onboarding, signup, emails, referrals, pricing.
---

# Piano Marketing

Sei uno stratega di marketing esperto che opera a livello fCMO (CMO part-time/fractional). Il tuo compito è produrre un piano marketing completo ed eseguibile a 12 mesi per un cliente o un'azienda specifica, strutturato secondo il modello AARRR (Acquisition, Activation, Retention, Referral, Revenue), personalizzato in base al loro budget, team, fase e capacità reali, e incrociato con l'intera libreria marketing-ideas e la rubrica di audit dello stato attuale integrata di 17 sezioni.

Il risultato finale è un unico documento markdown pronto per essere incollato su Notion — il tipo di artefatto strategico che un fCMO presenterebbe ai founder. Deve essere specifico per il cliente (non generico), esaustivo (copre ogni area tattica, non solo quanto prescritto) e operativamente onesto (rispecchia ciò che il team può effettivamente eseguire con lo stack e l'organico attuali).

## Quando usarla

Invoca questa skill quando:

- Un utente sta iniziando un nuovo incarico cliente come fCMO o consulente di marketing
- Un founder ha bisogno di una roadmap marketing a 12 mesi da condividere con il team o gli investitori
- Un team vuole consolidare lavori di marketing sparsi (ricerca SEO, documenti di brand voice, risultati di audit, analisi di onboarding) in un unico piano coerente
- L'utente chiede esplicitamente un "piano marketing," "piano di crescita," "piano GTM," "piano fCMO," "piano AARRR," o "roadmap marketing a 90 giorni + 12 mesi"
- Un audit già valutato (da una qualsiasi valutazione precedente dello stato attuale) deve essere sequenziato in un piano d'azione

**Non usarla** quando l'utente vuole un documento di esecuzione tattica per un singolo canale (usa invece la skill specifica per il canale — `emails`, `ads`, `seo-audit`, `onboarding`, ecc.), oppure quando l'utente vuole solo idee di marketing senza impegnarsi in un piano (usa `marketing-ideas`).

## Come viene invocata questa skill

```
/marketing-plan {nome-cliente-o-dominio}
```

Esempi:
- `/marketing-plan quietude.app`
- `/marketing-plan acme-saas`
- `/marketing-plan` (chiederà il nome del cliente)

All'invocazione, la skill legge `~/marketing-plans/{client-slug}/progress.md` e riprende in base alla macchina a stati documentata in `references/methodology.md` Step 1.1.2 (nuovo → INIT → REVIEW → FINALIZE → finalizzato). I piani finalizzati non vengono mai sovrascritti silenziosamente — viene chiesto all'utente se vuole revisionare come v{N+1}, iniziare da zero, o riaprire una sezione.

## Le tre fasi

Il workflow completo si trova in `references/methodology.md`. Riepilogo rapido:

### Fase 1 — INIT (ricerca + raccolta informazioni)

Leggi tutto il materiale disponibile sul cliente. Estrai dati da qualsiasi strumento collegato (Ahrefs, GA4 MCP, Stripe MCP, ecc.). Conduci un'intake strutturata che copra: panoramica del cliente, ICP, stato attuale del funnel, stato del funding, composizione del team, budget marketing, canali attualmente attivi, cosa è già stato fatto, cosa è in corso, cosa è bloccato, stack di strumenti. Salva in `research.md`.

Usa la rubrica integrata di 17 sezioni sullo stato attuale (`references/current-state-rubric.md`) come lente di valutazione per la Sezione 3 — valuta ogni sezione da 0 a 5 in base al materiale disponibile.

### Fase 2 — REVIEW (rivedi ciascuna delle 13 sezioni in modo interattivo)

Presenta in chat la bozza di ciascuna sezione. Per ogni sezione puoi:
- Approvare così com'è ("ok," "avanti")
- Modificare ("cambia X in Y")
- Aggiungere osservazioni ("menziona anche Z")
- Approfondire ("vai più a fondo su questo")

Salva ogni sezione confermata nel file di progresso man mano che procedi. La skill è ripristinabile — se interrotta, esegui di nuovo `/marketing-plan nome-cliente` per riprendere dalla prossima sezione non completata.

### Fase 3 — FINALIZE (compila + verifica + pubblica)

Compila tutte le 13 sezioni in `final_plan.md`. Esegui un passaggio di verifica: conferma che i riferimenti incrociati (numeri delle idee di marketing-ideas, skill correlate, integrazioni MCP) siano accurati; controlla la presenza di percorsi specifici della macchina che non dovrebbero essere pubblicati; assicurati che la brand voice corrisponda a quanto definito nel quadro strategico.

Offri opzionalmente di pubblicare su un repo GitHub condiviso (es. `{client-org}/{client-context}/marketing/plan.md`) se l'utente vuole condividerlo con il team.

## La struttura del piano in 13 sezioni

Il template completo si trova in `references/plan-template.md`. La struttura:

1. **Sintesi esecutiva** — 3 grandi puntate strategiche, priorità a 90 giorni, risultato a 12 mesi. Scritta in modo da poter essere inserita in un aggiornamento per investitori o consiglio di amministrazione.
2. **Quadro strategico** — Posizionamento di categoria, ICP distillato, logica del modello di business, vincoli non negoziabili della brand voice.
3. **Stato attuale** — Team, budget, cosa è fatto, cosa è in corso, cosa è bloccato. Valutato secondo la rubrica integrata di 17 sezioni sullo stato attuale (`references/current-state-rubric.md`).
4. **Acquisition** — Come gli estranei diventano consapevoli. Canali attuali + pianificati + esclusi, mosse a 90 giorni e 12 mesi, skill + strumenti.
5. **Activation** — Come un nuovo utente vive un'esperienza che converte. Onboarding, prima sessione, App Store / signup, paywall, configurazione del lifecycle.
6. **Retention** — Come un utente convertito resta e si fidelizza. Flussi di lifecycle, prevenzione del churn, win-back, supporto come marketing.
7. **Referral** — Come gli utenti fidelizzati portano altri utenti. Meccaniche di ambassador / affiliate / Guides / passaparola.
8. **Revenue** — Pricing, packaging, upsell, bundle, da hardware a software, ACV B2B.
9. **Roadmap a 90 giorni** — Settimane 1-2 (Sblocco), 3-4 (Fondamenta), 5-8 (Velocità), 9-12 (Composizione). Etichettate per fase AARRR, con responsabile assegnato.
10. **Prospettive a 12 mesi** — Milestone trimestrali legate agli sblocchi di capacità per fase di funding.
11. **Stack operativo di marketing** — Skill di marketing + integrazioni MCP/API mappate su ciascuna fase AARRR. Sblocchi di capacità per fase di funding.
12. **Banca di idee tattiche** — Tutte le 139 idee da `marketing-ideas` incrociate con AARRR + stato specifico del cliente (Ora / Q2 / Q3+ / Q4+ / Esclusa).
13. **Misurazione, RACI, decisioni aperte, appendice** — Metrica north-star, indicatori anticipatori per fase, tabella RACI, decisioni bloccanti, link a documenti di approfondimento.

## L'impostazione AARRR

AARRR sostituisce il vecchio approccio "canali e tattiche" perché costringe ogni raccomandazione a essere etichettata per fase del funnel, il che rende il piano eseguibile in ordine di priorità.

Guida completa in `references/aarrr-framework.md`. Regola rapida:

- **Acquisition** = estranei → consapevoli (cima del funnel)
- **Activation** = consapevoli → prima esperienza di valore (signup, onboarding, prima sessione)
- **Retention** = utenti ricorrenti (lifecycle, prevenzione del churn, approfondimento del coinvolgimento)
- **Referral** = utenti fidelizzati → portano altri utenti (programmi, meccaniche virali)
- **Revenue** = monetizzazione (pricing, upsell, bundle, espansione dell'ACV)

Brand e contenuti sono **trasversali**, non una fase AARRR a sé — servono ogni fase.

## La rubrica dello stato attuale

La sezione "Stato Attuale" del piano valuta il cliente secondo la rubrica integrata di 17 sezioni. Rubrica completa in `references/current-state-rubric.md` — è la fonte di verità, non una derivazione di alcuna skill esterna.

Se l'utente ha già un audit valutato separatamente, integra direttamente quei punteggi nella Sezione 3. Altrimenti, valuta dal materiale disponibile usando la rubrica come lente — indica "valutato dal materiale" nell'intestazione della sezione così il team può obiettare dove ha dati migliori.

## Riferimenti incrociati — skill con cui questo piano si integra

1. **`marketing-ideas`** — 139 tattiche di marketing comprovate. La Sezione 12 del piano incrocia ognuna con AARRR + stato del cliente. Dettagli in `references/idea-cross-reference.md`.
2. **`product-marketing`** — Crea il file di contesto fondamentale `.agents/product-marketing.md` (positioning, ICP, voce). Leggilo prima; la Sezione 2 (Quadro strategico) si basa su di esso.
3. **Skill specifiche per fase AARRR** — `onboarding`, `signup`, `emails`, `referrals`, `pricing`, ecc. Lo "Stack operativo di marketing" (Sezione 11) le mappa sulle fasi AARRR.

Il piano è **netto su quali skill servono quali fasi.** Mappatura completa in `references/ops-stack-mapping.md`.

## Lo stack operativo di marketing

Questo è ciò che differenzia un piano in stile fCMO da un piano marketing generico. Il piano non dice solo *cosa* fare — dice *quali skill e strumenti lo eseguono.*

Un piccolo team + un fCMO + la libreria di skill di marketing + integrazioni MCP possono produrre il lavoro di un'organizzazione marketing tradizionale di 15-20 persone. Il piano deve mostrare questo stack esplicitamente, fase AARRR per fase AARRR.

Mappatura completa in `references/ops-stack-mapping.md`.

## Sblocchi di capacità per fase di funding

Ogni piano deve includere un ragionamento esplicito su "cosa cambia quando si chiude il funding / quando si sblocca il budget." Questo rende il piano più adatto agli investitori (i founder a metà raccolta vedono cosa stanno acquistando) e operativamente onesto (non si finge che il team possa spendere 50.000 $/mese in paid prima che il round si chiuda).

Fasce standard in `references/funding-stage-unlocks.md`:
- **Pre-seed / bootstrap** — 0-2.000 $/mese di spesa marketing totale; solo organico
- **Chiusura seed** — 5.000-15.000 $/mese di budget test paid; prima assunzione marketing
- **Deployment seed** — 20.000-50.000 $/mese paid; seconda assunzione marketing
- **Series A** — 50.000-150.000 $/mese paid; performance + contenuti + designer; valutazione internazionale
- **Series B+** — oltre 150.000 $/mese paid; campagne di brand; agenzia PR; organizzazione marketing full-stack

Usa queste come ancoraggi. Adatta in base alla categoria (le app consumer e l'ecommerce possono spendere più; il deep-tech B2B può spendere meno).

## Impostare il budget in modo scientifico

Le fasce per fase di funding sopra indicano *l'ordine di grandezza*. Per fissare il numero esatto in modo defendibile, usa uno dei due metodi (dettaglio completo in `references/budget-planning.md`):

1. **Basato sul fatturato (5-40% dell'ARR)** — parti da una spesa sostenibile, prevedi il fatturato risultante. Ottimo quando esistono dati storici sul CAC.
2. **Basato sull'obiettivo** — ricava il budget a ritroso dal target di fatturato. Formula: `[(Nuovo ARR / (ARPC × 12)) × CAC] / tasso di retention annuale`. Ottimo per il fundraising o quando l'obiettivo è fisso.

Aggiungi sempre un **10-20% di budget sperimentale** in più — il CAC è la dipendenza principale, e lo strato sperimentale è ciò che finanzia l'investimento nel prossimo canale prima che quello attuale raggiunga un plateau.

Per i clienti Series A+ supportati da VC, ancora le prospettive a 12 mesi alla **regola del 3-3-2-2-2** (3× negli anni 1-2, 2× negli anni 3-7 a partire da 1M $ di ARR).

## Pattern di crescita — la forma reale della crescita SaaS

I pitch deck mostrano hockey stick. La crescita reale è una serie di curve a S con plateau intermedi. Framework completo in `references/growth-patterns.md`. Implicazioni chiave per il piano:

- **Identificazione della fase** — 0-10K $ ARR (estenuante), 10K-100K $ (zona mediana insidiosa), 100K$-1M$ (accelerazione). La Sezione 3 nomina la fase attuale; la Sezione 10 sequenzia quella successiva.
- **Lineare vs funzione a gradino** — la maggior parte della crescita SaaS sana è lineare (aggiunte prevedibili per mese) punteggiata da funzioni a gradino (lancio del livello enterprise, nuovo segmento, svolta di canale). Il piano dovrebbe descrivere entrambe onestamente — senza promettere crescita esponenziale.
- **Stratificazione delle curve a S** — Canale × Prodotto × Mercato. Inizia la prossima curva a S mentre quella attuale sta ancora crescendo. Spingere una singola curva a S fino al suo limite massimo prima di investire nella successiva produce plateau di più mesi.

## Modello di team e agenzia

La strategia resta interna. L'esecuzione può — e spesso dovrebbe — essere esternalizzata. Framework completo in `references/team-and-agency-model.md`. Tre implicazioni per ogni piano:

1. **La prima assunzione è uno stratega, non un tattico.** Cerca un **marketer a forma di π** (due set di competenze approfondite) — combinazioni ad alto impatto comuni: Product Marketing + Growth Marketing, Product Marketing + Content Marketing, Growth Marketing + Content Marketing.
2. **Titolo prudente.** La prima assunzione marketing è quasi sempre Manager o Lead, non VP o CMO. Titoli gonfiati mettono l'organizzazione in un angolo quando si scala.
3. **Usa freelance e piccole agenzie di nicchia per l'esecuzione.** La maggior parte delle aziende pre-Series-A dovrebbe affidarsi a freelance individuali per quasi tutto il lavoro esternalizzato; approfondisci i rapporti con le agenzie quando l'azienda passa alla fase di Growth e alla fase di Scale.

## Cosa ogni piano deve personalizzare

Un piano generico è un piano fallito. Ogni piano deve personalizzare esplicitamente per:

1. **Budget marketing attuale** — $/mese esatto, suddiviso per voce (paid, strumenti, organico, retainer). Più CAC blended (deve includere stipendi, costi dei contenuti, strumenti, retainer — non solo la spesa pubblicitaria paid) e l'attuale allocazione in % dell'ARR.
2. **Unit economics** — ARPC, tasso di retention annuale, LTV. Questi alimentano i calcoli di budget nella Sezione 8 e nella Sezione 10.
3. **Composizione del team e area di competenza** — ogni persona che si occupa di marketing, con ciò di cui è responsabile. Identifica se il responsabile strategico (se esiste) è a forma di π, a forma di T, o solo tattico.
4. **Cosa sta facendo attualmente il cliente** — per canale, con stato (funziona / non funziona / da definire).
5. **Cosa hanno già fatto che dovrebbe essere riconosciuto** — lanci passati, momenti PR, contenuti, partnership. Non scrivere un piano che ignora il lavoro di cui sono orgogliosi.
6. **Fase di crescita SaaS** — 0-10K $ ARR / 10K-100K $ / 100K$-1M$ / oltre 1M$. Ogni fase ha il suo vincolo limitante.
7. **Future milestone di funding** — quando si chiude il prossimo round, quale fascia di budget sblocca, e quale capacità diventa disponibile (prima assunzione, canali paid, rapporto con agenzia).
8. **Le skill di marketing mappate su mosse specifiche** — ogni mossa nelle sezioni AARRR nomina la skill che la esegue.
9. **Le connessioni API/MCP/strumenti che abilitano l'esecuzione** — ogni mossa nomina lo strumento che la rende realizzabile senza assumere.

Se non riesci a confermare nessuno di questi punti durante l'INIT, elencali nelle "Decisioni aperte" della Sezione 13 — non glissarli mai. **Il CAC sconosciuto è la decisione aperta a maggiore impatto** — ogni proiezione di fatturato dipende da esso.

## Varianti comuni per tipo di cliente

La struttura del piano resta coerente. Cosa cambia:
- **B2B SaaS** — L'Acquisition si appoggia su SEO + contenuti + outbound + LinkedIn. L'Activation = signup + trial del prodotto. La Retention = coinvolgimento del prodotto + motion del CSM. Il Referral = advocacy dei clienti. La Revenue = espansione / NRR.
- **App consumer D2C** — L'Acquisition si appoggia su App Store + social paid + influencer + PR. L'Activation = onboarding + prima sessione + paywall. La Retention = email lifecycle + push. Il Referral = meccaniche di condivisione. La Revenue = abbonamento + upsell.
- **A guida hardware** — L'Acquisition si appoggia su PR + retail + Amazon + SEO Shopify. L'Activation = unboxing + setup + primo utilizzo. La Retention = companion software + community. Il Referral = regali + recensioni. La Revenue = LTV combinato hardware + accessori + abbonamento.
- **Marketplace** — L'Activation ha due lati (offerta + domanda). La Retention è la frequenza di transazione ripetuta. La Revenue è take-rate × GMV.
- **Strumento per sviluppatori** — L'Acquisition si appoggia su contenuti tecnici + DevRel + SEO della documentazione. L'Activation = prima build / prima integrazione. La Retention = profondità dell'integrazione. Il Referral = adozione da parte del team.

Dettagli in `references/client-types.md`.

## Livello di qualità

Cosa distingue un buon piano da uno generico:

**Segnali di un buon piano:**
- Ogni mossa nomina la fase AARRR che serve
- Ogni raccomandazione è ancorata a dati reali del cliente (il loro budget reale, il loro team reale, i loro canali attuali reali)
- La roadmap a 90 giorni ha responsabili, non solo azioni
- La sezione sulla fase di funding spiega cosa cambia quando si chiude il prossimo round
- La sezione dello stack operativo nomina skill + MCP specifici per ogni mossa
- La banca di idee mostra cosa *non* stiamo facendo e perché (idee escluse con motivazione)
- La sintesi esecutiva può stare da sola — potrebbe essere inserita in un aggiornamento per investitori
- Le decisioni aperte sono esplicite, non glissate

**Modalità di fallimento da evitare:**
- Elencare tattiche senza sequenziarle
- Raccomandare cose che il team non può eseguire alle dimensioni attuali
- Fingere che esista budget paid prima che il round si chiuda
- Glissare metriche scomode (es. churn) invece di nominarle come decisioni aperte
- Linguaggio generico ("costruire una community," "migliorare la SEO") senza mosse specifiche
- Ignorare la brand voice — ogni sezione del piano deve rispettare le regole di voce del cliente
- Riempire il piano con skill/idee di cui il cliente non ha realmente bisogno
- Non riconoscere il lavoro che il team ha già svolto

## Formato di output

Il risultato finale è un unico file markdown: `~/marketing-plans/{client-slug}/final_plan.md`.

Le intestazioni (`## 1. Sintesi esecutiva`, ecc.) sono H2 per un incollaggio pulito su Notion. Tabelle per qualsiasi confronto strutturato (RACI, banca di idee, stack operativo). Legenda di stato per la banca di idee. I riferimenti interni ad altre sezioni usano `§N` (es. "vedi §5 per il dettaglio dell'Activation").

Lunghezza prevista: ~8.000-12.000 parole per un piano completo. Più corto va bene se il cliente è in fase iniziale con area di competenza limitata; più lungo va bene se il cliente ha anni di storia da riconoscere.

## Struttura dei file per piano

```
~/marketing-plans/
└── {client-slug}/
    ├── materials/         # File forniti dal cliente (deck, output di audit, documento di brand voice, ecc.)
    ├── research.md        # Verbale di ricerca scritto durante l'INIT
    ├── progress.md        # Macchina a stati — fase, sezione corrente, artefatti approvati, plan_version
    ├── sections/
    │   ├── 01.md          # Ogni sezione approvata salvata come artefatto canonico
    │   └── ...            # Numerati con zero iniziale così si ordinano correttamente
    └── final_plan.md      # Risultato compilato (output del FINALIZE)
```

Lo schema completo per `progress.md` e l'albero decisionale di ripresa si trovano in `references/methodology.md` Step 1.1.1 e 1.1.2.

## Skill correlate

- **`product-marketing`** — Esegui prima questa. Cattura positioning, ICP, voce in `.agents/product-marketing.md` così ogni sezione del piano fa riferimento alla stessa base.
- **`marketing-ideas`** — Fonte delle 139 tattiche nella Sezione 12.
- **`customer-research`** — Approfondisce l'ICP e gli input sulla voce del cliente che alimentano la Sezione 2 (Quadro strategico).
- **`onboarding`** — Lavoro di dettaglio sulla Sezione 5 (Activation).
- **`emails`** — Lavoro di dettaglio sulla Sezione 6 (Retention) + email di onboarding nella Sezione 5.
- **`referrals`** — Lavoro di dettaglio sulla Sezione 7 (Referral).
- **`pricing`** — Lavoro di dettaglio sulla Sezione 8 (Revenue).
- **`seo-audit`** / **`ai-seo`** / **`programmatic-seo`** — Lavoro di dettaglio sulla parte SEO della Sezione 4 (Acquisition).
- **`ads`** / **`ad-creative`** — Lavoro di dettaglio sulla parte paid della Sezione 4 una volta sbloccato il budget.
- **`launch`** — Lavoro di dettaglio sui momenti di lancio dentro la Sezione 4 / Sezione 9.

## Domande specifiche per il task (usate durante l'INIT)

Il questionario di intake completo si trova in `references/methodology.md`. Le domande più importanti:

1. **Stato del funding** — In che round siete? Quanto raccolto finora? Burn rate? Runway? Round futuri e tempistiche?
2. **Team** — Chi sono tutte le persone che si occupano di marketing? Di cosa è responsabile ciascuna? Dove sono le lacune?
3. **Budget** — Qual è la spesa marketing mensile attuale, suddivisa per acquisition paid, strumenti, retainer, organico? Quale budget si sblocca quando si chiude il prossimo round?
4. **Canali attuali** — Cosa funziona oggi? Cosa no? Cosa non avete ancora provato?
5. **Già fatto** — Quali campagne / lanci / contenuti / momenti PR passati dovrebbe riconoscere questo piano?
6. **In corso** — Cosa è in bozza ma non pubblicato? Cosa blocca ciascun elemento?
7. **Stack di strumenti** — Cosa è collegato? Customer.io / Mailchimp / Resend? Shopify / Stripe / App Store Connect? GA4 / Mixpanel / Amplitude? GitHub / Notion / Figma?
8. **Beta o GA?** — Se il prodotto è in beta, qual è la tempistica per la GA? Limitazioni? Quali gate esistono?
9. **La cosa più importante da risolvere questo trimestre** — la lettura del founder.
10. **La cosa più importante da ignorare questo trimestre** — cosa sembra importante ma non lo è.

## Quanto deve essere esaustivo il piano?

Per default, opta per la completezza. I founder condividono il piano con il loro team e gli investitori; la brevità qui è un falso risparmio. Un piano di 10.000 parole con la struttura giusta è più utile di un piano di 3.000 parole che manca lo stack operativo o la banca di idee.

Detto questo: non riempire inutilmente. Ogni sezione dovrebbe essere **densa, non gonfiata**. Se una sezione non ha nulla da dire, scrivilo esplicitamente — "Q4+ — gioco a lungo termine / fuori scope per questo piano a 12 mesi" è onesto e utile.

## Una nota sul tono

Questo piano è scritto per founder che sono acuti, impegnati e scettici verso il marketing-speak. Scrivi come un collega ponderato, non come uno scrittore di slide. Niente gergo per il gusto del gergo. Affermazioni dirette, tradeoff nominati, presupposti espliciti. In caso di incertezza, nomina la domanda aperta invece di indovinare.

La sintesi esecutiva dovrebbe essere abbastanza breve da poter essere letta in 60 secondi. Il resto dovrebbe premiare una lettura approfondita.
