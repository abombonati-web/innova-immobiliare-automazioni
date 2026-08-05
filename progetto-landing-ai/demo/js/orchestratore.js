/* ============================================================
   ORCHESTRATORE DELLE COMUNICAZIONI
   ------------------------------------------------------------
   Trasforma un evento (modulo inviato, prenotazione confermata,
   appuntamento mancato…) nell'elenco dei messaggi da spedire,
   con canale, testo compilato e istante esatto di invio.

   Questo modulo NON spedisce niente: calcola il piano. L'invio
   vero è compito del provider WhatsApp Business e del servizio
   email transazionale. Tenerli separati permette di vedere in
   anticipo — e di far approvare — che cosa riceverà il cliente,
   prima che parta una sola notifica.
   ============================================================ */

const UNITA = { m: 60_000, h: 3_600_000, g: 86_400_000 };

/** Converte "24h", "3g", "-24h", "15m", "immediato" in millisecondi. */
export function offsetInMs(offset) {
  if (!offset || offset === "immediato") return 0;
  const match = String(offset).trim().match(/^(-?\d+)\s*([mhg])$/i);
  if (!match) throw new Error(`Offset non valido: "${offset}"`);
  return parseInt(match[1], 10) * UNITA[match[2].toLowerCase()];
}

/* ---------- Fascia oraria degli invii ---------- */

const GIORNI = ["dom", "lun", "mar", "mer", "gio", "ven", "sab"];

/**
 * Sposta un invio che cadrebbe fuori dalla fascia consentita alla
 * prima finestra utile. Un messaggio automatico alle 3 di notte fa
 * più danni del silenzio.
 */
export function rispettaFasciaOraria(data, fascia) {
  if (!fascia || Number.isNaN(data.getTime())) return data;
  const risultato = new Date(data);
  const [dalleH, dalleM] = fascia.dalle.split(":").map(Number);
  const [alleH, alleM] = fascia.alle.split(":").map(Number);

  for (let tentativi = 0; tentativi < 14; tentativi++) {
    const giornoOk = fascia.giorni.includes(GIORNI[risultato.getDay()]);
    const minuti = risultato.getHours() * 60 + risultato.getMinutes();
    const inizio = dalleH * 60 + dalleM;
    const fine = alleH * 60 + alleM;

    if (giornoOk && minuti >= inizio && minuti <= fine) return risultato;

    if (giornoOk && minuti < inizio) {
      risultato.setHours(dalleH, dalleM, 0, 0);
      return risultato;
    }

    // Troppo tardi, o giorno non consentito: si prova il giorno dopo.
    risultato.setDate(risultato.getDate() + 1);
    risultato.setHours(dalleH, dalleM, 0, 0);
  }
  return risultato;
}

/* ---------- Compilazione dei segnaposto ---------- */

export function compila(testo, dati) {
  return String(testo || "").replace(/\{\{([^}]+)\}\}/g, (intero, percorso) => {
    const valore = percorso
      .trim()
      .split(".")
      .reduce((oggetto, chiave) => (oggetto == null ? undefined : oggetto[chiave]), dati);
    return valore === undefined || valore === null ? intero : String(valore);
  });
}

/* ---------- Costruzione del piano ---------- */

/**
 * @param {string} nomeSequenza  chiave dentro config.sequenze
 * @param {object} contesto      { contatto, immobile, agente, prenotazione, risposte, semaforo, link }
 * @param {object} config        contenuto di config/comunicazioni.json
 * @param {Date}   [istante]     momento dell'evento scatenante
 * @returns {Array} messaggi programmati, ordinati per data di invio
 */
export function pianificaSequenza(nomeSequenza, contesto, config, istante = new Date()) {
  const sequenza = config.sequenze[nomeSequenza];
  if (!sequenza) throw new Error(`Sequenza sconosciuta: "${nomeSequenza}"`);

  return sequenza.messaggi
    .map((messaggio) => {
      // Gli offset negativi si contano a ritroso dalla data
      // dell'appuntamento, non dal momento della prenotazione.
      let riferimento = istante;
      if (messaggio.riferimento) {
        const valore = leggi(contesto, messaggio.riferimento);
        riferimento = new Date(valore);
        // Meglio fermarsi qui che programmare un invio a una data
        // inesistente: un promemoria mai partito non si nota finché
        // il cliente non si presenta a un appuntamento dimenticato.
        if (Number.isNaN(riferimento.getTime())) {
          throw new Error(
            `Il messaggio "${messaggio.id}" si riferisce a ${messaggio.riferimento}, che non è una data valida: ${JSON.stringify(valore)}`
          );
        }
      }

      const grezza = new Date(riferimento.getTime() + offsetInMs(messaggio.offset));
      const programmata = messaggio.offset === "immediato"
        ? grezza
        : rispettaFasciaOraria(grezza, config.fascia_oraria_invii);

      return {
        id: messaggio.id,
        sequenza: nomeSequenza,
        destinatario: messaggio.destinatario || "cliente",
        canale: messaggio.canale_primario,
        canale_fallback: messaggio.canale_fallback || null,
        oggetto: compila(messaggio.oggetto, contesto),
        testo: compila(messaggio.testo, contesto),
        invio_previsto: programmata.toISOString(),
        condizione: messaggio.condizione || null,
        richiede_conferma: messaggio.richiede_conferma === true,
        azione_finale: messaggio.azione_finale || null,
        sla_ore: messaggio.sla_ore || null,
        interrompi_se: sequenza.interrompi_se || []
      };
    })
    .sort((a, b) => a.invio_previsto.localeCompare(b.invio_previsto));
}

function leggi(oggetto, percorso) {
  return percorso.split(".").reduce((o, k) => (o == null ? undefined : o[k]), oggetto);
}

/**
 * Applica le esclusioni: i contatti etichettati come delicati
 * (per esempio sovraindebitamento) non entrano nelle sequenze
 * commerciali. È una regola di rispetto, prima che di conformità.
 */
export function filtraSequenzeAmmesse(nomiSequenze, etichetteContatto, configServizi) {
  const escluse = new Set();
  for (const servizio of configServizi.servizi || []) {
    if (etichetteContatto.includes(servizio.id)) {
      (servizio.esclusione_automazioni || []).forEach((s) => escluse.add(s));
    }
  }
  return nomiSequenze.filter((n) => !escluse.has(n));
}

/**
 * Sceglie la sequenza da attivare in base a intento ed esito del
 * semaforo. È il punto in cui i punti 6, 8, 9 e 10 del progetto si
 * incontrano.
 */
export function sequenzePerContatto({ intento, esitoSemaforo, moduloInviato }) {
  const sequenze = [];
  if (intento === "venditore") {
    sequenze.push("venditore");
    return sequenze;
  }
  if (!moduloInviato) {
    sequenze.push("recupero_modulo_abbandonato");
    return sequenze;
  }
  if (esitoSemaforo === "giallo") sequenze.push("semaforo_giallo");
  sequenze.push("follow_up_lead");
  return sequenze;
}
