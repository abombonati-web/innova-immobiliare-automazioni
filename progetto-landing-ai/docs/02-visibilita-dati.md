# Parte seconda — Visibilità dei dati

Una sola regola, applicata alla struttura dei dati e non alla buona volontà di chi scrive il codice:

> Ogni immobile è diviso in due nodi, `pubblico` e `riservato`.
> Il generatore di landing legge **soltanto** il nodo `pubblico`.

Non è una questione di stile. Se i dati riservati arrivassero al browser — anche nascosti,
anche in un campo non visualizzato — sarebbero leggibili da chiunque apra gli strumenti per
sviluppatori. Nascondere con il CSS non è nascondere. L'unico modo per non mostrare il nome
del proprietario è non mandarlo.

## Visibile al cliente

Tutto quello che serve per decidere:

| Dato | Dove |
|---|---|
| Zona, indirizzo, anno di costruzione | carta d'identità |
| Superficie, composizione, piani | carta d'identità |
| Classe energetica, riscaldamento, abitabilità | carta d'identità |
| Categoria e rendita catastale | carta d'identità |
| Prezzo (o canone), spese condominiali | carta d'identità e hero |
| Planimetria | sbloccata dopo l'accesso al club |
| Descrizione narrativa | sezione "Come si vive, qui" |
| Foto, video, tour virtuale | galleria e sezione video |
| Agente di riferimento con recapiti | footer |
| **Provvigioni in chiaro** | sezione dedicata, calcolata su questo immobile |

Le provvigioni non sono scritte in piccolo in fondo: hanno una sezione con il criterio
applicato, imponibile, IVA e totale, e il momento in cui sono dovute.

- 5.000 € + IVA per immobili fino a 100.000 €
- 5% + IVA del prezzo per immobili oltre 100.000 €
- 15% + IVA del canone annuale per gli affitti

Su una villa da 720.000 € significa mostrare 36.000 € + 7.920 € di IVA = **43.920 €**,
scritto prima della visita e non dopo la proposta. È la scelta più scomoda del progetto ed
è anche quella che, da sola, distingue la landing da qualunque annuncio di portale.

## Riservato all'agenzia

Non esce mai dal gestionale, non passa dal browser, non compare in nessuna risposta di rete:

| Dato | Perché resta dentro |
|---|---|
| Scadenza e tipo di mandato | un concorrente saprebbe quando presentarsi dal proprietario |
| Nome e recapiti del proprietario | contatti diretti che scavalcano l'agenzia |
| Note interne sulla trattativa | offerte ricevute, storia del prezzo, fragilità del venditore |
| Margini di negoziazione | il prezzo minimo accettabile è la vostra posizione contrattuale |
| Provvigione lato venditore | accordo separato, non riguarda l'acquirente |

Questi campi arrivano solo al cruscotto interno di Innova Experience, con controllo di ruolo,
e viaggiano su una richiesta diversa da quella che alimenta la landing.

## Come è garantito

Tre livelli, perché uno solo prima o poi cede:

1. **Struttura dei dati.** I due nodi sono separati alla radice del file JSON, non mescolati
   con un elenco di campi da escludere. Un campo nuovo aggiunto per distrazione al nodo
   `riservato` resta riservato senza che nessuno debba ricordarsene.
2. **Codice.** `demo/js/genera-landing.js` accede sempre e solo a `immobile.pubblico`.
3. **Test.** Due test automatici verificano che nel nodo pubblico non compaiano mai le chiavi
   `mandato`, `proprieta`, `trattativa`, `note_interne` — e falliscono se qualcuno le sposta.

Quando i dati arriveranno dal gestionale invece che da file, la separazione va fatta **lato
server**: l'API che serve la landing deve restituire solo il nodo pubblico, non l'intero
record filtrato dopo. Chi filtra a valle prima o poi dimentica un campo.

## Nota sul prezzo nascosto

La landing dell'evento già online usa il meccanismo del prezzo ribassato svelato solo ai
partecipanti. È compatibile con questo sistema: basta portare il prezzo nel nodo `riservato`
e mostrare in pagina il prezzo di mercato con la nota di rivelazione. La regola non cambia —
quello che non deve vedersi non viene mandato al browser.
