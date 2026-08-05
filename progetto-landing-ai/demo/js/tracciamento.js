/* ============================================================
   MONITORAGGIO COMPORTAMENTALE
   ------------------------------------------------------------
   Raccoglie che cosa fa davvero il visitatore sulla landing:
   quali sezioni guarda e per quanto, quali foto apre, se avvia
   il tour virtuale, quali video guarda e fino a che punto, dove
   si ferma nel modulo.

   Gli eventi vengono accodati e spediti in blocco all'endpoint
   di Innova Experience. Finché l'endpoint non esiste, restano
   in sessione e sono ispezionabili dalla console: è quello che
   serve per collaudare il tracciamento prima di collegarlo.

   Privacy: nessun evento viene raccolto prima del consenso.
   Fino ad allora si contano solo eventi anonimi di pagina, senza
   identificativi persistenti.
   ============================================================ */

const STATO = {
  consenso: false,
  sessione: null,
  contatto: null,
  immobile: null,
  coda: [],
  iniziato: Date.now(),
  tempiSezione: new Map(),
  inviaA: null // URL dell'endpoint Innova Experience, quando esisterà
};

function idSessione() {
  return `s-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

export function inizializzaTracciamento({ immobile, endpoint = null } = {}) {
  STATO.sessione = idSessione();
  STATO.immobile = immobile?.id || null;
  STATO.inviaA = endpoint;
  traccia("pagina_aperta", {
    immobile: STATO.immobile,
    riferimento: document.referrer || null,
    parametri: Object.fromEntries(new URLSearchParams(location.search))
  });
  osservaSezioni();
  osservaUscita();
  return STATO.sessione;
}

/** Il consenso privacy sblocca il tracciamento identificato. */
export function attivaConsenso(contatto) {
  STATO.consenso = true;
  STATO.contatto = contatto || null;
  traccia("consenso_accordato", { canale: "modulo" });
}

export function traccia(evento, dati = {}) {
  const record = {
    evento,
    dati,
    immobile: STATO.immobile,
    sessione: STATO.sessione,
    contatto: STATO.consenso ? STATO.contatto : null,
    secondi_da_apertura: Math.round((Date.now() - STATO.iniziato) / 1000),
    ora: new Date().toISOString()
  };

  STATO.coda.push(record);

  // Ponte verso gli strumenti già in uso (Meta Pixel, GA4),
  // che restano opzionali: se non ci sono, non succede nulla.
  if (typeof window !== "undefined") {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: `innova_${evento}`, ...record });
    if (typeof window.fbq === "function" && evento === "modulo_inviato") {
      window.fbq("track", "Lead");
    }
  }

  spedisci();
  return record;
}

let timerInvio = null;
function spedisci() {
  if (!STATO.inviaA) return; // endpoint non ancora collegato: la coda resta locale
  clearTimeout(timerInvio);
  timerInvio = setTimeout(async () => {
    const daInviare = STATO.coda.splice(0, STATO.coda.length);
    if (!daInviare.length) return;
    try {
      await fetch(STATO.inviaA, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ eventi: daInviare }),
        keepalive: true
      });
    } catch (_) {
      STATO.coda.unshift(...daInviare); // riprova al prossimo giro
    }
  }, 2000);
}

/* ---------- Tempo di permanenza per sezione ---------- */

function osservaSezioni() {
  const sezioni = document.querySelectorAll("[data-sezione]");
  if (!sezioni.length || typeof IntersectionObserver === "undefined") return;

  const osservatore = new IntersectionObserver(
    (voci) => {
      voci.forEach((voce) => {
        const nome = voce.target.dataset.sezione;
        if (voce.isIntersecting) {
          STATO.tempiSezione.set(nome, Date.now());
          traccia("sezione_vista", { sezione: nome });
        } else if (STATO.tempiSezione.has(nome)) {
          const secondi = Math.round((Date.now() - STATO.tempiSezione.get(nome)) / 1000);
          STATO.tempiSezione.delete(nome);
          if (secondi >= 2) traccia("sezione_letta", { sezione: nome, secondi });
        }
      });
    },
    { threshold: 0.4 }
  );

  sezioni.forEach((s) => osservatore.observe(s));
}

/* ---------- Abbandono del modulo ---------- */

/**
 * Considera "modulo abbandonato" un modulo con almeno un contatto
 * valido compilato e mai inviato. È l'evento che innesca la
 * sequenza di recupero dopo pochi minuti.
 */
export function osservaAbbandonoModulo(form, { onAbbandono } = {}) {
  let toccato = false;
  let inviato = false;

  form.addEventListener("input", (e) => {
    if (!toccato) {
      toccato = true;
      traccia("modulo_iniziato", {});
    }
    if (e.target.name) traccia("campo_compilato", { campo: e.target.name });
  });

  form.addEventListener("submit", () => {
    inviato = true;
  });

  const verifica = () => {
    if (!toccato || inviato) return;
    const dati = Object.fromEntries(new FormData(form).entries());
    const contattabile = dati.email || dati.telefono;
    if (!contattabile) return;
    traccia("modulo_abbandonato", { ultimo_campo: ultimoCampo(form) });
    if (onAbbandono) onAbbandono(dati);
  };

  window.addEventListener("pagehide", verifica);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") verifica();
  });
}

function ultimoCampo(form) {
  const campi = [...form.elements].filter((e) => e.name && e.value);
  return campi.length ? campi[campi.length - 1].name : null;
}

/* ---------- Uscita dalla pagina ---------- */

function osservaUscita() {
  window.addEventListener("pagehide", () => {
    traccia("pagina_chiusa", {
      secondi_totali: Math.round((Date.now() - STATO.iniziato) / 1000),
      profondita_scroll: profonditaScroll()
    });
  });
}

function profonditaScroll() {
  const altezza = document.body.scrollHeight - window.innerHeight;
  if (altezza <= 0) return 100;
  return Math.min(100, Math.round((window.scrollY / altezza) * 100));
}

/* ---------- Ispezione in fase di collaudo ---------- */

export function codaEventi() {
  return [...STATO.coda];
}

export function riepilogoComportamento() {
  const perEvento = {};
  for (const record of STATO.coda) {
    perEvento[record.evento] = (perEvento[record.evento] || 0) + 1;
  }
  return {
    sessione: STATO.sessione,
    immobile: STATO.immobile,
    consenso: STATO.consenso,
    eventi_totali: STATO.coda.length,
    per_evento: perEvento
  };
}
