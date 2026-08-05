/* ============================================================
   MOTORE DI RILEVAMENTO DELL'INTENTO
   ------------------------------------------------------------
   Stabilisce se il contatto è un acquirente, un investitore, un
   affittuario o un venditore. Tre sorgenti, in ordine di
   affidabilità decrescente:

     1. la risposta esplicita del modulo         → certezza piena
     2. il contesto di arrivo (campagna, link)   → forte indizio
     3. il testo della conversazione con Sara    → indizio

   Quando le sorgenti sono in disaccordo vince quella più
   affidabile: se il cliente ha dichiarato "voglio vendere",
   nessuna parola pescata in chat può contraddirlo.
   ============================================================ */

export const INTENTI = ["acquirente", "investitore", "affittuario", "venditore"];

/* Parole e frasi tipiche di ciascun intento. Vanno lette come
   indizi cumulativi, non come interruttori: una sola parola non
   decide, il punteggio complessivo sì. */
const SEGNALI = {
  venditore: [
    "vendere", "vendo", "venderla", "mettere in vendita", "valutazione",
    "quanto vale", "stima", "mio appartamento", "casa mia", "ereditato",
    "eredità", "successione", "devo liberarmi", "mandato", "affittare la mia",
    "metto a reddito", "debiti", "asta", "pignoramento", "sovraindebitamento"
  ],
  affittuario: [
    "affitto", "in affitto", "locazione", "canone", "mensile", "prendere in affitto",
    "cerco casa in affitto", "trasferimento per lavoro", "contratto 4+4",
    "cedolare", "inquilino", "deposito cauzionale"
  ],
  investitore: [
    "investimento", "investire", "rendita", "reddito", "rendimento", "roi",
    "frazionamento", "frazionare", "b&b", "affitti brevi", "casa vacanze",
    "rivendere", "plusvalenza", "capitale", "portafoglio", "cap rate"
  ],
  acquirente: [
    "comprare", "acquistare", "prima casa", "mutuo", "viverci", "abitare",
    "famiglia", "traslocare", "cerco casa", "visita", "visitare", "planimetria",
    "trattabile", "prezzo"
  ]
};

/* Segnali che l'immobile stesso porta con sé: una landing di un
   immobile in affitto suggerisce, da sola, un affittuario. */
const PESO = {
  modulo: 100,
  parametro_url: 40,
  campagna: 25,
  tipo_immobile: 15,
  chat: 10 // per ogni segnale trovato
};

function normalizza(testo) {
  return (testo || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, ""); // via gli accenti: "perché" e "perche" devono coincidere
}

/**
 * @param {object} sorgenti
 *   @param {string} [sorgenti.rispostaModulo]  valore del campo 'intento' del modulo
 *   @param {string} [sorgenti.parametroUrl]    ?intento=... sul link della landing
 *   @param {string} [sorgenti.campagna]        utm_campaign / utm_content
 *   @param {string} [sorgenti.testoChat]       trascrizione della conversazione con Sara
 *   @param {string} [sorgenti.tipoOperazione]  'vendita' | 'affitto' dell'immobile visitato
 *   @param {string} [sorgenti.canale]          telefono, whatsapp, instagram, ...
 * @returns {{intento: string, confidenza: number, fonte: string, punteggi: object, motivazione: string}}
 */
export function rilevaIntento(sorgenti = {}) {
  const punteggi = Object.fromEntries(INTENTI.map((i) => [i, 0]));
  const motivazioni = [];

  // 1. Risposta esplicita del modulo: chiude il discorso.
  if (INTENTI.includes(sorgenti.rispostaModulo)) {
    punteggi[sorgenti.rispostaModulo] += PESO.modulo;
    motivazioni.push("dichiarato nel modulo");
  }

  // 2. Parametro esplicito sul link (link diversi per campagne diverse).
  if (INTENTI.includes(sorgenti.parametroUrl)) {
    punteggi[sorgenti.parametroUrl] += PESO.parametro_url;
    motivazioni.push("parametro del link");
  }

  // 3. Nome della campagna: "vendi-casa-palermo" dice molto.
  const campagna = normalizza(sorgenti.campagna);
  if (campagna) {
    for (const intento of INTENTI) {
      for (const segnale of SEGNALI[intento]) {
        if (campagna.includes(normalizza(segnale))) {
          punteggi[intento] += PESO.campagna;
          motivazioni.push(`campagna "${sorgenti.campagna}"`);
          break;
        }
      }
    }
  }

  // 4. Tipo di operazione dell'immobile su cui è atterrato.
  if (sorgenti.tipoOperazione === "affitto") {
    punteggi.affittuario += PESO.tipo_immobile;
    motivazioni.push("immobile in affitto");
  } else if (sorgenti.tipoOperazione === "vendita") {
    punteggi.acquirente += PESO.tipo_immobile;
    motivazioni.push("immobile in vendita");
  }

  // 5. Testo della conversazione con Sara o del chatbot.
  const testo = normalizza(sorgenti.testoChat);
  if (testo) {
    for (const intento of INTENTI) {
      const trovati = SEGNALI[intento].filter((s) => testo.includes(normalizza(s)));
      if (trovati.length) {
        punteggi[intento] += trovati.length * PESO.chat;
        motivazioni.push(`in conversazione: ${trovati.slice(0, 3).join(", ")}`);
      }
    }
  }

  const ordinati = Object.entries(punteggi).sort((a, b) => b[1] - a[1]);
  const [vincente, punteggio] = ordinati[0];
  const secondo = ordinati[1]?.[1] || 0;

  // Nessun segnale: si torna al comportamento neutro, non a un'ipotesi.
  if (punteggio === 0) {
    return {
      intento: "acquirente",
      confidenza: 0,
      fonte: "predefinito",
      punteggi,
      motivazione: "Nessun segnale disponibile: si chiede direttamente al cliente nel modulo."
    };
  }

  // La confidenza tiene conto anche del distacco dal secondo intento:
  // due intenti appaiati sono un caso da chiedere, non da indovinare.
  const distacco = (punteggio - secondo) / punteggio;
  const confidenza = Math.min(1, (punteggio / PESO.modulo) * 0.6 + distacco * 0.4);

  return {
    intento: vincente,
    confidenza: Math.round(confidenza * 100) / 100,
    fonte: sorgenti.rispostaModulo ? "modulo" : "inferito",
    punteggi,
    motivazione: motivazioni.join(" · ")
  };
}

/**
 * Sotto questa soglia non si personalizza la landing sull'intento
 * indovinato: si mostra la versione neutra e si chiede al cliente.
 */
export const SOGLIA_CONFIDENZA = 0.5;

export function intentoAffidabile(rilevazione) {
  return rilevazione.confidenza >= SOGLIA_CONFIDENZA;
}
