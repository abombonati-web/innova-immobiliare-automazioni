/* ============================================================
   MOTORE DEL SEMAFORO FINANZIARIO
   ------------------------------------------------------------
   Valuta le risposte del modulo contro le regole descritte in
   config/regole-semaforo.json e restituisce un esito
   (verde / giallo / rosso) con la motivazione e le azioni da
   scatenare.

   Due principi che il codice deve rispettare sempre:

   1. Le regole stanno nel JSON, non qui. Aggiungere un caso
      significa aggiungere un oggetto al file di configurazione,
      non modificare questo file.

   2. GDPR art. 22. Questo motore non nega mai un servizio in
      via definitiva: produce un esito e, per ogni esito diverso
      dal verde, espone sempre la possibilità di un riesame da
      parte di una persona (campo `revisione_umana`).

   Nota di sicurezza: in produzione la valutazione va eseguita
   lato server. Girando nel browser, le risposte sono
   modificabili dall'utente ed è impossibile impedire a chi ha
   voglia di provarci di sbloccare la prenotazione. Qui gira nel
   browser solo perché la demo è statica.
   ============================================================ */

/* ---------- Operatori disponibili nelle regole ---------- */

const OPERATORI = {
  uguale: (valore, atteso) => valore === atteso,
  diverso: (valore, atteso) => valore !== atteso,
  in: (valore, attesi) => Array.isArray(attesi) && attesi.includes(valore),
  non_in: (valore, attesi) => Array.isArray(attesi) && !attesi.includes(valore),
  maggiore: (valore, soglia) => numero(valore) !== null && numero(valore) > soglia,
  maggiore_uguale: (valore, soglia) => numero(valore) !== null && numero(valore) >= soglia,
  minore: (valore, soglia) => numero(valore) !== null && numero(valore) < soglia,
  minore_uguale: (valore, soglia) => numero(valore) !== null && numero(valore) <= soglia,
  vuoto: (valore) => vuoto(valore),
  non_vuoto: (valore) => !vuoto(valore)
};

function vuoto(valore) {
  return valore === undefined || valore === null || valore === "" ||
    (typeof valore === "number" && Number.isNaN(valore));
}

function numero(valore) {
  if (vuoto(valore)) return null;
  const n = typeof valore === "number" ? valore : parseFloat(String(valore).replace(",", "."));
  return Number.isNaN(n) ? null : n;
}

/* ---------- Valutazione di una singola condizione ---------- */

export function valutaCondizione(condizione, contesto) {
  if (!condizione) return false;

  switch (condizione.operatore) {
    case "sempre":
      return true;

    case "e":
      return (condizione.condizioni || []).every((c) => valutaCondizione(c, contesto));

    case "o":
      return (condizione.condizioni || []).some((c) => valutaCondizione(c, contesto));

    case "non":
      return !valutaCondizione(condizione.condizione, contesto);

    case "campi_mancanti":
      return (condizione.campi || []).some((campo) => vuoto(contesto[campo]));

    default: {
      const fn = OPERATORI[condizione.operatore];
      if (!fn) {
        throw new Error(`Operatore non riconosciuto nella regola: "${condizione.operatore}"`);
      }
      return fn(contesto[condizione.campo], condizione.valore);
    }
  }
}

/* ---------- Costruzione del contesto ---------- */

/**
 * Arricchisce le risposte del modulo con i campi derivati che le
 * regole possono interrogare. Il cliente non li compila: li calcola
 * il motore incrociando le risposte con i dati dell'immobile.
 */
export function preparaContesto(risposte, immobile) {
  const contesto = { ...risposte };
  const pubblico = immobile?.pubblico || {};

  const budget = numero(risposte.budget_massimo);
  const prezzo = numero(pubblico.prezzo);
  contesto.rapporto_budget_prezzo =
    budget !== null && prezzo ? budget / prezzo : null;

  const reddito = numero(risposte.reddito_mensile_netto);
  const canone = numero(pubblico.canone_mensile);
  contesto.incidenza_canone_reddito =
    reddito && canone ? canone / reddito : null;

  contesto.immobile_id = immobile?.id || null;
  contesto.tipo_operazione = immobile?.tipo_operazione || null;

  return contesto;
}

/* ---------- Valutazione completa ---------- */

/**
 * @param {object} risposte  risposte del modulo, con i nomi canonici di config/modulo-campi.json
 * @param {object} immobile  immobile di riferimento (può essere null per i venditori)
 * @param {object} config    contenuto di config/regole-semaforo.json
 * @returns {object} esito completo, pronto sia per la pagina sia per il CRM
 */
export function valutaSemaforo(risposte, immobile, config) {
  const contesto = preparaContesto(risposte || {}, immobile);

  let regolaVincente = null;
  for (const regola of config.regole) {
    if (valutaCondizione(regola.quando, contesto)) {
      regolaVincente = regola;
      break;
    }
  }

  // Se nessuna regola corrisponde — configurazione senza fallback —
  // il comportamento sicuro è il giallo, non il verde.
  if (!regolaVincente) {
    regolaVincente = {
      id: "nessuna-regola",
      esito: "giallo",
      motivazione: "Nessuna regola corrisponde alle risposte: si passa da una persona.",
      azioni: ["notifica_consulente_finanziario"]
    };
  }

  const esito = config.esiti[regolaVincente.esito];

  return {
    esito: regolaVincente.esito,
    etichetta: esito.etichetta,
    colore: esito.colore,
    prenotazione_sbloccata: esito.prenotazione_sbloccata === true,
    messaggio_cliente: esito.messaggio_cliente,
    messaggio_interno: esito.messaggio_interno,
    regola_applicata: regolaVincente.id,
    motivazione: regolaVincente.motivazione,
    azioni: regolaVincente.azioni || [],
    /* Sempre presente, qualunque sia l'esito: è il requisito
       dell'art. 22 GDPR sulla decisione automatizzata. */
    revisione_umana: {
      disponibile: true,
      canali: config.revisione_umana?.canali || [],
      testo: "Non ti ritrovi in questo esito? Parla con una persona del team: rivediamo insieme la tua situazione."
    },
    contesto_valutato: contesto,
    valutato_il: new Date().toISOString(),
    versione_regole: config.versione
  };
}

/**
 * Registra l'esito della verifica del consulente finanziario su un
 * caso giallo. È l'unico modo previsto per sbloccare la prenotazione
 * dopo un esito diverso dal verde: la decisione resta di una persona.
 */
export function applicaEsitoConsulente(valutazione, { approvato, operatore, note }) {
  return {
    ...valutazione,
    esito: approvato ? "verde" : valutazione.esito,
    prenotazione_sbloccata: approvato === true,
    revisione_effettuata: {
      approvato: approvato === true,
      operatore,
      note: note || "",
      registrata_il: new Date().toISOString()
    }
  };
}
