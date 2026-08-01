import { test } from "node:test";
import assert from "node:assert/strict";
import {
  numeroWa, trovaDuplicato, nuovoContatto, nuovaAttivitaFissa, contestoLead,
  fondi, fondiArchivio, creaToken, tokenValido, passwordCorretta,
  costruisciEmail, ATTIVITA_FISSA
} from "../netlify/functions/nucleo.mjs";

/* ============================================================
   NUMERI DI TELEFONO
============================================================ */
test("il numero viene portato in formato internazionale", () => {
  assert.equal(numeroWa("+39 333 1234567"), "393331234567");
  assert.equal(numeroWa("3331234567"),      "393331234567");
  assert.equal(numeroWa("0039 333 1234567"),"393331234567");
  assert.equal(numeroWa("091 6543210"),     "390916543210", "il prefisso fisso mantiene lo zero");
  assert.equal(numeroWa(""),                "");
  assert.equal(numeroWa(null),              "");
});

/* ============================================================
   RICONOSCIMENTO DEI DOPPIONI
============================================================ */
test("basta l'email oppure il telefono per riconoscere la stessa persona", () => {
  const contatti = [nuovoContatto({ nome:"Maria Rossi", telefono:"+39 333 1234567", email:"maria@example.it" })];

  assert.ok(trovaDuplicato(contatti, { email:"MARIA@example.it" }),      "email uguale, maiuscole diverse");
  assert.ok(trovaDuplicato(contatti, { telefono:"3331234567" }),         "telefono scritto in altro modo");
  assert.ok(trovaDuplicato(contatti, { email:"altra@example.it", telefono:"3331234567" }), "basta il telefono");
  assert.equal(trovaDuplicato(contatti, { email:"altra@example.it", telefono:"3339999999" }), null);
  assert.equal(trovaDuplicato(contatti, {}), null, "senza recapiti non si conclude nulla");
});

test("un contatto cancellato non blocca la creazione di uno nuovo", () => {
  const c = nuovoContatto({ nome:"Maria", email:"maria@example.it" });
  c.eliminato = true;
  assert.equal(trovaDuplicato([c], { email:"maria@example.it" }), null);
});

/* ============================================================
   CONTATTI E ATTIVITÀ FISSA
============================================================ */
test("il contatto nasce con i valori attesi", () => {
  const c = nuovoContatto({ nome:"  Luca Bianchi ", telefono:" 091 654 3210 ", utm_source:"meta" });
  assert.equal(c.nome, "Luca Bianchi");
  assert.equal(c.telefono, "091 654 3210");
  assert.equal(c.stato, "nuovo");
  assert.equal(c.origine.utm_source, "meta");
  assert.ok(c.id.startsWith("c_"));
  assert.ok(c.creato && c.aggiornato);
});

test("senza nome il contatto non resta anonimo", () => {
  assert.equal(nuovoContatto({ telefono:"3331234567" }).nome, "Senza nome");
});

test("l'attività fissa scade dopo le ore configurate e porta la traccia della chiamata", () => {
  const creato = new Date("2026-07-15T10:00:00.000Z");
  const c = nuovoContatto({ nome:"Maria", interesse:"Investimento / rendita", slot:"Mer 22 mattina" }, creato);
  const a = nuovaAttivitaFissa(c, ATTIVITA_FISSA);

  assert.equal(a.stato, "aperta");
  assert.equal(a.automatica, true);
  assert.equal(a.contattoId, c.id);
  assert.equal(new Date(a.scadenza).toISOString(), "2026-07-16T10:00:00.000Z");
  assert.match(a.note, /Interesse: Investimento \/ rendita/);
  assert.match(a.note, /Fascia richiesta: Mer 22 mattina/);
  assert.match(a.note, /• Confermare la fascia di visita richiesta/);
});

test("la scadenza segue le impostazioni della piattaforma", () => {
  const creato = new Date("2026-07-15T10:00:00.000Z");
  const c = nuovoContatto({ nome:"Maria" }, creato);
  const a = nuovaAttivitaFissa(c, { ...ATTIVITA_FISSA, scadenzaOre: 4 });
  assert.equal(new Date(a.scadenza).toISOString(), "2026-07-15T14:00:00.000Z");
});

test("il contesto della lead riassume solo ciò che è stato dichiarato", () => {
  const c = nuovoContatto({ nome:"Maria", interesse:"Investimento / rendita" });
  const testo = contestoLead(c);
  assert.match(testo, /Interesse: Investimento/);
  assert.doesNotMatch(testo, /Fascia richiesta/);
  assert.doesNotMatch(testo, /Acquisto/);
});

/* ============================================================
   SINCRONIZZAZIONE
============================================================ */
test("fra due versioni della stessa scheda vince la più recente", () => {
  const vecchia = { id:"c1", nome:"Maria", aggiornato:"2026-07-15T10:00:00.000Z" };
  const nuova   = { id:"c1", nome:"Maria Rossi", aggiornato:"2026-07-15T12:00:00.000Z" };

  assert.equal(fondi([vecchia], [nuova])[0].nome, "Maria Rossi", "la più recente sostituisce");
  assert.equal(fondi([nuova], [vecchia])[0].nome, "Maria Rossi", "la più vecchia non sovrascrive");
});

test("le schede nuove si aggiungono senza toccare le altre", () => {
  const esistenti = [{ id:"c1", nome:"Maria", aggiornato:"2026-07-15T10:00:00.000Z" }];
  const unito = fondi(esistenti, [{ id:"c2", nome:"Luca", aggiornato:"2026-07-15T11:00:00.000Z" }]);
  assert.equal(unito.length, 2);
  assert.deepEqual(unito.map(c => c.nome).sort(), ["Luca", "Maria"]);
});

test("la cancellazione fatta su un dispositivo si propaga agli altri", () => {
  const presente  = { id:"c1", nome:"Maria", aggiornato:"2026-07-15T10:00:00.000Z" };
  const cancellato= { id:"c1", nome:"Maria", eliminato:true, aggiornato:"2026-07-15T12:00:00.000Z" };
  assert.equal(fondi([presente], [cancellato])[0].eliminato, true);
});

test("schede senza identificativo vengono ignorate", () => {
  assert.equal(fondi([], [{ nome:"senza id" }, null]).length, 0);
});

test("l'archivio unito incrementa la versione e conserva le impostazioni", () => {
  const base = { contatti:[], attivita:[], attivitaFissa:{ titolo:"Vecchio" }, versione: 3 };
  const unito = fondiArchivio(base, { contatti:[{ id:"c1", aggiornato:"2026-07-15T10:00:00.000Z" }] });
  assert.equal(unito.versione, 4);
  assert.equal(unito.contatti.length, 1);
  assert.equal(unito.attivitaFissa.titolo, "Vecchio");
});

test("le impostazioni aggiornate sostituiscono le precedenti", () => {
  const base = { contatti:[], attivita:[], attivitaFissa:{ titolo:"Vecchio", aggiornato:"2026-07-15T10:00:00.000Z" }, versione:1 };
  const unito = fondiArchivio(base, { attivitaFissa:{ titolo:"Nuovo", aggiornato:"2026-07-15T12:00:00.000Z" } });
  assert.equal(unito.attivitaFissa.titolo, "Nuovo");
});

test("un archivio inesistente non fa fallire la fusione", () => {
  const unito = fondiArchivio(null, { contatti:[{ id:"c1", aggiornato:"2026-07-15T10:00:00.000Z" }] });
  assert.equal(unito.contatti.length, 1);
  assert.equal(unito.versione, 1);
});

/* ============================================================
   ACCESSO
============================================================ */
test("il token firmato viene accettato solo con il segreto giusto", () => {
  const t = creaToken("segreto-lungo-e-casuale");
  assert.ok(tokenValido(t, "segreto-lungo-e-casuale"));
  assert.equal(tokenValido(t, "un-altro-segreto"), false);
});

test("il token scaduto non vale più", () => {
  const t = creaToken("segreto", 1, Date.now() - 2 * 3600 * 1000);
  assert.equal(tokenValido(t, "segreto"), false);
});

test("token manomessi o malformati vengono rifiutati", () => {
  const segreto = "segreto";
  const t = creaToken(segreto);
  const [scadenza, firma] = t.split(".");
  assert.equal(tokenValido(scadenza + ".00" + firma.slice(2), segreto), false, "firma alterata");
  assert.equal(tokenValido("9999999999999.abc", segreto), false, "firma corta");
  assert.equal(tokenValido("non-un-token", segreto), false);
  assert.equal(tokenValido("", segreto), false);
  assert.equal(tokenValido(t, ""), false, "senza segreto non si valida nulla");
});

test("senza password configurata nessuno entra", () => {
  assert.equal(passwordCorretta("qualsiasi", ""), false);
  assert.equal(passwordCorretta("", ""), false);
});

test("la password viene confrontata per intero", () => {
  assert.ok(passwordCorretta("Villa2026!", "Villa2026!"));
  assert.equal(passwordCorretta("Villa2026", "Villa2026!"), false, "prefisso corretto ma incompleto");
  assert.equal(passwordCorretta("villa2026!", "Villa2026!"), false, "maiuscole diverse");
});

/* ============================================================
   EMAIL DI RIEPILOGO
============================================================ */
test("l'email contiene tutto ciò che serve per chiamare", () => {
  const c = nuovoContatto({
    nome:"Maria Rossi", telefono:"+39 333 1234567", email:"maria@example.it",
    interesse:"Investimento / rendita", finanziamento:"Mutuo",
    slot:"Mercoledì 22 · mattina", note:"Chiamatemi dopo le 18",
    utm_source:"meta", utm_campaign:"villa-luglio"
  });
  const a = nuovaAttivitaFissa(c, ATTIVITA_FISSA);
  const email = costruisciEmail(c, a, "https://innovaexperience.it/gestione.html#contatto=" + c.id);

  assert.match(email._subject, /Maria Rossi/);
  assert.equal(email["A cosa è interessata"], "Investimento / rendita");
  assert.equal(email["Come intende acquistare"], "Mutuo");
  assert.equal(email["Cosa ha scritto"], "Chiamatemi dopo le 18");
  assert.equal(email["▶ Chiama ora"], "tel:+393331234567");
  assert.equal(email["▶ Scrivi su WhatsApp"], "https://wa.me/393331234567");
  assert.match(email["▶ Apri nella piattaforma"], new RegExp(c.id));
  assert.match(email["Provenienza campagna"], /meta · villa-luglio/);
  assert.match(email["Traccia per la chiamata"], /rendita, zona, potenziale/);
  assert.match(email["Traccia per la chiamata"], /consulenza mutuo/);
});

test("i campi non compilati non lasciano buchi nell'email", () => {
  const c = nuovoContatto({ nome:"Anonimo", telefono:"3331234567" });
  const email = costruisciEmail(c, nuovaAttivitaFissa(c, ATTIVITA_FISSA), "");
  assert.equal(email["Email"], "non lasciata");
  assert.equal(email["A cosa è interessata"], "non indicato");
  assert.equal(email["Fascia di visita richiesta"], "nessuna preferenza");
  assert.equal(email["Provenienza campagna"], "diretta / non tracciata");
});
