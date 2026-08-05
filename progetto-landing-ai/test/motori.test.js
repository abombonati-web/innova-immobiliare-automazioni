/* ============================================================
   Test dei motori: semaforo, intento, calcoli economici,
   orchestratore delle comunicazioni e generazione slot.

   Si esegue con:   node --test progetto-landing-ai/test/
   (Node 18 o superiore, nessuna dipendenza da installare)
   ============================================================ */

import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

import { valutaSemaforo, applicaEsitoConsulente, valutaCondizione } from "../demo/js/motore-semaforo.js";
import { rilevaIntento, intentoAffidabile } from "../demo/js/rilevamento-intento.js";
import { calcolaProvvigione, calcolaPassaggiVendita, calcolaImportiAffitto, valoreCatastale } from "../demo/js/calcoli.js";
import { pianificaSequenza, offsetInMs, compila, rispettaFasciaOraria, sequenzePerContatto, filtraSequenzeAmmesse } from "../demo/js/orchestratore.js";
import { generaSlot, luoghiDisponibili } from "../demo/js/prenotazione.js";

const radice = join(dirname(fileURLToPath(import.meta.url)), "..");
const leggi = (percorso) => JSON.parse(readFileSync(join(radice, percorso), "utf8"));

const regole = leggi("config/regole-semaforo.json");
const provvigioni = leggi("config/provvigioni.json");
const costi = leggi("config/costi-passaggi.json");
const comunicazioni = leggi("config/comunicazioni.json");
const servizi = leggi("config/servizi.json");
const agenzia = leggi("data/agenzia.json");
const villa = leggi("data/immobili/villa-citta-giardino.json");
const trilocale = leggi("data/immobili/trilocale-via-siracusa.json");

/* ============================================================
   SEMAFORO
   ============================================================ */

test("contanti: via libera immediata alla prenotazione", () => {
  const esito = valutaSemaforo(
    { intento: "acquirente", modalita_acquisto: "contanti", budget_massimo: 750000 },
    villa,
    regole
  );
  assert.equal(esito.esito, "verde");
  assert.equal(esito.prenotazione_sbloccata, true);
  assert.ok(esito.azioni.includes("sblocca_prenotazione"));
});

test("mutuo deliberato: equivale al contante", () => {
  const esito = valutaSemaforo(
    { intento: "acquirente", modalita_acquisto: "mutuo_deliberato", budget_massimo: 700000 },
    villa,
    regole
  );
  assert.equal(esito.esito, "verde");
  assert.ok(esito.azioni.includes("richiedi_copia_delibera"));
});

test("mutuo da richiedere: prenotazione bloccata e consulente avvisato", () => {
  const esito = valutaSemaforo(
    { intento: "acquirente", modalita_acquisto: "mutuo_da_richiedere", budget_massimo: 700000 },
    villa,
    regole
  );
  assert.equal(esito.esito, "giallo");
  assert.equal(esito.prenotazione_sbloccata, false);
  assert.ok(esito.azioni.includes("notifica_consulente_finanziario"));
});

test("situazione poco chiara: giallo, non rifiuto", () => {
  const esito = valutaSemaforo(
    { intento: "acquirente", modalita_acquisto: "non_so" },
    villa,
    regole
  );
  assert.equal(esito.esito, "giallo");
  assert.equal(esito.revisione_umana.disponibile, true);
});

test("budget molto distante dal prezzo: rosso, ma con persona e alternative", () => {
  const esito = valutaSemaforo(
    { intento: "acquirente", modalita_acquisto: "contanti", budget_massimo: 200000 },
    villa,
    regole
  );
  assert.equal(esito.esito, "rosso");
  assert.equal(esito.prenotazione_sbloccata, false);
  assert.ok(esito.azioni.includes("proponi_immobili_alternativi"));
});

test("il budget alto non fa scattare il rosso", () => {
  const esito = valutaSemaforo(
    { intento: "acquirente", modalita_acquisto: "contanti", budget_massimo: 700000 },
    villa,
    regole
  );
  assert.equal(esito.esito, "verde");
});

test("modalità mancante: giallo per dati incompleti, mai verde", () => {
  const esito = valutaSemaforo({ intento: "acquirente" }, villa, regole);
  assert.equal(esito.esito, "giallo");
  assert.equal(esito.regola_applicata, "dati-incompleti");
});

test("affitto sostenibile: verde con documenti richiesti", () => {
  const esito = valutaSemaforo(
    { intento: "affittuario", modalita_acquisto: "contanti", reddito_mensile_netto: 2600 },
    trilocale,
    regole
  );
  assert.equal(esito.esito, "verde");
  assert.ok(esito.contesto_valutato.incidenza_canone_reddito < 0.4);
});

test("affitto con canone troppo pesante: verifica prima di prenotare", () => {
  const esito = valutaSemaforo(
    { intento: "affittuario", modalita_acquisto: "contanti", reddito_mensile_netto: 1500 },
    trilocale,
    regole
  );
  assert.equal(esito.esito, "giallo");
  assert.ok(esito.azioni.includes("valuta_garante"));
});

test("venditore: nessun semaforo finanziario, si va alla valutazione", () => {
  const esito = valutaSemaforo({ intento: "venditore" }, null, regole);
  assert.equal(esito.esito, "verde");
  assert.ok(esito.azioni.includes("avvia_pipeline_valutazione"));
});

test("l'esito del consulente è l'unico modo di sbloccare un giallo", () => {
  const giallo = valutaSemaforo(
    { intento: "acquirente", modalita_acquisto: "mutuo_da_richiedere" },
    villa,
    regole
  );
  const approvato = applicaEsitoConsulente(giallo, { approvato: true, operatore: "consulente.test" });
  assert.equal(approvato.prenotazione_sbloccata, true);
  assert.equal(approvato.revisione_effettuata.operatore, "consulente.test");

  const respinto = applicaEsitoConsulente(giallo, { approvato: false, operatore: "consulente.test" });
  assert.equal(respinto.prenotazione_sbloccata, false);
  assert.equal(respinto.esito, "giallo");
});

test("ogni esito espone sempre la revisione umana (GDPR art. 22)", () => {
  const casi = [
    { modalita_acquisto: "contanti" },
    { modalita_acquisto: "mutuo_da_richiedere" },
    { modalita_acquisto: "contanti", budget_massimo: 100000 }
  ];
  for (const risposte of casi) {
    const esito = valutaSemaforo({ intento: "acquirente", ...risposte }, villa, regole);
    assert.equal(esito.revisione_umana.disponibile, true);
    assert.ok(esito.revisione_umana.canali.length > 0);
  }
});

test("una configurazione senza fallback non produce mai un verde per sbaglio", () => {
  const regoleMonche = { ...regole, regole: [] };
  const esito = valutaSemaforo({ intento: "acquirente", modalita_acquisto: "contanti" }, villa, regoleMonche);
  assert.equal(esito.esito, "giallo");
});

test("operatore sconosciuto: errore esplicito, non silenzio", () => {
  assert.throws(
    () => valutaCondizione({ campo: "x", operatore: "quasi_uguale", valore: 1 }, { x: 1 }),
    /Operatore non riconosciuto/
  );
});

/* ============================================================
   INTENTO
   ============================================================ */

test("la risposta del modulo vince su tutto il resto", () => {
  const r = rilevaIntento({
    rispostaModulo: "venditore",
    tipoOperazione: "vendita",
    testoChat: "cerco casa in affitto per la mia famiglia"
  });
  assert.equal(r.intento, "venditore");
  assert.equal(r.fonte, "modulo");
  assert.ok(intentoAffidabile(r));
});

test("il nome della campagna basta a riconoscere un venditore", () => {
  const r = rilevaIntento({ campagna: "vendere-casa-palermo-2026", tipoOperazione: "vendita" });
  assert.equal(r.intento, "venditore");
});

test("le parole della chat riconoscono l'investitore", () => {
  const r = rilevaIntento({
    testoChat: "cerco un immobile da mettere a reddito, mi interessa il rendimento e il frazionamento",
    tipoOperazione: "vendita"
  });
  assert.equal(r.intento, "investitore");
});

test("gli accenti non cambiano il riconoscimento", () => {
  const r = rilevaIntento({ testoChat: "ho una casa ereditata con una successione da chiudere" });
  assert.equal(r.intento, "venditore");
});

test("senza segnali non si indovina: confidenza zero e si chiede al cliente", () => {
  const r = rilevaIntento({});
  assert.equal(r.confidenza, 0);
  assert.equal(intentoAffidabile(r), false);
});

test("una landing di un affitto suggerisce l'affittuario", () => {
  const r = rilevaIntento({ tipoOperazione: "affitto" });
  assert.equal(r.intento, "affittuario");
});

/* ============================================================
   CALCOLI ECONOMICI
   ============================================================ */

test("provvigione sopra i 100.000: 5% + IVA", () => {
  const p = calcolaProvvigione(villa, provvigioni);
  assert.equal(p.imponibile, 36000);              // 5% di 720.000
  assert.equal(Math.round(p.iva), 7920);          // IVA 22%
  assert.equal(Math.round(p.totale), 43920);
});

test("provvigione sotto i 100.000: quota fissa di 5.000 + IVA", () => {
  const economico = JSON.parse(JSON.stringify(villa));
  economico.pubblico.prezzo = 85000;
  const p = calcolaProvvigione(economico, provvigioni);
  assert.equal(p.imponibile, 5000);
  assert.equal(Math.round(p.totale), 6100);
});

test("provvigione affitto: 15% del canone annuale + IVA", () => {
  const p = calcolaProvvigione(trilocale, provvigioni);
  assert.equal(p.imponibile, 850 * 12 * 0.15);    // 1.530
  assert.equal(Math.round(p.totale), 1867);
});

test("il valore catastale prima casa è più basso della seconda casa", () => {
  const prima = valoreCatastale(villa.pubblico.rendita_catastale, true, costi);
  const seconda = valoreCatastale(villa.pubblico.rendita_catastale, false, costi);
  assert.ok(prima < seconda);
  assert.equal(Math.round(prima), Math.round(2480.55 * 115.5));
});

test("i tre passaggi dell'acquisto ci sono tutti e hanno importi calcolati", () => {
  const c = calcolaPassaggiVendita(villa, costi, provvigioni, { primaCasa: true });
  assert.equal(c.passaggi.length, 3);
  assert.deepEqual(c.passaggi.map((p) => p.id), ["proposta", "preliminare", "rogito"]);
  for (const passaggio of c.passaggi) {
    for (const voce of passaggio.voci) {
      assert.notEqual(voce.importo, null, `voce senza importo: ${voce.id}`);
    }
  }
});

test("la caparra al preliminare è al netto del deposito già versato", () => {
  const c = calcolaPassaggiVendita(villa, costi, provvigioni);
  const deposito = c.passaggi[0].voci.find((v) => v.id === "deposito").importo;
  const caparra = c.passaggi[1].voci.find((v) => v.id === "caparra").importo;
  assert.equal(deposito, 720000 * 0.02);
  assert.equal(caparra, 720000 * 0.1 - deposito);
});

test("il saldo del prezzo non viene contato fra le spese", () => {
  const c = calcolaPassaggiVendita(villa, costi, provvigioni);
  const rogito = c.passaggi[2];
  const saldo = rogito.voci.find((v) => v.id === "saldo").importo;
  assert.ok(saldo > 600000);
  assert.ok(rogito.totale_spese < 100000, "il saldo è finito nel totale delle spese");
});

test("l'imposta di registro prima casa è il 2% del valore catastale, con minimo 1.000", () => {
  const c = calcolaPassaggiVendita(villa, costi, provvigioni, { primaCasa: true });
  const registro = c.passaggi[2].voci.find((v) => v.id === "imposta_registro").importo;
  const atteso = Math.max(2480.55 * 115.5 * 0.02, 1000);
  assert.equal(Math.round(registro), Math.round(atteso));
});

test("seconda casa: imposta di registro più alta", () => {
  const prima = calcolaPassaggiVendita(villa, costi, provvigioni, { primaCasa: true });
  const seconda = calcolaPassaggiVendita(villa, costi, provvigioni, { primaCasa: false });
  const r1 = prima.passaggi[2].voci.find((v) => v.id === "imposta_registro").importo;
  const r2 = seconda.passaggi[2].voci.find((v) => v.id === "imposta_registro").importo;
  assert.ok(r2 > r1 * 4);
});

test("affitto: con la cedolare secca l'imposta di registro non è dovuta", () => {
  const c = calcolaImportiAffitto(trilocale, costi, provvigioni);
  assert.equal(c.cedolare_secca, true);
  const registrazione = c.alla_firma.find((v) => v.id === "registrazione");
  assert.equal(registrazione.importo, 0);
  assert.match(registrazione.dettaglio, /cedolare secca/);
});

test("affitto: senza cedolare secca l'imposta compare", () => {
  const senzaCedolare = JSON.parse(JSON.stringify(trilocale));
  senzaCedolare.pubblico.tipo_contratto = "4+4 ordinario";
  const c = calcolaImportiAffitto(senzaCedolare, costi, provvigioni);
  assert.ok(c.alla_firma.find((v) => v.id === "registrazione").importo > 0);
});

test("affitto: il totale alla firma somma cauzione, prima mensilità e provvigione", () => {
  const c = calcolaImportiAffitto(trilocale, costi, provvigioni);
  const atteso = 850 * 3 + 850 + calcolaProvvigione(trilocale, provvigioni).totale;
  assert.equal(Math.round(c.totale_firma), Math.round(atteso));
});

/* ============================================================
   ORCHESTRATORE DELLE COMUNICAZIONI
   ============================================================ */

test("gli offset si leggono in minuti, ore e giorni", () => {
  assert.equal(offsetInMs("15m"), 900_000);
  assert.equal(offsetInMs("24h"), 86_400_000);
  assert.equal(offsetInMs("3g"), 259_200_000);
  assert.equal(offsetInMs("-24h"), -86_400_000);
  assert.equal(offsetInMs("immediato"), 0);
  assert.throws(() => offsetInMs("domani"), /Offset non valido/);
});

test("i segnaposto vengono compilati con i dati del contatto", () => {
  const testo = compila("Ciao {{contatto.nome}}, {{immobile.titolo}} ti aspetta", {
    contatto: { nome: "Marco" },
    immobile: { titolo: "la villa" }
  });
  assert.equal(testo, "Ciao Marco, la villa ti aspetta");
});

test("un segnaposto senza dato resta visibile invece di stampare 'undefined'", () => {
  const testo = compila("Ciao {{contatto.nome}}", {});
  assert.match(testo, /\{\{contatto\.nome\}\}/);
});

test("il follow-up ha tre messaggi a 24 ore, 3 giorni e 7 giorni", () => {
  const partenza = new Date("2026-09-07T10:00:00+02:00"); // lunedì mattina
  const piano = pianificaSequenza(
    "follow_up_lead",
    { contatto: { nome: "Marco" }, immobile: { titolo: "la villa", zona: "Città Giardino" }, link: {} },
    comunicazioni,
    partenza
  );
  assert.equal(piano.length, 3);
  const giorni = piano.map((m) => Math.round((new Date(m.invio_previsto) - partenza) / 86_400_000));
  assert.deepEqual(giorni, [1, 3, 7]);
});

test("nessun invio fuori dalla fascia oraria consentita", () => {
  const fascia = comunicazioni.fascia_oraria_invii;
  const notte = new Date("2026-09-08T03:20:00+02:00");
  const spostato = rispettaFasciaOraria(notte, fascia);
  assert.ok(spostato.getHours() >= 9 && spostato.getHours() <= 20);
});

test("nessun invio di domenica", () => {
  const fascia = comunicazioni.fascia_oraria_invii;
  const domenica = new Date("2026-09-13T11:00:00+02:00");
  assert.equal(domenica.getDay(), 0);
  const spostato = rispettaFasciaOraria(domenica, fascia);
  assert.notEqual(spostato.getDay(), 0);
});

test("il recupero del modulo abbandonato scatta dopo pochi minuti", () => {
  const partenza = new Date("2026-09-07T11:00:00+02:00");
  const piano = pianificaSequenza(
    "recupero_modulo_abbandonato",
    { contatto: { nome: "Marco" }, immobile: { titolo: "la villa" }, link: {} },
    comunicazioni,
    partenza
  );
  assert.equal(piano.length, 1);
  const minuti = (new Date(piano[0].invio_previsto) - partenza) / 60_000;
  assert.equal(minuti, 15);
});

test("il promemoria appuntamento si conta a ritroso dalla data della visita", () => {
  const prenotazione = { data_ora: "2026-09-18T10:00:00+02:00", luogo: "l'immobile" };
  const piano = pianificaSequenza(
    "appuntamento",
    { contatto: { nome: "Marco" }, immobile: { titolo: "la villa" }, prenotazione, link: {} },
    comunicazioni,
    new Date("2026-09-10T09:00:00+02:00")
  );
  const promemoria = piano.find((m) => m.id === "ap-promemoria");
  const visita = new Date(prenotazione.data_ora);
  assert.ok(new Date(promemoria.invio_previsto) < visita, "il promemoria deve precedere la visita");
  const orePrima = (visita - new Date(promemoria.invio_previsto)) / 3_600_000;
  assert.ok(orePrima >= 20 && orePrima <= 28, `promemoria a ${orePrima} ore dalla visita`);
});

test("una data di appuntamento non valida ferma la programmazione con un errore chiaro", () => {
  assert.throws(
    () =>
      pianificaSequenza(
        "appuntamento",
        {
          contatto: { nome: "Marco" },
          immobile: { titolo: "la villa" },
          // etichetta leggibile al posto della data ISO: l'errore tipico
          prenotazione: { data_ora: "lunedì 8 settembre, ore 09:30", luogo: "l'immobile" },
          link: {}
        },
        comunicazioni
      ),
    /non è una data valida/
  );
});

test("il mancato arrivo non chiude il contatto: due recuperi", () => {
  const piano = pianificaSequenza(
    "mancato_arrivo",
    { contatto: { nome: "Marco" }, immobile: { titolo: "la villa", zona: "Città Giardino" }, link: {} },
    comunicazioni
  );
  assert.equal(piano.length, 2);
  assert.equal(piano[1].azione_finale, "notifica_agente_per_chiamata");
});

test("il semaforo giallo avvisa cliente e consulente, con sollecito", () => {
  const piano = pianificaSequenza(
    "semaforo_giallo",
    { contatto: { nome: "Marco" }, immobile: { titolo: "la villa" }, semaforo: {}, risposte: {}, link: {} },
    comunicazioni
  );
  const destinatari = new Set(piano.map((m) => m.destinatario));
  assert.ok(destinatari.has("cliente"));
  assert.ok(destinatari.has("consulente_finanziario"));
  assert.equal(piano.find((m) => m.id === "sf-consulente").sla_ore, 4);
});

test("il venditore entra nella sua pipeline, non nel follow-up acquirenti", () => {
  const sequenze = sequenzePerContatto({ intento: "venditore", esitoSemaforo: "verde", moduloInviato: true });
  assert.deepEqual(sequenze, ["venditore"]);
});

test("un giallo attiva sia la sequenza del semaforo sia il follow-up", () => {
  const sequenze = sequenzePerContatto({ intento: "acquirente", esitoSemaforo: "giallo", moduloInviato: true });
  assert.deepEqual(sequenze, ["semaforo_giallo", "follow_up_lead"]);
});

test("i contatti in sovraindebitamento restano fuori dalle sequenze commerciali", () => {
  const ammesse = filtraSequenzeAmmesse(
    ["follow_up_lead", "semaforo_giallo"],
    ["sovraindebitamento"],
    servizi
  );
  assert.deepEqual(ammesse, ["semaforo_giallo"]);
});

/* ============================================================
   PRENOTAZIONE
   ============================================================ */

test("gli slot rispettano fasce, durata e anticipo minimo", () => {
  const adesso = new Date("2026-09-07T08:00:00+02:00");
  const slot = generaSlot(agenzia.prenotazione, [], { adesso, massimo: 20 });
  assert.ok(slot.length > 0);
  for (const s of slot) {
    const inizio = new Date(s.inizio);
    assert.ok(inizio - adesso >= 24 * 3_600_000 - 1000, "slot troppo ravvicinato");
    assert.notEqual(inizio.getDay(), 0, "slot di domenica");
    assert.equal(s.durata_minuti, agenzia.prenotazione.durata_slot_minuti);
  }
});

test("gli orari già occupati a calendario non vengono proposti", () => {
  const adesso = new Date("2026-09-07T08:00:00+02:00");
  const liberi = generaSlot(agenzia.prenotazione, [], { adesso, massimo: 30 });
  const primo = liberi[0];
  const conImpegno = generaSlot(
    agenzia.prenotazione,
    [{ inizio: primo.inizio, fine: primo.fine }],
    { adesso, massimo: 30 }
  );
  assert.ok(!conImpegno.some((s) => s.inizio === primo.inizio), "lo slot occupato è ancora proposto");
});

test("la sala visore non compare a chi non è prequalificato", () => {
  const senza = luoghiDisponibili(agenzia.prenotazione, { prequalificato: false, immobile: villa });
  assert.ok(!senza.some((l) => l.id === "ufficio_visore"));

  const con = luoghiDisponibili(agenzia.prenotazione, { prequalificato: true, immobile: villa });
  assert.ok(con.some((l) => l.id === "ufficio_visore"));
});

test("se l'immobile non ha il visore, il luogo non compare nemmeno ai prequalificati", () => {
  const luoghi = luoghiDisponibili(agenzia.prenotazione, { prequalificato: true, immobile: trilocale });
  assert.ok(!luoghi.some((l) => l.id === "ufficio_visore"));
});

/* ============================================================
   VISIBILITÀ DEI DATI
   ============================================================ */

test("ogni immobile tiene separati i dati pubblici da quelli riservati", () => {
  for (const immobile of [villa, trilocale]) {
    assert.ok(immobile.pubblico, "manca il nodo pubblico");
    assert.ok(immobile.riservato, "manca il nodo riservato");
    const chiaviPubbliche = Object.keys(immobile.pubblico);
    for (const vietata of ["mandato", "proprieta", "trattativa", "note_interne"]) {
      assert.ok(!chiaviPubbliche.includes(vietata), `"${vietata}" non deve stare nel nodo pubblico`);
    }
  }
});

test("il nodo riservato contiene tutto ciò che non va mostrato al cliente", () => {
  const riservato = villa.riservato;
  assert.ok("mandato" in riservato && "scadenza" in riservato.mandato);
  assert.ok("proprieta" in riservato);
  assert.ok("note_interne" in riservato.trattativa);
  assert.ok("margine_negoziazione_percentuale" in riservato.trattativa);
});
