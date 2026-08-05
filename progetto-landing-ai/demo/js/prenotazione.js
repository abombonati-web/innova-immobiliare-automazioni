/* ============================================================
   PRENOTAZIONE CON SLOT REALI
   ------------------------------------------------------------
   Genera gli slot disponibili a partire dalla configurazione
   dell'agenzia e li incrocia con gli impegni già a calendario.

   In produzione gli impegni arrivano da Google Calendar con
   l'API FreeBusy (una sola chiamata, nessun dato sensibile
   esposto: restituisce solo gli intervalli occupati) e la
   conferma crea l'evento con Calendar Events.insert, invitando
   cliente e agente. Nessuna conferma manuale: lo slot scelto è
   già l'appuntamento.

   Qui la funzione `caricaOccupati` è sostituibile: la demo usa
   dati finti, la produzione le passa il vero client Google.
   ============================================================ */

const GIORNI = ["dom", "lun", "mar", "mer", "gio", "ven", "sab"];

const ETICHETTE_GIORNO = {
  0: "domenica", 1: "lunedì", 2: "martedì", 3: "mercoledì",
  4: "giovedì", 5: "venerdì", 6: "sabato"
};

const MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
  "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"];

export function etichettaSlot(data) {
  const ore = String(data.getHours()).padStart(2, "0");
  const minuti = String(data.getMinutes()).padStart(2, "0");
  return `${ETICHETTE_GIORNO[data.getDay()]} ${data.getDate()} ${MESI[data.getMonth()]}, ore ${ore}:${minuti}`;
}

/**
 * Costruisce gli slot liberi dei prossimi giorni.
 *
 * @param {object} configPrenotazione  nodo 'prenotazione' di data/agenzia.json
 * @param {Array}  occupati            [{inizio: ISO, fine: ISO}] dal calendario
 * @param {object} opzioni
 *   @param {number} [opzioni.giorni=14]  orizzonte di ricerca
 *   @param {number} [opzioni.massimo=12] quanti slot mostrare
 *   @param {Date}   [opzioni.adesso]
 */
export function generaSlot(configPrenotazione, occupati = [], opzioni = {}) {
  const giorni = opzioni.giorni || 14;
  const massimo = opzioni.massimo || 12;
  const adesso = opzioni.adesso || new Date();
  const durata = configPrenotazione.durata_slot_minuti;
  const anticipoMs = (configPrenotazione.anticipo_minimo_ore || 0) * 3_600_000;
  const primaDisponibilita = new Date(adesso.getTime() + anticipoMs);

  const impegni = occupati.map((o) => ({
    inizio: new Date(o.inizio).getTime(),
    fine: new Date(o.fine).getTime()
  }));

  const slot = [];

  for (let g = 0; g <= giorni && slot.length < massimo; g++) {
    const giorno = new Date(adesso);
    giorno.setDate(giorno.getDate() + g);
    if (!configPrenotazione.giorni_disponibili.includes(GIORNI[giorno.getDay()])) continue;

    for (const fascia of configPrenotazione.fasce) {
      const [hDalle, mDalle] = fascia.dalle.split(":").map(Number);
      const [hAlle, mAlle] = fascia.alle.split(":").map(Number);

      const inizioFascia = new Date(giorno);
      inizioFascia.setHours(hDalle, mDalle, 0, 0);
      const fineFascia = new Date(giorno);
      fineFascia.setHours(hAlle, mAlle, 0, 0);

      for (
        let t = inizioFascia.getTime();
        t + durata * 60_000 <= fineFascia.getTime() && slot.length < massimo;
        t += durata * 60_000
      ) {
        const fine = t + durata * 60_000;
        if (t < primaDisponibilita.getTime()) continue;
        const sovrapposto = impegni.some((i) => t < i.fine && fine > i.inizio);
        if (sovrapposto) continue;

        slot.push({
          inizio: new Date(t).toISOString(),
          fine: new Date(fine).toISOString(),
          etichetta: etichettaSlot(new Date(t)),
          durata_minuti: durata
        });
      }
    }
  }

  return slot;
}

/**
 * Luoghi selezionabili, filtrati sui permessi del cliente: la sala
 * visore è riservata a chi ha superato la prequalifica.
 */
export function luoghiDisponibili(configPrenotazione, { prequalificato, immobile }) {
  return configPrenotazione.luoghi.filter((luogo) => {
    if (luogo.riservato_a === "clienti_prequalificati" && !prequalificato) return false;
    if (luogo.id === "ufficio_visore" && !immobile?.pubblico?.media?.visore_in_ufficio?.disponibile) return false;
    return true;
  });
}

/**
 * Prepara l'evento da creare su Google Calendar. In produzione
 * questo oggetto viene passato tale e quale a Events.insert.
 */
export function preparaEventoCalendario({ slot, luogo, contatto, immobile, agenzia }) {
  const indirizzo = luogo.id === "ufficio_visore"
    ? agenzia.indirizzo
    : immobile.pubblico.indirizzo;

  return {
    summary: `${luogo.etichetta} — ${immobile.pubblico.titolo}`,
    location: indirizzo,
    description: [
      `Cliente: ${contatto.nome} — ${contatto.telefono} — ${contatto.email}`,
      `Immobile: ${immobile.pubblico.titolo} (${immobile.id})`,
      `Tipo: ${luogo.etichetta}`,
      `Prenotazione generata automaticamente dalla landing.`
    ].join("\n"),
    start: { dateTime: slot.inizio, timeZone: "Europe/Rome" },
    end: { dateTime: slot.fine, timeZone: "Europe/Rome" },
    attendees: [{ email: contatto.email }, { email: agenzia.email }],
    reminders: {
      useDefault: false,
      overrides: [
        { method: "popup", minutes: 24 * 60 },
        { method: "popup", minutes: 60 }
      ]
    }
  };
}

/** File .ics da allegare alla conferma, utile anche senza integrazione. */
export function generaIcs(evento) {
  const stampa = (iso) => iso.replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  return [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Innova Immobiliare//Landing//IT",
    "BEGIN:VEVENT",
    `UID:${Date.now()}@innovaimmobiliare.it`,
    `DTSTAMP:${stampa(new Date().toISOString())}`,
    `DTSTART:${stampa(evento.start.dateTime)}`,
    `DTEND:${stampa(evento.end.dateTime)}`,
    `SUMMARY:${evento.summary}`,
    `LOCATION:${evento.location}`,
    `DESCRIPTION:${evento.description.replace(/\n/g, "\\n")}`,
    "END:VEVENT",
    "END:VCALENDAR"
  ].join("\r\n");
}

/**
 * Punto di innesto per il calendario reale. La demo restituisce
 * impegni finti; in produzione qui si chiama l'API FreeBusy.
 */
export async function caricaOccupati({ finti = true } = {}) {
  if (!finti) {
    throw new Error("Collegare qui Google Calendar FreeBusy (vedi docs/03-architettura.md).");
  }
  const domani = new Date();
  domani.setDate(domani.getDate() + 1);
  domani.setHours(10, 0, 0, 0);
  const dopo = new Date(domani.getTime() + 90 * 60_000);
  return [{ inizio: domani.toISOString(), fine: dopo.toISOString() }];
}
