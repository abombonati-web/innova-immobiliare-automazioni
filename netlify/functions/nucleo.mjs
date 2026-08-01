/* ============================================================
   INNOVA EXPERIENCE — nucleo della piattaforma
   ------------------------------------------------------------
   Qui stanno le regole che governano contatti e attività, senza
   niente che dipenda dalla rete o dall'archivio: è il pezzo che
   si può provare da solo, ed è lo stesso che gira sul server.
============================================================ */

import crypto from "node:crypto";

/* ---------- Attività fissa applicata a ogni nuova lead ---------- */
export const ATTIVITA_FISSA = {
  titolo: "Chiamare la lead e confermare la fascia di visita",
  tipo: "chiamata",
  scadenzaOre: 24,
  checklist: [
    "Confermare la fascia di visita richiesta",
    "Capire se compra per abitarci o come investimento",
    "Verificare come intende acquistare (mutuo / liquidità)",
    "Spiegare le 4 tappe e l'apertura della piattaforma di venerdì",
    "Confermare email e telefono per l'accesso riservato"
  ]
};

export const ARCHIVIO_VUOTO = {
  contatti: [],
  attivita: [],
  attivitaFissa: { ...ATTIVITA_FISSA },
  versione: 0
};

/* ============================================================
   UTILITÀ
============================================================ */

export function uid(prefisso){
  return prefisso + "_" + Date.now().toString(36) + "_" + crypto.randomBytes(4).toString("hex");
}

/* Numero in formato WhatsApp internazionale (Italia di default) */
export function numeroWa(tel){
  let n = String(tel || "").replace(/\D/g, "");
  if(!n) return "";
  if(n.startsWith("0039")) n = n.slice(2);
  if(!n.startsWith("39"))  n = "39" + n;
  return n;
}

/* Due schede sono la stessa persona se condividono l'email oppure il telefono */
export function trovaDuplicato(contatti, dati, escludiId){
  const email = String(dati.email || "").toLowerCase().trim();
  const tel   = numeroWa(dati.telefono);
  if(!email && !tel) return null;
  return contatti.find(c =>
    !c.eliminato && c.id !== escludiId && (
      (email && String(c.email || "").toLowerCase().trim() === email) ||
      (tel   && numeroWa(c.telefono) === tel)
    )
  ) || null;
}

/* ============================================================
   CONTATTI E ATTIVITÀ
============================================================ */

export function nuovoContatto(dati, ora = new Date()){
  const iso = ora.toISOString();
  return {
    id: dati.id || uid("c"),
    nome:          String(dati.nome || "").trim() || "Senza nome",
    telefono:      String(dati.telefono || "").trim(),
    email:         String(dati.email || "").trim(),
    slot:          dati.slot          || "",
    interesse:     dati.interesse     || "",
    finanziamento: dati.finanziamento || "",
    note:          dati.note          || "",
    stato:         dati.stato         || "nuovo",
    evento:        dati.evento        || "Villa Città Giardino",
    origine: {
      utm_source:   dati.utm_source   || "",
      utm_medium:   dati.utm_medium   || "",
      utm_campaign: dati.utm_campaign || "",
      utm_content:  dati.utm_content  || ""
    },
    creato:     dati.creato || iso,
    aggiornato: iso
  };
}

/* Il riassunto del motivo per cui la lead ha scritto: serve in chiamata */
export function contestoLead(c){
  const r = [];
  if(c.interesse)     r.push("Interesse: " + c.interesse);
  if(c.slot)          r.push("Fascia richiesta: " + c.slot);
  if(c.finanziamento) r.push("Acquisto: " + c.finanziamento);
  if(c.note)          r.push("Ha scritto: «" + c.note + "»");
  const camp = [c.origine?.utm_source, c.origine?.utm_campaign].filter(Boolean).join(" · ");
  if(camp)            r.push("Proviene da: " + camp);
  return r.join("\n");
}

export function nuovaAttivitaFissa(contatto, impostazioni = ATTIVITA_FISSA, ora = new Date()){
  const ore = Number(impostazioni.scadenzaOre) || 24;
  const scadenza = new Date(new Date(contatto.creato).getTime() + ore * 3600 * 1000);
  const checklist = (impostazioni.checklist || []).filter(Boolean).map(r => "• " + r).join("\n");
  const iso = ora.toISOString();
  return {
    id: uid("a"),
    contattoId: contatto.id,
    tipo: impostazioni.tipo || "chiamata",
    titolo: impostazioni.titolo || ATTIVITA_FISSA.titolo,
    note: [contestoLead(contatto), checklist].filter(Boolean).join("\n\n"),
    stato: "aperta",
    scadenza: scadenza.toISOString(),
    svoltaIl: null,
    esito: "",
    automatica: true,
    creato: iso,
    aggiornato: iso
  };
}

/* ============================================================
   SINCRONIZZAZIONE
   Ogni scheda porta la propria data di aggiornamento: fra due
   versioni della stessa scheda vince la più recente. Le schede
   cancellate restano come segnaposto, così la cancellazione si
   propaga anche ai dispositivi che erano offline.
============================================================ */
export function fondi(esistenti, arrivati){
  const mappa = new Map((esistenti || []).map(x => [x.id, x]));
  (arrivati || []).forEach(nuovo => {
    if(!nuovo || !nuovo.id) return;
    const vecchio = mappa.get(nuovo.id);
    if(!vecchio || new Date(nuovo.aggiornato || 0) >= new Date(vecchio.aggiornato || 0)){
      mappa.set(nuovo.id, nuovo);
    }
  });
  return [...mappa.values()];
}

export function fondiArchivio(archivio, arrivato){
  const base = archivio || { ...ARCHIVIO_VUOTO };
  const unito = {
    contatti: fondi(base.contatti, arrivato?.contatti),
    attivita: fondi(base.attivita, arrivato?.attivita),
    attivitaFissa: base.attivitaFissa || { ...ATTIVITA_FISSA },
    versione: (base.versione || 0) + 1
  };
  /* Le impostazioni seguono la stessa regola: vince la più recente */
  const a = arrivato?.attivitaFissa;
  if(a && (!base.attivitaFissa?.aggiornato || new Date(a.aggiornato || 0) >= new Date(base.attivitaFissa.aggiornato || 0))){
    unito.attivitaFissa = a;
  }
  unito.aggiornato = new Date().toISOString();
  return unito;
}

/* ============================================================
   ACCESSO — password condivisa e token firmato
============================================================ */

function confrontoSicuro(a, b){
  const x = Buffer.from(String(a));
  const y = Buffer.from(String(b));
  if(x.length !== y.length) return false;
  return crypto.timingSafeEqual(x, y);
}

export function creaToken(segreto, oreValidita = 24 * 14, ora = Date.now()){
  const scadenza = ora + oreValidita * 3600 * 1000;
  const firma = crypto.createHmac("sha256", segreto).update(String(scadenza)).digest("hex");
  return scadenza + "." + firma;
}

export function tokenValido(token, segreto, ora = Date.now()){
  if(!token || !segreto) return false;
  const parti = String(token).split(".");
  if(parti.length !== 2) return false;
  const [scadenza, firma] = parti;
  if(!/^\d+$/.test(scadenza) || Number(scadenza) < ora) return false;
  const atteso = crypto.createHmac("sha256", segreto).update(scadenza).digest("hex");
  return confrontoSicuro(firma, atteso);
}

export function passwordCorretta(inserita, attesa){
  if(!attesa) return false;
  return confrontoSicuro(String(inserita || "").padEnd(64, "\0").slice(0, 64),
                         String(attesa).padEnd(64, "\0").slice(0, 64));
}

/* ============================================================
   EMAIL DI RIEPILOGO
   Costruita qui, sul server, così arriva sempre completa anche
   se la candidatura entra da un canale diverso dalla landing.
============================================================ */

export function tracciaChiamata(d){
  const punti = ["Confermare la fascia di visita e i dati di contatto"];
  if(d.interesse === "Investimento / rendita")          punti.push("Portare i numeri: rendita, zona, potenziale di rivalutazione");
  else if(d.interesse === "Frazionamento in due unità") punti.push("Presentare il progetto di frazionamento già disponibile");
  else if(d.interesse === "Comprare per abitarci")      punti.push("Puntare su parco privato, 11 camere e servizi della zona");
  else if(d.interesse === "Scoprire il nuovo prezzo")   punti.push("Spiegare che il prezzo si scopre solo dopo la visita, venerdì");
  if(d.finanziamento === "Mutuo" || d.finanziamento === "Mutuo + liquidità")
    punti.push("Proporre la consulenza mutuo disponibile in villa");
  punti.push("Ricordare le 4 tappe e l'apertura della piattaforma di venerdì");
  return punti.map((p, i) => (i + 1) + ") " + p).join("  ");
}

export function costruisciEmail(c, attivita, indirizzoGestione){
  const fmt = d => new Date(d).toLocaleString("it-IT", {
    weekday:"long", day:"2-digit", month:"long", hour:"2-digit", minute:"2-digit", timeZone:"Europe/Rome"
  });
  const wa = numeroWa(c.telefono);
  const campagna = [c.origine?.utm_source, c.origine?.utm_medium, c.origine?.utm_campaign, c.origine?.utm_content]
    .filter(Boolean).join(" · ");

  return {
    _subject:  `🔔 Nuova lead Innova Experience — ${c.nome}${c.telefono ? " — " + c.telefono : ""}`,
    _template: "table",
    _captcha:  "false",

    "Nome e cognome":             c.nome,
    "Telefono":                   c.telefono || "non lasciato",
    "Email":                      c.email    || "non lasciata",
    "A cosa è interessata":       c.interesse     || "non indicato",
    "Come intende acquistare":    c.finanziamento || "non indicato",
    "Fascia di visita richiesta": c.slot          || "nessuna preferenza",
    "Cosa ha scritto":            c.note          || "—",
    "Immobile":                   c.evento,
    "Candidatura ricevuta il":    fmt(c.creato),
    "Da richiamare entro":        attivita ? fmt(attivita.scadenza) : "—",
    "Provenienza campagna":       campagna || "diretta / non tracciata",
    "Traccia per la chiamata":    tracciaChiamata(c),
    "▶ Chiama ora":               c.telefono ? "tel:" + c.telefono.replace(/\s/g, "") : "—",
    "▶ Scrivi su WhatsApp":       wa ? "https://wa.me/" + wa : "—",
    "▶ Apri nella piattaforma":   indirizzoGestione || "—",

    _honey: ""
  };
}
