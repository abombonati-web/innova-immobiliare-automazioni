import { test } from "node:test";
import assert from "node:assert/strict";
import { creaGestore } from "../netlify/functions/rotte.mjs";
import { creaToken } from "../netlify/functions/nucleo.mjs";

const ENV = {
  INNOVA_PASSWORD: "Villa2026!",
  INNOVA_SEGRETO: "segreto-lungo-e-casuale-per-i-token",
  INNOVA_EMAIL: "info@innovaimmobiliare.it"
};

/* Piattaforma finta: archivio in memoria ed email registrate */
function piattaforma(env = ENV){
  let archivio = null;
  const email = [];
  const gestore = creaGestore({
    leggi:  async () => archivio,
    scrivi: async (a) => { archivio = JSON.parse(JSON.stringify(a)); },
    inviaEmail: async (corpo, casella) => { email.push({ corpo, casella }); return true; },
    env
  });
  return {
    email,
    archivio: () => archivio,
    chiama: (percorso, opzioni = {}) => gestore(new Request("https://innovaexperience.it/api/" + percorso, opzioni)),
    post: (percorso, corpo, token) => gestore(new Request("https://innovaexperience.it/api/" + percorso, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...(token ? { Authorization: "Bearer " + token } : {}) },
      body: JSON.stringify(corpo)
    })),
    token: () => creaToken(env.INNOVA_SEGRETO)
  };
}

const LEAD = {
  nome: "Maria Rossi", telefono: "+39 333 1234567", email: "maria@example.it",
  interesse: "Investimento / rendita", finanziamento: "Mutuo",
  slot: "Mercoledì 22 · mattina", note: "Chiamatemi dopo le 18",
  utm_source: "meta", utm_campaign: "villa-luglio"
};

/* ============================================================
   UNA CANDIDATURA ENTRA DA SOLA
============================================================ */
test("la candidatura crea contatto e attività fissa senza che nessuno intervenga", async () => {
  const p = piattaforma();
  const r = await p.post("lead", LEAD);
  assert.equal(r.status, 200);

  const corpo = await r.json();
  assert.equal(corpo.ok, true);
  assert.equal(corpo.giaPresente, false);
  assert.equal(corpo.emailInviata, true);

  const a = p.archivio();
  assert.equal(a.contatti.length, 1);
  assert.equal(a.attivita.length, 1);
  assert.equal(a.contatti[0].nome, "Maria Rossi");
  assert.equal(a.contatti[0].stato, "nuovo");
  assert.equal(a.contatti[0].origine.utm_campaign, "villa-luglio");
  assert.equal(a.attivita[0].automatica, true);
  assert.equal(a.attivita[0].contattoId, a.contatti[0].id);
  assert.equal(a.attivita[0].stato, "aperta");
});

test("l'email di riepilogo parte con i link per chiamare e per aprire la scheda", async () => {
  const p = piattaforma();
  await p.post("lead", LEAD);

  assert.equal(p.email.length, 1);
  assert.equal(p.email[0].casella, "info@innovaimmobiliare.it");
  const e = p.email[0].corpo;
  assert.match(e._subject, /Maria Rossi/);
  assert.equal(e["▶ Chiama ora"], "tel:+393331234567");
  assert.match(e["▶ Apri nella piattaforma"], /gestione\.html#contatto=c_/);
  assert.equal(e["A cosa è interessata"], "Investimento / rendita");
});

test("se l'email non parte la lead resta comunque in archivio", async () => {
  let archivio = null;
  const gestore = creaGestore({
    leggi:  async () => archivio,
    scrivi: async (a) => { archivio = a; },
    inviaEmail: async () => { throw new Error("servizio email irraggiungibile"); },
    env: ENV
  });
  const r = await gestore(new Request("https://x.it/api/lead", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(LEAD)
  }));

  assert.equal(r.status, 200);
  assert.equal((await r.json()).emailInviata, false);
  assert.equal(archivio.contatti.length, 1, "la candidatura non va persa");
});

test("chi ricandida non diventa un doppione, ma ottiene un nuovo richiamo", async () => {
  const p = piattaforma();
  await p.post("lead", LEAD);
  const r = await p.post("lead", { ...LEAD, telefono: "", note: "Ho cambiato idea sulla fascia" });

  assert.equal((await r.json()).giaPresente, true);
  const a = p.archivio();
  assert.equal(a.contatti.length, 1, "un solo contatto");
  assert.equal(a.attivita.length, 2, "ma due richiami in agenda");
  assert.match(a.contatti[0].note, /Chiamatemi dopo le 18/);
  assert.match(a.contatti[0].note, /Ho cambiato idea/);
});

test("lo spam viene scartato senza sporcare l'archivio", async () => {
  const p = piattaforma();
  const r = await p.post("lead", { ...LEAD, _honey: "bot" });
  assert.equal(r.status, 200);
  assert.equal(p.archivio(), null);
});

test("una candidatura senza alcun recapito viene rifiutata", async () => {
  const p = piattaforma();
  const r = await p.post("lead", { note: "solo una nota" });
  assert.equal(r.status, 400);
  assert.equal(p.archivio(), null);
});

/* ============================================================
   ACCESSO
============================================================ */
test("con la password giusta si ottiene un token valido", async () => {
  const p = piattaforma();
  const r = await p.post("accesso", { password: "Villa2026!" });
  assert.equal(r.status, 200);

  const { token } = await r.json();
  const archivio = await p.chiama("archivio", { headers: { Authorization: "Bearer " + token } });
  assert.equal(archivio.status, 200);
});

test("password errata e assente vengono respinte", async () => {
  const p = piattaforma();
  assert.equal((await p.post("accesso", { password: "sbagliata" })).status, 401);
  assert.equal((await p.post("accesso", {})).status, 401);
});

test("senza configurazione la piattaforma lo dice invece di lasciare entrare", async () => {
  const p = piattaforma({});
  const r = await p.post("accesso", { password: "qualsiasi" });
  assert.equal(r.status, 503);
  assert.match((await r.json()).errore, /non è ancora configurata/);
});

test("l'archivio non si legge né si scrive senza un accesso valido", async () => {
  const p = piattaforma();
  assert.equal((await p.chiama("archivio")).status, 401, "lettura senza token");
  assert.equal((await p.chiama("archivio", { headers: { Authorization: "Bearer falso.00" } })).status, 401);
  assert.equal((await p.post("sincronizza", { contatti: [] })).status, 401, "scrittura senza token");
});

test("la candidatura resta pubblica: non serve alcun accesso", async () => {
  const p = piattaforma();
  assert.equal((await p.post("lead", LEAD)).status, 200);
});

/* ============================================================
   SINCRONIZZAZIONE
============================================================ */
test("le modifiche fatte in gestione arrivano in archivio", async () => {
  const p = piattaforma();
  await p.post("lead", LEAD);
  const contatto = p.archivio().contatti[0];

  const r = await p.post("sincronizza", {
    contatti: [{ ...contatto, stato: "visita_confermata", aggiornato: new Date(Date.now() + 1000).toISOString() }],
    attivita: []
  }, p.token());

  assert.equal(r.status, 200);
  const unito = await r.json();
  assert.equal(unito.contatti[0].stato, "visita_confermata");
  assert.equal(p.archivio().contatti[0].stato, "visita_confermata");
});

test("una modifica vecchia non sovrascrive una più recente fatta altrove", async () => {
  const p = piattaforma();
  await p.post("lead", LEAD);
  const contatto = p.archivio().contatti[0];

  /* Dispositivo A, appena aggiornato */
  await p.post("sincronizza", {
    contatti: [{ ...contatto, stato: "visitato", aggiornato: new Date(Date.now() + 5000).toISOString() }]
  }, p.token());

  /* Dispositivo B, rimasto indietro */
  await p.post("sincronizza", {
    contatti: [{ ...contatto, stato: "nuovo", aggiornato: new Date(Date.now() - 5000).toISOString() }]
  }, p.token());

  assert.equal(p.archivio().contatti[0].stato, "visitato");
});

test("una lead arrivata mentre si era offline non viene cancellata dalla sincronizzazione", async () => {
  const p = piattaforma();
  await p.post("lead", LEAD);
  const primo = p.archivio().contatti[0];

  /* Arriva una seconda candidatura mentre la gestione è scollegata */
  await p.post("lead", { nome: "Luca Bianchi", telefono: "0916543210" });
  assert.equal(p.archivio().contatti.length, 2);

  /* La gestione invia la propria copia, che il secondo contatto non ce l'ha */
  const r = await p.post("sincronizza", { contatti: [primo], attivita: [] }, p.token());
  const unito = await r.json();

  assert.equal(unito.contatti.length, 2, "il contatto arrivato nel frattempo resta");
  assert.ok(unito.contatti.some(c => c.nome === "Luca Bianchi"));
});

test("la cancellazione fatta in gestione si propaga all'archivio", async () => {
  const p = piattaforma();
  await p.post("lead", LEAD);
  const contatto = p.archivio().contatti[0];

  await p.post("sincronizza", {
    contatti: [{ ...contatto, eliminato: true, aggiornato: new Date(Date.now() + 1000).toISOString() }]
  }, p.token());

  assert.equal(p.archivio().contatti[0].eliminato, true);
});

test("le impostazioni dell'attività fissa si aggiornano per tutti", async () => {
  const p = piattaforma();
  await p.post("lead", LEAD);

  await p.post("sincronizza", {
    attivitaFissa: { titolo: "Richiamare entro 4 ore", tipo: "chiamata", scadenzaOre: 4, checklist: [], aggiornato: new Date().toISOString() }
  }, p.token());

  await p.post("lead", { nome: "Luca Bianchi", telefono: "0916543210" });
  const ultima = p.archivio().attivita[0];
  assert.equal(ultima.titolo, "Richiamare entro 4 ore");

  const ore = (new Date(ultima.scadenza) - new Date(p.archivio().contatti[0].creato)) / 3600000;
  assert.ok(Math.abs(ore - 4) < 0.01, "la scadenza segue le nuove impostazioni");
});

/* ============================================================
   ROBUSTEZZA
============================================================ */
test("una rotta inesistente risponde 404", async () => {
  const p = piattaforma();
  assert.equal((await p.chiama("inesistente")).status, 404);
});

test("un corpo non leggibile non manda in errore la piattaforma", async () => {
  const p = piattaforma();
  const r = await p.chiama("lead", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: "{non json"
  });
  assert.equal(r.status, 400, "trattata come candidatura vuota");
});

test("un guasto dell'archivio viene riportato come errore della piattaforma", async () => {
  const gestore = creaGestore({
    leggi:  async () => { throw new Error("archivio irraggiungibile"); },
    scrivi: async () => {},
    inviaEmail: async () => true,
    env: ENV
  });
  const r = await gestore(new Request("https://x.it/api/lead", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(LEAD)
  }));
  assert.equal(r.status, 500);
  assert.match((await r.json()).errore, /archivio irraggiungibile/);
});
