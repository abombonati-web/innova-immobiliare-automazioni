/* ============================================================
   GENERATORE DI LANDING
   ------------------------------------------------------------
   Costruisce l'intera pagina a partire da un solo file JSON di
   immobile. Nessun contenuto è scritto nell'HTML: cambiare
   immobile significa cambiare il parametro ?immobile=... e la
   pagina si riscrive da sola.

   Regola non negoziabile: il generatore legge SOLO immobile.pubblico.
   Il nodo `riservato` (mandato, proprietario, note di trattativa,
   margini) non entra mai nel DOM, nemmeno nascosto: quello che
   arriva al browser è pubblico per definizione.
   ============================================================ */

import { euro, calcolaProvvigione, calcolaPassaggiVendita, calcolaImportiAffitto } from "./calcoli.js";
import { rilevaIntento } from "./rilevamento-intento.js";
import { valutaSemaforo } from "./motore-semaforo.js";
import { generaSlot, luoghiDisponibili, caricaOccupati, preparaEventoCalendario, generaIcs } from "./prenotazione.js";
import { pianificaSequenza, sequenzePerContatto } from "./orchestratore.js";
import { inizializzaTracciamento, attivaConsenso, traccia, osservaAbbandonoModulo, riepilogoComportamento } from "./tracciamento.js";

/* ---------- Utilità ---------- */

const esc = (testo) =>
  String(testo ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

const nl2p = (testo) =>
  String(testo || "")
    .split(/\n\s*\n/)
    .map((p) => `<p>${esc(p.trim())}</p>`)
    .join("");

async function carica(percorso) {
  const risposta = await fetch(percorso);
  if (!risposta.ok) throw new Error(`Non riesco a leggere ${percorso} (${risposta.status})`);
  return risposta.json();
}

/* ---------- Stato della pagina ---------- */

const app = {
  immobile: null,
  agenzia: null,
  config: {},
  intento: null,
  valutazione: null,
  contatto: null,
  piano: []
};

/* ============================================================
   AVVIO
   ============================================================ */

export async function avvia() {
  const parametri = new URLSearchParams(location.search);
  const idImmobile = parametri.get("immobile") || "villa-citta-giardino";

  try {
    const [immobile, agenzia, regole, provvigioni, costi, comunicazioni, servizi, campi] =
      await Promise.all([
        carica(`../data/immobili/${idImmobile}.json`),
        carica("../data/agenzia.json"),
        carica("../config/regole-semaforo.json"),
        carica("../config/provvigioni.json"),
        carica("../config/costi-passaggi.json"),
        carica("../config/comunicazioni.json"),
        carica("../config/servizi.json"),
        carica("../config/modulo-campi.json")
      ]);

    app.immobile = immobile;
    app.agenzia = agenzia;
    app.config = { regole, provvigioni, costi, comunicazioni, servizi, campi };
  } catch (errore) {
    document.getElementById("landing").innerHTML =
      `<div class="container avviso-errore">
         <h1>Immobile non trovato</h1>
         <p>${esc(errore.message)}</p>
         <p>Apri la demo dall'<a href="./index.html">indice</a>, oppure servi la cartella con un server locale
         (<code>python3 -m http.server</code>): aprendo il file con doppio clic il browser blocca la lettura dei JSON.</p>
       </div>`;
    return;
  }

  app.intento = rilevaIntento({
    parametroUrl: parametri.get("intento"),
    campagna: parametri.get("utm_campaign") || parametri.get("utm_content"),
    testoChat: parametri.get("chat"),
    tipoOperazione: app.immobile.tipo_operazione,
    canale: parametri.get("utm_source")
  });

  disegna();
  inizializzaTracciamento({ immobile: app.immobile });
  collegaEventi();
}

/* ============================================================
   DISEGNO DELLA PAGINA
   ============================================================ */

function disegna() {
  const { immobile } = app;
  const vendita = immobile.tipo_operazione === "vendita";

  document.title = `${immobile.pubblico.titolo} — ${immobile.pubblico.zona} | Innova Immobiliare`;

  document.getElementById("landing").innerHTML = [
    sezioneHero(),
    sezioneCartaIdentita(),
    sezioneDescrizione(),
    sezioneGalleria(),
    sezioneVideo(),
    sezioneEsperienze(),
    sezioneModulo(),
    `<div id="area-esito"></div>`,
    vendita ? sezionePassaggiVendita() : sezioneAffitto(),
    sezioneProvvigioni(),
    sezioneServizi(),
    sezioneFooter()
  ].join("");
}

/* ---------- Hero ---------- */

function sezioneHero() {
  const p = app.immobile.pubblico;
  const vendita = app.immobile.tipo_operazione === "vendita";
  const prezzo = vendita
    ? `${euro(p.prezzo)}`
    : `${euro(p.canone_mensile)} <span class="al-mese">al mese</span>`;

  return `
  <header class="hero" data-sezione="hero">
    <div class="container">
      <span class="eyebrow">${esc(p.zona)} · ${vendita ? "In vendita" : "In affitto"}</span>
      <h1>${esc(p.titolo)}</h1>
      <p class="sub">${esc(p.sottotitolo || "")}</p>
      <div class="hero-prezzo">
        <span class="etichetta">${vendita ? "Prezzo richiesto" : "Canone"}</span>
        <span class="valore">${prezzo}</span>
      </div>
      <div class="hero-sintesi">
        <span><strong>${esc(p.superficie_mq)}</strong> mq</span>
        <span><strong>${esc(p.classe_energetica)}</strong> classe energetica</span>
        <span><strong>${esc(p.piani || "—")}</strong></span>
      </div>
      <div class="cta-row">
        <a class="btn" href="#accesso">Accedi alla scheda completa</a>
        <span class="hint">${esc(app.agenzia.club.promessa)}</span>
      </div>
    </div>
  </header>`;
}

/* ---------- Carta d'identità digitale ---------- */

function sezioneCartaIdentita() {
  const p = app.immobile.pubblico;
  const vendita = app.immobile.tipo_operazione === "vendita";

  const voci = [
    ["Zona", p.zona],
    ["Indirizzo", p.indirizzo],
    ["Anno di costruzione", p.anno_costruzione],
    ["Superficie", p.superficie_mq ? `${p.superficie_mq} mq` : null],
    ["Superficie esterna", p.superficie_esterna_mq ? `${p.superficie_esterna_mq} mq` : null],
    ["Composizione", p.composizione],
    ["Piani", p.piani],
    ["Classe energetica", p.classe_energetica],
    ["Riscaldamento", p.riscaldamento],
    ["Abitabilità", p.abitabilita],
    ["Categoria catastale", p.categoria_catastale],
    ["Rendita catastale", p.rendita_catastale ? euro(p.rendita_catastale, 2) : null],
    [vendita ? "Prezzo" : "Canone mensile", vendita ? euro(p.prezzo) : euro(p.canone_mensile)],
    vendita
      ? ["Spese condominiali", p.spese_condominiali_annue ? `${euro(p.spese_condominiali_annue)} l'anno` : null]
      : ["Spese condominiali", p.spese_condominiali_mensili ? `${euro(p.spese_condominiali_mensili)} al mese` : null],
    !vendita ? ["Tipo di contratto", p.tipo_contratto] : null,
    !vendita ? ["Arredamento", p.arredato] : null,
    !vendita ? ["Disponibile dal", p.disponibile_dal] : null
  ].filter((v) => v && v[1]);

  return `
  <section class="carta" data-sezione="carta-identita">
    <div class="container">
      <h2 class="titolo-sezione">La carta d'identità dell'immobile</h2>
      <p class="occhiello">Gli stessi dati che troveresti in agenzia, tutti insieme e senza doverli chiedere.</p>
      <dl class="griglia-dati">
        ${voci.map(([etichetta, valore]) => `
          <div class="dato">
            <dt>${esc(etichetta)}</dt>
            <dd>${esc(valore)}</dd>
          </div>`).join("")}
      </dl>
      <p class="nota-planimetria">
        ${app.immobile.pubblico.planimetria?.disponibile
          ? "📐 Planimetria e documentazione completa disponibili dopo l'accesso alla scheda riservata."
          : "Planimetria in preparazione."}
      </p>
    </div>
  </section>`;
}

/* ---------- Descrizione ---------- */

function sezioneDescrizione() {
  const p = app.immobile.pubblico;
  return `
  <section class="descrizione" data-sezione="descrizione">
    <div class="container stretto">
      <h2 class="titolo-sezione">Come si vive, qui</h2>
      <div class="testo-lungo">${nl2p(p.descrizione)}</div>
      ${p.punti_di_forza?.length ? `
        <ul class="punti-forza">
          ${p.punti_di_forza.map((punto) => `<li>${esc(punto)}</li>`).join("")}
        </ul>` : ""}
    </div>
  </section>`;
}

/* ---------- Galleria ---------- */

function sezioneGalleria() {
  const foto = app.immobile.pubblico.media?.foto || [];
  if (!foto.length) return "";
  return `
  <section class="galleria-sezione" data-sezione="galleria">
    <div class="container">
      <h2 class="titolo-sezione">Le immagini</h2>
      <div class="galleria">
        ${foto.map((url, i) => `
          <a href="${esc(url)}" target="_blank" rel="noopener" data-foto="${i}">
            <img src="${esc(url)}" loading="lazy" alt="${esc(app.immobile.pubblico.titolo)} — foto ${i + 1}">
          </a>`).join("")}
      </div>
    </div>
  </section>`;
}

/* ---------- Video ---------- */

function incorporaVideo(video) {
  if (video.piattaforma === "youtube" && video.id) {
    return `<iframe src="https://www.youtube-nocookie.com/embed/${esc(video.id)}"
              title="${esc(video.titolo)}" loading="lazy" allowfullscreen
              referrerpolicy="strict-origin-when-cross-origin"></iframe>`;
  }
  if (video.url) {
    return `<a class="video-mancante" href="${esc(video.url)}" target="_blank" rel="noopener">
              Guarda "${esc(video.titolo)}" sul canale originale</a>`;
  }
  return `<div class="video-mancante">Video "${esc(video.titolo)}" da collegare.</div>`;
}

function sezioneVideo() {
  const dellImmobile = app.immobile.pubblico.media?.video_immobile || [];
  const istituzionali = app.agenzia.video_istituzionali || [];
  if (!dellImmobile.length && !istituzionali.length) return "";

  const blocco = (titolo, elenco, chiave) => !elenco.length ? "" : `
    <h3 class="sotto-titolo">${esc(titolo)}</h3>
    <div class="video-griglia">
      ${elenco.map((v, i) => `
        <figure class="video" data-video="${esc(chiave)}-${i}" data-titolo="${esc(v.titolo)}">
          ${incorporaVideo(v)}
          <figcaption>${esc(v.titolo)}</figcaption>
        </figure>`).join("")}
    </div>`;

  return `
  <section class="video-sezione" data-sezione="video">
    <div class="container">
      <h2 class="titolo-sezione">Guarda, prima di venire</h2>
      <p class="occhiello">Gli stessi contenuti che pubblichiamo sui nostri canali, raccolti qui.</p>
      ${blocco("L'immobile", dellImmobile, "immobile")}
      ${blocco("Chi siamo e come lavoriamo", istituzionali, "istituzionale")}
    </div>
  </section>`;
}

/* ---------- I due percorsi di esperienza ---------- */

function sezioneEsperienze() {
  const media = app.immobile.pubblico.media || {};
  const tour = media.tour_virtuale || {};
  const visore = media.visore_in_ufficio || {};

  return `
  <section class="esperienze" data-sezione="esperienze">
    <div class="container">
      <h2 class="titolo-sezione">Due modi per visitarla</h2>
      <div class="due-percorsi">
        <article class="percorso">
          <span class="numero">01</span>
          <h3>Tour virtuale, subito</h3>
          <p>Cammini dentro l'immobile dal divano di casa tua, quando vuoi, quante volte vuoi. Nessun appuntamento, nessuna fretta.</p>
          <button class="btn btn-secondario" id="btn-tour" ${tour.url ? "" : "disabled"}>
            ${tour.url ? "Avvia il tour virtuale" : "Tour in preparazione"}
          </button>
          <span class="nota">${tour.url ? "Aperto a tutti, dopo l'accesso al club." : esc(tour.nota || "")}</span>
        </article>
        <article class="percorso ${visore.disponibile ? "" : "spento"}">
          <span class="numero">02</span>
          <h3>Il visore, nel nostro ufficio</h3>
          <p>${visore.disponibile
            ? `Ti sedi in ${esc(visore.luogo)} e la vivi in scala reale con il visore, con un nostro agente accanto per rispondere a tutto. ${visore.durata_minuti} minuti.`
            : "Per questo immobile la prova con il visore non è ancora disponibile."}</p>
          <button class="btn btn-secondario" id="btn-visore" ${visore.disponibile ? "" : "disabled"}>Prenota la prova con il visore</button>
          <span class="nota">🔒 Riservato ai clienti prequalificati: i posti in sala sono pochi e li teniamo per chi è pronto a decidere.</span>
        </article>
      </div>
    </div>
  </section>`;
}

/* ---------- Il modulo, presentato come accesso al club ---------- */

function campoScelta(id, definizione) {
  return `
    <div class="campo">
      <label for="${esc(id)}">${esc(definizione.etichetta)}${definizione.obbligatorio ? " *" : ""}</label>
      <select id="${esc(id)}" name="${esc(id)}" ${definizione.obbligatorio ? "required" : ""}>
        <option value="">Scegli…</option>
        ${definizione.opzioni.map((o) => `<option value="${esc(o.valore)}">${esc(o.etichetta)}</option>`).join("")}
      </select>
    </div>`;
}

function sezioneModulo() {
  const campi = app.config.campi.campi_canonici;
  const club = app.agenzia.club;
  const vendita = app.immobile.tipo_operazione === "vendita";
  const intentoPredefinito = app.intento.intento;

  return `
  <section class="accesso" id="accesso" data-sezione="modulo">
    <div class="container">
      <h2 class="titolo-sezione chiaro">${esc(club.nome)}</h2>
      <p class="occhiello chiaro">${esc(club.promessa)}</p>

      <div class="accesso-griglia">
        <ul class="vantaggi">
          ${club.vantaggi.map((v) => `<li>${esc(v)}</li>`).join("")}
        </ul>

        <form class="modulo" id="modulo-accesso" novalidate>
          <h3>Richiedi l'accesso</h3>
          <p class="modulo-sub">Trenta secondi. Servono a capire come aiutarti davvero, non a riempire un archivio.</p>

          ${campoScelta("intento", { ...campi.intento, opzioni: campi.intento.opzioni })}
          ${campoScelta("modalita_acquisto", campi.modalita_acquisto)}

          <div class="campo" id="campo-budget">
            <label for="budget_massimo">${esc(campi.budget_massimo.etichetta)}</label>
            <input type="number" inputmode="numeric" min="0" step="1000" id="budget_massimo" name="budget_massimo"
                   placeholder="${vendita ? "es. 650000" : "es. 900"}">
          </div>

          <div class="campo nascosto" id="campo-reddito">
            <label for="reddito_mensile_netto">${esc(campi.reddito_mensile_netto.etichetta)}</label>
            <input type="number" inputmode="numeric" min="0" step="100" id="reddito_mensile_netto" name="reddito_mensile_netto" placeholder="es. 2200">
          </div>

          ${campoScelta("tempistica", campi.tempistica)}

          <div class="campo">
            <label for="nome">${esc(campi.nome.etichetta)} *</label>
            <input type="text" id="nome" name="nome" required autocomplete="name">
          </div>
          <div class="campo">
            <label for="telefono">${esc(campi.telefono.etichetta)} *</label>
            <input type="tel" id="telefono" name="telefono" required autocomplete="tel" placeholder="+39 ...">
          </div>
          <div class="campo">
            <label for="email">${esc(campi.email.etichetta)} *</label>
            <input type="email" id="email" name="email" required autocomplete="email">
          </div>

          <label class="consenso">
            <input type="checkbox" id="consenso_privacy" name="consenso_privacy" required>
            <span>${esc(campi.consenso_privacy.etichetta)} *</span>
          </label>
          <label class="consenso">
            <input type="checkbox" id="consenso_marketing" name="consenso_marketing">
            <span>${esc(campi.consenso_marketing.etichetta)}</span>
          </label>

          <button class="btn" type="submit">Entra nel club</button>
          <p class="errore" id="errore-modulo" hidden></p>
          <p class="micro">Intento rilevato all'arrivo: <strong>${esc(intentoPredefinito)}</strong>
             (confidenza ${app.intento.confidenza}). Puoi correggerlo qui sopra: vince sempre quello che dici tu.</p>
        </form>
      </div>
    </div>
  </section>`;
}

/* ---------- Percorso vendita: i tre passaggi ---------- */

function sezionePassaggiVendita() {
  const calcolo = calcolaPassaggiVendita(
    app.immobile,
    app.config.costi,
    app.config.provvigioni,
    { primaCasa: true }
  );

  return `
  <section class="passaggi" data-sezione="passaggi-acquisto">
    <div class="container">
      <h2 class="titolo-sezione">Dall'offerta alle chiavi, in tre passaggi</h2>
      <p class="occhiello">Con i numeri davanti, calcolati su questo immobile. Stima con i requisiti prima casa.</p>

      <div class="passaggi-griglia">
        ${calcolo.passaggi.map((passaggio) => `
          <article class="passaggio">
            <span class="numero">Passaggio ${passaggio.numero}</span>
            <h3>${esc(passaggio.titolo)}</h3>
            <p class="cosa-succede">${esc(passaggio.cosa_succede)}</p>
            <ul class="voci">
              ${passaggio.voci.map((voce) => `
                <li>
                  <span class="voce-etichetta">${esc(voce.etichetta)}</span>
                  <span class="voce-importo">${voce.importo === null ? "da definire" : euro(voce.importo)}</span>
                  ${voce.dettaglio ? `<span class="voce-nota">${esc(voce.dettaglio)}</span>` : ""}
                </li>`).join("")}
            </ul>
            <p class="durata">${esc(passaggio.durata_tipica)}</p>
          </article>`).join("")}
      </div>

      <p class="totale-spese">
        Spese e imposte stimate oltre al prezzo: <strong>${euro(calcolo.totale_spese_complessive)}</strong>
      </p>
      <p class="avvertenza">${esc(calcolo.avvertenza)}</p>
    </div>
  </section>`;
}

/* ---------- Percorso affitto ---------- */

function sezioneAffitto() {
  const calcolo = calcolaImportiAffitto(app.immobile, app.config.costi, app.config.provvigioni);

  const elenco = (voci) => `
    <ul class="voci">
      ${voci.map((v) => `
        <li>
          <span class="voce-etichetta">${esc(v.etichetta)}</span>
          <span class="voce-importo">${v.importo === null ? "da definire" : euro(v.importo)}</span>
          ${v.dettaglio ? `<span class="voce-nota">${esc(v.dettaglio)}</span>` : ""}
        </li>`).join("")}
    </ul>`;

  return `
  <section class="passaggi" data-sezione="percorso-affitto">
    <div class="container">
      <h2 class="titolo-sezione">${esc(app.config.costi.affitto.titolo)}</h2>

      <div class="passaggi-griglia">
        <article class="passaggio">
          <span class="numero">Documenti</span>
          <h3>Che cosa ti serve</h3>
          <ul class="elenco-semplice">
            ${calcolo.documenti_richiesti.map((d) => `<li>${esc(d)}</li>`).join("")}
          </ul>
        </article>

        <article class="passaggio">
          <span class="numero">Passaggio 1</span>
          <h3>Alla proposta</h3>
          ${elenco(calcolo.alla_proposta)}
          <p class="durata">Totale alla proposta: <strong>${euro(calcolo.totale_proposta)}</strong></p>
        </article>

        <article class="passaggio">
          <span class="numero">Passaggio 2</span>
          <h3>Alla firma del contratto</h3>
          ${elenco(calcolo.alla_firma)}
          <p class="durata">Totale alla firma: <strong>${euro(calcolo.totale_firma)}</strong></p>
        </article>
      </div>

      <h3 class="sotto-titolo">Come velocizzare tutto</h3>
      <ul class="punti-forza">
        ${calcolo.come_velocizzare.map((c) => `<li>${esc(c)}</li>`).join("")}
      </ul>
      <p class="avvertenza">${esc(app.config.costi.avvertenza)}</p>
    </div>
  </section>`;
}

/* ---------- Provvigioni in chiaro ---------- */

function sezioneProvvigioni() {
  const provvigione = calcolaProvvigione(app.immobile, app.config.provvigioni);
  const c = app.config.provvigioni;

  return `
  <section class="provvigioni" data-sezione="provvigioni">
    <div class="container stretto">
      <h2 class="titolo-sezione">La nostra provvigione, scritta prima</h2>
      <p class="occhiello">${esc(c.nota_trasparenza)}</p>

      <div class="riquadro-provvigione">
        <div class="riga"><span>Criterio applicato</span><strong>${esc(provvigione.criterio)}</strong></div>
        <div class="riga"><span>Imponibile</span><strong>${euro(provvigione.imponibile)}</strong></div>
        <div class="riga"><span>IVA ${(c.iva * 100).toFixed(0)}%</span><strong>${euro(provvigione.iva)}</strong></div>
        <div class="riga totale"><span>Totale</span><strong>${euro(provvigione.totale)}</strong></div>
        <p class="quando">${esc(provvigione.quando)}</p>
      </div>

      <ul class="tariffario">
        <li>${esc(c.vendita.sotto_soglia.testo)}</li>
        <li>${esc(c.vendita.sopra_soglia.testo)}</li>
        <li>${esc(c.affitto.testo)}</li>
      </ul>
    </div>
  </section>`;
}

/* ---------- Servizi ---------- */

function sezioneServizi() {
  return `
  <section class="servizi" data-sezione="servizi">
    <div class="container">
      <h2 class="titolo-sezione">Di che cosa ci occupiamo</h2>
      <div class="servizi-griglia">
        ${app.config.servizi.servizi.map((s) => `
          <article class="servizio" data-servizio="${esc(s.id)}">
            <h3>${esc(s.titolo)}</h3>
            <p>${esc(s.testo)}</p>
            <button class="link-servizio" data-chiedi="${esc(s.id)}">Voglio saperne di più</button>
          </article>`).join("")}
      </div>
    </div>
  </section>`;
}

/* ---------- Footer ---------- */

function sezioneFooter() {
  const a = app.agenzia;
  const agente = app.immobile.pubblico.agente;
  return `
  <footer data-sezione="footer">
    <div class="container footer-inner">
      <div>
        <div class="marchio">Innova <span>Immobiliare</span></div>
        <div class="payoff">${esc(a.payoff)}</div>
      </div>
      <div class="agente">
        <strong>Il tuo riferimento</strong><br>
        ${esc(agente.nome)}<br>
        ${esc(agente.telefono)} · ${esc(agente.email)}
      </div>
      <div>
        ${esc(a.indirizzo)}<br>
        ${esc(a.telefono)}<br>
        ${esc(a.email)}
      </div>
    </div>
  </footer>`;
}

/* ============================================================
   COMPORTAMENTI
   ============================================================ */

function collegaEventi() {
  const form = document.getElementById("modulo-accesso");

  // Intento preselezionato da quello rilevato all'arrivo.
  const selectIntento = document.getElementById("intento");
  if (selectIntento) {
    selectIntento.value = app.intento.intento;
    aggiornaCampiPerIntento(selectIntento.value);
    selectIntento.addEventListener("change", (e) => {
      aggiornaCampiPerIntento(e.target.value);
      traccia("intento_corretto_dal_cliente", { intento: e.target.value });
    });
  }

  form.addEventListener("submit", inviaModulo);
  osservaAbbandonoModulo(form, {
    onAbbandono: (dati) => {
      const piano = pianificaSequenza("recupero_modulo_abbandonato", contestoComunicazioni(dati), app.config.comunicazioni);
      console.info("[Innova] Recupero modulo abbandonato — messaggi programmati:", piano);
    }
  });

  document.querySelectorAll("[data-foto]").forEach((a) =>
    a.addEventListener("click", () => traccia("foto_aperta", { indice: a.dataset.foto }))
  );

  document.querySelectorAll("[data-video]").forEach((f) =>
    f.addEventListener("click", () => traccia("video_avviato", { video: f.dataset.video, titolo: f.dataset.titolo }))
  );

  document.querySelectorAll("[data-chiedi]").forEach((b) =>
    b.addEventListener("click", () => {
      traccia("servizio_richiesto", { servizio: b.dataset.chiedi });
      b.textContent = "Richiesta registrata: ti ricontattiamo noi ✓";
      b.disabled = true;
    })
  );

  const btnTour = document.getElementById("btn-tour");
  if (btnTour) btnTour.addEventListener("click", () => {
    const tour = app.immobile.pubblico.media.tour_virtuale;
    traccia("tour_virtuale_avviato", { fornitore: tour.fornitore });
    if (tour.url) window.open(tour.url, "_blank", "noopener");
  });

  const btnVisore = document.getElementById("btn-visore");
  if (btnVisore) btnVisore.addEventListener("click", () => {
    traccia("visore_richiesto", {});
    if (!app.valutazione?.prenotazione_sbloccata) {
      document.getElementById("accesso").scrollIntoView({ behavior: "smooth" });
      lampeggia(document.getElementById("modulo-accesso"));
    } else {
      document.getElementById("area-esito").scrollIntoView({ behavior: "smooth" });
    }
  });
}

/** Affitto, vendita e valutazione non chiedono le stesse cose. */
function aggiornaCampiPerIntento(intento) {
  const affitto = intento === "affittuario";
  const venditore = intento === "venditore";

  // A chi cerca in affitto non si chiede come finanzierà un acquisto:
  // la domanda giusta è quanto entra ogni mese.
  document.getElementById("campo-reddito").classList.toggle("nascosto", !affitto);
  document.getElementById("campo-budget").classList.toggle("nascosto", venditore || affitto);
  document.getElementById("modalita_acquisto")
    .closest(".campo")
    .classList.toggle("nascosto", venditore || affitto);
}

function lampeggia(elemento) {
  elemento.classList.add("lampeggia");
  setTimeout(() => elemento.classList.remove("lampeggia"), 1200);
}

/* ---------- Invio del modulo ---------- */

async function inviaModulo(evento) {
  evento.preventDefault();
  const form = evento.currentTarget;
  const errore = document.getElementById("errore-modulo");
  errore.hidden = true;

  const risposte = Object.fromEntries(new FormData(form).entries());
  risposte.consenso_privacy = form.consenso_privacy.checked;
  risposte.consenso_marketing = form.consenso_marketing.checked;

  const mancanti = [];
  if (!risposte.nome) mancanti.push("nome");
  if (!risposte.telefono) mancanti.push("telefono");
  if (!risposte.email) mancanti.push("email");
  if (!risposte.intento) mancanti.push("cosa stai cercando");
  if (!risposte.consenso_privacy) mancanti.push("consenso privacy");
  if (mancanti.length) {
    errore.textContent = `Manca ancora: ${mancanti.join(", ")}.`;
    errore.hidden = false;
    return;
  }

  app.contatto = { nome: risposte.nome, telefono: risposte.telefono, email: risposte.email };
  attivaConsenso(app.contatto);
  traccia("modulo_inviato", { intento: risposte.intento });

  // Il semaforo: qui, in produzione, si chiama il server.
  app.valutazione = valutaSemaforo(risposte, app.immobile, app.config.regole);
  traccia("semaforo_valutato", {
    esito: app.valutazione.esito,
    regola: app.valutazione.regola_applicata
  });

  // Le sequenze di comunicazione che partono da questo invio.
  const nomi = sequenzePerContatto({
    intento: risposte.intento,
    esitoSemaforo: app.valutazione.esito,
    moduloInviato: true
  });
  app.piano = nomi.flatMap((nome) =>
    pianificaSequenza(nome, contestoComunicazioni(risposte), app.config.comunicazioni)
  );
  console.info("[Innova] Comunicazioni programmate:", app.piano);

  form.querySelector("button[type=submit]").textContent = "Accesso ottenuto ✓";
  form.querySelector("button[type=submit]").disabled = true;

  await mostraEsito(risposte);
}

function contestoComunicazioni(risposte) {
  const p = app.immobile.pubblico;
  return {
    contatto: app.contatto || { nome: risposte.nome || "", telefono: risposte.telefono || "", email: risposte.email || "" },
    immobile: {
      titolo: p.titolo,
      zona: p.zona,
      prezzo: app.immobile.tipo_operazione === "vendita" ? euro(p.prezzo) : `${euro(p.canone_mensile)}/mese`,
      punti_di_forza: (p.punti_di_forza || []).slice(0, 2).join(" e ")
    },
    agente: p.agente,
    risposte,
    semaforo: app.valutazione || {},
    sla: 24,
    link: {
      prenotazione: `${location.origin}${location.pathname}?immobile=${app.immobile.id}#area-esito`,
      modulo_precompilato: `${location.origin}${location.pathname}?immobile=${app.immobile.id}#accesso`,
      tour: app.immobile.pubblico.media?.tour_virtuale?.url || "",
      riprogramma: "",
      mappa: `https://maps.google.com/?q=${encodeURIComponent(p.indirizzo || p.zona)}`,
      calendario: "",
      esito_consulente: "",
      caso_studio: "",
      prenotazione_valutazione: ""
    }
  };
}

/* ---------- Esito del semaforo e prenotazione ---------- */

async function mostraEsito(risposte) {
  const area = document.getElementById("area-esito");
  const v = app.valutazione;

  area.innerHTML = `
  <section class="esito" data-sezione="esito-semaforo" style="--colore-esito:${esc(v.colore)}">
    <div class="container stretto">
      <span class="pallino"></span>
      <h2 class="titolo-sezione">${esc(v.etichetta)}</h2>
      <p class="messaggio">${esc(v.messaggio_cliente)}</p>
      <div id="area-prenotazione"></div>
      <div class="revisione-umana">
        <p>${esc(v.revisione_umana.testo)}</p>
        <a class="btn btn-secondario" href="tel:${esc(app.agenzia.telefono.replace(/\s/g, ""))}">Parla con una persona</a>
      </div>
      <details class="dietro-le-quinte">
        <summary>Che cosa è successo dietro le quinte (visibile solo in demo)</summary>
        <p><strong>Regola applicata:</strong> ${esc(v.regola_applicata)}</p>
        <p><strong>Motivazione:</strong> ${esc(v.motivazione)}</p>
        <p><strong>Azioni scatenate:</strong> ${esc(v.azioni.join(", "))}</p>
        <p><strong>Comunicazioni programmate:</strong></p>
        <ul>${app.piano.map((m) =>
          `<li>${esc(m.id)} → ${esc(m.destinatario)} via ${esc(m.canale)}, il ${new Date(m.invio_previsto).toLocaleString("it-IT")}</li>`
        ).join("")}</ul>
      </details>
    </div>
  </section>`;

  area.scrollIntoView({ behavior: "smooth", block: "start" });

  if (v.prenotazione_sbloccata) {
    await disegnaPrenotazione(risposte);
  } else {
    document.getElementById("area-prenotazione").innerHTML = `
      <div class="in-attesa">
        <p><strong>Prenotazione in attesa di verifica.</strong> Appena il consulente conferma, ricevi il link per scegliere il giorno.</p>
        <p class="micro">Nel frattempo il tour virtuale resta a tua disposizione.</p>
      </div>`;
  }
}

async function disegnaPrenotazione(risposte) {
  const configPren = app.agenzia.prenotazione;
  const occupati = await caricaOccupati({ finti: true });
  const slot = generaSlot(configPren, occupati, { massimo: 9 });
  const luoghi = luoghiDisponibili(configPren, {
    prequalificato: app.valutazione.prenotazione_sbloccata,
    immobile: app.immobile
  });

  document.getElementById("area-prenotazione").innerHTML = `
    <div class="prenotazione">
      <h3>Scegli quando</h3>
      <div class="campo">
        <label for="luogo">Dove</label>
        <select id="luogo">
          ${luoghi.map((l) => `<option value="${esc(l.id)}">${esc(l.etichetta)}</option>`).join("")}
        </select>
      </div>
      <div class="slot-griglia">
        ${slot.map((s) => `<button class="slot" data-inizio="${esc(s.inizio)}" data-fine="${esc(s.fine)}">${esc(s.etichetta)}</button>`).join("")}
      </div>
      <p class="micro">Gli orari già occupati non compaiono: quello che vedi è libero adesso.</p>
      <div id="conferma-prenotazione"></div>
    </div>`;

  document.querySelectorAll(".slot").forEach((bottone) =>
    bottone.addEventListener("click", () => confermaSlot(bottone, luoghi, risposte))
  );
}

function confermaSlot(bottone, luoghi, risposte) {
  const luogoId = document.getElementById("luogo").value;
  const luogo = luoghi.find((l) => l.id === luogoId);
  const slot = {
    inizio: bottone.dataset.inizio,
    fine: bottone.dataset.fine,
    etichetta: bottone.textContent
  };

  const evento = preparaEventoCalendario({
    slot,
    luogo,
    contatto: app.contatto,
    immobile: app.immobile,
    agenzia: app.agenzia
  });

  traccia("prenotazione_confermata", { slot: slot.inizio, luogo: luogoId });

  /* `data_ora` è la data ISO su cui l'orchestratore calcola gli offset
     (il promemoria a -24h); `etichetta` è la forma leggibile che finisce
     nei messaggi. Confonderle significa programmare invii a date inesistenti. */
  const piano = pianificaSequenza(
    "appuntamento",
    {
      ...contestoComunicazioni(risposte),
      prenotazione: { data_ora: slot.inizio, etichetta: slot.etichetta, luogo: luogo.etichetta }
    },
    app.config.comunicazioni
  );
  console.info("[Innova] Evento per Google Calendar:", evento);
  console.info("[Innova] Sequenza appuntamento:", piano);

  document.querySelectorAll(".slot").forEach((b) => (b.disabled = true));
  bottone.classList.add("scelto");

  const ics = generaIcs(evento);
  const url = URL.createObjectURL(new Blob([ics], { type: "text/calendar" }));

  document.getElementById("conferma-prenotazione").innerHTML = `
    <div class="confermato">
      <h4>È fatta: ${esc(slot.etichetta)}</h4>
      <p>${esc(luogo.etichetta)} — ${esc(evento.location)}</p>
      <p>Ti arriva subito la conferma su WhatsApp ed email, con il promemoria il giorno prima.</p>
      <a class="btn btn-secondario" href="${url}" download="visita-innova.ics">Aggiungi al calendario</a>
      <p class="micro">In demo l'evento non viene creato davvero su Google Calendar: lo trovi stampato nella console del browser, pronto per l'API.</p>
    </div>`;
}

/* Comodo in fase di collaudo: innova.riepilogo() dalla console. */
if (typeof window !== "undefined") {
  window.innova = {
    stato: app,
    riepilogo: riepilogoComportamento,
    piano: () => app.piano
  };
}
